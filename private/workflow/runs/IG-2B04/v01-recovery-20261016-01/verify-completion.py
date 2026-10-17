"""Record independent technical acceptance and preservation after validation-only repair."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o
PREP = 'private/workflow/runs/IG-2B04/v01-recovery-20261016-01/'
ORIGINAL = 'private/workflow/runs/IG-2B04/continuation-13-16-rg04/delivery-manifest.json'
RUN = 'private/workflow/orchestrator/20261016T142331Z-0d4dc364/'
def pin(rel):
    p = ROOT / rel
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}
q = w.read_json(ROOT / w.QUEUE)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert t['status'] == 'done', 'B04 has not passed independent review and closure yet'
accepted_event = next(e for e in reversed(t['events']) if e['to'] == 'accepted')
delivery_event = next(e for e in reversed(t['events']) if e['to'] == 'review')
done_event = t['events'][-1]
assert done_event['to'] == 'done'
for event in (accepted_event, delivery_event, done_event):
    assert pin(event['evidence'])['sha256'] == event['sha256']
review = w.read_json(ROOT / accepted_event['evidence'])
delivery = w.read_json(ROOT / delivery_event['evidence'])
done = w.read_json(ROOT / done_event['evidence'])
original = w.read_json(ROOT / ORIGINAL)
assert len(original['artifacts']) == 2325
assert delivery['artifacts'][:2325] == original['artifacts']
assert review['artifacts'] == delivery['artifacts'] == done['artifacts']
assert review['actor'] != delivery['actor']
assert review['outcome'] == 'pass' and not review.get('findings')
assert review['criteria'] == t['acceptance']
assert review['checks'] and all(c['exit_code'] == 0 for c in review['checks'])
assert done['checks'] and all(c['exit_code'] == 0 for c in done['checks'])
assert not t['semantic_acceptance_required']
o.verify_artifacts(ROOT, original)
o.verify_artifacts(ROOT, delivery)
o.continuation_preservation(ROOT, t)
executor_config = w.read_json(ROOT / delivery['configuration_evidence'])
reviewer_config = w.read_json(ROOT / review['configuration_evidence'])
for config in (executor_config, reviewer_config):
    assert config['status'] == 'confirmed' and config['model'] == 'gpt-6.1-sol' and config['reasoning'] == 'high'
assert executor_config['session_id'] != reviewer_config['session_id']
state = w.read_json(ROOT / RUN / 'status.json')
runtime_state = {'state': state['state'], 'task': state.get('task'), 'role': state.get('role')}
if state['state'] == 'running':
    process = w.read_json(Path(state['session']) / 'process.json')
    runtime_state.update(supervisor_pid=process['supervisor_pid'], executor_pid=process['pid'],
                         heartbeat_utc=process.get('heartbeat_utc'), process_state=process['state'])
    if process['state'] == 'running':
        assert (datetime.now(timezone.utc) - datetime.fromisoformat(process['heartbeat_utc'])).total_seconds() < 20
report = {'role': 'coordinator', 'actor': 'operator-authorized-v01-recovery-20261016-01',
    'model': None, 'reasoning': None, 'configuration_evidence': 'Builder actual configuration unavailable; fresh executor/reviewer metadata independently verified.',
    'verified_utc': o.utc(), 'task': t['id'], 'status': t['status'],
    'summary': 'Validation-only repair passed fresh independent review and deterministic supervisor checks; B04 accepted and done with every original reviewed artifact unchanged.',
    'original_delivery': pin(ORIGINAL), 'original_artifacts_verified_unchanged': 2325,
    'delivery': pin(delivery_event['evidence']), 'independent_review': pin(accepted_event['evidence']),
    'closure': pin(done_event['evidence']), 'complete_delivery_artifacts': len(delivery['artifacts']),
    'executor_actor': delivery['actor'], 'reviewer_actor': review['actor'],
    'executor_configuration': pin(delivery['configuration_evidence']),
    'reviewer_configuration': pin(review['configuration_evidence']),
    'review_checks': [{'command': c['command'], 'exit_code': c['exit_code']} for c in review['checks']],
    'supervisor_and_review_checks': [{'command': c['command'], 'exit_code': c['exit_code']} for c in done['checks']],
    'accepted_event': accepted_event, 'done_event': done_event, 'orchestrator': runtime_state,
    'source_regenerated_by_this_repair': False, 'semantic_acceptance_granted': False}
target = ROOT / PREP / 'completion-verified.json'
assert not target.exists()
o.dump(target, report)
print(json.dumps({'task': t['id'], 'status': t['status'], 'original_artifacts_unchanged': 2325,
                  'independent_review': accepted_event['evidence'], 'review_outcome': review['outcome'],
                  'orchestrator': runtime_state}))
