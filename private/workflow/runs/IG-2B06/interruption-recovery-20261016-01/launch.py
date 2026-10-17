"""Start the reconciled B06 continuation after unchanged checks succeed."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

prep = Path(__file__).resolve().parent
q = w.read_json(ROOT / w.QUEUE)
w.validate(q, ROOT)
task, role = o.select(q)
if task['id'] != 'IG-2B06' or role != 'executor' or task['status'] != 'ready':
    raise ValueError('Expected fresh ready B06 executor; reconcile ownership')
recovery = w.read_json(prep / 'recovery-result.json')
if recovery['queue_sha256'] != w.digest(ROOT / w.QUEUE):
    raise ValueError('Queue changed after recovery preparation')
preserved = o.continuation_preservation(ROOT, task, require_absent=True)
check_root = 'private/workflow/checks/active-0d030e315b654e96a07f5518fff6820d/'
checks = w.read_json(ROOT / (check_root + 'result.json'))
if any(checks[k] != 0 for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit')):
    raise ValueError('Required checks are not green')
previous = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
rg = previous['ripgrep']
if not Path(previous['codex']).is_file() or w.digest(Path(rg['path'])) != rg['sha256']:
    raise ValueError('Installed runtime binding changed')
record = {'utc': datetime.now(timezone.utc).isoformat(),
    'operator_requested_recovery': True, 'task': task['id'], 'role': role,
    'queue_sha256': w.digest(ROOT / w.QUEUE), 'preserved_artifacts': len(preserved),
    'checks': checks, 'check_logs': check_root,
    'actual_model': None, 'actual_reasoning': None,
    'configuration_evidence': 'Exact coordinating model/reasoning unavailable. Next executor must confirm actual startup metadata.',
    'cause_limit': 'Named-pipe access failure and Windows launcher PID mismatch were confirmed. The external cause of abrupt old supervisor/CLI termination remains unknown.',
    'artifacts': [{'path': rel, 'sha256': w.digest(ROOT / rel)} for rel in (
        'scripts/orchestrate_ig2.py', 'tests/test_orchestrator.py', 'docs/work/IG2-ORCHESTRATOR.md',
        check_root + 'result.json')]}
with (prep / 'launch-preflight.json').open('x', encoding='utf-8') as f:
    json.dump(record, f, indent=2)
    f.write('\n')
env = dict(os.environ, WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
           PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
result = subprocess.run([sys.executable, 'scripts/orchestrate_ig2.py', 'start', '--codex', previous['codex']],
                        cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=60)
with (prep / 'start-result.json').open('x', encoding='utf-8') as f:
    json.dump({'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}, f, indent=2)
    f.write('\n')
print(result.stdout, end='')
if result.stderr:
    print(result.stderr, file=sys.stderr, end='')
sys.exit(result.returncode)
