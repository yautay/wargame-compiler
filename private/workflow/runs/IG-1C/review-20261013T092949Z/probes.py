"""Reviewer-authored structural oracles; no gameplay gold or semantic decisions."""
import base64
import json

import pytest

from wgc.wgu_adapter.importer import finish, import_bytes
from wgc.wgu_adapter.parser import ParseError, parse


@pytest.mark.parametrize('raw,line', [
    (b'terms: [{en: Alpha, en: Beta}]', 1),
    (b'terms:\n - en: Alpha\n   extension: {x: 1, x: 2}\n', 3),
    (b'terms: [{en: !!python/name:os.system ""}]', 1),
    (b'terms: [{en: !!python/object/new:subprocess.Popen []}]', 1),
    (b'terms: [{en: Alpha}]\n---\nterms: []\n', 2),
    (b'terms: [{en: Alpha, refs: [unfinished}]', 1),
])
def test_rejected_yaml_preserves_bytes_and_has_location(raw, line):
    f = import_bytes(raw, 'kb/terms.yaml')
    result = finish([f])
    assert result['record_counts'] == {'processed': 0, 'raw': 0, 'error': 1}
    assert f['document'] is None
    assert base64.b64decode(f['raw_base64']) == raw
    assert f['diagnostics'][0]['code'] == 'yaml_error'
    assert f['diagnostics'][0]['line'] == line
    assert f['diagnostics'][0]['column'] is not None


@pytest.mark.parametrize('scalar', ['!!bool invalid', '!!timestamp invalid', '!!int invalid', '!!float invalid'])
def test_malformed_explicit_safe_scalars_are_accounted(scalar):
    # Explicit safe tags still need well-formed values. Invalid input must return
    # an error record, not abort the complete directory import with KeyError etc.
    raw = ('terms: [{en: Alpha, extension: ' + scalar + '}]\n').encode()
    f = import_bytes(raw, 'kb/terms.yaml')
    assert finish([f])['record_counts'] == {'processed': 0, 'raw': 0, 'error': 1}
    assert base64.b64decode(f['raw_base64']) == raw
    assert f['diagnostics'][0]['code'] == 'yaml_error'


@pytest.mark.parametrize('raw', [
    b'x: &loop {child: *loop}\n',
    b'x: &loop [*loop]\n',
    b'? [non, scalar]\n: value\n',
    b'x: &base {a: 1}\ny: {<<: *base}\n',
    b'\xff\xfe', b'', b'# only comment\n',
])
def test_recursive_or_unsupported_documents_remain_error(raw):
    f = import_bytes(raw, 'kb/extension.yaml')
    assert finish([f])['record_counts']['error'] == 1
    assert base64.b64decode(f['raw_base64']) == raw


def test_real_depth_budget():
    raw = ('x: ' + '[' * 110 + 'leaf' + ']' * 110).encode()
    with pytest.raises(ParseError):
        parse(raw)


def test_real_alias_expansion_budget():
    # 8-way aliases exceed 200,000 expanded field occurrences, although the
    # YAML has fewer than 600 bytes. Exercise actual production constants.
    raw = 'a0: &a0 [x,x,x,x,x,x,x,x]\n'
    raw += ''.join(f'a{i}: &a{i} [' + ','.join([f'*a{i-1}'] * 8) + ']\n' for i in range(1, 6))
    with pytest.raises(ParseError, match='budget'):
        parse(raw.encode())


@pytest.mark.parametrize('raw', [
    b'terms: {en: Alpha}', b'terms: [42]', b'terms: [{en: null}]',
    b'procedures: [{id: P-A, title: A, subprocedures: {id: P-B}}]',
    b'procedures: [{id: P-A, title: A, steps: [{n: 1, text: A, substeps: false}]}]',
    b'relations: [{from: R-A, to: R-B}]',
    b'concepts: [{id: null}]',
])
def test_malformed_records_and_collections_have_explicit_errors(raw):
    f = import_bytes(raw, 'kb/extension.yaml')
    assert finish([f])['record_counts']['error'] > 0
    assert base64.b64decode(f['raw_base64']) == raw
    assert f['diagnostics']


def test_cross_file_duplicate_ids_no_overwrite():
    a = import_bytes(b'concepts: [{id: C-A}]', 'kb/terminology.yaml')
    b = import_bytes(b'procedures: [{id: P-A, title: A, subprocedures: [{id: C-A, title: B}]}]', 'kb/procedures.yaml')
    result = finish([a, b])
    assert result['record_counts'] == {'processed': 1, 'raw': 0, 'error': 2}
    assert len(result['duplicate_ids']) == 1
    assert len(result['duplicate_ids'][0]['occurrences']) == 2


