"""CI tests use wholly fabricated tiny gzip files, not Bitstamp prices."""
import csv
from datetime import datetime, timedelta, timezone
import gzip
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from research.btc_h1_m1.stream import (
    H1_FILE, M1_FILES, COLUMNS, files_for, read_bars, iter_cases, limited_preview
)
from research.btc_h1_m1.experiment import compare_history


def _write_gz(path, year, count, seconds, *, zero_at=None, gap_at=None):
    start=datetime(year,1,1,tzinfo=timezone.utc)
    with gzip.open(path,"wt",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS)
        writer.writeheader()
        for i in range(count):
            t=start+timedelta(seconds=(i+(1 if gap_at is not None and i>=gap_at else 0))*seconds)
            price=round(100+i*0.08+(i%7)*0.03,5)
            writer.writerow({
                "datetime_utc":t.isoformat(sep=" "),
                "open":price,"high":price+0.1,"low":price-0.1,
                "close":price,"volume":0 if i==zero_at else 15.0
            })


def artificial_files(folder):
    folder.mkdir(parents=True,exist_ok=True)
    # H1 history includes a real time gap from 2012 to 2022 (not interpolated).
    with gzip.open(folder/H1_FILE,"wt",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=COLUMNS);w.writeheader()
        for year in (2012,2022,2026):
            for i in range(100):
                t=datetime(year,1,1,tzinfo=timezone.utc)+timedelta(hours=i)
                p=round(100+i*.1+((year-2012)*12),4)
                w.writerow({"datetime_utc":t.isoformat(sep=" "),
                            "open":p,"high":p+.1,"low":p-.1,"close":p,
                            "volume":1.0})
    for year,name in zip(range(2012,2027),M1_FILES):
        _write_gz(folder/name,year,70,60)


class SyntheticCompressedHistoryTests(unittest.TestCase):
    def test_all_archives_stream_and_do_not_expose_2026_targets(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            artificial_files(folder)
            self.assertEqual(len(files_for("M1",folder)),15)
            self.assertEqual(len(files_for("H1",folder)),1)
            self.assertEqual(sum(1 for _ in read_bars("M1",folder)),15*70)
            self.assertEqual(len(limited_preview("H1",folder,limit=3)),3)
            for interval in ("H1","M1"):
                cases=list(iter_cases(interval,folder,step=1))
                self.assertTrue(any(k=="train" for k,c in cases))
                self.assertTrue(any(k=="development" for k,c in cases))
                self.assertFalse(any(c.target_open.year==2026 for _,c in cases))
                for _,c in cases:
                    self.assertEqual(len(c.encoded_past),20)
                    self.assertLess(c.decision_time,c.label_available_time)
                    self.assertLessEqual(c.origin_open,c.decision_time)

    def test_three_architectures_on_fake_hourly_and_minute(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            artificial_files(folder)
            for interval in ("H1","M1"):
                with self.subTest(interval=interval):
                    r=compare_history(interval=interval,folder=folder,
                        steps=1,seeds=(11,),max_train=40,max_dev=40,stride=1)
                    self.assertEqual(len(r["results"]),3)
                    self.assertTrue(r["2026_observations_quarantined"])
                    self.assertFalse(r["independent_test_used"])
                    self.assertGreater(r["baseline"]["persistence_mae_usd"],0)
                    for row in r["results"]:
                        self.assertGreater(row["dev_nll"],0)

    def test_gap_zero_volume_and_invalid_options(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            artificial_files(folder)
            _write_gz(folder/M1_FILES[0],2012,70,60,zero_at=30,gap_at=50)
            cases=list(iter_cases("M1",folder,step=1))
            in_2012=[c for split,c in cases if c.target_open.year==2012]
            self.assertTrue(in_2012)
            self.assertFalse(any(c.target_open.minute in (30,31,50) for c in in_2012))
            with self.assertRaises(ValueError):
                list(iter_cases("M1",folder,context=21))
            with self.assertRaises(ValueError):
                list(iter_cases("M1",folder,step=0))
            with self.assertRaises(ValueError):
                list(read_bars("D1",folder))
            with self.assertRaises(ValueError):
                compare_history(interval="H1",folder=folder,steps=0)


if __name__=="__main__":
    unittest.main()
