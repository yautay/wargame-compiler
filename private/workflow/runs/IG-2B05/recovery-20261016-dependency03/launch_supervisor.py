"""Launch the existing bounded supervisor after successful recovery preflight."""
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
task = next(t for t in q['tasks'] if t['id'] == 'IG-2B05')
if task['status'] != 'ready':
    raise ValueError('Task is no longer ready; reconcile ownership')
preserved = o.continuation_preservation(ROOT, task, require_absent=True)
check_root = 'private/workflow/checks/active-6d3391170cb442e0a0e84245e62c01b7/'
checks = w.read_json(ROOT / (check_root + 'result.json'))
if any(checks[k] != 0 for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit')):
    raise ValueError('Required checks are not green')
previous = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
cli = previous['codex']
rg = previous['ripgrep']
if not Path(cli).is_file() or w.digest(Path(rg['path'])) != rg['sha256']:
    raise ValueError('Installed runtime binding changed')
record = {'operator_request': 'wznow prace', 'task': task['id'],
          'coordinator_actual_model': None, 'coordinator_actual_reasoning': None,
          'configuration_evidence': 'Not exposed in current coordinating session; next executor must confirm startup metadata.',
          'checks': [
              {'command': 'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B05', 'exit_code': 0,
               'result': '257 passed in 33.79s', 'logs': check_root},
              {'command': 'git diff --check', 'exit_code': 0}],
          'preserved_artifacts': len(preserved), 'queue_sha256': w.digest(ROOT / w.QUEUE),
          'artifacts': [{'path': p, 'sha256': w.digest(ROOT / p)} for p in (
              'scripts/orchestrate_ig2.py', 'tests/test_orchestrator.py', check_root + 'result.json')],
          'codex': {'path': cli, 'sha256': w.digest(Path(cli))}, 'ripgrep': rg}
with (prep / 'launch-preflight.json').open('x', encoding='utf-8') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
env = dict(os.environ, WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
           PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
result = subprocess.run([sys.executable, 'scripts/orchestrate_ig2.py', 'start', '--codex', cli],
                        cwd=ROOT, env=env, capture_output=True, text=True,
                        encoding='utf-8', timeout=60)
with (prep / 'start-result.json').open('x', encoding='utf-8') as stream:
    json.dump({'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}, stream, indent=2)
    stream.write('\n')
print(result.stdout, end='')
if result.stderr:
    print(result.stderr, file=sys.stderr, end='')
sys.exit(result.returncode)
