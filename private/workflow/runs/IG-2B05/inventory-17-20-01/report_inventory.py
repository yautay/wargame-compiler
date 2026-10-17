"""Complete preservation, replay, component, boundary and reference checks.

Reads only the selected task's exact pins, assigned original pages and newly
derived outputs. No history, queue events or prior derivation helpers are used.
"""
from pathlib import Path
from collections import Counter
import copy
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
import pdfplumber
from PIL import Image, ImageDraw, ImageFont
from wgc.sources.inventory import coverage, digest, page_basis_hash, seal, validate
from build_inventory import ROOT,RUN,SESSION,INPUT,read,write,pin,identity,inputs,LINKS

def common(doc):
    return {**identity(),'task':'IG-2B05',
            'final_inventory':pin(RUN+'/final-verified/inventory.json'),
            'final_inventory_revision':doc['revision'],
            'identity_registry':pin(RUN+'/final-verified/identity-registry.json'),
            'source':doc['source'],'assigned_physical_pages':[17,18,19,20],
            'authored_partition':pin(RUN+'/authored-partition.json'),
            'assigned_region_ids':[r['id'] for r in assigned(doc)],
            'assigned_evidence_ids':[e['id'] for e in doc['evidence'] if e['pdf_page'] in (17,18,19,20)]}

def assigned(doc):
    pages={p['id'] for p in doc['pages'] if p['pdf_page'] in (17,18,19,20)}
    return [r for r in doc['regions'] if r['page_id'] in pages]

def preservation(doc,contract,refs,base,old_registry):
    retired=set(contract['target_ids'])
    old={r['id']:r for r in base['regions']};new={r['id']:r for r in doc['regions']}
    assert set(old)-set(new)==retired
    assert all(new[k]==v for k,v in old.items() if k not in retired)
    assert doc['pages']==base['pages'] and doc['source']==base['source']
    assert doc['toolchain']==base['toolchain']
    assert doc['links'][:len(base['links'])]==base['links']
    assert doc['evidence'][:len(base['evidence'])]==base['evidence']
    assert [x for x in doc['reading_order'] if x in old]==[x for x in base['reading_order'] if x not in retired]
    before={(e['kind'],e['key']):e for e in old_registry['entries']}
    after={(e['kind'],e['key']):e for e in doc['registry']['entries']}
    assert all(after[k]==v for k,v in before.items())
    old_evidence=[pin(ev[k]['path']) for ev in base['evidence'] for k in ('crop_pdf','image','text')]
    assert old_evidence==[ev[k] for ev in base['evidence'] for k in ('crop_pdf','image','text')]
    assert len(doc['pages'])==44
    assert read(RUN+'/final-verified/identity-registry.json')==doc['registry']
    return {**common(doc),'format':'wgc-preservation-report-1','passed':True,
            'baseline_inventory':refs['baseline_inventory'],'baseline_registry':refs['identity_registry'],
            'retired_memberships':contract['inventory_batch']['replace_placeholders'],
            'retired_identity_bindings_retained':True,
            'source_pages_equal':44,'nonassigned_and_other_retained_regions_equal':len(old)-4,
            'retained_evidence_records_equal':len(base['evidence']),
            'retained_evidence_artifacts_rehashed':len(old_evidence),
            'retained_evidence_pin_set_hash':digest(old_evidence),
            'retained_links_equal':len(base['links']),
            'original_registry_entries_equal':len(before),
            'nonassigned_reading_order_equal':True,'source_metadata_equal':True,
            'baseline_toolchain_metadata_equal':True,
            'new_regions':len(assigned(doc)),'new_evidence_records':len(doc['evidence'])-len(base['evidence']),
            'scope':'Only the four assigned placeholder memberships are replaced. Original labels, all 44 pages, other regions, evidence, links, registry bindings and reading order are retained.'}

