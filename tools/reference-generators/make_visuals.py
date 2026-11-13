import sys,json,math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from PIL import ImageFont
from brand_common import *

RECORDS=[];JOBS=[]
def fit(value,size,width):
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',100)
    return min(size,width*100/f.getlength(value))
def queue(path,w,h,body,title,b=None,category='social',variant='logo',pdf=False,**extra):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(svg(w,h,body,title))
    JOBS.append((path,pdf))
    paths=[path,path.with_suffix('.png')]+([path.with_suffix('.pdf')] if pdf else [])
    if b:RECORDS.extend(record(paths,b,category,variant,**extra))
    else:
        sources=[dict(file=source_path(br,variant).name,sha256=sha(source_path(br,variant))) for br in extra.pop('brands',BRANDS)]
        RECORDS.extend(dict(path=str(p.relative_to(ROOT)),brand='ecosystem',category=category,classification='derivative artwork; embedded source logos unchanged',source_assets=sources,owner_review='layout and copy',**extra) for p in paths)

def motif(b,x,y,w,h,dark=False):
    a=b['accent'];s=b['secondary'];ink='#FFFFFF' if dark else b['ink'];out=''
    # Themes are separate artwork, never a reconstruction of a protected mark.
    if b['id']=='vitruveo':
        for k in range(3):
            out+=f'<ellipse cx="{x+w*.53}" cy="{y+h*.5}" rx="{w*(.24+k*.10)}" ry="{h*(.14+k*.10)}" fill="none" stroke="{ink}" opacity="{.10+k*.04}" stroke-width="2" transform="rotate(-25 {x+w*.53} {y+h*.5})"/>'
        pts=[(.12,.53),(.37,.22),(.61,.4),(.88,.12),(.8,.78),(.43,.87)]
        for i,j in [(0,1),(1,2),(2,3),(2,4),(4,5),(0,5),(1,5)]:
            p,q=pts[i],pts[j];out+=f'<path d="M{x+p[0]*w},{y+p[1]*h} L{x+q[0]*w},{y+q[1]*h}" stroke="{ink}" stroke-width="2" fill="none" opacity=".22"/>'
        for i,(u,v) in enumerate(pts):out+=f'<circle cx="{x+u*w}" cy="{y+v*h}" r="{min(w,h)*(.032 if i%2 else .047)}" fill="{s if i%2 else ink}"/>'
    elif b['id']=='verticalfoundation':
        for k in range(6):
            xx=x+w*(.08+k*.145);hh=h*(.22+(k%3)*.18)
            out+=rect(xx,y+h*.82-hh,w*.09,hh,ink,opacity=.12+(k%3)*.10)
            out+=f'<path d="M{xx},{y+h*.82-hh} l{w*.04},-{w*.03} h{w*.09} l-{w*.04},{w*.03}" fill="{s}" opacity=".65"/>'
        out+=f'<path d="M{x+w*.03},{y+h*.88} H{x+w*.96}" stroke="{ink}" opacity=".35" stroke-width="2"/>'
    elif b['id']=='pretrend':
        for k in range(1,6):out+=f'<path d="M{x},{y+h*k/6}H{x+w} M{x+w*k/6},{y}V{y+h}" stroke="{ink}" opacity=".08" stroke-width="1"/>'
        pts=[(0,.83),(.15,.66),(.29,.73),(.44,.39),(.6,.48),(.75,.19),(1,.08)]
        line=' '.join(f'{x+u*w},{y+v*h}' for u,v in pts)
        out+=f'<polyline points="{line}" fill="none" stroke="{s}" stroke-width="{max(3,w*.012)}" stroke-linecap="round" stroke-linejoin="round"/>'
        out+=f'<circle cx="{x+w}" cy="{y+h*.08}" r="{max(5,w*.02)}" fill="{ink}"/>'
    elif b['id']=='aiwars':
        for k in range(5):
            xx=x+k*w*.22
            out+=f'<path d="M{xx+w*.17},{y+h*.1} H{xx+w*.27} L{xx+w*.01},{y+h*.9} H{xx-w*.09} Z" fill="{ink}" opacity="{.11+k*.045}"/>'
        for k in range(3):out+=rect(x+w*.56+k*w*.12,y+h*.38,w*.07,h*.06,s)
    else:
        cx=x+w*.54;cy=y+h*.49
        for k in range(1,5):out+=f'<circle cx="{cx}" cy="{cy}" r="{min(w,h)*(.09*k)}" fill="none" stroke="{ink}" opacity="{.10+k*.025}" stroke-width="2"/>'
        out+=f'<path d="M{cx},{cy} L{cx+w*.24},{cy-h*.28} A{min(w,h)*.38},{min(w,h)*.38} 0 0 1 {cx+w*.33},{cy+h*.13} Z" fill="{s}" opacity=".35"/>'
        for u,v in [(.3,.3),(.7,.43),(.45,.77)]:out+=f'<circle cx="{x+w*u}" cy="{y+h*v}" r="{max(5,w*.016)}" fill="{ink}"/>'
    return out

