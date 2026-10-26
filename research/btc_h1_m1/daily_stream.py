"""Dedicated D1 importer for the pinned BTC Release.

Indicative 2010-2011 close-only prices MUST NOT be converted to fake
OHLCV candles or mixed into the principal Bitstamp training cohorts.
All daily closing prices become observable at 00:00 UTC *next* day.
"""
from __future__ import annotations

import csv
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
import math

from research.btc_h1_m1.release_store import D1_FILES, DEFAULT_CACHE, ensure_assets
from research.btc_h1_m1.stream import Candle, CUTOFF

OHLCV_FIELDS = ("open", "high", "low", "close", "volume")
DAILY_SECONDS = 86400


def _daily_paths(folder=DEFAULT_CACHE):
    root = Path(folder).expanduser()
    if root == DEFAULT_CACHE:
        return ensure_assets("D1", directory=root)
    paths = tuple(root / filename for filename in D1_FILES)
    for path in paths:
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"missing D1 file: {path.name}")
    return paths


def _date_utc(value):
    stamp = date.fromisoformat(value)
    return datetime.combine(stamp, time.min, tzinfo=timezone.utc)


def read_indicative_close_only(folder=DEFAULT_CACHE):
    """Return (date, close) only, NEVER Candle; research metadata only."""
    indicative, _, _ = _daily_paths(folder)
    with indicative.open(newline="", encoding="utf-8") as fp:
        reader = csv.DictReader(fp, strict=True)
        if tuple(reader.fieldnames or ()) != ("date_utc", "close_indicative_usd"):
            raise ValueError("unexpected D1 indicative schema")
        last = None
        for row in reader:
            if None in row or not row.get("date_utc") or not row.get("close_indicative_usd"):
                raise ValueError("malformed D1 indicative")
            started = _date_utc(row["date_utc"])
            price = float(row["close_indicative_usd"])
            if not math.isfinite(price) or price <= 0:
                raise ValueError("invalid indicative price")
            if last is not None and started - last != timedelta(days=1):
                raise ValueError("indicative discontinuity")
            last = started
            yield started, price


def read_daily_bitstamp_bars(folder=DEFAULT_CACHE):
    """Read actual 2011+ Bitstamp OHLCV, without inventing volume or gaps."""
    _, older, recent = _daily_paths(folder)
    previous = None
    for path, schema in (
        (older, ("date_utc",) + OHLCV_FIELDS),
        (recent, ("datetime_utc",) + OHLCV_FIELDS),
    ):
        with path.open(newline="", encoding="utf-8") as fp:
            reader = csv.DictReader(fp, strict=True)
            if tuple(reader.fieldnames or ()) != schema:
                raise ValueError(f"unexpected daily schema: {path.name}")
            for row in reader:
                if None in row or any(v is None or v == "" for v in row.values()):
                    raise ValueError("incomplete D1 OHLCV")
                stamp = (
                    _date_utc(row["date_utc"])
                    if path == older
                    else datetime.fromisoformat(row["datetime_utc"])
                )
                if (stamp.tzinfo is None or stamp.utcoffset() != timedelta(0)
                        or stamp.time() != time.min):
                    raise ValueError("D1 bar must begin midnight UTC")
                if stamp >= CUTOFF:
                    continue
                if previous is not None and stamp <= previous:
                    raise ValueError("duplicate/out-of-order D1 candle")
                op, high, low, close, volume = (float(row[key]) for key in OHLCV_FIELDS)
                if (not all(math.isfinite(v) for v in (op, high, low, close, volume))
                        or min(op, high, low, close) <= 0 or volume < 0
                        or high < max(op, close) or low > min(op, close)):
                    raise ValueError("invalid daily OHLCV values")
                previous = stamp
                yield Candle(stamp, op, high, low, close, volume)
