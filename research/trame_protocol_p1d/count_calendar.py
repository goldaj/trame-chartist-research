"""Count admissible origins using existing ECB dates only. No model or price score."""
from pathlib import Path
import csv
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
source_dir = ROOT/'research/trame_poc0/ecb_exploratory'
audit = json.loads((source_dir/'audit.json').read_text(encoding='utf-8'))
raw = source_dir/Path(audit['raw_file'])
assert hashlib.sha256(raw.read_bytes()).hexdigest() == audit['raw_sha256']
currencies = ['USD', 'JPY', 'GBP', 'CHF', 'CAD', 'AUD']
with raw.open(encoding='utf-8-sig', newline='') as stream:
    rows = list(csv.DictReader(stream))
dates_by_currency = {
    c: sorted(row['TIME_PERIOD'] for row in rows if row['CURRENCY'] == c
              and row['OBS_STATUS'] == 'A' and row['OBS_VALUE'].strip())
    for c in currencies
}
dates = dates_by_currency['USD']
assert len(dates) == len(set(dates))
assert all(ds == dates for ds in dates_by_currency.values())
splits = [('train', '1999-01-01', '2009-12-31'),
          ('development', '2010-01-01', '2014-12-31'),
          ('retrospective_pseudo_test', '2015-01-01', '2020-12-31')]
context = 256
horizons = [1, 5, 20]
result = {
    'kind': 'calendar-only design audit, not a forecast evaluation',
    'computed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_sha256': audit['raw_sha256'], 'currency_count': len(currencies),
    'date_count': len(dates), 'context_prices': context, 'horizons_publications': horizons,
    'common_origins_for_all_horizons': True,
    'historical_context_may_precede_split': True,
    'no_proven_point_in_time_vintages': True, 'splits': {},
}
for name, lo, hi in splits:
    inside = [i for i, date in enumerate(dates) if lo <= date <= hi]
    origins = [i for i in inside if i >= context-1 and i+max(horizons) < len(dates)
               and dates[i+max(horizons)] <= hi]
    warmup = [i for i in inside if i < context-1]
    boundary = [i for i in inside if i >= context-1 and i not in origins]
    assert len(inside) == len(origins)+len(warmup)+len(boundary)
    result['splits'][name] = {
        'calendar_range': [lo, hi], 'dates': len(inside), 'origins': len(origins),
        'warmup_origins_excluded': len(warmup), 'boundary_origins_excluded': len(boundary),
        'first_origin': dates[origins[0]], 'last_origin': dates[origins[-1]],
        'asset_origins': len(origins)*len(currencies),
        'target_cells_three_horizons': len(origins)*len(currencies)*len(horizons),
        'maximum_target_date': dates[origins[-1]+max(horizons)],
    }
(HERE/'calendar_counts.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
