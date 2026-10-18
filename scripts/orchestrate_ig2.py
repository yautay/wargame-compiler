"""Bounded IG-2 supervisor: fresh local Codex processes, authoritative workflow gates."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid

import workflow as w
import search_task as task_search
import dependency_context as dep_context
import context_guard
import host_runtime

STAGE = 'IG-2'
MODEL = 'gpt-6.1-sol'
REASONING = 'high'
INVENTORY_TOOL_CONTEXT = [
    'docs/work/EVIDENCE.md', 'contracts/ig/README.md', 'contracts/ig/regions.schema.json',
    'src/wgc/sources/README.md', 'src/wgc/sources/__init__.py', 'src/wgc/sources/__main__.py',
    'src/wgc/sources/inventory.py', 'src/wgc/sources/geometry.py', 'src/wgc/sources/pdf.py',
    'docs/skills/wgc-execute/SKILL.md', 'docs/skills/wgc-review/SKILL.md',
]
SCHEMA = {
    'type': 'object', 'additionalProperties': False,
    'properties': {
        'outcome': {'type': 'string', 'enum': ['progress', 'pass', 'changes_requested', 'blocked']},
        'evidence': {'type': ['string', 'null']},
        'summary': {'type': 'string'},
    },
    'required': ['outcome', 'evidence', 'summary'],
}


def utc():
    return datetime.now(timezone.utc).isoformat()


def dump(path, data):
    """Atomic status replacement; session/result evidence uses unique directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.pending')
    with temp.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    for attempt in range(3):
        try:
            os.replace(temp, path)
            break
        except PermissionError as error:
            # Windows can briefly deny replacement while a reader/scanner holds
            # the destination. Keep atomicity and retry the same closed candidate.
            # Persistent denials remain failures; never truncate the old file.
            if attempt == 2 or getattr(error, 'winerror', None) not in {5, 32, 33}:
                raise
            time.sleep(0.05 * (attempt + 1))


def stage_tasks(q):
    return [t for t in q['tasks'] if t['stage'] == STAGE]


def repair_authorized(task):
    """An old repair packet never authorizes a new independent finding."""
    if task['status'] != 'changes_requested' or not task['events']:
        return False
    event = task['events'][-1]
    auth = task.get('repair_authorization', {})
    return (event['to'] == 'changes_requested' and
            auth.get('review_evidence') == event['evidence'] and
            auth.get('review_sha256') == event['sha256'] and
            bool(auth.get('scope')) and bool(auth.get('attempt')) and
            bool(auth.get('evidence')))


def select(q):
    """Recompute after every role; never infer readiness from filesystem contents."""
    stage = stage_tasks(q)
    if not stage or not {'IG-2C', 'IG-2D'} <= {t['id'] for t in stage}:
        raise ValueError('Incomplete IG-2 scope in queue')
    if all(t['status'] == 'done' for t in stage):
        return None, 'complete'
    busy = [t for t in q['tasks'] if t['status'] in w.BUSY]
    if busy:
        t = busy[0]
        if t['stage'] != STAGE:
            raise ValueError('Another stage owns the sequential work slot')
        if t['status'] in {'in_progress', 'accepted'}:
            raise ValueError(f'{t["id"]}: existing ownership requires checkpoint/acceptance triage')
        if t['status'] == 'review':
            return t, 'reviewer'
        return t, 'executor' if repair_authorized(t) else 'coordinator'
    for t in stage:
        if t['status'] == 'ready':
            return t, 'executor'
    by_id = {t['id']: t for t in q['tasks']}
    for t in stage:
        if t['status'] == 'planned' and all(by_id[d]['status'] == 'done' for d in t['depends']):
            return t, 'coordinator'
    raise ValueError('No eligible IG-2 work; resolve the queue blocker or dependency explicitly')


def outside_stage(q):
    return [t for t in q['tasks'] if t['stage'] != STAGE]


def check_queue_delta(before, after, task, role, frozen_targets=None, outcome=None):
    """Role-specific contracts, including blocked responses, precede all decisions."""
    if outcome == 'blocked' and before == after:
        return
    if role == 'reviewer':
        if after != before:
            raise ValueError('Reviewer modified the authoritative queue')
        return
    if {k: v for k, v in before.items() if k not in {'tasks', 'updated'}} != {
            k: v for k, v in after.items() if k not in {'tasks', 'updated'}}:
        raise ValueError('Queue metadata changed outside coordinator scope')
    old = {t['id']: t for t in before['tasks']}
    new = {t['id']: t for t in after['tasks']}
    if not old.keys() <= new.keys():
        raise ValueError('Existing task removed')
    for id, record in old.items():
        if id != task['id'] and record != new[id]:
            raise ValueError(f'Another task contract/status changed: {id}')
    current = new[task['id']]
    if current['stage'] != STAGE or current['id'] != task['id']:
        raise ValueError('Selected stage/identity changed')
    extra = [t for id, t in new.items() if id not in old]
    if role == 'executor':
        if extra or {k: v for k, v in current.items() if k not in {'status', 'events'}} != {
                k: v for k, v in task.items() if k not in {'status', 'events'}}:
            raise ValueError('Executor changed an immutable task contract')
        allowed = {'in_progress', 'review', 'blocked'}
    else:
        if task['status'] == 'changes_requested':
            if extra or current['status'] != task['status'] or current['events'] != task['events']:
                raise ValueError('Repair coordinator may refine only the current contract, not transition it')
            if not repair_authorized(current):
                raise ValueError('Repair coordinator did not bind scope to the current finding')
        if frozen_targets is not None and not extra:
            if (current['status'] not in {'planned', 'blocked'} or
                    {k: v for k, v in current.items() if k not in {'status', 'events'}} !=
                    {k: v for k, v in task.items() if k not in {'status', 'events'}}):
                raise ValueError('IG-2D refinement must create the bounded corpus partition')
        if task['semantic_acceptance_required'] and not current['semantic_acceptance_required']:
            raise ValueError('Coordinator weakened human acceptance gate')
        for key in ('context_recovery_authorization', 'dependency_scope'):
            if key in task and current.get(key) != task[key]:
                raise ValueError('Coordinator changed operator context recovery scope')
        for key in ('acceptance', 'tests'):
            if not set(task[key]) <= set(current[key]):
                raise ValueError(f'Coordinator removed required {key}')
        if extra:
            if task['id'] != 'IG-2D' or current['kind'] != 'closure' or current['status'] != 'planned':
                raise ValueError('Unexpected corpus partition')
            if set(current['depends']) != {t['id'] for t in extra}:
                raise ValueError('Closure does not depend on every new child')
            targets = []
            for child in extra:
                if (not child['id'].startswith(task['id'] + '-') or child['stage'] != STAGE or
                        child['status'] not in {'planned', 'ready'} or child['depends'] != task['depends'] or
                        (task['semantic_acceptance_required'] and not child['semantic_acceptance_required'])):
                    raise ValueError('Invalid child identity/dependencies/gates')
                ids = child.get('target_ids', [])
                if not ids or len(ids) > 20 or not all(isinstance(id, str) and id for id in ids):
                    raise ValueError('Child requires 1-20 exact target_ids')
                targets.extend(ids)
            universe = current.get('target_ids', [])
            if not frozen_targets or set(universe) != set(frozen_targets):
                raise ValueError('Partition universe differs from accepted dependency evidence')
            if not universe or len(targets) != len(set(targets)) or set(targets) != set(frozen_targets):
                raise ValueError('Partition target set mismatch or duplicate target')
        elif current['depends'] != task['depends']:
            raise ValueError('Dependencies changed outside a corpus partition')
        allowed = {'ready', 'blocked'}
    if current['events'][:len(task['events'])] != task['events']:
        raise ValueError('Prior transition evidence was rewritten')
    if any(e['to'] not in allowed for e in current['events'][len(task['events']):]):
        raise ValueError('Role recorded a forbidden status transition')


def configuration_binding(root, session, evidence):
    path = session / 'runtime-configuration.json'
    observed = w.read_json(path)
    if (observed.get('status') != 'confirmed' or observed.get('model') != MODEL or
            observed.get('reasoning') != REASONING or not observed.get('session_id')):
        raise ValueError('Session runtime configuration is not confirmed')
    if (evidence.get('model') != MODEL or evidence.get('reasoning') != REASONING or
            evidence.get('configuration_evidence') != path.relative_to(root).as_posix() or
            evidence.get('configuration_sha256') != w.digest(path)):
        raise ValueError('Evidence is not bound to this observed session configuration')


def delivery_pin_matches(root, actual, expected):
    """Compare identity fields; optional byte metadata must describe the same file."""
    if not isinstance(actual, dict) or any(actual.get(k) != expected[k] for k in ('path', 'sha256')):
        return False
    if 'bytes' in actual:
        size = actual['bytes']
        if type(size) is not int or size < 0 or w.safe_path(root, expected['path']).stat().st_size != size:
            return False
    return True


