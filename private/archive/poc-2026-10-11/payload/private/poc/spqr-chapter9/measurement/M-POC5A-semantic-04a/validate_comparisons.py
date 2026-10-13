"""Verify frozen inputs, lexical provenance and pending boundaries; not meaning."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent;REV=P/'reviews/semantic-01';OUT=REV/'part-04a'
sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def resolve(o,pointer):
    if not pointer:return o
    for k in pointer.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');o=o[int(k)] if isinstance(o,list) else o[k]
    return o
def span_check(raw,obj,pointer,s,value=None):
    b=raw[s['start_byte']:s['end_byte_exclusive']]
    assert hashlib.sha256(b).hexdigest()==s['sha256'],pointer
    v=resolve(obj,pointer)
    assert json.loads(b)==v,pointer
    if value is not None:assert v==value,pointer
start=load(M/'start.json'); D=load(OUT/'comparisons.json'); C=load(REV/'checklist.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
read=load(M/'read-inputs.json')
assert read['required_files']==56
for r in read['files']:assert ref(ROOT/r['path'])==r,r['path']
manifest_counts={}
for rel,base in [('inputs/v1/manifest.json',P),('transfer/context-v1/context/pass-01/manifest.json',P/'transfer/context-v1'),('evaluation/eval-v1/manifest.json',ROOT),('reports/first-001/manifest.json',ROOT),('reports/context-01/manifest.json',ROOT)]:
    m=load(P/rel)
    for r in m['artifacts']:
        b=(base/r['path']).read_bytes()
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
    manifest_counts[rel]=len(m['artifacts'])
assert D['owner_decisions']==[] and D['summary']['owner_accepted_local_groups_per_answer']==43
assert D['summary']['reviewed_context_requirements_per_answer']==2
assert D['prior_state']==ref(REV/'current-state-05.json')
assert D['evaluation']==C['evaluation'] and D['responses']==C['responses']
for r in [D['evaluation'],D['source'],D['prior_owner_overlay']]+D['prior_owner_decisions']:assert ref(ROOT/r['path'])==r
assert [e['id'] for e in D['expectations']]==[f'EXP-{n:03}' for n in range(51,75)]
assert Counter(e['classification'] for e in D['expectations'])=={'confirmed_local_content_scope':21,'requires_context':3}
E=load(P/'evaluation/eval-v1/expectations.json');trace_counts={};prov_counts={};field_counts={}
for run,response in D['responses'].items():
    assert ref(ROOT/response['path'])==response
    raw=(ROOT/response['path']).read_bytes();obj=json.loads(raw)
    assert (P/f'proposals/{run}/proposal.json').read_bytes()==raw
    pr=load(P/f'proposals/{run}/provenance.json')
    for pointer,s in pr['json_value_spans'].items():span_check(raw,obj,pointer,s)
    prov_counts[run]=len(pr['json_value_spans']);ids=set();fc=0
    for e,old in zip(D['expectations'],C['expectations'][50:74]):
        n=int(e['id'].split('-')[1]); frozen=E['expectations'][n-1]
        assert e['source_scope']==frozen['reviewed_scope']
        for k in ['id','classification','criticality','source_evidence','inventory_refs','limits','source_scope']:assert e[k]==old[k]
        assert e['human_status']=='pending' and e['human_reviewer'] is None and e['result']=='not_assessable'
        assert not e['whole_record_accepted']
        r=e['runs'][run]
        assert r['status']=='pending' and r['human_reviewer'] is None and r['meaning_result']=='not_assessable'
        assert r['response']==response
        for rid,t in r['output_trace'].items():
            assert t==C['output_records'][run][rid]
            span_check(raw,obj,t['pointer'],t['raw_span'],t['original_record']);ids.add(rid)
        for rid,fields in r['field_trace'].items():
            for f,t in fields.items():span_check(raw,obj,t['pointer'],t['raw_span'],t['original_value']);fc+=1
        for v in e['source_evidence']:
            assert v['source_sha256']==D['source']['sha256']
            assert hashlib.sha256((P/v['render']).read_bytes()).hexdigest()==v['render_sha256']
    trace_counts[run]=len(ids);field_counts[run]=fc
assert D['summary']['mapped_record_count']==26 and D['summary']['mapped_value_identical_count']==26
assert len(D['inventory'])==31 and len(D['categories'])==95
for r in D['inventory']+D['categories']:assert r['status']=='pending' and r['human_reviewer'] is None
issues=load(OUT/'issues.json')
assert [i['id'] for i in issues['issues']]==['SEM-011','SEM-012','SEM-013']
assert issues['inherited_pending']==[f'SEM-{n:03}' for n in range(1,11)]
for i in issues['issues']:assert i['status']=='pending' and i['human_reviewer'] is None
for run in D['responses']:
    e64=D['expectations'][13]
    for g in ['G-D994scenario','G-D995scenario']:assert e64['runs'][run]['output_trace'][g]['original_record']['blocking'] is True
    e66=D['expectations'][15]
    assert e66['runs'][run]['output_trace']['G-D996tables']['original_record']['blocking'] is False
    assert e66['runs'][run]['output_trace']['D996tables']['original_record']['impact_if_missing']['blocks_full_result'] is False
for r in load(OUT/'manifest.json')['artifacts']:assert ref(ROOT/r['path'])==r,r['path']
cur=load(REV/'current-state-06.json'); old=load(REV/'current-state-05.json')
assert cur['proposal_overlay']==ref(OUT/'manifest.json')
assert cur['pending_expectation_ids']==load(REV/'owner-review-overlay-02.json')['pending_expectation_ids']
assert cur['owner_accepted_local_groups_per_answer']==old['owner_accepted_local_groups_per_answer']==43
assert not cur['M_POC5A_closed'] and not cur['M_POC5A_4_closed']
assert cur['new_owner_decisions']==[] and cur['remaining_uncompared_expectations']==0
result=dict(result='passed',protected_files=len(start['protected']),previous_measurement_prefix_preserved=True,required_inputs_read=56,manifest_artifact_counts=manifest_counts,all_provenance_values_checked=prov_counts,verified_distinct_record_traces=trace_counts,verified_field_trace_occurrences=field_counts,new_expectations=24,source_inventory_items=31,diagnostic_category_units=95,new_owner_decisions=0,accepted_local_scopes_per_answer=43,reviewed_context_requirements_per_answer=2,still_pending_expectations=29,all_prior_pending_preserved=True,full_metrics='not_assessable',visual_scope=['pdf-31-core-right','pdf-33-core-right','pdf-35-core-left','pdf-35-core-right','pdf-36-core-left','pdf-36-core-right','pdf-37-core-left'],visual_limit='Exact operative text and illustration roles/states; no tiny ratings, identity mapping or glyph-boundary certification.',tooling_diagnostic='A diagnostic print attempted slicing a provenance dict and raised KeyError before modifying any data. The dict shape was then inspected; full span audit follows its actual mapping.')
target=M/'validation.json';assert not target.exists();target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
