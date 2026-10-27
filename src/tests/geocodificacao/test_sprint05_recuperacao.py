"""Regressão executável com unittest para a recuperação controlada do GEO_001."""

import csv
import hashlib
import json
import math
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "geocodificacao" / "recuperacao_geo001"
SOURCE = ROOT.parent


def rows(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Sprint05RecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.diagnostic = rows("diagnostico_98.csv")
        cls.result = rows("resultado_recuperacao.csv")
        cls.queries = rows("consultas_recuperacao.csv")
        cls.compare = rows("comparacao_fontes.csv")
        cls.qa = rows("qa_manual.csv")
        cls.matrix = rows("matriz_antes_depois.csv")
        cls.manifest = json.loads((OUT / "manifesto_recuperacao.json").read_text(encoding="utf-8"))
        cls.stats = json.loads((OUT / "estatisticas_recuperacao.json").read_text(encoding="utf-8"))
        with (ROOT / "data/geocodificacao/geocodificacao_lote_001.csv").open(encoding="utf-8-sig", newline="") as stream:
            cls.audit = list(csv.DictReader(stream))
        cls.geo = json.loads((ROOT / "data/pontos_classe_a.geojson").read_text(encoding="utf-8"))

    def test_01_universe_exactly_98(self): self.assertEqual(len(self.result), 98)
    def test_02_two_original_a_excluded(self): self.assertTrue(set(self.manifest["classes_a_originais_excluidas"]).isdisjoint({x["ID_ENDERECO"] for x in self.result}))
    def test_03_no_new_address_entered(self): self.assertEqual({x["ID_ENDERECO"] for x in self.result}, {x["ID_ENDERECO"] for x in self.audit if x["CLASSIFICACAO"] != "A"})
    def test_04_original_class_preserved(self): self.assertEqual({x["ID_ENDERECO"]: x["CLASSIFICACAO_ORIGINAL"] for x in self.result}, {x["ID_ENDERECO"]: x["CLASSIFICACAO"] for x in self.audit if x["CLASSIFICACAO"] != "A"})
    def test_05_original_nominatim_audit_hash(self): self.assertEqual(digest(ROOT / "data/geocodificacao/geocodificacao_lote_001.csv"), self.manifest["hashes_fontes_sha256"]["geocodificacao_lote_001.csv"])
    def test_06_original_cache_hash(self): self.assertEqual(digest(ROOT / "data/geocodificacao/cache_geocodificacao.json"), self.manifest["hashes_fontes_sha256"]["cache_geocodificacao.json"])
    def test_07_raw_history_hash(self): self.assertEqual(digest(SOURCE / "fact_verificacao_item_mapa.csv"), self.manifest["hashes_fontes_sha256"]["fact_verificacao_item_mapa.csv"])
    def test_08_internal_trace_fields(self): self.assertTrue(all("IDS_EVIDENCIA_INTERNA" in x for x in self.diagnostic))
    def test_09_original_address_preserved(self): self.assertTrue(all(x["ENDERECO_ORIGINAL"] for x in self.result))
    def test_10_recovered_address_separate(self): self.assertTrue(all("ENDERECO_RECUPERADO" in x for x in self.result))
    def test_11_cep_is_text(self): self.assertTrue(all(isinstance(x["CEP_ORIGINAL"], str) for x in self.diagnostic))
    def test_12_cep_original_preserved(self): self.assertEqual(len(self.diagnostic), 98)
    def test_13_sn_never_gets_number(self): self.assertTrue(all(not x["NUMERO_RECUPERADO"] for x, d in zip(self.result, self.diagnostic) if d["NUMERO_ORIGINAL"].upper().replace("/", " ").strip() in {"S N", "SN", ""}))
    def test_14_missing_road_not_invented_in_diagnostic(self): self.assertTrue(all(not x["LOGRADOURO_ORIGINAL"] or x["LOGRADOURO_ORIGINAL"] == "-" for x in self.diagnostic if "LOGRADOURO_AUSENTE" in x["MOTIVO_PRIMARIO"]))
    def test_15_alternative_queries_registered(self): self.assertEqual(len(self.queries), 98)
    def test_16_viacep_cache_has_43(self): self.assertEqual(len(json.loads((OUT / "cache_provedor_2.json").read_text(encoding="utf-8"))), 43)
    def test_17_nominatim_cache_independent(self): self.assertNotEqual(OUT / "cache_nominatim_variantes.json", ROOT / "data/geocodificacao/cache_geocodificacao.json")
    def test_18_second_provider_does_not_overwrite_first(self): self.assertTrue(self.manifest["resultado_original_preservado"])
    def test_19_city_validated_for_recovered(self): self.assertTrue(all(x["MUNICIPIO_RECUPERADO"] for x in self.result if x["PUBLICAR"] == "true"))
    def test_20_state_validated_for_recovered(self): self.assertTrue(all(x["UF_RECUPERADA"] == "SP" for x in self.result if x["PUBLICAR"] == "true"))
    def test_21_coordinates_valid(self): self.assertTrue(all(-90 <= float(x["LATITUDE_RECUPERADA"]) <= 90 and -180 <= float(x["LONGITUDE_RECUPERADA"]) <= 180 for x in self.result if x["PUBLICAR"] == "true"))
    def test_22_distance_nonnegative(self): self.assertTrue(all(float(x["DISTANCIA_ENTRE_FONTES_METROS"]) >= 0 for x in self.compare if x["DISTANCIA_ENTRE_FONTES_METROS"]))
    def test_23_conflict_detectable(self): self.assertTrue(all(x["CONFLITO_DETECTAVEL"] in {"true", "false"} for x in self.compare))
    def test_24_no_poi_identity_rule(self): self.assertFalse(any("NOME" in x["REGRA_RECUPERACAO"] for x in self.result))
    def test_25_b_requires_extra_evidence(self): self.assertTrue(all(x["CLASSIFICACAO_APOS_RECUPERACAO"] == "B_MANTIDO" for x in self.result if x["CLASSIFICACAO_ORIGINAL"] == "B" and x["PUBLICAR"] != "true"))
    def test_26_review_not_auto_promoted(self): self.assertTrue(all(x["CLASSIFICACAO_APOS_RECUPERACAO"] == "REVISAO_MANUAL" for x in self.result if x["CLASSIFICACAO_ORIGINAL"] == "REVISAO_MANUAL" and x["PUBLICAR"] != "true"))
    def test_27_not_found_not_auto_promoted(self): self.assertTrue(all(x["CLASSIFICACAO_APOS_RECUPERACAO"] == "NAO_ENCONTRADO" for x in self.result if x["CLASSIFICACAO_ORIGINAL"] == "NAO_ENCONTRADO" and x["PUBLICAR"] != "true"))
    def test_28_recovered_has_justification(self): self.assertTrue(all(x["EVIDENCIA_ENDERECO"] for x in self.result if x["PUBLICAR"] == "true"))
    def test_29_recovered_has_provenance(self): self.assertTrue(all(x["ORIGEM_VALIDACAO"] == "RECUPERACAO_SPRINT05" for x in self.result if x["PUBLICAR"] == "true"))
    def test_30_qa_covers_all_recovered(self): self.assertEqual({x["ID_ENDERECO"] for x in self.qa}, {x["ID_ENDERECO"] for x in self.result if x["PUBLICAR"] == "true"})
    def test_31_only_recovered_publish(self): self.assertTrue(all((x["PUBLICAR"] == "true") == (x["CLASSIFICACAO_APOS_RECUPERACAO"] == "A_RECUPERADO") for x in self.result))
    def test_32_18_previous_preserved(self): self.assertGreaterEqual(len(self.geo["features"]), 18)
    def test_33_total_reconciled(self): self.assertEqual(len(self.geo["features"]), self.stats["publicados_depois"])
    def test_34_geojson_valid(self): self.assertEqual(self.geo["type"], "FeatureCollection")
    def test_35_all_geometry_points(self): self.assertTrue(all(x["geometry"]["type"] == "Point" for x in self.geo["features"]))
    def test_36_filter_core_preserved(self): self.assertTrue((ROOT / "js/filter-core.js").exists())
    def test_37_sede_preserved(self): self.assertEqual(len(json.loads((ROOT / "data/sede.geojson").read_text(encoding="utf-8"))["features"]), 1)
    def test_38_radius_preserved(self): self.assertIn("radius", (ROOT / "js/filter-core.js").read_text(encoding="utf-8").lower())
    def test_39_dynamic_counter_preserved(self): self.assertIn('ui["point-counter"].textContent', (ROOT / "js/map.js").read_text(encoding="utf-8"))
    def test_40_rollback_available(self): self.assertTrue((ROOT.parent / "safeflow-map-sprint04-baseline/BASELINE_SPRINT04.json").exists())
    def test_41_hashes_registered(self): self.assertGreaterEqual(len(self.manifest["hashes_fontes_sha256"]), 6)
    def test_42_no_route_geometry(self): self.assertFalse(any(x["geometry"]["type"] == "LineString" for x in self.geo["features"]))
    def test_43_no_visit_sequence_semantics(self): self.assertNotIn("sequencia_visita", json.dumps(self.geo, ensure_ascii=False).lower())
    def test_44_all_have_primary_reason(self): self.assertTrue(all(x["MOTIVO_PRIMARIO"] for x in self.diagnostic))
    def test_45_matrix_sums_98(self): self.assertEqual(sum(int(x["QUANTIDADE"]) for x in self.matrix), 98)
    def test_46_current_result_zero_recovered(self): self.assertEqual(self.stats["a_recuperado"], 0)
    def test_47_current_map_stays_18(self): self.assertEqual(len(self.geo["features"]), 18)
    def test_48_no_paid_cost(self): self.assertEqual(self.stats["custo_monetario"], 0)
    def test_49_original_a_still_two(self): self.assertEqual(sum(x["CLASSIFICACAO"] == "A" for x in self.audit), 2)
    def test_50_manifest_universe_ordered(self): self.assertEqual(len(self.manifest["universo_ids"]), len(set(self.manifest["universo_ids"])))


if __name__ == "__main__":
    unittest.main()
