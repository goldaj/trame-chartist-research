"""TRAME POC0: reproducible research measurements, not a forecasting/trading model."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import argparse, calendar, csv, hashlib, io, json, math, urllib.request, zipfile
import numpy as np

ROOT = Path(__file__).resolve().parent
P = json.loads((ROOT / 'protocol.json').read_text(encoding='utf-8'))
RAW, OUT = ROOT / 'raw', ROOT / 'results'
HOUR = 3600000

def stamp():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')

def freeze():
    path = ROOT / 'freeze.json'
    record = {'protocol_sha256': sha((ROOT/'protocol.json').read_bytes()), 'analysis_sha256': sha(Path(__file__).read_bytes())}
    if path.exists():
        old = json.loads(path.read_text(encoding='utf-8'))
        assert all(old[k] == v for k, v in record.items()), 'Frozen protocol or analysis has changed; record a new version first'
        return old
    record['frozen_at_utc'] = stamp()
    save(path, record)
    return record

def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'TRAME-personal-research/0.1'})
    with urllib.request.urlopen(request, timeout=45) as r:
        body = r.read(6_000_001)
        assert len(body) <= 6_000_000, 'Unexpected response size'
        return body, {'status': r.status, 'last_modified': r.headers.get('Last-Modified'), 'etag': r.headers.get('ETag')}

def validate_archive(body, checksum, filename):
    expected = checksum.decode('ascii').strip().split()
    assert len(expected) == 2 and expected[1].lstrip('*') == filename, 'Bad checksum filename'
    assert sha(body) == expected[0], 'Checksum mismatch'
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        assert z.namelist() == [filename[:-4]+'.csv'], 'Unexpected archive member'
        info = z.infolist()[0]
        assert info.file_size <= 12_000_000, 'Unexpected uncompressed size'
        return z.read(info).decode('utf-8')

def acquire(job):
    asset, month = job
    assert asset in P['assets'] and month in P['months_download_allowed'], 'Download outside preregistered development scope'
    name = f'{asset}-1h-{month}.zip'
    url = f"{P['source']}{asset}/1h/{name}"
    path = RAW / asset / name
    meta_path = path.with_suffix('.provenance.json')
    if path.exists():
        body, chk = path.read_bytes(), Path(str(path)+'.CHECKSUM').read_bytes()
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
    else:
        chk, _ = fetch(url+'.CHECKSUM')
        body, headers = fetch(url)
        validate_archive(body, chk, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        Path(str(path)+'.CHECKSUM').write_bytes(chk)
        meta = {'asset': asset, 'month': month, 'url': url, 'checksum_url': url+'.CHECKSUM', 'retrieved_at_utc': stamp(), 'sha256': sha(body), 'bytes': len(body), **headers}
        save(meta_path, meta)
    content = validate_archive(body, chk, name)
    rows, audit = parse(content, month)
    assert meta['sha256'] == sha(body)
    return asset, rows, {**meta, **audit}

def parse(content, month):
    year, mon = map(int, month.split('-'))
    start = int(datetime(year, mon, 1, tzinfo=timezone.utc).timestamp()*1000)
    expected = calendar.monthrange(year, mon)[1]*24
    end = start + expected*HOUR
    rows = []
    for row in csv.reader(io.StringIO(content)):
        assert len(row) == 12, 'Unexpected schema'
        ts = int(row[0]); o,h,l,c,v = map(float, row[1:6])
        assert start <= ts < end and ts % HOUR == 0, 'Timestamp outside month or misaligned'
        assert int(row[6]) == ts+HOUR-1, 'Unexpected close timestamp'
        assert all(math.isfinite(x) for x in (o,h,l,c,v)), 'Nonfinite observation'
        assert min(o,h,l,c)>0 and v>=0 and l<=min(o,c)<=max(o,c)<=h, 'Invalid OHLCV'
        assert not rows or ts > rows[-1][0], 'Duplicate or out-of-order timestamp'
        rows.append((ts,o,h,l,c,v))
    assert rows, 'Empty monthly archive'
    missing = sorted(set(range(start,end,HOUR))-set(r[0] for r in rows))
    return rows, {'observations': len(rows), 'calendar_slots': expected, 'missing_hours': len(missing), 'missing_open_times_utc': [datetime.fromtimestamp(t/1000,timezone.utc).isoformat() for t in missing]}

def aggregate(rows, hours=4):
    groups = {}
    step = HOUR*hours
    for r in rows:
        groups.setdefault(r[0]//step*step, []).append(r)
    result = []
    for t, rs in sorted(groups.items()):
        if [r[0] for r in rs] == [t+HOUR*k for k in range(hours)]:
            result.append((t, rs[0][1], max(r[2] for r in rs), min(r[3] for r in rs), rs[-1][4], sum(r[5] for r in rs)))
    return result

def segments(rows, hours):
    cuts = [0] + [i for i in range(1,len(rows)) if rows[i][0]-rows[i-1][0] != HOUR*hours] + [len(rows)]
    return [rows[a:b] for a,b in zip(cuts[:-1],cuts[1:]) if b>a]

def features(rows, hours):
    records = []
    for seg in segments(rows,hours):
        a = np.asarray(seg,dtype=float)
        closes = np.log(a[:,4])
        for i in range(65,len(seg)):
            prev = a[i-1,4]; o,h,l,c,v = a[i,1:6]
            sigma = max(float(np.std(np.diff(closes[i-65:i]),ddof=0)),1e-6)
            ref = max(float(np.median(a[i-64:i,5])),1e-12)
            x = [math.log(o/prev),math.log(c/o),math.log(h/max(o,c)),math.log(min(o,c)/l),math.log1p(v/ref)]
            records.append({'t':int(a[i,0]),'x':x,'prev':prev,'sigma':sigma,'ref':ref,'true':[o,h,l,c],'volume':v})
    return records

def fit(x):
    fields = []
    for j in range(5):
        a=x[:,j]; nonzero=a[a!=0]
        inner=np.unique(np.quantile(nonzero,np.linspace(0,1,64)[1:-1])) if len(nonzero) else np.array([])
        ids=np.searchsorted(inner,nonzero,side='right')
        centers=[float(np.median(nonzero[ids==k])) if np.any(ids==k) else float(inner[min(k,len(inner)-1)]) for k in range(len(inner)+1)] if len(nonzero) else [0.0]
        med={str(s):float(np.median(a[np.sign(a)==s])) if np.any(np.sign(a)==s) else 0.0 for s in [-1,0,1]}
        med['0']=0.0
        fields.append({'inner':inner.tolist(),'centers':centers,'sign_median':med,'min':float(a.min()),'max':float(a.max())})
    return fields

def encode(x,sigma,codec,book):
    if codec=='continuous': return x.copy(),None
    if codec in ('fixed','adaptive'):
        step=np.full_like(x,0.001)
        if codec=='adaptive': step[:,:4]=0.1*sigma[:,None]
        step[:,4]=0.05
        ids=np.rint(x/step).astype(np.int64)
        return ids*step,ids
    decoded=np.zeros_like(x); ids=np.zeros_like(x,dtype=np.int64)
    for j,field in enumerate(book):
        if codec=='quantile64':
            k=np.searchsorted(field['inner'],x[:,j],side='right')
            decoded[:,j]=np.array(field['centers'])[k]
            ids[:,j]=k+1
            decoded[x[:,j]==0,j]=0; ids[x[:,j]==0,j]=0
        elif codec=='signs':
            ids[:,j]=np.sign(x[:,j]).astype(np.int64)
            decoded[:,j]=[field['sign_median'][str(k)] for k in ids[:,j]]
        else: raise ValueError(codec)
    return decoded,ids

def reconstruct(decoded,previous,refs):
    o=previous*np.exp(decoded[:,0]); c=o*np.exp(decoded[:,1])
    h=np.maximum(o,c)*np.exp(decoded[:,2]); l=np.minimum(o,c)*np.exp(-decoded[:,3])
    v=refs*np.expm1(decoded[:,4])
    return np.column_stack([o,h,l,c]),v

def stats(a):
    a=np.asarray(a).ravel()
    if len(a)==0: return {'n':0}
    return {'n':int(len(a)),'mean':float(a.mean()),'p50':float(np.quantile(a,.5)),'p95':float(np.quantile(a,.95)),'p99':float(np.quantile(a,.99)),'max':float(a.max())}

def measure(records,hours,codec,book,tail,train_ids):
    x=np.array([r['x'] for r in records]); sigma=np.array([r['sigma'] for r in records])
    prev=np.array([r['prev'] for r in records]); refs=np.array([r['ref'] for r in records]); true=np.array([r['true'] for r in records]); vol=np.array([r['volume'] for r in records])
    decoded,ids=encode(x,sigma,codec,book); prices,vhat=reconstruct(decoded,prev,refs)
    errors=np.abs(np.log(prices/true))*10000
    valid=(prices[:,2]<=np.minimum(prices[:,0],prices[:,3])) & (np.maximum(prices[:,0],prices[:,3])<=prices[:,1]) & (vhat>=0)
    drift=[]; segment_ends=[]; acc=0.0; last=None
    for r,delta in zip(records,(decoded[:,0]+decoded[:,1]-x[:,0]-x[:,1])*10000):
        if last is None or r['t']-last!=hours*HOUR:
            if last is not None: segment_ends.append(abs(acc))
            acc=0.0
        acc+=float(delta); drift.append(abs(acc)); last=r['t']
    segment_ends.append(abs(acc))
    output={'bars':len(records),'ohlc_log_bps':stats(errors),'close_log_bps':stats(errors[:,3]),'tail_bars':int(sum(np.abs(x[:,1])>=tail)),'tail_ohlc_log_bps':stats(errors[np.abs(x[:,1])>=tail]),'volume_log_reference_error':stats(np.abs(decoded[:,4]-x[:,4])),'volume_relative_error_positive':stats(np.abs(vhat[vol>0]-vol[vol>0])/vol[vol>0]),'zero_volumes':int(sum(vol==0)),'zero_volume_decoded_nonzero':int(sum(vhat[vol==0]!=0)),'invalid_bars':int(sum(~valid)),'conditional_close_drift_log_bps':stats(drift),'conditional_segment_end_drift_log_bps':stats(segment_ends),'outside_training_support_per_field':[float(np.mean((x[:,j]<b['min'])|(x[:,j]>b['max']))) for j,b in enumerate(book)]}
    if ids is not None:
        tuples=[tuple(r) for r in ids.tolist()]
        output['distinct_tuples']=len(set(tuples))
        output['unseen_tuple_share']=float(np.mean([r not in train_ids for r in tuples]))
        output['distinct_symbols_per_field']=[len(set(ids[:,j].tolist())) for j in range(5)]
    return output

def event_diagnostic(rows,hours):
    events=[]; censored=[]
    for seg in segments(rows,hours):
        anchor=math.log(seg[0][4]); last=seg[0][0]
        for r in seg[1:]:
            displacement=math.log(r[4])-anchor
            steps=math.floor(abs(displacement)/.005)
            if steps:
                signed=steps if displacement>0 else -steps
                anchor+=signed*.005
                events.append({'close_time':r[0]+hours*HOUR-1,'steps':signed,'elapsed_hours':(r[0]-last)/HOUR,'residual_log':math.log(r[4])-anchor})
                last=r[0]
        censored.append({'end_close_time':seg[-1][0]+hours*HOUR-1,'hours':(seg[-1][0]-last)/HOUR})
    return {'events':len(events),'multi_step_events':sum(abs(e['steps'])>1 for e in events),'elapsed_hours':stats([e['elapsed_hours'] for e in events]),'right_censored_tails':censored,'max_abs_residual_log':max((abs(e['residual_log']) for e in events),default=0)}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--freeze-only',action='store_true'); args=parser.parse_args()
    record=freeze()
    if args.freeze_only:
        print(json.dumps(record)); return
    jobs=[(a,m) for a in P['assets'] for m in P['months_download_allowed']]
    allrows={a:[] for a in P['assets']}; audits=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for a,rows,audit in pool.map(acquire,jobs):
            allrows[a].extend(rows); audits.append(audit)
            print(a,audit['month'],len(rows),'missing',audit['missing_hours'],flush=True)
    save(OUT/'data_manifest.json',{'started_from':record,'generated_at_utc':stamp(),'archives':audits,'observations':sum(len(r) for r in allrows.values()),'missing_hours':sum(r['missing_hours'] for r in audits)})
    start_dev=int(datetime(2021,9,1,tzinfo=timezone.utc).timestamp()*1000)
    result={'generated_at_utc':stamp(),'protocol':record,'purpose':P['purpose'],'timeframes':{}}
    for hours in [1,4]:
        series={a:rs if hours==1 else aggregate(rs,hours) for a,rs in allrows.items()}
        data={a:features(rs,hours) for a,rs in series.items()}
        train=[r for rs in data.values() for r in rs if r['t']<start_dev]
        dev={a:[r for r in rs if r['t']>=start_dev] for a,rs in data.items()}
        tx=np.array([r['x'] for r in train]); ts=np.array([r['sigma'] for r in train])
        book=fit(tx); tail=float(np.quantile(np.abs(tx[:,1]),.99))
        save(OUT/f'codebook_{hours}h.json',{'fit_end_exclusive':'2021-09-01','fields':book,'tail_abs_body_99pct':tail})
        section={'raw_bars_per_asset':{a:len(rs) for a,rs in series.items()},'usable_train':len(train),'usable_dev':sum(map(len,dev.values())),'warmup_excluded_total':sum(map(len,series.values()))-sum(map(len,data.values())),'tail_abs_body_99pct':tail,'codecs':{},'events_close_only_development':{a:event_diagnostic([r for r in rs if r[0]>=start_dev],hours) for a,rs in series.items()}}
        for codec in P['codecs']:
            _,tid=encode(tx,ts,codec,book)
            training_ids=set(map(tuple,tid.tolist())) if tid is not None else set()
            section['codecs'][codec]={a:measure(rs,hours,codec,book,tail,training_ids) for a,rs in dev.items()}
        result['timeframes'][str(hours)+'h']=section
    save(OUT/'measurements.json',result)
    print('DONE',OUT,flush=True)

if __name__=='__main__': main()
