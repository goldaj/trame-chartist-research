"""Causality, differentiability and pairing on purely artificial data."""
import unittest

import torch

from research.architecture_comparison.experiment import ARMS, compare, choose_widths


class ComparisonTests(unittest.TestCase):
    def test_all_arms_ignore_future_inputs(self):
        for name, factory in ARMS.items():
            with self.subTest(name=name):
                torch.manual_seed(2026)
                model = factory(width=16).eval()
                x = torch.arange(20, dtype=torch.float64)[None, :].repeat(2, 1)
                changed = x.clone()
                changed[:, 10:] += 100.0
                with torch.no_grad():
                    before = model(x)
                    after = model(changed)
                for a, b in zip(before, after):
                    torch.testing.assert_close(a[:, :10], b[:, :10], atol=1e-10, rtol=1e-10)

    def test_all_arms_have_finite_backward(self):
        for name, factory in ARMS.items():
            with self.subTest(name=name):
                torch.manual_seed(42)
                model = factory(width=16)
                x = torch.zeros((2, 8), dtype=torch.float64)
                y = torch.ones_like(x)
                loss = model.nll(x, y)
                self.assertTrue(bool(torch.isfinite(loss)))
                loss.backward()
                self.assertTrue(all(p.grad is not None and bool(torch.isfinite(p.grad).all())
                                    for p in model.parameters()))

    def test_compare_dev_only_and_deterministic_losses(self):
        one = compare(steps=2, seeds=(9,))
        two = compare(steps=2, seeds=(9,))
        self.assertEqual(len(one['results']), 3)
        self.assertFalse(one['reserved_synthetic_test_opened'])
        self.assertEqual(one['split_used'], ['train', 'development'])
        self.assertFalse(one['compute_matched'])
        for a, b in zip(one['results'], two['results']):
            self.assertEqual(a['architecture'], b['architecture'])
            self.assertAlmostEqual(a['end_development_nll'], b['end_development_nll'], places=9)
            self.assertGreater(a['parameter_count'], 0)

    def test_nearest_parameter_capacity_is_not_compute_fair(self):
        info=choose_widths()
        self.assertTrue(info['all_within_10_percent'])
        self.assertFalse(info['compute_matched'])
        self.assertEqual(info['selected']['legacy_causal_transformer']['width'],16)
        self.assertEqual(info['selected']['recurrent_gru_control']['width'],20)

    def test_invalid_compare_settings(self):
        for kwargs in ({'steps':0}, {'steps':201}, {'steps':True},
                       {'seeds':()}, {'seeds':(1,1)}, {'seeds':(False,)}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                compare(**kwargs)


if __name__ == '__main__':
    unittest.main()
