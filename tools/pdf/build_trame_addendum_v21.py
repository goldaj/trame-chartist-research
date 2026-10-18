from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / 'tmp/pdfs/build_trame_documents.py'
ns = {'__file__': str(base)}
# Reuse the already verified layout functions without executing the v2 publishing block.
exec(compile(base.read_text(encoding='utf-8').split('manifest=[]')[0], str(base), 'exec'), ns)
globals().update({k: v for k, v in ns.items() if not k.startswith('__')})

def decoration21(label):
    def draw(c, doc):
        c.saveState(); c.setFont('Body', 8); c.setFillColor(colors.HexColor('#56616C'))
        c.drawString(M, H-28, 'TRAME  /  RECHERCHE SCIENTIFIQUE  /  COMPLÉMENT 2.1')
        c.drawRightString(W-M, H-28, '15 OCTOBRE 2026')
        c.setStrokeColor(colors.HexColor('#D6DDE3')); c.setLineWidth(.5); c.line(M, 35, W-M, 35)
        c.drawString(M, 22, label); c.drawRightString(W-M, 22, str(doc.page)); c.restoreState()
    return draw

names['09'] = 'Corpus, langage typé et protocole'
file = SRC / '09_corpus_langage_type_et_protocole.md'
out = OUT / ('TRAME_' + file.stem + '.pdf')
text = file.read_text(encoding='utf-8')
doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=M, leftMargin=M,
                        topMargin=49, bottomMargin=49, title=names['09'],
                        author='Codex - projet TRAME', pageCompression=1)
doc.build(md_flow(text, '09'), onFirstPage=decoration21(names['09']), onLaterPages=decoration21(names['09']))
manifest = json.loads((ROOT/'tmp/pdfs/manifest.json').read_text(encoding='utf-8'))
assert len(manifest) == 9
for e in manifest:
    assert hashlib.sha256(Path(e['pdf']).read_bytes()).hexdigest() == e['sha256']
manifest.append({'number': '09', 'name': names['09'], 'source': str(file), 'pdf': str(out),
                 'pages': len(PdfReader(out).pages), 'words': len(text.split()),
                 'sha256': hashlib.sha256(out.read_bytes()).hexdigest()})

cover = ROOT / 'tmp/pdfs/v21/index.pdf'
cover.parent.mkdir(parents=True, exist_ok=True)
flow = [para('TRAME', 'title'), para('Langages des marchés et prévision des prix', 'h2'),
        para('Dossier 2.1 - 15 octobre 2026. Les documents 00 à 08 conservent leur édition du 14 octobre ; le complément 09 précise et amende le corpus, la langue et le protocole.'),
        para('Lecture de cette mise à jour', 'h2'),
        para('Lire d’abord la première page du document 09 : acquisition réelle de matières premières, sémantique des observations, effet du moyennage et expérience en deux temps. La synthèse 00 reste l’introduction générale en trois pages.')]
offset = 1
for e in manifest:
    e['combined_start_page'] = offset + 1
    flow.append(para(f"**{e['number']}  {e['name']}** - page {offset+1} ; {e['pages']} pages", 'body'))
    offset += e['pages']
flow += [Spacer(1, 7), para('État des preuves', 'h2'),
         para('Trois sources réelles auditées et cinq encodages comparés en reconstruction. Aucun modèle prédictif entraîné. Les 4 392 valeurs mensuelles supplémentaires de 1960-2020 enrichissent l’histoire ; elles ne créent pas de trajectoires à la seconde.'),
         para('Panel humain fictif. Cette itération a été revue par l’agent principal ; les tâches parallèles ont été interrompues par une limite de service. Les versions 1 et 2 sont archivées.', 'small')]
doc = SimpleDocTemplate(str(cover), pagesize=A4, rightMargin=M, leftMargin=M, topMargin=49,
                        bottomMargin=49, title='TRAME Dossier complet 2.1', author='Codex')
doc.build(flow, onFirstPage=decoration21('Guide de lecture'), onLaterPages=decoration21('Guide de lecture'))
assert len(PdfReader(cover).pages) == 1, 'Index overflow'
writer = PdfWriter(); writer.append(str(cover)); offset = 1
for e in manifest:
    writer.append(e['pdf']); writer.add_outline_item(e['number']+' '+e['name'], offset)
    offset += e['pages']
writer.add_metadata({'/Title': 'TRAME Dossier scientifique 2.1', '/Author': 'Codex',
                     '/Subject': 'Langages, observation des prix, GPT et protocole scientifique'})
with (OUT/'TRAME_Dossier_complet.pdf').open('wb') as stream:
    writer.write(stream)
(ROOT/'tmp/pdfs/v21/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'new_pages': manifest[-1]['pages'], 'new_words': manifest[-1]['words'],
                  'combined_pages': offset, 'new_start': manifest[-1]['combined_start_page']}, indent=2))
