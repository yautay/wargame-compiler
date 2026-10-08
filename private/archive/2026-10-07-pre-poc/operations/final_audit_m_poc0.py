import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(r'C:\dev\wargame-compiler')
SNAP = ROOT / 'private/archive/2026-10-07-pre-poc'
LEGACY = ROOT / 'archive/legacy-2026-10-07/project'
manifest = json.loads((SNAP / 'manifest.json').read_text(encoding='utf-8'))
mapping = json.loads((SNAP / 'movement-map.json').read_text(encoding='utf-8'))

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def git(*args):
    result = subprocess.run(['git', '-c', f'safe.directory={ROOT.as_posix()}', *args],
                            cwd=ROOT, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'),
                            capture_output=True, check=True)
    return result.stdout.decode('utf-8')

def save(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')

assert sha(SNAP / 'manifest.json') == (SNAP / 'manifest.sha256').read_text().split()[0]
checks = {}
for label, root in [('snapshot', SNAP / 'payload'), ('initial_restore', SNAP / 'restore-check'),
                    ('delivered_restore_tool', ROOT / 'private/archive/restore-cli-check-2026-10-07')]:
    for row in manifest['files']:
        p = root / row['path']
        assert p.stat().st_size == row['size'] and sha(p) == row['sha256'], (label, row['path'])
    checks[label] = len(manifest['files'])
for row in mapping:
    p = ROOT / row['destination']
    assert p.stat().st_size == row['size'] and sha(p) == row['sha256'], row['destination']
checks['post_move_after_tests'] = len(mapping)
original_public = {row['path'] for row in manifest['files'] if row['class'] == 'public'}
archived_files = set()
for parent, dirs, files in os.walk(LEGACY):
    dirs[:] = [d for d in dirs if d not in {'__pycache__', '.pytest_cache'}]
    for filename in files:
        archived_files.add((Path(parent) / filename).relative_to(LEGACY).as_posix())
assert archived_files == original_public, (archived_files - original_public, original_public - archived_files)
assert all(not row['destination'].startswith('archive/') for row in mapping if row['class'] == 'private')
assert git('rev-parse', 'HEAD').strip() == manifest['git']['head']
assert sha(ROOT / '.git/index') == manifest['git']['index_sha256']
tracked = git('ls-files').splitlines()
assert not any(p.startswith('private/') for p in tracked)
ignored = git('check-ignore', 'private/poc/spqr-chapter9/README.md', 'private/archive/2026-10-07-pre-poc/manifest.json').splitlines()
assert len(ignored) == 2
git('diff', '--check')
active = [ROOT/'README.md', ROOT/'CLAUDE.md', ROOT/'.gitignore', ROOT/'.gitattributes', ROOT/'pyproject.toml',
          *ROOT.joinpath('docs').rglob('*.md'), *ROOT.joinpath('tests').glob('*.py'),
          *ROOT.joinpath('scripts').glob('*.ps1'), ROOT/'archive/legacy-2026-10-07/README.md',
          ROOT/'archive/legacy-2026-10-07/restore.py']
for p in active:
    body = p.read_text(encoding='utf-8')
    assert body.endswith('\n'), p
    assert not any(line.rstrip(' \t') != line for line in body.splitlines()), p
wrapper = ROOT/'archive/legacy-2026-10-07/README.md'
for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)', wrapper.read_text(encoding='utf-8')):
    assert (wrapper.parent / href).exists(), href
metadata = {'python': sys.version, 'executable': sys.executable,
            'packages': sorted([{'name': p.metadata['Name'], 'version': p.version}
                                for p in importlib.metadata.distributions()], key=lambda p:p['name'].lower()),
            'note': 'Environment not copied; no dependencies installed by M-POC0'}
save(SNAP/'environment.json', metadata)
report = {'date': '2026-10-07', 'hash_checks': checks, 'mismatches': [],
          'bytes_per_copy': sum(r['size'] for r in manifest['files']),
          'public_original_files': len(original_public), 'private_original_files': len(mapping)-len(original_public),
          'unchanged_source_artifact_files': sum(r['path'].startswith('private/source-artifacts/') for r in mapping),
          'public_archive_matches_original_public_inventory': True,
          'private_files_only_in_private_destinations': True, 'private_not_tracked_and_ignored': True,
          'head_unchanged': True, 'index_unchanged': True, 'git_diff_check': 'passed',
          'new_active_file_whitespace_check': 'passed', 'new_active_files_checked': len(active),
          'existing_restore_destination_refused': True,
          'limitations': ['Snapshot excludes .git and .venv; original Git history remains in place',
                         'No external/off-device backup made', 'Legacy original gitattributes can normalize CRLF on future staging; snapshot preserves raw bytes',
                         'Global user ignore unreadable in sandbox; filesystem inventory independent of Git ignore']}
save(SNAP/'final-audit.json', report)
operations = SNAP / 'operations'
operations.mkdir()
for name in ['snapshot_m_poc0.py', 'move_m_poc0.ps1', 'verify_move_m_poc0.py', 'write_poc_cards.py', 'final_audit_m_poc0.py']:
    shutil.copyfile(Path(__file__).parent / name, operations / name)
print(json.dumps(report, indent=2))
