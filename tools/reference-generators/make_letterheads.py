"""Build matching A4 stationery masters and editable Word templates.

Protected artwork is placed from source files with its aspect ratio intact.
No protected mark is reconstructed or recolored by this generator.
"""
from pathlib import Path
import base64
import json
import subprocess
import zipfile
from xml.sax.saxutils import escape
from PIL import Image
import fitz
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from brand_common import BRANDS as SYSTEM_BRANDS, sha

BASE = Path('/workspace/work')
ROOT = BASE / 'brand-system'
SOURCE = BASE / 'source'
PAGE_W, PAGE_H = 595.2756, 841.8898
MARGIN = 50
INK, MUTED, LINE = '#182333', '#5c6673', '#dce3e8'
BRANDS = [(b['id'],b['name'],b['folder'],b['accent']) for b in SYSTEM_BRANDS]
STYLES = ['formal', 'office', 'technical']
RECORDS = []


def source_uri(brand):
    return 'data:image/svg+xml;base64,' + base64.b64encode((SOURCE / brand / f'{brand}-logo.svg').read_bytes()).decode()


def image_fit(brand, x, y, maxw, maxh, center=False):
    """Place original SVG image with explicit contain scaling, never crop."""
    im = Image.open(SOURCE / brand / f'{brand}-logo.png')
    ratio = im.width / im.height
    w = min(maxw, maxh * ratio)
    h = w / ratio
    if center:
        x -= w / 2
    return (f'<image x="{x:.4f}" y="{y:.4f}" width="{w:.4f}" height="{h:.4f}" '
            f'preserveAspectRatio="xMidYMid meet" xlink:href="{source_uri(brand)}"/>')


def txt(s, x, y, size=8.5, color=MUTED, anchor='start', weight='normal', spacing=0):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="DejaVu Sans" '
            f'font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" '
            f'fill="{color}">{escape(s)}</text>')


def line(x1, y1, x2, y2, color=LINE, width=.7):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>'


def make_svg(brand, name, accent, style):
    body = ['<rect width="100%" height="100%" fill="#ffffff"/>']
    right = PAGE_W - MARGIN
    if style == 'formal':
        body += [image_fit(brand, MARGIN, 46, 177, 64),
                 f'<rect x="{right-28}" y="46" width="28" height="4" rx="1" fill="{accent}"/>',
                 line(MARGIN, 140, right, 140, LINE, .8),
                 line(MARGIN, 140, MARGIN+42, 140, accent, 2),
                 line(MARGIN, 780, right, 780, LINE, .8),
                 txt(name.upper(), MARGIN, 799, 7.7, INK, weight='bold', spacing=.6),
                 txt('[Email]  |  [Website]', right, 799, 8, MUTED, 'end')]
    elif style == 'office':
        body += [image_fit(brand, PAGE_W/2, 42, 185, 68, center=True),
                 line(MARGIN+70, 140, right-70, 140, LINE, .8),
                 line(PAGE_W/2-20, 140, PAGE_W/2+20, 140, accent, 2.4),
                 line(MARGIN+70, 780, right-70, 780, LINE, .8),
                 txt('[Email]  |  [Website]', PAGE_W/2, 799, 8.4, MUTED, 'middle')]
    else:
        body += [image_fit(brand, MARGIN, 45, 167, 64),
                 txt('TECHNICAL CORRESPONDENCE', right, 53, 7.3, INK, 'end', 'bold', .5),
                 txt('[Document reference]', right, 72, 8.3, MUTED, 'end'),
                 line(MARGIN, 136, right, 136, accent, 2),
                 line(MARGIN, 141, right, 141, LINE, .6),
                 line(MARGIN, 780, right, 780, LINE, .8),
                 txt('[Email]  |  [Website]', MARGIN, 799, 8, MUTED),
                 txt('[Revision]  |  [Page]', right, 799, 8, MUTED, 'end')]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="210mm" height="297mm" viewBox="0 0 {PAGE_W} {PAGE_H}">\n'
            '<title>' + escape(name + ' — ' + style.title() + ' A4 letterhead') + '</title>\n' +
            '\n'.join(body) + '\n</svg>\n')


def set_cell_margins(cell, top=0, left=0, bottom=0, right=0):
    tcpr = cell._tc.get_or_add_tcPr()
    margins = OxmlElement('w:tcMar')
    for key, value in [('top', top), ('left', left), ('bottom', bottom), ('right', right)]:
        el = OxmlElement(f'w:{key}')
        el.set(qn('w:w'), str(value))
        el.set(qn('w:type'), 'dxa')
        margins.append(el)
    tcpr.append(margins)


def border(paragraph, color, size=6, space=4, location='bottom'):
    ppr = paragraph._p.get_or_add_pPr()
    borders = ppr.find(qn('w:pBdr'))
    if borders is None:
        borders = OxmlElement('w:pBdr'); ppr.append(borders)
    el = OxmlElement(f'w:{location}')
    for k, v in [('val', 'single'), ('sz', str(size)), ('space', str(space)), ('color', color.lstrip('#'))]:
        el.set(qn('w:'+k), v)
    borders.append(el)


