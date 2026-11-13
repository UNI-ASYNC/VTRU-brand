from pathlib import Path
import json,csv,zipfile,hashlib,xml.etree.ElementTree as ET,re,collections,subprocess,concurrent.futures,os
from PIL import Image,ImageChops,ImageStat,ImageColor
ROOT=Path('/workspace')
BASE=ROOT/'work/source'
TMP=ROOT/'work/audit-renders';TMP.mkdir(exist_ok=True)

def sha(data): return hashlib.sha256(data).hexdigest()
def tag(e):return e.tag.rsplit('}',1)[-1]
def hex_color(x):
    x=x.strip()
    if x.startswith('rgb('):
        vals=x[4:-1].split(',')
        return '#'+''.join(f'{max(0,min(255,round(float(v.strip().rstrip("%"))*(2.55 if "%" in v else 1)))):02X}' for v in vals)
    try:return '#'+''.join(f'{v:02X}' for v in ImageColor.getrgb(x))
    except:return None

def colors_svg(root):
    fills=[];grads=[];allhex=set()
    for e in root.iter():
        if tag(e) in ['linearGradient','radialGradient']:
            stops=[]
            for s in e:
                style=dict(re.findall(r'([\w-]+)\s*:\s*([^;]+)',s.get('style','')))
                c=s.get('stop-color',style.get('stop-color',''))
                item={'offset':s.get('offset'),'color':c,'hex_rounded_srgb':hex_color(c),'opacity':s.get('stop-opacity',style.get('stop-opacity','1'))}
                if item['hex_rounded_srgb']:allhex.add(item['hex_rounded_srgb'])
                stops.append(item)
            grads.append({'type':tag(e),'id':e.get('id'),'attributes':e.attrib,'stops':stops})
        for key in ['fill','stroke','stop-color']:
            if e.get(key): fills.append(e.get(key))
        fills+=re.findall(r'(?:fill|stroke|stop-color)\s*:\s*([^;}]+)',e.get('style',''))
        if tag(e)=='style': fills+=re.findall(r'(?:fill|stroke|stop-color)\s*:\s*([^;}]+)',e.text or '')
    for f in fills:
        c=hex_color(f)
        if c:allhex.add(c)
    return sorted(set(fills)),sorted(allhex),grads

def render_compare(item):
    brand=item['brand'];name=item['source_filename'];svg=BASE/brand/name
    target=TMP/f'{brand}__{svg.stem}.png'
    env=os.environ.copy();env['XDG_CACHE_HOME']=str(TMP/'cache')
    p=subprocess.run(['inkscape',str(svg),'--export-type=png','--export-width=512','--export-filename='+str(target)],capture_output=True,text=True,env=env)
    if p.returncode:return {'source_filename':name,'render_ok':False,'error':p.stderr[-1000:]}
    rendered=Image.open(target).convert('RGBA');png=Image.open(svg.with_suffix('.png')).convert('RGBA').resize(rendered.size,Image.Resampling.LANCZOS)
    # Compare full canvas; output by source-supplied PNGs can differ at antialiased edges.
    diffs=[]
    for color in [(255,255,255,255),(18,24,39,255)]:
        bg=Image.new('RGBA',rendered.size,color)
        a=Image.alpha_composite(bg,rendered).convert('RGB');b=Image.alpha_composite(bg,png).convert('RGB')
        diffs.append(sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3)
    return {'source_filename':name,'render_ok':True,'comparison_width_px':512,'mean_abs_channel_difference_on_white':round(diffs[0],4),'mean_abs_channel_difference_on_dark':round(diffs[1],4),'interpretation':'Rendered SVG compared against corresponding supplied PNG resized with Lanczos; low differences are rasterization differences, not a legal or authorship check.'}

records=[];zipchecks=[]
for zpath in sorted((ROOT/'attachments').glob('*/*.zip')):
    brand=zpath.name.split('-brandkit')[0]
    with zipfile.ZipFile(zpath) as z:
        crc=z.testzip();contents=z.infolist()
        zipchecks.append({'archive':zpath.name,'sha256':sha(zpath.read_bytes()),'bytes':zpath.stat().st_size,'file_count':len(contents),'crc_check':'pass' if crc is None else crc,'path_safety':all('/' not in x.filename and '\\' not in x.filename for x in contents)})
        for member in contents:
            data=z.read(member.filename);p=BASE/brand/member.filename
            item={'brand':brand,'archive':zpath.name,'source_filename':member.filename,'sha256':sha(data),'bytes':len(data),'extracted_matches_archive':p.read_bytes()==data,'format':p.suffix[1:].upper()}
            if p.suffix=='.png':
                with Image.open(p) as im:
                    im.verify()
                with Image.open(p) as im:
                    rgba=im.convert('RGBA');bbox=rgba.getchannel('A').getbbox()
                    item.update(width=im.width,height=im.height,mode=im.mode,alpha_bbox=list(bbox) if bbox else None,has_transparency=rgba.getchannel('A').getextrema()[0]<255)
            else:
                root=ET.fromstring(data);fills,colors,grads=colors_svg(root)
                refs=[];active=[]
                for e in root.iter():
                    if tag(e) in ['script','foreignObject']:active.append(tag(e))
                    for k,v in e.attrib.items():
                        if k.lower().startswith('on'):active.append(k)
                        if k.rsplit('}',1)[-1] in ['href','src'] and not v.startswith('#'):refs.append(v)
                text=data.decode('utf-8')
                css_external=re.findall(r'url\(\s*[\'\"]?((?!#)[^)\s]+)',text)
                refs.extend(css_external)
                vb=[float(v) for v in root.get('viewBox','').split()]
                item.update(viewBox=root.get('viewBox'),viewBox_values=vb,aspect_ratio=vb[2]/vb[3] if len(vb)==4 else None,element_counts=dict(collections.Counter(tag(e) for e in root.iter())),fill_and_stroke_tokens=fills,colors_srgb_hex_rounded=colors,gradients=grads,active_content=active,external_references=refs,contains_live_text=any(tag(e)=='text' for e in root.iter()),path_geometry_sha256=sha(('\n'.join(e.get('d','') for e in root.iter() if tag(e)=='path')).encode()))
            records.append(item)
