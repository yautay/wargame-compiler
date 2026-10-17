"""Complete set, byte replay, preservation, and source-reference accounting."""
import copy
from collections import Counter
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from wgc.sources.inventory import coverage, digest, file_pin, page_basis_hash, validate

ROOT = Path.cwd()
BASE = Path(__file__).resolve().parent
REL = BASE.relative_to(ROOT).as_posix()
SESSION = 'private/workflow/orchestrator/20261016T154824Z-fae43db9/001-IG-2B05-executor-008601fd'

def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def pin(path):
    return file_pin(ROOT,path)

def write(name,value):
    (BASE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def common():
    claim=load(REL+'/claim.json')
    return {k:claim[k] for k in ('task','actor','role','model','reasoning','configuration_evidence','configuration_sha256')}

def normalized(doc,prefix):
    # Only derived evidence artifact paths differ. Hashes, bytes, locators, IDs,
    # labels, source metadata, all records and registry remain in the comparison.
    d=copy.deepcopy(doc)
    d.pop('revision')
    changed=[]
    for e in d['evidence']:
        for field in ('crop_pdf','text','image'):
            path=e[field]['path']
            if path.startswith(prefix+'/'):
                e[field]['path']='<DERIVATION>/'+path[len(prefix)+1:]
                changed.append({'evidence_id':e['id'],'field':field+'.path'})
    return d,changed

def reports():
    final=load(REL+'/final-verified/inventory.json')
    registry=load(REL+'/final-verified/identity-registry.json')
    part=load(REL+'/authored-partition.json')
    old=load('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/inventory.json')
    oldreg=load('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/identity-registry.json')
    assert pin('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/inventory.json')['sha256']=='5ac48725279f2a44d77bdbc6a14ca8bb6c828ee709b5f143b117700bb4c5f656'
    assert pin('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/identity-registry.json')['sha256']=='50f254c8f3ceb8cc0feb688ea8b31f5a39b4bb6c76fbcd89fa2d45d87d245375'
    task=load(SESSION+'/task.json')
    pageids={p['id'] for p in final['pages'] if p['pdf_page'] in (17,18,19,20)}
    new=[r for r in final['regions'] if r['page_id'] in pageids]
    newids={r['id'] for r in new}
    ev={e['region_id']:e for e in final['evidence'] if e['region_id'] in newids}
    bykey={r['key']:r for r in new}
    assert len(new)==len(newids)==len(ev)==len(part['regions'])==102
    assert set(bykey)=={i['key'] for i in part['regions']}
    assert all(r['denominator_role']=='inventory' for r in new)
    pins={'inventory':pin(REL+'/final-verified/inventory.json'),'inventory_revision':final['revision'],
          'registry':pin(REL+'/final-verified/identity-registry.json'),'source':final['source'],
          'assigned_physical_pages':[17,18,19,20],'assigned_ids':[r['id'] for r in new]}
    envelope={**common(),**pins,'assigned_evidence':[{
        'region_id':e['region_id'],'evidence_id':e['id'],'page_basis_hash':e['page_basis_hash'],
        'crop_pdf':e['crop_pdf'],'image':e['image'],'text':e['text']} for e in ev.values()],
        'human_semantic_acceptance':False,'gameplay_readiness':False}
    crop_review=load(REL+'/crop-review.json')
    for sheet in crop_review['sheets']:
        for key,image_pin in zip(sheet['region_keys'],sheet['reviewed_images']):
            final_image=ev[bykey[key]['id']]['image']
            assert image_pin['sha256']==final_image['sha256'] and image_pin['bytes']==final_image['bytes']
            assert (ROOT/image_pin['path']).read_bytes()==(ROOT/final_image['path']).read_bytes()
    crop_review.update(envelope)
    crop_review['all_reviewed_image_bytes_equal_final']=True
    crop_review['followup_requirement']=None
    write('crop-review.json',crop_review)
    untouched_old=[r for r in old['regions'] if r['page_id'] not in pageids]
    untouched_new=[r for r in final['regions'] if r['page_id'] not in pageids]
    retired=set(task['target_ids'])
    checks={
        'all_44_pages_equal':len(final['pages'])==44 and old['pages']==final['pages'],
        'source_equal':old['source']==final['source'],
        'nonassigned_regions_equal':untouched_old==untouched_new,
        'retained_evidence_prefix_equal':final['evidence'][:len(old['evidence'])]==old['evidence'],
        'retained_links_prefix_equal':final['links'][:len(old['links'])]==old['links'],
        'all_original_registry_entries_retained':all(e in registry['entries'] for e in oldreg['entries']),
        'registry_matches_persisted':registry==load(REL+'/persisted-registry.json')==final['registry'],
        'exactly_four_placeholders_removed':set(r['id'] for r in old['regions'])-set(r['id'] for r in final['regions'])==retired,
        'all_nonassigned_reading_order_unchanged':[x for x in old['reading_order'] if x not in retired]==[x for x in final['reading_order'] if x not in newids],
        'retired_identity_bindings_retained':all(any(e['id']==identity for e in registry['entries']) for identity in retired),
        'nonassigned_evidence_unchanged':[e for e in final['evidence'] if e['region_id'] not in newids]==old['evidence'],
    }
    # All retained evidence byte pins and full source geometry are checked again here.
    structural=validate(final,ROOT)
    assert all(checks.values()),checks
    scope=load(task['continuation_authorization']['scope']['path'])
    blocked=load(scope['preserve_manifest']['path'])
    for a in blocked['artifacts']:
        assert pin(a['path'])['sha256']==a['sha256'],a['path']
    write('preservation-report.json',{**envelope,'checks':checks,'retained_pages':44,
          'retained_region_count':len(untouched_old),'retained_evidence_count':len(old['evidence']),
          'retained_links_count':len(old['links']),'retained_registry_entries':len(oldreg['entries']),
          'retired_memberships':sorted(retired),'retained_artifact_byte_checks':len(old['evidence'])*3,
          'blocked_attempt':{'manifest':scope['preserve_manifest'],'verified_files':len(blocked['artifacts']),'mismatches':[]},
          'full_source_geometry_and_evidence_validation':'passed'})
    rows=[]
    component_ids=[]
    for i,item in enumerate(part['regions']):
        r=bykey[item['key']]; evidence=ev[r['id']]
        components=[]
        for j,label in enumerate(item['components']):
            cid=f'component:p{item["page"]}:{i+1:03}:{j+1:02}'
            components.append({'id':cid,'description':label,'region_id':r['id'],
                               'disposition':'structurally_inventoried','evidence_id':evidence['id'],
                               'boundary_basis':'Complete visible component within the enclosing disjoint authored rectangle.'})
            component_ids.append(cid)
        rows.append({'region_id':r['id'],'region_revision':r['revision'],'key':r['key'],
                     'physical_page':item['page'],'title':item['title'],'kind':r['kind'],
                     'pixel_box':item['pixel_box'],'box':r['box'],'page_basis_hash':evidence['page_basis_hash'],
                     'reading_order_index':final['reading_order'].index(r['id']),
                     'components':components,'evidence':evidence,'coverage':r['coverage'],
                     'structural_disposition':'Inventoried; original page and fresh crop visually compared.',
                     'uncertainty':r['uncertainty'],'exclusion':None})
    assert len(component_ids)==len(set(component_ids))
    write('region-ledger.json',{**envelope,'pixel_frame':part['pixel_frame'],
          'coordinate_rounding':'Shared pixel boundary to nearest integer page millionth; identical shared boundaries remain disjoint.',
          'regions':rows,'component_count':len(component_ids),'component_reconciliation':{'visible_components':len(component_ids),
          'assigned_components':len(component_ids),'unassigned_components':[],'duplicate_component_ids':[]},
          'editorial_disposition':'Headers, rules, printed glyphs and footers inventoried; no exclusion authorization or represented semantic level.',
          'blank_area_disposition':'Explicit geometric gaps in coverage-report.json; never treated as represented or excluded.',
          'label_status':'Assigned page labels remain unchanged. Seeing the printed glyph is not verified label metadata.'})
    newlinks=[l for l in final['links'] if l['from'] in newids or l['to'] in newids]
    def locator(identity):
        r=next(r for r in new if r['id']==identity); e=ev[identity]
        return {'region_id':identity,'revision':r['revision'],'page_id':r['page_id'],
                'physical_page':e['pdf_page'],'box':r['box'],'evidence_id':e['id']}
    def keyed(page,suffix): return bykey[f'physical-page:{page}:ig2b05:{suffix}']['id']
    write('continuations.json',{**envelope,'links':[{**l,'from_locator':locator(l['from']),'to_locator':locator(l['to'])} for l in newlinks],
          'boundaries':[
              {'boundary':'16-17','status':'context_only_prior_exit','accepted_observation':'Page 16 final play note ends in a complete sentence.',
               'assigned_entry':locator(keyed(17,'6-56')),'observation':'Page 17 begins with a new numbered 6.56 clause; no dangling visible sentence at entry.',
               'context_access_in_this_attempt':False,'chapter_relation':'unresolved beyond scoped context'},
              {'boundary':'17-18','status':'resolved_structural_continuation','from':locator(keyed(17,'voluntary-example-start')),
               'to':locator(keyed(18,'voluntary-example-velites')),'observation':'Example 1 continues with Velites paragraph, then Hastati paragraph.'},
              {'boundary':'18-19','status':'resolved_structural_continuation','from':locator(keyed(18,'6-73-start')),
               'to':locator(keyed(19,'6-73-end')),'observation':'Facing definition continues after the word opposite into Rear.'},
              {'boundary':'19-20','status':'complete_sentence_then_new_chapter','from':locator(keyed(19,'pw-play-note-2')),
               'to':locator(keyed(20,'7-0-heading')),'observation':'Page 19 ends a complete play note; page 20 begins chapter 7.0.'},
              {'boundary':'20-21','status':'unresolved_uninspected_target','from':locator(keyed(20,'7-24-start')),
               'observation':'7.24 ends at an introductory colon; its following conditions are outside assignment.',
               'target_physical_page':21,'target_region_id':None,'context_access_in_this_attempt':False}],
          'context_only_accesses':[],'context_inventory_denominator':0,
          'other_numeric_references':'Retained as literal locators in source-reference-index.json; uninspected targets stay unresolved.'})
    full=coverage(final)
    assigned={k:sum(r['coverage'][k]['status']=='unprocessed' for r in new) for k in ('transcription','descriptive_semantics','formal_semantics')}
    write('coverage-report.json',{**envelope,'full_44_page_inventory':full,
          'full_counts':{'pages':44,'regions':len(final['regions']),'evidence':len(final['evidence']),'links':len(final['links'])},
          'assigned_task':{'physical_pages':[17,18,19,20],'region_denominator':len(new),'structurally_inventoried_regions':len(new),
          'components':len(component_ids),'evidence_count':len(ev),'represented':{k:0 for k in assigned},'unprocessed':assigned,
          'per_page':[{**p,'component_count':sum(len(i['components']) for i in part['regions'] if i['page']==p['pdf_page'])} for p in full['pages'] if p['pdf_page'] in (17,18,19,20)]},
          'context_only':{'new_accesses':0,'regions':0,'assigned_denominator_contribution':0,'represented_contribution':0},
          'unresolved_nonassigned_placeholders':[{'id':r['id'],'key':r['key'],'coverage':r['coverage']} for r in untouched_new if r['key'].endswith(':unprocessed-placeholder')],
          'partition_set_equality':True,'coverage_limits':'Region accounting and geometric area do not prove verified transcription, semantic coverage, acceptance, or executable readiness.'})
    page_observations={
        17:'Two-column page: 6.56 and its Elephant exception; italic Withdrawal example and gray play note; 6.57. Right column: 6.6 heading, definition, blue design note, 6.61, 6.62 and exception, 6.63 with four bullets, gray play note, Example 1 beginning. Header/rule/page glyph and footer present.',
        18:'Example 1 continues with Velites then Hastati; Example 2 and blue Roman flexibility note; 6.64-6.66. 6.66 sentence wraps to right-column top. 6.67, 6.68 with seven bullets, 6.69; 6.7 and blue design note. In Column marker beside 6.71 split text, exceptions, 6.72 and unfinished 6.73. Header/rule/page glyph and footer present.',
        19:'6.73 continues at left top. 6.74 and two-row hex/counter movement diagram with separate italic caption; 6.75-6.77. Right: 6.8 heading, two marker faces and wrapped introduction, 6.81-6.83, two bullets and two italic play notes. Header/rule/page glyph and footer present.',
        20:'Chapter 7.0 and 7.1 headings; 7.11, separate single-hex and Phalanx facing diagrams with Front/Flank/Rear labels; 7.12 with four bullets, 7.13-7.15. Right: 7.15 exception and gray note, 7.16 and blue note; 7.2 heading, definition and ZOC diagram with wrapped 7.21, 7.22, 7.23 with three bullets, exception and gray note, following paragraph; 7.24 ends at introductory colon. Header/rule/page glyph and footer present.'}
    write('original-page-inspection.json',{**envelope,'basis':'Fresh original-page PNGs rendered from pinned PDF at 144 DPI, then all proposed region crops visually compared in crop-review sheets.',
          'inspection_actor':common()['actor'],'pages':[{'physical_page':n,'original_image':pin(REL+f'/original-pages/page-{n}.png'),
          'full_page_inspected':True,'observation':page_observations[n],'region_count':sum(i['page']==n for i in part['regions']),
          'region_keys':[i['key'] for i in part['regions'] if i['page']==n]} for n in (17,18,19,20)],
          'crop_review':load(REL+'/crop-review.json'),'uncertainty':part['uncertainty'],
          'adjacent_pages_inspected':[],'inherited_inspection_claims':False})
    write('source-pins.json',{**envelope,'packet':pin(SESSION+'/packet.json'),'task_contract':pin(SESSION+'/task.json'),
          'authored_partition':pin(REL+'/authored-partition.json'),'persisted_registry':pin(REL+'/persisted-registry.json'),
          'assigned_page_basis':[{'page_id':p['id'],'physical_page':p['pdf_page'],'page_basis_hash':page_basis_hash(p)} for p in final['pages'] if p['id'] in pageids],
          'dependency_projection':{'path':SESSION+'/dependency-view.json','sha256':'95f7c6edb5c7245a9dc59b56e220ff7ecdaea2d9d682bbef23f6835301882523','dependency':'IG-2B04'},
          'retained_baseline':pin('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/inventory.json'),
          'retained_registry':pin('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/identity-registry.json')})
    versions={name:importlib.metadata.version(name) for name in ('pypdf','pdfplumber','Pillow','pytest','reportlab')}
    natives={name:subprocess.run([name,*args],capture_output=True,text=True,check=True).stdout for name,args in [('git',['--version']),('pwsh',['--version'])]}
    for name in ('pdfinfo','pdftoppm'):
        p=subprocess.run([name,'-v'],capture_output=True,text=True,check=True); natives[name]=(p.stdout+p.stderr).strip()
    write('toolchain.json',{**envelope,'python_executable':pin(Path(sys.executable).relative_to(ROOT).as_posix()),
          'process_pythonpath':os.environ.get('PYTHONPATH'),'process_path_prefix':os.environ['PATH'].split(os.pathsep)[0],
          'libraries':versions,'native':natives,'dpi':144,'process_only_settings':True,'installed_dependencies_changed':False})
    norm,fields=normalized(final,REL+'/final-verified')
    replay_results=[]
    for name in ('replay-1','replay-2'):
        replay=load(REL+'/'+name+'/inventory.json')
        report=validate(replay,ROOT)
        other,otherfields=normalized(replay,REL+'/'+name)
        assert norm==other, name+' complete normalized logical sidecar'
        assert fields==otherfields and len(fields)==102*3
        assert registry==load(REL+'/'+name+'/identity-registry.json')==replay['registry']
        assert (ROOT/(REL+'/final-verified/identity-registry.json')).read_bytes()==(ROOT/(REL+'/'+name+'/identity-registry.json')).read_bytes()
        replay_ev={e['region_id']:e for e in replay['evidence'] if e['region_id'] in newids}
        assert set(replay_ev)==newids==set(ev)
        assert {e['id'] for e in replay['evidence']}=={e['id'] for e in final['evidence']}
        compared=[]
        for identity in sorted(newids):
            for field in ('crop_pdf','image','text'):
                a=ev[identity][field]; b=replay_ev[identity][field]
                assert a['sha256']==b['sha256'] and a['bytes']==b['bytes']
                assert (ROOT/a['path']).read_bytes()==(ROOT/b['path']).read_bytes()
                compared.append({'region_id':identity,'artifact_type':field,'final':a,'replay':b,'bytes_equal':True})
        replay_results.append({'name':name,'inventory':pin(REL+'/'+name+'/inventory.json'),
            'registry':pin(REL+'/'+name+'/identity-registry.json'),'complete_logical_sidecar_equal':True,
            'registry_bytes_equal':True,'assigned_region_set_sha256':digest(sorted(newids)),
            'complete_region_set_sha256':digest(sorted(r['id'] for r in replay['regions'])),
            'complete_evidence_set_sha256':digest(sorted(e['id'] for e in replay['evidence'])),
            'normalized_sidecar_sha256':digest(other),'normalized_fields':fields,
            'complete_region_id_set_equal':True,'complete_evidence_id_set_equal':{e['id'] for e in replay['evidence']}=={e['id'] for e in final['evidence']},
            'counts':{'all_regions':len(replay['regions']),'all_evidence':len(replay['evidence']),'assigned_regions':102,'assigned_artifacts':len(compared)},
            'compared_artifacts':compared,'source_structure_and_evidence_validation':'passed'})
    write('replay-report.json',{**envelope,'normalization':'Only the 306 assigned crop_pdf.path/image.path/text.path fields replace their derivation output prefix; enclosing inventory revision is recomputed and compared via normalized sidecar hash. No IDs, locators, hashes, byte counts, source paths, page/region revisions, registry, links, toolchain, labels or retained evidence fields are dropped.',
          'normalized_final_sha256':digest(norm),'complete_set_comparison':True,'sampled':False,'replays':replay_results})
    report_names=['region-ledger.json','continuations.json','coverage-report.json','source-pins.json','toolchain.json',
                  'original-page-inspection.json','preservation-report.json','replay-report.json','crop-review.json']
    refs=[]
    for i,r in enumerate(new):
        text=(ROOT/ev[r['id']]['text']['path']).read_text(encoding='utf-8')
        for m in re.finditer(r'(?<![\d.])\d{1,2}\.\d{1,2}(?![\d.])',text):
            refs.append({'region_id':r['id'],'evidence_id':ev[r['id']]['id'],'literal':m.group(),
                         'text_path':ev[r['id']]['text']['path'],'start':m.start(),'end':m.end(),
                         'target_status':'unresolved','reason':'Literal navigation only; source target and meaning not verified by this inventory.'})
    index={**envelope,'reports':[{**pin(REL+'/'+name),'inventory_revision':final['revision']} for name in report_names],
           'region_entries':[{'region_id':row['region_id'],'region_revision':row['region_revision'],
             'ledger_path':REL+'/region-ledger.json','json_pointer':f'/regions/{i}',
             'evidence_id':row['evidence']['id']} for i,row in enumerate(rows)],'literal_numeric_references':refs}
    ledger=load(REL+'/region-ledger.json')
    for ref in refs:
        text=(ROOT/ref['text_path']).read_text(encoding='utf-8')
        assert text[ref['start']:ref['end']]==ref['literal']
    for row in index['region_entries']:
        target=ledger['regions'][int(row['json_pointer'].rsplit('/',1)[1])]
        assert target['region_id']==row['region_id'] and target['region_revision']==row['region_revision']
    for item in index['reports']:
        assert pin(item['path'])['sha256']==item['sha256']
        assert load(item['path'])['inventory_revision']==final['revision']
    write('source-reference-index.json',index)
    write('set-validation-report.json',{**envelope,'assigned_region_evidence_ledger_sets_equal':True,
          'all_visible_components_have_dispositions':True,'component_count':len(component_ids),
          'all_current_report_hashes_and_source_reference_pointers_resolve':True,'checked_report_count':len(report_names),
          'checked_region_pointer_count':len(rows),'numeric_reference_offsets_checked':len(refs),
          'nonassigned_preservation_passed':all(checks.values()),'both_complete_replays_passed':True,
          'unresolved_targets_remain_unresolved':True,'context_only_denominator':0})
    print(json.dumps({'regions':len(final['regions']),'evidence':len(final['evidence']),'components':len(component_ids),
                      'report_index':REL+'/source-reference-index.json','status':'passed'}))

if __name__=='__main__':
    reports()
