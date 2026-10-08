"""Restore an original-byte snapshot into a new directory, without touching Git."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def safe_relative(value: str) -> Path:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value:
        raise ValueError(f'Unsafe manifest path: {value!r}')
    if path.parts[0] == '.git':
        raise ValueError('Snapshot must not contain Git internals')
    return Path(*path.parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    source = args.snapshot.resolve(strict=True)
    destination = args.destination.resolve()
    if destination.exists() or destination.is_relative_to(source):
        raise ValueError('Destination must be new and outside the snapshot')
    # Do not traverse junctions/symlinks in an existing destination ancestor.
    for parent in [args.destination.absolute(), *args.destination.absolute().parents]:
        if parent.exists() and (parent.is_symlink() or getattr(parent.lstat(), 'st_file_attributes', 0) & 1024):
            raise ValueError(f'Reparse destination ancestor: {parent}')
    manifest_path = source / 'manifest.json'
    expected = (source / 'manifest.sha256').read_text(encoding='ascii').split()[0]
    if digest(manifest_path) != expected:
        raise ValueError('Manifest hash mismatch')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest['format'] != 'pre-poc-snapshot@1':
        raise ValueError('Unsupported manifest version')
    original_root = Path(manifest['root']).resolve()
    if destination.is_relative_to(original_root) and not destination.is_relative_to(original_root / 'private/archive'):
        raise ValueError('Inside the active repository, restore only under private/archive')
    payload = source / 'payload'
    paths = [safe_relative(row['path']) for row in manifest['files']]
    if len({str(path).casefold() for path in paths}) != len(paths):
        raise ValueError('Duplicate manifest paths')
    for row, rel in zip(manifest['files'], paths):
        path = payload / rel
        if not path.resolve(strict=True).is_relative_to(payload.resolve()):
            raise ValueError(f'Payload path escapes snapshot: {rel}')
        if path.stat().st_size != row['size'] or digest(path) != row['sha256']:
            raise ValueError(f'Snapshot mismatch: {rel}')
    directories = [safe_relative(value) for value in manifest['directories']]
    destination.mkdir(parents=True, exist_ok=False)
    for rel in directories:
        (destination / rel).mkdir(parents=True, exist_ok=True)
    for row, rel in zip(manifest['files'], paths):
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        with (payload / rel).open('rb') as incoming, target.open('xb') as outgoing:
            shutil.copyfileobj(incoming, outgoing)
        if target.stat().st_size != row['size'] or digest(target) != row['sha256']:
            raise ValueError(f'Restore mismatch (partial destination retained): {rel}')
    print(json.dumps({'restored_files': len(paths), 'verified_files': len(paths),
                      'bytes': sum(row['size'] for row in manifest['files']),
                      'destination': str(destination), 'mismatches': []}, indent=2))


if __name__ == '__main__':
    main()
