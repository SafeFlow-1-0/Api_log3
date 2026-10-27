"""Exporta somente os pontos Classe A homologados da Sprint 01 para GeoJSON.

O CSV de origem e preservado: este script apenas o le e grava novos artefatos.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "mapa_historico_pontos.csv"
FACT_SOURCE = ROOT.parent / "fact_verificacao_item_mapa.csv"
SEDE_SOURCE = ROOT.parent / "sedes_mapa.csv"
SEDE_VALIDATION = ROOT / "data" / "sede_validacao_geografica.json"
LOT_AUDIT = ROOT / "data" / "geocodificacao" / "geocodificacao_lote_001.csv"
RECOVERY_AUDIT = ROOT / "data" / "geocodificacao" / "recuperacao_geo001" / "resultado_recuperacao.csv"
OUTPUT = ROOT / "data" / "pontos_classe_a.geojson"
SEDE_OUTPUT = ROOT / "data" / "sede.geojson"
MANIFEST = ROOT / "data" / "manifesto_exportacao.json"


def split_related(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(" | ") if part.strip()]


def integer(value: str | None) -> int:
    return int(value) if value and value.strip() else 0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_feature(
    row: dict[str, str], dates: list[str], audit: dict[str, str] | None = None,
    recovery: dict[str, str] | None = None,
) -> dict:
    latitude = recovery["LATITUDE_RECUPERADA"] if recovery else (audit["LATITUDE_RETORNADA"] if audit else row["LATITUDE"])
    longitude = recovery["LONGITUDE_RECUPERADA"] if recovery else (audit["LONGITUDE_RETORNADA"] if audit else row["LONGITUDE"])
    return {
        "type": "Feature",
        "id": row["ID_ENDERECO"],
        "geometry": {
            "type": "Point",
            "coordinates": [float(longitude), float(latitude)],
        },
        "properties": {
            "id_ponto": row["ID_PONTO"],
            "id_endereco": row["ID_ENDERECO"],
            "endereco": row["ENDERECO_NORMALIZADO"],
            "municipio": row["MUNICIPIO"],
            "uf": row["UF"],
            "primeiro_registro": row["PRIMEIRO_REGISTRO"],
            "ultimo_registro": row["ULTIMO_REGISTRO"],
            "datas_historicas": dates,
            "total_datas_com_registro": integer(row["TOTAL_DATAS_COM_REGISTRO"]),
            "total_rld": integer(row["TOTAL_RLD"]),
            "total_registros_item": integer(row["TOTAL_REGISTROS_ITEM"]),
            "total_estabelecimentos_candidatos": integer(
                row["TOTAL_ESTABELECIMENTOS_CANDIDATOS"]
            ),
            "codigos_estabelecimento": split_related(row["COD_PROPR_RELACIONADOS"]),
            "estabelecimentos": split_related(row["NOMES_FANTASIA_RELACIONADOS"]),
            "fiscais": split_related(row["FISCAIS_RELACIONADOS"]),
            "motoristas": split_related(row["MOTORISTAS_RELACIONADOS"]),
            "status_geocodificacao": "ENCONTRADO_VALIDO" if (audit or recovery) else row["STATUS_GEOCODIFICACAO"],
            "qualidade_geocodificacao": "A" if (audit or recovery) else row["QUALIDADE_GEOCODIFICACAO"],
            "fonte_geocodificacao": recovery["FONTE_RECUPERACAO"] if recovery else (audit["PROVEDOR"] if audit else row["FONTE_GEOCODIFICACAO"]),
            "estrategia_geocodificacao": "RECUPERACAO_SPRINT05" if recovery else ("LOTE_PILOTO_GEO_001" if audit else row["ESTRATEGIA_GEOCODIFICACAO"]),
            "data_geocodificacao": audit["DATA_HORA_UTC"] if audit else row["DATA_GEOCODIFICACAO"],
            "versao_regra_geografica": recovery["VERSAO_REGRA"] if recovery else (audit["VERSAO_REGRA_GEOGRAFICA"] if audit else row["VERSAO_REGRA_GEOGRAFICA"]),
            "id_lote_geocodificacao": audit["ID_LOTE"] if audit else None,
            "classificacao_lote": audit["CLASSIFICACAO"] if audit else None,
            "motivo_classificacao_lote": audit["MOTIVO_CLASSIFICACAO"] if audit else None,
            "origem_validacao": recovery["ORIGEM_VALIDACAO"] if recovery else None,
            "evidencia_recuperacao": recovery["EVIDENCIA_ENDERECO"] if recovery else None,
        },
    }


def main() -> None:
    source_hash_before = sha256(SOURCE)
    fact_hash_before = sha256(FACT_SOURCE)
    sede_hash_before = sha256(SEDE_SOURCE)
    with SOURCE.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))

    baseline_eligible = [
        row
        for row in rows
        if row["STATUS_GEOCODIFICACAO"] == "ENCONTRADO_VALIDO"
        and row["QUALIDADE_GEOCODIFICACAO"] == "A"
    ]
    audit_by_id: dict[str, dict[str, str]] = {}
    if LOT_AUDIT.exists():
        with LOT_AUDIT.open("r", encoding="utf-8-sig", newline="") as stream:
            audit_by_id = {
                audit["ID_ENDERECO"]: audit
                for audit in csv.DictReader(stream)
                if audit["CLASSIFICACAO"] == "A" and audit["PUBLICAR"] == "true"
            }
    new_eligible = [
        row
        for row in rows
        if row["ID_ENDERECO"] in audit_by_id
        and row["STATUS_GEOCODIFICACAO"] == "PENDENTE"
    ]
    recovery_by_id: dict[str, dict[str, str]] = {}
    if RECOVERY_AUDIT.exists():
        with RECOVERY_AUDIT.open("r", encoding="utf-8-sig", newline="") as stream:
            recovery_by_id = {
                item["ID_ENDERECO"]: item for item in csv.DictReader(stream)
                if item["CLASSIFICACAO_APOS_RECUPERACAO"] == "A_RECUPERADO" and item["PUBLICAR"] == "true"
            }
    recovered_eligible = [
        row for row in rows
        if row["ID_ENDERECO"] in recovery_by_id
        and row["ID_ENDERECO"] not in audit_by_id
        and row["STATUS_GEOCODIFICACAO"] == "PENDENTE"
    ]
    eligible = baseline_eligible + new_eligible + recovered_eligible
    eligible_ids = {row["ID_ENDERECO"] for row in eligible}
    dates_by_address: dict[str, set[str]] = {key: set() for key in eligible_ids}
    with FACT_SOURCE.open("r", encoding="utf-8-sig", newline="") as stream:
        fact_rows = list(csv.DictReader(stream))
    for row in fact_rows:
        address_id = row.get("ID_ENDERECO", "")
        date = row.get("DATAVERIFICACAO", "").strip()
        if address_id in eligible_ids and date:
            dates_by_address[address_id].add(date)

    missing_dates = sorted(key for key, values in dates_by_address.items() if not values)
    if missing_dates:
        raise ValueError(f"Pontos Classe A sem datas históricas reais: {missing_dates}")
    collection = {
        "type": "FeatureCollection",
        "name": "SafeFlow - pontos historicos Classe A",
        "metadata": {
            "criterio": "Classe A homologada anterior + GEO_001 A + somente A_RECUPERADO da Sprint 05",
            "semantica": "Enderecos historicos consolidados; nao representam visitas, sequencia ou rotas.",
            "fonte": "mapa_historico_pontos.csv - Sprint 01",
        },
        "features": [
            build_feature(
                row,
                sorted(dates_by_address[row["ID_ENDERECO"]]),
                audit_by_id.get(row["ID_ENDERECO"]),
                recovery_by_id.get(row["ID_ENDERECO"]),
            )
            for row in eligible
        ],
    }
    OUTPUT.write_text(
        json.dumps(collection, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    validation = json.loads(SEDE_VALIDATION.read_text(encoding="utf-8"))
    with SEDE_SOURCE.open("r", encoding="utf-8-sig", newline="") as stream:
        sede_rows = list(csv.DictReader(stream))
    sede_source = next(row for row in sede_rows if row["ID_SEDE"] == "SEDE_001")
    if validation["status_sede"] != "VALIDADA":
        raise ValueError("SEDE_001 não está validada; raio deve permanecer bloqueado.")
    sede_collection = {
        "type": "FeatureCollection",
        "name": "SafeFlow - sede operacional validada",
        "features": [
            {
                "type": "Feature",
                "id": "SEDE_001",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        validation["longitude_retornada"],
                        validation["latitude_retornada"],
                    ],
                },
                "properties": {
                    "id_sede": "SEDE_001",
                    "nome": validation["nome"],
                    "logradouro": sede_source["LOGRADOURO"],
                    "numero": sede_source["NUMERO"],
                    "bairro": sede_source["BAIRRO"],
                    "municipio": sede_source["MUNICIPIO"],
                    "uf": sede_source["UF"],
                    "referencia": "Referência operacional fixa do mapa",
                    "status_sede": validation["status_sede"],
                    "provedor": validation["provedor"],
                    "precisao": validation["precisao"],
                    "data_consulta": validation["data_consulta"],
                },
            }
        ],
    }
    SEDE_OUTPUT.write_text(
        json.dumps(sede_collection, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    source_hash_after = sha256(SOURCE)
    fact_hash_after = sha256(FACT_SOURCE)
    sede_hash_after = sha256(SEDE_SOURCE)
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(SOURCE),
        "source_sha256_before": source_hash_before,
        "source_sha256_after": source_hash_after,
        "source_unchanged": source_hash_before == source_hash_after,
        "fact_source": str(FACT_SOURCE),
        "fact_sha256_before": fact_hash_before,
        "fact_sha256_after": fact_hash_after,
        "fact_source_unchanged": fact_hash_before == fact_hash_after,
        "sede_source": str(SEDE_SOURCE),
        "sede_sha256_before": sede_hash_before,
        "sede_sha256_after": sede_hash_after,
        "sede_source_unchanged": sede_hash_before == sede_hash_after,
        "source_rows": len(rows),
        "exported_features": len(eligible),
        "baseline_class_a_features": len(baseline_eligible),
        "new_class_a_features_geo_001": len(new_eligible),
        "recovered_class_a_features_sprint05": len(recovered_eligible),
        "features_with_real_dates": sum(bool(values) for values in dates_by_address.values()),
        "sede_status": validation["status_sede"],
        "sede_provider": validation["provedor"],
        "eligibility_rule": {
            "STATUS_GEOCODIFICACAO": "ENCONTRADO_VALIDO",
            "QUALIDADE_GEOCODIFICACAO": "A",
        },
    }
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
