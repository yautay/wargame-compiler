"""Check coverage/source crops/raw bytes and faithful bounded owner decision."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c2'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def resolve(x,pointer):
    for k in pointer.lstrip('/').split('/') if pointer else []:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
c=load(OUT/'comparisons.json');mf=load(OUT/'manifest.json');a=load(M/'annotations.json');diag=load(M/'locator-diagnostics.json');plan=load(P/'measurement/M-POC5A-semantic-04c1/scope-plan.json')
s=load(R/'current-state-18.json');prior=load(R/'current-state-17.json');oldstate=load(R/'current-state-16.json')
d=load(R/'owner-decision-08.json');o=load(R/'owner-review-overlay-08.json');oldo=load(R/'owner-review-overlay-07.json');oldpacket=load(R/'part-04c1/comparisons.json')
for x in [c['source'],c['evaluation'],*c['responses'].values(),*mf['artifacts'],mf['manual_annotations'],mf['locator_diagnostics'],mf['scope_plan'],mf['estimate'],*load(M/'owner-decision-artifacts.json')['artifacts']]:assert ref(ROOT/x['path'])==x
raws={r:(ROOT/x['path']).read_bytes() for r,x in c['responses'].items()};parsed={r:json.loads(b) for r,b in raws.items()};helpers=load(P/'inputs/v1/helper-regions.json')
records=fields=0;geometry=readable=rawfail=envelope=precision=0
def tracecheck(run,t):
    global records,fields
    def field(span,value,pointer):
        b=raws[run][span['start_byte']:span['end_byte_exclusive']];assert sha(b)==span['sha256'] and json.loads(b)==value and resolve(parsed[run],pointer)==value
    field(t['raw_span'],t['original_record'],t['pointer']);records+=1
    for f in list(t['fields'].values())+list(t.get('locator_fields',{}).values()):field(f['raw_span'],f['original_value'],f['pointer']);fields+=1
assert [x['id'] for x in c['locators']]==plan['parts'][1]['evidence_ids']==[x[0] for x in a['rows']]
for row,note,x in zip(c['locators'],a['rows'],diag['rows']):
    assert row['manual_assessment']==note[1] and row['manual_comparison']==note[2] and row['diagnostic']==x
    assert row['status']=='waiting_review' and row['human_reviewer'] is None
    helper=row['independent_source_helper'];text=resolve(helpers,helper['pointer']);begin,end=helper['character_range'];assert text[begin:end]==helper['literal_text'] and sha(helper['literal_text'].encode())==helper['utf8_excerpt_sha256']
    assert ref(ROOT/helper['artifact']['path'])==helper['artifact']
    im=Image.open(ROOT/x['source_image']['path']).convert('RGB');assert ref(ROOT/x['source_image']['path'])==x['source_image'];w,h=im.size;b=x['original_bbox_pixels']
    assert [w,h]==x['actual_dimensions']==[1700,2200] and 0<=b[0]<b[2]<=w and 0<=b[1]<b[3]<=h
    pw,ph=x['page_dimensions_pdf_points'];assert x['bbox_pdf_points']==[b[0]*pw/w,b[1]*ph/h,b[2]*pw/w,b[3]*ph/h]
    exact=Image.open(ROOT/x['exact_crop']['path']).convert('RGB');assert exact.size==(b[2]-b[0],b[3]-b[1]) and exact.tobytes()==im.crop(tuple(b)).tobytes()
    for artifact in [x['exact_crop'],x['quote_reference'],*[g['magnified_boundary_patch'] for g in x['quote_glyphs_outside_box']]]:assert ref(ROOT/artifact['path'])==artifact
    assert x['pdf_page'] in [34,35] and x['quote_glyphs_outside_box'] and not x['quote_whole_glyph_envelopes_contained']
    assert sum(g['dark_pixels_outside_original_crop'] for g in x['quote_glyphs_outside_box'])==0
    if row['id']=='E962':
        assert len(x['quote_glyphs_outside_box'])==1 and x['quote_glyphs_outside_box'][0]['text']=='c'
        assert x['quote_glyphs_outside_box'][0]['overflow_pdf_points']['left']==2.842170943040401e-14
        assert row['strict_full_quote_glyph_envelope']=='not_assessable_numeric_precision'
    else:
        assert max(max(g['overflow_pdf_points'].values()) for g in x['quote_glyphs_outside_box'])>1e-8
        assert row['strict_full_quote_glyph_envelope']=='fails_exact_envelope_containment'
    for run,rr in row['runs'].items():
        tracecheck(run,rr['output_trace']);e=rr['output_trace']['original_record'];assert e['id']==row['id'] and e['quote']['value']==x['quote'] and e['image']['bbox']==b and e['image']['sha256']==x['source_image']['sha256']
        assert rr['evaluator_compared'] and rr['status']=='waiting_review' and rr['human_reviewer'] is None and rr['owner_decision'] is None
        for er in rr['inherited_report_observations']:assert ref(ROOT/er['artifact']['path'])==er['artifact'] and resolve(load(ROOT/er['artifact']['path']),er['pointer'])==er['original_observation']
        geometry+=1;rawfail+=1;readable+=1
        if row['id']=='E962':precision+=1
        else:envelope+=1
    assert row['runs']['first-001']['output_trace']['original_record']['quote']==row['runs']['context-01']['output_trace']['original_record']['quote']
    assert row['runs']['first-001']['output_trace']['original_record']['image']==row['runs']['context-01']['output_trace']['original_record']['image']
assert (geometry,readable,rawfail,envelope,precision)==(42,42,42,40,2)
for key in ['full_pages_manually_inspected','quote_sheets_manually_inspected','exact_crops_manually_inspected','magnified_boundary_patches_manually_inspected']:
    for artifact in c[key]:assert ref(ROOT/artifact['path'])==artifact
assert d['owner_reply_verbatim']=='zatwierdzam i kontynuuj' and len(d['scopes'])==22 and d['newly_reviewed_locator_occurrences']==44
assert (d['readable_raster_without_observed_ink_loss'],d['readable_with_descenders_clipped'],d['missing_final_quote_line'])==(38,4,2)
assert d['strict_quote_glyph_envelope_passes']==0 and d['strict_quote_glyph_envelope_failures']==44
byid={r['id']:r for r in oldpacket['locators']};ownerreviewed=0
for row in d['scopes']:
    base=byid[row['id']];assert row['whole_evidence_record_accepted'] is False and row['original_locator_repaired'] is False
    for key in ['source_scope','source_quote_original','independent_source_helper','source_image']:assert row[key]==base[key]
    assert row['accepted_facets']['strict_whole_glyph_containment'] is False and row['accepted_facets']['raster_result']==base['raster_short_quote']
    for run,x in row['runs'].items():assert x['output_trace']==base['runs'][run]['output_trace'];tracecheck(run,x['output_trace']);ownerreviewed+=1
assert ownerreviewed==44
for run,v in o['runs'].items():
    previous=oldo['runs'][run]
    for key in previous:assert v[key]==previous[key]
    assert len(v['locator_scopes'])==22 and v['owner_reviewed_locator_scoped_occurrences']==22
    assert v['assigned_remaining_unreviewed_locator_occurrences']==(37 if run=='first-001' else 43)
for key in ['category_units','category_accepted_scope_counts','pending_expectation_ids','illustration_states','all_output_edges_review','relationship_owner_decision','relation_facet_decisions']:assert o[key]==oldo[key]
assert len(o['category_units'])==264 and o['accepted_relation_scoped_occurrences']==257
for key in ['SEM-004','SEM-014','SEM-015','SEM-016','SEM-017','SEM-018','SEM-019']:assert s['issue_dispositions'][key]==oldstate['issue_dispositions'][key]
assert s['unresolved_issue_ids']==oldstate['unresolved_issue_ids'] and s['pending_expectation_ids']==oldstate['pending_expectation_ids'] and len(s['pending_expectation_ids'])==8
assert s['owner_accepted_relationship_occurrences']==257 and s['owner_pending_relationship_occurrences']==0 and s['locator_evaluator_compared_occurrences']==86
assert s['locator_owner_reviewed_occurrences']==44 and s['locator_owner_pending_compared_occurrences']==42 and s['remaining_uncompared_locator_occurrences']==38
assert s['next_part']=='M-POC5A.4c3' and not s['M_POC5A_closed'] and not s['M_POC5A_4b_closed'] and not s['M_POC5A_4c_closed']
assert s['decision']==ref(R/'owner-decision-08.json') and s['overlay']==ref(R/'owner-review-overlay-08.json') and s['issue_dispositions']==prior['issue_dispositions']
start=load(M/'start.json');changed=[x['path'] for x in start['protected'] if not (ROOT/x['path']).exists() or ref(ROOT/x['path'])!=x];assert not changed,changed
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(status='passed',locator_occurrences_verified=42,prior_locator_owner_assent_occurrences_verified=44,original_records_verified=records,raw_fields_verified=fields,
    geometry_and_source_helpers_verified=True,exact_crops_pixel_equal=True,raw_envelope_false42_retained=True,measurable_envelope40_numericprecision2_separated=True,
    readable_raster42_no_observed_ink_loss=True,no_automatic_tolerance_pass_or_semantic_error=True,previous_relation257_category264_and_all_pending_unchanged=True,
    no_new_locator_owner_acceptance=True,protected_files_preserved=len(start['protected']),previous_sessions_prefix_preserved_before_append=True)
assert not (M/'validation.json').exists();(M/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