def format_paragraph(p, align=WD_ALIGN_PARAGRAPH.LEFT, before=0, after=0, size=8.5):
    p.alignment = align
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1
    for r in p.runs:
        r.font.name = 'DejaVu Sans'
        r.font.size = Pt(size)
        r.font.color.rgb = RGBColor.from_string(MUTED[1:])


def add_logo(paragraph, brand, maxw, maxh):
    im = Image.open(SOURCE / brand / f'{brand}-logo.png')
    w = min(maxw, maxh * im.width / im.height)
    h = w * im.height / im.width
    paragraph.add_run().add_picture(str(SOURCE / brand / f'{brand}-logo.png'), width=Pt(w), height=Pt(h))


def add_page_field(p):
    fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE')
    r = OxmlElement('w:r'); props = OxmlElement('w:rPr')
    size = OxmlElement('w:sz'); size.set(qn('w:val'), '16'); props.append(size)
    r.append(props); text_el = OxmlElement('w:t'); text_el.text='1'; r.append(text_el)
    fld.append(r); p._p.append(fld)


def add_fixed_header_table(header, columns):
    table = header.add_table(rows=1, cols=columns, width=Pt(PAGE_W-2*MARGIN))
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = [PAGE_W-2*MARGIN] if columns == 1 else [250, PAGE_W-2*MARGIN-250]
    for cell, width in zip(table.rows[0].cells, widths):
        cell.width = Pt(width); set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    return table


