import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PREP = Path('private/workflow/runs/IG-2B08/prepare-F03-F05-F09-1e0c3c94')
DISPATCH = Path('private/workflow/orchestrator/20261017T151724Z-86fb83c5/003-IG-2B08-coordinator-1e0c3c94')

def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def pin(p):
    p = Path(p)
    return {'path': p.as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}

def fresh_write(p, obj):
    assert not p.exists()
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

log = PREP / 'full-check-approved.log'
text = log.read_text(encoding='utf-8-sig', errors='replace')
root = Path(re.search(r'LOG_ROOT=(.+)', text).group(1).strip())
check_result = read(root / 'result.json')
assert all(check_result[k] == 0 for k in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'])
with (PREP / 'diff-check.log').open('xb') as f:
    diff = subprocess.run(['git', 'diff', '--check'], stdout=f, stderr=subprocess.STDOUT)
assert diff.returncode == 0

auth_path = PREP / 'authorization.json'
auth = read(auth_path)
identity = {k: auth[k] for k in ['role', 'actor', 'model', 'reasoning', 'configuration_evidence', 'configuration_sha256']}
assert sha(identity['configuration_evidence']) == identity['configuration_sha256']
scope = read(PREP / 'repair-scope.json')
snapshot = read(DISPATCH / 'task.json')
assert scope['acceptance'] == snapshot['acceptance'] and scope['tests'] == snapshot['tests']
assert not Path(scope['attempt']).exists()
manifest = read(scope['preserve_manifest']['path'])
assert sha(scope['preserve_manifest']['path']) == scope['preserve_manifest']['sha256']
for p in manifest['artifacts']:
    assert sha(p['path']) == p['sha256'], 'Immutable preservation mismatch'
queue_path = Path('docs/work/queue.json')
queue = read(queue_path)
task = next(t for t in queue['tasks'] if t['id'] == 'IG-2B08')
refs = read(DISPATCH / 'references.json')
assert task['status'] == 'changes_requested'
assert task['events'][-1]['sha256'] == refs['findings']['sha256']
assert task['repair_authorization']['scope']['sha256'] == sha(PREP / 'repair-scope.json')
assert task['acceptance'] == snapshot['acceptance'] and task['tests'] == snapshot['tests']
events_before = json.dumps(task['events'], sort_keys=True, ensure_ascii=False)
checks = read(PREP / 'render-validation.json')['checks'] + [
    {'command': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-2B08'], 'exit_code': 0,
     'execution_permissions': 'require_escalated', 'log': pin(log),
     'result': pin(root.relative_to(Path.cwd()) / 'result.json')},
    {'command': ['git', 'diff', '--check'], 'exit_code': 0, 'log': pin(PREP / 'diff-check.log')}]
report = {
    **identity, 'task': 'IG-2B08', 'utc': datetime.now(timezone.utc).isoformat(),
    'summary': 'Current bounded repair contract rendered and validated; unchanged full repository checks passed with approved execution after restricted-token temporary-directory failure.',
    'checks': checks, 'check_exit_fields': {k: check_result[k] for k in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit']},
    'execution_attempts': [
        {'command': ['powershell', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-2B08'], 'exit_code': 1,
         'reason': 'Windows PowerShell refused script loading under its execution policy; tests did not start.', 'log': pin(PREP / 'full-check.log')},
        {'command': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-2B08'], 'exit_code': 1,
         'reason': 'Restricted-token pytest temporary-directory access failure; planning, dry-run and diff checks passed.', 'log': pin(PREP / 'full-check-pwsh.log')},
        {'command': ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', 'IG-2B08'], 'exit_code': 0,
         'execution_permissions': 'require_escalated',
         'authorization_basis': 'Current operator explicitly authorized approved exact-command execution for restricted-token test access failures.', 'log': pin(log)}],
    'preservation_status': 'verified', 'preserved_artifact_count': len(manifest['artifacts']),
    'acceptance_and_tests_unchanged': True, 'status_unchanged': 'changes_requested',
    'attempt_absent': True, 'semantic_acceptance_granted': False, 'executable_readiness': False}
report_path = PREP / 'validation-report.json'
fresh_write(report_path, report)
auth['checks'] = checks
auth['artifacts'] += [pin(report_path), pin(PREP / 'prepare.py'), pin(PREP / 'finalize.py'), pin(PREP / 'preserve-manifest.json')]
auth['validation_summary'] = {'all_required_preparation_checks_passed': True,
                              'preserved_artifacts_reverified': len(manifest['artifacts']),
                              'acceptance_and_tests_unchanged': True, 'attempt_absent': True}
# This preparation evidence is finalized before returning it to the supervisor.
# No queue event references these draft bytes; only the new authorization pin changes.
assert task['repair_authorization']['evidence']['sha256'] == sha(auth_path)
auth_path.write_text(json.dumps(auth, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
task['repair_authorization']['evidence'] = pin(auth_path)
assert json.dumps(task['events'], sort_keys=True, ensure_ascii=False) == events_before
queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({'task': 'IG-2B08', 'checks_passed': True, 'preserved_artifacts': len(manifest['artifacts']),
                  'status': task['status'], 'events_unchanged': True, 'attempt_absent': True,
                  'authorization': pin(auth_path)}))
