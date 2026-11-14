"""Package V2 without rewriting or deleting V1 evidence."""
from pathlib import Path
import json,hashlib,shutil,zipfile,csv,subprocess
from PIL import Image

REPO=Path(__file__).resolve().parents[1]
V2=REPO/'v2';REPORTS=V2/'reports';DOWNLOADS=REPO/'downloads/v2'
BASELINE='5f4d5593a67ecfc814326212a704a07289480b87'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob_sha(p):
    data=p.read_bytes();return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def preserve_v1():
    raw=subprocess.check_output(['git','ls-tree','-r','-z',BASELINE],cwd=REPO)
    unchanged=[];nav=[];errors=[]
    for entry in raw.split(b'\0'):
        if not entry:continue
        header,name=entry.split(b'\t',1);expected=header.split()[2].decode();rel=name.decode();p=REPO/rel
        if rel in ['README.md','GALLERY.md']:
            nav.append(rel);continue
        if not p.is_file() or blob_sha(p)!=expected:errors.append(rel)
        else:unchanged.append(rel)
    if errors:raise AssertionError('V1 evidence changed: '+str(errors))
    receipt=dict(checked_on='2026-11-14',baseline_commit=BASELINE,frozen_tag='v1.0.0',unchanged_original_files=len(unchanged),navigation_files_updated=nav,all_original_artwork_zip_reports_sources_unchanged=True,errors=errors,note='Only version-navigation documents are updated. Their original bytes remain in the frozen tag.')
    (REPORTS/'v1-preservation.json').write_text(json.dumps(receipt,indent=2))
    return receipt

def normalize():
    records=[]
    for r in json.loads((REPORTS/'social-records.json').read_text()):
        for key in ['path','png_path']:
            n=dict(r);n['path']=r[key]
            if key=='path':n.pop('png_source_overrides',None)
            records.append(n)
    for r in json.loads((REPORTS/'supplemental-records.json').read_text())['files']:
        n=dict(r);n['path']=r['file'];records.append(n)
    records+=json.loads((REPORTS/'letterhead-records.json').read_text())
    out=[]
    for r in records:
        p=V2/r['path'];r=dict(r);r.update(sha256=sha(p),bytes=p.stat().st_size,extension=p.suffix[1:])
        if p.suffix=='.png':
            with Image.open(p) as im:r.update(width=im.width,height=im.height)
        out.append(r)
    assert len(out)==338 and len({r['path'] for r in out})==338
    other=[]
    excluded={'asset-manifest.json','asset-manifest.csv','sha256sums.txt'}
    production={r['path'] for r in out}
    for p in sorted(V2.rglob('*')):
        if not p.is_file() or p.name in excluded or str(p.relative_to(V2)) in production:continue
        other.append(dict(path=str(p.relative_to(V2)),sha256=sha(p),bytes=p.stat().st_size,classification='V2 supporting document, font, preview or audit'))
    (REPORTS/'asset-manifest.json').write_text(json.dumps(dict(version=2,designs=154,production_files=len(out),files=out,supporting_files=other),indent=2))
    fields=['path','extension','category','width','height','bytes','sha256']
    with (REPORTS/'asset-manifest.csv').open('w') as f:
        w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(out)
    allfiles=[p for p in sorted(V2.rglob('*')) if p.is_file() and p.name!='sha256sums.txt']
    (REPORTS/'sha256sums.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(V2)}' for p in allfiles)+'\n')
    return out

def make_zip(dest,files,prefix='VTRU-Brand-V2',readme=None):
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        if readme:z.writestr(prefix+'/README.md',readme)
        for p in sorted(set(files)):
            if p.is_file():z.write(p,Path(prefix)/p.relative_to(V2))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
    return dict(name=dest.name,bytes=dest.stat().st_size,sha256=sha(dest))

def main():
    DOWNLOADS.mkdir(parents=True,exist_ok=True)
    receipt=preserve_v1();records=normalize()
    paths=[p for p in V2.rglob('*') if p.is_file()]
    packages=[make_zip(DOWNLOADS/'VTRU-Brand-V2-General-Templates.zip',paths)]
    shared=list((V2/'resources').rglob('*'))+[REPORTS/'current-website-copy.json',REPORTS/'COPY-SOURCES.md',V2/'USAGE-GUIDE.md',V2/'VERSION-NOTES.md']
    for ident,folder in [('vitruveo','03-Vitruveo'),('verticalfoundation','04-Vertical-Foundation'),('pretrend','05-Pretrend'),('aiwars','06-AI-Wars'),('vtruscope','07-VTRU-Scope')]:
        files=list((V2/'social-templates'/folder).rglob('*'))+list((V2/'supplemental'/ident).rglob('*'))+shared
        note=f'# {ident} — V2 general templates\n\nSupplied logos and existing website copy only. Open areas are reserved for the team’s existing imagery. This package contains the platform templates and supplemental/document templates for this brand.\n\nBrowse the complete V2 gallery at https://github.com/UNI-ASYNC/VTRU-brand/blob/main/v2/GALLERY.md . V1 evidence remains separate.\n'
        packages.append(make_zip(DOWNLOADS/f'{folder[3:]}-V2-Templates.zip',files,readme=note))
    for folder in ['01-Ecosystem-Four-Brands','02-Ecosystem-Five-Brands']:
        files=list((V2/'social-templates'/folder).rglob('*'))+shared
        note='# V2 ecosystem templates\n\nSource logos and the sourced Vitruveo website headline. White/empty areas are for owner-supplied imagery. These are templates, not finished campaigns.\n'
        packages.append(make_zip(DOWNLOADS/f'{folder[3:]}-V2-Templates.zip',files,readme=note))
    (DOWNLOADS/'package-manifest.json').write_text(json.dumps(dict(version=2,packages=packages),indent=2))
    rows=['# V2 ZIP downloads','','These are the separate **V2 general templates**. Existing V1 ZIPs remain unchanged in the parent download folder.','','| Package | Size | Download |','|---|---:|---|']
    for r in packages:rows.append(f'| {r["name"]} | {r["bytes"]/1e6:.2f} MB | [Download]({r["name"]}?raw=true) |')
    rows+=['','[Browse V2 images](../../v2/GALLERY.md) · [V2 source-copy inventory](../../v2/reports/COPY-SOURCES.md) · [Preserved V1 ZIPs](../README.md)','']
    (DOWNLOADS/'README.md').write_text('\n'.join(rows))
    print(json.dumps(dict(designs=154,production_files=len(records),v1_unchanged_files=receipt['unchanged_original_files'],packages=packages),indent=2))
if __name__=='__main__':main()
