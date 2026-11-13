from pathlib import Path
import sys,json,base64,hashlib,xml.etree.ElementTree as ET,subprocess,os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent))
from social_common import SPECS
W=Path('/workspace/work');ROOT=W/'Neon-Social-Banner-Pack';SOURCES=W/'source';QA=W/'neon-qa-temp';QA.mkdir(exist_ok=True)
specs={s['name']:s for s in SPECS};specs['reference-wide-master']=dict(w=2400,h=800,safe=[160,90,2080,580])
hashbytes=lambda d:hashlib.sha256(d).hexdigest()
originals={hashbytes(p.read_bytes()):p.name for p in SOURCES.glob('*/*.svg')}
original_pngs={p.name:p for p in SOURCES.glob('*/*.png')}
errors=[];warnings=[];checks=[]
records=[]
for name in ['neon-ecosystem-records.json','neon-single-records.json']:
 p=W/name
 if p.exists():records.extend(json.loads(p.read_text()))
if len(records)!=79:errors.append(f'Expected79 design metadata records; got {len(records)}')
by_path={r['path']:r for r in records}

def check(p):
 path=str(p.relative_to(ROOT));r=ET.parse(p).getroot();spec=specs.get(p.stem);errs=[];warns=[];source_files=[];backgrounds=[];text_ids=[]
 if not spec:return dict(file=path,errors=['Unknown target filename'],warnings=[])
 w,h=spec['w'],spec['h'];sx,sy,sw,sh=spec['safe']
 if [float(r.get('width')),float(r.get('height'))]!=[w,h]:errs.append('Wrong SVG canvas')
 # No layout filter, transform or opacity may be added to a source logo.
 parents={e:par for par in r.iter() for e in par}
 for i,e in enumerate(r.iter()):
  local=e.tag.split('}')[-1]
  if local=='text':
   ident='qaText'+str(i);e.set('id',ident);text_ids.append((ident,''.join(e.itertext())))
  if local!='image':continue
  href=e.get('{http://www.w3.org/1999/xlink}href',e.get('href',''))
  if href.startswith('data:image/svg+xml;base64,'):
   data=base64.b64decode(href.split(',',1)[1]);sha=hashbytes(data)
   if sha not in originals:errs.append('Logo SVG bytes do not match supplied source')
   source_files.append(dict(file=originals.get(sha,'UNMATCHED'),sha256=sha))
   par=e.get('preserveAspectRatio','xMidYMid meet')
   if par!='xMidYMid meet':errs.append('Logo image aspect mode not meet: '+par)
   for q in [e]+list(_ancestors(e,parents)):
    if q.get('filter') or q.get('transform') or q.get('opacity') or q.get('clip-path') or q.get('mask'):errs.append('Layout effect/transform applied to source logo')
   x,y,lw,lh=[float(e.get(a,'0')) for a in ['x','y','width','height']]
   if x<sx-.5 or y<sy-.5 or x+lw>sx+sw+.5 or y+lh>sy+sh+.5:errs.append('Logo nominal frame outside internal safe area')
  else:
   if href.startswith('data:'):errs.append('Unexpected embedded non-source image')
   else:
    q=(p.parent/href).resolve();backgrounds.append(str(q.relative_to(ROOT)) if q.is_relative_to(ROOT) else str(q))
    if not q.exists():errs.append('Background reference missing')
    if q.parent!=ROOT/'00-Guide-and-Audit'/'Backgrounds':errs.append('Unexpected background destination')
 if len(backgrounds)!=1:errs.append('Expected one background reference')
 if path.startswith('01-') and len(source_files)!=4:errs.append('Four-brand design does not contain four source images')
 if path.startswith('02-') and len(source_files)!=5:errs.append('Five-brand design does not contain five source images')
 if path[:2] in ['03','04','05','06','07'] and len(source_files)!=1:errs.append('Standalone design does not contain single source image')
 record=by_path.get(path)
 if not record:errs.append('Missing metadata record')
 elif sorted(s['sha256'] for s in source_files)!=sorted(s['sha256'] for s in record['sources']):errs.append('Source manifest mismatch')
 override=record.get('png_source_override') if record else None
 is_scope=path.startswith('02-') or path.startswith('07-')
 if is_scope and not override:errs.append('Scope PNG override metadata missing')
 if override:
  sourcepng=original_pngs.get(override['file'])
  if not sourcepng:errs.append('PNG override source file missing')
  elif hashbytes(sourcepng.read_bytes())!=override['sha256']:errs.append('PNG override hash mismatch')
  elif Image.open(sourcepng).width!=2400:errs.append('PNG override not supplied2400px source')
  if override['file']!='vtruscope-logo-dark.png':errs.append('Unexpected PNG override source')
  if not is_scope:errs.append('Unexpected PNG override on non-Scope design')
 png=p.with_suffix('.png');size=0
 if not png.exists():errs.append('PNG export missing')
 else:
  im=Image.open(png);im.verify();im=Image.open(png)
  if im.size!=(w,h):errs.append('PNG dimensions mismatch')
  size=png.stat().st_size
  if 'Rumble' in path and size>=2000000:errs.append('Rumble export exceeds2MB')
  if p.stem=='youtube-channel-banner' and size>=6000000:errs.append('YouTube channel exceeds6MB')
  if not png.stat().st_mtime>=p.stat().st_mtime-1:errs.append('PNG export older than SVG master')
 # Inkscape returns real text bounds and includes letter spacing and italic overhangs.
 temp=QA/(p.parent.parent.name+'-'+p.stem+'.svg');ET.ElementTree(r).write(temp,encoding='unicode')
 env=os.environ.copy();env['XDG_CACHE_HOME']=str(W/'cache')
 out=subprocess.run(['inkscape',str(temp),'--query-all'],capture_output=True,text=True,env=env)
 boxes={line.split(',')[0]:line.split(',')[1:] for line in out.stdout.splitlines() if line.startswith('qaText')}
 for ident,txt in text_ids:
  if ident not in boxes:errs.append('Text bounds unavailable: '+txt)
  else:
   x,y,tw,th=map(float,boxes[ident])
   if x<sx-.5 or y<sy-.5 or x+tw>sx+sw+.5 or y+th>sy+sh+.5:errs.append('Text outside safe area: '+txt)
 return dict(file=path,svg_dimensions=[w,h],safe_area=[sx,sy,sw,sh],sources=source_files,backgrounds=backgrounds,png_bytes=size,text_count=len(text_ids),png_source_override=override,errors=errs,warnings=warns)

