"""Independent mechanical review; exact pinned inputs only, no tree discovery."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
RUN = Path(__file__).parent
BASE = Path('private/workflow/runs/IG-2B05/continuation-17-20-dependency03')
SESSION = Path('private/workflow/orchestrator/20261016T154824Z-fae43db9/002-IG-2B05-reviewer-d526bcf5')
def load(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
def pin(p):
    b = (ROOT / p).read_bytes()
    return {'path': str(p).replace('\\', '/'), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
COMMON = dict(task='IG-2B05', role='reviewer', actor='ig2:002-IG-2B05-reviewer-d526bcf5:reviewer',
              model='gpt-6.1-sol', reasoning='high', configuration_evidence=(SESSION/'runtime-configuration.json').as_posix(),
              configuration_sha256=sha(SESSION/'runtime-configuration.json'))
checks = {}
def check(name, condition): checks[name] = bool(condition)
task = load(SESSION/'task.json')
delivery = load(BASE/'delivery.json')
final = load(BASE/'final-verified/inventory.json')
registry = load(BASE/'final-verified/identity-registry.json')
ledger = load(BASE/'region-ledger.json')
part = load(BASE/'authored-partition.json')
assigned_pages = {p['id'] for p in final['pages'] if p['pdf_page'] in [17,18,19,20]}
assigned = {r['id']: r for r in final['regions'] if r['page_id'] in assigned_pages}
ev = {e['region_id']:e for e in final['evidence'] if e['region_id'] in assigned}
byid = {r['id']:r for r in final['regions']}
bykey = {r['key']:r for r in assigned.values()}
check('delivery_criteria_exact', delivery['criteria'] == task['acceptance'])
check('assigned_sets', set(assigned)==set(ev)=={r['region_id'] for r in ledger['regions']})
check('partition_keys', {r['key'] for r in part['regions']} == set(bykey))
check('ledger_identity_geometry_evidence', all(
    x['region_revision']==assigned[x['region_id']]['revision'] and
    x['box']==assigned[x['region_id']]['box'] and x['evidence']==ev[x['region_id']] and
    x['reading_order_index']==final['reading_order'].index(x['region_id']) and
    x['coverage']==assigned[x['region_id']]['coverage'] and
    all(c['region_id']==x['region_id'] and c['evidence_id']==x['evidence']['id'] and
        c['disposition']=='structurally_inventoried' for c in x['components']) for x in ledger['regions']))
check('partition_ledger_components', all(
    next(x for x in ledger['regions'] if x['key']==r['key'])['pixel_box']==r['pixel_box'] and
    [c['description'] for c in next(x for x in ledger['regions'] if x['key']==r['key'])['components']]==r['components']
    for r in part['regions']))
components = [c['id'] for x in ledger['regions'] for c in x['components']]
check('all_components_unique', len(components)==len(set(components))==138)
check('assigned_levels_unprocessed', all(c['status']=='unprocessed' and c['gap'] for r in assigned.values() for c in r['coverage'].values()))
check('assigned_dpi', all(e['render_parameters']['dpi']==144 for e in ev.values()))
check('registry_persisted', registry==load(BASE/'persisted-registry.json')==final['registry'])

# Accepted dependency records are consumed only for mechanical equality, never dumped as context.
bp=Path('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/inventory.json')
br=Path('private/workflow/runs/IG-2B04/continuation-13-16-rg04/final-verified/identity-registry.json')
assert sha(bp)=='5ac48725279f2a44d77bdbc6a14ca8bb6c828ee709b5f143b117700bb4c5f656'
assert sha(br)=='50f254c8f3ceb8cc0feb688ea8b31f5a39b4bb6c76fbcd89fa2d45d87d245375'
old=load(bp); oldreg=load(br); retired=set(task['target_ids'])
check('preserved_source_pages_toolchain', final['source']==old['source'] and final['pages']==old['pages'] and len(final['pages'])==44 and final['toolchain']==old['toolchain'])
check('preserved_nonassigned_regions', [r for r in final['regions'] if r['id'] not in assigned]==[r for r in old['regions'] if r['id'] not in retired])
check('exact_retirement', {r['id'] for r in old['regions']}-{r['id'] for r in final['regions']}==retired)
check('preserved_evidence_links', final['evidence'][:len(old['evidence'])]==old['evidence'] and final['links'][:len(old['links'])]==old['links'])
check('preserved_registry_entries', all(x in registry['entries'] for x in oldreg['entries']))
check('preserved_reading_order', [x for x in final['reading_order'] if x not in assigned]==[x for x in old['reading_order'] if x not in retired])
retained_artifacts=[e[k] for e in old['evidence'] for k in ['crop_pdf','image','text']]
check('retained_evidence_bytes', all(pin(p['path'])==p for p in retained_artifacts))

def normalize(doc, prefix):
    d=copy.deepcopy(doc); del d['revision']
    for e in d['evidence']:
        if e['region_id'] in assigned:
            for k in ['crop_pdf','image','text']:
                assert e[k]['path'].startswith(prefix+'/')
                e[k]['path']='$OUTPUT/'+e[k]['path'][len(prefix)+1:]
    return d
normal = normalize(final,(BASE/'final-verified').as_posix())
from wgc.sources.inventory import digest, coverage
reported_replays=load(BASE/'replay-report.json')
hash_normal=copy.deepcopy(normal)
for e in hash_normal['evidence']:
    if e['region_id'] in assigned:
        for k in ['crop_pdf','image','text']:e[k]['path']=e[k]['path'].replace('$OUTPUT/','<DERIVATION>/',1)
check('reported_normalized_final_hash',digest(hash_normal)==reported_replays['normalized_final_sha256'])
replays=[]
for name in ['replay-1','replay-2']:
    replay=load(BASE/name/'inventory.json')
    check(name+'_complete_logical_equality',normalize(replay,(BASE/name).as_posix())==normal)
    check(name+'_registry_bytes',sha(BASE/name/'identity-registry.json')==sha(BASE/'final-verified/identity-registry.json'))
    rep_ev={e['region_id']:e for e in replay['evidence'] if e['region_id'] in assigned}
    check(name+'_assigned_artifact_equality',set(rep_ev)==set(ev) and all(
        sha(rep_ev[r][k]['path'])==sha(ev[r][k]['path']) and
        rep_ev[r][k]['bytes']==ev[r][k]['bytes'] for r in ev for k in ['crop_pdf','image','text']))
    reported=next(x for x in reported_replays['replays'] if x['name']==name)
    check(name+'_reported_complete_hashes_counts',reported['assigned_region_set_sha256']==digest(sorted(assigned)) and
          reported['complete_region_set_sha256']==digest(sorted(r['id'] for r in replay['regions'])) and
          reported['complete_evidence_set_sha256']==digest(sorted(e['id'] for e in replay['evidence'])) and
          reported['normalized_sidecar_sha256']==digest(hash_normal) and len(reported['normalized_fields'])==306 and
          len(reported['compared_artifacts'])==306 and reported['counts']=={'all_regions':646,'all_evidence':622,'assigned_regions':102,'assigned_artifacts':306})
    replays.append({'name':name,'inventory':pin(BASE/name/'inventory.json'),'assigned_artifacts_compared':len(ev)*3})

report_names=['region-ledger.json','continuations.json','coverage-report.json','source-pins.json','toolchain.json',
              'original-page-inspection.json','preservation-report.json','replay-report.json','validation-report.json',
              'crop-review.json','source-reference-index.json','set-validation-report.json']
check('all_current_report_envelopes',all(
    (d:=load(BASE/name))['inventory']==pin(BASE/'final-verified/inventory.json') and
    d['inventory_revision']==final['revision'] and d['registry']==pin(BASE/'final-verified/identity-registry.json') and
    set(d['assigned_ids'])==set(assigned) and {e['evidence_id'] for e in d['assigned_evidence']}=={e['id'] for e in ev.values()}
    for name in report_names))
index=load(BASE/'source-reference-index.json')
check('indexed_report_pins',all({k:p[k] for k in ['path','bytes','sha256']}==pin(p['path']) and load(p['path'])['inventory_revision']==p['inventory_revision']==final['revision'] for p in index['reports']))
check('index_ledger_pointers', all(
    (x:=load(p['ledger_path'])['regions'][int(p['json_pointer'].split('/')[-1])])['region_id']==p['region_id'] and
    x['region_revision']==p['region_revision'] and x['evidence']['id']==p['evidence_id'] for p in index['region_entries']))
check('literal_reference_offsets', all((ROOT/p['text_path']).read_text(encoding='utf-8')[p['start']:p['end']]==p['literal'] for p in index['literal_numeric_references']))
continuations=load(BASE/'continuations.json')
locators=[]
for boundary in continuations['boundaries']:
    for k in ['from','to','assigned_entry']:
        if k in boundary: locators.append(boundary[k])
check('continuation_locators', all(
    (r:=byid[p['region_id']])['revision']==p['revision'] and r['page_id']==p['page_id'] and r['box']==p['box'] and
    ev[p['region_id']]['id']==p['evidence_id'] for p in locators))
check('new_links_complete', [{k:p[k] for k in ['kind','from','to','reason']} for p in continuations['links']]==final['links'][len(old['links']):])
check('new_link_locators',all(
    (r:=byid[p['region_id']])['revision']==p['revision'] and r['page_id']==p['page_id'] and r['box']==p['box'] and
    ev[p['region_id']]['id']==p['evidence_id'] for link in continuations['links'] for p in [link['from_locator'],link['to_locator']]))

# Independently confirm that all sheet images are literal unscaled crop pixels.
from PIL import Image
sheet_count=0; sheet_regions=[]; pixel_errors=[]
crop_review=load(BASE/'crop-review.json')
for s in crop_review['sheets']:
    metadata=load(s['source_metadata']['path'])
    sheet_count+=1
    sheet_regions.extend(s['region_keys'])
    check('sheet_'+str(sheet_count)+'_pins', pin(s['sheet']['path'])==s['sheet'] and pin(s['source_metadata']['path'])==s['source_metadata'] and all(pin(p['path'])==p for p in s['reviewed_images']))
    images=[Image.open(ROOT/p).convert('RGB') for p in metadata['source_images']]
    sheet=Image.open(ROOT/s['sheet']['path']).convert('RGB')
    width=max(520,max(im.width for im in images))+20
    y=10
    for i in range(0,len(images),2):
        for j in range(2):
            if i+j>=len(images): break
            im=images[i+j]; x=10+j*width
            if sheet.crop((x,y+32,x+im.width,y+32+im.height)).tobytes()!=im.tobytes():
                pixel_errors.append(metadata['source_images'][i+j])
        y+=max(im.height for im in images[i:i+2])+52
    for im in images: im.close()
    sheet.close()
check('all_102_crops_in_sheets_once',Counter(sheet_regions)==Counter(bykey.keys()))
check('all_sheet_crop_pixels_equal',not pixel_errors)
original_equality={str(n):sha(RUN.relative_to(ROOT)/f'original-{n}.png')==sha(BASE/f'original-pages/page-{n}.png') for n in [17,18,19,20]}
check('independent_original_renders_equal',all(original_equality.values()))

coverage_report=load(BASE/'coverage-report.json')
check('full_counts',coverage_report['full_counts']=={k:len(final[k]) for k in ['pages','regions','evidence','links']})
check('full_denominator',coverage_report['full_44_page_inventory']['denominator_regions']==sum(r['denominator_role']=='inventory' for r in final['regions']))
check('full_coverage_report_exact',coverage_report['full_44_page_inventory']==coverage(final))
check('context_zero',coverage_report['context_only']['assigned_denominator_contribution']==0 and continuations['context_inventory_denominator']==0 and not continuations['context_only_accesses'])
preserve_path=Path('private/workflow/runs/IG-2B05/recovery-20261016-dependency03/preserve-manifest.json')
check('recovery_preserve_manifest_pin',sha(preserve_path)=='fbcd7661481d0f8948bf896df27e3dd255ea4592943ef62bda8acab2c48a885b')
preserve=load(preserve_path)
check('blocked_attempt_967_artifacts_unchanged',all(all(pin(p['path'])[k]==v for k,v in p.items()) for p in preserve['artifacts']))
check('blocked_evidence_unchanged',sha(task['continuation_authorization']['blocked_evidence'])==task['continuation_authorization']['blocked_sha256'])
check('frozen_delivery_2710_artifacts_still_unchanged',all(pin(p['path'])==p for p in delivery['artifacts']))
result={**COMMON,'format':'wgc-independent-review-audit-1','checks':checks,'all_passed':all(checks.values()),
        'failed_checks':[k for k,v in checks.items() if not v], 'retained_artifact_checks':len(retained_artifacts),
        'counts':{k:len(final[k]) for k in ['pages','regions','evidence','links']},
        'assigned_regions':len(assigned),'components':len(components),'replays':replays,
        'independent_original_renders_equal':original_equality,'sheet_count':sheet_count,
        'continuation_locators_checked':len(locators),'indexed_reports_checked':len(index['reports']),
        'numeric_reference_offsets_checked':len(index['literal_numeric_references'])}
(RUN/'technical-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
hash_audit=load(RUN/'hash-audit.json')
(RUN/'hash-audit.json').write_text(json.dumps({**COMMON,**hash_audit},indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['all_passed','failed_checks','counts','assigned_regions','components','sheet_count']}))
raise SystemExit(0 if result['all_passed'] else 1)
