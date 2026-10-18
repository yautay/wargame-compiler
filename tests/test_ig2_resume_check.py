"""A clone must contain the exact reports referenced by its repair checkpoint."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
try:
    import ig2_resume_check as c
finally:
    sys.path.pop(0)


@pytest.fixture
def checkpoint(tmp_path, monkeypatch):
    def pin(rel, value):
        path = tmp_path / rel; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding='utf-8')
        return {'path': rel, 'sha256': c.w.digest(path), 'bytes': path.stat().st_size}
    report = pin('private/workflow/checks/original/pytest.log', {'opaque': 'original captured output'})
    manifest = pin('private/workflow/runs/IG-2B08/preparation/preserve-manifest.json', {'artifacts': [report]})
    scope = pin('private/workflow/runs/IG-2B08/preparation/scope.json', {'preserve_manifest': manifest})
    delivery = pin('private/workflow/runs/IG-2B08/attempt/delivery.json', {'artifacts': [report]})
    task = {'id': 'IG-2B08', 'status': 'changes_requested', 'depends': [], 'context': [scope['path']],
            'events': [{'evidence': delivery['path'], 'sha256': delivery['sha256']}],
            'repair_authorization': {'scope': scope}}
    q = {'tasks': [task]}
    pin(c.w.QUEUE, q)
    _, paths, _ = c.inventory(tmp_path, q, task['id'])
    for rel in paths:
        path = tmp_path / rel
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text('Synthetic public file\n')
    tracked = set(paths)
    def git(*args, **kwargs):
        return subprocess.CompletedProcess([], 0, '\0'.join(sorted(tracked)).encode() + b'\0', b'')
    monkeypatch.setattr(c.subprocess, 'run', git)
    return tmp_path, q, report, tracked


def test_pinned_ignored_report_is_required_even_when_not_under_task_output(checkpoint):
    root, q, report, tracked = checkpoint
    tracked.remove(report['path'])
    result = c.audit(root, q, 'IG-2B08')
    assert not result['portable_inputs_complete']
    assert result['not_in_git'] == [report['path']]
    assert result['missing_files'] == []
    tracked.add(report['path'])
    assert c.audit(root, q, 'IG-2B08')['portable_inputs_complete']


@pytest.mark.parametrize('change', ['missing', 'recreated'])
def test_rerunning_or_losing_a_frozen_report_cannot_pass_resume_audit(checkpoint, change):
    root, q, report, tracked = checkpoint
    path = root / report['path']
    if change == 'missing':
        path.unlink()
    else:
        path.write_text('New passing output cannot replace historical bytes')
    result = c.audit(root, q, 'IG-2B08')
    assert not result['portable_inputs_complete']
    assert result['missing_files' if change == 'missing' else 'changed_files'] == [report['path']]


def test_audit_refuses_a_frozen_manifest_that_escapes_checkout(checkpoint):
    root, q, report, tracked = checkpoint
    rel = q['tasks'][0]['context'][0]
    scope = c.w.read_json(root / rel)
    manifest = root / scope['preserve_manifest']['path']
    manifest.write_text(json.dumps({'artifacts': [{'path': '../outside.log', 'sha256': 'invalid'}]}))
    scope['preserve_manifest']['sha256'] = c.w.digest(manifest)
    (root / rel).write_text(json.dumps(scope))
    q['tasks'][0]['repair_authorization']['scope']['sha256'] = c.w.digest(root / rel)
    with pytest.raises(ValueError, match='Unsafe relative path'):
        c.inventory(root, q, 'IG-2B08')
