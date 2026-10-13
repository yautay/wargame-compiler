"""Verify literal evidence lineage, bounded assent, counts, scope and immutability."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c3'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def resolve(x,pointer):
    for k in pointer.lstrip('/').split('/') if pointer else []:
        k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
    return x
c=load(OUT/'comparisons.json');mf=load(OUT/'manifest.json');a=load(M/'annotations.json');diag=load(M/'locator-diagnostics.json');plan=load(P/'measurement/M-POC5A-semantic-04c1/scope-plan.json')
s=load(R/'current-state-20.json');prior=load(R/'current-state-19.json');oldstate=load(R/'current-state-18.json');d=load(R/'owner-decision-09.json');o=load(R/'owner-review-overlay-09.json');oldo=load(R/'owner-review-overlay-08.json');oldpacket=load(R/'part-04c2/comparisons.json')
for x in [c['source'],c['evaluation'],*c['responses'].values(),*mf['artifacts'],mf['manual_annotations'],mf['locator_diagnostics'],mf['scope_plan'],mf['estimate'],*load(M/'owner-decision-artifacts.json')['artifacts']]:assert ref(ROOT/x['path'])==x
assert c['source']['sha256']=='e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
assert c['evaluation']['sha256']=='7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce'
raws={r:(ROOT/x['path']).read_bytes() for r,x in c['responses'].items()};parsed={r:json.loads(b) for r,b in raws.items()}
assert len(raws['first-001'])==617941 and sha(raws['first-001'])=='3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307'
assert len(raws['context-01'])==712014 and sha(raws['context-01'])=='95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b'
records=fields=0
def tracecheck(run,t):
    global records,fields
    def field(span,value,pointer):
        b=raws[run][span['start_byte']:span['end_byte_exclusive']];assert sha(b)==span['sha256'] and json.loads(b)==value and resolve(parsed[run],pointer)==value
    field(t['raw_span'],t['original_record'],t['pointer']);records+=1
    for f in list(t['fields'].values())+list(t.get('locator_fields',{}).values()):field(f['raw_span'],f['original_value'],f['pointer']);fields+=1
assert [x['id'] for x in c['locators']]==plan['parts'][2]['evidence_ids']==[x[0] for x in a['rows']]
count={'first-001':0,'context-01':0};readable=clipped=context_only=0
for row,note,x in zip(c['locators'],a['rows'],diag['rows']):
    assert row['manual_assessment']==note[1] and row['manual_comparison']==note[2] and row['diagnostic']==x
    assert row['status']=='waiting_review' and row['human_reviewer'] is None
    helper=row['independent_source_helper'];hp=ROOT/helper['artifact']['path'];text=resolve(load(hp),helper['pointer']) if helper['pointer'] else hp.read_text(encoding='utf-8-sig')
    begin,end=helper['character_range'];assert text[begin:end]==helper['literal_text'] and sha(helper['literal_text'].encode())==helper['utf8_excerpt_sha256'];assert ref(hp)==helper['artifact']
    im=Image.open(ROOT/x['source_image']['path']).convert('RGB');assert ref(ROOT/x['source_image']['path'])==x['source_image'];w,h=im.size;b=x['original_bbox_pixels']
    assert [w,h]==x['actual_dimensions'] and 0<=b[0]<b[2]<=w and 0<=b[1]<b[3]<=h
    mapping=x['coordinate_mapping'];sx,sy=mapping['scale_pdf_points_per_pixel'];ox,oy=mapping['pixel_offset_on_render'];assert x['bbox_pdf_points']==[(b[0]+ox)*sx,(b[1]+oy)*sy,(b[2]+ox)*sx,(b[3]+oy)*sy]
    if x['pdf_page']==27:
        assert (w,h)==(433,395) and list(row['runs'])==['context-01'] and helper['pointer'] is None
        scopepath=ROOT/mapping['scope_artifact']['path'];assert ref(scopepath)==mapping['scope_artifact'];scope=load(scopepath);assert [ox,oy]==scope['pixel_bbox_on_reviewer_render'][:2]
        bx=scope['pixel_bbox_on_reviewer_render'];assert mapping['allowed_pdf_clip']==[bx[0]*sx,bx[1]*sy,bx[2]*sx,bx[3]*sy]
        clip=mapping['allowed_pdf_clip'];qb=x['source_quote_match']['bbox_pdf_points'];assert clip[0]<=qb[0]<qb[2]<=clip[2] and clip[1]<=qb[1]<qb[3]<=clip[3]
        context_only+=1
    else:assert (w,h)==(1700,2200) and x['pdf_page'] in [36,37] and list(row['runs'])==['first-001','context-01'] and [ox,oy]==[0,0]
    exact=Image.open(ROOT/x['exact_crop']['path']).convert('RGB');assert exact.size==(b[2]-b[0],b[3]-b[1]) and exact.tobytes()==im.crop(tuple(b)).tobytes()
    for artifact in [x['exact_crop'],x['quote_reference'],*[g['magnified_boundary_patch'] for g in x['quote_glyphs_outside_box']]]:assert ref(ROOT/artifact['path'])==artifact
    assert x['quote_glyphs_outside_box'] and not x['quote_whole_glyph_envelopes_contained']
    assert max(max(g['overflow_pdf_points'].values()) for g in x['quote_glyphs_outside_box'])>1e-8 # category check only, not tolerance pass
    loss=sum(g['dark_pixels_outside_original_crop'] for g in x['quote_glyphs_outside_box']);assert loss==(7 if row['id']=='E1011' else 0)
    assert row['strict_full_quote_glyph_envelope']=='fails_exact_envelope_containment'
    for run,rr in row['runs'].items():
        tracecheck(run,rr['output_trace']);e=rr['output_trace']['original_record'];assert e['id']==row['id'] and e['quote']['value']==x['quote'] and e['image']['bbox']==b and e['image']['sha256']==x['source_image']['sha256']
        assert rr['evaluator_compared'] and rr['status']=='waiting_review' and rr['human_reviewer'] is None and rr['owner_decision'] is None
        for er in rr['inherited_report_observations']:assert ref(ROOT/er['artifact']['path'])==er['artifact'] and resolve(load(ROOT/er['artifact']['path']),er['pointer'])==er['original_observation']
        count[run]+=1
        if loss:assert rr['raster_review']=='readable_but_descender_ink_clipped';clipped+=1
        else:assert rr['raster_review']=='readable_no_observed_ink_loss';readable+=1
    if len(row['runs'])==2:
        assert row['runs']['first-001']['output_trace']['original_record']['quote']==row['runs']['context-01']['output_trace']['original_record']['quote']
        assert row['runs']['first-001']['output_trace']['original_record']['image']==row['runs']['context-01']['output_trace']['original_record']['image']
assert (count,readable,clipped,context_only)==({'first-001':16,'context-01':22},36,2,6)
for key in ['full_pages_manually_inspected','quote_sheets_manually_inspected','exact_crops_manually_inspected','magnified_boundary_patches_manually_inspected']:
    for artifact in c[key]:assert ref(ROOT/artifact['path'])==artifact
assert ref(ROOT/c['supplied_context_crop_manually_inspected']['path'])==c['supplied_context_crop_manually_inspected']
assert d['owner_reply_verbatim']=='zatwierdzam i kontynuuj - powiedz ile jeszcze do końca etapu 5 ??' and d['part']=='M-POC5A.4c2'
assert len(d['scopes'])==21 and d['newly_reviewed_locator_occurrences']==42 and d['strict_quote_glyph_envelope_failures']==40 and d['strict_quote_glyph_envelope_numericprecision_unresolved']==2 and d['readable_raster_without_observed_ink_loss']==42
byid={r['id']:r for r in oldpacket['locators']};ownerreviewed=0
for row in d['scopes']:
    base=byid[row['id']];assert row['whole_evidence_record_accepted'] is False and row['original_locator_repaired'] is False
    for key in ['source_scope','source_quote_original','independent_source_helper','source_image']:assert row[key]==base[key]
    assert row['accepted_facets']['strict_whole_glyph_containment']==base['strict_full_quote_glyph_envelope'] and row['accepted_facets']['raster_result']==base['raster_short_quote']
    for run,x in row['runs'].items():assert x['output_trace']==base['runs'][run]['output_trace'];tracecheck(run,x['output_trace']);ownerreviewed+=1
assert ownerreviewed==42
for run,v in o['runs'].items():
    previous=oldo['runs'][run]
    for key in previous:
        if key not in ['locator_scopes','owner_reviewed_locator_scoped_occurrences','assigned_remaining_unreviewed_locator_occurrences']:assert v[key]==previous[key]
    assert v['locator_scopes'][:22]==previous['locator_scopes'] and len(v['locator_scopes'])==43 and v['owner_reviewed_locator_scoped_occurrences']==43
    assert v['assigned_remaining_unreviewed_locator_occurrences']==(16 if run=='first-001' else 22)
for key in ['category_units','category_accepted_scope_counts','pending_expectation_ids','illustration_states','all_output_edges_review','relationship_owner_decision','relation_facet_decisions']:assert o[key]==oldo[key]
assert len(o['category_units'])==264 and o['accepted_relation_scoped_occurrences']==257
for key in oldstate['issue_dispositions']:
    if key!='SEM-007':assert s['issue_dispositions'][key]==oldstate['issue_dispositions'][key]
assert s['issue_dispositions']==prior['issue_dispositions'] and s['unresolved_issue_ids']==oldstate['unresolved_issue_ids'] and s['pending_expectation_ids']==oldstate['pending_expectation_ids'] and len(s['pending_expectation_ids'])==8
assert s['owner_accepted_relationship_occurrences']==257 and s['owner_pending_relationship_occurrences']==0 and s['locator_evaluator_compared_occurrences']==124
assert s['locator_owner_reviewed_occurrences']==86 and s['locator_owner_pending_compared_occurrences']==38 and s['remaining_uncompared_locator_occurrences']==0
assert s['next_part']=='M-POC5A.4d' and not s['M_POC5A_closed'] and not s['M_POC5A_4b_closed'] and not s['M_POC5A_4c_closed']
assert s['decision']==ref(R/'owner-decision-09.json') and s['overlay']==ref(R/'owner-review-overlay-09.json')
situations=load(P/'evaluation/eval-v1/situations.json');assert len(situations['situations'])==20
start=load(M/'start.json');changed=[x['path'] for x in start['protected'] if not (ROOT/x['path']).exists() or ref(ROOT/x['path'])!=x];assert not changed,changed
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
result=dict(status='passed',locator_occurrences_verified=38,prior_locator_owner_assent_occurrences_verified=42,total_owner_locator_occurrences=86,original_records_verified=records,raw_fields_verified=fields,
    geometry_and_source_helpers_verified=True,context_only6_and_suppliedcrop_mapping_verified=True,exact_crops_pixel_equal=True,measurable_envelope38_verified=True,readable36_clipped2_verified=True,
    previous_relation257_category264_and_all_pending_unchanged=True,no_new_locator_owner_acceptance=True,protected_files_preserved=len(start['protected']),previous_sessions_prefix_preserved_before_append=True)
assert not (M/'validation.json').exists();(M/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))
