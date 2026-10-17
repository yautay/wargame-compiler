"""Freeze bounded structural, visual, preservation and replay reports."""
import copy
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from PIL import Image
from build import ROOT, OUT, SESSION, SCOPE, COMMON, load, write
from wgc.sources.inventory import file_pin, validate, coverage, page_basis_hash
from wgc.sources.geometry import box_to_pdf, render_size_pixels
from wgc.contracts.source import canonical_bytes

# Literal references observed on original assigned pages. They are retained, not followed.
CITATIONS={
 'p09:435':['4.5'], 'p09:44-item-5':['6.64'], 'p09:44-item-6':['8.64'],
 'p09:452':['7.33'], 'p09:453':['Line Command Eligibility Chart for that battle'],
 'p09:454':['Line Command Eligibility Chart','7.33'],
 'p10:46-body':['4.33'], 'p10:46-exception':['4.74'], 'p10:471':['4.4'],
 'p10:472':['6.0, 8.5, 8.6, etc.','6.27','6.51'], 'p10:473':['Leader Casualty Table','8.19'],
 'p10:475':['4.56'], 'p10:483':['9.16','4.71'], 'p10:484':['9.14'],
 'p11:511-continuation':['5.33'], 'p11:512':['5.26'],
 'p11:513-exceptions':['5.3','5.33','5.5'], 'p11:514-exceptions':['5.33','5.5'],
 'p11:515-bullet-4':['5.26'], 'p11:515-bullet-5':['5.26'], 'p11:515-bullet-6':['6.8'],
 'p11:515-exception':['5.33'], 'p11:521':['4.2','4.3'],
 'p12:522-item-3':['10.16'], 'p12:522-item-4':['10.28'], 'p12:522-item-5':['4.74'],
 'p12:522-item-6':['6.66'], 'p12:522-item-7':['8.64'], 'p12:522-closing':['4.35, 4.52, etc.'],
 'p12:523-item-1':['4.32','9.66'], 'p12:524':['6.11, 6.12'], 'p12:525':['8.4','8.1','8.2'],
 'p12:526-paragraph-1':['4.24, 4.33','7.33','5.15'], 'p12:526-paragraph-2-start':['5.15 #4'],
 'p12:527':['8.4'], 'p12:528-item-1':['5.3'], 'p12:531-bullet-1':['5.26'],
 'p12:531-bullet-2':['5.44'], 'p12:531-bullet-3':['5.15'], 'p12:534':['5.33']
}

PAGE_OBSERVATIONS={
 9:'Left: 4.34, 4.35 and design note; 4.4 heading, commander counter and introduction, six numbered items and historical note. Right: 4.5 two-line heading/introduction, 4.51, 4.52 and exception, 4.53 and play note, 4.54, 4.55, opening 4.56 fragment. Running furniture and copyright retained. No standalone table/legend seen.',
 10:'Left: literal 4.56 sentence continuation and two bullets, 4.6 heading/body/exception/historical digression, 4.7 heading, 4.71 and 4.72. Right: 4.73, 4.74 and design note, 4.75, 4.8 heading/introduction, 4.81-4.84 and design note. Running furniture and copyright retained. No standalone diagram/table/legend seen.',
 11:'Left: 4.85, 4.9 optional heading, Elephant 1 counter, 4.91 introduction/two bullets, 4.92 introduction/three bullets/closing sentence, 4.93, 4.94, 5.0 heading/introduction, red-bordered IMPORTANT note, 5.1 heading and 5.11 start. Right: 5.11 literal column continuation, 5.12, 5.13/exceptions/activation example, 5.14/exceptions, 5.15 introduction/six bullets/closing/exception, 5.2 heading, 5.21/example and 5.22 list introduction. Running furniture and copyright retained. No standalone table seen.',
 12:'Left: seven 5.22 numbered items and closing paragraph, 5.23 introduction/two items/closing sentence, 5.24/example, 5.25, 5.26 first paragraph and second-paragraph start. Right: literal 5.26 column continuation/example, 5.27, 5.28 introduction/two items/closing, 5.3 heading/play note, 5.31 introduction/three bullets, 5.32/example, 5.33 introduction/three result bullets and 5.34. Running furniture and copyright retained. No standalone diagram/table/legend seen.'
}

