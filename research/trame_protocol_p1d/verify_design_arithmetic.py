"""Arithmetic checks of a documentary design; no market prices, codec or model run.

Constructed examples establish finite-precision counterexamples, not forecast scores.
Only the standard library is used. This file does not read any market dataset.
"""
from pathlib import Path
import datetime
import hashlib
import json
import math
import struct

HERE = Path(__file__).resolve().parent


def f32(x):
    return struct.unpack('!f', struct.pack('!f', x))[0]


counts = []
expected = [(797717, 864021, 1322005),
            (4747797, 4880405, 5796373),
            (25237525, 25502741, 27334677)]
for (layers, width, heads), expected_row in zip(
        [(4, 128, 4), (6, 256, 8), (8, 512, 8)], expected):
    # Count each operation separately from the compact formula in the document.
    qkv = 3 * width * width + 3 * width
    out = width * width + width
    mlp = width * (4 * width) + 4 * width + (4 * width) * width + width
    block_norm = 4 * width
    common = (layers * (qkv + out + mlp + block_norm)
              + 6 * width + 5 * width + 2 * width + 21 * width + 21)
    assert common == 12 * layers * width ** 2 + 13 * layers * width + 34 * width + 21
    numeric = common + 2 * width
    hierarchical = common + (512 + 3 * 2 + 2) * width
    flat = common + (4096 + 2) * width
    assert (numeric, hierarchical, flat) == expected_row
    assert width % heads == 0
    counts.append(dict(layers=layers, width=width, heads=heads,
                       common=common, C_Q=numeric, H=hierarchical, F=flat,
                       F_minus_H=flat-hierarchical))

all_codes = set()
for k in range(-2048, 2048):
    coarse = k // 8
    remainder = k - 8 * coarse
    bits = (remainder // 4, (remainder // 2) % 2, remainder % 2)
    code = (coarse, *bits)
    assert -256 <= coarse <= 255
    assert k == 8*coarse + 4*bits[0] + 2*bits[1] + bits[2]
    midpoint = (2*k+1)/16
    assert f32(midpoint) == midpoint
    all_codes.add(code)
assert len(all_codes) == 4096

# Boundary witnesses; the general sufficient condition is proved in the note.
boundary_checks = []
for k in [-2**23, -2**23+1, -1, 0, 2**23-2, 2**23-1]:
    midpoint = (2*k+1)/16
    assert f32(midpoint) == midpoint
    boundary_checks.append(dict(k=k, midpoint=midpoint))
outside_k = 2**23
outside_midpoint = (2*outside_k+1)/16
assert f32(outside_midpoint) != outside_midpoint

# Why quantization must start from the same x as the continuous reference.
below = math.nextafter(0.125, -math.inf)
edge = 0.125
assert below != edge and f32(below) == f32(edge)
old_indices = [math.floor(8*x) for x in [below, edge]]
new_indices = [math.floor(8*f32(x)) for x in [below, edge]]
assert old_indices == [0, 1] and new_indices == [1, 1]

# Illustrative, non-market values: median interpolation need not commute with exp.
price_interpolation = 0.5*1 + 0.5*9
log_interpolation = math.exp(0.5*math.log(1) + 0.5*math.log(9))
assert price_interpolation == 5 and abs(log_interpolation-3) < 1e-12

result = {
    'computed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': 'Documentary arithmetic verification only; constructed examples; no market dataset read',
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'all_assertions_passed': True,
    'parameter_counts': counts,
    'core_integer_bijections_checked': len(all_codes),
    'float32_exact_midpoint_boundary_witnesses': boundary_checks,
    'float32_failure_witness': {
        'k': outside_k, 'exact_midpoint': outside_midpoint,
        'float32_midpoint': f32(outside_midpoint)},
    'rounding_order_counterexample': {
        'float64_values': [below, edge], 'common_float32': f32(edge),
        'quantize_float64_before_cast': old_indices,
        'quantize_common_float32': new_indices},
    'interpolation_example_not_market_data': {
        'prices': [1, 9], 'price_space_median': price_interpolation,
        'exp_log_space_median': log_interpolation},
    'real_data_range_audited': False,
    'predictor_implemented': False, 'predictor_trained': False,
    'forecast_results': None,
}
(HERE/'design_arithmetic_checks.json').write_text(
    json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
print(json.dumps(result, indent=2, ensure_ascii=False))
