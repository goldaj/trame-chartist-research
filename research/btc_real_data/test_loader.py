"""Offline fixtures for the BTC bridge. No actual market CSV in public CI."""
import csv
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from research.btc_real_data.loader import (
    ROOT, FIRST, LAST, TRAIN_END, DEVELOPMENT_END, SOURCES,
    DailyBTC, load_history, create_cases, quantize_return
)


def write_fake_history(folder: Path):
    folder.mkdir(parents=True, exist_ok=True)
    counter=0
    for name, columns, kind, start, end in SOURCES:
        with (folder/name).open("w", encoding="utf-8", newline="") as stream:
            writer=csv.DictWriter(stream,fieldnames=list(columns))
            writer.writeheader()
            day=start
            while day<=end:
                # Positive, slow drift plus varying returns, entirely fictional.
                price=round(1.0+counter*0.1+(counter%19)*0.01,4)
                if kind=="indicative_close_only":
                    writer.writerow({"date_utc":day.isoformat(),"close_indicative_usd":price})
                else:
                    opening=round(price*0.999,5)
                    row={
                        "open":opening, "high":round(price*1.01,5),
                        "low":round(opening*0.99,5), "close":price,
                        "volume":0 if counter%13==0 else 123.4,
                    }
                    if "datetime_utc" in columns:
                        row["datetime_utc"]=day.isoformat()+" 00:00:00+00:00"
                    else:
                        row["date_utc"]=day.isoformat()
                    writer.writerow(row)
                day+=timedelta(days=1)
                counter+=1


class BridgeTests(unittest.TestCase):
    def test_reader_and_boundaries(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            write_fake_history(folder)
            history=load_history(folder)
            self.assertEqual(len(history),5827)
            self.assertEqual((history[0].day,history[-1].day),(FIRST,LAST))
            self.assertEqual(history[0].grade,"indicative_close_only")
            self.assertEqual(history[-1].grade,"bitstamp_spot_ohlcv")
            cases=create_cases(history)
            self.assertGreater(len(cases["train"]),1000)
            self.assertGreater(len(cases["development"]),1000)
            self.assertEqual(cases["train"][-1].target, TRAIN_END)
            self.assertEqual(cases["development"][0].target, date(2022,1,1))
            self.assertEqual(cases["development"][-1].target, DEVELOPMENT_END)
            first=cases["development"][0]
            self.assertEqual(first.decision_at_utc.isoformat(),"2022-01-01T00:00:00+00:00")
            self.assertEqual(first.label_available_at_utc.isoformat(),"2022-01-02T00:00:00+00:00")
            self.assertEqual(len(first.prior_codes),20)
            self.assertEqual(first.target_code, quantize_return(first.anchor_usd,first.target_usd))
            self.assertFalse(any(c.target >= date(2026,1,1)
                                 for v in cases.values() for c in v))

    def test_mutating_quarantined_2026_does_not_change_usable_cases(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            write_fake_history(folder)
            history=list(load_history(folder))
            before=create_cases(tuple(history))
            for i,h in enumerate(history):
                if h.day>=date(2026,1,1):
                    history[i]=replace(h,close=h.close*20.0)
            after=create_cases(tuple(history))
            self.assertEqual(before,after)

    def test_reject_gap_and_invalid_csv(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            write_fake_history(folder)
            path=folder/SOURCES[0][0]
            lines=path.read_text(encoding="utf-8").splitlines()
            path.write_text("\n".join(lines[:2]+lines[3:])+"\n",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"nonconsecutive"):
                load_history(folder)

    def test_reject_extraneous_future_history_and_bad_context(self):
        with TemporaryDirectory() as tmp:
            folder=Path(tmp)
            write_fake_history(folder)
            history=load_history(folder)
            with self.assertRaises(ValueError):
                create_cases(history,context=21)
            with self.assertRaises(ValueError):
                create_cases(history,context=True)
            with self.assertRaises(ValueError):
                create_cases(history[:10])

    def test_parser_does_not_download_sources(self):
        self.assertTrue(str(ROOT).endswith("research/btc_real_data/raw"))
        self.assertEqual(len(SOURCES),3)
        self.assertEqual(quantize_return(100,100),0)


if __name__=="__main__":
    unittest.main()
