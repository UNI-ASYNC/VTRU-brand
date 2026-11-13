from pathlib import Path
import base64,html,hashlib,os,subprocess,xml.etree.ElementTree as ET

BASE=Path('/workspace/work')
SOURCE=BASE/'source'
ROOT=BASE/'brand-system'
FONT='DejaVu Sans'
BRANDS=[
 dict(id='vitruveo',name='Vitruveo',folder='01-Vitruveo',accent='#7B64F5',secondary='#39BEEB',ink='#19162E',pale='#F4F1FC',descriptor='NETWORK / INFRASTRUCTURE',headline=['A connected','future.']),
 dict(id='verticalfoundation',name='Vertical Foundation',folder='02-Vertical-Foundation',accent='#7C827F',secondary='#B5A88C',ink='#293A34',pale='#F2F5F0',descriptor='FOUNDATION / COMMUNITY',headline=['Progress,','together.']),
 dict(id='pretrend',name='Pretrend',folder='03-Pretrend',accent='#0056BB',secondary='#7AC543',ink='#102C37',pale='#F0F7F4',descriptor='TRENDS / PERSPECTIVE',headline=['Follow the','possibilities.']),
 dict(id='aiwars',name='AI Wars',folder='04-AI-Wars',accent='#0B5CFF',secondary='#A3C5FF',ink='#060B14',pale='#F0F4FF',descriptor='PLAY / COMPETE / CONNECT',headline=['Make your','next move.']),
 dict(id='vtruscope',name='VTRU Scope',folder='05-VTRU-Scope',accent='#8D5CF5',secondary='#22BCEB',ink='#1B1835',pale='#F4F2FC',descriptor='DISCOVERY / PERSPECTIVE',headline=['See the','bigger picture.'])
]
BY_ID={b['id']:b for b in BRANDS}
def esc(v):return html.escape(str(v),quote=True)
def rect(x,y,w,h,fill,rx=0,**attrs):
    a=' '.join(f'{k.replace("_","-")}="{esc(v)}"' for k,v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {a}/>'
def text(x,y,value,size=24,fill='#191C26',weight=400,anchor='start',**attrs):
    a=' '.join(f'{k.replace("_","-")}="{esc(v)}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {a}>{esc(value)}</text>'
def svg(w,h,body,title='Brand system design'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{esc(title)}</title>{body}</svg>'
def source_path(b,variant='logo'):
    key=b['id'] if isinstance(b,dict) else b
    return SOURCE/key/f'{key}-{variant}.svg'
def logo(b,x,y,w,h,variant='logo'):
    p=source_path(b,variant)
    data=base64.b64encode(p.read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/svg+xml;base64,{data}"/>'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def render(path,png=True,pdf=False,dpi=None):
    path=Path(path);env=os.environ.copy();env['XDG_CACHE_HOME']='/workspace/work/cache'
    Path(env['XDG_CACHE_HOME']).mkdir(exist_ok=True)
    results=[]
    for ext,do in [('png',png),('pdf',pdf)]:
        if not do:continue
        dest=path.with_suffix('.'+ext)
        cmd=['inkscape',str(path),'--export-type='+ext,'--export-filename='+str(dest),'--export-area-page']
        if dpi and ext=='png':cmd+=['--export-dpi='+str(dpi)]
        if ext=='pdf':cmd+=['--export-text-to-path']
        r=subprocess.run(cmd,env=env,capture_output=True,text=True)
        if r.returncode:raise RuntimeError(r.stderr[-1500:])
        if not dest.exists():raise RuntimeError('Missing '+str(dest))
        results.append(dest)
    return results
def write_design(path,w,h,body,title='Brand system design',png=True,pdf=False):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(svg(w,h,body,title))
    return [path]+render(path,png=png,pdf=pdf)
def record(paths,b,category,variant='logo',**extra):
    p=source_path(b,variant)
    return [dict(path=str(Path(f).relative_to(ROOT)),brand=b['id'],category=category,source_file=p.name,source_sha256=sha(p),classification='derivative artwork; embedded source logo unchanged',owner_review='layout and copy',**extra) for f in paths]
