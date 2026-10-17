"""Seal preparation and actual check evidence only; perform no workflow transition."""
import hashlib, json, re, subprocess
from datetime import datetime, timezone
from pathlib import Path

R = Path('C:/repo/wargame-compiler')
P = Path(__file__).resolve().parent

def pin(path):
    raw = path.read_bytes()
    return dict(path=path.relative_to(R).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

state = json.loads((P/'preparation.json').read_text(encoding='utf-8'))
checks = json.loads((P/'checks.json').read_text(encoding='utf-8'))
assert all(check['exit_code']==0 for check in checks['checks'])
assert pin(R/'docs/work/queue.json')==state['queue_snapshot']
assert not (R/state['reserved_absent_repair_attempt']).exists()
assert not (P/'preparation-seal.json').exists()
command = [str(R/'.venv/Scripts/python.exe'), '-B', str(P/'verify-frozen-bases.py'), '--report', str(P/'postchecks-frozen-base-verification.json')]
result = subprocess.run(command, cwd=R, capture_output=True)
with (P/'postchecks-frozen-verification.stdout').open('xb') as stream:
    stream.write(result.stdout)
with (P/'postchecks-frozen-verification.stderr').open('xb') as stream:
    stream.write(result.stderr)
assert result.returncode==0
frozen = json.loads((P/'postchecks-frozen-base-verification.json').read_text(encoding='utf-8'))
assert frozen['frozen_unique_refs_verified']==4246 and frozen['queue_equals_preparation_snapshot']
stdout = (P/'repository-check.stdout').read_text(encoding='utf-8')
match = re.search(r'LOG_ROOT=(.+)', stdout)
assert match
check_root = Path(match[1].strip())
check_root.resolve().relative_to((R/'private/workflow/checks').resolve())
check_result = json.loads((check_root/'result.json').read_text(encoding='utf-8-sig'))
assert all(check_result[key]==0 for key in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
pytest_log = (check_root/'pytest.log').read_text(encoding='utf-8-sig')
assert '102 passed' in pytest_log
submitted = sorted(path for path in P.iterdir() if path.is_file())
submitted += [R/'docs/work/repair-context/IG-2B02-R01-R02-20261015T091559Z.json']
submitted += [check_root/name for name in ('plan.log','dry-run.log','pytest.log','diff-check.log','result.json')]
queue = json.loads((R/'docs/work/queue.json').read_text(encoding='utf-8'))
task = next(task for task in queue['tasks'] if task['id']=='IG-2B02')
assert task['status']=='review' and len(task['events'])==3
delivery = json.loads((P/'instruction-delivery.json').read_text(encoding='utf-8'))
for name in ('repair_instruction','coordinator_plan','rereview_template'):
    row = delivery[name]
    assert pin(R/row['path'])==row
seal = dict(task='IG-2B02', role='repair_instruction_preparer', sealed_utc=datetime.now(timezone.utc).isoformat(), actor=state['preparer_actor'], purpose='Complete new local GPT-6.1 Sol/high repair instruction for R01/R02 and fresh independent rereview; preparation only.', original_queue_snapshot=state['queue_snapshot'], queue_unchanged=True, status='review', event_count=3, reserved_repair_attempt_absent=True, frozen_unique_refs_verified_before_and_after=4246, preparation_checks=dict(repository_check_exit=0, workflow_validate_exit=0, git_diff_check_exit=0, full_suite='102 passed', note='Existing Xref/line-ending warnings remain in actual logs; no warnings suppressed. These are preparation checks, not source-content review or repair verification.'), instruction=delivery['repair_instruction'], coordinator_setup_plan=delivery['coordinator_plan'], rereview_template=delivery['rereview_template'], selected_queue_patch=delivery['selected_queue_patch'], artifacts=[pin(path) for path in submitted], self_exclusion_policy='This seal excludes itself. Its actual SHA256 and bytes are reported separately; no sealed instruction is rewritten.', future_queue_and_repair_hashes=None, future_hashes_reason='Coordinator setup and repair have not run. Actual future packet/event/output pins must be filled and verified at their stated gates.', session_created=False, repair_executed=False, queue_transition_performed=False, acceptance_granted=False, token_usage=None, token_usage_reason='Exact usage unavailable to this preparation.', cost=None, cost_reason='Exact cost unavailable.', operator_time=None, operator_time_reason='Not measured.', next_operation='Operator may separately authorize coordinator setup; then a new actual-configuration-confirmed repair executor. No launch or acceptance is performed by this preparation.')
with (P/'preparation-seal.json').open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(seal, stream, indent=2)
    stream.write('\n')
print(json.dumps(dict(seal=pin(P/'preparation-seal.json'), instruction=delivery['repair_instruction'], full_suite='102 passed', frozen_refs=4246, queue_unchanged=True, repair_attempt_absent=True), indent=2))
