"""Synthetic contract oracles; no publisher examples or expected gameplay truth."""
import base64
import json

import pytest

from wgc.wgu_adapter.parser import ParseError, parse
from wgc.wgu_adapter.importer import canonical, finish, import_bytes


@pytest.mark.parametrize('raw,line', [
    (b'a: 1\na: 2\n',2),
    (b'outer:\n  a: 1\n  a: 2\n',3),
    (b'a: !!python/object/apply:os.system [echo forbidden]\n',1),
    (b'a: !!python/object:some.Type {}\n',1),
    (b'a: [unclosed\n',2),
    (b'a: {nested: 1, nested: 2}\n',1),
])
def test_yaml_rejections_have_locations_and_never_empty_success(raw,line):
    with pytest.raises(ParseError) as exc:
        parse(raw,'synthetic.yaml')
    assert exc.value.diagnostic['line']==line
    result=finish([import_bytes(raw,'kb/terms.yaml')])
    assert result['record_counts']=={'processed':0,'raw':0,'error':1}
    assert base64.b64decode(result['files'][0]['raw_base64'])==raw


@pytest.mark.parametrize('raw', [b'',b'# comments only\n',b'\xff',
                              b'root: &loop [*loop]\n',b'? [complex, key]\n: value\n',
                              b'default: &d {a: 1}\nother: {<<: *d, a: 2}\n'])
def test_explicit_parse_errors(raw):
    with pytest.raises(ParseError):parse(raw)


def test_alias_expansion_budget(monkeypatch):
    monkeypatch.setattr('wgc.wgu_adapter.parser.MAX_NODES',12)
    with pytest.raises(ParseError,match='budget'):
        parse(b'a: &a [one,two,three]\nb: [*a,*a,*a,*a]\n')


def test_raw_bytes_unicode_fields_and_safe_scalar_types():
    raw='\ufeffa/b:\r\n  ~key: "zażółć"\r\nwhen: 2024-01-02\r\nfloat: .nan\r\nbin: !!binary YWJj\r\n'.encode('utf-8')
    f=import_bytes(raw,'kb/extension.yaml')
    assert base64.b64decode(f['raw_base64'])==raw
    assert f['document']['a/b']['~key']=='zażółć'
    assert f['document']['when']=={'yaml_type':'timestamp','value':'2024-01-02'}
    assert f['document']['bin']=={'yaml_type':'binary','base64':'YWJj'}
    fields={x['field']:x for x in f['fields']}
    assert fields['/a~1b/~0key']['line']==2
    assert fields['/a~1b/~0key']['key_column']==3
    json.loads(canonical(f))


def test_anonymous_terms_and_nested_steps_preserve_numbering_and_extensions():
    raw=b'''terms:
  - en: Sentinel
    extension: {nested: [one, two]}
procedures:
  - id: P-Synthetic
    title: Sequence
    steps:
      - n: 1
        text: First
        substeps:
          - n: "1.a"
            text: Inner
    subprocedures:
      - id: P-Child
        title: Child
        steps:
          - n: "ii"
            text: Last
'''
    f=import_bytes(raw,'kb/extension.yaml'); result=finish([f])
    assert result['kind_counts']=={'procedure':2,'step':3,'term':1}
    assert result['record_counts']=={'processed':6,'raw':0,'error':0}
    term=f['records'][0]
    assert term['external_id'] is None
    assert term['unknown_field_paths']==['/terms/0/extension']
    inner=next(r for r in f['records'] if r['field'].endswith('/substeps/0'))
    assert inner['value']['n']=='1.a'
    assert inner['parent_field']=='/procedures/0/steps/0'
    assert '/terms/0/extension/nested/1' in {x['field'] for x in f['fields']}


def test_duplicate_ids_include_anonymous_terms_with_ids_and_nested_procedures():
    files=[import_bytes(b'terms: [{id: D-Synthetic, en: A}]','kb/terms.yaml'),
           import_bytes(b'procedures: [{id: P-Synthetic, title: A, subprocedures: [{id: D-Synthetic, title: B}]}]','kb/procedures.yaml')]
    result=finish(files)
    assert result['record_counts']=={'processed':1,'raw':0,'error':2}
    assert len(result['duplicate_ids'])==1
    assert [x['field'] for x in result['duplicate_ids'][0]['occurrences']]==['/terms/0','/procedures/0/subprocedures/0']


@pytest.mark.parametrize('raw',[
    b'terms: null',b'terms: {}',b'terms: [null]',b'terms: [en]',
    b'terms: [{en: 123}]',b'terms: [{en: A, refs: nope}]',
    b'procedures: [{id: P-Synthetic, title: A, steps: invalid}]',
    b'procedures: [{id: P-Synthetic, title: A, steps: [{n: false, text: A}]}]',
    b'notes: a',b'[]',b'{}'
])
def test_malformed_records_are_explicit_and_lossless(raw):
    f=import_bytes(raw,'kb/terms.yaml');result=finish([f])
    assert result['record_counts']['error']>0
    assert base64.b64decode(f['raw_base64'])==raw
    assert f['diagnostics']


def test_metadata_navigation_questions_terminology_auxiliary():
    raw=b'''relations: [{from: R-A, to: R-B, type: see, status: verified}]
tables: [{id: T-Synthetic, title: Lookup, complete: true, data: {extension: [a,b]}}]
ambiguities: [{id: N-Synthetic, title: Problem, status: resolved}]
questions: [{id: Q-Synthetic, question: Why, answer: Old answer, then: {x: 2}}]
concepts: [{id: C-Synthetic, source_term: Alpha, novel: preserved}]
unknown: {deep: [x, y]}
'''
    f=import_bytes(raw,'kb/extension.yaml');result=finish([f])
    assert result['record_counts']=={'processed':5,'raw':1,'error':0}
    q=next(r for r in f['records'] if r['kind']=='question')
    assert q['mapping_status']=='evaluation_candidate'
    assert q['value']['answer']=='Old answer'
    assert q['semantic_acceptance']=='not_granted'
    relation=next(r for r in f['records'] if r['kind']=='relation')
    assert relation['value']['status']=='verified'
    assert relation['semantic_acceptance']=='not_granted'
    unknown=next(r for r in f['records'] if r['status']=='raw')
    assert unknown['value']=={'deep':['x','y']}
    binary=import_bytes(b'\x00\xff','kb/notes/raw.dat')
    assert finish([binary])['record_counts']=={'processed':0,'raw':1,'error':0}


def test_repeated_import_is_byte_deterministic():
    raw=b'terms: [{en: Sentinel}]\n'
    assert canonical(finish([import_bytes(raw,'kb/terms.yaml')]))==canonical(finish([import_bytes(raw,'kb/terms.yaml')]))


def test_shared_game_metadata_is_not_duplicate_entity_identity():
    result=finish([import_bytes(b'game: {id: synthetic}\n','wgu.yaml'),
                   import_bytes(b'schema: wgu/kb@1\ngame: {id: synthetic}\n','kb/manifest.yaml')])
    assert result['duplicate_ids']==[]
    assert result['record_counts']=={'processed':0,'raw':3,'error':0}
    assert sum(r['field']=='/game' and r['status']=='raw' for f in result['files'] for r in f['records'])==2


def test_refs_and_see_are_navigation_only():
    f=import_bytes(b'rules: [{id: R-Synthetic, title: A, refs: [R-Other], see: R-Other}]','kb/rules/synthetic.yaml')
    assert [x['role'] for x in f['records'][0]['navigation']]==['navigation','navigation']
    assert f['records'][0]['semantic_acceptance']=='not_granted'