comparisons=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(render_compare,[r for r in records if r['format']=='SVG']))
issues=[
{'brand':'aiwars','severity':'production_note','finding':'The supplied aiwars-logomark.svg contains the full AI Wars wordmark, with the same viewBox and path geometry as aiwars-logo.svg. Circle/square variants add a square viewport around that same wordmark; they are not an isolated icon.','action':'Use this exact wordmark with adequate light space. Do not invent an A, slash, or compact symbol as the official logomark.'},
{'brand':'verticalfoundation','severity':'production_note','finding':'The full Foundation logo is approximately 1.59:1 and includes the organization name below the architectural symbol; the supplied logomark omits that wording but retains a 1.59:1 artboard.','action':'Respect aspect ratio and allow greater header height; do not squeeze it into the proportions of the other horizontal wordmarks.'},
{'brand':'all','severity':'production_note','finding':'Source -circle and -square filenames refer to viewport sizing and spacing. They do not guarantee an added circular/square background or circle-safe crop.','action':'Place exact source artwork within a padded avatar canvas and evaluate circular crop separately; retain full source viewBox.'},
{'brand':'vitruveo','severity':'production_note','finding':'The supplied circular brand symbol consists of six paths with magenta-to-cyan radial gradients and transparent negative-space separators.','action':'Embed intact source SVG or an exact supplied raster, preserving the six-path geometry. Never draw a replacement circle or fill its negative spaces.'},
{'brand':'all','severity':'scope_note','finding':'Files are verified against the user-supplied archives. The audit does not establish copyright ownership, trademark permissions, or whether an archive is a brand owner’s latest master.','action':'Describe status as source-matched artwork and derivative layout, without claiming owner approval.'}
]
primary={}
for brand in sorted(x.name for x in BASE.iterdir()):
    r=next(r for r in records if r['source_filename']==brand+'-logo.svg')
    primary[brand]={'source':r['source_filename'],'flat_colors_exact_tokens':[x for x in r['fill_and_stroke_tokens'] if not x.startswith('url(')],'gradient_endpoints':[{'id':g['id'],'first':g['stops'][0] if g['stops'] else None,'last':g['stops'][-1] if g['stops'] else None} for g in r['gradients']],'note':'All tokens come from primary supplied SVG; hex values are rounded sRGB representations. Supporting layout colors are not source-defined official brand colors.'}
summary={'archive_count':len(zipchecks),'source_file_count':len(records),'svg_count':sum(r['format']=='SVG' for r in records),'png_count':sum(r['format']=='PNG' for r in records),'all_extracted_hashes_match':all(r['extracted_matches_archive'] for r in records),'all_archives_crc_valid':all(z['crc_check']=='pass' for z in zipchecks),'active_content_count':sum(len(r.get('active_content',[])) for r in records),'external_reference_count':sum(len(r.get('external_references',[])) for r in records),'all_svg_renders_pass':all(r['render_ok'] for r in comparisons),'max_svg_png_mean_difference':max(max(x.get('mean_abs_channel_difference_on_white',0),x.get('mean_abs_channel_difference_on_dark',0)) for x in comparisons)}
out={'audit_basis':'User-supplied ZIP bytes; no external authorization or brand-standard assertions.','summary':summary,'archives':zipchecks,'findings':issues,'source_palettes':primary,'svg_png_comparisons':comparisons,'files':records}
(ROOT/'work/source-audit.json').write_text(json.dumps(out,indent=2))
cols=['brand','archive','source_filename','format','sha256','bytes','extracted_matches_archive','width','height','viewBox','aspect_ratio','element_counts','active_content','external_references','colors_srgb_hex_rounded']
with (ROOT/'work/source-inventory.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
    for r in records:
        w.writerow({k:(json.dumps(r[k],ensure_ascii=False) if isinstance(r.get(k),(dict,list)) else r.get(k,'')) for k in cols})
print(json.dumps(summary,indent=2))
print('Highest differences:')
for x in sorted(comparisons,key=lambda x:max(x.get('mean_abs_channel_difference_on_white',0),x.get('mean_abs_channel_difference_on_dark',0)),reverse=True)[:8]:print(x)
