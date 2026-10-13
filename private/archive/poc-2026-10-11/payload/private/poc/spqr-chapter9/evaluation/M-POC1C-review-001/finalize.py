"""Record actual partial closure and controls, without freezing evaluation."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
P = ROOT / 'private/poc/spqr-chapter9'
C = P / 'evaluation/eval-v1-candidate-20261008-02'
CHECK = ROOT / 'private/poc/_checks/active-0d5188fc3b364cb2bd6dd5576ba6b14c'
MEASUREMENT = P / 'measurement/M-POC1C-review-001'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def ref(path):
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha, 'bytes': path.stat().st_size}


def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


manifest = load(C / 'manifest.json')
for item in [*manifest['artifacts'], *manifest['provenance']]:
    assert ref(ROOT / item['path']) == item, item
baseline = load(HERE / 'baseline.json')
allowed = set(baseline['allowed_public_updates'])
changed, unchanged = [], []
for item in baseline['files']:
    current = ref(ROOT / item['path'])
    if current != item:
        assert item['path'] in allowed, (item, current)
        changed.append({'before': item, 'after': current})
    else:
        unchanged.append(current)

result = load(CHECK / 'result.json')
assert result['tests_exit'] == result['diff_exit'] == 0
pytest_log = (CHECK / 'pytest.log').read_text(encoding='utf-8-sig')
assert '87 passed' in pytest_log
git_prefix = ['git', '-c', 'safe.directory=C:/dev/wargame-compiler']
git_env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}
diff = subprocess.run([*git_prefix, 'diff', '--check'], cwd=ROOT, env=git_env, capture_output=True, text=True)
assert diff.returncode == 0
branch = subprocess.run([*git_prefix, 'branch', '--show-current'], cwd=ROOT, env=git_env, check=True, capture_output=True, text=True).stdout.strip()
head = subprocess.run([*git_prefix, 'rev-parse', 'HEAD'], cwd=ROOT, env=git_env, check=True, capture_output=True, text=True).stdout.strip()
staged = subprocess.run([*git_prefix, 'diff', '--cached', '--quiet'], cwd=ROOT, env=git_env, capture_output=True, text=True)
assert branch == 'feature/tests' and head == '90535261a4498cabcd6abc0af33b56a4267b6193'
assert staged.returncode == 0
assert not (P / 'evaluation/eval-v1').exists() and not (P / 'evaluation/freeze-public-v1.json').exists()
MEASUREMENT.mkdir()
completion = {
    'id': 'M-POC1C-review-001-partial', 'date': '2026-10-08', 'timezone': 'Europe/Warsaw',
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(), 'card': 'M-POC1C',
    'outcome': 'partial', 'workflow_status': 'waiting_review', 'milestone': 'M-POC1',
    'milestone_status': 'next', 'next_card': 'M-POC1C', 'branch': branch, 'head': head,
    'source': ref(P / 'source/original-pdf-20261008-01.pdf'),
    'candidate_manifest': ref(C / 'manifest.json'), 'audit': ref(HERE / 'audit.json'),
    'validation': ref(HERE / 'validation.json'), 'pending_question': ref(HERE / 'pending-question.json'),
    'actual_new_owner_decisions': [], 'freeze_authorized': False, 'frozen': False,
    'previous_freeze_question_disposition': 'withdrawn as premature; candidate 01 was not a complete scoring basis',
    'latest_user_message': 'Podbiłem model na sol',
    'latest_message_is_approval': False,
    'counts': manifest['counts'],
    'open_gates': manifest['open_gates'],
    'limitations': 'Detailed retained source/semantic limits and exact ID scopes are in the candidate review and JSON files; no external parameter was invented.',
    'checks': {
        'invocation': 'scripts/check.ps1 -Python C:/dev/wargame-compiler/.venv/Scripts/python.exe',
        'actual_result': result, 'pytest': '87 passed',
        'local_TMP_and_TEMP': str(CHECK / 'temp'), 'new_basetemp': True,
        'logs': [ref(CHECK / 'pytest.log'), ref(CHECK / 'result.json')],
        'diff_check_log': 'not created because successful git diff --check emitted no output',
        'separate_final_git_diff_check': {'exit': diff.returncode, 'stdout': diff.stdout, 'stderr': diff.stderr},
    },
    'preservation': {
        'baseline_checked': len(baseline['files']), 'unchanged_files': len(unchanged),
        'intentional_public_updates': changed,
        'historical_and_candidate01_files_preserved': True,
        'all_prior_B_manifest_references_verified': 440,
        'historical_archive_9298_file_audit_repeated': False,
        'Git_index_unchanged_against_current_session_baseline': True,
        'historical_Git_index_hashes': 'Historical only; later authorized commits/pushes are not reversions to perform.',
        'staged_diff_exit': staged.returncode,
        'new_private_files': 'Ignored by /private/ despite existing tracked private files; no staging/commit/push performed.',
    },
    'measurement': {
        'application': 'Codex', 'model_selector_owner_report': 'sol', 'exact_model_visible_version': 'unknown',
        'reasoning_selector': 'unknown', 'user_active_time': 'unknown', 'model_active_time': 'unknown',
        'tokens': 'unknown', 'cost': 'unknown', 'remaining_user_budget': 'unknown',
        'calendar_time_is_active_work': False, 'M_POC0_cost_included': False,
    },
    'quality_metrics': 'n/a: no eval freeze or extractor response',
    'plan_thresholds_changed': False, 'plan_limits_changed': False,
    'MPOC2A_executed': False, 'MPOC2B_executed': False, 'semantic_extraction_run': False,
    'forbidden_work_performed': [],
}
save(HERE / 'completion.json', completion)
save(MEASUREMENT / 'completion.json', completion)
seal = {
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(), 'card': 'M-POC1C',
    'outcome': 'partial', 'workflow_status': 'waiting_review', 'frozen': False,
    'candidate_manifest': ref(C / 'manifest.json'), 'completion': ref(HERE / 'completion.json'),
    'measurement_completion': ref(MEASUREMENT / 'completion.json'),
    'public_documents': [ref(ROOT / name) for name in ('docs/STATUS.md','docs/ROADMAP.md','docs/HANDOFF.md','docs/handoff/2026-10-08-M-POC1C-review-001.md')],
    'next': {'milestone':'M-POC1','card':'M-POC1C','question':'M-POC1C-RQ-01-DEP008'},
    'scripts': [ref(HERE / name) for name in ('prepare.py','seal_candidate.py','finalize.py')],
    'no_self_hash_cycle': True,
}
save(HERE / 'closure-seal.json', seal)
print(json.dumps({'candidate_manifest': ref(C / 'manifest.json'), 'completion': ref(HERE / 'completion.json'),
                  'closure_seal': ref(HERE / 'closure-seal.json'), 'preserved_files':len(unchanged),
                  'test_result':'87 passed','final_diff_check':diff.returncode},indent=2))