def verify_repair_authorization(root, task, require_absent=True):
    if not repair_authorized(task):
        raise ValueError('Current findings need a fresh coordinator repair scope')
    auth = task['repair_authorization']
    attempt = auth['attempt']
    path = w.safe_path(root, attempt)
    prefix = f'private/workflow/runs/{task["id"]}/'
    if not attempt.startswith(prefix) or not attempt.endswith('/') or attempt not in task['write_scope']:
        raise ValueError('Repair attempt is outside the exact authorized write scope')
    if require_absent and path.exists():
        raise ValueError('Authorized new repair attempt already exists; reconcile ownership before resume')
    for pin in [auth['scope'], auth['evidence']]:
        if not pin['path'].startswith(prefix):
            raise ValueError('Repair authorization must be preserved in the selected task run')
    verify_artifacts(root, {'artifacts': [auth['scope'], auth['evidence']]})
    scope = w.read_json(w.safe_path(root, auth['scope']['path']))
    required = {'review_evidence': auth['review_evidence'], 'review_sha256': auth['review_sha256'],
                'attempt': attempt, 'acceptance': task['acceptance'], 'tests': task['tests']}
    if any(scope.get(k) != v for k, v in required.items()) or not scope.get('finding_ids'):
        raise ValueError('Repair scope does not pin the actual review, criteria, checks and ownership')
    review = w.read_json(w.safe_path(root, auth['review_evidence']))
    ids = [f['id'] for f in review.get('findings', [])]
    if set(scope['finding_ids']) != set(ids) or len(scope['finding_ids']) != len(ids):
        raise ValueError('Repair scope does not account for the current independent findings')
    event, _ = latest_delivery(root, task)
    if not delivery_pin_matches(root, scope.get('immutable_delivery'),
                                {'path': event['evidence'], 'sha256': event['sha256']}):
        raise ValueError('Repair scope does not pin the current immutable delivery')
    if all(f.get('category') == 'required_validation_environment_failure' for f in review.get('findings', [])):
        if scope.get('mode') != 'validation_only':
            raise ValueError('Environment finding must have a validation-only repair scope')
    return scope


def continuation_preservation(root, task, require_absent=False):
    """Assess draft recovery without promoting a blocked attempt to accepted evidence."""
    auth = task.get('continuation_authorization')
    if not auth:
        return None
    prefix = f'private/workflow/runs/{task["id"]}/'
    for pin in [auth['scope'], auth['evidence']]:
        if not pin['path'].startswith(prefix):
            raise ValueError('Continuation authority must be a selected task run artifact')
    verify_artifacts(root, {'artifacts': [auth['scope'], auth['evidence']]})
    scope = w.read_json(w.safe_path(root, auth['scope']['path']))
    blocked = next(e for e in reversed(task['events']) if e['to'] == 'blocked')
    if (auth.get('blocked_evidence') != blocked['evidence'] or auth.get('blocked_sha256') != blocked['sha256'] or
            scope.get('blocked_evidence') != blocked['evidence'] or scope.get('blocked_sha256') != blocked['sha256']):
        raise ValueError('Continuation does not bind the exact blocked incident')
    blocked_pin = {'path': blocked['evidence'], 'sha256': blocked['sha256']}
    verify_artifacts(root, {'artifacts': [blocked_pin]})
    blocked_attempt = Path(blocked['evidence']).parent.as_posix() + '/'
    if not blocked_attempt.startswith(prefix) or scope.get('blocked_attempt') != blocked_attempt:
        raise ValueError('Continuation changed the original blocked attempt')
    if (scope.get('mode') != 'draft_revalidation' or scope.get('acceptance') != task['acceptance'] or
            scope.get('tests') != task['tests'] or scope.get('attempt') != auth.get('attempt')):
        raise ValueError('Continuation scope/gates differ from the authorized contract')
    attempt = auth['attempt']
    if not attempt.startswith(prefix) or not attempt.endswith('/'):
        raise ValueError('Continuation attempt is outside the selected task run')
    path = w.safe_path(root, attempt)
    continuation_delivery = None
    if attempt not in task['write_scope']:
        # After review, the current repair owns a new directory. The continuation
        # becomes a frozen input; its original ownership is not the current writer.
        if require_absent:
            raise ValueError('Initial continuation requires exact write ownership')
        repair_auth = task.get('repair_authorization', {})
        changes = next((i for i in range(len(task['events']) - 1, -1, -1)
                        if task['events'][i]['to'] == 'changes_requested' and
                        task['events'][i]['evidence'] == repair_auth.get('review_evidence') and
                        task['events'][i]['sha256'] == repair_auth.get('review_sha256')), None)
        if changes is None:
            raise ValueError('Continuation ownership changed without a reviewed repair')
        at_finding = dict(task, status='changes_requested', events=task['events'][:changes + 1])
        repair = verify_repair_authorization(root, at_finding, require_absent=False)
        repair_path = w.safe_path(root, repair['attempt'])
        if repair_path == path or path in repair_path.parents or repair_path in path.parents:
            raise ValueError('Review repair must own a separate continuation sibling')
        event = next((e for e in task['events'][:changes] if e['to'] == 'review' and
                      Path(e['evidence']).parent.as_posix() + '/' == attempt), None)
        if event is None:
            raise ValueError('Continuation has no frozen delivery before the repair finding')
        continuation_delivery = {'path': event['evidence'], 'sha256': event['sha256']}
        verify_artifacts(root, {'artifacts': [continuation_delivery]})
    old_path = w.safe_path(root, blocked_attempt)
    if path == old_path or old_path in path.parents or path in old_path.parents:
        raise ValueError('Continuation must use a separate fresh attempt')
    if require_absent and path.exists():
        raise ValueError('Fresh continuation attempt already exists; reconcile ownership')
    manifest_pin = scope['preserve_manifest']
    verify_artifacts(root, {'artifacts': [manifest_pin]})
    preserved = w.read_json(w.safe_path(root, manifest_pin['path']))['artifacts']
    blocked_body = w.read_json(w.safe_path(root, blocked['evidence']))
    blocked_artifacts = blocked_body['artifacts']
    verify_artifacts(root, {'artifacts': blocked_artifacts})
    original_paths = {blocked_attempt + name for name in (
        'blocked-state-manifest.json', 'blocked-attempt-preservation.json')}
    originals = [p for p in blocked_artifacts if p['path'] in original_paths]
    if len(originals) != 1:
        raise ValueError('Blocked event has no unique original preservation manifest')
    original = w.read_json(w.safe_path(root, originals[0]['path']))['artifacts']
    if preserved[:len(original)] != original:
        raise ValueError('Continuation omitted or changed original preserved artifacts')
    # Event references contain path/hash only; preservation rows may additionally
    # carry byte counts. Require every specified field without rejecting richer
    # records for the same exact immutable bytes.
    preserved_by_path = {}
    for stored in preserved:
        preserved_by_path.setdefault(stored['path'], []).append(stored)
    if any(not any(all(stored.get(k) == v for k, v in pin.items())
                   for stored in preserved_by_path.get(pin['path'], []))
           for pin in blocked_artifacts + [blocked_pin]):
        raise ValueError('Continuation omitted blocked-event evidence')
    verify_artifacts(root, {'artifacts': preserved})
    drafts = scope.get('drafts', [])
    if not drafts or any(not p['path'].startswith(scope['blocked_attempt']) for p in drafts):
        raise ValueError('Continuation drafts are not exact blocked-attempt inputs')
    verify_artifacts(root, {'artifacts': drafts})
    if continuation_delivery is not None:
        delivery = w.read_json(w.safe_path(root, continuation_delivery['path']))
        verify_artifacts(root, delivery)
        # Snapshot both immutable attempts for the existing post-role check and
        # reconstruct this baseline on later review/restart, including blocked outcomes.
        preserved = list(preserved)
        known = {p['path']: p['sha256'] for p in preserved}
        for pin in delivery['artifacts'] + [continuation_delivery]:
            if pin['path'] in known:
                if known[pin['path']] != pin['sha256']:
                    raise ValueError('Continuation preservation has conflicting artifact pins')
            else:
                preserved.append(pin)
                known[pin['path']] = pin['sha256']
    return preserved


def verify_artifacts(root, evidence):
    if not evidence.get('artifacts'):
        raise ValueError('Empty delivery manifest')
    for a in evidence['artifacts']:
        p = w.safe_path(root, a['path'])
        if w.denied(a['path']) or not p.is_file() or w.digest(p) != a['sha256']:
            raise ValueError(f'Frozen artifact changed: {a["path"]}')


def verify_preserved_delivery(root, original, new_delivery=None):
    verify_artifacts(root, {'artifacts': original})
    if new_delivery is not None and new_delivery.get('artifacts', [])[:len(original)] != original:
        raise ValueError('Validation-only repair omitted, changed or reordered an immutable delivery entry')


def ripgrep_environment(env, binding):
    """Preserve every inherited entry while exposing the verified tool to raw tests."""
    result = dict(env)
    result.update(WGC_RIPGREP_PATH=binding['path'], WGC_RIPGREP_SHA256=binding['sha256'])
    result['PATH'] = str(Path(binding['path']).parent) + os.pathsep + result.get('PATH', '')
    return result


