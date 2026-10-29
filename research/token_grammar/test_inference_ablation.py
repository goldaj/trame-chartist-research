"""S3.1F synthetic-only exact pricing and causal training-parity tests."""
import math
import unittest
import numpy as np

from research.token_grammar.test_predictive import cases
from research.token_grammar.inference_ablation import (
    RULES,inference_rule_prices,run_cases)
from research.token_grammar.reconciliation_loss import run_cases as s3e_run_cases


class InferenceAblationTests(unittest.TestCase):
    def test_direct_hard_soft_have_distinct_and_finite_prices(self):
        mu=np.array([-3.,2.,-1.])
        p=np.array([.8,.9,.2])
        anchors=np.array([10000.,12000.,14000.])
        values=inference_rule_prices(mu,p,anchors,scale_bps=50.)
        self.assertEqual(set(values),set(RULES))
        self.assertGreater(values["joint_hard"][0],anchors[0])
        self.assertLess(values["signed_direct_mu"][0],anchors[0])
        self.assertLess(abs(values["joint_soft_tanh"][0]-anchors[0]),
                        abs(values["joint_hard"][0]-anchors[0]))
        self.assertTrue(all(np.isfinite(x).all() for x in values.values()))
        with self.assertRaises(ValueError):
            inference_rule_prices(mu,np.array([1.5,.2,.3]),anchors,scale_bps=50.)

    def test_retrained_legacy_is_identical_to_s3e_reference(self):
        train=cases(2018)+cases(2019)
        mon=cases(2020)+cases(2021)
        settings=dict(interval="H1",seeds=(17,),checkpoints=(1,2))
        a=run_cases(train,mon,**settings)
        b=s3e_run_cases(train,mon,arms=("legacy",),**settings)
        self.assertEqual(len(a["trajectories"]),1)
        self.assertEqual(len(a["results"]),6)
        self.assertEqual(len(b["results"]),2)
        for step in (1,2):
            hard=next(r for r in a["results"] if r["step"]==step
                      and r["rule"]=="joint_hard")
            old=next(r for r in b["results"] if r["checkpoint_updates"]==step)
            self.assertEqual(hard["backbone_initial_sha256"],
                             old["backbone_initial_sha256"])
            for score in ("balanced_direction_accuracy","mae_native_usd",
                          "mae_bps_anchor","absolute_magnitude_error_bps"):
                self.assertAlmostEqual(hard[score],old[score],places=10)
            rows=[r for r in a["results"] if r["step"]==step]
            self.assertEqual(len(set(x["parameter_count"] for x in rows)),1)
            self.assertEqual(len(set(x["head_brier_score"] for x in rows)),1)
            self.assertTrue(all(math.isfinite(x["mae_bps_anchor"]) for x in rows))
        self.assertTrue(a["hard_reproduces_existing_forecast_prices_exactly"])
        self.assertFalse(a["external_dev_2022_2025_accessed"])
        self.assertFalse(a["holdout_2026_accessed"])

    def test_rejects_future_2022_2026_monitor_and_bad_real_checkpoint(self):
        tr=cases(2018)
        for year in (2023,2026):
            with self.assertRaises(ValueError):
                run_cases(tr,cases(year),interval="D1",
                          seeds=(3,),checkpoints=(1,))
        with self.assertRaises(ValueError):
            run_cases(tr,cases(2020),interval="D1",seeds=(3,),
                      checkpoints=(2,1))
        with self.assertRaises(ValueError):
            run_cases(tr,cases(2020),interval="D1",seeds=(3,),
                      checkpoints=(1,),data_origin="BTC_PUBLIC_REAL")


if __name__=="__main__":
    unittest.main()
