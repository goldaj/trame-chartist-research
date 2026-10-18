from pathlib import Path
import datetime, hashlib, json, re, shutil, zipfile
import pdfplumber
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2];D=ROOT/'dossier/recherche_lcm';O=ROOT/'output'
W=ROOT/'tmp/pdfs/v24';P=ROOT/'research/trame_research_plan/20261016'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def jwrite(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=O/'versions/TRAME_dossier_v2_3_scientifique_20261015.zip'
assert sha(old)=='2afe7615f4ec8a27ffff70b71a6bbaa58db26f182da9a51b5cf481739a145fea'
dest=O/'versions/TRAME_dossier_v2_4_scientifique_20261016.zip'
assert not dest.exists(),'Never overwrite historical edition'
M=json.loads((W/'manifest.json').read_text(encoding='utf-8'))
assert len(M)==14 and sum(e['pages'] for e in M)+1==102
with zipfile.ZipFile(old) as z:
    prior_names=z.namelist();conserved=0
    for e in M[:-1]:
        for key in ['source','pdf']:
            p=Path(e[key]);assert p.read_bytes()==z.read(p.relative_to(ROOT).as_posix()),str(p)
    for name in prior_names:
        if name.startswith('research/') or name.startswith('dossier/recherche_lcm/notes_'):
            assert (ROOT/name).read_bytes()==z.read(name),name;conserved+=1

seal=json.loads((P/'freeze.json').read_text(encoding='utf-8'))
for name,digest in seal['files_sha256'].items():assert sha(P/name)==digest,name
report=json.loads((P/'target_audit_report.json').read_text(encoding='utf-8'))
design=json.loads((P/'design_report.json').read_text(encoding='utf-8'))
assert design['script_sha256']==sha(P/'check_design.py')
assert design['candidate_sha256']==sha(P/'p1b0_candidate.json')
assert not report['violations'] and report['total']['label_presentations']==304920
assert report['unique_target_prices']==15360 and report['total']['distinct_codes']==156
assert report['freeze']==seal

jwrite(P/'source_audit.json',{'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'reproduced_publication_results':False,'sources':[
 {'title':'SciPy log_ndtr','url':'https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.log_ndtr.html',
  'read':'definition, notes, examples; page displayed SciPy1.18.0','use':'log CDF numerical cancellation; no financial validation',
  'library_executed':False},
 {'title':'SciPy logsumexp','url':'https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html',
  'read':'API definition, notes, examples','use':'stable reduction for proposed normalizer; no implementation tested',
  'library_executed':False},
 {'title':'PixelCNN++','url':'https://arxiv.org/abs/1701.05517','read':'abstract rechecked; section2.1 previously read for edition2.3',
  'use':'prior CDF-difference likelihood; bounded logistic pixel setting differs from unbounded Gaussian price codes'}],
 'own_derivations':['DPCM integer lattice equivalence','head counts','normalizer output-gradient identity','uniform tail upper bound',
                    'differenced quantization error mechanism under explicitly additional iid-uniform approximation'],
 'runtime_limitations':'SciPy and mpmath absent; four standard-library illustrations only, no high-precision reference or derivatives'})
jwrite(P/'progress.json',{'date':'2026-10-16','parent_plan':'../20261015/plan.json','active_candidate':'p1b0_candidate.json',
 'P1D_candidate':'../../trame_protocol_p1d/protocol_candidate.json','stages':{'1':'started','2':'started, specified and target codec audited; qualification incomplete',
 '3':'planned, prior source inventories exist','4':'planned','5':'not started','6':'planned'},
 'new_persona_cycle':12,'personas_simulated':True,'independent_review':False,
 'agent_status':'previously known service limits; no new independent-agent review claimed',
 'next':['Specify common native-price scores and Monte Carlo error control','Challenge bounds and conditional distribution on a declared multi-market matrix',
         'Qualify differentiable numerical primitives and gradients in future technical phase','Set P1B optimization and compute-balanced controls'],
 'no_models_or_training':True,'no_new_market_download':True,'future_test_not_opened':True})
