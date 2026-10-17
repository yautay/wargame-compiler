from ops import *
import copy
from collections import Counter
from wgc.sources.inventory import seal,validate,coverage,page_basis_hash,partition_hash
from wgc.sources.geometry import box_to_pdf,render_size_pixels
from wgc.contracts.source import canonical_bytes
from PIL import Image
from pypdf import PdfReader
spec=load(AR+'/author-specifications-final.json');specmap={s['key']:s for s in spec['specifications']};components=load(AR+'/component-observations.json')['corrections_after_enlargement']
scope=load(P+'/scope.json');base=load(scope['baseline']['path']);author=load(AR+'/authored/inventory.json');reg=load(AR+'/authored/identity-registry.json');new=load(AR+'/new-evidence.json')
assert len(new)==141
for p in (scope['baseline'],scope['registry']):assert pin(p['path'])==p
doc=copy.deepcopy(author);doc['evidence'].extend(new)
for page in doc['pages']:
 if page['pdf_page'] in (5,6,7,8):
  r=next(r for r in doc['regions'] if r['key']==f'ig2b02:p{page["pdf_page"]}:printed-label');ev=next(e for e in new if e['region_id']==r['id'])
  page['label']={'status':'verified','value':str(page['pdf_page']),'reason':'Executor directly observed printed label on exact assigned original PNG and same-page label crop; independent review pending.','evidence':ev['id']}
doc['pages']=[seal(p) if p['pdf_page'] in (5,6,7,8) else p for p in doc['pages']];doc=seal(doc)
report=validate(doc,R);(A/'final-verified').mkdir(exist_ok=False)
for name,obj in [('inventory.json',doc),('identity-registry.json',reg),('coverage.json',report)]:
 with (A/'final-verified'/name).open('xb') as f:f.write(canonical_bytes(obj)+b'\n')
pages={p['id']:p for p in doc['pages']};regions={r['id']:r for r in doc['regions']};evmap={e['region_id']:e for e in new}
newregions=[r for r in doc['regions'] if r['key'].startswith('ig2b02:')];assert len(newregions)==141
ledger=[]
for r in newregions:
 item=specmap[r['key']];ev=evmap[r['id']];native=box_to_pdf(r['box'],pages[r['page_id']]);text=(R/ev['text']['path']).read_text(encoding='utf-8')
 ledger.append({'region':r,'pdf_page':pages[r['page_id']]['pdf_page'],'label':item['label'],'group':item['group'],'components':components.get(r['key'],item['components']),'grouping_policy':spec['grouping_policy'],'reading_order_index':doc['reading_order'].index(r['id']),'evidence':ev,'native_crop_bounds':[{'numerator':f.numerator,'denominator':f.denominator} for f in native],'raw_text_codepoints':len(text),'exact_text_pin':ev['text'],'visual_status':'Executor inspected original page, complete overlay boundary and grouped components; independent review pending','links':[l for l in doc['links'] if l['from']==r['id'] or l['to']==r['id']],'coverage_limits':r['coverage']})
