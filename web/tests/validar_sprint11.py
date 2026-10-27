import csv
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT.parent / "safeflow-sprint10-baseline"
GEO = ROOT / "data" / "geografia"
results = []


def check(name, condition):
    results.append((name, bool(condition)))


with (ROOT / "data/pontos_classe_a.geojson").open(encoding="utf-8") as f:
    points = json.load(f)["features"]
with (ROOT / "data/sede.geojson").open(encoding="utf-8") as f:
    sede = json.load(f)["features"][0]
with (ROOT / "data/sede_para_locais.json").open(encoding="utf-8") as f:
    integration = json.load(f)
with (GEO / "sede_para_locais.csv").open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
with (GEO / "fila_roteamento_sede.csv").open(encoding="utf-8-sig", newline="") as f:
    queue = list(csv.DictReader(f))

point_ids = [x["properties"]["id_endereco"] for x in points]
row_ids = [x["ID_ENDERECO"] for x in rows]
relation_ids = [x["ID_RELACAO"] for x in rows]
distances = [float(x["DISTANCIA_RODOVIARIA_KM"]) for x in rows]
straight = [float(x["DISTANCIA_RETA_KM"]) for x in rows]
times = [float(x["TEMPO_ESTIMADO_MIN"]) for x in rows]
js = (ROOT / "js/map.js").read_text(encoding="utf-8")
html = (ROOT / "index.html").read_text(encoding="utf-8")
all_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in [ROOT / "index.html", ROOT / "js/map.js", ROOT / "data/sede_para_locais.json", GEO / "sede_para_locais.csv"])

# Baseline e integridade
check("01_total_pontos_1583", len(points) == 1583)
check("02_ids_pontos_unicos", len(set(point_ids)) == 1583)
check("03_todos_classe_a", all(x["properties"].get("qualidade_geocodificacao") == "A" for x in points))
check("04_status_geo_valido", all(x["properties"].get("status_geocodificacao") == "ENCONTRADO_VALIDO" for x in points))
check("05_sede_preservada", sede["properties"].get("id_sede") == "SEDE_001")
check("06_coordenadas_sede", sede["geometry"]["coordinates"] == [-45.8808507, -23.1800797])
check("07_baseline_existe", BASELINE.joinpath("index.html").exists())
check("08_geojson_baseline_igual", BASELINE.joinpath("data/pontos_classe_a.geojson").read_bytes() == ROOT.joinpath("data/pontos_classe_a.geojson").read_bytes())
check("09_sede_baseline_igual", BASELINE.joinpath("data/sede.geojson").read_bytes() == ROOT.joinpath("data/sede.geojson").read_bytes())
check("10_filtros_preservados", all(x in html for x in ["filter-fiscal", "filter-motorista", "filter-municipio", "filter-data-inicial", "filter-raio", "filter-busca"]))

# Fila, relações e rastreabilidade
check("11_fila_1583", len(queue) == 1583)
check("12_fila_ordenada", [x["ID_ENDERECO"] for x in queue] == sorted(x["ID_ENDERECO"] for x in queue))
check("13_resultado_1583", len(rows) == 1583)
check("14_ids_resultado_unicos", len(set(row_ids)) == 1583)
check("15_relacoes_unicas", len(set(relation_ids)) == 1583)
check("16_ids_reconciliados", set(row_ids) == set(point_ids))
check("17_origem_sede_001", all(x["ID_ORIGEM"] == "SEDE_001" for x in rows))
check("18_id_relacao_deterministico", all(x["ID_RELACAO"] == f"SEDE_001__{x['ID_ENDERECO']}" for x in rows))
check("19_nenhuma_relacao_local_local", all(x["ID_ORIGEM"].startswith("SEDE_") and x["ID_ENDERECO"].startswith("END_") for x in rows))
check("20_perfil_carro", all(x["PERFIL"] == "CARRO" for x in rows))
check("21_provedor_tomtom", all(x["PROVEDOR"] == "TOMTOM_ROUTING_API" for x in rows))
check("22_tipo_tempo_documentado", all(x["TIPO_TEMPO"] == "NO_TRAFFIC_TRAVEL_TIME_CURRENT_GRAPH" for x in rows))
check("23_status_calculado", all(x["STATUS"] == "CALCULADO" for x in rows))
check("24_sem_erros", all(not x["ERRO"] for x in rows))
check("25_cache_keys_preenchidas", all(len(x["CACHE_KEY"]) == 64 for x in rows))
check("26_cache_keys_unicas", len({x["CACHE_KEY"] for x in rows}) == 1583)
check("27_datas_calculo_preenchidas", all(x["DATA_CALCULO_UTC"] for x in rows))

