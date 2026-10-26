"""S2 calibration diagnostics only on fabricated price labels."""
import math
import unittest
from dataclasses import replace

import numpy as np

from research.continuous_direction.diagnostics import prior_from_train, probability_report
from research.continuous_direction.test_continuous import fabricated_case
from research.continuous_direction.runner import run_cases, _origin_digest


class DiagnosticTests(unittest.TestCase):
    def test_smoothed_prior_and_no_development_label_fitting(self):
        train=[fabricated_case(2018,i) for i in range(40)]
        dev=[fabricated_case(2023,i) for i in range(40)]
        prior=prior_from_train(train)
        self.assertTrue(prior["prior_fit_on_training_only"])
        self.assertGreater(prior["p_up"],0)
        self.assertLess(prior["p_up"],1)
        original=probability_report(
            [x.anchor_usd for x in dev], [x.target_usd for x in dev],
            np.full(len(dev),prior["p_up"]),train_prior=prior)
        self.assertAlmostEqual(original["brier_skill_vs_train_prior"],0.0)
        self.assertAlmostEqual(original["binary_ce_delta_vs_train_prior"],0.0)
        self.assertEqual(sum(x["count"] for x in original["reliability_bins"]),
                         original["nonflat_probability_cases"])
        changed=[replace(x,target_usd=x.anchor_usd*1.1) for x in dev]
        self.assertEqual(prior,prior_from_train(train))
        changed_score=probability_report(
            [x.anchor_usd for x in changed], [x.target_usd for x in changed],
            np.full(len(changed),prior["p_up"]),train_prior=prior)
        self.assertEqual(changed_score["train_only_prior_up"],prior["p_up"])

    def test_flat_dev_and_invalid_probabilities_do_not_invent_brier(self):
        train=[fabricated_case(2018,i) for i in range(40)]
        prior=prior_from_train(train)
        report=probability_report([100,100],[100,100],[0.4,0.6],
                                  train_prior=prior)
        self.assertIsNone(report["brier_nonflat"])
        self.assertEqual(report["flat_probability_cases_excluded"],2)
        with self.assertRaises(ValueError):
            probability_report([100],[101],[float("nan")],train_prior=prior)
        with self.assertRaises(ValueError):
            probability_report([100],[101],[1.1],train_prior=prior)
        with self.assertRaises(ValueError):
            probability_report([100],[101],[0.8],
                               train_prior={"p_up":0.6})

    def test_case_origin_digest_is_label_blind_and_order_sensitive(self):
        values=[fabricated_case(2018,i) for i in range(40)]
        canonical=_origin_digest(values)
        changed_labels=[replace(x,target_usd=x.target_usd*1.01) for x in values]
        self.assertEqual(_origin_digest(changed_labels),canonical)
        self.assertNotEqual(_origin_digest(list(reversed(values))),canonical)
        self.assertEqual(len(canonical),64)

    def test_runner_reports_untrained_regression_logit_as_unavailable(self):
        train=[fabricated_case(2018,i) for i in range(40)]
        dev=[fabricated_case(2023,i) for i in range(40)]
        report=run_cases(train,dev,interval="D1",widths=(16,),depths=(1,),
                         modes=("regression","joint"),steps=1,seeds=(3,))
        self.assertEqual(len(report["results"]),2)
        self.assertTrue(report["direction_class_prior_train_only"]
                        ["prior_fit_on_training_only"])
        self.assertIn("model_source_commit",report)
        self.assertEqual(len(report["development_origins_sha256"]),64)
        self.assertIsNone(report["approved_private_release_tag"])
        by_mode={row["mode"]:row for row in report["results"]}
        self.assertIsNone(by_mode["regression"]["brier_nonflat"])
        self.assertFalse(by_mode["regression"]
                         ["binary_probabilities_from_trained_head"])
        self.assertIsInstance(by_mode["joint"]["brier_nonflat"],float)
        self.assertTrue(by_mode["joint"]["binary_probabilities_from_trained_head"])
        self.assertTrue(math.isfinite(by_mode["joint"]
                                      ["brier_skill_vs_train_prior"]))


if __name__ == "__main__":
    unittest.main()
