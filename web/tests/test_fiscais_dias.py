import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('fiscais', Path(__file__).resolve().parents[1] / 'scripts/preparar_fiscais_dias.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class FiscalDaysTests(unittest.TestCase):
    def test_individual_year_and_day(self):
        result = module.aggregate([
            dict(FISCAL='A', DATAVERIFICACAO='2018-01-01T09:00:00', ID_ENDERECO='X'),
            dict(FISCAL='A', DATAVERIFICACAO='2018-01-01T18:00:00', ID_ENDERECO='Y'),
            dict(FISCAL='B', DATAVERIFICACAO='2018-02-02', ID_ENDERECO='X'),
            dict(FISCAL='B', DATAVERIFICACAO='2018-03-03', ID_ENDERECO='Z'),
            dict(FISCAL='A', DATAVERIFICACAO='2019-01-01', ID_ENDERECO='X'),
        ])
        counts = {(r['fiscal'], r['ano']): r['dias_distintos'] for r in result['por_fiscal_ano']}
        self.assertEqual(counts, {('A', 2018): 1, ('A', 2019): 1, ('B', 2018): 2})
        self.assertNotIn(dict(fiscal='A', data='2018-02-02'), result['por_id_endereco']['X'])

    def test_reject_aggregated_or_missing(self):
        for fiscal in ('A|B', ''):
            with self.assertRaises(ValueError):
                module.aggregate([dict(FISCAL=fiscal, DATAVERIFICACAO='2018-01-01', ID_ENDERECO='X')])

if __name__ == '__main__':
    unittest.main()
