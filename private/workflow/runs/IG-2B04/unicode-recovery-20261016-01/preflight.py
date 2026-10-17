"""Operator-authorized fresh preflight after the Windows search encoding failure."""
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B04/unicode-recovery-20261016-01/'
OLD_RUN = 'private/workflow/orchestrator/20261015T204557Z-7260655f/'
OLD_SESSION = OLD_RUN + '001-IG-2B04-executor-4db8b52e/'
def pin(rel):
    p = ROOT / rel
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}

q = w.read_json(ROOT / w.QUEUE)
before = w.digest(ROOT / w.QUEUE)
task = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert task['status'] == 'ready'
assert not (ROOT / task['continuation_authorization']['attempt']).exists()
assert not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
old_status = w.read_json(ROOT / OLD_RUN / 'status.json')
assert old_status['state'] == 'blocked'
denial = w.read_json(ROOT / OLD_SESSION / 'context-denied.json')
assert 'charmap' in denial['reason'] and '\\u2192' in denial['reason']
session = ROOT / PREP / 'preflight'
session.mkdir(exist_ok=False)
o.prepare(ROOT, q, task, 'executor', session)
env = o.launch_environment(ROOT, task, session)
env.update(PYTHONIOENCODING='cp1252:strict', PYTHONUTF8='0')
result = subprocess.run([sys.executable, str(ROOT / 'scripts/search_task.py'),
    '--pattern', 'claim|configuration_sha256|checkpoint|in_progress', '--file', 'scripts/workflow.py'],
    cwd=ROOT, env=env, capture_output=True, timeout=12)
(session / 'search.stdout.json').write_bytes(result.stdout)
(session / 'search.stderr.log').write_bytes(result.stderr)
assert result.returncode == 0, result.stderr.decode('ascii', errors='replace')
assert not (session / 'context-denied.json').exists()
output = json.loads(result.stdout.decode('ascii'))
assert output['matches']
assert any('\u2192' in match['text'] for match in output['matches'])
assert len(result.stdout) <= output['max_output_bytes']
assert w.digest(ROOT / w.QUEUE) == before
assessment = {'role': 'coordinator', 'actor': 'operator-authorized-unicode-recovery-20261016-01',
    'model': None, 'reasoning': None,
    'configuration_evidence': 'Builder actual model/reasoning unavailable; no Sol/high claim.',
    'operator_request': 'Fix Windows search encoding, add a test, restart IG-2 and verify B04 actually starts.',
    'observed_utc': o.utc(),
    'summary': 'Search serialized literal Unicode to a legacy Windows pipe. Shared ASCII JSON serialization fixes the encoding failure without changing source bytes, guard behavior or task scope.',
    'incident': [pin(OLD_RUN + 'status.json'), pin(OLD_SESSION + 'context-denied.json'),
                 pin(OLD_SESSION + 'runtime-configuration.json'), pin(OLD_SESSION + 'process-result.json')],
    'queue_sha256_before_launch': before, 'task_status': task['status'],
    'fresh_output_absent': True, 'existing_lock_absent': True,
    'authorized_attempt': task['continuation_authorization']['attempt'],
    'preflight': {'command': 'Exact previously failing scoped search, with fresh current hash pins and cp1252:strict stdout, active guard, no model.',
                  'exit_code': result.returncode, 'matches': len(output['matches']),
                  'arrow_preserved_after_json_decode': True, 'denial_marker_absent': True,
                  'serialized_bytes': len(result.stdout), 'queue_unchanged': True,
                  'output': pin(PREP + 'preflight/search.stdout.json')},
    'checks': {'focused_unicode_regressions': '6 passed', 'required_repository_checks': 'Recorded separately before launch'},
    'semantics_accepted': False, 'models_launched': 0}
assert not (ROOT / PREP / 'assessment.json').exists()
o.dump(ROOT / PREP / 'assessment.json', assessment)
print(json.dumps({'result': 'passed', 'matches': len(output['matches']),
                  'arrow_preserved': True, 'queue_unchanged': True, 'models_launched': 0}))
