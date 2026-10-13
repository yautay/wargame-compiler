"""Freeze explicitly enumerated WGU bytes and source registry files offline.

Snapshots are append-only and content addressed. Every reuse verifies disk bytes;
this is application immutability, not an OS guarantee against operator edits.
No YAML, publisher text, source semantics or gameplay is interpreted.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import uuid

from wgc.contracts.source import (
    ContractError, _check_schema, _no_float, _pairs, _shape, canonical_bytes, load_json,
)

SCHEMA_PATH = Path(__file__).resolve().parents[3] / 'contracts/ig/input.schema.json'


class SnapshotError(ValueError):
    """Unsafe scope, unavailable required bytes, mutation or corrupt snapshot."""


def canonical(value):
    return canonical_bytes(value)


def relative_path(value):
    """Reject traversal, ADS, Windows aliases and all noncanonical path spellings."""
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise SnapshotError('unsafe relative path')
    parts = value.split('/')
    reserved = {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)),
                *(f'LPT{i}' for i in range(1, 10))}
    for part in parts:
        if (part in {'', '.', '..'} or part[-1:] in {' ', '.'}
                or any(ord(c) < 32 or c in '<>"|?*' for c in part)
                or part.split('.')[0].upper() in reserved):
            raise SnapshotError('unsafe relative path')
    return value


def no_links(path):
    """Inspect every existing ancestor; junctions are reparse points on Windows."""
    for part in [*reversed(path.parents), path]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            return
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 1024:
            raise SnapshotError('linked path: ' + str(part))


def root_path(value):
    path = Path(value)
    if not path.is_absolute() or '..' in path.parts:
        raise SnapshotError('roots must be explicit absolute paths without traversal')
    no_links(path)
    if not path.is_dir():
        raise SnapshotError('input root is not an existing directory')
    return path


def signature(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


@contextmanager
def open_read(path):
    """Open read-only and refuse links before consuming any content bytes.

    Windows checks the actual opened handle path, refuses reparse handles and
    shares only reads. POSIX walks directory descriptors using O_NOFOLLOW.
    """
    path = path.absolute()
    no_links(path)
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes
        import msvcrt
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        create = kernel.CreateFileW
        create.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                           wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        create.restype = wintypes.HANDLE
        close = kernel.CloseHandle
        close.argtypes = [wintypes.HANDLE]
        close.restype = wintypes.BOOL
        handle = create(str(path), 0x80000000, 1, None, 3, 0x00200000, None)
        if handle == ctypes.c_void_p(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            class Attributes(ctypes.Structure):
                _fields_ = [('attributes', wintypes.DWORD), ('tag', wintypes.DWORD)]
            info = Attributes()
            get_info = kernel.GetFileInformationByHandleEx
            get_info.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
            get_info.restype = wintypes.BOOL
            if not get_info(handle, 9, ctypes.byref(info), ctypes.sizeof(info)):
                raise ctypes.WinError(ctypes.get_last_error())
            if info.attributes & (1024 | 16):
                raise SnapshotError('opened source is linked or not regular')
            get_path = kernel.GetFinalPathNameByHandleW
            get_path.argtypes = [wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD]
            get_path.restype = wintypes.DWORD
            buffer = ctypes.create_unicode_buffer(32768)
            length = get_path(handle, buffer, len(buffer), 0)
            if not length or length >= len(buffer):
                raise SnapshotError('cannot verify opened source path; WinError ' + str(ctypes.get_last_error()))
            actual = buffer.value
            if actual.startswith('\\\\?\\UNC\\'):
                actual = '\\\\' + actual[8:]
            elif actual.startswith('\\\\?\\'):
                actual = actual[4:]
            if actual.casefold() != str(path).casefold():
                raise SnapshotError('opened source escaped its exact enumerated path')
            descriptor = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
            handle = None  # descriptor now owns the handle
        finally:
            if handle is not None:
                close(handle)
    else:
        directory = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
        try:
            for component in path.parts[1:-1]:
                child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=directory)
                os.close(directory)
                directory = child
            descriptor = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        finally:
            os.close(directory)
    with os.fdopen(descriptor, 'rb') as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise SnapshotError('source is not a regular file')
        yield stream


def enumerate_game_files(root):
    """Inventory names only in wgu.yaml and kb/, without following linked paths."""
    root = root_path(root)
    no_links(root / 'wgu.yaml')
    no_links(root / 'kb')
    if not (root / 'kb').is_dir():
        raise SnapshotError('required kb directory unavailable')
    result = ['wgu.yaml']
    def error(caught):
        raise SnapshotError('cannot enumerate KB: ' + str(caught)) from caught
    for directory, dirs, files in os.walk(root / 'kb', followlinks=False, onerror=error):
        for name in dirs + files:
            path = Path(directory) / name
            no_links(path)
            relative_path(path.relative_to(root).as_posix())
        result.extend((Path(directory) / name).relative_to(root).as_posix() for name in files)
    return sorted(result)


def digest_stream(stream, destination=None):
    digest = hashlib.sha256()
    size = 0
    while chunk := stream.read(1024 * 1024):
        digest.update(chunk)
        size += len(chunk)
        if destination is not None:
            destination.write(chunk)
    return size, digest.hexdigest()


def measure(path, destination=None):
    with open_read(path) as source:
        before = os.fstat(source.fileno())
        size, digest = digest_stream(source, destination)
        after = os.fstat(source.fileno())
    no_links(path)
    # Windows fstat and pathname stat expose different creation/change-time
    # semantics. Compare ctime only within the same handle API, and compare
    # path identity/size/mtime separately. Full byte rehash also runs globally.
    if (signature(before) != signature(after)
            or signature(after)[:4] != signature(path.stat())[:4]):
        raise SnapshotError('input changed during copy: ' + str(path))
    return size, digest, (before.st_dev, before.st_ino)


def validate_plan(request):
    canonical(request)
    game = root_path(request['game_root'])
    registry = root_path(request['registry_root'])
    groups = [('game', request['game_files'], {'game_config', 'kb'}, True),
              ('game', request['historical_configured_sources'], {'configured_source'}, False),
              ('registry', request['registry_files'], {'provenance', 'selected_rulebook'}, True)]
    entries = []
    seen = set()
    for root, items, roles, required in groups:
        for item in items:
            name = relative_path(item['relative_path'])
            key = (root, name.casefold())
            if key in seen:
                raise SnapshotError('duplicate path/case alias')
            seen.add(key)
            if item['role'] not in roles:
                raise SnapshotError('unexpected file role')
            if required:
                if (type(item.get('bytes')) is not int or item['bytes'] < 0
                        or not isinstance(item.get('sha256'), str)
                        or len(item['sha256']) != 64
                        or any(c not in '0123456789abcdef' for c in item['sha256'])):
                    raise SnapshotError('required inputs need exact size/hash pins')
            if root == 'game' and required and not (name == 'wgu.yaml' or name.startswith('kb/')):
                raise SnapshotError('unintended game input outside wgu.yaml and kb/')
            entries.append((root, item, required))
    expected = sorted(i['relative_path'] for i in request['game_files'])
    if enumerate_game_files(game) != expected:
        raise SnapshotError('unintended or missing KB file outside explicit enumeration')
    selection = request['selection']
    schema = load_json(SCHEMA_PATH)
    _check_schema(schema, schema)
    if _shape(selection, schema['$defs']['selection'], schema, '$/selection'):
        raise SnapshotError('explicit new source pin must preserve unknown original identity and valid metadata')
    selected = [i for i in request['registry_files'] if i['relative_path'] == selection['selected_path']]
    if (len(selected) != 1 or selected[0]['role'] != 'selected_rulebook'
            or selection['sha256'] != selected[0]['sha256']
            or selection['identity_to_wgu_original'] != 'unknown'
            or selection['semantic_acceptance'] != 'not_granted'):
        raise SnapshotError('explicit new source pin must preserve unknown original identity')
    # Check ALL planned path chains before the first content read.
    for root, item, _ in entries:
        no_links((game if root == 'game' else registry) / item['relative_path'])
    return game, registry, entries


def snapshot_manifest(body):
    identifier = hashlib.sha256(canonical(body)).hexdigest()
    return {**body, 'snapshot_id': 'sha256:' + identifier}


def read_structured(path, require_canonical=False):
    with open_read(path) as stream:
        raw = stream.read()
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs,
                       parse_float=_no_float, parse_constant=_no_float)
    expected = canonical(value) + b'\n'
    if require_canonical and raw != expected:
        raise SnapshotError('snapshot metadata is not canonical UTF-8 JSON')
    return value


def _verify_snapshot(directory, enforce_directory_name=True):
    directory = Path(directory).absolute()
    no_links(directory)
    manifest = read_structured(directory / 'manifest.json', require_canonical=True)
    schema = load_json(SCHEMA_PATH)
    _check_schema(schema, schema)
    errors = _shape(manifest, schema, schema, '$')
    if errors:
        raise SnapshotError('input manifest schema: ' + '; '.join(errors[:5]))
    expected = snapshot_manifest({k: v for k, v in manifest.items() if k != 'snapshot_id'})
    if manifest != expected or (enforce_directory_name and directory.name != 'sha256-' + manifest['snapshot_id'][7:]):
        raise SnapshotError('snapshot manifest integrity mismatch')
    seen = set()
    for item in manifest['files']:
        name = relative_path(item['path'])
        if name.casefold() in seen:
            raise SnapshotError('duplicate path/case alias in snapshot')
        seen.add(name.casefold())
        if item['availability'] == 'missing':
            if any(item[k] is not None for k in ['bytes', 'sha256', 'blob_path']):
                raise SnapshotError('missing input falsely contains byte evidence')
            continue
        if item['blob_path'] != 'files/' + name:
            raise SnapshotError('copy path differs from exact enumerated path')
        path = directory / relative_path(item['blob_path'])
        size, digest, _ = measure(path)
        if size != item['bytes'] or digest != item['sha256']:
            raise SnapshotError('snapshot copy hash mismatch')
    if manifest['kind'] == 'source_snapshot':
        selection = manifest['selection']
        targets = [f for f in manifest['files'] if f['path'] == selection['selected_path']]
        if (len(targets) != 1 or targets[0]['availability'] != 'available'
                or targets[0]['role'] != 'selected_rulebook' or targets[0]['sha256'] != selection['sha256']):
            raise SnapshotError('selected source differs from snapshot bytes')
        pin = read_structured(directory / 'source-pin.json', require_canonical=True)
        if pin != {**manifest['selection'], 'source_snapshot_id': manifest['snapshot_id'],
                   'selection_purpose': 'new_ig_source'}:
            raise SnapshotError('source pin integrity mismatch')
    return manifest


def verify_snapshot(directory):
    """Check a published directory name, canonical metadata, file bytes and pin."""
    return _verify_snapshot(directory)


def publish(staging, parent, manifest, source_pin=False):
    target = parent / ('sha256-' + manifest['snapshot_id'][7:])
    no_links(target)
    if target.exists():
        if verify_snapshot(target) != manifest:
            raise SnapshotError('existing snapshot differs; never overwrite')
        # Only this invocation's fresh staging can be discarded. Check the
        # resolved absolute boundary before recursive removal on Windows.
        no_links(staging)
        for directory, dirs, files in os.walk(staging, followlinks=False):
            for name in dirs + files:
                no_links(Path(directory) / name)
        if (staging.resolve().parent != parent.resolve()
                or not staging.name.startswith('.pending-') or len(staging.name) != 41):
            raise SnapshotError('unsafe staging cleanup boundary')
        shutil.rmtree(staging)
        return target
    (staging / 'manifest.json').write_bytes(canonical(manifest) + b'\n')
    if source_pin:
        pin = {**manifest['selection'], 'source_snapshot_id': manifest['snapshot_id'],
               'selection_purpose': 'new_ig_source'}
        (staging / 'source-pin.json').write_bytes(canonical(pin) + b'\n')
    _verify_snapshot(staging, enforce_directory_name=False)
    try:
        staging.rename(target)
    except FileExistsError as error:
        raise SnapshotError('concurrent snapshot publication; no overwrite') from error
    verify_snapshot(target)
    return target


def freeze_inputs(request, input_parent, source_parent):
    """Freeze pinned bytes, then rehash all origins before publishing either set."""
    game, registry, entries = validate_plan(request)
    parents = [Path(input_parent).absolute(), Path(source_parent).absolute()]
    for parent in parents:
        no_links(parent)
        if '..' in parent.parts:
            raise SnapshotError('unsafe destination')
        for origin in [game, registry]:
            if parent.is_relative_to(origin) or origin.is_relative_to(parent):
                raise SnapshotError('destination overlaps read-only input root')
    if parents[0] == parents[1] or any(a.is_relative_to(b) for a, b in [(parents[0], parents[1]), (parents[1], parents[0])]):
        raise SnapshotError('snapshot destinations overlap')
    staging = []
    for parent in parents:
        parent.mkdir(parents=True, exist_ok=True)
        no_links(parent)
        pending = parent / ('.pending-' + uuid.uuid4().hex)
        pending.mkdir(exist_ok=False)
        staging.append(pending)
    manifests = [[], []]
    observed = []
    identities = set()
    for root, item, required in entries:
        index = 0 if root == 'game' else 1
        origin = (game if root == 'game' else registry) / item['relative_path']
        name = item['relative_path']
        record = {'path': name, 'role': item['role'], 'availability': 'missing',
                  'bytes': None, 'sha256': None, 'blob_path': None, 'edition_label': None}
        no_links(origin)
        try:
            origin.lstat()
        except FileNotFoundError:
            if required:
                raise SnapshotError('required input missing: ' + name)
            if item.get('availability', 'missing') != 'missing':
                raise SnapshotError('configured source availability changed')
            observed.append((origin, None))
        else:
            if item.get('availability', 'available') != 'available':
                raise SnapshotError('configured source availability changed')
            destination = staging[index] / 'files' / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open('xb') as output:
                size, digest, identity = measure(origin, output)
            if identity in identities:
                raise SnapshotError('duplicate physical input alias')
            identities.add(identity)
            if required and (size != item['bytes'] or digest != item['sha256']):
                raise SnapshotError('input revision changed from pinned request: ' + name)
            copied_size, copied_digest, _ = measure(destination)
            if (copied_size, copied_digest) != (size, digest):
                raise SnapshotError('independent copy hash mismatch')
            record.update(availability='available', bytes=size, sha256=digest,
                          blob_path='files/' + name)
            if item['role'] == 'selected_rulebook':
                record['edition_label'] = request['selection']['edition_label']
            observed.append((origin, (size, digest)))
        manifests[index].append(record)
    if enumerate_game_files(game) != sorted(i['relative_path'] for i in request['game_files']):
        raise SnapshotError('KB enumeration changed during snapshot')
    for origin, expected in observed:
        no_links(origin)
        if expected is None:
            if origin.exists():
                raise SnapshotError('missing source appeared during snapshot')
        else:
            size, digest, _ = measure(origin)
            if (size, digest) != expected:
                raise SnapshotError('input changed during snapshot: ' + str(origin))
    source_manifest = snapshot_manifest({'schema_version': 'wgc-input-1', 'kind': 'source_snapshot',
                                        'origin_root': str(registry), 'files': sorted(manifests[1], key=lambda f: f['path']),
                                        'selection': request['selection']})
    source_dir = publish(staging[1], parents[1], source_manifest, source_pin=True)
    input_manifest = snapshot_manifest({'schema_version': 'wgc-input-1', 'kind': 'input_snapshot',
                                       'origin_root': str(game), 'files': sorted(manifests[0], key=lambda f: f['path']),
                                       'source_snapshot_id': source_manifest['snapshot_id']})
    input_dir = publish(staging[0], parents[0], input_manifest)
    return {'input_snapshot': str(input_dir), 'source_snapshot': str(source_dir),
            'input_snapshot_id': input_manifest['snapshot_id'], 'source_snapshot_id': source_manifest['snapshot_id'],
            'game_files_available': sum(f['availability'] == 'available' and f['role'] != 'configured_source' for f in manifests[0]),
            'configured_sources_missing': sum(f['availability'] == 'missing' and f['role'] == 'configured_source' for f in manifests[0]),
            'semantic_acceptance_granted': False, 'executable_readiness_granted': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('request', type=Path)
    parser.add_argument('--inputs', required=True, type=Path)
    parser.add_argument('--sources', required=True, type=Path)
    args = parser.parse_args()
    try:
        # The request is an operator-supplied local plan, never a source path to infer.
        request = read_structured(args.request)
        result = freeze_inputs(request, args.inputs, args.sources)
    except (SnapshotError, ContractError, OSError, ValueError, KeyError, TypeError) as error:
        print('Snapshot rejected: ' + str(error))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
