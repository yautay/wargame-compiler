"""Final preservation audit and one append-only scoped session record."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[5]; P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent;REV=P/'reviews/semantic-01';OUT=REV/'part-04a'
sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_bytes().decode('utf-8-sig'))
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json');D=load(OUT/'comparisons.json');V=load(M/'validation.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
for r in load(OUT/'manifest.json')['artifacts']:assert ref(ROOT/r['path'])==r
for r in [D['evaluation'],D['source']]+list(D['responses'].values()):assert ref(ROOT/r['path'])==r
checklog=(M/'check-script.log').read_text(encoding='utf-8-sig')
checkroot=Path(re.search(r'LOG_ROOT=(.+)',checklog).group(1).strip())
checks=load(checkroot/'result.json')
assert checks['tests_exit']==checks['diff_exit']==0
assert '129 passed' in checklog
assert load(M/'git-diff-check-result.json')['exit_code']==0
assert D['owner_decisions']==[]
save(M/'presentation-delivery.json',dict(packet=ref(OUT/'owner-focus.md'),tool='open_in_codex',observed_result='queued',owner_opened_packet_or_images='unknown',owner_decisions=[],semantic_acceptance='not_performed'))
now=datetime.now(timezone.utc)
record=dict(id='M-POC5A-semantic-04a-comparisons',card='M-POC5A',part='M-POC5A.4a',milestone='M-POC5',outcome='partial',status='waiting_review',timezone='Europe/Warsaw',author='Codex',owner_instruction='Kontynuuj M-POC5A, część M-POC5A.4a: EXP-051–074.',instruction_is_semantic_acceptance=False,recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),recorded_calendar_elapsed_seconds=(now-datetime.fromisoformat(start['recorded_at_utc'])).total_seconds(),bootstrap_start='unknown',timing_limitation='Recorded start after bootstrap; calendar elapsed does not measure active user/model time or certify the 90-minute/overall budget.',active_user_time='unknown',active_model_time='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',actual_model_selector='unknown',reasoning_selector='unknown',tokens='unknown',price='unknown',evaluation=D['evaluation'],responses=D['responses'],source=D['source'],summary=D['summary'],prior_owner_decisions=D['prior_owner_decisions'],prior_owner_overlay=D['prior_owner_overlay'],new_owner_decisions=[],new_semantic_acceptance='not_performed',current_state=ref(REV/'current-state-06.json'),presentation=ref(M/'presentation-delivery.json'),new_extractions=0,new_context_rounds=0,new_corrections=0,new_sources=0,situations_evaluated=0,preserved_context_totals=D['limits'],preserved_operational_limitations=D['limitations'],full_gap_closures=0,partial_updates_retained_blocking=4,new_context_declarations_retained=4,full_graph_depth_compliance='not_assessable',semantic_TP_FP_FN='not_assessable',full_semantic_metrics='not_assessable',protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,tooling_diagnostic=V['tooling_diagnostic'],checks=dict(passed=129,result=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),script_diff_log=ref(checkroot/'diff-check.log'),script_call_log=ref(M/'check-script.log'),explicit_diff_result=ref(M/'git-diff-check-result.json'),explicit_diff_log=ref(M/'git-diff-check.log'),comparison_validation=ref(M/'validation.json'),local_tmp_temp=True,unique_basetemp=checks['basetemp'],limitation='Integrity/structural controls do not approve meaning. CRLF normalization warnings retained.'),artifacts=[ref(f) for f in sorted(OUT.iterdir()) if f.is_file()],required_read_manifest=ref(M/'read-inputs.json'),instruction_files=[ref(P/'prompts/semantic-review-part04a-start-v1.txt'),ref(P/'prompts/semantic-review-start-v1.txt')],public_documents=[ref(ROOT/f) for f in ['docs/STATUS.md','docs/ROADMAP.md','docs/HANDOFF.md','docs/work/tasks/semantic/M-POC5A.4a.md','docs/handoff/2026-10-10-M-POC5A-semantic-04a.md']],resume='Owner decisions on exact positive scopes (20 local and EXP-064 source need), separate SEM-011/012/013 and prior pending. Next separate .4b relationships, then .4c/.4d; split before work if needed.',next_card='M-POC5A',next_part='M-POC5A.4b',next_milestone='M-POC5',M_POC5A_closed=False,M_POC5A_4_closed=False,git_publication='not_requested; no commit/push')
sessions=P/'measurement/sessions.jsonl';old=sessions.read_bytes();before=start['sessions_before']
assert len(old)==before['bytes'] and hashlib.sha256(old).hexdigest()==before['sha256']
assert old.endswith(b'\n') and record['id'].encode() not in old
save(M/'completion.json',record)
entry=dict(record,completion=ref(M/'completion.json'))
with sessions.open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
assert sessions.read_bytes()[:len(old)]==old
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
save(M/'append-seal.json',dict(previous=before,sessions_after=ref(sessions),added_records=1,original_prefix_preserved=True,completion=ref(M/'completion.json'),protected_files_preserved=len(start['protected']),new_artifact_hashes=[ref(f) for f in sorted(M.iterdir()) if f.is_file() and f.name!='append-seal.json'],semantic_acceptance='not_performed'))
print(json.dumps(dict(outcome='partial',status='waiting_review',passed=129,protected_files=1018,new_owner_decisions=0,measurement_appended=1,still_pending=29),ensure_ascii=False))
