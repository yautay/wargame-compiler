"""Append an honest session measurement and seal this preparation, without owner decisions."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
M = Path(__file__).resolve().parent
OUT = P / 'reviews/semantic-01'

def load(path):
    return json.loads(path.read_bytes())

def ref(path):
    data = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())

def save(path, obj):
    assert not path.exists(), path
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

start = load(M / 'start.json')
for record in start['protected']:
    assert ref(ROOT / record['path']) == record, record['path']

# Check current hash-bearing links in closures, receipts and source-review lineage.
# Historical C:/dev locations and self-reported exposure are not converted into facts.
lineage = []
paths = [P / f'reports/{r}/{name}' for r in ['first-001','context-01'] for name in ['manifest.json','closure.json']]
paths += [P / 'runs/context-01/run.json', P / 'context/pass-01/freeze-v1.json',
    P / 'measurement/M-POC4B-context-01/report-reference-supplement.json',
    P / 'reviews/context-source-01/decision-01.json', P / 'reviews/context-source-01/review-closure-01.json']
for path in paths:
    data = load(path)
    for key,value in data.items():
        if isinstance(value,dict) and {'path','bytes','sha256'} <= value.keys():
            actual = ref(ROOT / value['path'])
            assert all(actual[k] == value[k] for k in ['path','bytes','sha256']), (path,key)
            lineage.append(dict(parent=path.relative_to(ROOT).as_posix(), field=key, reference=actual))
save(M / 'lineage-validation.json', dict(result='passed', checked_references=lineage,
    scope='Current hash-bearing top-level closure/receipt/freeze/reference links; no historical source-path or isolation certification.'))

checks_root = ROOT / 'private/poc/_checks/active-9ea772af22484df09520e5eb42b4e4ec'
check_result = load(checks_root / 'result.json')
assert check_result['tests_exit'] == 0 and check_result['diff_exit'] == 0
assert '120 passed' in (checks_root / 'pytest.log').read_text(encoding='utf-8-sig')
diff = load(M / 'git-diff-check-result.json')
assert diff['exit_code'] == 0
C = load(OUT / 'checklist.json')
assert C['human_decisions'] == [] and C['semantic_acceptance'] == 'not_performed'
end = datetime.now(timezone.utc)
first = datetime.fromisoformat(start['first_recorded_clock_utc'])
record = dict(id='M-POC5A-semantic-01-preparation', card='M-POC5A', part='M-POC5A.1', milestone='M-POC5',
    outcome='partial', status='waiting_review', timezone='Europe/Warsaw', author='Codex',
    first_recorded_clock_utc=start['first_recorded_clock_utc'], completed_at_utc=end.isoformat(),
    recorded_calendar_elapsed_seconds=(end-first).total_seconds(),
    timing_limitation='First clock is after bootstrap; elapsed calendar is not active time or complete session duration.',
    active_user_time='unknown', active_model_time='unknown', active_budget_remaining='unknown',
    time_budget_compliance='unknown', actual_model_selector='unknown', reasoning_selector='unknown', tokens='unknown', price='unknown',
    evaluation=C['evaluation'], responses=C['responses'], source=C['source'], counts=C['counts'],
    preparation_scope='Complete evidence docket plus first three local proposals shown; no completed full semantic review.',
    human_review=dict(status='waiting_review', exact_scope_ids=['SEM-001','SEM-002','SEM-003'],
        owner_decisions=[], semantic_acceptance='not_performed', report_or_image_open_verified=False),
    split_before_assessment=True, remaining_parts=['M-POC5A.2','M-POC5A.3','M-POC5A.4'],
    new_extractions=0, new_context_rounds=0, new_corrections=0, situations_evaluated=0,
    context_totals=C['limits'], operational_limitations=C['limitations'],
    protected_files_preserved=len(start['protected']), previous_measurement_prefix_preserved=True,
    checks=dict(scripts_check=dict(passed=120, result=ref(checks_root / 'result.json'),
        pytest_log=ref(checks_root / 'pytest.log'), diff_log=ref(checks_root / 'diff-check.log'),
        local_tmp_temp=True, unique_previously_nonexistent_basetemp=check_result['basetemp']),
        explicit_git_diff_check=dict(result=ref(M / 'git-diff-check-result.json'),log=ref(M / 'git-diff-check.log'),exit_code=0),
        docket_validation=ref(M / 'docket-validation.json'), lineage_validation=ref(M / 'lineage-validation.json'),
        limitations='Structural checks do not accept meaning. Git emitted CRLF-to-LF normalization warnings for three edited public documents.'),
    artifacts=[ref(f) for f in sorted(OUT.iterdir()) if f.is_file()],
    resume='Await owner decisions for SEM-001/002/003 in focus-01.md, record separately with exact hashes/scopes. Then first pending in parts .2/.3/.4; no M-POC5B in this part.',
    git_publication='not_requested; local uncommitted artifacts',
    next_card='M-POC5A', next_milestone='M-POC5')
save(M / 'completion.json',record)
sessions_path = P / 'measurement/sessions.jsonl'
before = start['sessions_before']
previous = sessions_path.read_bytes()
assert hashlib.sha256(previous[:before['bytes']]).hexdigest() == before['sha256']
assert record['id'].encode() not in previous
assert previous.endswith(b'\n')
entry = dict(record, completion=ref(M / 'completion.json'))
with sessions_path.open('ab') as handle:
    handle.write((json.dumps(entry,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
assert sessions_path.read_bytes()[:len(previous)] == previous
save(M / 'append-seal.json',dict(previous=before, sessions_after=ref(sessions_path),
    added_records=1, original_bytes_preserved=True, completion=ref(M / 'completion.json')))
print(json.dumps(dict(outcome=record['outcome'],status=record['status'],protected_files=len(start['protected']),
    lineage_links=len(lineage),tests_passed=120,owner_decisions=0,measurement_appended=1,
    recorded_calendar_elapsed_seconds=record['recorded_calendar_elapsed_seconds']),ensure_ascii=False))
