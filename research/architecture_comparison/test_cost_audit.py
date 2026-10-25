"""Synthetic-only hardware diagnostic invariants; don't assert timing ranks."""
import unittest
from research.architecture_comparison.cost_audit import cost_audit


class CostAuditTests(unittest.TestCase):
    def test_synthetic_cost_audit(self):
        report=cost_audit(widths=(8,),repeats=3)
        self.assertTrue(report['not_fair_flops_comparison'])
        self.assertFalse(report['reserved_synthetic_test_opened'])
        self.assertEqual(len(report['results']),3)
        for row in report['results']:
            self.assertEqual(row['width'],8)
            self.assertGreater(row['parameters'],0)
            self.assertGreater(row['median_forward_ms'],0)
            self.assertGreater(row['median_forward_backward_ms'],0)

    def test_invalid_controls(self):
        for kwargs in ({'widths':()}, {'widths':(8,8)}, {'widths':(7,)},
                       {'repeats':2}, {'repeats':True}, {'seed':True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                cost_audit(**kwargs)


if __name__=='__main__':
    unittest.main()
