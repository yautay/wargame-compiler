"""Bounded coordinator refinement. Never print queue records or source text."""
import copy
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path.cwd()
RUN = Path('private/workflow/runs/IG-2B06/refinement-1bcd2b72-01')
SESSION = Path('private/workflow/orchestrator/20261016T164231Z-37ee310d/001-IG-2B06-coordinator-1bcd2b72')
OUTPUT = 'private/workflow/runs/IG-2B06/inventory-21-24-01'
BASE = Path('private/workflow/runs/IG-2B05/continuation-17-20-dependency03')
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w


def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def pin(p):
    p = Path(p)
    return {'path': p.as_posix(), 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def dump(p, value):
    with Path(p).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


initial = load(RUN / 'checkpoint-initial.json')
identity = {k: initial[k] for k in ('role', 'actor', 'model', 'reasoning', 'configuration_evidence', 'configuration_sha256')}
assert w.digest(identity['configuration_evidence']) == identity['configuration_sha256']
assert not Path(OUTPUT).exists(), 'Future executor must own a fresh absent directory'
pins = initial['verified_inputs']
for p in pins:
    assert w.digest(p['path']) == p['sha256']
by_name = {Path(p['path']).name: p for p in pins}
baseline = load(by_name['inventory.json']['path'])
pages = [p for p in baseline['pages'] if p['pdf_page'] in [21, 22, 23, 24]]
page_ids = {p['id'] for p in pages}
regions = [r for r in baseline['regions'] if r['page_id'] in page_ids]
assert len(pages) == len(regions) == 4
assert all(r['kind'] == 'unclassified' and r['key'].endswith(':unprocessed-placeholder') for r in regions)
targets = [{k: r[k] for k in ('id', 'key', 'revision', 'page_id', 'box', 'denominator_role')} for r in regions]
summary_toolchain = {
    **identity,
    'format': 'wgc-coordinator-toolchain-pin-1',
    'task': 'IG-2B06',
    'accepted_toolchain': by_name['toolchain.json'],
    'process_pythonpath': r'C:\repo\wargame-compiler\src;C:\Users\yauta\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages',
    'process_path_prefix': r'C:\Users\yauta\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell',
    'libraries': {'pypdf': '6.10.0', 'pdfplumber': '0.11.9', 'Pillow': '12.3.0', 'pytest': '9.1.1', 'reportlab': '4.4.9'},
    'python_executable': by_name['python.exe'],
    'purpose': 'Small hash-bound projection for inherited process settings; the accepted full report remains immutable.'
}
dump(RUN / 'toolchain.json', summary_toolchain)
inspection = {
    **identity, 'format': 'wgc-coordinator-source-scope-observation-1', 'task': 'IG-2B06',
    'source': by_name['rulebook.pdf'], 'provenance': by_name['provenance.json'],
    'purpose': 'Original-page visual observations for refinement only. Executor and independent reviewer must inspect afresh.',
    'assigned_physical_pages': [21, 22, 23, 24],
    'observations': [
        {'pdf_page': 21, 'observed_components': ['Incoming bullet continuation of 7.24', '7.25 and 7.3 with exceptions, examples and two marker illustrations', '8.0/8.1 headings, notes, four sample counters and 8.11', 'Header, printed label, footer and whitespace']},
        {'pdf_page': 22, 'observed_components': ['8.12-8.17, bullet exceptions and notes', 'Front/flank hex diagram with arrows, embedded counter and labels', '8.15 across-column continuation', 'Two missile-supply marker illustrations', 'Header, printed label, footer and whitespace']},
        {'pdf_page': 23, 'observed_components': ['Two large note blocks associated with preceding missile-supply material', '8.18-8.19', '8.2 and 8.21-8.25 with exception paragraphs', '8.3 heading, note and 8.31 with exceptions', 'Header, printed label, footer and whitespace']},
        {'pdf_page': 24, 'observed_components': ['8.32-8.34 with ordered bullets and design note', 'Large hex/counter/arrow diagram with labels A-D and W-Z', 'Example caption continued at top of right column', '8.4 heading, notes, PROCEDURE and red IMPORTANT box', 'Header, printed label, footer and whitespace']}
    ],
    'context_only_observations': [
        {'pdf_page': 20, 'box': [500000, 730000, 940000, 930000], 'purpose': 'Incoming 7.24 lead-in at the lower right; preserve accepted baseline records.'},
        {'pdf_page': 25, 'box': [60000, 60000, 940000, 410000], 'purpose': 'Outgoing 8.4 procedure/sequence continuation at the upper page; do not inventory page 25.'}
    ],
    'render_dpi': 120,
    'renders': [pin(RUN / 'inspection' / f'page-{p}.png') for p in [21,22,23,24]] + [pin(RUN / 'inspection/context-bottom-20.png'), pin(RUN / 'inspection/context-top-25.png')],
    'limitations': ['No region denominator authored, no source meaning approved, no gameplay legality decided.', 'Adjacent render crops were used only to establish the narrow continuation locators above.']
}
dump(RUN / 'source-scope-observation.json', inspection)
required_files = ['final-verified/inventory.json', 'final-verified/identity-registry.json', 'region-ledger.json', 'continuations.json', 'coverage-report.json', 'source-pins.json', 'toolchain.json', 'original-page-inspection.json', 'preservation-report.json', 'replay-report.json', 'validation-report.json', 'delivery-handoff.md']
contract = {
    **identity, 'format': 'wgc-inventory-batch-refinement-1', 'task': 'IG-2B06',
    'summary': 'Replace only the physical-page 21-24 placeholders in the latest accepted full 44-page inventory; preserve the remaining corpus and registry.',
    'dependency': {'id': 'IG-2B05', 'status': 'done', 'done': load(SESSION / 'references.json')['dependencies']['IG-2B05']},
    'input_pins': pins,
    'assigned_physical_pages': [21,22,23,24],
    'assigned_page_metadata': [{k:p[k] for k in ('id','key','revision','pdf_page','source_revision','media_box','crop_box','effective_crop_box','rotation','user_unit')} for p in pages],
    'placeholder_targets': targets,
    'context_only_source_regions': inspection['context_only_observations'],
    'accepted_counts': {'pages': len(baseline['pages']), 'regions': len(baseline['regions']), 'evidence': len(baseline['evidence']), 'links': len(baseline['links'])},
    'owned_executor_root': OUTPUT,
    'required_deliverables': [OUTPUT + '/' + name for name in required_files],
    'preservation': [
        'Load the full accepted inventory and its exact companion identity-registry, checking embedded registry binding before editing; do not rebuild from an ancestor or a structural importer.',
        'Keep all 44 original page identities/geometry/source revisions. Nonassigned records, links, evidence and reading-order relative order remain structurally equal; copy them internally without dumping their contents.',
        'Remove only the four assigned placeholder memberships and their reading-order positions. Never delete or remap their old registry entries; assign explicit new region keys and retain all registry bindings.',
        'Preserve every pre-existing evidence artifact byte-for-byte and every baseline report as an immutable input. Update only assigned records and necessary full-inventory revision/registry/coverage bindings through existing tooling.',
        'For links crossing the assigned boundary, preserve existing accepted references; record new links to exact current region IDs and reasons without replacing unassigned records. New context regions have denominator_role=context and do not replace the page-25 placeholder.',
        'Use the latest accepted source-reference reports pinned above. No old placeholder source path, ancestor baseline, blocked attempt, transcript or derivation helper is an input.'
    ],
    'inspection_and_inventory': [
        'Freshly render and visually inspect all four original assigned pages. List every authored region and all components in original-page-inspection.json with exact source/page/box and fresh render pins; coordinator observations are navigation only.',
        'Inspect every clause, bullet, heading, note, example, counter image, diagram, arrow, label, table/legend if present, header/footer and editorial area. Subdivide compound diagrams/counter groups into identified components or explicitly justify a complete compound region. Do not omit any component.',
        'Use integer normalized half-open boxes and the installed locator contract. Distinguish inventory from context. Explicitly account for whitespace and all geometric gaps without claiming gaps or placeholders are represented source content.',
        'Independently author the denominator from source regions; never use KB headings or a smaller selection. Keep transcription, descriptive semantics, formal semantics, technical review and human acceptance separate.',
        'Inspect only the narrow adjacent context regions above to resolve incoming and outgoing continuations. Assigned pages are full-page inspection scope. If other context is indispensable, checkpoint and request a fresh bounded contract rather than expand access.',
        'Record incoming 20-to-21, internal across-column and across-page continuations, and outgoing 24-to-25 references with region/page IDs, exact boxes and evidence pins. A known sequence/reference boundary need not falsely claim unfinished text.',
        'Mark uncertain readings explicitly. Without a real scoped human decision, keep non-game/editorial material inventoried with appropriate explicit coverage gaps; do not fabricate excluded/accepted semantics.'
    ],
    'fresh_evidence_and_replays': [
        'Generate fresh source-bound text/PNG/cropped-PDF evidence for every assigned authored region at 144 DPI, using installed wgc.sources tools. Fresh evidence must bind source SHA, page basis, exact region revision/box, file paths/bytes/hashes and engine versions.',
        'Use two separate new replay output directories replay-a and replay-b. Independently re-run complete assigned-page evidence generation from the same pre-evidence authored full inventory plus persisted registry, including all proposed boundaries/components; neither replay may reuse the other replay output as its input.',
        'Compare canonical assigned author projections, stable IDs and registry, full nonassigned preservation, source/page/region bases, extracted text bytes, crop-PDF bytes, PNG bytes and dimensions across both replays. Report and explain path-dependent inventory/evidence IDs instead of asserting complete inventory byte equality across disjoint paths.',
        'Create final-verified/inventory.json with its identity-registry.json in a fresh final output directory and fresh path-correct evidence locators. Validate the complete final inventory against actual source bytes and all artifact hashes; do not merely copy evidence claims from replays.',
        'Each required report is task-local and pins exact current final inventory/registry and all relevant current input/output reports. Do not inherit old report input indexes or copy an entire old artifact manifest into context.'
    ],
    'reports': {
        'region-ledger.json': 'Exact complete assigned region IDs/revisions, page/box, kind, component list, reading order, evidence IDs and explicit uncertainty/gaps; account for every original-page area.',
        'continuations.json': 'Exact incoming/internal/outgoing links and reasons plus distinct context-only IDs/boxes; retain cross-batch references and explicitly unresolved boundaries.',
        'coverage-report.json': 'Separate full 44-page, assigned 4-page and context-only denominators/counts/areas; account for remaining placeholders and gaps, no inference of semantic acceptance or executable readiness.',
        'source-pins.json': 'Actual official PDF/provenance, accepted baseline/registry and named reports, assigned pages/targets and all current final report/evidence pins; no obsolete placeholder path.',
        'toolchain.json': 'Installed interpreter/native/library versions and exact executable hashes, process_pythonpath including both repo/src and bundled site-packages, process_path_prefix, render settings; no installs or global changes.',
        'preservation-report.json': 'Machine-checked nonassigned-record/link/evidence equality, unchanged old registry mappings and retained retired entries, complete page identities, baseline input hashes rechecked after execution.',
        'original-page-inspection.json': 'Fresh original-page and narrow context visual observations mapped to every ledger region/component; do not inherit coordinator inspection claims.',
        'replay-report.json': 'Two independent complete replay command/exit records, input/output hashes and explicit stable/path-dependent comparison results.',
        'validation-report.json': 'Actual checks, exit codes and immutable log pins; no predicted passes.',
        'delivery-handoff.md': 'Full frozen artifact manifest reference, criteria met/unmet, independent technical/source inventory review request, unknown measurements, remaining issues and exact next action.'
    },
    'executor_validation': [
        '.venv/Scripts/python.exe -m wgc.sources validate ' + OUTPUT + '/final-verified/inventory.json',
        '.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp ' + OUTPUT + '/pytest-sources-01 -p no:cacheprovider --tb=short',
        'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B06',
        'git diff --check',
        'Machine assertions: all nonassigned records/links/evidence preserved; registry binding/mappings retained; precisely four placeholders retired; full/task/context counts and no overlap; every assigned region has fresh evidence; both replays agree on stable content and locators validate.'
    ],
    'independent_review': [
        'A fresh distinct reviewer must inspect every assigned original page and every proposed region/component and boundary against the complete ledger and frozen final evidence, revalidate all pins/preservation/replay comparisons and run required checks.',
        'Technical/source inventory review does not accept source meaning. Keep any existing human gate binding; no model may fabricate human authority or decide gameplay legality.',
        'Review and acceptance apply only to exact frozen output hashes and complete task acceptance/tests. Readiness of this contract grants no product acceptance or completed status.'
    ],
    'context_policy': 'Only exact public control windows, selected own metadata and prepared dependency projections; assigned source pages/IDs/boxes above. No historical transcripts, archives, whole manifests/queue events, private search or unassigned source analysis.',
    'measurement': {'input_tokens': None, 'output_tokens': None, 'operator_seconds': None, 'unknown_reason': 'Not exposed to this coordinator.'}
}
dump(RUN / 'refinement-contract.json', contract)

queue_path = Path(w.QUEUE)
queue = load(queue_path)
assert w.digest(queue_path) == initial['base_files'][0]['sha256'], 'Concurrent queue writer'
task = next(t for t in queue['tasks'] if t['id'] == 'IG-2B06')
selected = load(SESSION / 'task.json')
assert {k:v for k,v in task.items() if k != 'events'} == selected
before_others = {t['id']: copy.deepcopy(t) for t in queue['tasks'] if t['id'] != task['id']}
assert all(next(t for t in queue['tasks'] if t['id'] == d)['status'] == 'done' for d in task['depends'])
task['title'] = 'Inventory SPQR PDF pages 21-24'
task['outputs'] = contract['required_deliverables']
task['write_scope'] = [OUTPUT + '/', 'private/workflow/runs/IG-2B06/review-inventory-21-24/', 'private/workflow/checks/']
task['inputs'] = [f"{p['path']} (SHA-256 {p['sha256']})" for p in pins]
task['inputs'].append(f"Exact refinement contract: {RUN.as_posix()}/refinement-contract.json (SHA-256 {w.digest(RUN/'refinement-contract.json')}); physical pages 21-24 assigned, adjacent context only as boxed there.")
task['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md', by_name['provenance.json']['path'], (RUN/'refinement-contract.json').as_posix(), (RUN/'toolchain.json').as_posix()]
task['refinement_contract'] = pin(RUN/'refinement-contract.json')
task['source_scope'] = {'source': by_name['rulebook.pdf'], 'assigned_physical_pages': [21,22,23,24], 'target_ids':[r['id'] for r in regions], 'context_only_regions': inspection['context_only_observations']}
task['acceptance'] += [
    'Preserve the complete accepted 44-page sidecar, companion registry and all nonassigned records, links and evidence; retire only the four assigned placeholders without deleting registry entries, and machine-check preservation.',
    'Deliver the complete fresh final-verified inventory/registry and all reports pinned in the refinement contract, including original-page inspection, component accounting, two independent complete evidence replays and separate full/task/context denominators.',
    'A fresh independent reviewer inspects every assigned original page, all proposed regions/components and continuation boundaries against the frozen ledger/evidence and verifies preservation, fresh locators and replay comparisons; no human semantic acceptance or gameplay readiness is inferred.'
]
task['tests'] += [
    'Execute all exact validation commands in the hash-pinned refinement contract with the installed process-local toolchain; preserve actual command/exit/log evidence and keep assertions unchanged.',
    'Assert complete nonassigned preservation, retained identity-registry bindings/retired keys, exact assigned placeholder retirement, full/task/context denominator separation, fresh evidence for every assigned region and two independent replay equivalence checks with explicit path-dependent differences.'
]
task['start_conditions'] += ['Fresh absent executor root and checkpoint; verified latest accepted baseline/registry/source/report pins and observed gpt-6.1-sol/high; comply with the hash-pinned refinement contract and exact source context scope.']
task['handoff'] += ['Freeze all final inventory, registry, evidence, reports and meaningful validation logs in their original order; request fresh independent whole-batch review. Coordinator readiness never grants acceptance.']
assert all(x in task['acceptance'] for x in selected['acceptance'])
assert all(x in task['tests'] for x in selected['tests'])
assert task['semantic_acceptance_required'] == selected['semantic_acceptance_required']
assert all(t == before_others[t['id']] for t in queue['tasks'] if t['id'] in before_others)
policy_path = Path('docs/work/context-policy.json')
assert w.digest(policy_path) == initial['base_files'][1]['sha256']
policy = load(policy_path)
added = []
for p in task['context']:
    if p not in policy['allow']:
        policy['allow'].append(p)
        added.append(p)
# Only selected structural edits; preserve every other task and existing policy entry.
with policy_path.open('w',encoding='utf-8') as f:
    json.dump(policy,f,ensure_ascii=False,indent=2); f.write('\n')
w.validate(queue, ROOT, check_views=False)
with queue_path.open('w',encoding='utf-8') as f:
    json.dump(queue,f,ensure_ascii=False,indent=2); f.write('\n')
w.render(queue, ROOT)
dump(RUN/'refinement-edit-report.json', {**identity, 'format':'wgc-refinement-edit-report-1', 'task':'IG-2B06', 'status':'planned', 'summary':'Only selected task refined; original acceptance/tests preserved verbatim; exact context policy entries appended.', 'contract':pin(RUN/'refinement-contract.json'), 'queue':pin(queue_path), 'context_policy':pin(policy_path), 'added_policy_paths':added, 'other_tasks_unchanged':True, 'future_executor_root_absent':True, 'source_scope_observation':pin(RUN/'source-scope-observation.json')})
print(json.dumps({'task':'IG-2B06','status':'planned','assigned_pages':4,'placeholder_targets':4,'nonselected_tasks_preserved':len(before_others),'context_entries_added':len(added),'refinement_contract':pin(RUN/'refinement-contract.json')}))
