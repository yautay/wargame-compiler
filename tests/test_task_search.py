"""Packet search cannot read globally allowed private or out-of-packet sentinels."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


@pytest.fixture(autouse=True)
def isolate_live_guard(monkeypatch):
    # Expected synthetic denials must not latch a real coordinator running pytest.
    monkeypatch.delenv('WGC_CONTEXT_GUARD', raising=False)
    monkeypatch.delenv('WGC_CONTEXT_GUARD_SHA256', raising=False)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
try:
    spec = importlib.util.spec_from_file_location('packet_search', ROOT / 'scripts/search_task.py')
    s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
finally:
    sys.path.pop(0)


def dump(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body), encoding='utf-8')


@pytest.fixture
def scope(tmp_path):
    for rel, content in [('scripts/allowed.py', 'def evidence():\n    return "PACKET_MATCH"\n'),
                         ('scripts/outside.py', 'OUTSIDE_SENTINEL PACKET_MATCH\n'),
                         ('private/unrelated/source.json', '{"source":"PRIVATE_SENTINEL PACKET_MATCH"}')]:
        p = tmp_path / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding='utf-8')
    dump(tmp_path / 'docs/work/context-policy.json', {'allow': ['scripts/', 'private/unrelated/source.json']})
    rel = 'private/workflow/packets/synthetic/search-manifest.json'
    dump(tmp_path / rel, {'format': s.FORMAT, 'task': 'IG-2B03',
                          'files': [{'path': 'scripts/allowed.py', 'sha256': s.w.digest(tmp_path / 'scripts/allowed.py')}]})
    return tmp_path, rel, s.w.digest(tmp_path / rel)


def test_only_packet_file_is_searched_despite_global_allowlist(scope):
    root, manifest, sha = scope
    result = s.search(root, manifest, sha, 'IG-2B03', 'PACKET_MATCH')
    text = json.dumps(result)
    assert len(result['matches']) == 1
    assert result['matches'][0]['path'] == 'scripts/allowed.py'
    assert 'PRIVATE_SENTINEL' not in text and 'OUTSIDE_SENTINEL' not in text


@pytest.mark.parametrize('rel', ['scripts/outside.py', 'private/unrelated/source.json', '../outside', 'scripts/'])
def test_explicit_file_cannot_expand_packet(scope, rel):
    root, manifest, sha = scope
    with pytest.raises(ValueError, match='not in'):
        s.search(root, manifest, sha, 'IG-2B03', 'PACKET_MATCH', [rel])


def test_missing_binding_never_falls_back_to_global_search(scope, monkeypatch):
    root, manifest, sha = scope
    monkeypatch.setattr(s.subprocess, 'run', lambda *a, **kw: pytest.fail('No global fallback'))
    with pytest.raises(ValueError, match='mandatory'):
        s.search(root, None, None, None, 'PACKET_MATCH')


def test_changed_manifest_and_file_are_rejected_before_search(scope):
    root, manifest, sha = scope
    with pytest.raises(ValueError, match='manifest changed'):
        s.search(root, manifest, 'wrong', 'IG-2B03', 'PACKET_MATCH')
    (root / 'scripts/allowed.py').write_text('changed', encoding='utf-8')
    with pytest.raises(ValueError, match='input changed'):
        s.search(root, manifest, sha, 'IG-2B03', 'PACKET_MATCH')


def test_wrong_task_identity_is_rejected(scope):
    root, manifest, sha = scope
    with pytest.raises(ValueError, match='identity'):
        s.search(root, manifest, sha, 'IG-2B04', 'PACKET_MATCH')


@pytest.mark.parametrize('path', ['private/unrelated/source.json', 'docs/work/queue.json',
                                 'docs/work/QUEUE.JSON', 'docs/work/CONTEXT-POLICY.JSON',
                                 'docs/STATUS.md', 'docs/HANDOFF.md', 'docs/ROADMAP.md',
                                 'DOCS/Status.MD', 'DOCS/HandOff.MD', 'DOCS/RoadMap.MD',
                                 'docs/work/tasks/IG-2B03.md', 'archive/a.md', 'source.pdf'])
def test_private_volatile_history_and_binary_are_not_generic_search_inputs(scope, path):
    root, manifest, _ = scope
    p = root / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('SENTINEL', encoding='utf-8')
    dump(root / manifest, {'format': s.FORMAT, 'task': 'IG-2B03',
                           'files': [{'path': path, 'sha256': s.w.digest(p)}]})
    with pytest.raises(ValueError, match='cannot be searched'):
        s.search(root, manifest, s.w.digest(root / manifest), 'IG-2B03', 'SENTINEL')


def test_output_is_bounded_and_truncation_is_explicit(scope):
    root, manifest, _ = scope
    p = root / 'scripts/allowed.py'
    p.write_text(('PACKET_MATCH ' + 'x' * 4000 + '\n') * 30, encoding='utf-8')
    dump(root / manifest, {'format': s.FORMAT, 'task': 'IG-2B03',
                           'files': [{'path': 'scripts/allowed.py', 'sha256': s.w.digest(p)}]})
    result = s.search(root, manifest, s.w.digest(root / manifest), 'IG-2B03', 'PACKET_MATCH',
                      max_matches=3, max_bytes=2048)
    assert result['truncated'] and len(result['matches']) <= 3
    assert len(json.dumps(result, ensure_ascii=False).encode('utf-8')) + 1 <= 2048
    assert all(m['line_truncated'] for m in result['matches'])


def test_pattern_is_an_operand_not_an_option(scope):
    root, manifest, sha = scope
    assert s.search(root, manifest, sha, 'IG-2B03', '--files')['matches'] == []


def test_supported_cli_cannot_replace_session_binding(scope):
    root, manifest, sha = scope
    env = dict(s.os.environ, WGC_TASK_ID='IG-2B03', WGC_TASK_SEARCH_MANIFEST=manifest,
               WGC_TASK_SEARCH_SHA256=sha)
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/search_task.py'), '--task', 'IG-2B04',
                             '--pattern', 'PACKET_MATCH'], env=env, cwd=root,
                            capture_output=True, text=True, timeout=15)
    assert result.returncode == 2 and 'session binding' in result.stderr
    assert 'SENTINEL' not in result.stdout


def test_ambient_ripgrep_config_cannot_preprocess_pinned_bytes(scope, monkeypatch):
    root, manifest, sha = scope
    config = root / 'hostile-rg-config'
    # The invalid preprocessor would fail if rg honored this ambient configuration.
    config.write_text('--pre=not-an-authorized-preprocessor\n--glob=!allowed.py\n', encoding='utf-8')
    monkeypatch.setenv('RIPGREP_CONFIG_PATH', str(config))
    result = s.search(root, manifest, sha, 'IG-2B03', 'PACKET_MATCH')
    assert len(result['matches']) == 1
    assert 'SENTINEL' not in json.dumps(result)


@pytest.mark.parametrize('encoding', ['cp1252:strict', 'cp1250:strict', 'ascii:strict'])
def test_guarded_search_cli_preserves_unicode_with_windows_pipe_encoding(scope, encoding):
    root, manifest, _ = scope
    text = 'CLAIM \u2192 checkpoint \u017c\u00f3\u0142\u0107 \u6f22\u5b57 \U0001f3b2'
    source = root / 'scripts/allowed.py'
    source.write_text(text + '\n', encoding='utf-8')
    dump(root / manifest, {'format': s.FORMAT, 'task': 'IG-2B03', 'files': [
        {'path': 'scripts/allowed.py', 'sha256': s.w.digest(source)}]})
    guard = 'private/session/context-guard.json'
    marker = root / 'private/session/context-denied.json'
    dump(root / guard, {'format': 'wgc-context-guard-1', 'task': 'IG-2B03',
                        'denial': marker.relative_to(root).as_posix()})
    executable = s.ripgrep_binding()
    env = dict(s.os.environ, PATH='', PYTHONIOENCODING=encoding, PYTHONUTF8='0',
               WGC_RIPGREP_PATH=executable['path'], WGC_RIPGREP_SHA256=executable['sha256'],
               WGC_TASK_ID='IG-2B03', WGC_TASK_SEARCH_MANIFEST=manifest,
               WGC_TASK_SEARCH_SHA256=s.w.digest(root / manifest),
               WGC_CONTEXT_GUARD=guard, WGC_CONTEXT_GUARD_SHA256=s.w.digest(root / guard))
    # Exercise the actual CLI parser, rg process and guard, not a mocked encoder.
    code = ('import sys; from pathlib import Path; '
            f'sys.path.insert(0, {str(ROOT / "scripts")!r}); '
            'import search_task as s; s.w.ROOT=Path(sys.argv.pop(1)); '
            's.guard.cli(s.w.ROOT, "task_search", s.main)')
    try:
        result = subprocess.run([sys.executable, '-c', code, str(root), '--pattern', 'CLAIM'],
                                cwd=root, env=env, capture_output=True, timeout=8)
    except subprocess.TimeoutExpired:
        pytest.fail('Valid Unicode search was incorrectly latched by the context guard')
    assert result.returncode == 0, result.stderr.decode('ascii', errors='replace')
    assert not marker.exists() and not result.stderr
    output = json.loads(result.stdout.decode('ascii'))
    assert output['matches'][0]['text'] == text
    assert b'\\u2192' in result.stdout and not output['truncated']
    assert len(result.stdout) <= output['max_output_bytes']


@pytest.mark.parametrize('fault', ['missing', 'digest', 'relative', 'incomplete'])
def test_invalid_executable_binding_never_falls_back_to_path(scope, monkeypatch, fault):
    root, manifest, sha = scope
    executable = s.ripgrep_binding()
    monkeypatch.setenv('WGC_RIPGREP_PATH', executable['path'])
    monkeypatch.setenv('WGC_RIPGREP_SHA256', executable['sha256'])
    if fault == 'missing':
        monkeypatch.setenv('WGC_RIPGREP_PATH', str(root / 'missing-rg.exe'))
    elif fault == 'digest':
        monkeypatch.setenv('WGC_RIPGREP_SHA256', '0' * 64)
    elif fault == 'relative':
        monkeypatch.setenv('WGC_RIPGREP_PATH', 'rg.exe')
    else:
        monkeypatch.delenv('WGC_RIPGREP_SHA256')
    monkeypatch.setattr(s.subprocess, 'run', lambda *a, **k: pytest.fail('Invalid pin must not execute any search'))
    with pytest.raises(ValueError, match='ripgrep executable'):
        s.search(root, manifest, sha, 'IG-2B03', 'PACKET_MATCH')


def test_missing_path_has_an_actionable_preflight_failure(monkeypatch):
    monkeypatch.delenv('WGC_RIPGREP_PATH', raising=False)
    monkeypatch.delenv('WGC_RIPGREP_SHA256', raising=False)
    monkeypatch.setenv('PATH', '')
    with pytest.raises(ValueError, match='supply WGC_RIPGREP_PATH'):
        s.ripgrep_binding()


def test_search_budget_counts_escaped_unicode_on_the_wire(scope):
    root, manifest, _ = scope
    source = root / 'scripts/allowed.py'
    source.write_text(('CLAIM ' + '\u2192\U0001f3b2' * 20 + '\n') * 10, encoding='utf-8')
    dump(root / manifest, {'format': s.FORMAT, 'task': 'IG-2B03', 'files': [
        {'path': 'scripts/allowed.py', 'sha256': s.w.digest(source)}]})
    output = s.search(root, manifest, s.w.digest(root / manifest), 'IG-2B03', 'CLAIM', max_bytes=1024)
    assert output['truncated'] and output['matches']
    assert len(s.guard.json_text(output).encode('ascii')) + 1 <= 1024
