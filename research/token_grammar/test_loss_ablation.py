"""S3.1D objective weights causal invariants (fabricated returns only)."""
from dataclasses import replace
import math
import unittest
import torch
from research.continuous_direction.models import ContinuousDirectionModel
from research.token_grammar.test_predictive import cases
from research.token_grammar.loss_ablation import OBJECTIVES,objective,components,run_cases


class LossAblationTests(unittest.TestCase):
    def test_reference_is_exactly_existing_joint_loss_and_zero_flat_mask(self):
        torch.manual_seed(17)
        m=ContinuousDirectionModel(width=16,depth=1,mode="joint")
        x=torch.arange(80,dtype=torch.float64).reshape(4,20)/20
        y=torch.tensor([-.2,.5,0.,-.1],dtype=torch.float64)
        torch.testing.assert_close(objective(m,x,y,"reference"),m.loss(x,y),
                                   rtol=1e-13,atol=1e-13)
        _,logits=m(x)
        a,b,c=components(torch.zeros(4,dtype=torch.float64),logits,
                           torch.zeros(4,dtype=torch.float64))
        self.assertEqual(float(b),0.)
        self.assertTrue(math.isfinite(float(a+c)))
        self.assertEqual(len(OBJECTIVES),5)

    def test_all_objective_arms_same_initial_weights_and_real_price_targets(self):
        train=cases(2018)+cases(2019)
        monitor=cases(2020)+cases(2021)
        report=run_cases(train,monitor,interval="D1",
                         seeds=(3,),checkpoints=(1,2))
        self.assertEqual(len(report["results"]),10)
        self.assertEqual(report["checkpoint_steps"],[1,2])
        self.assertFalse(report["external_2022_2025_used"])
        self.assertFalse(report["holdout_2026_used"])
        self.assertTrue(report["all_arms_same_model_initial_weights"])
        self.assertTrue(report["all_arms_same_forecast_reconciliation"])
        self.assertEqual(len({r["backbone_initial_sha256"]
                              for r in report["results"]}),1)
        self.assertEqual(len({r["parameter_count"]
                              for r in report["results"]}),1)
        self.assertEqual({r["loss_arm"] for r in report["results"]},
                         set(OBJECTIVES))
        for row in report["results"]:
            self.assertTrue(math.isfinite(row["mae_native_usd"]))
            self.assertTrue(math.isfinite(row["mae_bps_anchor"]))
            self.assertTrue(math.isfinite(row["absolute_magnitude_error_bps"]))
            self.assertTrue(math.isfinite(row["brier_skill_vs_train_prior"]))
            self.assertEqual(row["mode"],"joint")
            self.assertTrue(row["model_checkpoint_continuing_same_optimizer"])

    def test_monitor_labels_do_not_fit_tokens_scale_or_prior(self):
        train=cases(2018)+cases(2019)
        monitor=cases(2020)+cases(2021)
        config=dict(interval="H1",arms=("reference",),seeds=(7,),
                    checkpoints=(1,))
        a=run_cases(train,monitor,**config)
        changed=[replace(c,target_usd=c.target_usd*1.002) for c in monitor]
        b=run_cases(train,changed,**config)
        for key in ("quantile_g2_boundaries_train_only_bps",
                    "normalizer_std_bps_train_only",
                    "train_only_direction_prior",
                    "train_origins_sha256"):
            self.assertEqual(a[key],b[key])
        self.assertNotEqual(a["results"][0]["mae_native_usd"],
                            b["results"][0]["mae_native_usd"])

    def test_external_2022_2025_and_2026_rejected(self):
        train=cases(2018)
        with self.assertRaises(ValueError):
            run_cases(train,cases(2023),interval="M1",
                      seeds=(1,),checkpoints=(1,))
        with self.assertRaises(ValueError):
            run_cases(train,cases(2026),interval="M1",
                      seeds=(1,),checkpoints=(1,))
        with self.assertRaises(ValueError):
            run_cases(train,cases(2020),interval="M1",
                      seeds=(1,),checkpoints=(2,1))
        with self.assertRaises(ValueError):
            run_cases(train,cases(2020),interval="M1",
                      data_origin="BTC_PUBLIC_REAL",seeds=(1,),checkpoints=(1,))


if __name__=="__main__":
    unittest.main()
