"""Native-price scoring and separate Monte-Carlo checks on fictional prices."""
import math
import unittest

import numpy as np

try:
    from .calibration import score_ensemble, mc_replicate_crps
except ImportError:
    from calibration import score_ensemble, mc_replicate_crps


class EnsembleScoringTests(unittest.TestCase):
    def test_exact_constructed_coverage_and_width(self):
        x=np.array([1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.])
        report=score_ensemble(x, observed=6., anchor=5.)
        self.assertEqual(report['median'],6.)
        self.assertTrue(report['coverage50'])
        self.assertTrue(report['coverage80'])
        self.assertTrue(report['coverage90'])
        self.assertAlmostEqual(report['median_absolute_error'],0.)
        self.assertAlmostEqual(report['persistence_absolute_error'],1.)
        self.assertTrue(report['width90'] >= report['width80'] >= report['width50'])

    def test_far_outlier_not_counted_as_covered(self):
        x=np.array([100.,101.,102.,103.,104.,105.])
        report=score_ensemble(x, observed=1000., anchor=98.)
        self.assertFalse(report['coverage90'])
        self.assertFalse(report['coverage80'])
        self.assertGreater(report['crps_price_units'],0.)

    def test_crps_scales_homogeneously_in_native_price_units(self):
        x=[100.,110.,120.,130.,140.]
        r1=score_ensemble(x,115.,100.)
        r2=score_ensemble([v*70 for v in x],115.*70,100.*70)
        for metric in ['crps_price_units','median_absolute_error',
                       'persistence_absolute_error','width90']:
            self.assertAlmostEqual(r2[metric],r1[metric]*70,delta=1e-8)

    def test_monte_carlo_replicates_not_market_uncertainty(self):
        rng=np.random.default_rng(2031)
        groups=[np.exp(rng.normal(0.0,.15,150))*100 for _ in range(6)]
        report=mc_replicate_crps(groups,100.)
        self.assertEqual(report['replicates'],6)
        self.assertGreaterEqual(report['mc_standard_error_across_independent_ensembles'],0.)
        self.assertIn('not from market',report['warning'])
        with self.assertRaises(ValueError):
            mc_replicate_crps(groups[:2],100.)

    def test_reject_bad_prices(self):
        for draws in ([],[1.],[1.,float('nan')],[0.,1.],[-1.,1.]):
            with self.assertRaises(ValueError):
                score_ensemble(draws,observed=1.,anchor=1.)


if __name__=='__main__':
    unittest.main()
