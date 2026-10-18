"""Prepare theoretical specifications and an audit declaration. Reads no market values."""
from pathlib import Path
import datetime, hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def write(name, value):
    p=HERE/name
    assert not p.exists(), str(p)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

old=ROOT/'research/trame_research_plan/20261015/p1b0_candidate.json'
c=json.loads(old.read_text(encoding='utf-8'))
c.update(id='TRAME-P1B0-candidate-0.2',date='2026-10-16',
    parent_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),
    status='theoretical specification; locally sealed before descriptive target audit; no model implementation, training or registration',
    target_code='n[h]=floor((log(P[i+h])-log(P[i]))/delta+1/2); k[h]=n[h]-n[h-1]; n[0]=0',
    state_update='exact integer n[h]=n[h-1]+k[h]; u_hat[h]=log(P[i])+delta*n[h]',
    recurrence_equivalence='Identical to closed-loop DPCM in exact arithmetic; floating recurrence compared in separate audit',
    joint='product over h=1..20 of p(k[h] | H_i,k[1],...,k[h-1])')
c.pop('tail_parameters_trained_on_ordinary_targets')
c['base_parameters_receive_proposed_loss_on_all_target_types']=True
c['bounds_proposal']={'M':256,'S':64,'sigma_min':0.25,'A':4,
    'rationale':'Provisional fixed design: one k unit is s_i/8, so mean bound 32*s_i and sd bound 8*s_i; not empirically validated.',
    'mu':'M*tanh(g_mu/M)',
    'sigma':'sigma_min+(S-sigma_min)*sigmoid(g_sigma)',
    'correction':'A*tanh(g_k/A)',
    'initial_values':{'mu':0,'sigma':8,'all_corrections':0},
    'parameter_initialization':'output matrices zero; g_mu and correction biases zero; g_sigma bias log((8-.25)/(64-8))',
    'predeclared_scale_sensitivity_S':[64,256],
    'sensitivity_status':'hypotheses only; no tuning or predictive comparison executed',
    'support':'all integer codes, not clipped',
    'uniform_joint_moment_bound':'conditional on origin and fixed finite delta; not uniform across all possible origins'}
c['sufficient_joint_first_moment_conditions']['constants']='M=256,S=64,A=4 proposed; S=256 sensitivity; sigma_min=.25; not fitted'
c['architecture']={
    'shared_input_across_heads':'Q affine past encoder from P1-D 0.4; no simultaneous comparison of past encoders',
    'past_tokens':256,'bos_tokens':1,'previous_future_tokens':19,'teacher_forced_sequence_length':276,
    'loss_positions':'BOS predicts k1; token n[h]/8 predicts k[h+1], h=1..19; no history loss',
    'future_numeric_value':'n[h]/8, derived only from previous true codes in teacher forcing, own sampled codes in generation',
    'future_calendar_gap':'zero sentinel meaning unknown, distinguished by FUTURE type; no true future calendar information',
    'future_metadata':'log(P_i), log(s_i), log1p(0), indicator n[h] outside [-2048,2047]',
    'bos_metadata':'same origin constants, gap=0, escape=0; numeric value=0; BOS type',
    'past_metadata':'P1-D four fields; history gap and escape of the past Q code',
    'shared_modules':'P1-D blocks, fixed sinusoidal positions, numeric affine 2d, asset embeddings 6d, four-feature affine 5d, final layernorm 2d, three type embeddings 3d',
    'common_parameter_formula':'12*L*d*d+13*L*d+18*d',
    'arms':{
      'BASE':{'head_outputs':2,'meaning':'mu,sigma; q only, normalizer 1'},
      'FLAT':{'head_outputs':4098,'meaning':'mu,sigma and 4096 independent central correction logits'},
      'HIER':{'head_outputs':520,'meaning':'mu,sigma,512 coarse outputs and 3 pairs of bit outputs; g_k=g_q+sum(g_bit); q=floor(k/8), three remainder bits'}},
    'correction_gauge':'HIER additive component parameters not identifiable; counts are allocated weights, not independent function dimensions',
    'heads_not_information_equivalent':'same conditioning data and base; distinct function classes and capacities',
    'exact_normalizer_core_terms_each_step':4096,
    'head_matrix_flops_per_origin':'2*20*d*r, r in {2,4098,520}; excludes nonlinearities, 4096 cell weights/CDFs and normalization',
    'block_forward_flops_per_origin':'L*(24*n*d*d+4*n*n*d), n=276, dense attention; excludes softmax/LN/activations and backward',
    'precision':'future integer state exact in mathematical contract; finite-range and float32 embedding conversion must be audited before implementation; no universal machine-precision guarantee',
    'unseen_output_codes':'normalizer creates gradients for codes not observed as positive targets; do not apply frozen-unvisited-input-table policy to output heads'}