def normalized(doc,name):
    value=copy.deepcopy(doc)
    # These are the only actual path-dependent fields: three artifact paths of
    # each newly derived evidence record, and the enclosing inventory revision.
    for ev in value['evidence']:
        if ev['pdf_page'] in (17,18,19,20):
            for kind in ('crop_pdf','image','text'):
                prefix=f'{RUN}/{name}/'
                assert ev[kind]['path'].startswith(prefix)
                ev[kind]['path']=f'{RUN}/final-verified/'+ev[kind]['path'][len(prefix):]
    return seal(value)

def replays(doc):
    results=[]
    ids={r['id'] for r in assigned(doc)}
    final_ev={e['id']:e for e in doc['evidence'] if e['region_id'] in ids}
    final_normalized=normalized(doc,'final-verified')
    for name in ('replay-1','replay-2'):
        replay=read(f'{RUN}/{name}/inventory.json')
        assert read(f'{RUN}/{name}/identity-registry.json')==doc['registry']==replay['registry']
        ev={e['id']:e for e in replay['evidence'] if e['region_id'] in ids}
        assert set(ev)==set(final_ev)
        assert {e['region_id'] for e in ev.values()}==ids
        comparisons=[]
        for eid,expected in final_ev.items():
            actual=ev[eid]
            for kind in ('crop_pdf','image','text'):
                assert pin(actual[kind]['path'])==actual[kind]
                assert pin(expected[kind]['path'])==expected[kind]
                assert actual[kind]['sha256']==expected[kind]['sha256']
                assert actual[kind]['bytes']==expected[kind]['bytes']
                # Explicit complete byte comparison, in addition to the hashes.
                assert (ROOT/actual[kind]['path']).read_bytes()==(ROOT/expected[kind]['path']).read_bytes()
                comparisons.append({'evidence_id':eid,'kind':kind,'final':expected[kind],'replay':actual[kind],'bytes_equal':True})
        replay_normalized=normalized(replay,name)
        assert replay_normalized==final_normalized
        results.append({'name':name,'inventory':pin(f'{RUN}/{name}/inventory.json'),
                        'registry':pin(f'{RUN}/{name}/identity-registry.json'),
                        'full_logical_sidecar_equal':True,'full_normalized_hash':digest(replay_normalized),
                        'all_region_set_equal':True,'all_region_count':len(replay['regions']),
                        'all_region_set_hash':digest(sorted(r['id'] for r in replay['regions'])),
                        'all_evidence_set_equal':True,'all_evidence_count':len(replay['evidence']),
                        'all_evidence_set_hash':digest(sorted(e['id'] for e in replay['evidence'])),
                        'assigned_region_count':len(ids),'assigned_evidence_count':len(ev),
                        'all_assigned_locators_equal_after_path_normalization':True,
                        'artifact_comparison_count':len(comparisons),'artifact_comparisons':comparisons})
    return {**common(doc),'format':'wgc-complete-replay-report-1','passed':True,
            'build_basis':'Each derivation independently reloads the accepted baseline, authored partition and same persisted registry; no replay copies a final crop or sidecar.',
            'normalization':['Only new crop_pdf.path, image.path and text.path prefixes change to final-verified/; all byte counts and hashes remain exact.','Outer revision is recomputed after path normalization; no other fields are omitted.'],
            'final_normalized_hash':digest(final_normalized),'complete_replays':results}

def source_character_check(authored):
    result=[]
    pdf=read(SESSION+'/task.json')['inventory_batch']['source']['pdf']['path']
    with pdfplumber.open(ROOT/pdf) as source:
        for number in (17,18,19,20):
            rows=[r for r in authored['regions'] if r['page']==number]
            missing=[]; clipped=[]; count=0
            for char in source.pages[number-1].chars:
                if not char['text'].strip():continue
                count+=1
                x=char['x0']+char['x1'];y=char['top']+char['bottom']
                hits=[r for r in rows if r['pixel_box'][0]<=x<r['pixel_box'][2] and r['pixel_box'][1]<=y<r['pixel_box'][3]]
                if len(hits)!=1:missing.append(char['text']);continue
                a,b,c,d=hits[0]['pixel_box']
                if not (a<=char['x0']*2 and b<=char['top']*2 and char['x1']*2<=c and char['bottom']*2<=d):clipped.append(char['text'])
            assert not missing, f'Unassigned or multiply assigned source characters: {number}'
            assert not clipped, f'Clipped source glyph metric bounds: {number}'
            result.append({'pdf_page':number,'non_whitespace_characters':count,'exactly_one_authored_region':True,'fully_contained_glyph_metric_bounds':True,'unassigned':0,'clipped':0})
    return result

