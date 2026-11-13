from pathlib import Path
import sys,json,html
sys.path.insert(0,'/workspace/work/scripts')
from brand_common import BRANDS,SOURCE,ROOT
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether,Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from PIL import Image

OUT=ROOT/'00-Brand-Guide-and-Audit';OUT.mkdir(parents=True,exist_ok=True)
audit=json.loads(Path('/workspace/work/source-audit.json').read_text())
roles={'vitruveo':'Network and infrastructure identity','verticalfoundation':'Foundation and community identity','pretrend':'Trend and prediction identity','aiwars':'Gaming and competition identity','vtruscope':'Ecosystem discovery and intelligence identity'}
source_swatch={
'vitruveo':[('#FF00FF','Gradient stop'),('#00FFFF','Gradient stop'),('#000000','Primary lettering')],
'verticalfoundation':[('#C2D3C7','Architecture'),('#949F9C','Architecture'),('#7C8280','Architecture'),('#D5E2D8','Architecture'),('#B5A88C','Lettering')],
'pretrend':[('#7ABE4D','Gradient endpoint'),('#0057D6','Gradient endpoint'),('#0B82BE','Gradient endpoint'),('#A5D03F','Gradient endpoint'),('#000000','Lettering')],
'aiwars':[('#060B14','Primary lettering'),('#0B5CFF','Slash accent')],
'vtruscope':[('#FF00FF','Gradient stop'),('#00FFFF','Gradient stop'),('#000000','Primary lettering'),('#FFFFFF','Target detail')]
}

md='''# Vitruveo ecosystem brand system\n\nProduction edition 1.0 · prepared 13 November 2026\n\nA coordinated set of layouts built around five distinct, user-supplied brand identities. The supplied ZIP artwork is the source of truth for the marks. The visual system adds typography, spacing, backgrounds, and communication templates; those additions are production recommendations, not pre-existing official brand standards.\n\n## Review status\n\nThe source audit passed. All supplied artwork is source-matched to the uploaded archives, and the package contains new derivative layouts. Editorial and brand-owner approval has not been asserted. Review proposed headlines, layout choices, and placeholders before publication. No legal ownership certification is provided.\n\n## Five brand families\n\n'''
for b in BRANDS:
    md+=f"### {b['name']}\n\nRole used in this system: {roles[b['id']]}. These role labels are based on the supplied plan and are descriptive.\n\nSource family: `{b['id']}-*.svg` and matching PNG files in `{b['id']}-brandkit.zip`. Full logo for named communications; supplied logomark for compact identity where available.\n\n"
    md+='Source-derived colors (rounded sRGB): '+', '.join(f'`{h}` {label.lower()}' for h,label in source_swatch[b['id']])+'.\n\n'
    md+=f"Proposed template colors: accent `{b['accent']}`, secondary `{b['secondary']}`, dark ink `{b['ink']}`, pale field `{b['pale']}`. These colors support the new layouts; they do not recolor the protected logo.\n\n"
