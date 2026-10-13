"""Publish current frozen/archive bytes without interpreting archived content."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).parent
plan = json.loads((HERE / 'raw-index-plan.json').read_text(encoding='utf-8'))
if plan['force_frozen_paths']:
    subprocess.run(['git', '-c', 'core.longpaths=true', 'add', '-f',
                    '--pathspec-from-file=' + str(HERE / 'frozen-force-paths.bin'),
                    '--pathspec-file-nul'], check=True, capture_output=True)
assert subprocess.run(['git', 'rev-parse', '--show-object-format'], check=True,
                      capture_output=True, text=True).stdout.strip() == 'sha1'
if plan['raw_files']:
    names = '\n'.join(a['path'] for a in plan['raw_files']) + '\n'
    result = subprocess.run(['git', '-c', 'core.longpaths=true', 'hash-object', '-w',
                             '--no-filters', '--stdin-paths'], input=names.encode('utf-8'),
                            capture_output=True, check=True)
    objects = result.stdout.decode('ascii').splitlines()
    assert len(objects) == len(plan['raw_files'])
    records = []
    for item, oid in zip(plan['raw_files'], objects):
        assert oid == item['raw_oid']
        assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256']
        records.append((item['mode'] + ' ' + oid + '\t' + item['path']).encode('utf-8'))
    subprocess.run(['git', '-c', 'core.longpaths=true', 'update-index', '-z', '--index-info'],
                   input=b'\0'.join(records) + b'\0', check=True, capture_output=True)
(HERE / 'raw-index-result.json').write_text(json.dumps({
    'result': 'pass', 'force_frozen_file_count': len(plan['force_frozen_paths']),
    'raw_byte_preserved_files': plan['raw_files'],
    'note': 'Only current index/blob storage changed; no worktree or archived file byte was rewritten. No history inspection or global configuration change.'
}, indent=2) + '\n', encoding='utf-8')
print('Exact index bytes preserved for', len(plan['raw_files']), 'files; retained',
      len(plan['force_frozen_paths']), 'otherwise ignored frozen references.')
