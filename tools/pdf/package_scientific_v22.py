from pathlib import Path
import hashlib, json, re, zipfile, shutil, datetime
import pdfplumber
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'dossier/recherche_lcm'; O=ROOT/'output'; W=ROOT/'tmp/pdfs/v22'
M=json.loads((W/'manifest.json').read_text(encoding='utf-8'))
total=1+sum(e['pages'] for e in M)
assert total==84 and len(M)==11
historic=O/'versions/TRAME_dossier_v2_1_scientifique_20261015.zip'
assert hashlib.sha256(historic.read_bytes()).hexdigest()=='74b0e98d47966ae176c736a873f32cd90ad231b6d8d5aba50cef6d1ccc10444f'
dest=O/'versions/TRAME_dossier_v2_2_scientifique_20261015.zip'
assert not dest.exists(), 'Published version must never be overwritten'

with zipfile.ZipFile(historic) as z:
    old_names=z.namelist()
    for e in M:
        if e['number'] in ('00','10'): continue
        for key in ('source','pdf'):
            p=Path(e[key]); assert p.read_bytes()==z.read(p.relative_to(ROOT).as_posix()),p
    assert 'dossier/recherche_lcm/00_synthese_accessible.md' in old_names

# The existing candidate and descriptive audit are scientific inputs to this publication.
# Preserve their bytes; do not rerun measurements or amend model proposals in a packaging step.
working=O/'travail_en_cours/TRAME_P1D_candidat_0_3_20261015.zip'
assert hashlib.sha256(working.read_bytes()).hexdigest()=='4938ecdc0c41d6963909ca7bb96a7b5c396c986aa46e310ba3c5dfbe02936d1c'
with zipfile.ZipFile(working) as z:
    preserved=0
    for name in z.namelist():
        if name.startswith('research/trame_protocol_p1d/') or name.startswith('dossier/recherche_lcm/notes_'):
            assert (ROOT/name).read_bytes()==z.read(name),name
            preserved+=1

guide='''# TRAME : dossier scientifique actif

**Édition 2.2 du 15 octobre 2026 : onze documents, 84 pages assemblées.** La synthèse 00 est actualisée et tient en trois pages. Le nouveau chapitre 10 consolide les cinq notes du 15 octobre et le candidat P1-D 0.3. Les documents 01 à 09 conservent leur édition précédente ; 10 prévaut lorsque les propositions expérimentales divergent. Les anciennes versions restent disponibles.

Pour découvrir le projet, lire 00, puis 08 pour le Marché latent et le GPT. Pour les dernières avancées, lire 10. L'objet reste la prévision scientifique des prix bruts sur plusieurs familles d'actifs. Aucun modèle prédictif ou tokenizer appris n'a été construit ou entraîné.

| Document | Pages | PDF | Source modifiable |
|---|---:|---|---|
'''
for e in M:
    guide+=f"| {e['number']} {e['name']} | {e['pages']} | [Lire](../../output/pdf/{Path(e['pdf']).name}) | [Markdown]({Path(e['source']).name}) |\n"