(P/'README.md').write_text('''# P1-B0 0.2 : qualification documentaire

Voir le chapitre 13, édition 2.4. `freeze.json` scelle le candidat, le protocole et le script avant le nouvel audit de cibles. Il ne constitue pas une préinscription externe. Les choix restent discutables ; les données d'ajustement avaient déjà été explorées.

`target_audit_report.json` : 304 920 présentations, 15 360 cotations cibles distinctes, partition 1999-2009 exclusivement. Aucun modèle ou score prédictif. Les scripts refusent d'écraser leurs rapports.

`design_report.json` : identités rationnelles, inventaire de paramètres et quatre illustrations math.erfc. Aucune tête complète, normalisation différentiable ou simulation de trajectoires implémentée. SciPy/mpmath absents du runtime ; leur documentation n'est pas un test exécuté.

Le champ hérité `arithmetic_recurrence_check` du candidat 0.2 désigne le contrôle historique `../20261015/design_checks.json`. Les contrôles nouveaux sont dans `design_report.json`. Le candidat 0.1 et le plan original restent inchangés dans 20261015. Le nouveau statut est dans `progress.json`.

Le candidat utilise S=64 par défaut. La sensibilité déclarée S=256 doit changer le biais initial en log((8-.25)/(256-8)) pour garder sigma initial égal à huit. Ce complément explicite figure au chapitre 13 ; aucune exécution de modèle n'a suivi. Les très faibles bornes de masse hors dictionnaire limitent la portée générale de la tête.

Ne pas relancer les scripts de préparation ou d'audit sur les rapports existants. Toute modification doit être versionnée et sa position chronologique par rapport aux lectures de données indiquée.
''',encoding='utf-8')

guide='''# TRAME : dossier scientifique actif

**Édition 2.4 du 16 octobre 2026 : quatorze documents, 102 pages.** Le chapitre 13 précise une sortie générative GPT et présente le nouvel audit réel. Le plan général reste dans 11. P1-D est en révision 0.4 ; P1-B0 est en révision théorique 0.2, qualifiée partiellement et non entraînée.

La synthèse 00 reste une introduction de trois pages. Lire ensuite la section 1 du chapitre 13 pour l'avancée actuelle. Les documents 00-12 sont préservés exactement ; 13 amende les propositions génératives de 12 quand elles diffèrent. Aucun modèle, entraînement, achat ou résultat prédictif n'est annoncé.

| Document | Pages | PDF | Source modifiable |
|---|---:|---|---|
'''
for e in M:guide+=f"| {e['number']} {e['name']} | {e['pages']} | [Lire](../../output/pdf/{Path(e['pdf']).name}) | [Markdown]({Path(e['source']).name}) |\n"
guide+='''
[Dossier complet](../../output/pdf/TRAME_Dossier_complet.pdf) - [Archive complète actuelle](../../output/TRAME_dossier_et_sources.zip) - [Édition 2.4 figée](../../output/versions/TRAME_dossier_v2_4_scientifique_20261016.zip).

## Résultats de cette étape

Le codec en écarts depuis le prix reconstruit équivaut exactement à un état entier sur une grille logarithmique fixe. Le candidat décrit 276 positions GPT et trois sorties BASE/FLAT/HIER. HIER réduit les poids de sortie mais conserve les 4 096 contributions centrales du normalisateur à chaque pas.

L'audit porte sur la seule partition BCE 1999-2009 : 304 920 présentations recouvrantes, 15 360 cotations cibles distinctes. Zéro divergence entre les deux formulations ; borne de reconstruction satisfaite dans les calculs contrôlés. L'union contient 156 codes de -82 à 101, sans sortie du dictionnaire. Aucun résultat prédictif n'en découle.

Les bornes de paramètres proposées rendent mathématiquement presque nulle la masse hors dictionnaire. Elles restent des hypothèses de comparaison, pas une solution validée pour les crises. La normalisation stable, les gradients, la simulation et les scores en prix natifs demandent encore qualification. Un douzième cycle de personas simulés a produit ces objections ; aucune nouvelle validation indépendante.

## Sources et reproduction

[Statut actuel du plan](../../research/trame_research_plan/20261016/progress.json) - [Plan original](../../research/trame_research_plan/20261015/plan.json) - [P1-D 0.4](../../research/trame_protocol_p1d/protocol_candidate.json) - [P1-B0 0.2](../../research/trame_research_plan/20261016/p1b0_candidate.json).

[Déclaration d'audit](../../research/trame_research_plan/20261016/audit_protocol.json) - [Gel local](../../research/trame_research_plan/20261016/freeze.json) - [Résultats réels](../../research/trame_research_plan/20261016/target_audit_report.json) - [Contrôles arithmétiques](../../research/trame_research_plan/20261016/design_report.json) - [Lectures et limites](../../research/trame_research_plan/20261016/source_audit.json) - [Conventions de reproduction](../../research/trame_research_plan/20261016/README.md).

Les fichiers et données de 2.3 sont conservés. L'ancienne version P1-B0 0.1 reste dans le dossier daté 20261015 ; les contrôles 0.2 sont dans 20261016. Les labels futurs analysés étaient des valeurs historiques connues de la partition d'ajustement, pas des prédictions ni de nouveaux tests indépendants.

## Prochaine tâche concrète

Définir les scores communs en prix bruts et le contrôle d'erreur de simulation ; challenger les distributions et bornes sur une matrice de corpus et régimes déclarée. Puis qualifier les primitives numériques et gradients lors de la phase technique appropriée. Le réglage de P1-B0 et le test indépendant multi-marchés restent ouverts.

[Édition 2.3, 95 pages](../../output/versions/TRAME_dossier_v2_3_scientifique_20261015.zip) - [2.2, 84 pages](../../output/versions/TRAME_dossier_v2_2_scientifique_20261015.zip) - [2.1, 72 pages](../../output/versions/TRAME_dossier_v2_1_scientifique_20261015.zip) - [2, 63 pages](../../output/versions/TRAME_dossier_v2_scientifique_20261014.zip) - [1](../../output/versions/TRAME_dossier_v1_documentaire_20261014.zip).

[Journal](JOURNAL_DES_VERSIONS.md) - [Bibliographie](BIBLIOGRAPHIE_LIENS.md) - [Continuité](CONTINUITE.md).
'''
(D/'LIRE_EN_PREMIER.md').write_text(guide,encoding='utf-8')
with (D/'BIBLIOGRAPHIE_LIENS.md').open('a',encoding='utf-8') as f:
    f.write('\n109. [SciPy log_ndtr](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.log_ndtr.html) - document 13, documentation lue ; bibliothèque non exécutée.\n110. [SciPy logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html) - document 13, documentation lue ; bibliothèque non exécutée.\n\nPixelCNN++ (108) est aussi utilisé dans 13 ; abstract relu, section 2.1 lue à l’édition précédente.\n')
