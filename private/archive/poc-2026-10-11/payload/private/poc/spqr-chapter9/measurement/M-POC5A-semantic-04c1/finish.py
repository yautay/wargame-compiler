"""Final immutable-history audit and one append-only measured session."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c1'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json');validation=load(M/'validation.json');assert validation['status']=='passed'
for x in load(OUT/'manifest.json')['artifacts']+load(M/'public-document-artifacts.json')+load(M/'owner-decision-artifacts.json')['artifacts']:
    assert ref(ROOT/x['path'])==x
for x in load(M/'packet-artifacts.json').values():assert ref(ROOT/x['path'])==x
changed=[x['path'] for x in start['protected'] if not (ROOT/x['path']).exists() or ref(ROOT/x['path'])!=x];assert not changed,changed
log=(M/'check-script.log').read_text(encoding='utf-8-sig');match=re.search(r'LOG_ROOT=(.+)',log);assert match;checkroot=Path(match.group(1).strip());checks=load(checkroot/'result.json');assert checks['tests_exit']==checks['diff_exit']==0
match=re.search(r'(\d+) passed',log);assert match;passed=int(match.group(1))
save(M/'check-script-result.json',dict(exit_code=0,passed=passed,result=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),git_diff_log=ref(checkroot/'diff-check.log'),unique_basetemp=checks['basetemp'],local_tmp_temp=True))
sessions=P/'measurement/sessions.jsonl';before=sessions.read_bytes();prefix=start['sessions_before'];assert len(before)==prefix['bytes'] and sha(before)==prefix['sha256'] and before.endswith(b'\n')
save(M/'final-audit.json',dict(status='passed',protected_files=len(start['protected']),changed_protected_files=changed,
    original_responses_sources_eval_previous_reports_decisions_and_measurements_preserved=True,previous_sessions_prefix_preserved=True,previous_sessions=prefix,public_aggregate_documents_intentionally_updated=True))
now=datetime.now(timezone.utc);summary=load(M/'packet-summary.json')
completion=dict(id='M-POC5A-semantic-04c1',date='2026-10-11',timezone='Europe/Warsaw',card='M-POC5A.4c1',milestone='M-POC5',outcome='partial_waiting_review',author='Codex manual evaluator; owner accepts meaning',
    packet_manifest=ref(OUT/'manifest.json'),current_state=ref(R/'current-state-16.json'),scope_plan=ref(M/'scope-plan.json'),
    prior_packet_owner_reply='ok kontynuuj',prior_packet_new_owner_decision=ref(R/'owner-decision-07.json'),prior_packet_new_owner_overlay=ref(R/'owner-review-overlay-07.json'),new_prior_relationship_scopes_decided=72,total_relation_scoped_decisions=257,
    summary=summary,new_locator_owner_decisions=0,locator_available_occurrences=44,locator_compared_occurrences=44,locator_owner_pending_occurrences=44,remaining_uncompared_locator_occurrences=80,
    recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),estimate_before_locator_review=start['estimate_before_locator_review'],calendar_elapsed_seconds=(now-datetime.fromisoformat(start['recorded_at_utc'])).total_seconds(),
    active_model_time='unknown',active_user_time='unknown',model_selector='unknown',reasoning_selector='unknown',tokens='unknown',price='unknown',time_budget_compliance='unknown',timing_limitation='Calendar interval is not active experiment time.',
    checks=ref(M/'check-script-result.json'),validation=ref(M/'validation.json'),operational_events=ref(M/'operational-events.json'),audit=ref(M/'final-audit.json'),protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,
    previous_pending_expectations=8,previous_pending_issues_preserved=True,whole_record_acceptance=False,full_graph_certified=False,full_metrics='not_assessable',
    new_sources=0,new_extractions=0,new_context_rounds=0,new_corrections=0,new_chats=0,situations_evaluated=0,
    unchanged_limits=dict(extra_pages=1,extra_rules=1,extra_tables=0,context_rounds=1,corrections=0,full_gap_closures=0,partial_updates=4,new_declarations=4,source_expansion_stop_depth=2),
    next_card='M-POC5A',next_part='M-POC5A.4c2',next_milestone='M-POC5',whole_card_closed=False,resume='Owner decisions on.4c1 then separate.4c2,21IDs/42occurrences after estimate; remaining.4c3 and older pending retained.',git_publication='not requested; no commit/push')
save(M/'completion.json',completion)
with sessions.open('ab') as f:f.write((json.dumps(dict(completion,completion=ref(M/'completion.json')),ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
after=sessions.read_bytes();assert after[:len(before)]==before and len(after.splitlines())==len(before.splitlines())+1
save(M/'append-seal.json',dict(previous=prefix,after=ref(sessions),previous_prefix_preserved=True,new_records=1,completion=ref(M/'completion.json')))
assert all(ref(ROOT/x['path'])==x for x in start['protected'])
print(json.dumps(dict(locator_compared=44,new_locator_owner_decisions=0,previous_relation_scopes_newly_accepted=72,total_relation_scopes=257,tests_passed=passed,protected_preserved=len(start['protected']),append_only=True)))
