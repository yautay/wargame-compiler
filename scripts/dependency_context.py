"""Bounded, hash-pinned dependency projections. Never release event histories or manifests."""
from __future__ import annotations

import argparse
import copy
import os
from pathlib import Path
import re
import sys

import workflow as w
import context_guard as guard

FORMAT = 'wgc-dependency-view-1'
SECTIONS = ('summary', 'outputs', 'inventory', 'boundary', 'toolchain')
MAX_BYTES = 24000


def checked(root, pin):
    p = w.safe_path(root, pin['path'])
    if w.denied(pin['path']) or not p.is_file() or w.digest(p) != pin['sha256']:
        raise ValueError('Dependency artifact changed or is forbidden: ' + pin['path'])
    return p


def bounded(value):
    if len(guard.json_text(value).encode('ascii')) + 1 > MAX_BYTES:
        raise ValueError('Dependency projection exceeds its byte ceiling; refine the fields, never dump or truncate')
    return value


def event_pin(event):
    return {'path': event['evidence'], 'sha256': event['sha256']}


def pin_fields(pin):
    value = {k: pin[k] for k in ('path', 'sha256')}
    if 'bytes' in pin:
        if type(pin['bytes']) is not int or pin['bytes'] < 0:
            raise ValueError('Invalid dependency artifact byte count')
        value['bytes'] = pin['bytes']
    return value


def assigned_pages(task):
    if not re.fullmatch(r'IG-2B\d{2}', task['id']):
        return []
    explicit = task.get('dependency_scope', {}).get('physical_pages')
    numbers = [int(x) for x in re.findall(r'\d+', task.get('title', ''))]
    if len(numbers) != 2 or numbers[1] - numbers[0] != 3:
        raise ValueError('Inventory dependency projection requires an exact four-page task title')
    pages = list(range(numbers[0], numbers[1] + 1))
    if explicit is not None and explicit != pages:
        raise ValueError('Dependency page scope conflicts with the selected task')
    return pages


def choose(artifacts, outputs, name, suffix=None):
    matches = [p for p in artifacts if Path(p['path']).name == name]
    declared = [p for p in matches if p['path'] in outputs]
    candidates = declared or [p for p in matches if suffix is None or p['path'].endswith(suffix)]
    if len(candidates) != 1:
        raise ValueError('Ambiguous or missing accepted dependency artifact: ' + name)
    return pin_fields(candidates[0])


def exit_boundary(cont, expected_page):
    boundary = cont.get('assigned_range_exit', {})
    if not boundary:
        return {}
    # Accepted reports use either spelling for the physical PDF page ordinal.
    # Normalize only this explicit exit; never infer it from retained reports.
    ordinals = [boundary[k] for k in ('physical_page', 'pdf_page') if k in boundary]
    if not ordinals or any(type(n) is not int or n != expected_page for n in ordinals):
        raise ValueError('Dependency exit is not the assigned range boundary')
    result = {'physical_page': expected_page}
    if 'observation' in boundary:
        result['observation'] = boundary['observation']
    return result


def native_toolchain(native):
    """Normalize accepted version strings and structured executable records."""
    if not isinstance(native, dict):
        raise ValueError('Native toolchain must be an object')
    result = {}
    for name, value in native.items():
        if name not in {'pdfinfo', 'pdftoppm', 'pdftotext', 'pwsh', 'git'}:
            continue
        if isinstance(value, str):
            value = {'version': value}
        if not isinstance(value, dict):
            raise ValueError('Invalid native toolchain record: ' + name)
        record = {}
        if 'version' in value:
            if not isinstance(value['version'], str):
                raise ValueError('Invalid native toolchain version: ' + name)
            record['version'] = value['version']
        if 'executable' in value:
            executable = value['executable']
            if not isinstance(executable, dict) or not {'path', 'sha256'} <= executable.keys():
                raise ValueError('Invalid native toolchain executable: ' + name)
            record['executable'] = pin_fields(executable)
        result[name] = record
    return result


