"""V2 source-only layout helpers. Existing V1 files are never written by this module."""
from pathlib import Path
import base64,html,json,hashlib,os,subprocess,tempfile
from PIL import ImageFont

REPO=Path(__file__).resolve().parents[1]
V2=REPO/'v2'
SOURCE=REPO/'source-brand-kits'/'unpacked'
COPY=json.loads((V2/'reports/current-website-copy.json').read_text())['brands']
BRANDS=[dict(id=k,**COPY[k]) for k in ['vitruveo','verticalfoundation','pretrend','aiwars','vtruscope']]
BY_ID={b['id']:b for b in BRANDS}
FONT='DejaVu Sans'
FONT_DIR=V2/'resources/fonts'
if not FONT_DIR.is_dir():FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
INK='#111111'
XLINK='{http://www.w3.org/1999/xlink}href'

def esc(v):return html.escape(str(v),quote=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def source_path(b,variant='logo',ext='svg'):
    key=b['id'] if isinstance(b,dict) else b
    return SOURCE/key/f'{key}-{variant}.{ext}'
def logo(b,x,y,w,h,variant='logo'):
    data=base64.b64encode(source_path(b,variant).read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/svg+xml;base64,{data}"/>'
def rect(x,y,w,h,fill='#FFFFFF',**attrs):
    a=' '.join(f'{k.replace("_","-")}="{esc(v)}"' for k,v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {a}/>'
def text(x,y,value,size=24,weight=400,anchor='start',fill=INK,**attrs):
    a=' '.join(f'{k.replace("_","-")}="{esc(v)}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {a}>{esc(value)}</text>'
def lines(value,size,width,weight=400):
    f=ImageFont.truetype(str(FONT_DIR/('DejaVuSans'+('-Bold' if weight>=600 else '')+'.ttf')),max(1,int(size)))
    result=[];line=''
    for word in value.split():
        new=(line+' '+word).strip()
        if line and f.getlength(new)>width:result.append(line);line=word
        else:line=new
    if line:result.append(line)
    return result
def copy_block(b,x,y,width,size=32,weight=400,anchor='start',leading=1.32):
    value=b['headline'];ls=lines(value,size,width,weight)
    return ''.join(text(x,y+i*size*leading,t,size,weight,anchor) for i,t in enumerate(ls)),len(ls)*size*leading
def svg(w,h,body,title,art_area=None,transparent=False):
    bg='' if transparent else rect(0,0,w,h)
    guide=''
    if art_area:
        x,y,aw,ah=art_area
        guide=f'<g inkscape:groupmode="layer" inkscape:label="Image placement guide (hidden in export)" id="image-placement-guide" style="display:none">{rect(x,y,aw,ah,"none",stroke="#999999",stroke_width=1)}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{esc(title)}</title>{bg}<g id="client-artwork" inkscape:groupmode="layer" inkscape:label="Owner imagery (empty)"><desc>Reserved for existing owner-supplied imagery; intentionally empty.</desc></g><g id="brand-layout" inkscape:groupmode="layer" inkscape:label="Supplied logo and verified copy">{body}</g>{guide}</svg>'
def save_design(path,w,h,body,title,brands,art_area=None,transparent=False,category='social',copy_ids=None):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(svg(w,h,body,title,art_area,transparent))
    sources=[]
    for b,v in brands:
        q=source_path(b,v);sources.append({'file':q.name,'sha256':sha(q)})
    row=dict(path=str(p.relative_to(V2)),png_path=str(p.with_suffix('.png').relative_to(V2)),width=w,height=h,title=title,category=category,sources=sources,copy_ids=copy_ids or [],imagery='supplied source marks only; client artwork area intentionally empty',background='transparent' if transparent else 'white',status='V2 editable layout; no invented slogans or decorative imagery')
    row['png_source_overrides']=[{'file':source_path(b,v,'png').name,'sha256':sha(source_path(b,v,'png')),'reason':'Untouched paired high-resolution source PNG for Scope raster sharpness; SVG master keeps untouched SVG.'} for b,v in brands if b['id']=='vtruscope']
    return row
def render(path,pdf=False,dpi=None):
    p=Path(path);env=os.environ.copy()
    cache=Path(env.get('XDG_CACHE_HOME',tempfile.gettempdir()))/'vtru-brand-v2-cache'
    cache.mkdir(parents=True,exist_ok=True);env['XDG_CACHE_HOME']=str(cache)
    # Render the small-viewBox Scope mark using its untouched, paired high-resolution PNG.
    # The editable SVG continues to embed the untouched source SVG.
    data=p.read_text();changed=False
    for v in ['logo','logo-dark','logo-white','logo-bw','logomark','logomark-circle','logomark-square']:
        s=source_path('vtruscope',v);old='data:image/svg+xml;base64,'+base64.b64encode(s.read_bytes()).decode()
        if old in data:
            q=source_path('vtruscope',v,'png')
            data=data.replace(old,'data:image/png;base64,'+base64.b64encode(q.read_bytes()).decode());changed=True
    temp=None;input_path=p
    if changed:
        with tempfile.NamedTemporaryFile('w',suffix='.svg',prefix='v2-render-',delete=False) as f:f.write(data);temp=Path(f.name)
        input_path=temp
    outputs=[]
    try:
        for ext in ['png']+(['pdf'] if pdf else []):
            out=p.with_suffix('.'+ext);cmd=['inkscape',str(input_path),'--export-area-page','--export-type='+ext,'--export-filename='+str(out)]
            if dpi and ext=='png':cmd.append('--export-dpi='+str(dpi))
            if ext=='pdf':cmd.append('--export-text-to-path')
            r=subprocess.run(cmd,capture_output=True,text=True,env=env)
            if r.returncode:raise RuntimeError(r.stderr[-2000:])
            outputs.append(out)
    finally:
        if temp:temp.unlink(missing_ok=True)
    return outputs
