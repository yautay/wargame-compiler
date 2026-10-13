"""Seal the second proposal packet and append a measurement, not owner acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
OUT=P/'reviews/semantic-01/part-02'
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(path,obj):
    assert not path.exists(),path
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
D=load(OUT/'comparisons.json')
assert D['owner_decisions']==[]
for r in list(D['responses'].values())+[D['evaluation'],D['source']]:assert ref(ROOT/r['path'])==r
manifest=load(OUT/'manifest.json')
for r in manifest['artifacts']:assert ref(ROOT/r['path'])==r
checkroot=ROOT/'private/poc/_checks/active-a1452919b5224bf4a102e4af93ae9089'
checks=load(checkroot/'result.json');assert checks['tests_exit']==0 and checks['diff_exit']==0
assert '121 passed' in (checkroot/'pytest.log').read_text(encoding='utf-8-sig')
assert load(M/'git-diff-check-result.json')['exit_code']==0
now=datetime.now(timezone.utc)
record=dict(id='M-POC5A-semantic-02-comparisons',card='M-POC5A',part='M-POC5A.2',milestone='M-POC5',
    outcome='partial',status='waiting_review',timezone='Europe/Warsaw',author='Codex',
    user_instruction='ok kontynuuj',instruction_is_semantic_acceptance=False,
    first_recorded_clock_utc=start['first_recorded_clock_utc'],completed_at_utc=now.isoformat(),
    recorded_calendar_elapsed_seconds=(now-datetime.fromisoformat(start['first_recorded_clock_utc'])).total_seconds(),
    timing_limitation='First recorded clock after resumption bootstrap; calendar is not active user/model time.',
    active_user_time='unknown',active_model_time='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',
    actual_model_selector='unknown',reasoning_selector='unknown',tokens='unknown',price='unknown',
    evaluation=D['evaluation'],responses=D['responses'],source=D['source'],summary=D['summary'],
    human_decisions=[],semantic_acceptance='not_performed',
    owner_presentation=dict(previous_questions='SEM-001/002/003 pending',new_questions=['SEM-P02-LOCAL','SEM-009'],
        owner_report_or_image_open_verified=False,packet=ref(OUT/'owner-focus.md')),
    remaining_expectations=49,remaining_parts=['M-POC5A.3','M-POC5A.4'],
    previous_part_review_gate_not_closed=True,
    new_extractions=0,new_context_rounds=0,new_corrections=0,situations_evaluated=0,
    preserved_limits=D['limits'],preserved_operational_limitations=D['limitations'],
    protected_files_preserved=len(start['protected']),previous_review_and_measurement_bytes_preserved=True,
    artifacts=[ref(f) for f in sorted(OUT.iterdir()) if f.is_file()]+[ref(P/'reviews/semantic-01/current-state-02.json')],
    checks=dict(passed=121,results=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),
        script_diff_log=ref(checkroot/'diff-check.log'),explicit_diff_result=ref(M/'git-diff-check-result.json'),
        explicit_diff_log=ref(M/'git-diff-check.log'),comparison_integrity=ref(M/'validation.json'),
        local_tmp_temp=True,unique_basetemp=checks['basetemp'],
        limitations='Structural/evidence checks do not approve meaning. Three public-doc CRLF normalization warnings, no diff errors.'),
    resume='Owner exact-scope/hash decisions from focus-01.md and part-02/owner-focus.md; then remaining pending and next separate parts. Do not repair extraction.',
    git_publication='not_requested; no commit or push performed',next_card='M-POC5A',next_milestone='M-POC5')
save(M/'completion.json',record)
sessions=P/'measurement/sessions.jsonl';old=sessions.read_bytes();before=start['sessions_before']
assert len(old)==before['bytes'] and hashlib.sha256(old).hexdigest()==before['sha256']
assert old.endswith(b'\n') and record['id'].encode() not in old
entry=dict(record,completion=ref(M/'completion.json'))
with sessions.open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
assert sessions.read_bytes()[:len(old)]==old
save(M/'append-seal.json',dict(previous=before,sessions_after=ref(sessions),added_records=1,original_prefix_preserved=True,
    completion=ref(M/'completion.json')))
print(json.dumps(dict(outcome='partial',status='waiting_review',passed=121,protected_files=len(start['protected']),
    proposals=D['summary']['model_proposals'],owner_decisions=0,measurement_appended=1),ensure_ascii=False))
