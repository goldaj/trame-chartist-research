"""S3.1B aggregate integrity on artificial cases, no BTC downloads."""
from copy import deepcopy
import math
import unittest
from research.token_grammar.test_predictive import cases
from research.token_grammar.learned_embeddings import run_cases
from research.token_grammar.learned_embeddings_panel import panel,markdown


class PanelChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample=run_cases(
            cases(2018),cases(2023),interval="H1",
            modes=("joint",),widths=(16,),depths=(1,),
            seeds=(7,8),steps=1)

    def test_all_three_arms_required_and_parameters_disclosed(self):
        p=panel([self.sample])
        self.assertEqual(p["n_fits"],12)
        self.assertEqual(p["n_three_arm_groups"],4)
        self.assertEqual(len(p["summary"]),6)
        self.assertEqual(len(p["paired_deltas"]),6)
        self.assertTrue(p["learned_vs_numeric_parameter_confounded"])
        self.assertTrue(p["ordered_vs_random_parameter_matched"])
        for row in p["paired_deltas"]:
            self.assertEqual(row["n_paired_fits"],2)
            self.assertTrue(math.isfinite(row["balanced_direction_accuracy_delta"]["mean"]))
            if row["reference_arm"]=="embedding_random":
                self.assertTrue(row["exact_parameter_match"])
            else:
                self.assertFalse(row["exact_parameter_match"])
        self.assertIn("MAE USD",markdown(p))
        self.assertIn("Monoclasse",markdown(p))

    def test_rejects_missing_model_capacity_fraud_and_holdout(self):
        r=deepcopy(self.sample)
        r["results"].pop()
        with self.assertRaisesRegex(ValueError,"incomplete"):
            panel([r])
        r=deepcopy(self.sample)
        r["results"][0]["parameter_count"]+=1
        with self.assertRaisesRegex(ValueError,"capacity"):
            panel([r])
        r=deepcopy(self.sample)
        r["results"][2]["backbone_initial_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"backbone"):
            panel([r])
        r=deepcopy(self.sample)
        r["labels_2026_opened"]=True
        with self.assertRaises(ValueError):
            panel([r])
        r=deepcopy(self.sample)
        r["results"].append(deepcopy(r["results"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            panel([r])


if __name__=="__main__":
    unittest.main()
