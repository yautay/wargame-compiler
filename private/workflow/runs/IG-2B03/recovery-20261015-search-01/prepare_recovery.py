"""Operator-scoped blocked-attempt assessment and immutable recovery preparation."""
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B03/recovery-20261015-search-01/'
OLD = 'private/workflow/runs/IG-2B03/inventory-003-e285fb76/'
NEW = 'private/workflow/runs/IG-2B03/continuation-search-20261015-01/'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'bytes': p.stat().st_size, 'sha256': w.digest(p)}


def write(name, body):
    rel = PREP + name
    if (ROOT / rel).exists():
        raise ValueError('Recovery evidence must be new: ' + rel)
    o.dump(ROOT / rel, body)
    return pin(rel)


q = w.read_json(ROOT / w.QUEUE)
w.validate(q, ROOT)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B03')
assert t['status'] == 'blocked' and t['events'][-1]['evidence'] == OLD + 'blocked.json'
assert not (ROOT / NEW).exists() and not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
original_task = copy.deepcopy(t)
blocked = {'path': t['events'][-1]['evidence'], 'sha256': t['events'][-1]['sha256']}
o.verify_artifacts(ROOT, {'artifacts': [blocked]})
blocked_body = w.read_json(ROOT / blocked['path'])
o.verify_artifacts(ROOT, blocked_body)
original = w.read_json(ROOT / (OLD + 'blocked-state-manifest.json'))['artifacts']
o.verify_artifacts(ROOT, {'artifacts': original})
preserved = copy.deepcopy(original)
for p in blocked_body['artifacts'] + [blocked]:
    if p not in preserved:
        preserved.append(p)
preserve_pin = write('preserve-manifest.json', {'format': 'wgc-blocked-preservation-1', 'artifacts': preserved})

old_prep = 'private/workflow/runs/IG-2B03/preparation-003-e285fb76/'
inputs = w.read_json(ROOT / (old_prep + 'input-pins.json'))
o.verify_artifacts(ROOT, {'artifacts': inputs['files'] + inputs['context_only_evidence'] + [inputs['dependency_reference']]})
dep = next(x for x in q['tasks'] if x['id'] == 'IG-2B02')
assert dep['status'] == 'done'
accepted = {'path': dep['events'][-1]['evidence'], 'sha256': dep['events'][-1]['sha256']}
o.verify_artifacts(ROOT, {'artifacts': [accepted]})
accepted_body = w.read_json(ROOT / accepted['path'])
o.verify_artifacts(ROOT, accepted_body)
draft_names = ['authored/inventory.json', 'authored/identity-registry.json', 'authored/partition-plan.json',
               'final-verified/inventory.json', 'final-verified/identity-registry.json',
               'final-verified/coverage.json', 'text-geometry-audit.json', 'elephant-component-specifications.json']
drafts = [pin(OLD + name) for name in draft_names]
final = w.read_json(ROOT / (OLD + 'final-verified/inventory.json'))
evidence = [e[k] for e in final['evidence'] for k in ['text', 'image', 'crop_pdf']]
o.verify_artifacts(ROOT, {'artifacts': evidence})
baseline = w.read_json(ROOT / inputs['files'][0]['path'])
baseline_registry = w.read_json(ROOT / inputs['files'][1]['path'])
registry = w.read_json(ROOT / (OLD + 'final-verified/identity-registry.json'))
assigned_ids = set(t['target_ids'])
old_pages = [x for x in baseline['pages'] if x['id'] not in assigned_ids]
assert old_pages == [x for x in final['pages'] if x['id'] not in assigned_ids]
old_regions = [x for x in baseline['regions'] if x['page_id'] not in assigned_ids]
assert old_regions == [x for x in final['regions'] if x['page_id'] not in assigned_ids]
assert final['evidence'][:len(baseline['evidence'])] == baseline['evidence']
assert final['links'][:len(baseline['links'])] == baseline['links']
for entry in baseline_registry['entries']:
    assert entry in registry['entries']
