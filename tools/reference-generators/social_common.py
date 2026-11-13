from pathlib import Path
import sys,os,base64,json,math,hashlib,subprocess,html
sys.path.insert(0,str(Path(__file__).parent))
from brand_common import BRANDS,BY_ID,SOURCE,esc,rect,logo,source_path,sha

ROOT=Path('/workspace/work/Neon-Social-Banner-Pack')
GUIDE=ROOT/'00-Guide-and-Audit'
BACK=GUIDE/'Backgrounds'
SPECS=[
 dict(platform='Facebook',name='facebook-page-cover',w=1702,h=630,surface='Page cover',layout='wide',safe=[320,80,1140,470]),
 dict(platform='Facebook',name='facebook-cover-mobile-friendly',w=1640,h=720,surface='Alternate Page cover',layout='wide',safe=[300,100,1060,520]),
 dict(platform='Facebook',name='facebook-feed-landscape',w=1200,h=630,surface='Feed landscape',layout='landscape',safe=[60,50,1080,530]),
 dict(platform='X',name='x-profile-banner',w=1500,h=500,surface='Profile header',layout='x',safe=[380,65,1060,360]),
 dict(platform='YouTube',name='youtube-channel-banner',w=2560,h=1440,surface='Channel banner',layout='youtube',safe=[508,509,1544,422]),
 dict(platform='YouTube',name='youtube-video-thumbnail',w=1280,h=720,surface='Video thumbnail',layout='landscape',safe=[50,50,1180,610]),
 dict(platform='TikTok',name='tiktok-vertical-cover',w=1080,h=1920,surface='Vertical content cover',layout='vertical',safe=[108,270,800,1230]),
 dict(platform='Instagram',name='instagram-feed-square',w=1080,h=1080,surface='Square feed post',layout='square',safe=[65,65,950,950]),
 dict(platform='Instagram',name='instagram-feed-portrait',w=1080,h=1350,surface='Portrait feed post',layout='portrait',safe=[75,120,930,1110]),
 dict(platform='Instagram',name='instagram-story-reel-cover',w=1080,h=1920,surface='Story / Reel cover',layout='vertical',safe=[90,270,850,1230]),
 dict(platform='Rumble',name='rumble-channel-backsplash',w=3600,h=600,surface='Channel backsplash',layout='rumble',safe=[850,100,2250,400]),
]
FONT='DejaVu Sans'
def text(x,y,t,size=24,fill='#FFFFFF',weight=400,anchor='start',**attrs):
    a=' '.join(f'{k.replace("_","-")}="{esc(v)}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {a}>{esc(t)}</text>'
DEFS='''<defs>
 <linearGradient id="panelLine" x1="0" y1="1" x2="1" y2="0"><stop stop-color="#3695E7"/><stop offset=".6" stop-color="#58E5F1"/><stop offset="1" stop-color="#89E046"/></linearGradient>
 <linearGradient id="headlineLight"><stop stop-color="#22CFFF"/><stop offset=".4" stop-color="#EEE8FF"/><stop offset="1" stop-color="#B5EF99"/></linearGradient>
 <linearGradient id="hairline"><stop stop-color="#176DD1" stop-opacity="0"/><stop offset=".5" stop-color="#4CEBFF"/><stop offset="1" stop-color="#65DF89" stop-opacity="0"/></linearGradient>
 <filter id="softGlow" x="-.5" y="-.7" width="2" height="2.4"><feGaussianBlur stdDeviation="9"/></filter>
 </defs>'''
def svg(w,h,body,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{esc(title)}</title>{DEFS}{body}</svg>'
def background(w,h):
    name='portrait.png' if h>w else 'wide.png'
    return rect(0,0,w,h,'#020D24')+f'<image x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" xlink:href="../../00-Guide-and-Audit/Backgrounds/{name}"/>'
def card(x,y,w,h,rx=None):
    rx=rx if rx is not None else min(w,h)*.17
    return rect(x,y,w,h,'#021121',rx,fill_opacity='.80',stroke='url(#panelLine)',stroke_width=1.8)
def rule(x,y,w):
    return rect(x,y-5,w,10,'url(#hairline)',4,filter='url(#softGlow)')+rect(x,y,w,1.6,'url(#hairline)')
def featuring(x,y,label='NOW FEATURING',size=18):
    return f'<circle cx="{x}" cy="{y-size*.35}" r="{size*.25}" fill="#A0FF59"/>'+f'<circle cx="{x}" cy="{y-size*.35}" r="{size*.4}" fill="#A0FF59" opacity=".6" filter="url(#softGlow)"/>'+text(x+size*1.2,y,label,size,'#E1F6FF',700,letter_spacing=size*.22)
def guide(spec):
    x,y,w,h=spec['safe'];return '<g id="layout-guide" style="display:none">'+rect(x,y,w,h,'none',stroke='#F44FAD',stroke_width=2)+'</g>'
def output_paths(collection,spec):
    return ROOT/collection/spec['platform']/f'{spec["name"]}.svg'
def save_design(collection,spec,body,sources):
    p=output_paths(collection,spec);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(svg(spec['w'],spec['h'],background(spec['w'],spec['h'])+body+guide(spec),collection+' '+spec['surface']))
    return dict(path=str(p.relative_to(ROOT)),png_path=str(p.with_suffix('.png').relative_to(ROOT)),collection=collection,platform=spec['platform'],width=spec['w'],height=spec['h'],surface=spec['surface'],safe=spec['safe'],sources=[dict(file=source_path(b,v).name,sha256=sha(source_path(b,v))) for b,v in sources],status='derivative layout; original logo bytes embedded unchanged')
def render(p):
    p=Path(p);env=os.environ.copy();env['XDG_CACHE_HOME']='/workspace/work/cache'
    r=subprocess.run(['inkscape',str(p),'--export-area-page','--export-type=png','--export-filename='+str(p.with_suffix('.png'))],capture_output=True,text=True,env=env)
    if r.returncode:raise RuntimeError(r.stderr[-1500:])
    return p.with_suffix('.png')
