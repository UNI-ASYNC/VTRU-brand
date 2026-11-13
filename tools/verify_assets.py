#!/usr/bin/env python3
"""Verify published output hashes and original source kits without network access."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checked = 0
    errors = []
    for collection, manifest_name, path_key in [
        ('brand-system', '08-Manifests-and-Export-Checks/asset-manifest.json', 'path'),
        ('social-banners', '00-Guide-and-Audit/asset-manifest.json', 'file'),
    ]:
        base = ROOT / collection
        manifest = json.loads((base / manifest_name).read_text())
        for entry in manifest['files']:
            path = base / entry[path_key]
            if not path.is_file():
                errors.append(f'Missing file: {path.relative_to(ROOT)}')
            elif sha256(path) != entry['sha256']:
                errors.append(f'Hash mismatch: {path.relative_to(ROOT)}')
            checked += 1

    original = ROOT / 'source-brand-kits'
    members = 0
    for archive in sorted(original.glob('*-brandkit.zip')):
        brand = archive.name.split('-brandkit.zip')[0]
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None:
                errors.append(f'ZIP integrity failed: {archive.name}')
            for name in z.namelist():
                if name.endswith('/'):
                    continue
                path = original / 'unpacked' / brand / name
                expected = hashlib.sha256(z.read(name)).hexdigest()
                if not path.is_file() or sha256(path) != expected:
                    errors.append(f'Source mismatch: {brand}/{name}')
                members += 1
    if members != 70:
        errors.append(f'Expected 70 source files; found {members}')

    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {checked} manifest files and {members} original source files verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
