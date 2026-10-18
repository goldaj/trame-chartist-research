"""Documentary arithmetic only. No market dataset, forecasting model or learned tokenizer."""
from pathlib import Path
from fractions import Fraction as F
import datetime, hashlib, json, math

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
out=HERE/'design_checks.json'
assert not out.exists(), 'Preserve existing report; create a new audit for a revision'
totals=[]
for L,d in [(4,128),(6,256),(8,512)]:
    common=12*L*d*d+13*L*d+34*d+21
    values={'affine':common+2*d,'periodic':common+18*d,'mlp':common+18*d+32,
            'H+':common+520*d,'F+':common+4098*d}
    totals.append({'L':L,'d':d,**values})
assert [(x['periodic'],x['mlp']) for x in totals]==[(799765,799797),(4751893,4751925),(25245717,25245749)]
dates=2541; assets=6; batch_dates=32; epochs=30
batches=math.ceil(dates/batch_dates); examples=dates*assets*epochs
runs=8*(3*2+5)
budget={'runs':runs,'tuning_runs':8*3*2,'repeat_runs':8*5,'updates_per_run':batches*epochs,
        'examples_per_run':examples,'campaign_updates':runs*batches*epochs,
        'campaign_examples':runs*examples,'campaign_context_vectors':runs*examples*256,
        'three_sizes_runs':3*runs,'three_sizes_two_budgets_runs':3*runs*2}
assert budget['campaign_examples']==40249440
assert budget['campaign_context_vectors']==10303856640
assert dates%batch_dates==13

delta=F(1,8)
def recurrence(path):
    state=F(0); ks=[]; states=[]; errors=[]
    for value in path:
        ratio=(value-state)/delta+F(1,2)
        k=ratio.numerator//ratio.denominator
        state+=delta*k
        error=state-value
        assert abs(error)<=delta/2
        ks.append(k); states.append(str(state)); errors.append(str(error))
    return {'k':ks,'states':states,'errors':errors}
constructed=[F(0),F(1,16),F(-1,16),F(17,16),F(-35,16),F(0),F(1,1000)]
example=recurrence(constructed)
prefix=constructed[:4]
a=recurrence(prefix+[F(100),F(-200)])
b=recurrence(prefix+[F(-777),F(999)])
assert a['k'][:4]==b['k'][:4] and a['states'][:4]==b['states'][:4]
cases=0
for j in range(-64,65):
    recurrence([F(j,64),F(-j,80),F(j,100)])
    cases+=3

# Generic finite rational identity checks the normalization algebra only.
# It does NOT test the Gaussian CDF, infinite support, numerical tails or a neural head.
q={-2:F(1,10),-1:F(1,5),0:F(2,5),1:F(1,5),2:F(1,10)}
w={-2:F(1),-1:F(1,2),0:F(3),1:F(2),2:F(1)}
Z=sum(q[k]*w[k] for k in q)
assert sum(q[k]*w[k]/Z for k in q)==1
Z_out=sum(q[k] for k in [-2,2])+sum(q[k]*w[k] for k in [-1,0,1])
assert Z_out==Z
z=[-1.645,-1.282,-0.674,0,0.674,1.282,1.645]
raw=[z[0]]+[math.log(math.expm1(v-u)) for u,v in zip(z,z[1:])]
decoded=[raw[0]]
for r in raw[1:]: decoded.append(decoded[-1]+math.log1p(math.exp(r)))
assert max(abs(x-y) for x,y in zip(z,decoded))<1e-14
inputs=[ROOT/'research/trame_protocol_p1d/protocol_candidate.json',HERE/'p1b0_candidate.json',HERE/'plan.json']
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'integer, rational and scalar design arithmetic only; no market inputs; no predictive implementation',
 'inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'parameter_counts':totals,'budget':budget,
 'recurrence':{'constructed_log_values':[str(x) for x in constructed],'delta':str(delta),'example':example,
               'extra_constructed_transitions':cases,'bound_passed':True,'prefix_unchanged_by_future_suffix':True},
 'normalizer_algebra':{'finite_rational_example_only':True,'Z':str(Z),'mass_exactly_one':True,'gaussian_implementation_tested':False},
 'head_bias_inverse_softplus_check':True,'model_instantiated':False,'trained':False,'market_performance':None,
 'joint_moment_bound':'analytical derivation in document 12; not established by numeric examples'}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':True,'counts':totals,'budget':budget,'recurrence_transitions':cases+len(constructed)},indent=2))
