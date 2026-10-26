"""S3.1C: hostile fabricated split/checkpoint tests, no finance data."""
from dataclasses import replace
from datetime import datetime,timedelta,timezone
from pathlib import Path
from unittest.mock import patch
import math
import unittest

from research.token_grammar.test_predictive import cases
from research.token_grammar.internal_cohorts import (
    split_case_sequence,validate_internal,collect_pre2022,MONITOR_END)
from research.token_grammar.training_dynamics import run_cases
from research.btc_h1_m1 import stream


def fake_series():
    # 200 train targets followed by 80 separate monitor targets
    return cases(2018)+cases(2019)+cases(2020)+cases(2021)


class Pre2022SplitTests(unittest.TestCase):
    def test_deterministic_label_available_cutoffs_independent_of_targets(self):
        train_only=fake_series()
        left,lp=split_case_sequence(train_only,max_train=42,max_monitor=36)
        right,rp=split_case_sequence(train_only,max_train=42,max_monitor=36)
        self.assertEqual(lp,rp)
        self.assertEqual(lp["train_count"],42)
        self.assertEqual(lp["monitor_count"],36)
        self.assertEqual(lp["scanned_case_counts"],{"train":80,"monitor":80})
        self.assertEqual(left["train"],right["train"])
        self.assertEqual(left["monitor"],right["monitor"])
        self.assertLess(max(x.label_available_time for x in left["train"]),
                        min(x.label_available_time for x in left["monitor"]))
        contaminated=[replace(c,label_available_time=datetime(
            2022,1,1,tzinfo=timezone.utc)) for c in cases(2021)]
        with self.assertRaisesRegex(ValueError,"post-2021"):
            split_case_sequence(fake_series()+contaminated)

    def test_rejects_future_monitor_targets_and_internal_label_overlap(self):
        train,mon=cases(2018),cases(2020)
        report=validate_internal(train,mon)
        self.assertTrue(report["all_labels_before_2022"])
        with self.assertRaises(ValueError):
            validate_internal(train,cases(2023))
        with self.assertRaises(ValueError):
            validate_internal(train,train)
        with self.assertRaises(ValueError):
            validate_internal(cases(2020),mon)

    def test_bounded_stream_does_not_request_external_development(self):
        source=cases(2018)+cases(2020)
        def generator(interval,folder,*,step,train_only,stop_labels_before):
            self.assertTrue(train_only)
            self.assertEqual(stop_labels_before,MONITOR_END)
            self.assertEqual(step,60 if interval=="M1" else 1)
            for c in source:
                yield "train",c
        with patch("research.token_grammar.internal_cohorts.iter_cases",
                   side_effect=generator):
            pools,p=collect_pre2022("M1",Path("/not-real"),
                                    max_train=40,max_monitor=40)
        self.assertEqual(p["monitor_count"],40)
        self.assertEqual(p["sampling_stride"],60)
        self.assertTrue(all(x.label_available_time.year<2022
                            for x in pools["monitor"]))

    def test_hard_reader_stops_before_first_2022_candle(self):
        from research.btc_h1_m1.test_daily import make_fake_d1
        from tempfile import TemporaryDirectory
        # Explicit public 2012+ artifact is verified in the separate CI job;
        # here make a tiny fabricated reader with one post-2021 bar.
        from research.btc_h1_m1.stream import Candle
        cutoff=MONITOR_END
        bars=[Candle(datetime(2021,12,30,tzinfo=timezone.utc)+timedelta(days=i),
                     40000.,41000.,39000.,40000.+i,1.) for i in range(3)]
        def fake_read(interval,folder,*,stop_before=None):
            self.assertEqual(stop_before,cutoff)
            for bar in bars:
                if bar.started_at>=stop_before:
                    return
                yield bar
        with patch.object(stream,"read_bars",side_effect=fake_read):
            self.assertEqual(list(stream.iter_cases(
                "D1",Path("/not-real"),context=1,
                stop_labels_before=cutoff)),[])
        with self.assertRaises(ValueError):
            list(stream.iter_cases("D1",stop_labels_before=datetime(
                2023,1,1,tzinfo=timezone.utc)))


class ConvergenceCheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.train=cases(2018)+cases(2019)
        cls.monitor=cases(2020)+cases(2021)

    def test_real_checkpoint_continuity_and_paired_backbone(self):
        report=run_cases(self.train,self.monitor,interval="H1",
              seeds=(5,),checkpoints=(1,2),width=16,depth=1)
        self.assertEqual(report["experiment"],"TRAME_S3_1C_PRE2022_CONVERGENCE_V1")
        self.assertFalse(report["external_dev_2022_2025_opened"])
        self.assertFalse(report["labels_2026_opened"])
        self.assertEqual(len(report["trajectories"]),3)
        self.assertEqual(len(report["evaluations"]),6)
        self.assertEqual({x["checkpoint_steps"] for x in report["evaluations"]},{1,2})
        self.assertEqual(len({x["backbone_initial_sha256"]
                             for x in report["evaluations"]}),1)
        for row in report["evaluations"]:
            self.assertTrue(row["same_optimizer_continued"])
            self.assertEqual(row["forecast_rows"],80)
            self.assertTrue(math.isfinite(row["train_fixed_joint_loss"]))
            self.assertTrue(math.isfinite(row["monitor_joint_loss"]))
            self.assertTrue(math.isfinite(row["gradient_norm_before_clip_mean"]))
            self.assertTrue(math.isfinite(row["mae_bps_anchor"]))
            self.assertIsNotNone(row["brier_skill_vs_train_prior"])
            self.assertTrue(0<=row["gradient_clip_fraction_cumulative"]<=1)
        p={x["arm"]:x for x in report["trajectories"]}
        self.assertEqual(p["embedding_ordered"]["parameter_count"],
                         p["embedding_random"]["parameter_count"])
        self.assertEqual(p["embedding_ordered"]["parameter_count"]-
                         p["decoded"]["parameter_count"],11)

    def test_no_external_development_and_invalid_checkpoints(self):
        with self.assertRaises(ValueError):
            run_cases(self.train,cases(2023),interval="D1",
                      checkpoints=(1,),seeds=(1,))
        with self.assertRaises(ValueError):
            run_cases(self.train,self.monitor,interval="D1",
                      checkpoints=(2,1),seeds=(1,))
        with self.assertRaises(ValueError):
            run_cases(self.train,self.monitor,interval="D1",
                      checkpoints=(2001,),seeds=(1,))


if __name__=="__main__":
    unittest.main()
