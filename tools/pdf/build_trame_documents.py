from pathlib import Path
import re, json, html, hashlib
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'dossier/recherche_lcm'
OUT=ROOT/'output/pdf'
OUT.mkdir(exist_ok=True,parents=True)
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf'),('Italic','ariali.ttf'),('BoldItalic','arialbi.ttf'),('Mono','consola.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='BoldItalic')
W,H=A4; M=49; CW=W-2*M
S={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.0,leading=14.0,spaceAfter=6.5,splitLongWords=1,allowWidows=0,allowOrphans=0),
 'title':ParagraphStyle('title',fontName='Bold',fontSize=23,leading=27,spaceAfter=18,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='Bold',fontSize=14,leading=18,spaceBefore=15,spaceAfter=8,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='Bold',fontSize=11.2,leading=15,spaceBefore=10,spaceAfter=6,keepWithNext=True),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.2,leading=11.4,spaceAfter=4),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=8.3,leading=11.5,spaceAfter=0,splitLongWords=1),
 'cellhead':ParagraphStyle('cellhead',fontName='Bold',fontSize=8.3,leading=11.5,textColor=colors.white,spaceAfter=0),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=10,leading=14,leftIndent=12,firstLineIndent=-9,spaceAfter=5),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=8.4,leading=11.3,spaceAfter=6,leftIndent=8,rightIndent=8,splitLongWords=1),
}

def clean(s):
    return s.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-').replace('\u00a0',' ').replace('\u202f',' ')

def inline(s):
    s=clean(s)
    holds=[]
    def keep(v):
        holds.append(v);return f'ZZINLINE{len(holds)-1}ZZ'
    s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)',lambda m:keep('<a href="'+html.escape(m[2],quote=True)+'" color="#204E70">'+html.escape(m[1])+'</a>'),s)
    s=re.sub(r'`([^`]+)`',lambda m:keep('<font name="Mono" size="8.6">'+html.escape(m[1])+'</font>'),s)
    s=html.escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
    for i,v in enumerate(holds):s=s.replace(f'ZZINLINE{i}ZZ',v)
    return s

def para(s,kind='body'):return Paragraph(inline(s),S[kind])

def pipeline_figure():
    d=Drawing(CW,96)
    labels=[('DONNÉES','Marchés réels'),('LANGAGES','Représentations'),('MODÈLE','Futurs possibles'),('ÉVALUATION','Prévision et transfert')]
    bw=(CW-42)/4
    for i,(a,b) in enumerate(labels):
        x=i*(bw+14)
        d.add(Rect(x,23,bw,52,strokeColor=colors.HexColor('#617586'),fillColor=colors.HexColor('#F1F4F7'),strokeWidth=.7))
        d.add(String(x+bw/2,55,a,fontName='Bold',fontSize=8.3,textAnchor='middle'))
        d.add(String(x+bw/2,39,b,fontName='Body',fontSize=8.5,textAnchor='middle'))
        if i<3:
            d.add(Line(x+bw+2,49,x+bw+12,49,strokeWidth=.8))
            d.add(Polygon([x+bw+12,49,x+bw+8,52,x+bw+8,46],fillColor=colors.black,strokeColor=None))
    d.add(String(0,7,'Chaque étape a son propre critère de réussite.',fontName='Italic',fontSize=8.5,fillColor=colors.HexColor('#4C5962')))
    return d

def candles_figure():
    d=Drawing(CW,235)
    left=54; bottom=35; top=198
    def y(v):return bottom+(v-5800)/600*(top-bottom)
    for v in range(5800,6401,100):
        d.add(Line(left,y(v),CW-20,y(v),strokeColor=colors.HexColor('#DEE4E9'),strokeWidth=.45))
        d.add(String(left-7,y(v)-3,str(v),fontName='Body',fontSize=8,textAnchor='end'))
    for x,vals,label in [(176,(6064.27,6307.59,5900,6028.1),'Bougie réelle'),(348,(6067.01,6308.297922,5905.392386,6030.716928),'Après quantification')]:
        o,h,l,c=vals
        d.add(Line(x,y(l),x,y(h),strokeColor=colors.HexColor('#8C3442'),strokeWidth=1.2))
        d.add(Rect(x-18,y(min(o,c)),36,abs(y(o)-y(c)),strokeColor=colors.HexColor('#8C3442'),fillColor=colors.HexColor('#BB5665')))
        d.add(String(x,14,label,fontName='Body',fontSize=9,textAnchor='middle'))
    d.add(String(left,217,'BTCUSDT spot 12 mars 2020 12:00 UTC',fontName='Bold',fontSize=10))
    d.add(String(CW-20,217,'Prix en USDT',fontName='Body',fontSize=8,textAnchor='end'))
    return d