def ledger(doc,authored):
    regions={r['key']:r for r in assigned(doc)}
    evidence={ev['region_id']:ev for ev in doc['evidence'] if ev['pdf_page'] in (17,18,19,20)}
    page_map={p['id']:p for p in doc['pages']}
    rows=[];components=[]
    for index,rid in enumerate(doc['reading_order']):
        r=next((v for v in regions.values() if v['id']==rid),None)
        if r is None:continue
        authored_row=next(x for x in authored['regions'] if x['key']==r['key'])
        ev=evidence[rid]
        row={**authored_row,'region_id':rid,'region_revision':r['revision'],'page_id':r['page_id'],
             'box':r['box'],'page_basis_hash':page_basis_hash(page_map[r['page_id']]),
             'global_reading_order_index':index,'evidence':ev,
             'structural_inventory_disposition':'Inventoried from original page and exact current crop; fresh independent review pending.',
             'coverage':r['coverage'],
             'editorial_exclusion':'Not authorized; retained as an explicit editorial region with unprocessed coverage.' if r['kind']=='editorial' else None,
             'component_ids':[]}
        for number,component in enumerate(authored_row['components'],1):
            cid=f'component:p{authored_row["page"]}:{authored_row["key"].split(":")[-1]}:{number}'
            row['component_ids'].append(cid)
            components.append({'id':cid,'description':component,'parent_region_id':rid,
                               'parent_region_revision':r['revision'],'evidence_id':ev['id'],
                               'containing_box':r['box'],'disposition':'Visible component retained in the containing region evidence.',
                               'independent_denominator_units':0,'semantic_acceptance':False})
        rows.append(row)
    assert set(evidence)=={r['region_id'] for r in rows}
    assert len(rows)==len(authored['regions'])==len(regions)
    assert len({c['id'] for c in components})==len(components)
    return {**common(doc),'format':'wgc-region-component-ledger-1',
            'coordinate_convention':'Unrotated effective CropBox top-left page millionths; half-open. Pixel author boundaries quantized identically at shared edges to nearest millionth.',
            'reading_order':'Preserved baseline order, replacing each assigned placeholder with header, left column, right column, footer; diagram components have no inferred gameplay sequence.',
            'region_count':len(rows),'component_count':len(components),
            'all_visible_component_dispositions_present':True,'regions':rows,'components':components,
            'uncertainty':authored['uncertainty'],
            'geometric_gaps':'Blank margins and inter-component spacing remain explicit unrepresented geometry; not counted as represented or authorized exclusions.',
            'context_only_inspections':[]}

