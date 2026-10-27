"""Geocodificação controlada e retomável do lote piloto GEO_001."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_POINTS = ROOT.parent / "mapa_historico_pontos.csv"
SOURCE_ADDRESS = ROOT.parent / "dim_endereco_mapa.csv"
AUDIT_DIR = ROOT / "data" / "geocodificacao"
MANIFEST = AUDIT_DIR / "manifesto_geo_lote_001.json"
CACHE = AUDIT_DIR / "cache_geocodificacao.json"
AUDIT = AUDIT_DIR / "geocodificacao_lote_001.csv"
STATS = AUDIT_DIR / "estatisticas_lote_001.json"
QUALITY_STATS = AUDIT_DIR / "qualidade_origem_lote_001.csv"
CITY_STATS = AUDIT_DIR / "municipios_lote_001.csv"

LOT_ID = "GEO_001"
LOT_SIZE = 100
PROVIDER = "Nominatim / OpenStreetMap"
ENDPOINT = "https://nominatim.openstreetmap.org/search"
RULE_VERSION = "geografica-2.0-lote-piloto"
USER_AGENT = "SafeFlowMap-Sprint04/1.0 controlled-pilot"
REQUEST_INTERVAL_SECONDS = 1.05

AUDIT_FIELDS = [
    "ID_LOTE", "ID_ENDERECO", "ENDERECO_ENVIADO", "CONSULTA_UTILIZADA",
    "DATA_HORA_UTC", "PROVEDOR", "STATUS_HTTP", "NUMERO_TENTATIVA",
    "CACHE_HIT", "LATITUDE_RETORNADA", "LONGITUDE_RETORNADA",
    "ENDERECO_RETORNADO", "LOGRADOURO_RETORNADO", "NUMERO_RETORNADO",
    "BAIRRO_RETORNADO", "MUNICIPIO_ESPERADO", "MUNICIPIO_RETORNADO",
    "UF_ESPERADA", "UF_RETORNADA", "CEP_ORIGINAL", "CEP_NORMALIZADO",
    "CEP_RETORNADO", "REGRA_CEP_APLICADA", "ZERO_INICIAL_RECOMPOSTO",
    "QUALIDADE_ENDERECO_ORIGEM", "ENDERECO_SEM_NUMERO", "TIPO_RESULTADO",
    "OSM_TYPE", "OSM_ID", "COORDENADAS_VALIDAS", "MUNICIPIO_COMPATIVEL",
    "UF_COMPATIVEL", "LOGRADOURO_COMPATIVEL", "NUMERO_COMPATIVEL",
    "CLASSIFICACAO", "PUBLICAR", "MOTIVO_CLASSIFICACAO", "ERRO",
    "RESPOSTA_ORIGINAL_JSON", "CHAVE_CACHE", "VERSAO_REGRA_GEOGRAFICA",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize(value: str | None) -> str:
    text = unicodedata.normalize("NFD", value or "")
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return re.sub(r"[^A-Z0-9]+", " ", text.upper()).strip()


def digits(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def valid_coordinate(latitude: object, longitude: object) -> bool:
    try:
        lat, lon = float(latitude), float(longitude)
        return math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180
    except (TypeError, ValueError):
        return False


def address_city(address: dict) -> str:
    for key in ("city", "town", "village", "municipality", "city_district"):
        if address.get(key):
            return str(address[key])
    return ""


def state_code(address: dict) -> str:
    iso = str(address.get("ISO3166-2-lvl4", ""))
    if iso.upper().endswith("-SP"):
        return "SP"
    return "SP" if normalize(address.get("state")) == "SAO PAULO" else iso


def road_name(address: dict) -> str:
    for key in ("road", "pedestrian", "residential", "path", "place"):
        if address.get(key):
            return str(address[key])
    return ""


def compatible_text(expected: str, returned: str, threshold: float = 0.78) -> bool:
    left, right = normalize(expected), normalize(returned)
    if not left or not right:
        return False
    if left == right or left in right or right in left:
        return True
    return SequenceMatcher(None, left, right).ratio() >= threshold


def build_query(row: dict[str, str]) -> str:
    parts = []
    if normalize(row["LOGRADOURO"]) not in {"", "-"}:
        street = row["LOGRADOURO"]
        if normalize(row["NUMERO"]) not in {"", "S N", "SN"}:
            street += f", {row['NUMERO']}"
        parts.append(street)
    if row["BAIRRO"]:
        parts.append(row["BAIRRO"])
    parts.extend([row["MUNICIPIO"], "SP"])
    if row["CEP"]:
        parts.append(row["CEP"])
    parts.append("Brasil")
    return ", ".join(part for part in parts if part)


def cache_key(row: dict[str, str], query: str) -> str:
    payload = "|".join([normalize(query), normalize(row["MUNICIPIO"]), row["UF"], row["VERSAO_NORMALIZACAO"]])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_json_atomic(path: Path, payload: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_sources() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    with SOURCE_POINTS.open("r", encoding="utf-8-sig", newline="") as stream:
        points = list(csv.DictReader(stream))
    with SOURCE_ADDRESS.open("r", encoding="utf-8-sig", newline="") as stream:
        addresses = {row["ID_ENDERECO"]: row for row in csv.DictReader(stream)}
    return points, addresses


def select_lot(points: list[dict[str, str]], addresses: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    eligible = sorted(
        (row for row in points if row["STATUS_GEOCODIFICACAO"] == "PENDENTE"),
        key=lambda row: row["ID_ENDERECO"],
    )[:LOT_SIZE]
    if len(eligible) != LOT_SIZE:
        raise RuntimeError(f"Esperados {LOT_SIZE} pendentes; encontrados {len(eligible)}")
    return [{**row, **addresses[row["ID_ENDERECO"]]} for row in eligible]


def create_or_validate_manifest(selected: list[dict[str, str]]) -> dict:
    ids = [row["ID_ENDERECO"] for row in selected]
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if manifest["ids_selecionados"] != ids:
            raise RuntimeError("A seleção atual diverge do manifesto imutável de GEO_001")
        return manifest
    manifest = {
        "id_lote": LOT_ID,
        "data_criacao_utc": now_utc(),
        "versao": "1.0",
        "quantidade_solicitada": LOT_SIZE,
        "quantidade_selecionada": len(ids),
        "ids_selecionados": ids,
        "hash_fonte_mapa_historico_pontos_sha256": sha256(SOURCE_POINTS),
        "hash_fonte_dim_endereco_sha256": sha256(SOURCE_ADDRESS),
        "regra_selecao": "STATUS_GEOCODIFICACAO=PENDENTE; ordenar ID_ENDERECO crescente; primeiros 100",
        "provedor": PROVIDER,
        "endpoint": ENDPOINT,
        "politica_operacional": "Uma thread; no máximo uma consulta por segundo; User-Agent identificado; cache persistente; sem reprocessar além dos 100 IDs.",
        "versao_regra_geografica": RULE_VERSION,
        "status_processamento": "SELECIONADO",
    }
    write_json_atomic(MANIFEST, manifest)
    return manifest


def request_provider(query: str) -> tuple[int, list[dict]]:
    params = urllib.parse.urlencode({
        "format": "jsonv2", "addressdetails": 1, "limit": 5,
        "countrycodes": "br", "dedupe": 1, "q": query,
    })
    request = urllib.request.Request(
        f"{ENDPOINT}?{params}",
        headers={"User-Agent": USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"},
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def choose_candidate(candidates: list[dict], row: dict[str, str]) -> tuple[dict | None, str]:
    valid = [item for item in candidates if valid_coordinate(item.get("lat"), item.get("lon"))]
    if not valid:
        return None, "SEM_COORDENADAS_VALIDAS"
    expected_city = row["MUNICIPIO"]
    sp = [item for item in valid if state_code(item.get("address", {})) == "SP"]
    if not sp:
        return valid[0], "UF_INCOMPATIVEL"
    same_city = [item for item in sp if compatible_text(expected_city, address_city(item.get("address", {})), 0.9)]
    if not same_city:
        return sp[0], "MUNICIPIO_INCOMPATIVEL"

    def score(item: dict) -> float:
        address = item.get("address", {})
        points = 0.0
        points += 40 if compatible_text(row["LOGRADOURO"], road_name(address)) else 0
        points += 30 if digits(row["NUMERO"]) and digits(row["NUMERO"]) == digits(address.get("house_number")) else 0
        points += 10 if digits(row["CEP"]) and digits(row["CEP"]) == digits(address.get("postcode")) else 0
        points += 5 if compatible_text(row["BAIRRO"], str(address.get("suburb") or address.get("quarter") or ""), 0.7) else 0
        points += float(item.get("importance") or 0)
        return points

    return max(same_city, key=score), "COMPATIVEL"


def classify(row: dict[str, str], candidates: list[dict]) -> dict[str, str]:
    candidate, precheck = choose_candidate(candidates, row)
    if candidate is None:
        return {"CLASSIFICACAO": "NAO_ENCONTRADO", "PUBLICAR": "false", "MOTIVO_CLASSIFICACAO": precheck}
    address = candidate.get("address", {})
    city_ok = compatible_text(row["MUNICIPIO"], address_city(address), 0.9)
    uf_ok = state_code(address) == "SP"
    input_road = normalize(row["LOGRADOURO"])
    road_ok = input_road not in {"", "-"} and compatible_text(row["LOGRADOURO"], road_name(address))
    without_number = normalize(row["NUMERO"]) in {"", "S N", "SN"}
    returned_number = str(address.get("house_number", ""))
    number_ok = bool(digits(row["NUMERO"])) and digits(row["NUMERO"]) == digits(returned_number)
    if precheck == "UF_INCOMPATIVEL" or not uf_ok:
        classification, publish, reason = "REJEITADO_UF", "false", "UF retornada incompatível com SP"
    elif precheck == "MUNICIPIO_INCOMPATIVEL" or not city_ok:
        classification, publish, reason = "REJEITADO_MUNICIPIO", "false", "Município retornado incompatível"
    elif input_road in {"", "-"}:
        classification, publish, reason = "REVISAO_MANUAL", "false", "Logradouro de origem ausente ou inválido"
    elif road_ok and number_ok and not without_number:
        classification, publish, reason = "A", "true", "Município, UF, logradouro e número compatíveis"
    elif road_ok and (without_number or not returned_number):
        classification, publish, reason = "B", "false", "Município/UF/logradouro compatíveis, sem precisão de número"
    elif road_ok:
        classification, publish, reason = "REVISAO_MANUAL", "false", "Número retornado divergente"
    else:
        classification, publish, reason = "REVISAO_MANUAL", "false", "Município/UF compatíveis, logradouro ambíguo"
    return {
        "CLASSIFICACAO": classification, "PUBLICAR": publish,
        "MOTIVO_CLASSIFICACAO": reason,
        "COORDENADAS_VALIDAS": bool_text(valid_coordinate(candidate.get("lat"), candidate.get("lon"))),
        "MUNICIPIO_COMPATIVEL": bool_text(city_ok), "UF_COMPATIVEL": bool_text(uf_ok),
        "LOGRADOURO_COMPATIVEL": bool_text(road_ok), "NUMERO_COMPATIVEL": bool_text(number_ok),
        "LATITUDE_RETORNADA": str(candidate.get("lat", "")), "LONGITUDE_RETORNADA": str(candidate.get("lon", "")),
        "ENDERECO_RETORNADO": str(candidate.get("display_name", "")), "LOGRADOURO_RETORNADO": road_name(address),
        "NUMERO_RETORNADO": returned_number, "BAIRRO_RETORNADO": str(address.get("suburb") or address.get("quarter") or ""),
        "MUNICIPIO_RETORNADO": address_city(address), "UF_RETORNADA": state_code(address),
        "CEP_RETORNADO": str(address.get("postcode", "")), "TIPO_RESULTADO": str(candidate.get("addresstype") or candidate.get("type") or ""),
        "OSM_TYPE": str(candidate.get("osm_type", "")), "OSM_ID": str(candidate.get("osm_id", "")),
    }


def base_audit_row(row: dict[str, str], query: str, key: str) -> dict[str, str]:
    without_number = normalize(row["NUMERO"]) in {"", "S N", "SN"}
    return {
        "ID_LOTE": LOT_ID, "ID_ENDERECO": row["ID_ENDERECO"], "ENDERECO_ENVIADO": row["ENDERECO_NORMALIZADO"],
        "CONSULTA_UTILIZADA": query, "DATA_HORA_UTC": now_utc(), "PROVEDOR": PROVIDER,
        "NUMERO_TENTATIVA": "1", "MUNICIPIO_ESPERADO": row["MUNICIPIO"], "UF_ESPERADA": row["UF"],
        "CEP_ORIGINAL": row["CEP_ORIGINAL"], "CEP_NORMALIZADO": row["CEP"], "REGRA_CEP_APLICADA": row["REGRA_CEP_APLICADA"],
        "ZERO_INICIAL_RECOMPOSTO": bool_text(row["REGRA_CEP_APLICADA"] == "ZERO_INICIAL_RECOMPOSTO"),
        "QUALIDADE_ENDERECO_ORIGEM": row["QUALIDADE_ENDERECO"], "ENDERECO_SEM_NUMERO": bool_text(without_number),
        "CHAVE_CACHE": key, "VERSAO_REGRA_GEOGRAFICA": RULE_VERSION,
    }


def append_audit(row: dict[str, str]) -> None:
    exists = AUDIT.exists()
    with AUDIT.open("a", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=AUDIT_FIELDS, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in AUDIT_FIELDS})


def summarize(manifest: dict) -> None:
    with AUDIT.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    counts = Counter(row["CLASSIFICACAO"] for row in rows)
    processed = len(rows)
    stats = {
        "id_lote": LOT_ID, "selecionados": LOT_SIZE, "processados": processed,
        "encontrados": sum(counts[key] for key in ("A", "B", "REVISAO_MANUAL", "REJEITADO_MUNICIPIO", "REJEITADO_UF")),
        "classe_a": counts["A"], "classe_b": counts["B"], "revisao_manual": counts["REVISAO_MANUAL"],
        "rejeitados_municipio": counts["REJEITADO_MUNICIPIO"], "rejeitados_uf": counts["REJEITADO_UF"],
        "nao_encontrados": counts["NAO_ENCONTRADO"], "erros_servico": counts["ERRO_SERVICO"],
        "consultas_reais": sum(row["CACHE_HIT"] != "true" for row in rows), "cache_hits": sum(row["CACHE_HIT"] == "true" for row in rows),
        "taxas_percentuais": {key.lower(): round(value / processed * 100, 2) if processed else 0 for key, value in counts.items()},
        "finalizado_em_utc": now_utc(),
    }
    write_json_atomic(STATS, stats)

    def grouped(field: str) -> list[dict]:
        groups: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            groups[row[field]].append(row)
        output = []
        for key in sorted(groups):
            group = groups[key]
            counter = Counter(item["CLASSIFICACAO"] for item in group)
            output.append({field: key, "PROCESSADOS": len(group), "CLASSE_A": counter["A"], "CLASSE_B": counter["B"], "REVISAO_MANUAL": counter["REVISAO_MANUAL"], "REJEITADOS": counter["REJEITADO_MUNICIPIO"] + counter["REJEITADO_UF"], "NAO_ENCONTRADOS": counter["NAO_ENCONTRADO"], "ERROS_SERVICO": counter["ERRO_SERVICO"], "OUTROS": len(group) - counter["A"]})
        return output

    for path, field in ((QUALITY_STATS, "QUALIDADE_ENDERECO_ORIGEM"), (CITY_STATS, "MUNICIPIO_ESPERADO")):
        data = grouped(field)
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data[0]))
            writer.writeheader(); writer.writerows(data)

    manifest.update({"status_processamento": "CONCLUIDO" if processed == LOT_SIZE else "PARCIAL", "quantidade_processada": processed, "estatisticas": STATS.name})
    write_json_atomic(MANIFEST, manifest)


def main() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    points, addresses = load_sources()
    selected = select_lot(points, addresses)
    manifest = create_or_validate_manifest(selected)
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    completed: set[str] = set()
    if AUDIT.exists():
        with AUDIT.open("r", encoding="utf-8-sig", newline="") as stream:
            completed = {row["ID_ENDERECO"] for row in csv.DictReader(stream)}

    for index, row in enumerate(selected, start=1):
        if row["ID_ENDERECO"] in completed:
            continue
        query = build_query(row)
        key = cache_key(row, query)
        audit_row = base_audit_row(row, query, key)
        started = time.monotonic()
        try:
            if key in cache:
                payload = cache[key]
                audit_row["CACHE_HIT"] = "true"
            else:
                status, candidates = request_provider(query)
                payload = {"status_http": status, "response": candidates, "captured_at_utc": now_utc(), "query": query, "provider": PROVIDER}
                cache[key] = payload
                write_json_atomic(CACHE, cache)
                audit_row["CACHE_HIT"] = "false"
            audit_row["STATUS_HTTP"] = str(payload["status_http"])
            candidates = payload["response"]
            audit_row.update(classify(row, candidates))
            audit_row["RESPOSTA_ORIGINAL_JSON"] = json.dumps(candidates, ensure_ascii=False, separators=(",", ":"))
        except urllib.error.HTTPError as error:
            audit_row.update({"STATUS_HTTP": str(error.code), "CACHE_HIT": "false", "CLASSIFICACAO": "ERRO_SERVICO", "PUBLICAR": "false", "MOTIVO_CLASSIFICACAO": "Falha HTTP do provedor", "ERRO": repr(error), "RESPOSTA_ORIGINAL_JSON": ""})
        except Exception as error:  # Falha técnica nunca vira não encontrado.
            audit_row.update({"STATUS_HTTP": "", "CACHE_HIT": "false", "CLASSIFICACAO": "ERRO_SERVICO", "PUBLICAR": "false", "MOTIVO_CLASSIFICACAO": "Falha técnica do provedor", "ERRO": repr(error), "RESPOSTA_ORIGINAL_JSON": ""})
        append_audit(audit_row)
        elapsed = time.monotonic() - started
        if audit_row.get("CACHE_HIT") != "true":
            time.sleep(max(0.0, REQUEST_INTERVAL_SECONDS - elapsed))
        if index % 10 == 0 or index == LOT_SIZE:
            print(f"GEO_001: {index}/{LOT_SIZE} candidatos concluídos", flush=True)

    summarize(manifest)


if __name__ == "__main__":
    main()
