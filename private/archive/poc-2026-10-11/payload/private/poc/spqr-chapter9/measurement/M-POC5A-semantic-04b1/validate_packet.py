"""Evidence/coverage checks only. Never certify semantic correctness."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[5]; P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;OUT=P/'reviews/semantic-01/part-04b1'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def resolve(o,ptr):
    if ptr=='':return o
    for k in ptr.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');o=o[int(k)] if isinstance(o,list) else o[k]
    return o
def spancheck(raw,s,value=None):
    b=raw[s['start_byte']:s['end_byte_exclusive']]
    assert sha(b)==s['sha256']
    if value is not None:assert json.loads(b)==value
packet=load(OUT/'comparisons.json');plan=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json')
assert [r['id'] for r in packet['relationships']]==plan['parts'][0]['output_edge_ids']
assert len(set(r['id'] for r in packet['relationships']))==65
raw={r:(ROOT/v['path']).read_bytes() for r,v in packet['responses'].items()}
original={r:json.loads(b) for r,b in raw.items()}
span_count=0;trace_count=0;source_count=0
for r in raw:
    assert len(raw[r])==packet['responses'][r]['bytes'] and sha(raw[r])==packet['responses'][r]['sha256']
    prov=load(P/f'proposals/{r}/provenance.json')
    for ptr,s in prov['json_value_spans'].items():
        spancheck(raw[r],s,resolve(original[r],ptr));span_count+=1
    occ=[e for e in original[r]['dependencies'] if e['id'] in plan['parts'][0]['output_edge_ids']]
    compared=[row['runs'][r] for row in packet['relationships'] if row['runs'][r]['record_present']]
    assert len(occ)==len(compared)=={'first-001':60,'context-01':65}[r]
    assert all(x['evaluator_compared'] and x['reviewer'] and x['status']=='waiting_review' for x in compared)
    for row in packet['relationships']+packet['frozen_tuple_comparisons']:
        for t in row['runs'][r].get('output_trace',{}).values():
            assert resolve(original[r],t['pointer'])==t['original_record']
            spancheck(raw[r],t['raw_span'],t['original_record']);trace_count+=1
            for k,v in t['fields'].items():
                assert resolve(original[r],v['pointer'])==v['original_value']
                spancheck(raw[r],v['raw_span'],v['original_value'])
        for ev in row['runs'][r].get('bounded_independent_source',[]):
            a=ev['artifact'];assert sha((ROOT/a['path']).read_bytes())==a['sha256']
            if 'character_range' in ev:
                text=resolve(load(ROOT/a['path']),ev['pointer']);s,e=ev['character_range'];assert text[s:e]==ev['literal_helper_text']
            else:assert (ROOT/a['path']).read_text(encoding='utf-8')==ev['literal_helper_text']
            source_count+=1
assert len(packet['frozen_tuple_comparisons'])==22
cats={k:sum(1 for f in packet['frozen_tuple_comparisons'] if f['category']==k) for k in ['confirmed_execution_relations','mentions','continuations']}
assert cats==dict(confirmed_execution_relations=8,mentions=7,continuations=7)
for r in raw:
    # Independently search all original dependencies, not only historical candidate map.
    for fr,to,kind in [('R972','R971','condition'),('N914table','R914','exception'),('R986','R914','condition')]:
        assert not any(e['from']==fr and e['to']==to and e['kind']==kind for e in original[r]['dependencies'])
    for fr,name in [('N923ex','Shock'),('N932ex','Shock'),('N914diagram','compass'),('R966','Orderly Withdrawal')]:
        assert not any(e['from']==fr and e['kind']=='mention' and name.lower() in json.dumps(e.get('target_candidate'),ensure_ascii=False).lower() for e in original[r]['dependencies'])
pos=packet['summary']['positive_bounded_ids'];issues=packet['summary']['separate_issue_ids']
assert not set(pos)&set(issues) and set(pos)|set(issues)==set(plan['parts'][0]['output_edge_ids'])
positive_occ=sum(len([e for e in original[r]['dependencies'] if e['id'] in pos]) for r in raw)
assert positive_occ==116
for part in plan['parts'][1:]:
    assert not set(pos+issues)&set(part['output_edge_ids'])
for a in load(OUT/'manifest.json')['artifacts']:
    b=(ROOT/a['path']).read_bytes();assert len(b)==a['bytes'] and sha(b)==a['sha256']
state=load(P/'reviews/semantic-01/current-state-09.json');old=load(P/'reviews/semantic-01/current-state-08.json')
for k in ['decision','overlay','evaluation','responses','pending_expectation_ids','pending_local_ids','pending_context_ids']:
    assert state[k]==old[k]
result=dict(status='passed',semantic_acceptance=False,provenance_spans_verified=span_count,traces_verified=trace_count,bounded_source_blocks_verified=source_count,
            assignment_unique_ids=65,assignment_occurrences=125,positive_bounded_occurrences=116,separate_issue_occurrences=9,frozen_tuple_categories=cats,
            missing_record_search='all original dependency records, both answers;prose separately compared by evaluator',remaining_assigned_occurrences=132,
            protected_owner_state_unchanged=True)
f=M/'validation.json';assert not f.exists();f.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
