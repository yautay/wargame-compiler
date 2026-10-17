"""Independent complete ledger closure, direct mapping samples and two real seals."""
from collections import Counter
import copy
from datetime import datetime, timezone
import hashlib,json,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5];RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from wgc.export.source import validate_export
from wgc.inputs.snapshot import no_links,open_read,verify_tree_names

STORED=ROOT/'private/ig/projects/spqr/snapshots/sha256-4571340270f16519ee8207f0e474e6e71620ae11d74a1c787f273bb617a34fa7'
ACCEPT=ROOT/'private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013'
PACKAGE=ROOT/'private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc'
INPUT=ROOT/'private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json'
SOURCE=ROOT/'private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json'
started=datetime.now(timezone.utc);tick=time.perf_counter()
def read(p):return json.loads(p.read_bytes())
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def artifact(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p.read_bytes())}
def at(v,pointer):
    for part in pointer.split('/')[1:]:
        key=part.replace('~1','/').replace('~0','~')
        v=v[int(key)] if isinstance(v,list) else v[key]
    return v
def write(n,d):
    with (RUN/n).open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')

audit=read(RUN/'independent-accounting.json');assert audit['result']=='pass'
stored_audit=read(ACCEPT/'independent-accounting.json')
data_keys=['ledger','binding_ledger','unknown_locations','independent_unknown_roots','independent_unknown_field_locations',
    'kind_counts','independent_record_status_counts','independent_record_count','independent_field_count',
    'manifest_entries','available_files','missing_sources','independent_unknown_root_count','independent_unknown_location_count']
