"""Freeze task reports from actual complete serial runs, with no source expansion."""
import copy
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
from wgc.sources.inventory import coverage, digest, file_pin, seal, validate

ROOT=Path.cwd()
A=Path(__file__).parent.relative_to(ROOT)
SESSION=Path('private/workflow/orchestrator/20261016T195516Z-332903f5/005-IG-2B07-executor-32eedee6')
TASK=json.loads((SESSION/'task.json').read_text())
SCOPE=TASK['source_scope']
CFG=SESSION/'runtime-configuration.json'
META={'role':'executor','actor':'ig2:005-IG-2B07-executor-32eedee6:executor','model':'gpt-6.1-sol','reasoning':'high',
      'configuration_evidence':CFG.as_posix(),'configuration_sha256':file_pin(ROOT,CFG.as_posix())['sha256']}
def pin(p): return file_pin(ROOT,Path(p).as_posix())
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def report(name,v):
    destination=A/name
    assert not destination.exists(),str(destination)
    write(destination,{**META,**v})

def crop_sheets():
    """Review contact sheets preserve every fresh target with a visible key."""
    destination=A/'inspection-sheets'
    assert not destination.exists()
    destination.mkdir()
    rows=load(A/'final-verified/region-accounting.json')
    pins=[]
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
    for page in (24,25,26,27,28,29):
        page_rows=[r for r in rows if r['page']==page]
        for start in range(0,len(page_rows),8):
            batch=page_rows[start:start+8]
            # Each target is shown independently; narrow text is readable by
            # combining these exact crops with the full-page source inspection.
            sheet=Image.new('RGB',(1440,1600),'#e8e8e8')
            draw=ImageDraw.Draw(sheet)
            for i,row in enumerate(batch):
                x=(i%2)*720
                y=(i//2)*400
                draw.text((x+8,y+4),row['key'],font=font,fill='black')
                draw.text((x+8,y+26),f"{row['kind']} / {row['category']} / {row['role']}",font=small,fill='black')
                with Image.open(row['evidence']['image']['path']) as im:
                    im=im.convert('RGB')
                    im.thumbnail((704,348))
                    sheet.paste(im,(x+8,y+48))
            out=destination/f'page-{page}-batch-{start//8+1:02}.png'
            sheet.save(out)
            pins.append({**pin(out),'region_ids':[r['region']['id'] for r in batch]})
    write(destination/'index.json',pins)
    print(json.dumps({'sheets':len(pins),'targets':sum(len(p['region_ids']) for p in pins)}))

def reports():
    runs=[A/name for name in ('final-verified','replay-1','replay-2')]
    docs=[load(r/'inventory.json') for r in runs]
    rows=load(runs[0]/'region-accounting.json')
    derived=[load(r/'derivation-report.json') for r in runs]
    author=load(A/'author-input.json')
    old=load(SCOPE['baseline_inventory']['path'])
    oldreg=load(SCOPE['identity_registry']['path'])
    final=docs[0]
    newids=set(derived[0]['complete_target_ids'])
    componentids=set(derived[0]['component_ids'])
    taskids={r['region']['id'] for r in rows if r['role']=='inventory'}
    boundaryids={r['region']['id'] for r in rows if r['category']=='boundary'}
    bykey={r['key']:r for r in rows}
    assert len(newids)==189 and len(taskids)==100 and len(componentids)==87 and len(boundaryids)==2
    assert newids==taskids|componentids|boundaryids
    assert not taskids&componentids and not boundaryids&(taskids|componentids)
    # Path normalization changes only the current run prefix. The enclosing
    # inventory revision is recomputed because it hashes those paths.
    def normalize(value,prefix):
        if isinstance(value,str):
            return '$RUN/'+value[len(prefix)+1:] if value.startswith(prefix+'/') else value
        if isinstance(value,list): return [normalize(v,prefix) for v in value]
        if isinstance(value,dict): return {k:normalize(v,prefix) for k,v in value.items()}
        return value
    normalized=[]
    comparisons=[]
    for directory,doc,run in zip(runs,docs,derived):
        assert set(run['complete_target_ids'])==newids
        assert set(run['component_ids'])==componentids
        assert doc['registry']==final['registry']
        normalized.append(seal(normalize(doc,directory.as_posix())))
        assert normalized[-1]==normalized[0]
        assert normalize(load(directory/'region-accounting.json'),directory.as_posix())==normalize(rows,runs[0].as_posix())
        expected={f'evidence/{r["key"].replace(":","-")}/{suffix}' for r in rows for suffix in ('crop.pdf','text.txt','image.png')}
        expected|={'inventory.json','identity-registry.json','region-accounting.json','derivation-report.json'}
        # Resolve the exact generated output set through its evidence index. No
        # recursive file discovery or private-tree search is needed or permitted.
        actual={Path(ev[k]['path']).relative_to(directory).as_posix() for ev in doc['evidence'] if ev['region_id'] in newids for k in ('crop_pdf','text','image')}
        actual|={'inventory.json','identity-registry.json','region-accounting.json','derivation-report.json'}
        assert actual==expected
        comparisons.append({'directory':directory.as_posix(),'input_pins':run['input_pins'],'author_pins':run['author_pins'],
                            'invocation':run['command'],'derivation_report':pin(directory/'derivation-report.json'),
                            'normalized_inventory_sha256':digest(normalized[-1]),'output_count':len(actual),
                            'complete_target_set_equal':True,'component_set_equal':True,'registry_equal':True,
                            'author_fields_geometry_order_links_coverage_equal':True,'normalized_evidence_locators_equal':True,
                            'raw_payload_pins_equal':True,
                            'output_pins':[pin(directory/p) for p in sorted(actual)]})
        assert all(ev[k]['sha256']==next(e for e in final['evidence'] if e['id']==ev['id'])[k]['sha256'] for ev in doc['evidence'] if ev['region_id'] in newids for k in ('crop_pdf','text','image'))
    report('replay-report.json',{'format':'wgc-complete-serial-replay-report-1','independent_complete_runs':3,'required_replays':2,
                               'normalization':'Only current output directory prefix is replaced by $RUN; enclosing inventory revision is recomputed. All evidence payload hashes, IDs, author fields, registry, order, links and coverage compare exactly.',
                               'operational_reports':'Invocation path and elapsed wall time differ by run and are frozen separately; they are not substantive inventory/evidence outputs. Engine parameters and payload bytes compare exactly.',
                               'runs':comparisons,'target_ids':sorted(newids),'component_ids':sorted(componentids),'all_passed':True})
    positions={identity:i for i,identity in enumerate(final['reading_order'])}
    report('region-ledger.json',{'format':'wgc-region-accounting-1','regions':[{**r,'reading_order_index':positions[r['region']['id']]} for r in rows],
                              'preserved_nonassigned_index':[{'id':r['id'],'revision':r['revision'],'page_id':r['page_id'],'denominator_role':r['denominator_role']} for r in old['regions'] if r['id'] not in SCOPE['replace_only_region_ids']],
                              'leftovers':'Blank margins/gutters are geometric gaps, reported per page in coverage-report.json. The retained prior complete inspection reported no content-bearing remainder on the assigned original renders; this repair freshly inspects only the affected diagram and preserves all prior payload byte pins. Full transcription and tiny counter glyph readings remain unverified.',
                              'editorial_policy':'Headers, printed page labels, decorative artwork and copyright are accounted, without human exclusion or semantic acceptance.'})
    report('component-ledger.json',{'format':'wgc-nested-components-1','components':[r for r in rows if r['category']=='component'],
                                  'component_count':len(componentids),'additional_denominator':0,
                                  'scope':'Both complete page-28 diagrams and page-25 decorative artwork. Repeated hex strokes are one complete grid background per diagram. Counter faces include their visible internal numbers, words and symbols; their transcription is unverified. Each external label, arrow, counter, leader, Shock marker and result marker has a separate crop.',
                                  'uncertainty':'Overlapping nested component crops retain composite stacks; no occluded glyph is reconstructed.'})
    def endpoint(key):
        r=bykey['ig2b07:'+key]
        return {'id':r['region']['id'],'physical_page':r['page'],'box':r['box'],'evidence':r['evidence']}
    report('continuations.json',{'format':'wgc-continuation-accounting-1','links':[l for l in final['links'] if l not in old['links']],
                               'inherited_links_exact':{'count':len(old['links']),'canonical_sha256':digest(old['links'])},
                               'endpoints':[{ 'id':r['region']['id'],'evidence_id':r['evidence']['id'],'page':r['page'],'box':r['box']} for r in rows],
                               'assigned_range_entry':{'physical_page':25,'observation':'Page 24 Procedure/Important box establishes Shock step sequence. Page 25 begins with associated play/design notes and 8.41; no split sentence at this boundary was observed in the permitted strip. Empty prepared prior boundary projection was unknown, not absence. Inherited page-25 context and links are preserved.','from':endpoint('entry-context'),'to':endpoint('p25-play-note'),'additional_denominator':0},
                               'assigned_range_exit':{'physical_page':28,'observation':'Phalanx B paragraph ends with further; page-29 upper-left paragraph continues rounded up to 4:1 through not routing yet.','from':endpoint('p28-struggle-b'),'to':endpoint('exit-context'),'additional_denominator':0},
                               'cross_page_or_column_observations':[{'from':endpoint(left),'to':endpoint(right),'observation':text} for left,right,text in [
                                   ('p25-843-dr','p26-dr-mod-intro','Page-26 above DR modifiers refer back to the page-25 DR paragraph; remaining page-25 bullet sequence is retained.'),
                                   ('p26-example2','p26-example3','8.45 example series continues from left-column example 2 to right-column example 3.'),
                                   ('p26-step2-b1','p27-step2-b2','Rounding list continues on the next page.'),
                                   ('p28-charge-start','p28-charge-end','One sentence crosses from left-column bottom to right-column top.'),
                                   ('p28-struggle-b','exit-context','The example sentence crosses the assigned range boundary.')]],
                               'meaning_review':'Structural links only; no model semantic acceptance.'})
    fullids={r['id'] for r in final['regions'] if r['denominator_role']=='inventory'}
    contextids={r['id'] for r in final['regions'] if r['denominator_role']=='context'}
    assert fullids.isdisjoint(contextids) and fullids|contextids=={r['id'] for r in final['regions']}
    finalcov=coverage(final)
    report('coverage-report.json',{'format':'wgc-complete-batch-coverage-1','full_inventory_ids':sorted(fullids),'full_inventory_count':len(fullids),
                                 'assigned_inventory_ids':sorted(taskids),'assigned_inventory_count':len(taskids),
                                 'full_context_ids':sorted(contextids),'full_context_count':len(contextids),
                                 'new_boundary_ids':sorted(boundaryids),'new_nested_component_ids':sorted(componentids),'new_context_count':len(boundaryids|componentids),
                                 'context_denominator_contribution':0,'complete_new_target_set_equal':True,'inventory_context_disjoint':True,
                                 'full_coverage':finalcov,'assigned_page_geometry':[p for p in finalcov['pages'] if p['pdf_page'] in (25,26,27,28)],
                                 'remaining_unprocessed_placeholders':[{'id':r['id'],'page_id':r['page_id']} for r in final['regions'] if r['key'].endswith(':unprocessed-placeholder')],
                                 'new_coverage_status_counts':{'transcription_partial':len(taskids),'descriptive_semantics_unprocessed':len(taskids),'formal_semantics_unprocessed':len(taskids),'exclusions':0},
                                 'accounting_limits':author['limits'],'semantic_acceptance_granted':False,'executable_readiness':'unverified'})
    # Recheck complete preservation independently of the derivation assertions.
    retired=set(SCOPE['replace_only_region_ids'])
    now={r['id']:r for r in final['regions']}
    assert all(now[r['id']]==r for r in old['regions'] if r['id'] not in retired)
    assert {r['id'] for r in old['regions']}-set(now)==retired
    assert final['pages']==old['pages'] and final['source']==old['source']
    assert all(e in final['registry']['entries'] for e in oldreg['entries'])
    assert final['evidence'][:len(old['evidence'])]==old['evidence'] and final['links'][:len(old['links'])]==old['links']
    report('preservation-report.json',{'format':'wgc-exact-preservation-1','baseline':SCOPE['baseline_inventory'],'baseline_registry':SCOPE['identity_registry'],
                                     'result':pin(A/'final-verified/inventory.json'),'result_registry':pin(A/'final-verified/identity-registry.json'),
                                     'checks':derived[0]['preservation'],'old_counts':{k:len(old[k]) for k in ('pages','regions','links','evidence')},
                                     'result_counts':{k:len(final[k]) for k in ('pages','regions','links','evidence')},
                                     'old_registry_entries':len(oldreg['entries']),'preserved_registry_entries':len(oldreg['entries']),
                                     'new_region_ids':sorted(newids),'retired_only':sorted(retired),'all_inherited_artifacts_pins_validated':True,
                                     'no_placeholder_source_reference_pins':'Source and provenance pins are exactly the accepted baseline actual byte pins. Retired placeholder memberships are removed; their registry entries remain.'})
    native={}
    for command in ('pdfinfo','pdftoppm','pwsh'):
        path=Path(shutil.which(command)).resolve()
        native[command]={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
    interpreter=Path(sys.executable).resolve()
    report('toolchain.json',{'interpreter':{'path':str(interpreter),'sha256':hashlib.sha256(interpreter.read_bytes()).hexdigest(),'version':sys.version},
                           'process_pythonpath':os.environ.get('PYTHONPATH'),'process_path_prefix':os.environ.get('PATH','').split(';')[:next(i+1 for i,entry in enumerate(os.environ.get('PATH','').split(';')) if Path(entry).resolve()==Path(shutil.which('pdftoppm')).resolve().parent)],
                           'libraries':{name:importlib.metadata.version(name) for name in ('pypdf','pdfplumber','Pillow','pytest','reportlab')},'native':native,
                           'rendering':{'dpi':144,'format':'png','cropbox':True,'serial':True,'pool_workers':0},'process_settings_preserved':True})
    originals=load(A/'originals/pins.json')
    sheets=load(A/'inspection-sheets/index.json')
    # A bounded repair revalidates previous complete inspection without claiming
    # that prior-role visual observations were made freshly by this actor.
    observations=load(A/'visual-observations.json')
    assert observations['fresh_affected_diagram_viewed']
    affected={r['region']['id'] for r in rows if r['key']=='ig2b07:p28-diagram-after' or r.get('parent_key')=='ig2b07:p28-diagram-after'}
    assert set(observations['fresh_inspected_target_ids'])==affected
    assert set(observations['affected_sheet_paths'])=={s['path'] for s in load(A/'affected-inspection-sheets/index.json')}
    priorroot=Path('private/workflow/runs/IG-2B07/inventory-25-28-01')
    previous=load(priorroot/'final-verified/inventory.json')
    prevrows=load(priorroot/'final-verified/region-accounting.json')
    newbyid={r['id']:r for r in final['regions']}
    priorids={r['id'] for r in previous['regions']}
    arrowid=bykey['ig2b07:p28-diagram-after-upper-b-arrow']['region']['id']
    assert set(newbyid)-priorids=={arrowid}
    assert all(newbyid[r['id']]==r for r in previous['regions'])
    assert [x for x in final['reading_order'] if x!=arrowid]==previous['reading_order']
    assert final['links']==previous['links']
    assert all(e in final['registry']['entries'] for e in previous['registry']['entries'])
    prevev={e['id']:e for e in previous['evidence']}
    assert len(final['evidence'])==len(previous['evidence'])+1
    for ev in final['evidence']:
        if ev['id'] not in prevev:
            assert ev['region_id']==arrowid
            continue
        assert normalize(ev,(A/'final-verified').as_posix())==normalize(prevev[ev['id']],(priorroot/'final-verified').as_posix())
        for kind in ('crop_pdf','text','image'):
            assert ev[kind]['sha256']==prevev[ev['id']][kind]['sha256']
    assert final['source']==previous['source'] and final['pages']==previous['pages']
    assert len(fullids)==849 and len(contextids)==92 and len(final['regions'])==941
    previous_author=load(priorroot/'author-input.json')
    assert author['regions'][:-1]==previous_author['regions'] and author['links']==previous_author['links']
    report('repair-preservation-report.json',{'immutable_delivery':pin(priorroot/'delivery.json'),
           'prior_complete_inspection':pin(priorroot/'original-page-inspection.json'),
           'all_prior_region_records_exact':True,'all_prior_registry_entries_exact':True,
           'all_prior_evidence_metadata_equal_after_output_prefix_normalization':True,
           'all_prior_evidence_payload_byte_pins_exact':True,'all_prior_links_exact':True,
           'prior_reading_order_exact_after_removing_single_addition':True,
           'prior_author_rows_and_links_exact':True,'new_region_ids':[arrowid],
           'parent_boxes_unchanged':True,'inventory_denominators_unchanged':True,
           'previous_complete_target_count':len(prevrows),'new_complete_target_count':len(rows),
           'new_component_count':len(componentids),'full_region_count':len(final['regions']),
           'full_inventory_count':len(fullids),'full_context_count':len(contextids),
           'normalization':'Only exact previous/new final-verified output directory prefixes in evidence path fields; no evidence payload or observation changes.'})
    report('original-page-inspection.json',{'fresh_affected_originals':originals,
           'all_fresh_target_contact_sheet_index':pin(A/'inspection-sheets/index.json'),
           'fresh_affected_component_sheets':load(A/'affected-inspection-sheets/index.json'),
           'inspection':observations,'source_pdf':SCOPE['source_pdf'],'source_revision':SCOPE['source_revision'],
           'fresh_inspection_scope':{'physical_page':28,'parent_region_id':'region:93a4c97f-54e6-4b11-95c2-f0a704491226'},
           'prior_complete_four_page_and_boundary_inspection':pin(priorroot/'original-page-inspection.json'),
           'prior_inspection_attribution':'Prior executor observations retained as immutable inputs, not fresh inspection claims by this role.',
           'prior_coverage_revalidation':pin(A/'repair-preservation-report.json'),
           'transcription_verified':False,'semantic_acceptance_granted':False})
    allpins=[]
    for row in rows:
        for kind in ('crop_pdf','text','image'):
            allpins.append({**row['evidence'][kind],'source_sha256':SCOPE['source_revision'],'physical_page':row['page'],
                            'region_id':row['region']['id'],'parent_region_id':row['parent_region_id'],'box':row['box'],'kind':kind})
    report('source-pins.json',{'inputs':[SCOPE[k] for k in ('baseline_inventory','identity_registry','source_pdf','source_provenance')]+list(SCOPE['current_reports'].values())+[TASK['refinement_evidence']],
                             'originals':originals,'immutable_prior_delivery':pin(priorroot/'delivery.json'),'repair_scope':TASK['repair_authorization']['scope'],'fresh_region_component_artifacts':allpins,'replays':comparisons,
                             'source_reference_index':'All source locators use the actual accepted source SHA and exact page/region/component box; no placeholder source filename substitution.'})
    print(json.dumps({'reports_frozen':9,'replay_equality':True,'inventory_count':len(fullids),'context_count':len(contextids)}))

if __name__=='__main__':
    if sys.argv[1:] == ['--sheets']:
        crop_sheets()
    else:
        reports()
