"""Validate locator/source byte traces and faithful bounded assent/history."""
from pathlib import Path
import json,hashlib,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c1'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def resolve(x,pointer):
    for k in pointer.lstrip('/').split('/') if pointer else []:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
c=load(OUT/'comparisons.json');mf=load(OUT/'manifest.json');a=load(M/'annotations.json');diag=load(M/'locator-diagnostics.json');plan=load(M/'scope-plan.json');s=load(R/'current-state-16.json');prior=load(R/'current-state-15.json')
d=load(R/'owner-decision-07.json');o=load(R/'owner-review-overlay-07.json');oldo=load(R/'owner-review-overlay-06.json');oldstate=load(R/'current-state-14.json');approvalpacket=load(R/'part-04b3/comparisons.json')
for x in [c['source'],c['evaluation'],*c['responses'].values(),*mf['artifacts'],mf['manual_annotations'],mf['locator_diagnostics'],mf['scope_plan'],mf['estimate'],*load(M/'owner-decision-artifacts.json')['artifacts']]:assert ref(ROOT/x['path'])==x
raws={r:(ROOT/x['path']).read_bytes() for r,x in c['responses'].items()};parsed={r:json.loads(b) for r,b in raws.items()};helpers=load(P/'inputs/v1/helper-regions.json')
records=fields=44*0;counts=dict(geometry=0,strictfail=0,readable=0,descenders=0,missingline=0)
def check(run,t):
    global records,fields
    def field(span,value,pointer):
        b=raws[run][span['start_byte']:span['end_byte_exclusive']];assert sha(b)==span['sha256'] and json.loads(b)==value and resolve(parsed[run],pointer)==value
    field(t['raw_span'],t['original_record'],t['pointer']);records+=1
    for f in list(t['fields'].values())+list(t.get('locator_fields',{}).values()):field(f['raw_span'],f['original_value'],f['pointer']);fields+=1
assert [x['id'] for x in c['locators']]==plan['parts'][0]['evidence_ids']==[x[0] for x in a['rows']]
for row,note,x in zip(c['locators'],a['rows'],diag['rows']):
    assert row['manual_assessment']==note[1] and row['manual_comparison']==note[2] and row['diagnostic']==x
    assert row['status']=='waiting_review' and row['human_reviewer'] is None
    helper=row['independent_source_helper'];text=resolve(helpers,helper['pointer']);begin,end=helper['character_range'];assert text[begin:end]==helper['literal_text'] and sha(helper['literal_text'].encode())==helper['utf8_excerpt_sha256']
    assert ref(ROOT/helper['artifact']['path'])==helper['artifact']
    im=Image.open(ROOT/x['source_image']['path']).convert('RGB');assert ref(ROOT/x['source_image']['path'])==x['source_image'];w,h=im.size;b=x['original_bbox_pixels']
    assert [w,h]==x['actual_dimensions']==[1700,2200] and 0<=b[0]<b[2]<=w and 0<=b[1]<b[3]<=h
    pw,ph=x['page_dimensions_pdf_points'];assert x['bbox_pdf_points']==[b[0]*pw/w,b[1]*ph/h,b[2]*pw/w,b[3]*ph/h]
    exact=Image.open(ROOT/x['exact_crop']['path']).convert('RGB');assert exact.size==(b[2]-b[0],b[3]-b[1]) and exact.tobytes()==im.crop(tuple(b)).tobytes()
    for artifact in [x['exact_crop'],x['quote_reference'],*[z['magnified_boundary_patch'] for z in x['quote_glyphs_outside_box']]]:assert ref(ROOT/artifact['path'])==artifact
    assert x['pdf_page'] in [31,32,33] and x['quote_glyphs_outside_box'] and not x['quote_whole_glyph_envelopes_contained']
    for z in x['quote_glyphs_outside_box']:assert max(z['overflow_pdf_points'].values())>0
    for run,rr in row['runs'].items():
        check(run,rr['output_trace']);e=rr['output_trace']['original_record'];assert e['id']==row['id'] and e['quote']['value']==x['quote'] and e['image']['bbox']==b and e['image']['sha256']==x['source_image']['sha256']
        assert rr['evaluator_compared'] and rr['status']=='waiting_review' and rr['human_reviewer'] is None and rr['owner_decision'] is None
        for er in rr['inherited_report_observations']:
            assert ref(ROOT/er['artifact']['path'])==er['artifact'] and resolve(load(ROOT/er['artifact']['path']),er['pointer'])==er['original_observation']
        counts['geometry']+=1;counts['strictfail']+=1
        key={'readable_raster_envelope_not_contained':'readable','raster_descenders_clipped':'descenders','quote_line_outside_crop':'missingline'}[row['manual_assessment']];counts[key]+=1
    assert row['runs']['first-001']['output_trace']['original_record']['quote']==row['runs']['context-01']['output_trace']['original_record']['quote']
    assert row['runs']['first-001']['output_trace']['original_record']['image']==row['runs']['context-01']['output_trace']['original_record']['image']
