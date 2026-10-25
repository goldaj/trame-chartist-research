"""HTML and JSON output contract; constructed payload, no API or actual market."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research.trame_lab.cli import render_html,write_reports,run_lab,main


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
                            'manufactured_gain_by_construction':True},
        'architecture_comparison':{
            'data_origin':'ARTIFICIAL_ONLY',
            'reserved_synthetic_test_opened':False,
            'financial_holdout_opened':False,
            'compute_matched':False,
            'parameter_matched':False,
            'results':[
                {'architecture':name,'seed':seed,
                 'parameter_count':1000,'end_development_nll':2.9}
                for name in ('legacy_causal_transformer','modern_gpt_style_mini',
                             'recurrent_gru_control')
                for seed in (1,2,3)
            ]
        }
    }


class DemoTests(unittest.TestCase):
    def test_html_explicit_artificial_warning_and_scores(self):
        html=render_html(toy())
        self.assertIn('DONNÉES ARTIFICIELLES UNIQUEMENT',html)
        self.assertIn('Oracle synthétique connu',html)
        self.assertIn('aucune prédiction financière',html)
        self.assertIn('CRPS',html)
        self.assertIn('<table>',html)
        self.assertIn('<caption>NLL de développement sur données artificielles',html)
        self.assertIn('<th scope="row">TRAME mini-Transformer</th><td>2.8000</td>',html)
        self.assertIn('aria-hidden="true"',html)
        self.assertIn('href="#results"',html)
        self.assertIn('Trois architectures comparées en parallèle',html)
        self.assertIn('mini décodeur GPT-style',html)
        self.assertIn('NLL de développement artificiel par bras et par graine',html)

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

    def test_staging_error_preserves_existing_pair(self):
        # On an injected failure to create the second staging file, the
        # existing HTML+JSON remain untouched even when overwrite=True.
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td)/'report.html'
            write_reports(toy(),dest)
            html_before=dest.read_bytes()
            json_before=dest.with_suffix('.json').read_bytes()
            real_temp=tempfile.NamedTemporaryFile
            calls=0
            def fail_second_stage(**kwargs):
                nonlocal calls
                calls+=1
                if calls==2:
                    raise OSError('simulated temp write preparation failure')
                return real_temp(**kwargs)
            with patch('research.trame_lab.cli.NamedTemporaryFile',side_effect=fail_second_stage):
                with self.assertRaisesRegex(OSError,'simulated'):
                    write_reports(toy(),dest,overwrite=True)
            self.assertEqual(dest.read_bytes(),html_before)
            self.assertEqual(dest.with_suffix('.json').read_bytes(),json_before)
            self.assertEqual(sorted(p.name for p in Path(td).iterdir()),
                             ['report.html','report.json'])

    def test_reject_misleading_architecture_comparisons(self):
        cases=[
            ('data_origin','REAL'),
            ('reserved_synthetic_test_opened',True),
            ('financial_holdout_opened',True),
            ('compute_matched',True),
            ('parameter_matched',True),
        ]
        for field,invalid in cases:
            with self.subTest(field=field):
                payload=copy.deepcopy(toy())
                payload['architecture_comparison'][field]=invalid
                with self.assertRaises(ValueError):
                    render_html(payload)
        payload=toy()
        payload['architecture_comparison']['results'][0]['end_development_nll']=float('nan')
        with self.assertRaises(ValueError):
            render_html(payload)

    def test_reject_invalid_steps_without_training(self):
        for steps in (-1,0,201,1.5,True):
            with self.subTest(steps=steps),self.assertRaises(ValueError):
                run_lab(train_steps=steps)
        with self.assertRaises(SystemExit) as invalid_cli:
            main(['--steps','0'])
        self.assertEqual(invalid_cli.exception.code,2)

    def test_reject_invalid_artificial_metrics(self):
        cases=[
            (('model','end_development_nll'),float('nan')),
            (('model','model_parameters'),0),
            (('toy_forecast','price_q10'),120),
            (('toy_forecast','empirical_CRPS_price_units'),-1),
            (('paired_benchmark','toy_ci_block95'),[2,1]),
            (('paired_benchmark','manufactured_gain_by_construction'),False),
        ]
        for keys,invalid in cases:
            with self.subTest(keys=keys):
                payload=copy.deepcopy(toy())
                payload[keys[0]][keys[1]]=invalid
                with self.assertRaises(ValueError):
                    render_html(payload)

    def test_reject_misleading_output_and_missing_data(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                write_reports(toy(),Path(td)/'chart.pdf')
        with self.assertRaises(ValueError):
            render_html({'model':{}})


if __name__=='__main__':
    unittest.main()