cont=(D/'CONTINUITE.md').read_text(encoding='utf-8')
cont=cont.replace('État au 15 octobre 2026, édition scientifique publiée 2.3 ; candidat P1-D courant 0.4 et candidat théorique P1-B0 0.1.',
                  'État au 16 octobre 2026, édition scientifique publiée 2.4 ; candidat P1-D courant 0.4 et candidat théorique P1-B0 0.2 (dossier 20261016).')
cont=cont.replace('Treize documents actifs 00-12, synthèse générale de 3 pages, chapitre 10 de 12 pages, plan 11 de 4 pages et note technique 12 de 7 pages. Dossier PDF de 95 pages.',
                  'Quatorze documents actifs 00-13, synthèse générale de 3 pages, chapitre 10 de 12 pages, plan 11 de 4 pages et notes 12/13 de 7 pages chacune. Dossier PDF de 102 pages.')
cont+='''
## Édition 2.4 : sortie générative et audit des cibles, 16 octobre 2026

Nouveau chapitre13 de7 pages ; 00-12 inchangés exactement. P1-D0.4 inchangé. P1-B0 courant0.2 dans research/trame_research_plan/20261016 ; ancien0.1 et plan20261015 conservés sans modification. Aucun modèle/tête prédictive construit ni entraîné. Les scripts nouveaux sont des audits de codecs et des calculs de conception.

Équivalence en arithmétique réelle : avec delta fixe et n0=0, n_h=floor((log(P_(i+h))-log(P_i))/delta+.5), k_h=n_h-n_(h-1), uhat_h=log(P_i)+delta*n_h. C'est le DPCM0.1 sous forme d'état entier. Pas d'information nouvelle ; seulement un choix de représentation. Identité de bruit quantifié delta*k_h=increment_u+e_h-e_(h-1). Hypothèse iid uniforme supplémentaire produit covariance négative -delta²/12 ; aucun résultat empirique d'autocorrélation ni découverte de marché.

Architecture théorique : même entrée Q affine, 256 contextes+BOS+19 états futurs n_h/8, 276 positions, vingt sorties ; teacher forcing décalé, aucun vrai futur dans son propre input, aucune perte sur l'ancien contexte recentré. Trois types HISTORY/BOS/FUTURE, six actifs, quatre métadonnées (ancre, échelle, délai, indicateur). Délais futurs inconnus sentinelle0, indicateur futur dérivé de n. Commun12Ld²+13Ld+18d, têtes BASE2(d+1), FLAT4098(d+1), HIER520(d+1). Totaux petit795650/1324034/862472. HIER partage coarse512+trois pairesbits ; classe restreinte avec redondances. Normalisateur reste4096 cellules par pas,81920/origine ; moins de poids ne prouve pas réduction proportionnelle du calcul.

Bornes proposées avant audit : M256,S64,sigma_min.25,A4, sensibilitéS256. mu=M*tanh(g_mu/M), sigma=sigma_min+(S-sigma_min)*sigmoid, a=A*tanh(g/A). Matrices sortie0, mu0,sigma8,corrections0. Biais sigma log((8-.25)/(S-8)), donc changer ce biais dans sensibilité. Preuve conditionnelle de moments conservée, borne peut être très lâche. Outside weight1 et Z>=e^-A donnent p(horsI)<=e^A q(horsI), borne uniforme9.0844e-171 pourS64 et1.3977e-10 pourS256. Ces lois ne sont pas des solutions générales aux extrêmes ; support infini mais masse imposée très faible. Gradient de sortie pourcorrection j=p(j)-indicatrice(j=cible), même si j jamais réalisé ; distinction essentielle avec table d'entrée non visitée. Aucune fiabilité rare garantie.

Gel local02:59:37UTC avant audit réel : candidat SHA eba95c653977ba1ec39d3dba83cd1d6a93e55deacab13650c532285a1171456b ; protocole8eff4596427bbcd10d9e7abfe7ef83535f009d248a9dfae97992089eeb90fa7d ; script1a085a1e38c552c6f970c9dabdcad4fde18ee2e4509d0411864083ab88aa43bb. Gel d'intégrité, pas préinscription externe ; corpus déjà exploré. Le champ hérité arithmetic_recurrence_check du candidat désigne ../20261015/design_checks.json ; contrôles nouveaux design_report.json.

Audit sur valeurs1999-2009 seulement, filtre avant conversionfloat ; sourceECB entière vérifiée parhash inchangé.16896valeurs parsées,16950lignes horspartition ignorées pourprix.2541origines/devise du1999-12-27au2009-12-02,20cibles,304920présentations de15360cotations cibles distinctes. Union156codes,min-82,max101,zéroextérieur,zéros18155(5.954%),quantilesabs50/90/99/99.9=5/14/25/45. Aucun planchers, aucune divergence entre formulation entière et récurrenceflottante, aucune violation de borne avectolérance d'ingénierie déclarée. Maxerreur0.4999927317delta. Maximumabsolu101AUDcible2007-08-16,origine2007-07-24,h17,s.003259579227. Pas un rendement cumulé17jours. Ncummax247. Les tableaux reflètent des cibles recouvrantes, pas de nouvelles observations indépendantes. Aucun développement/pseudo-test lu pour ses prix dans cette opération ; ne pas requalifier ces partitions globalement comme inédites.

Design_report :3609transitions rationnelles, inventaireindépendantmodules,4illustrationsmath.erfc. [10,11]normal donneCDFnaïve0contre7.61966e-24viaerfc. NiSciPy nimpMath installés ; pasdecomparaisonhauteprécision,nidérivées,ninormalisateur complet nisampling. DocsSciPylog_ndtr/logsumexplues ; PixelCNNabstractrelu,section2.1déjàlue. Aucun modèleprédictif,supportmachineinfini oucalibration déclarévalidé.

Cycle12 des7personassimulés a challengééquivalence,artefactsdequantification,masquecausal,queues,comptesréels,gel etcommunication. Pasderelectureindépendante ; auxiliairesconnusindisponibles,pasrelancés. Prochainbloc :contratcommundescoresenprixetprécisionMonteCarlo,matricedecorpus/régimespourchallengerbornes,qualificationnumérique/gradients lorsdephaseappropriée,budgetP1Bettestindépendant. H2 Marchélatent,croisementactifs,or,indicesetsecondesnonévalués.

Publication2.4 :102pages,14signets ; chapitre13etnouvellecouverturerendusinspectés. Unecorrectiondemiseenformea préservélesmultiplicationsdanslesformulesmu/sigma/C. QAetempreintesdans tmp/pdfs/v24 ; archivedans output/versions/TRAME_dossier_v2_4_scientifique_20261016.zip etcopieactuelle output/TRAME_dossier_et_sources.zip. Scriptsdepublicationhistoriquesànepasrelancer ; rapportsd'auditrefusentl'écrasement. LesmoiscryptoNov/Dec2021restentprotégés etabsents.
'''
(D/'CONTINUITE.md').write_text(cont,encoding='utf-8')
with (D/'JOURNAL_DES_VERSIONS.md').open('a',encoding='utf-8') as f:
    f.write('''
## Édition 2.4 - 16 octobre 2026

Ajout du chapitre13 : tête GPT générative à trois variantes et audit descriptif des codes cibles. P1-B0 passe à0.2, défini avant l'audit ; P1-D0.4 inchangé. Identité entre récurrence DPCM et grille de niveaux, positions causales, comptes de paramètres/coûts, dérivée des sorties non observées, bornes explicites de queues. Le support infini peut conserver une masse extrême presque nulle : limitation du candidat, sans prétendre à une solution générale.

Audit déclaré puis exécuté sur la seule partition BCE1999-2009 :304920présentations,15360cotations distinctes,156codes observés, aucune divergence des deux formulations ni violation de reconstruction avec la tolérance prévue. Aucun modèle, score ou apprentissage. Calculs rationnels et quatre illustrations erfc séparés des données réelles ; primitives différentiables non qualifiées. Cycle12 du panel simulé, aucune validation indépendante.

Dossier102pages et14documents. PDF00-12 et leurs sources intacts, ancien candidat et tous rapports préservés. Nouveau chapitre de7pages et couverture inspectés visuellement ; correction de la notation des multiplications. Index,bibliographie,continuitéetstatutduplan actualisés. Archive2.3 conservée ; nouvellearchivefigée2.4.
''')