def make_docx(brand, name, accent, style, path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Pt(PAGE_W); sec.page_height = Pt(PAGE_H)
    sec.left_margin = Pt(MARGIN); sec.right_margin = Pt(MARGIN)
    sec.top_margin = Pt(162); sec.bottom_margin = Pt(80)
    sec.header_distance = Pt(43); sec.footer_distance = Pt(38)
    normal = doc.styles['Normal']
    normal.font.name = 'DejaVu Sans'; normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(INK[1:])
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.2
    for sname in ['Header','Footer']:
        sty = doc.styles[sname]
        sty.font.name = 'DejaVu Sans'; sty.font.size = Pt(8)
        sty.font.color.rgb = RGBColor.from_string(MUTED[1:])
        sty.paragraph_format.space_after = Pt(0)
    h = sec.header
    h.paragraphs[0].paragraph_format.space_after = Pt(0)
    h.paragraphs[0].paragraph_format.line_spacing = Pt(1)
    h.paragraphs[0].paragraph_format.space_before = Pt(0)
    h.paragraphs[0].add_run().font.size = Pt(1)
    if style == 'office':
        table = add_fixed_header_table(h, 1)
        p = table.cell(0,0).paragraphs[0]
        format_paragraph(p, WD_ALIGN_PARAGRAPH.CENTER)
        add_logo(p, brand, 185, 68)
        # Fixed clearance accommodates all source logo aspect ratios.
        table.rows[0].height = Pt(88)
        from docx.enum.table import WD_ROW_HEIGHT_RULE
        table.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        p = h.add_paragraph(); format_paragraph(p, after=0)
        p.paragraph_format.line_spacing = Pt(1)
        border(p, accent, 10, 0)
    else:
        table = add_fixed_header_table(h, 2)
        p = table.cell(0,0).paragraphs[0]
        format_paragraph(p)
        add_logo(p, brand, 177 if style=='formal' else 167, 64)
        p = table.cell(0,1).paragraphs[0]
        format_paragraph(p, WD_ALIGN_PARAGRAPH.RIGHT, size=7.3)
        if style=='technical':
            r = p.add_run('TECHNICAL CORRESPONDENCE'); r.bold=True
            r.font.name='DejaVu Sans'; r.font.size=Pt(7.3); r.font.color.rgb=RGBColor.from_string(INK[1:])
            p2=table.cell(0,1).add_paragraph('[Document reference]')
            format_paragraph(p2,WD_ALIGN_PARAGRAPH.RIGHT,before=8,size=8.3)
        else:
            r=p.add_run('━━━━'); r.font.color.rgb=RGBColor.from_string(accent[1:]); r.font.size=Pt(10)
        table.rows[0].height = Pt(87)
        from docx.enum.table import WD_ROW_HEIGHT_RULE
        table.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
        p=h.add_paragraph(); format_paragraph(p)
        p.paragraph_format.line_spacing=Pt(1)
        border(p, accent if style=='technical' else LINE, 12 if style=='technical' else 6, 0)
    footer = sec.footer
    fp = footer.paragraphs[0]
    format_paragraph(fp, size=8)
    border(fp, LINE, 6, 9, 'top')
    if style=='office':
        fp.alignment=WD_ALIGN_PARAGRAPH.CENTER
        fp.add_run('[Email]  |  [Website]')
    elif style=='formal':
        # Tab stop at the printable right edge keeps each field independently editable.
        fp.paragraph_format.tab_stops.add_tab_stop(Pt(PAGE_W-2*MARGIN), WD_ALIGN_PARAGRAPH.RIGHT)
        r=fp.add_run(name.upper()); r.bold=True
        fp.add_run('\t[Email]  |  [Website]')
    else:
        fp.paragraph_format.tab_stops.add_tab_stop(Pt(PAGE_W-2*MARGIN), WD_ALIGN_PARAGRAPH.RIGHT)
        fp.add_run('[Email]  |  [Website]\t[Revision]  |  ')
        add_page_field(fp)
    format_paragraph(fp, fp.alignment, size=8)
    # An empty body is intentional. The Word template opens ready for correspondence.
    p=doc.add_paragraph()
    p.paragraph_format.space_after=Pt(8)
    p.add_run('')
    doc.core_properties.title=f'{name} — {style.title()} A4 letterhead'
    doc.core_properties.subject='Editable reusable stationery using supplied brand artwork'
    doc.core_properties.author=''
    doc.core_properties.keywords='A4, letterhead, editable, source-preserved logo'
    doc.save(path)


def main():
    for brand, name, folder, accent in BRANDS:
        dest = ROOT / folder / 'Letterheads'
        dest.mkdir(parents=True, exist_ok=True)
        for style in STYLES:
            stem=f'{brand}-letterhead-{style}-A4'
            svg=dest/f'{stem}.svg'
            svg.write_text(make_svg(brand,name,accent,style))
            pdf=dest/f'{stem}.pdf'
            subprocess.run(['inkscape',str(svg),'--export-type=pdf','--export-area-page','--export-text-to-path',f'--export-filename={pdf}'],check=True,capture_output=True)
            # Render print PNG at exactly 300 dpi from the vector PDF master.
            with fitz.open(pdf) as doc:
                page=doc[0]
                pix=page.get_pixmap(matrix=fitz.Matrix(300/72,300/72),alpha=False)
                png=dest/f'{stem}-300dpi.png'
                pix.save(png)
            with Image.open(png) as image:
                # PDF rasterizers round dimensions up; remove only the outer white
                # edge to the standard 2480 x 3508 A4 raster (no artwork rescaling).
                image.crop((0,0,round(PAGE_W*300/72),round(PAGE_H*300/72))).save(png,dpi=(300,300),optimize=True)
            docx=dest/f'{stem}.docx'
            make_docx(brand,name,accent,style,docx)
            for p in [svg,pdf,png,docx]:
                source_file=SOURCE/brand/(f'{brand}-logo.'+('png' if p.suffix=='.docx' else 'svg'))
                RECORDS.append({'path':str(p.relative_to(ROOT)),'brand':brand,'category':'letterhead',
                    'layout':style,'paper':'A4','source_file':source_file.name,'source_sha256':sha(source_file),
                    'source_mark_placement':'aspect-ratio-preserving; no redraw or recolor',
                    'classification':'derivative artwork; embedded source logo unchanged','owner_review':'layout, contact placeholders, typography',
                    'notes': 'Editable Word layout; rendering can vary by editor.' if p.suffix=='.docx' else 'Blank writing area; editable placeholder contacts; RGB master, no bleed.'})
        (dest/'README.txt').write_text(
            f'{name} — A4 letterheads\n\n'
            'FORMAL: left-aligned logo and restrained footer.\n'
            'OFFICE: centered logo and centered contact line.\n'
            'TECHNICAL: document-reference header and revision/page footer.\n\n'
            'DOCX files are editable Word templates with real repeating headers and footers.\n'
            'Start typing in the blank body. Double-click the header/footer to replace bracketed\n'
            'contact or reference placeholders. The technical DOCX page number updates in Word.\n'
            'The supplied source logo is an embedded image, with its proportions preserved.\n'
            'Typography uses DejaVu Sans; install the font or select a substitute if unavailable.\n'
            'Word processors may reflow layout slightly. Check the final document before printing.\n\n'
            'PDF and SVG files are blank A4 visual masters; PNGs are 300 dpi RGB templates.\n'
            'PDFs retain the supplied vector artwork. All have white backgrounds and no bleed.\n'
            'They are suitable for office printing; a commercial printer may request CMYK/PDF-X.\n'
            'Replace contact placeholders before publishing or printing official correspondence.\n'
            'No legal entity details, physical address, or ownership statement has been invented.\n')
        print(f'Created 3 letterhead sets for {name}',flush=True)
    (BASE/'letterhead-records.json').write_text(json.dumps(RECORDS,indent=2))
    print(f'Created {len(RECORDS)} letterhead assets',flush=True)


if __name__=='__main__':
    main()