def native_path_prefix(value):
    """Accept one native directory or an ordered PATH snapshot, without mutation."""
    if value is None or value == '' or value == []:
        return ''
    paths = [value] if isinstance(value, str) else value
    if not isinstance(paths, list) or any(
            not isinstance(p, str) or not p or '\x00' in p or os.pathsep in p for p in paths):
        raise ValueError('Pinned native path prefix must be a string or list of nonempty directory strings')
    # An ordered PATH snapshot may retain expired session-wrapper directories.
    # Keep every entry exactly; the OS ignores nonexistent PATH entries. A single
    # explicitly pinned directory (or an entirely unavailable list) still fails.
    if not any(Path(p).is_dir() for p in paths):
        raise ValueError('Pinned native dependency directory is unavailable')
    return os.pathsep.join(paths)


def validation_environment(root, task, ripgrep=None):
    """Reuse the pinned installed runtime; never install or mutate libraries/configuration."""
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    host = host_runtime.bound(root)
    if host is not None:
        if ripgrep is not None and any(ripgrep[k] != host['tools']['rg'][k] for k in ('path', 'sha256')):
            raise ValueError('Ripgrep differs from the bound host runtime')
        return host_runtime.environment(host, env)
    if ripgrep is None and (env.get('WGC_RIPGREP_PATH') or env.get('WGC_RIPGREP_SHA256')):
        ripgrep = task_search.ripgrep_binding()
    if ripgrep is not None:
        env = ripgrep_environment(env, ripgrep)
    for rel in task.get('context', []):
        if Path(rel).name != 'toolchain.json':
            continue
        toolchain = w.read_json(w.safe_path(root, rel))
        pythonpath = toolchain.get('process_pythonpath')
        prefix = native_path_prefix(toolchain.get('process_path_prefix'))
        if pythonpath:
            if not all(Path(p).is_dir() for p in pythonpath.split(os.pathsep)):
                raise ValueError('Pinned Python dependency directories are unavailable')
            env['PYTHONPATH'] = pythonpath
        if prefix:
            env['PATH'] = prefix + os.pathsep + env.get('PATH', '')
    return env


def latest_delivery(root, task):
    event = next(e for e in reversed(task['events']) if e['to'] == 'review')
    p = w.safe_path(root, event['evidence'])
    if w.digest(p) != event['sha256']:
        raise ValueError('Frozen delivery evidence changed')
    delivery = w.read_json(p)
    verify_artifacts(root, delivery)
    return event, delivery


def launch_environment(root, task, session, cli=None):
    """Carry the installed pinned runtime into a planned coordinator, before refinement."""
    view = w.read_json(session / 'dependency-view.json')
    effective = task
    host = host_runtime.bound(root)
    if host is not None:
        if cli is not None and str(Path(cli).resolve()) != host['tools']['codex']['path']:
            raise ValueError('Selected Codex differs from the bound host runtime')
        host_runtime.verify_cli(host['tools']['codex']['path'])
        dump(session / 'host-runtime.json', host)
    if host is None and not any(Path(p).name == 'toolchain.json' for p in task.get('context', [])):
        refs = {p['path']: p for dep in view.get('dependencies', {}).values()
                if (p := dep.get('inventory', {}).get('reports', {}).get('toolchain.json'))}
        if len(refs) == 1:
            pin = next(iter(refs.values()))
            dep_context.checked(root, pin)
            effective = dict(task, context=task.get('context', []) + [pin['path']])
    ripgrep = task_search.ripgrep_binding(cli)
    version = subprocess.run([ripgrep['path'], '--version'], capture_output=True, text=True,
                             encoding='utf-8', errors='replace', timeout=5)
    if version.returncode or not version.stdout.startswith('ripgrep '):
        raise ValueError('Pinned ripgrep preflight failed; no model launched')
    dump(session / 'tool-runtime.json', {'ripgrep': {**ripgrep, 'version': version.stdout.splitlines()[0]},
                                      'verified_utc': utc()})
    return dict(validation_environment(root, effective, ripgrep), WGC_TASK_ID=task['id'],
                WGC_RIPGREP_PATH=ripgrep['path'], WGC_RIPGREP_SHA256=ripgrep['sha256'],
                WGC_TASK_SEARCH_MANIFEST=(session / 'search-manifest.json').relative_to(root).as_posix(),
                WGC_TASK_SEARCH_SHA256=w.digest(session / 'search-manifest.json'),
                WGC_TASK_DEPENDENCY_VIEW=(session / 'dependency-view.json').relative_to(root).as_posix(),
                WGC_TASK_DEPENDENCY_SHA256=w.digest(session / 'dependency-view.json'),
                WGC_TASK_ACCESS_MANIFEST=(session / 'access-manifest.json').relative_to(root).as_posix(),
                WGC_TASK_ACCESS_SHA256=w.digest(session / 'access-manifest.json'),
                WGC_CONTEXT_GUARD=(session / 'context-guard.json').relative_to(root).as_posix(),
                WGC_CONTEXT_GUARD_SHA256=w.digest(session / 'context-guard.json'))


def validation_repair_baseline(root, task):
    """Recover the immutable baseline across blocked/interrupted supervisor processes."""
    auth = task.get('repair_authorization', {})
    if not auth.get('scope'):
        return None
    verify_artifacts(root, {'artifacts': [auth['scope']]})
    scope = w.read_json(w.safe_path(root, auth['scope']['path']))
    if scope.get('mode') != 'validation_only':
        return None
    changes = next(i for i in range(len(task['events']) - 1, -1, -1)
                   if task['events'][i]['to'] == 'changes_requested')
    event = task['events'][changes]
    if auth.get('review_evidence') != event['evidence'] or auth.get('review_sha256') != event['sha256']:
        raise ValueError('Validation lineage does not match the latest repair review')
    previous = next(e for e in reversed(task['events'][:changes]) if e['to'] == 'review')
    pin = {'path': previous['evidence'], 'sha256': previous['sha256']}
    if not delivery_pin_matches(root, scope.get('immutable_delivery'), pin):
        raise ValueError('Validation lineage changed its original delivery')
    verify_artifacts(root, {'artifacts': [pin]})
    return w.read_json(w.safe_path(root, pin['path']))['artifacts']


def accepted_universe(root, q, task):
    """Freeze the universe from an independently accepted IG-2C delivery, before refinement."""
    dep = next(t for t in q['tasks'] if t['id'] == 'IG-2C')
    if 'IG-2C' not in task['depends'] or dep['status'] != 'done':
        raise ValueError('Partition requires accepted IG-2C dependency')
    event = dep['events'][-1]
    evidence_path = w.safe_path(root, event['evidence'])
    if w.digest(evidence_path) != event['sha256']:
        raise ValueError('Accepted universe evidence changed')
    manifest = w.read_json(evidence_path)
    matches = [a for a in manifest['artifacts'] if Path(a['path']).name == 'reconciliation-universe.json']
    if len(matches) != 1:
        raise ValueError('IG-2C must deliver exactly one accepted reconciliation-universe.json')
    reference = matches[0]
    verify_artifacts(root, {'artifacts': [reference]})
    universe = w.read_json(w.safe_path(root, reference['path']))
    ids = universe.get('target_ids', [])
    if (universe.get('format') != 'wgc-reconciliation-universe-1' or not ids or
            not all(isinstance(id, str) and id for id in ids) or len(ids) != len(set(ids)) or
            len(universe.get('inputs', [])) < 2):
        raise ValueError('Invalid accepted reconciliation universe or missing input provenance')
    verify_artifacts(root, {'artifacts': universe['inputs']})
    return ids, reference


