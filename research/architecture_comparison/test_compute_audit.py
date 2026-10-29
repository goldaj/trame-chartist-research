"""A3c CPU accounting tests: protect epistemic limits and reserved split."""
import json
import unittest

from research.architecture_comparison.compute_audit import compute_audit


class ComputeAuditTests(unittest.TestCase):
    def test_three_families_same_synthetic_workload(self):
        result = compute_audit(widths=(8,), contexts=(8,), repeats=3,
                               batch_size=3)
        self.assertEqual(result["data_origin"], "ARTIFICIAL_COST_ONLY")
        self.assertFalse(result["reserved_synthetic_test_opened"])
        self.assertTrue(result["cost_only_inputs_generated_from_seed"])
        self.assertFalse(result["financial_holdout_opened"])
        self.assertFalse(result["compute_matched"])
        self.assertFalse(result["flops_matched"])
        self.assertFalse(result["flops_coverage_complete"])
        self.assertEqual(len(result["results"]), 3)
        self.assertEqual(len({x["architecture"] for x in result["results"]}), 3)
        for row in result["results"]:
            self.assertEqual(row["context_tokens"], 8)
            self.assertEqual(row["width"], 8)
            self.assertEqual(row["batch_size"], 3)
            self.assertGreater(row["parameter_count"], 0)
            self.assertGreater(row["forward_median_ms_unprofiled"], 0)
            self.assertGreater(row["train_step_median_ms_unprofiled"], 0)
            for key in ("forward_profiler", "train_profiler"):
                p = row[key]
                self.assertFalse(p["flops_coverage_complete"])
                self.assertFalse(p["memory_is_process_peak"])
                self.assertGreater(p["profiler_event_types"], 0)
                self.assertGreaterEqual(p["accounted_flops_lower_bound"], 0)
        json.dumps(result, allow_nan=False)

    def test_long_context_all_families(self):
        import torch
        from research.architecture_comparison.experiment import ARMS
        for name, factory in ARMS.items():
            with self.subTest(architecture=name):
                model = factory(width=8, length=64).eval()
                x = torch.arange(64, dtype=torch.float64).remainder(7)[None]
                mutated = x.clone()
                mutated[:, 32:] += 50
                with torch.no_grad():
                    before = model(x)
                    after = model(mutated)
                for a, b in zip(before, after):
                    torch.testing.assert_close(a[:, :32], b[:, :32],
                                               atol=1e-10, rtol=1e-10)
                model.train()
                model.nll(x, x).backward()
                self.assertTrue(all(p.grad is not None and bool(torch.isfinite(p.grad).all())
                                    for p in model.parameters()))

    def test_invalid_choices(self):
        cases = [
            {"widths": ()}, {"widths": (8, 8)}, {"widths": (7,)},
            {"widths": (8.0,)}, {"contexts": ()}, {"contexts": (8, 8)},
            {"contexts": (21,)}, {"contexts": (256,)}, {"repeats": 2}, {"repeats": True},
            {"seed": True}, {"batch_size": 1}, {"batch_size": True},
        ]
        for kwargs in cases:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                compute_audit(**kwargs)


if __name__ == "__main__":
    unittest.main()
