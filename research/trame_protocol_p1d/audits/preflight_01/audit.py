"""Descriptive input audit only. No predictor, learned tokenizer, price forecast or fit."""
from pathlib import Path
import csv
import datetime
import hashlib
import json
import platform
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PARENT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


protocol = json.loads((HERE/'protocol.json').read_text(encoding='utf-8'))
freeze = json.loads((HERE/'freeze.json').read_text(encoding='utf-8'))
assert sha(HERE/'protocol.json') == freeze['protocol_sha256']
assert sha(Path(__file__)) == freeze['audit_sha256']
assert sha(HERE/'candidate_snapshot.json') == freeze['candidate_sha256']
assert not (HERE/'report.json').exists(), 'Keep existing reports; use a new documented run'
prior_counts = json.loads((PARENT/'calendar_counts.json').read_text(encoding='utf-8'))
ecb = ROOT/'research/trame_poc0/ecb_exploratory'
source_audit = json.loads((ecb/'audit.json').read_text(encoding='utf-8'))
raw = ecb/source_audit['raw_file']
assert sha(raw) == protocol['source_sha256']
currencies = protocol['currencies']
records = {c: {} for c in currencies}
with raw.open(encoding='utf-8-sig', newline='') as f:
    for row in csv.DictReader(f):
        c = row['CURRENCY']
        if c in records and row['OBS_STATUS'] == 'A' and row['OBS_VALUE'].strip():
            date = row['TIME_PERIOD']
            assert date not in records[c]
            value = float(row['OBS_VALUE'])
            assert np.isfinite(value) and value > 0
            records[c][date] = value
dates = sorted(records[currencies[0]])
assert all(sorted(records[c]) == dates for c in currencies)
assert len(dates) == prior_counts['date_count'] == 5632
prices = {c: np.array([records[c][d] for d in dates], dtype=np.float64) for c in currencies}
context = protocol['context_prices']
horizons = protocol['horizons_publications']
cohorts = {}
for name, (lo, hi) in protocol['splits'].items():
    origins = np.array([i for i, date in enumerate(dates)
                        if lo <= date <= hi and i >= context-1
                        and i+max(horizons) < len(dates)
                        and dates[i+max(horizons)] <= hi], dtype=np.int64)
    assert len(origins) == prior_counts['splits'][name]['origins']
    cohorts[name] = origins

report = {
    'id': protocol['id'], 'computed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': protocol['scope'], 'corpus_status': protocol['corpus_status'],
    'provenance': freeze,
    'runtime': {'python': platform.python_version(), 'numpy': np.__version__},
    'source_sha256': sha(raw), 'source_numeric_prices': sum(len(d) for d in records.values()),
    'splits': {}, 'violations': [],
    'overlapping_contexts_are_not_new_independent_data': True,
    'model_built': False, 'model_fitted': False, 'forecast_scores': None,
}
train_flat_support = set()
train_coarse_support = set()
train_bit_support = [set(), set(), set()]
all_unique_input_keys = set()

