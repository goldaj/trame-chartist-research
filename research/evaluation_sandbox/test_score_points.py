import unittest

try:
    from .score_points import validate_and_score
except ImportError:
    from score_points import validate_and_score


class ScoreTests(unittest.TestCase):
    def record(self, **updates):
        row = dict(asset="DEMO", origin_index=10, target_index=11, horizon=1,
                   anchor=100.0, actual=110.0, forecast=109.0)
        row.update(updates)
        return row

    def test_persistence_comparison_and_native_units(self):
        report = validate_and_score([self.record()])
        group = report["groups"][0]
        self.assertEqual(group["forecast_mae_price_units"], 1.0)
        self.assertEqual(group["persistence_mae_price_units"], 10.0)
        self.assertEqual(group["paired_mae_gain_price_units"], 9.0)
        self.assertEqual(group["distinct_target_observations"], 1)
        self.assertTrue(report["not_independent_test_proof"])

    def test_missing_or_duplicate_rows_are_rejected(self):
        a = self.record()
        for rows in ([a, a], [dict(a, extra="x")], [], [{k:v for k,v in a.items() if k!="anchor"}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                validate_and_score(rows)

    def test_future_indices_and_non_numeric_prices(self):
        for update in ({"target_index": 10}, {"target_index": 12},
                       {"horizon": 0}, {"horizon": True},
                       {"actual": float("nan")}, {"forecast": -1},
                       {"anchor": "100"}, {"actual": float("inf")}):
            with self.subTest(update=update), self.assertRaises(ValueError):
                validate_and_score([self.record(**update)])

    def test_horizons_are_not_naively_pooled(self):
        report = validate_and_score([
            self.record(), self.record(origin_index=11, target_index=12),
            self.record(horizon=2, target_index=12)])
        self.assertEqual(len(report["groups"]), 2)
        self.assertEqual(report["groups"][0]["origins"], 2)
        self.assertEqual(report["groups"][1]["origins"], 1)

    def test_assets_not_pooled_into_price_units(self):
        report = validate_and_score([
            self.record(), self.record(asset="OTHER", anchor=1, actual=1.1, forecast=1.09)])
        self.assertEqual(len(report["groups"]), 2)
        self.assertEqual(report["groups"][0]["asset"], "DEMO")

    def test_horizon_validation_detects_noncausal_target(self):
        with self.assertRaisesRegex(ValueError, "future target"):
            validate_and_score([self.record(origin_index=100, target_index=99)])


if __name__ == "__main__":
    unittest.main()
