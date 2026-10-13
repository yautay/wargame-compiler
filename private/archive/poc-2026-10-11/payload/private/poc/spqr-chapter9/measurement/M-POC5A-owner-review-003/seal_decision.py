"""Validate exact acceptance/preservation, then seal and append its measurement."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent;REV=P/'reviews/semantic-01'
sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_bytes().decode('utf-8-sig'))
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def resolve(o,pointer):
    for k in pointer.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');o=o[int(k)] if isinstance(o,list) else o[k]
    return o
start=load(M/'start.json');decision=load(REV/'owner-decision-03.json');overlay=load(REV/'owner-review-overlay-03.json')
prior=load(REV/'owner-review-overlay-02.json');D=load(REV/'part-04a/comparisons.json');C=load(REV/'checklist.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
for r in load(M/'decision-artifacts.json')['artifacts']:assert ref(ROOT/r['path'])==r
for r in list(C['responses'].values())+[C['evaluation'],C['source']]:assert ref(ROOT/r['path'])==r
expected={f'EXP-{n:03}' for n in [51]+list(range(53,66))+list(range(67,74))}
assert decision['owner_reply']=='zatwierdzzm' and len(decision['scopes'])==21
assert {s['id'] for s in decision['scopes']}==expected
assert decision['context_acceptance_is_gap_closure'] is False and decision['M_POC5A_closed'] is False
assert decision['date']=='2026-10-11'
for s in decision['scopes']:
    e=next(e for e in D['expectations'] if e['id']==s['id'])
    assert s['reviewed_scope']==e['source_scope'] and s['source_evidence']==e['source_evidence']
    assert s['status']=='reviewed' and s['reviewer']==decision['reviewer']
    assert s['whole_record_accepted'] is False
    if s['id']=='EXP-064':assert s['result']=='correct_source_requirement_declaration' and s['full_dependent_result']=='blocked_source'
    else:assert s['result']=='correct_in_owner_accepted_scope'
    for run,traces in s['output_trace'].items():
        raw=(ROOT/C['responses'][run]['path']).read_bytes();obj=json.loads(raw)
        for rid,t in traces.items():
            assert t['pointer']==e['runs'][run]['output_trace'][rid]['pointer']
            span=t['raw_span'];b=raw[span['start_byte']:span['end_byte_exclusive']]
            assert hashlib.sha256(b).hexdigest()==span['sha256'] and json.loads(b)==resolve(obj,t['pointer'])
for run,r in overlay['runs'].items():
    assert len(r['scopes'])==63 and len({s['id'] for s in r['scopes']})==63
    assert r['scopes'][:43]==prior['runs'][run]['scopes']
    assert r['context_requirements'][:2]==prior['runs'][run]['context_requirements']
    assert len(r['context_requirements'])==3
    assert r['pending_content_groups']==3 and r['pending_context_groups']==5
    assert all(s['response']==C['responses'][run] for s in r['scopes']+r['context_requirements'])
    assert all(s['full_dependent_result']=='blocked_source' for s in r['context_requirements'])
    assert r['complete_rule_quality']=='not_assessable' and r['semantic_TP_FP_FN']=='not_assessable'
assert len(overlay['category_units'])==264 and len({r['id'] for r in overlay['category_units']})==264
assert overlay['category_units'][:175]==prior['category_units']
assert Counter(r['category'] for r in overlay['category_units'])==overlay['category_accepted_scope_counts']
assert overlay['pending_expectation_ids']==[f'EXP-{n:03}' for n in [10,17,19,40,50,52,66,74]]
assert overlay['all_output_edges_review']=='pending' and overlay['all_locator_review']=='unchanged'
assert overlay['pending_prior_issue_ids']==prior['pending_prior_issue_ids']+['SEM-011','SEM-012','SEM-013']
cur=load(REV/'current-state-07.json')
assert cur['decision']==ref(REV/'owner-decision-03.json') and cur['overlay']==ref(REV/'owner-review-overlay-03.json')
assert cur['previous_state']==ref(REV/'current-state-06.json')
assert cur['remaining_pending_expectations']==8 and cur['next_part']=='M-POC5A.4b'
assert cur['remaining_uncompared_expectations']==0 and not cur['M_POC5A_closed'] and not cur['M_POC5A_4_closed']
if sys.argv[1]=='validate':
    assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
    save(M/'validation.json',dict(result='passed',new_local_scopes_per_answer=20,new_context_requirements_per_answer=1,local_groups_per_answer=63,context_requirements_per_answer=3,pending_expectations=8,category_units=264,protected_files=len(start['protected']),all_prior_pending_preserved=True,all_prior_accepted_scopes_preserved=True,source_requirements_still_block_full_results=True,whole_card='partial',next_part='M-POC5A.4b'))
    print('Exact scope and original-byte validation passed.')
elif sys.argv[1]=='finish':
    checklog=(M/'check-script.log').read_text(encoding='utf-8-sig');checkroot=Path(re.search(r'LOG_ROOT=(.+)',checklog).group(1).strip())
    checks=load(checkroot/'result.json');passed=int(re.search(r'(\d+) passed',checklog).group(1))
    assert checks['tests_exit']==checks['diff_exit']==0
    assert load(M/'git-diff-check-result.json')['exit_code']==0
    now=datetime.now(timezone.utc)
    record=dict(id='M-POC5A-owner-review-003-acceptance',card='M-POC5A',part='M-POC5A.4a-owner-review',milestone='M-POC5',outcome='partial',status='remaining_waiting_review',date='2026-10-11',timezone='Europe/Warsaw',author='Codex',owner_reply=decision['owner_reply'],recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),recorded_calendar_elapsed_seconds=(now-datetime.fromisoformat(start['recorded_at_utc'])).total_seconds(),timing_limitation='Recorded clock after bootstrap; calendar is not active user/model time.',active_user_time='unknown',active_model_time='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',actual_model_selector='unknown',reasoning_selector='unknown',tokens='unknown',price='unknown',new_local_scopes_per_answer=20,new_context_requirements_per_answer=1,cumulative_local_scopes_per_answer=63,local_denominator=66,pending_local=3,cumulative_context_requirements_per_answer=3,context_denominator=8,pending_context=5,pending_expectations=8,scoped_category_units=264,context_full_results='blocked_source; acceptance of source need is not gap closure',full_metrics='not_assessable',semantic_TP_FP_FN='not_assessable',whole_card_closed=False,owner_decision=ref(REV/'owner-decision-03.json'),overlay=ref(REV/'owner-review-overlay-03.json'),current_state=ref(REV/'current-state-07.json'),approval_evidence=ref(M/'approval-evidence.json'),evaluation=decision['evaluation'],responses=decision['responses'],source=decision['source'],exclusions=decision['excluded'],owner_file_or_image_open_verified=False,new_extractions=0,new_context_rounds=0,new_corrections=0,situations_evaluated=0,parts_4b_4c_4d_not_executed=True,new_chat_created=False,context_totals=D['limits'],full_gap_closures=0,partial_updates_retained_blocking=4,new_context_declarations_retained=4,third_step_source_acquired=False,full_graph_depth_compliance='not_assessable',assessment_exposure='unknown',clean_context='unknown',scope_discovery_outside_allowlist='confirmed_context_session',contamination_proven=False,full_isolation_proven=False,protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,checks=dict(passed=passed,result=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),script_diff_log=ref(checkroot/'diff-check.log'),script_call_log=ref(M/'check-script.log'),explicit_diff_result=ref(M/'git-diff-check-result.json'),explicit_diff_log=ref(M/'git-diff-check.log'),decision_validation=ref(M/'validation.json'),local_tmp_temp=True,unique_basetemp=checks['basetemp'],limitation='Structural checks do not accept meaning; actual human acceptance recorded separately.'),artifacts=load(M/'decision-artifacts.json')['artifacts'],public_documents=[ref(ROOT/f) for f in ['docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md','docs/work/tasks/semantic/M-POC5A.4a.md','docs/handoff/2026-10-11-M-POC5A-owner-review-03.md']],next_card='M-POC5A',next_milestone='M-POC5',next_part='M-POC5A.4b',resume=cur['resume'],git_publication='not_requested; no commit or push')
    sessions=P/'measurement/sessions.jsonl';old=sessions.read_bytes();before=start['sessions_before']
    assert len(old)==before['bytes'] and hashlib.sha256(old).hexdigest()==before['sha256'] and old.endswith(b'\n')
    assert record['id'].encode() not in old
    save(M/'completion.json',record);entry=dict(record,completion=ref(M/'completion.json'))
    with sessions.open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
    assert sessions.read_bytes()[:len(old)]==old
    save(M/'append-seal.json',dict(previous=before,sessions_after=ref(sessions),added_records=1,original_prefix_preserved=True,protected_files_preserved=len(start['protected']),completion=ref(M/'completion.json')))
    print(json.dumps(dict(passed=passed,local_scopes=63,context_requirements=3,pending=8,protected_files=len(start['protected']),measurement_appended=1),ensure_ascii=False))