for split, origins in cohorts.items():
    idx = origins[:, None] + np.arange(-(context-1), 1)[None, :]
    sidx = origins[:, None] + np.arange(-64, 0)[None, :]
    unique_dates = np.unique(idx)
    split_result = {'origins_per_asset': int(len(origins)), 'currencies': {},
                    'first_input_date': dates[int(unique_dates[0])],
                    'last_input_date': dates[int(unique_dates[-1])],
                    'unique_input_dates_per_asset': int(len(unique_dates))}
    split_flat, split_coarse = set(), set()
    for currency in currencies:
        p = prices[currency]
        increments = np.log(p[1:]/p[:-1])
        scale_raw = np.std(increments[sidx], axis=1, ddof=0)
        scale = np.maximum(scale_raw, 1e-6)
        x64 = np.log(p[idx]/p[origins, None])/scale[:, None]
        x32 = x64.astype(np.float32)
        if not np.all(np.isfinite(x64)) or not np.all(np.isfinite(x32)):
            report['violations'].append({'split': split, 'currency': currency, 'kind': 'nonfinite input'})
            continue
        k_float = np.floor(8*x32.astype(np.float64))
        bound_bad = (k_float < -2**23) | (k_float > 2**23-1)
        if np.any(bound_bad):
            report['violations'].append({'split': split, 'currency': currency,
                                         'kind': 'declared precision bound breach', 'count': int(bound_bad.sum())})
            continue
        k = k_float.astype(np.int64)
        midpoint = (2*k+1)/16
        exact_midpoint = midpoint.astype(np.float32).astype(np.float64) == midpoint
        q = k//8
        r = k-8*q
        bits = [r//4, (r//2)%2, r%2]
        decoded = 8*q + 4*bits[0]+2*bits[1]+bits[2]
        assert np.array_equal(k, decoded)
        assert np.all(exact_midpoint)
        quant_error = np.abs(midpoint-x32.astype(np.float64))
        assert np.max(quant_error) <= 1/16
        escape = (k < -2048) | (k > 2047)
        core = ~escape
        core_k = k[core]
        core_q = q[core]
        core_flat_set = set(map(int, np.unique(core_k)))
        core_coarse_set = set(map(int, np.unique(core_q)))
        split_flat.update(core_flat_set)
        split_coarse.update(core_coarse_set)
        if split == 'train':
            train_flat_support.update(core_flat_set)
            train_coarse_support.update(core_coarse_set)
            for bit_ix, bit in enumerate(bits):
                train_bit_support[bit_ix].update(map(int, np.unique(bit[core])))
        old_k = np.floor(8*x64)
        cast_changed = old_k != k_float
        data = {
            'asset_origins': int(len(origins)), 'input_exposures': int(k.size),
            'unique_underlying_input_prices': int(len(unique_dates)),
            'x32_min': float(x32.min()), 'x32_max': float(x32.max()),
            'k_min': int(k.min()), 'k_max': int(k.max()),
            'scale_min': float(scale.min()), 'scale_max': float(scale.max()),
            'scale_floor_origins': int(np.sum(scale_raw < 1e-6)),
            'escape_exposures': int(escape.sum()), 'origins_with_escape': int(np.any(escape, axis=1).sum()),
            'distinct_core_flat_codes': len(core_flat_set), 'distinct_core_coarse_codes': len(core_coarse_set),
            'changed_cells_due_to_common_float32_parent': int(cast_changed.sum()),
            'origins_with_changed_cells': int(np.any(cast_changed, axis=1).sum()),
            'max_x_rounding_error': float(np.max(np.abs(x32.astype(np.float64)-x64))),
            'max_quantization_error_x32': float(quant_error.max()),
            'exact_midpoint_failures': int((~exact_midpoint).sum()),
            'hierarchical_decode_failures': int(np.sum(k != decoded)),
        }
        if split != 'train':
            unseen_flat = core & ~np.isin(k, sorted(train_flat_support))
            unseen_coarse = core & ~np.isin(q, sorted(train_coarse_support))
            unseen_any_component = unseen_coarse.copy()
            for bit_ix, bit in enumerate(bits):
                unseen_any_component |= core & ~np.isin(bit, sorted(train_bit_support[bit_ix]))
            data.update({
                'new_core_flat_types_vs_pooled_train': len(core_flat_set-train_flat_support),
                'new_core_coarse_types_vs_pooled_train': len(core_coarse_set-train_coarse_support),
                'unseen_flat_exposures_vs_pooled_train': int(unseen_flat.sum()),
                'origins_with_unseen_flat': int(np.any(unseen_flat, axis=1).sum()),
                'unseen_coarse_exposures_vs_pooled_train': int(unseen_coarse.sum()),
                'origins_with_unseen_coarse': int(np.any(unseen_coarse, axis=1).sum()),
                'unseen_any_h_component_exposures': int(unseen_any_component.sum()),
                'origins_with_unseen_any_h_component': int(np.any(unseen_any_component, axis=1).sum()),
            })
        split_result['currencies'][currency] = data
        all_unique_input_keys.update((currency, int(i)) for i in unique_dates)
    values = list(split_result['currencies'].values())
    sums = ['asset_origins','input_exposures','unique_underlying_input_prices','escape_exposures',
            'origins_with_escape','scale_floor_origins','changed_cells_due_to_common_float32_parent',
            'origins_with_changed_cells','exact_midpoint_failures','hierarchical_decode_failures']
    if split != 'train':
        sums += ['unseen_flat_exposures_vs_pooled_train','origins_with_unseen_flat',
                 'unseen_coarse_exposures_vs_pooled_train','origins_with_unseen_coarse',
                 'unseen_any_h_component_exposures','origins_with_unseen_any_h_component']
    split_result['totals'] = {key: sum(v[key] for v in values) for key in sums}
    split_result['pooled_distinct_core_flat_codes'] = len(split_flat)
    split_result['pooled_distinct_core_coarse_codes'] = len(split_coarse)
    if split != 'train':
        split_result['pooled_new_core_flat_types'] = len(split_flat-train_flat_support)
        split_result['pooled_new_core_coarse_types'] = len(split_coarse-train_coarse_support)
    report['splits'][split] = split_result

report['train_support'] = {'flat': sorted(train_flat_support), 'coarse': sorted(train_coarse_support),
                           'bits': [sorted(s) for s in train_bit_support]}
report['total_repeated_input_exposures'] = sum(s['totals']['input_exposures'] for s in report['splits'].values())
report['total_unique_underlying_input_prices_across_splits'] = len(all_unique_input_keys)

# Only dates and indexes are used below, not targets, coefficients or residual values.
b3 = []
train_origins = cohorts['train'].tolist()
for year in protocol['baseline_calendar']['residual_years']:
    lo, hi = f'{year}-01-01', f'{year}-12-31'
    for h in horizons:
        fit = [i for i in train_origins if dates[i+h] < lo]
        residual = [i for i in train_origins if lo <= dates[i] <= hi and dates[i+h] <= hi]
        assert fit and residual
        assert max(dates[i+h] for i in fit) < lo
        assert min(dates[i] for i in residual) >= lo
        b3.append({'year': year, 'horizon': h, 'fit_origins_per_asset': len(fit),
                   'latest_fit_target_date': max(dates[i+h] for i in fit),
                   'residual_origins_per_asset': len(residual),
                   'first_residual_origin': dates[residual[0]], 'last_residual_origin': dates[residual[-1]],
                   'latest_residual_target_date': dates[residual[-1]+h]})
report['b3_calendar_only'] = b3
report['b3_residual_origins_per_asset_by_horizon'] = {
    str(h): sum(r['residual_origins_per_asset'] for r in b3 if r['horizon'] == h) for h in horizons}
report['passed_numeric_preconditions'] = not report['violations']
assert sha(raw) == protocol['source_sha256']
(HERE/'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
compact = {key: report[key] for key in ['id','runtime','passed_numeric_preconditions','violations',
            'total_repeated_input_exposures','total_unique_underlying_input_prices_across_splits',
            'b3_residual_origins_per_asset_by_horizon']}
compact['splits'] = {name: {**s['totals'], 'pooled_distinct_core_flat_codes': s['pooled_distinct_core_flat_codes'],
                           'pooled_distinct_core_coarse_codes': s['pooled_distinct_core_coarse_codes']}
                     for name, s in report['splits'].items()}
print(json.dumps(compact, indent=2))
