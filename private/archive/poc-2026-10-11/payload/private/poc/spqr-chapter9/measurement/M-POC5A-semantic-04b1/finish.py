"""Final integrity audit and append-only session record. No semantic acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01';OUT=REV/'part-04b1'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json');prefix=start['sessions_before'];sessions=P/'measurement/sessions.jsonl'
current=sessions.read_bytes();assert len(current)==prefix['bytes'] and sha(current)==prefix['sha256']
fail=[]
for a in start['protected']:
    f=ROOT/a['path']
    if not f.exists() or ref(f)!=a:fail.append(a['path'])
assert not fail,fail
for a in load(OUT/'manifest.json')['artifacts']:assert ref(ROOT/a['path'])==a
testroot=ROOT/'private/poc/_checks/active-7e03847297f746deaf09e77d1587a494'
checks=load(testroot/'result.json');assert checks['tests_exit']==checks['diff_exit']==0
assert load(M/'git-diff-check-result.json')['exit_code']==0
save(M/'presentation-delivery.json',dict(tool='mcp__codex_app__open_in_codex',targets=[ref(OUT/'comparisons.md'),ref(OUT/'owner-focus.md')],
    results=[dict(status='queued',threadId='01a129d9-5823-72a2-a2c3-b86aab44ca8b')]*2,
    actual_owner_open_or_read='unknown',policy='Tool queued delivery and final links only, no assertion of human viewing.'))
save(M/'operational-events.json',dict(events=[
    dict(step='compact console input inspection',observed='UnicodeEncodeError cp1252 for Polish text; rerun with Python -X utf8',semantic_effect='none'),
    dict(step='packet materialization',observed='StopIteration reading continuation candidate list; historical continuation uses singular output_id, explicitly mapped all7original edges then materialized',semantic_effect='none; originals unchanged'),
    dict(step='local evidence validator',observed='KeyError empty pointer at JSON root; added RFC6901 root handling;35095spans validated',semantic_effect='none; originals unchanged'),
    dict(step='first scripts/check.ps1',observed='1 failed,134passed: handoff next-card field contained semicolon; corrected public handoff fields/history pointer; logs retained',log=ref(M/'check-script.log'),result=ref(M/'check-script-result.json')),
    dict(step='final scripts/check.ps1',observed='135 passed, diff_exit0',log=ref(M/'check-script-final.log'),result=ref(testroot/'result.json')),
],test_or_response_mutations=False))
audit=dict(status='passed',protected_files=len(start['protected']),changed_protected_files=fail,previous_sessions_prefix_preserved=True,
    previous_sessions=prefix,packet_manifest_verified=True,owner_decisions_01_02_03_and_overlay_03_preserved=True,
    eval_v1_original_responses_source_inputs_context_closed_reports_old_reviews_measurements_preserved=True,publication='no commit/push',
    original_hash_checks=[ref(P/f) for f in ['runs/first-001/first-001.json','runs/context-01/response.raw.txt','evaluation/eval-v1/manifest.json','source/original-pdf-20261008-01.pdf']],
    audit_limit='Named immutable evidence trees captured after bootstrap, before semantic review; not a whole-repository/legacy filesystem certificate. Public docs intentionally updated.')
save(M/'final-audit.json',audit)
now=datetime.now(timezone.utc);s=datetime.fromisoformat(start['recorded_at_utc'])
completion=dict(id='M-POC5A-semantic-04b1',date='2026-10-11',timezone='Europe/Warsaw',card='M-POC5A',part='M-POC5A.4b1',milestone='M-POC5',outcome='partial',
    author='Codex — evaluator proposals, owner accepts meaning',recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),calendar_elapsed_seconds=(now-s).total_seconds(),
    timing_limitation='After bootstrap timestamp, not active user/model time or proof of90minute/totalbudget compliance. Estimate75–90minutes recorded before semantic review.',
    active_user_time='unknown',active_model_time='unknown',time_budget_compliance='unknown',active_budget_remaining='unknown',tokens='unknown',price='unknown',actual_model_selector='unknown',reasoning_selector='unknown',
    summary=load(M/'packet-summary.json'),source_review='Supplied PDF31–37 renders and boundedStep4crop only; no new page/context',
    current_state=ref(REV/'current-state-09.json'),packet_manifest=ref(OUT/'manifest.json'),validation=ref(M/'validation.json'),
    protected_files_preserved=len(start['protected']),final_audit=ref(M/'final-audit.json'),new_owner_decisions=0,owner_acceptance='waiting_review',
    checks=dict(passed=135,result=ref(testroot/'result.json'),pytest_log=ref(testroot/'pytest.log'),diff_log=ref(M/'git-diff-check.log'),diff_result=ref(M/'git-diff-check-result.json'),local_tmp_temp=True,unique_basetemp=checks['basetemp'],first_failed_run_retained=ref(M/'check-script-result.json')),
    presentation=ref(M/'presentation-delivery.json'),previous_measurement_prefix_preserved=True,new_extractions=0,new_context_rounds=0,new_corrections=0,new_sources=0,situations_evaluated=0,
    complete_graph_certified=False,remaining_4b_occurrences=132,next_card='M-POC5A',next_part='M-POC5A.4b2',next_milestone='M-POC5',whole_card_closed=False,
    resume='Owner bounded positive scope and SEM-004/014/015/016 plus all prior pending; new owner-decision only upon reply. Then separate4b2existing30IDs/60occurrences, estimate before review.',git_publication='not requested;no commit/push',
    artifacts=[ref(f) for f in sorted(OUT.iterdir()) if f.is_file()])
save(M/'completion.json',completion)
record={**completion,'completion':ref(M/'completion.json')}
assert current.endswith(b'\n')
with sessions.open('ab') as f:f.write((json.dumps(record,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
after=sessions.read_bytes();assert after[:len(current)]==current and len(after.splitlines())==len(current.splitlines())+1
save(M/'append-seal.json',dict(previous=prefix,after=ref(sessions),previous_prefix_preserved=True,new_records=1,completion=ref(M/'completion.json')))
# Recheck protected originals at the actual end, after append (sessions intentionally excluded).
assert all(ref(ROOT/a['path'])==a for a in start['protected'])
print(json.dumps(dict(protected_preserved=len(start['protected']),tests_passed=135,provenance_spans=35095,assigned_compared=125,new_owner_review=0,pending=125,remaining_other_parts=132,sessions_append_only=True)))
