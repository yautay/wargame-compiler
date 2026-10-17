from ops import *
from fractions import Fraction
from collections import Counter
from wgc.sources.inventory import validate,page_basis_hash
from wgc.sources.geometry import box_to_pdf,render_size_pixels
from pypdf import PdfReader
from PIL import Image
import pdfplumber
doc=load(AR+'/final-verified/inventory.json');new=load(AR+'/new-evidence.json');ledger=load(AR+'/region-ledger-final.json');regions={r['id']:r for r in doc['regions']};pages={p['id']:p for p in doc['pages']}
rows=[];uncertain=[]
(A/'render-replay').mkdir(exist_ok=False)
for e in new:
 r=regions[e['region_id']];p=pages[e['page_id']];native=box_to_pdf(r['box'],p);expected=render_size_pixels(r['box'],p,144)
 assert e['box']==r['box'] and e['region_revision']==r['revision'] and e['source_sha256']==doc['source']['sha256'] and e['page_basis_hash']==page_basis_hash(p) and e['pdf_page']==p['pdf_page']
 assert all(pin(e[k]['path'])==e[k] for k in ('text','image','crop_pdf'))
 raw=(R/e['text']['path']).read_bytes();text=raw.decode('utf-8');assert not raw.startswith(b'\xef\xbb\xbf') and '\r' not in text
 assert e['text_codepoints']==len(text) and e['text_offsets']=={'unit':'unicode_codepoints','bounds':'half_open','start':0,'end':len(text)}
 reader=PdfReader(R/e['crop_pdf']['path'],strict=True);assert len(reader.pages)==1
 cp=reader.pages[0];actual_media=[Fraction(str(v)) for v in cp.mediabox];actual_crop=[Fraction(str(v)) for v in cp.cropbox]
 assert actual_media==native and actual_crop==native and cp.rotation%360==p['rotation'],(r['key'],actual_media,native)
 assert Fraction(str(cp.get('/UserUnit',1)))==1
 render_prefix=A/'render-replay'/r['id'].split(':')[1]
 render_check=run('render-replay-'+r['id'].split(':')[1],[POP+'/pdftoppm.EXE','-f','1','-l','1','-singlefile','-cropbox','-r','144','-png',str(R/e['crop_pdf']['path']),str(render_prefix)])
 assert render_check['exit_code']==0
 replay_pin=pin(str(render_prefix)+'.png');assert replay_pin['sha256']==e['image']['sha256'] and replay_pin['bytes']==e['image']['bytes']
 with pdfplumber.open(R/e['crop_pdf']['path']) as extracted:
  view=extracted.pages[0].crop(extracted.pages[0].bbox);replayed_text=view.extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
 assert replayed_text.encode('utf-8')==raw
 with Image.open(R/e['image']['path']) as im:actual_pixels=im.size
 assert expected==actual_pixels==(e['render_parameters']['width_pixels'],e['render_parameters']['height_pixels'])
 assert e['text_parameters']['version']=='0.11.9' and e['crop_parameters']['version']=='6.10.0' and e['render_parameters']['dpi']==144 and e['render_parameters']['version'].startswith('pdftoppm version 26.07.0')
 native_report=[{'numerator':f.numerator,'denominator':f.denominator} for f in native]
 anomalies=[];cursor=0
 for line in text.splitlines(keepends=True):
  visible=line.rstrip('\n')
  if visible.endswith('-'):anomalies.append({'kind':'literal_line_end_hyphen','offset':cursor+len(visible)-1,'excerpt':visible,'policy':'Retained byte-for-byte; neither dehyphenated nor resolved automatically.'})
  cursor+=len(line)
 for index,char in enumerate(text):
  if char in ('\ufffd','\x00'):anomalies.append({'kind':'extraction_codepoint_anomaly','offset':index,'codepoint':ord(char)})
 if not text:anomalies.append({'kind':'empty_extraction','policy':'Valid geometry-only source or unrecognized graphical text; PNG is not verified transcription.'})
 if r['kind']=='diagram':anomalies.append({'kind':'diagram_literal_extraction','policy':'Raw extraction does not preserve visual rating layout, graphic arrows or image-only glyphs. Component ledger and exact PNG/crop remain separate.'})
 if anomalies:uncertain.append({'region_id':r['id'],'revision':r['revision'],'key':r['key'],'evidence_id':e['id'],'text_pin':e['text'],'anomalies':anomalies})
 rows.append({'region_id':r['id'],'region_revision':r['revision'],'key':r['key'],'source_sha256':e['source_sha256'],'pdf_page':p['pdf_page'],'page_basis_hash':e['page_basis_hash'],'box':r['box'],'rational_native_bounds':native_report,'crop_mediabox_exact':True,'crop_cropbox_exact':True,'rotation_exact':True,'user_unit_normalized':True,'offsets_exact':True,'raw_utf8_bytes_unchanged':True,'replayed_text_bytes_identical':True,'render_replay_command':render_check,'replayed_png':replay_pin,'replayed_png_bytes_identical':True,'expected_pixels':list(expected),'actual_pixels':list(actual_pixels),'triple_pins':[e[k] for k in ('text','image','crop_pdf')],'outcome':'passed'})