def prepare(root, q, task, role, session):
    """Small contract plus lazy, hash-pinned references; no transcript carry-over."""
    contract = {k: v for k, v in task.items() if k != 'events'}
    dump(session / 'task.json', contract)
    recovery = task.get('context_recovery_authorization')
    if recovery:
        pins = [recovery[k] for k in ('incident', 'scope', 'assessment')]
        if any(not p['path'].startswith(f'private/workflow/runs/{task["id"]}/') for p in pins):
            raise ValueError('Context recovery authority must belong to the selected task')
        verify_artifacts(root, {'artifacts': pins})
        dump(session / 'context-recovery-preserved.json', pins)
    protected = continuation_preservation(root, task, require_absent=role == 'executor' and task['status'] == 'ready')
    if protected is not None:
        dump(session / 'continuation-preserved.json', protected)
        dump(session / 'continuation-scope-reference.json', task['continuation_authorization']['scope'])
    if role == 'executor' and task['status'] == 'changes_requested':
        scope = verify_repair_authorization(root, task)
        dump(session / 'repair-scope.json', scope)
        if scope.get('mode') == 'validation_only':
            base = w.read_json(w.safe_path(root, scope['immutable_delivery']['path']))
            dump(session / 'preserved-artifacts.json', base['artifacts'])
    if role == 'coordinator':
        refs = []
        # A planned contract may legitimately contain missing inputs. Refine first.
        for rel in task['context']:
            p = w.safe_path(root, rel)
            if not w.permitted(root, rel):
                raise ValueError(f'Forbidden planned context: {rel}')
            refs.append({'path': rel, 'exists': p.is_file(),
                         'sha256': w.digest(p) if p.is_file() else None})
        packet = {'task': task['id'], 'queue_sha256': w.digest(root / w.QUEUE), 'files': refs}
    else:
        packet = w.packet(q, root, task['id'], output=False)
    # These exact control files are operator-authorized tooling context, read on demand.
    controls = ['README.md', 'docs/work/WORKFLOW.md',
                'scripts/workflow.py', 'scripts/check.ps1', 'scripts/search_task.py', 'scripts/dependency_context.py',
                'scripts/context_guard.py', 'scripts/task_access.py',
                'scripts/orchestrate_ig2.py',
                'docs/skills/' + {'executor': 'wgc-execute', 'reviewer': 'wgc-review',
                                  'coordinator': 'wgc-queue'}[role] + '/SKILL.md']
    controls += task.get('tool_context', INVENTORY_TOOL_CONTEXT if re.fullmatch(r'IG-2B\d{2}', task['id']) else [])
    if host_runtime.bound(root) is not None:
        controls += ['scripts/host_runtime.py', 'docs/work/IG2-RESTORE.md', host_runtime.REQUIREMENTS]
    controls = list(dict.fromkeys(controls))
    control_pins = []
    for rel in controls:
        p = w.safe_path(root, rel)
        if not task_search.searchable(rel) or not w.permitted(root, rel) or not p.is_file():
            raise ValueError(f'Missing or forbidden task control context: {rel}')
        control_pins.append({'path': rel, 'bytes': p.stat().st_size, 'sha256': w.digest(p)})
    packet['control_files'] = control_pins
    dump(session / 'packet.json', packet)
    search_pins = {p['path']: p for p in packet['files'] + control_pins
                   if p.get('sha256') and task_search.searchable(p['path'])}
    dump(session / 'search-manifest.json', {'format': task_search.FORMAT, 'task': task['id'],
         'packet': {'path': (session / 'packet.json').relative_to(root).as_posix(),
                    'sha256': w.digest(session / 'packet.json')},
         'files': list(search_pins.values()),
         'policy': 'Exact stable public text only; private evidence needs scoped locators/JSON selection, never generic search.'})
    git_paths = [f'private/workflow/runs/{task["id"]}/', w.QUEUE, 'docs/work/context-policy.json',
                 f'docs/work/tasks/{task["id"]}.md', 'docs/STATUS.md', 'docs/HANDOFF.md', 'docs/ROADMAP.md']
    git_paths += [p for p in task.get('write_scope', [])
                  if p not in {'private/workflow/checks/', 'private/workflow/packets/'}]
    git_paths += list(search_pins)
    bootstrap_reads = {}
    for rel in ('docs/STATUS.md', 'docs/HANDOFF.md'):
        source = w.safe_path(root, rel)
        if source.is_file():
            target = session / 'bootstrap' / Path(rel).name
            target.parent.mkdir(exist_ok=True)
            with target.open('xb') as stream:
                stream.write(source.read_bytes())
            bootstrap_reads[rel] = {'path': target.relative_to(root).as_posix(),
                                    'sha256': w.digest(target), 'bytes': target.stat().st_size}
    validation_scope = {}
    if role == 'reviewer':
        event, delivery = latest_delivery(root, task)
        attempt = task.get('inventory_contract', {}).get('attempt_root')
        if attempt:
            paths = [attempt.rstrip('/') + '/' + name + '/inventory.json'
                     for name in ('final-verified', 'replay-1', 'replay-2')]
            inputs = []
            for path in paths:
                matches = [a for a in delivery['artifacts'] if a['path'] == path]
                if len(matches) != 1:
                    raise ValueError('Frozen delivery lacks an exact final/replay validation input')
                inputs.append(matches[0])
            validation_scope = {'mode': 'frozen', 'inputs': inputs,
                'log_root': f'private/workflow/runs/{task["id"]}/review-validation-{session.name}/'}
    elif role == 'executor':
        attempt = task.get('inventory_contract', {}).get('attempt_root')
        if attempt:
            attempt = attempt.rstrip('/') + '/'
            if (attempt not in task.get('write_scope', []) or
                    not attempt.startswith(f'private/workflow/runs/{task["id"]}/')):
                raise ValueError('Executor validation attempt lacks exact task write ownership')
            validation_scope = {'mode': 'owned_attempt', 'attempt': attempt,
                'inputs': [{'path': attempt + name + '/inventory.json'}
                           for name in ('final-verified', 'replay-1', 'replay-2')],
                'log_root': f'private/workflow/runs/{task["id"]}/review-validation-{session.name}/'}
    dump(session / 'access-manifest.json', {'format': 'wgc-task-access-1', 'task': task['id'],
         'search_manifest': {'path': (session / 'search-manifest.json').relative_to(root).as_posix(),
                             'sha256': w.digest(session / 'search-manifest.json')},
         'git_paths': list(dict.fromkeys(git_paths)), 'bootstrap_reads': bootstrap_reads,
         'source_validation': validation_scope})
    dump(session / 'context-guard.json', {'format': 'wgc-context-guard-1', 'task': task['id'],
         'denial': (session / 'context-denied.json').relative_to(root).as_posix()})
    by_id = {t['id']: t for t in q['tasks']}
    references = {'dependencies': {id: by_id[id]['events'][-1] for id in task['depends']
                                    if by_id[id]['events']}}
    changes = next((i for i in range(len(task['events']) - 1, -1, -1)
                    if task['events'][i]['to'] == 'changes_requested'), None)
    if changes is not None:
        references['findings'] = task['events'][changes]
        references['prior_delivery'] = next((e for e in reversed(task['events'][:changes])
                                              if e['to'] == 'review'), None)
        references['repair_claim'] = next((e for e in task['events'][changes + 1:]
                                            if e['to'] == 'in_progress'), None)
    dump(session / 'references.json', references)
    dump(session / 'dependency-view.json', dep_context.build(root, q, task))
    if role == 'reviewer':
        original = validation_repair_baseline(root, task)
        if original is not None:
            verify_preserved_delivery(root, original, delivery)
        dump(session / 'delivery-reference.json', event)
        # Full manifest is on disk, never copied to the launch prompt.
        dump(session / 'delivery.json', delivery)
    elif task['status'] == 'changes_requested':
        dump(session / 'repair-reference.json', task['events'][-1])
    return packet


