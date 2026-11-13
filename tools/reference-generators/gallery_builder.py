from pathlib import Path
from urllib.parse import quote, unquote
from PIL import Image
import html, re, json

repo=Path('/workspace/work/VTRU-brand')
g=repo/'gallery';g.mkdir(parents=True,exist_ok=True)
neon=Path('/workspace/work/Neon-Social-Banner-Pack')
br=Path('/workspace/work/brand-system')
brands=[('vitruveo','Vitruveo','01-Vitruveo'),('verticalfoundation','Vertical Foundation','02-Vertical-Foundation'),('pretrend','Pretrend','03-Pretrend'),('aiwars','AI Wars','04-AI-Wars'),('vtruscope','VTRU Scope','05-VTRU-Scope')]
def url(p):return quote(str(p),safe='/.-')
def img(p,label,width):return f'<a href="{url(p)}"><img src="{url(p)}" alt="{html.escape(label,quote=True)}" width="{width}"></a>'
def nav():return '[All galleries](../GALLERY.md) · [Repository home](../README.md)'
def size(p):
    with Image.open(p) as im:return im.size
def links(rel,p):
    master=p.with_name(p.stem.replace('-300dpi','')) if p.stem.endswith('-300dpi') else p.with_suffix('')
    master_rel=rel.with_name(master.name)
    out=[f'[PNG]({url(rel)})']
    if master.with_suffix('.svg').exists():out.append(f'[SVG]({url(master_rel.with_suffix(".svg"))})')
    for ext in ['pdf','docx']:
        if master.with_suffix('.'+ext).exists():out.append(f'[{ext.upper()}]({url(master_rel.with_suffix("."+ext))})')
    return ' · '.join(out)
def preview(p,rel,title,width=None):
    w,h=size(p)
    width=width or (300 if h>w*1.3 else 460 if h>=w*.85 else 900)
    return [f'### {title}','',f'{w} × {h} px · '+links(rel,p),'',img(rel,title,width),'']

collections=sorted(p for p in neon.glob('0[1-7]-*') if p.is_dir())
counts={}
for collection in collections:
    rows=[f'# {collection.name[3:].replace("-"," ")} — neon social banners','',nav(),'','PNG previews are the upload-ready images. SVGs are editable masters. Keep the shared `00-Guide-and-Audit/Backgrounds/` directory with the masters when downloading or editing.','']
    pngs=sorted(collection.glob('*/*.png'));counts[collection.name]=len(pngs)
    for platform in ['Master','Facebook','X','YouTube','TikTok','Instagram','Rumble']:
        ps=[p for p in pngs if p.parent.name==platform]
        if not ps:continue
        rows+=['## '+platform,'']
        if platform in ['TikTok','Instagram']:rows+=['Use the named content-cover, feed, Story or Reel format.','']
        for p in ps:
            rel=Path('../social-banners')/p.relative_to(neon)
            rows+=preview(p,rel,p.stem.replace('-',' '))
            if platform=='YouTube' and p.stem=='youtube-channel-banner' and collection.name.startswith(('01-','02-')):
                crop=Path('../social-banners/08-Previews')/(collection.name+'-youtube-center-preview.png')
                rows+=['Centered desktop/mobile crop preview:','',img(crop,'YouTube center crop',900),'']
    rows+=['[Complete neon preview PDF](../social-banners/08-Previews/Neon-Social-Banners-Preview.pdf)','']
    (g/('neon-'+collection.name+'.md')).write_text('\n'.join(rows))

brand_count=0
for key,name,folder in brands:
    rows=[f'# {name} — brand-system gallery','',nav(),'','Open any image for full resolution. Editable SVG, PDF and DOCX files are linked beside the relevant design.','']
    for category in ['Social-Banners','Announcement-Templates','Profile-Images','Document-Headers','Emojis','Stickers','Letterheads']:
        ps=sorted((br/folder/category).glob('*.png'));brand_count+=len(ps)
        if not ps:continue
        rows+=['## '+category.replace('-',' '),'']
        if category in ['Emojis','Stickers','Profile-Images']:
            rows+=['| Preview | File and master |','|---|---|']
            for p in ps:
                rel=Path('../brand-system')/p.relative_to(br);w,h=size(p)
                width={'Emojis':72,'Stickers':160,'Profile-Images':180}[category]
                rows+=['| '+img(rel,p.stem,width)+f' | **{p.stem}**<br>{w} × {h} px<br>'+links(rel,p)+' |']
            rows+=['']
        else:
            for p in ps:
                rel=Path('../brand-system')/p.relative_to(br)
                rows+=preview(p,rel,p.stem.replace(key+'-',''),300 if category=='Letterheads' else None)
    rows+=['## Contact sheets','']
    for c in ['social','discord','letterheads']:
        rel=Path('../brand-system/07-Previews-and-Contact-Sheets')/(key+'-'+c+'-contact-sheet.png')
        rows+=[f'- [{c.capitalize()} contact sheet]({url(rel)})']
    rows+=['','[Complete brand-system preview PDF](../brand-system/07-Previews-and-Contact-Sheets/Complete-Preview-Book.pdf)','']
    (g/('brand-system-'+key+'.md')).write_text('\n'.join(rows))

