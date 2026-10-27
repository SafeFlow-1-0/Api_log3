from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GEO = DATA / "geografia"
POINTS = DATA / "pontos_classe_a.geojson"
PILOT_CACHE = DATA / "sprint10_revisada" / "cache_osrm_sede_local.json"
QUEUE = GEO / "fila_roteamento_sede.csv"
PREFLIGHT = GEO / "preflight_sprint11.json"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> None:
    GEO.mkdir(parents=True, exist_ok=True)
    features = json.loads(POINTS.read_text(encoding="utf-8"))["features"]
    if len(features) != 1583:
        raise RuntimeError("Baseline inválida: esperados 1.583 pontos.")
    rows = []
    for feature in sorted(features, key=lambda x: x["properties"]["id_endereco"]):
        prop = feature["properties"]
        lon, lat = feature["geometry"]["coordinates"]
        ident = prop["id_endereco"]
        raw_key = f"SEDE_001|{ident}|TOMTOM_ROUTING|CARRO|SEM_TRANSITO_HISTORICO"
        rows.append({
            "ID_ENDERECO": ident, "LAT": lat, "LON": lon,
            "MUNICIPIO": prop.get("municipio", ""),
            "STATUS_GEO": prop.get("status_geocodificacao", ""),
            "QUALIDADE_GEO": prop.get("qualidade_geocodificacao", ""),
            "STATUS_ROTEAMENTO": "PENDENTE", "PROVEDOR": "TOMTOM_ROUTING",
            "CACHE_KEY": sha256_text(raw_key),
        })
    with QUEUE.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    key_present = bool(os.environ.get("SAFEFLOW_TOMTOM_API_KEY", "").strip())
    osrm_cache = len(json.loads(PILOT_CACHE.read_text(encoding="utf-8"))) if PILOT_CACHE.exists() else 0
    preflight = {
        "TOTAL_PONTOS": 1583,
        "CACHE_EXISTENTE_TOMTOM": 0,
        "CACHE_OSRM_PRESERVADO_NAO_REUTILIZAVEL": osrm_cache,
        "CHAMADAS_NECESSARIAS": 1583,
        "CHAVE_AMBIENTE_PRESENTE": key_present,
        "COTA_CONFIRMADA": False,
        "COTA_MINIMA_NECESSARIA": 1583,
        "QPS_OFICIAL_REFERENCIA": 5,
        "QPS_CONFIGURADO": 2,
        "INTERVALO_SEGUNDOS": 0.5,
        "RETRIES": 3,
        "BACKOFF_SEGUNDOS": [2, 5, 15],
        "RISCO_COBRANCA": "NAO_AUTORIZADO; BLOQUEADO_ATE_CONFIRMACAO_DE_COTA",
        "PROVEDOR": "TOMTOM_ROUTING_API",
        "STATUS_PREFLIGHT": "BLOQUEADO" if not key_present else "AGUARDANDO_CONFIRMACAO_DE_COTA",
        "MOTIVO": "Chave ausente no ambiente e cota atual não confirmada" if not key_present else "Cota atual não confirmada",
        "SEGREDO_PERSISTIDO": False,
    }
    PREFLIGHT.write_text(json.dumps(preflight, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(preflight, ensure_ascii=False))


if __name__ == "__main__":
    main()