issues=[];external=set()
with pdfplumber.open(O/'pdf/TRAME_Dossier_complet.pdf') as pdf:
    assert len(pdf.pages)==102
    for i,p in enumerate(pdf.pages,1):
        t=p.extract_text() or ''
        if not t.strip() or '\ufffd' in t:issues.append({'page':i,'text':True})
        bad=[v['text'] for v in p.extract_words() if v['x0']<20 or v['x1']>p.width-20 or v['top']<7 or v['bottom']>p.height-7]
        if bad:issues.append({'page':i,'bounds':bad})
        for a in p.hyperlinks:
            if a.get('uri'):external.add(a['uri'])
assert not issues,issues
assert len(PdfReader(O/'pdf/TRAME_Dossier_complet.pdf').outline)==14
for e in M:assert sha(Path(e['pdf']))==e['sha256']
R0=ROOT/'research/trame_poc0';freeze=json.loads((R0/'freeze.json').read_text())
for name,key in [('protocol.json','protocol_sha256'),('run_research.py','analysis_sha256')]:assert sha(R0/name)==freeze[key]
assert not list((R0/'raw').rglob('*2021-11*')) and not list((R0/'raw').rglob('*2021-12*'))
broken=[]
for s in [D/'LIRE_EN_PREMIER.md',Path(M[-1]['source'])]:
    for target in re.findall(r'\]\(([^)]+)\)',s.read_text(encoding='utf-8')):
        if target.startswith(('https:','http:','#')):continue
        p=(s.parent/target).resolve()
        if not p.exists() and p!=dest:broken.append(str(p))
