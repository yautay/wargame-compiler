from review_driver import *
from math import floor,ceil
from wgc.sources.geometry import box_to_pdf
doc=load(D/'final-verified/inventory.json');ledger=load(D/'region-ledger-final.json')['regions'];spec=load(D/'author-specifications-final.json');corrections=load(D/'component-observations.json')['corrections_after_enlargement']
regions={r['id']:r for r in doc['regions']};evs={e['region_id']:e for e in doc['evidence']};pages={p['id']:p for p in doc['pages']};specs={s['key']:s for s in spec['specifications']}
assert len(ledger)==len(specs)==141
rows=[]
for i,l in enumerate(ledger,1):
    r=regions[l['region']['id']];p=pages[r['page_id']];s=specs[r['key']]
    assert l['region']==r and l['evidence']==evs[r['id']]
    assert l['pdf_page']==p['pdf_page'] and l['reading_order_index']==doc['reading_order'].index(r['id'])
    assert l['label']==s['label'] and l['group']==s['group']
    assert l['components']==corrections.get(r['key'],s['components'])
    x0,y0,x1,y1=s['observed_pixel_box']
    assert r['box']==[floor(x0*1000000/1224),floor(y0*1000000/1584),ceil(x1*1000000/1224),ceil(y1*1000000/1584)]
    assert l['native_crop_bounds']==[{'numerator':v.numerator,'denominator':v.denominator} for v in box_to_pdf(r['box'],p)]
    assert l['coverage_limits']==r['coverage'] and l['exact_text_pin']==evs[r['id']]['text']
    rows.append({'index':i,'region_id':r['id'],'key':r['key'],'result':'metadata_exact','component_description_truth':'See independent region-review-ledger and R01/R02, not inferred from internal report agreement.'})
gaps=load(D/'gaps.json')['representation_gaps'];assert len(gaps)==141
for g in gaps:
    r=regions[g['region_id']];assert r['revision']==g['revision'] and r['key']==g['key'] and r['coverage']==g['levels']
coverage=load(D/'final-verified/coverage.json');root_result=load(R/'commands/05-root-inventory-validate.stdout');assert coverage==root_result
scope=load(D/'scope-report-final.json')
assert [scope[k] for k in ('task_denominator','preserved_authored_denominator','unprocessed_placeholder_denominator','full_denominator','context_regions','context_denominator','represented_or_excluded_new_regions')]==[141,130,36,307,1,0,0]
assert scope['task_counts_by_physical_page']=={'5':39,'6':33,'7':39,'8':30}
assert scope['source_coverage_levels']==coverage['levels']
assert scope['task_coverage_levels']=={'transcription':{'partial':141},'descriptive_semantics':{'unprocessed':141},'formal_semantics':{'unprocessed':141}}
write('report-consistency-audit.json',{'outcome':'metadata_consistent','regions':rows,'raw_evidence_and_inventory_metadata_exact':True,'gap_entries_exact':len(gaps),'coverage_matches_own_root_validation':True,'scope_report_counts_exact':True,'source_truth':'Internal consistency does not validate component readings. R01/R02 contradict executor source-completeness claims in three grouped counter entries.','superseded_drafts':'Not treated as product targets. Final ledger correctly applies later component-observations overrides, but those overrides do not cover the three defective entries.'})
print('REPORT CONSISTENCY PASS; SOURCE COMPONENT FINDINGS REMAIN')
