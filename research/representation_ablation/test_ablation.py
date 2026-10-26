"""S2b input-only ablation: invented examples, no private BTC access."""
from dataclasses import replace
import math
import unittest

import numpy as np

from research.continuous_direction.test_continuous import fabricated_case
from research.representation_ablation.runner import (
    REPRESENTATIONS, features, quantization_diagnostics, run_cases,
)


class RepresentationAblationTests(unittest.TestCase):
    @staticmethod
    def cohorts():
        return (
            [fabricated_case(2018,i) for i in range(40)],
            [fabricated_case(2023,i) for i in range(40)],
        )

    def test_quantized_past_loses_tiny_signs_but_both_inputs_remain_causal(self):
        train,_=self.cohorts()
        continuous=features(train,"continuous_bps")
        quantized=features(train,"legacy_quantized_bps")
        self.assertTrue(np.any(continuous!=0))
        self.assertTrue(np.all(quantized==0))
        stat=quantization_diagnostics(train)
        self.assertEqual(stat["past_nonzero_observations"],
                         stat["past_sign_lost_or_changed_count"])
        self.assertGreater(stat["past_reconstruction_mae_bps"],0)
        self.assertTrue(stat["diagnostics_only_not_prediction_skill"])
        with self.assertRaises(ValueError):
            features(train,"future_target")
        changed=[replace(x,target_usd=x.target_usd*1.15,
                         encoded_target=1000) for x in train]
        np.testing.assert_array_equal(features(changed,"continuous_bps"),
                                      continuous)
        np.testing.assert_array_equal(features(changed,"legacy_quantized_bps"),
                                      quantized)

    def test_paired_smoke_has_same_initial_weights_and_true_targets(self):
        train,dev=self.cohorts()
        r=run_cases(train,dev,interval="D1",
                    representations=REPRESENTATIONS,
                    modes=("regression","joint"),
                    widths=(16,),depths=(1,),seeds=(11,),steps=1)
        self.assertEqual(len(r["results"]),4)
        self.assertEqual(r["experiment"],"TRAME_S2B_REPRESENTATION_ABLATION_V1")
        self.assertFalse(r["labels_2026_opened"])
        self.assertTrue(r["same_target_normalization_all_representations"])
        self.assertTrue(r["same_input_normalization_all_representations"])
        self.assertEqual(len(r["train_origins_sha256"]),64)
        self.assertTrue(r["common_batch_indices_per_seed"])
        self.assertEqual(r["quantization_input_train"]["past_quantized_to_zero_count"],
                         r["quantization_input_train"]["past_nonzero_observations"])
        same_modes={}
        for x in r["results"]:
            self.assertTrue(math.isfinite(x["mae_bps_anchor"]))
            self.assertTrue(math.isfinite(x["absolute_magnitude_error_bps"]))
            self.assertIn("always_up_1bp",r["baseline_scores"])
            self.assertGreater(x["target_normalizer_std_bps_common"],0)
            same_modes.setdefault(x["mode"],[]).append(x)
        for mode,pair in same_modes.items():
            self.assertEqual(len(pair),2)
            self.assertEqual(pair[0]["initial_state_sha256"],
                             pair[1]["initial_state_sha256"])
            self.assertEqual(pair[0]["parameter_count"],pair[1]["parameter_count"])
            self.assertEqual(pair[0]["target_normalizer_std_bps_common"],
                             pair[1]["target_normalizer_std_bps_common"])
            self.assertEqual(pair[0]["input_normalizer_std_bps"],
                             pair[1]["input_normalizer_std_bps"])
            self.assertEqual(pair[0]["input_scale_fallback"],
                             pair[1]["input_scale_fallback"])
            self.assertNotEqual(pair[0]["input_information_degenerate"],
                                pair[1]["input_information_degenerate"])
        self.assertTrue(all(x["brier_nonflat"] is None
                            for x in same_modes["regression"]))
        self.assertTrue(all(isinstance(x["brier_nonflat"],float)
                            for x in same_modes["joint"]))

    def test_continuous_arm_reproduces_original_S2_at_same_seed_and_loss(self):
        from research.continuous_direction.runner import run_cases as s2_run_cases
        train,dev=self.cohorts()
        settings=dict(interval="H1",widths=(16,),depths=(1,),
                      modes=("regression",),seeds=(29,),steps=2)
        old=s2_run_cases(train,dev,**settings)
        new=run_cases(train,dev,representations=("continuous_bps",),
                      **settings)
        left=old["results"][0]
        right=new["results"][0]
        for metric in ("direction_accuracy_all","balanced_direction_accuracy",
                       "mae_native_usd","mae_bps_anchor",
                       "absolute_magnitude_error_bps",
                       "gross_signal_return_mean_bps_per_sample"):
            self.assertAlmostEqual(left[metric],right[metric],places=10,
                                   msg=f"continuous S2 numerical drift: {metric}")
        self.assertEqual(left["parameter_count"],right["parameter_count"])
        self.assertEqual(old["train_origins_sha256"],new["train_origins_sha256"])

    def test_development_2026_never_opened(self):
        train,dev=self.cohorts()
        dev_future=[fabricated_case(2026,i) for i in range(40)]
        with self.assertRaisesRegex(ValueError,"development"):
            run_cases(train,dev_future,interval="M1",widths=(16,),
                      depths=(1,),modes=("regression",),
                      seeds=(7,),steps=1)

    def test_different_development_prices_cannot_refit_input_normalization(self):
        train,dev=self.cohorts()
        r1=run_cases(train,dev,interval="H1",widths=(16,),depths=(1,),
                     modes=("regression",),seeds=(3,),steps=1)
        changed=[replace(x,target_usd=x.target_usd*1.2) for x in dev]
        r2=run_cases(train,changed,interval="H1",widths=(16,),depths=(1,),
                     modes=("regression",),seeds=(3,),steps=1)
        self.assertEqual(r1["target_train_std_bps"],r2["target_train_std_bps"])
        self.assertEqual(
            [x["input_normalizer_std_bps"] for x in r1["results"]],
            [x["input_normalizer_std_bps"] for x in r2["results"]])
        self.assertEqual(
            [x["initial_state_sha256"] for x in r1["results"]],
            [x["initial_state_sha256"] for x in r2["results"]])
        self.assertEqual(r1["development_origins_sha256"],
                         r2["development_origins_sha256"])


if __name__=="__main__":
    unittest.main()
