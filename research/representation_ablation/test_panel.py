"""S2b comparison panel fixtures only."""
import copy
import math
import unittest

from research.representation_ablation.runner import run_cases
from research.representation_ablation.panel import build_panel, to_markdown
from research.continuous_direction.test_continuous import fabricated_case


class PanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        train=[fabricated_case(2018,i) for i in range(40)]
        dev=[fabricated_case(2023,i) for i in range(40)]
        cls.sample=run_cases(
            train,dev,interval="H1",widths=(16,),depths=(1,),
            seeds=(5,6),steps=1)

    def test_paired_report_preserves_direction_and_amount(self):
        panel=build_panel([self.sample])
        self.assertEqual(panel["n_fits"],8)
        self.assertEqual(len(panel["groups"]),2)
        for row in panel["groups"]:
            self.assertEqual(row["n_seeds"],2)
            self.assertTrue(math.isfinite(
                row["balanced_direction_accuracy_delta_continuous_minus_quantized"]["mean"]))
            self.assertTrue(math.isfinite(
                row["mae_bps_anchor_delta_continuous_minus_quantized"]["mean"]))
            self.assertEqual(row["seeds"],[5,6])
        text=to_markdown(panel)
        self.assertIn("Δ balanced",text)
        self.assertIn("Δ amplitude",text)

    def test_rejects_incomplete_or_unpaired_arms(self):
        sample=copy.deepcopy(self.sample)
        sample["results"].pop()
        with self.assertRaisesRegex(ValueError,"BOTH paired"):
            build_panel([sample])
        sample=copy.deepcopy(self.sample)
        sample["results"][1]["initial_state_sha256"]="a"*64
        with self.assertRaisesRegex(ValueError,"matched initialization"):
            build_panel([sample])

    def test_rejects_tampering_holdout_and_duplicate_seed(self):
        sample=copy.deepcopy(self.sample)
        sample["labels_2026_opened"]=True
        with self.assertRaises(ValueError):
            build_panel([sample])
        sample=copy.deepcopy(self.sample)
        sample["results"].append(copy.deepcopy(sample["results"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            build_panel([sample])
        with self.assertRaisesRegex(ValueError,"duplicate horizon"):
            build_panel([self.sample,self.sample])


if __name__=="__main__":
    unittest.main()
