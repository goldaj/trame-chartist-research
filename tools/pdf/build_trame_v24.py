from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[2]
base=ROOT/'tmp/pdfs/build_trame_documents.py'
ns={'__file__':str(base)}
exec(compile(base.read_text(encoding='utf-8').split('manifest=[]')[0],str(base),'exec'),ns)
globals().update({k:v for k,v in ns.items() if not k.startswith('__')})
WORK=ROOT/'tmp/pdfs/v24';WORK.mkdir(parents=True,exist_ok=True)
names['13']='Tête générative et audit des cibles'
def decoration24(label):
    def draw(c,doc):
        c.saveState();c.setFont('Body',8);c.setFillColor(colors.HexColor('#56616C'))
        c.drawString(M,H-28,'TRAME  /  RECHERCHE SCIENTIFIQUE  /  ÉDITION 2.4')
        c.drawRightString(W-M,H-28,'16 OCTOBRE 2026')
        c.setStrokeColor(colors.HexColor('#D6DDE3'));c.setLineWidth(.5);c.line(M,35,W-M,35)
        c.drawString(M,22,label);c.drawRightString(W-M,22,str(doc.page));c.restoreState()
    return draw
manifest=json.loads((ROOT/'tmp/pdfs/v23/manifest.json').read_text(encoding='utf-8'))
for e in manifest: assert hashlib.sha256(Path(e['pdf']).read_bytes()).hexdigest()==e['sha256']
source=SRC/'13_tete_generative_et_audit_des_cibles.md';content=source.read_text(encoding='utf-8')
output=OUT/('TRAME_'+source.stem+'.pdf')
doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=49,bottomMargin=49,
                     title=names['13'],author='Codex - projet TRAME',pageCompression=1)
doc.build(md_flow(content,'13'),onFirstPage=decoration24(names['13']),onLaterPages=decoration24(names['13']))
manifest.append({'number':'13','name':names['13'],'source':str(source),'pdf':str(output),
    'pages':len(PdfReader(output).pages),'words':len(content.split()),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()})
flow=[para('TRAME','title'),para('Langage génératif et prix bruts','h2'),
      para('Édition 2.4 - 16 octobre 2026. Nouveau chapitre 13 : sortie GPT, limites de distribution et audit de cibles réelles. Les documents 00-12 sont conservés ; 13 précise et amende P1-B0 en révision 0.2.'),
      para('Lecture rapide : synthèse 00, puis section 1 du chapitre 13. Plan général : 11. Aucun modèle construit ou entraîné ; les nouveaux résultats concernent la reconstruction historique et des calculs de conception.')]
offset=1
for e in manifest:
    e['combined_start_page']=offset+1
    flow.append(para(f"**{e['number']}  {e['name']}** - page {offset+1} ; {e['pages']} pages"))
    offset+=e['pages']
flow.extend([Spacer(1,4),para('Statut des preuves','h2'),
      para('304 920 présentations de cibles issues de 15 360 cotations distinctes. Audit limité à la partition BCE 1999-2009 déjà exploratoire ; aucune performance prédictive. Les bornes de queues et les fonctions numériques restent des sujets de qualification.'),
      para('Personas simulés, sans validation indépendante. Anciennes éditions et rapports conservés ; protocole prédictif amendable.','small')])
cover=WORK/'index.pdf'
doc=SimpleDocTemplate(str(cover),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=49,bottomMargin=49,
                      title='Guide TRAME 2.4',author='Codex')
doc.build(flow,onFirstPage=decoration24('Guide de lecture'),onLaterPages=decoration24('Guide de lecture'))
assert len(PdfReader(cover).pages)==1
writer=PdfWriter();writer.append(str(cover));offset=1
for e in manifest:
    writer.append(e['pdf']);writer.add_outline_item(e['number']+' '+e['name'],offset);offset+=e['pages']
writer.add_metadata({'/Title':'TRAME - Dossier scientifique 2.4','/Author':'Codex',
                     '/Subject':'Tête générative, langage de prix et audit des cibles historiques'})
with (OUT/'TRAME_Dossier_complet.pdf').open('wb') as f:writer.write(f)
(WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'pages':offset,'new':manifest[-1]},ensure_ascii=False,indent=2))