def boundary_report(doc):
    ids={(r['key'].split(':')[1],r['key'].split(':')[-1]):r['id'] for r in assigned(doc)}
    def rid(page,key):return ids[(str(page),key)]
    return {**common(doc),'format':'wgc-continuation-boundary-report-1',
            'internal_continuations':[link for link in doc['links'] if link['kind']=='continuation' and link['from'] in set(ids.values())],
            'boundaries':[
                {'boundary':'16-to-17','status':'No sentence continuation asserted','incoming_context':{'dependency':'IG-2B04','section':'boundary','projection':pin(SESSION+'/dependency-view.json'),'observation':'Accepted page-16 exit note ends in a complete sentence.'},'assigned_entrance':rid(17,'6-56'),'observation':'Assigned page 17 begins numbered 6.56; broader 6.5 chapter context remains outside assigned scope.','adjacent_page_inspected':False,'assigned_denominator_contribution':0},
                {'boundary':'17-to-18','status':'resolved structural continuation','from':rid(17,'voluntary-example-start'),'to':rid(18,'voluntary-example-velites'),'observation':'Voluntary stacking example continues in italic paragraphs.'},
                {'boundary':'18-to-19','status':'resolved structural continuation','from':rid(18,'6-73-start'),'to':rid(19,'6-73-end'),'observation':'6.73 continues from opposite to Rear across the physical page boundary.'},
                {'boundary':'19-to-20','status':'No open sentence; chapter transition','exit':rid(19,'pw-play-note-2'),'entrance':rid(20,'7-0-heading'),'observation':'Page 19 final PW note ends with a complete sentence; page 20 starts 7.0.'},
                {'boundary':'20-to-21','status':'unresolved','from':rid(20,'7-24-start'),'target_physical_page':21,'target_region_id':None,'raw_locator':'7.24: all the following apply:','gap':'Conditions continue beyond assigned page 20; page 21 and its content/region identity were not inspected.','adjacent_page_inspected':False,'assigned_denominator_contribution':0}],
            'context_only_inspections':[],'context_only_regions':0,'context_only_denominator':0,
            'meaning_or_executable_dependency_decisions':False}

def reference_index(doc,led):
    canonical={}
    for r in led['regions']:
        match=re.match(r'^(\d+\.\d+)\b',r['title'])
        if match:
            label=match[1]
            if r['key'].split(':')[-1]==label.replace('.','-') or r['key'].split(':')[-1].startswith(label.replace('.','-')+'-'):
                canonical.setdefault(label,[]).append(r)
    refs=[]
    for row in led['regions']:
        ev=row['evidence'];text=(ROOT/ev['text']['path']).read_text(encoding='utf-8')
        for index,match in enumerate(re.finditer(r'\b(?:[4-9]|10)\.\d{1,2}\b',text)):
            candidates=canonical.get(match.group(),[])
            candidate=candidates[0] if candidates else None
            refs.append({'id':f'text-locator:{row["region_id"]}:{index}',
                         'source_region_id':row['region_id'],'source_region_revision':row['region_revision'],
                         'evidence_id':ev['id'],'text':ev['text'],'unicode_codepoint_range':[match.start(),match.end()],
                         'raw_locator':match.group(),'reference_kind':'Textual locator candidate; heading and citation occurrences are not gameplay dependencies.',
                         'target_status':'resolved_current_inventory_navigation' if candidate else 'unresolved',
                         'target_region_id':candidate['region_id'] if candidate else None,
                         'target_region_revision':candidate['region_revision'] if candidate else None,
                         'target_regions':[{'region_id':r['region_id'],'region_revision':r['region_revision']} for r in candidates],
                         'current_report':pin(RUN+'/region-ledger.json') if candidate else None,
                         'gap':None if candidate else 'Referenced target is outside the assigned inspected inventory; no old or adjacent content was loaded.',
                         'semantic_acceptance':False})
    for ref in refs:
        text=(ROOT/ref['text']['path']).read_text(encoding='utf-8')
        a,b=ref['unicode_codepoint_range'];assert text[a:b]==ref['raw_locator']
        if ref['target_region_id']:
            assert any(r['region_id']==ref['target_region_id'] and r['region_revision']==ref['target_region_revision'] for r in led['regions'])
            assert pin(ref['current_report']['path'])==ref['current_report']
            for target in ref['target_regions']:
                assert any(r['region_id']==target['region_id'] and r['region_revision']==target['region_revision'] for r in led['regions'])
    return {**common(doc),'format':'wgc-current-source-reference-index-1',
            'reports':{name:pin(RUN+'/'+name) for name in ('region-ledger.json','continuations.json','coverage-report.json','source-pins.json','toolchain.json','original-page-inspection.json','preservation-report.json','replay-report.json')},
            'records':refs,'all_current_paths_hashes_and_region_revisions_verified':True,
            'uninspected_targets_remain_unresolved':True,'scope':'Exact extracted numeric locator occurrences; semantic cross-reference reconciliation is a later gate.'}

