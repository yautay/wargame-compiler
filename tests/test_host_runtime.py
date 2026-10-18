"""Host relocation must preserve old evidence and fail closed on stale bindings."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
try:
    import host_runtime as h
    import orchestrate_ig2 as o
finally:
    sys.path.pop(0)


@pytest.fixture
def host(tmp_path, monkeypatch):
    (tmp_path / 'src').mkdir()
    libraries = tmp_path / 'installed libraries'; libraries.mkdir()
    requirements = tmp_path / h.REQUIREMENTS
    requirements.parent.mkdir(parents=True)
    requirements.write_text('pytest==9.1.1\n', encoding='utf-8')
    def executable(name):
        path = tmp_path / ('.venv/Scripts/python.exe' if name == 'python' else 'tools/' + name + '.exe')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(('synthetic ' + name).encode())
        return h.executable_pin(path)
    body = {'format': h.FORMAT, 'root': str(tmp_path.resolve()),
            'requirements_sha256': h.w.digest(requirements), 'libraries': {'pytest': '9.1.1'},
            'python_version': [3, 12, 14], 'python': executable('python'),
            'base_python': executable('base-python'),
            'process_pythonpath': [str(tmp_path / 'src'), str(libraries)],
            'tools': {n: dict(executable(n), version=h.NATIVE_VERSIONS.get(n, 'synthetic version')) for n in h.TOOLS}}
    rel = 'private/workflow/hosts/synthetic.json'
    path = tmp_path / rel; path.parent.mkdir(parents=True)
    path.write_text(json.dumps(body), encoding='utf-8')
    monkeypatch.setattr(h, 'probe_python', lambda *a: {'python': [3, 12, 14], 'libraries': body['libraries']})
    for key in ('PATH', 'PYTHONPATH', 'PYTHONDONTWRITEBYTECODE', 'GIT_OPTIONAL_LOCKS',
                'WGC_RIPGREP_PATH', 'WGC_RIPGREP_SHA256', 'WGC_HOST_RUNTIME', 'WGC_HOST_RUNTIME_SHA256'):
        monkeypatch.setenv(key, h.os.environ.get(key, ''))
    return tmp_path, rel, body


def test_explicit_host_binding_replaces_unavailable_historical_paths_without_editing_them(host):
    root, rel, body = host
    frozen = root / 'toolchain.json'
    frozen.write_text(json.dumps({'process_pythonpath': 'unavailable original host',
                                 'process_path_prefix': 'unavailable original native directory'}))
    original = frozen.read_bytes()
    h.bind(root, rel)
    env = o.validation_environment(root, {'context': ['toolchain.json']})
    assert env['PYTHONPATH'] == h.os.pathsep.join(body['process_pythonpath'])
    assert env['WGC_RIPGREP_PATH'] == body['tools']['rg']['path']
    assert env['PATH'].startswith(str(Path(body['tools']['pdfinfo']['path']).parent))
    assert frozen.read_bytes() == original
    assert env['WGC_HOST_RUNTIME_SHA256'] == h.w.digest(root / rel)


@pytest.mark.parametrize('change', ['configuration', 'executable', 'requirements'])
def test_changed_bound_runtime_never_falls_back_to_old_toolchain(host, change):
    root, rel, body = host
    h.bind(root, rel)
    path = {'configuration': root / rel, 'executable': Path(body['tools']['rg']['path']),
            'requirements': root / h.REQUIREMENTS}[change]
    path.write_bytes(path.read_bytes() + b'changed')
    with pytest.raises(ValueError, match='changed'):
        o.validation_environment(root, {'context': []})


def test_moving_checkout_requires_new_observed_host_record(host, tmp_path):
    root, rel, body = host
    other = root / 'another checkout'; other.mkdir()
    path = other / rel; path.parent.mkdir(parents=True)
    path.write_bytes((root / rel).read_bytes())
    with pytest.raises(ValueError, match='another checkout'):
        h.load(other, rel, h.w.digest(path))


def test_incomplete_binding_and_different_ripgrep_are_rejected(host, monkeypatch):
    root, rel, body = host
    monkeypatch.setenv('WGC_HOST_RUNTIME', rel)
    monkeypatch.delenv('WGC_HOST_RUNTIME_SHA256', raising=False)
    with pytest.raises(ValueError, match='incomplete'):
        h.bound(root)
    h.bind(root, rel)
    with pytest.raises(ValueError, match='Ripgrep differs'):
        o.validation_environment(root, {}, {'path': 'other', 'sha256': 'other'})


@pytest.mark.parametrize('versions,python', [({'pytest': 'different'}, [3, 12, 14]),
                                           ({'pytest': '9.1.1'}, [3, 13, 0])])
def test_dependency_probe_refuses_wrong_package_or_python_version(monkeypatch, versions, python):
    body = {'python': python, 'libraries': versions, 'directories': []}
    monkeypatch.setattr(h.subprocess, 'run', lambda *a, **kw: subprocess.CompletedProcess([], 0, json.dumps(body), ''))
    with pytest.raises(ValueError, match='Python 3.12'):
        h.probe_python('synthetic', [], {'pytest': '9.1.1'})


def test_host_record_creation_cannot_overwrite_existing_evidence(host):
    root, rel, _ = host
    before = (root / rel).read_bytes()
    with pytest.raises(ValueError, match='already exists'):
        h.create(root, rel, {})
    assert (root / rel).read_bytes() == before


def test_native_tool_name_cannot_resolve_to_another_binary_on_host_path(host):
    root, rel, body = host
    native = root / 'native' / 'pdfinfo.exe'; native.parent.mkdir()
    native.write_bytes(b'a different pinned native distribution')
    body['tools']['pdfinfo'].update(h.executable_pin(native))
    with pytest.raises(ValueError, match='PATH shadows.*pdfinfo'):
        h.environment(body)


@pytest.mark.parametrize('complete', [True, False])
def test_preflight_detects_unsupported_cli_before_a_model_can_start(monkeypatch, complete):
    text = '--ephemeral --approve-for-me --output-schema --output-last-message --color --cd' if complete else '--model'
    monkeypatch.setattr(h.subprocess, 'run', lambda *a, **kw: subprocess.CompletedProcess([], 0, text, ''))
    if complete:
        h.verify_cli('synthetic')
    else:
        with pytest.raises(ValueError, match='required supervisor arguments'):
            h.verify_cli('synthetic')
