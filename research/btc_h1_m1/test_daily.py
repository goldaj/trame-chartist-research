"""Validate long-run daily grade boundaries on entirely invented prices."""
import csv
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from research.btc_h1_m1.daily import read_daily
from research.btc_h1_m1.release_store import D1_FILES


def make_fake_d1(root):
    segments=(
        (date(2010,7,18),date(2011,8,17),
         ("date_utc","close_indicative_usd")),
        (date(2011,8,18),date(2011,12,31),
         ("date_utc","open","high","low","close","volume")),
        (date(2012,1,1),date(2026,6,30),
         ("datetime_utc","open","high","low","close","volume")),
    )
    for name,(begin,end,columns) in zip(D1_FILES,segments):
        with (root/name).open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=columns)
            writer.writeheader()
            day=begin
            while day<=end:
                close=round(2.0+(day.year-2010)*11+(day.toordinal()%9)*.04,6)
                if "close_indicative_usd" in columns:
                    writer.writerow({"date_utc":day.isoformat(),
                                     "close_indicative_usd":close})
                else:
                    row={"open":close,"high":close+1,"low":close-1,
                         "close":close,"volume":3}
                    if "date_utc" in columns:
                        row["date_utc"]=day.isoformat()
                    else:
                        row["datetime_utc"]=day.isoformat()+" 00:00:00+00:00"
                    writer.writerow(row)
                day+=timedelta(days=1)


class DailyReferenceTests(unittest.TestCase):
    def test_owner_d1_segments_and_utc_visibility(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            make_fake_d1(folder)
            rows=list(read_daily(directory=folder))
        self.assertEqual(len(rows),5827)
        self.assertEqual(rows[0].day,date(2010,7,18))
        self.assertEqual(rows[-1].day,date(2026,6,30))
        self.assertEqual(rows[0].grade,"indicative_close_only")
        self.assertIsNone(rows[0].open_usd)
        self.assertEqual(rows[396].grade,"bitstamp_spot_ohlcv")
        self.assertEqual(rows[396].available_at_utc.isoformat(),
                         "2011-08-19T00:00:00+00:00")
        self.assertEqual(rows[-1].available_at_utc.isoformat(),
                         "2026-07-01T00:00:00+00:00")

    def test_d1_schema_invalid_aborts(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            make_fake_d1(folder)
            path=folder/D1_FILES[0]
            lines=path.read_text(encoding="utf-8").splitlines()
            path.write_text("\n".join(lines[:2]+lines[3:])+"\n",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"gap or duplicate"):
                list(read_daily(directory=folder))


if __name__=="__main__":
    unittest.main()