def _ancestors(e,parents):
 while e in parents:
  e=parents[e];yield e

ps=sorted(ROOT.rglob('*.svg'))
if len(ps)!=79:errors.append(f'Expected79 SVG designs; got{len(ps)}')
with ThreadPoolExecutor(max_workers=4) as pool:checks=list(pool.map(check,ps))
for c in checks:
 errors.extend(c['file']+': '+e for e in c['errors']);warnings.extend(c['file']+': '+v for v in c['warnings'])
extra_svgs=[str(p.relative_to(ROOT)) for p in ps if p.stem not in specs]
extra_pngs=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*.png') if p.stem not in specs and '/Backgrounds/' not in str(p) and '/Previews/' not in str(p)]
# Only source substitutions require exact template counts; previews are generated separately.
overrides=[c for c in checks if c.get('png_source_override')]
if len(overrides)!=23:errors.append(f'Expected23 Scope PNG overrides; got{len(overrides)}')
if extra_svgs:errors.append('Unexpected SVG files: '+str(extra_svgs))
result=dict(status='PASS' if not errors else 'FAIL',expected_designs=79,checked_designs=len(checks),errors=errors,warnings=warnings,checks=checks,limits=['Internal safe areas and file targets tested; platform accounts and live upload/cropping not tested.'])
(W/'neon-independent-qa.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(status=result['status'],checked_designs=len(checks),errors=errors,warnings=warnings),indent=2))
