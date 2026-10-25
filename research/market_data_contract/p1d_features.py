"""P1-D origin-local numerical representation from *available* prices only.

No global normalization, no target values, no interpolation. Source
permissions and temporal vintages are enforced by asof.validate_rows.
"""
import math
import numpy as np

from research.market_data_contract.asof import as_of

K_MIN,K_MAX=-8388608,8388607


def p1d_origin_view(rows, *,asset,knowledge_at,context=256):
    if context!=256:
        raise ValueError('candidate P1-D context is exactly 256 observations')
    records=as_of(rows,asset=asset,knowledge_at=knowledge_at,context=context)
    if len(records)!=context:
        raise ValueError('insufficient causally available history')
    prices=np.array([float(q.price) for q in records],dtype=np.float64)
    if not np.isfinite(prices).all() or (prices<=0).any():
        raise ValueError('unrepresentable native price')
    logp=np.log(prices)
    last64=np.diff(logp[-65:])  # 64 observed increments ending at origin
    scale=max(float(np.std(last64,ddof=0)),1e-6)
    anchor=float(prices[-1])
    x64=(logp-logp[-1])/scale
    x32=x64.astype(np.float32)
    if not np.isfinite(x32).all():
        raise ValueError('normalization outside float32')
    # Exact promotion of rounded float32 to float64, as P1-D 0.4.
    q=np.floor(8*x32.astype(np.float64)).astype(np.int64)
    if np.any(q<K_MIN) or np.any(q>K_MAX):
        raise ValueError('precision candidate bound exceeded; stop, do not clip')
    midpoint=(2*q+1)/16.
    if np.any(midpoint.astype(np.float32).astype(np.float64)!=midpoint):
        raise ArithmeticError('quantization midpoint not exactly representable')
    past_gaps=np.array([0]+[
        (a.observed_at-b.observed_at).days
        for b,a in zip(records,records[1:])],dtype=int)
    if np.any(past_gaps[1:]<0):
        raise ValueError('invalid calendar history')
    return {'asset':asset,'anchor':anchor,'scale':scale,
            'date_of_anchor':records[-1].observed_at.isoformat(),
            'n':len(records),'q_codes':tuple(int(x) for x in q),
            'past_gaps_days':tuple(int(x) for x in past_gaps),
            'escape_count':int(np.count_nonzero((q < -2048)|(q > 2047))),
            'future_values_used':False,'normalization_scope':'last 64 PAST observed increments',
            'price_units':records[-1].unit}
