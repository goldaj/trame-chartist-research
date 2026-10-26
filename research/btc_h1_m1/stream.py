"""Streaming BTC/USD OHLCV H1/M1 reader from pinned private GitHub Release.

Owner accepts the historical data as-is. Files reside unchanged in a local
cache, not the TRAME Git repository. This reader is offline and never trades.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from research.btc_h1_m1.release_store import DEFAULT_CACHE, H1_FILES, M1_FILES, D1_FILES, ensure_assets
import csv
import gzip
import math


ROOT = DEFAULT_CACHE
CUTOFF = datetime(2026, 7, 1, tzinfo=timezone.utc)
TRAIN_END_EXCLUSIVE = datetime(2022, 1, 1, tzinfo=timezone.utc)
DEVELOPMENT_END_EXCLUSIVE = datetime(2026, 1, 1, tzinfo=timezone.utc)
INTERVALS = {"D1": 86400, "H1": 3600, "M1": 60}
COLUMNS = ("datetime_utc", "open", "high", "low", "close", "volume")
H1_FILE = H1_FILES[0]
FIXED_SCALE = 1000.0  # fixed log-return encoder, not fit from test/future


@dataclass(frozen=True)
class Candle:
    started_at: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    @property
    def zero_volume(self) -> bool:
        return self.volume == 0


@dataclass(frozen=True)
class Case:
    """Available context at origin; target will close one candle later."""
    origin_open: datetime
    target_open: datetime
    decision_time: datetime
    label_available_time: datetime
    encoded_past: tuple[int, ...]
    encoded_target: int
    anchor_usd: float
    target_usd: float
    grade: str


def files_for(interval: str, folder: Path = ROOT) -> tuple[Path, ...]:
    """Use pinned cache in production; allow explicit test-fixture directories."""
    if Path(folder).expanduser() == DEFAULT_CACHE:
        return ensure_assets(interval, directory=folder)
    if interval not in INTERVALS:
        raise ValueError("interval must be D1, H1 or M1")
    names = D1_FILES if interval == "D1" else (H1_FILE,) if interval == "H1" else M1_FILES
    paths = tuple(Path(folder) / name for name in names)
    for path in paths:
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"missing local BTC archive {path.name}")
    return paths


def read_bars(interval: str, folder: Path = ROOT):
    """Yield from gzip, never materialize the full multi-million-candle archive."""
    seconds = INTERVALS.get(interval)
    if seconds is None:
        raise ValueError("interval must be H1 or M1")
    if interval == "D1":
        from research.btc_h1_m1.daily_stream import read_daily_bitstamp_bars
        yield from read_daily_bitstamp_bars(folder)
        return
    prev = None
    for path in files_for(interval, folder):
        with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, strict=True)
            fields = tuple(reader.fieldnames or ())
            if fields[:6] != COLUMNS or any(
                name not in ("source", "quote_currency") for name in fields[6:]
            ):
                raise ValueError(f"unexpected historical columns: {path.name}")
            for row in reader:
                if None in row or any(v is None or v == "" for v in row.values()):
                    raise ValueError("invalid historical row")
                stamp = datetime.fromisoformat(row["datetime_utc"])
                if stamp.tzinfo is None or stamp.utcoffset().total_seconds() != 0:
                    raise ValueError("history must contain UTC timestamps")
                if stamp >= CUTOFF:
                    # Entire quarantined period is excluded before reading prices.
                    continue
                if stamp.year < 2012 or stamp.timestamp() % seconds != 0:
                    raise ValueError("unexpected timestamp or candle grid")
                if interval == "M1":
                    expected_year = int(path.name.rsplit("_", 1)[-1][:4])
                    if stamp.year != expected_year:
                        raise ValueError("minute file year mismatch")
                if prev is not None and (stamp - prev).total_seconds() <= 0:
                    raise ValueError("duplicate or out-of-order bar")
                values = [float(row[k]) for k in COLUMNS[1:]]
                op,hi,lo,cl,vol = values
                if (not all(math.isfinite(v) for v in values) or
                    min(op,hi,lo,cl) <= 0 or vol < 0 or hi < max(op,cl) or lo > min(op,cl)):
                    raise ValueError("invalid OHLCV bar")
                prev = stamp
                yield Candle(stamp,op,hi,lo,cl,vol)


def code_return(previous: float, current: float) -> int:
    if not all(math.isfinite(v) and v > 0 for v in (previous,current)):
        raise ValueError("requires positive finite prices")
    return math.floor(FIXED_SCALE * math.log(current / previous) + 0.5)


def iter_cases(interval: str, folder: Path = ROOT, *, context: int = 20,
               step: int = 1, train_only: bool = False):
    """Generate causal next-candle samples from consecutive non-zero-volume bars.

    D1 uses genuine 2011+ Bitstamp OHLCV; 2010-2011 indicative close-only
    stays out of this trading-like training pipeline.

    A gap or volume=0 breaks the usable context. No artificial interpolation.
    Context contains only observed closes strictly earlier than the label.
    """
    if type(context) is not int or not 1 <= context <= 20:
        raise ValueError("context must be 1..20")
    if type(step) is not int or step < 1:
        raise ValueError("step must be a positive integer")
    seconds=INTERVALS.get(interval)
    if seconds is None:
        raise ValueError("interval must be H1 or M1")
    previous=None
    returns=deque(maxlen=context)
    since=0
    for bar in read_bars(interval, folder):
        if bar.started_at >= DEVELOPMENT_END_EXCLUSIVE:
            # Do not even calculate 2026 target labels.
            break
        if previous is None or (bar.started_at-previous.started_at).total_seconds()!=seconds or bar.zero_volume or previous.zero_volume:
            returns.clear()
            previous=bar
            since=0
            continue
        current_code=code_return(previous.close,bar.close)
        # Train/dev partition based on completed target time.
        target_completed=bar.started_at.timestamp()+seconds
        split="train" if target_completed <= TRAIN_END_EXCLUSIVE.timestamp() else "development"
        if len(returns)==context and since % step == 0 and (
            not train_only or split=="train"
        ):
            yield split, Case(
                origin_open=previous.started_at,
                target_open=bar.started_at,
                decision_time=datetime.fromtimestamp(bar.started_at.timestamp(),tz=timezone.utc),
                label_available_time=datetime.fromtimestamp(target_completed,tz=timezone.utc),
                encoded_past=tuple(returns),
                encoded_target=current_code,
                anchor_usd=previous.close,
                target_usd=bar.close,
                grade=f"bitstamp_{interval}_observed_nonzero_volume"
            )
        returns.append(current_code)
        since += 1
        previous=bar


def limited_preview(interval: str, folder: Path = ROOT, *, limit: int = 5):
    """A very small safe dry run; not a historical performance result."""
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("limit 1..100")
    output=[]
    for split, case in iter_cases(interval,folder):
        output.append({
            "split": split, "origin":case.origin_open.isoformat(),
            "target":case.target_open.isoformat(), "n_past":len(case.encoded_past),
            "anchor_usd":case.anchor_usd,
            "grade":case.grade,
        })
        if len(output)>=limit:
            break
    return output
