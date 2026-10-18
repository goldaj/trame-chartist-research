from pathlib import Path
import datetime
import hashlib
import json
import re
import shutil
import zipfile
import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
D = ROOT/'dossier/recherche_lcm'; O = ROOT/'output'; R = ROOT/'research/trame_poc0'
manifest = json.loads((ROOT/'tmp/pdfs/v21/manifest.json').read_text(encoding='utf-8'))
total = 1 + sum(e['pages'] for e in manifest)
guide = f'''# TRAME : dossier scientifique actif

Version 2.1 du 15 octobre 2026. Dix documents, {total} pages assemblées. Les documents 00-08 conservent leur édition du 14 octobre. Le complément 09 précise et amende les points relatifs au corpus, au langage et au protocole. Les versions précédentes sont conservées.

**Pour lire seulement la mise à jour, commencer par la première page du document 09.** Pour découvrir le projet, lire les trois pages de synthèse 00, puis 08 sur Marché latent et GPT. L'objet demeure la prévision scientifique des prix bruts, avec plusieurs familles d'actifs et des observations réelles. Aucun modèle prédictif n'a été développé ou entraîné.

| Document | Pages | PDF | Source modifiable |
|---|---:|---|---|
'''
for e in manifest:
    guide += f"| {e['number']} {e['name']} | {e['pages']} | [Lire](../../output/pdf/{Path(e['pdf']).name}) | [Markdown]({Path(e['source']).name}) |\n"
guide += '''
[Dossier complet](../../output/pdf/TRAME_Dossier_complet.pdf) - [Archive complète actuelle](../../output/TRAME_dossier_et_sources.zip) - [Version 2 archivée](../../output/versions/TRAME_dossier_v2_scientifique_20261014.zip) - [Version 1 archivée](../../output/versions/TRAME_dossier_v1_documentaire_20261014.zip).

## Ce qui a réellement été fait

Une étude de reconstruction porte sur 58 240 bougies horaires complètes, avant exclusions de contexte. Un audit BCE porte sur 33 792 références quotidiennes de devises. Le nouveau fichier Banque mondiale apporte notamment six séries de matières premières avec chacune 732 valeurs mensuelles entre 1960 et 2020, soit 4 392 valeurs. Ces unités différentes ne sont pas additionnées comme si elles étaient des exemples indépendants de même nature.

Le complément démontre analytiquement un effet connu de l'agrégation et propose un langage qui décrit le type d'observation, sa précision et sa disponibilité. Le protocole P1 compare séparément représentation, capacité, partage de paramètres et contexte des autres actifs. Il reste à figer et à exécuter. Les sources fines pour actions, or et indices sont qualifiées au niveau de leurs catalogues, sans acquisition commerciale.

Les données et outils d'audit se trouvent dans research/trame_poc0 et research/trame_corpus/worldbank. Les observations restent intactes, les erreurs et absences explicites. Les fichiers reçus en 2026 ne sont pas présumés correspondre aux versions publiées à chaque date historique.

Le panel est fictif. Les trois relectures parallèles tentées pour le complément 2.1 ont échoué sur une limite de service ; cette itération a été menée et vérifiée par l'agent principal, sans validation indépendante. Une reconstruction fidèle ou un accord du panel ne prouve aucune performance prédictive.

[Journal des versions](JOURNAL_DES_VERSIONS.md) - [Bibliographie de liens](BIBLIOGRAPHIE_LIENS.md) - [Continuité de la recherche](CONTINUITE.md).
'''
(D/'LIRE_EN_PREMIER.md').write_text(guide, encoding='utf-8')

links = {}
for e in manifest:
    for title, url in re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', Path(e['source']).read_text(encoding='utf-8')):
        if url not in links: links[url] = [title, set()]
        links[url][1].add(e['number'])
bib = '# Bibliographie liée de la version scientifique 2.1\n\nLiens extraits des dix documents. Les versions, degrés de lecture et limites sont précisés près des affirmations. Un lien ne constitue pas une reproduction de résultat. Le fichier Banque mondiale et ses métadonnées sont conservés avec un manifeste dans research/trame_corpus/worldbank.\n\n'
for i, (url, (title, docs)) in enumerate(links.items(), 1):
    bib += f"{i}. [{title}]({url}) - documents {', '.join(sorted(docs))}.\n"
