"""A3c.4: conservative proxy-budget pilot tests."""
import json
import unittest

from research.architecture_comparison.budget_pilot import (
    allocate_steps, run_pilot,
)
from research.architecture_comparison.experiment import ARMS


class BudgetPilotTests(unittest.TestCase):
    def test_same_counted_ops_target_with_different_steps(self):
        names = list(ARMS)
        plan = allocate_steps(dict(zip(names, (100, 200, 50))),
                              reference_steps=12, step_cap=100)
        steps = [plan["arms"][n]["steps"] for n in names]
        self.assertEqual(steps, [12, 6, 24])
        self.assertTrue(plan["proxy_budget_within_10pct"])
        self.assertFalse(plan["true_compute_matched"])
        self.assertFalse(plan["flops_coverage_complete"])

    def test_capped_budget_never_claims_true_parity(self):
        plan = allocate_steps(dict(zip(ARMS, (100, 1000, 10))),
                              reference_steps=10, step_cap=20)
        self.assertFalse(plan["true_compute_matched"])
        self.assertFalse(plan["proxy_budget_within_10pct"])

    def test_strict_controls(self):
        valid = dict(zip(ARMS, (100, 200, 50)))
        for costs, kw in [
            ({}, {}), ({**valid, "other": 1}, {}), (dict(zip(ARMS, (100, 0, 50))), {}),
            (dict(zip(ARMS, (100, True, 50))), {}), (valid, {"reference_steps": True}),
            (valid, {"step_cap": 1}), (valid, {"step_cap": True}),
        ]:
            with self.subTest(costs=costs, params=kw), self.assertRaises(ValueError):
                allocate_steps(costs, **kw)

    def test_end_to_end_synthetic_no_holdout(self):
        out = run_pilot(seeds=(9, 10, 11), reference_steps=2, max_steps=4)
        self.assertEqual(out["data_origin"], "ARTIFICIAL_TRAIN_AND_DEVELOPMENT")
        self.assertFalse(out["reserved_synthetic_test_opened"])
        self.assertFalse(out["true_compute_matched"])
        self.assertFalse(out["tuning_compute_equalized"])
        self.assertEqual(out["seed_count"], 3)
        self.assertEqual(len(out["results"]), 9)
        self.assertEqual(len({r["architecture"] for r in out["results"]}), 3)
        for row in out["results"]:
            self.assertGreater(row["train_cpu_seconds"], 0)
            self.assertGreater(row["planned_partial_counted_ops"], 0)
        json.dumps(out, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
