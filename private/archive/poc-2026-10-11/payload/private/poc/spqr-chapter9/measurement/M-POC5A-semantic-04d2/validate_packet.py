"""Check exact lineage, child scopes, numerical facts, images and bounded assent."""
from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';O=R/'part-04d2'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def resolve(x,pointer):
    for k in pointer.lstrip('/').split('/') if pointer else []:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
c=load(O/'comparisons.json');mf=load(O/'manifest.json');A=load(M/'annotations.json');assign=load(M/'scope-assignment.json');plan=load(ROOT/assign['original_before_review_plan']['path']);inv=load(P/'evaluation/eval-v1/inventory.json');checklist=load(R/'checklist.json');s=load(R/'current-state-24.json');prior=load(R/'current-state-23.json')
for x in [c['source'],c['evaluation'],*c['responses'].values(),*mf['artifacts'],mf['scope_plan'],mf['scope_assignment'],mf['estimate'],mf['manual_annotations'],mf['source_views'],*load(M/'owner-decision-artifacts.json')['artifacts'],*load(M/'public-document-artifacts.json'),*load(M/'packet-artifacts.json').values()]:assert ref(ROOT/x['path'])==x
assert c['source']['sha256']=='e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e' and c['evaluation']['sha256']=='7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce'
raws={r:(ROOT/x['path']).read_bytes() for r,x in c['responses'].items()};parsed={r:json.loads(b) for r,b in raws.items()}
assert len(raws['first-001'])==617941 and sha(raws['first-001'])=='3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307'
assert len(raws['context-01'])==712014 and sha(raws['context-01'])=='95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b'
records=fields=0
def tracecheck(run,t):
    global records,fields
    def field(span,v,ptr):
        b=raws[run][span['start_byte']:span['end_byte_exclusive']];assert sha(b)==span['sha256'] and json.loads(b)==v and resolve(parsed[run],ptr)==v
    field(t['raw_span'],t['original_record'],t['pointer']);records+=1
    for f in t['fields'].values():field(f['raw_span'],f['original_value'],f['pointer']);fields+=1
ids=[x['id'] for x in c['inventory']];assert ids==assign['assigned_ids']==plan['parts'][1]['inventory_ids']==[x[0] for x in A['rows']] and len(ids)==68
allids=[i for p in plan['parts'] for i in p['inventory_ids']];assert len(allids)==len(set(allids))==207 and set(allids)=={x['id'] for x in inv['items']}
assert len(set(plan['parts'][2]['inventory_ids']+plan['parts'][3]['inventory_ids']))==100 and not set(ids)&set(plan['parts'][0]['inventory_ids'])
assert load(M/'start.json')['estimate_before_semantic_review']['refreshed_minutes_range']==[75,90]
unique={r:set() for r in c['responses']};counts={r:0 for r in c['responses']};source_ranges=graphics=clauses=0;overlay=load(R/'owner-review-overlay-11.json')
for row,note in zip(c['inventory'],A['rows']):
    assert row['manual_assessment']==note[1] and row['manual_comparison']==note[2] and row['status']=='waiting_review' and row['human_reviewer'] is None and not row['whole_record_accepted']
    frozen=resolve(inv,row['evaluation_pointer']);assert frozen==row['frozen_inventory_item'];clauses+=row['inventory_type']=='clause_group'
    assert [x['original_evidence'] for x in row['source_scopes']]==frozen['evidence']
    for src in row['source_scopes']:
        for x in [src['source_visual'],src['evaluation_inventory']]:assert ref(ROOT/x['path'])==x
        assert src['parent_mapping_not_child_certificate']
        if 'literal_scope' in src:
            assert src['literal_scope']==src['original_evidence']['transcription'];x=src['helper'];assert ref(ROOT/x['path'])==x;helper=(ROOT/x['path']).read_text(encoding='utf-8-sig');begin,end=src['helper_character_range']
            assert helper[begin:end]==src['literal_scope'] and sha(src['literal_scope'].encode())==src['literal_scope_sha256'];source_ranges+=1
        else:
            g=src['graphic_scope'];assert g['id']==row['id'] and g['inventory_bbox_pdf_points']==src['original_evidence']['bbox_pdf_points'];graphics+=1
            for x in [g['source'],g['exact_crop'],g['readability_zoom']]:assert ref(ROOT/x['path'])==x
            im=Image.open(ROOT/g['source']['path']).convert('RGB');crop=Image.open(ROOT/g['exact_crop']['path']).convert('RGB');zoom=Image.open(ROOT/g['readability_zoom']['path']).convert('RGB');b=g['inventory_bbox_pdf_points'];w,h=im.size
            pix=[round(b[0]*w/612),round(b[1]*h/792),round(b[2]*w/612),round(b[3]*h/792)];assert pix==g['derived_pixel_bbox'] and crop.tobytes()==im.crop(tuple(pix)).tobytes() and crop.size==im.crop(tuple(pix)).size
            assert zoom.tobytes()==crop.resize((crop.width*4,crop.height*4),Image.Resampling.NEAREST).tobytes()
    for run,rr in row['runs'].items():
        counts[run]+=1;assert rr['evaluator_compared'] and rr['status']=='waiting_review' and rr['human_reviewer'] is None and rr['owner_decision'] is None and not rr['whole_record_accepted']
        assert rr['source_scopes']==row['source_scopes'] and rr['mapping_not_semantic_proof']
        mapped=checklist['inventory'][int(row['evaluation_pointer'].split('/')[-1])]['runs'][run]['output_record_ids'];assert [t['original_record']['id'] for t in rr['output_traces']]==mapped;unique[run].update(mapped)
        for t in rr['output_traces']+rr['evidence_traces']+rr['gap_traces']:tracecheck(run,t)
        for fld in rr['selected_output_fields']:assert any(fld['pointer'] in t['fields'] for t in rr['output_traces'])
        for z in rr['prior_local_scopes']+rr['prior_context_requirements']:assert ref(ROOT/z['artifact']['path'])==z['artifact'] and resolve(overlay,z['pointer'])==z['prior_scoped_decision']
    assert row['mapped_records_equal_between_runs'] and [t['original_record'] for t in row['runs']['first-001']['output_traces']]==[t['original_record'] for t in row['runs']['context-01']['output_traces']]
