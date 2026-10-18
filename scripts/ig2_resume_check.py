"""Audit the selected IG-2 resume inputs against disk and the Git index; launch no model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import uuid

import workflow as w
import orchestrate_ig2 as o
import host_runtime


def inventory(root, q, task_id):
    """Read selected task/dependency evidence metadata, never corpus text or archives."""
    by_id = {t['id']: t for t in q['tasks']}
    task = by_id[task_id]
    selected = [task] + [by_id[id] for id in task['depends']]
    prefixes = tuple(f'private/workflow/runs/{t["id"]}/' for t in selected)
    paths = set(w.BASE_CONTEXT + task['context'] + task.get('tool_context', []))
    paths.update(['scripts/host_runtime.py', 'scripts/ig2_resume_check.py', host_runtime.REQUIREMENTS,
                  'docs/work/IG2-RESTORE.md', 'scripts/orchestrate_ig2.py', 'scripts/workflow.py',
                  'scripts/check.ps1', 'scripts/search_task.py', 'scripts/dependency_context.py',
                  'scripts/context_guard.py', 'scripts/task_access.py', w.QUEUE])
    pins, pending, parsed = {}, set(), set()

    def pin(path, digest, size=None):
        if not path or '\\' in path or ':' in path or Path(path).is_absolute() or '..' in Path(path).parts:
            raise ValueError('Unsafe relative path: ' + path)
        if w.denied(path):
            raise ValueError('Resume reference leaves current task context: ' + path)
        paths.add(path)
        previous = pins.get(path)
        if previous and previous['sha256'] != digest:
            raise ValueError('Conflicting frozen resume references: ' + path)
        value = dict(previous or {'path': path, 'sha256': digest})
        if size is not None:
            if type(size) is not int or size < 0:
                raise ValueError('Invalid resume byte count: ' + path)
            if 'bytes' in value and value['bytes'] != size:
                raise ValueError('Conflicting frozen resume byte counts: ' + path)
            value['bytes'] = size
        pins[path] = value
        if path.startswith(prefixes) and 'manifest' in Path(path).name and path.endswith('.json'):
            pending.add(path)

    def walk(value, location=()):
        if isinstance(value, dict):
            if isinstance(value.get('path'), str) and value.get('sha256'):
                path = value['path']
                # Historical review diagnostics also record host-absolute tools
                # and replay operands. Only relative pins define portable inputs.
                if ':' in path or Path(path).is_absolute():
                    if location[:1] == ('artifacts',):
                        raise ValueError('Delivery artifact needs a repo-relative path: ' + path)
                else:
                    pin(path, value['sha256'], value.get('bytes'))
            if value.get('configuration_evidence') and value.get('configuration_sha256'):
                pin(value['configuration_evidence'], value['configuration_sha256'])
            for key, item in value.items():
                walk(item, location + (key,))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, location + (index,))

    for record in selected:
        for event in record['events']:
            pin(event['evidence'], event['sha256'])
            pending.add(event['evidence'])
    for key in ('repair_authorization', 'context_recovery_authorization', 'continuation_authorization'):
        value = task.get(key, {})
        walk(value)
        pending.update(p['path'] for p in pins.values()
                       if p['path'].startswith(prefixes) and p['path'].endswith('.json'))
    pending.update(p for p in paths if p.startswith(prefixes) and p.endswith('.json'))
    while pending - parsed:
        rel = sorted(pending - parsed)[0]
        parsed.add(rel)
        path = w.safe_path(root, rel)
        if not path.is_file():
            continue
        if rel in pins and w.digest(path) != pins[rel]['sha256']:
            raise ValueError('Frozen resume metadata changed: ' + rel)
        obj = w.read_json(path)
        walk(obj)
        # Only explicit manifest/scope/context pins extend the metadata walk.
        for key in ('scope', 'preserve_manifest', 'blocked_state_manifest', 'immutable_delivery'):
            value = obj.get(key)
            if isinstance(value, dict) and value.get('path', '').startswith(prefixes):
                pending.add(value['path'])
    return task, paths, pins


def audit(root, q, task_id, verify_hashes=True):
    task, paths, pins = inventory(root, q, task_id)
    proc = subprocess.run(['git', '-c', 'core.longpaths=true', 'ls-files', '-z'],
                          cwd=root, capture_output=True, check=True)
    tracked = set(proc.stdout.decode('utf-8').split('\0'))
    missing, changed = [], []
    parents = {}
    for rel in sorted(paths):
        parent = Path(rel).parent.as_posix()
        if parent not in parents:
            parents[parent] = w.safe_path(root, parent)
        path = parents[parent] / Path(rel).name
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
            raise ValueError('Linked resume file: ' + rel)
        if not path.is_file():
            missing.append(rel)
        elif rel in pins:
            pin = pins[rel]
            if (('bytes' in pin and path.stat().st_size != pin['bytes']) or
                    (verify_hashes and w.digest(path) != pin['sha256'])):
                changed.append(rel)
    untracked = sorted(paths - tracked)
    return {'format': 'wgc-ig2-resume-audit-1', 'task': task_id, 'status': task['status'],
            'queue_sha256': w.digest(root / w.QUEUE), 'required_files': len(paths),
            'hashed_pins': len(pins) if verify_hashes else 0,
            'missing_files': missing, 'changed_files': changed, 'not_in_git': untracked,
            'portable_inputs_complete': not (missing or changed or untracked), 'models_launched': 0}


def preflight(root, q, task_id):
    task, role = o.select(q)
    if task is None or task['id'] != task_id or role != 'executor' or task['status'] != 'changes_requested':
        raise ValueError('Queue no longer selects the expected unclaimed IG-2 repair executor')
    host = host_runtime.bound(root)
    if host is None:
        raise ValueError('Preflight needs an explicitly configured host runtime')
    before = w.digest(root / w.QUEUE)
    session = root / 'private/workflow/checks' / ('migration-preflight-' + uuid.uuid4().hex)
    session.mkdir(parents=True, exist_ok=False)
    o.prepare(root, q, task, role, session)
    o.launch_environment(root, task, session, host['tools']['codex']['path'])
    if w.digest(root / w.QUEUE) != before:
        raise ValueError('Preflight changed the queue')
    return {'task': task_id, 'role': role, 'session': session.relative_to(root).as_posix(),
            'queue_unchanged': True, 'models_launched': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task', default='IG-2B08')
    parser.add_argument('--host-runtime')
    parser.add_argument('--preflight', action='store_true')
    args = parser.parse_args()
    if args.host_runtime:
        host_runtime.bind(w.ROOT, args.host_runtime)
    q = w.read_json(w.ROOT / w.QUEUE)
    w.validate(q, w.ROOT)
    report = audit(w.ROOT, q, args.task)
    if report['portable_inputs_complete'] and args.preflight:
        report['preflight'] = preflight(w.ROOT, q, args.task)
    print(json.dumps(report, indent=2))
    return 0 if report['portable_inputs_complete'] else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(2)