md+='''## Artwork rules\n\n- Embed the exact supplied SVG or PNG. Keep paths, gradients, lettering, transparent negative spaces, and the original aspect ratio.\n- Scale uniformly. Do not stretch, rotate, redraw, recolor, outline, add effects to, or crop the mark. Decorative lines, charts, and status glyphs remain separate from it.\n- Start with clear space equal to at least one quarter of the visible logo height, then increase it where composition allows. This is a proposed layout rule, not a source-defined official requirement.\n- Use the primary full-color source on a light field. Use a supplied white variant on a dark field. A filename alone does not establish contrast suitability: inspect its rendered appearance.\n- Keep the entire mark inside a crop-safe area. Profile files use padded 1024-square canvases; check the actual circular crop and upload preview in the destination account.\n- New emoji symbols and sticker illustrations are supporting artwork. They must never be presented as replacement brand logos.\n\n### Important source quirks\n\nAI Wars has no separate compact icon in these archives. Its file named `aiwars-logomark.svg` is the full wordmark, with the same geometry and viewBox as its primary logo. Its circle and square variants place that wordmark in a square viewport; preserve it rather than inventing a letter symbol.\n\nVertical Foundation is taller than the other wordmarks, approximately 1.59:1. The full logo includes the name beneath the architecture; the separate logomark omits that name. Allocate enough height. Its `logo-dark.svg` is byte-identical to the primary logo; choose `logo-white.svg` when a white lockup is needed.\n\nVitruveo's circular symbol is built from six gradient-filled paths with transparent separators. Keep the original source geometry intact. Do not reconstruct a circle or fill its open spaces.\n\nAcross the source families, circle/square filenames describe viewports and spacing, not a guaranteed circular background. White SVG variants can contain unused gradient definitions; visible appearance, not a list of color tokens, determines how that variant looks.\n\n## Typography and layout\n\nDejaVu Sans is the proposed supporting typeface: bold for headlines, regular for body text and labels. It is independent of the outlined lettering in the logos, which remains unchanged. Use a clear title/body/metadata hierarchy and generous quiet space around the artwork. Font files are not bundled. If an editor lacks the font, substitute deliberately and review line breaks.\n\nEach brand retains its own source colors and visual character. The shared system contributes consistent margins, label sizes, modular cards, and export standards. Shared ecosystem pieces use a neutral composition with each source mark intact.\n\n## Asset formats and production targets\n\n| Asset | Production target | Use |\n| --- | --- | --- |\n| Emoji | 128 × 128 transparent PNG, below 256 KB | 10 distinct static expressions per brand |\n| Sticker | 320 × 320 transparent PNG, below 512 KB | 4 static expressions per brand |\n| Letterhead | A4 portrait, 210 × 297 mm | 3 layouts per brand: formal, office, technical |\n| Profile image | 1024 × 1024 PNG | Light, dark, and framed treatments |\n| X banner | 1500 × 500 PNG | Profile header |\n| Facebook cover | 1640 × 720 PNG | Cover production canvas |\n| LinkedIn company cover | 1512 × 256 PNG | Company header |\n| LinkedIn personal cover | 1584 × 396 PNG | Personal profile header |\n| Discord banner | 960 × 540 PNG | Server-banner canvas |\n| Website hero | 1920 × 640 PNG | Wide hero image |\n| Square social | 1080 × 1080 PNG | Square post |\n| Landscape social | 1200 × 630 PNG | Wide post |\n| Story | 1080 × 1920 PNG | Vertical post |\n\nThese are the package's production targets. They are not a claim that every platform's current requirements, mobile crop, or account-specific placement has been independently verified. Review the live destination preview before uploading.\n\nThe social collection contains nine compositions per brand, plus three announcement templates and two document headers per brand. Editable SVG masters accompany the graphics. Header dimensions are recorded in the export manifest.\n\n### Letterhead use\n\nEach design has an editable DOCX, an A4 PDF, and a blank high-resolution PNG at approximately 300 dpi. The writing area remains clear. The PDF is an RGB print master with no bleed; commercial printing may require printer-specific color conversion. Do not claim PDF/X certification or CMYK separation. The DOCX keeps contact fields editable. Replace bracketed placeholders such as `[Email]` and `[Website]`; do not invent legal addresses, staff titles, or ownership statements.\n\nThe DOCX is an editable office layout. Word processors can reflow text or substitute fonts; inspect its print preview before sending. Use the supplied PDF when fixed placement matters.\n\n### Social and announcement use\n\nEdit the SVG to update content, then export a fresh PNG at the recorded dimensions. The PNG is a fixed rendering. Keep important content away from expected profile-picture overlays and the edge of the frame. A wide composition and a vertical composition use different arrangements, so avoid making one from an automatic crop of another.\n\nProposed headlines and descriptors are sample copy, not verified product promises. Review them editorially before publication. Bracketed fields in announcement masters must be replaced. Never publish placeholder text as finished communication.\n\n## Ecosystem compositions\n\nThe original four-brand composition contains Vitruveo, Pretrend, AI Wars, and Vertical Foundation. VTRU Scope belongs in the separate five-brand ecosystem compositions. All five remain included in the complete package.\n\nNo previous promotional banner was supplied in this thread. The new four-brand banner is a fresh composition based on the actual source marks, rather than a pixel-specific correction of an unavailable original.\n\n## Verification and provenance\n\nFive archives supplied 70 assets: 35 SVGs and 35 PNGs, seven of each per brand. Archive CRC checks passed, all extracted-file hashes matched archive bytes, all SVGs parsed and rendered, and all PNGs decoded. No SVG script, event handler, foreignObject, or external reference was found.\n\nRendered SVGs were compared with their paired supplied PNGs at a 512-pixel width on white and dark fields. The largest mean absolute channel difference was 0.814 on a 0–255 scale, consistent with small rasterization differences. This numerical comparison supplements the source hash audit; it does not certify legal authorship or trademark rights.\n\n`08-Manifests-and-Export-Checks/source-inventory.csv` records every supplied filename, source archive, format, byte size, SHA-256 hash, dimensions or viewBox, and structural details. `source-audit.json` contains the full audit, gradient stops, source notes, and SVG/PNG comparisons. The export manifest links derivative files to the source artwork used and records export checks.\n\nA derivative layout combines exact supplied artwork with newly authored layout elements. A source match means the embedded artwork traces to those source bytes; it does not mean the complete derivative has received the brand owner's approval. The original ZIPs and unchanged standalone source artwork are not repackaged. Keep the uploaded originals as archival masters.\n\n## Working workflow\n\n1. Choose the brand folder and the destination format.\n2. Open an editable SVG or DOCX, replace placeholders, and review proposed copy.\n3. Preserve the embedded logo and its proportions; adjust only the supporting layout.\n4. Export at the manifest dimensions and check transparency, edge spacing, and text size.\n5. Preview the actual destination crop or print page, then publish the reviewed asset.\n6. Keep the edited master and the exported file together for future updates.\n\nThe package is a reusable production system with recorded source provenance. Owner review remains appropriate for editorial choices and final placement; it is not a statement of legal ownership.\n'''
(OUT/'Brand-System-Guide.md').write_text(md)