def verify_pins(records):
    for r in records:
        a=file_pin(ROOT,r['path'])
        assert all(a[k]==v for k,v in r.items() if k in ('path','bytes','sha256')),r['path']

def main():
    # Qualify this attempt's unfrozen native tool reports with observed actor/config.
    # No inventory/schema bytes, old attempt, or previously frozen artifact changes.
    for name in ('final-verified','replay-a-verified','replay-b-verified'):
        path=OUT/name/'coverage.json';native=load(path)
        if 'actor' in native:
            assert all(native[k]==v for k,v in COMMON.items())
        else:
            path.write_bytes(canonical_bytes({**COMMON,**native})+b'\n')
    final=load(OUT/'final-verified/inventory.json');base=load(SCOPE['preservation']['baseline_inventory']['path'])
    pages={p['id']:p for p in final['pages']};assigned={p['id'] for p in final['pages'] if p['pdf_page'] in (9,10,11,12)}
    regions=[r for r in final['regions'] if r['page_id'] in assigned];ids={r['id'] for r in regions}
    evs={e['region_id']:e for e in final['evidence'] if e['region_id'] in ids}
    assert len(regions)==len(evs)
    components=load(OUT/'component-ledger.json');audit=load(OUT/'text-geometry-audit.json')
    for n in (9,10,11,12):
        page=next(p for p in final['pages'] if p['pdf_page']==n)
        expected=render_size_pixels([0,0,1000000,1000000],page,144)
        with Image.open(OUT/'original-pages'/f'page-{n:02}.png') as original:
            assert original.size==expected==(1224,1584)
    entries=[]
    for r in regions:
        p=pages[r['page_id']];ev=evs[r['id']];n=p['pdf_page'];key=r['key'][7:]
        with Image.open(ev['image']['path']) as image:actual=list(image.size)
        expected=list(render_size_pixels(r['box'],p,ev['render_parameters']['dpi']))
        assert actual==expected==[ev['render_parameters']['width_pixels'],ev['render_parameters']['height_pixels']]
        text=Path(ev['text']['path']).read_text(encoding='utf-8')
        assert len(text)==ev['text_codepoints'] and ev['page_basis_hash']==page_basis_hash(p)
        entries.append({'region':r,'pdf_page':n,'page_revision':p['revision'],'page_basis_hash':page_basis_hash(p),'reading_order_index':final['reading_order'].index(r['id']),'page_reading_order_index':[x['id'] for x in regions if x['page_id']==p['id']].index(r['id']),'native_pdf_bounds_rational':[str(v) for v in box_to_pdf(r['box'],p)],'evidence':ev,'predicted_pixels':expected,'actual_png_pixels':actual,'raw_extracted_text':text,'text_status':'Machine extraction only; typography, hyphenation, artwork glyphs and reading order require independent checking. No representation promotion.','boundary_observation':'Compared on original page with complete region overlay. '+({'heading':'Heading and all wrapped heading lines.','clause':'Numbered clause, paragraph, introduction, closing fragment or individual list item as identified by explicit key.','note':'Entire visible note/exception, including visible background/border within its box.','example':'Complete visible source-labelled example.','diagram':'Entire counter, with independently inspected component locators in component-ledger.json.','editorial':'Running title, printed label, separator or copyright; retained in denominator without an exclusion.'}[r['kind']]),'raw_cross_references':CITATIONS.get(key,[]),'cross_reference_policy':'Literal citations only; no referenced source outside pages 9-12 was opened. Exact text above is retained for checking this manual citation list.','components':[c for c in components['components'] if c['parent_region_id']==r['id']]})
    write(OUT/'region-ledger.json',{**COMMON,'format':'wgc-region-ledger-1','assigned_pages':[9,10,11,12],'inventory':file_pin(ROOT,(OUT/'final-verified/inventory.json').as_posix()),'regions':entries,'reading_order':[r['id'] for r in regions],'all_authored_region_boundaries_inspected':True,'standalone_tables_or_legends_observed':[],'semantic_acceptance_granted':False})
    links=[l for l in final['links'] if l['from'] in ids or l['to'] in ids]
    continuation_links=[l for l in links if l['kind']=='continuation']
    write(OUT/'continuations.json',{**COMMON,'links':links,'literal_continuations':continuation_links,'assigned_range_entry':{'physical_page':9,'observation':'Starts with complete numbered 4.34 clause, not an unfinished sentence. Optional accepted page-8 context was not read.','context_id':load(SCOPE['input_pins']['path'])['context_only_ids'][0],'task_denominator_contribution':0},'assigned_range_exit':{'physical_page':12,'observation':'Ends with a complete visible 5.34 sentence. No page 13 access; chapter continuation beyond the assigned range is unresolved.'},'within_page_order':[{'page':n,'observation':'Left column followed by right column. Literal sentence continuation is explicitly linked on pages 11 and 12; page 10 continues the numbered 4.7 subsection sequence across columns.'} for n in (9,10,11,12)],'unfollowed_references':[{'region_id':e['region']['id'],'raw':e['raw_cross_references']} for e in entries if e['raw_cross_references']],'no_access_outside_contract':True,'semantic_acceptance_granted':False})
    full=coverage(final)
    task_counts={level:dict(Counter(r['coverage'][level]['status'] for r in regions if r['denominator_role']=='inventory')) for level in ('transcription','descriptive_semantics','formal_semantics')}
    assert all(not r['coverage'][level]['status'] in ('represented','excluded') for r in regions for level in task_counts)
    write(OUT/'coverage-report.json',{**COMMON,'full_inventory':full,'task':{'physical_pages':[9,10,11,12],'denominator_regions':len(regions),'per_page_region_counts':{str(n):sum(pages[r['page_id']]['pdf_page']==n for r in regions) for n in (9,10,11,12)},'kinds':dict(Counter(r['kind'] for r in regions)),'levels':task_counts,'geometric_gaps':audit['pages']},'context':{'optional_accepted_page8_accessed':False,'optional_page8_task_denominator':0,'component_context_regions':len(components['components']),'component_task_denominator':0,'inherited_full_inventory_context_unchanged':True},'content_gaps':[{'region_id':r['id'],'coverage':r['coverage']} for r in regions],'gap_policy':'All transcription/descriptive/formal representation remains unprocessed. Editorial regions remain inventory, never automatically excluded. Complete visible content accounting and byte locators do not establish semantic coverage.','import_accounting':'44 original physical pages structurally retained; independent source inventory increment only for pages 9-12.','human_semantic_acceptance':'not granted','executable_readiness':'unverified'})
    write(OUT/'visual-review.json',{**COMMON,'role_scope':'Executor original-page inspection only; fresh independent reviewer still required.','pages':[{'pdf_page':n,'original_image':file_pin(ROOT,(OUT/'original-pages'/f'page-{n:02}.png').as_posix()),'boundary_overlay':file_pin(ROOT,(OUT/'original-pages'/f'boundaries-{n:02}.png').as_posix()),'dpi':144,'pixel_dimensions':[1224,1584],'observation':PAGE_OBSERVATIONS[n],'region_ids':[r['id'] for r in regions if pages[r['page_id']]['pdf_page']==n],'comparison':'Full original page, both columns, all proposed rectangles and running furniture inspected; no text character falls outside author boxes in independent geometry audit.'} for n in (9,10,11,12)],'counter_detail_dpi':600,'counter_component_images_inspected':file_pin(ROOT,(OUT/'components/contact-sheet.png').as_posix()),'component_ids':[c['region_id'] for c in components['components']],'uncertainties':['Machine extraction is not a verified transcription.','Elephant counter central artwork is preserved visually without resolving precise art identity.','Counter ratings and symbols are observations only; no gameplay interpretation or legality decision.','Independent original-page and full-ledger review remains pending.'],'semantic_acceptance_granted':False})
    old_pages=[p for p in base['pages'] if p['id'] not in assigned];new_pages=[p for p in final['pages'] if p['id'] not in assigned]
    old_regions=[r for r in base['regions'] if r['page_id'] not in assigned];new_regions=[r for r in final['regions'] if r['page_id'] not in assigned]
    assert old_pages==new_pages and old_regions==new_regions
    assert all(e in final['registry']['entries'] for e in base['registry']['entries'])
    assert final['evidence'][:len(base['evidence'])]==base['evidence']
    assert final['links'][:len(base['links'])]==base['links']
    assert [x for x in final['reading_order'] if x not in ids]==[x for x in base['reading_order'] if x in {r['id'] for r in old_regions}]
    assert final['source']==base['source'] and final['toolchain']==base['toolchain']
    blocked=load(SCOPE['preserve_manifest']['path'])['artifacts'];accepted=load(SCOPE['accepted_dependency']['path'])['artifacts']
    verify_pins(blocked);verify_pins(accepted)
    for ev in base['evidence']:verify_pins([ev[k] for k in ('text','image','crop_pdf')])
    write(OUT/'preservation-report.json',{**COMMON,'baseline':SCOPE['preservation']['baseline_inventory'],'registry':SCOPE['preservation']['registry'],'exact_unassigned_pages':len(old_pages),'exact_unassigned_region_records':len(old_regions),'exact_prior_evidence_records':len(base['evidence']),'exact_prior_link_records':len(base['links']),'persisted_prior_bindings':len(base['registry']['entries']),'retired_placeholder_bindings_retained':[r['id'] for r in base['regions'] if r['page_id'] in assigned],'nonassigned_reading_order_unchanged':True,'old_evidence_artifacts_verified':len(base['evidence'])*3,'blocked_artifact_manifest':SCOPE['preserve_manifest'],'blocked_artifacts_verified':len(blocked),'accepted_dependency_event':SCOPE['accepted_dependency'],'accepted_dependency_artifacts_verified':len(accepted),'all_old_bytes_unchanged':True,'optional_context_record_mutated':False,'semantic_acceptance_granted':False})
    authored=[];verified=[]
    for name in ('authored','replay-a-authored','replay-b-authored'):
        authored.append({'name':name,'inventory':file_pin(ROOT,(OUT/name/'inventory.json').as_posix()),'registry':file_pin(ROOT,(OUT/name/'identity-registry.json').as_posix())})
    for name in ('final-verified','replay-a-verified','replay-b-verified'):
        d=load(OUT/name/'inventory.json');v=load(OUT/name/'validation.json');assert v['exit_code']==0
        assert d['registry']==final['registry']
        assert [{k:v for k,v in r.items()} for r in d['regions']]==final['regions']
        current=[e for e in d['evidence'] if e['region_id'] in ids]
        assert len(current)==len(regions)
        assert all(e[k]['path'].startswith((OUT/name).as_posix()+'/') for e in current for k in ('text','image','crop_pdf'))
        verified.append({'name':name,'inventory':file_pin(ROOT,(OUT/name/'inventory.json').as_posix()),'validation':file_pin(ROOT,(OUT/name/'validation.json').as_posix()),'current_assigned_evidence_count':len(current),'complete_path_dependent_validation_exit_code':0})
    assert len({x['inventory']['sha256'] for x in authored})==1 and len({x['registry']['sha256'] for x in authored})==1
    component_replays=[]
    for name in ('components','components-replay-a','components-replay-b'):
        v=load(OUT/name/'validation.json');assert v['exit_code']==0
        assert (OUT/name/'authored-inventory.json').read_bytes()==(OUT/'components/authored-inventory.json').read_bytes()
        assert (OUT/name/'identity-registry.json').read_bytes()==(OUT/'components/identity-registry.json').read_bytes()
        component_replays.append({'name':name,'authored_inventory':file_pin(ROOT,(OUT/name/'authored-inventory.json').as_posix()),'registry':file_pin(ROOT,(OUT/name/'identity-registry.json').as_posix()),'inventory':file_pin(ROOT,(OUT/name/'inventory.json').as_posix()),'validation':file_pin(ROOT,(OUT/name/'validation.json').as_posix()),'new_component_locators':22})
    write(OUT/'registry-replay-report.json',{**COMMON,'authored_builds':authored,'canonical_authored_inventory_bytes_equal':True,'canonical_registry_bytes_equal':True,'explicit_ids_equal':True,'persisted_registry_seed':SCOPE['drafts'][1],'verified_builds':verified,'independent_complete_replays':2,'component_builds_and_two_replays':component_replays,'path_dependent_final_bytes_equal_claimed':False,'method':'Each author() call independently starts from accepted baseline and exact candidate assigned fields with persisted registry. Each evidence pass reopens original source and regenerates all 135 region text/PNG/crop-PDF artifacts into a distinct absent output directory, then validates that complete path-dependent result. Additional zero-denominator component locators are also completely rebuilt twice with their persisted registry. No prior evidence/green checks are inherited.'})
    pins=load(SCOPE['input_pins']['path']);verify_pins(pins['files']+[pins['dependency_reference']]+pins['context_only_evidence'])
    packet=load(SESSION/'packet.json')
    generated={'docs/STATUS.md','docs/HANDOFF.md','docs/work/tasks/IG-2B03.md'}
    verify_pins([r for r in packet['files']+packet['control_files'] if r['path'] not in generated])
    write(OUT/'source-pins.json',{**COMMON,'input_packet':file_pin(ROOT,(SESSION/'packet.json').as_posix()),'input_pin_manifest':SCOPE['input_pins'],'files':pins['files'],'assigned_pages':[9,10,11,12],'source_page_count':44,'initial_packet_pins_verified_before_claim':True,'workflow_generated_projection_changes':sorted(generated),'projection_change_reason':'The authorized workflow transition ready -> in_progress renders these three generated views; initial hashes were verified before claim. All other packet context/tool pins are reverified at reporting.','source_access':'Original text/images extracted only from physical pages 9-12; all 44 pages accessed structurally for count/geometry only. Nonassigned accepted records and evidence were compared mechanically for preservation; optional page-8 content was not analyzed.','accepted_dependency':SCOPE['accepted_dependency'],'continuation_scope':file_pin(ROOT,'private/workflow/runs/IG-2B03/recovery-20261015-search-01/scope.json'),'blocked_preservation_manifest':SCOPE['preserve_manifest']})
    oldtool=load(SCOPE['toolchain']['path'])
    write(OUT/'toolchain.json',{**oldtool,**COMMON,'inherited_toolchain':SCOPE['toolchain'],'verification':'Executable SHA-256/bytes and actual versions checked at claim time; library versions match. Both pinned PYTHONPATH entries inherited intact; actual pdftoppm resolves to pinned executable. Process-local only.','main_region_dpi':144,'component_dpi':600,'original_page_dpi':144,'original_page_pixels':[1224,1584],'pypdf_warning':'Repeated nonzero-indexed xref warning was observed while reopening original PDF; strict source count/geometry and evidence validation passed. Original PDF bytes preserved.'})
    approved_root='private/workflow/checks/active-3e51455aec7445fc961ad354ee008322'
    result=load(approved_root+'/result.json');assert all(result[k]==0 for k in ('tests_exit','dry_run_exit','plan_exit','diff_exit'))
    checks=[{'command':'.venv/Scripts/python.exe -B -m pytest -q tests/sources --basetemp private/workflow/checks/b03-c99dc525 -p no:cacheprovider --tb=short','exit_code':0,'observed_result':'71 passed in 20.20s','permissions':'require_escalated, approved after restricted-token WinError 5'},
      {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B03','exit_code':0,'observed_result':'184 passed in 32.69s; plan=0 dry-run=0 pytest=0 diff=0','permissions':'require_escalated, approved after restricted-token WinError 5','reports':[file_pin(ROOT,approved_root+'/'+name) for name in ('plan.log','dry-run.log','pytest.log','diff-check.log','result.json')]},
      {'command':'.venv/Scripts/python.exe -B scripts/workflow.py validate','exit_code':0,'observed_result':'Validated 39 tasks, DAG, scope, context and derived views.'},
      {'command':'git diff --check','exit_code':0,'observed_result':'Required command returned zero; restricted token emitted preexisting temp-path access warnings. Approved repository check repeated diff check with exit 0 and no access failures.'}]
    write(OUT/'test-report.json',{**COMMON,'checks':checks,'recovered_environment_failures':[{'command':checks[0]['command'],'exit_code':1,'cause':'PermissionError WinError 5 on pytest mode-0700 basetemp. Exact unchanged approved rerun passed.'},{'command':checks[1]['command'],'exit_code':1,'cause':'plan=0 dry-run=0 pytest=1 diff=0 due to pytest mode-0700 basetemp WinError 5. Exact unchanged approved rerun passed.'}],'tests_tools_contracts_or_acls_changed':False,'no_assertions_disabled':True,'no_packages_installed':True,'semantic_acceptance_granted':False})
    print('all bounded reports written; preservation verified',len(blocked),len(accepted))

if __name__=='__main__':main()