SIZES=[('x-banner',1500,500),('facebook-cover',1640,720),('linkedin-company',1512,256),('linkedin-personal',1584,396),('discord-server',960,540),('website-hero',1920,640),('social-square',1080,1080),('social-landscape',1200,630),('story-vertical',1080,1920)]
def social(b,name,w,h):
    ink=b['ink'];a=b['accent'];p=b['pale'];s=b['secondary']
    out=rect(0,0,w,h,p)
    # Different aspect families are individually laid out.
    if h/w<.22:
        out+=rect(w*.73,0,w*.27,h,ink)+motif(b,w*.77,h*.08,w*.20,h*.84,True)
        out+=logo(b,w*.23,h*.15,w*.26,h*.70)
        out+=rect(w*.53,h*.24,2,h*.52,a)
        fs=min(fit(t,h*.12,w*.15) for t in b['headline'])
        out+=text(w*.57,h*.43,b['headline'][0],fs,ink,700)+text(w*.57,h*.60,b['headline'][1],fs,ink,700)
    elif name in ['x-banner','linkedin-personal']:
        out+=rect(w*.76,0,w*.24,h,ink)+motif(b,w*.78,h*.14,w*.20,h*.72,True)
        out+=logo(b,w*.28,h*.14,w*.27,h*.57)
        fs=min(fit(t,h*.085,w*.17) for t in b['headline'])
        out+=text(w*.57,h*.39,b['headline'][0],fs,ink,700)+text(w*.57,h*.52,b['headline'][1],fs,ink,700)
        out+=rect(w*.28,h*.81,w*.10,4,a)
    elif name=='facebook-cover':
        out+=rect(w*.76,0,w*.24,h,ink)+motif(b,w*.77,h*.18,w*.21,h*.64,True)
        out+=logo(b,w*.24,h*.18,w*.30,h*.47)
        fs=min(fit(t,h*.075,w*.18) for t in b['headline'])
        out+=text(w*.56,h*.37,b['headline'][0],fs,ink,700)+text(w*.56,h*.49,b['headline'][1],fs,ink,700)
        out+=text(w*.56,h*.65,'ECOSYSTEM / COMMUNITY',h*.023,a,700,letter_spacing=2)
    elif h>w*1.3:
        out+=rect(0,h*.65,w,h*.35,ink)+motif(b,w*.1,h*.69,w*.8,h*.27,True)
        out+=logo(b,w*.12,h*.12,w*.68,h*.18)
        out+=text(w*.12,h*.37,b['headline'][0],w*.090,ink,700)+text(w*.12,h*.43,b['headline'][1],w*.090,ink,700)
        out+=rect(w*.12,h*.49,w*.16,7,a)
        out+=text(w*.12,h*.55,b['descriptor'],w*.021,ink,500,letter_spacing=2)
    elif h>=w*.9:
        out+=rect(w*.60,h*.38,w*.4,h*.62,ink)+motif(b,w*.62,h*.49,w*.34,h*.40,True)
        out+=logo(b,w*.09,h*.08,w*.58,h*.24)
        fs=min(fit(t,w*.066,w*.48) for t in b['headline'])
        out+=text(w*.09,h*.50,b['headline'][0],fs,ink,700)+text(w*.09,h*.59,b['headline'][1],fs,ink,700)
        out+=rect(w*.09,h*.69,w*.11,6,a)
        out+=text(w*.09,h*.84,'COMMUNITY / ECOSYSTEM',w*.018,ink,700,letter_spacing=1)
    else:
        out+=rect(w*.67,0,w*.33,h,ink)+motif(b,w*.7,h*.13,w*.27,h*.75,True)
        out+=logo(b,w*.07,h*.12,w*.42,h*.30)
        out+=text(w*.07,h*.60,b['headline'][0],min(h*.105,w*.053),ink,700)+text(w*.07,h*.74,b['headline'][1],min(h*.105,w*.053),ink,700)
        out+=text(w*.07,h*.90,b['descriptor'],h*.023,a,700,letter_spacing=1.2)
    # Editor-only internal crop guides; hidden in exported graphics.
    out+=f'<g id="crop-guide" style="display:none">{rect(w*.2,h*.16,w*.6,h*.68,"none",stroke="#E64980",stroke_width=2)}</g>'
    queue(ROOT/b['folder']/'Social-Banners'/f'{b["id"]}-{name}.svg',w,h,out,f'{b["name"]} {name}',b,'social',target_width=w,target_height=h,copy_status='proposed sample headline')