pdfmetrics.registerFont(TTFont('DVS','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVS-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
C=colors.HexColor
styles={
'kicker':ParagraphStyle('kicker',fontName='DVS-Bold',fontSize=8,leading=11,textColor=C('#7165BD'),spaceAfter=13),
'h1':ParagraphStyle('h1',fontName='DVS-Bold',fontSize=30,leading=36,textColor=C('#19162E'),spaceAfter=20),
'h2':ParagraphStyle('h2',fontName='DVS-Bold',fontSize=18,leading=23,textColor=C('#19162E'),spaceBefore=4,spaceAfter=13),
'h3':ParagraphStyle('h3',fontName='DVS-Bold',fontSize=12,leading=16,textColor=C('#19162E'),spaceBefore=13,spaceAfter=7),
'body':ParagraphStyle('body',fontName='DVS',fontSize=9.4,leading=14.8,textColor=C('#343745'),spaceAfter=10),
'small':ParagraphStyle('small',fontName='DVS',fontSize=7.6,leading=11.8,textColor=C('#5D6373'),spaceAfter=7),
'cell':ParagraphStyle('cell',fontName='DVS',fontSize=8.1,leading=12,textColor=C('#343745')),
'cellb':ParagraphStyle('cellb',fontName='DVS-Bold',fontSize=8.1,leading=12,textColor=C('#19162E'))
}
def p(t,s='body'):return Paragraph(t,styles[s])
def para(t,s='body'):story.append(p(t,s))
def table(rows,widths,header=True):
    content=[[p(str(c),'cellb' if header and i==0 else 'cell') for c in row] for i,row in enumerate(rows)]
    t=Table(content,colWidths=widths,hAlign='LEFT',repeatRows=1 if header else 0)
    rules=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.5,C('#D7DAE5'))]
    if header:rules+=[('BACKGROUND',(0,0),(-1,0),C('#F0EFF8'))]
    for i in range(1 if header else 0,len(rows)):
        if i%2==0:rules+=[('BACKGROUND',(0,i),(-1,i),C('#F7F8FA'))]
    t.setStyle(TableStyle(rules));story.append(t);story.append(Spacer(1,10))

