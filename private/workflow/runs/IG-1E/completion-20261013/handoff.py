"""Write final English full-stage handoff only after all five tasks are done."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
ROOT=Path.cwd();RUN=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def art(p):return {'path':str(p).replace('\\','/'),'sha256':sha(p)}
q=read('docs/work/queue.json');rows=[]
for task in q['tasks']:
 if task['id'] not in ['IG-1A','IG-1B','IG-1C','IG-1D','IG-1E']:continue
 assert task['status']=='done'
 events={state:next(e for e in reversed(task['events']) if e['to']==state) for state in ['review','accepted','done']}
 for e in events.values():assert sha(e['evidence'])==e['sha256']
 accepted=read(events['accepted']['evidence']);delivery=read(events['review']['evidence'])
 assert accepted['criteria']==task['acceptance'] and accepted['artifacts']==delivery['artifacts']
 assert all(c['exit_code']==0 for c in accepted['checks'])
 for a in accepted['artifacts']:assert sha(a['path'])==a['sha256'],a['path']
 review=accepted['independent_review'];assert sha(review['path'])==review['sha256']
 rows.append({'task':task['id'],'title':task['title'],'status':'done','criteria':task['acceptance'],
  'delivery':art(events['review']['evidence']),'independent_review':review,
  'acceptance':art(events['accepted']['evidence']),'coordinator_done':art(events['done']['evidence']),
  'reviewer_actor':accepted['actor'],'model':accepted['model'],'reasoning':accepted['reasoning'],
  'human_semantic_acceptance_required':task['semantic_acceptance_required'],'human_semantic_acceptance_granted':False})
report=read('private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013/acceptance-report.json')
snapshot=Path(report['snapshot_directory'])
manifest=read(snapshot/'manifest.json');assert manifest['state']=='sealed'
assert sha(snapshot/'manifest.json')==report['snapshot']['sha256']
for f in manifest['files']:assert sha(snapshot/f['path'])==f['sha256']
source_ledger=art(snapshot/'input-coverage-ledger.json')
summary={'format':'wgc-stage-handoff-1','stage':'IG-1','completed_tasks':rows,
 'queue':art('docs/work/queue.json'),'snapshot':report['snapshot'],'input_coverage_ledger':source_ledger,
 'accounting':{k:report[k] for k in ['files','available_files','missing_sources','independent_record_counts','field_locations','unknown_roots','unknown_field_locations','gap_counts']},
 'repeatability':{'imports':True,'transforms_and_publications':True,'seals':True},
 'readiness':{'structural_import':'complete_and_technically_accepted','structural_snapshot':'sealed',
             'publisher_source_coverage':'not_verified','human_semantic_acceptance':'not_granted','executable_readiness':'blocked'},
 'prerequisites':report['reconciliation_prerequisites'],'recorded_utc':datetime.now(timezone.utc).isoformat(),
 'executor_model':'gpt-6.1-sol','executor_reasoning':'high',
 'executor_configuration_evidence':art('private/workflow/runs/IG-1D/resume-audit-20261013T134548Z/configuration-confirmed.json'),
 'input_tokens':None,'output_tokens':None,'cost':None,'operator_time_seconds':None,
 'no_commit_or_push':True,'IG_2_started':False}
with (RUN/'final-stage-handoff.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(summary,f,indent=2);f.write('\n')
lines=['# IG-1 final stage handoff','',
 'IG-1A, IG-1B, IG-1C, IG-1D and IG-1E are done in the authoritative queue. Each exact delivery passed independent technical review and coordinator completion. Original and repaired versions, all frozen reports and accepted foundation bytes are retained. No commit or push was created.','',
 '## Exact task gates and evidence','',
 '| Task | Gate | Delivery SHA256 | Independent review SHA256 |','|---|---|---|---|']
for row in rows:lines.append(f"| {row['task']} | done; every technical criterion passed | {row['delivery']['sha256']} | {row['independent_review']['sha256']} |")
lines+=['','Exact paths, reviewer identities, complete acceptance criteria and accepted/done hashes are in final-stage-handoff.json. Accepted/done evidence pins the entire corresponding delivery artifact list. IG-1D R01–R03 used one repair each; R04 used two. Its independent repair-2 PASS closed all findings. IG-1E independent review and exact acceptance are recorded without transferring game-source meaning.','',
 '## Complete input accounting and repeatability','',
 f"The independently checked ledger has {report['files']} entries: {report['available_files']} available and {report['missing_sources']} missing. Record statuses: {report['independent_record_counts']}. It retains {report['field_locations']} YAML field/container locations, {report['unknown_roots']} unknown roots and {report['unknown_field_locations']} unknown subtree locations. Every file/record/field/binding/raw byte and hash/revision closure is accounted for. Counts are computed from exact raw input and compared with adapter counters, not accepted from counters alone.",'',
 f"The sealed structural snapshot is {report['snapshot_directory']}. Its manifest SHA256 is {report['snapshot']['sha256']}. The input-coverage-ledger.json SHA256 is {source_ledger['sha256']}. Two new full imports equal accepted IG-1C bytes; two full transforms/publications equal accepted IG-1D canonical draft bytes; two seals have identical canonical files and manifest. The exact draft snapshot remains as historical lineage, with every selected revision and readiness assessment retained.",'',
 '## Validation and actual configuration','',
 'IG-1D executor validation: 128 public/original/risk/history controls and 102 project tests, plus full accounting and two canonical publications. Independent repair-2 review repeated those controls, added six boundary probes and confirmed the full corpus. IG-1E executor validation: 106 integration/adapter/export tests, 102 project tests, two fresh imports, full independent corpus audit and two structural seals. The independent IG-1E commands/results and measured UTC/wall time are pinned by its review evidence. Required scripts/check.ps1, queue validation and git diff --check passed. Setup failures and corrections remain visible in their own immutable reports.','',
 'The current executor and continuing independent reviewer were separately operator-confirmed as GPT-6.1 Sol / high. Actual operational measurements are outside canonical hashes. Token counts, cost and operator time are unavailable/null; no total historical stage duration or invented monetary estimate is asserted.','',
 '## Remaining readiness gates and next action','',
 f"The snapshot retains gap counts {report['gap_counts']}, all {report['missing_sources']} missing configured source paths and original mixed-edition/source/version claims. The selected 5E source identity to the missing WGU original and edition compatibility remain unknown. No automatic edition precedence was applied. Structural sealing is separate from publisher coverage, human semantic acceptance and executable readiness; those gates remain unverified/ungranted/blocked.",'',
 *['- '+p for p in report['reconciliation_prerequisites']], '',
 'Next exact action: the operator/coordinator selects and refines the subsequent source-inventory/reconciliation task from queue.json with exact source pages/IDs, materials and reviewer authority. No IG-2 task was claimed or started. No gameplay/runtime/compiler/POC or LLM legality implementation was added.']
with (RUN/'final-stage-handoff.md').open('x',encoding='utf-8',newline='\n') as f:f.write('\n'.join(lines)+'\n')
print(json.dumps({'handoff':art('private/workflow/runs/IG-1E/completion-20261013/final-stage-handoff.md'),'completed_tasks':5,'snapshot':report['snapshot']}))