missing = [rel[len(OLD):] for rel in t['outputs'] if not (ROOT / rel).is_file()]
assessment = write('assessment.json', {
    'format': 'wgc-draft-assessment-1', 'task': t['id'], 'role': 'coordinator',
    'actor': 'operator-recovery:20261015-search-01', 'model': None, 'reasoning': None,
    'configuration_evidence': 'Actual builder model/reasoning are not exposed; no Sol/high execution claim.',
    'operator_request': 'Repair packet-only search, assess preserved IG-2B03 drafts, prepare safe continuation and restart IG-2.',
    'assessed_utc': datetime.now(timezone.utc).isoformat(),
    'blocked_event': blocked, 'accepted_dependency': accepted,
    'preserve_manifest': preserve_pin, 'drafts': drafts,
    'results': {'original_manifest_hashes_verified': len(original),
                'blocked_metadata_hashes_verified': len(blocked_body['artifacts']) + 1,
                'accepted_dependency_artifacts_verified': len(accepted_body['artifacts']),
                'final_evidence_artifact_hashes_verified': len(evidence),
                'full_pages': len(final['pages']), 'full_regions': len(final['regions']),
                'assigned_regions': sum(x['page_id'] in assigned_ids for x in final['regions']),
                'unchanged_unassigned_pages': len(old_pages), 'unchanged_unassigned_regions': len(old_regions),
                'preserved_prior_evidence': len(baseline['evidence']),
                'preserved_prior_registry_bindings': len(baseline_registry['entries'])},
    'missing_delivery_outputs': missing,
    'limitations': ['No delivery, independent review or technical acceptance exists for this attempt.',
                   'First replay is partial and second replay is absent; neither is reusable completion evidence.',
                   'Old green checks do not validate recovery. Raw session transcript and derivation helpers are excluded.',
                   'Structural/hash preservation does not establish semantic accuracy, boundary completeness or source coverage.',
                   'No newly generated publisher content was read outside assigned pages; no semantic acceptance granted.'],
    'decision': 'Reuse only exact pinned data as unaccepted candidate drafts; reinspect source and regenerate complete evidence in a fresh attempt.'})
old_scope = w.read_json(ROOT / (old_prep + 'scope.json'))
scope = {'format': 'wgc-continuation-scope-1', 'mode': 'draft_revalidation', 'task': t['id'],
    'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256'], 'blocked_attempt': OLD,
    'attempt': NEW, 'acceptance': t['acceptance'], 'tests': t['tests'],
    'assigned_physical_pages': inputs['assigned_physical_pages'], 'target_ids': t['target_ids'],
    'context_only_ids': t['context_only_ids'], 'input_pins': pin(old_prep + 'input-pins.json'),
    'toolchain': pin(old_prep + 'toolchain.json'), 'accepted_dependency': accepted,
    'preserve_manifest': preserve_pin, 'assessment': assessment, 'drafts': drafts,
    'supersedes': 'Old attempt ownership, old source-inspection assertions and prior completion/check claims. Input/source/tool hashes and original gates remain binding.',
    'content_access': old_scope['content_access'], 'preservation': old_scope['preservation'],
    'required_outputs': old_scope['required_outputs'], 'evidence_policy': old_scope['evidence_policy'],
    'replay': old_scope['replay'], 'review': old_scope['review'],
    'required_commands': [x.replace(OLD.rstrip('/'), NEW.rstrip('/')) for x in old_scope['required_commands']],
    'continuation_steps': [
        'Verify all pins, dependencies, packet and observed runtime; claim new ownership and checkpoint before authoring.',
        'Do not load prior transcripts or old helper scripts. Select only assigned page/region fields from the exact pinned draft JSON files.',
        'Independently inspect original pages 9-12 at sufficient resolution and each proposed region/component. Correct candidate drafts where source inspection warrants; preserved counts are not acceptance targets.',
        'Preserve full 44-page denominator, all accepted nonassigned records and every persisted binding including retired placeholders. Use accepted IG-2B02 as baseline; retain draft-generated IDs where the same identity is still valid.',
        'Regenerate all new task evidence in the fresh attempt. Never copy old evidence paths as fresh task validation. Do not alter any old attempt or accepted bytes.',
        'Run TWO complete independent builds of the authored partition using persisted registry in separate fresh directories. Compare canonical authored bytes/IDs and independently validate path-dependent evidence for each.',
        'Create the complete region/component ledger, continuation and coverage/visual/preservation/replay reports, source/tool pins and full delivery manifest/handoff.',
        'Run unchanged source tests, repository checks, workflow validation and diff check in the pinned process environment; request permitted exact validation execution if Windows temp ACLs require it.',
        'Freeze all new outputs and evidence; transition to review and request fresh independent original-page and complete-ledger review. No semantic acceptance is granted.'],
    'excluded': ['Old transcripts and derivation helpers', 'Generic private/source tree search',
                 'Fresh extraction/rendering outside pages 9-12', 'Mutation of accepted or blocked evidence',
                 'Inherited green checks or inspection claims', 'Automatic semantic acceptance or gameplay legality decisions'],
    'semantic_acceptance_granted': False}
