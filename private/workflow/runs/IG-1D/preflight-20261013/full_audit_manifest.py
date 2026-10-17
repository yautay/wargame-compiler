"""Full private export and independent observations/field-binding accounting."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import hashlib,json,sys,time
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'src'))
from wgc.contracts.source import canonical_bytes
from wgc.export.source import build,validate_export
from wgc.export.storage import publish
from wgc.inputs.snapshot import verify_snapshot
from wgc.wgu_adapter.identity import locator

R=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,d):
 with (R/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
started=datetime.now(timezone.utc);clock=time.monotonic()
input_path=Path('private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json')
assert sha(input_path)=='2999d63c680b4c52a095e0edb18952c70eefdf4baf7c2e01481840cda18ca61a'
imported=read(input_path)
ip=Path('private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df')
sp=Path('private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008')
im=verify_snapshot(ip);sm=verify_snapshot(sp)
assert sm['selection']['identity_to_wgu_original']=='unknown'
kwargs={'namespace':'wgu.spqr','source_manifest':sm,
        'input_manifest_sha256':sha(ip/'manifest.json'),'source_manifest_sha256':sha(sp/'manifest.json')}
one=build(imported,read(R/'initial-registry.json'),**kwargs)
print('First full source export built',len(one['bundle']['records']),'records',flush=True)
two=build(imported,one['registry'],previous_bundle=one['bundle'],**kwargs)
for key in ['bundle','registry','references']:
 assert canonical_bytes(one[key])==canonical_bytes(two[key]),key+' changed on identical repeated input'
assignments={a['locator']:a for a in one['assignments']}
entries={e['id']:e for e in one['registry']['entries']};gaps={g['id']:g for g in one['registry']['gaps']}
store={(r['id'],r['revision_id']):r for r in one['bundle']['records']}
snapshot=next(r for r in one['bundle']['records'] if r['id']==one['bundle']['snapshot_id'])
current={r['id']:store[(r['id'],r['revision_id'])] for r in snapshot['data']['selected']}
bindings=[r['data'] for r in current.values() if r['record_type']=='origin_binding']
binding_by_origin={}
for b in bindings:binding_by_origin.setdefault((b['input_snapshot_id'],b['relative_path'],b['field_locator']),[]).append(b)
def field_value(value,path):
 if not path:return value
 for key in path.split('/')[1:]:
  key=key.replace('~1','/').replace('~0','~')
  value=value[int(key)] if isinstance(value,list) else value[key]
 return value
ledger=[];records=0;fields=0;kind_counts=Counter()
for f in imported['files']:
 row={'path':f['path'],'availability':f['availability'],'record_count':len(f['records']),'field_count':len(f['fields']),'records':[]}
 if f['availability']=='available':
  assert sha(ip/f['blob_path'])==f['sha256']
 for r in f['records']:
  a=assignments[locator(f['path'],r['field'])]
  targets=a['ids'] or [a['gap_id']]
  observations=[o for target in targets for o in (entries[target]['observations'] if target in entries else gaps[target]['observations'])
                if o['origin']['relative_path']==f['path'] and o['origin']['field_locator']==r['field']]
  assert observations and all(o['value']==r['value'] for o in observations)
  bound=binding_by_origin[(imported['input_snapshot_id'],f['path'],'json-pointer:'+r['field'])]
  assert sum({ref['id'] for ref in binding['ig_refs']}==set(targets) for binding in bound)==1
  row['records'].append({'field':r['field'],'kind':r['kind'],'source_status':r['status'],
                         'target_ids':targets,'identity_status':'ambiguous' if a['gap_id'] else 'assigned',
                         'value_sha256':hashlib.sha256(canonical_bytes(r['value'])).hexdigest()})
  records+=1;kind_counts[r['kind']]+=1
 for field in f['fields']:
  pointer=field['field'];owners=[r for r in f['records'] if pointer==r['field'] or pointer.startswith(r['field']+'/')]
  if owners:
   owner=max(owners,key=lambda r:len(r['field']))
   assert field_value(owner['value'],pointer[len(owner['field']):])==field_value(f['document'],pointer)
   a=assignments[locator(f['path'],owner['field'])]
   targets=a['ids'] or [a['gap_id']]
   assert all(target in current for target in targets)
  else:
   # Collection/root containers are preserved by the exact whole-file source binding
   # and its frozen bytes, not assigned invented semantic identities.
   assert f['availability']=='available' and f['sha256']
   assert any(b['input_snapshot_id']==imported['input_snapshot_id'] and b['relative_path']==f['path']
              and b['field_locator']=='json-pointer:' for b in bindings)
  fields+=1
 ledger.append(row)
assert records==sum(len(f['records']) for f in imported['files'])==imported['record_total']
assert fields==sum(len(f['fields']) for f in imported['files'])
for e in one['registry']['entries']:
 if not e['active'] or e['kind']!='binding':continue
 for o in e['observations']:
  if o['origin']['relative_path']=='manifest.json' and o['origin']['input_snapshot_id'] in (im['snapshot_id'],sm['snapshot_id']):
   metadata=im if o['origin']['input_snapshot_id']==im['snapshot_id'] else sm
   assert o['value']==field_value(metadata,o['origin']['field_locator'])
   continue
  f=next((f for f in imported['files'] if f['path']==o['origin']['relative_path'] and o['origin']['input_snapshot_id']==imported['input_snapshot_id']),None)
  if f is None or f['availability']!='available':continue
  if o['origin']['field_locator']=='' and f['document'] is None:assert o['value'] is None
  elif f['document'] is not None:assert o['value']==field_value(f['document'],o['origin']['field_locator'])
result=publish(one,'private/ig/projects/spqr/records/exports',operation_evidence={
    'task':'IG-1D','model':'gpt-6.1-sol','reasoning':'high',
    'configuration_source':'Earlier direct operator UI confirmation in same ongoing executor conversation',
    'operator_profile_approval':str(R/'operator-profile-approval.json')})
repeated=publish(two,'private/ig/projects/spqr/records/exports',operation_evidence={'task':'IG-1D','purpose':'independent repeated publication'})
assert result['manifest']==repeated['manifest'] and result['package']==repeated['package']
report={'result':'pass','package':result,'repeat_operation':repeated['operation'],
    'independent_record_count':records,'independent_field_count':fields,'kind_counts':dict(kind_counts),
    'identity_entry_count':len(entries),'active_identity_gaps':sum(g['active'] for g in gaps.values()),
    'source_graph_record_count':len(one['bundle']['records']),'reference_diagnostic_count':len(one['references']['diagnostics']),
    'allowed_cycles':one['references']['cycles'],'validation':one['validation'],
    'all_values_and_field_subtrees_retained':True,'repeat_canonical_files_byte_identical':True,
    'operational_timestamps_outside_canonical_hashes':True,'identity_to_wgu_original':'unknown',
    'missing_sources':sum(f['availability']=='missing' for f in imported['files']),
    'ledger':ledger,'started_utc':started.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
    'wall_seconds':time.monotonic()-clock,'tokens':None,'cost':None,'operator_seconds':None,
    'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False}
write('full-export-accounting-final.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ['ledger','validation','package','allowed_cycles']}),flush=True)
