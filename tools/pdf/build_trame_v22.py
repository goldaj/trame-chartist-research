from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[2]
base = ROOT/'tmp/pdfs/build_trame_documents.py'
ns = {'__file__': str(base)}
exec(compile(base.read_text(encoding='utf-8').split('manifest=[]')[0], str(base), 'exec'), ns)
globals().update({k:v for k,v in ns.items() if not k.startswith('__')})

WORK = ROOT/'tmp/pdfs/v22'
WORK.mkdir(parents=True, exist_ok=True)
names['10'] = "Du langage à l'expérience contrôlée"

def decoration22(label):
    def draw(c, doc):
        c.saveState(); c.setFont('Body',8); c.setFillColor(colors.HexColor('#56616C'))
        c.drawString(M,H-28,'TRAME  /  RECHERCHE SCIENTIFIQUE  /  ÉDITION 2.2')
        c.drawRightString(W-M,H-28,'15 OCTOBRE 2026')
        c.setStrokeColor(colors.HexColor('#D6DDE3')); c.setLineWidth(.5); c.line(M,35,W-M,35)
        c.drawString(M,22,label); c.drawRightString(W-M,22,str(doc.page)); c.restoreState()
    return draw

old = json.loads((ROOT/'tmp/pdfs/v21/manifest.json').read_text(encoding='utf-8'))
manifest=[]
for e in old:
    if e['number'] != '00':
        assert hashlib.sha256(Path(e['pdf']).read_bytes()).hexdigest() == e['sha256']
        manifest.append(e)

for number, filename in [('00','00_synthese_accessible.md'),('10','10_langage_hybride_et_experience_controlee.md')]:
    source=SRC/filename; content=source.read_text(encoding='utf-8'); output=OUT/('TRAME_'+source.stem+'.pdf')
    doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=49,bottomMargin=49,
                          title=names[number],author='Codex - projet TRAME',pageCompression=1)
    doc.build(md_flow(content,number),onFirstPage=decoration22(names[number]),onLaterPages=decoration22(names[number]))
    count=len(PdfReader(output).pages)
    if number=='00': assert count==3, f'Summary has {count} pages'
    manifest.append({'number':number,'name':names[number],'source':str(source),'pdf':str(output),'pages':count,
                     'words':len(content.split()),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()})
manifest.sort(key=lambda e:e['number'])
cover=WORK/'index.pdf'
flow=[para('TRAME','title'),para('Langages des marchés et prévision des prix','h2'),
      para('Édition 2.2 - 15 octobre 2026. Synthèse 00 actualisée et nouveau chapitre 10. Les chapitres 01 à 09 conservent leur édition antérieure ; 10 prévaut pour le candidat expérimental P1-D 0.3.'),
      para('Lire les trois pages de 00 pour découvrir le projet ; lire 10 pour les dernières mesures et le protocole corrigé. Les cinq notes détaillées, sources et rapports sont inclus dans l’archive.')]
offset=1
for e in manifest:
    e['combined_start_page']=offset+1
    flow.append(para(f"**{e['number']}  {e['name']}** - page {offset+1} ; {e['pages']} pages"))
    offset+=e['pages']
flow += [Spacer(1,6),para('État des preuves','h2'),
         para('Données réelles auditées, reconstruction mesurée et conditions numériques vérifiées. Le langage hybride corrige une branche sans exemples d’ajustement ; son bénéfice prédictif reste inconnu. Aucun modèle prédictif construit ou entraîné.'),
         para('Panel simulé ; pas de nouvelle validation indépendante. Les sources révisées et le pseudo-test exploré ne constituent pas une évaluation finale intacte. Éditions antérieures archivées.','small')]
doc=SimpleDocTemplate(str(cover),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=49,bottomMargin=49,
                      title='TRAME - Guide de lecture 2.2',author='Codex')
doc.build(flow,onFirstPage=decoration22('Guide de lecture'),onLaterPages=decoration22('Guide de lecture'))
assert len(PdfReader(cover).pages)==1,'Cover overflow'
writer=PdfWriter(); writer.append(str(cover)); offset=1
for e in manifest:
    writer.append(e['pdf']); writer.add_outline_item(e['number']+' '+e['name'],offset); offset+=e['pages']
writer.add_metadata({'/Title':'TRAME - Dossier scientifique 2.2','/Author':'Codex',
                     '/Subject':'Langages, GPT, audits réels et comparaison scientifique des prix'})
with (OUT/'TRAME_Dossier_complet.pdf').open('wb') as f: writer.write(f)
(WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'total_pages':offset,'documents':len(manifest),
                  'updated':[{k:e[k] for k in ['number','pages','words','combined_start_page']} for e in manifest if e['number'] in ['00','10']]},ensure_ascii=False,indent=2))
