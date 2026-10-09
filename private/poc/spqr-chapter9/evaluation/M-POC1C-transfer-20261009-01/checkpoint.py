"""Scoped checkpoint/staging audit for explicitly authorized laptop transfer."""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
HERE = Path(__file__).resolve().parent
LAST = P / 'evaluation/M-POC1C-review-006'
C = P / 'evaluation/eval-v1-candidate-20261009-03'
PUBLIC = ['docs/STATUS.md', 'docs/ROADMAP.md', 'docs/HANDOFF.md']
HANDOFF = 'docs/handoff/2026-10-09-M-POC1C-transfer.md'

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def ref(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest, 'bytes': path.stat().st_size}

def save(name, value):
    with (HERE / name).open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def git(*args, binary=False):
    result = subprocess.run(['git', '-c', 'safe.directory=C:/dev/wargame-compiler', *args], cwd=ROOT,
                            env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}, capture_output=True, check=True)
    return result.stdout if binary else result.stdout.decode('utf-8').strip()

def selected():
    paths = set()
    for n in range(1, 7):
        for directory in (P / f'evaluation/M-POC1C-review-{n:03d}', P / f'measurement/M-POC1C-review-{n:03d}'):
            paths.update(path for path in directory.iterdir() if path.is_file())
    for name in ('eval-v1-candidate-20261008-01', 'eval-v1-candidate-20261008-02', 'eval-v1-candidate-20261009-03'):
        paths.update(path for path in (P / 'evaluation' / name).iterdir() if path.is_file())
    return paths

def nested_refs(value):
    if isinstance(value, dict):
        if {'path', 'sha256', 'bytes'} <= value.keys():
            yield value
        for child in value.values():
            yield from nested_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from nested_refs(child)

def private_blob_matches(item, revision):
    content = git('show', f"{revision}:{item['path']}", binary=True)
    assert len(content) == item['bytes'] and hashlib.sha256(content).hexdigest() == item['sha256'], item

assert git('branch', '--show-current') == 'feature/tests'
assert not (P / 'evaluation/eval-v1').exists() and not (P / 'evaluation/freeze-public-v1.json').exists()
now = datetime.now(timezone.utc).isoformat()
mode = sys.argv[1]
if mode == 'prepare':
    assert git('diff', '--cached', '--name-only') == ''
    baseline = {ROOT / item['path'] for item in load(LAST / 'baseline.json')['files']}
    baseline.update(selected())
    baseline.add(ROOT / 'docs/handoff/2026-10-09-M-POC1C-review-006.md')
    save('baseline.json', {'recorded_at_utc': now, 'files': [ref(path) for path in sorted(baseline)], 'allowed_public_updates': PUBLIC})
    candidate = load(C / 'manifest.json')
    for item in [*candidate['artifacts'], *candidate['provenance']]:
        assert ref(ROOT / item['path']) == item, item
    paths = selected()
    logs = set()
    tracked = set(git('ls-files').splitlines())
    missing_private_refs = []
    for path in sorted(paths):
        if path.suffix != '.json':
            continue
        for item in nested_refs(load(path)):
            rel = item['path']
            if rel.startswith('private/') and rel not in tracked and ROOT / rel not in paths:
                target = ROOT / rel
                if target.is_file() and rel.startswith('private/poc/_checks/'):
                    assert target.name in {'pytest.log', 'result.json', 'diff-check.log'}, rel
                    assert ref(target) == item, item
                    logs.add(target)
                else:
                    missing_private_refs.append(item)
    assert not missing_private_refs, missing_private_refs
    paths.update(logs)
    save('publication-inventory.json', {
        'recorded_at_utc': now, 'branch': 'feature/tests', 'remote': 'origin', 'parent_head': git('rev-parse', 'HEAD'),
        'actual_owner_authorization': ref(HERE / 'owner-publication-authorization.raw.txt'),
        'publication_is_scope_or_freeze_approval': False, 'candidate': ref(C / 'manifest.json'),
        'files': [ref(path) for path in sorted(paths)], 'related_check_logs': [ref(path) for path in sorted(logs)],
        'publication_method': 'explicit paths via git add -f; existing /private/ ignore policy unchanged; existing -text attributes preserve private bytes',
        'excluded': ['.venv', 'pytest temp/basetemp contents', 'unrelated private/legacy files', 'credentials'],
        'git_operations_authorized': ['scoped add', 'commit', 'normal push origin feature/tests'],
        'not_authorized': ['freeze', 'extraction', 'other stages', 'reset/clean/stash', 'branch switching', 'force push', 'global Git config'],
    })
    print(json.dumps({'private_files': len(paths), 'related_logs': len(logs), 'candidate': ref(C / 'manifest.json')}, indent=2))