guide+='''
[Dossier complet](../../output/pdf/TRAME_Dossier_complet.pdf) - [Archive complète actuelle](../../output/TRAME_dossier_et_sources.zip) - [Édition 2.2 conservée](../../output/versions/TRAME_dossier_v2_2_scientifique_20261015.zip).

## La contribution consolidée

Le chapitre 10 sépare information, écriture et apprentissage fini. Il précise la causalité du prétraitement, les ancres, les cellules communes et leurs encodeurs, puis rassemble les résultats réels et la correction proposée. La voie numérique réservée aux échappements du candidat 0.2 n'aurait reçu aucun exemple à l'ajustement ; la version 0.3 utilise une base numérique partout, puis des corrections symboliques. Cette comparaison est explicitement hybride. Aucun gain de prévision n'est revendiqué.

L'audit réel parcourt 8 166 912 présentations de 33 672 prix distincts. Les 195 échappements dans 40 contextes CHF motivent la correction. Un diagnostic exploratoire postérieur explique le cas extrême par un ancien niveau exprimé dans une petite unité de volatilité récente ; ce n'est pas un choc quotidien de 463 écarts-types. L'audit initial et le diagnostic ont des traces séparées.

Les études antérieures portent sur 58 240 bougies horaires complètes en reconstruction, 33 792 références BCE et six séries mensuelles de matières premières complètes de 1960 à 2020. Ces unités et leurs répétitions ne sont pas additionnées comme des exemples indépendants. Les fichiers reçus en 2026 ne sont pas certifiés être les versions disponibles à chaque date historique.

## Détails et preuves reproductibles

Les cinq notes sont désormais intégrées dans l'archive publiée ; elles développent les formules du chapitre 10 : [candidat 0.3](notes_p1d_candidat_20261015.md), [ancres et DPCM](notes_ancres_causalite_dpcm_20261015.md), [alphabet et paramètres, avec amendement 0.3](notes_alphabet_information_egale_20261015.md), [témoins exacts](notes_temoins_p1d_20261015.md), [audit réel et langage hybride](notes_audit_reel_et_langage_hybride_20261015.md).

[Protocole documentaire courant](../../research/trame_protocol_p1d/protocol_candidate.json) - [Rapport descriptif](../../research/trame_protocol_p1d/audits/preflight_01/report.json) - [Diagnostic CHF exploratoire](../../research/trame_protocol_p1d/audits/preflight_01/followup_scale_report.json). Les versions 0.1 et 0.2 et les gels de calcul restent conservés. Publication du dossier ne signifie pas gel du protocole prédictif.

Le panel est simulé. Aucune nouvelle relecture indépendante n'a pu être menée : les tâches auxiliaires ont échoué sur une limite de service. La consolidation a été vérifiée par le principal, avec inspection visuelle de toutes les pages modifiées et vérification des empreintes des éléments conservés.

## Étape suivante

Fixer les sensibilités numériques, initialisations, budgets, optimisation et diagnostics ; préciser le flux causal P1-B et l'évaluation indépendante. Poursuivre la réflexion multi-marchés et multi-échelles. Aucun entraînement, achat de données ou calcul payant ne découle implicitement de ce dossier.

## Historique

[Édition 2.1, 72 pages](../../output/versions/TRAME_dossier_v2_1_scientifique_20261015.zip) - [Édition 2, 63 pages](../../output/versions/TRAME_dossier_v2_scientifique_20261014.zip) - [Édition 1](../../output/versions/TRAME_dossier_v1_documentaire_20261014.zip).

Archives de travail : [0.3](../../output/travail_en_cours/TRAME_P1D_candidat_0_3_20261015.zip), [0.2](../../output/travail_en_cours/TRAME_P1D_candidat_0_2_20261015.zip), [0.1](../../output/travail_en_cours/TRAME_P1D_candidat_20261015.zip). Elles restent figées et ne remplacent pas l'édition complète 2.2.

[Journal](JOURNAL_DES_VERSIONS.md) - [Bibliographie](BIBLIOGRAPHIE_LIENS.md) - [Continuité](CONTINUITE.md).
'''
(D/'LIRE_EN_PREMIER.md').write_text(guide,encoding='utf-8')

links={}
for e in M:
    for title,url in re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',Path(e['source']).read_text(encoding='utf-8')):
        if url not in links: links[url]=[title,set()]
        links[url][1].add(e['number'])
old_bib=(D/'BIBLIOGRAPHIE_LIENS.md').read_text(encoding='utf-8')
prefix=re.split(r'^1\. ',old_bib,flags=re.M)[0]
prefix=prefix.replace('version scientifique 2.1','version scientifique 2.2').replace('des dix documents','des onze documents')
prefix+='Les références des notes P1-D sont consolidées dans le chapitre 10. Aucun nouvel article ni résultat externe n’a été vérifié pendant la seule opération de publication 2.2 ; les lectures ciblées antérieures et leurs limites restent celles des audits de sources.\n\n'
for i,(url,(title,docs)) in enumerate(links.items(),1):
    prefix+=f"{i}. [{title}]({url}) - documents {', '.join(sorted(docs))}.\n"
(D/'BIBLIOGRAPHIE_LIENS.md').write_text(prefix,encoding='utf-8')

