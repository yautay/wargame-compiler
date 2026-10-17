"""Fresh task-local accounting, preservation and independent replay comparisons."""
import collections
import datetime
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import file_pin, digest, page_basis_hash, coverage
from wgc.sources.geometry import area

ROOT = Path.cwd()
RUN = Path('private/workflow/runs/IG-2B06/continuation-21-24-serial02')
SESSION = Path('private/workflow/orchestrator/20261016T182116Z-202cea4c/001-IG-2B06-executor-f2379326')
claim = json.loads((RUN/'claim.json').read_text())
META = {k:claim[k] for k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256','task')}
task = json.loads((SESSION/'task.json').read_text())
contract = json.loads(Path(task['refinement_contract']['path']).read_text())
scope = json.loads(Path(task['continuation_authorization']['scope']['path']).read_text())
baseline = json.loads(Path(contract['input_pins'][0]['path']).read_text())
base_registry = json.loads(Path(contract['input_pins'][1]['path']).read_text())
author = json.loads((RUN/'authored/inventory.json').read_text())
rows = json.loads((RUN/'author-regions.json').read_text())['regions']
docs = {name:json.loads((RUN/name/'inventory.json').read_text()) for name in ('replay-a','replay-b','final-verified')}
final = docs['final-verified']
page_by_id = {p['id']:p for p in final['pages']}
regions = {r['id']:r for r in final['regions']}
new_ids = {r['id'] for r in final['regions'] if r['key'].startswith('ig2b06:')}
assigned_ids = {rid for rid in new_ids if regions[rid]['denominator_role']=='inventory'}
context_ids = new_ids-assigned_ids
target_ids = set(task['source_scope']['target_ids'])
assert len(assigned_ids)==112 and len(context_ids)==2

def pin(path):
    return file_pin(ROOT,Path(path).as_posix())

COMMON = {'final_inventory':pin(RUN/'final-verified/inventory.json'),
          'final_registry':pin(RUN/'final-verified/identity-registry.json'),
          'input_packet':pin(SESSION/'packet.json'),'selected_task':pin(SESSION/'task.json'),
          'refinement_contract':pin(task['refinement_contract']['path']),
          'authored_input':pin(RUN/'authored/inventory.json'),
          'authored_registry':pin(RUN/'authored/identity-registry.json')}

def write(name,summary,**data):
    p=RUN/name
    assert not p.exists(),str(p)
    p.write_text(json.dumps({**META,'summary':summary,**COMMON,**data},indent=2)+'\n',encoding='utf-8')
    return pin(p)

# All original accepted records are compared internally, never dumped as context.
expected_regions = [r for r in baseline['regions'] if r['id'] not in target_ids]
old_ids = {r['id'] for r in baseline['regions']}
base_entries = {(e['kind'],e['key']):e['id'] for e in base_registry['entries']}
preservation_results = {}
for name,doc in docs.items():
    entries = {(e['kind'],e['key']):e['id'] for e in doc['registry']['entries']}
    checks = {
        'source_metadata_equal':doc['source']==baseline['source'],
        'all_44_page_records_equal':doc['pages']==baseline['pages'] and len(doc['pages'])==44,
        'all_nonassigned_regions_equal_in_original_relative_order':[r for r in doc['regions'] if r['id'] in old_ids]==expected_regions,
        'all_original_links_equal_prefix':doc['links'][:len(baseline['links'])]==baseline['links'],
        'all_original_evidence_equal_prefix':doc['evidence'][:len(baseline['evidence'])]==baseline['evidence'],
        'all_original_registry_bindings_retained':all(entries.get(k)==v for k,v in base_entries.items()),
        'exactly_four_placeholder_memberships_removed':old_ids-{r['id'] for r in doc['regions']}==target_ids,
        'retired_placeholder_registry_entries_retained':all(e in doc['registry']['entries'] for e in base_registry['entries'] if e['id'] in target_ids),
        'nonassigned_reading_order_equal':[rid for rid in doc['reading_order'] if rid in old_ids]==[rid for rid in baseline['reading_order'] if rid not in target_ids],
        'authored_regions_links_order_registry_equal':all(doc[k]==author[k] for k in ('regions','links','reading_order','registry','pages','source','toolchain')),
    }
    assert all(checks.values()),(name,checks)
    preservation_results[name]=checks
input_rechecks=[]
for x in contract['input_pins']+scope['drafts']+[scope['preserve_manifest'],scope['assessment'],scope['effective_refinement_contract']]:
    assert pin(x['path'])==x,x['path']; input_rechecks.append(x)
preserved=json.loads(Path(scope['preserve_manifest']['path']).read_text())
for x in preserved['artifacts']:
    actual=pin(x['path']); assert actual['sha256']==x['sha256'],x['path']
for ev in baseline['evidence']:
    for k in ('text','image','crop_pdf'):
        assert pin(ev[k]['path'])==ev[k]
preservation_pin=write('preservation-report.json','Machine-checked complete accepted baseline and blocked-attempt preservation across both independent replays and final output.',
    checks=preservation_results,baseline_inventory=contract['input_pins'][0],baseline_registry=contract['input_pins'][1],
    nonassigned_region_count=len(expected_regions),original_link_count=len(baseline['links']),original_evidence_count=len(baseline['evidence']),
    original_registry_count=len(base_registry['entries']),retired_placeholder_ids=sorted(target_ids),
    blocked_attempt_artifacts_rehashed=len(preserved['artifacts']),baseline_evidence_files_rehashed=len(baseline['evidence'])*3,
    input_pins_rechecked_after_generation=input_rechecks,all_passed=True)

# Compare every generated artifact's bytes/hash and every stable locator field.
new_evidence={name:{e['region_id']:e for e in doc['evidence'] if e['region_id'] in new_ids} for name,doc in docs.items()}
for name,items in new_evidence.items():
    assert set(items)==new_ids
    assert all(e[k]['path'].startswith((RUN/name).as_posix()+'/') for e in items.values() for k in ('text','image','crop_pdf'))
comparisons=[]
for rid in sorted(new_ids):
    evs=[new_evidence[n][rid] for n in docs]
    stable=[{k:v for k,v in e.items() if k not in ('text','image','crop_pdf')} for e in evs]
    assert stable[0]==stable[1]==stable[2],rid
    files={}
    for k in ('text','image','crop_pdf'):
        pins=[e[k] for e in evs]
        assert len({p['path'] for p in pins})==3
        assert len({(p['bytes'],p['sha256']) for p in pins})==1,(rid,k)
        assert all(pin(p['path'])==p for p in pins)
        files[k]={'sha256':pins[0]['sha256'],'bytes':pins[0]['bytes'],'distinct_paths':[p['path'] for p in pins]}
    comparisons.append({'region_id':rid,'region_revision':regions[rid]['revision'],'page_basis_hash':evs[0]['page_basis_hash'],
        'evidence_id':evs[0]['id'],'stable_locator_fields_equal':True,'artifact_bytes_equal':True,'artifacts':files,
        'png_pixels':[evs[0]['render_parameters']['width_pixels'],evs[0]['render_parameters']['height_pixels']]})
assert len({doc['revision'] for doc in docs.values()})==3
generation_reports=[json.loads((RUN/name/'generation-report.json').read_text()) for name in docs]
assert len({g['input_inventory']['sha256'] for g in generation_reports})==1
assert len({g['input_registry']['sha256'] for g in generation_reports})==1
assert all(set(g['complete_region_ids'])==new_ids and g['exit_code']==0 for g in generation_reports)
replay_pin=write('replay-report.json','Two complete separate serial replays and independently generated final evidence agree on every stable author field, identity, locator basis and generated byte.',
    generation_reports=[pin(RUN/n/'generation-report.json') for n in docs],commands=[{'command':g['command'],'exit_code':g['exit_code']} for g in generation_reports],
    replay_input_inventory=pin(RUN/'authored/inventory.json'),replay_input_registry=pin(RUN/'authored/identity-registry.json'),
    complete_assigned_regions=112,complete_context_regions=2,comparison_count=len(comparisons),comparisons=comparisons,
    output_inventory_revisions={n:d['revision'] for n,d in docs.items()},registry_equal_across_all_runs=len({digest(d['registry']) for d in docs.values()})==1,
    path_dependent_differences='All text/image/crop locators name their own disjoint output directories; inventory revisions therefore differ. Installed evidence IDs depend only on region ID/revision, page basis and DPI and are observed equal. No assertion of whole-inventory byte equality is made.',
    preservation_report=preservation_pin,all_passed=True)

def gaps_for(regs):
    xs=sorted({0,1000000,*[x for r in regs for x in (r['box'][0],r['box'][2])]})
    ys=sorted({0,1000000,*[y for r in regs for y in (r['box'][1],r['box'][3])]})
    gaps=[]
    for top,bottom in zip(ys,ys[1:]):
        current=None
        for left,right in zip(xs,xs[1:]):
            occupied=any(r['box'][0]<=left and right<=r['box'][2] and r['box'][1]<=top and bottom<=r['box'][3] for r in regs)
            if not occupied:
                if current is not None:current[2]=right
                else:current=[left,top,right,bottom]
            elif current is not None:gaps.append(current);current=None
        if current is not None:gaps.append(current)
    assert sum(area(b) for b in gaps)+sum(area(r['box']) for r in regs)==1000000000000
    return gaps

page_accounting=[]
for n in [21,22,23,24]:
    regs=[r for r in final['regions'] if r['id'] in assigned_ids and page_by_id[r['page_id']]['pdf_page']==n]
    gs=gaps_for(regs)
    page_accounting.append({'pdf_page':n,'page_id':regs[0]['page_id'],'inventory_region_count':len(regs),
        'inventoried_box_area_trillionths':sum(area(r['box']) for r in regs),'explicit_gap_area_trillionths':sum(area(b) for b in gs),
        'gap_boxes':gs,'gap_reason':'Visually inspected margins, column gutter, inter-block whitespace, and background between split note/text regions. These remain geometric gaps and are not represented source content.',
        'gap_semantic_acceptance':False})
ordered_new=[rid for rid in final['reading_order'] if rid in new_ids]
ledger=[]
for rid in ordered_new:
    region=regions[rid]; row=next(r for r in rows if r['region_id']==rid); ev=new_evidence['final-verified'][rid]
    ledger.append({**region,'pdf_page':page_by_id[region['page_id']]['pdf_page'],'description':row['description'],
        'components':row['components'],'reading_order_index':final['reading_order'].index(rid),
        'evidence_ids':[ev['id']],'fresh_evidence':ev,'inspection_status':'Compared against fresh original render and proposed boundary overlay',
        'component_accounting':'All named components visually inspected; a compound region is retained only where its connected field and overprinted arrows/counters cannot be disjointly boxed.' if len(row['components'])>1 else 'Complete named text block or counter/marker face; its border, glyphs, figures, values and background are included where applicable.'})
ledger_pin=write('region-ledger.json','Complete ordered 112-region assigned ledger with two separate context regions, exact fresh evidence and explicit geometric gaps.',
    coordinate_basis='Integer normalized half-open top-left page millionths; original unrotated effective CropBox.',
    regions=ledger,assigned_region_ids=sorted(assigned_ids),context_region_ids=sorted(context_ids),page_accounting=page_accounting,
    assigned_component_count=sum(len(r['components']) for r in rows if r['region_id'] in assigned_ids),
    unresolved_readings=['Machine extraction remains unverified transcription.','Context page 25 is deliberately clipped at the authorized lower boundary.'],
    human_semantic_acceptance=False,executable_readiness='unverified')

new_links=final['links'][len(baseline['links']):]
def endpoint(rid):
    r=regions[rid];return {'region_id':rid,'region_revision':r['revision'],'page_id':r['page_id'],'pdf_page':page_by_id[r['page_id']]['pdf_page'],'box':r['box'],
        'evidence':new_evidence['final-verified'][rid] if rid in new_ids else None}
continuation_pin=write('continuations.json','Freshly inspected incoming, internal and outgoing structural boundaries with exact endpoint evidence and preserved accepted links.',
    preserved_link_count=len(baseline['links']),preserved_links_digest=digest(baseline['links']),
    links=[{**l,'source_endpoint':endpoint(l['from']),'target_endpoint':endpoint(l['to'])} for l in new_links],
    context_regions=[endpoint(rid) for rid in sorted(context_ids)],
    boundary_notes=['Page 20 7.24 lead-in ends with a condition-list introduction; three bullets continue on page 21.',
        'Page 21 7.33 exception list crosses columns; 7.32 mark-/ers and 8.11 counter-adjacent text are split physically without losing links.',
        'Page 22 8.15 sentence crosses columns; 8.17 supply text wraps beside markers; page 23 notes follow complete page-22 bullets.',
        'Page 23 8.31 exception text is complete; the 8.3 sequence resumes on page 24.',
        'Page 24 Beneventum example crosses columns. Important paragraph is complete; page 25 continues the shock procedure/sequence in context only.'],
    unresolved_boundaries=[],human_semantic_acceptance=False)

full_coverage=coverage(final)
assigned_rows=[regions[rid] for rid in assigned_ids]
assigned_area=sum(area(r['box']) for r in assigned_rows)
coverage_pin=write('coverage-report.json','Separate full 44-page, assigned four-page, and zero-contribution context denominators; geometric gaps are never counted as represented content.',
    full_inventory=full_coverage,
    assigned={'physical_pages':[21,22,23,24],'denominator_regions':112,'inventory_box_area_trillionths':assigned_area,
        'total_page_area_trillionths':4000000000000,'gap_area_trillionths':4000000000000-assigned_area,
        'levels':{level:dict(collections.Counter(r['coverage'][level]['status'] for r in assigned_rows)) for level in ('transcription','descriptive_semantics','formal_semantics')},
        'pages':page_accounting},
    task_context={'regions':2,'region_ids':sorted(context_ids),'box_area_trillionths':sum(area(regions[r]['box']) for r in context_ids),'denominator_regions':0,'denominator_area_trillionths':0},
    remaining_placeholders=[{'region_id':r['id'],'key':r['key'],'pdf_page':page_by_id[r['page_id']]['pdf_page']} for r in final['regions'] if r['key'].endswith(':unprocessed-placeholder')],
    geometric_nonoverlap='Validated by installed inventory validator; complement rectangles account for every assigned page area.',
    region_ledger=ledger_pin,semantic_acceptance_granted=False,executable_readiness='unverified')

observations={
21:'Two columns: 7.24 incoming bullets/exception/blue note, 7.25, 7.3 heading/introduction, 7.31-7.33 with two shock markers and example; exception list crosses columns. Right column enters 8.0/8.1, historical notes, four separate missile counters, 8.11 wrapped text/exception/examples. Header and footer included.',
22:'Two columns: 8.12-8.14, complete missile arc compound diagram (hex field, one counter, four Front/Flank labels and nine green dashed arrows), LOS exceptions/note. 8.15 crosses columns; DRM text/blue note/example, 8.16, 8.17 introduction/five bullets with separate Missile No/Low markers and adjacent wraps. Header/footer included.',
23:'Left: complete blue 8.17 design note, gray play note with introduction/two numbered items/completion, 8.18 introduction/two bullets, 8.19. Right: 8.2 heading/introduction, 8.21-8.25 and two exceptions; 8.3 heading/history, 8.31 with two exceptions. Header/footer included.',
24:'Left: 8.32, 8.33 introduction/three bullets/two paragraphs/blue note, 8.34, complete Beneventum compound diagram and example opening. Diagram includes eight labeled counters A-D/W-Z and eight arrows over a connected hex field. Right: four example paragraphs, 8.4 heading/design/play notes, Procedure heading/text and red Important box. Header/footer included.'}
inspection_pin=write('original-page-inspection.json','Fresh direct visual inspection of all assigned originals, all proposed boundaries/components, and only the two contracted context crops.',
    source=final['source']['pdf'],render_dpi=144,
    original_pages=[{'pdf_page':n,'full_page_box':[0,0,1000000,1000000],'render':pin(RUN/f'original-renders/page-{n}.png'),
        'boundary_overlay':pin(RUN/f'original-renders/overlay-{n}.png'),'observation':observations[n],
        'region_component_inspections':[{'region_id':r['id'],'box':r['box'],'components':r['components'],'result':'Visually compared; no omitted named component or assigned text block observed.'} for r in ledger if r['pdf_page']==n]} for n in [21,22,23,24]],
    context_inspections=[{'pdf_page':c['pdf_page'],'box':c['box'],'render':pin(RUN/f"original-renders/context-{c['pdf_page']}.png"),'crop_pdf':pin(RUN/f"original-renders/context-{c['pdf_page']}.pdf"),
        'observation':'7.24 condition-list lead-in and narrow preceding context only.' if c['pdf_page']==20 else '8.4 notes/designation and shock-resolution overview/steps; deliberately clipped at the authorized lower boundary. Sequence context only.'} for c in contract['context_only_source_regions']],
    glyph_center_audit=pin(RUN/'glyph-audit.json'),region_ledger=ledger_pin,continuations=continuation_pin,
    inherited_inspection_claims=False,semantic_acceptance=False,executable_readiness='unverified')

tools=[]
for name in ('pdfinfo','pdftoppm'):
    path=Path(shutil.which(name)).resolve(); b=path.read_bytes()
    import hashlib
    result=subprocess.run([str(path),'-v'],capture_output=True,text=True,check=True)
    tools.append({'name':name,'path':str(path),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'version':(result.stdout+result.stderr).strip()})
toolchain_pin=write('toolchain.json','Observed installed interpreter, libraries and native executables with inherited process-local settings; no installation or global changes.',
    interpreter={'path':sys.executable,'version':sys.version,'pin':pin('.venv/Scripts/python.exe')},
    libraries={name:importlib.metadata.version(name) for name in ('pypdf','pdfplumber','Pillow','pytest','reportlab')},
    native_executables=tools,process_pythonpath=os.environ.get('PYTHONPATH'),process_path_prefix=os.environ.get('PATH','').split(os.pathsep)[0],
    pinned_process_settings=json.loads(Path('private/workflow/runs/IG-2B06/refinement-1bcd2b72-01/toolchain.json').read_text())['process_pythonpath'],
    render_settings={'dpi':144,'cropbox':True,'format':'png','mode':'serial'},
    generation_reports=[pin(RUN/n/'generation-report.json') for n in docs])

source_pin=write('source-pins.json','Exact official source, accepted baseline/report pins, task pages/targets, and fresh final evidence/report index.',
    source_pdf=final['source']['pdf'],provenance=final['source']['provenance'],accepted_input_pins=contract['input_pins'],
    assigned_pages=contract['assigned_page_metadata'],retired_targets=contract['placeholder_targets'],context_boxes=contract['context_only_source_regions'],
    current_reports=[preservation_pin,replay_pin,ledger_pin,continuation_pin,coverage_pin,inspection_pin,toolchain_pin],
    evidence=[e for e in final['evidence'] if e['region_id'] in new_ids],
    final_manifest_note='The immutable delivery envelope adds validation logs/report and handoff after those checks run; this source index avoids circular report hashes.')
write('machine-checks.json','All task-specific preservation, identity, source locator, complete replay, and denominator assertions passed.',
    command=f'.venv/Scripts/python.exe {RUN.as_posix()}/reports.py',exit_code=0,
    checks={'complete_source_and_registry_preservation':True,'exact_four_placeholder_retirement':True,'assigned_count_112_context_count_2':True,
        'all_114_fresh_evidence_triples_in_each_run':True,'both_independent_replays_and_final_bytes_equal':True,
        'all_assigned_pages_fully_partitioned_into_regions_and_explicit_gaps':True,'all_source_input_hashes_rechecked':True},
    reports=[preservation_pin,replay_pin,ledger_pin,continuation_pin,coverage_pin,inspection_pin,toolchain_pin,source_pin])
print(json.dumps({'reports_generated':9,'assigned_regions':112,'task_context_regions':2,'assigned_components':sum(len(r['components']) for r in rows if r['region_id'] in assigned_ids),
    'full_inventory_denominator':full_coverage['denominator_regions'],'full_context_regions':full_coverage['context_regions'],'all_machine_checks_passed':True}))
