"""HTML and JSON output contract; constructed payload, no API or actual market."""
import json
from pathlib import Path
import tempfile
import unittest

from research.trame_lab.cli import render_html,write_reports


def toy():
    return {
        'model':{
            'end_development_nll':2.8,'optimization_steps':4,
            'model_parameters':5000,'development_paths':12,
            'controls_development':{
                'oracle_known_generator_nll':2.2,
                'linear_train_only_nll':2.5,
                'constant_mu0_train_scale_nll':3.1
            }},
        'toy_forecast':{
            'price_median':101,'price_q10':80,'price_q90':110,
            'empirical_CRPS_price_units':9.4
        },
        'paired_benchmark':{'toy_gain_native':0.8,'toy_ci_block95':[0.8,0.8],
                            'manufactured_gain_by_construction':True}
    }


class DemoTests(unittest.TestCase):
    def test_html_explicit_artificial_warning_and_scores(self):
        html=render_html(toy())
        self.assertIn('DONNÉES ARTIFICIELLES UNIQUEMENT',html)
        self.assertIn('Oracle synthétique connu',html)
        self.assertIn('aucune prédiction financière',html)
        self.assertIn('CRPS',html)

    def test_pair_of_files_and_no_unintentional_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td)/'report.html'
            first,second=write_reports(toy(),dest)
            self.assertTrue(Path(first).exists())
            self.assertTrue(Path(second).exists())
            self.assertEqual(json.loads(Path(second).read_text())['model']['model_parameters'],5000)
            with self.assertRaises(FileExistsError):
                write_reports(toy(),dest)
            write_reports(toy(),dest,overwrite=True)

    def test_reject_misleading_output_and_missing_data(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                write_reports(toy(),Path(td)/'chart.pdf')
        with self.assertRaises(ValueError):
            render_html({'model':{}})


if __name__=='__main__':
    unittest.main()
