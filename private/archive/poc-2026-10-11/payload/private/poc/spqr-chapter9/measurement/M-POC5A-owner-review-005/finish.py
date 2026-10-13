"""Seal owner-decision recording, preserving the previous measurement prefix."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json');validation=load(M/'validation.json');assert validation['status']=='passed'
for a in load(M/'decision-artifacts.json')['artifacts']+load(M/'public-document-artifacts.json'):
    assert ref(ROOT/a['path'])==a
changed=[a['path'] for a in start['protected'] if not (ROOT/a['path']).exists() or ref(ROOT/a['path'])!=a];assert not changed,changed
log=(M/'check-script.log').read_text(encoding='utf-8-sig')
match=re.search(r'LOG_ROOT=(.+)',log);assert match
testroot=Path(match.group(1).strip());checks=load(testroot/'result.json')
assert checks['tests_exit']==checks['diff_exit']==0
match=re.search(r'(\d+) passed',log);assert match
passed=int(match.group(1));assert passed==137
save(M/'check-script-result.json',dict(exit_code=0,passed=passed,result=ref(testroot/'result.json'),pytest_log=ref(testroot/'pytest.log'),
    git_diff_log=ref(testroot/'diff-check.log'),local_tmp_temp=True,unique_basetemp=checks['basetemp']))
sessions=P/'measurement/sessions.jsonl';before=sessions.read_bytes();prefix=start['sessions_before']
assert len(before)==prefix['bytes'] and sha(before)==prefix['sha256'] and before.endswith(b'\n')
save(M/'final-audit.json',dict(status='passed',protected_files=len(start['protected']),changed_protected_files=changed,
    original_responses_eval_sources_old_decisions_and_packets_preserved=True,previous_sessions_prefix_preserved=True,
    previous_sessions=prefix,public_aggregate_docs_intentionally_updated=True))
now=datetime.now(timezone.utc)
completion=dict(id='M-POC5A-owner-review-005',date='2026-10-11',timezone='Europe/Warsaw',card='M-POC5A',part='M-POC5A.4b1-owner-review',milestone='M-POC5',outcome='partial',
    author='Codex recording explicit owner decision',owner_reply_verbatim='zgodnie z rekomendacją',recommendations_accepted=6,
    decision=ref(R/'owner-decision-05.json'),overlay=ref(R/'owner-review-overlay-05.json'),current_state=ref(R/'current-state-11.json'),
    prior_positive_scopes_preserved=116,newly_decided_assigned_occurrences=9,per_answer={'first-001':4,'context-01':5},extra_frozen_mention_occurrences=2,
    assigned_scoped_decisions_total=125,whole_edges_correct_count='not_assessable',pending_assigned_4b1=0,remaining_other_parts_scoped_review=132,
    pending_expectations=8,remaining_prior_issue_ids=[f'SEM-{n:03}' for n in range(1,14)],SEM_004='partial; remaining earlier scope open',
    SEM_014_015_016='resolved only in six presented exact scopes',whole_record_acceptance=False,full_graph_certified=False,metrics='not_assessable',
    recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),estimate_minutes=start['estimate_minutes'],
    calendar_elapsed_seconds=(now-datetime.fromisoformat(start['recorded_at_utc'])).total_seconds(),active_user_time='unknown',active_model_time='unknown',
    tokens='unknown',price='unknown',time_budget_compliance='unknown',timing_limitation='Calendar interval of recording, not active experiment budget or extraction time.',
    checks=ref(M/'check-script-result.json'),validation=ref(M/'validation.json'),audit=ref(M/'final-audit.json'),protected_files_preserved=len(start['protected']),
    previous_measurement_prefix_preserved=True,new_extractions=0,new_sources=0,new_context_rounds=0,new_corrections=0,new_chats=0,situations_evaluated=0,
    next_card='M-POC5A',next_part='M-POC5A.4b2',next_milestone='M-POC5',whole_card_closed=False,git_publication='not requested; no commit/push',
    resume='Next separate .4b2:30IDs/60occurrences, estimate before execution. Preserve remaining old pending and excluded fields. No next batch executed by this decision.')
save(M/'completion.json',completion)
with sessions.open('ab') as f:
    f.write((json.dumps(dict(completion,completion=ref(M/'completion.json')),ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
after=sessions.read_bytes();assert after[:len(before)]==before and len(after.splitlines())==len(before.splitlines())+1
save(M/'append-seal.json',dict(previous=prefix,after=ref(sessions),previous_prefix_preserved=True,new_records=1,completion=ref(M/'completion.json')))
assert all(ref(ROOT/a['path'])==a for a in start['protected'])
print(json.dumps(dict(recommendations=6,new_assigned_decisions=9,extra_mention_decisions=2,tests_passed=passed,protected_preserved=len(start['protected']),sessions_append_only=True)))