root_report=validate(doc,R)
write('locator-audit.json',{'outcome':'passed','inventory':pin(A/'final-verified/inventory.json'),'audited_new_locators':len(rows),'new_text_png_crop_pdf_files':len(rows)*3,'regions':rows,'root_validation':root_report,'old_locator_preservation':'Exact old evidence plus all old bytes verified in preservation-report and unchanged root validator. No regeneration.'})
write('uncertainty.json',{'scope':'New assigned physical pages 5-8 only','literal_anomalies':uncertain,'small_counter_glyphs':[{'region_id':r['id'],'key':r['key'],'uncertainty':r['uncertainty']} for r in regions.values() if r['key'].startswith('ig2b02:') and r['uncertainty']],'reading_order':'Explicit ledger order; full-page extraction can interleave two columns and is not the authoring order.','transcription':'Partial for every new region; no complete verified transcription asserted. Original publisher bytes and exact per-region extraction are unchanged.','boundary_uncertainty':{'page_4_to_5':'Observed exact accepted fragment ends spear-armed; current authored tail begins heavy infantry. Old context stays unchanged.','page_5_to_6':'Literal magnifi- / cent join observed; retain separate raw strings and linked region identities.','page_8_to_9':'No content probe needed; final assigned paragraph ends complete.'}})
# Exact complement of the disjoint inventory rectangles, in normalized units.
complements=[]
for page in doc['pages']:
 if page['pdf_page'] not in (5,6,7,8):continue
 boxes=[r['box'] for r in regions.values() if r['page_id']==page['id'] and r['denominator_role']=='inventory'];ys=sorted({0,1000000,*[v for b in boxes for v in (b[1],b[3])]});gaps=[]
 for y0,y1 in zip(ys,ys[1:]):
  occupied=sorted((b[0],b[2]) for b in boxes if b[1]<=y0 and b[3]>=y1);cursor=0
  for x0,x1 in occupied:
   if cursor<x0:gaps.append([cursor,y0,x0,y1])
   cursor=max(cursor,x1)
  if cursor<1000000:gaps.append([cursor,y0,1000000,y1])
 area=sum((b[2]-b[0])*(b[3]-b[1]) for b in gaps);expected=next(p['unaccounted_area_trillionths'] for p in root_report['pages'] if p['pdf_page']==page['pdf_page']);assert area==expected
 complements.append({'page_id':page['id'],'pdf_page':page['pdf_page'],'rectangles':gaps,'unaccounted_area_trillionths':area,'description':'Exact geometric complement includes margins and inter-region whitespace; it remains an explicit geometric gap, not represented/excluded semantics or a percentage of rule meaning.'})
write('geometric-gaps.json',{'unit':'integer trillionths of normalized page area','assigned_page_complement':complements,'full_page_accounting':root_report['pages'],'content_claim':'Geometry only; no approved exclusion or semantic coverage inferred.'})
newregions=[r for r in regions.values() if r['key'].startswith('ig2b02:')]
write('gaps.json',{'representation_gaps':[{'region_id':r['id'],'revision':r['revision'],'key':r['key'],'levels':r['coverage']} for r in newregions],'content_gaps':{'executor_uninventoried_visible_assigned_components':[],'status':'No visible assigned component omission found during executor original/overlay/component inspection; completeness remains subject to independent review.','literal_transcription_gaps':'All new regions remain partial; diagrams and counters preserve image-based components not guaranteed by raw extraction.','outside_assigned_scope':'Thirty-six unchanged unprocessed inventory placeholders on pages 9-44; no source content inspection.'},'geometric_gaps_reference':pin(A/'geometric-gaps.json'),'source_IG_reconciliation':'Pending exact full-record region targets and whole-inventory basis; sidecar partition hashes do not replace frozen IG-1A targets.','human_authenticity_and_semantic_acceptance':'Separate pending gate','executable_readiness':'unverified'})
write('visual-inspection.json',{'actor':load(AR+'/configuration.json')['actor'],'model':'gpt-6.1-sol','reasoning':'high','inspection_kind':'Executor self-inspection, not independent technical/source-meaning review','assigned_pages':[{'pdf_page':n,'original':pin(A/f'inspection/original-{n:02}.png'),'overlay':pin(A/f'inspection/overlay-{n:02}.png'),'viewed':True,'region_count':sum(e['pdf_page']==n for e in new),'result':'Every visible heading/clause/bullet/note/example/diagram/counter/callout/editorial item accounted by displayed bounds and explicit grouped ledger. No visible assigned omissions found.'} for n in (5,6,7,8)],'overlay_index':pin(A/'overlay-index.json'),'enlarged_component_sheets':[pin(A/f'inspection/components-{n:02}.png') for n in (5,6,7)],'component_observations':pin(A/'component-observations.json'),'every_region':[{'region_id':r['id'],'revision':r['revision'],'key':r['key'],'original_and_overlay_boundary_inspected':True,'components':next(x['components'] for x in ledger['regions'] if x['region']['id']==r['id']),'component_evidence_id':next(e['id'] for e in new if e['region_id']==r['id']),'result':'Bounds include observed source component group; raw extraction is separate from verified transcription.'} for r in newregions],'page_4_access':load(AR+'/context-access.json')['page_4'],'page_9_accessed':False,'pages_10_44':'Structural counts/geometry only','independent_review':'pending'})
checkpoint('audited',['All 141 exact locators, rational crop bounds, offsets and predicted/actual PNG sizes passed','Preservation, replay and geometric complement passed','Complete ledger and executor visual inspection reports ready'],'Run unchanged source tests and required repository checks; freeze delivery')
print('AUDIT PASSED: 141 locators / 423 exact files; rational native bounds exact')
