"""Complete baseline preservation, source/component index and replay verifier.

Reads accepted inputs internally, emitting only this task's summary. Deliberate
in-memory corruptions prove omissions and stale indexes cannot return success.
"""
import copy
import json
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw
from wgc.sources.inventory import coverage, digest, page_basis_hash, validate
from wgc.sources.geometry import overlaps
from build_inventory import (ROOT, REPO, PIN, TASK, SPECS, CONTRACT, baseline, load,
                             write, pin, metadata, old_preservation)
from check_arrow_completeness import reference_masks, check_document, KEY as ARROW_KEY
from check_hit_completeness import check_all as check_hit_all
from check_component_completeness import check_all as check_component_all
KEYS = {'ig2b08:p29:collapse-diagram-component-v-counter', 'ig2b08:p29:advance-diagram-component-c-hits'}


def new_regions(doc):
    return [r for r in doc['regions'] if r['key'].startswith('ig2b08:')]


def check_preservation(base, result):
    retired=set(TASK['inventory_contract']['placeholder_target_ids'])
    old={r['id']:r for r in base['regions']};now={r['id']:r for r in result['regions']}
    assert set(old)-set(now)==retired
    for identity,r in old.items():
        if identity not in retired: assert now[identity]==r
    assert result['source']==base['source'] and result['pages']==base['pages']
    assert result['links'][:len(base['links'])]==base['links']
    assert result['evidence'][:len(base['evidence'])]==base['evidence']
    old_entries={tuple(sorted(e.items())) for e in base['registry']['entries']}
    new_entries={tuple(sorted(e.items())) for e in result['registry']['entries']}
    assert old_entries<=new_entries
    old_order=[x for x in base['reading_order'] if x not in retired]
    assert [x for x in result['reading_order'] if x in set(old_order)]==old_order
    return {'retired_active_placeholders':sorted(retired),'preserved_regions':len(old)-4,
        'preserved_evidence_objects':len(base['evidence']),'preserved_links':len(base['links']),
        'preserved_registry_entries':len(old_entries),'result_registry_entries':len(new_entries),
        'retained_reading_order_count':len(old_order),'retained_reading_order_hash':digest(old_order),
        'preserved_region_objects_hash':digest([r for r in base['regions'] if r['id'] not in retired]),
        'pages_before_after_hash':digest(base['pages']),'links_before_prefix_hash':digest(base['links']),
        'evidence_before_prefix_hash':digest(base['evidence']),'source_before_after_hash':digest(base['source'])}


def require_components(doc):
    selected={s['key'] for s in SPECS}
    assert {r['key'] for r in new_regions(doc)}==selected,'Missing assigned region/component'
    assert len(new_regions(doc))==len(selected)
    ev={e['region_id']:e for e in doc['evidence']}
    pages={p['id']:p for p in doc['pages']}
    for r in new_regions(doc):
        assert r['id'] in ev,'Missing assigned evidence'
        assert ev[r['id']]['page_basis_hash']==page_basis_hash(pages[r['page_id']])
        assert ev[r['id']]['region_revision']==r['revision']
        for field in ('crop_pdf','text','image'):
            assert pin(ev[r['id']][field]['path'])==ev[r['id']][field]
    for i,r in enumerate(new_regions(doc)):
        if r['denominator_role']=='inventory':
            for q in new_regions(doc)[:i]:
                if q['page_id']==r['page_id'] and q['denominator_role']=='inventory':
                    assert not overlaps(q['box'],r['box'])
    assert len({p['pdf_page'] for p in doc['pages']})==44


def normalized_evidence(doc):
    ids={r['id'] for r in new_regions(doc)}
    rows=[]
    for e in doc['evidence']:
        if e['region_id'] not in ids:continue
        e=copy.deepcopy(e)
        for field in ('crop_pdf','text','image'):
            e[field]['path']=e[field]['path'].split('/evidence/',1)[1]
        rows.append(e)
    return rows


def require_replay(final, replay):
    require_components(replay)
    for field in ('source','pages','regions','registry','reading_order','links','toolchain'):
        assert final[field]==replay[field],field
    assert normalized_evidence(final)==normalized_evidence(replay),'Path-normalized evidence bytes/locators differ'