elif mode == 'close':
    check_root = (ROOT / sys.argv[2]).resolve()
    assert check_root.is_relative_to((ROOT / 'private/poc/_checks').resolve())
    result = load(check_root / 'result.json')
    assert result['tests_exit'] == result['diff_exit'] == 0
    log = (check_root / 'pytest.log').read_text(encoding='utf-8-sig')
    assert re.search(r'\b93 passed\b', log)
    baseline = load(HERE / 'baseline.json')
    changed, unchanged = [], []
    for item in baseline['files']:
        actual = ref(ROOT / item['path'])
        if actual == item:
            unchanged.append(actual)
        else:
            assert item['path'] in PUBLIC, (item, actual)
            changed.append({'before': item, 'after': actual})
    inventory = load(HERE / 'publication-inventory.json')
    for item in inventory['files']:
        assert ref(ROOT / item['path']) == item
    git('diff', '--check')
    save('completion.json', {
        'recorded_at_utc': now, 'date': '2026-10-09', 'timezone': 'Europe/Warsaw', 'card': 'M-POC1C',
        'result': 'partial', 'workflow_status': 'waiting_review', 'milestone': 'M-POC1', 'milestone_status': 'next',
        'branch': 'feature/tests', 'parent_head_before_commit': git('rev-parse', 'HEAD'),
        'candidate': inventory['candidate'], 'owner_publication_authorization': inventory['actual_owner_authorization'],
        'publication_inventory': ref(HERE / 'publication-inventory.json'),
        'latest_semantic_review_closure': ref(LAST / 'closure-seal-after-decision-05.json'),
        'pending_question': ref(LAST / 'pending-question-06-scope.json'),
        'actual_semantic_C_decisions': 5, 'scope_policy_approved': False, 'freeze_authorized': False, 'frozen': False,
        'remaining_decisions': ['Scope/grouping/rubrics/retained limits and thresholds', 'Distinct actual owner freeze decision'],
        'checks': {'pytest': '93 passed', 'result': result, 'local_TMP_TEMP': str(check_root / 'temp'), 'new_basetemp': True,
                   'logs': [ref(check_root / 'pytest.log'), ref(check_root / 'result.json')], 'git_diff_check_exit': 0},
        'preservation': {'unchanged_files': unchanged, 'intentional_public_updates': changed},
        'measurement': {'active_user_time': 'unknown', 'active_model_time': 'unknown', 'tokens': 'unknown', 'cost': 'unknown',
                        'model_selector_owner_report': 'sol', 'exact_model_version': 'unknown', 'reasoning_selector': 'unknown'},
        'publication_status_at_recording': 'prepared for explicitly authorized commit/push; verify committed and remote tree after publication',
        'historical_time_paths': 'Absolute paths in old measurements are historical; resolve new work from repository root. Do not rewrite history.',
        'no_extraction_or_other_cards': True,
    })
    save('closure-seal.json', {'recorded_at_utc': now, 'completion': ref(HERE / 'completion.json'),
                             'publication_inventory': ref(HERE / 'publication-inventory.json'),
                             'public_documents': [ref(ROOT / name) for name in (*PUBLIC, HANDOFF)],
                             'scope_policy_approved': False, 'freeze_authorized': False, 'frozen': False})
    print(json.dumps({'preserved_files': len(unchanged), 'closure_seal': ref(HERE / 'closure-seal.json')}, indent=2))
elif mode == 'stage':
    assert git('diff', '--cached', '--name-only') == ''
    inventory = load(HERE / 'publication-inventory.json')
    paths = {ROOT / item['path'] for item in inventory['files']}
    paths.update(path for path in HERE.iterdir() if path.is_file())
    for item in load(HERE / 'completion.json')['checks']['logs']:
        paths.add(ROOT / item['path'])
    paths.update(ROOT / name for name in PUBLIC)
    paths.update(path for path in (ROOT / 'docs/handoff').iterdir() if path.is_file() and ('M-POC1C-review-' in path.name or path.name == Path(HANDOFF).name))
    names = sorted(path.relative_to(ROOT).as_posix() for path in paths)
    for n in range(0, len(names), 25):
        git('add', '-f', '--', *names[n:n+25])
    staged = set(git('diff', '--cached', '--name-only').splitlines())
    assert staged == set(names), (staged - set(names), set(names) - staged)
    for name in sorted(staged):
        if name.startswith('private/'):
            private_blob_matches(ref(ROOT / name), '')
    git('diff', '--cached', '--check')
    print(json.dumps({'staged_files': len(staged), 'private_blobs_byte_exact': len([n for n in staged if n.startswith('private/')])}, indent=2))
elif mode == 'verify':
    # Read-only verification after commit/push or after clone; does not execute old assembly scripts.
    inventory = load(HERE / 'publication-inventory.json')
    for item in inventory['files']:
        assert ref(ROOT / item['path']) == item, item
        private_blob_matches(item, 'HEAD')
    for path in HERE.iterdir():
        if path.is_file():
            private_blob_matches(ref(path), 'HEAD')
    for item in load(C / 'manifest.json')['artifacts']:
        assert ref(ROOT / item['path']) == item
        private_blob_matches(item, 'HEAD')
    for item in load(HERE / 'completion.json')['checks']['logs']:
        assert ref(ROOT / item['path']) == item
        private_blob_matches(item, 'HEAD')
    source = ref(P / 'source/original-pdf-20261008-01.pdf')
    assert source['sha256'] == 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
    private_blob_matches(source, 'HEAD')
    assert git('diff', '--cached', '--name-only') == ''
    assert git('status', '--porcelain', '--untracked-files=all') == ''
    print(json.dumps({'verified_commit': git('rev-parse', 'HEAD'), 'branch': 'feature/tests',
                      'private_publication_files': len(inventory['files']), 'source_byte_exact': True,
                      'candidate_manifest': ref(C / 'manifest.json'), 'clean_worktree': True,
                      'scope_policy_approved': False, 'freeze_authorized': False}, indent=2))
else:
    raise SystemExit('Use prepare, close CHECK_ROOT, stage or verify.')
