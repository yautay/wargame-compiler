"""Freeze first bounded repair with preserved parent artifact versions."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path.cwd();R=Path(__file__).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def art(p):return {'path':p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix(),'sha256':sha(p)}
def write(n,d):
 with (R/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
scope=read(R/'repair-scope.json');parent=read(scope['parent_delivery']['path'])
baseline=read(R/'baseline-manifest.json')['files'];mapping={x['original']['path']:x for x in baseline}
preserved=[]
for a in parent['artifacts']:
 p=Path(a['path'])
 if sha(p)==a['sha256']:preserved.append({**a,'verified_path':a['path'],'version':'current_unchanged'})
 else:
  b=mapping[a['path']];assert b['original']['sha256']==a['sha256']
  assert sha(b['preserved_copy']['path'])==a['sha256']
  preserved.append({**a,'verified_path':b['preserved_copy']['path'],'version':'preserved_parent_copy'})
review=read(scope['review']['path'])
for a in review['artifacts']:assert sha(a['path'])==a['sha256']
foundation=read('private/workflow/runs/IG-1C/stage-20261013/foundation-audit.json')
for a in foundation['artifacts']:assert sha(a['verified_path'])==a['sha256']
write('preservation.json',{'parent_full_manifest':preserved,'parent_artifact_count':len(preserved),'review_artifacts_unchanged':len(review['artifacts']),'foundation_artifacts_unchanged':len(foundation['artifacts']),'prior_import_outputs_unchanged':True})
out=Path('private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013')
account=read(out/'independent-accounting.json');assert account['result']=='pass'
assert (Path('private/ig/projects/spqr/runs/import/ig1c-repair01-20261013')/'import.json').read_bytes()==(out/'import.json').read_bytes()
checkroot=Path('private/workflow/checks/active-b54e78e615d14ca9ba260b8458848c5c');c=read(checkroot/'result.json')
assert all(c[k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
checks=read(R/'final-checks.json')+[{'command':'.venv/Scripts/python.exe private/workflow/runs/IG-1C/repair-01-20261013/full_audit_final.py (normally reviewed native escalation)','exit_code':0,'report':art(out/'independent-accounting.json')},{'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-1C','exit_code':0,'tests_passed':102,'reported_seconds':46.02,'result':art(checkroot/'result.json')}]
write('checks.json',checks)
cfg=read('private/workflow/runs/IG-1C/stage-20261013/configuration.json')
write('configuration.json',{**cfg,'same_ongoing_executor_conversation':True,'earlier_direct_operator_statement_used':'sol 6.1 high','configuration_change_requested_or_observed':False,'reviewer_confirmation_not_used_for_executor':True})
report='''# IG-1C first bounded repair delivery

Independent findings IG1C-R01, IG1C-R02 and IG1C-R03 are each at repair iteration 1
of maximum 2. The parent review and delivery remain byte-preserved. Re-review must
verify these new hashes; passing executor probes does not close the findings.

R01: normalize malformed built-in bool/timestamp/int/float/binary scalar constructor
failures into located ParseError. Normalization is restricted to those scalar tags,
so unrelated implementation defects propagate. Inventory node pointers before scalar
construction; retain exact file/field/line/column. Multi-file sealed-snapshot testing
proves a malformed scalar is an accounted error while subsequent valid/raw files
still survive. Existing unsafe-tag, duplicate-key and alias/depth controls stay strict.

R02: embed the exact operator-pinned WGU structural schema in the owned importer
with its source hash; no neighboring runtime reads or new dependencies. Validate
known optional scalar types, enums, identifiers and nested shapes and canonical file
metadata. Unknown extensions remain preserved. The deliberate existing integer
step.n extension is documented, preserves original values and excludes bool; the
embedded original schema remains unchanged. These are structural checks, not game
semantics. Empty title/en strings allowed by the pinned schema are not falsely rejected.

R03: confusables item values follow the schema's unconstrained item contract;
strings, sequences, null, numbers and mapping extensions survive without false
errors. Their incidental id fields are not entity identities. Genuine malformed
entity records and duplicate recognized IDs remain errors.

Controls: 59 public synthetic adapter regressions plus 35 unchanged independent
reviewer probes pass (94 total). Project check passes with 102 existing tests;
diff check passes. Full independent frozen-file/record/field audit and two complete
imports pass: 23 available WGU files / 36 missing source entries; 1692 records,
1655 processed / 37 raw / zero errors; 38206 locations. The final repair import is
also byte-identical to the earlier successful repair audit after metadata-validation
completion. Earlier outputs and every frozen report are preserved. No historical
count is a test oracle; original full-accounting assertions were not weakened.

One synthetic shared-game-ID fixture was missing mandatory manifest.schema under
the newly added metadata validation. It now includes schema: wgu/kb@1; zero-error
and duplicate-ID assertions stay strict, with stronger exact accounting for the
added raw field and two retained game fields. Separate invalid-metadata tests still
reject missing/wrong schema. This was a changed input condition, not assertion relaxation.

All 53 parent artifact versions are verified against current or explicitly preserved
baseline copies. All 40 reviewer evidence artifacts and 148 accepted foundation
artifacts are unchanged. Only parser.py/importer.py and assigned synthetic tests
were changed; private outputs use new directories. No foundation, neighboring,
archive/history, global settings, new chat/agent/worktree or API changes occurred.

Actual executor Sol/high is based on the earlier direct operator observation in
this same ongoing conversation, with no observed/requested setting change. The
independent reviewer has its own separate operator-confirmed configuration. Native
handle tests/full import used normally reviewed narrow local escalation because
sandbox WinError 5 was previously measured. Native symlink measurements remain null.
Tokens, cost and operator time remain unavailable/null.

Independent re-review and coordinator technical acceptance/done remain outstanding.
Missing sources, mixed editions, source identity unknown, publisher coverage,
human semantic acceptance and executable readiness remain separate. IG-1D/E planned.
'''
(R/'report.md').write_bytes(report.encode('utf-8'))
checkpoint=read(R/'checkpoint.json');end=datetime.now(timezone.utc)
write('measurement.json',{'started_utc':checkpoint['started_utc'],'ended_utc':end.isoformat(),'wall_seconds':(end-datetime.fromisoformat(checkpoint['started_utc'])).total_seconds(),'input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None,'native_file_symlink':None,'native_directory_symlink':None})
products=[Path('src/wgc/wgu_adapter/parser.py'),Path('src/wgc/wgu_adapter/importer.py')]+sorted(Path('tests/wgu_adapter').glob('*.py'))
paths=products+sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts)+sorted(out.glob('*.json'))+sorted(p for p in checkroot.glob('*') if p.is_file())
q=read('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-1C')
write('delivery.json',{'role':'executor','actor':'ig1-stage-executor-20261013','task':'IG-1C','summary':'First bounded repairs for independent IG1C-R01/R02/R03: located scalar failures, pinned known-field/file structural validation, unconstrained confusables; 94 strict adapter/reviewer probes and 102 project tests pass; full lossless accounting/repeatability preserved. Independent re-review pending.','criteria':t['acceptance'],'artifacts':[art(p) for p in paths],'checks':checks,'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':art(R/'configuration.json'),'input_packet':read(R/'current-packet.json'),'parent_delivery':scope['parent_delivery'],'parent_review':scope['review'],'repair_findings':scope['finding_iterations'],'repair_cycles_per_finding':1,'unmet_lifecycle_gates':['Independent re-review of repaired hashes','Coordinator acceptance/done'],'semantic_acceptance_granted':False,'executable_readiness_granted':False,'source_coverage_granted':False})
print('Frozen repair delivery',len(paths),'artifacts',sha(R/'delivery.json'))