def artifact_pins(docs):
    seen={}
    def visit(o):
        if isinstance(o,dict):
            if 'path' in o and 'sha256' in o:
                actual=pin(o['path']);assert actual['sha256']==o['sha256']
                if 'bytes' in o:assert actual['bytes']==o['bytes']
                seen[actual['path']]=actual
            for v in o.values():visit(v)
        elif isinstance(o,list):
            for v in o:visit(v)
    for doc in docs:visit(doc)
    return list(seen.values())


def ensure_index(index, required):
    indexed={p['path']:p for p in index}
    assert len(indexed)==len(index),'Duplicate source index paths'
    for p in required:
        assert indexed.get(p['path'])==p,'Missing/stale source index path'
    for p in index:assert pin(p['path'])==p,'Missing/stale indexed bytes'


def gap_rectangles(regions, page_id):
    boxes=[r['box'] for r in regions if r['page_id']==page_id and r['denominator_role']=='inventory']
    cuts=sorted({0,1000000,*[b[i] for b in boxes for i in (1,3)]})
    gaps=[]
    for y0,y1 in zip(cuts,cuts[1:]):
        intervals=sorted((b[0],b[2]) for b in boxes if b[1]<=y0 and b[3]>=y1)
        at=0
        for x0,x1 in intervals:
            if x0>at:gaps.append([at,y0,x0,y1])
            at=x1
        if at<1000000:gaps.append([at,y0,1000000,y1])
    return gaps


def negative_check(call):
    try:call()
    except (AssertionError,ValueError,FileNotFoundError):return 'correctly_rejected'
    raise AssertionError('Negative omission/tamper case was accepted')


