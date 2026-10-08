"""One-off, read-only inventory then exclusive snapshot and restore verification."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(r'C:\dev\wargame-compiler').resolve()
DEST = ROOT / 'private/archive/2026-10-07-pre-poc'
PUBLIC = {'.gitattributes', '.gitignore', 'CLAUDE.md', 'README.md', 'COPYRIGHT.md',
          'pyproject.toml', 'requirements.txt', 'bench', 'contracts', 'docs', 'glu', 'tests', 'wgc'}
EXCLUDED_TOP = {'.git', '.venv', '.pytest_cache', 'wargame_compiler.egg-info',
                '.agents', '.codex', '.aws'}
TEST_DIRS = {'.glu/desktop-export-tests', '.glu/desktop-plan-tests',
             '.glu/desktop-contract-tests/focused-1', '.glu/desktop-contract-tests/full-1'}

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def write_json(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

def git(*args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    return subprocess.run(['git', '-c', f'safe.directory={ROOT.as_posix()}', *args], cwd=ROOT,
                          env=env, check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout

assert not DEST.exists(), 'Never overwrite a snapshot'
unknown = {p.name for p in ROOT.iterdir()} - PUBLIC - EXCLUDED_TOP - {'.glu', 'private'}
assert not unknown, f'Unclassified top-level entries: {unknown}'
assert {p.name for p in (ROOT / 'private').iterdir()} <= {'source-artifacts'}, 'Review existing archives'
files, directories, exclusions = [], [], []
for base, dirs, names in os.walk(ROOT):
    parent = Path(base)
    for name in list(dirs):
        p = parent / name
        rel = p.relative_to(ROOT).as_posix()
        assert not (p.lstat().st_file_attributes & 1024), f'Reparse point: {rel}'
        reason = None
        if rel in EXCLUDED_TOP:
            reason = 'Git history / environment / generated metadata / managed agent or login configuration; kept in place initially'
        elif rel in TEST_DIRS:
            reason = 'Reproducible pytest basetemp; no inference needed; not copied, original preserved in later private move'
        elif name in {'__pycache__', '.pytest_cache'}:
            reason = 'Reproducible Python/pytest cache'
        if reason:
            exclusions.append({'path': rel, 'reason': reason})
            dirs.remove(name)
        else:
            directories.append(rel)
    for name in names:
        p = parent / name
        rel = p.relative_to(ROOT).as_posix()
        assert not (p.lstat().st_file_attributes & 1024), f'Reparse file: {rel}'
        if name == '.env' or name.startswith('.env.') or name.lower() in {'credentials', 'auth.json', 'id_rsa', 'id_ed25519'} or p.suffix.lower() in {'.key', '.pfx', '.p12'}:
            raise RuntimeError(f'Potential secret/login configuration needs classification: {rel}')
        files.append({'path': rel, 'size': p.stat().st_size, 'sha256': sha(p),
                      'class': 'private' if rel.startswith(('private/', '.glu/')) else 'public'})

status_before = git('status', '--porcelain=v1', '-uall')
git_metadata = {'head': git('rev-parse', 'HEAD').decode().strip(),
                'branch': git('branch', '--show-current').decode().strip(),
                'status_porcelain': status_before.decode('utf-8'),
                'index_sha256': sha(ROOT / '.git/index'),
                'history': 'Original .git retained untouched; not copied into snapshot',
                'command_overrides': ['safe.directory for this command only', 'GIT_OPTIONAL_LOCKS=0'],
                'limitation': 'User-level ignore file unreadable in sandbox; repository ignore rules used; all untracked public files independently inventoried'}
DEST.mkdir(parents=True, exist_ok=False)
payload = DEST / 'payload'
payload.mkdir()
for rel in directories:
    (payload / rel).mkdir(parents=True, exist_ok=True)
for item in files:
    p = payload / item['path']
    p.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / item['path'], p)
    assert p.stat().st_size == item['size'] and sha(p) == item['sha256'], item['path']
assert status_before == git('status', '--porcelain=v1', '-uall'), 'Source Git state changed during snapshot'
assert git_metadata['index_sha256'] == sha(ROOT / '.git/index')
for item in files:
    assert sha(ROOT / item['path']) == item['sha256'], f'Source changed: {item["path"]}'
manifest = {'format': 'pre-poc-snapshot@1', 'date': '2026-10-07', 'root': str(ROOT),
            'git': git_metadata, 'files': sorted(files, key=lambda v: v['path']),
            'directories': sorted(directories), 'excluded': exclusions,
            'scope_notes': ['Destination did not exist at inventory time; private/archive never included',
                            'No .git, .venv, credentials or login configuration copied',
                            'All source-artifacts and non-test .glu results included; Q-11, M-DESK1, M-DESK2 retained',
                            'No external repository copied or modified; original PDF in C:/dev/spqr remains external',
                            'Working bytes preserved without newline conversion; Git patches are supplemental only']}
write_json(DEST / 'manifest.json', manifest)
(DEST / 'manifest.sha256').write_text(sha(DEST / 'manifest.json') + '  manifest.json\n', encoding='ascii')
for filename, args in [('git-status.txt', ('status', '--short', '--branch', '-uall')),
                       ('git-tracked-files.txt', ('ls-files',)),
                       ('git-unstaged.patch', ('diff', '--binary', '--no-ext-diff')),
                       ('git-staged.patch', ('diff', '--cached', '--binary', '--no-ext-diff'))]:
    with (DEST / filename).open('xb') as f:
        f.write(git(*args))
restore = DEST / 'restore-check'
shutil.copytree(payload, restore)
for item in files:
    p = restore / item['path']
    assert p.stat().st_size == item['size'] and sha(p) == item['sha256'], item['path']
report = {'snapshot_verified': len(files), 'restore_verified': len(files),
          'bytes': sum(f['size'] for f in files), 'mismatches': [],
          'manifest_sha256': sha(DEST / 'manifest.json'), 'restore_directory': str(restore),
          'head': git_metadata['head'], 'index_unchanged': True,
          'python': sys.version, 'reorganization_allowed': True}
write_json(DEST / 'verification.json', report)
print(json.dumps(report, indent=2))
