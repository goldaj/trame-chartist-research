"""Constructed arithmetic and standard-library probability illustrations, not a predictor."""
from pathlib import Path
from fractions import Fraction as F
import datetime, hashlib, json, math, platform

HERE=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (HERE/'design_report.json').exists(),'Keep reports immutable'
c=json.loads((HERE/'p1b0_candidate.json').read_text(encoding='utf-8'))
round_up=lambda x: math.floor(x+F(1,2))
tested=0
for delta in [F(1,8),F(1,64),F(3,17)]:
    for u0 in [F(0),F(5,3),F(-7,11)]:
        old_n=0; old_u=u0
        for h in range(401):
            value=u0+F(((h*137)%401)-200,73)
            k=round_up((value-old_u)/delta)
            n=round_up((value-u0)/delta)
            assert n==old_n+k
            rec=u0+delta*n
            assert abs(rec-value)<=delta/2
            old_n=n;old_u=rec;tested+=1
module_counts=[]
for row in c['parameter_counts']:
    L,d=row['L'],row['d']
    modules={'qkv':L*(3*d*d+3*d),'attention_out':L*(d*d+d),
      'mlp_up':L*(4*d*d+4*d),'mlp_down':L*(4*d*d+d),'block_layernorms':L*4*d,
      'numeric_affine':2*d,'asset_embeddings':6*d,'metadata_affine':4*d+d,'final_layernorm':2*d,'type_embeddings':3*d}
    assert sum(modules.values())==row['common']
    for arm,r in [('BASE',2),('FLAT',4098),('HIER',520)]:
        assert sum(modules.values())+d*r+r==row['total'][arm]
    module_counts.append({'L':L,'d':d,'modules':modules,'total':row['total']})

# Limited finite arguments only; this is not a robust log-CDF routine.
Phi=lambda x: .5*(1+math.erf(x/math.sqrt(2)))
illustrations=[]
for a,b in [(0,1),(8,9),(10,11),(28,29)]:
    naive=Phi(b)-Phi(a)
    tail=.5*(math.erfc(a/math.sqrt(2))-math.erfc(b/math.sqrt(2)))
    assert tail>0
    illustrations.append({'standard_normal_interval':[a,b],'naive_cdf_difference':naive,
       'erfc_difference':tail,'log_mass_via_erfc':math.log(tail),
       'scope':'finite selected inputs only, no general stability or derivative guarantee'})
bounds=[]
for S in c['bounds_proposal']['predeclared_scale_sensitivity_S']:
    M=c['bounds_proposal']['M'];A=c['bounds_proposal']['A']
    q_upper=.5*math.erfc((2048.5-M)/(S*math.sqrt(2)))+.5*math.erfc((2047.5-M)/(S*math.sqrt(2)))
    bound=min(1,math.exp(A)*q_upper)
    bounds.append({'M':M,'S':S,'A':A,'outside_core_probability_upper_bound':bound,
       'log10_upper_bound':math.log10(bound),
       'reason':'outside weight=1 and Z>=exp(-A); each Gaussian tail maximized separately, so a conservative common bound'})
out={'computed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':sha(Path(__file__)),
     'candidate_sha256':sha(HERE/'p1b0_candidate.json'),'runtime_python':platform.python_version(),
     'market_data_read':False,'model_implemented':False,'normalizer_or_sampler_implemented':False,
     'rational_transitions_checked':tested,'allocated_module_counts':module_counts,
     'cdf_illustrations':illustrations,'analytic_tail_bound_numerical_values':bounds,
     'limitations':['math.erfc returns zero for sufficiently large arguments; examples are not a log-CDF implementation',
                    'No gradients, Monte Carlo, normalization stress test, training, forecasting or price scoring tested']}
(HERE/'design_report.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'rational_transitions':tested,'cdf':illustrations,'bounds':bounds},indent=2))
