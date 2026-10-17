"""Reproduce existing R03 pointer mismatches from pinned metadata; do not repair."""
import hashlib,json
from pathlib import Path
R=Path('C:/repo/wargame-compiler');P=Path(__file__).resolve().parent
state=json.loads((P/'preparation.json').read_text(encoding='utf-8')); B=R/state['directories']['reviewed_repair']; scope=json.loads((P/'repair-scope.json').read_text(encoding='utf-8'))
targets={t['key']:t for t in scope['targets']}
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def pin(path):
    raw=path.read_bytes();return dict(path=path.relative_to(R).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def resolve(obj,pointer):
    assert pointer.startswith('/')
    for raw in pointer[1:].split('/'):
        key=raw.replace('~1','/').replace('~0','~')
        if isinstance(obj,list):assert key=='0' or (key.isdigit() and not key.startswith('0'));obj=obj[int(key)]
        else:obj=obj[key]
    return obj
rows=[]
for name in ('affected-component-audit.json','finding-dispositions.json'):
    document=read(B/name)
    if name.startswith('affected'): contexts=[('/targets/'+str(i),row) for i,row in enumerate(document['targets'])]
    else:contexts=[('/findings/'+str(i)+'/targets/'+str(j),row) for i,f in enumerate(document['findings']) for j,row in enumerate(f['targets'])]
    for location,row in contexts:
        target=targets[row['key']];assert row['region_id']==target['region_id'] and row['revision']==target['revision'] and row['after']==target['expected_components']
        for index,binding in enumerate(row['current_changes']):
            reference=read(R/binding['artifact']['path']);before=binding['pointer'];required=target['expected_pointer'] if binding['artifact']['path'].endswith('/author-specifications-final.json') else before
            assert resolve(reference,required)==row['after']
            rows.append(dict(report=pin(B/name),binding_location=location+'/current_changes/'+str(index),expected_key=row['key'],expected_region_id=row['region_id'],expected_revision=row['revision'],artifact=binding['artifact'],declared_pointer=before,required_pointer=required,expected_components=row['after'],before_matches_expected_components=resolve(reference,before)==row['after'],correction_required=before!=required))
assert len(rows)==24 and sum(row['correction_required'] for row in rows)==6 and sum(row['before_matches_expected_components'] for row in rows)==18
result=dict(task='IG-2B02',finding='IG-2B02-R03',purpose='Preparation metadata reproduction only; no report edited and no source content viewed.',bindings=rows,binding_count=24,wrong_occurrences=6,unchanged_correct_occurrences=18,repair_executed=False)
with (P/'binding-expectations.json').open('x',encoding='utf-8',newline='\n') as stream:json.dump(result,stream,indent=2);stream.write('\n')
print('R03 reproduced from metadata: 6 wrong and 18 correct bindings; no repair performed.')