def footer(c,doc):
    w,h=A4;c.saveState();c.setStrokeColor(C('#DBDDE7'));c.setLineWidth(.5);c.line(44,41,w-44,41)
    c.setFont('DVS',7);c.setFillColor(C('#6B7080'));c.drawString(44,27,'VITRUVEO ECOSYSTEM  /  BRAND SYSTEM 1.0');c.drawRightString(w-44,27,f'{doc.page:02d}')
    if doc.page>1:
        c.setFillColor(C('#7165BD'));c.rect(44,h-36,24,3,fill=1,stroke=0)
        c.setFont('DVS-Bold',7);c.setFillColor(C('#6B7080'));c.drawString(76,h-36,'PRODUCTION GUIDE  ·  SOURCE-MATCHED ARTWORK')
    c.restoreState()

pdfpath=OUT/'Brand-System-Guide.pdf'
doc=SimpleDocTemplate(str(pdfpath),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=55,bottomMargin=58,title='Vitruveo Ecosystem — Brand System Guide',author='Brand system production',subject='User-supplied source marks, derivative templates, production targets and audit')
story=[]
para('PRODUCTION EDITION 1.0  /  13 NOVEMBER 2026','kicker')
para('Five identities.<br/>One production system.','h1')
para('VITRUVEO ECOSYSTEM BRAND SYSTEM','kicker')
para('A reusable collection of communication assets built from the actual supplied marks for Vitruveo, Vertical Foundation, Pretrend, AI Wars, and VTRU Scope.')
para('The five identities retain their original artwork. The shared system adds typography, spacing, backgrounds, and export standards. These supporting choices are new production recommendations, not claims of pre-existing official brand rules.')
story.append(Spacer(1,14))
# Exact supplied logos, not cropped or redrawn.
logo_cells=[]
for b in BRANDS:
    f=SOURCE/b['id']/(b['id']+'-logo.png')
    im=Image.open(f);w=135;h=w*im.height/im.width
    logo_cells.append([RLImage(str(f),width=w,height=h),p(b['name'],'small')])
t=Table(logo_cells,colWidths=[165,320]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),('LINEBELOW',(0,0),(-1,-1),.4,C('#E7E8ED'))]));story.append(t)
story.append(Spacer(1,15))
para('<b>Review status.</b> Source audit passed. New layouts and proposed copy are provided for owner review. Source matching does not establish legal ownership or certify brand-owner approval.','small')
story.append(PageBreak())

para('01 / Identity directory','kicker');para('Distinct by design.','h1')
para('Role labels below describe how the supplied plan organizes the families; they are not independent product verification. Supporting layout colors are kept separate from source artwork.')
for b in BRANDS[:3]:
    para(b['name'],'h2');para(roles[b['id']], 'small')
    para(f"<b>Source family:</b> {b['id']}-brandkit.zip · seven SVG and seven PNG variants. Use the full logo for named communication and the supplied logomark for compact identity where available.")
    s=', '.join(f'{h} ({label.lower()})' for h,label in source_swatch[b['id']])
    para('<b>Source-derived colors:</b> '+s+'.','small')
    para(f"<b>Proposed layout palette:</b> accent {b['accent']} · secondary {b['secondary']} · ink {b['ink']} · pale field {b['pale']}.",'small')