def prompt(root, task, role, session):
    rel = session.relative_to(root).as_posix()
    skill = {'executor': 'wgc-execute', 'reviewer': 'wgc-review', 'coordinator': 'wgc-queue'}[role]
    instructions = {
        'executor': '''Verify readiness or the bounded changes_requested repair, dependencies,
ownership, packet pins and your own confirmed runtime configuration. For an existing
repair use only the current finding/scope references; do not repeat unchanged work.
Claim through scripts/workflow.py transition, checkpoint, implement ONLY this task,
run its required checks, freeze every delivery file and transition to review. Return
progress with the delivery evidence path. If ownership is uncertain, stop blocked.''',
        'reviewer': '''Read delivery-reference.json and delivery.json. Verify EVERY frozen artifact.
Independently inspect the entire assigned original page/target scope and complete
ledger; cheap summaries are not proof. For rereview use current frozen hashes, exact
findings, changed material and affected risks, and verify preserved prior coverage.
Write a new independent review artifact under private/workflow/runs/<task>/<new-review>/.
For pass use role reviewer, your unique actor, ALL exact acceptance criteria, EXACT
delivery artifacts in the same order, actual configuration and passing named checks.
Return pass with this evidence path, or changes_requested with precise actionable
findings, affected criteria, repair validation and same evidence fields.
Use stable finding IDs across reviews: keep an unresolved/reopened issue's original
ID and allocate unused IDs only for genuinely new issues. Never renumber findings
to reset repair limits. Each finding has its own two-cycle lifetime budget.
Do not mutate queue/status, implementation, sources, or old attempts. Never mark accepted or done.''',
        'coordinator': '''Refine ONLY this selected planned task. FIRST read accepted dependency
sections through scripts/dependency_context.py. Its inventory section supplies the
current full baseline, companion registry, exact current report pins, source pins and
assigned-page metadata; boundary is only the prior range's exit observation. Outputs
identifies the accepted dependency's declared result pins. Toolchain supplies installed
process paths: use them for coordinator checks as well as the future executor.
Never decode/print dependency queue records, event lists, accepted closure/delivery
envelopes, complete artifact manifests or unassigned source content into model context.
For byte preservation, tool code may decode pins and copy unchanged records internally;
emit only counts/hashes, never manifest rows, histories or unassigned source text.
Read only assigned fields/pages from the
selected report/inventory references; copy nonassigned records structurally without output.
For IG-2B inventory batches, retain the complete accepted 44-page sidecar, every
nonassigned record/link/evidence and persisted registry binding. Replace only the
assigned placeholders; retire membership without deleting old registry entries.
Use final-verified/inventory.json and companion identity-registry.json under a new
owned attempt, with region-ledger.json, continuations.json, coverage-report.json,
source-pins.json and toolchain.json at its root. Current source-reference index
repairs supersede only named reports; never use an ancestor inventory as the latest
baseline. Pin all original-page inspection, fresh evidence, two independent replays,
full/task/context denominators and fresh independent review before executor readiness.
Pin actual input files, hashes, pages/target IDs, disjoint outputs, acceptance and tests.
Replace obsolete placeholder source paths with verified accepted dependency inputs.
Update queue/context policy and render derived views. Make ready only after complete
refinement, available exact context and done dependencies, with real ready evidence.
For IG-2D partition at most 20 clauses per child, pin context-only IDs, validate target
set equality without overlaps, preserve cross-batch references, make parent closure
depend on children which inherit its former prerequisites. All children stay IG-2.
Record target_ids on the parent (complete universe) and each child (1-20 assigned
targets), and context_only_ids separately; the supervisor checks exact partition sets.
For IG-2C refinement REQUIRE the deliverable reconciliation-universe.json, format
wgc-reconciliation-universe-1, unique namespaced target_ids for the COMPLETE source
inventory and imported record universe, and inputs (path/SHA-256 for both pinned
inventory and import). Add explicit tests and independent acceptance verifying set
equality against both complete inputs. Include this JSON in IG-2C's frozen manifest.
For IG-2D use partition-universe-reference.json from the supervisor: this accepted
IG-2C universe is immutable and must not be reconstructed from a smaller selection.
Preserve every original acceptance criterion and required test verbatim; append
refinements rather than replacing them. Never lower a human acceptance gate.
Never fabricate product deliverables, acceptance, source meaning or completed status.
Do not change any other existing task except dependency rewiring needed by this
partition, and never change tasks outside IG-2. Return progress plus readiness or
partition evidence, or blocked with the smallest missing decision.''',
    }[role]
    if role == 'coordinator' and task['status'] == 'changes_requested':
        instructions = '''Prepare ONLY a new bounded repair contract for the CURRENT review in
references.json, before any executor is launched. Do not repair source/product files,
claim, transition status, accept or finish a task. Preserve all previous events, exact
acceptance criteria and required tests, and every already frozen artifact.
Read current findings and latest frozen delivery by exact references. Allocate a NEW
ABSENT attempt under private/workflow/runs/<task>/repair-<finding>-<unique>/; replace
obsolete write ownership/start conditions/output instructions and old repair context
with the CURRENT finding. Keep earlier source corrections immutable. For validation
environment findings the scope is validation-only: no source/tool/test/contract edits.
Write a small scope JSON under a separate new preparation run with review_evidence,
review_sha256, finding_ids, attempt (slash-terminated), acceptance and tests copied
verbatim, immutable_delivery (path/SHA256), mode, allowed changes and required checks.
Write a coordinator authorization evidence JSON with your actor/config fields and
artifacts pinning that scope and the current review. Bind task.repair_authorization:
review_evidence/review_sha256 equal CURRENT changes_requested event; scope/evidence
are path/SHA256 pins; attempt equals the new slash-terminated owned directory.
Keep task status changes_requested and events unchanged. Update context-policy only
with exact new scope/authorization files or a small docs/work/repair-context index;
do not inject the huge delivery/review manifests into packet text. Render and validate
views. Return progress with coordinator authorization evidence path. If inputs or
permissions remain unavailable, preserve the missing decision and return blocked.'''
    return f'''Work in {root}. The operator explicitly authorized automatic sequential IG-2
executor/reviewer sessions. This permission replaces manual launch only; all quality,
human acceptance, source access and preservation gates remain binding.
Role: {role}. Task: {task['id']}. Unique actor: ig2:{session.name}:{role}.

FIRST read {rel}/runtime-configuration.json. If pending, wait at most 30 seconds for
the supervisor to confirm CLI STARTUP metadata. If it is absent/unconfirmed/mismatched,
return blocked without claims or product writes. Invocation flags are not observation.
Use only observed gpt-6.1-sol/high. Every claim, delivery, readiness/partition or review
JSON MUST set configuration_evidence to the exact repository-relative path
{rel}/runtime-configuration.json and configuration_sha256 to its actual SHA-256.
Set actor to ig2:{session.name}:{role}; model/reasoning to the observed values.

Read AGENTS.md, README.md, docs/STATUS.md, docs/HANDOFF.md,
docs/work/WORKFLOW.md and docs/skills/{skill}/SKILL.md, then
{rel}/task.json, {rel}/packet.json and {rel}/references.json. The manifest is the
exact task packet. References pin accepted dependency events and current repair
findings/prior delivery/claim, without copying their entire histories.
Verify hashes locally. Read required text/contracts on demand in bounded sections;
inspect all source pages/regions assigned by the contract. Binary byte hashes do not
authorize whole-PDF analysis. Do not load context.txt, whole queue event histories,
prior transcripts, entire run directories, archives, Git history or neighbouring repos.
For structural edits, use task.json for the selected contract. Load queue.json only
inside the edit/check process; never print it or dependency records/event histories.
Print only needed non-event fields for this task or authorized direct partition children.
DEPENDENCY READ OVERRIDE: use ONLY the prepared, hash-bound projection command
.venv/Scripts/python.exe scripts/dependency_context.py --task {task['id']}
--manifest {rel}/dependency-view.json --sha256 {w.digest(session / 'dependency-view.json')}
--dependency '<direct dependency ID>' --section summary|outputs|inventory|boundary|toolchain
(one command, one section). No history, full-manifest, arbitrary-field or global mode exists.
The helper binds WGC_TASK_DEPENDENCY_* and rejects unlisted dependencies/stale authority.
Do not read old dependency transcripts or dump their closure JSON even by exact path.
If task.json has context_recovery_authorization, read ONLY its new scope/assessment;
the old incident is immutable metadata, not a transcript to replay. This is a fresh
coordinator session and grants no readiness or acceptance in advance.
TASK SEARCH OVERRIDE AUTHORIZED BY THE OPERATOR: for text search use ONLY
.venv/Scripts/python.exe scripts/search_task.py --task {task['id']}
--manifest {rel}/search-manifest.json --sha256 {w.digest(session / 'search-manifest.json')}
--pattern '<regex>' [--file '<exact path>'] (one command; quoted regex).
The supervisor binds this session to {rel}/search-manifest.json via WGC_TASK_SEARCH_*
environment variables. The packet's control_files are additional exact tooling context
for this task, read on demand. NEVER call the frozen legacy scripts/search.ps1, raw
repository-wide rg, workflow.py files, or recursive directory searches in a task session.
The task helper refuses unlisted paths and private/binary/volatile files and bounds
output. For private evidence use only exact task-authorized locators or selected JSON
fields/pages/IDs; do not print whole manifests or search private trees. No global fallback.
Read stable public packet text ONLY with
.venv/Scripts/python.exe scripts/task_access.py read --file '<exact packet path>'
--start-line 1 --lines 80 (one command; access binding is inherited).
Required docs/STATUS.md and docs/HANDOFF.md reads use this same command. Their exact
dispatch snapshots are pinned in access-manifest.json bootstrap_reads. These are
navigation views, never live task/status authority; task.json and workflow gates
govern your selected task. They remain excluded from generic search. Never directly
read the changing live generated views or substitute them for the selected contract.
Bootstrap files explicitly named above and this session's own JSON metadata may be
read by exact path. Source evidence remains limited to assigned pages/IDs.
Read only needed documentation/code windows from control_files; do not prefetch all.
CONTEXT REQUESTS MUST BE SEQUENTIAL. A helper refusal writes a durable denial latch
and holds the request while the supervisor terminates this CLI tree. No next command,
direct Get-Content/Python file read, raw rg or alternate-tool fallback is permitted.
Missing context requires coordinator/operator refinement in a NEW session.
For working-tree state use ONLY
.venv/Scripts/python.exe scripts/task_access.py git-status --max-items 40
(one command). Its fixed literal Git pathspecs select task runs/outputs, exact packet
files and authorized queue/views, excluding other tasks and global checks/packets.
Never run raw repository-wide git status or recursive file listings. The required
git diff --check remains allowed; preserve all preexisting staged/unstaged work.
Persist evidence under private/.
For executor AND reviewer source CLI validation use ONLY
.venv/Scripts/python.exe scripts/task_access.py validate-source --file '<exact inventory path>'
(one command, inherited task/access binding). access-manifest.json pins the current
final-verified and both replay inventories and a separate task-owned private log root.
For an executor, these are the exact three generated output paths in its owned
attempt, authorized only after this observed session claims the current task. Each
call snapshots the generated inventory hash and verifies it again after validation.
For a reviewer, dispatch pins the immutable delivered inventory hashes instead.
The helper runs the unchanged full validator and returns only exit code and log pins.
Full stdout/stderr remain private, including failures. Never print raw validation logs,
tails, traceback payloads or unassigned-page coverage rows. Additional diagnostics
require explicit assigned-page/field selection or a fresh coordinator scope.
Capture other validation/check output in new private logs too; release command/exit
and explicitly selected task fields only. No generic last-N-character/line preview.

{instructions}

Generate source-region evidence serially in the current Python process. Do not use
multiprocessing, ProcessPoolExecutor or worker-process pools: the Windows restricted
token can deny their named pipes. Run both complete independent replays separately;
serial generation must preserve the complete region/component set and every check.
Ordinary installed source CLI/native tools remain allowed within the task scope.

Tests still run unchanged. If the Windows restricted token cannot access pytest's
mode-0700 temporary directory, request approved execution of that exact unchanged
validation command using sandbox_permissions=require_escalated and a clear reason.
The same approved exact-command path applies when Windows denies terminating the
owned synthetic process tree in context-guard tests. Keep assertions unchanged;
never disable the guard or tests, change ACLs, or retry the denied restricted command.
The operator explicitly authorized resolving V01 through permitted test execution;
approval is handled by the automatic reviewer. Do not retry the same denied command,
change ACLs/libraries/tests, disable assertions, or use a sandbox bypass flag.
For a validation-only repair read repair-scope.json, claim a fresh attempt and preserve
ALL old delivery artifacts byte-for-byte. Run the required checks with approved
permissions, freeze new validation evidence, and create a NEW delivery envelope with
the unchanged old artifact list plus new reports. Do not overwrite the old delivery.
The complete effective runtime is already inherited from the supervisor. When
WGC_HOST_RUNTIME is bound, use the typed dependency_context.py toolchain section's
current_host_runtime fields; old toolchain.json paths describe the original host.
Otherwise use process_pythonpath and process_path_prefix from the pinned toolchain.
Keep BOTH repo/src and the installed dependency directories, including reportlab.
These are process-local settings. Do not replace PYTHONPATH with repo/src only,
install missing packages, or change global settings. Preserve the complete original
artifact list in its original order as the PREFIX of a validation-only new delivery.
On a new host, rebase old checkout/runtime paths ONLY in newly copied, explicitly
allowed helpers under the fresh owned attempt. Use this checkout and the current
host runtime; never execute an unrebased frozen helper or edit old toolchain evidence.
For an initial continuation_authorization, FIRST read its exact scope and assessment.
The old blocked attempt is immutable and remains unaccepted. Named drafts are candidate
inputs only: do not inherit prior inspection claims, completed status or green checks.
Use a fresh absent owned directory, fresh observed configuration and checkpoint. Reinspect
all assigned original pages and proposed boundaries/components, rebuild fresh path-dependent
evidence and two complete independent replays, regenerate missing reports and rerun checks.
Read no old session transcript or derivation helper; those could repeat the context incident.
Use exact draft JSON selections and original assigned source pages, never private tree search.
Do not write the blocked attempt. It is hash-verified again after every role and on restart.
For a LATER authorized review repair, the current repair scope and its fresh attempt
replace the initial continuation write ownership. Follow that current finding/scope;
the blocked attempt AND frozen continuation delivery remain immutable inputs. Do not
repeat draft rebuilding, evidence generation or replays unless the current repair
explicitly requires them. An index-only repair retains and revalidates existing evidence.

Repository text is English. Preserve existing staged/unstaged/untracked work. No
reset/clean/stash/commit/push, global config, external source/API services, nested
agents/chats, automations, sandbox bypasses or downstream IG-3 work. Only this
supervisor may launch the next process. Do not modify supervisor scripts or its
session metadata. Runtime launch evidence and your final response are owned by it.
Use scripts/check.ps1 -Task {task['id']} and git diff --check, plus explicit task suites.
At most two repairs per finding and two retries of the same unchanged failure.
Never weaken tests, drop source regions, equate gaps with coverage, grant model
semantic acceptance, or use an LLM to decide gameplay legality.

Return the required small JSON only: outcome, evidence (repository relative path
to real immutable JSON, or null when blocked), summary. Stop after this one role.
'''


