"""Seal the owner acceptance, planned split and ready prompt; append measurement only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01'
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(path,obj):
    assert not path.exists(),path
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
decision=load(REV/'owner-decision-02.json');overlay=load(REV/'owner-review-overlay-02.json')
assert decision['owner_reply']=='Akceptuję i podaj prompt dla nowej sesji'
assert len(decision['scopes'])==23 and decision['context_acceptance_is_gap_closure'] is False
assert len(overlay['runs']['first-001']['scopes'])==43 and len(overlay['pending_expectation_ids'])==29
for r in load(M/'decision-artifacts.json')['artifacts']:assert ref(ROOT/r['path'])==r
checkroot=ROOT/'private/poc/_checks/active-3d54199cc32f4a20b3f50401a3537df4'
checks=load(checkroot/'result.json');assert checks['tests_exit']==0 and checks['diff_exit']==0
assert '128 passed' in (checkroot/'pytest.log').read_text(encoding='utf-8-sig')
assert load(M/'git-diff-check-result.json')['exit_code']==0
prompt=P/'prompts/semantic-review-part04a-start-v1.txt'
cards=[ROOT/f'docs/work/tasks/semantic/M-POC5A.4{n}.md' for n in 'abcd']
planning=[ref(prompt)]+[ref(p) for p in cards]+[ref(ROOT/'docs/work/tasks/semantic/M-POC5A.4.md')]
save(M/'handoff-prompt-artifacts.json',dict(prompt=ref(prompt),parts=planning[1:],split_before_execution=True,
    next_part='M-POC5A.4a',next_part_executed=False,new_chat_created=False))
now=datetime.now(timezone.utc)
record=dict(id='M-POC5A-owner-review-002-acceptance-and-prompt',card='M-POC5A',milestone='M-POC5',
    part='M-POC5A.3-owner-review',outcome='partial',status='remaining_waiting_review',date='2026-10-10',
    timezone='Europe/Warsaw',author='Codex',owner_reply=decision['owner_reply'],
    first_recorded_clock_utc=start['first_recorded_clock_utc'],completed_at_utc=now.isoformat(),
    recorded_calendar_elapsed_seconds=(now-datetime.fromisoformat(start['first_recorded_clock_utc'])).total_seconds(),
    timing_limitation='Recorded clock after owner message/bootstrap; calendar is not active user/model time.',
    active_user_time='unknown',active_model_time='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',
    actual_model_selector='unknown',reasoning_selector='unknown',tokens='unknown',price='unknown',
    new_local_scopes_per_answer=21,new_context_requirements_per_answer=2,
    cumulative_local_scopes_per_answer=43,local_denominator=66,pending_local=23,
    cumulative_context_requirements_per_answer=2,context_denominator=8,pending_context=6,
    context_full_results='blocked_source; no gap closure',pending_expectations=29,scoped_category_units=175,
    full_metrics='not_assessable',semantic_TP_FP_FN='not_assessable',whole_card_closed=False,
    owner_decision=ref(REV/'owner-decision-02.json'),overlay=ref(REV/'owner-review-overlay-02.json'),
    current_state=ref(REV/'current-state-05.json'),evaluation=decision['evaluation'],responses=decision['responses'],
    exclusions=decision['excluded'],owner_file_or_image_open_verified=False,
    next_session_prompt=ref(prompt),planned_parts=['M-POC5A.4a','M-POC5A.4b','M-POC5A.4c','M-POC5A.4d'],
    split_before_execution=True,parts_4_not_executed=True,new_chat_created=False,
    new_extractions=0,new_context_rounds=0,new_corrections=0,situations_evaluated=0,
    context_totals=dict(extra_pages=1,extra_rules=1,extra_tables=0,rounds=1,corrections=0,source_stop_depth=2),
    third_step_source_acquired=False,full_graph_depth_compliance='not_assessable',
    assessment_exposure='unknown',clean_context='unknown',scope_discovery_outside_allowlist='confirmed_context_session',
    contamination_proven=False,full_isolation_proven=False,
    protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,
    checks=dict(passed=128,result=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),
        script_diff_log=ref(checkroot/'diff-check.log'),explicit_diff_result=ref(M/'git-diff-check-result.json'),
        explicit_diff_log=ref(M/'git-diff-check.log'),decision_and_prompt_validation=ref(M/'validation.json'),
        local_tmp_temp=True,unique_basetemp=checks['basetemp'],
        limitations='Structural checks do not accept meaning; three public-doc CRLF normalization warnings, no diff errors.'),
    artifacts=load(M/'decision-artifacts.json')['artifacts']+planning,
    next_card='M-POC5A',next_milestone='M-POC5',next_part='M-POC5A.4a',
    resume='Owner manually starts a local session with the saved .4a prompt. Retain all earlier pending and do not run the remaining planned parts in that session.',
    git_publication='not_requested; no commit or push')
save(M/'completion.json',record)
sessions=P/'measurement/sessions.jsonl';old=sessions.read_bytes();before=start['sessions_before']
assert len(old)==before['bytes'] and hashlib.sha256(old).hexdigest()==before['sha256']
assert old.endswith(b'\n') and record['id'].encode() not in old
entry=dict(record,completion=ref(M/'completion.json'))
with sessions.open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
assert sessions.read_bytes()[:len(old)]==old
save(M/'append-seal.json',dict(previous=before,sessions_after=ref(sessions),added_records=1,original_prefix_preserved=True,
    completion=ref(M/'completion.json')))
print(json.dumps(dict(local_scopes=43,context_requirements=2,pending_expectations=29,passed=128,
    protected_files=len(start['protected']),next_part='M-POC5A.4a',prompt=str(prompt),measurement_appended=1),ensure_ascii=False))
