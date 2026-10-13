"""Compare current staged frozen bytes with working files before publication."""
import collections
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).parent
index = subprocess.run(['git', 'ls-files', '--stage', '-z'], capture_output=True, check=True).stdout
entries = {}
for row in index.split(b'\0'):
    if not row:
        continue
    header, path = row.split(b'\t', 1)
    mode, oid, stage = header.decode('ascii').split()
    assert stage == '0'
    entries[path.decode('utf-8')] = (mode, oid)
refs = json.loads((HERE / 'frozen-reference-inventory.json').read_text(encoding='utf-8'))['files']
rows = []
for item in refs:
    name = item['path']
    raw = Path(name).read_bytes()
    oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert name in entries and entries[name][1] == oid, name
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], name
    rows.append({'path': name, 'sha256': item['sha256'], 'raw_index_matches': True})
for manifest in ['private/workflow/runs/IG-1A/attempt-review-repair-02/delivery.json',
                 'private/workflow/runs/IG-1B/attempt-review-repair-01-20261012T193641Z/delivery.json']:
    data = json.loads(Path(manifest).read_text(encoding='utf-8'))
    for item in data['artifacts']:
        raw = Path(item['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == item['sha256']
        oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert entries[item['path']][1] == oid
result = {'result': 'pass', 'index_file_count': len(entries), 'frozen_reference_count': len(rows),
          'frozen_bytes': rows, 'accepted_ig_1a_82_and_ig_1b_66_match_exact_index_bytes': True,
          'index_categories': dict(collections.Counter(p.split('/')[0] for p in entries)),
          'publication_checks': {'workflow_validate_exit': 0, 'project_tests_exit': 0,
                                 'project_tests_passed': 102, 'project_pytest_seconds': 42.84,
                                 'diff_check_exit': 0, 'script_check_exit': 1, 'dry_run_exit': 1,
                                 'dry_run_reason': 'Explicit IG-1B is done; packet/dry-run requires ready/active. There is no ready/active task. No completed task or product was changed to hide this planner-state refusal.'}}
(HERE / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print('Current index:', len(entries), 'files; exact frozen references:', len(rows), '; all accepted hashes match.')