def mosaics(doc):
    rows=[r for n in (17,18,19,20) for r in read(RUN+'/authored-partition.json')['regions'] if r['page']==n]
    evs={e['region_id']:e for e in doc['evidence']}
    region_map={r['key']:r for r in assigned(doc)}
    sheets=[]; placements=[];canvas=Image.new('RGB',(1100,1900),'#edf0f2');ys=[10,10];number=1
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
    def flush():
        nonlocal canvas,ys,number,placements
        if not placements:return
        rel=f'{RUN}/visual-audit/sheet-{number:02d}.png'
        (ROOT/rel).parent.mkdir(parents=True,exist_ok=True)
        canvas.crop((0,0,1100,max(ys)+10)).save(ROOT/rel)
        sheets.append({'image':pin(rel),'placements':placements})
        canvas=Image.new('RGB',(1100,1900),'#edf0f2');ys=[10,10];number+=1;placements=[]
    for index,row in enumerate(rows,1):
        region=region_map[row['key']];ev=evs[region['id']]
        with Image.open(ROOT/ev['image']['path']) as original:
            crop=original.convert('RGB')
        if crop.width>530:
            crop.thumbnail((530,1800)) # Only the running header needs reduction.
        col=0 if ys[0]<=ys[1] else 1
        if ys[col]+crop.height+43>1900:
            flush();col=0
        x=10+col*550;y=ys[col]
        draw=ImageDraw.Draw(canvas)
        draw.text((x,y),f'{index:03d} p{row["page"]} {row["key"].split(":")[-1]}',fill='black',font=font)
        canvas.paste(crop,(x,y+24));ys[col]=y+crop.height+43
        placements.append({'index':index,'region_id':region['id'],'evidence_image':ev['image'],'sheet_box':[x,y+24,x+crop.width,y+24+crop.height]})
    flush()
    write(RUN+'/visual-audit/index.json',{'format':'wgc-crop-contact-index-1',**common(doc),'sheets':sheets,'region_count':len(rows),'all_regions_present':True})
    print(json.dumps({'contact_sheets':len(sheets),'regions':len(rows)}))

