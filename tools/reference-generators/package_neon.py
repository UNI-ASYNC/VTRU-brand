from social_common import *
from PIL import Image,ImageFont,ImageDraw
from reportlab.pdfgen import canvas
from collections import Counter
import csv,shutil,zipfile

PREVIEW=ROOT/'08-Previews';PREVIEW.mkdir(exist_ok=True)
records=json.loads((ROOT.parent/'neon-ecosystem-records.json').read_text())+json.loads((ROOT.parent/'neon-single-records.json').read_text())
FREG=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
FBOLD=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',34)
collections=list(dict.fromkeys(r['collection'] for r in records))
sheets=[]
for collection in collections:
    rs=[r for r in records if r['collection']==collection]
    rows=math.ceil(len(rs)/3);cw,ch=580,440
    im=Image.new('RGB',(1800,rows*ch+140),'#E7ECF2');d=ImageDraw.Draw(im)
    title=collection[3:].replace('-',' ')
    d.text((30,30),title,font=FBOLD,fill='#111D32')
    for i,r in enumerate(rs):
        p=ROOT/r['png_path'];a=Image.open(p).convert('RGBA');a.thumbnail((cw-18,ch-60))
        x=30+(i%3)*cw;y=115+(i//3)*ch
        d.rectangle((x,y,x+cw-20,y+ch-55),fill='#081627')
        im.paste(a,(x+(cw-20-a.width)//2,y+(ch-55-a.height)//2),a)
        label=Path(r['png_path']).stem
        while FREG.getlength(label)>cw-30:label=label[:-2]
        d.text((x,y+ch-44),label,font=FREG,fill='#26384F')
    out=PREVIEW/(collection+'-contact-sheet.jpg');im.save(out,quality=92)
    sheets.append(out)

# Show the actual phone/desktop-safe center region alongside the full YouTube canvas.
for collection in collections[:2]:
    p=ROOT/collection/'YouTube/youtube-channel-banner.png'
    with Image.open(p) as im:
        im.crop((508,509,2052,931)).save(PREVIEW/(collection+'-youtube-center-preview.png'))

pdf=PREVIEW/'Neon-Social-Banners-Preview.pdf'
c=canvas.Canvas(str(pdf),pagesize=(900,1140));c.setTitle('Vitruveo Ecosystem / Neon Social Banners')
def draw_image(p,x,y,w,h):
    with Image.open(p) as im:iw,ih=im.size
    s=min(w/iw,h/ih);dw,dh=iw*s,ih*s
    c.drawImage(str(p),x+(w-dw)/2,y+(h-dh)/2,width=dw,height=dh,mask='auto')
def footer(n):
    c.setFillColorRGB(.3,.37,.47);c.setFont('Helvetica',10)
    c.drawString(28,25,'NEON SOCIAL BANNERS / ORIGINAL ZIP LOGOS');c.drawRightString(870,25,str(n))
def newpage(n):
    c.setFillColorRGB(.94,.96,.98);c.rect(0,0,900,1140,fill=1,stroke=0);footer(n)
newpage(1)
c.setFont('Helvetica-Bold',29);c.setFillColorRGB(.05,.10,.18);c.drawString(35,1060,'Your actual brands. Across every format.')
c.setFont('Helvetica',14);c.drawString(35,1026,'Facebook / X / YouTube / TikTok / Instagram / Rumble')
draw_image(ROOT/collections[0]/'Master/reference-wide-master.png',30,590,840,400)
c.setFont('Helvetica',13);c.drawString(35,570,'Four-brand version, following your supplied reference.')
draw_image(ROOT/collections[1]/'Master/reference-wide-master.png',30,100,840,400)
c.drawString(35,80,'Five-brand alternative includes VTRU Scope. Individual-brand sets are also included.')
c.showPage()
for n,p in enumerate(sheets,2):
    newpage(n);draw_image(p,25,55,850,1050);c.showPage()
newpage(9)
c.setFont('Helvetica-Bold',25);c.setFillColorRGB(.05,.10,.18);c.drawString(35,1060,'YouTube / center crop previews')
c.setFont('Helvetica',13);c.drawString(35,1025,'Critical content is within the centered 1544 x 422 production safe area.')
for i,collection in enumerate(collections[:2]):
    draw_image(PREVIEW/(collection+'-youtube-center-preview.png'),30,610-i*430,840,300)
    c.drawString(35,590-i*430,collection[3:].replace('-',' '))
c.showPage();c.save()

fontdir=GUIDE/'Template-Fonts';fontdir.mkdir(exist_ok=True)
for name in ['DejaVuSans.ttf','DejaVuSans-Bold.ttf','DejaVuSans-Oblique.ttf','DejaVuSans-BoldOblique.ttf']:
    shutil.copy2(Path('/usr/share/fonts/truetype/dejavu')/name,fontdir/name)
shutil.copy2('/usr/share/doc/fonts-dejavu-core/copyright',fontdir/'Font-License.txt')
for src in ['social-platform-specs.json','neon-single-qc.json','neon-independent-qa.json']:
    if (ROOT.parent/src).exists():shutil.copy2(ROOT.parent/src,GUIDE/src)

rows=['| Platform / surface | PNG dimensions |','|---|---:|']
for s in SPECS:rows.append(f'| {s["platform"]} — {s["surface"]} | {s["w"]} × {s["h"]} |')
readme='''# Neon Social Banner Pack

This set uses the exact brand artwork from your five supplied ZIP files. The Vitruveo, Pretrend, AI Wars, Vertical Foundation and VTRU Scope logo SVG bytes are embedded directly in the editable masters. Logo geometry, colors and lettering remain as supplied. The blue/purple/green atmospheric backgrounds are newly generated decorative art.

## Use the files

- Upload the PNG in the relevant platform folder.
- For editing, extract the entire ZIP and keep its folder structure. SVGs refer to the two shared background images in `00-Guide-and-Audit/Backgrounds/`; the original logos are embedded inside the SVGs. Template fonts and their license are included. Re-export a PNG after editing an SVG.
- `01-Ecosystem-Four-Brands` follows your example: Vitruveo, Pretrend, AI Wars and Vertical Foundation, with the example's “AI Blockchain”, “powered by” and “Now Featuring” copy.
- `02-Ecosystem-Five-Brands` adds VTRU Scope. Folders 03–07 contain each brand separately.
- The two `Master/reference-wide-master` designs are wide reference compositions at 2400 × 800.
- See `08-Previews/Neon-Social-Banners-Preview.pdf` for all designs and the YouTube center-crop previews.

## Sizes

'''+ '\n'.join(rows)+'''

Instagram and TikTok files are content covers/feed/Story formats. They are not channel-header upload slots. On those services, select the image as an appropriate content cover or publish it in the corresponding post/Story format.

YouTube's full canvas is deliberately spacious: important logos and text sit in the centered 1544 × 422 production safe area for the narrow desktop/mobile crop. X keeps important content at least 60 px from the top and bottom and away from the lower-left profile area. Rumble exports are 3600 × 600 and below 2 MB. Platform UI crops can vary by account and device; check the upload preview before publishing. Facebook and Instagram sizes are production targets; their official documentation was access-blocked during this pass. Evidence and source URLs are recorded in `00-Guide-and-Audit/social-platform-specs.json`.

## Original artwork verification

The asset manifest maps each output master and PNG export to the exact supplied source filename and SHA-256. All embedded logo images were checked against extracted ZIP contents. No logo was redrawn or generated. All upload PNGs use the same matched layouts. For sharper raster output, VTRU Scope's PNG exports use its untouched supplied 2400 px PNG logo at the identical layout position; the editable masters retain the supplied SVG. Both source hashes are recorded. Background art and framing are new derivatives. The packet includes 79 compositions, each in PNG + editable SVG, plus previews and audit documentation. Original ZIP archives and standalone unchanged logo masters are excluded.
'''
(ROOT/'START-HERE.md').write_text(readme)

manifest=[]
for r in records:
    for key in ['path','png_path']:
        p=ROOT/r[key];row=dict(r);row['file']=str(p.relative_to(ROOT));row['sha256']=sha(p);row['bytes']=p.stat().st_size;row['type']=p.suffix[1:]
        if key=='path':row.pop('png_source_override',None)
        elif row.get('png_source_override'):row['sources']=row['sources']+[row['png_source_override']]
        manifest.append(row)
(GUIDE/'asset-manifest.json').write_text(json.dumps(dict(designs=len(records),production_files=len(manifest),files=manifest),indent=2))
fields=['file','collection','platform','surface','width','height','type','bytes','sha256']
with (GUIDE/'asset-manifest.csv').open('w') as f:
    w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(manifest)
summary=dict(compositions=len(records),pngs=len(records),editable_svgs=len(records),collections=len(collections),platforms=['Facebook','X','YouTube','TikTok','Instagram','Rumble'],preview_pages=9,original_logo_source_match='passed',counts=dict(Counter(r['platform'] for r in records)),backgrounds='new generated decorative art without logos',all_logo_artwork='exact SVGs from user supplied brand ZIPs')
(GUIDE/'export-summary.json').write_text(json.dumps(summary,indent=2))
files=[p for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!='sha256sums.txt']
(GUIDE/'sha256sums.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(ROOT)}' for p in files)+'\n')
archive=ROOT.parent/'Vitruveo-Neon-Social-Banners.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():z.write(p,Path('Vitruveo-Neon-Social-Banners')/p.relative_to(ROOT))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps(dict(zip=str(archive),bytes=archive.stat().st_size,files=len(files)+1,designs=len(records),preview=str(pdf)),indent=2))
