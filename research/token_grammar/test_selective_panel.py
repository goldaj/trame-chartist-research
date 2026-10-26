"""S3.1G conditional-forecast paired panel integrity on fabricated samples."""
from copy import deepcopy
import unittest
from research.token_grammar.test_predictive import cases
from research.token_grammar.selective_forecast import run_cases
from research.token_grammar.selective_panel import panel,markdown

class ConditionalPanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.experiment=run_cases(
            cases(2018)+cases(2019),cases(2020)+cases(2021),
            interval="H1",seeds=(5,),training_steps=2)
    def test_one_model_twelve_coverage_rule_cells(self):
        report=panel([self.experiment],seeds=(5,),steps=2)
        self.assertEqual(report["n_models_trained"],1)
        self.assertEqual(report["n_threshold_price_rule_scores"],12)
        self.assertEqual(len(report["summary"]),12)
        self.assertEqual(len(report["paired_deltas"]),8)
        self.assertTrue(report["same_selected_cases_all_rules"])
        self.assertTrue(report["thresholds_train_predictions_only"])
        self.assertIn("Persistance bps même cas",markdown(report))
        self.assertFalse(report["external_dev_2022_2025_opened"])
        self.assertFalse(report["holdout_2026_opened"])

    def test_refuse_leakage_threshold_drift_and_selected_sample_fraud(self):
        for field,wrong in (
            ("external_2022_2025_used",True),
            ("holdout_2026_used",True),
            ("only_train_predictions_define_cutoffs",False),
            ("same_rules_same_selected_subset",False),
        ):
            if field not in self.experiment: continue
            changed=deepcopy(self.experiment)
            changed[field]=wrong
            with self.assertRaises(ValueError):
                panel([changed],seeds=(5,),steps=2)
        sample=deepcopy(self.experiment)
        sample["results"][0]["selection_sha256"]="0"*64
        with self.assertRaises(ValueError):
            panel([sample],seeds=(5,),steps=2)
        sample=deepcopy(self.experiment)
        sample["results"][0]["threshold_train_bps"]+=.1
        with self.assertRaises(ValueError):
            panel([sample],seeds=(5,),steps=2)
        sample=deepcopy(self.experiment)
        sample["results"].pop()
        with self.assertRaises(ValueError):
            panel([sample],seeds=(5,),steps=2)
        sample=deepcopy(self.experiment)
        sample["results"][0]["mae_bps_anchor"]=float("nan")
        with self.assertRaises(ValueError):
            panel([sample],seeds=(5,),steps=2)
        sample=deepcopy(self.experiment)
        sample["results"][0]["balanced_direction_accuracy"]=None
        sample["results"][0]["status"]="INSUFFICIENT_COVERAGE_OR_CLASS"
        with self.assertRaises(ValueError):
            panel([sample],seeds=(5,),steps=2)

if __name__=="__main__":
    unittest.main()
