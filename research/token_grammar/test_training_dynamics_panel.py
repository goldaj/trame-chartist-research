"""S3.1C report adversarial fixture tests. No public/private BTC fetch."""
from copy import deepcopy
import unittest
from research.token_grammar.test_predictive import cases
from research.token_grammar.training_dynamics import run_cases
from research.token_grammar.training_dynamics_panel import summarise,markdown


class ConvergencePanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake=run_cases(
            cases(2018)+cases(2019),cases(2020)+cases(2021),
            interval="D1",seeds=(11,),checkpoints=(1,2))

    def test_three_trajectories_are_not_six_independent_models(self):
        report=summarise([self.fake],checkpoints=(1,2),seeds=(11,))
        self.assertEqual(report["n_distinct_trajectories"],3)
        self.assertEqual(report["n_checkpoint_evaluations"],6)
        self.assertEqual(len(report["summary"]),6)
        self.assertFalse(report["external_dev_2022_2025_opened"])
        self.assertFalse(report["labels_2026_opened"])
        self.assertIn("MAE bps",markdown(report))

    def test_refuse_embargo_break_incomplete_trajectories_and_bad_params(self):
        bad=deepcopy(self.fake)
        bad["external_dev_2022_2025_opened"]=True
        with self.assertRaises(ValueError):
            summarise([bad],checkpoints=(1,2),seeds=(11,))
        bad=deepcopy(self.fake)
        bad["evaluations"].pop()
        with self.assertRaisesRegex(ValueError,"missing checkpoints"):
            summarise([bad],checkpoints=(1,2),seeds=(11,))
        bad=deepcopy(self.fake)
        bad["evaluations"][0]["parameter_count"]+=1
        with self.assertRaisesRegex(ValueError,"capacity"):
            summarise([bad],checkpoints=(1,2),seeds=(11,))
        bad=deepcopy(self.fake)
        bad["evaluations"][1]["backbone_initial_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"backbone"):
            summarise([bad],checkpoints=(1,2),seeds=(11,))
        bad=deepcopy(self.fake)
        bad["checkpoints"]=[1,2,100]
        with self.assertRaises(ValueError):
            summarise([bad],checkpoints=(1,2),seeds=(11,))


if __name__=="__main__":
    unittest.main()
