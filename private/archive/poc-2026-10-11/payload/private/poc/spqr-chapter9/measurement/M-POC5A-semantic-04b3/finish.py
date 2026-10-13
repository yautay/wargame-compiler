"""Audit history and append exactly one completed evaluation-session record."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04b3'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json');validation=load(M/'validation.json');assert validation['status']=='passed'
for a in load(OUT/'manifest.json')['artifacts']+load(M/'public-document-artifacts.json'):
    assert ref(ROOT/a['path'])==a
for a in load(M/'packet-artifacts.json').values():assert ref(ROOT/a['path'])==a
changed=[x['path'] for x in start['protected'] if not (ROOT/x['path']).exists() or ref(ROOT/x['path'])!=x];assert not changed,changed
log=(M/'check-script.log').read_text(encoding='utf-8-sig');match=re.search(r'LOG_ROOT=(.+)',log);assert match
checkroot=Path(match.group(1).strip());checks=load(checkroot/'result.json');assert checks['tests_exit']==checks['diff_exit']==0
match=re.search(r'(\d+) passed',log);assert match;passed=int(match.group(1))
save(M/'check-script-result.json',dict(exit_code=0,passed=passed,result=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),git_diff_log=ref(checkroot/'diff-check.log'),unique_basetemp=checks['basetemp'],local_tmp_temp=True))
sessions=P/'measurement/sessions.jsonl';before=sessions.read_bytes();prefix=start['sessions_before'];assert len(before)==prefix['bytes'] and sha(before)==prefix['sha256'] and before.endswith(b'\n')
save(M/'final-audit.json',dict(status='passed',protected_files=len(start['protected']),changed_protected_files=changed,original_responses_eval_sources_previous_reviews_decisions_measurements_preserved=True,
    previous_sessions_prefix_preserved=True,previous_sessions=prefix,public_aggregate_documents_intentionally_updated=True))
now=datetime.now(timezone.utc)
completion=dict(id='M-POC5A-semantic-04b3',date='2026-10-11',timezone='Europe/Warsaw',card='M-POC5A.4b3',milestone='M-POC5',outcome='partial_waiting_review',author='Codex manual evaluator; owner accepts meaning',
    packet_manifest=ref(OUT/'manifest.json'),current_state=ref(R/'current-state-14.json'),owner_decision_unchanged=ref(R/'owner-decision-06.json'),owner_overlay_unchanged=ref(R/'owner-review-overlay-06.json'),
    assigned_distinct_ids=36,evaluator_compared_occurrences=72,per_answer={'first-001':36,'context-01':36},positive_bounded_proposals=68,separate_issue_occurrences=4,new_issues=['SEM-018','SEM-019'],
    owner_available_occurrences=72,new_owner_reviewed_occurrences=0,owner_pending_occurrences=72,owner_actual_file_open_or_read='unknown',previously_decided_kind_components_unchanged=2,
    previous_owner_decided_assigned_scopes=185,total_evaluator_compared_assigned_occurrences=257,remaining_uncompared_occurrences=0,total_owner_pending_scopes=72,
    pending_expectations=8,previous_issues_and_bounded_dispositions_preserved=True,whole_record_acceptance=False,full_graph_certified=False,metrics='not_assessable',
    recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),estimate_before_review=start['estimate_before_semantic_review'],calendar_elapsed_seconds=(now-datetime.fromisoformat(start['recorded_at_utc'])).total_seconds(),
    active_user_time='unknown',active_model_time='unknown',tokens='unknown',price='unknown',time_budget_compliance='unknown',timing_limitation='Calendar interval is not active experiment time budget.',
    checks=ref(M/'check-script-result.json'),validation=ref(M/'validation.json'),operational_events=ref(M/'operational-events.json'),audit=ref(M/'final-audit.json'),protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,
    new_extractions=0,new_sources=0,new_context_rounds=0,new_corrections=0,new_chats=0,situations_evaluated=0,
    unchanged_limits=dict(extra_pages=1,extra_rules=1,extra_tables=0,context_rounds=1,corrections=0,full_gap_closures=0,partial_updates=4,new_declarations=4,source_expansion_stop_depth=2),
    next_card='M-POC5A',next_part='M-POC5A.4c',next_milestone='M-POC5',whole_card_closed=False,
    resume='Owner decisions .4b3 owner-focus68+2+2; retain previous kindD961stack and all older pending. Afterwards separate .4c after estimate/pre-review split if needed. Not full .4b closure.',git_publication='not requested; no commit/push')
save(M/'completion.json',completion)
with sessions.open('ab') as f:f.write((json.dumps(dict(completion,completion=ref(M/'completion.json')),ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
after=sessions.read_bytes();assert after[:len(before)]==before and len(after.splitlines())==len(before.splitlines())+1
save(M/'append-seal.json',dict(previous=prefix,after=ref(sessions),previous_prefix_preserved=True,new_records=1,completion=ref(M/'completion.json')))
assert all(ref(ROOT/a['path'])==a for a in start['protected'])
print(json.dumps(dict(compared=72,positive_proposals=68,separate_issue_occurrences=4,new_owner_decisions=0,tests_passed=passed,protected_preserved=len(start['protected']),append_only=True)))