assert counts=={'first-001':68,'context-01':68} and all(len(x)==25 for x in unique.values()) and clauses==43 and graphics==3
byid={x['id']:x for x in c['inventory']}
for run in c['responses']:
    def node(iid):return byid[iid]['runs'][run]['output_traces'][0]['original_record']
    def params(iid):return {x['name']:x['value'] for x in node(iid)['parameters']['value']}
    p=params('R-9.11');assert p['Pre-Shock modifier']==1 and p['defender Hits multiplier']=='1/2, round down' and p['Elephant Hits adjustment']==-1 and p['defenders permitted']==2 and p['unoccupied Rear minimum']==1
    p=params('R-9.14');assert p['directional roll movement']==3 and p['Front contact']==1 and p['Flank/Rear contact']==p['cavalry contact']==2 and p['isolation termination']=='>=8' and p['maximum sequence']==4 and p['concurrent Rampages maximum']==1 and p['Leader rally Hits']=='TQ–2'
    assert node('C-9.16-01')['interpretation']['state']=='unknown' and 'G916' in node('C-9.16-01')['gap_ids']
    assert node('C-9.18-01')['exceptions']['state']=='unknown' and 'G-D918specific' in node('C-9.18-01')['exceptions']['gap_ids'] and 'Unless' in node('C-9.18-01')['transcription']['value'][0]
    assert params('R-9.21')['approaching MA']=='<= withdrawing Skirmisher MA' and params('R-9.21')['OW maximum']==2
    assert params('R-9.22')['Skirmisher-target modifier']==2
    assert params('R-9.23')['Skirmisher inflicted-Hits cap']==1 and params('R-9.23')['Skirmisher inflicted-Hits scaling']=='1/2, round down'
    assert params('R-9.24')['line interruption allowance']==1 and params('R-9.24')['facing cost']==0
    table=node('T-01')['content']['value']['transcription'];assert table['headers']==['Die Roll','Result'] and [x['die_roll'] for x in table['rows']]==['0','1–6','7–9']
    for iid,output in zip(['TR-01','TR-02','TR-03'],table['rows']):assert ' '.join(byid[iid]['source_scopes'][0]['literal_scope'].split())==' '.join((output['die_roll']+' '+output['result']).split())
    assert node('G-01')['content']['value']['transcription']['visible_text']==['Africa','15','J','a','5','EL','5','7']
    assert node('G-02')['content']['value']['transcription']['visible_text']==["Bal'ric",'6','S','1','SK','3','6']
    assert node('D-01')['content']['value']['transcription']['direction_labels']=={'upper_left':'6','upper_right':'1','right':'2','lower_right':'3','lower_left':'4','left':'5'}
    for iid,owner in [('K-01','R911'),('K-02','N914table'),('K-03','R914'),('K-04','R924')]:assert all(t['original_record']['content']['value'].get('owner_rule_id',t['original_record']['content']['value'].get('owner_node_id'))==owner for t in byid[iid]['runs'][run]['output_traces'])
    g=next(t['original_record'] for t in byid['C-9.23-05']['runs'][run]['gap_traces'] if t['original_record']['id']=='G-D923shock');assert g['blocking'] and (g.get('context_status')=='partially_supplied_still_blocking')==(run=='context-01')
