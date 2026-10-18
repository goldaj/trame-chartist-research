from pathlib import Path
import datetime, hashlib, json, re, shutil, zipfile
import pdfplumber
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'dossier/recherche_lcm'; O=ROOT/'output'; W=ROOT/'tmp/pdfs/v23'
P=ROOT/'research/trame_research_plan/20261015'; R=ROOT/'research/trame_protocol_p1d'
M=json.loads((W/'manifest.json').read_text(encoding='utf-8'))
assert len(M)==13 and 1+sum(e['pages'] for e in M)==95
old=O/'versions/TRAME_dossier_v2_2_scientifique_20261015.zip'
assert hashlib.sha256(old.read_bytes()).hexdigest()=='6a0bfd6110bd91fc421daf376dcd1b783dc51117a182d30a9ebf6f35b93322c6'
dest=O/'versions/TRAME_dossier_v2_3_scientifique_20261015.zip'
assert not dest.exists(),'Never overwrite a published historical edition'
with zipfile.ZipFile(old) as z:
    prior_names=z.namelist()
    for e in M[:11]:
        for key in ['source','pdf']:
            p=Path(e[key]); assert p.read_bytes()==z.read(p.relative_to(ROOT).as_posix())
    assert (R/'versions/candidate_0_3/protocol_candidate.json').read_bytes()==z.read('research/trame_protocol_p1d/protocol_candidate.json')
    assert (R/'versions/candidate_0_3/README.md').read_bytes()==z.read('research/trame_protocol_p1d/README.md')
    # Audits, real data, older candidates and working notes are untouched.
    conserved=0
    for name in prior_names:
        if name.startswith(('research/trame_poc0/','research/trame_corpus/','research/trame_protocol_p1d/audits/','research/trame_protocol_p1d/versions/')) or name.startswith('dossier/recherche_lcm/notes_'):
            assert (ROOT/name).read_bytes()==z.read(name),name
            conserved+=1

checks=json.loads((P/'design_checks.json').read_text(encoding='utf-8'))
for name,digest in checks['inputs_sha256'].items(): assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
assert hashlib.sha256((P/'verify_design.py').read_bytes()).hexdigest()==checks['script_sha256']
shutil.copyfile(R/'protocol_candidate.json',P/'p1d_candidate_snapshot.json')

guide='''# TRAME : dossier scientifique actif

**Édition 2.3 du 15 octobre 2026 : treize documents, 95 pages.** Le plan demandé par le porteur est maintenant explicite et ses deux premières étapes sont engagées. Lire 11 pour le plan et les personas ; lire 12 pour les nouveaux témoins, le budget proposé et le générateur causal théorique P1-B0. Le candidat P1-D courant est 0.4, non gelé et non entraîné.

La synthèse 00 reste une introduction de trois pages. Les documents 00-10 sont conservés exactement ; 12 amende les choix expérimentaux antérieurs lorsqu'ils diffèrent. La publication ne constitue pas une autorisation implicite d'entraînement, de dépense ou de collecte payante.

| Document | Pages | PDF | Source modifiable |
|---|---:|---|---|
'''
for e in M:
    guide+=f"| {e['number']} {e['name']} | {e['pages']} | [Lire](../../output/pdf/{Path(e['pdf']).name}) | [Markdown]({Path(e['source']).name}) |\n"
