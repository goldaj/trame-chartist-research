"""TRAME Research Lab v0.1: honest, local, read-only-of-research sources.

Runs ONLY fabricated market-like laws, no downloads/APIs/trading accounts.
Writes explicit standalone HTML and machine JSON reports, with opt-in
overwrite. Never labels synthetic training as financial prediction.
"""
import argparse
import html
import json
import math
from pathlib import Path
from tempfile import NamedTemporaryFile

from research.mini_gpt_synthetic.experiment import run as run_gpt
from research.p1b0_numerics.rollout_study import run as run_rollout
from research.benchmark_synthetic.bootstrap import paired_group_report,moving_block_interval


REQUIRED_RESULTS=('model','toy_forecast','paired_benchmark')


def make_example_benchmark():
    """A manufactured gain, to test the scoring path, not model skill."""
    records=[]
    for i in range(120):
        # Intentionally make the alternative forecast better than persistence.
        # Its score is engineering proof only, not a genuine forecast.
        records.append({
            'asset':'FAKE-UNIT','origin_index':i,'target_index':i+1,
            'horizon':1,'anchor':100.,'actual':101.,'forecast':100.8})
    group=paired_group_report(records)['FAKE-UNIT::h=1']
    interval=moving_block_interval(group['paired_gains'],block=20,
                                   seed=20261025,resamples=300)
    return {'origin_count':group['n_origin_presentations'],
            'toy_gain_native':group['mean_paired_gain_native'],
            'toy_ci_block95':interval['percentile_ci95'],
            'manufactured_gain_by_construction':True,
            'not_statistical_evidence_for_trame':True}


def run_lab(*,train_steps=40):
    if type(train_steps) is not int or not 1 <= train_steps <= 200:
        raise ValueError('train_steps must be an integer between 1 and 200')
    return {
        'lab_version':'0.1-research-only',
        'data_origin':'ARTIFICIAL GENERATED LOCALLY',
        'market_data_accessed':False,
        'financial_forecast_evaluated':False,
        'no_trading_or_network_actions':True,
        'limitations':[
            'Synthetic AR(1) oracle is not a real financial market',
            'Development experiments are not untouched test data',
            'BASE/HIER/FLAT cost and parameter counts are unequal',
            'Tail conditional draw does not solve unconditional extreme-event simulation',
            'Real sources and point-in-time vintages are still unqualified',
            'Cannot infer profits, trade returns, backtest reliability, or future market direction',
        ],
        'model':run_gpt(steps=train_steps),
        'toy_forecast':run_rollout(),
        'paired_benchmark':make_example_benchmark(),
    }