def test_anonymous_terms_nested_numbering_unknown_fields_and_metadata():
    raw = b'''terms: [{en: Alpha, novel: {"a/b": {"~x": [one, two]}}}]
procedures:
 - id: P-A
   title: A
   steps:
    - n: "ii.a"
      text: First
      substeps: [{n: "ii.a.1", text: Second}]
concepts: [{id: C-A, status: decided, novel: {nested: true}}]
unknown_metadata: {id: C-A, nested: [one, two]}
'''
    f = import_bytes(raw, 'kb/novel.yaml')
    result = finish([f])
    assert result['record_counts'] == {'processed': 5, 'raw': 1, 'error': 0}
    assert not result['duplicate_ids']
    term = next(r for r in f['records'] if r['kind'] == 'term')
    assert term['external_id'] is None
    fields = {r['field'] for r in f['fields']}
    assert '/terms/0/novel/a~1b/~0x/1' in fields
    concept = next(r for r in f['records'] if r['kind'] == 'terminology')
    assert '/concepts/0/novel' in concept['unknown_field_paths']
    inner = next(r for r in f['records'] if r['field'].endswith('/substeps/0'))
    assert inner['value']['n'] == 'ii.a.1'
    assert inner['parent_field'] == '/procedures/0/steps/0'
    assert all(r['semantic_acceptance'] == 'not_granted' for r in f['records'])


def test_navigation_and_imported_decisions_do_not_grant_meaning():
    raw = b'''rules: [{id: R-A, title: A, refs: [R-B], see: R-C}]
relations: [{from: R-A, to: R-B, type: requires, status: verified}]
tables: [{id: T-A, title: A, complete: true}]
ambiguities: [{id: N-A, title: A, status: resolved}]
scenarios: [{id: Q-A, question: Why, answer: Claim, given: {x: 1}, then: {x: 2}}]
concepts: [{id: C-A, status: decided, decided_by: owner}]
'''
    result = finish([import_bytes(raw, 'kb/extension.yaml')])
    assert result['semantic_acceptance'] == 'not_granted'
    assert result['publisher_source_coverage'] == 'not_verified'
    assert result['executable_readiness'] == 'not_granted'
    records = result['files'][0]['records']
    assert next(r for r in records if r['kind'] == 'question')['mapping_status'] == 'evaluation_candidate'
    rule = next(r for r in records if r['kind'] == 'rule')
    assert [n['role'] for n in rule['navigation']] == ['navigation', 'navigation']
    assert all(r['semantic_acceptance'] == 'not_granted' and r['executable_readiness'] == 'not_granted' for r in records)


def test_unknown_file_bytes_are_preserved():
    raw = b'\x00\xffarbitrary\r\n'
    f = import_bytes(raw, 'kb/auxiliary.bin')
    assert base64.b64decode(f['raw_base64']) == raw
    assert finish([f])['record_counts'] == {'processed': 0, 'raw': 1, 'error': 0}


@pytest.mark.parametrize('raw', [
    b'terms: [{en: Alpha, definition: 42}]',
    b'rules: [{id: R-A, title: A, flags: [unsupported]}]',
    b'tables: [{id: T-A, title: A, tables: {rows: invalid}}]',
    b'relations: [{from: R-A, to: R-B, type: unsupported, status: verified}]',
])
def test_known_schema_invalid_fields_are_not_processed(raw):
    # WGU kb.schema.json explicitly types/limits these known fields. Preserve
    # extensions, but malformed known structure cannot be reported processed.
    f = import_bytes(raw, 'kb/extension.yaml')
    assert finish([f])['record_counts']['error'] >= 1
    assert base64.b64decode(f['raw_base64']) == raw


def test_schema_valid_confusable_scalar_is_preserved_without_false_error():
    # Pinned termsFile schema defines confusables as an unconstrained array.
    f = import_bytes(b'terms: [{en: Alpha}]\nconfusables: [Alpha, Beta]\n', 'kb/terms.yaml')
    result = finish([f])
    assert result['record_counts']['error'] == 0
    assert len(f['records']) == 3
    assert [r['value'] for r in f['records'] if r['kind'] == 'confusable'] == ['Alpha', 'Beta']
