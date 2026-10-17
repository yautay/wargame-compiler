"""Preserve the stopped writer and authorize a fresh source-inspection attempt."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B04/rg-recovery-20261016-01/'
OLD = 'private/workflow/runs/IG-2B04/continuation-13-16-recovery03/'
NEW = 'private/workflow/runs/IG-2B04/continuation-13-16-rg04/'
SESSION = 'private/workflow/orchestrator/20261016T111418Z-76d89b82/001-IG-2B04-executor-ecf458a5/'
DOC = 'docs/work/repair-context/IG-2B04-rg-recovery04.md'
def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}
def write(rel, body):
    assert not (ROOT / rel).exists(), 'Never overwrite recovery evidence: ' + rel
    o.dump(ROOT / rel, body)
    return pin(rel)
def copy_pin(source, destination):
    assert not (ROOT / destination).exists()
    shutil.copyfile(ROOT / source, ROOT / destination)
    result = pin(destination)
    assert result['sha256'] == pin(source)['sha256']
    return result

q = w.read_json(ROOT / w.QUEUE)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert t['status'] == 'in_progress' and not (ROOT / NEW).exists()
assert not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
before = copy.deepcopy(q)
write(PREP + 'queue-before.json', q)
protected = o.continuation_preservation(ROOT, t)
old_scope = w.read_json(ROOT / t['continuation_authorization']['scope']['path'])
checkpoint = w.read_json(ROOT / OLD / 'checkpoint.json')
o.verify_artifacts(ROOT, {'artifacts': checkpoint['base_files']})
assert pin(OLD + 'claim.json')['sha256'] == t['events'][-1]['sha256']
assert not checkpoint['completed_criteria'] and not checkpoint['changed_files']
common = {'role': 'coordinator', 'actor': 'operator-authorized-rg-recovery-20261016-01',
          'task': t['id'], 'model': None, 'reasoning': None,
          'configuration_evidence': 'Builder actual configuration unavailable; no Sol/high claim.',
          'utc': o.utc(), 'criteria': t['acceptance'],
          'operator_request': 'Fix missing rg, add a test, restart IG-2 and verify B04 actually starts page inspection.'}
incident = copy_pin(SESSION + 'context-denied.json', PREP + 'incident.json')
rg = o.task_search.ripgrep_binding()
version = subprocess.run([rg['path'], '--version'], capture_output=True, text=True, timeout=5, check=True).stdout.splitlines()[0]
assessment = write(PREP + 'assessment.json', {**common,
    'summary': 'The independent Windows host did not have rg in PATH. No page rendering/inspection occurred after the prior claim. Approved process inspection confirmed all prior owned processes stopped.',
    'incident': incident, 'prior_claim': pin(OLD + 'claim.json'), 'prior_checkpoint': pin(OLD + 'checkpoint.json'),
    'rg': {**rg, 'version': version}, 'base_inputs_verified': len(checkpoint['base_files']),
    'original_preserved_pins_verified': len(protected),
    'recovery': 'Pass absolute installed executable and SHA256 through the independent host, preflight before any model, preserve every prior byte and give a fresh executor a separate absent output root.',
    'source_inspection_inherited': False, 'semantic_acceptance_granted': False})
# These are exact candidate-data copies made by recovery, never prior inspection claims.
drafts = []
draft_provenance = []
for source in old_scope['drafts']:
    destination = OLD + 'recovery-candidate-' + Path(source['path']).name
    copied = copy_pin(source['path'], destination)
    drafts.append(copied)
    draft_provenance.append({'original': source, 'copy': copied})
own_files = [pin(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT / OLD).rglob('*')) if p.is_file()]
originals = protected + own_files
manifest = write(OLD + 'blocked-state-manifest.json', {**common, 'artifacts': originals,
    'summary': 'All earlier protected evidence plus the stopped claim/checkpoint and exact recovery candidate copies; none are accepted product delivery.',
    'recovery_candidate_provenance': draft_provenance})
blocked = write(OLD + 'blocked.json', {**common,
    'summary': 'Executor stopped on missing rg before page inspection. Preserve the claim, checkpoint and all earlier evidence; explicit fresh recovery required.',
    'artifacts': [manifest, assessment, pin(OLD + 'claim.json'), pin(OLD + 'checkpoint.json')]})
w.transition(q, ROOT, t['id'], 'blocked', blocked['path'])
preserved = originals + [manifest, assessment, blocked, {'path': blocked['path'], 'sha256': blocked['sha256']}]
preserve = write(PREP + 'preserve.json', {**common, 'artifacts': preserved,
    'summary': 'Exact original manifest prefix and all latest blocked-event evidence.'})
scope = write(PREP + 'scope.json', {**common, 'mode': 'draft_revalidation',
    'blocked_attempt': OLD, 'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256'],
    'attempt': NEW, 'acceptance': t['acceptance'], 'tests': t['tests'], 'assessment': assessment,
    'preserve_manifest': preserve, 'drafts': drafts, 'draft_provenance': draft_provenance,
    'physical_pages': [13, 14, 15, 16],
    'required': ['Fresh original-page renders and visual inspection of all assigned pages/components.',
                 'Candidate copies contain data only; inherit no old inspection, script, transcript or passing checks.',
                 'Fresh assigned evidence, two complete independent replays and all exact original tests/reports.',
                 'Full44-page baseline and registry preservation; unchanged acceptance and independent review gates.',
                 'Use supervisor-bound absolute ripgrep; no PATH reset, installation, guard bypass or source scope expansion.']})
def relocate(value):
    if isinstance(value, str): return value.replace(OLD, NEW)
    if isinstance(value, list): return [relocate(v) for v in value]
    if isinstance(value, dict): return {k: relocate(v) for k, v in value.items()}
    return value
old_contract = t['inventory_contract']
o.verify_artifacts(ROOT, {'artifacts': [old_contract]})
contract = relocate(w.read_json(ROOT / old_contract['path']))
contract.update(common)
contract.pop('configuration_sha256', None)
contract.update(summary='Exact inventory contract retained with fresh rg04 output ownership and no inherited inspection.',
                recovery_scope=scope, previous_contract=old_contract)
contract_pin = write(PREP + 'execution-contract.json', contract)
authorization = write(PREP + 'authorization.json', {**common,
    'summary': 'Operator-authorized fresh rg04 continuation after stopped-writer and input-hash triage. No source or semantic acceptance.',
    'artifacts': [scope, preserve, assessment, incident, contract_pin]})
t['continuation_authorization'] = {'scope': scope, 'evidence': authorization, 'attempt': NEW,
    'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256']}
t['context_recovery_authorization'] = {'incident': incident, 'scope': scope, 'assessment': assessment}
t['inventory_contract'] = contract_pin
t['outputs'] = relocate(t['outputs'])
t['write_scope'] = [NEW, 'private/workflow/runs/IG-2B04/', 'private/workflow/checks/', 'private/workflow/packets/']
t['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md',
                'docs/work/repair-context/IG-2B04-context-access-02.md', DOC]
t['inputs'] = [v for v in t['inputs'] if not v.startswith(('Exact recovery contract:', 'Exact execution contract:'))]
t['inputs'].append('Exact recovery contract: ' + contract_pin['path'] + ' SHA256 ' + contract_pin['sha256'])
t['start_conditions'] = [v for v in t['start_conditions'] if not v.startswith('Recovery03 supersedes')]
t['start_conditions'].append('RG recovery04 supersedes previous output ownership. Fresh absent root, exact preserved inputs and observed Sol/high are required before claim; no old page inspection is inherited.')
doc = f'''# IG-2B04 rg recovery04

The operator authorized this fresh session after missing ripgrep stopped the prior
executor. The exact contract is `{contract_pin['path']}` SHA256
`{contract_pin['sha256']}`. Read the exact continuation scope and assessment references.
Only original physical pages13-16 are assigned; page12 exit metadata is the only
adjacent context. Page17 and cross-chapter targets remain inaccessible.

The new exclusively owned output root is `{NEW}` and must be absent before claim.
The previous claim/checkpoint and all earlier evidence remain immutable. The three
named draft JSON files were byte-copied by recovery from earlier candidate data;
they grant no inspection, correctness, completion or acceptance. Reinspect every
original assigned page and every proposed component, generate fresh path-dependent
evidence, two complete independent replays and every required report. Carry the
full44-page baseline, nonassigned records and persisted registry structurally.
All original criteria/tests and independent review remain binding. Human semantic
acceptance remains separate; never decide gameplay legality with an LLM.

Ripgrep is supervisor-bound by WGC_RIPGREP_PATH and WGC_RIPGREP_SHA256, recorded in
the session tool-runtime.json. Use the supported scoped search helper; do not reset
these variables, use raw searches or fall back after any helper refusal. Python and
Poppler still use both pinned Python path entries and the installed native prefix.
Run unchanged required checks with approved permissions for known Windows temp or
process-tree restrictions. No installation, ACL or global configuration change.

Write a new inspection progress checkpoint once original-page rendering and visual
inspection begin, with exact page-image paths/hashes and actual completed operations.
Rendering alone does not establish visual inspection or source acceptance.
'''
assert not (ROOT / DOC).exists()
(ROOT / DOC).write_text(doc, encoding='utf-8')
w.transition(q, ROOT, t['id'], 'planned', authorization['path'])
w.transition(q, ROOT, t['id'], 'ready', authorization['path'])
assert t['acceptance'] == next(x for x in before['tasks'] if x['id'] == t['id'])['acceptance']
assert [x for x in q['tasks'] if x['id'] != t['id']] == [x for x in before['tasks'] if x['id'] != t['id']]
o.continuation_preservation(ROOT, t, require_absent=True)
q['updated'] = '2026-10-16'
o.dump(ROOT / w.QUEUE, q)
w.render(q, ROOT)
w.validate(q, ROOT)
print(json.dumps({'task': t['id'], 'status': t['status'], 'preserved_pins': len(preserved),
                  'new_attempt': NEW, 'rg': rg, 'source_inspection_inherited': False}))
