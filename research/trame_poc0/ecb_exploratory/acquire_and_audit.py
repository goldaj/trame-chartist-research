"""One-off acquisition/audit of official ECB EXR daily references, no models.

Only writes below this script's directory. Raw responses are exclusive-create.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import io
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)
URL = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD+JPY+GBP+CHF+CAD+AUD.EUR.SP00.A?startPeriod=1999-01-01&endPeriod=2020-12-31&format=csvdata"
CURRENCIES = ["USD", "JPY", "GBP", "CHF", "CAD", "AUD"]
START, END = dt.date(1999, 1, 1), dt.date(2020, 12, 31)
STAMP = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
META = {
    "source": "ECB statistics",
    "requested_url": URL,
    "requested_start_period": START.isoformat(),
    "requested_end_period": END.isoformat(),
    "requested_currencies": CURRENCIES,
    "retrieval_started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "kind": "daily euro foreign exchange reference rates; not OHLCV",
    "units": "units of foreign currency per 1 EUR",
    "source_page": "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html",
    "usage_policy": "https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html",
    "api_documentation": "https://data.ecb.europa.eu/help/api/data",
}

if "--offline" in sys.argv:
    manifests = sorted(RAW.glob("ecb_exr_daily_six_1999_2020_*.metadata.json"))
    if len(manifests) != 1:
        raise ValueError("Offline audit expects one unambiguous acquisition manifest")
    META = json.loads(manifests[0].read_text(encoding="utf-8"))
    raw_path = (ROOT / META["raw_path"]).resolve()
    if not raw_path.is_relative_to(RAW.resolve()):
        raise ValueError("Manifest path outside permitted raw directory")
    content = raw_path.read_bytes()
    if hashlib.sha256(content).hexdigest() != META["sha256"]:
        raise ValueError("Immutable raw digest mismatch")
else:
    try:
        request = Request(URL, headers={"Accept": "text/csv", "User-Agent": "LCM-research-data-audit/1.0"})
        with urlopen(request, timeout=45) as response:
            content = response.read(30_000_001)
            if len(content) > 30_000_000:
                raise ValueError("Response exceeds bounded 30 MB acquisition limit")
            META.update({"http_status": response.status, "resolved_url": response.url,
                         "response_headers": dict(response.headers.items())})
        META["retrieval_finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        META["bytes"] = len(content)
        META["sha256"] = hashlib.sha256(content).hexdigest()
        raw_path = RAW / f"ecb_exr_daily_six_1999_2020_{STAMP}_{META['sha256'][:12]}.csv"
        with raw_path.open("xb") as f:
            f.write(content)
        META["raw_path"] = str(raw_path.relative_to(ROOT))
        with (RAW / f"{raw_path.stem}.metadata.json").open("x", encoding="utf-8") as f:
            json.dump(META, f, indent=2, ensure_ascii=False)
    except Exception as exc:
        META["acquisition_error"] = f"{type(exc).__name__}: {exc}"
        with (ROOT / f"acquisition_failure_{STAMP}.json").open("x", encoding="utf-8") as f:
            json.dump(META, f, indent=2, ensure_ascii=False)
        raise

reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
rows = list(reader)
required = {"KEY", "FREQ", "CURRENCY", "CURRENCY_DENOM", "EXR_TYPE", "EXR_SUFFIX", "TIME_PERIOD", "OBS_VALUE"}
if not required.issubset(set(reader.fieldnames or [])):
    raise ValueError(f"Unexpected CSV schema: {reader.fieldnames}")

grouped = defaultdict(list)
key_counts = Counter()
bad = []
missing = []
for index, row in enumerate(rows, start=2):
    key_counts[(row["KEY"], row["TIME_PERIOD"])] += 1
    try:
        date = dt.date.fromisoformat(row["TIME_PERIOD"])
        assert row["CURRENCY"] in CURRENCIES, "unrequested currency"
        assert row["FREQ"] == "D" and row["CURRENCY_DENOM"] == "EUR", "wrong dimension"
        assert row["EXR_TYPE"] == "SP00" and row["EXR_SUFFIX"] == "A", "wrong series type"
        assert START <= date <= END, "date outside requested bounds"
        if not row["OBS_VALUE"].strip():
            missing.append({"currency": row["CURRENCY"], "date": date.isoformat(), "status": row.get("OBS_STATUS", "")})
            continue
        val = float(row["OBS_VALUE"])
        assert math.isfinite(val) and val > 0, "nonfinite or nonpositive value"
    except Exception as exc:
        bad.append({"csv_row": index, "reason": str(exc), "key": row.get("KEY"), "time": row.get("TIME_PERIOD")})
        continue
    grouped[row["CURRENCY"]].append((date, val, row))

dates = sorted({d for observations in grouped.values() for d, _, _ in observations})
calendar = [START + dt.timedelta(days=i) for i in range((END - START).days + 1)]
weekdays = {d for d in calendar if d.weekday() < 5}
missing_weekdays = sorted(weekdays - set(dates))
yearly = []
summary = {}
for currency in CURRENCIES:
    observations = sorted(grouped[currency], key=lambda a: a[0])
    obs_dates = [d for d, _, _ in observations]
    gaps = Counter((b - a).days for a, b in zip(obs_dates, obs_dates[1:]))
    summary[currency] = {
        "rows": len(observations), "unique_dates": len(set(obs_dates)),
        "raw_rows": sum(r["CURRENCY"] == currency for r in rows),
        "explicit_missing_values": sum(r["currency"] == currency for r in missing),
        "first_date": obs_dates[0].isoformat() if obs_dates else None,
        "last_date": obs_dates[-1].isoformat() if obs_dates else None,
        "missing_vs_union_dates": [d.isoformat() for d in dates if d not in set(obs_dates)],
        "weekend_observations": sum(d.weekday() >= 5 for d in obs_dates),
        "calendar_day_gap_counts": dict(sorted(gaps.items())),
        "min_value": min((v for _, v, _ in observations), default=None),
        "max_value": max((v for _, v, _ in observations), default=None),
        "first_value": observations[0][2]["OBS_VALUE"] if observations else None,
        "last_value": observations[-1][2]["OBS_VALUE"] if observations else None,
        "OBS_STATUS": dict(Counter(r.get("OBS_STATUS", "") for _, _, r in observations)),
        "OBS_CONF": dict(Counter(r.get("OBS_CONF", "") for _, _, r in observations)),
        "TITLE": sorted({r.get("TITLE", "") for _, _, r in observations}),
        "TITLE_COMPL": sorted({r.get("TITLE_COMPL", "") for _, _, r in observations}),
        "UNIT": sorted({r.get("UNIT", "") for _, _, r in observations}),
        "UNIT_MULT": sorted({r.get("UNIT_MULT", "") for _, _, r in observations}),
    }
    for year in range(START.year, END.year + 1):
        yearly.append({"currency": currency, "year": year, "numeric_observations": sum(d.year == year for d in obs_dates),
                       "explicit_missing_values": sum(r["currency"] == currency and r["date"].startswith(str(year)) for r in missing)})

audit = {
    "source": "ECB statistics", "raw_file": META["raw_path"], "raw_sha256": META["sha256"],
    "audit_generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "scope": "Exploratory data acquisition and quality audit only; no fitted model, no performance evaluation",
    "requested_period": [START.isoformat(), END.isoformat()],
    "total_rows": len(rows), "valid_rows": sum(len(v) for v in grouped.values()),
    "columns": reader.fieldnames, "distinct_series": sorted({r["KEY"] for r in rows}),
    "duplicate_series_date_keys": sum(count - 1 for count in key_counts.values() if count > 1),
    "invalid_rows": bad,
    "explicit_missing_values_count": len(missing),
    "explicit_missing_values_status_counts": dict(Counter(r["status"] for r in missing)),
    "explicit_missing_dates": sorted({r["date"] for r in missing}),
    "observation_status_counts_all_rows": dict(Counter(r.get("OBS_STATUS", "") for r in rows)),
    "union_date_count": len(dates),
    "intersection_date_count": len(set.intersection(*(set(d for d, _, _ in grouped[c]) for c in CURRENCIES))),
    "calendar_day_count": len(calendar), "weekday_count": len(weekdays),
    "weekdays_without_any_observation_count": len(missing_weekdays),
    "weekdays_without_any_observation": [d.isoformat() for d in missing_weekdays],
    "missing_weekday_interpretation": "Not automatically data defects: ECB publication calendar includes TARGET closures; no external calendar equivalence asserted.",
    "currency_summary": summary,
    "point_in_time_limit": "Current downloaded vintage of historical values; source TIME_PERIOD is not a proven original release timestamp.",
    "data_not_included": ["open", "high", "low", "close of exchange session", "volume", "bid", "ask", "intraday path"],
    "reserved_crypto_data_accessed": False,
}
with (ROOT / "audit.json").open("w", encoding="utf-8") as f:
    json.dump(audit, f, indent=2, ensure_ascii=False)
with (ROOT / "counts_by_year.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["currency", "year", "numeric_observations", "explicit_missing_values"])
    writer.writeheader()
    writer.writerows(yearly)
with (ROOT / "weekday_nonpublication_candidates.csv").open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "weekday_iso", "source_status", "interpretation"])
    explicit_missing_dates = {r["date"] for r in missing}
    writer.writerows((d.isoformat(), d.isoweekday(), "H" if d.isoformat() in explicit_missing_dates else "no row", "nonpublication; do not impute") for d in missing_weekdays)
print(json.dumps({"raw_file": META["raw_path"], "bytes": META["bytes"], "sha256": META["sha256"],
                  "total_rows": len(rows), "numeric_values": audit["valid_rows"], "union_dates": len(dates), "invalid_rows": len(bad), "explicit_missing": len(missing),
                  "duplicates": audit["duplicate_series_date_keys"], "weekday_absences": len(missing_weekdays),
                  "per_currency": {k: {kk: vv for kk, vv in v.items() if kk in ["rows", "first_date", "last_date", "first_value", "last_value", "OBS_STATUS", "OBS_CONF", "UNIT", "UNIT_MULT"]} for k, v in summary.items()}}, ensure_ascii=False, indent=2))
