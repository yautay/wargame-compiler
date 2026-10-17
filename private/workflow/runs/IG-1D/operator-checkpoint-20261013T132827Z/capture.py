"""Capture an append-only coordinator checkpoint without mutating product or queue."""
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
CHECK = ROOT / 'private/workflow/checks/active-02f4922eacab4dfea3acf1c850564f5b'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(name, value):
    with (OUT / name).open('x', encoding='utf-8', newline='\n') as stream:
        if isinstance(value, str):
            stream.write(value)
        else:
            json.dump(value, stream, ensure_ascii=True, indent=2)
            stream.write('\n')


started = datetime.now(timezone.utc).isoformat()
clock = time.perf_counter()
delivery = ROOT / 'private/workflow/runs/IG-1D/repair-01-20261013/delivery.json'
assert digest(delivery) == '3ebef08719717c41043cb4df8bb98874d214e38d0e8fdbf21de6e35a9adfaa73'
verified = []
for entry in load(delivery)['artifacts']:
    actual = digest(ROOT / entry['path'])
    assert actual == entry['sha256'], entry['path']
    verified.append(dict(entry, verified_path=entry['path'], group='current_delivery'))
preservation = load(ROOT / 'private/workflow/runs/IG-1D/repair-01-20261013/preservation.json')
for group, entries in preservation.items():
    if not isinstance(entries, list):
        continue
    for entry in entries:
        path = entry.get('verified_path', entry['path'])
        assert digest(ROOT / path) == entry['sha256'], path
        verified.append(dict(entry, verified_path=path, group=group))
write('verified-artifact-manifest.json', verified)
queue = ROOT / 'docs/work/queue.json'
statuses = {task['id']: task['status'] for task in load(queue)['tasks'] if task['id'].startswith('IG-1')}
assert statuses['IG-1C'] == 'done' and statuses['IG-1D'] == 'review' and statuses['IG-1E'] == 'planned', statuses
checks = []
for name, argv in [('queue-validation', [str(ROOT / '.venv/Scripts/python.exe'), 'scripts/workflow.py', 'validate']),
                   ('diff-check', ['git', 'diff', '--check']),
                   ('worktree-status', ['git', 'status', '--short']),
                   ('worktree-stat', ['git', 'diff', '--stat'])]:
    result = subprocess.run(argv, cwd=ROOT, capture_output=True)
    write(name + '.log', result.stdout.decode('utf-8', errors='replace') + result.stderr.decode('utf-8', errors='replace'))
    assert result.returncode == 0, name
    checks.append({'command': argv, 'exit_code': result.returncode, 'log': name + '.log'})
check_result = load(CHECK / 'result.json')
assert all(check_result[key] == 0 for key in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'])
checks.append({'command': 'scripts/check.ps1 -Task IG-1D', 'exit_code': 0,
               'result': CHECK.relative_to(ROOT).as_posix() + '/result.json', 'details': check_result})
write('checkpoint.json', {
    'format': 'wgc-operator-checkpoint-1', 'task': 'IG-1D',
    'actor': 'ig1-stage-executor-20261013', 'reason': 'Operator requested saved checkpoint and continuation prompt.',
    'started_utc': started, 'ended_utc': datetime.now(timezone.utc).isoformat(),
    'capture_wall_seconds': round(time.perf_counter() - clock, 3),
    'model': 'gpt-6.1-sol', 'reasoning': 'high',
    'configuration_evidence': {'source': 'Direct operator confirmation in this ongoing session',
                               'verbatim': 'sol 6.1 high', 'scope': 'Previous executor session only; new session needs fresh evidence.'},
    'tokens': None, 'cost': None, 'operator_time': None,
    'queue': {'path': 'docs/work/queue.json', 'sha256': digest(queue), 'statuses': statuses},
    'delivery': {'path': delivery.relative_to(ROOT).as_posix(), 'sha256': digest(delivery), 'artifact_count': len(load(delivery)['artifacts'])},
    'verified_manifest': {'path': 'verified-artifact-manifest.json', 'sha256': digest(OUT / 'verified-artifact-manifest.json'), 'entries': len(verified)},
    'checks': checks,
    'reviewer': {'thread_id': '01a13421-44a0-71a3-9484-bf796c2922fc', 'host_id': 'local',
                'title': 'Independent technical review IG-1C', 'observed_utc': '2026-10-13T13:28:27Z',
                'observed_status': 'active', 'turn_status': 'inProgress',
                'cursor': '57e8f390-5c50-4865-9543-3ce1c2b62dba:92',
                'note': 'May finish after this checkpoint. Fetch fresh status before dependent work.'},
    'repair_budget': {'IG1D-R01': {'used': 1, 'maximum': 2}, 'IG1D-R02': {'used': 1, 'maximum': 2},
                      'IG1D-R03': {'used': 1, 'maximum': 2}, 'IG1D-R04': {'used': 1, 'maximum': 2}},
    'completed': ['IG-1A/IG-1B/IG-1C done', 'IG-1D repair 1 frozen', '108 public/reviewer controls passed',
                  '102 project tests passed', 'Full independent accounting and canonical repeatability passed'],
    'pending': ['IG-1D independent re-review and technical acceptance/completion', 'Entire IG-1E task and final stage handoff'],
    'next_operation': 'Confirm new executor actual configuration; inspect existing reviewer fresh result and current queue/hashes before edits.',
    'queue_changed_by_checkpoint': False, 'commit_created': False,
    'product_changed_by_checkpoint': False, 'new_task_started': False,
    'continuation_prompt': 'CONTINUE-PROMPT.txt', 'handoff': 'handoff.md'
})
write('checkpoint-files.json', [{'path': path.name, 'sha256': digest(path)} for path in sorted(OUT.iterdir()) if path.is_file()])
print(json.dumps({'checkpoint': str(OUT / 'checkpoint.json'), 'verified_entries': len(verified), 'statuses': statuses, 'checks': 'pass'}))
