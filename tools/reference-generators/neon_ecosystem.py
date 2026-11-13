from social_common import *
from PIL import ImageFont
from concurrent.futures import ThreadPoolExecutor

V=BY_ID['vitruveo'];F=BY_ID['verticalfoundation'];P=BY_ID['pretrend'];A=BY_ID['aiwars'];S=BY_ID['vtruscope']
FONTFILE='/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf'
def fit(t,size,width):
    f=ImageFont.truetype(FONTFILE,100)
    return min(size,width*100/f.getlength(t))
def tagline(x,y,size,width,anchor='start'):
    return text(x,y,'AI Blockchain',fit('AI Blockchain',size,width),'url(#headlineLight)',700,anchor,font_style='italic')
def panel_logo(b,x,y,w,h):
    return card(x,y,w,h)+logo(b,x+w*.08,y+h*.08,w*.84,h*.84,'logo-dark')

def wide(x,y,w,h,partners):
    out=logo(V,x,y+h*.06,w*.58,h*.34,'logo-dark')
    out+=tagline(x+w*.06,y+h*.57,min(h*.15,w*.065),w*.51)
    out+=rule(x+w*.06,y+h*.66,w*.48)
    out+=text(x+w*.12,y+h*.86,'powered by',min(h*.054,w*.018),'#B8CFE7')
    out+=logo(F,x+w*.35,y+h*.70,w*.18,h*.28,'logo-dark')
    px=x+w*.64;pw=w*.35
    out+=featuring(px+w*.01,y+h*.08,size=min(h*.038,w*.0125))
    if len(partners)==2:
        for b,yy,hh in [(partners[0],.14,.36),(partners[1],.57,.31)]:out+=panel_logo(b,px,y+h*yy,pw,h*hh)
    else:
        for b,yy,hh in [(partners[0],.14,.27),(partners[1],.45,.22),(partners[2],.71,.22)]:out+=panel_logo(b,px,y+h*yy,pw,h*hh)
    return out
def square(x,y,w,h,partners):
    out=logo(V,x+w*.03,y+h*.015,w*.94,h*.21,'logo-dark')
    out+=tagline(x+w*.50,y+h*.33,w*.081,w*.85,'middle')
    out+=rule(x+w*.10,y+h*.38,w*.80)
    out+=featuring(x+w*.29,y+h*.47,size=w*.020)
    n=len(partners);gap=w*.035;cw=(w-gap*(n-1))/n
    for i,b in enumerate(partners):out+=panel_logo(b,x+i*(cw+gap),y+h*.52,cw,h*.23)
    out+=text(x+w*.16,y+h*.90,'powered by',w*.026,'#B8CFE7')
    out+=logo(F,x+w*.47,y+h*.80,w*.28,h*.19,'logo-dark')
    return out
def vertical(x,y,w,h,partners):
    out=logo(V,x,y+h*.015,w,h*.18,'logo-dark')
    out+=tagline(x+w*.5,y+h*.265,w*.092,w*.94,'middle')
    out+=rule(x+w*.06,y+h*.305,w*.88)
    out+=featuring(x+w*.24,y+h*.36,size=w*.022)
    if len(partners)==2:
        for b,yy,hh in [(partners[0],.405,.225),(partners[1],.67,.155)]:out+=panel_logo(b,x+w*.05,y+h*yy,w*.9,h*hh)
    else:
        for b,yy,hh in [(partners[0],.40,.18),(partners[1],.615,.125),(partners[2],.775,.115)]:out+=panel_logo(b,x+w*.05,y+h*yy,w*.9,h*hh)
    fy=.86 if len(partners)==2 else .91
    fh=.135 if len(partners)==2 else .085
    out+=text(x+w*.19,y+h*(fy+fh*.60),'powered by',w*.029,'#B8CFE7')
    out+=logo(F,x+w*.52,y+h*fy,w*.27,h*fh,'logo-dark')
    return out
def rumble(x,y,w,h,partners):
    out=logo(V,x,y+h*.02,w*.34,h*.49,'logo-dark')
    out+=tagline(x+w*.035,y+h*.79,h*.19,w*.30)
    out+=text(x+w*.39,y+h*.17,'powered by',h*.046,'#B8CFE7')
    out+=logo(F,x+w*.37,y+h*.23,w*.145,h*.60,'logo-dark')
    start=.57;n=len(partners);cw=w*(.42/n-.015)
    out+=featuring(x+w*start,y+h*.17,size=h*.043)
    for i,b in enumerate(partners):out+=panel_logo(b,x+w*start+i*(cw+w*.015),y+h*.27,cw,h*.49)
    return out

def main():
    records=[]
    master=dict(platform='Master',name='reference-wide-master',w=2400,h=800,surface='Wide reference composition',layout='master',safe=[160,90,2080,580])
    for folder,partners in [('01-Ecosystem-Four-Brands',[P,A]),('02-Ecosystem-Five-Brands',[P,A,S])]:
        for spec in SPECS+[master]:
            x,y,w,h=spec['safe'];layout=spec['layout']
            if layout=='rumble':body=rumble(x,y,w,h,partners)
            elif layout in ['vertical','portrait']:body=vertical(x,y,w,h,partners)
            elif layout=='square':body=square(x,y,w,h,partners)
            else:body=wide(x,y,w,h,partners)
            src=[(V,'logo-dark'),(F,'logo-dark')]+[(b,'logo-dark') for b in partners]
            records.append(save_design(folder,spec,body,src))
    with ThreadPoolExecutor(max_workers=2) as pool:
        for i,p in enumerate(pool.map(lambda r:render(ROOT/r['path']),records)):
            if i%4==0:print('Rendered',i+1,'/',len(records),p.name,flush=True)
    (ROOT.parent/'neon-ecosystem-records.json').write_text(json.dumps(records,indent=2))
    print('Ecosystem complete:',len(records),'designs',flush=True)
if __name__=='__main__':main()
