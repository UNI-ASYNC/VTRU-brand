"""Build V2 neutral A4 stationery without changing any V1 file."""
from pathlib import Path
import base64
import importlib.util
import json
import sys
import xml.etree.ElementTree as ET
import zipfile

from PIL import Image
from docx import Document
import fitz

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from v2_common import BRANDS,V2,SOURCE,logo,source_path,sha,render,esc,text

REFERENCE=HERE/'reference-generators'/'make_letterheads.py'
sys.path.insert(0,str(REFERENCE.parent))
spec=importlib.util.spec_from_file_location('v1_letterhead_reference',REFERENCE)
ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
ref.SOURCE=SOURCE
ref.INK='#111111';ref.MUTED='#555555';ref.LINE='#D0D0D0'

PW,PH=595.2756,841.8898
M=50
STYLES=['formal','office','technical']

def line(x1,y,x2,color='#D0D0D0',width=.7):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="{width}"/>'

def put_logo(b,x,y,maxw,maxh,center=False):
    with Image.open(source_path(b,'logo','png')) as im:r=im.width/im.height
    w=min(maxw,maxh*r);h=w/r
    if center:x-=w/2
    return logo(b,x,y,w,h,'logo')

def make_svg(b,style):
    right=PW-M
    body='<rect x="0" y="0" width="595.2756" height="841.8898" fill="#FFFFFF"/>'
    body+='<g id="client-content"><desc>Blank area reserved for correspondence.</desc></g>'
    if style=='formal':
        body+=put_logo(b,M,46,177,64)+line(M,140,right)
        body+=line(M,780,right)+text(M,799,b['name'],7.7,600)
        body+=text(right,799,'[Email]  |  [Website]',8,anchor='end',fill='#555555')
    elif style=='office':
        body+=put_logo(b,PW/2,42,185,68,True)+line(M+70,140,right-70)
        body+=line(M+70,780,right-70)+text(PW/2,799,'[Email]  |  [Website]',8.4,anchor='middle',fill='#555555')
    else:
        body+=put_logo(b,M,45,167,64)
        body+=text(right,53,'[Document title]',7.3,600,'end')
        body+=text(right,72,'[Document reference]',8.3,anchor='end',fill='#555555')
        body+=line(M,136,right,'#555555',1)+line(M,780,right)
        body+=text(M,799,'[Email]  |  [Website]',8,fill='#555555')
        body+=text(right,799,'[Revision]  |  [Page]',8,anchor='end',fill='#555555')
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="210mm" height="297mm" viewBox="0 0 {PW} {PH}"><title>{esc(b["name"])} — {style} A4 letterhead, V2 source-only</title>{body}</svg>'

def make_docx(b,style,path):
    # Reuse the original document mechanics, with neutral rules and no decorative bar.
    ref.make_docx(b['id'],b['name'],'#555555',style,path)
    doc=Document(path)
    ns='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    for part in [doc.element]+[s.header._element for s in doc.sections]+[s.footer._element for s in doc.sections]:
        for el in part.iter(ns+'t'):
            if el.text=='━━━━':el.text=''
            elif el.text=='TECHNICAL CORRESPONDENCE':el.text='[Document title]'
            elif el.text==b['name'].upper():el.text=b['name']
    doc.core_properties.title=f'{b["name"]} — {style.title()} A4 letterhead, V2'
    doc.core_properties.subject='Neutral editable correspondence template with unchanged supplied brand artwork'
    doc.core_properties.keywords='V2, A4, source-only, editable letterhead'
    doc.save(path)

