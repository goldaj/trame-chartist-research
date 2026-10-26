"""S3.1G artificial-only tests for train predicted thresholds and fair selection."""
from dataclasses import replace
import unittest
import numpy as np

from research.token_grammar.test_predictive import cases
from research.token_grammar.selective_forecast import (
    eligible_masks,selected_metrics,run_cases)
from research.token_grammar.inference_ablation import run_cases as old_run_cases

class SelectivePredictionsTests(unittest.TestCase):
    def test_fixed_quantiles_are_train_only_even_if_monitor_changes(self):
        train=np.arange(1,101,dtype=np.float64)
        mon=np.array([5.,40.,65.,88.,120.])
        thresholds,mask=eligible_masks(train,mon)
        changed,other=eligible_masks(train,np.array([1000.,900.,800.,700.,600.]))
        self.assertEqual(thresholds,changed)
        self.assertEqual(thresholds["all"],0.)
        self.assertTrue(all(mask["all"]))
        self.assertTrue(np.all(mask["q90"]<=mask["q75"]))
        self.assertTrue(np.all(mask["q75"]<=mask["q50"]))
        self.assertFalse(np.array_equal(mask["q90"],other["q90"]))
        with self.assertRaises(ValueError):
            eligible_masks(np.array([1.,float("nan")]),mon)

    def test_same_training_as_old_legacy_and_all_subset_exact(self):
        tr=cases(2018)+cases(2019)
        dev=cases(2020)+cases(2021)
        kw=dict(interval="D1",seeds=(9,))
        selected=run_cases(tr,dev,training_steps=2,**kw)
        previous=old_run_cases(tr,dev,checkpoints=(1,2),**kw)
        self.assertEqual(len(selected["trajectories"]),1)
        self.assertEqual(len(selected["results"]),12)
        self.assertFalse(selected["external_2022_2025_used"])
        self.assertFalse(selected["holdout_2026_used"])
        byrule={x["rule"]:x for x in previous["results"] if x["step"]==2}
        allrows=[x for x in selected["results"] if x["threshold"]=="all"]
        self.assertEqual(len(allrows),3)
        self.assertEqual(len({x["selection_sha256"] for x in allrows}),1)
        for row in allrows:
            match=byrule[row["rule"]]
            for name in ("balanced_direction_accuracy","mae_native_usd",
                         "mae_bps_anchor","absolute_magnitude_error_bps"):
                self.assertAlmostEqual(row[name],match[name],places=10)
            self.assertEqual(row["n_selected"],len(dev))
            self.assertEqual(row["status"],"INFORMATIVE")
        per_rule={}
        for r in selected["results"]:
            per_rule.setdefault(r["threshold"],[]).append(r)
        for subset in per_rule.values():
            self.assertEqual(len({x["n_selected"] for x in subset}),1)
            self.assertEqual(len({x["threshold_train_bps"] for x in subset}),1)
            self.assertEqual(len({x["selection_sha256"] for x in subset}),1)
        self.assertGreaterEqual(per_rule["q50"][0]["n_selected"],
                                per_rule["q75"][0]["n_selected"])
        self.assertGreaterEqual(per_rule["q75"][0]["n_selected"],
                                per_rule["q90"][0]["n_selected"])

    def test_monitor_targets_never_set_cutoffs(self):
        tr=cases(2018)+cases(2019)
        mon=cases(2020)+cases(2021)
        k=dict(interval="H1",seeds=(4,),training_steps=1)
        first=run_cases(tr,mon,**k)
        alternate=run_cases(tr,[replace(x,target_usd=x.target_usd*1.001)
                                  for x in mon],**k)
        for key in ("train_origins_sha256","g2_quantiles_train_only_bps",
                    "train_normalizer_std_bps"):
            self.assertEqual(first[key],alternate[key])
        for i,j in zip(first["results"],alternate["results"]):
            self.assertEqual(i["threshold_train_bps"],j["threshold_train_bps"])
            self.assertEqual(i["selection_sha256"],j["selection_sha256"])

    def test_reject_future_data_and_zero_cover_cannot_claim_accuracy(self):
        with self.assertRaises(ValueError):
            run_cases(cases(2018),cases(2023),
                      interval="M1",seeds=(2,),training_steps=1)
        with self.assertRaises(ValueError):
            run_cases(cases(2018),cases(2026),
                      interval="M1",seeds=(2,),training_steps=1)
        from research.scaling_study.metrics import training_magnitude_thresholds
        from research.continuous_direction.diagnostics import prior_from_train
        tr=cases(2018)
        result=selected_metrics([1.,1.],[1.1,.9],[1.,1.],
                  np.array([False,False]),train_thresholds=training_magnitude_thresholds(tr),
                  train_prior=prior_from_train(tr),head_probabilities=[.5,.5])
        self.assertEqual(result["status"],"NO_COVERAGE")
        self.assertIsNone(result["balanced_direction_accuracy"])
        with self.assertRaises(ValueError):
            run_cases(cases(2018),cases(2020),interval="D1",
                      data_origin="BTC_PUBLIC_REAL",training_steps=1)

if __name__=="__main__":
    unittest.main()
