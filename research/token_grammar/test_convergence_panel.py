"""S3.1C paired monitor audit validation on fabricated small histories only."""
from copy import deepcopy
import math
import unittest
from research.token_grammar.test_predictive import cases
from research.token_grammar.convergence import run_cases
from research.token_grammar.convergence_panel import build_panel,markdown


class TestMonitorPanel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample=run_cases(cases(2018),cases(2020),
             interval="D1",seeds=(7,8),checkpoints=(2,4),
             data_origin="ARTIFICIAL_FIXTURE")

    def test_6_trajectories_12_checkpoints(self):
        p=build_panel([self.sample])
        self.assertEqual(p["n_trajectories"],6)
        self.assertEqual(p["n_checkpoint_rows"],12)
        self.assertEqual(len(p["summary"]),6)
        self.assertEqual(len(p["paired_deltas"]),4)
        self.assertFalse(p["external_2022_2025_used"])
        for row in p["summary"]:
            self.assertEqual(row["n_fits"],2)
            self.assertTrue(math.isfinite(row["train_monitor_loss"]["mean"]))
            self.assertTrue(math.isfinite(row["internal_validation_monitor_loss"]["mean"]))
        self.assertIn("Brier skill",markdown(p))

    def test_rejects_incomplete_models_wrong_backbone_or_2026(self):
        broken=deepcopy(self.sample)
        broken["results"].pop()
        with self.assertRaisesRegex(ValueError,"incomplete"):
            build_panel([broken])
        broken=deepcopy(self.sample)
        broken["results"][0]["backbone_initial_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"backbone"):
            build_panel([broken])
        broken=deepcopy(self.sample)
        broken["results"][0]["parameter_count"]+=1
        with self.assertRaisesRegex(ValueError,"capacity"):
            build_panel([broken])
        broken=deepcopy(self.sample)
        broken["external_development_2022_2025_accessed"]=True
        with self.assertRaises(ValueError):
            build_panel([broken])
        with self.assertRaisesRegex(ValueError,"duplicate"):
            build_panel([self.sample,self.sample])


if __name__=="__main__":
    unittest.main()
