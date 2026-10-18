"""Explicit process-local runtime rebinding; frozen task toolchains stay unchanged."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import workflow as w

FORMAT = 'wgc-host-runtime-1'
REQUIREMENTS = 'docs/work/ig2-runtime-requirements.txt'
TOOLS = {'codex': ['--version'], 'rg': ['--version'], 'pwsh': ['--version'],
         'pdfinfo': ['-v'], 'pdftoppm': ['-v']}
NATIVE_VERSIONS = {'pdfinfo': 'pdfinfo version 26.07.0', 'pdftoppm': 'pdftoppm version 26.07.0'}
PROBE = """
import importlib.metadata as m, json, sys
names = json.loads(sys.argv[1])
print(json.dumps({'python': list(sys.version_info[:3]),
 'libraries': {n: m.version(n) for n in names},
 'directories': sorted({str(m.distribution(n).locate_file('').resolve()) for n in names})}))
"""


def requirements(root):
    result = {}
    for line in (root / REQUIREMENTS).read_text(encoding='utf-8').splitlines():
        if line and not line.startswith('#'):
            name, version = line.split('==')
            result[name] = version
    return result


def probe_python(executable, directories, expected):
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(directories), PYTHONDONTWRITEBYTECODE='1')
    proc = subprocess.run([executable, '-c', PROBE, json.dumps(list(expected))],
                          env=env, capture_output=True, text=True, timeout=30)
    if proc.returncode:
        raise ValueError('Host Python dependencies unavailable; restore the pinned requirements first')
    result = json.loads(proc.stdout)
    if result['python'][:2] != [3, 12] or result['libraries'] != expected:
        raise ValueError('Host requires Python 3.12 and the exact IG-2 library versions')
    return result


def executable_pin(path):
    path = Path(path).resolve()
    if not path.is_absolute() or not path.is_file():
        raise ValueError('Host executable is unavailable: ' + str(path))
    return {'path': str(path), 'sha256': w.digest(path)}


def verify_cli(path):
    """Check the supervisor's required arguments without launching a model or API."""
    proc = subprocess.run([path, 'exec', '--help'], capture_output=True, text=True,
                          encoding='utf-8', errors='replace', timeout=15)
    flags = ('--ephemeral', '--approve-for-me', '--output-schema', '--output-last-message', '--color', '--cd')
    if proc.returncode or any(flag not in proc.stdout + proc.stderr for flag in flags):
        raise ValueError('Installed Codex CLI lacks required supervisor arguments')


def configuration_path(root, rel):
    if not rel.startswith('private/workflow/hosts/') or not rel.endswith('.json'):
        raise ValueError('Host configuration must be a local JSON under private/workflow/hosts/')
    return w.safe_path(root, rel)


def create(root, rel, tools, library_paths=()):
    """Observe installed tools only; never install, authenticate or change global settings."""
    root = root.resolve()
    if os.name != 'nt':
        raise ValueError('This IG-2 restore profile supports Windows hosts only')
    target = configuration_path(root, rel)
    if target.exists():
        raise ValueError('Host configuration already exists; choose a new file')
    if Path(sys.executable).resolve() != (root / '.venv/Scripts/python.exe').resolve():
        raise ValueError('Configure using this checkout\'s .venv/Scripts/python.exe')
    expected = requirements(root)
    directories = [str(root / 'src')] + [str(Path(p).resolve()) for p in library_paths]
    observed = probe_python(sys.executable, directories, expected)
    directories = list(dict.fromkeys(directories + observed['directories']))
    records = {}
    for name, flags in TOOLS.items():
        resolved = shutil.which(tools.get(name) or name)
        if not resolved:
            raise ValueError('Host tool not found: ' + name)
        pin = executable_pin(resolved)
        proc = subprocess.run([pin['path'], *flags], capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=15)
        lines = (proc.stdout + '\n' + proc.stderr).strip().splitlines()
        if proc.returncode or not lines:
            raise ValueError('Host tool version probe failed: ' + name)
        if name in NATIVE_VERSIONS and lines[0] != NATIVE_VERSIONS[name]:
            raise ValueError('Restore the pinned Poppler 26.07.0 tools before configuring this host')
        records[name] = dict(pin, version=lines[0])
    body = {'format': FORMAT, 'root': str(root), 'created_utc': datetime.now(timezone.utc).isoformat(),
            'requirements_sha256': w.digest(root / REQUIREMENTS),
            'python': executable_pin(sys.executable), 'python_version': observed['python'],
            'base_python': executable_pin(getattr(sys, '_base_executable', None) or sys.executable),
            'libraries': expected, 'process_pythonpath': directories, 'tools': records,
            'model': None, 'reasoning': None,
            'configuration_evidence': 'Installed host runtime only; no model session launched.'}
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        json.dump(body, stream, indent=2); stream.write('\n')
    return body


