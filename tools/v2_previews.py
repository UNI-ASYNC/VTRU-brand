"""Build V2-only GitHub galleries and preview documents without changing V1."""
from pathlib import Path
from collections import OrderedDict
import json, math, re, urllib.parse
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

REPO = Path(__file__).resolve().parents[1]
V2 = REPO / 'v2'
GALLERY = V2 / 'gallery'
PREVIEWS = V2 / 'previews'
FONT_DIR = V2 / 'resources/fonts'
if not FONT_DIR.is_dir():
    FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
REG = ImageFont.truetype(str(FONT_DIR / 'DejaVuSans.ttf'), 22)
BOLD = ImageFont.truetype(str(FONT_DIR / 'DejaVuSans-Bold.ttf'), 34)
SMALL = ImageFont.truetype(str(FONT_DIR / 'DejaVuSans.ttf'), 18)
COPY = json.loads((V2 / 'reports/current-website-copy.json').read_text())['brands']

SURFACES = {
    'facebook-page-cover': 'Facebook Page cover',
    'facebook-cover-mobile-friendly': 'Facebook alternate Page cover',
    'facebook-feed-landscape': 'Facebook landscape feed post',
    'x-profile-banner': 'X profile header',
    'youtube-channel-banner': 'YouTube channel banner',
    'youtube-video-thumbnail': 'YouTube video thumbnail template',
    'tiktok-vertical-cover': 'TikTok content cover',
    'instagram-feed-square': 'Instagram square feed post',
    'instagram-feed-portrait': 'Instagram portrait feed post',
    'instagram-story-reel-cover': 'Instagram Story / Reel cover',
    'rumble-channel-backsplash': 'Rumble channel backsplash',
    'ecosystem-wide-master': 'Wide ecosystem template',
}
SOCIAL_ORDER = {name: i for i, name in enumerate(SURFACES)}


def href(path, parent):
    import os
    return urllib.parse.quote(os.path.relpath(path, parent), safe='/-_.')


def purpose(path):
    if path.stem in SURFACES:
        return SURFACES[path.stem]
    stem = path.stem
    if '-announcement-' in stem:
        return 'Announcement template / ' + stem.split('-announcement-', 1)[1].replace('-', ' ')
    if '-document-header-' in stem:
        return 'Document header / ' + stem.split('-document-header-', 1)[1]
    if '-letterhead-' in stem:
        return 'A4 letterhead / ' + stem.split('-letterhead-', 1)[1].replace('-A4', '')
    if '-avatar-' in stem:
        return 'Avatar / supplied ' + stem.split('-avatar-', 1)[1].replace('-', ' ')
    if stem.endswith('-linkedin-company'):
        return 'LinkedIn Company Page cover'
    if stem.endswith('-linkedin-personal'):
        return 'LinkedIn personal profile cover'
    if stem.endswith('-discord-server-banner'):
        return 'Discord server banner'
    if stem.endswith('-website-hero'):
        return 'Website header / hero template'
    return stem.replace('-', ' ')


def dimensions(path):
    with Image.open(path) as im:
        value = f'{im.width} × {im.height} px'
    if 'letterhead-' in path.stem:
        value = 'A4 / ' + value + ' / 300 dpi PNG'
    return value


def paired_files(path):
    files = [('PNG', path)]
    stem = path.stem.replace('-300dpi', '')
    for label, ext in [('Editable SVG', '.svg'), ('PDF', '.pdf'), ('Editable DOCX', '.docx')]:
        p = path.with_name(stem + ext)
        if p.exists():
            files.append((label, p))
    return files


def wrap_label(value, font, width):
    rows = []
    line = ''
    for word in value.split():
        candidate = (line + ' ' + word).strip()
        if line and font.getlength(candidate) > width:
            rows.append(line)
            line = word
        else:
            line = candidate
    if line:
        rows.append(line)
    return rows