oldpacket=load(R/'part-04d1/comparisons.json');d=load(R/'owner-decision-11.json');oldo=load(R/'owner-review-overlay-10.json')
assert d['owner_reply_verbatim']=='Zatwierdzam i kontynuuj' and d['newly_reviewed_inventory_occurrences']==78 and d['bounded_supported_occurrences']==76 and d['qualified_content_summary_omission_occurrences']==2
assert len(d['scopes'])==len(oldpacket['inventory'])==39
for row,b in zip(d['scopes'],oldpacket['inventory']):
    for key in ['id','source_scopes','manual_assessment','manual_comparison','exclusions']:assert row[key]==b[key]
    assert row['status']=='reviewed' and not row['whole_record_accepted']
    for run,rr in row['runs'].items():
        assert rr['status']=='reviewed' and rr['output_traces']==b['runs'][run]['output_traces'] and not rr['whole_record_accepted']
        for t in rr['output_traces']:tracecheck(run,t)
for run,v in overlay['runs'].items():
    for key in oldo['runs'][run]:assert v[key]==oldo['runs'][run][key]
    assert len(v['inventory_scopes'])==39
for key in ['category_units','category_accepted_scope_counts','pending_expectation_ids','illustration_states','all_output_edges_review','relationship_owner_decision','relation_facet_decisions']:assert overlay[key]==oldo[key]
assert len(overlay['category_units'])==264 and overlay['accepted_relation_scoped_occurrences']==257 and overlay['owner_reviewed_locator_scoped_occurrences']==124
assert s['pending_expectation_ids']==prior['pending_expectation_ids'] and len(s['pending_expectation_ids'])==8 and s['unresolved_issue_ids']==prior['unresolved_issue_ids'] and len(s['unresolved_issue_ids'])==13 and s['issue_dispositions']==prior['issue_dispositions']
assert s['decision']==ref(R/'owner-decision-11.json') and s['locator_owner_decision']==ref(R/'owner-decision-10.json') and s['relationship_owner_decision']==ref(R/'owner-decision-07.json') and s['expectation_owner_decision']==ref(R/'owner-decision-03.json')
assert s['inventory_evaluator_compared_assigned_occurrences']==214 and s['inventory_owner_reviewed_assigned_occurrences']==78 and s['inventory_owner_pending_compared_occurrences']==136 and s['inventory_remaining_assigned_occurrences']==200 and s['next_part']=='M-POC5A.4d3'
assert not any(s[k] for k in ['M_POC5A_closed','M_POC5A_4_closed','M_POC5A_4b_closed','M_POC5A_4c_closed','M_POC5A_4d_closed'])
assert not load(O/'issues.json')['new_issues'] and c['summary']['new_owner_reviewed_occurrences']==0 and c['summary']['bounded_supported_inventory_occurrences']==136
start=load(M/'start.json');changed=[x['path'] for x in start['protected'] if not (ROOT/x['path']).exists() or ref(ROOT/x['path'])!=x];assert not changed,changed;assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(status='passed',inventory_occurrences_verified=136,source_text_ranges_verified=source_ranges,exact_clause_scopes_verified=clauses,graphic_crops_pixel_equal_verified=graphics,unique_mapped_records_per_answer={r:len(x) for r,x in unique.items()},raw_records_verified=records,raw_fields_verified=fields,local_numeric_operator_and_table_values_verified=True,old_pending_and_context_partial_gap_preserved=True,prior_owner_inventory_assent_occurrences_verified=78,new_owner_decisions=0,protected_files_preserved=len(start['protected']),previous_sessions_prefix_preserved_before_append=True)
assert not (M/'validation.json').exists();(M/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
