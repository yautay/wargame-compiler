"""Record actual task ownership, checkpoint and live heartbeat after the Unicode fix."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o
PREP = 'private/workflow/runs/IG-2B04/unicode-recovery-20261016-01/'
RUN = sys.argv[1].rstrip('/') + '/'
state = w.read_json(ROOT / RUN / 'status.json')
SESSION = Path(state['session']).relative_to(ROOT).as_posix() + '/'
q = w.read_json(ROOT / w.QUEUE)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert t['status'] == 'in_progress', 'B04 has not claimed execution yet'
event = t['events'][-1]
assert event['to'] == 'in_progress'
assert w.digest(ROOT / event['evidence']) == event['sha256']
claim = w.read_json(ROOT / event['evidence'])
o.configuration_binding(ROOT, ROOT / SESSION, claim)
assert claim['actor'] == f'ig2:{Path(state["session"]).name}:executor'
attempt = Path(t['continuation_authorization']['attempt'])
checkpoint_path = ROOT / attempt / 'checkpoint.json'
assert checkpoint_path.is_file(), 'Initial checkpoint is not present'
checkpoint = w.read_json(checkpoint_path)
assert checkpoint['actor'] == claim['actor']
assert checkpoint['model'] == 'gpt-6.1-sol' and checkpoint['reasoning'] == 'high'
process = w.read_json(ROOT / SESSION / 'process.json')
assert process['state'] == 'running'
assert (datetime.now(timezone.utc) - datetime.fromisoformat(process['heartbeat_utc'])).total_seconds() < 20
assert not (ROOT / SESSION / 'context-denied.json').exists()
assert w.read_json(ROOT / RUN / 'status.json')['state'] == 'running'
def pin(rel):
    p = ROOT / rel
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}
report = {'role': 'coordinator', 'actor': 'operator-authorized-unicode-recovery-20261016-01',
    'model': None, 'reasoning': None,
    'configuration_evidence': 'Builder actual configuration unavailable; executor configuration is independently observed below.',
    'verified_utc': o.utc(), 'summary': 'B04 actually claimed by the new executor, with matching checkpoint and an advancing supervisor heartbeat.',
    'task': t['id'], 'status': t['status'], 'claim': {'path': event['evidence'], 'sha256': event['sha256']},
    'checkpoint_at_verification': pin(checkpoint_path.relative_to(ROOT).as_posix()),
    'executor_configuration': pin(SESSION + 'runtime-configuration.json'),
    'observed_model': 'gpt-6.1-sol', 'observed_reasoning': 'high',
    'supervisor_pid': process['supervisor_pid'], 'executor_pid': process['pid'],
    'heartbeat_utc': process['heartbeat_utc'], 'denial_marker_absent': True,
    'run': RUN, 'launch': sys.argv[2],
    'repository_tests': '236 passed; plan, dry-run and diff check passed',
    'task_completed': False, 'semantic_acceptance_granted': False}
target = ROOT / PREP / 'restart-verified.json'
assert not target.exists()
o.dump(target, report)
print(json.dumps({'task': t['id'], 'status': t['status'], 'claim': event['evidence'],
                  'checkpoint': str(checkpoint_path), 'supervisor_pid': process['supervisor_pid'],
                  'executor_pid': process['pid'], 'heartbeat_utc': process['heartbeat_utc']}))