def main():
    records=[];qc={'checked_on':'2026-11-14','sets':15,'errors':[],'docx_visual_rendering':'Not performed; package/header/footer/media structure checked.','pdf':'A4 RGB print master, no bleed; source marks unchanged. Scope PDF/PNG render uses its untouched supplied high-resolution PNG; SVG retains original SVG.','checks':[]}
    for b in BRANDS:
        dest=V2/'supplemental'/b['id']/'Letterheads';dest.mkdir(parents=True,exist_ok=True)
        for style in STYLES:
            stem=f'{b["id"]}-letterhead-{style}-A4'
            svg=dest/(stem+'.svg');svg.write_text(make_svg(b,style))
            render(svg,pdf=True,dpi=300)
            png=svg.with_suffix('.png');pdf=svg.with_suffix('.pdf');docx=svg.with_suffix('.docx')
            make_docx(b,style,docx)
            with Image.open(png) as im:
                assert im.size==(2480,3508),(png,im.size)
                png_size=im.size
                # Inkscape writes 300dpi metadata; readback is recorded rather than assumed.
                dpi=im.info.get('dpi')
            with fitz.open(pdf) as d:
                assert len(d)==1
                page=d[0];assert abs(page.rect.width-PW)<.1 and abs(page.rect.height-PH)<.1
            svgroot=ET.parse(svg).getroot()
            source_data=[]
            for el in svgroot.iter():
                uri=el.get('{http://www.w3.org/1999/xlink}href','')
                if uri.startswith('data:image/svg+xml;base64,'):source_data.append(base64.b64decode(uri.split(',',1)[1]))
            assert len(source_data)==1 and source_data[0]==source_path(b).read_bytes()
            with zipfile.ZipFile(docx) as z:
                assert z.testzip() is None
                assert any(n.startswith('word/header') for n in z.namelist())
                assert any(n.startswith('word/footer') for n in z.namelist())
                media=[z.read(n) for n in z.namelist() if n.startswith('word/media/')]
                assert source_path(b,'logo','png').read_bytes() in media
            for p in [svg,png,pdf,docx]:
                raster_source=p.suffix=='.docx' or (b['id']=='vtruscope' and p.suffix in ['.png','.pdf'])
                s=source_path(b,'logo','png' if raster_source else 'svg')
                row={'path':str(p.relative_to(V2)),'brand':b['id'],'category':'letterhead','layout':style,'paper':'A4','extension':p.suffix[1:],'source_file':s.name,'source_sha256':sha(s),'classification':'V2 source-only neutral template','imagery':'unchanged supplied logo only','copy':'functional editable document/contact placeholders only','status':'white page and neutral functional rules; no invented imagery, slogans or marketing copy'}
                if p.suffix=='.png':row.update(width=png_size[0],height=png_size[1],dpi=list(dpi) if dpi else None)
                if b['id']=='vtruscope' and p.suffix in ['.png','.pdf']:row['paired_source_note']='Same logo and coordinates as SVG master, rendered from exact supplied 2400px PNG for sharpness.'
                if p.suffix=='.docx':row['visual_limit']='Structural/source checks passed; not rendered in Word/LibreOffice.'
                records.append(row)
            qc['checks'].append({'brand':b['id'],'layout':style,'svg_source_exact':True,'docx_source_exact':True,'pdf_pages':1,'A4':True,'png_size':list(png_size),'headers_footers':True})
        (dest/'README.md').write_text(f'''# {b['name']} — V2 A4 letterheads\n\nThree neutral layouts: formal, office and technical. Each has an editable DOCX, a source-preserving SVG, an A4 RGB PDF without bleed, and a 2480 × 3508 PNG at300dpi. The writing area is intentionally blank.\n\nThe full-color supplied logo is unchanged. Header/footer rules are functional neutral gray; there are no added illustrations, decorative motifs or marketing slogans. Bracketed contact and document fields are editable placeholders. Double-click the DOCX header/footer to edit them. The technical DOCX includes a real PAGE field.\n\nTemplate text uses DejaVu Sans as a neutral editable font, not a claimed official brand font. DOCX header/footer structure and original source-image bytes were checked; visual rendering in Word/LibreOffice was not performed. PDFs and PNGs are the visual layout reference.\n\nFor VTRU Scope, the SVG embeds the supplied source SVG; PDF and PNG exports use the untouched paired high-resolution source PNG at the same position for clarity.\n''')
        print('Created',b['name'],'letterheads',flush=True)
    (V2/'reports/letterhead-records.json').write_text(json.dumps(records,indent=2))
    qc['status']='PASS';(V2/'reports/letterhead-qc.json').write_text(json.dumps(qc,indent=2))
    print('Created',len(records),'assets; allchecks passed',flush=True)

if __name__=='__main__':main()
