"""Capture continuation preflight without claiming implementation or changing queue."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
started = datetime.now(timezone.utc)
tick = time.perf_counter()

def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def load(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def save(name, value):
    with (OUT / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')

checkpoint_dir = 'private/workflow/runs/IG-1D/operator-checkpoint-20261013T132827Z'
delivery_path = 'private/workflow/runs/IG-1D/repair-01-20261013/delivery.json'
review_dir = 'private/workflow/runs/IG-1D/rereview-20261013T131151Z'
manifest = load(checkpoint_dir + '/verified-artifact-manifest.json')
verified = []
for artifact in manifest:
    path = artifact.get('verified_path', artifact['path'])
    actual = digest(path)
    assert actual == artifact['sha256'], path
    verified.append({**artifact, 'actual_sha256': actual})
delivery = load(delivery_path)
for artifact in delivery['artifacts']:
    assert digest(artifact['path']) == artifact['sha256'], artifact['path']
queue = load('docs/work/queue.json')
assert digest('docs/work/queue.json') == '07cb9707259e91d1f779360ba4eb8606a3d2ae51502aaba53c4961a7e264e1e3'
assert digest(delivery_path) == '3ebef08719717c41043cb4df8bb98874d214e38d0e8fdbf21de6e35a9adfaa73'
statuses = {t['id']: t['status'] for t in queue['tasks'] if t['id'].startswith('IG-1')}
assert statuses == {'IG-1A': 'done', 'IG-1B': 'done', 'IG-1C': 'done', 'IG-1D': 'review', 'IG-1E': 'planned'}
checks_path = 'private/workflow/checks/active-fc51ad8a1aca40028cf6ef33c5bd83a5/result.json'
checks = load(checks_path)
assert all(checks[k] == 0 for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'))
diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
assert diff.returncode == 0, diff.stderr
save('verified-artifacts.json', verified)
save('proposed-repair-scope.json', {
    'task': 'IG-1D', 'finding': 'IG1D-R04', 'proposed_iteration': 2,
    'maximum_iterations': 2, 'claimed': False, 'implementation_started': False,
    'basis': review_dir + '/dispositions.json',
    'changed_hypothesis': 'The repair-1 filter hides persisted receipt children of another logical kind or scope, then wrongly treats the empty filtered set as an initial allocation. Check the named persisted output contract before replacement allocation.',
    'proposed_product_paths': ['src/wgc/wgu_adapter/identity.py', 'tests/wgu_adapter/test_lineage_contract_repairs.py'],
    'required_boundary': 'Reject incompatible reuse of a named receipt for a changed logical kind, resolved scope or persistent child key; preserve caller registry immutability. A deliberately different output contract requires a new decision identifier.',
    'preserve': ['Unique merge-child text correction and rename', 'Original 15 independent assertions', 'All repair-1 risk and history assertions', 'Historical parent and child revisions', 'Multi-child ambiguity and persistent keyed children', 'All frozen prior artifacts'],
    'verification_after_claim': ['Strict changed-child-kind probe unchanged', 'Scope and persistent-child-key incompatibility; new named decision positive control', 'Full adapter/export and original/risk/history suites with fresh short basetemp and no cacheprovider', 'Independent complete private file/record/field/binding accounting and two canonical transforms/publications', 'scripts/check.ps1 -Task IG-1D and git diff --check', 'Independent re-review in the existing authorized reviewer chat'],
    'prerequisites': ['Fresh actual executor Sol/high configuration evidence', 'Final frozen repair-1 independent review and artifact manifest', 'Workflow changes_requested transition, new bounded claim and preserved current product versions']
})
evidence_paths = [delivery_path, review_dir + '/dispositions.json', review_dir + '/risk-check.json', review_dir + '/accounting-check.json', checks_path]
save('checkpoint.json', {
    'format': 'wgc-continuation-preflight-1', 'task': 'IG-1D',
    'actor': 'ig1-continuation-executor-20261013',
    'model': None, 'reasoning': None,
    'requested_model': 'gpt-6.1-sol', 'requested_reasoning': 'high',
    'configuration_evidence': 'Actual model/reasoning is not exposed by available session tools; fresh direct operator confirmation was requested and has not been received at capture time. Prior-session confirmation is not reused.',
    'queue': {'path': 'docs/work/queue.json', 'sha256': digest('docs/work/queue.json'), 'statuses': statuses},
    'preservation': {'entries_verified': len(verified), 'delivery_artifacts_verified': len(delivery['artifacts']), 'mismatches': [], 'verified_version_mapping_used': True},
    'reviewer': {'thread_id': '01a13421-44a0-71a3-9484-bf796c2922fc', 'host_id': 'local', 'title': 'Independent technical review IG-1C', 'live_status': None, 'final_review_exists': (ROOT / review_dir / 'review.json').exists(), 'tool_failures': ['wait_threads: durable host unavailable', 'read_thread: durable host unavailable', 'wait_threads without host: durable host unavailable', 'send_message_to_thread: no rollout found'], 'message_delivered': False, 'local_assessment': 'R01-R03 closed; R04 remaining changed-child-contract boundary after iteration 1. dispositions.json is not substituted for a final frozen review.json.'},
    'checks': [{'command': 'scripts/workflow.py validate', 'exit_code': 0}, {'command': 'pwsh -NoProfile -File scripts/check.ps1 -Task IG-1D', 'exit_code': 0, 'result': checks_path, 'project_tests_passed': 102}, {'command': 'git diff --check', 'exit_code': diff.returncode}],
    'artifacts': [{'path': p, 'sha256': digest(p)} for p in evidence_paths],
    'measurements': {'started_utc': started.isoformat(), 'ended_utc': datetime.now(timezone.utc).isoformat(), 'capture_wall_seconds': time.perf_counter() - tick, 'session_start_utc': None, 'session_wall_seconds': None, 'input_tokens': None, 'output_tokens': None, 'cost': None, 'operator_time_seconds': None, 'unknown_reason': 'Capture interval measured only; full session timing and usage not exposed.'},
    'product_changed': False, 'queue_changed': False, 'new_repair_claimed': False,
    'IG_1E_started': False, 'technical_acceptance_granted': False,
    'semantic_acceptance_granted': False,
    'next_operation': 'Obtain fresh actual executor configuration and restore/finalize the existing reviewer result, then claim the bounded second repair of R04. IG-1E depends on IG-1D acceptance/done.'
})
print(json.dumps({'output': str(OUT), 'verified_entries': len(verified), 'delivery_artifacts': len(delivery['artifacts']), 'project_tests_passed': 102, 'product_changed': False, 'queue_changed': False}))