def auxiliary(b):
    root=ROOT/b['folder'];ink=b['ink'];a=b['accent'];p=b['pale']
    for style in ['light','dark','framed']:
        bg=ink if style=='dark' else p
        body=rect(0,0,1024,1024,bg)
        if style=='framed':body+=rect(80,80,864,864,'#FFFFFF',120,stroke=a,stroke_width=3)
        v='logo-white' if style=='dark' and b['id']=='aiwars' else 'logomark'
        # All other color marks are readable on both fields; no wordmark introduced.
        body+=logo(b,190,245 if b['id']=='aiwars' else 190,644,534 if b['id']=='aiwars' else 644,v)
        queue(root/'Profile-Images'/f'{b["id"]}-avatar-{style}.svg',1024,1024,body,f'{b["name"]} avatar {style}',b,'profile',variant=v,target_width=1024,target_height=1024)
    for name,title,subtitle in [('announcement','[Announcement title]','[Add the key message here]'),('event','[Event title]','[Date]  /  [Time & time zone]'),('update','[Update title]','[Short summary or next step]')]:
        body=rect(0,0,1080,1080,p)+rect(0,820,1080,260,ink)
        body+=logo(b,90,65,560,245)+text(90,380,name.upper(),19,a,700,letter_spacing=3)
        body+=text(90,485,title,53,ink,700)+text(90,570,subtitle,28,ink)
        body+=rect(90,642,130,6,a)+text(90,733,'[Optional link or call to action]',24,ink)
        body+=motif(b,720,837,290,205,True)+text(90,970,b['name'].upper(),20,'#FFFFFF',700,letter_spacing=2)
        queue(root/'Announcement-Templates'/f'{b["id"]}-{name}.svg',1080,1080,body,f'{b["name"]} editable {name}',b,'announcement',target_width=1080,target_height=1080,copy_status='editable placeholders')
    for style in ['light','dark']:
        body=rect(0,0,1600,320,ink if style=='dark' else '#FFFFFF')
        body+=rect(0,310,1600,10,a)
        v='logo-white' if style=='dark' else 'logo'
        body+=logo(b,90,40,620,230,v)+text(1510,168,'[DOCUMENT TITLE]',30,'#FFFFFF' if style=='dark' else ink,700,'end')
        queue(root/'Document-Headers'/f'{b["id"]}-document-header-{style}.svg',1600,320,body,f'{b["name"]} document header',b,'document-header',variant=v,target_width=1600,target_height=320,copy_status='editable placeholders')

