"""Save planning state and audit/measure the prompt preparation only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01';sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_bytes().decode('utf-8-sig'))
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json');plan=load(M/'scope-plan.json');prompt=P/'prompts/semantic-review-part04b1-start-v1.txt'
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
old=load(REV/'current-state-07.json')
for r in [old['decision'],old['overlay'],old['evaluation']]+list(old['responses'].values()):assert ref(ROOT/r['path'])==r
if sys.argv[1]=='state':
    state=dict(old)
    state.update(id='M-POC5A-current-state-08',part='M-POC5A.4b-planning',next_part='M-POC5A.4b1',previous_state=ref(REV/'current-state-07.json'),scope_plan=ref(M/'scope-plan.json'),next_session_prompt=ref(prompt),split_before_execution=True,parts_4b1_4b2_4b3_not_executed=True,semantic_state_unchanged=True,resume='Owner manually starts a new local session with the saved .4b1 prompt. Estimate first; split further before review if needed. .4b2/.4b3/.4c/.4d separate, all earlier pending preserved.')
    save(REV/'current-state-08.json',state)
elif sys.argv[1]=='validate':
    actual={r:{d['id'] for d in load(P/f'proposals/{r}/proposal.json')['dependencies']} for r in ['first-001','context-01']}
    sets=[set(s['output_edge_ids']) for s in plan['parts']]
    assert not any(sets[a]&sets[b] for a in range(3) for b in range(a+1,3))
    assert set.union(*sets)==set.union(*actual.values()) and sum(map(len,sets))==131
    assert [len(s) for s in sets]==[65,30,36]
    for s in plan['parts']:
        assert s['semantic_review']=='not_performed' and s['status']=='planned'
        for r,ids in actual.items():assert s['occurrences'][r]==len(set(s['output_edge_ids'])&ids)
    text=prompt.read_text(encoding='utf-8')
    for t in ['C:\\repo\\wargame-compiler','feature/tests','current-state-08.json','63/66','3/8','8 oczekiwań','65 ID','125 wystąpień','PO LUDZKU','PRZED wykonaniem','scripts/check.ps1','git diff --check']:
        assert t in text,t
    for r in list(old['responses'].values())+[old['evaluation']]:assert r['sha256'] in text
    assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
    cur=load(REV/'current-state-08.json')
    for k in ['decision','overlay','evaluation','responses','pending_expectation_ids','owner_accepted_local_groups_per_answer','reviewed_context_requirements_per_answer']:assert cur[k]==old[k],k
    assert cur['next_part']=='M-POC5A.4b1' and not cur['M_POC5A_closed']
    artifacts=[ref(prompt),ref(M/'scope-plan.json'),ref(REV/'current-state-08.json')]+[ref(ROOT/f'docs/work/tasks/semantic/M-POC5A.4b{n}.md') for n in [1,2,3]]
    save(M/'validation.json',dict(result='passed',protected_files=len(start['protected']),split_before_execution=True,part_id_counts=[65,30,36],part_occurrences=[125,60,72],all_257_occurrences_assigned_once=True,prior_semantic_state_unchanged=True,no_edge_review_performed=True,artifacts=artifacts))
    print('Prompt and exhaustive split validated; no relation reviewed.')
elif sys.argv[1]=='finish':
    v=load(M/'validation.json')
    for r in v['artifacts']:assert ref(ROOT/r['path'])==r
    log=(M/'check-script.log').read_text(encoding='utf-8-sig');checkroot=Path(re.search(r'LOG_ROOT=(.+)',log).group(1).strip())
    checks=load(checkroot/'result.json');passed=int(re.search(r'(\d+) passed',log).group(1))
    assert checks['tests_exit']==checks['diff_exit']==0 and load(M/'git-diff-check-result.json')['exit_code']==0
    now=datetime.now(timezone.utc)
    record=dict(id='M-POC5A-part04b-preparation-001-prompt-and-split',date='2026-10-11',timezone='Europe/Warsaw',card='M-POC5A',part='M-POC5A.4b-planning',milestone='M-POC5',outcome='partial',author='Codex',owner_request=start['request'],scope='Prompt and metadata-only exhaustive partition; no semantic edge review or owner acceptance.',recorded_start_utc=start['recorded_at_utc'],completed_at_utc=now.isoformat(),calendar_elapsed_seconds=(now-datetime.fromisoformat(start['recorded_at_utc'])).total_seconds(),active_user_time='unknown',active_model_time='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',tokens='unknown',price='unknown',actual_model_selector='unknown',reasoning_selector='unknown',timing_limitation='Calendar after bootstrap, not active user/model time.',current_state=ref(REV/'current-state-08.json'),owner_accepted_local_per_answer=63,reviewed_context_requirements_per_answer=3,pending_expectations=8,category_units=264,semantic_state_unchanged=True,relations_reviewed=0,new_owner_decisions=0,semantic_TP_FP_FN='not_assessable',full_graph_certified=False,next_part='M-POC5A.4b1',scope_plan=ref(M/'scope-plan.json'),next_session_prompt=ref(prompt),parts_4b1_4b2_4b3_not_executed=True,new_chat_created=False,new_extractions=0,new_sources=0,new_context_rounds=0,new_corrections=0,situations_evaluated=0,protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,checks=dict(passed=passed,result=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),diff_log=ref(M/'git-diff-check.log'),diff_result=ref(M/'git-diff-check-result.json'),prompt_validation=ref(M/'validation.json'),local_tmp_temp=True,unique_basetemp=checks['basetemp']),artifacts=v['artifacts'],next_card='M-POC5A',next_milestone='M-POC5',whole_card_closed=False,git_publication='not_requested; no commit/push')
    sessions=P/'measurement/sessions.jsonl';b=sessions.read_bytes();before=start['sessions_before']
    assert len(b)==before['bytes'] and hashlib.sha256(b).hexdigest()==before['sha256'] and b.endswith(b'\n')
    assert record['id'].encode() not in b
    save(M/'completion.json',record)
    with sessions.open('ab') as f:f.write((json.dumps(dict(record,completion=ref(M/'completion.json')),ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
    assert sessions.read_bytes()[:len(b)]==b
    save(M/'append-seal.json',dict(previous=before,sessions_after=ref(sessions),completion=ref(M/'completion.json'),added_records=1,original_prefix_preserved=True))
    print(json.dumps(dict(passed=passed,protected_files=len(start['protected']),scope_ids=[65,30,36],edge_review_performed=False,measurement_appended=1)))
