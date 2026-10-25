"""Read owner-approved Bitcoin daily closes from the same pinned private Release.

The 2010-2011 earliest segment is indicative close ONLY. Never invent
OHLC or order-book liquidity. This module has no network dependency.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import math
from pathlib import Path

from research.btc_h1_m1.release_store import DEFAULT_CACHE, D1_FILES, ensure_assets


@dataclass(frozen=True)
class DailyClose:
    day: date
    close_usd: float
    grade: str
    open_usd: float | None = None
    high_usd: float | None = None
    low_usd: float | None = None
    volume_btc: float | None = None

    @property
    def available_at_utc(self) -> datetime:
        return datetime.combine(self.day + timedelta(days=1),
                                datetime.min.time(),tzinfo=timezone.utc)


def read_daily(*, directory: Path = DEFAULT_CACHE):
    """Yield daily BTC/USD prices; exact archives, no provenance investigation."""
    root=Path(directory).expanduser()
    if root == DEFAULT_CACHE:
        paths=ensure_assets("D1",directory=root)
    else:
        paths=tuple(root / name for name in D1_FILES)
        for p in paths:
            if not p.is_file() or p.is_symlink():
                raise FileNotFoundError(f"missing D1 history: {p.name}")
    schemas=(
        ("date_utc","close_indicative_usd"),
        ("date_utc","open","high","low","close","volume"),
        ("datetime_utc","open","high","low","close","volume"),
    )
    prev_day=None
    for ix,path in enumerate(paths):
        with path.open("r",encoding="utf-8",newline="") as f:
            reader=csv.DictReader(f,strict=True)
            if tuple(reader.fieldnames or ())!=schemas[ix]:
                raise ValueError(f"unexpected D1 columns in {path.name}")
            for row in reader:
                if None in row or any(v is None or v=="" for v in row.values()):
                    raise ValueError("invalid D1 row")
                if ix == 2:
                    instant=datetime.fromisoformat(row["datetime_utc"])
                    if (instant.tzinfo is None
                            or instant.utcoffset()!=timedelta(0)
                            or instant.time()!=datetime.min.time()):
                        raise ValueError("D1 timestamp must be midnight UTC")
                    when=instant.date()
                else:
                    when=date.fromisoformat(row["date_utc"])
                if prev_day is not None and when!=prev_day+timedelta(days=1):
                    raise ValueError(f"D1 gap or duplicate at {when}")
                close=float(row["close_indicative_usd"] if ix==0 else row["close"])
                if not math.isfinite(close) or close<=0:
                    raise ValueError("D1 close must be positive and finite")
                if ix==0:
                    item=DailyClose(when,close,"indicative_close_only")
                else:
                    op,hi,lo,vol=[float(row[k]) for k in ("open","high","low","volume")]
                    if (not all(math.isfinite(v) for v in (op,hi,lo,vol))
                            or min(op,hi,lo)<=0 or vol<0
                            or lo>min(op,close) or hi<max(op,close)):
                        raise ValueError("invalid D1 OHLCV")
                    item=DailyClose(when,close,"bitstamp_spot_ohlcv",op,hi,lo,vol)
                yield item
                prev_day=when
