"""Post-audit explanation and scalar cross-check of a selected real-data extreme."""
from pathlib import Path
import csv
import datetime
import hashlib
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
plan = json.loads((HERE/'followup_plan.json').read_text(encoding='utf-8'))
assert not (HERE/'followup_scale_report.json').exists()
stamp = {
    'declared_before_followup_calculation_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'post_original_audit': True,
    'plan_sha256': hashlib.sha256((HERE/'followup_plan.json').read_bytes()).hexdigest(),
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
assert not (HERE/'followup_freeze.json').exists()
(HERE/'followup_freeze.json').write_text(json.dumps(stamp, indent=2)+'\n', encoding='utf-8')
ecb = ROOT/'research/trame_poc0/ecb_exploratory'
meta = json.loads((ecb/'audit.json').read_text(encoding='utf-8'))
raw = ecb/meta['raw_file']
assert hashlib.sha256(raw.read_bytes()).hexdigest() == plan['existing_source_sha256']
with raw.open(encoding='utf-8-sig', newline='') as f:
    items = sorted((r['TIME_PERIOD'], float(r['OBS_VALUE'])) for r in csv.DictReader(f)
                   if r['CURRENCY']=='CHF' and r['OBS_STATUS']=='A' and r['OBS_VALUE'].strip())
dates, values = zip(*items)
p = np.array(values, dtype=np.float64)
origins = np.array([i for i, d in enumerate(dates) if '2010-01-01'<=d<='2014-12-31'
                    and i>=255 and i+20<len(dates) and dates[i+20]<='2014-12-31'])
idx = origins[:, None] + np.arange(-255, 1)[None, :]
r = np.log(p[1:]/p[:-1])
scale = np.maximum(np.std(r[origins[:, None]+np.arange(-64, 0)[None, :]], axis=1), 1e-6)
x64 = np.log(p[idx]/p[origins, None])/scale[:, None]
x32 = x64.astype(np.float32)
k = np.floor(8*x32.astype(np.float64)).astype(np.int64)
escape = (k < -2048) | (k > 2047)
escape_origins = origins[np.any(escape, axis=1)]
row, col = np.unravel_index(np.argmin(x32), x32.shape)
i, j = int(origins[row]), int(idx[row, col])
past_returns = [math.log(values[t]/values[t-1]) for t in range(i-63, i+1)]
mean = math.fsum(past_returns)/64
scalar_s = math.sqrt(math.fsum((v-mean)**2 for v in past_returns)/64)
scalar_x = math.log(values[j]/values[i])/max(scalar_s, 1e-6)
assert abs(scalar_s-float(scale[row])) < 1e-14
assert abs(scalar_x-float(x64[row,col])) < 1e-9
assert int(escape.sum()) == 195 and len(escape_origins) == 40
long_s = float(np.std(r[i-255:i], ddof=0))
result = {
    'id': plan['id'], 'provenance': stamp, 'source_sha256': plan['existing_source_sha256'],
    'selection_is_posthoc_exploratory': True,
    'first_escape_origin': dates[int(escape_origins[0])], 'last_escape_origin': dates[int(escape_origins[-1])],
    'escape_exposures': 195, 'escape_origins': 40,
    'minimum': {'origin_date': dates[i], 'historical_input_date': dates[j],
                'current_price_chf_per_eur': values[i], 'historical_price_chf_per_eur': values[j],
                'log_price_ratio': math.log(values[j]/values[i]),
                'scale_64': float(scale[row]), 'scale_255_context_only': long_s,
                'scale_255_over_scale_64': long_s/float(scale[row]),
                'x64': float(x64[row,col]), 'x32': float(x32[row,col]), 'k': int(k[row,col]),
                'scalar_scale_64': scalar_s, 'scalar_x64': scalar_x},
    'scalar_crosscheck_passed': True,
    'normalization_changed': False, 'model_fitted': False, 'forecast_scores': None,
}
(HERE/'followup_scale_report.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2))
