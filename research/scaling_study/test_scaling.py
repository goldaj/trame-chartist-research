"""S1.6: fabricated-only adversarial fixtures. No private market prices."""
import math
from datetime import datetime, timedelta, timezone
import unittest

import numpy as np
import torch

from research.btc_h1_m1.stream import Case
from research.scaling_study.metrics import (
    score_forecasts, training_magnitude_thresholds, baseline_forecasts,
)
from research.scaling_study.models import (
    FAMILIES, DEPTHS, capacity_grid, expected_parameters,
)
from research.scaling_study.runner import run_cases


def make_case(year, i):
    stamp = datetime(year, 1, 2, tzinfo=timezone.utc) + timedelta(hours=i)
    anchor = 100.0 + i * 0.1
    # Both directions and zero-valued cases; different signs available.
    actual = anchor * (1.0 + (-1 if i % 3 == 0 else 1 if i % 3 == 1 else 0) * 0.002)
    return Case(
        origin_open=stamp - timedelta(hours=1), target_open=stamp,
        decision_time=stamp, label_available_time=stamp + timedelta(hours=1),
        encoded_past=tuple((j + i) % 5 - 2 for j in range(20)),
        encoded_target=int(round(math.log(actual / anchor) * 1000)),
        anchor_usd=anchor, target_usd=actual, grade="fabricated",
    )


class ScalingModelTests(unittest.TestCase):
    def test_parameter_formula_and_depths(self):
        # Every architecture/depth at small widths; no need to allocate huge nets.
        for family, factory in FAMILIES.items():
            for depth in DEPTHS:
                with self.subTest(family=family, depth=depth):
                    model = factory(width=12, depth=depth, length=20)
                    actual = sum(p.numel() for p in model.parameters())
                    expected = expected_parameters(
                        family, width=12, depth=depth, length=20)
                    self.assertEqual(actual, expected)
                    self.assertTrue(all(p.dtype == torch.float64
                                        for p in model.parameters()))
        grid = capacity_grid(targets=(2400, 37000),
                             depths=(1, 2, 4))
        self.assertEqual(len(grid), 18)
        self.assertTrue(all(not row["compute_matched"] for row in grid))

    def test_strict_causal_future_token_invariance(self):
        torch.manual_seed(3)
        torch.set_num_threads(1)
        data = torch.randn((2, 7), dtype=torch.float64)
        changed = data.clone()
        changed[:, -1] = 100.0
        for name, factory in FAMILIES.items():
            for depth in DEPTHS:
                with self.subTest(name=name, depth=depth):
                    net = factory(width=8, depth=depth, length=20)
                    net.eval()
                    with torch.no_grad():
                        a, _ = net(data)
                        b, _ = net(changed)
                    torch.testing.assert_close(a[:, :-1], b[:, :-1],
                                               atol=1e-10, rtol=1e-10)

    def test_finite_gradients(self):
        torch.set_num_threads(1)
        x = torch.randn(3, 5, dtype=torch.float64)
        y = torch.zeros_like(x)
        for factory in FAMILIES.values():
            model = factory(width=8, depth=2, length=20)
            loss = model.nll(x, y)
            self.assertTrue(bool(torch.isfinite(loss)))
            loss.backward()
            self.assertTrue(all(p.grad is None or bool(torch.isfinite(p.grad).all())
                                for p in model.parameters()))


class DirectionTests(unittest.TestCase):
    def test_sign_flats_and_abstention(self):
        train = [make_case(2018, i) for i in range(40)]
        t = training_magnitude_thresholds(train)
        anchors = [100, 100, 100, 100]
        actuals = [101, 99, 100, 102]
        predicted = [101, 98, 100, 99]
        stats = score_forecasts(anchors, actuals, predicted,
                                train_thresholds=t)
        self.assertEqual(stats["forecast_rows"], 4)
        self.assertEqual(stats["direction_accuracy_all"], .75)
        self.assertEqual(stats["signal_coverage"], .75)
        self.assertEqual(stats["n_flat_actual"], 1)
        self.assertEqual(stats["n_predicted_down"], 2)
        self.assertEqual(sum(v["count"] for v in
                             stats["direction_by_predicted_magnitude"].values()), 4)
        self.assertTrue(stats["not_cumulative_portfolio_return"])
        self.assertTrue(stats["no_trading_costs"])

    def test_explicit_always_up_down_no_skill_baselines(self):
        dev = [make_case(2023, i) for i in range(40)]
        forecasts = baseline_forecasts(dev)
        self.assertIn("always_up_1bp", forecasts)
        self.assertIn("always_down_1bp", forecasts)
        self.assertTrue(all(f > c.anchor_usd for f,c in
                            zip(forecasts["always_up_1bp"], dev)))
        self.assertTrue(all(f < c.anchor_usd for f,c in
                            zip(forecasts["always_down_1bp"], dev)))

    def test_persistence_not_falsely_called_directional(self):
        t = training_magnitude_thresholds(
            [make_case(2018, i) for i in range(40)])
        s = score_forecasts([100,100,100], [101,99,100],
                            [100,100,100], train_thresholds=t)
        self.assertEqual(s["signal_coverage"], 0)
        self.assertIsNone(s["direction_accuracy_when_signaled"])
        self.assertEqual(s["direction_accuracy_all"], 1/3)

    def test_metric_rejects_nonfinite_and_bad_training_threshold(self):
        t = training_magnitude_thresholds(
            [make_case(2018, i) for i in range(40)])
        with self.assertRaises(ValueError):
            score_forecasts([100], [101], [math.nan], train_thresholds=t)
        with self.assertRaises(ValueError):
            score_forecasts([100], [101], [101], train_thresholds={
                "q50_bps": 1, "q75_bps": 3, "thresholds_trained_only": False
            })
        with self.assertRaises(ValueError):
            training_magnitude_thresholds([make_case(2018, 1)])

    def test_history_runner_fixture_origin_and_holdout_guard(self):
        train = [make_case(2018, i) for i in range(40)]
        dev = [make_case(2023, i) for i in range(36)]
        r = run_cases(
            train, dev, interval="H1", targets=(2400,),
            depths=(1,), architectures=("modern_gpt_style_mini",),
            steps=1, seeds=(11,), data_origin="ARTIFICIAL_FIXTURE",
        )
        self.assertEqual(len(r["results"]), 1)
        self.assertEqual(r["data_origin"], "ARTIFICIAL_FIXTURE")
        self.assertTrue(r["synthesized_or_mocked_data"])
        self.assertFalse(r["independent_test_used"])
        self.assertFalse(r["labels_2026_opened"])
        self.assertEqual(r["development_cases"], 36)
        self.assertTrue(math.isfinite(r["results"][0]["development_nll"]))
        with self.assertRaises(ValueError):
            run_cases(train, [make_case(2026, i) for i in range(24)],
                      interval="H1", targets=(2400,), depths=(1,),
                      architectures=("modern_gpt_style_mini",),
                      steps=1, seeds=(11,))


if __name__ == "__main__":
    unittest.main()