guide+='''
[Dossier complet](../../output/pdf/TRAME_Dossier_complet.pdf) - [Archive complète actuelle](../../output/TRAME_dossier_et_sources.zip) - [Édition 2.3 figée](../../output/versions/TRAME_dossier_v2_3_scientifique_20261015.zip).

## Plan et premières opérations exécutées

Six étapes : fermer les contrastes de représentation ; définir la génération causale ; étendre le corpus réel ; geler l'évaluation indépendante ; réaliser le futur POC ; étudier l'échelle et la fiabilité. Les deux premières sont engagées, pas achevées. Sept personas simulés ont organisé deux cycles d'objections. Les agents auxiliaires restent en erreur de limite de service ; aucun avis indépendant supplémentaire n'est revendiqué.

Le candidat 0.4 définit deux contrôles numériques, leurs paramètres, une initialisation et une proposition de réglage/optimisation. La première campagne envisagée comprend huit variantes et 88 exécutions à petite taille ; elle n'a pas été lancée. Les tailles plus grandes et budgets longs constituent des extensions, sans garantie de convergence.

P1-B0 définit un futur de vingt codes conditionnés par le passé et les seuls codes précédents. Une base normale arrondie sur tous les entiers, corrigée dans un dictionnaire, permet de définir une loi normalisée sans écrêter les valeurs hors dictionnaire. Une condition suffisante de moments finis en prix est dérivée. La tête complète, ses bornes, sa stabilité et ses performances restent à préciser.

Les seuls nouveaux calculs exécutés sont arithmétiques : paramètres, budgets, exemples rationnels de récurrence, invariant de préfixe, normalisation sur un exemple fini et initialisation des biais. Aucune cotation lue, aucun modèle construit, aucune performance prédictive. Les calculs rationnels ne testent pas la stabilité d'une future tête gaussienne ni un réseau entraîné.

## Sources de travail et preuves

[Plan structuré](../../research/trame_research_plan/20261015/plan.json) - [P1-D 0.4](../../research/trame_protocol_p1d/protocol_candidate.json) - [P1-B0 0.1](../../research/trame_research_plan/20261015/p1b0_candidate.json) - [Vérifications arithmétiques](../../research/trame_research_plan/20261015/design_checks.json) - [Lectures ciblées](../../research/trame_research_plan/20261015/source_audit.json).

Les données et résultats réels antérieurs restent conservés : [audit descriptif BCE](../../research/trame_protocol_p1d/audits/preflight_01/report.json), [diagnostic exploratoire CHF](../../research/trame_protocol_p1d/audits/preflight_01/followup_scale_report.json). Leurs 8 166 912 présentations correspondent à 33 672 prix distincts. Le défaut de branche sans exemples a motivé 0.3 ; 0.4 ajoute des contrôles et un budget sans nouveau résultat sur les marchés.

Les cinq notes détaillées du 15 octobre restent dans l'archive : [candidat historique 0.3](notes_p1d_candidat_20261015.md), [ancres et DPCM](notes_ancres_causalite_dpcm_20261015.md), [alphabet et paramètres](notes_alphabet_information_egale_20261015.md), [témoins exacts](notes_temoins_p1d_20261015.md), [audit et hybride](notes_audit_reel_et_langage_hybride_20261015.md).

## Prochaine tâche concrète

Qualifier les bornes et le calcul de P1-B0, puis établir l'inventaire des tests indépendants multi-marchés. Faire challenger les choix de réglage avant gel. La conception avance ; le prix brut demeure la cible, sans frais ni infrastructure applicative.

[Édition 2.2, 84 pages](../../output/versions/TRAME_dossier_v2_2_scientifique_20261015.zip) - [2.1, 72 pages](../../output/versions/TRAME_dossier_v2_1_scientifique_20261015.zip) - [2, 63 pages](../../output/versions/TRAME_dossier_v2_scientifique_20261014.zip) - [1](../../output/versions/TRAME_dossier_v1_documentaire_20261014.zip).

[Journal](JOURNAL_DES_VERSIONS.md) - [Bibliographie](BIBLIOGRAPHIE_LIENS.md) - [Continuité](CONTINUITE.md).
'''
(D/'LIRE_EN_PREMIER.md').write_text(guide,encoding='utf-8')

links={}
for e in M:
    for title,url in re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',Path(e['source']).read_text(encoding='utf-8')):
        if url not in links: links[url]=[title,set()]
        links[url][1].add(e['number'])
