"""Independent first-repair verification with contract-derived expected values."""
import base64
import hashlib
import json
from pathlib import Path

import pytest
import yaml

from wgc.wgu_adapter.importer import finish, import_bytes, import_snapshot


@pytest.mark.parametrize('scalar', [
    '!!bool malformed', '!!timestamp malformed', '!!timestamp 2026-99-99',
    '!!int malformed', '!!float malformed', '!!binary "é"',
])
def test_scalar_diagnostics_exact_escaped_pointer_and_location(scalar):
    raw = ('terms:\r\n  - en: Alpha\r\n    "a/b":\r\n      "~x": ' + scalar + '\r\n').encode('utf-8')
    f = import_bytes(raw, 'kb/terms.yaml')
    result = finish([f])
    assert result['record_counts'] == {'processed': 0, 'raw': 0, 'error': 1}
    assert base64.b64decode(f['raw_base64']) == raw
    d = f['diagnostics'][0]
    assert (d['file'], d['field'], d['line'], d['column']) == ('kb/terms.yaml', '/terms/0/a~1b/~0x', 4, 13)


@pytest.mark.parametrize('raw,path,field,line', [
    (b'terms:\n  - en: Alpha\n    definition: []\n', 'kb/terms.yaml', '/terms/0/definition', 3),
    (b'terms: [{en: Alpha}]\nnotes: [wrong]\n', 'kb/terms.yaml', '/notes', 2),
    (b'chapter: {title: Alpha}\nrules: [{id: R-A, title: A, version: {introduced: false}}]', 'kb/rules/x.yaml', '/rules/0/version/introduced', 2),
    (b'chapter: {title: Alpha}\nrules: [{id: R-A, title: A, digital: {kind: unsupported}}]', 'kb/rules/x.yaml', '/rules/0/digital/kind', 2),
    (b'chapter: {title: Alpha}\nrules: [{id: R-A, title: A, source: {translation: [{file: false}]}}]', 'kb/rules/x.yaml', '/rules/0/source/translation/0/file', 2),
    (b'tables: [{id: T-A, title: A, tables: [{rows: [{wrong: shape}]}]}]', 'kb/tables.yaml', '/tables/0/tables/0/rows/0', 1),
    (b'changes: [{id: C-A, kind: imaginary}]', 'kb/changes.yaml', '/changes/0/kind', 1),
    (b'ambiguities: [{id: N-A, title: A, scope: imaginary}]', 'kb/ambiguities.yaml', '/ambiguities/0/scope', 1),
    (b'scenarios: [{id: Q-A, question: A, chain: null}]', 'kb/scenarios.yaml', '/scenarios/0/chain', 1),
    (b'procedures: [{id: P-A, title: A, subprocedures: [{id: P-B, title: A, steps: [{n: true, text: A}]}]}]', 'kb/procedures.yaml', '/procedures/0/subprocedures/0/steps/0/n', 1),
    (b'schema: wgu/kb@1\ngame: false\n', 'kb/manifest.yaml', '/game', 2),
    (b'schema: wgu/kb@1\ngame: {}\nlanguage: false\n', 'kb/manifest.yaml', '/language', 3),
    (b'schema: wgu/kb@1\ngame: {}\nhistory: {}\n', 'kb/manifest.yaml', '/history', 3),
    (b'procedures: []\nlegend: false\n', 'kb/procedures.yaml', '/legend', 2),
])
def test_nested_and_file_known_schema_shapes_are_located_errors(raw, path, field, line):
    f = import_bytes(raw, path)
    assert finish([f])['record_counts']['error'] > 0
    assert base64.b64decode(f['raw_base64']) == raw
    d = next(d for d in f['diagnostics'] if d['field'] == field)
    assert d['line'] == line and d['column'] is not None


def test_missing_file_metadata_uses_existing_parent_location():
    raw = b'rules: [{id: R-A, title: A}]\n'
    f = import_bytes(raw, 'kb/rules/x.yaml')
    d = next(d for d in f['diagnostics'] if d['field'] == '/chapter')
    assert d['line'] == 1 and d['column'] == 1
    assert any(r['field'] == '/chapter' and r['status'] == 'error' for r in f['records'])
    assert base64.b64decode(f['raw_base64']) == raw


