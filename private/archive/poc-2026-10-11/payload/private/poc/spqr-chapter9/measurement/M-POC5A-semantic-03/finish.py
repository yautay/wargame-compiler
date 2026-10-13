"""Seal this comparison packet and append an honest scoped session measurement."""
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
OUT=REV/'part-03'
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(path,obj):
    assert not path.exists(),path
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
D=load(OUT/'comparisons.json')
assert D['owner_decisions']==[] and D['summary']['previous_owner_accepted_groups_per_answer']==22
for r in list(D['responses'].values())+[D['evaluation'],D['source']]:assert ref(ROOT/r['path'])==r
for r in load(OUT/'manifest.json')['artifacts']:assert ref(ROOT/r['path'])==r
assert ref(ROOT/D['prior_owner_decision']['path'])==D['prior_owner_decision']
checkroot=ROOT/'private/poc/_checks/active-bf54422bfbc1432a86356e30e1e63a25'
checks=load(checkroot/'result.json');assert checks['tests_exit']==0 and checks['diff_exit']==0
assert '123 passed' in (checkroot/'pytest.log').read_text(encoding='utf-8-sig')
assert load(M/'git-diff-check-result.json')['exit_code']==0
now=datetime.now(timezone.utc)
record=dict(id='M-POC5A-semantic-03-comparisons',card='M-POC5A',part='M-POC5A.3',milestone='M-POC5',
    outcome='partial',status='waiting_review',timezone='Europe/Warsaw',author='Codex',owner_instruction='kontynuuj',
    instruction_is_semantic_acceptance=False,first_recorded_clock_utc=start['first_recorded_clock_utc'],
    completed_at_utc=now.isoformat(),recorded_calendar_elapsed_seconds=(now-datetime.fromisoformat(start['first_recorded_clock_utc'])).total_seconds(),
    timing_limitation='First clock after bootstrap; recorded calendar is not active user/model time.',
    active_user_time='unknown',active_model_time='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',
    actual_model_selector='unknown',reasoning_selector='unknown',tokens='unknown',price='unknown',
    evaluation=D['evaluation'],responses=D['responses'],source=D['source'],summary=D['summary'],
    previous_owner_decision=D['prior_owner_decision'],previous_accepted_local_groups_per_answer=22,
    new_owner_decisions=[],new_semantic_acceptance='not_performed',
    current_state=ref(REV/'current-state-04.json'),
    presentation=dict(packet=ref(OUT/'owner-focus.md'),open_result='queued; owner open unknown',
        new_questions=['SEM-P03-POSITIVE','SEM-010'],previous_pending_preserved=True),
    new_extractions=0,new_context_rounds=0,new_corrections=0,situations_evaluated=0,
    preserved_context_totals=D['limits'],preserved_operational_limitations=D['limitations'],
    source_expansion=0,full_graph_depth_compliance='not_assessable',
    full_semantic_metrics='not_assessable',semantic_TP_FP_FN='not_assessable',
    protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,
    tooling_diagnostic=D['tooling_diagnostic'],
    checks=dict(passed=123,result=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),
        script_diff_log=ref(checkroot/'diff-check.log'),explicit_diff_result=ref(M/'git-diff-check-result.json'),
        explicit_diff_log=ref(M/'git-diff-check.log'),comparison_validation=ref(M/'validation.json'),
        local_tmp_temp=True,unique_basetemp=checks['basetemp'],
        limitations='Structural checks do not approve meaning. CRLF normalization warnings in three public documents, no diff errors.'),
    artifacts=[ref(f) for f in sorted(OUT.iterdir()) if f.is_file()],
    resume='Owner decisions for exact part-03 positive scopes and SEM-010, prior pending alternatives. Separate .4 with 24 expectations and remaining inventory/edges/locators; split before work if beyond 90 minutes.',
    next_card='M-POC5A',next_milestone='M-POC5',git_publication='not_requested; no commit or push')
save(M/'completion.json',record)
sessions=P/'measurement/sessions.jsonl';old=sessions.read_bytes();before=start['sessions_before']
assert len(old)==before['bytes'] and hashlib.sha256(old).hexdigest()==before['sha256']
assert old.endswith(b'\n') and record['id'].encode() not in old
entry=dict(record,completion=ref(M/'completion.json'))
with sessions.open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
assert sessions.read_bytes()[:len(old)]==old
save(M/'append-seal.json',dict(previous=before,sessions_after=ref(sessions),added_records=1,original_prefix_preserved=True,
    completion=ref(M/'completion.json')))
print(json.dumps(dict(outcome='partial',status='waiting_review',passed=123,protected_files=len(start['protected']),
    previous_owner_accepted_groups_per_answer=22,new_owner_decisions=0,model_proposals=D['summary']['model_proposals'],
    measurement_appended=1),ensure_ascii=False))
