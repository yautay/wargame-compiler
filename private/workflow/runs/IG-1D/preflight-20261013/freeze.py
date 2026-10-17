"""Freeze complete IG-1D implementation and measured canonical package evidence."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path.cwd();R=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def art(p):return {'path':p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix(),'sha256':sha(p)}
def write(n,d):
 with (R/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
report=read(R/'full-export-accounting-final.json');assert report['result']=='pass'
assert report['repeat_canonical_files_byte_identical'] and report['all_values_and_field_subtrees_retained']
package=Path(report['package']['package'])
checks=read(R/'captured-checks.json');assert all(c['exit_code']==0 for c in checks)
checkroot=Path('private/workflow/checks/active-05983aca87d741b0bc505acd28f822cb')
result=read(checkroot/'result.json');assert all(result[k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
checks+= [{'command':'.venv/Scripts/python.exe private/workflow/runs/IG-1D/preflight-20261013/full_audit_final.py (normally reviewed native escalation)',
           'exit_code':0,'report':art(R/'full-export-accounting-final.json')},
          {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-1D','exit_code':0,'tests_passed':102,
           'reported_seconds':40.14,'result':art(checkroot/'result.json')}]
write('checks.json',checks)
protected=[]
q=read('docs/work/queue.json')
for name in ['IG-1A','IG-1B','IG-1C']:
 task=next(t for t in q['tasks'] if t['id']==name);assert task['status']=='done'
 accepted=read(next(e['evidence'] for e in reversed(task['events']) if e['to']=='accepted'))
 for a in accepted['artifacts']:assert sha(a['path'])==a['sha256'];protected.append(a)
write('foundation-preservation.json',{'protected_current_accepted_artifact_count':len(protected),'all_hashes_match':True,'artifacts':protected})
write('configuration.json',{'model':'gpt-6.1-sol','reasoning':'high','source':'Earlier direct operator UI observation in this same ongoing executor conversation','operator_statement':'sol 6.1 high','same_session_continuity':True,'configuration_change_requested_or_observed':False,'runtime_metadata':None,'tokens':None,'cost':None})
text='''# IG-1D technical delivery

Persisted allocation identities and origin keys use namespace counters. Current
content descriptors, declared labels, local numbering and raw byte fingerprints
justify unambiguous rematches; they never generate IDs. Reorder/insert/correction,
unambiguous rename and file move preserve identities. Ambiguous collisions and
insufficient rename evidence remain gaps. Exact null values and opaque auxiliary
byte evidence participate correctly in repeated-input matching.

Explicit many-to-many binding and split/merge APIs require recorded bases. Children
receive new allocations with parent lineage. Decision/child receipts make replay
idempotent; identical children require explicit persistent child keys. Old identities,
input coordinates and bindings remain in the canonical registry. Exact prior source
revisions remain in export lineage/history when the previous bundle is supplied.
No prior approval transfers to a new revision or child.

Reference diagnostics preserve navigation versus typed candidates, raw locators,
exact current IDs/unique aliases and explicit scope bases. Wildcards/subpoints do
not automatically expand or resolve to their base. Unknown endpoints remain gaps;
both endpoints must resolve before a candidate can be marked resolved. Iterative
cycle diagnostics allow cyclic rule/procedure descriptions without a false DAG gate.

The operator approved the concrete wgc-source-export-1 profile after identifying
source-v1's mandatory canonical run timestamp conflict. Its only structural changes
are explicit version identity and null canonical run timestamps. All other mechanical,
reference/hash/review/readiness constraints and the frozen validator remain unchanged.
Actual configuration/time/usage evidence is operational and outside canonical hashes.
Original IG-1A/B/C deliveries and reports remain byte-preserved.

The canonical registry holds every full raw observation and exact bound subtree;
the source graph exposes stable top-field aspects and dedicated clause/concept/
procedure/step/table descriptions. Publisher-source meaning, composition, table
axes/cells, evidence and units remain explicitly unreconciled. No PDF page, human
decision or accepted question answer is fabricated. A table's unreconciled axis is
an explicit placeholder, not a coverage claim. Original raw bytes and all nested
field marks remain in the pinned complete input/import.

Private audit: 1692 input records and 38206 field/container locations independently
compared against complete values, exact root/top-field bindings and field subtrees.
36 configured sources remain missing; promoted PDF identity to original is unknown.
Two complete imports of identical pinned data produce byte-identical source graph,
identity registry and references; publication reuses the exact canonical package.
Earlier draft package/operation measurements are preserved. Final binding observation
values match their subtree instead of unnecessarily duplicating whole entities.

Controls: 84 explicit adapter/export tests (including 59 frozen IG-1C controls) and
102 project tests pass; queue/diff checks pass. The first full audit's platform-codec
error was fixed by explicit UTF-8. Strict local regressions exposed and fixed raw-null
replay, repeated lineage allocation and unresolved-from labeling. Their assertions
were retained. No independent IG-1D repair cycle has been consumed yet.

Source package remains STRUCTURAL DRAFT. Publisher coverage, human semantic
acceptance and executable readiness are separate and not granted. Independent
technical review and coordinator acceptance/done remain outstanding. IG-1E planned.
Native no-follow snapshot/package checks used normally reviewed narrow local
escalation; actual symlink behavior is unmeasured/null. Unexposed usage/cost/operator
time remain null. No neighboring writes, archive/Git-history access, commits/pushes,
new agents/worktrees/automations or unrelated API calls occurred.
'''
(R/'report.md').write_bytes(text.encode('utf-8'))
checkpoint=read(R/'checkpoint.json');end=datetime.now(timezone.utc)
write('measurement.json',{'started_utc':checkpoint['started_utc'],'ended_utc':end.isoformat(),
    'wall_seconds':(end-datetime.fromisoformat(checkpoint['started_utc'])).total_seconds(),
    'input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None,
    'native_file_symlink':None,'native_directory_symlink':None})
products=[Path('src/wgc/wgu_adapter/identity.py'),Path('src/wgc/wgu_adapter/references.py')]+sorted(p for p in Path('src/wgc/export').glob('*') if p.is_file())
products+=[Path('tests/wgu_adapter/test_identity.py'),Path('tests/wgu_adapter/test_references.py'),Path('tests/export/test_source.py')]
paths=products+sorted(p for p in R.glob('*') if p.is_file())+sorted(p for p in package.glob('*') if p.is_file())
paths+=[Path(report['package']['operation']),Path(report['repeat_operation'])]
paths+=sorted(p for p in checkroot.glob('*') if p.is_file())
task=next(t for t in q['tasks'] if t['id']=='IG-1D')
write('delivery.json',{'role':'executor','actor':'ig1-stage-executor-20261013','task':'IG-1D',
    'summary':'Persisted identities/lineage and exact reference diagnostics with deterministic operator-approved structural export; all 1692 input records and 38206 field locations retained, repeated canonical files identical; 84 explicit and 102 project tests pass. Independent review pending.',
    'criteria':task['acceptance'],'artifacts':[art(p) for p in paths],'checks':checks,
    'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':art(R/'configuration.json'),
    'input_packet':checkpoint['input_packet'],'operator_profile_approval':art(R/'operator-profile-approval.json'),
    'unmet_lifecycle_gates':['Independent technical review','Coordinator acceptance/done'],
    'semantic_acceptance_granted':False,'source_coverage_granted':False,'executable_readiness_granted':False})
print('IG-1D delivery frozen',len(paths),'artifacts',sha(R/'delivery.json'))