def reports():
    contract,refs,base,old_registry=inputs();doc=read(RUN+'/final-verified/inventory.json')
    authored=read(RUN+'/authored-partition.json');led=ledger(doc,authored)
    write(RUN+'/preservation-report.json',preservation(doc,contract,refs,base,old_registry))
    write(RUN+'/replay-report.json',replays(doc))
    write(RUN+'/region-ledger.json',led)
    write(RUN+'/continuations.json',boundary_report(doc))
    cov=coverage(doc)
    own=assigned(doc)
    own_levels={level:dict(Counter(r['coverage'][level]['status'] for r in own)) for level in ('transcription','descriptive_semantics','formal_semantics')}
    write(RUN+'/coverage-report.json',{**common(doc),'format':'wgc-separated-coverage-report-1',
        'full_44_page_inventory':cov,
        'assigned_inventory':{'physical_pages':4,'region_denominator':len(own),'regions_by_page':dict(Counter(str(next(p['pdf_page'] for p in doc['pages'] if p['id']==r['page_id'])) for r in own)),
                              'levels':own_levels,'structurally_inventoried_regions':len(own),'represented_by_inventory_presence':False},
        'context_only':{'new_regions':0,'new_inspected_pages':0,'inventory_denominator':0,'assigned_denominator':0,'accepted_incoming_boundary_observations':1},
        'retained_nonassigned_placeholders':[{'id':r['id'],'key':r['key'],'coverage':r['coverage']} for r in doc['regions'] if r['key'].endswith(':unprocessed-placeholder')],
        'executable_readiness':False,'human_semantic_acceptance':False,'fresh_independent_review':'pending',
        'note':'Structural inventory, character accounting, transcription, descriptive semantics, formal semantics and executable readiness remain separate. No geometric gap or excluded/unprocessed area is represented.'})
    write(RUN+'/source-pins.json',{**common(doc),'format':'wgc-current-source-pins-1',
        'input_reference':pin(INPUT),'baseline_report_pins':refs['reports'],
        'final_pages':[p for p in doc['pages'] if p['pdf_page'] in (17,18,19,20)],
        'evidence':[{**e,'all_artifacts_rehashed':all(pin(e[k]['path'])==e[k] for k in ('crop_pdf','image','text'))} for e in doc['evidence'] if e['pdf_page'] in (17,18,19,20)],
        'source_structure_access':'All 44 pages checked geometrically; content inspection only on physical pages 17-20.'})
    tool=read(INPUT)['toolchain']
    actual={name:importlib.metadata.version(name) for name in tool['libraries']}
    assert actual==tool['libraries']
    assert os.environ['PYTHONPATH']==tool['process_pythonpath']
    assert tool['process_path_prefix'] in os.environ['PATH'].split(';')
    executable_sha=hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest()
    assert executable_sha==tool['python_executable']['sha256']
    native={}
    for name,args in [('pdfinfo',['pdfinfo','-v']),('pdftoppm',['pdftoppm','-v']),
                      ('git',['git','--version']),('pwsh',['pwsh','--version'])]:
        observed=subprocess.run(args,capture_output=True,text=True,check=True)
        native[name]={'version':(observed.stdout+observed.stderr).strip()}
        assert native[name]==tool['native'][name]
    packet=read(SESSION+'/packet.json')
    write(RUN+'/toolchain.json',{**common(doc),'format':'wgc-observed-task-toolchain-1',
        'pinned_dependency_toolchain':refs['reports']['toolchain.json'],
        'process_pythonpath':os.environ['PYTHONPATH'],'process_path_prefix':tool['process_path_prefix'],
        'libraries':actual,'python_executable':tool['python_executable'],'native':native,
        'current_control_files':[pin(item['path']) for item in packet['control_files']],
        'render_settings':{'dpi':144,'format':'png','cropbox':True,'text_encoding':'UTF-8'},
        'global_configuration_changed':False,'dependencies_installed':False})
    chars=source_character_check(authored)
    write(RUN+'/original-page-inspection.json',{**common(doc),'format':'wgc-original-page-inspection-1',
        'inspection_actor':identity()['actor'],'basis':'Fresh visual inspection of all four complete original-page renders before authoring the partition; no coordinator observations substitute for this inspection.',
        'pages':[{'pdf_page':n,'image':pin(f'{RUN}/original-pages/page-{n}.png'),'text_helper':pin(f'{RUN}/original-pages/page-{n}.txt'),
                  'full_page_inspected':True,'all_columns_and_editorial_areas_inspected':True,
                  'components_reconciled_in':pin(RUN+'/region-ledger.json'),
                  'printed_label':'Glyph visible; baseline label status retained. Glyph presence alone is not label verification.'} for n in (17,18,19,20)],
        'character_accounting':chars,'context_only_accesses':[],
        'fresh_independent_source_page_review':'pending; executor inspection is not independent review',
        'human_semantic_acceptance':False,'gameplay_readiness':False})
    write(RUN+'/source-reference-index.json',reference_index(doc,led))
    print(json.dumps({'preservation':'passed','complete_replays':2,'regions':len(own),'components':len(led['components']),'full_regions':len(doc['regions']),'full_evidence':len(doc['evidence'])}))

if __name__=='__main__':
    if sys.argv[1]=='mosaics':mosaics(read(RUN+'/final-verified/inventory.json'))
    elif sys.argv[1]=='reports':reports()
    else:raise ValueError('Unknown bounded report operation')
