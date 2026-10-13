"""Validate new evidence traces and retain the prior exact owner acceptance."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01'
OUT=REV/'part-03'
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def resolve(obj,pointer):
    for k in pointer.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
    return obj

start=load(M/'start.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
C=load(REV/'checklist.json');D=load(OUT/'comparisons.json')
decision=load(REV/'owner-decision-01.json')
assert len(decision['scopes'])==22
assert D['prior_owner_decision']==ref(REV/'owner-decision-01.json')
assert D['owner_decisions']==[] and D['summary']['previous_owner_accepted_groups_per_answer']==22
assert D['evaluation']==C['evaluation'] and D['responses']==C['responses']
assert [e['id'] for e in D['expectations']]==[f'EXP-{n:03}' for n in range(26,51)]
assert Counter(e['classification'] for e in D['expectations'])=={'confirmed_local_content_scope':22,'requires_context':3}
assert Counter(e['proposed_assessment'] for e in D['expectations'])=={
    'supported_local_scope':21,'source_block_supported':2,'incomplete_local_interpretation_pending_source_availability':1,
    'partial_context_declaration_pending':1}
assert len(D['inventory'])==44 and len(D['categories'])==94
assert len({r['base_item']['id'] for r in D['inventory']})==44
assert len({r['base_unit']['id'] for r in D['categories']})==94
assert set(e['id'] for e in D['expectations']).isdisjoint(e['id'] for e in decision['scopes'])
for e,old in zip(D['expectations'],C['expectations'][25:50]):
    for key in ['id','source_scope','source_evidence','inventory_refs','criticality','limits']:
        assert e[key]==old[key],(e['id'],key)
    assert e['human_status']=='pending' and e['human_reviewer'] is None and e['result']=='not_assessable'
    assert e['whole_record_accepted'] is False
traces={}
for run,response in D['responses'].items():
    raw=(ROOT/response['path']).read_bytes();assert ref(ROOT/response['path'])==response;obj=json.loads(raw)
    ids=set()
    for e in D['expectations']:
        r=e['runs'][run]
        assert r['response']==response and r['evaluation']==C['evaluation']
        assert r['status']=='pending' and r['human_reviewer'] is None and r['meaning_result']=='not_assessable'
        for rid,t in r['output_trace'].items():
            assert t==C['output_records'][run][rid]
            assert resolve(obj,t['pointer'])==t['original_record']
            s=t['raw_span'];piece=raw[s['start_byte']:s['end_byte_exclusive']]
            assert hashlib.sha256(piece).hexdigest()==s['sha256'] and json.loads(piece)==t['original_record']
            ids.add(rid)
    traces[run]=len(ids)
for r in D['inventory']+D['categories']:assert r['status']=='pending' and r['human_reviewer'] is None
assert D['summary']['mapped_record_count']==26 and D['summary']['mapped_value_identical_count']==24
assert D['summary']['changed_mapped_record_ids']==['N932ex','R932']
e40=next(r for r in D['expectations'] if r['id']=='EXP-040')
assert e40['proposed_assessment']=='incomplete_local_interpretation_pending_source_availability'
for run in C['responses']:
    assert e40['runs'][run]['output_trace']['G953']['original_record']['blocking'] is True
    e42=next(r for r in D['expectations'] if r['id']=='EXP-042')
    assert e42['runs'][run]['output_trace']['G-D962shock']['original_record']['blocking'] is True
issue=load(OUT/'issues.json')['issues'][0]
assert issue['id']=='SEM-010' and issue['status']=='pending' and issue['human_reviewer'] is None
assert 'SEM-009' in load(OUT/'issues.json')['inherited_pending']
manifest=load(OUT/'manifest.json')
for r in manifest['artifacts']:assert ref(ROOT/r['path'])==r,r['path']
current=load(REV/'current-state-04.json')
assert current['overlay']==ref(OUT/'manifest.json') and current['no_new_owner_decisions'] is True
assert current['owner_accepted_local_groups_per_answer']==22 and current['remaining_uncompared_expectations']==24
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(result='passed',protected_files=len(start['protected']),previous_measurement_prefix_preserved=True,
    new_expectations=25,source_inventory_items=44,diagnostic_category_units=94,verified_distinct_traces=traces,
    new_owner_decisions=0,prior_owner_accepted_groups_per_answer=22,all_old_pending_preserved=True,
    all_full_metrics='not_assessable',source_expansion=0,
    visual_scope=['pdf-33-core-right','pdf-34-core-left','pdf-34-core-right','pdf-35-core-left','pdf-35-core-right','8.46-step-4-pdf-27'],
    visual_limit='Exact source scopes/text and panel layout only; no full glyph, counter identity or graphic-rating certificate.')
target=M/'validation.json';assert not target.exists();target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
