"""S3.1A adversarial fixtures. Never access BTC datasets."""
from dataclasses import replace
from math import floor
import math
import unittest

import numpy as np

from research.continuous_direction.test_continuous import fabricated_case
from research.representation_ablation.runner import run_cases as s2b_run_cases
from research.token_grammar.predictive import (
    TrainOnlyGrammarFeatures,GRAMMARS,run_cases as s3_run_cases,
)


def cases(year):
    results=[]
    for i in range(40):
        c=fabricated_case(year,i)
        past=tuple(((-1)**(i+j))*(0.1+0.33*(j+i%7)+0.01*i)
                   for j in range(20))
        results.append(replace(c,continuous_past_bps=past,
            encoded_past=tuple(floor(v/10+0.5) for v in past)))
    return results


class GrammarPredictionTests(unittest.TestCase):
    def test_train_only_vocabulary_cannot_learn_development_extremes(self):
        train,dev=cases(2018),cases(2023)
        grammar=TrainOnlyGrammarFeatures(train)
        boundaries=grammar.quantile_boundaries_bps
        self.assertEqual(len(boundaries),4)
        x=grammar(dev,"signed_quantile_g2")
        extreme=[replace(c,continuous_past_bps=tuple(1e8 for _ in range(20)))
                 for c in dev]
        y=grammar(extreme,"signed_quantile_g2")
        self.assertEqual(boundaries,grammar.quantile_boundaries_bps)
        self.assertEqual(x.shape,y.shape)
        self.assertFalse(np.all(x==y))
        self.assertTrue(np.isfinite(y).all())
        altered_labels=[replace(c,target_usd=c.target_usd*1.03,
                                encoded_target=333) for c in dev]
        np.testing.assert_array_equal(
            grammar(dev,"signed_quantile_g2"),
            grammar(altered_labels,"signed_quantile_g2"))
        np.testing.assert_array_equal(
            grammar(dev,"signed_uniform_g1"),
            grammar(altered_labels,"signed_uniform_g1"))

    def test_g0_arms_identical_to_existing_s2b_numerics(self):
        train,dev=cases(2018),cases(2023)
        shared=dict(interval="D1",widths=(16,),depths=(1,),
                    modes=("regression","joint"),
                    seeds=(17,),steps=2)
        left=s2b_run_cases(train,dev,**shared)
        right=s3_run_cases(train,dev,grammars=GRAMMARS,**shared)
        self.assertEqual(len(right["results"]),8)
        self.assertEqual(right["experiment"],
                         "TRAME_S3_1A_PREDICTIVE_GRAMMAR_V1")
        self.assertFalse(right["labels_2026_opened"])
        self.assertEqual(right["train_origins_sha256"],
                         left["train_origins_sha256"])
        self.assertEqual(right["development_origins_sha256"],
                         left["development_origins_sha256"])
        for mode in ("regression","joint"):
            baseline={x["representation"]:x for x in left["results"] if x["mode"]==mode}
            extra={x["representation"]:x for x in right["results"] if x["mode"]==mode}
            fingerprints={x["initial_state_sha256"] for x in extra.values()}
            self.assertEqual(len(fingerprints),1)
            for name in ("continuous_bps","legacy_quantized_bps"):
                for metric in ("balanced_direction_accuracy","mae_native_usd",
                               "mae_bps_anchor","absolute_magnitude_error_bps",
                               "direction_accuracy_all"):
                    self.assertAlmostEqual(
                        baseline[name][metric],extra[name][metric],places=10)
                self.assertEqual(baseline[name]["initial_state_sha256"],
                                 extra[name]["initial_state_sha256"])
            self.assertEqual(
                {x["parameter_count"] for x in extra.values()},
                {baseline["continuous_bps"]["parameter_count"]})
            self.assertEqual(len({x["input_normalizer_std_bps"]
                                  for x in extra.values()}),1)
            self.assertTrue(all(math.isfinite(x["mae_bps_anchor"])
                                for x in extra.values()))
            self.assertEqual(
                sum(x["binary_probabilities_from_trained_head"] is True
                    for x in extra.values()),4 if mode=="joint" else 0)

    def test_holdout_and_incomplete_input_are_rejected(self):
        train,dev=cases(2018),cases(2026)
        with self.assertRaises(ValueError):
            s3_run_cases(train,dev,interval="M1",steps=1,seeds=(1,),
                         widths=(16,),depths=(1,))
        codec=TrainOnlyGrammarFeatures(train)
        with self.assertRaises(ValueError):
            codec([replace(train[0],continuous_past_bps=(1.,2.))],
                  "signed_uniform_g1")

    def test_each_signed_grammar_preserves_nonzero_sign_in_reconstruction(self):
        train=cases(2018)
        codec=TrainOnlyGrammarFeatures(train)
        for kind in ("signed_uniform_g1","signed_quantile_g2"):
            encoded=codec(train,kind)
            original=np.asarray([c.continuous_past_bps for c in train])
            self.assertTrue(np.all(np.sign(original)==np.sign(encoded)))


if __name__=="__main__":
    unittest.main()