(D/'BIBLIOGRAPHIE_LIENS.md').write_text(bib, encoding='utf-8')

continuity = (D/'CONTINUITE.md').read_text(encoding='utf-8')
continuity = continuity.replace('État au 14 octobre 2026, version scientifique 2.', 'État au 15 octobre 2026, version scientifique 2.1.')
continuity = continuity.replace('Neuf documents actifs 00–08, synthèse de 3 pages, dossier PDF de 63 pages. Ancienne version de 64 pages archivée.', 'Dix documents actifs 00-09, synthèse générale de 3 pages et première page de 09 résumant la mise à jour. Dossier PDF de 72 pages. Versions 1 (64 pages) et 2 (63 pages) archivées. Les éditions 00-08 restent inchangées, complétées/amendées explicitement par 09 (9 pages).')
start = continuity.index('## Prochain bloc de recherche utile')
continuity = continuity[:start] + '''## Complément 2.1 achevé

Banque mondiale : fichier réel reçu le 15 octobre 2026 à 07:09:25 UTC, 586 099 octets, SHA-256 ea1c350827878ea3bbe30e3cda16a13fd3bd5b409b8458940dc94a36b5a33154. Feuille Monthly Prices : 71 séries, 801 mois 1960-2026, 50 451 nombres, 6 416 absences et quatre erreurs Excel Rice Thai 25%. Six séries (or, argent, cuivre, Brent, maïs, blé HRW) complètes 1960-2020 : 4 392 nombres. Définition Gold changée juin 2025, Description!B103. Pas de modèle ni de score prédictif. Audit en lecture seule dans research/trame_corpus/worldbank. L'historique est exploratoire et révisé, pas une archive point-in-time. Ne pas traiter les indices composites comme actifs indépendants ; pas de chemin 1 seconde reconstruit depuis des moyennes.

09 ajoute contrat d'observation typé, dérivation analytique d'autocorrélation 1/4 sous moyennage d'un brownien (effet classique, pas mesure sur l'or), langue à raffinements binaires avec borne de reconstruction, distinction P1-A représentation du passé / tête physique commune et P1-B génération autorégressive des prochains codes. Le protocole distingue partage des paramètres et information croisée, contrôle des numéraires et disponibilités. Pas de nouveauté absolue revendiquée : Kronos a déjà du grossier/fin.

Sources qualifiées : FRED SP500 dix ans glissants avec restrictions ; NYSE Daily TAQ 1993+, précision des temps variable selon époque ; Databento futures 2010-06+, OHLCV 1s sans ligne si aucune transaction, journée UTC et définition de contrat. Aucun achat ni acquisition de ces corpus fins. SP500 reste une interprétation du SP550 utilisateur.

Trois sous-tâches d'agents ont échoué sur limite de service, sans livrables exploitables. Le principal a poursuivi seul. Panel fictif et absence de relecture indépendante explicités. Les limites de service ne sont pas une raison d'arrêter les travaux que le principal peut mener.

## Prochain bloc de recherche utile

Transformer P1 en fiche préenregistrable pour une première tâche BCE quotidienne (P1-D), sans développement ni entraînement : conventions et disponibilité, origines/horizons, sélection des actifs, budgets de comparaison, sorties/scoring, critères d'amendement, capacités diagnostiques puis échelle. Les détails demeurent proposés, non gelés. P1-M sur l'or mensuel constitue un test complémentaire d'observation. La haute fréquence GC/ES/actions reste à qualifier sur échantillons réels et conditions d'accès avant toute acquisition.

Conserver l'idée centrale du langage, explorer alternatives audacieuses et ne pas faire de la collecte la seule contribution. La richesse des entrées, la quantité de données et la puissance sont des axes distincts. Une petite expérience ne réfute pas une langue universellement. Les sources et les modifications des conclusions restent traçables.

Les mois crypto novembre/décembre 2021 n'ont pas été téléchargés dans POC0. Ne pas les ouvrir pour régler les langues. Les corpus BCE et Banque mondiale audités sont exploratoires, pas des tests finaux inédits. Ne pas refaire les acquisitions ni les mesures déjà réussies. Les fichiers du gel POC0 restent inchangés. Aucun modèle, achat ou résultat non exécuté ne doit être annoncé.

Les outils de publication de la version 2 sont historiques : ne pas relancer package_scientific_v2.py ou update_scientific_docs.py, qui écraseraient la continuité. La publication 2.1 réutilise les PDFs 00-08 intacts et ajoute 09 au dossier complet. Voir tmp/pdfs/v21/manifest.json et final_qa.json. Archive complète actuelle : output/TRAME_dossier_et_sources.zip ; version figée 2.1 dans output/versions.
'''
(D/'CONTINUITE.md').write_text(continuity, encoding='utf-8')

