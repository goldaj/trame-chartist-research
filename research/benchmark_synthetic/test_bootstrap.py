"""Adversarial block-bootstrap tests; all observations fictitious."""
import unittest

from research.benchmark_synthetic.bootstrap import (
    validate_records,paired_group_report,moving_block_interval)


def fabricated(n=120,*,asset='TOY',horizon=1,unit_scale=1):
    return [{'asset':asset,'origin_index':i,'target_index':i+horizon,
             'horizon':horizon,'anchor':100.0*unit_scale,
             'actual':101.0*unit_scale,'forecast':100.8*unit_scale}
            for i in range(n)]


class PairedComparisonTests(unittest.TestCase):
    def test_same_native_prices_and_uncertainty_per_asset_horizon(self):
        one=fabricated(120)
        two=fabricated(120,asset='DIFFERENT',unit_scale=150)
        report=paired_group_report(one+two)
        self.assertEqual(set(report),{'TOY::h=1','DIFFERENT::h=1'})
        self.assertAlmostEqual(report['TOY::h=1']['mean_paired_gain_native'],.8)
        self.assertAlmostEqual(report['DIFFERENT::h=1']['mean_paired_gain_native'],120.)
        self.assertAlmostEqual(report['TOY::h=1']['gain_percent_if_defined'],80.)

    def test_known_constant_block_ci_around_gain(self):
        r=paired_group_report(fabricated())
        gains=r['TOY::h=1']['paired_gains']
        boot=moving_block_interval(gains,block=20,resamples=300,seed=20)
        self.assertAlmostEqual(boot['observed_mean_gain'],.8,delta=1e-10)
        self.assertAlmostEqual(boot['percentile_ci95'][0],.8,delta=1e-10)
        self.assertAlmostEqual(boot['percentile_ci95'][1],.8,delta=1e-10)
        self.assertTrue(boot['cannot_fix_selection_leakage'])

    def test_labels_overlap_when_horizon_exceeds_origin_spacing(self):
        r=paired_group_report(fabricated(horizon=5))
        self.assertTrue(r['TOY::h=5']['labels_overlap'])

    def test_fail_on_too_short_series_or_origin_duplicates(self):
        with self.assertRaises(ValueError):
            moving_block_interval([1.,2.],block=2)
        rows=fabricated(5)
        with self.assertRaises(ValueError):
            validate_records(rows + [dict(rows[0])])

    def test_reject_invalid_forecast_and_inconsistent_origin_target(self):
        for change in [{'forecast':float('nan')},{'forecast':0.},
                       {'target_index':10000},{'origin_index':-1},
                       {'horizon':0},{'actual':-10.}]:
            with self.subTest(change=change):
                row={**fabricated(1)[0],**change}
                with self.assertRaises(ValueError):
                    validate_records([row])


if __name__=='__main__':
    unittest.main()
