import json,shutil,hashlib,csv,io,zipfile,math
from pathlib import Path
from collections import Counter
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from brand_common import *

PREV=ROOT/'07-Previews-and-Contact-Sheets';AUDIT=ROOT/'08-Manifests-and-Export-Checks'
PREV.mkdir(exist_ok=True);AUDIT.mkdir(exist_ok=True)
REG=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
BOLD=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',35)
def sheet(files,title,out,cols=3,cell=(500,370)):
    cw,ch=cell;rows=math.ceil(len(files)/cols)
    img=Image.new('RGB',(cols*cw+60,rows*ch+145),'#EEF0F4');d=ImageDraw.Draw(img)
    d.text((30,30),title,font=BOLD,fill='#171C28')
    for i,p in enumerate(files):
        x=30+i%cols*cw;y=115+i//cols*ch
        im=Image.open(p).convert('RGBA');im.thumbnail((cw-30,ch-60))
        xx=x+(cw-30-im.width)//2
        d.rectangle((x-2,y-2,x+cw-24,y+ch-53),fill='white')
        img.paste(im,(xx,y+(ch-60-im.height)//2),im)
        label=p.stem
        for b in BRANDS:label=label.replace(b['id']+'-','')
        label=label.replace('letterhead-','').replace('-A4','').replace('emoji-','').replace('sticker-','')
        while REG.getlength(label)>cw-30:label=label[:-2]
        d.text((x,y+ch-44),label,font=REG,fill='#354257')
    img.save(out,optimize=True)
    return out

preview_paths=[]
for b in BRANDS:
    base=ROOT/b['folder'];f=[]
    for n in ['x-banner','facebook-cover','linkedin-company','linkedin-personal','discord-server','website-hero','social-square','social-landscape','story-vertical']:
        f.append(base/'Social-Banners'/f'{b["id"]}-{n}.png')
    f+=sorted((base/'Announcement-Templates').glob('*.png'))+sorted((base/'Profile-Images').glob('*.png'))+sorted((base/'Document-Headers').glob('*.png'))
    preview_paths.append(sheet(f,b['name']+' / Social & editorial',PREV/f'{b["id"]}-social-contact-sheet.png'))
    f=sorted((base/'Emojis').glob('*.png'))+sorted((base/'Stickers').glob('*.png'))
    preview_paths.append(sheet(f,b['name']+' / Discord',PREV/f'{b["id"]}-discord-contact-sheet.png',cols=5,cell=(300,390)))
    f=sorted((base/'Letterheads').glob('*.png'))
    preview_paths.append(sheet(f,b['name']+' / Letterheads',PREV/f'{b["id"]}-letterheads-contact-sheet.png',cols=3,cell=(500,720)))
preview_paths.append(sheet(sorted((ROOT/'06-Ecosystem-Wide').glob('*/*.png')),'Ecosystem / Multi-brand collection',PREV/'ecosystem-contact-sheet.png',cols=2,cell=(750,550)))

pdf=PREV/'Complete-Preview-Book.pdf'
c=canvas.Canvas(str(pdf),pagesize=(900,1160));c.setTitle('Vitruveo Ecosystem — Complete Preview Book')
identity=ROOT/'00-Brand-Guide-and-Audit'/'Five-Brand-Identity-Sheet.png'
for i,p in enumerate([identity]+preview_paths):
    im=Image.open(p);w,h=im.size;scale=min(850/w,1080/h);dw,dh=w*scale,h*scale
    c.setFillColorRGB(.95,.96,.98);c.rect(0,0,900,1160,fill=1,stroke=0)
    c.drawImage(str(p),(900-dw)/2,60+(1080-dh)/2,width=dw,height=dh,mask='auto')
    c.setFont('Helvetica',10);c.setFillColorRGB(.3,.35,.4)
    c.drawString(25,25,'VITRUVEO ECOSYSTEM / PRODUCTION PREVIEW');c.drawRightString(875,25,str(i+1))
    c.showPage()
c.save()

for source in ['source-inventory.csv','source-audit.json','independent-qa.json','letterhead-qc.json']:
    shutil.copy2(BASE/source,AUDIT/source)

fontdir=ROOT/'00-Brand-Guide-and-Audit'/'Template-Fonts';fontdir.mkdir(exist_ok=True)
for name in ['DejaVuSans.ttf','DejaVuSans-Bold.ttf']:
    shutil.copy2(Path('/usr/share/fonts/truetype/dejavu')/name,fontdir/name)
license=Path('/usr/share/doc/fonts-dejavu-core/copyright')
if license.exists():shutil.copy2(license,fontdir/'DejaVu-Font-License.txt')

readme='''# Vitruveo Ecosystem — Brand System

Built from the five supplied brand kits. The protected marks retain the supplied geometry, colors, proportions and lettering. Layout graphics and editorial copy are new proposals.

## Start here

1. Review `00-Brand-Guide-and-Audit/Five-Brand-Identity-Sheet.pdf` and `07-Previews-and-Contact-Sheets/Complete-Preview-Book.pdf`.
2. Open the brand folder and choose a PNG for direct use, or its SVG master for editing. Embedded logos are self-contained; avoid ungrouping, recoloring or stretching them. Template text uses DejaVu Sans; the regular and bold fonts and license are included.
3. Edit bracketed text in the announcement/header masters and DOCX stationery. Sample social slogans are proposals; review copy before publishing. Re-export after editing. PNG/PDF exports are flattened presentation files; SVG and DOCX are the editable masters.
4. Upload Discord PNGs. Emoji names should use each file's semantic suffix; stickers need their description and associated emoji set in Discord. The stickers are static PNGs.
5. Check the crop in the target account before publishing. Hidden crop guides in social SVGs are internal layout guides, not a platform guarantee. All sizes are documented production targets; no live account upload was performed.

## Inventory

- 50 distinct static emojis: 10 per brand, 128 × 128 PNG + SVG.
- 20 distinct static stickers: four per brand, 320 × 320 PNG + SVG.
- 15 letterhead layouts: formal, office and technical for each brand, in DOCX, SVG, PDF and 300 dpi PNG.
- 45 social/cover/hero layouts: nine per brand, PNG + SVG.
- 15 announcement templates, 15 avatar compositions and 10 document headers, PNG + SVG.
- Five ecosystem layouts: a new four-brand banner, two five-brand compositions and two announcement templates, PNG + SVG.
- Identity sheet, brand guide, complete preview book, contact sheets, source audit and export/provenance manifests.

The original four-brand banner was not supplied. The four-brand output is a new composition using Vitruveo, Pretrend, AI Wars and Vertical Foundation. VTRU Scope appears in the separate five-brand collection.

## Documents and printing

Letterhead PDFs are blank A4 RGB vector masters without bleed; PNGs are 2480 × 3508 at 300 dpi. Confirm a printer's color and PDF requirements before a commercial run. DOCX files use real repeating headers/footers and editable contact fields. DOCX package structure was checked; its final appearance can vary by word processor and was not rendered in Word/LibreOffice in this environment. PDF/SVG/PNG layouts were visually checked.

## Audit and review status

Every production SVG embeds byte-matched source artwork. DOCX files use byte-matched supplied source PNGs. The manifest maps outputs to source hashes; raster exports derive from the matching masters. Production layouts are derivative artwork and require owner editorial/design review. Source matching is not legal ownership verification or brand-owner sign-off. The source ZIPs and standalone unchanged logo masters are intentionally excluded.

`08-Manifests-and-Export-Checks/asset-manifest.json` contains dimensions, file hashes and provenance; `sha256sums.txt` covers every package file except itself. The audit reports describe their check scope and limits.
'''
(ROOT/'START-HERE.md').write_text(readme)

records=[]
for name in ['visual-records.json','discord-records.json','letterhead-records.json']:
    records+=json.loads((BASE/name).read_text())
mapping={r['path']:r for r in records}
all_sources=[dict(file=p.name,sha256=sha(p)) for p in SOURCE.glob('*/*.svg')]
items=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or p.parent==AUDIT and p.name in ['asset-manifest.json','asset-manifest.csv','sha256sums.txt','Export-Summary.json']:continue
    rel=str(p.relative_to(ROOT));r=dict(mapping.get(rel,{}))
    r.update(path=rel,bytes=p.stat().st_size,sha256=sha(p),extension=p.suffix[1:])
    if p.suffix=='.png':
        with Image.open(p) as im:r.update(width=im.width,height=im.height,mode=im.mode)
    if not r.get('classification'):
        r['classification']='documentation / audit / preview' if 'Template-Fonts' not in rel else 'bundled template font'
    if rel.startswith('07-') or p.name=='Brand-System-Guide.pdf':
        r['provenance']='composite preview / documentation built from production designs and supplied marks'
        r['source_artwork_note']='See production source mappings and source-inventory.csv'
    items.append(r)
(AUDIT/'asset-manifest.json').write_text(json.dumps(dict(schema_version=1,source_archive_count=5,source_asset_count=70,production_output_count=len(records),files=items,review_status='source matching passed; layouts and proposed copy require owner editorial review'),indent=2))
fields=['path','brand','category','extension','width','height','bytes','sha256','source_file','source_sha256','classification','owner_review']
with (AUDIT/'asset-manifest.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(items)
summary=dict(production_outputs=len(records),production_designs=176,production_counts=dict(Counter(r['category'] for r in records)),source_files=70,source_archives=5,emoji_pngs=50,sticker_pngs=20,letterhead_layouts=15,social_layouts=45,announcement_templates=15,avatar_compositions=15,document_headers=10,ecosystem_layouts=5,preview_book_pages=17,source_mark_check='all SVG embeddings match source bytes',limitations=['DOCX visual rendering not performed; structural checks passed','Live platform crop/upload not performed','RGB PDF without bleed, not certified PDF/X','Proposed slogans and supporting colors require owner editorial review'])
(AUDIT/'Export-Summary.json').write_text(json.dumps(summary,indent=2))
lines=[f'{sha(p)}  {p.relative_to(ROOT)}' for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='sha256sums.txt']
(AUDIT/'sha256sums.txt').write_text('\n'.join(lines)+'\n')
archive=BASE/'Vitruveo-Ecosystem-Brand-System.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():z.write(p,Path('Vitruveo-Ecosystem-Brand-System')/p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert not any(n.endswith('.zip') for n in z.namelist())
print(json.dumps(dict(archive=str(archive),bytes=archive.stat().st_size,files=len(lines)+1,production_outputs=len(records),preview_pages=17),indent=2))