issues = []
with pdfplumber.open(O/'pdf/TRAME_Dossier_complet.pdf') as pdf:
    assert len(pdf.pages) == total
    for n, page in enumerate(pdf.pages, 1):
        text = page.extract_text() or ''
        if not text.strip() or '\ufffd' in text: issues.append({'page': n, 'text_issue': True})
        bad = [w['text'] for w in page.extract_words() if w['x0']<20 or w['x1']>page.width-20 or w['top']<7 or w['bottom']>page.height-7]
        if bad: issues.append({'page': n, 'out_of_bounds': bad})
assert not issues, issues
assert len(PdfReader(O/'pdf/TRAME_Dossier_complet.pdf').outline) == 10
freeze = json.loads((R/'freeze.json').read_text())
for filename, key in [('protocol.json','protocol_sha256'),('run_research.py','analysis_sha256')]:
    assert hashlib.sha256((R/filename).read_bytes()).hexdigest() == freeze[key]
assert not list((R/'raw').rglob('*2021-11*')) and not list((R/'raw').rglob('*2021-12*'))
wb = ROOT/'research/trame_corpus/worldbank'
acquisition = json.loads((wb/'acquisition_manifest.json').read_text(encoding='utf-8'))
assert hashlib.sha256(next(wb.glob('*.xlsx')).read_bytes()).hexdigest() == acquisition['sha256']
qa = {'version':'2.1','pages':total,'documents':10,'bookmarks':10,'links':len(links),
      'issues':issues,'poc0_hashes_verified':True,'protected_months_absent':True,'worldbank_source_hash_verified':True,
      'visual_review':'Nine new pages and updated cover inspected via rendered PNGs; old PDFs preserved by SHA-256.',
      'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(ROOT/'tmp/pdfs/v21/final_qa.json').write_text(json.dumps(qa, indent=2), encoding='utf-8')
files = [O/'pdf/TRAME_Dossier_complet.pdf'] + [Path(e['pdf']) for e in manifest] + [Path(e['source']) for e in manifest]
files += [D/f for f in ['LIRE_EN_PREMIER.md','BIBLIOGRAPHIE_LIENS.md','JOURNAL_DES_VERSIONS.md','CONTINUITE.md','notes_bce_reelle_20261014.md','notes_sources_poc_20261014.md','notes_scaling_scientifique_20261014.md','notes_marche_latent_20261014.md']]
for folder in (R, ROOT/'research/trame_corpus'):
    files += [p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
files += [p for p in (D/'sources_reelles').glob('*') if p.is_file()]
files += [ROOT/'tmp/pdfs/v2/final_qa.json',ROOT/'tmp/pdfs/v21/final_qa.json',ROOT/'tmp/pdfs/v21/manifest.json']
package = O/'TRAME_dossier_et_sources.zip'
with zipfile.ZipFile(package,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for path in sorted(set(files)): archive.write(path,path.relative_to(ROOT))
with zipfile.ZipFile(package) as archive: assert archive.testzip() is None
version = O/'versions/TRAME_dossier_v2_1_scientifique_20261015.zip'
if version.exists():
    assert hashlib.sha256(version.read_bytes()).hexdigest() == hashlib.sha256(package.read_bytes()).hexdigest(), 'Do not overwrite a published historical version'
else: shutil.copy2(package, version)
print(json.dumps({**qa,'archive_bytes':package.stat().st_size,'archive_files':len(set(files))},ensure_ascii=False))
