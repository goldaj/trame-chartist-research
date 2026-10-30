"""S3.1B five-way comparison synthetic tests."""
from copy import deepcopy
import unittest

from research.token_grammar.test_predictive import cases
from research.token_grammar.embedding_runner import run_cases
from research.token_grammar.embedding_panel import build_panel,to_markdown


class TestEmbeddingPanel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run_cases(cases(2018),cases(2023),interval="H1",
            widths=(16,),depths=(1,),modes=("regression","joint"),
            seeds=(8,9),steps=1)

    def test_full_paired_5_arm_comparison(self):
        result=build_panel([self.report])
        self.assertEqual(result["n_fits"],20)
        self.assertEqual(result["n_paired_groups"],4)
        self.assertEqual(len(result["summary"]),10)
        self.assertEqual(len(result["paired_deltas"]),8)
        for r in result["summary"]:
            self.assertEqual(r["n_fits"],2)
            self.assertEqual(r["unique_seeds"],2)
        text=to_markdown(result)
        self.assertIn("Erreur amplitude bps",text)
        self.assertIn("Monoclasse",text)

    def test_rejects_incomplete_misaligned_or_2026(self):
        bad=deepcopy(self.report)
        bad["results"].pop()
        with self.assertRaisesRegex(ValueError,"all five"):
            build_panel([bad])
        bad=deepcopy(self.report)
        bad["results"][1]["initial_state_sha256"]="a"*64
        with self.assertRaisesRegex(ValueError,"mismatched"):
            build_panel([bad])
        bad=deepcopy(self.report)
        bad["results"][1]["parameter_count"]+=1
        with self.assertRaisesRegex(ValueError,"mismatched"):
            build_panel([bad])
        bad=deepcopy(self.report)
        bad["labels_2026_opened"]=True
        with self.assertRaises(ValueError):
            build_panel([bad])
        bad=deepcopy(self.report)
        bad["results"].append(deepcopy(bad["results"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            build_panel([bad])


if __name__=="__main__":
    unittest.main()
