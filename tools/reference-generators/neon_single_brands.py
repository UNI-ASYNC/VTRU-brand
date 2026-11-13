from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,math,base64,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from social_common import *

COLLECTIONS={
 'vitruveo':'03-Vitruveo',
 'verticalfoundation':'04-Vertical-Foundation',
 'pretrend':'05-Pretrend',
 'aiwars':'06-AI-Wars',
 'vtruscope':'07-VTRU-Scope'
}

def composition(b,s):
    w,h=s['w'],s['h'];sx,sy,sw,sh=s['safe'];kind=s['layout']
    # Keep the complete source wordmark as the sole identity element.
    if kind in ['youtube','x','rumble']:
        px=sx+sw*.035;py=sy+sh*.035;pw=sw*.93;ph=sh*.91
        body=card(px,py,pw,ph,min(ph*.13,38))
        # Lettering and mark stay well within the live-device safe region.
        ly=py+ph*.12;lh=ph*.61;lw=pw*.85;lx=px+pw*.075
        if b['id']=='verticalfoundation':
            lh=ph*.68;ly=py+ph*.05
        body+=logo(b,lx,ly,lw,lh,'logo-dark')
        cy=py+ph*.83
        caption='AI Blockchain' if b['id']=='vitruveo' else 'VITRUVEO ECOSYSTEM'
        fs=ph*.083 if b['id']=='vitruveo' else ph*.043
        body+=text(px+pw*.5,cy,caption,fs,'#D4EAF7',500,'middle',letter_spacing=0 if b['id']=='vitruveo' else ph*.01)
        body+=rule(px+pw*.18,py+ph*.94,pw*.64)
    elif kind in ['vertical','portrait','square']:
        if kind=='vertical':
            px,py,pw,ph=sx+sw*.035,sy+sh*.16,sw*.93,sh*.62
            topy=sy+sh*.09
        elif kind=='portrait':
            px,py,pw,ph=sx+sw*.03,sy+sh*.16,sw*.94,sh*.61
            topy=sy+sh*.085
        else:
            px,py,pw,ph=sx+sw*.03,sy+sh*.19,sw*.94,sh*.60
            topy=sy+sh*.11
        body=text(sx+sw*.5,topy,'VITRUVEO ECOSYSTEM',min(21,sw*.026),'#CEE6FA',600,'middle',letter_spacing=3)
        body+=card(px,py,pw,ph,36)
        body+=logo(b,px+pw*.075,py+ph*.12,pw*.85,ph*.66,'logo-dark')
        if b['id']=='vitruveo':
            body+=text(px+pw*.5,py+ph*.84,'AI Blockchain',pw*.053,'url(#headlineLight)',600,'middle',font_style='italic')
        else:
            body+=rule(px+pw*.22,py+ph*.88,pw*.56)
        body+=rule(sx+sw*.13,py+ph+sh*.075,sw*.74)
    else:
        # Facebook and YouTube landscape feed assets use a framed lockup.
        px=sx+sw*.025;py=sy+sh*.09;pw=sw*.95;ph=sh*.77
        body=card(px,py,pw,ph,30)
        body+=logo(b,px+pw*.075,py+ph*.10,pw*.85,ph*.66,'logo-dark')
        caption='AI Blockchain' if b['id']=='vitruveo' else 'VITRUVEO ECOSYSTEM'
        fs=min(33,ph*.09) if b['id']=='vitruveo' else min(18,ph*.047)
        body+=text(px+pw*.5,py+ph*.88,caption,fs,'#D6EDF8',500,'middle',letter_spacing=0 if b['id']=='vitruveo' else 3)
        body+=rule(px+pw*.15,py+ph*.97,pw*.70)
    return body

def main():
    records=[]
    for b in BRANDS:
        for s in SPECS:
            records.append(save_design(COLLECTIONS[b['id']],s,composition(b,s),[(b,'logo-dark')]))
    def go(r):
        p=render(ROOT/r['path'])
        # Lossless optimization retains source-logo edge antialiasing.
        with Image.open(p) as im:
            if im.mode=='RGBA' and im.getextrema()[3]==(255,255):im=im.convert('RGB')
            im.save(p,optimize=True)
        return p
    with ThreadPoolExecutor(max_workers=3) as pool:
        for i,p in enumerate(pool.map(go,records)):
            if (i+1)%5==0:print(f'Rendered {i+1}/{len(records)} {p.parent.parent.name}',flush=True)
    Path('/workspace/work/neon-single-records.json').write_text(json.dumps(records,indent=2))
    # Large contact sheet includes every layout family and all five brands.
    fonts='/usr/share/fonts/truetype/dejavu/'
    titlefont=ImageFont.truetype(fonts+'DejaVuSans-Bold.ttf',26)
    labelfont=ImageFont.truetype(fonts+'DejaVuSans.ttf',17)
    chosen=['x-profile-banner','youtube-channel-banner','instagram-feed-square','tiktok-vertical-cover','rumble-channel-backsplash']
    sheet=Image.new('RGB',(1800,5*600+100),'#E7ECF3');d=ImageDraw.Draw(sheet)
    d.text((24,20),'Standalone brands / exact source marks',font=titlefont,fill='#142035')
    for i,b in enumerate(BRANDS):
        d.text((24,80+i*600),b['name'],font=titlefont,fill='#142035')
        for j,name in enumerate(chosen):
            s=next(x for x in SPECS if x['name']==name)
            p=ROOT/COLLECTIONS[b['id']]/s['platform']/(name+'.png')
            im=Image.open(p).convert('RGB');im.thumbnail((330,470))
            x=20+j*356;y=125+i*600
            sheet.paste(im,(x+(330-im.width)//2,y+(470-im.height)//2))
            d.text((x,y+490),name[:29],font=labelfont,fill='#142035')
    review=Path('/workspace/work/neon-single-contact-sheet.jpg');sheet.save(review,quality=90)
    # Audit exact embedded source bytes plus formats and upload limits.
    errors=[];sizes={}
    ns={'s':'http://www.w3.org/2000/svg'}
    for r in records:
        p=ROOT/r['path'];doc=ET.parse(p).getroot()
        sources=[]
        for image in doc.findall('.//s:image',ns):
            href=image.get('{http://www.w3.org/1999/xlink}href','')
            if href.startswith('data:image/svg+xml;base64,'):
                data=base64.b64decode(href.split(',',1)[1]);sources.append(hashlib.sha256(data).hexdigest())
        if sources!=[r['sources'][0]['sha256']]:errors.append('Source mismatch '+r['path'])
        png=ROOT/r['png_path'];im=Image.open(png)
        if im.size!=(r['width'],r['height']):errors.append('Wrong size '+str(png))
        size=png.stat().st_size;sizes[r['png_path']]=size
        if r['platform']=='Rumble' and size>2000000:errors.append('Rumble >2MB '+str(png))
        if r['platform']=='YouTube' and 'channel' in png.name and size>6000000:errors.append('YouTube >6MB '+str(png))
    Path('/workspace/work/neon-single-qc.json').write_text(json.dumps(dict(designs=len(records),svg_count=len(records),png_count=len(records),source_byte_matches=len(records),errors=errors,png_bytes=sizes),indent=2))
    print(json.dumps(dict(designs=len(records),outputs=len(records)*2,errors=errors,max_rumble=max(v for k,v in sizes.items() if 'Rumble' in k),max_youtube=max(v for k,v in sizes.items() if 'channel-banner' in k)),indent=2),flush=True)
    if errors:raise RuntimeError(errors)

if __name__=='__main__':main()
