"""Freeze exact first-cycle IG-1D repair and preserve parent/foundation versions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path.cwd();R=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def art(p):return {'path':p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix(),'sha256':sha(p)}
def write(n,d):
 with (R/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
scope=read(R/'repair-scope.json');parent=read(scope['parent_delivery']['path']);review=read(scope['parent_review']['path'])
baseline={b['original']['path']:b for b in read(R/'baseline-manifest.json')['files']}
rows=[]
for a in parent['artifacts']:
 path=Path(a['path'])
 if sha(path)==a['sha256']:verified=path
 else:
  b=baseline[a['path']];assert b['original']['sha256']==a['sha256']
  verified=Path(b['preserved_copy']['path']);assert sha(verified)==a['sha256']
 rows.append({**a,'verified_path':verified.as_posix()})
for a in review['artifacts']:assert sha(a['path'])==a['sha256']
q=read('docs/work/queue.json');protected=[]
for task in q['tasks']:
 if task['id'] in ['IG-1A','IG-1B','IG-1C']:
  assert task['status']=='done'
  accepted=read(next(e['evidence'] for e in reversed(task['events']) if e['to']=='accepted'))
  for a in accepted['artifacts']:assert sha(a['path'])==a['sha256'];protected.append(a)
write('preservation.json',{'parent_artifact_versions':rows,'all_parent_69_versions_preserved':True,
    'review_artifacts_unchanged':len(review['artifacts']),'foundation_artifacts_unchanged':len(protected)})
account=read(R/'full-export-accounting-final.json');assert account['result']=='pass'
prior_account=read('private/workflow/runs/IG-1D/preflight-20261013/full-export-accounting-final.json')
assert account['package']['manifest']==prior_account['package']['manifest']
checks=read(R/'captured-checks.json');assert all(c['exit_code']==0 for c in checks)
checkroot=Path('private/workflow/checks/active-39a4fb89432a4b458fb71adf87ce534f');result=read(checkroot/'result.json')
assert all(result[k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
checks+=[{'command':'.venv/Scripts/python.exe private/workflow/runs/IG-1D/repair-01-20261013/full_audit.py (normally reviewed native escalation)',
          'exit_code':0,'report':art(R/'full-export-accounting-final.json')},
         {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-1D','exit_code':0,'tests_passed':102,
          'reported_seconds':40.84,'result':art(checkroot/'result.json')}]
write('checks.json',checks)
write('configuration.json',{'model':'gpt-6.1-sol','reasoning':'high','source':'Earlier direct operator UI confirmation in this same ongoing executor conversation','operator_statement':'sol 6.1 high','same_session_continuity':True,'requested_or_observed_settings_change':False,'runtime_metadata':None,'tokens':None,'cost':None})
text='''# IG-1D first bounded repair delivery

Independent IG1D-R01/R02/R03/R04 are each at iteration 1 of maximum 2. The four
original independent failing probes remain unchanged and pass under executor
controls; only independent re-review can close findings.

R01 compares applicable anonymous fallback evidence against the same previous
candidate set before assigning. Contradictory label/endpoint/number versus substantive
evidence retains both candidate identities and exact observations as a gap. Explicit
hints can resolve the conflict without replacing allocations or altering raw values.
The earlier step-renumbering fixture assumed body evidence outranked conflicting
numbers; it now supplies explicit synthetic authoring bindings and keeps its exact
identity/raw-number assertions. A separate strict negative step-number/body conflict
test requires gaps. No assertion was weakened; the changed input condition is recorded.

R02 rejects all hint/lineage child overlap atomically before modifying previous
registry state. Disjoint many-to-many hints, keyed identical children and normal
decision replay remain supported. Neither recorded basis is silently discarded.

R03 resolves direct active allocations as well as unique aliases; colliding direct
IDs/aliases remain ambiguous and retired IDs are not active. Navigation and typed
candidate roles/cycle diagnostics remain separate from semantic approval. Both
endpoints still must resolve for a relationship candidate to be resolved.

R04 uses the stable unique merge-child receipt, kind/scope and child contract to
retain identity through correction/rename independently of content. Reusing a named
receipt with a changed operation/parent/basis contract rejects. Multiple-child/key
ambiguity remains a gap. Export retains exact historical parents and superseded child
revisions; no acceptance is transferred.

Controls: 93 public adapter/export tests plus 15 unchanged reviewer probes pass
(108 total). Current project check has 102 passing tests; queue/diff checks pass.
Full independent accounting, every manifest/record/field/binding comparison and two
canonical transformations/publications pass. The package manifest is byte-identical
to the accepted-for-review parent draft: 1692 records, 38206 locations, 18303 graph
records; no active identity gaps in this exact measured corpus. Adversarial collision
cases still produce gaps as required. This is not source-meaning acceptance.

All 69 parent artifact versions are verified at current or explicit preserved baseline
paths; all 42 independent review evidence artifacts and 182 accepted foundation
artifacts remain unchanged. Original schema/validator/approved export profile and
canonical run null timestamps remain unchanged. Actual operation/session measurements
remain outside canonical hashes. Previous packages/reports are preserved.

Only owned identity/reference modules and assigned synthetic tests changed. No new
dependency, neighboring write, history/archive read, new chat/agent/worktree/automation,
global setting, commit/push or gameplay runtime/LLM legality was introduced. Native
checks used narrowly reviewed local execution; real symlinks remain unmeasured/null.
Tokens, cost and operator time unavailable/null. Independent re-review and coordinator
acceptance/done remain pending. IG-1E planned; source coverage, human semantic approval
and executable readiness are not granted.
'''
(R/'report.md').write_bytes(text.encode('utf-8'))
cp=read(R/'checkpoint.json');end=datetime.now(timezone.utc)
write('measurement.json',{'started_utc':cp['started_utc'],'ended_utc':end.isoformat(),'wall_seconds':(end-datetime.fromisoformat(cp['started_utc'])).total_seconds(),
    'input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None,'native_file_symlink':None,'native_directory_symlink':None})
products=[Path('src/wgc/wgu_adapter/identity.py'),Path('src/wgc/wgu_adapter/references.py')]
products+=sorted(p for p in Path('src/wgc/export').glob('*') if p.is_file())
products+=sorted(Path('tests/wgu_adapter').glob('*.py'))+sorted(Path('tests/export').glob('*.py'))
package=Path(account['package']['package'])
paths=products+sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
paths+=sorted(p for p in package.glob('*') if p.is_file())+[Path(account['package']['operation']),Path(account['repeat_operation'])]
paths+=sorted(p for p in checkroot.glob('*') if p.is_file())
task=next(t for t in q['tasks'] if t['id']=='IG-1D')
write('delivery.json',{'role':'executor','actor':'ig1-stage-executor-20261013','task':'IG-1D',
    'summary':'First bounded repairs for four independent identity/decision/reference/merge-child findings; 108 strict public/reviewer controls, 102 project tests and complete private byte/field/binding accounting/reproducibility pass. Independent re-review pending.',
    'criteria':task['acceptance'],'artifacts':[art(p) for p in paths],'checks':checks,'model':'gpt-6.1-sol','reasoning':'high',
    'configuration_evidence':art(R/'configuration.json'),'input_packet':read(R/'packet.json'),
    'parent_delivery':scope['parent_delivery'],'parent_review':scope['parent_review'],'repair_findings':scope['finding_iterations'],
    'repair_cycles_per_finding':1,'semantic_acceptance_granted':False,'source_coverage_granted':False,'executable_readiness_granted':False,
    'unmet_lifecycle_gates':['Independent re-review','Coordinator acceptance/done']})
print('First IG-1D repair frozen',len(paths),'artifacts',sha(R/'delivery.json'))
