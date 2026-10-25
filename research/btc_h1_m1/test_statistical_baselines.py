"""A7.3 synthetic fixtures for causal financial baselines."""
import json
import math
import unittest
from datetime import datetime, timedelta, timezone

from research.btc_h1_m1.stream import Case
from research.btc_h1_m1.statistical_baselines import (
    fit_baselines, score_baselines,
)


def fake_cases(year, *, n=96, volatility=1.):
    """Artificial training cases with known past: no exchange history."""
    start = datetime(year, 1, 1, tzinfo=timezone.utc)
    cases = []
    for i in range(n):
        codes = tuple(int((j+i) % 7 - 3) for j in range(20))
        origin = start + timedelta(hours=i)
        target = origin + timedelta(hours=1)
        anchor = 20000. + i
        true = anchor * math.exp(volatility *
                                  (0.5*codes[-1] + (i%5-2))/1000)
        cases.append(Case(
            origin_open=origin, target_open=target,
            decision_time=target,
            label_available_time=target+timedelta(hours=1),
            encoded_past=codes, encoded_target=0,
            anchor_usd=anchor, target_usd=true, grade="ARTIFICIAL_ONLY"))
    return cases


class ClassicalBaselineTests(unittest.TestCase):
    def test_fit_only_on_pre2022_and_finite_scoring(self):
        train, dev = fake_cases(2020), fake_cases(2023)
        result = score_baselines(train, dev)
        self.assertTrue(result["2026_test_quarantined"])
        self.assertFalse(result["fit"]["fitted_using_development"])
        self.assertFalse(result["not_hyperliquid_execution"] is False)
        for model in result["baselines"].values():
            self.assertEqual(model["forecast_rows"], 96)
            self.assertTrue(math.isfinite(model["mae_native_usd"]))
            self.assertTrue(0 <= model["coverage_80pct"] <= 1)
        json.dumps(result, allow_nan=False)

    def test_dev_label_change_never_retrains_baselines(self):
        train = fake_cases(2020)
        stable = score_baselines(train, fake_cases(2023))
        shifted = score_baselines(train, fake_cases(2023, volatility=20.))
        self.assertEqual(stable["fit"], shifted["fit"])
        self.assertNotEqual(stable["baselines"]["ridge_three_past_only_features"][
            "mae_native_usd"], shifted["baselines"]["ridge_three_past_only_features"][
            "mae_native_usd"])

    def test_reject_2026_and_train_dev_overlap(self):
        with self.assertRaises(ValueError):
            score_baselines(fake_cases(2020), fake_cases(2026))
        with self.assertRaises(ValueError):
            score_baselines(fake_cases(2023), fake_cases(2024))
        with self.assertRaises(ValueError):
            fit_baselines(fake_cases(2020), ridge_alpha=0)

    def test_train_cannot_contain_development_label(self):
        with self.assertRaises(ValueError):
            fit_baselines(fake_cases(2022))


if __name__ == "__main__":
    unittest.main()
