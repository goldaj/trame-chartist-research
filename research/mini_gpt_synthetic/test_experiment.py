"""Guardrails for exploratory research; never access reserved test."""
import math
import unittest

from research.mini_gpt_synthetic.experiment import run, baselines
from research.mini_gpt_synthetic.data import get_split


class ExperimentTests(unittest.TestCase):
    def test_strong_controls_and_no_reserved_test(self):
        train=get_split('train')
        development=get_split('development')
        score=baselines(train,development)
        self.assertTrue(math.isfinite(score['oracle_known_generator_nll']))
        self.assertTrue(math.isfinite(score['linear_train_only_nll']))
        self.assertTrue(math.isfinite(score['constant_mu0_train_scale_nll']))
        self.assertEqual(score['linear_parameters']['fitted_on'],'train_only')
        with self.assertRaises(PermissionError):
            get_split('reserved_synthetic_test')

    def test_short_training_is_finite_reproducible_and_unlocked_only_on_dev(self):
        report=run(steps=2,seed=20261025)
        self.assertTrue(report['reserved_test_not_opened'])
        self.assertTrue(report['not_full_p1b0'])
        self.assertTrue(math.isfinite(report['start_development_nll']))
        self.assertTrue(math.isfinite(report['end_development_nll']))
        self.assertGreater(report['model_parameters'],0)


if __name__=='__main__':
    unittest.main()
