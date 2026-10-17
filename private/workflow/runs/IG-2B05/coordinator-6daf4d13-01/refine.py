"""Refine only the selected task, retaining existing queue bytes semantically."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()
RUN = Path('private/workflow/runs/IG-2B05/coordinator-6daf4d13-01')
SESSION = Path('private/workflow/orchestrator/20261016T150146Z-33452c9a/001-IG-2B05-coordinator-6daf4d13')
OUT = 'private/workflow/runs/IG-2B05/inventory-17-20-01'
ACTOR = 'ig2:001-IG-2B05-coordinator-6daf4d13:coordinator'

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def pin(p):
    p = Path(p)
    return {'path': p.as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}

def write(p, obj):
    with Path(p).open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write('\n')

assert not Path(OUT).exists(), 'Executor attempt must be absent'
config = load(SESSION / 'runtime-configuration.json')
assert (config['status'], config['model'], config['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
binding = {'actor': ACTOR, 'model': config['model'], 'reasoning': config['reasoning'],
           'configuration_evidence': (SESSION / 'runtime-configuration.json').as_posix(),
           'configuration_sha256': sha(SESSION / 'runtime-configuration.json')}
inputs = load(RUN / 'dependency-inputs.json')
inv = inputs['inventory']
for p in [inv['baseline_inventory'], inv['identity_registry'], inv['source']['pdf'],
          inv['source']['provenance'], *inv['reports'].values()]:
    assert sha(p['path']) == p['sha256']
observations = {
    17: 'Two columns; clauses, heading, exceptions, withdrawal example, shaded design/play notes, stacking bullets, footer/header and a stacking example continuing onto page 18.',
    18: 'Two columns; incoming stacking examples and shaded note, clauses and bullets, column-movement heading and note, marker artwork, exception, and a clause continuing onto page 19.',
    19: 'Two columns; incoming column-movement clause, movement diagram with caption, remaining clauses; pre-arranged-withdrawal heading, marker artwork, clauses, bullets and two play notes.',
    20: 'Two columns; facing and ZOC headings, clauses, bullet lists, facing diagrams and ZOC illustration, shaded notes and exceptions; final passage introduces following conditions beyond this page.'
}
inspection = {'format': 'wgc-coordinator-page-navigation-1', 'task': 'IG-2B05', **binding,
              'source': inv['source']['pdf'], 'physical_pages': [17, 18, 19, 20],
              'command': 'pdftoppm -f 17 -l 20 -r 100 -png <pinned-pdf> <owned-run>/page',
              'exit_code': 0, 'pages': [{'physical_page': n,
                  'image': pin(RUN / f'page-{n}.png'), 'observation': observations[n]} for n in observations],
              'scope': 'Coordinator navigation only. No region inventory, completeness, transcription acceptance, semantic acceptance or gameplay legality decision. Executor and independent reviewer must inspect all original assigned pages freshly.'}
write(RUN / 'page-navigation.json', inspection)
original = load(SESSION / 'task.json')
new_acceptance = [
    'Use the exact accepted IG-2B04 baseline and companion registry in the pinned dependency-inputs.json; retain the complete 44-page sidecar. Copy every nonassigned page, region, evidence record and link unchanged. Replace only the four assigned unprocessed placeholder memberships on physical pages 17-20, retaining all old registry entries and identity bindings.',
    'Freshly inspect the pinned original PDF physical pages 17, 18, 19 and 20 in full, including every visible component, column, heading, clause, exception, note, example, diagram, marker, bullet, caption, header/footer and editorial area. Document uncertainty and proposed boundaries; extraction or inherited coordinator observations cannot substitute for original-page inspection.',
    'Provide explicit disjoint regions and reading order, component/region reconciliation, precise evidence locators and source references. Keep structural inventory, transcription, descriptive semantics, formal semantics, exclusions and executable readiness separate. Never treat an unprocessed placeholder, geometric gap, unknown meaning or excluded region as represented.',
    'Create fresh path-dependent cropped PDF, PNG and UTF-8 text evidence for every new assigned region at 144 DPI, with exact hashes, bytes, geometry and page_basis_hash. Revalidate all retained evidence without rewriting its bytes. Keep label verification separate from merely finding a printed glyph.',
    'Write final-verified/inventory.json and final-verified/identity-registry.json under the new owned attempt, with region-ledger.json, continuations.json, coverage-report.json, source-pins.json and toolchain.json at its root. All reports must pin the final inventory revision/hash and registry, source, assigned IDs and evidence; source-reference indexes must resolve against these exact current reports.',
    'Provide two complete independent fresh derivation replays from the same authored partition and persisted registry in disjoint replay-1/ and replay-2/ outputs. Compare the complete logical sidecar, registry identities, all assigned crop PDF/PNG/text bytes and locators, with explicit normalization only for actual path-dependent fields; record complete set equality, counts and hashes, not sampled comparisons.',
    'Report full 44-page inventory counts/denominators, assigned-page task counts/denominators and context-only counts/denominators separately. Preserve unresolved nonassigned placeholders explicitly; context-only observations contribute zero assigned inventory denominator.',
    'Trace incoming, internal and outgoing continuation boundaries, including pages 17-18, 18-19 and page 20 exit. Accepted page-16 exit is context only. Adjacent physical page 16 or 21 may be inspected only for a named continuation boundary; record exact inspected boxes/IDs and purpose before access, keep evidence in context-only outputs and do not inventory or claim coverage of unassigned content. Other referenced source targets remain unresolved.',
    'Freeze every delivered product, helper, evidence artifact, report and check log with SHA-256. Obtain fresh independent technical/source-page review by a different actor against every assigned original page, proposed boundaries/components, the complete region ledger, preservation report and both complete replays. Green tooling and model review grant no human semantic acceptance or gameplay readiness.'
]
new_tests = [
    '.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp private/workflow/runs/IG-2B05/inventory-17-20-01/tests-sources -p no:cacheprovider --tb=short',
    '.venv/Scripts/python.exe -m wgc.sources validate private/workflow/runs/IG-2B05/inventory-17-20-01/final-verified/inventory.json',
    'Run fresh .venv/Scripts/python.exe -m wgc.sources validate on both complete replay inventories with the inherited pinned process_pythonpath and process_path_prefix; never replace PYTHONPATH with repo/src alone.',
    'Run an explicit preservation check: all 44 source pages remain; nonassigned records, links, evidence, registry bindings and original registry entries equal the accepted baseline; exactly the four pinned placeholder memberships are retired; no nonassigned record is reauthored or silently dropped.',
    'Run complete set/replay checks: all newly assigned region IDs have fresh current evidence and a ledger entry, all visible components have dispositions, independent replay region/evidence sets equal final assigned sets, and all current report/source-reference paths and hashes resolve.',
    'Review all assigned original pages and every region crop visually; audit reading order, column transitions, notes/examples/diagram components and uncertainty; inspect named adjacent continuation boxes only, and verify context-only records never inflate task/full represented counts.',
    'Run scripts/check.ps1 -Task IG-2B05 and git diff --check unchanged. For the specific Windows restricted-token pytest temporary-directory or owned context-guard termination denial, request approved execution of the exact unchanged command; do not alter assertions, ACLs or libraries.'
]
outputs = [f'{OUT}/{p}' for p in ['final-verified/inventory.json', 'final-verified/identity-registry.json',
    'region-ledger.json', 'continuations.json', 'coverage-report.json', 'source-pins.json', 'toolchain.json',
    'original-page-inspection.json', 'preservation-report.json', 'replay-report.json', 'validation-report.json',
    'delivery-handoff.md']]
context = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md',
           'contracts/ig/regions.schema.json', 'src/wgc/sources/README.md',
           (RUN / 'dependency-inputs.json').as_posix(), (RUN / 'page-navigation.json').as_posix(),
           inv['source']['pdf']['path'], inv['source']['provenance']['path'],
           inv['reports']['toolchain.json']['path']]
contract = copy.deepcopy(original)
contract.update(outputs=outputs, write_scope=[OUT + '/'], context=context,
    inputs=[f"Accepted IG-2B04 full baseline: {inv['baseline_inventory']['path']} SHA-256 {inv['baseline_inventory']['sha256']}",
            f"Accepted companion registry: {inv['identity_registry']['path']} SHA-256 {inv['identity_registry']['sha256']}",
            f"Official SPQR 5E PDF: {inv['source']['pdf']['path']} SHA-256 {inv['source']['pdf']['sha256']}; physical pages 17-20 are the only assigned inventory pages.",
            f"Official provenance: {inv['source']['provenance']['path']} SHA-256 {inv['source']['provenance']['sha256']}",
            'IG-2A locator contract as implemented by the pinned current regions schema and wgc.sources toolchain; current accepted reports, assigned page/placeholder IDs, revisions and process-local dependency settings are in dependency-inputs.json.',
            'IG-2B04 accepted page-16 exit observation is boundary context only, not inspection of page 17. Coordinator page navigation is candidate navigation only and grants no executor inspection or completion claim.'],
    acceptance=original['acceptance'] + new_acceptance, tests=original['tests'] + new_tests,
    assigned_physical_pages=[17,18,19,20], target_ids=[r['id'] for r in inv['assigned_region_metadata']],
    context_only_ids=[],
    inventory_batch={'format':'wgc-inventory-batch-contract-1', 'dependency':'IG-2B04',
       'input_reference': pin(RUN / 'dependency-inputs.json'), 'source': inv['source'],
       'assigned_pages': inv['assigned_page_metadata'], 'replace_placeholders':inv['assigned_region_metadata'],
       'owned_attempt': OUT, 'context_only_physical_pages':[16,21],
       'context_only_access':'Named continuation boxes only; record purpose and exact region before inspection. No full adjacent-page analysis.',
       'independent_replay_outputs':[OUT+'/replay-1/',OUT+'/replay-2/'],
       'required_review':'Fresh independent full assigned-page, component/boundary, preservation and replay audit. Human semantic gates unchanged.'})
contract['start_conditions'] += [
    'The new owned inventory-17-20-01 directory must be absent before claim. Record a fresh checkpoint and observed confirmed gpt-6.1-sol/high session evidence before product writes. Reverify every pinned input and preserve all preexisting work.',
    'Use only the task-bound dependency projection and search/access helpers; no old transcripts, closure envelopes, whole dependency manifests, unassigned source analysis, global searches or source APIs.',
    'All contracts, exact assigned original pages, accepted baseline/registry/current reports and installed toolchain must be available and hash-verified. Any mismatch or missing bounded context blocks execution pending a new coordinator session.'
]
write(RUN/'refined-contract.json', contract)
lock = Path('private/workflow/queue.lock')
fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    before = sha('docs/work/queue.json')
    preflight = load(RUN/'preflight.json')
    baseline = next(p for p in preflight['preexisting_owned_paths'] if p['path']=='docs/work/queue.json')
    assert before == baseline['sha256'], 'Queue changed after preflight'
    q = load('docs/work/queue.json')
    saved = copy.deepcopy(q)
    t = next(t for t in q['tasks'] if t['id']=='IG-2B05')
    assert all(t[k] == v for k,v in original.items()), 'Task contract changed since dispatch'
    assert t['status']=='planned'
    t.update(contract)
    policy_path = Path('docs/work/context-policy.json')
    policy = load(policy_path)
    for p in context:
        if not any(p == a or (a.endswith('/') and p.startswith(a)) for a in policy['allow']):
            policy['allow'].append(p)
    write(RUN/'context-policy-before.json', load(policy_path))
    policy_path.write_text(json.dumps(policy, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
    spec = importlib.util.spec_from_file_location('wgc_workflow', ROOT/'scripts/workflow.py')
    w = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(w)
    w.validate(q, ROOT, check_views=False)
    assert all(a == b for a,b in zip(saved['tasks'],q['tasks']) if a['id']!='IG-2B05')
    for key in ['acceptance','tests']:
        assert t[key][:len(original[key])] == original[key]
    assert t['semantic_acceptance_required'] == original['semantic_acceptance_required']
    assert sha('docs/work/queue.json') == before
    write('docs/work/queue.pending.json',q)
    os.replace('docs/work/queue.pending.json','docs/work/queue.json')
    w.render(q, ROOT)
    write(RUN/'refinement-report.json', {'task':'IG-2B05','role':'coordinator',**binding,
        'original_task': pin(SESSION/'task.json'), 'refined_contract':pin(RUN/'refined-contract.json'),
        'queue_before_sha256':before,'queue_after_sha256':sha('docs/work/queue.json'),
        'other_task_records_unchanged':True,'original_acceptance_and_tests_preserved_verbatim':True,
        'human_gate_unchanged':True,'product_deliverables_created':False,
        'status':'planned','executor_attempt_absent':not Path(OUT).exists(),
        'pinned_dependency_inputs':pin(RUN/'dependency-inputs.json')})
finally:
    os.close(fd)
    lock.unlink()
print(json.dumps({'task':'IG-2B05','status':'planned','refined_contract_sha256':sha(RUN/'refined-contract.json'),
                  'other_task_records_unchanged':True,'executor_attempt_absent':not Path(OUT).exists()}))
