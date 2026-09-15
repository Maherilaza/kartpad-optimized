#!/usr/bin/env python3
"""Compose reviewed dependency sources with an exact migrated core snapshot."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--prior', type=Path, required=True)
p.add_argument('--core', type=Path, required=True)
p.add_argument('--core-manifest', type=Path, required=True)
p.add_argument('--runtime', type=Path, required=True)
p.add_argument('--apk', type=Path, required=True)
p.add_argument('--build-manifest', type=Path, required=True)
p.add_argument('output', type=Path)
a = p.parse_args()
sha = lambda data: hashlib.sha256(data).hexdigest()
if a.output.exists():
    p.error('output already exists')
files = {}
with tarfile.open(a.prior) as archive:
    old = json.load(archive.extractfile('SOURCE-MANIFEST.json'))
    names = archive.getnames()
    if len(names) != len(set(names)) or set(names) != set(old['files']) | {'SOURCE-MANIFEST.json'}:
        p.error('prior source manifest coverage mismatch')
    for member in archive.getmembers():
        if not member.isfile() or member.name.startswith('/') or '..' in Path(member.name).parts:
            p.error('unsafe prior source member')
        if member.name == 'SOURCE-MANIFEST.json':
            continue
        data = archive.extractfile(member).read()
        expected = old['files'][member.name]
        if len(data) != expected['bytes'] or sha(data) != expected['sha256']:
            p.error('prior source member failed integrity check')
        if member.name.startswith(('prepared-runtime/', 'supplement/')) or member.name.endswith('-core-source.tar.gz'):
            continue
        files[member.name] = data
core = a.core.read_bytes()
core_manifest = json.loads(a.core_manifest.read_text())
if sha(core) != core_manifest['sha256'] or len(core) != core_manifest['bytes']:
    p.error('core snapshot does not match its manifest')
files['KartPad-0.4.22-core-source.tar.gz'] = core
files['core-source-manifest.json'] = a.core_manifest.read_bytes()
for path in a.runtime.rglob('*'):
    if path.is_symlink():
        p.error('runtime contains a symlink')
    if path.is_file():
        files['prepared-runtime/android/' + path.relative_to(a.runtime).as_posix()] = path.read_bytes()
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location('provenance', Path(__file__).with_name('write-build-provenance.py'))
mod = module_from_spec(spec); spec.loader.exec_module(mod)
build = json.loads(a.build_manifest.read_text())
if build['source_dirty'] or mod.tree(a.runtime) != build['prepared_runtime']:
    p.error('prepared runtime is not the clean compiled input')
if core_manifest['archives'][0]['commit'] != build['source_revision']:
    p.error('core snapshot does not identify the compiled Android source')
files['REBUILD.md'] = b'''# KartPad 0.4.22 source delivery

The core snapshot contains the exact Android compilation commit, all four maintained runtime submodules, the pinned upstream WiiCompiled source and Dolphin. Apple production inputs match the maintained sources with the documented builder validation-count correction. Original compilation identities remain in the binary provenance; no old binary is relabeled as newly compiled.

Dependency archives, configured Dolphin dependency sources and profile tools are retained from the reviewed 0.4.19 delivery and verified against its complete file manifest. The prepared Android runtime is replaced with the exact current compiled input and fingerprint-checked. Rebuild using the core snapshot's platform instructions; platform SDKs and separate user-supplied game inputs remain required. The delivery does not include translated game functions, disc images, saves or signing material.

Verify SOURCE-MANIFEST.json, then extract the core snapshot. Its restore-source-git.py and metadata files reconstruct the exact Git identities, including submodules, offline. Dependency layouts and reconstruction instructions describe the retained dependency sources. Older version references in that dependency guide describe the retained dependency recipes, not this release's app source or binaries.
'''
files['supplement/package-migration-source-delivery.py'] = Path(__file__).read_bytes()
files['supplement/write-build-provenance.py'] = Path(__file__).with_name('write-build-provenance.py').read_bytes()
manifest = {'schemaVersion': 1, 'applicationSources': {'android': build['source_revision']},
            'androidAPK_SHA256': sha(a.apk.read_bytes()), 'preparedRuntime': {'android': build['prepared_runtime']},
            'files': {n: {'bytes': len(d), 'sha256': sha(d)} for n,d in sorted(files.items())}}
files['SOURCE-MANIFEST.json'] = (json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode()
with a.output.open('xb') as output, gzip.GzipFile(filename='', fileobj=output, mode='wb', mtime=0) as gz, tarfile.open(fileobj=gz, mode='w|') as archive:
    for name,data in sorted(files.items()):
        info=tarfile.TarInfo(name); info.size=len(data); info.mode=0o644; archive.addfile(info,io.BytesIO(data))
print(json.dumps({'bytes': a.output.stat().st_size, 'sha256': sha(a.output.read_bytes())}))