def contact_sheet(files, title, out):
    columns = 3
    cw, ch = 600, 470
    rows = math.ceil(len(files) / columns)
    sheet = Image.new('RGB', (1860, 150 + rows * ch), '#F1F2F4')
    draw = ImageDraw.Draw(sheet)
    draw.text((30, 28), title, font=BOLD, fill='#111111')
    draw.text((30, 78), 'V2 · Source-only layouts · Open space is reserved for owner imagery', font=SMALL, fill='#555555')
    for i, p in enumerate(files):
        x, y = 30 + (i % columns) * cw, 130 + (i // columns) * ch
        box_w, box_h = 568, 365
        draw.rectangle((x, y, x + box_w, y + box_h), fill='white', outline='#D5D5D5', width=1)
        with Image.open(p) as source:
            im = source.convert('RGBA')
            im.thumbnail((box_w - 16, box_h - 16), Image.Resampling.LANCZOS)
            ix, iy = x + (box_w - im.width) // 2, y + (box_h - im.height) // 2
            if 'letterhead-' in p.stem:
                # Keep the whole A4 page visible against the white cell.
                draw.rectangle((ix - 1, iy - 1, ix + im.width, iy + im.height), outline='#D5D5D5', width=1)
            sheet.paste(im, (ix, iy), im)
        label_rows = wrap_label(purpose(p), REG, box_w)
        for j, line in enumerate(label_rows[:2]):
            draw.text((x, y + box_h + 13 + j * 27), line, font=REG, fill='#111111')
        draw.text((x, y + box_h + 72), dimensions(p), font=SMALL, fill='#555555')
    out.parent.mkdir(exist_ok=True)
    sheet.save(out, optimize=True)
    return out


def write_collection_page(slug, title, files, sheet):
    path = GALLERY / (slug + '.md')
    body = [
        f'# V2 — {title}', '',
        '[V2 gallery index](../GALLERY.md) · [Usage guide](../USAGE-GUIDE.md) · [Website-copy sources](../reports/COPY-SOURCES.md)', '',
        'These are general editable canvases. Empty white areas are deliberately available for the owner’s existing imagery. The preview labels describe their intended use; they are not additional marketing copy.', '',
        f'[![Contact sheet for {title}]({href(sheet, path.parent)})]({href(sheet, path.parent)})', '',
    ]
    for p in files:
        label = purpose(p)
        with Image.open(p) as im:
            portrait = im.height > im.width * 1.15
        width = 330 if portrait else 900
        links = ' · '.join(f'[{name}]({href(f, path.parent)})' for name, f in paired_files(p))
        body += [
            f'## {label}', '',
            dimensions(p) + ' · ' + links, '',
            f'<a href="{href(p, path.parent)}"><img src="{href(p, path.parent)}" alt="{label} — {title}" width="{width}"></a>', '',
        ]
    path.write_text('\n'.join(body))
    return path


def draw_pdf_image(c, path, x, y, w, h):
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(str(path), x + (w - dw) / 2, y + (h - dh) / 2, width=dw, height=dh, mask='auto')


def preview_book(sheets, counts):
    pdfmetrics.registerFont(TTFont('V2Sans', str(FONT_DIR / 'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('V2Sans-Bold', str(FONT_DIR / 'DejaVuSans-Bold.ttf')))
    out = PREVIEWS / 'VTRU-Brand-V2-Preview.pdf'
    c = canvas.Canvas(str(out), pagesize=(960, 1350))
    c.setTitle('Source-only templates / V2')
    c.setAuthor('VTRU brand review package')
    def page(n):
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, 960, 1350, fill=1, stroke=0)
        c.setFillColorRGB(.3, .3, .3)
        c.setFont('V2Sans', 10)
        c.drawString(30, 24, 'VTRU BRAND / V2 / SOURCE-ONLY TEMPLATES')
        c.drawRightString(930, 24, str(n))
    page(1)
    c.setFillColorRGB(.06, .06, .06)
    c.setFont('V2Sans-Bold', 31)
    c.drawString(35, 1285, 'Source-only templates / V2')
    c.setFont('V2Sans', 14)
    for i, line in enumerate([
        'Original logos from the supplied ZIP files. Existing website wording only.',
        'White areas are intentionally open for the owner’s existing imagery.',
        'V1 remains preserved as evidence of the earlier proposals.',
        f'{counts} image canvases are shown in the following contact sheets.',
    ]):
        c.drawString(35, 1245 - i * 24, line)
    brand_ids = ['vitruveo', 'verticalfoundation', 'pretrend', 'aiwars', 'vtruscope']
    dirs = ['03-Vitruveo', '04-Vertical-Foundation', '05-Pretrend', '06-AI-Wars', '07-VTRU-Scope']
    for i, (brand, folder) in enumerate(zip(brand_ids, dirs)):
        p = V2 / 'social-templates' / folder / 'Facebook/facebook-page-cover.png'
        yy = 905 - i * 186
        c.setFont('V2Sans', 12)
        c.setFillColorRGB(.1, .1, .1)
        c.drawString(35, yy + 153, COPY[brand]['name'] + ' / Facebook Page cover')
        c.setStrokeColorRGB(.82, .82, .82)
        c.rect(35, yy, 890, 142, fill=0, stroke=1)
        draw_pdf_image(c, p, 41, yy + 4, 878, 134)
    c.showPage()
    for n, sheet in enumerate(sheets, 2):
        page(n)
        draw_pdf_image(c, sheet, 25, 54, 910, 1260)
        c.showPage()
    c.save()
    return out, len(sheets) + 1


def check_local_links(paths):
    errors = []
    count = 0
    for p in paths:
        text = p.read_text()
        urls = re.findall(r'\]\(([^)]+)\)', text) + re.findall(r'(?:src|href)="([^"]+)"', text)
        for url in urls:
            if url.startswith(('https://', 'http://', 'mailto:', '#', 'data:')):
                continue
            raw = urllib.parse.unquote(url.split('#', 1)[0].split('?', 1)[0])
            count += 1
            if not (p.parent / raw).exists():
                errors.append([str(p.relative_to(V2)), url])
    return count, errors


def main():
    GALLERY.mkdir(exist_ok=True)
    PREVIEWS.mkdir(exist_ok=True)
    pages, sheets, groups = [], [], []
    social_count = supplemental_count = 0
    for collection in sorted((V2 / 'social-templates').iterdir()):
        if not collection.is_dir():
            continue
        files = sorted(collection.glob('*/*.png'), key=lambda p: SOCIAL_ORDER.get(p.stem, 100))
        if not files:
            continue
        title = collection.name[3:].replace('-', ' ')
        slug = 'social-' + collection.name.lower()
        sheet = contact_sheet(files, title + ' / Social formats', PREVIEWS / (slug + '-contact-sheet.png'))
        page = write_collection_page(slug, title + ' / Social formats', files, sheet)
        pages.append(page); sheets.append(sheet); groups.append(('Social', title, page, files))
        social_count += len(files)
    for brand in ['vitruveo', 'verticalfoundation', 'pretrend', 'aiwars', 'vtruscope']:
        files = sorted((V2 / 'supplemental' / brand).glob('*/*.png'), key=lambda p: (p.parent.name, p.stem))
        title = COPY[brand]['name']
        slug = 'supplemental-' + brand
        sheet = contact_sheet(files, title + ' / Additional templates', PREVIEWS / (slug + '-contact-sheet.png'))
        page = write_collection_page(slug, title + ' / Additional templates', files, sheet)
        pages.append(page); sheets.append(sheet); groups.append(('Additional', title, page, files))
        supplemental_count += len(files)
    pdf, pdf_pages = preview_book(sheets, social_count + supplemental_count)
    top = V2 / 'GALLERY.md'
    body = [
        '# V2 — Source-only template gallery', '',
        '[V2 overview](README.md) · [Usage guide](USAGE-GUIDE.md) · [Verified website copy](reports/COPY-SOURCES.md) · [V1 evidence gallery](../GALLERY.md)', '',
        'These are static image canvases for covers, feed posts, Stories/Reels, video thumbnails, website headers, announcements and stationery. They use the supplied source logos and the recorded existing website wording. The open areas are intentionally reserved for the owner’s existing imagery.', '',
        'The announcement/document fields in brackets are editable functional placeholders. These canvases are not finished campaign posters, websites or applications.', '',
        f'**[Open the {pdf_pages}-page preview book]({href(pdf, top.parent)})**', '',
        '## Social formats', '',
    ]
    for kind, title, page, files in groups:
        if kind != 'Social':
            continue
        body.append(f'- [{title}: covers, posts and content templates]({href(page, top.parent)})')
    body += ['', '## Additional templates', '']
    for kind, title, page, files in groups:
        if kind == 'Additional':
            body.append(f'- [{title}: announcements, headers, avatars, LinkedIn, Discord, website and A4 stationery]({href(page, top.parent)})')
    body += ['', '## Representative V2 canvases', '']
    for folder in ['03-Vitruveo', '04-Vertical-Foundation', '05-Pretrend', '06-AI-Wars', '07-VTRU-Scope']:
        p = V2 / 'social-templates' / folder / 'Facebook/facebook-page-cover.png'
        body += [f'### {folder[3:].replace("-", " ")} / Facebook Page cover', '', f'[![{folder[3:].replace("-", " ")} Facebook Page cover]({href(p, top.parent)})]({href(p, top.parent)})', '']
    for folder in ['01-Ecosystem-Four-Brands', '02-Ecosystem-Five-Brands']:
        p = V2 / 'social-templates' / folder / 'Master/ecosystem-wide-master.png'
        body += [f'### {folder[3:].replace("-", " ")} / Wide ecosystem template', '', f'[![{folder[3:].replace("-", " ")} wide ecosystem template]({href(p, top.parent)})]({href(p, top.parent)})', '']
    body += ['V1 artwork, previews, ZIPs and reports remain separate and unchanged as evidence. [Version notes](VERSION-NOTES.md).', '']
    top.write_text('\n'.join(body))
    checked, errors = check_local_links([top] + pages)
    if errors:
        raise RuntimeError(json.dumps(errors, indent=2))
    print(json.dumps({'social_pngs': social_count, 'supplemental_pngs': supplemental_count, 'total_png_canvases': social_count + supplemental_count, 'gallery_pages': len(pages) + 1, 'contact_sheets': len(sheets), 'preview_pdf_pages': pdf_pages, 'local_links_checked': checked, 'link_errors': 0, 'preview_pdf': str(pdf.relative_to(REPO))}, indent=2))


if __name__ == '__main__':
    main()
