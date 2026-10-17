"""Resume bounded IG-2 coordination after verifying the toolchain parser fix."""
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
preflight = w.read_json(prep / 'preflight-result.json')
if task['id'] != 'IG-2B06' or role != 'coordinator' or task['status'] != 'planned':
    raise ValueError('Expected planned IG-2B06 coordinator; reconcile ownership')
if preflight['queue_sha256'] != w.digest(ROOT / w.QUEUE):
    raise ValueError('Queue changed after verified preparation')
o.verify_artifacts(ROOT, preflight)
check_root = 'private/workflow/checks/active-10b2b8774071430598e39b2732a79e97/'
result = w.read_json(ROOT / (check_root + 'result.json'))
if any(result[k] != 0 for k in ('plan_exit', 'tests_exit', 'diff_exit')):
    raise ValueError('Queue, suite or diff verification failed')
if result['dry_run_exit'] != 1 or (ROOT / (check_root + 'dry-run.log')).read_text(encoding='utf-8-sig').strip() != 'ERROR: Task is not ready or active':
    raise ValueError('Unexpected dry-run result; do not bypass another check failure')
# This launch is contract refinement only. Product delivery still requires all
# unchanged checks after the coordinator establishes ready execution ownership.
previous = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
rg = previous['ripgrep']
if not Path(previous['codex']).is_file() or w.digest(Path(rg['path'])) != rg['sha256']:
    raise ValueError('Installed runtime changed')
record = {'utc': datetime.now(timezone.utc).isoformat(),
    'operator_request': 'Fix toolchain.json reading and resume the orchestrator from IG-2B06.',
    'task': task['id'], 'role': role, 'queue_sha256': w.digest(ROOT / w.QUEUE),
    'checks': result, 'check_logs': check_root,
    'state_dependent_dry_run': 'The unchanged legacy dry-run requires ready/active state. No task currently has that state. Actual planned-coordinator preparation and launch environment were separately verified; this authorizes refinement only, not delivery or acceptance.',
    'actual_model': None, 'actual_reasoning': None,
    'configuration_evidence': 'Current coordinator metadata unavailable; child model/reasoning must be observed from CLI startup.',
    'old_processes': 'Approved Win32_Process inspection found neither prior supervisor PID 11900 nor reviewer PID 20964. No supervisor or queue lock remains.',
    'preflight': {'path': (prep / 'preflight-result.json').relative_to(ROOT).as_posix(), 'sha256': w.digest(prep / 'preflight-result.json')}}
with (prep / 'launch-authorization.json').open('x', encoding='utf-8') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
env = dict(os.environ, WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
           PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
launch = subprocess.run([sys.executable, 'scripts/orchestrate_ig2.py', 'start', '--codex', previous['codex']],
                        cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', timeout=60)
with (prep / 'start-result.json').open('x', encoding='utf-8') as stream:
    json.dump({'exit_code': launch.returncode, 'stdout': launch.stdout, 'stderr': launch.stderr}, stream, indent=2)
    stream.write('\n')
print(launch.stdout, end='')
if launch.stderr:
    print(launch.stderr, file=sys.stderr, end='')
sys.exit(launch.returncode)
