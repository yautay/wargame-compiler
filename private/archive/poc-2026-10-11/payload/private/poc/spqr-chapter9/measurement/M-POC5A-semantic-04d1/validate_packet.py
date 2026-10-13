"""Independent lineage, factual examples, bounded scope and immutable history checks."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';O=R/'part-04d1'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def resolve(x,pointer):
    for k in pointer.lstrip('/').split('/') if pointer else []:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
c=load(O/'comparisons.json');mf=load(O/'manifest.json');plan=load(M/'scope-plan.json');a=load(M/'annotations.json');s=load(R/'current-state-22.json');prior=load(R/'current-state-21.json');inv=load(P/'evaluation/eval-v1/inventory.json');checklist=load(R/'checklist.json')
for x in [c['source'],c['evaluation'],*c['responses'].values(),*mf['artifacts'],mf['manual_annotations'],mf['scope_plan'],mf['estimate'],mf['source_views'],mf['estimate_arithmetic_note'],*load(M/'owner-decision-artifacts.json')['artifacts'],*load(M/'public-document-artifacts.json'),*load(M/'packet-artifacts.json').values()]:assert ref(ROOT/x['path'])==x
assert c['source']['sha256']=='e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
assert c['evaluation']['sha256']=='7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce'
raws={r:(ROOT/x['path']).read_bytes() for r,x in c['responses'].items()};parsed={r:json.loads(b) for r,b in raws.items()}
assert len(raws['first-001'])==617941 and sha(raws['first-001'])=='3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307'
assert len(raws['context-01'])==712014 and sha(raws['context-01'])=='95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b'
records=fields=0
def tracecheck(run,t):
    global records,fields
    def field(span,value,pointer):
        b=raws[run][span['start_byte']:span['end_byte_exclusive']]
        assert sha(b)==span['sha256'] and json.loads(b)==value and resolve(parsed[run],pointer)==value
    field(t['raw_span'],t['original_record'],t['pointer']);records+=1
    for f in t['fields'].values():field(f['raw_span'],f['original_value'],f['pointer']);fields+=1
ids=[x['id'] for x in c['inventory']];assert ids==plan['parts'][0]['inventory_ids']==[x[0] for x in a['rows']]
assert plan['before_semantic_review'] and [len(x['inventory_ids']) for x in plan['parts']]==[39,68,59,41,0]
allids=[iid for part in plan['parts'] for iid in part['inventory_ids']];assert len(allids)==len(set(allids))==207 and set(allids)=={x['id'] for x in inv['items']}
assert sum(p['minutes_range'][0] for p in plan['parts'])==330 and sum(p['minutes_range'][1] for p in plan['parts'])==430
assert plan['parts'][0]['minutes_range']==[70,85] and all(p['minutes_range'][1]<=90 for p in plan['parts'])
for n in range(1,6):assert (ROOT/f'docs/work/tasks/semantic/M-POC5A.4d{n}.md').exists()
unique={r:set() for r in c['responses']};count={r:0 for r in c['responses']};child=0;source_ranges=0
overlay=load(R/'owner-review-overlay-10.json')
for row,note in zip(c['inventory'],a['rows']):
    assert row['manual_assessment']==note[1] and row['manual_comparison']==note[2]
    assert row['status']=='waiting_review' and row['human_reviewer'] is None and not row['whole_record_accepted']
    frozen=resolve(inv,row['evaluation_pointer']);assert frozen==row['frozen_inventory_item']
    expected=frozen.get('source_transcription');child+=expected is not None
    for src in row['source_scopes']:
        for x in [src['helper'],src['evaluation_inventory'],src['source_visual']]:assert ref(ROOT/x['path'])==x
        helper=(ROOT/src['helper']['path']).read_text(encoding='utf-8-sig');begin,end=src['helper_character_range'];literal=src['literal_scope']
        assert helper[begin:end]==literal and sha(literal.encode())==src['literal_scope_sha256']
        assert literal==(expected if expected is not None else src['original_evidence']['transcription'])
        assert src['original_evidence'] in frozen['evidence'] and src['parent_envelope_not_child_certificate'];source_ranges+=1
    for run,rr in row['runs'].items():
        count[run]+=1
        assert rr['evaluator_compared'] and rr['status']=='waiting_review' and rr['human_reviewer'] is None and rr['owner_decision'] is None and not rr['whole_record_accepted']
        assert rr['source_scopes']==row['source_scopes'] and rr['mapping_not_semantic_proof']
        assert [t['original_record']['id'] for t in rr['output_traces']]==checklist['inventory'][int(row['evaluation_pointer'].split('/')[-1])]['runs'][run]['output_record_ids']
        for t in rr['output_traces']:unique[run].add(t['original_record']['id'])
        for t in rr['output_traces']+rr['evidence_traces']+rr['gap_traces']+rr['central_statement_evidence']:tracecheck(run,t)
        for z in rr['prior_local_scopes']+rr['prior_context_requirements']:
            assert ref(ROOT/z['artifact']['path'])==z['artifact'] and resolve(overlay,z['pointer'])==z['prior_scoped_decision']
    vals=[[t['original_record'] for t in row['runs'][run]['output_traces']] for run in c['responses']]
    assert row['mapped_records_equal_between_runs']==(vals[0]==vals[1])
    assert row['mapped_records_equal_between_runs']==(row['id']!='X-04')
assert count=={'first-001':39,'context-01':39} and all(len(x)==33 for x in unique.values()) and child==9
byid={x['id']:x for x in c['inventory']};n5=byid['N-05']
assert n5['source_scopes'][0]['literal_scope']=='HISTORICAL NOTE: Elephants did not fight in formations.'
for run in c['responses']:
    rr=n5['runs'][run];content=rr['output_traces'][0]['original_record']['content']['value'];quote=rr['central_statement_evidence'][0]['original_record']['quote']['value']
    assert content=='Historical statement; no additional formation procedure inferred.' and quote=='Elephants did not fight in formations.' and quote in n5['source_scopes'][0]['literal_scope']
    assert 'did not fight' not in content
    def data(iid):return byid[iid]['runs'][run]['output_traces'][0]['original_record']['content']['value']['transcription']
    v=data('N-04');assert v['counter_scale']==5 and '1 or 2 elephants' in v['rampage_representation']
    v=data('X-03');assert v['cases']==[{'Hastati':['2808','2810'],'Velites':['2809'],'line':'eligible'},{'Hastati':['2808','2811'],'Velites':['2809','2810'],'line':'not formed by the two Hastati'},{'Hastati':['2808','2810','2812'],'Velites':['2809','2811'],'line':'could form'}]
    v=data('X-05');assert v['attackers']=='2 LGs' and v['columns']=={'start':5,'shift':'4L','end':1} and v['assumption']=='no other adjustments'
    assert v['approximate_hits']=={'PH':'1, maybe 2','each_LG':'2 or 3'}
issues=load(O/'issues.json');assert len(issues['new_issues'])==1 and issues['new_issues'][0]['id']=='SEM-020' and issues['new_issues'][0]['runs']==n5['runs'] and issues['new_issues'][0]['status']=='waiting_review'
pres=load(O/'presentation.json');assert pres['decisions'][0]['occurrences']==76 and pres['decisions'][0]['ids']==[x for x in ids if x!='N-05'] and pres['decisions'][1]['occurrences']==2
summary=c['summary'];assert summary['bounded_supported_inventory_occurrences']+summary['qualified_summary_omission_occurrences']==summary['evaluator_compared_occurrences']==summary['owner_pending_occurrences']==78
assert summary['new_owner_reviewed_occurrences']==0 and summary['structured_transcription_observations_occurrences']==6 and summary['remaining_assigned_inventory_ids']==168 and summary['remaining_assigned_inventory_occurrences']==336
d=load(R/'owner-decision-10.json');oldo=load(R/'owner-review-overlay-09.json');oldpacket=load(R/'part-04c3/comparisons.json');oldloc={x['id']:x for x in oldpacket['locators']};accepted=0
assert d['owner_reply_verbatim']=='Zatwierdzam i kontynuuj' and d['newly_reviewed_locator_occurrences']==38 and d['per_answer']=={'first-001':16,'context-01':22}
for row in d['scopes']:
    b=oldloc[row['id']]
    for key in ['source_scope','source_quote_original','independent_source_helper','source_image']:assert row[key]==b[key]
    assert not row['whole_evidence_record_accepted'] and not row['original_locator_repaired']
    for run,rr in row['runs'].items():assert rr['output_trace']==b['runs'][run]['output_trace'];tracecheck(run,rr['output_trace']);accepted+=1
assert accepted==38 and d['readable_raster_without_observed_ink_loss']==36 and d['readable_with_descenders_clipped']==2
for run,v in overlay['runs'].items():
    old=oldo['runs'][run]
    for key in old:
        if key not in ['locator_scopes','owner_reviewed_locator_scoped_occurrences','assigned_remaining_unreviewed_locator_occurrences']:assert v[key]==old[key]
    assert v['locator_scopes'][:43]==old['locator_scopes'] and len(v['locator_scopes'])==(59 if run=='first-001' else 65) and v['assigned_remaining_unreviewed_locator_occurrences']==0
for key in ['category_units','category_accepted_scope_counts','pending_expectation_ids','illustration_states','all_output_edges_review','relationship_owner_decision','relation_facet_decisions']:assert overlay[key]==oldo[key]
assert len(overlay['category_units'])==264 and overlay['accepted_relation_scoped_occurrences']==257
assert s['pending_expectation_ids']==prior['pending_expectation_ids'] and len(s['pending_expectation_ids'])==8
assert s['unresolved_issue_ids']==prior['unresolved_issue_ids']+['SEM-020'] and s['issue_dispositions']==prior['issue_dispositions']
assert s['decision']==ref(R/'owner-decision-10.json') and s['relationship_owner_decision']==ref(R/'owner-decision-07.json') and s['expectation_owner_decision']==ref(R/'owner-decision-03.json')
assert s['locator_owner_reviewed_occurrences']==124 and s['locator_owner_pending_compared_occurrences']==0 and s['owner_accepted_relationship_occurrences']==257
assert s['inventory_evaluator_compared_assigned_occurrences']==78 and s['inventory_remaining_assigned_occurrences']==336 and s['next_part']=='M-POC5A.4d2'
assert not any(s[k] for k in ['M_POC5A_closed','M_POC5A_4_closed','M_POC5A_4b_closed','M_POC5A_4c_closed','M_POC5A_4d_closed'])
start=load(M/'start.json');changed=[x['path'] for x in start['protected'] if not (ROOT/x['path']).exists() or ref(ROOT/x['path'])!=x];assert not changed,changed
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(status='passed',inventory_occurrences_verified=78,source_scopes_verified=source_ranges,child_scopes_verified=child,unique_mapped_records_per_answer={r:len(x) for r,x in unique.items()},raw_records_verified=records,raw_fields_verified=fields,
    source_content_summary_omission2_verified=True,structured_facts6_verified=True,prior_owner_assent_occurrences_verified=38,total_prior_locator_owner_scopes=124,prior_relation257_category264_and_pending_preserved=True,new_owner_decisions=0,
    exhaustive207_disjoint_plan_and_remaining168_verified=True,protected_files_preserved=len(start['protected']),previous_sessions_prefix_preserved_before_append=True)
assert not (M/'validation.json').exists();(M/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
