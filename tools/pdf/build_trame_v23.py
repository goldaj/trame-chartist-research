from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parents[2]
base=ROOT/'tmp/pdfs/build_trame_documents.py'
ns={'__file__':str(base)}
exec(compile(base.read_text(encoding='utf-8').split('manifest=[]')[0],str(base),'exec'),ns)
globals().update({k:v for k,v in ns.items() if not k.startswith('__')})
WORK=ROOT/'tmp/pdfs/v23'; WORK.mkdir(parents=True,exist_ok=True)
names['11']='Plan de recherche et personas'; names['12']='Témoins numériques et génération causale'
def decoration23(label):
    def draw(c,doc):
        c.saveState(); c.setFont('Body',8); c.setFillColor(colors.HexColor('#56616C'))
        c.drawString(M,H-28,'TRAME  /  RECHERCHE SCIENTIFIQUE  /  ÉDITION 2.3')
        c.drawRightString(W-M,H-28,'15 OCTOBRE 2026')
        c.setStrokeColor(colors.HexColor('#D6DDE3')); c.setLineWidth(.5); c.line(M,35,W-M,35)
        c.drawString(M,22,label); c.drawRightString(W-M,22,str(doc.page)); c.restoreState()
    return draw
manifest=json.loads((ROOT/'tmp/pdfs/v22/manifest.json').read_text(encoding='utf-8'))
for e in manifest:
    assert hashlib.sha256(Path(e['pdf']).read_bytes()).hexdigest()==e['sha256']
for number,file in [('11','11_plan_recherche_et_personas.md'),('12','12_controles_numeriques_et_generation_causale.md')]:
    source=SRC/file; content=source.read_text(encoding='utf-8'); output=OUT/('TRAME_'+source.stem+'.pdf')
    doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=49,bottomMargin=49,
                          title=names[number],author='Codex - projet TRAME',pageCompression=1)
    doc.build(md_flow(content,number),onFirstPage=decoration23(names[number]),onLaterPages=decoration23(names[number]))
    manifest.append({'number':number,'name':names[number],'source':str(source),'pdf':str(output),
        'pages':len(PdfReader(output).pages),'words':len(content.split()),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()})
flow=[para('TRAME','title'),para('Programme de recherche et langage des prix','h2'),
      para('Édition 2.3 - 15 octobre 2026. Lire 11 pour le plan et les personas, puis 12 pour les premières décisions exécutées. Les documents 00 à 10 sont conservés ; 12 amende P1-D en 0.4 et introduit P1-B0, séparé et théorique.'),
      para('La synthèse 00 reste une introduction de trois pages. Le plan engage la conception et des vérifications arithmétiques ; aucun modèle construit ou entraîné, aucune campagne de calcul lancée.')]
offset=1
for e in manifest:
    e['combined_start_page']=offset+1
    flow.append(para(f"**{e['number']}  {e['name']}** - page {offset+1} ; {e['pages']} pages"))
    offset+=e['pages']
flow.extend([Spacer(1,6),para('Lecture des preuves','h2'),
             para('Données et audits précédents conservés. Nouvelles définitions d’encodeurs, budget proposé, récurrence causale et loi de codes normalisée. Les bornes de reconstruction et de moments ne sont pas des garanties de prévision.'),
             para('Personas simulés, sans validation indépendante. Toutes les versions antérieures sont archivées. Le protocole prédictif reste amendable avant gel.','small')])
cover=WORK/'index.pdf'
doc=SimpleDocTemplate(str(cover),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=49,bottomMargin=49,
                      title='Guide TRAME 2.3',author='Codex')
doc.build(flow,onFirstPage=decoration23('Guide de lecture'),onLaterPages=decoration23('Guide de lecture'))
assert len(PdfReader(cover).pages)==1
writer=PdfWriter(); writer.append(str(cover)); offset=1
for e in manifest:
    writer.append(e['pdf']); writer.add_outline_item(e['number']+' '+e['name'],offset); offset+=e['pages']
writer.add_metadata({'/Title':'TRAME - Dossier scientifique 2.3','/Author':'Codex','/Subject':'Plan de recherche, contrôles numériques et génération causale de prix'})
with (OUT/'TRAME_Dossier_complet.pdf').open('wb') as f: writer.write(f)
(WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'total_pages':offset,'new':[{k:e[k] for k in ['number','pages','words','combined_start_page']} for e in manifest[-2:]]},indent=2))
