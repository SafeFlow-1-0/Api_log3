from __future__ import annotations

import csv
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT.parent
AUDIT_DIR = ROOT / "data" / "geocodificacao"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def load_pipeline():
    path = ROOT / "scripts" / "geocode_lote_001.py"
    spec = importlib.util.spec_from_file_location("geocode_lote_001", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class Sprint04LotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = load_pipeline()
        cls.source = read_csv(OUTPUTS / "mapa_historico_pontos.csv")
        cls.source_by_id = {row["ID_ENDERECO"]: row for row in cls.source}
        cls.addresses = {row["ID_ENDERECO"]: row for row in read_csv(OUTPUTS / "dim_endereco_mapa.csv")}
        cls.audit = read_csv(AUDIT_DIR / "geocodificacao_lote_001.csv")
        cls.manifest = json.loads((AUDIT_DIR / "manifesto_geo_lote_001.json").read_text(encoding="utf-8"))
        cls.cache = json.loads((AUDIT_DIR / "cache_geocodificacao.json").read_text(encoding="utf-8"))
        cls.stats = json.loads((AUDIT_DIR / "estatisticas_lote_001.json").read_text(encoding="utf-8"))
        cls.geojson = json.loads((ROOT / "data" / "pontos_classe_a.geojson").read_text(encoding="utf-8"))
        cls.baseline_geojson = json.loads((OUTPUTS / "safeflow-map-sprint03-baseline" / "data" / "pontos_classe_a.geojson").read_text(encoding="utf-8"))
        cls.baseline_manifest = json.loads((OUTPUTS / "safeflow-map-sprint03-baseline" / "BASELINE_SPRINT03.json").read_text(encoding="utf-8"))

    def test_01_exatamente_100_selecionados(self): self.assertEqual(self.manifest["quantidade_selecionada"], 100)
    def test_02_todos_eram_pendentes(self): self.assertTrue(all(self.source_by_id[i]["STATUS_GEOCODIFICACAO"] == "PENDENTE" for i in self.manifest["ids_selecionados"]))
    def test_03_classe_a_antiga_fora_do_lote(self): self.assertFalse({r["ID_ENDERECO"] for r in self.source if r["QUALIDADE_GEOCODIFICACAO"] == "A"} & set(self.manifest["ids_selecionados"]))
    def test_04_classe_b_antiga_fora_do_lote(self): self.assertFalse({r["ID_ENDERECO"] for r in self.source if r["QUALIDADE_GEOCODIFICACAO"] == "B"} & set(self.manifest["ids_selecionados"]))
    def test_05_rejeitados_antigos_fora_do_lote(self): self.assertFalse({r["ID_ENDERECO"] for r in self.source if r["STATUS_GEOCODIFICACAO"].startswith("REJEITADO")} & set(self.manifest["ids_selecionados"]))
    def test_06_nao_encontrados_antigos_fora_do_lote(self): self.assertFalse({r["ID_ENDERECO"] for r in self.source if r["STATUS_GEOCODIFICACAO"] == "NAO_ENCONTRADO"} & set(self.manifest["ids_selecionados"]))
    def test_07_sede_fora_do_lote(self): self.assertNotIn("SEDE_001", self.manifest["ids_selecionados"])
    def test_08_selecao_deterministica(self): self.assertEqual(self.manifest["ids_selecionados"], sorted(r["ID_ENDERECO"] for r in self.source if r["STATUS_GEOCODIFICACAO"] == "PENDENTE")[:100])
    def test_09_manifesto_contem_100_ids_unicos(self): self.assertEqual(len(set(self.manifest["ids_selecionados"])), 100)
    def test_10_cache_contem_as_100_consultas(self): self.assertEqual(len(self.cache), 100)
    def test_11_retomada_nao_duplicou_auditoria(self): self.assertEqual(len(self.audit), len({r["ID_ENDERECO"] for r in self.audit})); self.assertEqual(len(self.audit), 100)

    def test_12_latitudes_validas_quando_retornadas(self):
        self.assertTrue(all(-90 <= float(r["LATITUDE_RETORNADA"]) <= 90 for r in self.audit if r["LATITUDE_RETORNADA"]))

    def test_13_longitudes_validas_quando_retornadas(self):
        self.assertTrue(all(-180 <= float(r["LONGITUDE_RETORNADA"]) <= 180 for r in self.audit if r["LONGITUDE_RETORNADA"]))

    def test_14_uf_validada_nos_encontrados_compativeis(self): self.assertTrue(all(r["UF_RETORNADA"] == "SP" for r in self.audit if r["CLASSIFICACAO"] in {"A", "B", "REVISAO_MANUAL"}))
    def test_15_municipio_validado_para_a_e_b(self): self.assertTrue(all(r["MUNICIPIO_COMPATIVEL"] == "true" for r in self.audit if r["CLASSIFICACAO"] in {"A", "B"}))

    def test_16_incompatibilidade_municipio_e_rejeitada(self):
        row = {**self.addresses["END_000027"], "MUNICIPIO": "SAO JOSE DOS CAMPOS", "UF": "SP"}
        candidate = {"lat": "-23", "lon": "-46", "address": {"road": "Rua Abaete", "house_number": "104", "city": "Santos", "state": "São Paulo", "ISO3166-2-lvl4": "BR-SP"}}
        self.assertEqual(self.pipeline.classify(row, [candidate])["CLASSIFICACAO"], "REJEITADO_MUNICIPIO")

    def test_17_incompatibilidade_uf_e_rejeitada(self):
        row = {**self.addresses["END_000027"], "MUNICIPIO": "SAO JOSE DOS CAMPOS", "UF": "SP"}
        candidate = {"lat": "-22", "lon": "-43", "address": {"road": "Rua Abaete", "house_number": "104", "city": "São José dos Campos", "state": "Rio de Janeiro", "ISO3166-2-lvl4": "BR-RJ"}}
        self.assertEqual(self.pipeline.classify(row, [candidate])["CLASSIFICACAO"], "REJEITADO_UF")

    def test_18_sem_numero_nunca_classe_a(self): self.assertTrue(all(r["CLASSIFICACAO"] != "A" for r in self.audit if r["ENDERECO_SEM_NUMERO"] == "true"))
    def test_19_cep_original_preservado(self): self.assertTrue(all(r["CEP_ORIGINAL"] == self.addresses[r["ID_ENDERECO"]]["CEP_ORIGINAL"] for r in self.audit))
    def test_20_cep_recomposto_rastreavel(self): self.assertTrue(all((r["ZERO_INICIAL_RECOMPOSTO"] == "true") == (r["REGRA_CEP_APLICADA"] == "ZERO_INICIAL_RECOMPOSTO") for r in self.audit))
    def test_21_resposta_original_preservada(self): self.assertTrue(all(r["RESPOSTA_ORIGINAL_JSON"] for r in self.audit if r["CLASSIFICACAO"] != "ERRO_SERVICO"))
    def test_22_tentativa_registrada(self): self.assertTrue(all(r["NUMERO_TENTATIVA"] == "1" for r in self.audit))
    def test_23_erro_servico_e_categoria_separada(self): self.assertIn('"ERRO_SERVICO"', (ROOT / "scripts" / "geocode_lote_001.py").read_text(encoding="utf-8"))
    def test_24_classe_b_nao_publicada(self): self.assertTrue(all(r["PUBLICAR"] == "false" for r in self.audit if r["CLASSIFICACAO"] == "B"))
    def test_25_revisao_nao_publicada(self): self.assertTrue(all(r["PUBLICAR"] == "false" for r in self.audit if r["CLASSIFICACAO"] == "REVISAO_MANUAL"))
    def test_26_rejeitados_nao_publicados(self): self.assertTrue(all(r["PUBLICAR"] == "false" for r in self.audit if r["CLASSIFICACAO"].startswith("REJEITADO")))

    def test_27_somente_novos_a_foram_adicionados(self):
        new = [f for f in self.geojson["features"] if f["properties"]["id_lote_geocodificacao"] == "GEO_001"]
        self.assertEqual({f["properties"]["id_endereco"] for f in new}, {r["ID_ENDERECO"] for r in self.audit if r["CLASSIFICACAO"] == "A"})

    def test_28_dezesseis_antigos_permanecem(self): self.assertTrue({f["id"] for f in self.baseline_geojson["features"]}.issubset({f["id"] for f in self.geojson["features"]}))
    def test_29_contagem_publicada_reconciliada(self): self.assertEqual(len(self.geojson["features"]), 16 + self.stats["classe_a"])
    def test_30_geojson_valido(self): self.assertEqual(self.geojson["type"], "FeatureCollection")
    def test_31_ids_publicados_unicos(self): self.assertEqual(len(self.geojson["features"]), len({f["id"] for f in self.geojson["features"]}))
    def test_32_historico_relacionado_nos_novos(self): self.assertTrue(all(f["properties"]["datas_historicas"] and f["properties"]["estabelecimentos"] for f in self.geojson["features"] if f["properties"]["id_lote_geocodificacao"] == "GEO_001"))
    def test_33_filtros_sprint03_preservados(self): self.assertTrue((ROOT / "js" / "filter-core.js").exists() and "filterFeatures" in (ROOT / "js" / "filter-core.js").read_text(encoding="utf-8"))
    def test_34_contador_continua_dinamico(self): self.assertIn("allFeatures.length", (ROOT / "js" / "map.js").read_text(encoding="utf-8"))
    def test_35_sede_permanece_visivel(self): self.assertIn("sedeLayer", (ROOT / "js" / "map.js").read_text(encoding="utf-8"))
    def test_36_raio_permanece_haversine(self): self.assertIn("haversineKm", (ROOT / "js" / "filter-core.js").read_text(encoding="utf-8"))
    def test_37_sem_semantica_de_rota(self): self.assertNotIn("TOTAL_VISITAS", (ROOT / "js" / "map.js").read_text(encoding="utf-8"))
    def test_38_fontes_historicas_inalteradas(self): self.assertEqual(self.manifest["hash_fonte_mapa_historico_pontos_sha256"], self.pipeline.sha256(OUTPUTS / "mapa_historico_pontos.csv"))
    def test_39_hashes_baseline_registrados(self): self.assertGreaterEqual(len(self.baseline_manifest["files"]), 13)
    def test_40_rollback_possivel(self): self.assertEqual(len(self.baseline_geojson["features"]), 16)
    def test_41_estatisticas_totalizam_100(self): self.assertEqual(self.stats["classe_a"] + self.stats["classe_b"] + self.stats["revisao_manual"] + self.stats["rejeitados_municipio"] + self.stats["rejeitados_uf"] + self.stats["nao_encontrados"] + self.stats["erros_servico"], 100)
    def test_42_estatisticas_por_qualidade_existem(self): self.assertTrue((AUDIT_DIR / "qualidade_origem_lote_001.csv").exists())
    def test_43_estatisticas_por_municipio_existem(self): self.assertTrue((AUDIT_DIR / "municipios_lote_001.csv").exists())


if __name__ == "__main__":
    unittest.main()
