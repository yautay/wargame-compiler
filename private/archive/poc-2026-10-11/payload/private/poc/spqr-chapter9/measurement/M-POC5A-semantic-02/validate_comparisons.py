"""Consistency/integrity audit for additive proposals; not semantic acceptance."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
OUT=P/'reviews/semantic-01/part-02'

def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def resolve(obj,pointer):
    for k in pointer.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~')
        obj=obj[int(k)] if isinstance(obj,list) else obj[k]
    return obj

start=load(M/'start.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
base=load(P/'reviews/semantic-01/checklist.json')
data=load(OUT/'comparisons.json')
assert data['base_checklist']==ref(P/'reviews/semantic-01/checklist.json')
assert data['evaluation']==base['evaluation'] and data['responses']==base['responses']
assert data['owner_decisions']==[]
assert len(data['expectations'])==25
assert [r['id'] for r in data['expectations']]==[f'EXP-{n:03}' for n in range(1,26)]
assert Counter(r['classification'] for r in data['expectations'])=={'confirmed_local_content_scope':23,'requires_context':2}
assert len(data['inventory'])==42 and len(data['categories'])==88
assert len({r['base_item']['id'] for r in data['inventory']})==42
assert len({r['base_unit']['id'] for r in data['categories']})==88
for row,frozen in zip(data['expectations'],base['expectations'][:25]):
    for field in ['id','source_scope','source_evidence','criticality','limits','inventory_refs']:
        assert row[field]==frozen[field],(row['id'],field)
    assert row['human_status']=='pending' and row['human_reviewer'] is None and row['result']=='not_assessable'
    assert row['mapped_content_identical_between_runs'] is True
trace_counts={}
for run,response in data['responses'].items():
    raw=(ROOT/response['path']).read_bytes();assert ref(ROOT/response['path'])==response
    obj=json.loads(raw);traces=set()
    for row in data['expectations']:
        r=row['runs'][run]
        assert r['response']==response and r['status']=='pending' and r['human_reviewer'] is None
        assert r['meaning_result']=='not_assessable'
        for rid,t in r['output_trace'].items():
            assert resolve(obj,t['pointer'])==t['original_record']
            span=t['raw_span'];piece=raw[span['start_byte']:span['end_byte_exclusive']]
            assert hashlib.sha256(piece).hexdigest()==span['sha256']
            assert json.loads(piece)==t['original_record']
            traces.add(rid)
    trace_counts[run]=len(traces)
    # Unchanged source/operator records, not necessarily unchanged JSON lexical bytes.
    for row in data['expectations']:
        for rid in base['expectations'][int(row['id'][4:])-1]['runs'][run]['output_record_ids']:
            assert base['output_records']['first-001'][rid]['original_record']==base['output_records']['context-01'][rid]['original_record']
for r in data['inventory']:
    assert r['status']=='pending' and r['human_reviewer'] is None
for r in data['categories']:
    assert r['status']=='pending' and r['result']=='not_assessable' and r['human_reviewer'] is None
manifest=load(OUT/'manifest.json')
for r in manifest['artifacts']:assert ref(ROOT/r['path'])==r,r['path']
current=load(P/'reviews/semantic-01/current-state-02.json')
assert current['overlay']==ref(OUT/'manifest.json')
assert current['owner_decisions']==[]
issue=load(OUT/'issues.json')['issues'][0]
assert issue['id']=='SEM-009' and issue['status']=='pending' and issue['human_reviewer'] is None
for run in data['responses']:
    assert issue['evidence'][run]==data['expectations'][18]['runs'][run]['output_trace']
before=start['sessions_before']
sessions=(P/'measurement/sessions.jsonl').read_bytes()
assert len(sessions)==before['bytes'] and hashlib.sha256(sessions).hexdigest()==before['sha256']
result=dict(result='passed',protected_files=len(start['protected']),previous_session_prefix_unchanged=True,
    expectations=25,inventory_source_items=42,diagnostic_category_units=88,verified_distinct_traces=trace_counts,
    owner_decisions=0,semantic_metrics='not_assessable',source_expansion=0,
    visual_scope=['pdf-31-core-right','pdf-32-core-left','pdf-32-core-right','pdf-33-core-left','pdf-33-core-right'],
    visual_limits='Source-scope comparison only; no complete glyph or graphic-number certificate.')
assert not (M/'validation.json').exists()
(M/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