rows=['# Ecosystem-wide brand-system gallery','',nav(),'']
for category in ['Multi-Brand-Banners','Cross-Project-Announcements']:
    rows+=['## '+category.replace('-',' '),'']
    for p in sorted((br/'06-Ecosystem-Wide'/category).glob('*.png')):
        rel=Path('../brand-system')/p.relative_to(br);rows+=preview(p,rel,p.stem)
(g/'brand-system-ecosystem.md').write_text('\n'.join(rows))

rows=['# Original brand marks','',nav(),'','These are the supplied source files. The public brand-library ZIPs match the uploads byte for byte. Logo lettering, geometry and colors are retained.','']
for key,name,folder in brands:
    base=Path('../source-brand-kits/unpacked')/key
    rows+=['## '+name,'',f'<picture><source media="(prefers-color-scheme: dark)" srcset="{url(base/(key+"-logo-dark.png"))}"><img alt="{name} supplied full logo" src="{url(base/(key+"-logo.png"))}" width="480"></picture>','', '| Supplied variant | PNG | SVG |','|---|---|---|']
    for v in ['logo','logo-dark','logo-white','logo-bw','logomark','logomark-circle','logomark-square']:
        rows+=[f'| {v} | [PNG]({url(base/(key+"-"+v+".png"))}) | [SVG]({url(base/(key+"-"+v+".svg"))}) |']
    rows+=['']
(g/'source-brand-marks.md').write_text('\n'.join(rows))

rows=['# Image galleries','','Browse the actual images here. Each gallery includes full-resolution PNGs and links to editable masters. ZIP downloads are retained in the repository.','', '[Repository home](README.md) · [Developer handoff](DEVELOPER-HANDOFF.md) · [Research report](reports/RESEARCH-REPORT.md)','', '## Reference-style ecosystem banners','','### Four brands','',img(Path('social-banners/01-Ecosystem-Four-Brands/Master/reference-wide-master.png'),'Four-brand neon reference composition',1000),'','[Browse all four-brand platform formats](gallery/neon-01-Ecosystem-Four-Brands.md)','','### Five brands','',img(Path('social-banners/02-Ecosystem-Five-Brands/Master/reference-wide-master.png'),'Five-brand neon reference composition',1000),'','[Browse all five-brand platform formats](gallery/neon-02-Ecosystem-Five-Brands.md)','','## Neon social banner collections','','| Collection | Compositions | Platforms |','|---|---:|---|']
for p in collections:rows+=[f'| [{p.name[3:].replace("-"," ")}](gallery/neon-{p.name}.md) | {counts[p.name]} | Facebook, X, YouTube, TikTok, Instagram, Rumble |']
rows+=['','[Neon preview PDF](social-banners/08-Previews/Neon-Social-Banners-Preview.pdf)','','## Brand-system galleries','','Includes social graphics, announcements, avatars, document headers, Discord emojis and stickers, and letterheads.','','| Brand | Contact-sheet preview |','|---|---|']
for key,name,folder in brands:
    rel=Path('brand-system/07-Previews-and-Contact-Sheets')/(key+'-discord-contact-sheet.png')
    rows+=[f'| [{name}](gallery/brand-system-{key}.md) | <a href="gallery/brand-system-{key}.md"><img src="{url(rel)}" alt="{name} Discord contact sheet" width="320"></a> |']
rows+=['','[Ecosystem-wide brand-system images](gallery/brand-system-ecosystem.md) · [Complete brand-system preview PDF](brand-system/07-Previews-and-Contact-Sheets/Complete-Preview-Book.pdf)','','## Source identity sheet','',img(Path('brand-system/00-Brand-Guide-and-Audit/Five-Brand-Identity-Sheet.png'),'Five-brand source identity sheet',900),'','[Inspect all original mark variants](gallery/source-brand-marks.md) · [Identity sheet PDF](brand-system/00-Brand-Guide-and-Audit/Five-Brand-Identity-Sheet.pdf)','']
(repo/'GALLERY.md').write_text('\n'.join(rows))
print(json.dumps({'gallery_files':len(list(g.glob('*.md'))),'neon_compositions':sum(counts.values()),'brand_family_pngs':brand_count,'ecosystem_brand_system_pngs':len(list((br/'06-Ecosystem-Wide').glob('*/*.png'))),'top_gallery':'GALLERY.md'},indent=2))
