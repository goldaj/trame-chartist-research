"""A5 CPU hybrid controls and adversarial checks."""
import json
import unittest

import torch
from torch import nn

from research.hybrid_controls.contract import verify_sequence_backbone
from research.hybrid_controls.models import AttentionGRUHybrid
from research.hybrid_controls.experiment import compare_hybrid


class BadFutureMean(nn.Module):
    def forward(self, x):
        return x.mean(dim=1, keepdim=True).expand_as(x)


class HybridControlsTests(unittest.TestCase):
    def test_contract_rejects_obvious_future_leak(self):
        x = torch.arange(64, dtype=torch.float64)[None, :, None].repeat(2, 1, 16)
        with self.assertRaisesRegex(ValueError, "future"):
            verify_sequence_backbone(BadFutureMean(), x)

    def test_hybrid_prefix_causality_and_gradients_64(self):
        torch.manual_seed(777)
        net = AttentionGRUHybrid(width=16, length=64)
        features = torch.randn((2, 64, 16), dtype=torch.float64)
        outcome = verify_sequence_backbone(net.encode, features)
        self.assertTrue(outcome["causal_prefix_perturbation_passed"])
        x = torch.randn((2, 64), dtype=torch.float64)
        target = torch.zeros_like(x)
        loss = net.nll(x, target)
        self.assertTrue(bool(torch.isfinite(loss)))
        loss.backward()
        self.assertTrue(all(p.grad is not None and bool(torch.isfinite(p.grad).all())
                            for p in net.parameters()))

    def test_paired_synthetic_four_arms(self):
        out = compare_hybrid(steps=2, seeds=(42, 43, 44))
        self.assertEqual(out["data_origin"], "ARTIFICIAL_ONLY")
        self.assertFalse(out["hybrid_is_selective_ssm"])
        self.assertFalse(out["compute_matched"])
        self.assertFalse(out["reserved_synthetic_test_opened"])
        self.assertEqual(len(out["results"]), 12)
        self.assertEqual(len({r["architecture"] for r in out["results"]}), 4)
        json.dumps(out, allow_nan=False)

    def test_reject_invalid_seeds(self):
        with self.assertRaises(ValueError):
            compare_hybrid(steps=2, seeds=(1, 1, 2))
        with self.assertRaises(ValueError):
            compare_hybrid(steps=True, seeds=(1, 2, 3))


if __name__ == "__main__":
    unittest.main()