write('region-ledger-final.json',{'task':'IG-2B02','source':doc['source'],'inventory_pin':pin(A/'final-verified/inventory.json'),'registry_pin':pin(A/'final-verified/identity-registry.json'),'ledger_scope':'Complete new assigned inventory on physical pages 5-8; preserved accepted and placeholder records stay exact in complete 44-page inventory.','regions':ledger,'preserved_context':scope['existing_context']['record'],'denominator_role':'Only new inventory regions; grouped diagram components do not add denominator units','independent_review':'pending'})
counts=dict(sorted(Counter(pages[r['page_id']]['pdf_page'] for r in newregions).items()));assert counts=={5:39,6:33,7:39,8:30}
assert report['denominator_regions']==130+36+141 and report['context_regions']==1
write('scope-report-final.json',{'assigned_pages':[5,6,7,8],'full_structural_pages':44,'task_denominator':141,'task_counts_by_physical_page':counts,'preserved_authored_denominator':130,'unprocessed_placeholder_denominator':36,'full_denominator':307,'context_regions':1,'context_denominator':0,'source_coverage_levels':report['levels'],'task_coverage_levels':{l:dict(Counter(r['coverage'][l]['status'] for r in newregions)) for l in ('transcription','descriptive_semantics','formal_semantics')},'represented_or_excluded_new_regions':0,'content_access':load(AR+'/context-access.json'),'absent_categories_observed':'No assigned standalone tables; callout legends are grouped within the Sample Leader Counter diagram. Sixteen sample unit counters and one annotated leader counter are explicit diagram regions.','sidecar_partition_hash':partition_hash(doc),'whole_record_IG1A_targets':'Not established by this sidecar; exact region/inventory reconciliation remains a separate gate','semantic_acceptance_granted':False,'executable_readiness':'unverified'})
oldctx=next(r for r in doc['regions'] if r['id']==scope['existing_context']['record']['id']);authored=next(r for r in newregions if r['key']=='ig2b02:p5:triarii-authored-tail');assert oldctx==scope['existing_context']['record']
write('context-authored-correspondence.json',{'source_sha256':doc['source']['sha256'],'physical_page':5,'context':oldctx,'context_evidence':scope['existing_context']['evidence'],'authored':authored,'authored_evidence':evmap[authored['id']],'correspondence':'Independently observed two-line completion of the Triarii entry. Existing context and new authored region refer to the same visible tail with distinct IDs and independently selected boxes.','context_denominator':0,'authored_denominator':1,'preserved_prior_links':[l for l in base['links'] if oldctx['id'] in (l['from'],l['to'])],'new_source_observed_link':[l for l in doc['links'] if l['to']==authored['id']],'lineage_decision':'Initial independent inventory authoring alongside retained context; no split/merge/remap or review transfer','review_transfer':False})
write('continuations.json',{'source_sha256':doc['source']['sha256'],'preserved_links':base['links'],'added_links':[l for l in doc['links'] if l not in base['links']],'page_4_basis':load(AR+'/context-access.json')['page_4'],'page_9':{'accessed':False,'reason':'Observed final page-8 paragraph ends complete at Initial Orders Phase. No unfinished page-8 fragment required a neighboring-page probe.'},'source_meaning_review':'pending'})
# Compare all unchanged nested records, original links/order, all original evidence
# bytes and every old registry entry without exposing unassigned source content.
retired=set(load(AR+'/retired-placeholder-memberships.json')['retired_ids'])
oldregions={r['id']:r for r in base['regions'] if r['id'] not in retired}
assert all(regions[i]==r for i,r in oldregions.items())
assert all(next(p for p in doc['pages'] if p['id']==old['id'])==old for old in base['pages'] if old['pdf_page'] not in (5,6,7,8))
assert all(e in doc['evidence'] for e in base['evidence']) and all(l in doc['links'] for l in base['links'])
assert [i for i in doc['reading_order'] if i in oldregions]==[i for i in base['reading_order'] if i in oldregions]
assert all(e in reg['entries'] for e in base['registry']['entries'])
assert all(next(p for p in doc['pages'] if p['id']==old['id'])[k]==old[k] for old in base['pages'] for k in ('id','key','pdf_page','source_revision','media_box','crop_box','effective_crop_box','rotation','user_unit'))
oldpins=[]
for e in base['evidence']:
 for k in ('text','image','crop_pdf'):assert pin(e[k]['path'])==e[k];oldpins.append(e[k])
existing=load(AR+'/existing-changes.json');unrelated=[];projection=[]
for p in existing['tracked_modified_files']:
 isview=p['path'] in ('docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md','docs/work/queue.json') or p['path'].startswith('docs/work/tasks/')
 if isview:projection.append({'before':p,'after':pin(p['path'])})
 else:assert pin(p['path'])==p;unrelated.append(p)
write('preservation-report.json',{'outcome':'passed','baseline':scope['baseline'],'registry_baseline':scope['registry'],'unchanged_regions':len(oldregions),'unchanged_pages':40,'old_registry_entries':len(base['registry']['entries']),'old_evidence_records':len(base['evidence']),'old_evidence_files':oldpins,'old_links_exact':True,'relative_old_order_exact':True,'retired_placeholder_memberships':list(retired),'retired_registry_entries_retained':True,'page_basis_geometry_all_44_preserved':True,'source_metadata_preserved':doc['source']==base['source'],'old_context_exact':oldctx==scope['existing_context']['record'],'unrelated_existing_changes_preserved':unrelated,'authorized_projection_changes':projection,'no_old_evidence_regenerated':True})
replays=[]
for dest in ('replay-one','replay-two'):
 for f in ('inventory.json','identity-registry.json'):
  a=pin(A/'authored'/f);b=pin(A/dest/f);assert a['sha256']==b['sha256'] and a['bytes']==b['bytes'];replays.append({'authored':a,'replay':b,'identical_bytes':True})
write('replay-report.json',{'outcome':'passed','persisted_registry':pin(A/'authored/identity-registry.json'),'specifications':pin(A/'author-specifications-final.json'),'script':pin(A/'author.py'),'fresh_output_directories':['replay-one','replay-two'],'comparisons':replays,'identity_allocation':'Only first authoring allocated new UUIDs; both replays reused all exact persisted bindings. No content/coordinate/hash-based remap.'})
checkpoint('final-inventory',['141 exact new evidence triples','Final complete inventory root validated','307 full denominator; context zero','Preservation and deterministic replay passed'],'Audit rational crops/locators, raw anomalies, geometric complement and final tests')
print('FINAL INVENTORY READY; denominators 141 task / 307 full / 0 context')
