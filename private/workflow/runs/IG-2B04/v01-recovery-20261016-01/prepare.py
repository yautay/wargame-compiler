"""Recover the unclaimed validation-only repair without changing reviewed product bytes."""
import copy
import json
from pathlib import Path
import shutil
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o
PREP = 'private/workflow/runs/IG-2B04/v01-recovery-20261016-01/'
OLD_SESSION = 'private/workflow/orchestrator/20261016T115606Z-694df602/004-IG-2B04-executor-7b1b7a3c/'
DOC = 'docs/work/repair-context/IG-2B04-v01-status-path-recovery.md'
def pin(rel):
    p = ROOT / rel
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}
def write(rel, value):
    assert not (ROOT / rel).exists(), rel
    o.dump(ROOT / rel, value)
    return pin(rel)
q = w.read_json(ROOT / w.QUEUE)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert t['status'] == 'changes_requested'
before = copy.deepcopy(q)
write(PREP + 'queue-before.json', q)
scope = o.verify_repair_authorization(ROOT, t, require_absent=True)
event, delivery = o.latest_delivery(ROOT, t)
o.verify_artifacts(ROOT, delivery)
protected = o.continuation_preservation(ROOT, t)
assert len(delivery['artifacts']) == 2325
assert not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
incident_path = ROOT / PREP / 'incident.json'
assert not incident_path.exists()
shutil.copyfile(ROOT / OLD_SESSION / 'context-denied.json', incident_path)
incident = pin(PREP + 'incident.json')
common = {'role': 'coordinator', 'actor': 'operator-authorized-v01-recovery-20261016-01',
    'task': t['id'], 'model': None, 'reasoning': None,
    'configuration_evidence': 'Builder actual configuration unavailable; no Sol/high claim.',
    'utc': o.utc(), 'operator_request': 'Fix validation PATH and STATUS manifest conflict, preserve reviewed results, restart and verify validation plus independent review.'}
assessment = write(PREP + 'assessment.json', {**common,
    'summary': 'All2325 reviewed delivery artifacts and continuation preservation verified. Prior repair session stopped before claim while reading a required generated view excluded from search; authorized repair root is still absent.',
    'current_review': {'path': t['events'][-1]['evidence'], 'sha256': t['events'][-1]['sha256']},
    'incident': incident, 'immutable_delivery': scope['immutable_delivery'],
    'reviewed_delivery_artifacts_verified': len(delivery['artifacts']), 'protected_pins_verified': len(protected),
    'prior_owned_processes_absent': True, 'repair_attempt_absent': True,
    'fixes': ['Verified rg directory is added to complete inherited PATH before native toolchain prefixes; both pinned PYTHONPATH entries retained.',
              'Only STATUS and HANDOFF receive bounded, hash-pinned dispatch snapshots via the read helper; generic volatile search remains forbidden.'],
    'source_reinspection_or_regeneration_authorized': False, 'semantic_acceptance_granted': False})
context_scope = write(PREP + 'scope.json', {**common,
    'mode': 'validation_only_context_and_environment_recovery', 'incident': incident, 'assessment': assessment,
    'repair_authorization': t['repair_authorization'], 'immutable_delivery': scope['immutable_delivery'],
    'acceptance': t['acceptance'], 'tests': t['tests'], 'attempt': scope['attempt'],
    'required': ['Preserve the complete original ordered delivery prefix byte-for-byte.',
                 'Create only fresh approved validation evidence, handoff and delivery envelope in the absent repair attempt.',
                 'No source inspection, rebuilding, replay regeneration, test/assertion/guard weakening or prior-attempt writes.',
                 'Rereview verifies preserved source-review coverage and current hashes plus all new validation evidence.',
                 'Use task_access read for STATUS/HANDOFF snapshots; do not treat them as live queue authority.']})
write(PREP + 'authorization.json', {**common, 'summary': 'Current operator authorizes the fresh validation-only restart under unchanged current V01 repair scope.',
    'artifacts': [incident, assessment, context_scope, t['repair_authorization']['scope'], t['repair_authorization']['evidence']]})
doc = f'''# IG-2B04 V01 status/PATH recovery

This fresh session follows the stopped preclaim V01 executor. Preserve the existing
repair authorization and exact current review. The incident is metadata only;
read the new context recovery scope/assessment references, never its old transcript.
The operator requested environment and bootstrap-context fixes. All2325 frozen product
artifacts, both full replays and the prior independent source review are unchanged.
No source inspection, rebuilding, reinterpretation or semantic acceptance is authorized.

Required STATUS.md and HANDOFF.md reads use scripts/task_access.py read with their
normal docs/ paths. The access manifest pins session bootstrap copies and the helper
labels them as dispatch snapshots without status authority. They remain excluded
from search; task.json and workflow transitions govern this repair.

The supervisor makes the installed hash-pinned rg directory available on PATH while
retaining every inherited entry, pinned Poppler prefix and both PYTHONPATH entries.
For approved commands, explicitly retain this same process-local environment in that
command as well: read the current repair scope's exact rg path/SHA256 and toolchain,
verify the executable hash, prepend its directory to the complete current PATH, and
set both pinned PYTHONPATH entries before running the unchanged validation command.
Approval may start another shell; never assume custom environment survived that boundary.
Record resolved rg, complete preservation of inherited PATH and actual command exits.
No test, assertion, guard, source, global setting, ACL or old-attempt edit is allowed.

Claim only the still-absent `{scope['attempt']}` using your observed Sol/high metadata.
Run the exact required repository check and explicit source suite through approved
ordinary-user execution when required. Freeze fresh evidence and create a new delivery
whose ordered artifacts start with ALL2325 original entries unchanged, then append
only new validation/repair evidence. Transition to review; do not self-accept.

Independent rereview uses the prior review's frozen source-inspection/regeneration
coverage and verifies every preserved hash. Review the new environment/validation
evidence and current complete delivery; do not repeat source rebuilding or inspection
for this validation-only finding. Pass requires all required checks at exit zero.
'''
assert not (ROOT / DOC).exists()
(ROOT / DOC).write_text(doc, encoding='utf-8')
t['context'].append(DOC)
t['context_recovery_authorization'] = {'incident': incident, 'scope': context_scope, 'assessment': assessment}
assert t['status'] == 'changes_requested' and t['events'] == next(x for x in before['tasks'] if x['id'] == t['id'])['events']
assert [x for x in before['tasks'] if x['id'] != t['id']] == [x for x in q['tasks'] if x['id'] != t['id']]
o.dump(ROOT / w.QUEUE, q)
w.render(q, ROOT)
w.validate(q, ROOT)
print(json.dumps({'task': t['id'], 'status': t['status'], 'reviewed_artifacts_unchanged': len(delivery['artifacts']),
                  'repair_attempt': scope['attempt'], 'events_unchanged': True}))