assert all(audit[k]==stored_audit[k] for k in data_keys)
assert (RUN/'import-1.json').read_bytes()==(RUN/'import-2.json').read_bytes()==(ACCEPT/'import-1.json').read_bytes()==(ACCEPT/'import-2.json').read_bytes()==(STORED/'import.json').read_bytes()
imported=read(RUN/'import-1.json');im=read(INPUT);sm=read(SOURCE)
assert sm['selection']['identity_to_wgu_original']=='unknown'
ledger=read(STORED/'input-coverage-ledger.json')
expected_coverage={'format':'wgc-input-coverage-ledger-1','input_manifest':artifact(INPUT),'source_manifest':artifact(SOURCE),
    'file_count':audit['manifest_entries'],'available_files':audit['available_files'],'missing_files':audit['missing_sources'],
    'record_counts':audit['independent_record_status_counts'],'field_count':audit['independent_field_count'],
    'unknown_root_count':audit['independent_unknown_root_count'],'unknown_location_count':audit['independent_unknown_location_count'],
    'kind_counts':audit['kind_counts'],'ledger':audit['ledger'],'unknown_roots':audit['independent_unknown_roots'],
    'unknown_field_locations':audit['independent_unknown_field_locations'],
    'oracle':'Exact path-set equality and raw YAML entity/field enumeration independent of importer counters; independent declared-field classification and raw subtree/hash/origin checks.',
    'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False}
assert ledger==expected_coverage
assert canonical(expected_coverage)+b'\n'==(STORED/'input-coverage-ledger.json').read_bytes()
assert {f['path'] for f in im['files']}=={f['path'] for f in ledger['ledger']}=={f['path'] for f in imported['files']}
for name in ['identity-registry.json','references.json']:
    assert (STORED/name).read_bytes()==(PACKAGE/name).read_bytes()
draft=read(PACKAGE/'source-ig.json');bundle=read(STORED/'source-ig.json')
parent=next(r for r in draft['records'] if r['id']==draft['snapshot_id'])
sealed=next(r for r in bundle['records'] if r['id']==bundle['snapshot_id'])
assert parent['data']['state']=='draft' and sealed['data']['state']=='sealed'
parent_ref={'mode':'historical','id':parent['id'],'record_type':'snapshot','revision_id':parent['revision_id']}
assert sealed['lineage_refs']==[parent_ref] and sealed['supersedes_refs']==[]
assert {k:v for k,v in sealed['data'].items() if k!='state'}=={k:v for k,v in parent['data'].items() if k!='state'}
assert sealed['id']=='wgc-snapshot:'+sha(canonical(sealed['data']))
assert len(bundle['records'])==len(draft['records'])+1
store={(r['id'],r['revision_id']):r for r in bundle['records']}
assert len(store)==len(bundle['records']) and all(store[(r['id'],r['revision_id'])]==r for r in draft['records'])
selected={r['id']:store[(r['id'],r['revision_id'])] for r in sealed['data']['selected']}
for r in bundle['records']:
    digest=sha(canonical({k:v for k,v in r.items() if k not in ['revision_id','content_hash']}))
    assert r['content_hash']==digest and r['revision_id']=='sha256:'+digest
    if r['record_type']=='node':
        for a in r['data']['aspects']:assert a['aspect_hash']==sha(canonical({k:v for k,v in a.items() if k!='aspect_hash'}))
def closure(v):
    if isinstance(v,dict):
        if v.get('mode') in ['active','historical']:
            t=selected[v['id']] if v['mode']=='active' else store[(v['id'],v['revision_id'])]
            assert t['record_type']==v['record_type']
            if 'aspect_id' in v:assert any(a['aspect_id']==v['aspect_id'] for a in t['data']['aspects'])
        for x in v.values():closure(x)
    elif isinstance(v,list):
        for x in v:closure(x)
closure(bundle)
validation=validate_export(bundle)
assert validation['structural_validation']=='passed' and validation['executable']['status']=='blocked' and not validation['semantic_acceptance_granted']
assert sealed['data']['assessments']['coverage_refs']==sealed['data']['assessments']['semantic_review_refs']==[]
assert all(r['data']['model'] is None and r['data']['started_utc'] is None and r['data']['ended_utc'] is None for r in selected.values() if r['record_type']=='run')
gaps=[r for r in selected.values() if r['record_type']=='gap']
assert any(r['data']['kind']=='missing_source' for r in gaps)
profile=selected[sealed['data']['profile_ref']['id']]
assert profile['data']['edition']=='mixed-unverified'
assert all(c['knowledge']=='unknown' for c in profile['data']['compatibility_decisions'])
manifest=read(STORED/'manifest.json')
assert manifest['snapshot_id']=='sha256:'+sha(canonical({k:v for k,v in manifest.items() if k!='snapshot_id'}))
assert STORED.name=='sha256-'+manifest['snapshot_id'][7:]
assert manifest['format']=='wgc-structural-snapshot-1' and manifest['state']=='sealed' and manifest['seal_scope']=='structural_integrity_only'
assert manifest['semantic_acceptance']=='not_granted' and manifest['publisher_source_coverage']=='not_verified' and manifest['executable_readiness']=='blocked'
assert manifest['schema_profile_sha256']==sha((ROOT/'src/wgc/export/source-export.schema.json').read_bytes())
assert manifest['source_snapshot_id']==sealed['id']
assert manifest['input_manifest']==artifact(INPUT) and manifest['selected_source_manifest']==artifact(SOURCE) and manifest['parent_export_manifest']==artifact(PACKAGE/'manifest.json')
verify_tree_names(STORED,{a['path'] for a in manifest['files']}|{'manifest.json'})
for a in manifest['files']:
    with open_read(STORED/a['path']) as f:raw=f.read()
    assert len(raw)==a['bytes'] and sha(raw)==a['sha256']
assert (STORED/'manifest.json').read_bytes()==canonical(manifest)+b'\n'

# Two separate reconstruction/publication runs from the independently checked
# raw import/ledger and accepted draft; do not call the executor seal helper.
operations=[]
for iteration in [1,2]:
    operation_start=datetime.now(timezone.utc);operation_tick=time.perf_counter()
    child=copy.deepcopy(parent);child['data']['state']='sealed'
    child['id']='wgc-snapshot:'+sha(canonical(child['data']))
    child['supersedes_refs']=[];child['lineage_refs']=[parent_ref]
    child['content_hash']=sha(canonical({k:v for k,v in child.items() if k not in ['revision_id','content_hash']}))
    child['revision_id']='sha256:'+child['content_hash']
    recreated={**copy.deepcopy(draft),'snapshot_id':child['id'],'records':sorted(draft['records']+[child],key=lambda r:(r['id'],r['revision_id']))}
    assert recreated==bundle
    assert validate_export(recreated)['executable']['status']=='blocked'
    payload={'import.json':(RUN/('import-'+str(iteration)+'.json')).read_bytes(),
        'identity-registry.json':(PACKAGE/'identity-registry.json').read_bytes(),
        'references.json':(PACKAGE/'references.json').read_bytes(),
        'input-coverage-ledger.json':canonical(expected_coverage)+b'\n',
        'source-ig.json':canonical(recreated)+b'\n'}
    body={'format':'wgc-structural-snapshot-1','state':'sealed','seal_scope':'structural_integrity_only',
        'schema_profile_sha256':sha((ROOT/'src/wgc/export/source-export.schema.json').read_bytes()),
        'source_snapshot_id':child['id'],'parent_export_manifest':artifact(PACKAGE/'manifest.json'),
        'input_manifest':artifact(INPUT),'selected_source_manifest':artifact(SOURCE),
        'files':[{'path':n,'bytes':len(raw),'sha256':sha(raw)} for n,raw in sorted(payload.items())],
        'semantic_acceptance':'not_granted','publisher_source_coverage':'not_verified','executable_readiness':'blocked'}
    recreated_manifest={**body,'snapshot_id':'sha256:'+sha(canonical(body))}
    assert recreated_manifest==manifest
    payload['manifest.json']=canonical(recreated_manifest)+b'\n'
    dest=RUN/'seals'/('repeat-'+str(iteration))/('sha256-'+recreated_manifest['snapshot_id'][7:])
    no_links(dest);dest.mkdir(parents=True,exist_ok=False)
    for n,raw in payload.items():
        assert raw==(STORED/n).read_bytes()
        no_links(dest/n)
        with (dest/n).open('xb') as f:f.write(raw)
    verify_tree_names(dest,set(payload))
    for n,raw in payload.items():
        with open_read(dest/n) as f:assert f.read()==raw
    operation={'iteration':iteration,'snapshot_manifest':artifact(dest/'manifest.json'),'started_utc':operation_start.isoformat(),
        'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-operation_tick,
        'review_actor':'ig1e-independent-reviewer-20261013T150750Z','configuration_continuity':read(RUN/'checkpoint.json')['configuration_evidence'],
        'model':'gpt-6.1-sol','reasoning':'high','tokens':None,'cost':None,'operator_seconds':None}
    write('independent-seal-operation-'+str(iteration)+'.json',operation);operations.append(operation)
assert operations[0]['snapshot_manifest']['sha256']==operations[1]['snapshot_manifest']['sha256']==artifact(STORED/'manifest.json')['sha256']

report=read(ACCEPT/'acceptance-report.json')
missing=[f['path'] for f in im['files'] if f['availability']=='missing']
assert report['missing_source_paths']==missing and len(missing)==audit['missing_sources']
claims=[{'file':f['path'],'field':r['field'],'kind':r['kind'],
    'claims':{k:r['value'][k] for k in ['version','from_version','to_version','source'] if k in r['value']}}
    for f in imported['files'] for r in f['records'] if isinstance(r['value'],dict) and any(k in r['value'] for k in ['version','from_version','to_version','source'])]
assert claims==report['edition_and_source_claims']
assert report['selected_source_identity_to_wgu_original']=='unknown' and report['reconciliation_prerequisites']
assert report['gap_counts']==dict(Counter(r['data']['kind'] for r in gaps))

# Direct samples select one actual source-derived mapping per representative kind
# with exact payload hashes and preserved binding targets, written privately.
samples=[]
for kind in ['rule','step','term','terminology','relation','auxiliary']:
    f,r=next((f,r) for f in imported['files'] for r in f['records'] if r['kind']==kind)
    doc=f['document'];value=at(doc,r['field']) if doc is not None else None
    assert value==r['value']
    row=next(row for lf in audit['ledger'] if lf['path']==f['path'] for row in lf['records'] if row['field']==r['field'] and row['kind']==kind)
    assert row['value_sha256']==sha(canonical(value))
    bindings=[b for b in audit['binding_ledger'] if b['origin']['relative_path']==f['path'] and b['origin']['field_locator']==r['field'] and any(t['id']==row['identity'] for t in b['target_refs'])]
    assert bindings
    samples.append({'file':f['path'],'field':r['field'],'kind':kind,'status':r['status'],'input_sha256':f['sha256'],
        'identity':row['identity'],'origin_key':row['origin_key'],'parent_field':row['parent_field'],
        'value_sha256':row['value_sha256'],'bindings':bindings})
write('mapping-samples.json',{'samples':samples,'all_direct_mapping_checks_passed':True})
result={'result':'pass','started_utc':started.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-tick,
    'entire_delivered_file_record_field_binding_unknown_ledger_matches_independent_ledger':True,
    'two_independent_actual_seals_equal_frozen_snapshot':True,'snapshot_manifest':artifact(STORED/'manifest.json'),
    'draft_snapshot_retained':parent_ref,'original_graph_record_count':len(draft['records']),'sealed_graph_record_count':len(bundle['records']),
    'selected_revision_count':len(selected),'gap_counts':dict(Counter(r['data']['kind'] for r in gaps)),
    'missing_source_paths':missing,'edition_source_claim_count':len(claims),'all_edition_source_claims_exactly_retained':True,
    'directory_identity_and_every_file_hash_verified':True,'canonical_clocks_null':True,
    'sample_count':len(samples),'operations':operations,
    'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False,
    'tokens':None,'cost':None,'operator_seconds':None}
write('independent-seal.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['operations','missing_source_paths']}))
