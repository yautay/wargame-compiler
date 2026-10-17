"""Complete recovery after verifying the existing preservation gate's exact pin shape."""
import copy
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o
PREP = 'private/workflow/runs/IG-2B04/recovery-20261015-03/'
OLD = 'private/workflow/runs/IG-2B04/inventory-13-16-f870c628-01/'
NEW = 'private/workflow/runs/IG-2B04/continuation-13-16-recovery03/'
DOC = 'docs/work/repair-context/IG-2B04-interruption-recovery03.md'
def pin(rel):
    p = ROOT / rel
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}
def write(rel, body):
    assert not (ROOT / rel).exists(), rel
    o.dump(ROOT / rel, body)
    return pin(rel)
q = w.read_json(ROOT / w.QUEUE)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert t['status'] == 'in_progress' and not (ROOT / NEW).exists()
before = copy.deepcopy(t)
blocked = pin(OLD + 'blocked.json')
common = w.read_json(ROOT / PREP / 'authorization.json')
common = {k: v for k, v in common.items() if k not in {'artifacts', 'summary', 'readiness_granted', 'semantic_acceptance_granted'}}
preserve = w.read_json(ROOT / PREP / 'preserve.json')
preserve['artifacts'].append({'path': blocked['path'], 'sha256': blocked['sha256']})
preserve_pin = write(PREP + 'preserve-02.json', preserve)
scope = w.read_json(ROOT / PREP / 'scope.json')
scope['preserve_manifest'] = preserve_pin
scope_pin = write(PREP + 'scope-02.json', scope)
contract = w.read_json(ROOT / PREP / 'execution-contract.json')
contract['recovery_scope'] = scope_pin
contract_pin = write(PREP + 'execution-contract-02.json', contract)
authorization = write(PREP + 'authorization-02.json', {**common,
    'summary': 'Explicit operator recovery; exact preservation pin shapes verified. All original gates retained; no source inspection or acceptance inherited.',
    'artifacts': [scope_pin, preserve_pin, contract_pin, pin(PREP + 'assessment.json')],
    'readiness_granted': True, 'semantic_acceptance_granted': False})
w.transition(q, ROOT, t['id'], 'blocked', blocked['path'])
t['continuation_authorization'] = {'scope': scope_pin, 'evidence': authorization, 'attempt': NEW,
    'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256']}
t['inventory_contract'] = contract_pin
t['outputs'] = [v.replace(OLD, NEW) for v in t['outputs']]
t['write_scope'] = [NEW, 'private/workflow/runs/IG-2B04/', 'private/workflow/checks/', 'private/workflow/packets/']
t['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md',
                'docs/work/repair-context/IG-2B04-context-access-02.md', DOC]
t['inputs'] = [v for v in t['inputs'] if not v.startswith('Exact execution contract:')]
t['inputs'].append('Exact recovery contract: ' + contract_pin['path'] + ' SHA256 ' + contract_pin['sha256'])
t['start_conditions'].append('Recovery03 supersedes the interrupted output path; preserve the blocked attempt, use only named draft JSON and a fresh absent continuation root.')
doc = ROOT / DOC
text = doc.read_text(encoding='utf-8')
old_contract = pin(PREP + 'execution-contract.json')
write(PREP + 'preparation-error.json', {**common,
    'summary': 'First preservation validation rejected the blocked-event pin with an extra bytes field. Queue stayed unchanged. New immutable manifests retain both exact pin representations; no gate weakened.',
    'artifacts': [pin(PREP + 'preserve.json'), pin(PREP + 'scope.json'), old_contract]})
doc.write_text(text.replace(old_contract['path'], contract_pin['path']).replace(old_contract['sha256'], contract_pin['sha256']), encoding='utf-8')
w.transition(q, ROOT, t['id'], 'planned', authorization['path'])
w.transition(q, ROOT, t['id'], 'ready', authorization['path'])
assert t['acceptance'] == before['acceptance'] and t['tests'] == before['tests']
o.continuation_preservation(ROOT, t, require_absent=True)
o.dump(ROOT / w.QUEUE, q)
w.render(q, ROOT)
w.validate(q, ROOT)
print(json.dumps({'task': t['id'], 'status': t['status'], 'preserved': len(preserve['artifacts']), 'scope': scope_pin}))
