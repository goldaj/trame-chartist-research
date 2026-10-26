"""S3.1C optimizer diagnostics on fabricated returns only."""
from dataclasses import replace
import math
import unittest

from research.token_grammar.test_predictive import cases
from research.token_grammar.convergence import (
    split_internal_pre2022,run_cases,CHECKPOINTS,
)


class TestConvergence(unittest.TestCase):
    def test_pre2022_isolated_temporal_cohorts(self):
        train,monitor=split_internal_pre2022(cases(2018)+cases(2020))
        self.assertEqual(len(train),40)
        self.assertEqual(len(monitor),40)
        self.assertTrue(all(x.label_available_time.year<2020 for x in train))
        self.assertTrue(all(2020<=x.label_available_time.year<=2021 for x in monitor))
        with self.assertRaises(ValueError):
            split_internal_pre2022(cases(2018)+cases(2023))
        with self.assertRaises(ValueError):
            split_internal_pre2022(cases(2018)+cases(2026))

    def test_checkpoints_are_same_optimizer_trajectory_and_distinct_monitor(self):
        r=run_cases(cases(2018),cases(2020),interval="D1",
                    seeds=(7,),checkpoints=(2,4),
                    data_origin="ARTIFICIAL_FIXTURE")
        self.assertEqual(r["checkpoint_steps"],[2,4])
        self.assertEqual(len(r["results"]),6)
        self.assertFalse(r["external_development_2022_2025_accessed"])
        self.assertFalse(r["labels_2026_opened"])
        self.assertEqual(len({x["backbone_initial_sha256"]
                              for x in r["results"]}),1)
        for arm in ("decoded","embedding_ordered","embedding_random"):
            rows=[x for x in r["results"] if x["arm"]==arm]
            self.assertEqual([x["checkpoint_updates"] for x in rows],[2,4])
            self.assertEqual(rows[0]["parameter_count"],rows[1]["parameter_count"])
            self.assertTrue(all(math.isfinite(x["gradient_norm_last50_mean_before_clip"]) for x in rows))
            self.assertTrue(all(0<=x["predicted_up_percent"]<=100 for x in rows))
            self.assertTrue(all(math.isfinite(x["mae_bps_anchor"]) for x in rows))
            self.assertTrue(all(math.isfinite(x["internal_validation_monitor_loss"]) for x in rows))
        self.assertEqual(
            next(x for x in r["results"] if x["arm"]=="embedding_ordered")["parameter_count"]-
            next(x for x in r["results"] if x["arm"]=="decoded")["parameter_count"],11)
        self.assertEqual(r["train_count"],40)
        self.assertEqual(r["monitor_count"],40)

    def test_monitor_labels_do_not_affect_train_vocabulary_or_scale(self):
        train,monitor=cases(2018),cases(2020)
        a=run_cases(train,monitor,interval="H1",
                    arms=("decoded",),seeds=(3,),checkpoints=(1,))
        changed=[replace(c,target_usd=c.target_usd*1.03) for c in monitor]
        b=run_cases(train,changed,interval="H1",
                    arms=("decoded",),seeds=(3,),checkpoints=(1,))
        self.assertEqual(a["quantile_g2_boundaries_train_only_bps"],
                         b["quantile_g2_boundaries_train_only_bps"])
        self.assertEqual(a["normalizer_std_bps_train_only"],
                         b["normalizer_std_bps_train_only"])
        self.assertEqual(a["train_only_up_prior"],b["train_only_up_prior"])
        self.assertNotEqual(a["results"][0]["mae_native_usd"],
                            b["results"][0]["mae_native_usd"])

    def test_hard_pre2022_reader_stop_before_external_price_rows(self):
        from pathlib import Path
        from unittest.mock import patch
        from research.btc_h1_m1.stream import read_bars
        from research.token_grammar.convergence import collect_internal,MONITOR_END
        from research.btc_h1_m1 import stream

        bars=list(read_bars("D1",Path("research/data/reference"),
                            stop_before=MONITOR_END))
        self.assertGreater(len(bars),3000)
        self.assertLess(max(x.started_at for x in bars),MONITOR_END)

        def only_early(interval,directory,*,step,train_only,stop_labels_before):
            self.assertTrue(train_only)
            self.assertEqual(stop_labels_before,MONITOR_END)
            for c in cases(2018)+cases(2020):
                yield "train",c

        with patch("research.token_grammar.convergence.iter_cases",
                   side_effect=only_early):
            train,monitor,provenance=collect_internal(
                "M1",Path("/fake"),max_cases=100,max_monitor=40)
        self.assertEqual(len(train),40)
        self.assertEqual(len(monitor),40)
        self.assertTrue(provenance["train_reservoir_is_independent_of_monitor_counts"])

    def test_real_runs_reject_nonpreregistered_checkpoints(self):
        with self.assertRaises(ValueError):
            run_cases(cases(2018),cases(2020),interval="M1",
                      seeds=(1,),checkpoints=(2,4),
                      data_origin="BTC_PUBLIC_REAL")


if __name__=="__main__":
    unittest.main()