def test_valid_extensions_unconstrained_values_and_numbering_are_not_rejected():
    raw = b'''terms: [{en: Alpha, novel: {nested: [null, false, 7]}}]
confusables: [null, false, 7, "", [one,two], {id: X, refs: anything, novel: {a: b}}, {id: X}]
procedures: [{id: P-A, title: A, steps: [{n: -2, text: A, substeps: [{n: "i.a", text: B, novel: true}]}]}]
tables: [{id: T-A, title: A, data: {unconstrained: [null, false, 7]}}]
concepts: [{id: X, novel: {whatever: [a,b]}, status: decided, decided_by: owner}]
novel: {id: X, nested: {extra: [null, false]}}
'''
    f = import_bytes(raw, 'kb/extension.yaml')
    result = finish([f])
    assert result['record_counts'] == {'processed': 13, 'raw': 1, 'error': 0}
    assert result['duplicate_ids'] == []
    assert f['document'] == yaml.safe_load(raw)
    assert all(r['external_id'] is None for r in f['records'] if r['kind'] == 'confusable')
    assert all(r['semantic_acceptance'] == 'not_granted' and r['executable_readiness'] == 'not_granted' for r in f['records'])
    assert '/terms/0/novel/nested/2' in {x['field'] for x in f['fields']}
    assert '/procedures/0/steps/0/substeps/0/novel' in {x['field'] for x in f['fields']}
    assert result['structural_extensions']['step.n']


def synthetic_snapshot(tmp_path, blobs):
    # Independent construction of the documented canonical snapshot envelope;
    # no production freeze helper supplies the expected fixture/record values.
    body = {'schema_version': 'wgc-input-1', 'kind': 'input_snapshot',
            'origin_root': str(tmp_path.absolute()), 'source_snapshot_id': 'sha256:' + '0' * 64,
            'files': [{'path': p, 'blob_path': 'files/' + p, 'availability': 'available',
                       'role': 'kb', 'edition_label': None, 'bytes': len(raw),
                       'sha256': hashlib.sha256(raw).hexdigest()} for p, raw in sorted(blobs.items())]}
    encode = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    identity = hashlib.sha256(encode(body)).hexdigest()
    manifest = {**body, 'snapshot_id': 'sha256:' + identity}
    directory = tmp_path / ('sha256-' + identity)
    directory.mkdir()
    (directory / 'manifest.json').write_bytes(encode(manifest) + b'\n')
    for path, raw in blobs.items():
        p = directory / 'files' / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
    return directory


def test_multi_file_import_continues_and_preserves_every_raw_byte(tmp_path):
    blobs = {
        'kb/00-invalid.yaml': b'terms: [{en: A, novel: !!timestamp impossible}]',
        'kb/01-invalid.yaml': b'terms: [{en: A, novel: !!bool impossible}]',
        'kb/terms.yaml': b'terms: [{en: A}]\nconfusables: [null, A]\n',
        'kb/tables.yaml': b'tables: [{id: T-A, title: A, complete: true, data: {novel: [a,b]}}]',
        'kb/relations.yaml': b'relations: [{from: T-A, to: T-A, type: see, status: verified}]',
        'kb/unknown.bin': b'\x00\xffunknown\r\n',
    }
    result = import_snapshot(synthetic_snapshot(tmp_path, blobs))
    assert len(result['files']) == len(blobs)
    assert result['record_counts'] == {'processed': 5, 'raw': 1, 'error': 2}
    for f in result['files']:
        assert base64.b64decode(f['raw_base64']) == blobs[f['path']]
    assert result['semantic_acceptance'] == 'not_granted'
    assert result['publisher_source_coverage'] == 'not_verified'
    assert result['executable_readiness'] == 'not_granted'


def test_unrelated_constructor_programming_errors_are_not_masked(monkeypatch):
    from wgc.wgu_adapter.parser import StrictSafeLoader
    def fail(self, node):
        raise KeyError('synthetic implementation error')
    monkeypatch.setitem(StrictSafeLoader.yaml_constructors, 'tag:yaml.org,2002:str', fail)
    with pytest.raises(KeyError, match='synthetic implementation error'):
        import_bytes(b'terms: [{en: A}]', 'kb/terms.yaml')
