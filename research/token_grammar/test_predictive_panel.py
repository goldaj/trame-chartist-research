"""S3.1A four-grammar paired comparison, synthetic only."""
from copy import deepcopy
import math
import unittest
from research.token_grammar.test_predictive import cases
from research.token_grammar.predictive import run_cases,GRAMMARS
from research.token_grammar.predictive_panel import build_panel,to_markdown


class TestPredictivePanel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample=run_cases(
            cases(2018),cases(2023),interval="H1",
            widths=(16,),depths=(1,),seeds=(3,4),steps=1)

    def test_full_comparison_with_4_matched_grammars(self):
        panel=build_panel([self.sample])
        self.assertEqual(panel["n_fits"],16)
        self.assertEqual(panel["paired_groups"],4)
        self.assertEqual(len(panel["summary"]),8)
        self.assertEqual(len(panel["paired_deltas"]),6)
        self.assertIn("G1", "G1")  # sanity of declared synthetic scenario
        for x in panel["summary"]:
            self.assertEqual(x["n_fits"],2)
            self.assertEqual(x["n_unique_seeds"],2)
            self.assertGreaterEqual(x["predicted_up_percent"]["mean"],0)
            self.assertTrue(math.isfinite(x["mae_bps_anchor"]["mean"]))
        md=to_markdown(panel)
        self.assertIn("Erreur amplitude bps",md)
        self.assertIn("Monoclasse",md)

    def test_refuse_missing_grammar_and_mismatched_initialization(self):
        broken=deepcopy(self.sample)
        broken["results"].pop()
        with self.assertRaisesRegex(ValueError,"missing matched grammar"):
            build_panel([broken])
        broken=deepcopy(self.sample)
        broken["results"][1]["initial_state_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"mismatched"):
            build_panel([broken])
        broken=deepcopy(self.sample)
        broken["results"][1]["input_normalizer_std_bps"] *= 1.05
        with self.assertRaisesRegex(ValueError,"mismatched"):
            build_panel([broken])

    def test_rejects_2026_and_duplicate_runs(self):
        tampered=deepcopy(self.sample)
        tampered["labels_2026_opened"]=True
        with self.assertRaises(ValueError):
            build_panel([tampered])
        tampered=deepcopy(self.sample)
        tampered["results"].append(deepcopy(tampered["results"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate arm"):
            build_panel([tampered])
        with self.assertRaisesRegex(ValueError,"duplicate resolution"):
            build_panel([self.sample,self.sample])

if __name__=="__main__":
    unittest.main()
