"""Task-scoped public reads, Git status and privately logged source validation."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
import uuid

import workflow as w
import search_task as search
import context_guard as guard

BOOTSTRAP_VIEWS = {'docs/STATUS.md', 'docs/HANDOFF.md'}


def manifest(root, rel, sha256, task):
    if not rel or not sha256 or not task:
        raise ValueError('Pinned task access manifest required; no global fallback')
    p = w.safe_path(root, rel)
    if w.digest(p) != sha256:
        raise ValueError('Task access manifest changed')
    body = w.read_json(p)
    if body.get('format') != 'wgc-task-access-1' or body.get('task') != task:
        raise ValueError('Task access manifest belongs to another task')
    return body


@guard.protect('task_access.read')
def read_public(root, rel, sha256, task, file, start=1, lines=80):
    if start < 1 or not 1 <= lines <= 150:
        raise ValueError('Text read window exceeds task limits')
    body = manifest(root, rel, sha256, task)
    snapshot = body.get('bootstrap_reads', {}).get(file)
    if snapshot is not None:
        expected = (w.safe_path(root, rel).parent / 'bootstrap' / Path(file).name).relative_to(root).as_posix()
        if file not in BOOTSTRAP_VIEWS or snapshot.get('path') != expected:
            raise ValueError('Bootstrap snapshot is not an authorized session view')
        source = w.safe_path(root, snapshot['path'])
        if not source.is_file() or w.digest(source) != snapshot.get('sha256'):
            raise ValueError('Bootstrap snapshot changed or is missing')
    else:
        ref = body['search_manifest']
        search.load_scope(root, ref['path'], ref['sha256'], task, [file])
        source = w.safe_path(root, file)
    data = source.read_text(encoding='utf-8-sig').splitlines()
    result = {'task': task, 'path': file, 'start_line': start, 'lines': [], 'truncated': False}
    if snapshot is not None:
        result.update(basis='dispatch_snapshot', snapshot=snapshot, status_authority=False)
    for line in data[start - 1:start - 1 + lines]:
        result['lines'].append(line)
        if len(guard.json_text(result).encode('ascii')) + 1 > 12000:
            result['lines'].pop(); result['truncated'] = True; break
    result['truncated'] |= start - 1 + len(result['lines']) < len(data)
    return result


@guard.protect('task_access.git_status')
def git_status(root, rel, sha256, task, max_items=40):
    if not 1 <= max_items <= 100:
        raise ValueError('Status item limit exceeded')
    body = manifest(root, rel, sha256, task)
    paths = body.get('git_paths', [])
    if not paths:
        raise ValueError('Empty task Git scope; never fall back to global status')
    for p in paths:
        w.safe_path(root, p)
        if w.denied(p):
            raise ValueError('Forbidden task Git path')
    result = subprocess.run(['git', '--no-optional-locks', '--literal-pathspecs',
        '-c', 'core.fsmonitor=false', '-c', 'status.relativePaths=false', 'status',
        '--porcelain=v1', '-z', '--no-renames', '--untracked-files=all', '--', *paths],
        cwd=root, capture_output=True, timeout=20)
    if result.returncode:
        raise ValueError('Task-scoped Git status failed; no raw-command fallback')
    entries = []
    for record in result.stdout.split(b'\0'):
        if not record: continue
        text = record.decode('utf-8')
        path = text[3:].replace('\\', '/')
        if not any(path == p or (p.endswith('/') and path.startswith(p)) for p in paths):
            raise ValueError('Git returned an unlisted path; no output released')
        entries.append({'status': text[:2], 'path': path})
    output = {'task': task, 'entries': [], 'truncated': False, 'max_items': max_items}
    for entry in entries:
        if len(output['entries']) >= max_items:
            output['truncated'] = True; break
        output['entries'].append(entry)
        if len(guard.json_text(output).encode('ascii')) + 1 > 12000:
            output['entries'].pop(); output['truncated'] = True; break
    return output


@guard.protect('task_access.validate_source')
def validate_source(root, rel, sha256, task, file):
    """Run the unchanged validator; release no stdout/stderr content, even on failure."""
    body = manifest(root, rel, sha256, task)
    scope = body.get('source_validation', {})
    matches = [p for p in scope.get('inputs', []) if p.get('path') == file]
    if len(matches) != 1:
        raise ValueError('Inventory is not in the pinned validation scope')
    source = w.safe_path(root, file)
    mode = scope.get('mode', 'frozen')
    owner_queue_sha256 = None
    if mode == 'owned_attempt':
        # Generated executor outputs cannot have dispatch-time hashes. Bind them
        # instead to the exact three paths, current queue ownership and observed
        # session claim; snapshot the bytes for each individual validation call.
        session = w.safe_path(root, rel).parent
        owner_queue_sha256 = w.digest(root / w.QUEUE)
        q = w.read_json(root / w.QUEUE)
        current = next(t for t in q['tasks'] if t['id'] == task)
        attempt = scope['attempt']
        expected = [attempt + name + '/inventory.json'
                    for name in ('final-verified', 'replay-1', 'replay-2')]
        if (current['status'] != 'in_progress' or attempt not in current['write_scope'] or
                current.get('inventory_contract', {}).get('attempt_root', '').rstrip('/') + '/' != attempt or
                [p['path'] for p in scope['inputs']] != expected):
            raise ValueError('Executor no longer owns the exact validation attempt')
        event = next(e for e in reversed(current['events']) if e['to'] == 'in_progress')
        claim_path = w.safe_path(root, event['evidence'])
        if claim_path.parent != w.safe_path(root, attempt) or w.digest(claim_path) != event['sha256']:
            raise ValueError('Executor claim changed')
        claim = w.read_json(claim_path)
        runtime = session / 'runtime-configuration.json'
        observed = w.read_json(runtime)
        if (claim.get('configuration_evidence') != runtime.relative_to(root).as_posix() or
                claim.get('configuration_sha256') != w.digest(runtime) or
                claim.get('actor') != f'ig2:{session.name}:executor' or
                claim.get('model') != 'gpt-6.1-sol' or claim.get('reasoning') != 'high' or
                observed.get('status') != 'confirmed' or observed.get('model') != 'gpt-6.1-sol' or
                observed.get('reasoning') != 'high' or not observed.get('session_id')):
            raise ValueError('Validation claim is not bound to this observed executor session')
        input_pin = {'path': file, 'sha256': w.digest(source), 'bytes': source.stat().st_size}
    elif mode == 'frozen':
        input_pin = matches[0]
        if w.digest(source) != input_pin['sha256']:
            raise ValueError('Frozen validation input changed')
    else:
        raise ValueError('Unknown validation ownership mode')
    log_rel = scope.get('log_root', '')
    if not log_rel.startswith(f'private/workflow/runs/{task}/review-validation-') or not log_rel.endswith('/'):
        raise ValueError('Validation logs require the exact task-owned review scope')
    log_root = w.safe_path(root, log_rel)
    if source.is_relative_to(log_root):
        raise ValueError('Validation log scope contains frozen input')
    target = log_root / uuid.uuid4().hex
    target.mkdir(parents=True, exist_ok=False)
    stdout, stderr = target / 'stdout.log', target / 'stderr.log'
    command = [sys.executable, '-m', 'wgc.sources', 'validate', file]
    with stdout.open('xb') as out, stderr.open('xb') as err:
        try:
            result = subprocess.run(command, cwd=root, stdin=subprocess.DEVNULL,
                                    stdout=out, stderr=err, timeout=900)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 124
    if w.digest(source) != input_pin['sha256']:
        raise ValueError('Frozen validation input changed during validation')
    if owner_queue_sha256 is not None and w.digest(root / w.QUEUE) != owner_queue_sha256:
        raise ValueError('Executor ownership changed during validation')
    def pin(path):
        return {'path': path.relative_to(root).as_posix(), 'sha256': w.digest(path),
                'bytes': path.stat().st_size}
    summary = {'task': task, 'inventory': input_pin, 'command': command, 'exit_code': code,
               'stdout': pin(stdout), 'stderr': pin(stderr),
               'output_policy': 'Private logs only; no raw output or tail is released.'}
    with (target / 'result.json').open('x', encoding='utf-8') as stream:
        stream.write(guard.json_text(summary) + '\n')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['read', 'git-status', 'validate-source'])
    parser.add_argument('--task', default=os.environ.get('WGC_TASK_ID'))
    parser.add_argument('--manifest', default=os.environ.get('WGC_TASK_ACCESS_MANIFEST'))
    parser.add_argument('--sha256', default=os.environ.get('WGC_TASK_ACCESS_SHA256'))
    parser.add_argument('--file')
    parser.add_argument('--start-line', type=int, default=1)
    parser.add_argument('--lines', type=int, default=80)
    parser.add_argument('--max-items', type=int, default=40)
    args = parser.parse_args()
    for key, value in [('WGC_TASK_ID', args.task), ('WGC_TASK_ACCESS_MANIFEST', args.manifest),
                       ('WGC_TASK_ACCESS_SHA256', args.sha256)]:
        if os.environ.get(key) and os.environ[key] != value:
            raise ValueError('Task access override differs from the session binding')
    if args.operation == 'read':
        if not args.file: raise ValueError('An exact packet file is required')
        output = read_public(w.ROOT, args.manifest, args.sha256, args.task, args.file, args.start_line, args.lines)
    elif args.operation == 'git-status':
        if args.file: raise ValueError('Git scope cannot be overridden by a file argument')
        output = git_status(w.ROOT, args.manifest, args.sha256, args.task, args.max_items)
    else:
        if not args.file: raise ValueError('An exact frozen inventory is required')
        output = validate_source(w.ROOT, args.manifest, args.sha256, args.task, args.file)
    print(guard.json_text(output))
    return output['exit_code'] if args.operation == 'validate-source' else 0


if __name__ == '__main__':
    raise SystemExit(guard.cli(w.ROOT, 'task_access', main))
