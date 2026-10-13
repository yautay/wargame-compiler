"""Synthetic oracles from the IG-1B byte/scope contract; no publisher content."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from wgc.inputs import snapshot as s


def fixture(tmp_path):
    game = tmp_path / 'game'
    registry = tmp_path / 'registry'
    (game / 'kb').mkdir(parents=True)
    registry.mkdir()
    (game / 'wgu.yaml').write_bytes(b'name: synthetic\r\n')
    (game / 'kb' / 'rule.yaml').write_bytes(b'raw: copper\r\n# e\xcc\x81\n')
    (registry / 'provenance.json').write_bytes(b'{"identity":"unknown"}\n')
    (registry / 'rulebook.pdf').write_bytes(b'%PDF-invented-source\x00\xff')
    def entry(root, name, role):
        raw = (root / name).read_bytes()
        return {'relative_path': name, 'role': role, 'bytes': len(raw),
                'sha256': hashlib.sha256(raw).hexdigest()}
    request = {'game_root': str(game), 'registry_root': str(registry),
               'game_files': [entry(game, 'wgu.yaml', 'game_config'), entry(game, 'kb/rule.yaml', 'kb')],
               'registry_files': [entry(registry, 'provenance.json', 'provenance'), entry(registry, 'rulebook.pdf', 'selected_rulebook')],
               'historical_configured_sources': [{'relative_path': 'docs/original.pdf', 'role': 'configured_source', 'availability': 'missing'}],
               'selection': {'source_id': 'synthetic-rulebook', 'role': 'rulebook', 'edition_label': 'invented-1',
                             'edition_basis': 'Synthetic operator-selected fixture', 'selected_path': 'rulebook.pdf',
                             'sha256': hashlib.sha256((registry / 'rulebook.pdf').read_bytes()).hexdigest(),
                             'identity_to_wgu_original': 'unknown', 'semantic_acceptance': 'not_granted'}}
    return request, tmp_path / 'inputs', tmp_path / 'sources'


def freeze(f):
    return s.freeze_inputs(*f)


def sealed(parent):
    return list(parent.glob('sha256-*')) if parent.exists() else []


def test_original_bytes_independent_hashes_availability_and_pin(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    origins = {p: Path(p).read_bytes() for p in [
        str(Path(request['game_root']) / i['relative_path']) for i in request['game_files']
    ] + [str(Path(request['registry_root']) / i['relative_path']) for i in request['registry_files']]}
    result = s.freeze_inputs(request, inputs, sources)
    assert result['game_files_available'] == 2  # Synthetic fixture count only.
    assert result['configured_sources_missing'] == 1
    for kind in ['input_snapshot', 'source_snapshot']:
        directory = Path(result[kind])
        manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
        for item in manifest['files']:
            assert {'path', 'bytes', 'sha256', 'role', 'availability'} <= item.keys()
            if item['availability'] == 'missing':
                assert item['role'] == 'configured_source'
                assert item['bytes'] is item['sha256'] is item['blob_path'] is None
            else:
                raw = (directory / item['blob_path']).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == item['sha256']
                assert len(raw) == item['bytes']
                assert raw == origins[str(Path(manifest['origin_root']) / item['path'])]
        # Independent manifest ID oracle; no call to snapshot_manifest/canonical.
        body = {k: v for k, v in manifest.items() if k != 'snapshot_id'}
        expected = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        assert manifest['snapshot_id'] == 'sha256:' + hashlib.sha256(expected).hexdigest()
        assert s.verify_snapshot(directory) == manifest
    pin = json.loads((Path(result['source_snapshot']) / 'source-pin.json').read_text(encoding='utf-8'))
    assert pin['identity_to_wgu_original'] == 'unknown'
    assert pin['semantic_acceptance'] == 'not_granted'
    assert pin['selection_purpose'] == 'new_ig_source'
    assert result['semantic_acceptance_granted'] is False
    assert result['executable_readiness_granted'] is False
    assert all(Path(p).read_bytes() == raw for p, raw in origins.items())
    assert not (Path(result['input_snapshot']) / 'files/docs/original.pdf').exists()


def test_repeatability_reuses_exact_bytes_despite_plan_order_and_time(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    first = s.freeze_inputs(request, inputs, sources)
    prior = {p: p.read_bytes() for root in [Path(first['input_snapshot']), Path(first['source_snapshot'])]
             for p in root.rglob('*') if p.is_file()}
    request['game_files'].reverse()
    request['registry_files'].reverse()
    request['enumerated_utc'] = 'different planning timestamp'
    second = s.freeze_inputs(request, inputs, sources)
    assert first == second
    assert all(p.read_bytes() == raw for p, raw in prior.items())
    assert len(sealed(inputs)) == len(sealed(sources)) == 1


@pytest.mark.parametrize('name', ['../outside', '/outside', 'kb/..', 'kb\\rule.yaml',
                                  'kb/rule.yaml:stream', 'kb/NUL', 'kb/name.', 'kb//rule.yaml', 'kb/x?'])
def test_path_escape_rejected_before_any_content_read(tmp_path, monkeypatch, name):
    request, inputs, sources = fixture(tmp_path)
    request['game_files'][1]['relative_path'] = name
    reads = []
    monkeypatch.setattr(s, 'open_read', lambda p: reads.append(p))
    with pytest.raises(s.SnapshotError, match='unsafe relative path'):
        s.freeze_inputs(request, inputs, sources)
    assert reads == []
    assert not inputs.exists() and not sources.exists()


@pytest.mark.parametrize('case_alias', [False, True])
def test_duplicate_path_rejected_before_reads(tmp_path, monkeypatch, case_alias):
    request, inputs, sources = fixture(tmp_path)
    duplicate = copy.deepcopy(request['game_files'][1])
    if case_alias:
        duplicate['relative_path'] = 'KB/RULE.YAML'
    request['game_files'].append(duplicate)
    reads = []
    monkeypatch.setattr(s, 'open_read', lambda p: reads.append(p))
    with pytest.raises(s.SnapshotError, match='duplicate path/case alias'):
        s.freeze_inputs(request, inputs, sources)
    assert not reads


def test_unenumerated_file_rejected_without_reading_it(tmp_path, monkeypatch):
    request, inputs, sources = fixture(tmp_path)
    (Path(request['game_root']) / 'kb/new.yaml').write_bytes(b'not authorized to read')
    reads = []
    monkeypatch.setattr(s, 'open_read', lambda p: reads.append(p))
    with pytest.raises(s.SnapshotError, match='explicit enumeration'):
        s.freeze_inputs(request, inputs, sources)
    assert not reads


def test_changed_pinned_bytes_never_publish(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    (Path(request['game_root']) / 'kb/rule.yaml').write_bytes(b'changed before snapshot')
    with pytest.raises(s.SnapshotError, match='pinned request'):
        s.freeze_inputs(request, inputs, sources)
    assert not sealed(inputs) and not sealed(sources)


def test_mutation_after_early_copy_is_detected_by_global_rehash(tmp_path, monkeypatch):
    request, inputs, sources = fixture(tmp_path)
    origin = Path(request['game_root']) / 'wgu.yaml'
    real = s.measure
    changed = False
    def mutate(path, destination=None):
        nonlocal changed
        result = real(path, destination)
        if path == origin and destination is not None and not changed:
            # Source handle is closed; this mutation occurs during the full snapshot.
            old = origin.stat()
            origin.write_bytes(b'name: different\r\n')  # equal byte count
            os.utime(origin, ns=(old.st_atime_ns, old.st_mtime_ns))
            changed = True
        return result
    monkeypatch.setattr(s, 'measure', mutate)
    with pytest.raises(s.SnapshotError, match='input changed during snapshot'):
        s.freeze_inputs(request, inputs, sources)
    assert changed and not sealed(inputs) and not sealed(sources)


def test_new_kb_file_during_copy_never_publishes(tmp_path, monkeypatch):
    request, inputs, sources = fixture(tmp_path)
    real = s.measure
    def mutate(path, destination=None):
        result = real(path, destination)
        if destination is not None and path.name == 'wgu.yaml':
            (Path(request['game_root']) / 'kb/new.yaml').write_bytes(b'new byte source')
        return result
    monkeypatch.setattr(s, 'measure', mutate)
    with pytest.raises(s.SnapshotError, match='enumeration changed'):
        s.freeze_inputs(request, inputs, sources)
    assert not sealed(inputs) and not sealed(sources)


def test_missing_source_appearing_during_copy_never_publishes(tmp_path, monkeypatch):
    request, inputs, sources = fixture(tmp_path)
    real = s.enumerate_game_files
    calls = 0
    def enumerate_again(root):
        nonlocal calls
        calls += 1
        if calls == 2:
            target = root / 'docs/original.pdf'
            target.parent.mkdir()
            target.write_bytes(b'later source')
        return real(root)
    monkeypatch.setattr(s, 'enumerate_game_files', enumerate_again)
    with pytest.raises(s.SnapshotError, match='appeared'):
        s.freeze_inputs(request, inputs, sources)
    assert not sealed(inputs) and not sealed(sources)


def test_missing_required_input_fails_but_optional_source_does_not(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    (Path(request['registry_root']) / 'rulebook.pdf').unlink()
    with pytest.raises(s.SnapshotError, match='required input missing'):
        s.freeze_inputs(request, inputs, sources)
    assert not sealed(inputs) and not sealed(sources)


def test_available_configured_source_is_copied_without_substitution(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    target = Path(request['game_root']) / 'docs/original.pdf'
    target.parent.mkdir()
    target.write_bytes(b'an explicitly available original, unlike selected promoted bytes')
    request['historical_configured_sources'][0]['availability'] = 'available'
    result = s.freeze_inputs(request, inputs, sources)
    manifest = s.verify_snapshot(result['input_snapshot'])
    item = next(f for f in manifest['files'] if f['role'] == 'configured_source')
    assert item['sha256'] == hashlib.sha256(target.read_bytes()).hexdigest()
    assert item['sha256'] != request['selection']['sha256']
    assert result['configured_sources_missing'] == 0


def link_directory(link, target):
    if os.name == 'nt':
        result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)], capture_output=True)
        assert result.returncode == 0, result.stderr
    else:
        link.symlink_to(target, target_is_directory=True)


def test_real_junction_or_symlink_escape_rejected_before_reads(tmp_path, monkeypatch):
    request, inputs, sources = fixture(tmp_path)
    outside = tmp_path / 'outside'
    outside.mkdir()
    (outside / 'secret.yaml').write_bytes(b'never read this')
    link_directory(Path(request['game_root']) / 'kb/linked', outside)
    reads = []
    monkeypatch.setattr(s, 'open_read', lambda p: reads.append(p))
    with pytest.raises(s.SnapshotError, match='linked path'):
        s.freeze_inputs(request, inputs, sources)
    assert not reads and not inputs.exists() and not sources.exists()


def test_opened_handle_rejects_link_redirection_even_if_precheck_lost_race(tmp_path, monkeypatch):
    outside = tmp_path / 'outside'
    outside.mkdir()
    (outside / 'secret').write_bytes(b'never consume redirected content')
    link = tmp_path / 'linked'
    link_directory(link, outside)
    monkeypatch.setattr(s, 'no_links', lambda path: None)
    with pytest.raises((s.SnapshotError, OSError)):
        with s.open_read(link / 'secret'):
            pytest.fail('redirected handle must be rejected before reading')


def test_no_output_in_read_only_neighbour_root(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    before = {p: p.read_bytes() for p in Path(request['game_root']).rglob('*') if p.is_file()}
    with pytest.raises(s.SnapshotError, match='overlaps read-only'):
        s.freeze_inputs(request, Path(request['game_root']) / 'output', sources)
    assert all(p.read_bytes() == raw for p, raw in before.items())
    assert not (Path(request['game_root']) / 'output').exists()


def test_hardlink_alias_rejected(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    origin = Path(request['game_root']) / 'kb/rule.yaml'
    alias = origin.with_name('alias.yaml')
    os.link(origin, alias)
    request['game_files'].append({**request['game_files'][1], 'relative_path': 'kb/alias.yaml'})
    with pytest.raises(s.SnapshotError, match='physical input alias'):
        s.freeze_inputs(request, inputs, sources)
    assert not sealed(inputs) and not sealed(sources)


def test_existing_corrupt_snapshot_not_rewritten(tmp_path):
    f = fixture(tmp_path)
    result = freeze(f)
    target = Path(result['input_snapshot']) / 'files/kb/rule.yaml'
    target.write_bytes(b'operator changed sealed bytes')
    with pytest.raises(s.SnapshotError, match='copy hash mismatch'):
        freeze(f)
    assert target.read_bytes() == b'operator changed sealed bytes'


def test_original_identity_and_semantics_cannot_be_claimed(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    request['selection']['identity_to_wgu_original'] = 'same'
    with pytest.raises(s.SnapshotError, match='unknown original identity'):
        s.freeze_inputs(request, inputs, sources)


def test_cli_and_no_inferred_content_reads(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    plan = tmp_path / 'request.json'
    plan.write_text(json.dumps(request), encoding='utf-8')
    env = {**os.environ, 'PYTHONPATH': str(Path(__file__).resolve().parents[2] / 'src'),
           'PYTHONDONTWRITEBYTECODE': '1'}
    args = [sys.executable, '-m', 'wgc.inputs.snapshot', str(plan), '--inputs', str(inputs), '--sources', str(sources)]
    result = subprocess.run(args, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)['semantic_acceptance_granted'] is False
    request['game_files'][0]['relative_path'] = '../outside'
    plan.write_text(json.dumps(request), encoding='utf-8')
    result = subprocess.run(args, env=env, capture_output=True, text=True)
    assert result.returncode == 1 and 'Snapshot rejected' in result.stdout


def test_selected_source_metadata_rejected_before_any_publication(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    request['selection']['role'] = 'silently substituted source'
    with pytest.raises(s.SnapshotError, match='valid metadata'):
        s.freeze_inputs(request, inputs, sources)
    assert not inputs.exists() and not sources.exists()


def test_duplicate_success_does_not_leave_unsealed_staging(tmp_path):
    f = fixture(tmp_path)
    freeze(f)
    freeze(f)
    assert not list(f[1].glob('.pending-*')) and not list(f[2].glob('.pending-*'))


def test_linked_destination_never_writes_to_target(tmp_path):
    request, inputs, sources = fixture(tmp_path)
    outside = tmp_path / 'outside'
    outside.mkdir()
    link_directory(inputs, outside)
    with pytest.raises(s.SnapshotError, match='linked path'):
        s.freeze_inputs(request, inputs, sources)
    assert list(outside.iterdir()) == []


def test_duplicate_metadata_keys_reject(tmp_path):
    path = tmp_path / 'plan.json'
    path.write_bytes(b'{"game_root":"safe","game_root":"other"}')
    with pytest.raises(ValueError, match='duplicate JSON key'):
        s.read_structured(path)


def test_windows_open_handle_blocks_writes_while_reading(tmp_path):
    path = tmp_path / 'bytes'
    path.write_bytes(b'original')
    with s.open_read(path) as stream:
        if os.name == 'nt':
            with pytest.raises(OSError):
                path.write_bytes(b'mutation')
        assert stream.read() == b'original'


def test_noncanonical_snapshot_metadata_rejects(tmp_path):
    result = freeze(fixture(tmp_path))
    path = Path(result['source_snapshot']) / 'manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    with pytest.raises(s.SnapshotError, match='not canonical'):
        s.verify_snapshot(path.parent)
