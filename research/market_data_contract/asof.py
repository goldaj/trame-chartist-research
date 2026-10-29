"""Strict point-in-time financial-data contract. No provider/network code.

A historical 'observation time' is NOT evidence of knowledge at that time.
A value becomes eligible only at its recorded available_at (UTC).
All real sources require explicit licensing + timestamp provenance approval.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import math


REQUIRED={'source_id','asset','observed_at','available_at',
          'price','unit','revision'}


def utc(value):
    if not isinstance(value,str) or not value.endswith(('Z','+00:00')):
        raise ValueError('timestamps must be explicit UTC ISO-8601 strings')
    try:
        d=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError as exc:
        raise ValueError('invalid UTC timestamp') from exc
    if d.tzinfo is None or d.utcoffset().total_seconds()!=0:
        raise ValueError('non-UTC timestamp')
    return d


@dataclass(frozen=True)
class Quote:
    source_id:str
    asset:str
    observed_at:datetime
    available_at:datetime
    price:Decimal
    unit:str
    revision:int


def validate_manifest(manifest):
    if not isinstance(manifest,dict) or not manifest.get('source_id'):
        raise ValueError('source_id required')
    status=manifest.get('rights_status')
    if status == 'approved_synthetic':
        if not manifest.get('synthetic'):
            raise PermissionError('synthetic approval cannot masquerade as real')
    elif status == 'verified_real':
        if manifest.get('synthetic') or not all(manifest.get(k) for k in (
                'rights_evidence_url','data_owner','permitted_research_use',
                'available_at_method','download_provenance')):
            raise PermissionError('verified real source needs explicit evidence')
    else:
        raise PermissionError('source rights, vintage or metadata unverified')
    return manifest


def validate_rows(rows, manifest):
    validate_manifest(manifest)
    if not isinstance(rows,list) or not rows:
        raise ValueError('at least one observation is required')
    parsed=[]
    for raw in rows:
        if not isinstance(raw,dict) or set(raw)!=REQUIRED:
            raise ValueError('exact point-in-time fields required')
        if raw['source_id']!=manifest['source_id']:
            raise ValueError('source mismatch')
        if not isinstance(raw['asset'],str) or not raw['asset'] or not isinstance(raw['unit'],str) or not raw['unit']:
            raise ValueError('asset and unit required')
        if type(raw['revision']) is not int or raw['revision']<0:
            raise ValueError('revision must be a nonnegative integer')
        observed=utc(raw['observed_at'])
        available=utc(raw['available_at'])
        if available<observed:
            raise ValueError('source cannot publish a value before its observation')
        if type(raw['price']) is not str:
            raise TypeError('price must be decimal string, not binary float')
        try:
            price=Decimal(raw['price'])
        except InvalidOperation as exc:
            raise ValueError('invalid decimal price') from exc
        if not price.is_finite() or price<=0:
            raise ValueError('positive finite native price required')
        parsed.append(Quote(raw['source_id'],raw['asset'],observed,available,
                            price,raw['unit'],raw['revision']))
    groups={}
    units={}
    for q in parsed:
        key=(q.asset,q.observed_at)
        groups.setdefault(key,[]).append(q)
        if q.asset in units and units[q.asset]!=q.unit:
            raise ValueError('native price unit changed silently')
        units[q.asset]=q.unit
    for key,versions in groups.items():
        ordered=sorted(versions,key=lambda x:x.revision)
        if [v.revision for v in ordered]!=list(range(len(ordered))):
            raise ValueError('revision ids must start at 0 and be contiguous')
        if any(a.available_at >= b.available_at for a,b in zip(ordered,ordered[1:])):
            raise ValueError('revisions must have strictly increasing knowledge time')
    return sorted(parsed,key=lambda q:(q.asset,q.observed_at,q.revision))


def as_of(verified_rows, *,asset,knowledge_at,context=None):
    """Exactly the latest known revision per observed time at decision time."""
    moment=utc(knowledge_at)
    latest={}
    for q in verified_rows:
        if q.asset!=asset or q.observed_at>moment or q.available_at>moment:
            continue
        key=q.observed_at
        if key not in latest or q.revision>latest[key].revision:
            latest[key]=q
    result=[latest[t] for t in sorted(latest)]
    if context is not None:
        if type(context) is not int or context<1:
            raise ValueError('context must be positive integer')
        result=result[-context:]
    return result


def forecast_origin_evidence(verified_rows, *,asset,knowledge_at,
                             horizon,split_end,context):
    """Check target eligibility WITHOUT returning target values as model inputs.

    Only provenance/availability metadata enters this decision, never raw
    future prices. Future target values are only for a later scorer.
    """
    if type(horizon) is not int or horizon<1:
        raise ValueError('positive observation horizon needed')
    moment=utc(knowledge_at)
    end=utc(split_end)
    if end<=moment:
        return {'eligible':False,'reason':'target window cannot end before origin'}
    past=as_of(verified_rows,asset=asset,knowledge_at=knowledge_at,context=context)
    if len(past)<context:
        return {'eligible':False,'reason':'insufficient past available context'}
    # Selection on stable observed timestamps, not on price magnitude.
    future_times=sorted({q.observed_at for q in verified_rows
                         if q.asset==asset and moment<q.observed_at<=end})
    if len(future_times)<horizon:
        return {'eligible':False,'reason':'future target outside split'}
    return {'eligible':True,'origin_known_context':len(past),
            'target_observed_at':future_times[horizon-1].isoformat(),
            'future_price_revealed':False}