scope_pin = write('scope.json', scope)
checks = [{'command': '.venv/Scripts/python.exe -m pytest tests/test_orchestrator.py tests/test_task_search.py -q -p no:cacheprovider --basetemp private/workflow/checks/search-unit-04 --tb=short', 'exit_code': 0, 'result': '82 passed'}]
common = {'role': 'coordinator', 'actor': 'operator-recovery:20261015-search-01', 'task': t['id'],
          'model': None, 'reasoning': None, 'configuration_evidence': 'Actual builder configuration unavailable; coordinator only, not an executor claim.',
          'criteria': t['acceptance'], 'artifacts': [scope_pin, assessment, preserve_pin], 'checks': checks}
authorization = write('authorization.json', dict(common, summary='Operator-authorized draft revalidation, packet-scoped search and fresh independent review; old blocked attempt stays immutable.'))
ready = write('ready.json', dict(common, summary='Accepted dependency and exact inputs verified; absent continuation output root reserved; original criteria/tests preserved.'))
index_rel = 'docs/work/repair-context/IG-2B03-search-continuation.md'
assert not (ROOT / index_rel).exists()
(ROOT / index_rel).write_text('# IG-2B03 draft continuation\n\nThe operator authorized packet-only search repair and a fresh continuation.\nRead the exact continuation scope and assessment on demand; prior drafts remain unaccepted.\n\n'
    + '\n'.join('- ' + p['path'] + ' SHA256 ' + p['sha256'] for p in [scope_pin, assessment, authorization])
    + '\n\nNo old transcripts, recursive source searches, inherited inspection claims or automatic semantic acceptance.\n', encoding='utf-8')

lock = ROOT / 'private/workflow/queue.lock'
fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    current = w.read_json(ROOT / w.QUEUE)
    ct = next(x for x in current['tasks'] if x['id'] == t['id'])
    assert ct == original_task
    ct['outputs'] = [x.replace(OLD, NEW) for x in ct['outputs']]
    ct['write_scope'] = [NEW, 'private/workflow/packets/', 'private/workflow/checks/']
    ct['context'] = [x for x in ct['context'] if x not in [old_prep + 'scope.json', old_prep + 'source-inspection.json']]
    ct['context'].append(index_rel)
    ct['inputs'][-1] = 'The current continuation scope supersedes old output ownership and inspection assertions. Original input-pins.json still binds accepted baseline/source/tool hashes; author only pages 9-12 in the full 44-page sidecar.'
    ct['start_conditions'][-1] = 'Read continuation_authorization scope and assessment, then original input-pins.json/toolchain on demand. Verify old preservation manifest. Fresh output root must be absent; old transcripts and derivation helpers are excluded.'
    ct['refinement_evidence'] = scope_pin
    ct['continuation_authorization'] = {'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256'],
        'scope': scope_pin, 'evidence': authorization, 'attempt': NEW}
    policy = w.read_json(ROOT / 'docs/work/context-policy.json')
    for rel in [index_rel] + [p['path'] for p in [scope_pin, assessment, preserve_pin, authorization, ready] + drafts]:
        if rel not in policy['allow']:
            policy['allow'].append(rel)
    o.dump(ROOT / 'docs/work/context-policy.json', policy)
    o.continuation_preservation(ROOT, ct, require_absent=True)
    w.transition(current, ROOT, t['id'], 'planned', authorization['path'])
    w.transition(current, ROOT, t['id'], 'ready', ready['path'])
    assert ct['acceptance'] == original_task['acceptance'] and ct['tests'] == original_task['tests']
    o.dump(ROOT / w.QUEUE, current)
    w.render(current, ROOT)
    w.validate(current, ROOT)
finally:
    os.close(fd)
    lock.unlink()
print(json.dumps({'task': t['id'], 'status': 'ready', 'scope': scope_pin,
                  'assessment': assessment, 'preserved_artifacts': len(preserved), 'new_attempt': NEW}, indent=2))