story.append(PageBreak())
para('02 / Identity directory','kicker');para('Keep each mark intact.','h1')
for b in BRANDS[3:]:
    para(b['name'],'h2');para(roles[b['id']], 'small')
    para(f"<b>Source family:</b> {b['id']}-brandkit.zip · seven SVG and seven PNG variants. Source lettering remains unchanged.")
    para('<b>Source-derived colors:</b> '+', '.join(f'{h} ({label.lower()})' for h,label in source_swatch[b['id']])+'.','small')
    para(f"<b>Proposed layout palette:</b> accent {b['accent']} · secondary {b['secondary']} · ink {b['ink']} · pale field {b['pale']}.",'small')
para('How to read the palettes','h3')
para('Source-derived hex values are rounded sRGB representations of exact tokens recorded in source-audit.json. Gradient endpoints do not describe every visible intermediate color. Proposed layout colors are new supporting choices and must never be used to recolor a supplied logo.')
para('Supporting typography','h3')
para('DejaVu Sans is the proposed template typeface: bold headlines, regular body text and metadata. Logo lettering is outlined source artwork and remains unchanged. Font files are not bundled. Review line breaks after any substitution.')
story.append(PageBreak())

para('03 / Artwork handling','kicker');para('Preserve the source.','h1')
rules=[('Embed, then compose.','Use the exact supplied SVG or PNG. Keep path geometry, gradients, lettering, transparent spaces, and aspect ratio.'),('Scale uniformly.','Do not stretch, rotate, redraw, recolor, outline, add effects to, or crop the mark. Keep decorative lines and status glyphs separate.'),('Give the logo room.','Start with clear space of at least one quarter of the visible logo height. This is a proposed layout rule; increase the space when possible.'),('Choose contrast deliberately.','Use full-color originals on a light field and a supplied white variant on a dark field. Inspect rendered appearance rather than trusting a filename.'),('Check the final crop.','Profiles use padded 1024-square canvases. Preview the actual circular crop and account placement. A square source viewport alone does not guarantee safety.')]
for title,body in rules:
    para(title,'h3');para(body)
para('New symbols are supporting artwork. Emoji expressions, charts, and sticker decorations are not replacement brand logos.','small')
story.append(PageBreak())

para('04 / Source-specific notes','kicker');para('Details that matter.','h1')
for title,body in [
('AI Wars is a wordmark.','The supplied file named aiwars-logomark.svg is the same full wordmark geometry and viewBox as the primary logo. Circle and square variants provide a square viewport around it. No compact official symbol was supplied; do not invent one.'),
('Foundation needs more height.','The full Vertical Foundation logo is approximately 1.59:1, with its name beneath the architecture. The separate logomark omits the wording. Its logo-dark.svg is byte-identical to the primary source; use logo-white.svg when a white lockup is needed.'),
('Vitruveo keeps its separators.','The circular Vitruveo symbol contains six gradient-filled paths and transparent negative-space separators. Embed the intact source. Do not reconstruct its circle or fill the open spaces.'),
('Viewports are not backgrounds.','Circle and square filenames describe source viewports and spacing, rather than an added circular or square background. Preserve the full viewBox.'),
('Definitions can be unused.','Some white SVG variants retain gradient definitions while visible fills are white. The audit lists all defined tokens; it does not imply every token is visible. SVG masters in the system embed source files independently, avoiding gradient-ID collisions.')]:
    para(title,'h3');para(body)
story.append(PageBreak())

para('05 / Digital production','kicker');para('Choose the destination.','h1')
table([['Asset','Production target'],['Emoji','128 × 128 PNG · transparent · below 256 KB'],['Sticker','320 × 320 PNG · transparent · below 512 KB'],['Profile image','1024 × 1024 · light, dark, framed'],['X profile banner','1500 × 500'],['Facebook cover','1640 × 720'],['LinkedIn company','1512 × 256'],['LinkedIn personal','1584 × 396'],['Discord banner','960 × 540'],['Website hero','1920 × 640'],['Square social','1080 × 1080'],['Landscape social','1200 × 630'],['Story / vertical','1080 × 1920']],[160,347])
para('These are production targets for this package, not independently verified current platform requirements. Inspect live upload previews for account-specific overlays and mobile crops.','small')
para('Each brand receives nine social compositions, three announcement templates, and two document headers. SVG masters accompany PNG exports. Proposed headlines and descriptors require editorial review; bracketed fields must be replaced before publication.')
story.append(PageBreak())