assert counts==dict(geometry=44,strictfail=44,readable=38,descenders=4,missingline=2)
for key in ['full_pages_manually_inspected','quote_sheets_manually_inspected','exact_crops_manually_inspected','magnified_boundary_patches_manually_inspected']:
    for artifact in c[key]:assert ref(ROOT/artifact['path'])==artifact
assert d['owner_reply_verbatim']=='ok kontynuuj' and len(d['recommendations'])==3 and [x['occurrences'] for x in d['recommendations']]==[68,2,2]
assert len(d['scopes'])==36 and d['newly_decided_assigned_occurrences']==72 and d['prior_kind_D961stack_preserved']
byid={r['id']:r for r in approvalpacket['relationships']}
approved=0
for row in d['scopes']:
    base=byid[row['id']]
    assert row['whole_record_accepted'] is False and row['full_dependent_result_accepted'] is False
    for key in ['source_scope','target_scope','bounded_independent_source','necessity_and_missing_impact']:assert row[key]==base[key]
    for run,x in row['runs'].items():assert x['edge_trace']==base['runs'][run]['output_trace'][row['id']];check(run,x['edge_trace']);approved+=1
    if row['id']=='D961stack':assert row['owner_recommendation_number']==3 and 'Prior mention-kind SEM-015 unchanged' in row['accepted_components']['decision']
assert approved==72
for run,v in o['runs'].items():
    previous=oldo['runs'][run];assert v['relationship_scopes'][:len(previous['relationship_scopes'])]==previous['relationship_scopes']
    assert len(v['relationship_scopes'])==(126 if run=='first-001' else 131) and v['remaining_without_owner_relation_scope']==0
    for key in ['scopes','context_requirements','accepted_scoped_groups','reviewed_context_groups']:assert v[key]==previous[key]
for key in ['category_units','category_accepted_scope_counts','pending_expectation_ids','illustration_states','all_locator_review']:assert o[key]==oldo[key]
assert len(o['category_units'])==264 and o['relation_facet_decisions'][:len(oldo['relation_facet_decisions'])]==oldo['relation_facet_decisions']
for key in ['SEM-004','SEM-014','SEM-015','SEM-016','SEM-017']:assert s['issue_dispositions'][key]==oldstate['issue_dispositions'][key]
assert s['unresolved_issue_ids']==oldstate['inherited_issue_ids'] and s['pending_expectation_ids']==oldstate['pending_expectation_ids'] and len(s['pending_expectation_ids'])==8
assert s['owner_accepted_relationship_occurrences']==257 and s['owner_pending_relationship_occurrences']==0 and s['locator_evaluator_compared_occurrences']==44 and s['remaining_uncompared_locator_occurrences']==80
assert s['locator_owner_reviewed_occurrences']==0 and s['next_part']=='M-POC5A.4c2' and not s['M_POC5A_closed'] and not s['M_POC5A_4b_closed'] and not s['M_POC5A_4c_closed']
assert s['decision']==ref(R/'owner-decision-07.json') and s['overlay']==ref(R/'owner-review-overlay-07.json')
checklist=load(R/'checklist.json')
for run,rows in checklist['locator_review'].items():
    actual=[eid for part in plan['parts'] for eid in part['evidence_ids'] if any(r['evidence_id']==eid for r in rows)]
    assert len(actual)==len(set(actual))==len(rows) and set(actual)=={r['evidence_id'] for r in rows}
assert [x['occurrences'] for x in plan['parts']]==[44,42,38] and plan['before_locator_review']
start=load(M/'start.json');changed=[x['path'] for x in start['protected'] if not (ROOT/x['path']).exists() or ref(ROOT/x['path'])!=x];assert not changed,changed
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(status='passed',locator_occurrences_verified=44,owner_assent_occurrences_verified=approved,original_records_verified=records,raw_fields_verified=fields,
    geometry_and_source_helper_hashes_verified=True,original_exact_crops_pixel_equal=True,locator_partition44_42_38_disjoint_exhaustive=True,
    raster_and_strict_glyph_criteria_separate=counts,prior185_relation_scopes_and_all_pending_preserved=True,prior264_category_units_unchanged=True,
    no_new_locator_owner_acceptance=True,protected_files_preserved=len(start['protected']),previous_sessions_prefix_unchanged_before_append=True)
assert not (M/'validation.json').exists();(M/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