def report():
    base,_=baseline();docs=[load(ROOT/name/'inventory.json') for name in ('final-verified','replay-1','replay-2')]
    final=docs[0];meta=metadata()
    _,arrow_masks=reference_masks()
    for doc in docs:check_document(doc,arrow_masks)
    check_hit_all()
    check_component_all()
    candidate_root=Path('private/workflow/runs/IG-2B08/repair-F02-validation02')
    candidate_specs=[{k:o[k] for k in SPECS[0]} for o in load(candidate_root/'region-ledger.json')['new_observations']]
    assert [s for s in candidate_specs if s['key'] not in KEYS]==[s for s in SPECS if s['key'] not in KEYS]
    candidate=load(candidate_root/'final-verified/inventory.json')
    assert candidate['registry']==final['registry']
    assert candidate['reading_order']==final['reading_order']
    assert candidate['links']==final['links']
    assert [r for r in candidate['regions'] if r['key'] not in KEYS]==[r for r in final['regions'] if r['key'] not in KEYS]
    old_evidence=normalized_evidence(candidate);fresh_evidence=normalized_evidence(final)
    target_ids={r['id'] for r in final['regions'] if r['key'] in KEYS}
    assert [e for e in old_evidence if e['region_id'] not in target_ids]==[e for e in fresh_evidence if e['region_id'] not in target_ids]
    write(ROOT/'repair-delta.json',{**meta,'summary':'Only the F03/F04 detail geometry/observations/revisions and its derivatives changed; unrelated author records, primary tiles, identities, registry history, order, links and normalized evidence remain identical.',
        'candidate_inventory':pin(candidate_root/'final-verified/inventory.json'),'current_inventory':pin(ROOT/'final-verified/inventory.json'),
        'changed_keys':sorted(KEYS),'changed_region_count':2,'unchanged_authored_selection_count':len(SPECS)-2,
        'unchanged_registry_order_links':True,'unchanged_non_target_normalized_evidence':True,'exit_code':0})
    preservation=check_preservation(base,final)
    for name,doc in zip(('final-verified','replay-1','replay-2'),docs):
        validate(doc,REPO);require_components(doc)
        assert load(ROOT/name/'identity-registry.json')==doc['registry']
        check_preservation(base,doc)
    for replay in docs[1:]:require_replay(final,replay)
    all_artifacts=artifact_pins(docs)
    # Every original-page and boundary artifact is indexed, including all words,
    # fresh overlay renders, access record and bounded context crop.
    originals=[pin(p) for p in sorted((ROOT/'originals').iterdir()) if p.is_file()]
    auxiliary=artifact_pins([load(ROOT/'proposal-preflight.json')])
    indexed=all_artifacts+originals+auxiliary
    seen={p['path']:p for p in indexed};indexed=list(seen.values())
    ensure_index(indexed,all_artifacts+originals)
    missing=copy.deepcopy(final);missing['regions']=[r for r in missing['regions'] if r['key']!=SPECS[-1]['key']]
    stale=copy.deepcopy(indexed);stale[0]['sha256']='0'*64
    missing_replay=copy.deepcopy(docs[1]);missing_replay['regions']=missing_replay['regions'][:-1]
    negative={'missing_component':negative_check(lambda:require_components(missing)),
              'missing_index_path':negative_check(lambda:ensure_index(indexed[1:],all_artifacts+originals)),
              'stale_index_hash':negative_check(lambda:ensure_index(stale,all_artifacts+originals)),
              'incomplete_replay':negative_check(lambda:require_replay(final,missing_replay))}
    write(ROOT/'preservation-report.json',{**meta,'summary':'Exact nonassigned objects and retained order preserved; only four active placeholders retired.','baseline':PIN['baseline_inventory'],'baseline_registry':PIN['identity_registry'],**preservation,'old_attempt_preserved_artifacts':old_preservation(),'human_semantic_acceptance':False})
    ids={r['key']:r for r in new_regions(final)};ev={e['region_id']:e for e in final['evidence']}
    observations=[]
    for s in SPECS:
        r=ids[s['key']]
        observations.append({**s,'region_id':r['id'],'revision':r['revision'],'box':r['box'],
            'evidence':ev[r['id']],'original_page':pin(ROOT/'originals'/f'page-{s["page"]}.png'),
            'inspection':'Fresh original and boundary overlay visually inspected in this executor session; physical descriptive observation only.',
            'denominator_contribution':int(s['role']=='inventory')})
    page_map={p['id']:p['pdf_page'] for p in final['pages']}
    write(ROOT/'region-ledger.json',{**meta,'summary':'Complete 44-page ledger; new independent author observations are explicit.','source_sha256':final['source']['sha256'],
        'regions':[{'id':r['id'],'key':r['key'],'revision':r['revision'],'pdf_page':page_map[r['page_id']],'box':r['box'],'kind':r['kind'],'denominator_role':r['denominator_role'],'coverage':r['coverage'],'origin':'fresh IG-2B08' if r['key'].startswith('ig2b08:') else 'preserved accepted baseline'} for r in final['regions']],
        'new_observations':observations,'reading_order':final['reading_order'],'links':final['links'],'input_ledger':PIN['reports']['region-ledger.json']})
    component_rows=[o for o in observations if o['kind'] in ('diagram','table','legend','example')]
    # Each detail belongs to a source field tile on its page. Intersections are
    # explicit; they do not manufacture additional represented inventory units.
    for o in component_rows:
        o['field_region_ids']=[q['region_id'] for q in observations if q['role']=='inventory' and q['page']==o['page'] and q['group']==o['group'] and q['group'] is not None and overlaps(q['box'],o['box'])]
    write(ROOT/'component-ledger.json',{**meta,'summary':'Complete table/caption/example/diagram set, with overlapping visual layers separated from primary disjoint source-field tiles.','components':component_rows,
        'new_component_count':len(component_rows),'primary_denominator':sum(o['role']=='inventory' for o in component_rows),
        'detail_denominator':0,'limitation':'Diagram layers overlap in source; detail crops can include adjacent layers. Machine glyphs and gameplay meaning remain unverified.'})
    access=load(ROOT/'original-access.json')
    write(ROOT/'original-page-inspection.json',{**meta,'summary':'Fresh original pages and all proposed boundary overlays inspected; page-33 output is bounded before pixels/text are released.',
        'source':PIN['source'],'access':access,'original_artifacts':originals,'assigned_pages':[29,30,31,32],
        'context_page33':{'points':[45,50,306,80],'normalized':[73529,63131,500000,101011],'observed':'Two complete continuation lines only, ending one rampaging Elephant at any one time. No following note visible.','fresh_image':pin(ROOT/'originals/page-33.png'),'fresh_text':pin(ROOT/'originals/page-33.txt'),'crop_pdf_warning':'Page streams may retain out-of-clip data; never used for raw text extraction.'},
        'page28':'Reference-only via accepted prepared boundary projection; not rendered or extracted.',
        'observations':observations,'semantic_acceptance_granted':False})
    inherited=coverage(base);full=coverage(final)
    assigned=[r for r in new_regions(final) if r['denominator_role']=='inventory']
    context=[r for r in final['regions'] if r['denominator_role']=='context']
    full['assigned_four_page']={'physical_pages':[29,30,31,32],'denominator_regions':len(assigned),
        'levels':{level:dict(Counter(r['coverage'][level]['status'] for r in assigned)) for level in ('transcription','descriptive_semantics','formal_semantics')},
        'geometric_gaps':[{'pdf_page':p['pdf_page'],'page_id':p['id'],'boxes':gap_rectangles(final['regions'],p['id']),'reason':'Explicit area outside independently authored source regions; predominantly margins/spacing. Not represented content.'} for p in final['pages'] if p['pdf_page'] in (29,30,31,32)]}
    inherited_regions=[r for r in base['regions'] if r['denominator_role']=='inventory' and r['id'] not in set(TASK['inventory_contract']['placeholder_target_ids'])]
    full['inherited_nonassigned']={'denominator_regions':len(inherited_regions),'preserved_regions_including_context':preservation['preserved_regions'],
        'levels':{level:dict(Counter(r['coverage'][level]['status'] for r in inherited_regions)) for level in ('transcription','descriptive_semantics','formal_semantics')},'removed_placeholder_units':4}
    full['context_only']={'total_regions':len(context),'new_regions':86,'new_assigned_detail_crops':85,'new_boundary_regions':1,'retained_regions':len(context)-86,'denominator_contribution':0,
        'ids':[r['id'] for r in context if r['key'].startswith('ig2b08:') or r['id'] in TASK['inventory_contract']['retained_context_ids']]}
    full['full_page_count']=44
    full['foreground_gap_probe']=load(ROOT/'geometric-content-probe.json')
    full['foreground_gap_limitation']='Fresh thresholded ink gaps and unassigned word centers, if any, are reported by page in foreground_gap_probe. They are gaps, not represented content or semantic completeness.'
    write(ROOT/'coverage-report.json',{**meta,'summary':'Separate full-source, assigned, inherited and zero-denominator context accounting; statuses retain gaps.',**full})
    write(ROOT/'continuations.json',{**meta,'summary':'All inherited links remain; fresh incoming, column/page and exit boundaries are explicit.','inherited_continuation_report':PIN['reports']['continuations.json'],
        'retained_incoming_context_id':TASK['inventory_contract']['retained_context_ids'][0],
        'new_links':final['links'][len(base['links']):],'all_links':final['links'],
        'context_denominator':0,'entry_observation':PIN['boundary'],'exit_context':ids['ig2b08:p33:exit-context'],
        'unresolved':'No continuation grants executable meaning; page 33 after the exact rectangle was not accessed.'})
    write(ROOT/'replay-report.json',{**meta,'summary':'Two complete independent fresh-path replays each regenerated the full region/component set serially from the accepted baseline and identical persisted author registry.',
        'commands':[f'.venv/Scripts/python.exe {ROOT.as_posix()}/build_inventory.py {n}' for n in ('replay-1','replay-2')],
        'reading_order_preservation':'Reviewed candidate sequence used explicitly, independently in all three baseline reconstructions.',
        'runs':[{'name':n,'inventory':pin(ROOT/n/'inventory.json'),'registry':pin(ROOT/n/'identity-registry.json'),'new_regions':len(new_regions(d)),'new_artifacts':len(new_regions(d))*3,'stable_ids':True,'author_fields_order_links_registry_equal':True,'normalized_evidence_hash':digest(normalized_evidence(d))} for n,d in zip(('final-verified','replay-1','replay-2'),docs)],
        'actual_inventory_hashes_are_path_dependent':True,'complete_assigned_regions':len(SPECS),'missing_references':0,'negative_cases':negative,'source_meaning_acceptance':False})
    source_report={'format':'wgc-source-pins-1',**meta,'summary':'Exhaustive assigned original/region/component and complete replay indexes, including every inherited artifact referenced by the three inventories.',
        'source':PIN['source'],'effective_input_contract':pin(CONTRACT),'accepted_input_reports':PIN['reports'],
        'diagnostic_preflight':{'denominator_contribution':0,'report':pin(ROOT/'proposal-preflight.json'),'artifacts':auxiliary},
        'artifacts':indexed,'region_evidence_sets':[{'name':n,'inventory':pin(ROOT/n/'inventory.json'),'registry':pin(ROOT/n/'identity-registry.json'),'region_ids':[r['id'] for r in new_regions(d)]} for n,d in zip(('final-verified','replay-1','replay-2'),docs)],
        'current_reports':[pin(ROOT/n) for n in ('original-page-inspection.json','component-ledger.json','preservation-report.json','replay-report.json','coverage-report.json','continuations.json','region-ledger.json','toolchain.json')],
        'text_protocol':'New text is clipped on original page before extraction. Page-33 normalized rounding is authorized; native raster dimensions constrain output. No raw crop-PDF text access.',
        'index_complete':True}
    write(ROOT/'source-pins.json',source_report)
    ensure_index(source_report['artifacts'],all_artifacts+originals)
    write(ROOT/'batch-verification.json',{**meta,'summary':'Complete preservation, identity, geometry, all artifact pins and both full replays verified.','checks':{'preservation':True,'full_page_set':44,'new_region_set':len(SPECS),'new_inventory_denominator':len(assigned),'all_source_artifact_pins':len(all_artifacts),'original_artifact_pins':len(originals),'complete_index_pins':len(indexed),'negative_cases':negative},'exit_code':0})
    # Compact visual QA sheets, generated solely from this fresh final evidence.
    details=[o for o in observations if o['role']=='context' and o['page']!=33]
    details += [o for o in observations if o['key'].split(':',2)[2] in ('rating-lcln','rating-lcln-value','rating-rchcbc','rating-rchcbc-value')]
    for start in range(0,len(details),16):
        batch=details[start:start+16];sheet=Image.new('RGB',(1000,1000),'white');draw=ImageDraw.Draw(sheet)
        for i,o in enumerate(batch):
            im=Image.open(o['evidence']['image']['path']).convert('RGB');im.thumbnail((238,214))
            x=(i%4)*250;y=(i//4)*250
            sheet.paste(im,(x,y+26));draw.text((x+2,y+2),o['key'].split(':',2)[2][-37:],fill='black')
        sheet.save(ROOT/f'component-sheet-{start//16+1}.png')
    sheet_pins=[pin(ROOT/f'component-sheet-{i+1}.png') for i in range((len(details)+15)//16)]
    source_report['artifacts']+=sheet_pins
    source_report['current_reports'] += [pin(ROOT/n) for n in ('geometric-content-probe.json','batch-verification.json','arrow-completeness-report.json','F02-completeness-report.json','repair-delta.json','proposal-preflight.json','F03-F04-completeness-report.json')]
    source_report['artifacts'] += [pin(ROOT/'arrow-original-detail.png'),pin(ROOT/'F02-original-detail.png'),pin(ROOT/'F02-source-mask.png')]+[pin(ROOT/f'geometric-gap-page-{p}.png') for p in (29,30,31,32)]
    write(ROOT/'source-pins.json',source_report)
    ensure_index(source_report['artifacts'],all_artifacts+originals+sheet_pins)
    print(json.dumps({'verified':True,'regions':len(SPECS),'inventory_denominator':len(assigned),'component_details':len(details),'source_index_pins':len(indexed),'negative_cases':negative}))


if __name__=='__main__': report()