def load(root, rel, sha256):
    path = configuration_path(root, rel)
    if not sha256 or not path.is_file() or w.digest(path) != sha256:
        raise ValueError('Host runtime binding is incomplete or changed; no historical-path fallback')
    body = w.read_json(path)
    if body.get('format') != FORMAT or body.get('root') != str(root.resolve()):
        raise ValueError('Host runtime belongs to another checkout; configure this host again')
    if body['python']['path'] != str((root / '.venv/Scripts/python.exe').resolve()):
        raise ValueError('Host Python is not this checkout\'s venv interpreter')
    if body.get('requirements_sha256') != w.digest(root / REQUIREMENTS) or body.get('libraries') != requirements(root):
        raise ValueError('Host runtime requirements changed; configure a fresh record')
    directories = body['process_pythonpath']
    if (not isinstance(directories, list) or not directories or directories[0] != str(root.resolve() / 'src')
            or any(not Path(p).is_absolute() or not Path(p).is_dir() for p in directories)):
        raise ValueError('Host Python directories are unavailable or belong to another checkout')
    if set(body['tools']) != set(TOOLS):
        raise ValueError('Host runtime lacks required tools')
    if any(body['tools'][n].get('version') != version for n, version in NATIVE_VERSIONS.items()):
        raise ValueError('Host Poppler version differs from the restore profile')
    for pin in [body['python'], body['base_python'], *body['tools'].values()]:
        p = Path(pin['path'])
        if not p.is_absolute() or not p.is_file() or w.digest(p) != pin['sha256']:
            raise ValueError('Pinned host executable changed: ' + str(p))
    probe_python(body['python']['path'], directories, body['libraries'])
    return body


def bound(root):
    rel, digest = os.environ.get('WGC_HOST_RUNTIME'), os.environ.get('WGC_HOST_RUNTIME_SHA256')
    if not rel and not digest:
        return None
    return load(root, rel or '', digest)


def environment(body, inherited=None):
    env = dict(os.environ if inherited is None else inherited)
    prefixes = list(dict.fromkeys(str(Path(p['path']).parent) for p in body['tools'].values()))
    env.update(PYTHONPATH=os.pathsep.join(body['process_pythonpath']),
               PATH=os.pathsep.join(prefixes + [env.get('PATH', '')]),
               PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0',
               WGC_RIPGREP_PATH=body['tools']['rg']['path'],
               WGC_RIPGREP_SHA256=body['tools']['rg']['sha256'])
    for name, pin in body['tools'].items():
        resolved = shutil.which(name, path=env['PATH'])
        if not resolved or os.path.normcase(str(Path(resolved).resolve())) != os.path.normcase(pin['path']):
            raise ValueError('Host PATH shadows the pinned executable: ' + name)
    return env


def bind(root, rel):
    path = configuration_path(root, rel)
    digest = w.digest(path)
    for key, value in [('WGC_HOST_RUNTIME', rel), ('WGC_HOST_RUNTIME_SHA256', digest)]:
        if os.environ.get(key) and os.environ[key] != value:
            raise ValueError('Host runtime override differs from the inherited binding')
    body = load(root, rel, digest)
    os.environ.update(environment(body))
    os.environ.update(WGC_HOST_RUNTIME=rel, WGC_HOST_RUNTIME_SHA256=digest)
    return body


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['configure', 'check', 'exec'])
    parser.add_argument('--file', default='private/workflow/hosts/local-runtime.json')
    parser.add_argument('--python-library-path', action='append', default=[])
    for name in TOOLS:
        parser.add_argument('--' + name)
    args, command = parser.parse_known_args()
    if args.operation == 'configure':
        if command:
            parser.error('Unexpected configure arguments')
        body = create(w.ROOT, args.file, {n: getattr(args, n) for n in TOOLS}, args.python_library_path)
    else:
        if args.operation != 'exec' and command:
            parser.error('Unexpected check arguments')
        body = bind(w.ROOT, args.file)
    if args.operation == 'exec':
        command = command[1:] if command[:1] == ['--'] else command
        if not command:
            parser.error('exec requires -- followed by an explicit command')
        return subprocess.run(command, cwd=w.ROOT).returncode
    print(json.dumps({'file': args.file, 'python_version': body['python_version'],
                      'tools': {n: p['version'] for n, p in body['tools'].items()},
                      'models_launched': 0}, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        sys.exit(2)