def render_html(report):
    if not all(key in report for key in REQUIRED_RESULTS):
        raise ValueError('incomplete laboratory report')
    exp=report['model']
    ctrl=exp['controls_development']
    nll=[
        ('TRAME mini-Transformer',exp['end_development_nll']),
        ('Oracle synthétique connu',ctrl['oracle_known_generator_nll']),
        ('Régression linéaire train-only',ctrl['linear_train_only_nll']),
        ('Constante train-only',ctrl['constant_mu0_train_scale_nll']),
    ]
    for _,v in nll:
        if not isinstance(v,(float,int)) or not math.isfinite(v) or v<=0:
            raise ValueError('invalid synthetic development NLL')
    for key in ('optimization_steps','model_parameters','development_paths'):
        if type(exp[key]) is not int or exp[key] < 1:
            raise ValueError(f'invalid experiment counter: {key}')
    sim=report['toy_forecast']
    for key in ('price_median','price_q10','price_q90','empirical_CRPS_price_units'):
        value=sim[key]
        if type(value) not in (float,int) or not math.isfinite(value):
            raise ValueError(f'invalid simulated result: {key}')
    if not (0 < sim['price_q10'] <= sim['price_median'] <= sim['price_q90']):
        raise ValueError('inconsistent simulated quantiles')
    if sim['empirical_CRPS_price_units'] < 0:
        raise ValueError('negative CRPS is impossible')
    b=report['paired_benchmark']
    if b.get('manufactured_gain_by_construction') is not True:
        raise ValueError('benchmark must be marked as manufactured')
    for value in (b['toy_gain_native'], *b['toy_ci_block95']):
        if type(value) not in (float,int) or not math.isfinite(value):
            raise ValueError('invalid fabricated benchmark result')
    if len(b['toy_ci_block95']) != 2 or b['toy_ci_block95'][0] > b['toy_ci_block95'][1]:
        raise ValueError('invalid interval order')
    maxv=max(v for _,v in nll)*1.15
    lines=[]
    for label,value in nll:
        safe=html.escape(label)
        width=round(400*value/maxv,2)
        lines.append(
            '<g transform="translate(0,{y})">'
            '<text x="0" y="15" fill="#d6e6f3" font-size="13">{label}</text>'
            '<rect x="265" y="1" width="{width}" height="19" rx="4" fill="#5eace3"/>'
            '<text x="{end}" y="15" font-size="12" fill="#fff">{value:.4f}</text>'
            '</g>'.format(y=len(lines)*41,label=safe,width=width,
                          end=271+width,value=value))
    chart='\n'.join(lines)
    accessible_rows='\n'.join(
        '<tr><th scope="row">{}</th><td>{:.4f}</td></tr>'.format(
            html.escape(label), value
        ) for label,value in nll
    )
    def decimal(v):
        return html.escape(f'{float(v):.4f}')
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>TRAME Research Lab 0.1 | expérience artificielle</title>
<style>
:root{{color-scheme:dark}}*{{box-sizing:border-box}}
body{{margin:0;background:#0b1323;color:#e8f0f8;font:15px/1.6 system-ui,Arial,sans-serif}}
main{{max-width:1100px;margin:30px auto;padding:0 24px 45px}}
h1{{font-size:clamp(26px,4vw,42px);line-height:1.1;margin:12px 0 8px}}
h2{{font-size:19px;margin:0 0 12px}}
small,.muted{{color:#aec0d3}}.eyebrow{{font-weight:700;letter-spacing:.12em;color:#7ed3e5}}
.banner{{border:1px solid #d29d59;border-radius:9px;padding:12px 16px;margin:20px 0;color:#ffdaaa;background:#2b221e}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;margin:22px 0}}
section{{border:1px solid #2a415b;background:#13223a;border-radius:11px;padding:22px;min-width:0}}
.stat{{font-size:26px;font-weight:700;color:#97e2ff}}.stats{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}}
svg{{width:100%;height:auto;overflow:visible}}
ul{{padding-left:20px}}.foot{{border-top:1px solid #293e55;margin-top:28px;padding-top:18px;color:#abc0d5}}
table{{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;margin-top:14px}}
caption{{text-align:left;font-weight:600;color:#e8f0f8;margin-bottom:6px}}
th,td{{padding:8px;border-bottom:1px solid #40536c;text-align:left}}
td{{text-align:right}}thead th{{font-weight:700;color:#cde7fc}}
.skip-link{{position:absolute;left:-9999px;top:6px;background:#fff;color:#000;padding:8px}}
.skip-link:focus{{left:8px;z-index:10}}
</style></head><body><a class="skip-link" href="#results">Aller aux résultats</a><main id="results" tabindex="-1">
<p class="eyebrow">TRAME / LABORATOIRE DE RECHERCHE LOCAL</p>
<h1>Expériences probabilistes synthétiques</h1>
<p class="muted">Version 0.1 · aucune connexion marché, aucun ordre, aucune prédiction financière mesurée.</p>
<div class="banner"><strong>DONNÉES ARTIFICIELLES UNIQUEMENT.</strong>
Ces courbes et pertes ont été générées à partir d'une loi simple connue.
Les scores ne démontrent ni avantage financier, ni rendement potentiel.</div>
<div class="grid">
<section><h2>Mini-Transformer vs témoins</h2>
<p class="muted">NLL moyenne sur le développement artificiel (plus petit = meilleur).
La comparaison reflète un seul budget d'optimisation exploratoire.</p>
<svg viewBox="0 0 750 185" aria-hidden="true" focusable="false">{chart}</svg>
<table><caption>NLL de développement sur données artificielles (plus petit = meilleur)</caption>
<thead><tr><th scope="col">Méthode</th><th scope="col">NLL</th></tr></thead>
<tbody>{accessible_rows}</tbody></table>
<p><small>{int(exp['optimization_steps'])} mises à jour, {int(exp['model_parameters'])}
paramètres, {int(exp['development_paths'])} chemins de développement.</small></p></section>
<section><h2>Simulation artificielle à 20 pas</h2>
<div class="stats"><div><span class="muted">Médiane fictive</span>
<div class="stat">{decimal(sim['price_median'])}</div></div>
<div><span class="muted">Intervalle empirique 10–90 %</span>
<div class="stat">{decimal(sim['price_q10'])} – {decimal(sim['price_q90'])}</div></div>
<div><span class="muted">CRPS prix fictifs</span>
<div class="stat">{decimal(sim['empirical_CRPS_price_units'])}</div></div>
<div><span class="muted">Origine fictive</span>
<div class="stat">100</div></div></div></section>
<section><h2>Test logiciel de comparaison appariée</h2>
<p>Gain fabriqué volontairement en faveur du modèle :
<strong>{decimal(b['toy_gain_native'])}</strong> unité fictive.</p>
<p>Intervalle par bootstrap de blocs :
{decimal(b['toy_ci_block95'][0])} – {decimal(b['toy_ci_block95'][1])}.</p>
<p class="muted">Un résultat imposé par construction ne constitue
aucune preuve de prédiction. Il vérifie simplement l'outil de score.</p></section>
<section><h2>Verrous avant recherche de marché</h2>
<ul><li>Licences, disponibilité et révisions des sources réelles</li>
<li>Préenregistrement des partitions et témoins financiers</li>
<li>Validation des cas extrêmes et stabilité hors distribution</li>
<li>Test externe indépendant, bloqué tant que les précédents manquent</li></ul></section>
</div>
<div class="foot">TRAME Research Lab est un démonstrateur reproductible.
Le rapport JSON adjacent contient les nombres bruts, la graine
et les limites scientifiques. Aucun conseil d'investissement.</div>
</main></body></html>"""


def write_reports(report,output,*,overwrite=False):
    htmlpath=Path(output)
    if htmlpath.suffix.lower()!='.html':
        raise ValueError('destination must have .html extension')
    jsonpath=htmlpath.with_suffix('.json')
    for path in (htmlpath,jsonpath):
        if path.exists() and not overwrite:
            raise FileExistsError(f'{path} already exists; use --overwrite explicitly')
        if not path.parent.is_dir():
            raise FileNotFoundError(f'parent directory does not exist: {path.parent}')
    htmltext=render_html(report)
    jsontext=json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
    # Stage BOTH complete outputs in the destination directory before replacing
    # either one. This guards staging errors, NOT cross-file atomicity.
    staged=[]
    try:
        for path,body in ((jsonpath,jsontext),(htmlpath,htmltext)):
            with NamedTemporaryFile(
                mode='w',encoding='utf-8',dir=path.parent,
                prefix=f'.{path.name}.',suffix='.tmp',delete=False,
            ) as tmp:
                staged.append(Path(tmp.name))
                tmp.write(body)
        # HTML is the entrypoint: place it last so an interrupted pair is
        # less likely to appear complete. A two-file transaction is NOT atomic.
        staged[0].replace(jsonpath)
        staged[1].replace(htmlpath)
    finally:
        for path in staged:
            path.unlink(missing_ok=True)
    return str(htmlpath),str(jsonpath)


def main(argv=None):
    ap=argparse.ArgumentParser(description='TRAME Research Lab: synthetic-only offline demo')
    ap.add_argument('--output',default='trame_research_lab.html')
    ap.add_argument('--steps',type=int,default=40,help='toy optimizer updates, 1 to 200')
    ap.add_argument('--overwrite',action='store_true')
    args=ap.parse_args(argv)
    if not 1 <= args.steps <= 200:
        ap.error('--steps must be between 1 and 200')
    # Fail fast before expensive synthetic training if destination is invalid.
    outfile=Path(args.output)
    if outfile.suffix.lower()!='.html':
        ap.error('--output must end in .html')
    if not outfile.parent.is_dir():
        ap.error('--output parent directory must already exist')
    if not args.overwrite and (outfile.exists() or outfile.with_suffix('.json').exists()):
        ap.error('output already exists; use --overwrite explicitly')
    result=run_lab(train_steps=args.steps)
    htmlfile,jsonfile=write_reports(result,args.output,overwrite=args.overwrite)
    print('TRAME Research Lab: artificial experiments only')
    print('HTML:',htmlfile)
    print('JSON:',jsonfile)


if __name__=='__main__':
    main()
