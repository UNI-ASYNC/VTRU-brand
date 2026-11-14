"""Clean social canvases: source marks, verified website wording, open image areas."""
import json,math,xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from v2_common import *

SPECS=[
 dict(platform='Facebook',name='facebook-page-cover',w=1702,h=630,surface='Page cover',layout='wide',safe=[320,80,1140,470]),
 dict(platform='Facebook',name='facebook-cover-mobile-friendly',w=1640,h=720,surface='Alternate Page cover',layout='wide',safe=[300,100,1060,520]),
 dict(platform='Facebook',name='facebook-feed-landscape',w=1200,h=630,surface='Feed landscape post',layout='landscape',safe=[60,50,1080,530]),
 dict(platform='X',name='x-profile-banner',w=1500,h=500,surface='Profile header',layout='wide',safe=[380,65,1060,360]),
 dict(platform='YouTube',name='youtube-channel-banner',w=2560,h=1440,surface='Channel banner',layout='wide',safe=[508,509,1544,422]),
 dict(platform='YouTube',name='youtube-video-thumbnail',w=1280,h=720,surface='Video thumbnail template',layout='landscape',safe=[50,50,1180,610]),
 dict(platform='TikTok',name='tiktok-vertical-cover',w=1080,h=1920,surface='Vertical content cover',layout='vertical',safe=[108,270,800,1230]),
 dict(platform='Instagram',name='instagram-feed-square',w=1080,h=1080,surface='Square feed post',layout='square',safe=[65,65,950,950]),
 dict(platform='Instagram',name='instagram-feed-portrait',w=1080,h=1350,surface='Portrait feed post',layout='portrait',safe=[75,120,930,1110]),
 dict(platform='Instagram',name='instagram-story-reel-cover',w=1080,h=1920,surface='Story / Reel cover',layout='vertical',safe=[90,270,850,1230]),
 dict(platform='Rumble',name='rumble-channel-backsplash',w=3600,h=600,surface='Channel backsplash',layout='wide',safe=[850,100,2250,400]),
]
COLLECTIONS={'vitruveo':'03-Vitruveo','verticalfoundation':'04-Vertical-Foundation','pretrend':'05-Pretrend','aiwars':'06-AI-Wars','vtruscope':'07-VTRU-Scope'}

def place_logo(b,x,y,w,h,center=False):
    root=ET.parse(source_path(b)).getroot();vb=[float(v) for v in root.get('viewBox').split()]
    ratio=vb[2]/vb[3];iw=min(w,h*ratio);ih=iw/ratio
    return logo(b,x+(w-iw)/2 if center else x,y+(h-ih)/2,iw,ih)

def single(b,s):
    x,y,w,h=s['safe'];kind=s['layout'];body=''
    if kind in ['vertical','portrait','square']:
        ly=y+h*.025;lh=h*.19;lw=w*.85
        body+=place_logo(b,x,ly,lw,lh)
        fs=min(48,w*.055)
        cy=y+h*.31
        block,bh=copy_block(b,x,cy,w*.94,fs,400)
        body+=block
        body+=text(x,y+h*.96,b['website'],min(18,w*.021),fill='#555555')
        art=(x,y+h*.53,w,h*.36)
    else:
        body+=place_logo(b,x,y+h*.04,w*.63,h*.36)
        fs=min(42,h*.11)
        block,bh=copy_block(b,x,y+h*.58,w*.67,fs,400)
        body+=block
        body+=text(x,y+h*.96,b['website'],min(18,h*.043),fill='#555555')
        art=(x+w*.72,y+h*.08,w*.27,h*.78)
    return body,art

def ecosystem(s,partners):
    b=BY_ID['vitruveo'];x,y,w,h=s['safe'];kind=s['layout'];body=''
    if kind in ['vertical','portrait','square']:
        body+=place_logo(b,x,y+h*.025,w*.94,h*.19)
        block,bh=copy_block(b,x,y+h*.30,w*.94,min(48,w*.055),400)
        body+=block
        grid_y=y+h*.65;cw=w*.46;ch=h*.135
        for i,p in enumerate(partners):
            body+=place_logo(p,x+(i%2)*w*.53,grid_y+(i//2)*h*.15,cw,ch,True)
        body+=text(x,y+h*.98,b['website'],min(17,w*.02),fill='#555555')
        art=(x,y+h*.38,w,h*.23)
    else:
        body+=place_logo(b,x,y+h*.10,w*.53,h*.32)
        block,bh=copy_block(b,x,y+h*.66,w*.53,min(42,h*.11),400)
        body+=block
        body+=text(x,y+h*.96,b['website'],min(18,h*.043),fill='#555555')
        cw=w*.35;ch=h*(.86/len(partners))
        for i,p in enumerate(partners):
            body+=place_logo(p,x+w*.64,y+h*.04+i*(h*.92/len(partners)),cw,ch,True)
        art=(x,y+h*.46,w*.53,h*.11)
    return body,art

def main():
    rows=[]
    for b in BRANDS:
        for s in SPECS:
            body,art=single(b,s)
            p=V2/'social-templates'/COLLECTIONS[b['id']]/s['platform']/(s['name']+'.svg')
            r=save_design(p,s['w'],s['h'],body,b['name']+' / '+s['surface'],[(b,'logo')],art,category='social',copy_ids=[b['id']]);r.update(platform=s['platform'],surface=s['surface'],safe=s['safe'],collection=COLLECTIONS[b['id']]);rows.append(r)
    master=dict(platform='Master',name='ecosystem-wide-master',w=2400,h=800,surface='Wide ecosystem template',layout='landscape',safe=[160,90,2080,580])
    for collection,ids in [('01-Ecosystem-Four-Brands',['pretrend','aiwars','verticalfoundation']),('02-Ecosystem-Five-Brands',['pretrend','aiwars','vtruscope','verticalfoundation'])]:
        partners=[BY_ID[k] for k in ids]
        for s in SPECS+[master]:
            body,art=ecosystem(s,partners)
            p=V2/'social-templates'/collection/s['platform']/(s['name']+'.svg')
            r=save_design(p,s['w'],s['h'],body,collection[3:].replace('-',' ')+' / '+s['surface'],[(BY_ID['vitruveo'],'logo')]+[(p,'logo') for p in partners],art,category='ecosystem-social',copy_ids=['vitruveo']);r.update(platform=s['platform'],surface=s['surface'],safe=s['safe'],collection=collection);rows.append(r)
    with ThreadPoolExecutor(max_workers=2) as pool:
        for i,out in enumerate(pool.map(lambda r:render(V2/r['path']),rows)):
            if i%10==0:print('Rendered',i+1,'/',len(rows),flush=True)
    (V2/'reports/social-records.json').write_text(json.dumps(rows,indent=2))
    print('Created',len(rows),'source-only social templates',flush=True)
if __name__=='__main__':main()
