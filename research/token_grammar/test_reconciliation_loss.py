"""S3.1E synthetic-only adversarial loss and hard-v-soft scoring tests."""
from dataclasses import replace
import math
import unittest
import torch

from research.continuous_direction.models import ContinuousDirectionModel
from research.token_grammar.test_predictive import cases
from research.token_grammar.reconciliation_loss import (
    ARMS,EPS,objective,run_cases,soft_reconciled_return,
)


class ReconciliationTests(unittest.TestCase):
    def test_legacy_reference_exact_s3_1c_joint_and_gradients(self):
        torch.manual_seed(42)
        model=ContinuousDirectionModel(width=16,depth=1,mode="joint")
        x=torch.linspace(-.2,.2,80,dtype=torch.float64).reshape(4,20)
        y=torch.tensor([.9,-1.3,0.,.3],dtype=torch.float64)
        old=model.loss(x,y)
        new=objective(model,x,y,"legacy")
        torch.testing.assert_close(old,new,rtol=1e-14,atol=1e-14)
        for arm in ARMS:
            model.zero_grad(set_to_none=True)
            loss=objective(model,x,y,arm)
            loss.backward()
            self.assertTrue(math.isfinite(float(loss)))
            self.assertGreater(float(model.direction_head.weight.grad.abs().sum()),0)
            self.assertGreater(float(model.return_head.weight.grad.abs().sum()),0)
        model.zero_grad(set_to_none=True)
        alone=objective(model,x,y,"reconciled_100")-objective(model,x,y,"legacy")
        alone.backward()
        self.assertGreater(float(model.direction_head.weight.grad.abs().sum()),0)
        self.assertGreater(float(model.return_head.weight.grad.abs().sum()),0)

    def test_soft_return_is_not_binary_hard_inference(self):
        mu=torch.tensor([2.,-3.,1.],dtype=torch.float64)
        logits=torch.tensor([0.,3.,-3.],dtype=torch.float64)
        soft=soft_reconciled_return(mu,logits)
        self.assertEqual(float(soft[0]),0.)
        self.assertGreater(float(soft[1]),0.)
        self.assertLess(float(soft[2]),0.)
        self.assertTrue(torch.all(soft.abs()<=mu.abs()+EPS).item())
        with self.assertRaises(ValueError):
            soft_reconciled_return(mu.float(),logits.float())

    def test_seed_initialization_capacity_and_external_dev_embargo(self):
        train=cases(2018)+cases(2019)
        mon=cases(2020)+cases(2021)
        kwargs=dict(interval="D1",checkpoints=(1,2),seeds=(5,))
        r=run_cases(train,mon,**kwargs)
        self.assertEqual(len(r["results"]),6)
        self.assertTrue(r["served_hard_sign_reconciliation_unchanged"])
        self.assertTrue(r["soft_surrogate_is_not_hard_served_forecast"])
        self.assertFalse(r["external_2022_2025_used"])
        self.assertFalse(r["holdout_2026_used"])
        self.assertEqual(len({x["backbone_initial_sha256"]
                              for x in r["results"]}),1)
        self.assertEqual(len({x["parameter_count"]
                              for x in r["results"]}),1)
        for row in r["results"]:
            for key in ("mae_native_usd","mae_bps_anchor",
                        "soft_surrogate_mae_bps_anchor",
                        "regression_vs_head_sign_disagreement_fraction",
                        "hard_soft_price_gap_bps"):
                self.assertTrue(math.isfinite(row[key]))
            self.assertGreaterEqual(row["hard_soft_price_gap_bps"],0)
        with self.assertRaises(ValueError):
            run_cases(train,cases(2023),**kwargs)
        with self.assertRaises(ValueError):
            run_cases(train,cases(2026),**kwargs)
        with self.assertRaises(ValueError):
            run_cases(train,mon,interval="D1",seeds=(5,),
                      checkpoints=(1,),data_origin="BTC_PUBLIC_REAL")

    def test_monitor_targets_cannot_set_training_normalizer_or_tokens(self):
        train=cases(2018)+cases(2019)
        mon=cases(2020)+cases(2021)
        opts=dict(interval="M1",arms=("legacy",),seeds=(3,),checkpoints=(1,))
        a=run_cases(train,mon,**opts)
        b=run_cases(train,[replace(c,target_usd=c.target_usd*1.001)
                           for c in mon],**opts)
        for key in ("train_normalizer_std_bps",
                    "quantile_boundaries_train_only_bps",
                    "train_only_prior_up","train_origins_sha256"):
            self.assertEqual(a[key],b[key])
        self.assertNotEqual(a["results"][0]["mae_native_usd"],
                            b["results"][0]["mae_native_usd"])


if __name__=="__main__":
    unittest.main()