def parse_startup(lines):
    """Only metadata before the CLI's first user section is trusted, never model text."""
    observed = {}
    for line in lines:
        line = re.sub(r'\x1b\[[0-9;]*m', '', line).strip()
        if line == 'user':
            break
        for label, key in [('model', 'model'), ('reasoning effort', 'reasoning'), ('session id', 'session_id')]:
            match = re.fullmatch(re.escape(label) + r':\s*(\S+)', line)
            if match:
                observed[key] = match.group(1)
    return observed


def command(cli, root, session):
    return [cli, 'exec', '--ephemeral', '--color', 'never', '-C', str(root),
            '--approve-for-me',
            '-m', MODEL, '-c', 'model_reasoning_effort="high"',
            '--output-schema', str(session / 'response-schema.json'),
            '-o', str(session / 'response.json'), '-']


def stop_process(proc):
    """Terminate this process tree with bounded cleanup; report failures explicitly."""
    if proc.poll() is not None:
        return
    if os.name == 'nt':
        failure = None
        try:
            killed = subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'],
                                    capture_output=True, timeout=5)
            if killed.returncode != 0 and proc.poll() is None:
                failure = f'Owned process tree termination failed; inspect descendants of PID {proc.pid}'
        except subprocess.TimeoutExpired:
            failure = f'Owned process tree termination timed out; inspect descendants of PID {proc.pid}'
        if failure and proc.poll() is None:
            proc.kill()  # Use the handle we own even if tree inspection/termination was denied.
    else:
        proc.kill()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired as exc:
        raise ValueError(f'Owned process did not exit; inspect PID {proc.pid}') from exc
    if os.name == 'nt' and failure:
        raise ValueError(failure)


def remaining(deadline):
    seconds = deadline - time.monotonic()
    if seconds <= 0:
        raise ValueError('Total wall-time budget exhausted; no next operation started')
    return seconds


def start_background(root, cli, max_sessions, session_seconds, total_seconds):
    """Detach an authorized launch from the invoking console and Windows job."""
    if (root / 'private/workflow/ig2-orchestrator.lock').exists():
        raise ValueError('Existing supervisor lock requires ownership triage before launch')
    launch_dir = root / 'private/workflow/launches' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:8])
    launch_dir.mkdir(parents=True, exist_ok=False)
    # Windows venv python.exe redirects to a second interpreter process. Launch
    # that interpreter directly so the saved handle/PID owns the actual supervisor.
    interpreter = (getattr(sys, '_base_executable', None) or sys.executable) if os.name == 'nt' else sys.executable
    argv = [interpreter, str(root / 'scripts/orchestrate_ig2.py'), 'run', '--codex', cli,
            '--max-sessions', str(max_sessions), '--session-seconds', str(session_seconds),
            '--total-seconds', str(total_seconds)]
    options = ({'creationflags': subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP |
                subprocess.CREATE_BREAKAWAY_FROM_JOB} if os.name == 'nt' else {'start_new_session': True})
    record = {'argv': argv, 'started_utc': utc(), 'invoking_pid': os.getpid(),
              'invoking_interpreter': sys.executable, 'supervisor_interpreter': interpreter,
              'mode': 'detached_breakaway' if os.name == 'nt' else 'new_session',
              'builder_model': None, 'builder_reasoning': None}
    try:
        with (launch_dir / 'stdout.log').open('x', encoding='utf-8') as stdout, (launch_dir / 'stderr.log').open('x', encoding='utf-8') as stderr:
            proc = subprocess.Popen(argv, cwd=root, stdin=subprocess.DEVNULL, stdout=stdout,
                                    stderr=stderr, close_fds=True, **options)
        record.update(pid=proc.pid, state='launched')
    except OSError as exc:
        record.update(state='launch_failed', error=str(exc))
        dump(launch_dir / 'launch.json', record)
        raise
    dump(launch_dir / 'launch.json', record)
    return {'launch_directory': str(launch_dir), **record}