continuity=(D/'CONTINUITE.md').read_text(encoding='utf-8')
continuity=continuity.replace('État au 15 octobre 2026, version scientifique 2.1.','État au 15 octobre 2026, édition scientifique publiée 2.2 ; candidat expérimental courant 0.3.')
continuity=continuity.replace('Dix documents actifs 00-09, synthèse générale de 3 pages et première page de 09 résumant la mise à jour. Dossier PDF de 72 pages. Versions 1 (64 pages) et 2 (63 pages) archivées. Les éditions 00-08 restent inchangées, complétées/amendées explicitement par 09 (9 pages).','Onze documents actifs 00-10, synthèse générale de 3 pages actualisée et chapitre 10 de 12 pages. Dossier PDF de 84 pages. Versions 1 (64 pages), 2 (63 pages) et 2.1 (72 pages) archivées. Les éditions 01-09 restent inchangées ; 10 consolide et amende leurs propositions expérimentales selon le candidat 0.3.')
continuity=continuity.replace('conformité des fenêtres réelles pas encore auditée.','conformité des fenêtres réelles non encore auditée à cette étape 0.2, puis vérifiée dans 0.3 ci-dessous.')
continuity=continuity.replace('Blocs calendaires B3 et conditions numériques restent à vérifier.','À cette étape 0.2, blocs calendaires B3 et conditions numériques restaient à vérifier ; ils sont vérifiés dans 0.3 ci-dessous.')
start=continuity.index('Attention : les travaux intermédiaires 0.1–0.3')
continuity=continuity[:start]+'''## Publication 2.2 consolidée, session du 15 octobre au soir

Les travaux 0.1-0.3 sont maintenant intégrés à l'archive publiée. Synthèse 00 actualisée, chapitre 10 de 12 pages, ensemble de 84 pages avec onze signets. Le chapitre 10 amende les propositions antérieures lorsque nécessaire ; les cinq notes détaillées restent disponibles. Les PDFs et sources 01-09 sont conservés exactement, vérifiés contre l'archive 2.1. L'ancienne synthèse est conservée dans cette même archive. La publication n'a modifié ni le candidat 0.3, ni les notes de travail, ni les rapports d'audit.

Les nouvelles pages 00 et 10 et la couverture ont toutes été rendues et inspectées visuellement. Contrôles structurels, liens locaux, intégrité des archives, gels et fichiers sources dans tmp/pdfs/v22/final_qa.json. Archive actuelle output/TRAME_dossier_et_sources.zip ; copie historique output/versions/TRAME_dossier_v2_2_scientifique_20261015.zip. Archives 2.1 et travail 0.3 préservées. Aucun calcul de modèle ou nouvelle acquisition pendant cette consolidation.

Ne pas relancer les anciens scripts de publication. Le nouveau build_trame_v22.py réutilise les fonctions de rendu sans exécuter l'ancienne publication ; package_scientific_v22.py interdit d'écraser l'archive historique 2.2. L'étape suivante reste scientifique : fermer les sensibilités numériques, les initialisations, budgets et diagnostics, puis formaliser P1-B causal et le test indépendant. Ne pas se limiter à produire de nouveaux résumés ; les hypothèses de langage et le passage à l'échelle restent à challenger. Les agents auxiliaires n'ont pas été relancés sans motif après leur limite de service connue.
'''
(D/'CONTINUITE.md').write_text(continuity,encoding='utf-8')

journal=(D/'JOURNAL_DES_VERSIONS.md').read_text(encoding='utf-8')
journal+='''
## Publication scientifique 2.2 - 15 octobre 2026, session du soir

Consolidation des cinq notes et du candidat P1-D 0.3 dans un nouveau chapitre 10 de douze pages. Synthèse 00 mise à jour, toujours trois pages. Le dossier complet contient 84 pages et onze documents ; le chapitre 10 prévaut sur les propositions expérimentales anciennes lorsqu'elles diffèrent. Sources et PDFs 01-09 préservés exactement. Aucun nouveau résultat de prévision, aucune nouvelle mesure de prix et aucune modification du candidat pendant cette publication.

Le nouveau texte relie équivalence d'information, causalité, audit réel, correction hybride, comptes de paramètres, témoins et futur flux P1-B. Il reprend les 195 échappements CHF et distingue la mesure initiale du diagnostic exploratoire postérieur. Les notions de reconstruction, de prévision et de preuve indépendante restent séparées. Les pistes symboliques pures ne sont pas déclarées réfutées.

Index, bibliographie et continuité actualisés. Toutes les pages nouvelles ou modifiées ont été inspectées après rendu. Archive publiée enrichie des cinq notes, du protocole et de ses versions, des rapports et traces. Les archives 2.1 et de travail 0.3 sont conservées par empreinte. Aucune validation indépendante supplémentaire ; panel simulé inchangé, pas de dixième cycle inventé.
'''
(D/'JOURNAL_DES_VERSIONS.md').write_text(journal,encoding='utf-8')

