from pathlib import Path
import hashlib,json,re,zipfile,datetime
import pdfplumber
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2]; D=ROOT/'dossier/recherche_lcm'; R=ROOT/'research/trame_poc0'; O=ROOT/'output'
manifest=json.loads((ROOT/'tmp/pdfs/manifest.json').read_text(encoding='utf-8'))
total=1+sum(e['pages'] for e in manifest)
guide=f'''# TRAME : dossier scientifique actif

Version 2 du 14 octobre 2026. Neuf documents, {total} pages assemblées. L'objet est la prévision scientifique des prix multi-marchés par représentations et modèles de type GPT. Les documents sont révisables ; le cadrage applicatif de la version 1 n'est plus actif.

Commencer par les trois pages de synthèse, puis le document 08 sur Marché latent et GPT. Le document 05 fournit le programme d'échelle ; le document 07 présente les observations réellement mesurées.

| Document | Pages | PDF | Source modifiable |
|---|---:|---|---|
'''
for e in manifest:
 guide+=f"| {e['number']} {e['name']} | {e['pages']} | [Lire](../../output/pdf/{Path(e['pdf']).name}) | [Markdown]({Path(e['source']).name}) |\n"
guide+='''

[Dossier complet](../../output/pdf/TRAME_Dossier_complet.pdf) - [Archive de la version précédente](../../output/versions/TRAME_dossier_v1_documentaire_20261014.zip).

La version 2 comprend une étude de reconstruction sur 58 240 bougies horaires complètes, avant exclusions de contexte, et un audit de 33 792 références quotidiennes de devises. Ce ne sont pas des prévisions. Aucun modèle neuronal n'a été entraîné ; aucun corpus général à la seconde n'a été constitué.

Le corpus de reconstruction est un témoin méthodologique. Les devises BCE apportent une autre famille et une histoire 1999–2020, sans OHLCV inventé. Les deux ensembles conservent provenance, empreintes, absences et limites de disponibilité historique. Le dossier research/trame_poc0 contient les instruments de mesure, tests, manifestes et résultats.

Le panel de dix profils est fictif. Les relectures entre agents logiciels et les recherches bibliographiques sont réelles, avec leur portée précisée. Ni un consensus du panel, ni une bonne reconstruction ne prouvent une compétence prédictive.

[Journal des versions](JOURNAL_DES_VERSIONS.md) - [Bibliographie de liens](BIBLIOGRAPHIE_LIENS.md) - [État pour la poursuite de la recherche](CONTINUITE.md).
'''
(D/'LIRE_EN_PREMIER.md').write_text(guide,encoding='utf-8')