bib=(D/'BIBLIOGRAPHIE_LIENS.md').read_text(encoding='utf-8')
prefix=re.split(r'^1\. ',bib,flags=re.M)[0].replace('version scientifique 2.2','version scientifique 2.3').replace('des onze documents','des treize documents')
prefix+='Nouvelle session du plan : relecture ciblée des embeddings numériques, consultation de l’article AdamW et lecture de PixelCNN++ section 2.1 (CDF, arrondi, bornes des pixels). Leurs résultats ne sont pas reproduits et ne valident pas les choix financiers proposés. Trace : research/trame_research_plan/20261015/source_audit.json.\n\n'
for i,(url,(title,docs)) in enumerate(links.items(),1): prefix+=f"{i}. [{title}]({url}) - documents {', '.join(sorted(docs))}.\n"
(D/'BIBLIOGRAPHIE_LIENS.md').write_text(prefix,encoding='utf-8')

cont=(D/'CONTINUITE.md').read_text(encoding='utf-8')
cont=cont.replace('édition scientifique publiée 2.2 ; candidat expérimental courant 0.3.','édition scientifique publiée 2.3 ; candidat P1-D courant 0.4 et candidat théorique P1-B0 0.1.')
cont=cont.replace('Onze documents actifs 00-10, synthèse générale de 3 pages actualisée et chapitre 10 de 12 pages. Dossier PDF de 84 pages.','Treize documents actifs 00-12, synthèse générale de 3 pages, chapitre 10 de 12 pages, plan 11 de 4 pages et note technique 12 de 7 pages. Dossier PDF de 95 pages.')
cont+='''
## Plan demandé par le porteur et début d'exécution, édition 2.3

L'utilisateur demande explicitement un plan expert, des personas adaptés puis le début de son exécution. Six étapes figurent dans 11 : fermer P1-A, définir P1-B, qualifier le corpus réel multi-marchés, geler l'évaluation indépendante, futur développement/POC, passage à l'échelle. Le périmètre initial de conception sans modèle reste respecté. Les deux premières étapes sont engagées ; aucun entraînement ou achat lancé.

Sept personas simulés organisent les cycles 10 et 11. list_agents confirme toujours les erreurs de limite de service des trois auxiliaires ; aucune relecture indépendante. La critique conduit à deux contrôles numériques plus expressifs et à une loi générative sans tête exclusive réservée aux extrêmes.

P1-D 0.4 ajoute C/Q-MLP (r16, 18d+32 paramètres de valeur) et C/Q périodique (8 périodes 0.5..64, 18d), N(v) conservé et corrections de sortie initialisées à zéro. W1 normal variance1, b1 nul. Premier total petit : 799797 MLP, 799765 périodique. Les quatre variantes 0.3 restent proposées, soit huit variantes. Initialisations, AdamW, learning rates, schedule et gestion des échecs sont documentaires ; jamais validés sur un réseau. Attention : tête initiale à poids nuls, donc gradient amont retardé ; W2 MLP ne reçoit pas automatiquement un gradient au tout premier pas global.

Budget initial proposé : petit gabarit seulement, 30 époques, 80 batches/époque (32 dates et six actifs, dernier lot13 dates), 2400 updates. Trois LR x deux seeds de réglage puis cinq seeds fraîches de répétition par variante : 88 exécutions, 211200 updates, 40249440 exemples actif-origine et 10303856640 vecteurs contextuels. Coût réel non mesuré, pas de lancement ni preuve de convergence. Trois tailles et deux budgets 30/90 époques représenteraient528 exécutions ; pas un engagement de ressources.

P1-B0 0.1 séparé : contexte causal à l'origine, delta=s_i/8 fixe, ancre log(P_i), futur20 codes arrondis au plus proche depuis l'état reconstruit, demi-entiers vers +inf. Teacher forcing ne voit que les codes cibles antérieurs ; génération utilise ses propres codes. Borne de reconstruction delta/2, aucune borne de prévision. Distribution q(k) normale arrondie sur Z, corrections exp(a_k) dans [-2048,2047], ailleurs1 ; normalisateur = queues exactes + somme centrale. Paramètres de base utilisés sur toutes les cibles. Tête et contraintes restent à spécifier.

Nouveau point mathématique : une queue de masse proportionnelle à exp(-k/b) donne une espérance de prix infinie si delta*b>=1. Une normale arrondie a ses moments exponentiels à état fixé ; une trajectoire nécessite un contrôle supplémentaire. Si |mu|<=M, sigma<=S et |a_k|<=A uniformes sur tous les états, avec delta fixe, E[P_hat_h|H_i]<=P_i*C^h, C=exp(2A+delta/2+delta*M+delta²S²/2). Bornes sur paramètres, pas sur support du prix. Valeurs M,S,A et plancher sigma non choisis ; aucune stabilité flottante démontrée par le seul raisonnement.

research/trame_research_plan/20261015 contient plan, p1b0_candidate, source_audit, verify_design et design_checks. Vérifications réussies : comptes, budgets, 394 transitions rationnelles principales plus contrôle de préfixe, normalisateur sur exemple fini rationnel, inverse softplus des biais. Aucun prix lu ni tête probabiliste implémentée. Le rapport ne teste pas les CDF gaussiennes ou un réseau. Il refuse l'écrasement. Snapshot 0.4 copié pour conserver le contexte ; hashes des entrées consignés. Candidat 0.3 et README archivés dans versions/candidate_0_3, identiques à l'archive2.2.

Prochain travail utile : qualifier la tête P1-B0 et ses bornes, stabilité et coût, puis inventaire de tests indépendants multi-marchés ; examiner la pertinence des choix d'optimisation avant gel. Ne pas annoncer que le plan est entièrement clos ou que P1-B0 est implémenté. Les définitions purement symboliques et multiscalaires restent des pistes distinctes, sans supériorité démontrée.

Publication2.3 : 95 pages, 13 signets ; 00-10 préservés exactement, 11-12 ajoutés. Toutes les nouvelles pages ont été rendues et inspectées, corrections de mise en forme mathématique appliquées. Archive actuelle output/TRAME_dossier_et_sources.zip, copie historique output/versions/TRAME_dossier_v2_3_scientifique_20261015.zip. QA dans tmp/pdfs/v23 ; ne pas relancer les scripts historiques de mutation/publication qui écraseraient l'état ou les archives.
'''
(D/'CONTINUITE.md').write_text(cont,encoding='utf-8')
journal=(D/'JOURNAL_DES_VERSIONS.md').read_text(encoding='utf-8')
journal+='''
## Édition 2.3 - plan demandé et début d'exécution, 15 octobre 2026

Création du plan11 (quatre pages), six étapes et sept personas simulés. Cycles critiques10-11 : témoins numériques plus expressifs et difficulté probabiliste des queues de prix. Agents auxiliaires toujours indisponibles sur limite de service ; pas de validation indépendante.

P1-D amendé en0.4 : contrôles MLP/périodiques, initialisations et proposition de budget/réglage. Ancien0.3 archivé sans altération. Nouveau candidat théorique séparé P1-B0 : récurrence causale de vingt codes, loi normale arrondie corrigée, normalisation exacte sur papier, condition suffisante de moments finis. Aucun modèle construit ou entraîné et aucun gain de prévision.

Exécution d'un audit arithmétique sans cotations : comptes, budgets, récurrence rationnelle et préfixe, identité de normalisation finie, biais quantiles. Il ne teste ni réseau ni CDF en queue. Les documents distinguent clairement calculs effectués, preuves conditionnelles et choix proposés. Relecture de mise en page et correction d'une formulation ambiguë du démarrage des gradients avec tête nulle.

Dossier de95 pages, treize documents ; anciens00-10 intacts. Index, bibliographie, continuité et README actualisés. Sources, snapshots, résultats réels et éditions précédentes conservés. Prochaine tâche : tête P1-B0, bornes numériques et test indépendant multi-marchés.
'''
(D/'JOURNAL_DES_VERSIONS.md').write_text(journal,encoding='utf-8')
readme=(R/'README.md').read_text(encoding='utf-8').replace('Les documents 11-12 portent la révision 0.4.','Les documents 11-12 de l’édition 2.3 (95 pages) portent la révision 0.4.')
(R/'README.md').write_text(readme,encoding='utf-8')

