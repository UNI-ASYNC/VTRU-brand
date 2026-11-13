from pathlib import Path
import json,sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from brand_common import BRANDS,ROOT,logo,svg,text,rect,render,record
from discord_icons import glyph

EMOJIS={
'vitruveo':['node','validated','block','linked','build','sync','launch','secure','vote','signal'],
'verticalfoundation':['foundation','connect','grant','milestone','governance','community','roadmap','approval','announce','impact'],
'pretrend':['crash','bear','flat','bull','moon','analysis','resolve','volatility','momentum','target'],
'aiwars':['battle','victory','strategy','energy','reward','defend','defeat','gg','ready','respawn'],
'vtruscope':['chart','search','signal','report','status','filter','compare','insight','alert','verified']}
STICKERS={
'vitruveo':[('Online','signal'),('Validated','validated'),('Building','build'),('Network','node')],
'verticalfoundation':[('Approved','approval'),('Announcement','announce'),('Progress','roadmap'),('Community','community')],
'pretrend':[('Bullish','bull'),('Bearish','bear'),('Trending','momentum'),('Resolved','resolve')],
'aiwars':[('Victory','victory'),('Defeat','defeat'),('Battle Ready','battle'),('GG','gg')],
'vtruscope':[('Data Live','chart'),('Verified','verified'),('Alert','alert'),('Insight','insight')]}

def emoji(b,key):
    body=rect(6,6,116,116,b['ink'],24,stroke='#FFFFFF',stroke_width=3)
    body+=f'<g transform="translate(32 15)">{glyph(key,b["secondary"])}</g>'
    variant='logo-white' if b['id']=='aiwars' else 'logomark'
    if b['id']=='aiwars': body+=logo(b,25,92,78,20,variant)
    elif b['id']=='verticalfoundation':body+=logo(b,39,89,50,30,variant)
    else:body+=logo(b,50,88,28,28,variant)
    return body,variant

def sticker(b,label,key):
    body=rect(10,10,300,300,b['ink'],40,stroke='#FFFFFF',stroke_width=6)
    body+=logo(b,46,22 if b['id']=='verticalfoundation' else 32,228,78 if b['id']=='verticalfoundation' else 54,'logo-white')
    body+=f'<g transform="translate(111 104) scale(1.53)">{glyph(key,b["secondary"])}</g>'
    size=29 if len(label)>11 else 34
    body+=text(160,254,label,size,'#FFFFFF',700,'middle')
    body+=rect(118,277,84,5,b['secondary'],2.5)
    return body,'logo-white'

jobs=[]
for b in BRANDS:
    for i,key in enumerate(EMOJIS[b['id']],1):
        p=ROOT/b['folder']/'Emojis'/f'{b["id"]}-emoji-{i:02d}-{key}.svg'
        body,variant=emoji(b,key);p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(svg(128,128,body,f'{b["name"]} — {key} emoji'))
        jobs.append((p,b,'Emojis',variant,128,128,256*1024,key))
    for i,(label,key) in enumerate(STICKERS[b['id']],1):
        slug=label.lower().replace(' ','-')
        p=ROOT/b['folder']/'Stickers'/f'{b["id"]}-sticker-{i:02d}-{slug}.svg'
        body,variant=sticker(b,label,key);p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(svg(320,320,body,f'{b["name"]} — {label} sticker'))
        jobs.append((p,b,'Stickers',variant,320,320,512*1024,label))

def export(job):
    p,b,category,variant,w,h,limit,label=job
    rendered=render(p)
    png=p.with_suffix('.png')
    im=Image.open(png)
    assert im.size==(w,h),(png,im.size)
    assert png.stat().st_size<limit,(png,png.stat().st_size)
    assert im.mode=='RGBA',(png,im.mode)
    assert im.getpixel((0,0))[3]==0,png
    return record([p]+rendered,b,category,variant=variant,width=w,height=h,label=label,
        intended_use='Discord static emoji' if category=='Emojis' else 'Discord static sticker',
        constraint_check='dimensions, PNG size and transparent corners passed')

with ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(export,jobs))
records=[r for group in results for r in group]
Path('/workspace/work/discord-records.json').write_text(json.dumps(records,indent=2))
print(json.dumps({'emojis':50,'stickers':20,'files':len(records),'largest_emoji_png':max(p.with_suffix('.png').stat().st_size for p,b,c,*_ in jobs if c=='Emojis'),'largest_sticker_png':max(p.with_suffix('.png').stat().st_size for p,b,c,*_ in jobs if c=='Stickers')}))
