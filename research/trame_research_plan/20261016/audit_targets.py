"""Historical-label codec audit. No predictive model, fitting, or loss optimization."""
from pathlib import Path
import csv, datetime, hashlib, json, platform
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((HERE/'freeze.json').read_text(encoding='utf-8'))
for name,digest in freeze['files_sha256'].items(): assert sha(HERE/name)==digest,name
assert not (HERE/'target_audit_report.json').exists(),'Use new declared audit; never overwrite'
pr=json.loads((HERE/'audit_protocol.json').read_text(encoding='utf-8'))
raw=ROOT/pr['source']; assert sha(raw)==pr['source_sha256']
records={c:{} for c in pr['currencies']}
skipped_rows=0
with raw.open(encoding='utf-8-sig',newline='') as f:
    for row in csv.DictReader(f):
        date=row['TIME_PERIOD']
        if not pr['date_filter_before_price_parsing'][0]<=date<=pr['date_filter_before_price_parsing'][1]:
            skipped_rows+=1
            continue
        c=row['CURRENCY']
        if c in records and row['OBS_STATUS']=='A' and row['OBS_VALUE'].strip():
            value=float(row['OBS_VALUE'])
            assert np.isfinite(value) and value>0 and date not in records[c]
            records[c][date]=value
dates=sorted(records[pr['currencies'][0]])
assert all(sorted(rec)==dates for rec in records.values())
origins=np.arange(pr['context']-1,len(dates)-pr['future_steps'],dtype=np.int64)
assert len(origins)==pr['expected_origins_per_asset']
idx=origins[:,None]+np.arange(1,21)[None,:]
unique_targets=np.unique(idx)
out={'id':pr['id'],'computed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'freeze':freeze,'source_sha256':sha(raw),'runtime':{'python':platform.python_version(),'numpy':np.__version__},
     'rows_outside_train_not_price_parsed':skipped_rows,
     'source_prices_parsed':len(dates)*6,'origins_per_asset':len(origins),
     'first_origin':dates[int(origins[0])],'last_origin':dates[int(origins[-1])],
     'unique_target_prices':len(unique_targets)*6,'first_target':dates[int(unique_targets[0])],'last_target':dates[int(unique_targets[-1])],
     'currencies':{},'violations':[],'forecast_results':None,'model_built':False,'model_fitted':False,
     'interpretation':'overlapping historical target-label encodings; neither new observations nor predictions; training subset of revised ECB snapshot'}
codes=[]
for c in pr['currencies']:
    p=np.array([records[c][d] for d in dates],dtype=np.float64)
    inc=np.log(p[1:]/p[:-1]); u=np.log(p)
    s0=np.std(inc[origins[:,None]+np.arange(-64,0)[None,:]],axis=1,ddof=0)
    s=np.maximum(s0,1e-6); delta=s/8; u0=u[origins]
    y=(u[idx]-u0[:,None])/delta[:,None]
    n=np.floor(y+.5).astype(np.int64)
    k=np.diff(np.column_stack((np.zeros(len(origins),dtype=np.int64),n)),axis=1)
    rebuilt=u0[:,None]+delta[:,None]*n
    err=np.abs(rebuilt-u[idx]); allowance=64*np.finfo(np.float64).eps*(1+np.abs(u0[:,None])+np.abs(u[idx])+np.abs(delta[:,None]*n))
    breach=err>delta[:,None]/2+allowance
    state=u0.copy(); recursive=[]
    for h in range(20):
        kr=np.floor((u[idx[:,h]]-state)/delta+.5).astype(np.int64)
        recursive.append(kr); state=state+delta*kr
    recursive=np.stack(recursive,axis=1)
    mismatch=np.argwhere(k!=recursive)
    a,b=np.unravel_index(np.argmax(np.abs(k)),k.shape)
    result={'label_presentations':int(k.size),'k_min':int(k.min()),'k_max':int(k.max()),
      'k_abs_quantiles':{str(q):float(np.quantile(np.abs(k),q,method='linear')) for q in [.5,.9,.99,.999,1]},
      'zero_codes':int(np.sum(k==0)),'distinct_codes':int(len(np.unique(k))),
      'outside_core':int(np.sum((k<-2048)|(k>2047))),
      'n_abs_max':int(np.abs(n).max()),'scale_floor_origins':int(np.sum(s0<1e-6)),
      'min_scale':float(s.min()),'max_scale':float(s.max()),
      'max_error_delta_units':float(np.max(err/delta[:,None])),
      'max_log_error':float(err.max()),'bound_violations_with_allowance':int(breach.sum()),
      'closest_rounding_boundary_in_cell_units':float(np.min(.5-np.abs(y-n))),
      'recursive_code_mismatches':int(len(mismatch)),
      'first_mismatch':None if not len(mismatch) else {'row':int(mismatch[0,0]),'h':int(mismatch[0,1]+1)},
      'max_abs_code_example':{'origin':dates[int(origins[a])],'target':dates[int(idx[a,b])],'h':int(b+1),
            'k':int(k[a,b]),'n':int(n[a,b]),'origin_price':float(p[origins[a]]),'target_price':float(p[idx[a,b]]),
            'scale':float(s[a]),'delta':float(delta[a]),'previous_reconstructed_log':float(u0[a]+delta[a]*(n[a,b]-k[a,b]))}}
    if breach.any() or len(mismatch): out['violations'].append({'currency':c,'bounds':int(breach.sum()),'recursive_mismatches':int(len(mismatch))})
    out['currencies'][c]=result;codes.append(k.ravel())
allk=np.concatenate(codes)
out['total']={'label_presentations':int(allk.size),'k_min':int(allk.min()),'k_max':int(allk.max()),
 'distinct_codes':int(len(np.unique(allk))),'outside_core':int(np.sum((allk<-2048)|(allk>2047))),
 'zero_codes':int(np.sum(allk==0)),'zero_fraction':float(np.mean(allk==0)),
 'abs_code_quantiles':{str(q):float(np.quantile(np.abs(allk),q,method='linear')) for q in [.5,.9,.99,.999,1]}}
(HERE/'target_audit_report.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['origins_per_asset','first_origin','last_origin','unique_target_prices','total','violations']},indent=2))
