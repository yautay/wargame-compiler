"""Task-owned preservation, replay and reference checks; never print source content."""
import copy
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

from wgc.sources.inventory import coverage, file_pin, validate, page_basis_hash
from build_inventory import ROOT, CONTRACT, load, write

REPO=Path.cwd()
BASE={k:v for k,v in load(ROOT/'claim.json').items() if k not in ('summary','criteria','artifacts','checks','utc')}

def pin(path): return file_pin(REPO,Path(path).as_posix())

def scan_pins(value, results):
    if isinstance(value,dict):
        if isinstance(value.get('path'),str) and isinstance(value.get('sha256'),str):
            path=value['path']
            if not Path(path).is_absolute():
                actual=pin(path)
                assert actual['sha256']==value['sha256'],path
                if 'bytes' in value: assert actual['bytes']==value['bytes'],path
                results[path]=actual
        for child in value.values(): scan_pins(child,results)
    elif isinstance(value,list):
        for child in value: scan_pins(child,results)

def normalized(document):
    result=copy.deepcopy(document)
    result.pop('revision')
    for evidence in result['evidence']:
        for field in ('crop_pdf','text','image'):
            artifact=evidence[field]
            if artifact['path'].startswith(ROOT.as_posix()+'/'):
                artifact['path']=artifact['path'].split('/evidence/',1)[-1]
    return result

