"""Append the measurement of one real, scoped owner acceptance."""
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
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(path,obj):
    assert not path.exists(),path
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
start=load(M/'start.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
decision=load(REV/'owner-decision-01.json')
assert decision['owner_reply']=='akceptuję' and len(decision['scopes'])==22
for r in load(M/'decision-artifacts.json')['artifacts']:assert ref(ROOT/r['path'])==r
checkroot=ROOT/'private/poc/_checks/active-5f1a04f487f6490da0767f3e683d8ee8'
checks=load(checkroot/'result.json');assert checks['tests_exit']==0 and checks['diff_exit']==0
assert '122 passed' in (checkroot/'pytest.log').read_text(encoding='utf-8-sig')
assert load(M/'git-diff-check-result.json')['exit_code']==0
now=datetime.now(timezone.utc)
record=dict(id='M-POC5A-owner-review-001-22-scopes',card='M-POC5A',part='M-POC5A.2-owner-review',milestone='M-POC5',
    outcome='partial',status='remaining_waiting_review',date='2026-10-10',timezone='Europe/Warsaw',author='Codex',
    first_recorded_clock_utc=start['first_recorded_clock_utc'],completed_at_utc=now.isoformat(),
    recorded_calendar_elapsed_seconds=(now-datetime.fromisoformat(start['first_recorded_clock_utc'])).total_seconds(),
    timing_limitation='Record clock after owner message/bootstrap; not exact owner message time or active user/model time.',
    active_user_time='unknown',active_model_time='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',
    actual_model_selector='unknown',reasoning_selector='unknown',tokens='unknown',price='unknown',
    owner_reply='akceptuję',semantic_owner_decisions_this_record=1,
    owner_decision=ref(REV/'owner-decision-01.json'),review_overlay=ref(REV/'owner-review-overlay-01.json'),
    current_state=ref(REV/'current-state-03.json'),evaluation=decision['evaluation'],responses=decision['responses'],
    accepted_exact_local_groups_per_answer=22,content_group_denominator=66,pending_content_groups=44,
    pending_context_groups=8,pending_expectations=52,category_units_in_accepted_scopes=85,
    category_units_are_extra_rule_points=False,full_metrics='not_assessable',semantic_TP_FP_FN='not_assessable',
    whole_card_closed=False,pending_alternative='SEM-009 choice not specified',previous_SEM_001_002_003='pending',
    locator_failure='E916 unchanged and excluded from acceptance',all_glyph_review='unchanged',all_relations='pending',
    no_whole_inventory_or_alias_approval=True,owner_file_or_image_open_verified=False,
    new_extractions=0,new_context_rounds=0,new_corrections=0,situations_evaluated=0,
    preserved_context_totals=dict(extra_pages=1,extra_rules=1,extra_tables=0,context_rounds=1,corrections=0,source_stop_depth=2),
    assessment_exposure='unknown',clean_context='unknown',scope_discovery_outside_allowlist='confirmed_context_session',
    contamination_proven=False,full_isolation_proven=False,
    protected_files_preserved=len(start['protected']),previous_measurement_prefix_preserved=True,
    checks=dict(passed=122,result=ref(checkroot/'result.json'),pytest_log=ref(checkroot/'pytest.log'),
        script_diff_log=ref(checkroot/'diff-check.log'),explicit_diff_result=ref(M/'git-diff-check-result.json'),
        explicit_diff_log=ref(M/'git-diff-check.log'),decision_validation=ref(M/'validation.json'),
        unique_basetemp=checks['basetemp'],local_tmp_temp=True,
        limitations='Structural tests validate recording, not meaning. Three CRLF normalization warnings, no diff errors.'),
    artifacts=load(M/'decision-artifacts.json')['artifacts'],
    next_card='M-POC5A',next_milestone='M-POC5',
    resume='SEM-009 alternative, other pending scope decisions, then separate .3/.4; never repair extraction or expand gold.',
    git_publication='not_requested; no commit or push')
save(M/'completion.json',record)
sessions=P/'measurement/sessions.jsonl';old=sessions.read_bytes();before=start['sessions_before']
assert len(old)==before['bytes'] and hashlib.sha256(old).hexdigest()==before['sha256']
assert old.endswith(b'\n') and record['id'].encode() not in old
entry=dict(record,completion=ref(M/'completion.json'))
with sessions.open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
assert sessions.read_bytes()[:len(old)]==old
save(M/'append-seal.json',dict(previous=before,sessions_after=ref(sessions),added_records=1,original_prefix_preserved=True,
    completion=ref(M/'completion.json')))
print(json.dumps(dict(owner_accepted_groups_per_answer=22,pending_expectations=52,card='partial',
    passed=122,protected_files=len(start['protected']),measurement_appended=1,SEM_009='pending_choice'),ensure_ascii=False))
