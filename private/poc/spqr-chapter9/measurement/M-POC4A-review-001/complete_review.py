"""Check the immutable review/freeze/transfer; append the real completion once."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
ROOT=Path.cwd();P=ROOT/'private/poc/spqr-chapter9'
M=P/'measurement/M-POC4A-review-001';E=P/'evaluation/M-POC4A-review-001'
C=P/'context/pass-01';T=P/'transfer/context-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(x):
    b=x.read_bytes();return dict(path=x.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def load(x):return json.loads(x.read_bytes())
def save(x,obj):
    assert not x.exists(),x
    x.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
before=load(M/'protected-before.json')
for a in before:assert desc(ROOT/a['path'])==a,a['path']
for a in load(P/'measurement/M-POC4A-pass-01/protected-before.json'):
    b=(ROOT/a['path']).read_bytes()
    if a['path'].endswith('/measurement/sessions.jsonl'):b=b[:a['bytes']]
    assert len(b)==a['bytes'] and sha(b)==a['sha256'],a['path']
freeze=load(C/'freeze-v1.json')
for a in freeze['frozen_files']+freeze['approved_source_files']+[freeze['decision'],freeze['request'],freeze['original_draft_manifest'],freeze['transfer_manifest'],freeze['execution_prompt'],freeze['mechanical_addendum']]:
    assert desc(ROOT/a['path'])==a,a['path']
manifest=load(T/'context/pass-01/manifest.json')
allowed=(T/'transfer-list.txt').read_text('utf-8').splitlines()
actual={x.relative_to(T).as_posix() for x in T.rglob('*') if x.is_file()}
assert len(allowed)==len(set(allowed))==42 and actual==set(allowed)
assert len(manifest['artifacts'])==41
for a in manifest['artifacts']:
    b=(T/a['path']).read_bytes();assert len(b)==a['bytes'] and sha(b)==a['sha256'],a['path']
assert not any(x.startswith(('evaluation/','reports/','measurement/')) for x in actual)
assert not any(x.endswith(('.pdf','review.md','targets.json','critical-source-audit.json','declaration-review.json')) for x in actual)
run=load(P/'runs/first-001/run.json')
original={f['package_path'] for f in run['inputs']['known_prepared_package_files']}
extra={'parent/first-001.json','formats/context-addendum-v1.md','prompts/context-v1.txt','transfer-list.txt',
       'context/pass-01/manifest.json','context/pass-01/freeze-public-v1.json',
       *('context/pass-01/evidence/'+n for n in ['8.46-step-4-pdf-27.png','8.46-step-4-helper.txt','8.46-step-4-scope.json'])}
assert actual==original|extra
for f in run['inputs']['known_prepared_package_files']:assert (T/f['package_path']).read_bytes()==(ROOT/f['canonical_path']).read_bytes()
assert (T/'parent/first-001.json').read_bytes()==(P/'runs/first-001/first-001.json').read_bytes()
assert manifest['source_scope']['additional_unique_pages']==[27] and manifest['source_scope']['additional_rule_ids']==['8.46']
assert manifest['source_scope']['additional_table_ids']==[] and manifest['source_scope']['performed_context_rounds']==0
assert manifest['frozen'] and manifest['assessment_content_included'] is False
assert freeze['semantic_acceptance']=='not_performed' and freeze['time_budget_compliance']=='unknown'
save(M/'protected-after.json',dict(all_match_before=True,count=len(before),files=before,
    earlier_baseline_protected_files_and_prefix=134,earlier_baseline_all_match=True))
save(M/'transfer-verification.json',dict(manifest=desc(T/'context/pass-01/manifest.json'),
    freeze=desc(C/'freeze-v1.json'),files=42,original_inputs_copied_byte_identical=33,
    parent_byte_identical=True,exact_allowlist_only=True,assessment_and_reports_absent=True,
    extra_files=sorted(extra),scope_delta=dict(pages=1,rules=1,tables=0,selected_depth=1,longest_depth=2),
    source_selection_accepted=True,semantic_acceptance='not_performed',transfer_state='prepared_not_sent'))
checkroot=ROOT/'private/poc/_checks/active-d809f8323e9149fb9aca1c07c4791e01'
check=json.loads((checkroot/'result.json').read_text('utf-8-sig'))
assert check['tests_exit']==check['diff_exit']==0 and '113 passed' in (checkroot/'pytest.log').read_text('utf-8-sig')
diff=subprocess.run(['git','diff','--check'],capture_output=True)
(M/'diff-check.log').write_bytes(diff.stdout+diff.stderr);assert diff.returncode==0
sessions=P/'measurement/sessions.jsonl';prefix=sessions.read_bytes()
prefixdesc=next(a for a in before if a['path']==desc(sessions)['path']);assert desc(sessions)==prefixdesc
end=datetime.datetime.now(datetime.timezone.utc)
clock=datetime.datetime(2026,10,10,14,37,47,tzinfo=datetime.timezone.utc)
record=dict(id='M-POC4A-review-001-freeze',date='2026-10-10',timezone='Europe/Warsaw',card='M-POC4A',
    milestone='M-POC4',outcome='done',scope='Owner approval of bounded source selection, additive freeze, isolated manual transfer preparation; no inference',
    phase='source_review_and_freeze',workflow_status='frozen_prepared_not_sent',milestone_status='next',
    first_recorded_clock_utc=clock.isoformat(),completed_at_utc=end.isoformat(),recorded_calendar_elapsed_seconds=(end-clock).total_seconds(),
    time_limitation='Clock recorded after approval and initial reads. Calendar interval excludes prior review waits and does not measure active time.',
    user_active_time='unknown',model_active_time='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',
    actual_model_visible_name='unknown',reasoning_level='unknown',tokens='unknown',price='unknown',
    first_run_configuration='unknown',historical_first_transfer='unknown',historical_first_clean_context='unknown',
    decision=desc(E/'decision-01.json'),review_closure=desc(E/'review-closure-01.json'),freeze=desc(C/'freeze-v1.json'),
    original_context_draft_manifest=desc(C/'manifest.json'),transfer_manifest=desc(T/'context/pass-01/manifest.json'),
    parent_response=desc(P/'runs/first-001/first-001.json'),assessment_version='eval-v1',
    evaluation_manifest=desc(P/'evaluation/eval-v1/manifest.json'),source_acceptance='owner_approved_exact_selection_scope',
    human_review=dict(reply='Zatwierdzam',scope='Source selection and bounded scope only',actual_owner_image_open='unknown',semantic_acceptance='not_performed'),
    semantic_acceptance='not_performed',semantic_result='not_assessable',limits_changed=False,
    counters=dict(additional_pages=1,additional_rules=1,additional_tables=0,selected_depth=1,longest_considered_depth=2,
        reserved_context_round=1,context_response_rounds=0,new_inference_responses=0,new_corrections=0),
    blocked_sources_retained=True,pending_candidates_and_frozen_expectations_unchanged=True,
    outputs=[dict(**desc(x),reason='Scoped owner decision/freeze, unchanged source preview or isolated context-transfer artifact',scope='One prepared pass, no extraction or semantic acceptance')
        for folder in [E,T] for x in sorted(folder.rglob('*')) if x.is_file()]+[dict(**desc(C/'freeze-v1.json'),reason='Authoritative additive freeze; draft bytes retained',scope='Approved source selection only')],
    audit_evidence=[desc(x) for x in sorted(M.iterdir()) if x.is_file()],
    protected_files_unchanged=len(before),earlier_baseline_protected_files_and_prefix_unchanged=134,
    transfer_allowlist_files=42,transfer_state='prepared_not_sent',sessions_append_baseline=prefixdesc,
    checks=dict(script='scripts/check.ps1',passed=113,tests_exit=0,diff_exit=0,result=desc(checkroot/'result.json'),
        pytest_log=desc(checkroot/'pytest.log'),script_diff_log=desc(checkroot/'diff-check.log'),standalone_diff_log=desc(M/'diff-check.log'),
        basetemp=check['basetemp'],tmp_temp_policy='Local GUID run root and previously nonexistent basetemp; offline'),
    next_card='M-POC4B',next_action='Owner manually opens separate isolated session in transfer/context-v1, reads allowlist/manifest and prompts/context-v1.txt, obtains one context-01.json. Evaluator then performs M-POC4B receipt/report; do not generate extraction in evaluator chat.',
    no_new_chat_created=True,M_POC4B_executed=False)
save(M/'completion.json',record)
assert prefix.endswith(b'\n') and not any(json.loads(x)['id']==record['id'] for x in prefix.splitlines())
line=dict(record,completion=desc(M/'completion.json'))
with sessions.open('ab') as stream:stream.write((json.dumps(line,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
assert sessions.read_bytes()[:len(prefix)]==prefix
save(M/'append-verification.json',dict(record_id=record['id'],previous_prefix=prefixdesc,prefix_preserved=True,
    completion=desc(M/'completion.json'),sessions_after=desc(sessions)))
print(json.dumps(dict(completion=desc(M/'completion.json'),tests_passed=113,protected_unchanged=len(before),
    earlier_baseline_protected=134,allowlist=42,prefix_preserved=True),indent=2))
