"""One-task coordinator refinement; no source extraction or queue-history output."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()
RUN = 'private/workflow/runs/IG-2B04/coordinator-f870c628-01'
SESSION = 'private/workflow/orchestrator/20261015T200250Z-56a048a1/001-IG-2B04-coordinator-f870c628'
ATTEMPT = 'private/workflow/runs/IG-2B04/inventory-13-16-f870c628-01'
DOC = 'docs/work/repair-context/IG-2B04-inventory-contract.md'

def load(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()

def pin(p):
    return {'path': p, 'sha256': sha(p), 'bytes': (ROOT / p).stat().st_size}

def create(p, value):
    with (ROOT / p).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')

def evidence(summary, **kwargs):
    return dict(role='coordinator', actor='ig2:001-IG-2B04-coordinator-f870c628:coordinator',
                task='IG-2B04', model='gpt-6.1-sol', reasoning='high',
                configuration_evidence=SESSION + '/runtime-configuration.json',
                configuration_sha256=sha(SESSION + '/runtime-configuration.json'),
                utc=datetime.now(timezone.utc).isoformat(), summary=summary, **kwargs)

packet = load(SESSION + '/packet.json')
task = load(SESSION + '/task.json')
config = load(SESSION + '/runtime-configuration.json')
assert (config['status'], config['model'], config['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
verified = []
for p in packet['files'] + packet['control_files']:
    assert sha(p['path']) == p['sha256'], p['path']
    verified.append(pin(p['path']))
for key in ('scope', 'assessment', 'incident'):
    p = task['context_recovery_authorization'][key]
    assert sha(p['path']) == p['sha256'], p['path']
    verified.append(pin(p['path']))
scope = load(task['context_recovery_authorization']['scope']['path'])
for p in scope['preserved']:
    assert sha(p['path']) == p['sha256'], p['path']
    verified.append(pin(p['path']))

pins = {
 'baseline_inventory': ('private/workflow/runs/IG-2B03/continuation-search-20261015-01/final-verified/inventory.json', '3d032bcb36eb272d142124f662f734d63a89b7755942e25f39b29de678792eb1'),
 'identity_registry': ('private/workflow/runs/IG-2B03/continuation-search-20261015-01/final-verified/identity-registry.json', '0f7beccbd18b71e92f69bdb1e33c8c21242b5cd2f13857ca6094f67fc2d95311'),
 'region_ledger': ('private/workflow/runs/IG-2B03/repair-r01-f684f3e2-01/region-ledger.json', '59f0df0946250b8ea2c4ac5c031cea2940646c8771d4d4e236ee202d63197d4d'),
 'continuations': ('private/workflow/runs/IG-2B03/repair-r01-f684f3e2-01/continuations.json', '52a29f9c28f308563dec1b2a0c0476aa6159fa2accaa2a7782cc3faf36540f39'),
 'coverage_report': ('private/workflow/runs/IG-2B03/continuation-search-20261015-01/coverage-report.json', 'c4d036f036e9c40d5ae4704b0d8154467b2fc2fffccb0bf7b15d0fb72b2a95a5'),
 'source_pins': ('private/workflow/runs/IG-2B03/continuation-search-20261015-01/source-pins.json', 'e7e085036c3a5597a6f0e9eb8de69ba141dbb199121a0ec98b4feee0f4aebdce'),
 'toolchain': ('private/workflow/runs/IG-2B03/continuation-search-20261015-01/toolchain.json', '29dbeff4e46cdfafc6adda7e236170245e15ea0c90cd97bf8c71e372aba7b315'),
 'pdf': ('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf', 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'),
 'provenance': ('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/provenance.json', '90ca669ff57bd499975fbf29353175caff5ee583cb0f4be588f37cf21d57959b'),
}
inputs = {}
for name, (path, expected) in pins.items():
    assert sha(path) == expected, path
    inputs[name] = pin(path)
    verified.append(inputs[name])
done_pin = load(SESSION + '/references.json')['dependencies']['IG-2B03']
assert sha(done_pin['evidence']) == done_pin['sha256']
verified.append(pin(done_pin['evidence']))

spec = importlib.util.spec_from_file_location('wgc_workflow', ROOT / 'scripts/workflow.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
queue_path = 'docs/work/queue.json'
assert sha(queue_path) == packet['queue_sha256']
q = load(queue_path)
before = copy.deepcopy(q)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert {k: v for k, v in t.items() if k != 'events'} == task
assert t['status'] == 'planned' and not t['events']
assert all(next(d for d in q['tasks'] if d['id'] == dep)['status'] == 'done' for dep in t['depends'])
assert not (ROOT / ATTEMPT).exists()
assert not (ROOT / DOC).exists()
policy_path = 'docs/work/context-policy.json'
base = [pin(queue_path), pin(policy_path)]
create(RUN + '/checkpoint.json', evidence('Fresh coordinator checkpoint before contract edits.',
       format='wgc-coordinator-checkpoint-1', input_packet=pin(SESSION + '/packet.json'),
       task_contract=pin(SESSION + '/task.json'), base_files=base, completed_criteria=[],
       next_operation='Refine the selected planned contract; no product-page inspection is claimed.'))

from wgc.sources.inventory import validate
inventory = load(inputs['baseline_inventory']['path'])
assert inventory['registry'] == load(inputs['identity_registry']['path'])
assert {k: len(inventory[k]) for k in ('pages', 'regions', 'evidence', 'links')} == dict(pages=44, regions=439, evidence=407, links=77)
report = validate(inventory, ROOT)
create(RUN + '/baseline-validation.json', report)
assigned_page_ids = {p['id'] for p in inventory['pages'] if p['pdf_page'] in (13, 14, 15, 16)}
targets = [r['id'] for r in inventory['regions'] if r['page_id'] in assigned_page_ids]
assert len(targets) == 4
assert all(r['key'].endswith(':unprocessed-placeholder') for r in inventory['regions'] if r['id'] in targets)

contract = evidence('Exact four-page inventory execution contract; future inspection and independent review remain required.',
 format='wgc-inventory-batch-contract-1', inputs=inputs,
 accepted_dependency={'id': 'IG-2B03', 'status': 'done', 'evidence': pin(done_pin['evidence'])},
 physical_pages=[13, 14, 15, 16], context_only_pages=[], target_ids=targets,
 context_only_ids=[], output_attempt=ATTEMPT,
 boundary={'physical_page': 12, 'observation': 'Ends with a complete visible 5.34 sentence. No page 13 access; chapter continuation beyond the assigned range is unresolved.', 'authority': 'Accepted dependency boundary projection; metadata only.'},
 baseline_counts=dict(pages=44, regions=439, evidence=407, links=77),
 preservation='Retain complete accepted 44-page sidecar, every nonassigned page/region/link/evidence and registry entry/binding. Remove only four assigned placeholders from active membership, retain retired registry entries, replace reading-order positions with authored assigned regions. Preserve nonassigned records byte-equivalently under canonical JSON and preserve old artifact files byte-for-byte.',
 outputs=[ATTEMPT + '/' + s for s in ('final-verified/inventory.json', 'final-verified/identity-registry.json', 'region-ledger.json', 'continuations.json', 'coverage-report.json', 'source-pins.json', 'toolchain.json', 'original-inspection.json', 'preservation-report.json', 'replay-report.json', 'reference-audit.json', 'test-report.json', 'delivery-manifest.json', 'delivery-handoff.md')],
 evidence_requirements=[
  'Render and visually inspect every original physical page 13-16 in a fresh owned original-pages/ directory at 144 DPI before authoring the independent ledger. Pin source PDF/provenance and every generated original PNG, with page, hash and inspection observation. No earlier inspection is inherited.',
  'Independently author every clause, heading, note, example, diagram, table/legend and editorial area from original pages; use exact normalized boxes, explicit reading order and stable explicit keys. Record uncertainty and unresolved references without interpretation or gameplay legality decisions.',
  'Generate fresh region PDF/PNG/text evidence and page-basis hashes for every assigned authored region under evidence/. Verify complete components and boundaries against original-page renders; extracted text alone is insufficient.',
  'Use two complete independently executed regeneration replays under replay-a/ and replay-b/, starting from the same pinned accepted baseline and persisted registry plus the explicit authored region specification; neither replay may copy final/replay output evidence. Rebuild all assigned evidence and validate both full inventories. Compare identities, authored records, evidence bytes/content and page geometry while normalizing only path-dependent locator hashes; record exact differences and independent command exits. Promote a separately validated full inventory to final-verified/.',
  'Carry all nonassigned ledger/continuation records structurally from the current repaired report pins, without dumping unassigned source content. Add assigned observations and exact path/hash/ID references; audit every local and retained reference against its original pin. Never substitute ancestor report paths.',
  'Report full 44-page, task 13-16 and context-only denominators separately at transcription/descriptive/formal levels, all gaps, represented/partial/unprocessed/excluded states and geometric coverage. Context contributes zero; gaps and placeholders never count as represented. Retain nonassigned gaps.',
  'Record continuations within pages 13-16 and unresolved entry/exit boundaries using only assigned pages and the page12 metadata observation. Page17 and other cross-reference targets are inaccessible; preserve unresolved locators and request a fresh scope if inspection is necessary.',
  'Freeze the complete actual file list with SHA-256 and bytes, including original-page renders, all assigned evidence, both complete replays, final inventory/companion registry and every root report. Fresh independent reviewer must inspect all assigned original pages, every region/component and both boundaries, verify preservation/reference audit/replays and all criteria/tests against frozen hashes before technical acceptance. No source meaning/human acceptance is granted by this contract.'
 ],
 required_commands=[
  '.venv/Scripts/python.exe -m wgc.sources validate ' + ATTEMPT + '/final-verified/inventory.json',
  '.venv/Scripts/python.exe -m wgc.sources validate ' + ATTEMPT + '/replay-a/inventory.json',
  '.venv/Scripts/python.exe -m wgc.sources validate ' + ATTEMPT + '/replay-b/inventory.json',
  '.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp <fresh-owned-short-path> -p no:cacheprovider --tb=short',
  'scripts/check.ps1 -Task IG-2B04', 'git diff --check'],
 toolchain_policy='Inherit both pinned process_pythonpath entries and process_path_prefix unchanged. Record actual interpreter, package and executable versions/hashes, 144 DPI and extraction settings. No install or global configuration.',
 original_acceptance=task['acceptance'], original_tests=task['tests'], semantic_acceptance_required=task['semantic_acceptance_required'])
create(RUN + '/execution-contract.json', contract)
create(RUN + '/input-verification.json', evidence('All selected packet, recovery preservation and accepted input byte pins verified locally; baseline validates structurally.',
       format='wgc-input-verification-1', verified=verified, artifacts=[pin(RUN + '/baseline-validation.json')],
       baseline_counts=contract['baseline_counts'], source_pages_inspected=[], checks=[{'command': 'wgc.sources.inventory.validate(accepted_baseline, repository_root)', 'exit_code': 0}]))

doc = '''# IG-2B04 exact inventory contract

This task inventories original physical pages 13-16 only. No source inspection,
coverage, acceptance or completed execution is inherited from preparation.

The exact input pins, assigned placeholder IDs, preservation rules, evidence and
replay requirements, output paths and required checks are frozen in:
`private/workflow/runs/IG-2B04/coordinator-f870c628-01/execution-contract.json`.
Its SHA-256 is CONTRACT_HASH.

Use the accepted IG-2B03 inventory/registry and its current repaired ledger and
continuations, all pinned there. The full 44-page sidecar remains complete. Preserve
all nonassigned records and evidence; retire only the four placeholder memberships
without deleting registry entries. Do not use the obsolete pages-13-16.json output
or the old spqr-5e source path. Only the official revision pinned in the contract is
an input. No old transcripts, derivation helpers or source trees may be searched.

The exclusively owned product attempt is
`private/workflow/runs/IG-2B04/inventory-13-16-f870c628-01/`; it must be absent at claim.
Final output is `final-verified/inventory.json` and companion
`final-verified/identity-registry.json`. Keep root region-ledger.json,
continuations.json, coverage-report.json, source-pins.json and toolchain.json.
Freeze every actual derived artifact and the original/replay/preservation/reference
reports in the complete delivery manifest. Lifecycle evidence uses fresh task-owned
attempts; all older attempts and accepted dependency bytes remain immutable.

Inspect all four original pages and every authored region/component. Produce fresh
path-dependent evidence, two complete independent replays and separate full/task/context
denominators. Fresh independent review repeats the original-page and region comparison
against exact frozen files. Technical checks never grant human semantic acceptance.

Only the accepted page12 exit observation is available outside pages13-16. Page17,
adjacent-page text/images and cross-chapter targets are outside scope. Record unresolved
boundaries without resolving gameplay meaning; request a new scope/session if needed.
Context requests remain sequential and helper refusal ends the session without fallback.
Use the pinned installed process toolchain, preserving BOTH Python path entries and
Poppler prefix. Run tests unchanged and follow the authorized exact-command approval
path for Windows temporary-directory or synthetic-tree termination permission failures.
'''.replace('CONTRACT_HASH', sha(RUN + '/execution-contract.json'))
with (ROOT / DOC).open('x', encoding='utf-8', newline='\n') as f:
    f.write(doc)
policy = load(policy_path)
for path in [DOC] + task['tool_context']:
    if not any(path == a or (a.endswith('/') and path.startswith(a)) for a in policy['allow']):
        policy['allow'].append(path)
(ROOT / policy_path).write_text(json.dumps(policy, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
t['title'] = 'Inventory SPQR PDF physical pages 13-16'
t['outputs'] = contract['outputs']
t['write_scope'] = [ATTEMPT + '/', 'private/workflow/runs/IG-2B04/', 'private/workflow/checks/', 'private/workflow/packets/']
t['inputs'] = [f"{name}: {p['path']} SHA256 {p['sha256']}" for name, p in inputs.items()] + ['Accepted IG-2B03 page12 exit observation only; no adjacent page access.', f"Exact execution contract: {RUN}/execution-contract.json SHA256 {sha(RUN + '/execution-contract.json')}"]
t['context'] = [p for p in task['context'] if p != 'private/ig/sources/spqr-5e/provenance.json'] + [DOC]
t['inventory_contract'] = pin(RUN + '/execution-contract.json')
t['target_ids'] = targets
t['context_only_ids'] = []
t['acceptance'] += [
 'Preserve the complete pinned 44-page inventory, every nonassigned record/link/evidence and all persisted registry bindings; replace only assigned placeholders and retain retired registry entries.',
 'Freeze fresh original-page inspection and every assigned region evidence artifact, two complete independent replays, full/task/context denominators, preservation and reference audits, and independent review of the frozen complete delivery.',
 'Use the exact execution-contract input pins and output layout, including the current repaired ledger/continuations and final-verified inventory plus companion registry; retain unresolved boundaries outside the authorized pages.'
]
t['tests'] += [
 'Validate final-verified and both independently regenerated replay inventories against the actual PDF, full persisted registry and fresh assigned evidence bytes; compare stable identities, revisions and normalized path-dependent evidence results.',
 'Assert full 44-page retention, nonassigned canonical record equality, unchanged original input/artifact hashes and registry-entry retention; assert only four assigned placeholder memberships retire.',
 'Audit every ledger/continuation/evidence locator, page basis, source hash and current report pin; independently compare every original assigned page/component and entry/exit boundary.',
 'Run the explicit unchanged tests/sources suite with a fresh basetemp and -p no:cacheprovider, scripts/check.ps1 -Task IG-2B04 and git diff --check; retain commands, logs and exits.'
]
t['start_conditions'] += ['The frozen inventory_contract is hash-verified, the exact product attempt is absent, and the installed toolchain/context is available. Claim requires fresh observed Sol/high evidence; preparation grants no inspection or acceptance.']
t['handoff'] += ['Complete artifact manifest includes every original-page render, fresh region PDF/PNG/text, both full replay trees, final inventory/registry and all root reports; request a fresh independent reviewer with original pages13-16 access.']
assert t['acceptance'][:len(task['acceptance'])] == task['acceptance']
assert t['tests'][:len(task['tests'])] == task['tests']
assert all(old == next(x for x in q['tasks'] if x['id'] == old['id']) for old in before['tasks'] if old['id'] != t['id'])
w.validate(q, ROOT, check_views=False)
assert sha(queue_path) == packet['queue_sha256']
(ROOT / queue_path).write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for rel, body in w.views(q).items():
    p = ROOT / rel
    if not p.exists() or p.read_text(encoding='utf-8') != body:
        p.write_text(body, encoding='utf-8')
w.validate(q, ROOT)
create(RUN + '/refinement.json', evidence('Selected planned contract refined; all original acceptance/tests preserved verbatim and no other task changed.',
       format='wgc-refinement-1', criteria=t['acceptance'], artifacts=[pin(RUN + '/execution-contract.json'), pin(RUN + '/input-verification.json'), pin(DOC)],
       queue_before=packet['queue_sha256'], queue_after=sha(queue_path), product_attempt_absent=True,
       checks=[{'command': 'workflow.validate(refined_queue, repository_root)', 'exit_code': 0}],
       completed=['Exact accepted input pins', 'Bounded page scope', 'Full baseline/registry preservation contract', 'Fresh evidence/replay/review obligations', 'Disjoint future product path', 'Exact tooling context'],
       source_pages_inspected=[], product_deliverables_created=False))
print(json.dumps({'task': 'IG-2B04', 'status': 'planned', 'verified_pin_count': len(verified), 'assigned_placeholder_count': len(targets), 'contract': pin(RUN + '/execution-contract.json'), 'baseline_validation': 'passed', 'other_tasks_unchanged': True}))