def identity():
    body=rect(0,0,1800,1650,'#F3F4F6')+text(80,100,'Five brands. Original marks.',54,'#161B25',700)
    body+=text(80,150,'SOURCE IDENTITY SHEET  /  VITRUVEO ECOSYSTEM',18,'#647083',700,letter_spacing=3)
    for i,b in enumerate(BRANDS):
        y=200+i*260
        body+=rect(80,y,1640,238,'#FFFFFF',18)
        body+=text(105,y+38,f'0{i+1}',18,b['accent'],700)
        body+=logo(b,160,y+28,520,175)
        body+=rect(740,y+24,210,190,b['ink'],12)+logo(b,765,y+45,160,145,'logo-white')
        body+=text(1010,y+52,b['name'],29,b['ink'],700)
        body+=text(1010,y+90,'Source artwork: unchanged',18,'#536171')
        body+=text(1010,y+124,'Supporting layout colors',15,'#536171')
        for j,c in enumerate([b['accent'],b['secondary'],b['ink'],b['pale']]):
            body+=rect(1010+j*160,y+145,130,24,c,4)+text(1010+j*160,y+195,c,15,'#536171')
    body+=text(80,1570,'Logos retain supplied geometry, aspect ratios, lettering and colors.',22,'#3E4A59')
    body+=text(80,1610,'Layout colors are proposed system tokens. No new ownership or authorization claim is made.',17,'#677382')
    queue(ROOT/'00-Brand-Guide-and-Audit'/'Five-Brand-Identity-Sheet.svg',1800,1650,body,'Five-brand source identity sheet',None,'identity-sheet',pdf=True)

def ecosystem():
    root=ROOT/'06-Ecosystem-Wide'
    originals=[BRANDS[0],BRANDS[2],BRANDS[3],BRANDS[1]]
    for name,w,h,brands in [('four-brand-banner',1920,640,originals),('five-brand-banner',1920,640,BRANDS),('five-brand-social-square',1080,1080,BRANDS)]:
        body=rect(0,0,w,h,'#F4F5F8')
        body+=text(w*.06,h*.15,'VITRUVEO ECOSYSTEM',w*.014,'#655F86',700,letter_spacing=3)
        body+=text(w*.06,h*.31,'Independent identities.',w*.038,'#191A30',700)
        body+=text(w*.06,h*.43,'Shared possibilities.',w*.038,'#191A30',700)
        if w>h:
            gap=22;cw=(w*.88-gap*(len(brands)-1))/len(brands)
            for i,b in enumerate(brands):
                x=w*.06+i*(cw+gap)
                body+=rect(x,h*.57,cw,h*.29,'#FFFFFF',10)+logo(b,x+cw*.1,h*.595,cw*.8,h*.23)
                body+=rect(x,h*.88,cw,3,b['accent'])
        else:
            for i,b in enumerate(brands):
                x=w*.06+(i%2)*w*.455;y=h*.49+(i//2)*h*.145;cw=w*.425
                body+=rect(x,y,cw,h*.125,'#FFFFFF',10)+logo(b,x+cw*.10,y+h*.013,cw*.8,h*.1)
        queue(root/'Multi-Brand-Banners'/f'{name}.svg',w,h,body,name,None,'ecosystem-banner',brands=brands,target_width=w,target_height=h,copy_status='proposed sample headline')
    for name,title in [('announcement','[Ecosystem announcement]'),('event','[Community event]')]:
        body=rect(0,0,1600,900,'#18182C')+text(90,105,'VITRUVEO ECOSYSTEM',24,'#B7A2FF',700,letter_spacing=4)
        body+=text(90,260,title,61,'#FFFFFF',700)+text(90,345,'[Add one clear sentence about the update]',28,'#D0CDE2')
        body+=text(90,470,'[Date / Time / Link]',25,'#FFFFFF')
        for i,b in enumerate(BRANDS):
            x=90+i*289;body+=rect(x,620,266,165,'#FFFFFF',10)+logo(b,x+25,645,216,115)
        queue(root/'Cross-Project-Announcements'/f'ecosystem-{name}.svg',1600,900,body,title,None,'ecosystem-announcement',target_width=1600,target_height=900,copy_status='editable placeholders')

def main():
    identity()
    for b in BRANDS:
        for n,w,h in SIZES:social(b,n,w,h)
        auxiliary(b)
    ecosystem()
    for r in RECORDS:
        if r['category']=='identity-sheet':
            r['source_assets']=[dict(file=source_path(br,v).name,sha256=sha(source_path(br,v))) for br in BRANDS for v in ['logo','logo-white']]
    def run(job):
        p,pdf=job;render(p,pdf=pdf);return str(p.relative_to(ROOT))
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i,r in enumerate(pool.map(run,JOBS)):
            if i%10==0:print(f'Rendered {i+1}/{len(JOBS)} {r}',flush=True)
    (BASE/'visual-records.json').write_text(json.dumps(RECORDS,indent=2))
    print('Done',len(JOBS),'designs',len(RECORDS),'outputs',flush=True)
if __name__=='__main__':main()