# Qualidade numérica
check("28_distancia_reta_positiva", all(x > 0 for x in straight))
check("29_distancia_rodoviaria_positiva", all(x > 0 for x in distances))
check("30_tempo_positivo", all(x > 0 for x in times))
check("31_sem_nan_reta", all(math.isfinite(x) for x in straight))
check("32_sem_nan_rodoviaria", all(math.isfinite(x) for x in distances))
check("33_sem_nan_tempo", all(math.isfinite(x) for x in times))
check("34_fator_calculado", all(float(x["FATOR_RODOVIARIO"]) > 0 for x in rows))
check("35_qa_apenas_estados_validos", {x["QA_STATUS"] for x in rows} <= {"OK", "REVISAR"})
check("36_qa_revisar_18", sum(x["QA_STATUS"] == "REVISAR" for x in rows) == 18)
check("37_qa_arquivo_18", len(list(csv.DictReader((GEO / "qa_roteamento.csv").open(encoding="utf-8-sig", newline="")))) == 18)
check("38_checkpoint_completo", json.loads((GEO / "checkpoint_roteamento.json").read_text(encoding="utf-8"))["processados"] == 1583)
check("39_estatistica_cobertura", json.loads((GEO / "estatisticas_roteamento.json").read_text(encoding="utf-8"))["COBERTURA_PCT"] == 100.0)
check("40_municipios_reconciliados", json.loads((GEO / "cobertura_municipios.json").read_text(encoding="utf-8"))["total_relacoes"] == 1583)

# Segurança e integração cartográfica
check("41_lookup_1583", len(integration["por_id_endereco"]) == 1583)
check("42_lookup_ids_reconciliados", set(integration["por_id_endereco"]) == set(point_ids))
check("43_fetch_lookup", 'fetch("data/sede_para_locais.json"' in js)
check("44_secao_painel", "A partir da sede do IPEM" in html)
check("45_rotulo_distancia", "Distância rodoviária estimada" in html)
check("46_rotulo_tempo", "Tempo estimado da sede" in html)
check("47_fallback_indisponivel", "Distância e tempo da sede indisponíveis" in js)
check("48_aviso_nao_historico", "não representam deslocamento histórico realizado" in html)
check("49_sem_chave_persistida", "FxPr2eNd9AXGXRrYb0RQ4iDHQEh6JT0n" not in all_text)
check("50_sem_nome_de_segredo_no_dataset", "SAFEFLOW_TOMTOM_API_KEY" not in all_text)
check("51_sem_motor_de_rota", not re.search(r"L\.routing|routeControl", js, re.I))
check("52_sem_timeline", "timeline" not in html.lower())
check("53_sem_otimizacao", not re.search(r"tsp|vrp|or-tools|otimiza", html + js, re.I))
check("54_sem_novo_filtro_distancia", "filter-distancia" not in html)
check("55_sem_novo_dashboard", "dashboard" not in html.lower())
check("56_marcadores_preservados", "visible.forEach" in js and "marker.addTo(historyLayer)" in js)
check("57_sede_preservada_na_interface", "marker.addTo(sedeLayer)" in js)
check("58_busca_preservada", 'filter-busca' in js)
check("59_raio_preservado", "updateRadius" in js)
check("60_painel_preservado", "showDetails" in js)
check("61_duplo_clique_configurado", 'marker.on("dblclick"' in js)
check("62_isolamento_por_id", "isolatedAddressId" in js and "filtered.filter" in js)
check("63_duplo_clique_reversivel", "isolatedAddressId === feature.properties.id_endereco ? null" in js)
check("64_limpar_restaura_todos", "isolatedAddressId = null" in js)
check("65_sem_rota_rodoviaria_apos_ajuste", not re.search(r"L\.routing|routeControl", js, re.I))
check("66_enquadramento_inclui_sede", "bounds.extend([sedeCoordinates.lat, sedeCoordinates.lon])" in js)
check("67_enquadramento_evitar_legenda", "paddingTopLeft: [360, 90]" in js)
check("68_agrupamento_marcadores", "L.markerClusterGroup" in js and "leaflet.markercluster" in html)
check("69_realce_selecionado", 'kind === "selected"' in js and "selectedPulse" in (ROOT / "css/map.css").read_text(encoding="utf-8"))
check("70_linha_referencia", "L.polyline" in js and "Ligação em linha reta" in html)
check("71_linha_nao_rota", "referência visual" in html and "Não representam sequência de visitas nem rotas" in html)
check("72_botao_restaurar", "restore-all" in html and 'ui["restore-all"].addEventListener' in js)
check("73_cartao_resumo", "focus-card-distance" in html and "updateFocusCard" in js)
check("74_cor_municipio", "municipalityColor" in js and 'filters.municipio ? "municipality"' in js)
check("75_legenda_modo", "legend-mode" in html and 'ui["legend-mode"].textContent' in js)
check("76_transicao_suave", "map.flyTo" in js and "duration: 0.65" in js)

failed = [name for name, passed in results if not passed]
for name, passed in results:
    print(f"{'OK' if passed else 'FALHA'} | {name}")
print(json.dumps({"total": len(results), "aprovados": len(results) - len(failed), "falhas": failed}, ensure_ascii=False))
raise SystemExit(1 if failed else 0)
