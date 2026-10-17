"""Freeze complete IG-1E technical delivery and all retained prerequisite bytes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent
DATA=ROOT/'private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013'
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def art(p):
 p=Path(p);return {'path':(p.relative_to(ROOT) if p.is_absolute() else p).as_posix(),'sha256':sha(p)}
def write(n,d):
 with (RUN/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
q=read('docs/work/queue.json');task=next(t for t in q['tasks'] if t['id']=='IG-1E')
assert task['status']=='in_progress'
protected=[];stage=[]
for t in q['tasks']:
 if t['id'] in ['IG-1A','IG-1B','IG-1C','IG-1D']:
  assert t['status']=='done'
  accepted_event=next(e for e in reversed(t['events']) if e['to']=='accepted')
  delivery_event=next(e for e in reversed(t['events']) if e['to']=='review')
  accepted=read(accepted_event['evidence'])
  for a in accepted['artifacts']:assert sha(a['path'])==a['sha256'],a['path'];protected.append(a)
  stage.append({'task':t['id'],'status':'done','delivery':art(delivery_event['evidence']),
                'acceptance':art(accepted_event['evidence']),'criteria':t['acceptance']})
pins=read(RUN/'input-contract.json')['pinned_inputs']
for a in pins:assert sha(a['path'])==a['sha256'],a['path']
write('preservation.json',{'accepted_foundation_artifacts':protected,'pinned_inputs':pins,
 'all_exact_prerequisites_unchanged':True,'prerequisite_task_gates':stage})
checks=[read(RUN/(n+'-check.json')) for n in ['explicit','accounting','seal','project','diff']]
assert all(c['exit_code']==0 for c in checks)
report=read(DATA/'acceptance-report.json');assert report['two_imports_and_two_transforms_and_two_seals_byte_identical']
snapshot=ROOT/report['snapshot_directory'];manifest=read(snapshot/'manifest.json')
assert manifest['state']=='sealed' and manifest['semantic_acceptance']=='not_granted'
assert sha(snapshot/'manifest.json')==report['snapshot']['sha256']
for f in manifest['files']:assert sha(snapshot/f['path'])==f['sha256'],f['path']
root=Path(re.search(r'LOG_ROOT=(.+)',(RUN/'project.log').read_text(encoding='utf-8-sig')).group(1).strip())
assert all(read(root/'result.json')[k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
start=datetime.fromisoformat(read(RUN/'checkpoint.json')['started_utc']);end=datetime.now(timezone.utc)
write('measurement.json',{'started_utc':start.isoformat(),'ended_utc':end.isoformat(),
 'wall_seconds':(end-start).total_seconds(),'input_tokens':None,'output_tokens':None,'cost':None,'operator_time_seconds':None})
text=f'''# IG-1E full-input structural acceptance delivery

The independent complete path-set inventory accounts for {report['files']} manifest
entries ({report['available_files']} available, {report['missing_sources']} missing).
Two new imports match the accepted IG-1C bytes. Independently enumerated record
statuses are {report['independent_record_counts']}; {report['field_locations']} YAML
field/container locations, {report['unknown_roots']} unknown roots and
{report['unknown_field_locations']} unknown subtree locations are retained.
Every raw byte/hash, entity, field mark/value and origin-binding subtree is checked.
Two full canonical transforms and real publications match the accepted IG-1D draft.

Two structural seals are byte-identical. The immutable snapshot directory is
{report['snapshot_directory']}; its manifest hash is {report['snapshot']['sha256']}.
The new selected snapshot is sealed; the exact draft snapshot remains in history
with a historical lineage reference. Every selected source revision, gap, profile
and readiness assessment is unchanged. The dedicated packaging manifest pins the
original input/source manifests, canonical import, registry, references and complete
independent ledger. Actual operational clocks/configuration are separate sidecars.

Missing configured sources and all original edition/source/version claims remain
in the private ledger/report and registry. The selected 5E source has unknown
identity to the missing WGU original; compatibility across edition claims is unknown.
No source text interpretation, automatic precedence or semantic approval is inferred.

Validation: 106 public integration/adapter/export tests and 102 project tests passed.
Full private accounting, fresh imports, two transforms/publications, two seals and
diff/queue checks passed. The full accounting oracle retains prior assertions and adds
independent file-set, status and unknown-field classification. All accepted IG-1A–D
artifact bytes and current input pins are verified unchanged in preservation.json.

IG-1A–D are done with independent technical acceptance. IG-1E awaits independent
review of this exact frozen delivery and coordinator acceptance/done. The final
full-stage handoff will be a separate coordinator closure artifact after those gates.
The snapshot seal means structural integrity. Publisher coverage, human semantic
acceptance and executable readiness remain ungranted; later exact source inventory,
reconciliation and authorized human meaning review are explicit prerequisites.
No IG-2/runtime/compiler/POC work, neighboring writes, history reads, commit or push.
'''
with (RUN/'delivery-handoff.md').open('x',encoding='utf-8',newline='\n') as f:f.write(text)
paths=set(Path('tests/integration').glob('*.py'))
for directory in [RUN,DATA,snapshot]:paths.update(p for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
paths.update(p for p in root.glob('*') if p.is_file())
write('delivery.json',{'role':'executor','actor':'ig1-continuation-executor-20261013','task':'IG-1E',
 'summary':'Complete independent file/record/unknown-field accounting, two fresh imports and canonical transforms/publications, public synthetic integration controls and repeatable sealed STRUCTURAL snapshot with all gaps and edition uncertainty preserved. Independent review pending.',
 'criteria':task['acceptance'],'artifacts':[art(p) for p in sorted(paths)],'checks':checks,
 'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':read(RUN/'checkpoint.json')['configuration_evidence'],
 'input_packet':read(RUN/'checkpoint.json')['input_packet'],'snapshot':report['snapshot'],
 'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False})
print(json.dumps({'delivery':art(RUN/'delivery.json'),'artifacts':len(paths),'snapshot':report['snapshot']}))