issues=[]
with pdfplumber.open(O/'pdf/TRAME_Dossier_complet.pdf') as pdf:
    assert len(pdf.pages)==95
    for i,p in enumerate(pdf.pages,1):
        content=p.extract_text() or ''
        if not content.strip() or '\ufffd' in content: issues.append({'page':i,'text':True})
        bad=[v['text'] for v in p.extract_words() if v['x0']<20 or v['x1']>p.width-20 or v['top']<7 or v['bottom']>p.height-7]
        if bad: issues.append({'page':i,'bounds':bad})
assert not issues,issues
assert len(PdfReader(O/'pdf/TRAME_Dossier_complet.pdf').outline)==13
for e in M: assert hashlib.sha256(Path(e['pdf']).read_bytes()).hexdigest()==e['sha256']
R0=ROOT/'research/trame_poc0'
freeze=json.loads((R0/'freeze.json').read_text())
for name,key in [('protocol.json','protocol_sha256'),('run_research.py','analysis_sha256')]: assert hashlib.sha256((R0/name).read_bytes()).hexdigest()==freeze[key]
assert not list((R0/'raw').rglob('*2021-11*')) and not list((R0/'raw').rglob('*2021-12*'))
broken=[]
for s in [D/'LIRE_EN_PREMIER.md']+[Path(e['source']) for e in M[-2:]]:
    for target in re.findall(r'\]\(([^)]+)\)',s.read_text(encoding='utf-8')):
        if target.startswith(('https:','http:','#')): continue
        p=(s.parent/target).resolve()
        if not p.exists() and p!=dest: broken.append(str(p))
