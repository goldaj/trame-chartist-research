"""S3.1F strict same-model panel integrity tests on artificial returns."""
from copy import deepcopy
import unittest
from research.token_grammar.test_predictive import cases
from research.token_grammar.inference_ablation import run_cases
from research.token_grammar.inference_panel import panel,markdown

class InferencePanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=run_cases(
            cases(2018)+cases(2019),cases(2020)+cases(2021),
            interval="D1",seeds=(11,),checkpoints=(1,2))

    def test_three_rule_reports_not_mistaken_for_three_models(self):
        p=panel([self.fixture],seeds=(11,),checkpoints=(1,2))
        self.assertEqual(p["n_models_trained"],1)
        self.assertEqual(p["n_distinct_checkpoints"],2)
        self.assertEqual(p["n_rule_evaluations"],6)
        self.assertEqual(len(p["summary"]),6)
        self.assertEqual(len(p["paired_deltas"]),4)
        self.assertTrue(p["hard_rule_exactly_previous_served_model"])
        self.assertIn("MAE bps",markdown(p))

    def test_rejects_time_leakage_extra_models_and_mismatched_rules(self):
        for attr,new in (("external_dev_2022_2025_accessed",True),
                         ("holdout_2026_accessed",True),
                         ("one_model_shared_by_three_pricing_rules",False),
                         ("hard_reproduces_existing_forecast_prices_exactly",False)):
            x=deepcopy(self.fixture)
            x[attr]=new
            with self.assertRaises(ValueError):
                panel([x],seeds=(11,),checkpoints=(1,2))
        x=deepcopy(self.fixture)
        x["results"].pop()
        with self.assertRaises(ValueError):
            panel([x],seeds=(11,),checkpoints=(1,2))
        x=deepcopy(self.fixture)
        x["results"][0]["parameter_count"]+=1
        with self.assertRaises(ValueError):
            panel([x],seeds=(11,),checkpoints=(1,2))
        x=deepcopy(self.fixture)
        x["results"][0]["head_brier_score"]+=0.01
        with self.assertRaises(ValueError):
            panel([x],seeds=(11,),checkpoints=(1,2))
        x=deepcopy(self.fixture)
        x["trajectories"].append(deepcopy(x["trajectories"][0]))
        with self.assertRaises(ValueError):
            panel([x],seeds=(11,),checkpoints=(1,2))

if __name__=="__main__":
    unittest.main()