def run_check(argv, root, log_path, deadline, env=None):
    timeout = remaining(deadline)
    with log_path.open('w', encoding='utf-8') as log:
        proc = subprocess.Popen(argv, cwd=root, stdout=log, stderr=subprocess.STDOUT, env=env,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        try:
            return proc.wait(timeout=timeout)
        finally:
            if proc.poll() is None:
                stop_process(proc)


def launch(cli, root, session, text, timeout, env=None):
    dump(session / 'response-schema.json', SCHEMA)
    config_path = session / 'runtime-configuration.json'
    config = {'status': 'pending', 'model': None, 'reasoning': None,
              'requested_model': MODEL, 'requested_reasoning': REASONING,
              'basis': 'Waiting for observed local CLI startup header; flags alone are insufficient.'}
    dump(config_path, config)
    argv = command(cli, root, session)
    dump(session / 'invocation.json', {'argv': argv, 'started_utc': utc()})
    (session / 'prompt.txt').write_text(text, encoding='utf-8')
    header, errors = [], []
    denied_signal = threading.Event()
    started = time.monotonic()
    denial = session / 'context-denied.json'
    guard_path = session / 'context-guard.json'
    guard_sha256 = w.digest(guard_path) if guard_path.exists() else None
    if denial.exists():
        raise ValueError('Session already has a context denial; only a fresh session may run')
    with (session / 'stdout.log').open('w', encoding='utf-8') as stdout:
        proc = subprocess.Popen(argv, cwd=root, stdin=subprocess.PIPE, stdout=stdout,
                                stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace',
                                env=env,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        process_state = {'supervisor_pid': os.getpid(), 'pid': proc.pid, 'started_utc': utc(),
                         'state': 'running', 'argv': argv, 'heartbeat_utc': utc()}
        dump(session / 'process.json', process_state)
        heartbeat_at = time.monotonic() + 5
        def consume():
            try:
                collecting = True
                with (session / 'stderr.log').open('w', encoding='utf-8') as log:
                    for line in proc.stderr:
                        log.write(line); log.flush()
                        if line.startswith(context_guard.DENIAL_SIGNAL):
                            denied_signal.set()
                        if collecting:
                            if len(header) >= 100 or line.strip() == 'user':
                                collecting = False
                                observed = parse_startup(header)
                                confirmed = (observed.get('model') == MODEL and
                                             observed.get('reasoning') == REASONING and
                                             bool(observed.get('session_id')))
                                config.update(observed)
                                config.update(status='confirmed' if confirmed else 'unconfirmed',
                                              observed_utc=utc(), startup_header=header,
                                              basis='Observed CLI startup metadata, not requested flags.')
                                dump(config_path, config)
                            else:
                                header.append(line.rstrip('\n'))
            except Exception as exc:
                errors.append(str(exc))
        reader = threading.Thread(target=consume, daemon=True)
        reader.start()
        def feed():
            try:
                proc.stdin.write(text)
                proc.stdin.close()
            except (OSError, ValueError) as exc:
                errors.append(f'Prompt feed failed: {exc}')
        writer = threading.Thread(target=feed, daemon=True)
        writer.start()
        try:
            while proc.poll() is None:
                if time.monotonic() >= heartbeat_at:
                    process_state.update(heartbeat_utc=utc())
                    dump(session / 'process.json', process_state)
                    heartbeat_at = time.monotonic() + 5
                if denial.exists() or denied_signal.is_set():
                    raise ValueError('Context helper denied a request; session stopped before fallback: ' +
                                     denial.relative_to(root).as_posix())
                if guard_sha256 and (not guard_path.exists() or w.digest(guard_path) != guard_sha256):
                    raise ValueError('Session context guard changed; session stopped')
                if errors or config['status'] == 'unconfirmed':
                    raise ValueError('CLI configuration could not be independently confirmed')
                if config['status'] == 'pending' and time.monotonic() - started > 40:
                    raise ValueError('No trusted CLI startup configuration within 40 seconds')
                if time.monotonic() - started > timeout:
                    raise ValueError('Session wall-time budget exhausted; preserve checkpoint for triage')
                time.sleep(0.1)
        finally:
            try:
                stop_process(proc)
            finally:
                reader.join(timeout=10)
                writer.join(timeout=1)
                process_state.update(state='exited', exit_code=proc.returncode, ended_utc=utc())
                dump(session / 'process.json', process_state)
                dump(session / 'process-result.json', {'exit_code': proc.returncode,
                     'ended_utc': utc(), 'wall_seconds': time.monotonic() - started,
                     'input_tokens': None, 'output_tokens': None, 'cost': None,
                     'unknown_reason': 'No trusted detailed usage or monetary billing exposed by this CLI adapter.'})
        if denial.exists() or denied_signal.is_set():
            raise ValueError('Context helper denied a request; no session result is accepted: ' +
                             denial.relative_to(root).as_posix())
        if errors or config['status'] != 'confirmed' or proc.returncode != 0:
            raise ValueError(f'Codex session failed or configuration unconfirmed (exit {proc.returncode})')
        if w.read_json(config_path) != config:
            raise ValueError('Session modified its supervisor-owned runtime configuration')
    result = w.read_json(session / 'response.json')
    if result.get('outcome') not in SCHEMA['properties']['outcome']['enum'] or not isinstance(result.get('summary'), str):
        raise ValueError('Invalid structured session response')
    return result


def apply_transition(root, task_id, target, evidence, deadline=None):
    result = subprocess.run([sys.executable, str(root / 'scripts/workflow.py'), 'transition',
                             '--task', task_id, '--to', target, '--evidence', evidence],
                            cwd=root, capture_output=True, text=True, encoding='utf-8', errors='replace',
                            timeout=remaining(deadline) if deadline is not None else 60)
    if result.returncode:
        raise ValueError(result.stderr.strip() or result.stdout.strip())


def finding_repair_budget(root, task, review):
    """Count immutable review requests per stable finding, across supervisor restarts."""
    def ids(body):
        findings = body.get('findings')
        if not isinstance(findings, list) or not findings:
            raise ValueError('Changes requested without actionable findings')
        values = [f.get('id') if isinstance(f, dict) else None for f in findings]
        if (any(not isinstance(value, str) or not value.strip() for value in values) or
                len(values) != len(set(values))):
            raise ValueError('Review findings need unique nonempty stable IDs')
        return values
    current = ids(review)
    counts = {}
    for event in task['events']:
        if event['to'] != 'changes_requested':
            continue
        path = w.safe_path(root, event['evidence'])
        if w.digest(path) != event['sha256']:
            raise ValueError('Prior finding review changed; repair budget cannot be reset')
        for id in ids(w.read_json(path)):
            counts[id] = counts.get(id, 0) + 1
    return {'limit_per_finding': 2, 'prior_requests': counts, 'current_findings': current,
            'exhausted': [id for id in current if counts.get(id, 0) >= 2]}


def finish_review(root, task, result, session, deadline=None, validation_session=None):
    deadline = deadline if deadline is not None else time.monotonic() + 3600
    rel = result.get('evidence')
    if not isinstance(rel, str) or not rel.startswith(f'private/workflow/runs/{task["id"]}/'):
        raise ValueError('Review evidence must be a new task run artifact')
    review = w.read_json(w.safe_path(root, rel))
    configuration_binding(root, session, review)
    _, delivery = latest_delivery(root, task)
    original = validation_repair_baseline(root, task)
    if original is not None:
        verify_preserved_delivery(root, original, delivery)
    if (review.get('role') != 'reviewer' or review.get('actor') == delivery['actor'] or
            review.get('actor') != f'ig2:{session.name}:reviewer' or
            review.get('model') != MODEL or review.get('reasoning') != REASONING):
        raise ValueError('Independent reviewer identity/configuration mismatch')
    if review.get('artifacts') != delivery['artifacts'] or review.get('criteria') != task['acceptance']:
        raise ValueError('Review does not account for the exact entire delivery/criteria')
    if result['outcome'] == 'changes_requested':
        budget = finding_repair_budget(root, task, review)
        if budget['exhausted']:
            raise ValueError('Two repair cycles already used for findings ' +
                             ', '.join(budget['exhausted']) + '; coordinator decision required')
        apply_transition(root, task['id'], 'changes_requested', rel, deadline)
        return
    if result['outcome'] != 'pass':
        raise ValueError('Reviewer did not return pass or changes_requested')
    if task['semantic_acceptance_required']:
        # Human authenticity is not delegated to a model or JSON shape validator.
        raise ValueError('Human semantic decision requires owner verification before acceptance')
    logs = session
    if validation_session is not None:
        logs = validation_session
        rel_logs = logs.relative_to(root).as_posix()
        if not rel_logs.startswith(f'private/workflow/runs/{task["id"]}/'):
            raise ValueError('Validation recovery must belong to the selected task run')
        w.safe_path(root, rel_logs)
        logs.mkdir(parents=True, exist_ok=False)
    checks = []
    for name, argv in [('project', ['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', task['id']]),
                       ('diff', ['git', 'diff', '--check'])]:
        exit_code = run_check(argv, root, logs / f'{name}-check.log', deadline,
                              validation_environment(root, task))
        checks.append({'command': subprocess.list2cmdline(argv), 'exit_code': exit_code})
    dump(logs / 'supervisor-checks.json', checks)
    if any(c['exit_code'] != 0 for c in checks):
        raise ValueError('Supervisor validation failed; no acceptance recorded')
    verify_artifacts(root, delivery)
    apply_transition(root, task['id'], 'accepted', rel, deadline)
    done = copy.deepcopy(review)
    done.update(role='coordinator', actor=f'ig2-supervisor:{logs.name}', model=None, reasoning=None,
                configuration_evidence='Deterministic Python supervisor; no model configuration.',
                summary='Verified independent technical review, frozen hashes, criteria and supervisor checks.',
                checks=review['checks'] + checks)
    done.pop('configuration_sha256', None)
    done_path = logs / 'done.json'
    dump(done_path, done)
    # workflow requires task run evidence, while session logs belong to the supervisor.
    target = root / 'private/workflow/runs' / task['id'] / ('closure-' + logs.name) / 'done.json'
    if target.exists():
        raise ValueError('Closure output already exists')
    dump(target, done)
    apply_transition(root, task['id'], 'done', target.relative_to(root).as_posix(), deadline)


def run(root, cli, run_dir, max_sessions, session_seconds, total_seconds):
    lock = w.safe_path(root, 'private/workflow/ig2-orchestrator.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, json.dumps({'pid': os.getpid(), 'run': str(run_dir), 'started_utc': utc()}).encode())
    started = time.monotonic()
    deadline = started + total_seconds
    status = {'format': 'wgc-ig2-supervisor-1', 'started_utc': utc(), 'sessions': 0,
              'state': 'starting', 'run': str(run_dir), 'cost': None, 'tokens': None,
              'builder_actual_model': None, 'builder_actual_reasoning': None,
              'builder_configuration_evidence': 'Not exposed in this builder session.',
              'max_sessions': max_sessions, 'session_seconds': session_seconds, 'total_seconds': total_seconds}
    preparation_retries = {}
    try:
        while True:
            q = w.read_json(root / w.QUEUE)
            w.validate(q, root)
            task, role = select(q)
            if role == 'complete':
                status.update(state='complete', summary='All current IG-2 tasks, including partition children, are done.')
                break
            if status['sessions'] >= max_sessions or time.monotonic() - started >= total_seconds:
                status.update(state='budget_stop', summary='Launch budget exhausted; no next model started.')
                break
            session = run_dir / f'{status["sessions"] + 1:03d}-{task["id"]}-{role}-{uuid.uuid4().hex[:8]}'
            session.mkdir(parents=True, exist_ok=False)
            before = w.digest(root / w.QUEUE)
            untouched = outside_stage(q)
            frozen_targets = None
            if task['id'] == 'IG-2D' and role == 'coordinator' and task['kind'] == 'refine':
                frozen_targets, reference = accepted_universe(root, q, task)
                dump(session / 'partition-universe-reference.json', reference)
            status.update(state='preparing', task=task['id'], role=role, session=str(session),
                          preparation_utc=utc())
            dump(run_dir / 'status.json', status)
            try:
                prepare(root, q, task, role, session)
                environment = launch_environment(root, task, session, cli)
            except PermissionError as error:
                # Explicit operator authorization covers bounded recovery of
                # transient Windows file locks before any model/claim starts.
                # Source/context refusals, hash changes and ownership changes
                # never enter this retry path.
                winerror = getattr(error, 'winerror', None)
                key = (task['id'], role, winerror)
                count = preparation_retries.get(key, 0)
                if (winerror not in {5, 32, 33} or count >= 2 or
                        w.digest(root / w.QUEUE) != before or (session / 'process.json').exists()):
                    raise
                preparation_retries[key] = count + 1
                dump(session / 'preparation-retry.json', {
                    'role': 'coordinator', 'actor': 'ig2-supervisor', 'model': None, 'reasoning': None,
                    'configuration_evidence': 'Deterministic pre-model recovery; no model launched.',
                    'task': task['id'], 'utc': utc(), 'winerror': winerror, 'retry': count + 1,
                    'queue_sha256': before, 'old_preparation_preserved': True,
                    'summary': 'Transient Windows preparation I/O failed; retry in a fresh dispatch directory with unchanged source scope and queue.'})
                status.update(state='retrying', summary='Retrying transient pre-model Windows I/O in a fresh dispatch.')
                dump(run_dir / 'status.json', status)
                time.sleep(0.1 * (count + 1))
                continue
            preserved = (w.read_json(session / 'preserved-artifacts.json')
                         if (session / 'preserved-artifacts.json').is_file() else None)
            continuation = (w.read_json(session / 'continuation-preserved.json')
                            if (session / 'continuation-preserved.json').is_file() else None)
            context_recovery = (w.read_json(session / 'context-recovery-preserved.json')
                                if (session / 'context-recovery-preserved.json').is_file() else None)
            if w.digest(root / w.QUEUE) != before:
                raise ValueError('Queue changed during dispatch; refresh before launching')
            status.update(state='running', task=task['id'], role=role, session=str(session),
                          sessions=status['sessions'] + 1)
            dump(run_dir / 'status.json', status)
            print(f'{utc()} {task["id"]} {role} session={status["sessions"]}', flush=True)
            try:
                result = launch(cli, root, session, prompt(root, task, role, session),
                                min(session_seconds, max(1, total_seconds - (time.monotonic() - started))),
                                environment)
            finally:
                if continuation is not None:
                    verify_artifacts(root, {'artifacts': continuation})
                if context_recovery is not None:
                    verify_artifacts(root, {'artifacts': context_recovery})
                if preserved is not None:
                    verify_preserved_delivery(root, preserved)
            after = w.read_json(root / w.QUEUE)
            w.validate(after, root)
            if outside_stage(after) != untouched:
                raise ValueError('Out-of-stage queue changed; preserve work and triage')
            check_queue_delta(q, after, task, role, frozen_targets, result['outcome'])
            current = next(t for t in after['tasks'] if t['id'] == task['id'])
            if preserved is not None:
                if current['status'] == 'review':
                    _, new_delivery = latest_delivery(root, current)
                    verify_preserved_delivery(root, preserved, new_delivery)
            if role != 'reviewer':
                for event in current['events'][len(task['events']):]:
                    e = w.read_json(w.safe_path(root, event['evidence']))
                    configuration_binding(root, session, e)
                    if e['actor'] != f'ig2:{session.name}:{role}':
                        raise ValueError('Transition actor is not the dispatched session')
            if result['outcome'] == 'blocked':
                status.update(state='blocked', summary=result['summary'], evidence=result.get('evidence'))
                break
            if role == 'reviewer':
                if w.digest(root / w.QUEUE) != before:
                    raise ValueError('Reviewer modified the authoritative queue')
                finish_review(root, task, result, session, deadline)
            else:
                if role == 'executor' and current['status'] != 'review':
                    raise ValueError('Executor did not freeze delivery and enter review')
                if role == 'coordinator' and w.digest(root / w.QUEUE) == before:
                    raise ValueError('Refinement made no queue progress; no unchanged retry')
                if not isinstance(result.get('evidence'), str):
                    raise ValueError('Role returned progress without immutable evidence')
                e = w.read_json(w.safe_path(root, result['evidence']))
                configuration_binding(root, session, e)
                if e.get('actor') != f'ig2:{session.name}:{role}':
                    raise ValueError('Progress evidence actor does not match this session')
                if role == 'coordinator' and task['status'] == 'changes_requested':
                    verify_repair_authorization(root, current)
            status.update(summary=result['summary'])
    except (OSError, ValueError, KeyError, StopIteration, subprocess.SubprocessError) as error:
        status.update(state='blocked', summary=str(error))
    except KeyboardInterrupt:
        status.update(state='interrupted', summary='Operator interruption; reconcile task checkpoint before resume.')
    except Exception as error:
        status.update(state='blocked', summary=f'Unexpected {type(error).__name__}: {error}')
        raise  # Preserve the traceback as well as a truthful final status.
    finally:
        status.update(ended_utc=utc(), wall_seconds=time.monotonic() - started)
        dump(run_dir / 'status.json', status)
        os.close(fd)
        lock.unlink()
    print(json.dumps(status, ensure_ascii=False, indent=2), flush=True)
    return 0 if status['state'] == 'complete' else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['plan', 'run', 'start'])
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--host-runtime', default=os.environ.get('WGC_HOST_RUNTIME'))
    parser.add_argument('--max-sessions', type=int, default=48)
    parser.add_argument('--session-seconds', type=int, default=3600)
    parser.add_argument('--total-seconds', type=int, default=28800)
    args = parser.parse_args()
    if min(args.max_sessions, args.session_seconds, args.total_seconds) < 1:
        parser.error('Budgets must be positive')
    root = w.ROOT
    host = host_runtime.bind(root, args.host_runtime) if args.host_runtime else host_runtime.bound(root)
    if host is not None:
        if args.codex != 'codex' and str(Path(shutil.which(args.codex) or args.codex).resolve()) != host['tools']['codex']['path']:
            raise ValueError('Codex override differs from the bound host runtime')
        args.codex = host['tools']['codex']['path']
    q = w.read_json(root / w.QUEUE)
    w.validate(q, root)
    task, role = select(q)
    if args.mode == 'plan':
        print(json.dumps({'stage': STAGE, 'next_task': task['id'] if task else None,
                          'next_role': role, 'queue_sha256': w.digest(root / w.QUEUE),
                          'done': sum(t['status'] == 'done' for t in stage_tasks(q)),
                          'total': len(stage_tasks(q)), 'models_launched': 0,
                          'max_sessions': args.max_sessions, 'session_seconds': args.session_seconds,
                          'total_seconds': args.total_seconds, 'requested_model': MODEL,
                          'requested_reasoning': REASONING, 'actual_model': None,
                          'actual_reasoning': None, 'monetary_cost': None}, indent=2))
        return 0
    cli = shutil.which(args.codex)
    if not cli:
        raise ValueError('Codex CLI not found; no installation or global configuration attempted')
    if args.mode == 'start':
        print(json.dumps(start_background(root, cli, args.max_sessions, args.session_seconds,
                                          args.total_seconds), indent=2))
        return 0
    rel = 'private/workflow/orchestrator/' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex[:8]
    run_dir = w.safe_path(root, rel)
    run_dir.mkdir(parents=True, exist_ok=False)
    print(f'RUN_ROOT={run_dir}', flush=True)
    return run(root, cli, run_dir, args.max_sessions, args.session_seconds, args.total_seconds)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, StopIteration) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
