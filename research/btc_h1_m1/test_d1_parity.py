"""D1 parity: fabricated original-format D1 files, never actual prices."""
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from research.btc_h1_m1.daily import read_daily
from research.btc_h1_m1.stream import read_bars, iter_cases
from research.btc_h1_m1.experiment import compare_history, collect
from research.btc_h1_m1.statistical_baselines import score_baselines
from research.btc_h1_m1.regime_analysis import group_report
from research.btc_h1_m1.test_daily import make_fake_d1
from research.scaling_study.runner import run_cases


class DailyExperimentParity(unittest.TestCase):
    def test_original_schemas_grade_split_and_future_holdout(self):
        with TemporaryDirectory() as temporary:
            root=Path(temporary)
            make_fake_d1(root)
            originals=list(read_daily(directory=root))
            candles=list(read_bars("D1", root))
            self.assertEqual(originals[0].day, date(2010,7,18))
            self.assertEqual(originals[0].grade, "indicative_close_only")
            self.assertTrue(all(row.started_at.year>=2011 for row in candles))
            self.assertEqual(candles[0].started_at.date(), date(2011,8,18))
            self.assertEqual(candles[-1].started_at.date(), date(2025,12,31))
            # Cannot invent 2010 volume/open nor leak the daily close at candle open.
            cases=list(iter_cases("D1", root))
            self.assertTrue(cases)
            self.assertTrue(all(c.grade=="bitstamp_D1_observed_nonzero_volume"
                                for _,c in cases))
            self.assertTrue(all(c.decision_time<c.label_available_time
                                for _,c in cases))
            self.assertTrue(all(c.target_open.year<=2025 for _,c in cases))
            self.assertTrue(any(s=="train" for s,_ in cases))
            self.assertTrue(any(s=="development" for s,_ in cases))

    def test_daily_baselines_neural_regimes_and_direction(self):
        with TemporaryDirectory() as temporary:
            root=Path(temporary)
            make_fake_d1(root)
            sample, scanned=collect("D1", root, max_train=64,max_dev=64,stride=1)
            self.assertGreaterEqual(scanned["train"],64)
            self.assertGreaterEqual(scanned["development"],64)
            a=score_baselines(sample["train"],sample["development"])
            self.assertTrue(a["2026_test_quarantined"])
            self.assertTrue(a["baselines"]["persistence"]["mae_native_usd"]>=0)
            comparisons=compare_history(
                interval="D1",folder=root,steps=1,seeds=(101,),
                max_train=64,max_dev=64,stride=1)
            self.assertEqual(len(comparisons["results"]),3)
            self.assertFalse(comparisons["independent_test_used"])
            regime=group_report(sample["train"],sample["development"],min_group=32)
            self.assertTrue(regime["regime_thresholds_derived_train_only"])
            self.assertTrue(regime["2026_test_opened"] is False)
            scaling=run_cases(
                sample["train"],sample["development"],interval="D1",
                targets=(2400,),depths=(1,),
                architectures=("modern_gpt_style_mini",),
                steps=1,seeds=(101,),data_origin="ARTIFICIAL_FIXTURE",
            )
            self.assertFalse(scaling["labels_2026_opened"])
            self.assertEqual(len(scaling["results"]),1)
            self.assertIn("direction_accuracy_all",scaling["results"][0])
            self.assertIn("absolute_magnitude_error_bps",scaling["results"][0])

if __name__=="__main__":
    unittest.main()
