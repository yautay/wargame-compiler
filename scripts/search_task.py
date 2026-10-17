"""Search only hash-pinned, stable public text from one task packet; never scan a tree."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import workflow as w
import context_guard as guard

FORMAT = 'wgc-task-search-1'
TEXT_SUFFIXES = {'.md', '.json', '.py', '.ps1', '.toml', '.txt', '.yaml', '.yml'}
VOLATILE = {'docs/work/queue.json', 'docs/work/context-policy.json',
            'docs/status.md', 'docs/handoff.md', 'docs/roadmap.md'}


def ripgrep_binding(cli=None):
    """Resolve once at dispatch; helpers verify the exact executable without PATH."""
    bound = os.environ.get('WGC_RIPGREP_PATH')
    expected = os.environ.get('WGC_RIPGREP_SHA256')
    if bound or expected:
        path = Path(bound or '')
        if not bound or not expected or not path.is_absolute() or not path.is_file():
            raise ValueError('Pinned ripgrep executable is missing or its binding is incomplete')
        if w.digest(path) != expected:
            raise ValueError('Pinned ripgrep executable changed; no PATH fallback')
        return {'path': str(path.resolve()), 'sha256': expected}
    candidates = []
    if cli and Path(cli).is_absolute():
        candidates.append(Path(cli).with_name('rg.exe' if os.name == 'nt' else 'rg'))
    found = shutil.which('rg')
    if found:
        candidates.append(Path(found))
    for path in candidates:
        if path.is_file():
            path = path.resolve()
            return {'path': str(path), 'sha256': w.digest(path)}
    raise ValueError('Ripgrep unavailable; supply WGC_RIPGREP_PATH and WGC_RIPGREP_SHA256 before dispatch')


def searchable(rel):
    lower = rel.lower()
    return (not lower.startswith('private/') and not w.denied(rel) and
            lower not in VOLATILE and not lower.startswith('docs/work/tasks/') and
            Path(rel).suffix.lower() in TEXT_SUFFIXES)


def relative_manifest(root, value):
    path = Path(value)
    rel = path.relative_to(root).as_posix() if path.is_absolute() else value
    return w.safe_path(root, rel)


@guard.protect('task_search.scope')
def load_scope(root, manifest, expected_sha256, task, files=None):
    if not manifest or not expected_sha256 or not task:
        raise ValueError('Task, manifest and expected manifest SHA256 are mandatory; no global fallback')
    path = relative_manifest(root, manifest)
    if w.digest(path) != expected_sha256:
        raise ValueError('Task search manifest changed')
    body = w.read_json(path)
    if body.get('format') != FORMAT or body.get('task') != task:
        raise ValueError('Wrong task search manifest format or task identity')
    pins = body.get('files', [])
    if not pins or len({p['path'] for p in pins}) != len(pins):
        raise ValueError('Empty or duplicate task search paths')
    by_path = {p['path']: p for p in pins}
    selected = list(dict.fromkeys(files)) if files else list(by_path)
    for rel in selected:
        if rel not in by_path:
            raise ValueError('Requested file is not in the task search manifest')
        p = w.safe_path(root, rel)
        if not searchable(rel) or not w.permitted(root, rel):
            raise ValueError('Private, volatile, binary or forbidden context cannot be searched')
        if not p.is_file() or w.digest(p) != by_path[rel]['sha256']:
            raise ValueError(f'Search input changed or is missing: {rel}')
    return selected


@guard.protect('task_search')
def search(root, manifest, sha256, task, pattern, files=None, max_matches=40, max_bytes=12000):
    if not 1 <= max_matches <= 100 or not 512 <= max_bytes <= 32000 or len(pattern) > 1024:
        raise ValueError('Search limits exceeded')
    selected = load_scope(root, manifest, sha256, task, files)
    # Exact file operands and -- prevent regex/option injection or implicit traversal.
    executable = ripgrep_binding()['path']
    result = subprocess.run([executable, '--no-config', '--json', '--max-count', str(max_matches + 1), '--', pattern, *selected],
                            cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace',
                            timeout=15)
    if result.returncode not in {0, 1}:
        raise ValueError('Scoped ripgrep failed: ' + result.stderr[:800])
    output = {'format': 'wgc-task-search-result-1', 'task': task, 'matches': [],
              'truncated': False, 'max_matches': max_matches, 'max_output_bytes': max_bytes}
    for line in result.stdout.splitlines():
        event = json.loads(line)
        if event.get('type') != 'match':
            continue
        data = event['data']
        rel = data['path'].get('text', '').replace('\\', '/')
        if rel not in selected:
            raise ValueError('Ripgrep returned an unlisted path; no output released')
        raw = data['lines'].get('text', '').rstrip('\r\n').encode('utf-8')
        start = max(0, (data.get('submatches') or [{}])[0].get('start', 0) - 120) if len(raw) > 800 else 0
        snippet = raw[start:start + 800].decode('utf-8', errors='replace')
        match = {'path': rel, 'line': data['line_number'], 'text': snippet,
                 'line_truncated': start > 0 or len(raw) > 800}
        if len(output['matches']) >= max_matches:
            output['truncated'] = True
            break
        output['matches'].append(match)
        if len(guard.json_text(output).encode('ascii')) > max_bytes - 1:
            output['matches'].pop()
            output['truncated'] = True
            break
        if match['line_truncated']:
            output['truncated'] = True
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', default=os.environ.get('WGC_TASK_SEARCH_MANIFEST'))
    parser.add_argument('--sha256', default=os.environ.get('WGC_TASK_SEARCH_SHA256'))
    parser.add_argument('--task', default=os.environ.get('WGC_TASK_ID'))
    parser.add_argument('--pattern', required=True)
    parser.add_argument('--file', action='append', dest='files')
    parser.add_argument('--max-matches', type=int, default=40)
    parser.add_argument('--max-output-bytes', type=int, default=12000)
    args = parser.parse_args()
    root = w.ROOT
    # A child cannot select another packet through this supported search entry point.
    for key, value in [('WGC_TASK_SEARCH_MANIFEST', args.manifest), ('WGC_TASK_SEARCH_SHA256', args.sha256),
                       ('WGC_TASK_ID', args.task)]:
        expected = os.environ.get(key)
        if expected and value != expected:
            raise ValueError('Task search override differs from the session binding')
    output = search(root, args.manifest, args.sha256, args.task, args.pattern,
                    args.files, args.max_matches, args.max_output_bytes)
    print(guard.json_text(output))


if __name__ == '__main__':
    guard.cli(w.ROOT, 'task_search', main)
