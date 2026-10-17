"""Synthetic regressions for independent IG1C-R01/R02/R03 findings."""
import base64
import hashlib
import json

import pytest

from wgc.inputs.snapshot import snapshot_manifest, canonical as manifest_bytes
from wgc.wgu_adapter.importer import finish, import_bytes, import_snapshot


@pytest.mark.parametrize('tag,content', [('bool','invalid'),('timestamp','invalid'),
                                       ('int','invalid'),('float','invalid')])
def test_bad_scalars_located(tag,content):
    raw=f'terms:\n  - en: Alpha\n    extension: !!{tag} {content}\n'.encode()
    f=import_bytes(raw,'kb/terms.yaml')
    assert finish([f])['record_counts']=={'processed':0,'raw':0,'error':1}
    assert base64.b64decode(f['raw_base64'])==raw
    d=f['diagnostics'][0]
    assert (d['file'],d['field'],d['line'],d['column'])==('kb/terms.yaml','/terms/0/extension',3,16)


def test_multi_file(tmp_path):
    blobs={'kb/terms.yaml':b'terms: [{en: Alpha, extension: !!bool invalid}]\n',
           'kb/tables.yaml':b'tables: [{id: T-A, title: A, complete: false}]\n',
           'kb/notes/unknown.bin':b'\x00\xff'}
    body={'schema_version':'wgc-input-1','kind':'input_snapshot','origin_root':str(tmp_path.absolute()),
          'source_snapshot_id':'sha256:'+'0'*64,'files':[
              {'path':p,'blob_path':'files/'+p,'availability':'available','role':'kb',
               'edition_label':None,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
              for p,raw in sorted(blobs.items())]}
    m=snapshot_manifest(body);root=tmp_path/('sha256-'+m['snapshot_id'][7:]);root.mkdir()
    (root/'manifest.json').write_bytes(manifest_bytes(m)+b'\n')
    for p,raw in blobs.items():
        dest=root/'files'/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
    result=import_snapshot(root)
    assert result['record_counts']=={'processed':1,'raw':1,'error':1}
    assert {f['path'] for f in result['files']}==set(blobs)
    for f in result['files']:assert base64.b64decode(f['raw_base64'])==blobs[f['path']]


@pytest.mark.parametrize('key,record,field',[
    ('terms','{en: Alpha, definition: 42}','/terms/0/definition'),
    ('terms','{en: Alpha, refs: [1]}','/terms/0/refs/0'),
    ('rules','{id: R-A, title: A, flags: [unsupported]}','/rules/0/flags/0'),
    ('rules','{id: R-A, title: A, source: {translation: [{lines: 42}]}}','/rules/0/source/translation/0/file'),
    ('rules','{id: R-A, title: A, source: {pages: 42}}','/rules/0/source/pages'),
    ('rules','{id: R-A, title: A, digital: {state: [false]}}','/rules/0/digital/state/0'),
    ('tables','{id: T-A, title: A, tables: {rows: invalid}}','/tables/0/tables'),
    ('tables','{id: T-A, title: A, tables: [{rows: [invalid]}]}','/tables/0/tables/0/rows/0'),
    ('tables','{id: T-A, title: A, complete: yesplease}','/tables/0/complete'),
    ('relations','{from: R-A, to: R-B, type: unsupported}','/relations/0/type'),
    ('relations','{from: R-A, to: R-B, type: see, status: accepted}','/relations/0/status'),
    ('ambiguities','{id: N-A, title: A, strength: false}','/ambiguities/0/strength'),
    ('changes','{id: C-A, source: {document: 42}}','/changes/0/source/document'),
    ('scenarios','{id: Q-A, question: Why, answer: 42}','/scenarios/0/answer'),
    ('procedures','{id: P-A, title: A, steps: [{n: 1, text: A, markers: [unsupported]}]}','/procedures/0/steps/0/markers/0'),
])
def test_known_fields_rejected(key,record,field):
    raw=f'{key}: [{record}]\n'.encode();f=import_bytes(raw,'kb/extension.yaml')
    assert f['records'][0]['status']=='error'
    assert base64.b64decode(f['raw_base64'])==raw
    d=next(d for d in f['diagnostics'] if d['field']==field)
    assert d['line']==1 and d['column'] is not None


def test_confusables_are_unconstrained():
    raw=b'''terms: [{en: Alpha}]
confusables: [Alpha, null, 7, false, [one,two], {text: A, extension: {unknown: B}, id: repeated}, {id: repeated}]
'''
    f=import_bytes(raw,'kb/terms.yaml');r=finish([f])
    assert r['record_counts']=={'processed':8,'raw':0,'error':0}
    assert r['duplicate_ids']==[]
    assert [x['value'] for x in f['records'][1:]]==['Alpha',None,7,False,['one','two'],
        {'text':'A','extension':{'unknown':'B'},'id':'repeated'},{'id':'repeated'}]


def test_extensions_and_integer_steps_remain_valid():
    raw=b'''procedures: [{id: P-A, title: "", steps: [{n: 1, text: A, extension: {deep: [one,two]}}]}]
terms: [{en: "", extension: {nested: true}}]
'''
    f=import_bytes(raw,'kb/extension.yaml');r=finish([f])
    assert r['record_counts']=={'processed':3,'raw':0,'error':0}
    assert r['structural_extensions']['step.n']
    assert f['records'][1]['value']['n']==1


def test_embedded_schema_matches_pin():
    from wgc.wgu_adapter.importer import WGU_SCHEMA, WGU_SCHEMA_SHA256
    assert WGU_SCHEMA_SHA256=='0a93858ed3e0d99382ea962350e3b2994fab90b872a8b86584519b5a9e33a551'
    assert WGU_SCHEMA['$defs']['termsFile']['properties']['confusables']=={'type':'array'}
    assert WGU_SCHEMA['$defs']['step']['properties']['n']=={'type':'string'}


@pytest.mark.parametrize('path,raw,field',[
    ('kb/terms.yaml', b'terms: [{en: Alpha}]\nnotes: 42\n', '/notes'),
    ('kb/rules/synthetic.yaml', b'chapter: {title: 42}\nrules: [{id: R-A, title: A}]\n','/chapter/title'),
    ('kb/rules/synthetic.yaml', b'rules: []\n', '/chapter'),
    ('kb/procedures.yaml', b'legend: false\nprocedures: []\n','/legend'),
    ('kb/manifest.yaml', b'schema: wrong\ngame: {}\n', '/schema')
])
def test_file_metadata_contract(path,raw,field):
    f=import_bytes(raw,path);r=finish([f])
    assert r['record_counts']['error']>0
    assert base64.b64decode(f['raw_base64'])==raw
    d=next(d for d in f['diagnostics'] if d['field']==field)
    assert d['line'] is not None
