"""S3.1D five-arm paired panel guardrails, fabricated data only."""
from copy import deepcopy
import unittest

from research.token_grammar.test_predictive import cases
from research.token_grammar.loss_ablation import run_cases
from research.token_grammar.loss_ablation_panel import panel,markdown


class LossPanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run_cases(
            cases(2018)+cases(2019),
            cases(2020)+cases(2021),
            interval="D1",seeds=(17,),checkpoints=(1,2))

    def test_all_five_losses_same_backbone_and_paired_checkpoints(self):
        p=panel([self.report],seeds=(17,),checkpoints=(1,2))
        self.assertEqual(p["n_distinct_trajectories"],5)
        self.assertEqual(p["n_checkpoint_observations"],10)
        self.assertEqual(len(p["summary"]),10)
        self.assertEqual(len(p["contrasts"]),8)
        self.assertTrue(p["same_capacity_all_loss_arms"])
        self.assertFalse(p["external_dev_2022_2025_used"])
        self.assertFalse(p["holdout_2026_used"])
        self.assertIn("MAE bps",markdown(p))

    def test_refuse_2022_access_malformed_objective_missing_arm_and_weights(self):
        modified=deepcopy(self.report)
        modified["external_2022_2025_used"]=True
        with self.assertRaises(ValueError):
            panel([modified],seeds=(17,),checkpoints=(1,2))
        modified=deepcopy(self.report)
        modified["results"].pop()
        with self.assertRaises(ValueError):
            panel([modified],seeds=(17,),checkpoints=(1,2))
        modified=deepcopy(self.report)
        modified["results"][0]["direction_weight"]*=10
        with self.assertRaises(ValueError):
            panel([modified],seeds=(17,),checkpoints=(1,2))
        modified=deepcopy(self.report)
        modified["results"][1]["parameter_count"]+=1
        with self.assertRaises(ValueError):
            panel([modified],seeds=(17,),checkpoints=(1,2))
        modified=deepcopy(self.report)
        modified["results"][1]["backbone_initial_sha256"]="0"*64
        with self.assertRaises(ValueError):
            panel([modified],seeds=(17,),checkpoints=(1,2))

if __name__=="__main__":
    unittest.main()