assert not broken,broken
qa={'version':'2.3','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':95,'documents':13,'bookmarks':13,
 'new_pages_visually_inspected':12,'visual_detail':'cover+4 plan+7 technical; corrected technical pages1,2,7 inspected after edits',
 'old_00_10_source_and_pdf_unchanged':True,'historical_candidate03_preserved':True,'unchanged_prior_scientific_files_compared':conserved,
 'design_audit_inputs_hash_verified':True,'old_archive22_sha256_verified':True,'poc0_freeze_verified':True,'protected_months_absent':True,
 'layout_issues':issues,'broken_local_links':broken,'external_link_targets':len(links),'models_instantiated':False,'trained':False,'independent_review':False}
(W/'final_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
files={ROOT/name for name in prior_names}
files.update(Path(e['source']) for e in M);files.update(Path(e['pdf']) for e in M)
for folder in [P,R/'versions/candidate_0_3']:
    files.update(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.update([W/'manifest.json',W/'final_qa.json',ROOT/'tmp/pdfs/build_trame_v23.py',Path(__file__).resolve(),ROOT/'tmp/advance_trame_plan_20261015.py'])
assert all(p.exists() for p in files)
temp=W/'TRAME_dossier_et_sources.zip'
with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files): z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(temp) as z: assert z.testzip() is None
current=O/'TRAME_dossier_et_sources.zip'
shutil.copyfile(temp,current);shutil.copyfile(temp,dest)
receipt={'version':'2.3','files':len(files),'bytes':current.stat().st_size,'sha256':hashlib.sha256(current.read_bytes()).hexdigest()}
(W/'archive_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps({'qa':qa,'archive':receipt},ensure_ascii=False,indent=2))