links={}
for e in manifest:
 for title,url in re.findall(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',Path(e['source']).read_text(encoding='utf-8')):
  if url not in links: links[url]=[title,set()]
  links[url][1].add(e['number'])
bib='# Bibliographie liée de la version scientifique 2\n\nLiens extraits des neuf documents. Les dates, versions, degrés de lecture et limites sont précisés près des affirmations dans les documents sources. Un lien accessible ne constitue pas une reproduction du résultat.\n\n'
for i,(url,(title,docs)) in enumerate(links.items(),1): bib+=f"{i}. [{title}]({url}) - documents {', '.join(sorted(docs))}.\n"
(D/'BIBLIOGRAPHIE_LIENS.md').write_text(bib,encoding='utf-8')

continuity='''# Continuité de la recherche TRAME

État au 14 octobre 2026, version scientifique 2.

## Instructions actives du porteur

Recherche approfondie sur le langage des courbes et la prévision des prix bruts, plusieurs familles d'actifs, longue histoire et temporalités fines si réellement disponibles. GPT constitue l'axe architectural principal. Les essais à petite taille ne peuvent pas réfuter toute une langue. Les deux intuitions à tester sont grammaires partagées et observations d'un Marché latent commun. Le cadrage applicatif initial n'appartient plus au dossier principal. Mettre les documents à jour après chaque itération et conserver les anciennes versions.

La demande initiale est une réflexion et une conception, sans développement d'un modèle à ce stade. Les scripts présents servent uniquement à auditer les données et à mesurer la reconstruction pour la recherche ; aucun modèle prédictif n'est implémenté ou entraîné. Ne pas transformer une poursuite documentaire en lancement de calcul payant ou en entraînement massif implicite.

## Travail achevé et artefacts

Neuf documents actifs 00–08, synthèse de 3 pages, dossier PDF de 63 pages. Ancienne version de 64 pages archivée. Théorie GPT et apprentissage multivue, numéraire et cohérence entre échelles, effets d'échelle, panel de 10 profils fictifs avec 6 cycles, sources actualisées. Voir LIRE_EN_PREMIER et JOURNAL_DES_VERSIONS.

POC0 : 80 archives réelles, 58 264 lignes sources, 104 heures absentes, 24 bougies à fermeture anticipée, 58 240 complètes. Protocole gelé puis amendement 1.1 avant métriques, traces dans research/trame_poc0. Neuf contrôles de calcul réussis. Les rapports comparent cinq codecs, sans prévision. Les quantiles 64 ont une bonne erreur moyenne H1 mais de fortes distorsions sur de rares amplitudes ; seulement 37 bougies de queue nominales H1 et 7 H4, possiblement corrélées. Cela ne réfute ni vocabulaire appris ni GPT. Aucune conclusion de performance prédictive n'est possible.

BCE : requête 1999–2020 uniquement, six devises contre EUR, 33 792 valeurs numériques, 372 cellules H, 46 dates ouvrées sans ligne non certifiées individuellement. Version historique reçue en 2026, sans preuve des versions disponibles à chaque date. Changement de publication de 14:30 vers 16:00 CET au 1er juillet 2016. Aucune géométrie OHLCV n'est fabriquée. Note finale : notes_bce_reelle_20261014.md.

## Prochain bloc de recherche utile

Préciser un premier protocole de prévision multi-familles avec une cible de prix commune, sans lancer l'entraînement : choisir les instruments exacts (or, indices, devises, actions), qualifier les sources réelles et construire une matrice profondeur/résolution/droits/disponibilité. Étudier les variantes progressives de langage et leur débit réel incluant ancres, échelles et résidus. Fixer les contrastes langue × capacité et partage de paramètres × information croisée. Les documents 05 et 08 posent le programme, mais les valeurs d'un protocole de prévision ne sont pas gelées.

Les mois crypto novembre/décembre 2021 n'ont pas été téléchargés dans POC0. Ne pas les ouvrir pour régler les langues. Le corpus BCE audité est exploratoire et ne peut pas être présenté comme un test final inédit. Ne pas repartir de zéro, ne pas refaire les acquisitions déjà réussies, et n'affirmer aucun entraînement, achat ou résultat non exécuté.
'''
# Keep continuity readable, including for a later automated wake-up.
continuity=continuity.replace('synthèse3pages','synthèse de 3 pages').replace('dossierPDF63pages','dossier PDF de 63 pages')
(D/'CONTINUITE.md').write_text(continuity,encoding='utf-8')

issues=[]
with pdfplumber.open(O/'pdf/TRAME_Dossier_complet.pdf') as pdf:
 assert len(pdf.pages)==total
 for n,page in enumerate(pdf.pages,1):
  text=page.extract_text() or ''
  if not text.strip(): issues.append({'page':n,'empty':True})
  if '\ufffd' in text: issues.append({'page':n,'replacement_glyph':True})
  bad=[w['text'] for w in page.extract_words() if w['x0']<20 or w['x1']>page.width-20 or w['top']<7 or w['bottom']>page.height-7]
  if bad: issues.append({'page':n,'out_of_bounds':bad})
assert not issues,issues
assert len(PdfReader(O/'pdf/TRAME_Dossier_complet.pdf').outline)==9
freeze=json.loads((R/'freeze.json').read_text())
assert hashlib.sha256((R/'protocol.json').read_bytes()).hexdigest()==freeze['protocol_sha256']
assert hashlib.sha256((R/'run_research.py').read_bytes()).hexdigest()==freeze['analysis_sha256']
assert not list((R/'raw').rglob('*2021-11*')) and not list((R/'raw').rglob('*2021-12*'))
qa={'version':2,'pages':total,'documents':9,'bookmarks':9,'links':len(links),'issues':issues,'protocol_and_analysis_hashes_verified':True,'holdout_absent':True,'visual_review':'All pages reviewed via contact sheets; critical formulas, tables and final report inspected at full size after repair of inline conditional-probability bars','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(ROOT/'tmp/pdfs/v2/final_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')

files=[O/'pdf/TRAME_Dossier_complet.pdf']+[Path(e['pdf']) for e in manifest]+[Path(e['source']) for e in manifest]
files += [D/f for f in ['LIRE_EN_PREMIER.md','BIBLIOGRAPHIE_LIENS.md','JOURNAL_DES_VERSIONS.md','CONTINUITE.md','notes_bce_reelle_20261014.md','notes_sources_poc_20261014.md','notes_scaling_scientifique_20261014.md','notes_marche_latent_20261014.md']]
files += [p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
files += [ROOT/'tmp/pdfs/v2/final_qa.json']
files += [p for p in (D/'sources_reelles').glob('*') if p.is_file()]
package=O/'TRAME_dossier_et_sources.zip'
with zipfile.ZipFile(package,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for path in sorted(set(files)):z.write(path,path.relative_to(ROOT))
with zipfile.ZipFile(package) as z: assert z.testzip() is None
print(json.dumps({**qa,'archive_bytes':package.stat().st_size,'archive_files':len(set(files))},ensure_ascii=False))