def inventory_projection(root, dep, artifacts, pages):
    local = [p for p in artifacts if p['path'].startswith(f'private/workflow/runs/{dep["id"]}/')]
    inv = choose(local, dep['outputs'], 'inventory.json', '/final-verified/inventory.json')
    doc = w.read_json(checked(root, inv))
    if doc.get('format') != 'wgc-inventory-1' or not all(1 <= n <= doc['source']['page_count'] for n in pages):
        raise ValueError('Wrong inventory format or assigned page range')
    folder = Path(inv['path']).parent.as_posix() + '/'
    registry = [p for p in artifacts if p['path'] == folder + 'identity-registry.json']
    if len(registry) != 1:
        raise ValueError('Accepted inventory has no unique companion registry')
    checked(root, registry[0])
    reports = {}
    attempt = Path(inv['path']).parent.parent.as_posix() + '/'
    for name in ['region-ledger.json', 'continuations.json', 'coverage-report.json', 'source-pins.json', 'toolchain.json']:
        # Original source reports live with this accepted inventory. A declared
        # repaired report supersedes that exact report; ancestor/preparation pins do not.
        candidates = [p for p in local if p['path'] in dep['outputs'] or p['path'] == attempt + name]
        reports[name] = choose(candidates, dep['outputs'], name)
        checked(root, reports[name])
    selected = [p for p in doc['pages'] if p['pdf_page'] in pages]
    if sorted(p['pdf_page'] for p in selected) != pages:
        raise ValueError('Assigned page metadata is missing or duplicated')
    ids = {p['id'] for p in selected}
    page_fields = ('id', 'key', 'revision', 'pdf_page', 'source_revision', 'media_box',
                   'crop_box', 'effective_crop_box', 'rotation', 'user_unit')
    region_fields = ('id', 'key', 'revision', 'page_id', 'source_revision', 'kind', 'box', 'denominator_role')
    source = {k: copy.deepcopy(doc['source'][k]) for k in ('id', 'sha256', 'page_count')}
    source.update({k: pin_fields(doc['source'][k]) for k in ('pdf', 'provenance')})
    for k in ['pdf', 'provenance']:
        checked(root, source[k])
    inventory = {'baseline_inventory': inv, 'identity_registry': pin_fields(registry[0]), 'source': source,
                 'reports': reports, 'assigned_physical_pages': pages,
                 'assigned_page_metadata': [{k: p[k] for k in page_fields if k in p} for p in selected],
                 'assigned_region_metadata': [{k: r[k] for k in region_fields if k in r}
                                              for r in doc['regions'] if r['page_id'] in ids],
                 'counts': {k: len(doc[k]) for k in ('pages', 'regions', 'evidence', 'links')}}
    cont = w.read_json(checked(root, reports['continuations.json']))
    # Only the prior range's explicit exit observation; no references or source text elsewhere.
    boundary = exit_boundary(cont, pages[0] - 1)
    tool = w.read_json(checked(root, reports['toolchain.json']))
    toolchain = {k: tool[k] for k in ('process_pythonpath', 'process_path_prefix', 'libraries') if k in tool}
    if 'python_executable' in tool:
        toolchain['python_executable'] = pin_fields(tool['python_executable'])
    toolchain['native'] = native_toolchain(tool.get('native', {}))
    return bounded(inventory), bounded(boundary), bounded(toolchain)


def build(root, q, task):
    result = {'format': FORMAT, 'task': task['id'], 'dependencies': {}}
    pages = assigned_pages(task)
    by_id = {t['id']: t for t in q['tasks']}
    for id in task['depends']:
        dep = by_id[id]
        if dep['status'] != 'done':
            raise ValueError('Dependency must be done before projection: ' + id)
        done = event_pin(dep['events'][-1])
        accepted = event_pin(next(e for e in reversed(dep['events']) if e['to'] == 'accepted'))
        body = w.read_json(checked(root, done))
        checked(root, accepted)
        artifacts = body['artifacts']
        outputs = [pin_fields(p) for p in artifacts if p['path'] in dep['outputs']]
        view = {'summary': {'id': id, 'status': 'done', 'done': done, 'accepted': accepted,
                            'artifact_count': len(artifacts)}, 'outputs': outputs,
                'inventory': {}, 'boundary': {}, 'toolchain': {}}
        if pages:
            view['inventory'], view['boundary'], view['toolchain'] = inventory_projection(root, dep, artifacts, pages)
        result['dependencies'][id] = view
    return bounded(result)


@guard.protect('dependency_context')
def read_view(root, manifest, sha256, task, dependency, section):
    if not manifest or not sha256 or not task or section not in SECTIONS:
        raise ValueError('Task, pinned dependency view and a supported section are required; no fallback')
    body = w.read_json(checked(root, {'path': manifest, 'sha256': sha256}))
    if body.get('format') != FORMAT or body.get('task') != task:
        raise ValueError('Dependency view belongs to another task or format')
    if dependency not in body['dependencies']:
        raise ValueError('Dependency is not in this selected task packet')
    view = body['dependencies'][dependency]
    q = w.read_json(root / w.QUEUE)
    dep = next(t for t in q['tasks'] if t['id'] == dependency)
    if dep['status'] != 'done' or event_pin(dep['events'][-1]) != view['summary']['done']:
        raise ValueError('Live dependency authority changed; prepare a new packet')
    checked(root, view['summary']['done'])
    return bounded({'task': task, 'dependency': dependency, 'section': section, 'data': view[section]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task', default=os.environ.get('WGC_TASK_ID'))
    parser.add_argument('--manifest', default=os.environ.get('WGC_TASK_DEPENDENCY_VIEW'))
    parser.add_argument('--sha256', default=os.environ.get('WGC_TASK_DEPENDENCY_SHA256'))
    parser.add_argument('--dependency', required=True)
    parser.add_argument('--section', choices=SECTIONS, default='summary')
    args = parser.parse_args()
    for key, value in [('WGC_TASK_ID', args.task), ('WGC_TASK_DEPENDENCY_VIEW', args.manifest),
                       ('WGC_TASK_DEPENDENCY_SHA256', args.sha256)]:
        if os.environ.get(key) and os.environ[key] != value:
            raise ValueError('Dependency override differs from the session binding')
    print(guard.json_text(read_view(w.ROOT, args.manifest, args.sha256, args.task, args.dependency, args.section)))


if __name__ == '__main__':
    guard.cli(w.ROOT, 'dependency_context', main)
