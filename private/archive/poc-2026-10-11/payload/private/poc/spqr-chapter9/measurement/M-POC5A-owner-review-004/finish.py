"""Verify bounded human-decision materialization and seal append-only measurement."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;REV=P/'reviews/semantic-01'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json');d=load(REV/'owner-decision-04.json');o=load(REV/'owner-review-overlay-04.json');old=load(REV/'owner-review-overlay-03.json');s=load(REV/'current-state-10.json')
packet=load(REV/'part-04b1/comparisons.json');pres=load(REV/'part-04b1/presentation.json');byid={x['id']:x for x in packet['relationships']}
assert d['accepted_relation_ids']==pres['positive_scope']['ids']
assert {x['id'] for x in d['scopes']}==set(d['accepted_relation_ids']) and len(d['scopes'])==60
assert not set(d['accepted_relation_ids'])&set(packet['summary']['separate_issue_ids'])
count=0;field_count=0
for run,a in d['responses'].items():
    raw=(ROOT/a['path']).read_bytes();assert sha(raw)==a['sha256'] and len(raw)==a['bytes']
    chosen=[x for x in d['scopes'] if run in x['runs']]
    assert len(chosen)==d['per_answer'][run]==len(o['runs'][run]['relationship_scopes'])
    for x in chosen:
        base=byid[x['id']];assert x['source_scope']==base['source_scope'] and x['target_scope']==base['target_scope']
        assert x['source_evidence']==base['source_evidence'] and x['target_evidence']==base['target_evidence']
        trace=x['runs'][run];sp=trace['edge_raw_span'];b=raw[sp['start_byte']:sp['end_byte_exclusive']]
        assert sha(b)==sp['sha256'] and json.loads(b)==base['runs'][run]['output_trace'][x['id']]['original_record'];count+=1
        for f in trace['edge_field_trace'].values():
            sp=f['raw_span'];b=raw[sp['start_byte']:sp['end_byte_exclusive']]
            assert sha(b)==sp['sha256'] and json.loads(b)==f['original_value'];field_count+=1
        assert trace['whole_record_accepted'] is False and trace['full_result_accepted'] is False
    for k in ['scopes','context_requirements','accepted_scoped_groups','reviewed_context_groups']:
        assert o['runs'][run][k]==old['runs'][run][k]
assert count==116 and d['separate_issue_occurrences']==9
for k in ['category_units','category_accepted_scope_counts','pending_expectation_ids','illustration_states','all_locator_review']:
    assert o[k]==old[k]
assert s['owner_pending_relationship_occurrences']==141 and s['remaining_uncompared_relationship_occurrences']==132
assert len(s['pending_expectation_ids'])==8 and len(o['category_units'])==264
assert d['unresolved_issue_ids']==[f'SEM-{n:03}' for n in range(1,17)]
save(M/'validation.json',dict(status='passed',accepted_scoped_occurrences=count,edge_fields_verified=field_count,per_answer=d['per_answer'],pending_4b1=9,
    prior_expectation_and_category_scopes_unchanged=True,earlier_and_separate_issues_kept_open=True,whole_record_acceptance=False,semantic_metrics='not_assessable'))
changed=[a['path'] for a in start['protected'] if not (ROOT/a['path']).exists() or ref(ROOT/a['path'])!=a];assert not changed,changed
sessions=P/'measurement/sessions.jsonl';before=sessions.read_bytes();prefix=start['sessions_before']
assert len(before)==prefix['bytes'] and sha(before)==prefix['sha256']
save(M/'final-audit.json',dict(status='passed',protected_files=len(start['protected']),changed_protected_files=changed,previous_sessions_prefix_preserved=True,
    previous_sessions=prefix,old_decisions_packages_measurements_responses_eval_sources_preserved=True,scope='All existing files under private P captured before decision, excluding new measurement and append-only sessions. Public docs intentionally updated.'))
log=(M/'check-script.log').read_text(encoding='utf-8-sig');match=re.search(r'LOG_ROOT=(.+)',log);assert match
testroot=Path(match.group(1).strip());checks=load(testroot/'result.json');assert checks['tests_exit']==checks['diff_exit']==0
assert '136 passed' in log and load(M/'git-diff-check-result.json')['exit_code']==0
now=datetime.now(timezone.utc)
completion=dict(id='M-POC5A-owner-review-004',date='2026-10-11',timezone='Europe/Warsaw',card='M-POC5A',part='M-POC5A.4b1-owner-review',milestone='M-POC5',outcome='partial',author='Codex recording direct owner decision',
    owner_reply_verbatim=d['owner_reply'],decision=ref(REV/'owner-decision-04.json'),overlay=ref(REV/'owner-review-overlay-04.json'),current_state=ref(REV/'current-state-10.json'),
    accepted_scoped_relation_occurrences=116,per_answer=d['per_answer'],pending_assigned_4b1=9,remaining_without_owner_relation_scope=141,remaining_uncompared_other_parts=132,pending_expectations=8,
    whole_record_acceptance=False,full_graph_certified=False,metrics='not_assessable',recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),
    calendar_elapsed_seconds=(now-datetime.fromisoformat(start['recorded_at_utc'])).total_seconds(),active_user_time='unknown',active_model_time='unknown',tokens='unknown',price='unknown',time_budget_compliance='unknown',
    timing_limitation='Calendar interval for recording decision, not active budget or extraction time.',
    checks=dict(passed=136,result=ref(testroot/'result.json'),pytest_log=ref(testroot/'pytest.log'),diff_log=ref(M/'git-diff-check.log'),diff_result=ref(M/'git-diff-check-result.json'),local_tmp_temp=True,unique_basetemp=checks['basetemp']),
    validation=ref(M/'validation.json'),audit=ref(M/'final-audit.json'),protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,
    decision_artifacts=load(M/'decision-artifacts.json')['artifacts'],new_extractions=0,new_sources=0,new_context_rounds=0,new_corrections=0,new_chats=0,situations_evaluated=0,
    next_card='M-POC5A',next_part='M-POC5A.4b2',next_milestone='M-POC5',whole_card_closed=False,
    resume='Next separate .4b2:30IDs/60occurrences from existing scope-plan. Estimate before execution; preserve all earlier/separate pending. No further part executed in this owner-decision turn.',git_publication='not requested; no commit/push')
save(M/'completion.json',completion)
assert before.endswith(b'\n')
with sessions.open('ab') as f:f.write((json.dumps(dict(completion,completion=ref(M/'completion.json')),ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
after=sessions.read_bytes();assert after[:len(before)]==before and len(after.splitlines())==len(before.splitlines())+1
save(M/'append-seal.json',dict(previous=prefix,after=ref(sessions),previous_prefix_preserved=True,new_records=1,completion=ref(M/'completion.json')))
assert all(ref(ROOT/a['path'])==a for a in start['protected'])
print(json.dumps(dict(accepted_scoped_occurrences=116,pending_4b1=9,tests_passed=136,protected_preserved=len(start['protected']),sessions_append_only=True)))