c['parameter_counts']=[]
for L,d in [(4,128),(6,256),(8,512)]:
    common=12*L*d*d+13*L*d+18*d
    c['parameter_counts'].append({'L':L,'d':d,'common':common,
       'total':{arm:common+v['head_outputs']*(d+1) for arm,v in c['architecture']['arms'].items()},
       'dense_block_forward_flops':L*(24*276*d*d+4*276*276*d),
       'head_forward_matrix_flops':{arm:2*20*d*v['head_outputs'] for arm,v in c['architecture']['arms'].items()}})
c['scoring']={'proposed_training':'mean negative log conditional code mass over 20 future steps',
 'interpretation':'proper likelihood for this fixed discretized path law, not a price-density likelihood',
 'quantizer_comparison':'NLL across different delta or rounding rules not directly comparable',
 'price_evaluation':'native-price pinball and calibration versus P1-D baseline; MC accuracy protocol still open',
 'within_cell_price_law':'not specified; decoded lattice prices are a discrete forecast law, not a calibrated law of all real prices'}
c['open']=['Stable log interval probabilities, derivatives, normalizer and tail sampler; no network or full head numerical audit',
 'Finite arithmetic range for cumulative codes, embeddings and exp(price)',
 'Head expressiveness, possible Gaussian tail misspecification and bounded-parameter saturation',
 'Optimization budget, compute-balanced controls and tests of gradients',
 'Native-price scoring with Monte Carlo diagnostics and independent multi-market evaluation']
write('p1b0_candidate.json',c)
write('audit_protocol.json',{
 'id':'TRAME-P1B-target-audit-01','scope':'Descriptive known training labels only, not forecasting or fitting',
 'source':'research/trame_poc0/ecb_exploratory/raw/ecb_exr_daily_six_1999_2020_20261014T094250Z_b8a684b6331d.csv',
 'source_sha256':'b8a684b6331d3cf0310a1838efdce806495906ead99d672671642c3bf24130de',
 'currencies':['USD','JPY','GBP','CHF','CAD','AUD'],'date_filter_before_price_parsing':['1999-01-01','2009-12-31'],
 'whole_file_hash_reads_bytes_only':True,'context':256,'future_steps':20,'expected_origins_per_asset':2541,
 'scale':'population std of last64 log(P[j]/P[j-1]) ending at origin, floor1e-6; delta=s/8',
 'primary_codec':'canonical integer cumulative n[h]=floor((log(P[i+h])-log(P_i))/delta+.5); k=diff n',
 'comparison_codec':'float64 recursive u_hat += delta*floor((u_target-u_hat)/delta+.5)',
 'metrics':['counts, min/max, zero fraction, abs-code quantiles .5/.9/.99/.999/1, distinct codes, core escapes',
            'unique source target dates vs overlapping label presentations','recurrence code mismatches',
            'canonical error in delta units, closest half-boundary distance, scale floor count',
            'max-abs-k example per currency, ties resolved by first origin then horizon'],
 'floating_error_allowance':'64*float64_eps*(1+abs(log_anchor)+abs(log_target)+abs(delta*n)) in log-price units; engineering diagnostic, not a proven forward-error bound',
 'failure_policy':'report all mismatches or bound violations; no silent repair/exclusion; never replace this audit report',
 'data_status':'revised2026 snapshot; historical training partition already explored; not point-in-time or untouched evidence',
 'predictive_training':False,'development_or_pseudo_test_values_parsed':False,
 'declaration_time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps({'candidate':c['id'],'counts':c['parameter_counts']},indent=2))
