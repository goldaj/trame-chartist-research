"""A7.5 regime report controls: fixed train thresholds, protected 2026 test."""
import json
import unittest

from research.btc_h1_m1.regime_analysis import group_report
from research.btc_h1_m1.test_statistical_baselines import fake_cases


class RegimeReportTests(unittest.TestCase):
    def test_two_dev_years_and_train_only_volatility_thresholds(self):
        train=fake_cases(2020,n=96)
        dev=fake_cases(2023,n=96)+fake_cases(2024,n=96)
        report=group_report(train,dev)
        self.assertTrue(report["baseline_fit_train_only"])
        self.assertTrue(report["regime_thresholds_derived_train_only"])
        self.assertFalse(report["2026_test_opened"])
        self.assertFalse(report["is_confirmatory"])
        years=[r for r in report["groups"] if r["dimension"]=="year"]
        self.assertEqual([x["group"] for x in years],["2023","2024"])
        for y in years:
            self.assertEqual(y["observations"],96)
            self.assertGreaterEqual(y["scores"]["persistence"]["mae_native_usd"],0.)
            self.assertGreaterEqual(y["scores"]["ridge_three_past_only_features"][
                "mean_abs_relative_error_bps"],0.)
        json.dumps(report,allow_nan=False)

    def test_dev_outcomes_cannot_change_train_regime_thresholds(self):
        train=fake_cases(2020)
        normal=group_report(train,fake_cases(2023,volatility=1.))
        changed=group_report(train,fake_cases(2023,volatility=25.))
        self.assertEqual(normal["thresholds_train_only_log_return_sigma"],
                         changed["thresholds_train_only_log_return_sigma"])
        normal_scores=[r["scores"] for r in normal["groups"] if r["dimension"]=="year"]
        changed_scores=[r["scores"] for r in changed["groups"] if r["dimension"]=="year"]
        self.assertNotEqual(normal_scores,changed_scores)

    def test_2026_cannot_be_scored(self):
        with self.assertRaisesRegex(ValueError,"2026"):
            group_report(fake_cases(2020),fake_cases(2026))
        with self.assertRaises(ValueError):
            group_report(fake_cases(2020),fake_cases(2023),min_group=31)


if __name__=="__main__":
    unittest.main()
