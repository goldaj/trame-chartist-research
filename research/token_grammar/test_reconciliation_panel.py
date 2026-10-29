"""S3.1E paired-panel corruption tests, artificial cases only."""
from copy import deepcopy
import unittest
from research.token_grammar.test_predictive import cases
from research.token_grammar.reconciliation_loss import run_cases
from research.token_grammar.reconciliation_panel import panel,markdown


class ReconciliationPanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake=run_cases(
            cases(2018)+cases(2019),
            cases(2020)+cases(2021),
            interval="H1",seeds=(7,),checkpoints=(1,2))

    def test_three_complete_trajectories_and_six_evaluations(self):
        p=panel([self.fake],seeds=(7,),checkpoints=(1,2))
        self.assertEqual(p["n_distinct_trajectories"],3)
        self.assertEqual(p["n_checkpoint_observations"],6)
        self.assertEqual(len(p["summary"]),6)
        self.assertEqual(len(p["paired_deltas"]),4)
        self.assertTrue(p["hard_forecast_is_served"])
        self.assertTrue(p["soft_forecast_diagnostics_only"])
        self.assertTrue(p["same_capacity_all_arms"])
        self.assertFalse(p["holdout_2026_used"])
        self.assertIn("MAE bps SOFT",markdown(p))

    def test_rejects_wrong_loss_weights_or_unpaired_model(self):
        for key,val in (("external_2022_2025_used",True),
                        ("served_hard_sign_reconciliation_unchanged",False),
                        ("all_arms_same_parameter_count",False)):
            x=deepcopy(self.fake)
            x[key]=val
            with self.assertRaises(ValueError):
                panel([x],seeds=(7,),checkpoints=(1,2))
        x=deepcopy(self.fake)
        x["results"][0]["reconciled_surrogate_weight"]=999
        with self.assertRaises(ValueError):
            panel([x],seeds=(7,),checkpoints=(1,2))
        x=deepcopy(self.fake)
        x["results"].pop()
        with self.assertRaises(ValueError):
            panel([x],seeds=(7,),checkpoints=(1,2))
        x=deepcopy(self.fake)
        x["results"][0]["backbone_initial_sha256"]="0"*64
        with self.assertRaises(ValueError):
            panel([x],seeds=(7,),checkpoints=(1,2))
        x=deepcopy(self.fake)
        x["results"][0]["parameter_count"]+=1
        with self.assertRaises(ValueError):
            panel([x],seeds=(7,),checkpoints=(1,2))


if __name__=="__main__":
    unittest.main()