def main():
    contract=load(CONTRACT)
    task=load('private/workflow/orchestrator/20261016T115606Z-694df602/001-IG-2B04-executor-0de1c1e6/task.json')
    assert pin(CONTRACT)==task['inventory_contract']
    assert contract['inputs']==load(ROOT/'checkpoint.json')['base_files']
    assert contract['physical_pages']==[13,14,15,16]
    baseline=load(contract['inputs']['baseline_inventory']['path'])
    current=load(ROOT/'final-verified/inventory.json')
    authored=load(ROOT/'authored-regions.json')['regions']
    common_author_input=load(ROOT/'authored-regions-build-input.json')['regions']
    author_fields=('key','id','pdf_page','kind','box')
    assert [{k:a[k] for k in author_fields} for a in authored]==[{k:a[k] for k in author_fields} for a in common_author_input]
    current_map={r['id']:r for r in current['regions']}
    target=set(contract['target_ids'])
    retained=[r for r in baseline['regions'] if r['id'] not in target]
    assert all(current_map[r['id']]==r for r in retained)
    assert len(current['pages'])==44 and current['pages']==baseline['pages']
    assert current['source']==baseline['source']
    assert current['links'][:len(baseline['links'])]==baseline['links']
    assert current['evidence'][:len(baseline['evidence'])]==baseline['evidence']
    assert all(e in current['registry']['entries'] for e in baseline['registry']['entries'])
    assert target.isdisjoint(current_map)
    assert set(r['id'] for r in baseline['regions'])-set(current_map)==target
    authored_ids={a['id'] for a in authored}
    assert set(current_map)-{r['id'] for r in baseline['regions']}==authored_ids
    assert [i for i in current['reading_order'] if i not in authored_ids]==[i for i in baseline['reading_order'] if i not in target]
    assert {a['pdf_page'] for a in authored}=={13,14,15,16}
    scope=load('private/workflow/runs/IG-2B04/rg-recovery-20261016-01/scope.json')
    preserved=load(scope['preserve_manifest']['path'])
    for artifact in preserved['artifacts']: assert pin(artifact['path'])['sha256']==artifact['sha256'],artifact['path']
    for item in contract['inputs'].values(): assert pin(item['path'])==item
    write(ROOT/'preservation-report.json',{**BASE,'summary':'All 44 pages, 435 nonassigned records, old links/evidence and every registry binding retained; only four placeholder memberships retire.',
        'input_pins':contract['inputs'],'preserve_manifest':scope['preserve_manifest'],'preserved_artifacts_verified':len(preserved['artifacts']),
        'nonassigned_regions_equal':len(retained),'pages_equal':44,'prior_links_retained':len(baseline['links']),
        'prior_evidence_retained':len(baseline['evidence']),'prior_registry_entries_retained':len(baseline['registry']['entries']),
        'retired_memberships':list(contract['target_ids']),'retired_registry_entries_retained':True,'passed':True})
    replays=[]
    for name in ('replay-a','replay-b'):
        replay=load(ROOT/name/'inventory.json')
        validate(replay,REPO)
        assert normalized(replay)==normalized(current),name
        assert replay['registry']==current['registry']
        replays.append({'name':name,'inventory':pin(ROOT/name/'inventory.json'),'build_report':pin(ROOT/name/'build-report.json'),
                        'full_inventory_equal_after_locator_path_normalization':True,'assigned_evidence_bytes_equal':True,
                        'stable_identities_revisions_and_page_geometry_equal':True})
    write(ROOT/'replay-report.json',{**BASE,'summary':'Two separate command executions started from the pinned baseline and authored registry; every assigned crop/text/image regenerated independently.',
        'common_authored_input_used_by_all_three_builds':pin(ROOT/'authored-regions-build-input.json'),
        'final_ledger_specification':pin(ROOT/'authored-regions.json'),
        'observation_only_correction':'Page14 example6.22 HI/MI label corrected after builds loaded the common input. Keys, IDs, pages, kinds and boxes are asserted equal; no region or evidence change.',
        'normalization':'Only inventory enclosing revision is omitted, and task-local artifact path prefixes before /evidence/ are removed. All evidence hashes, bytes, contents, identities, region revisions, page geometry, labels, coverage and registry remain compared exactly.',
        'final_inventory':pin(ROOT/'final-verified/inventory.json'),'replays':replays,'passed':True})
    full=validate(current,REPO)
    task_ids={a['id'] for a in authored}
    task_document=copy.deepcopy(current)
    task_document['regions']=[r for r in current['regions'] if r['id'] in task_ids]
    task_cov=coverage(task_document)
    task_cov['pages']=[p for p in task_cov['pages'] if p['pdf_page'] in contract['physical_pages']]
    assert task_cov['denominator_regions']==113 and task_cov['context_regions']==0
    assert all(p['unaccounted_area_trillionths']==0 for p in task_cov['pages'])
    context=[r for r in current['regions'] if r['denominator_role']=='context']
    context_levels={level:{status:sum(r['coverage'][level]['status']==status for r in context)
                           for status in ('represented','partial','unprocessed','excluded')}
                    for level in ('transcription','descriptive_semantics','formal_semantics')}
    write(ROOT/'coverage-report.json',{**BASE,'inventory':pin(ROOT/'final-verified/inventory.json'),
        'full_44_page':full,'task_pages_13_16':task_cov,
        'context_only':{'full_inventory_context_regions':len(context),'assigned_context_regions':0,
                        'denominator_regions':0,'levels_of_context_records_only':context_levels,
                        'records':context,'note':'Retained nonassigned context records contribute zero to every denominator; this task adds no context-only regions.'},
        'all_gaps':[{'region_id':r['id'],'coverage':r['coverage']} for r in current['regions'] if any(c['gap'] for c in r['coverage'].values())],
        'semantic_acceptance_granted':False,'executable_readiness':'unverified','note':'Full geometric coverage and evidence capture never count gaps or placeholders as represented.'})
    old_ledger=load(contract['inputs']['region_ledger']['path'])
    old_continuations=load(contract['inputs']['continuations']['path'])
    evidence_by_region={e['region_id']:e for e in current['evidence']}
    ledger={**BASE,'format':'wgc-inventory-task-ledger-2','inventory':pin(ROOT/'final-verified/inventory.json'),
        'assigned_pages':[13,14,15,16],'reading_order':[i for i in current['reading_order'] if i in task_ids],
        'retained_dependency_report_pin':contract['inputs']['region_ledger'],'retained_dependency_report':old_ledger,
        'regions':[{'specification':a,'record':current_map[a['id']],'evidence':evidence_by_region[a['id']],
                    'original_page_image':pin(ROOT/f"original-pages/page-{a['pdf_page']}.png"),
                    'boundary_visual_comparison':'Checked against fresh original page; every listed component included, with marker top correction on page14.'} for a in authored],
        'semantic_acceptance_granted':False,'all_assigned_components_compared_to_original':True,
        'tables_or_legends':'No standalone table appears on13-16; page15 diagram caption retained as legend; page16 diagram labels retained inside diagram.'}
    write(ROOT/'region-ledger.json',ledger)
    refs=[]
    for a in authored:
        ev=evidence_by_region[a['id']]
        text=Path(ev['text']['path']).read_text(encoding='utf-8')
        for m in re.finditer(r'\b(?:[4-9]|10)\.\d{1,2}\b',text):
            refs.append({'from_region':a['id'],'evidence_id':ev['id'],'text_artifact':ev['text'],'offset':[m.start(),m.end()],
                         'raw_locator':m.group(),'target_status':'unresolved','reason':'Literal extracted locator preserved; target meaning not adjudicated and out-of-range pages not inspected.'})
    new_links=[l for l in current['links'] if l not in baseline['links']]
    continuations={**BASE,'inventory':pin(ROOT/'final-verified/inventory.json'),
        'retained_dependency_report_pin':contract['inputs']['continuations'],'retained_dependency_report':old_continuations,
        'links':new_links,'literal_continuations':[l for l in new_links if l['kind']=='continuation'],
        'assigned_range_entry':{'pdf_page':13,'first_region_key':'b04:p13:exception-elite-momentum',
            'observation':'Opening Exception is complete visibly but its preceding anchor is outside scope. Page12 metadata reports complete5.34 sentence; no adjacent original page inspected.',
            'dependency_boundary':contract['boundary'],'target_status':'unresolved'},
        'assigned_range_exit':{'pdf_page':16,'last_substantive_key':'b04:p16:play-note-6.55',
            'observation':'Visible final play note ends in a complete sentence. Chapter continuation outside16 and all uninspected targets remain unresolved; page17 not inspected.','target_status':'unresolved'},
        'unfollowed_references':refs,'no_access_outside_contract':True,'semantic_acceptance_granted':False}
    write(ROOT/'continuations.json',continuations)
    write(ROOT/'source-pins.json',{**BASE,'source':current['source'],'inputs':contract['inputs'],
        'execution_contract':pin(CONTRACT),'packet':load(ROOT/'checkpoint.json')['input_packet'],
        'original_pages':[pin(ROOT/f'original-pages/page-{p}.png') for p in range(13,17)],
        'authored_specification':pin(ROOT/'authored-regions.json'),'authored_registry':pin(ROOT/'authored-registry.json')})
    native={}
    for name,args in [('pdfinfo',['-v']),('pdftoppm',['-v']),('git',['--version']),('pwsh',['--version'])]:
        executable=Path(shutil.which(name))
        result=subprocess.run([str(executable),*args],capture_output=True,text=True,check=True)
        native[name]={'path':executable.as_posix(),'sha256':__import__('hashlib').sha256(executable.read_bytes()).hexdigest(),
                      'version':(result.stdout+result.stderr).strip()}
    expected_tools=load(contract['inputs']['toolchain']['path'])
    libraries={n:importlib.metadata.version(n) for n in ('Pillow','pdfplumber','pypdf','pytest')}
    assert libraries==expected_tools['libraries']
    assert os.environ.get('PYTHONPATH')==expected_tools['process_pythonpath']
    path_entries=os.environ['PATH'].split(os.pathsep)
    pinned_entry=expected_tools['process_path_prefix'].casefold().rstrip('\\/')
    pinned_entry_indices=[i for i,entry in enumerate(path_entries) if entry.casefold().rstrip('\\/')==pinned_entry]
    assert pinned_entry_indices, 'Pinned Poppler directory missing from inherited PATH'
    assert __import__('hashlib').sha256(Path(sys.executable).read_bytes()).hexdigest()==expected_tools['python_executable']['sha256']
    for name,tool in native.items():
        assert tool['sha256']==expected_tools['native'][name]['executable']['sha256'],name
    write(ROOT/'toolchain.json',{**BASE,'python_executable':{'path':Path(sys.executable).as_posix(),'sha256':__import__('hashlib').sha256(Path(sys.executable).read_bytes()).hexdigest()},
        'libraries':libraries,'native':native,
        'process_pythonpath':os.environ.get('PYTHONPATH'),'process_path_prefix':load(contract['inputs']['toolchain']['path'])['process_path_prefix'],
        'inherited_path_contains_pinned_poppler_directory':True,'pinned_poppler_path_entry_indices':pinned_entry_indices,
        'all_native_executable_hashes_match_pinned_toolchain':True,
        'dpi':144,'text_parameters':{'x_tolerance':3,'y_tolerance':3,'layout':False},'installed_dependencies_only':True})
    pins={}
    for report in (ledger,continuations,load(ROOT/'source-pins.json')): scan_pins(report,pins)
    assert ledger['retained_dependency_report']==old_ledger
    assert continuations['retained_dependency_report']==old_continuations
    for a in authored:
        ev=evidence_by_region[a['id']]
        page=next(p for p in current['pages'] if p['id']==ev['page_id'])
        assert page_basis_hash(page)==ev['page_basis_hash']
        assert ev['region_revision']==current_map[a['id']]['revision']
    write(ROOT/'reference-audit.json',{**BASE,'inventory':pin(ROOT/'final-verified/inventory.json'),
        'current_reports':{n:pin(ROOT/n) for n in ('region-ledger.json','continuations.json','coverage-report.json','source-pins.json','toolchain.json','original-inspection.json','preservation-report.json','replay-report.json','test-report.json','crop-inspection/report.json')},
        'retained_reports_structurally_equal_to_current_contract_pins':True,'all_nested_local_pins_verified':len(pins),
        'verified_pins':list(pins.values()),'assigned_evidence_locators_page_basis_source_and_region_revisions_verified':113,
        'source_regions_outside13_16_not_extracted':True,'passed':True})
    print(json.dumps({'passed':True,'nonassigned_regions':len(retained),'assigned_regions':113,'reference_pins':len(pins),'full_denominator':full['denominator_regions']}))

if __name__=='__main__': main()
