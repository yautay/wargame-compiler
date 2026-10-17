"""Independent frozen-file / record / field accounting, not adapter counters."""
import base64, hashlib, json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'src'))
import yaml
from wgc.wgu_adapter.importer import import_snapshot, canonical

ROOT=Path('private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df')
OUT=Path('private/ig/projects/spqr/runs/import/ig1c-20261013')
OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'manifest.json').read_text())
result=import_snapshot(ROOT)
assert {f['path'] for f in result['files']}=={f['path'] for f in manifest['files']}
ledger=[]; expected_total=Counter(); field_total=0
def escape(k):return str(k).replace('~','~0').replace('/','~1')
def fields(value,p=''):
    yield p
    if isinstance(value,dict):
        for k,v in value.items():yield from fields(v,p+'/'+escape(k))
    elif isinstance(value,list):
        for i,v in enumerate(value):yield from fields(v,p+'/'+str(i))
def records(value):
    out=[]
    kinds={'rules':'rule','terms':'term','procedures':'procedure','tables':'table','relations':'relation','ambiguities':'ambiguity','changes':'change','scenarios':'question','questions':'question','concepts':'terminology','confusables':'confusable'}
    def nested(v,p,kind):
        out.append((p,kind,v))
        if kind in ('procedure','step'):
            for k,t in [('steps','step'),('substeps','step'),('subprocedures','procedure')]:
                if k in v:
                    assert isinstance(v[k],list)
                    for i,child in enumerate(v[k]):nested(child,p+'/'+k+'/'+str(i),t)
    for k,v in value.items():
        if k in kinds:
            assert isinstance(v,list)
            for i,x in enumerate(v):nested(x,'/'+k+'/'+str(i),kinds[k])
        else:out.append(('/'+escape(k),'auxiliary',v))
    return out
for item in manifest['files']:
    f=next(f for f in result['files'] if f['path']==item['path'])
    if item['availability']=='missing':
        assert f['records']==[] and f['raw_base64'] is None
        ledger.append({'path':item['path'],'availability':'missing','record_count':0});continue
    raw=(ROOT/item['blob_path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==item['sha256']
    assert base64.b64decode(f['raw_base64'])==raw
    if item['path'].endswith('.yaml'):
        independent=yaml.safe_load(raw)
        # This corpus uses only JSON-safe types; fail instead of normalizing silently.
        assert f['document']==independent
        paths=list(fields(independent)); assert len(paths)==len(f['fields'])
        assert set(paths)=={x['field'] for x in f['fields']}
        expected=records(independent)
        actual={(r['field'],r['kind']):r for r in f['records']}
        assert len(expected)==len(actual)==len(f['records'])
        for pointer,kind,value in expected:assert actual[(pointer,kind)]['value']==value
        field_total+=len(paths)
    else:
        expected=[('', 'auxiliary',None)];paths=[]
        assert len(f['records'])==1 and f['records'][0]['status']=='raw'
    expected_total.update(kind for _,kind,_ in expected)
    ledger.append({'path':item['path'],'sha256':item['sha256'],'bytes':len(raw),'availability':'available','record_count':len(expected),'field_count':len(paths),'records':[{'field':p,'kind':k} for p,k,_ in expected]})
assert dict(sorted(expected_total.items()))==result['kind_counts']
assert sum(expected_total.values())==result['record_total']
assert result['record_counts']['error']==0, result['record_counts']
second=import_snapshot(ROOT)
assert canonical(result)==canonical(second)
report={'result':'pass','independent_file_count':len(ledger),'available_files':sum(x['availability']=='available' for x in ledger),'missing_files':sum(x['availability']=='missing' for x in ledger),'available_bytes':sum(x.get('bytes',0) for x in ledger),'independent_record_count':sum(expected_total.values()),'independent_kind_counts':dict(sorted(expected_total.items())),'independent_field_count':field_total,'processed_raw_error':result['record_counts'],'all_unknown_fields_preserved':True,'two_imports_byte_identical':True,'ledger':ledger,'semantic_acceptance':'not_granted','source_coverage':'not_verified','executable_readiness':'not_granted'}
for name,data in [('import.json',canonical(result)+b'\n'),('independent-accounting.json',canonical(report)+b'\n')]:
    with (OUT/name).open('xb') as f:f.write(data)
print(json.dumps({k:v for k,v in report.items() if k!='ledger'}))
