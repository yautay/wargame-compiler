"""Create and repeat a structural seal without changing accepted source bytes."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import copy,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'src'))
from wgc.contracts.source import canonical_bytes,seal_record
from wgc.export.source import historical,validate_export,PROFILE_SHA256
from wgc.inputs.snapshot import no_links,open_read,verify_tree_names
RUN=ROOT/'private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013'
PACKAGE=ROOT/'private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc'
INPUT=ROOT/'private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json'
SOURCE=ROOT/'private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json'
def read(p):return json.loads(Path(p).read_bytes())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def art(p):return {'path':Path(p).relative_to(ROOT).as_posix(),'sha256':sha(Path(p).read_bytes())}
def write(n,d):
 with (RUN/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2,ensure_ascii=False);f.write('\n')
audit=read(RUN/'independent-accounting.json');assert audit['result']=='pass'
assert audit['two_fresh_imports_match_accepted_bytes'] and audit['two_complete_outputs_and_packages_byte_identical']
original=read(PACKAGE/'source-ig.json')
parent=next(r for r in original['records'] if r['id']==original['snapshot_id'])
assert parent['data']['state']=='draft'
def sealed_bundle():
 bundle=copy.deepcopy(original);record=copy.deepcopy(parent)
 record['data']['state']='sealed'
 record['id']='wgc-snapshot:'+sha(canonical_bytes(record['data']))
 record['supersedes_refs']=[];record['lineage_refs']=[historical(parent)]
 sealed=seal_record(record)
 bundle['snapshot_id']=sealed['id'];bundle['records'].append(sealed)
 bundle['records'].sort(key=lambda r:(r['id'],r['revision_id']))
 validation=validate_export(bundle)
 assert sealed['data']['selected']==parent['data']['selected']
 assert sealed['data']['assessments']==parent['data']['assessments']
 assert sealed['data']['conflict_refs']==parent['data']['conflict_refs']
 assert validation['executable']['status']=='blocked' and not validation['semantic_acceptance_granted']
 prior={(r['id'],r['revision_id']):r for r in bundle['records']}
 assert all(prior[(r['id'],r['revision_id'])]==r for r in original['records'])
 return bundle,validation
coverage={'format':'wgc-input-coverage-ledger-1','input_manifest':art(INPUT),'source_manifest':art(SOURCE),
 'file_count':audit['manifest_entries'],'available_files':audit['available_files'],'missing_files':audit['missing_sources'],
 'record_counts':audit['independent_record_status_counts'],'field_count':audit['independent_field_count'],
 'unknown_root_count':audit['independent_unknown_root_count'],'unknown_location_count':audit['independent_unknown_location_count'],
 'kind_counts':audit['kind_counts'],'ledger':audit['ledger'],'unknown_roots':audit['independent_unknown_roots'],
 'unknown_field_locations':audit['independent_unknown_field_locations'],
 'oracle':'Exact path-set equality and raw YAML entity/field enumeration independent of importer counters; independent declared-field classification and raw subtree/hash/origin checks.',
 'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False}
files={'import.json':(RUN/'import-1.json').read_bytes(),
 'identity-registry.json':(PACKAGE/'identity-registry.json').read_bytes(),
 'references.json':(PACKAGE/'references.json').read_bytes(),
 'input-coverage-ledger.json':canonical_bytes(coverage)+b'\n'}
operations=[];snapshots=[]
for iteration in [1,2]:
 start=datetime.now(timezone.utc);tick=time.perf_counter();bundle,validation=sealed_bundle()
 payload={**files,'source-ig.json':canonical_bytes(bundle)+b'\n'}
 body={'format':'wgc-structural-snapshot-1','state':'sealed','seal_scope':'structural_integrity_only',
  'schema_profile_sha256':PROFILE_SHA256,'source_snapshot_id':bundle['snapshot_id'],
  'parent_export_manifest':art(PACKAGE/'manifest.json'),'input_manifest':art(INPUT),'selected_source_manifest':art(SOURCE),
  'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(payload.items())],
  'semantic_acceptance':'not_granted','publisher_source_coverage':'not_verified','executable_readiness':'blocked'}
 manifest={**body,'snapshot_id':'sha256:'+sha(canonical_bytes(body))}
 payload['manifest.json']=canonical_bytes(manifest)+b'\n'
 target=ROOT/'private/ig/projects/spqr/snapshots'/('sha256-'+manifest['snapshot_id'][7:])
 no_links(target)
 if not target.exists():
  target.mkdir(parents=True,exist_ok=False)
  for name,raw in payload.items():
   no_links(target/name)
   with (target/name).open('xb') as f:f.write(raw)
 verify_tree_names(target,set(payload))
 for name,raw in payload.items():
  with open_read(target/name) as f:assert f.read()==raw,name
 operation={'format':'wgc-structural-seal-operation-1','task':'IG-1E','iteration':iteration,
  'snapshot_manifest':art(target/'manifest.json'),'started_utc':start.isoformat(),
  'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-tick,
  'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'private/workflow/runs/IG-1D/resume-audit-20261013T134548Z/configuration-confirmed.json',
  'tokens':None,'cost':None,'operator_time_seconds':None,'semantic_acceptance_granted':False}
 write('seal-operation-'+str(iteration)+'.json',operation);operations.append(operation);snapshots.append(art(target/'manifest.json'))
 assert original==read(PACKAGE/'source-ig.json')
assert snapshots[0]==snapshots[1]
imported=read(RUN/'import-1.json')
edition_claims=[{'file':f['path'],'field':r['field'],'kind':r['kind'],
                'claims':{k:r['value'][k] for k in ['version','from_version','to_version','source'] if k in r['value']}}
 for f in imported['files'] for r in f['records'] if isinstance(r['value'],dict)
 and any(k in r['value'] for k in ['version','from_version','to_version','source'])]
gaps=[r for r in bundle['records'] if r['record_type']=='gap']
gap_counts=dict(Counter(r['data']['kind'] for r in gaps))
write('acceptance-report.json',{'task':'IG-1E','result':'technical_delivery_pending_independent_review',
 'snapshot':snapshots[0],'snapshot_directory':target.relative_to(ROOT).as_posix(),
 'independent_record_counts':audit['independent_record_status_counts'],'records':audit['independent_record_count'],
 'files':audit['manifest_entries'],'available_files':audit['available_files'],'missing_sources':audit['missing_sources'],
 'field_locations':audit['independent_field_count'],'unknown_roots':audit['independent_unknown_root_count'],
 'unknown_field_locations':audit['independent_unknown_location_count'],'selected_source_identity_to_wgu_original':'unknown',
 'two_imports_and_two_transforms_and_two_seals_byte_identical':True,
 'draft_snapshot_retained':historical(parent),'sealed_source_snapshot_id':bundle['snapshot_id'],
 'gap_counts':gap_counts,'missing_source_paths':[f['path'] for f in imported['files'] if f['availability']=='missing'],
 'edition_and_source_claims':edition_claims,'edition_compatibility':'unknown; no automatic precedence or cross-edition acceptance',
 'reconciliation_prerequisites':['Independent inventory of the full selected 5E rulebook and required source materials',
   'Recover/identify missing configured sources without guessing original identity',
   'Compare every KB claim, source locator, table/procedure and mixed-edition claim with exact source evidence',
   'Resolve navigation/subpoint/wildcard references and source discrepancies using explicit evidence',
   'Human review/acceptance of exact semantic revisions before formal semantics or executable compilation'],
 'validation':validation,'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,
 'executable_readiness_granted':False,'input_tokens':None,'output_tokens':None,'cost':None,'operator_time_seconds':None})
print(json.dumps({'snapshot':snapshots[0],'records':audit['independent_record_count'],
 'unknown_roots':audit['independent_unknown_root_count'],'unknown_locations':audit['independent_unknown_location_count'],
 'gap_counts':gap_counts,'repeatability':'pass'}),flush=True)