para('06 / Documents and ecosystem','kicker');para('Built for reuse.','h1')
para('Letterhead system','h2')
para('Three A4 portrait designs per brand: formal correspondence, general office correspondence, and technical reports. Each includes an editable DOCX, fixed PDF, and blank high-resolution PNG at approximately 300 dpi. Use the supplied PDF for stable placement; office editors can reflow DOCX content.')
para('The writing area stays clear. Replace editable contact fields such as [Email] and [Website]. No physical address, staff title, legal entity, or ownership statement should be invented.')
para('PDF masters use RGB color and no bleed. A commercial printer may require color conversion or its own preflight. No PDF/X certification or CMYK separation is claimed.','small')
para('Four-brand and five-brand compositions','h2')
para('The original four-brand composition includes Vitruveo, Pretrend, AI Wars, and Vertical Foundation. VTRU Scope is included in separate five-brand ecosystem pieces and in the complete package.')
para('No earlier banner was uploaded in this thread. The four-brand banner is a fresh composition using the actual marks; it is not a pixel-specific correction of an unavailable original.')
para('Editable masters','h2')
para('SVG masters keep text and layout elements editable, with exact source logos embedded. PNG files are fixed renderings. DOCX contact and body text remain editable. Edit the master first, then export a new fixed file at the manifest dimensions.')
story.append(PageBreak())

para('07 / Audit and provenance','kicker');para('A traceable foundation.','h1')
table([['Source audit','Result'],['Archives / files','5 archives · 70 assets · 35 SVG + 35 PNG'],['Archive CRC and extraction','All pass; extracted bytes match archive content'],['SVG parsing and rendering','All 35 pass'],['PNG decoding','All 35 pass'],['SVG active or external content','No scripts, handlers, foreignObject, or external references found'],['SVG ↔ PNG comparison','Maximum mean channel difference 0.814 / 255 at 512 px']],[170,337])
para('The raster comparison used white and dark fields and supports a finding of small rendering differences between paired files. It supplements hash checks; it does not certify legal authorship or trademark rights.','small')
para('Where the evidence lives','h2')
para('<b>08-Manifests-and-Export-Checks/source-inventory.csv</b><br/>Every source filename, archive, byte size, SHA-256 hash, format, dimensions or viewBox, and structural details.','small')
para('<b>08-Manifests-and-Export-Checks/source-audit.json</b><br/>Full source checks, exact gradient stops, comparison results, and source-specific notes.','small')
para('The export manifest records generated files, their source artwork, and export checks. “Source-matched” means the embedded artwork traces to supplied source bytes. “Derivative” describes the new layout surrounding it. Editorial and layout review does not imply brand-owner approval.')
para('The original ZIPs and unchanged standalone source artwork are not repackaged. Keep the uploaded archives as the archival masters.','small')
story.append(PageBreak())

para('08 / Working workflow','kicker');para('Edit. Review. Export.','h1')
steps=[('01','Choose the brand and destination format.'),('02','Open the editable SVG or DOCX. Replace placeholders and review proposed copy.'),('03','Preserve the embedded mark and its aspect ratio. Adjust only supporting layout elements.'),('04','Export at the recorded dimensions. Check transparency, edge spacing, and small text.'),('05','Preview the actual platform crop or print page, then publish the reviewed file.'),('06','Keep the edited master and export together for future updates.')]
for n,body in steps:
    t=Table([[p(n,'h2'),p(body,'body')]],colWidths=[44,463]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),('LINEBELOW',(0,0),(-1,-1),.5,C('#E0E2EA'))]));story.append(t)
story.append(Spacer(1,28))
para('Production system, with recorded source provenance.','h2')
para('Owner review remains appropriate for final copy, visual choices, and placement. This package does not assert legal ownership or outside brand approval.','small')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(str(OUT/'Brand-System-Guide.md'));print(str(pdfpath))
