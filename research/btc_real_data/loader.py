"""BTC/USD daily history adapter for user-supplied historical CSV files.

No network, no live trading, no upstream source verification. Reads CSVs
already placed under research/btc_real_data/raw in a local TRAME checkout.
Separate closing-price studies from OHLC execution assumptions.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "raw"
FIRST = date(2010, 7, 18)
LAST = date(2026, 6, 30)
TRAIN_END = date(2021, 12, 31)
DEVELOPMENT_END = date(2025, 12, 31)
QUARANTINE_START = date(2026, 1, 1)
CODE_SCALE = 1000.0
SOURCES = (
    ("btcusd-indicative-close-d1-2010-2011.csv",
     ("date_utc", "close_indicative_usd"), "indicative_close_only",
     date(2010, 7, 18), date(2011, 8, 17)),
    ("btcusd-bitstamp-d1-2011H2.csv",
     ("date_utc", "open", "high", "low", "close", "volume"),
     "bitstamp_spot_ohlcv", date(2011, 8, 18), date(2011, 12, 31)),
    ("btcusd-bitstamp-d1-2012-2026H1.csv",
     ("datetime_utc", "open", "high", "low", "close", "volume"),
     "bitstamp_spot_ohlcv", date(2012, 1, 1), date(2026, 6, 30)),
)


@dataclass(frozen=True)
class DailyBTC:
    day: date
    close: float
    grade: str


@dataclass(frozen=True)
class ForecastCase:
    origin: date
    target: date
    available_at_utc: datetime
    prior_codes: tuple[int, ...]
    target_code: int
    anchor_usd: float
    target_usd: float
    target_grade: str


def _row_date(row: dict[str, str]) -> date:
    if "date_utc" in row:
        return date.fromisoformat(row["date_utc"])
    instant = datetime.fromisoformat(row["datetime_utc"])
    if instant.tzinfo is None or instant.utcoffset() != timedelta(0) or instant.time() != time.min:
        raise ValueError("BTC daily bar timestamp must be midnight UTC")
    return instant.date()


def load_history(directory: Path = ROOT) -> tuple[DailyBTC, ...]:
    """Read fixed three segments without downloading or certifying them."""
    root = Path(directory)
    history: list[DailyBTC] = []
    for filename, columns, grade, begin, end in SOURCES:
        path = root / filename
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"missing local CSV: {path}")
        with path.open("r", encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream, strict=True)
            if tuple(reader.fieldnames or ()) != columns:
                raise ValueError(f"unexpected CSV columns in {filename}")
            segment_count = 0
            for row in reader:
                if None in row or set(row) != set(columns) or any(v is None or not v for v in row.values()):
                    raise ValueError(f"invalid CSV row in {filename}")
                when = _row_date(row)
                if when != FIRST + timedelta(days=len(history)):
                    raise ValueError(f"nonconsecutive BTC day at {when}")
                if not begin <= when <= end:
                    raise ValueError("segment date out of fixed interval")
                close = float(row["close_indicative_usd"] if grade == "indicative_close_only" else row["close"])
                if not (math.isfinite(close) and close > 0):
                    raise ValueError("BTC close must be positive and finite")
                if grade == "bitstamp_spot_ohlcv":
                    op, hi, lo, volume = [float(row[name]) for name in ("open","high","low","volume")]
                    if (not all(math.isfinite(v) for v in (op,hi,lo,volume))
                            or min(op,hi,lo) <= 0 or volume < 0
                            or hi < max(op,close) or lo > min(op,close)):
                        raise ValueError("invalid BTC OHLCV row")
                history.append(DailyBTC(when, close, grade))
                segment_count += 1
            if segment_count != (end-begin).days + 1:
                raise ValueError(f"incomplete BTC segment: {filename}")
    if len(history) != 5827 or history[0].day != FIRST or history[-1].day != LAST:
        raise ValueError("unexpected BTC daily snapshot boundaries")
    return tuple(history)


def quantize_return(old_close: float, new_close: float) -> int:
    """Fixed, non-fitted return quantizer. Never fit it on future labels."""
    if not all(math.isfinite(v) and v > 0 for v in (old_close,new_close)):
        raise ValueError("BTC closes must be finite and positive")
    return math.floor(CODE_SCALE * math.log(new_close / old_close) + 0.5)


def create_cases(history: tuple[DailyBTC, ...], *, context: int = 20) -> dict[str, tuple[ForecastCase, ...]]:
    """Return D+1 targets; 2026 is never loaded into model training/evaluation."""
    if type(context) is not int or not 1 <= context <= 20:
        raise ValueError("context must be in 1..20")
    if len(history) < context + 2:
        raise ValueError("not enough BTC daily data")
    for a,b in zip(history,history[1:]):
        if b.day != a.day + timedelta(days=1):
            raise ValueError("non-contiguous BTC history")
    codes=[quantize_return(a.close,b.close) for a,b in zip(history,history[1:])]
    grouped: dict[str,list[ForecastCase]] = {"train":[],"development":[]}
    for i in range(context,len(codes)):
        origin, future = history[i], history[i+1]
        if future.day <= TRAIN_END:
            target_group="train"
        elif future.day <= DEVELOPMENT_END:
            target_group="development"
        else:
            # Important: don't materialize holdout labels or metrics.
            continue
        grouped[target_group].append(ForecastCase(
            origin=origin.day, target=future.day,
            available_at_utc=datetime.combine(future.day,time.min,tzinfo=timezone.utc),
            prior_codes=tuple(codes[i-context:i]),
            target_code=codes[i],
            anchor_usd=origin.close, target_usd=future.close,
            target_grade=future.grade
        ))
    if not grouped["train"] or not grouped["development"]:
        raise ValueError("missing train or development interval")
    return {k:tuple(v) for k,v in grouped.items()}


def summarize(history: tuple[DailyBTC,...], cases: dict[str,tuple[ForecastCase,...]]) -> dict:
    return {"series":"BTC/USD D1 close; 2010-2011 indicative, later Bitstamp spot",
            "from":history[0].day.isoformat(),"to":history[-1].day.isoformat(),
            "observations":len(history),"train_cases":len(cases["train"]),
            "development_cases":len(cases["development"]),
            "quarantined_interval":"2026-01-01 through 2026-06-30, not evaluated",
            "not_hyperliquid_data":True,
            "past_context_only":True,"real_data_trusted_by_owner":True,
            "provider_vintage_certified":False,"trading_execution_claim":False}


def main(argv=None):
    p=argparse.ArgumentParser(description="Offline TRAME BTC daily data reader; no network")
    p.add_argument("--directory",type=Path,default=ROOT)
    args=p.parse_args(argv)
    history=load_history(args.directory)
    print(json.dumps(summarize(history,create_cases(history)),indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
