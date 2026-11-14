"""Build V2 supplemental source-only templates; preserve every V1 artifact."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,xml.etree.ElementTree as ET
from PIL import Image
from v2_common import *

BASE=V2/'supplemental'
RECORDS=[]

def fit_logo(b,x,y,maxw,maxh,variant='logo',center=False):
    r=ET.parse(source_path(b,variant)).getroot()
    _,_,vw,vh=[float(v) for v in r.get('viewBox').replace(',',' ').split()]
    w=min(maxw,maxh*vw/vh);h=w*vh/vw
    if center:x-=w/2
    return logo(b,x,y,w,h,variant)

def write(b,category,name,w,h,body,art_area=None,variant='logo',copy=False,transparent=False):
    p=BASE/b['id']/category/f'{b["id"]}-{name}.svg'
    r=save_design(p,w,h,body,f'{b["name"]} — {name.replace("-"," ")}',[(b,variant)],art_area,transparent,category=category,copy_ids=[b['id']] if copy else [])
    r.update(brand=b['id'],layout=name)
    if b['id']=='vtruscope':
        q=source_path(b,variant,'png')
        r['png_source_override']={'file':q.name,'sha256':sha(q),'role':'Exact supplied high-resolution paired PNG for raster export only; SVG master keeps exact source SVG.'}
    RECORDS.append(r)

def announcements(b):
    # The brackets mark editable content fields, not newly authored campaign copy.
    mark=fit_logo(b,85,65,520,180)
    body=mark+text(85,325,'[Date]',21,fill='#555555')+text(85,435,'[Headline]',60,600)+text(85,525,'[Details]',28)
    write(b,'Announcements','announcement-headline-first',1080,1080,body,[85,610,910,375])
    body=mark+text(85,845,'[Headline]',57,600)+text(85,925,'[Details]',27)+text(85,1010,'[Date]',20,fill='#555555')
    write(b,'Announcements','announcement-image-first',1080,1080,body,[85,280,910,450])
    body=mark+text(85,385,'[Headline]',53,600)+text(85,465,'[Details]',26)+text(85,960,'[Date]',20,fill='#555555')
    write(b,'Announcements','announcement-side-image',1080,1080,body,[620,300,375,660])

def headers(b):
    body=fit_logo(b,80,45,580,225)+text(1520,177,'[Document title]',32,500,'end')
    write(b,'Document-Headers','document-header-standard',1600,320,body)
    body=fit_logo(b,80,93,400,135)+text(610,178,'[Document title]',31,500)
    body+='<line x1="80" y1="282" x2="1520" y2="282" stroke="#BBBBBB" stroke-width="1"/>'
    write(b,'Document-Headers','document-header-compact',1600,320,body)

def avatars(b):
    for variant,name in [('logo','avatar-full-logo'),('logomark','avatar-logomark'),('logomark-circle','avatar-source-circle')]:
        body=logo(b,115,115,794,794,variant)
        write(b,'Profile-Images',name,1024,1024,body,variant=variant)

def other_formats(b):
    body=fit_logo(b,350,47,405,155)
    copy,_=copy_block(b,835,85,590,size=24)
    write(b,'LinkedIn','linkedin-company',1512,256,body+copy,[335,28,1105,190],copy=True)
    body=fit_logo(b,410,70,450,185)
    copy,_=copy_block(b,930,112,545,size=28)
    write(b,'LinkedIn','linkedin-personal',1584,396,body+copy,[400,65,1080,255],copy=True)
    body=fit_logo(b,70,65,555,175)
    copy,_=copy_block(b,70,325,820,size=29)
    write(b,'Discord-Server','discord-server-banner',960,540,body+copy,[640,65,250,380],copy=True)
    body=fit_logo(b,120,75,730,230)
    copy,_=copy_block(b,120,415,1000,size=43)
    write(b,'Website','website-hero',1920,640,body+copy,[1190,75,610,490],copy=True)

def main():
    BASE.mkdir(parents=True,exist_ok=True)
    for b in BRANDS:
        announcements(b);headers(b);avatars(b);other_formats(b)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for i,_ in enumerate(pool.map(lambda r:render(V2/r['path']),RECORDS),1):
            if i%10==0:print('Rendered',i,'/',len(RECORDS),flush=True)
    # Each pair is separately recorded, including final bytes/hash and source provenance.
    outputs=[]
    for r in RECORDS:
        for key in ['path','png_path']:
            p=V2/r[key];row=dict(r);row['file']=r[key];row['sha256']=sha(p);row['bytes']=p.stat().st_size;row['type']=p.suffix[1:]
            if key=='path':row.pop('png_source_override',None)
            outputs.append(row)
    (V2/'reports/supplemental-records.json').write_text(json.dumps({'designs':len(RECORDS),'files':outputs},indent=2))
    qc={'designs':len(RECORDS),'pngs':0,'source_svg_matches':0,'errors':[]}
    source_hashes={sha(p) for p in SOURCE.glob('*/*.svg')}
    import base64
    for r in RECORDS:
        with Image.open(V2/r['png_path']) as im:
            if im.size!=(r['width'],r['height']):qc['errors'].append(r['png_path']+' dimensions')
            if im.convert('RGB').getpixel((0,0))!=(255,255,255):qc['errors'].append(r['png_path']+' background')
        qc['pngs']+=1
        root=ET.parse(V2/r['path']).getroot()
        images=root.findall('.//{http://www.w3.org/2000/svg}image')
        for im in images:
            href=im.get(XLINK,'');raw=base64.b64decode(href.split(',',1)[1])
            if hashlib.sha256(raw).hexdigest() not in source_hashes:qc['errors'].append(r['path']+' source image mismatch')
            else:qc['source_svg_matches']+=1
    qc['status']='PASS' if not qc['errors'] else 'FAIL'
    (V2/'reports/supplemental-qc.json').write_text(json.dumps(qc,indent=2))
    (BASE/'README.md').write_text('''# V2 supplemental templates\n\nThese files are neutral, editable layouts using the supplied brand marks. They do not introduce campaign slogans, galaxy/node/grid illustrations, or decorative side panels. V1 is preserved separately as evidence.\n\n- **Announcements:** square post layouts with editable `[Headline]`, `[Date]` and `[Details]` fields. Image placement guides are hidden from PNG exports; the open space is for existing owner-supplied imagery.\n- **Document headers:** standard and compact light-background layouts with an editable document-title field.\n- **Profile images:** three arrangements of existing source logo/logomark variants. No new avatar symbol was invented.\n- **LinkedIn, Discord and website layouts:** format-specific logo placement and wording copied exactly from the current website copy inventory.\n- **Letterheads:** formal, office and technical A4 stationery supplied separately in DOCX, SVG, PDF and 300 dpi PNG.\n\nSVG and DOCX are editable files. PNG and PDF are presentation exports. DejaVu Sans is a neutral template font, not a claim about an official brand typeface. The same exact source SVG is embedded in each SVG master; Scope raster exports use its untouched paired high-resolution source PNG for sharpness.\n\nSee [copy sources](../reports/COPY-SOURCES.md) and the per-file manifests in [reports](../reports/).\n''')
    print(json.dumps(qc,indent=2),flush=True)
if __name__=='__main__':main()
