import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GEO = ROOT / "data" / "geografia"


def main():
    with (GEO / "sede_para_locais.csv").open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))

    lookup = {}
    municipios = Counter()
    for row in rows:
        lookup[row["ID_ENDERECO"]] = {
            "id_relacao": row["ID_RELACAO"],
            "distancia_reta_km": float(row["DISTANCIA_RETA_KM"]),
            "distancia_rodoviaria_km": float(row["DISTANCIA_RODOVIARIA_KM"]),
            "tempo_estimado_min": float(row["TEMPO_ESTIMADO_MIN"]),
            "provedor": row["PROVEDOR"],
            "perfil": row["PERFIL"],
            "tipo_tempo": row["TIPO_TEMPO"],
            "data_calculo_utc": row["DATA_CALCULO_UTC"],
            "status": row["STATUS"],
            "qa_status": row["QA_STATUS"],
        }
        municipios[row["MUNICIPIO"]] += 1

    output = {
        "metadata": {
            "origem": "SEDE_001",
            "provedor": "TOMTOM_ROUTING_API",
            "perfil": "CARRO",
            "tipo_tempo": "NO_TRAFFIC_TRAVEL_TIME_CURRENT_GRAPH",
            "total_relacoes": len(lookup),
            "aviso": "Estimativas atuais do provedor; não representam deslocamentos históricos realizados.",
        },
        "por_id_endereco": lookup,
    }
    target = ROOT / "data" / "sede_para_locais.json"
    target.write_text(json.dumps(output, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    coverage = {
        "total_municipios": len(municipios),
        "total_relacoes": sum(municipios.values()),
        "por_municipio": dict(sorted(municipios.items())),
    }
    (GEO / "cobertura_municipios.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({"arquivo": str(target), "relacoes": len(lookup), "municipios": len(municipios)}))


if __name__ == "__main__":
    main()
