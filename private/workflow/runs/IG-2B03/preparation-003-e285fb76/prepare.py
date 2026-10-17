import copy
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
PREP = Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76')
SESSION = Path('private/workflow/orchestrator/20261015T144301Z-98bff5f8/003-IG-2B03-coordinator-e285fb76')
ATTEMPT = 'private/workflow/runs/IG-2B03/inventory-003-e285fb76'
BASE = Path('private/workflow/runs/IG-2B02/repair-r01-r02-20261015T091559Z-reserved-by-01a13c20-b7bd-7962-a954-f5841c09831c')
OLDPREP = Path('private/workflow/runs/IG-2B02/preparation-20261014T201344Z-01a13c09-ed4d-7ab2-b967-5e6db69e78b8')
ACTOR = 'ig2:003-IG-2B03-coordinator-e285fb76:coordinator'

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def pin(p):
    p = Path(p)
    return dict(path=p.as_posix(), bytes=p.stat().st_size, sha256=sha(p))

def save(name, data):
    p = PREP / name
    with p.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return pin(p)

configuration = SESSION / 'runtime-configuration.json'
runtime = load(configuration)
assert (runtime['status'], runtime['model'], runtime['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
META = dict(role='coordinator', actor=ACTOR, task='IG-2B03', model=runtime['model'], reasoning=runtime['reasoning'], configuration_evidence=configuration.as_posix(), configuration_sha256=sha(configuration))
now = datetime.now(timezone.utc).isoformat()
qpath = Path('docs/work/queue.json')
ppath = Path('docs/work/context-policy.json')
queue = load(qpath)
selected = next(t for t in queue['tasks'] if t['id'] == 'IG-2B03')
original = copy.deepcopy(selected)
assert selected['status'] == 'planned' and selected['events'] == []
assert {k:v for k,v in selected.items() if k != 'events'} == load(SESSION / 'task.json')
assert sha(qpath) == load(SESSION / 'packet.json')['queue_sha256']
for item in load(SESSION / 'packet.json')['files']:
    assert sha(item['path']) == item['sha256']
for name, path in [('queue-before.json', qpath), ('context-policy-before.json', ppath)]:
    with (PREP / name).open('xb') as out:
        out.write(path.read_bytes())
assert not Path(ATTEMPT).exists()
dep = next(t for t in queue['tasks'] if t['id'] == 'IG-2B02')
assert dep['status'] == 'done'
done_event = dep['events'][-1]
assert done_event == load(SESSION / 'references.json')['dependencies']['IG-2B02']
events = {state: next(e for e in reversed(dep['events']) if e['to'] == state) for state in ['done', 'accepted', 'review']}
for event in events.values():
    assert sha(event['evidence']) == event['sha256']
delivery = load(events['review']['evidence'])
review = load(events['accepted']['evidence'])
done = load(events['done']['evidence'])
assert delivery['artifacts'] == review['artifacts'] == done['artifacts']
assert review['technical_result'] == 'pass' and not review['findings']
verified = []
for item in delivery['artifacts']:
    assert Path(item['path']).is_file() and sha(item['path']) == item['sha256'], item['path']
    verified.append(item)
save('dependency-verification.json', dict(**META, format='wgc-dependency-verification-1', observed_utc=now, events=events, delivery=pin(events['review']['evidence']), accepted_review=pin(events['accepted']['evidence']), closure=pin(events['done']['evidence']), artifact_count=len(verified), all_frozen_artifacts_verified=True, product_inventory=pin(BASE/'final-verified/inventory.json'), registry=pin(BASE/'final-verified/identity-registry.json'), semantic_acceptance_granted=False))
inventory = load(BASE/'final-verified/inventory.json')
pages = {p['id']: p['pdf_page'] for p in inventory['pages']}
assigned_pages = [p for p in inventory['pages'] if p['pdf_page'] in [9,10,11,12]]
placeholders = [r for r in inventory['regions'] if pages[r['page_id']] in [9,10,11,12]]
assert len(placeholders) == 4 and all(r['key'].endswith(':unprocessed-placeholder') for r in placeholders)
context_region = next(r for r in inventory['regions'] if r['key'] == 'ig2b02:p8:subordinate-momentum')
context_evidence = [e for e in inventory['evidence'] if e['region_id'] == context_region['id']]
context_artifacts = []
for e in context_evidence:
    for value in e.values():
        if isinstance(value, dict) and {'path', 'sha256'} <= value.keys():
            assert sha(value['path']) == value['sha256']
            context_artifacts.append(pin(value['path']))
inputs = [pin(BASE/'final-verified/inventory.json'), pin(BASE/'final-verified/identity-registry.json'), pin(BASE/'continuations.json'), pin(OLDPREP/'contract-boundaries.md'), pin(OLDPREP/'toolchain.json')]
for value in [inventory['source']['pdf'], inventory['source']['provenance']]:
    assert sha(value['path']) == value['sha256']
    inputs.append(pin(value['path']))
for path in ['contracts/ig/README.md','contracts/ig/regions.schema.json','src/wgc/sources/README.md']:
    inputs.append(pin(path))
tools = load(OLDPREP/'toolchain.json')
for group in ['frozen_contract_and_tool_pins']:
    for item in tools[group]:
        assert sha(item['path']) == item['sha256']
        if item['path'] not in [i['path'] for i in inputs]:
            inputs.append(pin(item['path']))
save('input-pins.json', dict(**META, format='wgc-ig2b03-input-pins-1', files=inputs, dependency_reference=pin(PREP/'dependency-verification.json'), source_page_count=44, assigned_physical_pages=[9,10,11,12], assigned_page_records=[dict(id=p['id'], key=p['key'], pdf_page=p['pdf_page'], revision=p['revision']) for p in assigned_pages], replace_only_placeholders=[dict(id=r['id'], key=r['key'], revision=r['revision']) for r in placeholders], context_only_ids=[context_region['id']], context_only_revision=context_region['revision'], context_only_evidence=context_artifacts, full_baseline_policy='Read baseline structurally to preserve exact records, registry, evidence, links and coverage. Content analysis only assigned pages and the exact optional accepted page-8 region; never analyze remaining source pages.'))
save('toolchain.json', dict(**META, format='wgc-ig2b03-toolchain-1', inherited_pin=pin(OLDPREP/'toolchain.json'), process_pythonpath=tools['process_pythonpath'], process_path_prefix=tools['process_path_prefix'], python_executable=tools['python_executable'], libraries=tools['libraries'], native=tools['native'], settings_policy='Process-local only. PYTHONPATH must include both repo/src and bundled Python Lib/site-packages, including reportlab. No installs or global settings. Verify installed hashes and versions at claim time.'))
scope = dict(**META, format='wgc-ig2b03-refinement-1', prepared_utc=now, dependency='IG-2B02', kind='content', assigned_physical_pages=[9,10,11,12], target_ids=[p['id'] for p in assigned_pages], context_only_ids=[context_region['id']], inputs=pin(PREP/'input-pins.json'), output_root=ATTEMPT,
    content_access=dict(pdf_pages=[9,10,11,12], adjacent_context='Optional read of only the accepted page-8 subordinate-momentum region and exact evidence pinned in input-pins.json. No fresh extraction/rendering of page 8. Accepted boundary report says no unfinished fragment. No access to page 13 or other source pages; retain raw cross-chapter citations and unresolved gaps without following them.', structural_access='Hash entire pinned files, count PDF pages and verify geometry of all 44 physical pages without text/image extraction. Baseline metadata may be compared for preservation; accepted unrelated text/evidence may only be byte-compared, never analyzed.'),
    preservation=dict(baseline_inventory=pin(BASE/'final-verified/inventory.json'), registry=pin(BASE/'final-verified/identity-registry.json'), immutable_pages='Exact accepted pages/regions/coverage/evidence 1-8 and placeholders 13-44, all old evidence, links, registry entries and existing context regions remain unchanged. Only page-label evidence for assigned pages may be added with current exact locators. Retire only placeholder membership for 9-12; retain retired registry bindings. Extend explicit keys without remapping.', context='Do not convert the optional page-8 record to context in the inherited full inventory or change its accepted denominator role. Count it only as context in this task report; no new duplicate inventory membership or denominator units.'),
    original_acceptance=original['acceptance'], original_tests=original['tests'],
    required_outputs=['final-verified/inventory.json','final-verified/identity-registry.json','region-ledger.json','continuations.json','coverage-report.json','visual-review.json','preservation-report.json','registry-replay-report.json','source-pins.json','toolchain.json','delivery-manifest.json','delivery.json','delivery-handoff.md'],
    evidence_policy='Derive exact current UTF-8 text, PNG and crop PDF evidence for every new assigned region. New absent directories only. Pin source/page_basis_hash/box/revision/engines/DPI/actual dimensions/Unicode offsets and artifact bytes/SHA256. Ledger includes all region IDs and reading order; counters/diagrams have component observations. No automatic represented/excluded promotions. Blank geometry and all partial/unprocessed content stay explicit gaps.',
    replay='Replay authored partition with persisted registry in two new directories. Compare identical canonical authored inventory/registry bytes and IDs; evidence outputs use separate paths and must each independently validate, without claiming path-dependent final evidence bytes equal.',
    review='Independent fresh reviewer inspects original physical pages 9-12 and all authored region boundaries and components, not merely crops or ledger. Compare complete source coverage, exact preservation, old hashes, current locators and every submitted artifact. Technical review grants no semantic acceptance.',
    required_commands=[f'.venv/Scripts/python.exe -B -m wgc.sources validate {ATTEMPT}/final-verified/inventory.json','.venv/Scripts/python.exe -B -m pytest -q tests/sources --basetemp private/workflow/checks/b03-<unique-attempt> -p no:cacheprovider --tb=short','pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B03','.venv/Scripts/python.exe -B scripts/workflow.py validate','git diff --check'],
    operational='Fresh executor claims with its own observed Sol/high runtime evidence and ownership before authoring. Queue structural edits remain coordinator-owned. At most two repairs per finding/two unchanged retries. If restricted Windows token cannot access mode0700 pytest dirs, request approved exact unchanged command; never alter ACLs/tests/libraries/assertions. Stop after this task.',
    semantic_acceptance_granted=False, executable_readiness='unverified')
save('scope.json', scope)
notes = {
  '9': 'Both columns, header/page label/footer; 4.34-4.35; blue design note; 4.4 heading, commander counter and all component glyphs, introduction, numbered items 1-6 and historical note; 4.5 heading/introduction, 4.51-4.56 including exception and play note. 4.56 visibly continues to page 10.',
  '10': 'Both columns and furniture; top-left continuation of 4.56 and both bullets; 4.6 introduction, exception and historical digression; 4.7 and 4.71-4.75 with column transition; design note; 4.8 introduction, 4.81-4.84 and final design note.',
  '11': 'Both columns and furniture; 4.85; optional 4.9 heading, elephant counter and components, 4.91-4.94 including all bullets; 5.0 heading/introduction and boxed IMPORTANT note; 5.1/5.11 across columns; 5.12-5.15 with exceptions, activation example, all six Finished bullets and final exception; 5.2/5.21 and example, 5.22 introduction continuing to page 12.',
  '12': 'Both columns and furniture; 5.22 numbered items 1-7 and closing paragraph; 5.23 and both numbered items plus closing paragraph; 5.24 and example; 5.25; 5.26 across columns plus example; 5.27-5.28 and both numbered items/closure; 5.3 heading/play note; 5.31 with three restrictions, 5.32 and example, 5.33 with three die-result bullets, 5.34. Bottom text ends in complete sentence; no page-13 access needed.'
}
save('source-inspection.json', dict(**META, format='wgc-ig2b03-source-inspection-1', assigned_pages=[9,10,11,12], render_command='pdftoppm -f 9 -l 12 -r 120 -png '+inventory['source']['pdf']['path']+' '+PREP.as_posix()+'/page', render_exit_code=0, visual_inspection_completed=True, renders=[dict(**pin(PREP/f'page-{n:02d}.png'), physical_page=n, observation=notes[str(n)]) for n in [9,10,11,12]], purpose='Coordinator bounds and completeness requirements only; no inventory, semantic acceptance or full transcription delivered. Executor and reviewer must independently inspect all pages/regions at sufficient resolution.', boundary_8='Accepted continuation report records no unfinished fragment and no page-9 access by IG-2B02.', boundary_13='Not accessed; page 12 last paragraph visibly complete. Preserve any other cross-page reference as unresolved without expanding scope.'))
save('checkpoint.json', dict(**META, format='wgc-coordinator-checkpoint-1', started_utc=now, input_packet=pin(SESSION/'packet.json'), references=pin(SESSION/'references.json'), base_queue=pin(PREP/'queue-before.json'), base_policy=pin(PREP/'context-policy-before.json'), owned_paths=['docs/work/queue.json','docs/work/context-policy.json',PREP.as_posix()+'/','derived queue views'], completed=['Runtime confirmed','Exact dependency event and all frozen delivery artifact hashes verified','Assigned source pages visually inspected','Bounded source/input/output contract prepared'], blocker=None, next_operation='Refine selected queue task, render derived views, validate, then record readiness. No executor claim or product authoring.'))

selected['title'] = 'Inventory SPQR PDF pages 09-12'
selected['outputs'] = [ATTEMPT+'/'+s for s in scope['required_outputs']]
selected['write_scope'] = [ATTEMPT+'/', 'private/workflow/packets/', 'private/workflow/checks/']
selected['inputs'] = [f"{i['path']} SHA256 {i['sha256']}" for i in inputs[:7]] + ['Exact input-pins.json and scope.json are binding: full 44-page inventory; author only physical pages 9-12. Frozen contract/tool pins are read-only.']
selected['context'] = ['docs/work/EVIDENCE.md','src/wgc/sources/README.md','contracts/ig/regions.schema.json', inventory['source']['provenance']['path'], inventory['source']['pdf']['path']] + [(PREP/n).as_posix() for n in ['scope.json','input-pins.json','toolchain.json','source-inspection.json']] + [(OLDPREP/'contract-boundaries.md').as_posix()]
selected['acceptance'] += [
 'Retain the full 44-page wgc-inventory-1 sidecar. Preserve exact accepted pages/regions/coverage/evidence 1-8, placeholders 13-44, all old links/evidence/context and every persisted registry binding; replace only placeholder memberships 9-12 and retain retired registry entries.',
 'Independently inventory both columns and every heading, clause/list item, note, exception, example, diagram/counter component, table/legend and editorial region on physical pages 9-12; pin complete reading order, explicit geometric/content gaps and raw cross-chapter references.',
 'Pin every new region to current exact source/page/box/revision/page_basis_hash and text/PNG/crop-PDF bytes, Unicode offsets, tool versions and predicted/actual pixel dimensions. Preserve uncertainty; no crop or bbox grants represented coverage.',
 'Keep full/task/context denominators separate. Optional accepted page-8 context contributes zero task denominator and does not change its inherited record. Partial/unprocessed regions remain gaps; editorial classification does not authorize exclusion or semantic acceptance.',
 'Freeze full inventory, registry, complete region/component ledger, continuation list, visual/coverage/preservation/replay reports and all evidence in the delivery manifest. A fresh independent reviewer compares every original assigned page and all region/component boundaries against the complete ledger, verifies all frozen artifacts and unchanged prior scope.'
]
selected['tests'] += [
 'Root wgc.sources validate reopens the byte-pinned PDF, checks strict pypdf and Poppler counts of 44, all actual page geometry, schema/canonical revisions, persisted registry, partitions, reading order and current evidence bytes.',
 'Visually inspect all original physical pages 9-12 at sufficient resolution and every proposed region/counter component. Validate source/page/box/page_basis_hash/Unicode offsets, rational crop bounds and actual PNG header dimensions; compare complete source-region ledger independently.',
 'Compare exact accepted nested records 1-8 and placeholders 13-44, every prior region/evidence/link/registry binding and old artifact hash against accepted IG-2B02. Rebuild authored partition twice with the persisted registry in fresh directories and compare canonical authored bytes/IDs; independently validate each path-dependent evidence output.',
 'Verify literal continuations 9-to-10 and 11-to-12, within-page column continuations and zero task denominator for context; record no access outside the exact contract. All remaining geometric/content/representation gaps are explicit, and no gap or editorial region is silently represented/excluded.',
 'Run unchanged tests/sources with fresh short --basetemp and -p no:cacheprovider; pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B03; workflow validate; git diff --check. Preserve full pinned process PYTHONPATH including bundled site-packages and Poppler path. Request approved execution of exact unchanged commands for mode0700 Windows token failures; do not alter tests/tools/contracts/ACLs.'
]
selected['start_conditions'] += ['Accepted IG-2B02 event, all input SHA256 pins and complete available exact context verified; no unresolved refinement. New executor output root must be absent and exclusively claimed by a fresh observed Sol/high executor.', 'Read preparation-003-e285fb76/scope.json and input-pins.json on demand; do not read context.txt, whole historical manifests, prior transcripts, run directories or source content outside assigned scope.']
selected['exclusions'] += ['No source/tool/test/contract changes or old evidence regeneration. No new extraction/rendering outside physical pages 9-12. Optional context is restricted to the exact accepted page-8 region/evidence; do not access page 13, other source content or follow cross-chapter references.', 'No mutation of old delivery, prior accepted inventory, registry bindings or old artifact bytes. No source-IG semantic acceptance or gameplay legality decisions.']
selected['target_ids'] = scope['target_ids']
selected['context_only_ids'] = scope['context_only_ids']
selected['refinement_evidence'] = pin(PREP/'scope.json')
assert selected['acceptance'][:len(original['acceptance'])] == original['acceptance']
assert selected['tests'][:len(original['tests'])] == original['tests']
policy = load(ppath)
allow = list(dict.fromkeys([i['path'] for i in inputs] + [p['path'] for p in context_artifacts] + [(PREP/n).as_posix() for n in ['scope.json','input-pins.json','toolchain.json','source-inspection.json']]))
for value in allow:
    if value not in policy['allow']:
        policy['allow'].append(value)
assert sha(qpath) == sha(PREP/'queue-before.json') and sha(ppath) == sha(PREP/'context-policy-before.json')
qpath.write_text(json.dumps(queue, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
ppath.write_text(json.dumps(policy, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(preparation=PREP.as_posix(), dependency_frozen_artifacts_verified=len(verified), assigned_pages=[9,10,11,12], task_status=selected['status'])))
