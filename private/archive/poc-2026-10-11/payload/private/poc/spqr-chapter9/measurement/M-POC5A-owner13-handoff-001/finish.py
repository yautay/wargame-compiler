"""Validate bounded assent, preserve evidence, append one completed handoff session."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, re
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'; R=P/'reviews/semantic-01'; M=Path(__file__).resolve().parent
def load(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json'); old=load(R/'current-state-26.json'); s=load(R/'current-state-27.json')
d=load(R/'owner-decision-13.json'); o=load(R/'owner-review-overlay-13.json'); oo=load(R/'owner-review-overlay-12.json')
packet=load(R/'part-04d3/comparisons.json'); pres=load(R/'part-04d3/presentation.json')
assert d['owner_reply_verbatim']=='zatwierdzam i podaj prompt aby kontynuować w nowej sesji'
assert d['recommendations']==pres['decisions'] and len(d['scopes'])==59
assert d['newly_reviewed_inventory_occurrences']==118 and d['bounded_supported_occurrences']==114
assert d['mixed_parent_occurrences']==d['explanatory_child_omission_occurrences']==2
assert d['underlying_omitted_explanatory_clauses_per_answer']==1
for approved, original in zip(d['scopes'],packet['inventory']):
    assert approved['id']==original['id'] and approved['status']=='reviewed'
    for key,value in original.items():
        if key not in ['status','human_reviewer','reviewer','recorded_at_utc','whole_record_accepted','runs']:
            assert approved[key]==value,(approved['id'],key)
    for run, originalrun in original['runs'].items():
        a=approved['runs'][run]
        assert a['owner_decision']=='accepted_presented_bounded_judgment' and a['whole_record_accepted'] is False
        for key,value in originalrun.items():
            if key not in ['status','human_reviewer','reviewer','owner_decision','whole_record_accepted']:
                assert a[key]==value,(approved['id'],run,key)
for run,v in o['runs'].items():
    prior=oo['runs'][run]
    assert v['inventory_scopes'][:107]==prior['inventory_scopes']
    assert len(v['inventory_scopes'])==v['owner_reviewed_inventory_scoped_occurrences']==166
    assert [x['id'] for x in v['inventory_scopes'][107:]]==[x['id'] for x in packet['inventory']]
    for key,value in prior.items():
        if key not in ['inventory_scopes','owner_reviewed_inventory_scoped_occurrences']:
            assert v[key]==value,(run,key)
assert s['decision']==s['inventory_owner_decision']==ref(R/'owner-decision-13.json')
assert s['overlay']==ref(R/'owner-review-overlay-13.json')
assert s['unresolved_issue_ids']==[f'SEM-{i:03}' for i in range(1,14)]
assert s['pending_expectation_ids']==old['pending_expectation_ids']
assert {k:v for k,v in s['issue_dispositions'].items() if k!='SEM-021'}==old['issue_dispositions']
assert s['issue_dispositions']['SEM-021']==d['issue_disposition']['SEM-021']
for key in ['expectation_owner_decision','relationship_owner_decision','locator_owner_decision',
            'owner_accepted_relationship_occurrences','locator_owner_reviewed_occurrences',
            'inventory_scope_plan','inventory_evaluator_compared_assigned_occurrences',
            'inventory_remaining_assigned_occurrences','inventory_remaining_assigned_ids']:
    assert s[key]==old[key],key
assert s['inventory_owner_reviewed_assigned_occurrences']==332
assert s['inventory_owner_pending_compared_occurrences']==0 and s['part_4d3_owner_review_complete']
assert s['inventory_remaining_assigned_ids']==41 and s['inventory_remaining_assigned_occurrences']==82
assert s['part_4d5_reconciliation_pending'] and not s['M_POC5A_closed']
assert not (R/'part-04d4').exists(),'This handoff must not execute .4d4'
changed=[x['path'] for x in start['protected'] if ref(ROOT/x['path'])!=x]
assert not changed,changed
sessions=P/'measurement/sessions.jsonl'; before=sessions.read_bytes(); prefix=start['sessions_before']
assert len(before)==prefix['bytes'] and sha(before)==prefix['sha256'] and before.endswith(b'\n')
logs=[]
for name in ['check-script.log','check-script-retry.log']:
    log=(M/name).read_text(encoding='utf-8-sig')
    checkroot=Path(re.search(r'LOG_ROOT=(.+)',log).group(1).strip())
    result=load(checkroot/'result.json')
    logs.append(dict(log=ref(M/name),result=ref(checkroot/'result.json'),
        pytest_log=ref(checkroot/'pytest.log'),diff_log=ref(checkroot/'diff-check.log'),
        tests_exit=result['tests_exit'],diff_exit=result['diff_exit'],unique_basetemp=result['basetemp']))
assert logs[0]['tests_exit']==1 and logs[0]['diff_exit']==0
assert logs[1]['tests_exit']==logs[1]['diff_exit']==0
assert '155 passed' in (M/'check-script-retry.log').read_text(encoding='utf-8-sig')
save(M/'operational-events.json',dict(events=[dict(
    kind='documentation_continuity_check_failure',
    observation='Initial HANDOFF included two Markdown links to session handoffs; exactly one latest pointer is required.',
    resolution='Historical session reference changed to plain code text; retry passed155 tests. No test or semantic decision changed.',
    evidence=logs[0])]))
save(M/'checks.json',dict(status='passed_after_documentation_fix',passed=155,
    local_tmp_temp=True,attempts=logs,real_logs_preserved=True))
artifacts=load(M/'artifacts.json')['artifacts']
save(M/'final-artifacts.json',dict(artifacts=[ref(ROOT/x['path']) for x in artifacts],
    supersedes_document_hashes=ref(M/'artifacts.json'),reason='Corrected historical HANDOFF pointer after continuity check.'))
save(M/'validation.json',dict(status='passed',owner_judgments=118,supported=114,
    related_mixed_or_omission=4,underlying_omitted_clauses_per_answer=1,
    full_original_scopes_and_run_traces_preserved=True,prior_inventory_scopes_preserved=214,
    total_owner_inventory_scopes=332,remaining_assigned_ids=41,remaining_occurrences=82,
    older_pending_expectations=8,older_unresolved_issues=13,
    old_relations_locators_expectations_and_dispositions_preserved=True,
    no_new_semantic_review=True,protected_files=len(start['protected'])))
save(M/'final-audit.json',dict(status='passed',protected_files=len(start['protected']),
    changed_protected_files=changed,previous_sessions_prefix_preserved=True,
    previous_sessions=prefix,public_aggregate_documents_intentionally_updated=True,
    final_artifacts=ref(M/'final-artifacts.json')))
now=datetime.now(timezone.utc)
completion=dict(id='M-POC5A-owner13-handoff-001',date='2026-10-11',timezone='Europe/Warsaw',
    card='M-POC5A.4d3-owner-review',milestone='M-POC5',outcome='partial_owner_accepted_handoff_prepared',
    author='Codex records explicit owner acceptance',owner_reply_verbatim=d['owner_reply_verbatim'],
    decision=ref(R/'owner-decision-13.json'),overlay=ref(R/'owner-review-overlay-13.json'),
    current_state=ref(R/'current-state-27.json'),
    prompt=ref(P/'prompts/semantic-review-part04d4-start-v1.txt'),
    handoff=ref(ROOT/'docs/handoff/2026-10-11-M-POC5A-owner13-handoff-01.md'),
    newly_owner_reviewed_inventory_occurrences=118,bounded_supported_occurrences=114,
    related_mixed_or_omission_occurrences=4,total_owner_inventory_scopes=332,
    compared_inventory_occurrences=332,new_semantic_comparisons=0,
    owner_pending_compared_inventory_occurrences=0,remaining_assigned_ids=41,remaining_assigned_occurrences=82,
    previous_pending_expectations=8,previous_unresolved_issue_ids=s['unresolved_issue_ids'],
    issue_disposition={'SEM-021':d['issue_disposition']['SEM-021']},
    remaining_cards=['M-POC5A.4d4','M-POC5A.4d5','M-POC5B'],
    next_part='M-POC5A.4d4',next_card='M-POC5A',next_milestone='M-POC5',whole_card_closed=False,
    checks=ref(M/'checks.json'),validation=ref(M/'validation.json'),
    operational_events=ref(M/'operational-events.json'),audit=ref(M/'final-audit.json'),
    recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),
    calendar_elapsed_seconds=(now-datetime.fromisoformat(start['recorded_at_utc'])).total_seconds(),
    active_model_time='unknown',active_user_time='unknown',model_selector='unknown',
    reasoning_selector='unknown',tokens='unknown',price='unknown',time_budget_compliance='unknown',
    actual_owner_file_open_or_read='unknown',full_metrics='not_assessable',
    new_sources=0,new_extractions=0,new_context_rounds=0,new_corrections=0,new_chats=0,situations_evaluated=0,
    git_publication='not requested; no commit/push',previous_measurement_prefix_preserved=True)
save(M/'completion.json',completion)
with sessions.open('ab') as f:
    f.write((json.dumps(dict(completion,completion=ref(M/'completion.json')),ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
after=sessions.read_bytes()
assert after[:len(before)]==before and len(after.splitlines())==len(before.splitlines())+1
save(M/'append-seal.json',dict(previous=prefix,after=ref(sessions),
    previous_prefix_preserved=True,new_records=1,completion=ref(M/'completion.json')))
assert all(ref(ROOT/x['path'])==x for x in start['protected'])
assert all(ref(ROOT/x['path'])==x for x in load(M/'final-artifacts.json')['artifacts'])
print(json.dumps(dict(status='passed',new_owner_judgments=118,total_owner_inventory=332,
    protected_files=len(start['protected']),tests_passed=155,session_records_appended=1)))