issues=[]
with pdfplumber.open(O/'pdf/TRAME_Dossier_complet.pdf') as pdf:
    assert len(pdf.pages)==total
    for i,p in enumerate(pdf.pages,1):
        content=p.extract_text() or ''
        if not content.strip() or '\ufffd' in content: issues.append({'page':i,'text_issue':True})
        bad=[w['text'] for w in p.extract_words() if w['x0']<20 or w['x1']>p.width-20 or w['top']<7 or w['bottom']>p.height-7]
        if bad: issues.append({'page':i,'bounds':bad})
assert not issues,issues
assert len(PdfReader(O/'pdf/TRAME_Dossier_complet.pdf').outline)==11
for e in M:
    assert hashlib.sha256(Path(e['pdf']).read_bytes()).hexdigest()==e['sha256']

R=ROOT/'research/trame_poc0'
freeze=json.loads((R/'freeze.json').read_text())
for file,key in [('protocol.json','protocol_sha256'),('run_research.py','analysis_sha256')]:
    assert hashlib.sha256((R/file).read_bytes()).hexdigest()==freeze[key]
assert not list((R/'raw').rglob('*2021-11*')) and not list((R/'raw').rglob('*2021-12*'))
ecb=next((R/'ecb_exploratory/raw').glob('*.csv'))
assert hashlib.sha256(ecb.read_bytes()).hexdigest()=='b8a684b6331d3cf0310a1838efdce806495906ead99d672671642c3bf24130de'
wb=ROOT/'research/trame_corpus/worldbank'
assert hashlib.sha256(next(wb.glob('*.xlsx')).read_bytes()).hexdigest()=='ea1c350827878ea3bbe30e3cda16a13fd3bd5b409b8458940dc94a36b5a33154'

broken=[]
for source in [D/'LIRE_EN_PREMIER.md']+[Path(e['source']) for e in M if e['number'] in ('00','10')]:
    for target in re.findall(r'\]\(([^)]+)\)',source.read_text(encoding='utf-8')):
        if target.startswith(('http:','https:','#')): continue
        p=(source.parent/target).resolve()
        if not p.exists() and p!=dest: broken.append(str(p))
assert not broken,broken
qa={'edition':'2.2','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'pages':total,'documents':11,'bookmarks':11,'summary_pages':3,'new_chapter_pages':12,'external_link_targets':len(links),
    'visual_review':'All 16 new/changed pages inspected: cover, 3 summary pages, 12 chapter pages, rendered at 100 dpi.',
    'prior_01_09_pdf_and_sources_equal_v21':True,'candidate_audit_and_notes_preserved_from_working_zip':preserved,
    'old_archives_sha256_verified':True,'poc0_freeze_verified':True,'ecb_worldbank_sha256_verified':True,
    'protected_months_absent':True,'layout_issues':issues,'broken_local_links':broken,
    'new_market_analysis':False,'new_model_training':False,'independent_review':False}
(W/'final_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')

# Reuse the published file list, replacing current edited files and adding this edition.
files={ROOT/name for name in old_names}
files.update(Path(e['source']) for e in M); files.update(Path(e['pdf']) for e in M)
files.update(D.glob('notes_*20261015.md'))
files.update(p for p in (ROOT/'research/trame_protocol_p1d').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
files.update([W/'final_qa.json',W/'manifest.json',ROOT/'tmp/pdfs/build_trame_v22.py',Path(__file__).resolve()])
assert all(p.exists() for p in files),[str(p) for p in files if not p.exists()]
archive=O/'TRAME_dossier_et_sources.zip'
temp=W/'TRAME_dossier_et_sources.zip'
with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(files): z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(temp) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
shutil.copyfile(temp,archive); shutil.copyfile(temp,dest)
receipt={'version':'2.2','files':len(files),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
         'current':str(archive),'historical':str(dest)}
(W/'archive_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'qa':qa,'archive':receipt},ensure_ascii=False,indent=2))