def make_table(lines):
    def cells(line):
        # A conditional-probability bar inside inline math/code is not a column separator.
        protected=re.sub(r'`[^`]*`',lambda m:m[0].replace('|','ZZTABLEBARZZ'),line)
        protected=protected.replace('\\|','ZZTABLEBARZZ')
        return [c.strip().replace('ZZTABLEBARZZ','|') for c in protected.strip().strip('|').split('|')]
    rows=[cells(line) for line in lines]
    rows=[r for r in rows if not all(re.fullmatch(r'[:\- ]+',c or '-') for c in r)]
    if len(rows)<2:return []
    n=max(map(len,rows));rows=[r+['']*(n-len(r)) for r in rows]
    # Long narrative matrices are rendered as structured entries, not cramped columns.
    longform=(n>=4 and max(sum(len(c) for c in r) for r in rows)>460) or max(len(c) for r in rows for c in r)>520
    if longform:
        flow=[];head=rows[0]
        for row in rows[1:]:
            flow.append(para(row[0],'h3'))
            for key,val in zip(head[1:],row[1:]):flow.append(para('**'+key+' :** '+val))
        return flow
    if n==2:weights=[.33,.67]
    elif n==3:weights=[.25,.375,.375]
    elif n==4:weights=[.22,.26,.26,.26]
    else:weights=[1/n]*n
    data=[[para(c,'cellhead' if ri==0 else 'cell') for c in row] for ri,row in enumerate(rows)]
    t=Table(data,colWidths=[CW*w for w in weights],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#28475E')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),.45,colors.HexColor('#D9D9D9')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F2F5F7')])]))
    return [Spacer(1,4),t,Spacer(1,9)]

def md_flow(text,number):
    lines=text.splitlines(); flow=[];buf=[];i=0;added_figure=False
    def flush():
        if buf:flow.append(para(' '.join(buf)));buf.clear()
    while i<len(lines):
        s=lines[i].strip()
        if not s:flush();i+=1;continue
        if s.startswith('<!-- pagebreak'):flush();flow.append(PageBreak());i+=1;continue
        if s.startswith('<!-- pocfigure'):
            flush();flow.extend([Image(str(ROOT/'research/trame_poc0/results/reconstruction_errors.png'),width=CW,height=CW*.365),para('Figure : moyenne et corps extrêmes sur la même période de développement. Axe vertical logarithmique. Reconstruction de données connues, sans prévision. Source : calculs TRAME à partir de Binance Vision.','small')]);i+=1;continue
        if s.startswith('<!--'):i+=1;continue
        if s.startswith('```'):
            flush();code=[];i+=1
            while i<len(lines) and not lines[i].strip().startswith('```'):code.append(lines[i]);i+=1
            for row in code:flow.append(para(row or ' ','code'))
            i+=1;continue
        if s.startswith('|'):
            flush();table=[]
            while i<len(lines) and lines[i].strip().startswith('|'):table.append(lines[i]);i+=1
            flow.extend(make_table(table));continue
        m=re.match(r'^(#{1,5})\s+(.+)',s)
        if m:
            flush()
            if number=='02' and m[2].startswith('3.5') and not added_figure:
                flow.extend([candles_figure(),para('Illustration documentaire : les formes proches masquent une erreur de clôture de 4,34 points de base. Source réelle attribuée à Binance Vision ; transformation décrite dans le texte.','small')]);added_figure=True
            flow.append(para(m[2],'title' if len(m[1])==1 else 'h2' if len(m[1])==2 else 'h3'))
            if number=='01' and len(m[1])==1:flow.append(pipeline_figure())
            i+=1;continue
        if s in ('---','***'):flush();flow.append(Spacer(1,5));i+=1;continue
        m=re.match(r'^([-*]|\d+\.)\s+(.+)',s)
        if m:
            flush();prefix='•' if m[1] in ('-','*') else m[1]
            flow.append(para(prefix+' '+m[2],'bullet'));i+=1;continue
        if s.startswith('>'):flush();flow.append(para(s.lstrip('> ')));i+=1;continue
        buf.append(s);i+=1
    flush();return flow

def decoration(label):
    def draw(c,doc):
        c.saveState();c.setFont('Body',8);c.setFillColor(colors.HexColor('#56616C'))
        c.drawString(M,H-28,'TRAME  /  RECHERCHE SCIENTIFIQUE  /  VERSION 2')
        c.drawRightString(W-M,H-28,'14 OCTOBRE 2026')
        c.setStrokeColor(colors.HexColor('#D6DDE3'));c.setLineWidth(.5);c.line(M,35,W-M,35)
        c.drawString(M,22,label);c.drawRightString(W-M,22,str(doc.page));c.restoreState()
    return draw

names={
 '00':'Synthèse accessible',
 '01':'Papier de recherche',
 '02':'Atlas des langages',
 '03':'Faisabilité technique',
 '04':'Tutoriel du POC au système',
 '05':'Validation et panel critique',
 '06':"État de l'art et sources",
 '07':"Premières mesures réelles",
 '08':"Marché latent et GPT",
}
manifest=[]
for file in sorted(SRC.glob('0[0-8]_*.md')):
    number=file.name[:2];out=OUT/('TRAME_'+file.stem+'.pdf')
    text=file.read_text(encoding='utf-8')
    doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=49,bottomMargin=49,title=names[number],author='Codex - projet TRAME',pageCompression=1)
    doc.build(md_flow(text,number),onFirstPage=decoration(names[number]),onLaterPages=decoration(names[number]))
    reader=PdfReader(out)
    manifest.append({'number':number,'name':names[number],'source':str(file),'pdf':str(out),'pages':len(reader.pages),'words':len(text.split()),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
    print(number,len(reader.pages),out.name)

cover=ROOT/'tmp/pdfs/index_integral.pdf'
flow=[para('TRAME','title'),para('Langages des marchés et prévision des prix','h2'),para('Version scientifique 2 - 14 octobre 2026. Modèles GPT, plusieurs familles d’actifs, état latent commun et effets d’échelle.'),pipeline_figure(),para('Parcours de lecture','h2'),para('Commencer par la synthèse, puis le document 08 pour le Marché latent et le GPT. L’atlas 02 traite les langages ; le rapport 07 distingue les mesures réelles des hypothèses encore ouvertes.')]
offset=1
for e in manifest:
    e['combined_start_page']=offset+1
    flow.append(para(f"**{e['number']}  {e['name']}** - page {offset+1} ; {e['pages']} pages",'body'));offset+=e['pages']
flow.extend([Spacer(1,6),para('État des preuves','h2'),para('Bibliographie, théorie, audit de deux sources réelles et comparaison de cinq encodages réalisés. Aucun modèle prédictif entraîné. Le corpus général multi-marchés et les expériences de passage à l’échelle restent à constituer.'),para('Panel humain simulé ; relectures entre agents logiciels identifiées. Version précédente archivée. Les propositions restent révisables.','small')])
doc=SimpleDocTemplate(str(cover),pagesize=A4,rightMargin=M,leftMargin=M,topMargin=49,bottomMargin=49,title='TRAME Dossier complet',author='Codex')
doc.build(flow,onFirstPage=decoration('Guide de lecture'),onLaterPages=decoration('Guide de lecture'))
assert len(PdfReader(cover).pages)==1,'Index overflow'
writer=PdfWriter();writer.append(str(cover));offset=1
for e in manifest:
    writer.append(e['pdf']);writer.add_outline_item(e['number']+' '+e['name'],offset);offset+=e['pages']
writer.add_metadata({'/Title':'TRAME Dossier scientifique version 2','/Author':'Codex','/Subject':'GPT, marché latent, langages et prévision des prix - recherche et premières mesures'})
out=OUT/'TRAME_Dossier_complet.pdf'
with out.open('wb') as f:writer.write(f)
(ROOT/'tmp/pdfs/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',offset,'PAGES',sum(e['words'] for e in manifest),'WORDS')