assert not broken,broken
qa={'version':'2.4','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':102,'documents':14,'bookmarks':14,
    'new_pages_visually_inspected':8,'visual_detail':'cover+7 new chapter pages; changed page3 inspected after math formatting fix; other six final chapter rasters unchanged',
    'old_00_12_sources_and_pdfs_unchanged':True,'unchanged_prior_scientific_files_compared':conserved,
    'audit_seal_verified':True,'report_consistency_checked':True,'archive23_sha256_verified':True,'poc0_freeze_verified':True,
    'protected_months_absent':True,'layout_issues':issues,'broken_local_links':broken,'external_link_targets':len(external),
    'model_implemented':False,'trained':False,'independent_review':False}
jwrite(W/'final_qa.json',qa)
files={ROOT/name for name in prior_names}
files.update(Path(e['source']) for e in M);files.update(Path(e['pdf']) for e in M)
files.update(p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.update([W/'manifest.json',W/'final_qa.json',ROOT/'tmp/pdfs/build_trame_v24.py',Path(__file__).resolve()])
assert all(p.exists() for p in files)
temp=W/'TRAME_dossier_et_sources.zip'
with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(temp) as z:assert z.testzip() is None
shutil.copyfile(temp,O/'TRAME_dossier_et_sources.zip');shutil.copyfile(temp,dest)
receipt={'version':'2.4','files':len(files),'bytes':temp.stat().st_size,'sha256':sha(temp)}
jwrite(W/'archive_receipt.json',receipt)
print(json.dumps({'qa':qa,'archive':receipt},ensure_ascii=False,indent=2))
