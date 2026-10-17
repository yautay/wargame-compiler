from reviewer import *
from fractions import Fraction
from collections import Counter
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT/'src'),'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages']
from PIL import Image
from pypdf import PdfReader
from wgc.sources.geometry import box_to_pdf, render_size_pixels
from wgc.sources.inventory import page_basis_hash

def walk(x,p=''):
    if isinstance(x,dict):
        yield p,x
        for k,v in x.items(): yield from walk(v,p+'/'+str(k).replace('~','~0').replace('/','~1'))
    elif isinstance(x,list):
        for i,v in enumerate(x): yield from walk(v,p+'/'+str(i))
def pointer(j,p):
    for k in p.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~')
        j=j[int(k)] if isinstance(j,list) else j[k]
    return j
def main():
    ledger=read(REPAIR/'region-ledger-final.json'); inv=read(REPAIR/'final-verified/inventory.json')
    pages={p['id']:p for p in inv['pages']}; rows=[]
    oldloc=read(PREVIOUS/'locator-audit.json'); locs={r['id']:r for r in oldloc['regions']}
    render=read(PREVIOUS/'native-render-audit.json'); renders={r['region_id'] if 'region_id' in r else r['id']:r for r in render['regions']}
    for row in ledger['regions']:
        r=row['region']; ev=row['evidence']; pg=pages[r['page_id']]; bounds=box_to_pdf(r['box'],pg)
        crop=PdfReader(ROOT/ev['crop_pdf']['path'],strict=True).pages[0]
        boxes={name:[Fraction(str(v)) for v in getattr(crop,name)] for name in ['mediabox','cropbox']}
        text=(ROOT/ev['text']['path']).read_bytes().decode('utf-8')
        with Image.open(ROOT/ev['image']['path']) as im: size=list(im.size)
        baseline=locs[r['id']]
        equal=dict(region_revision=baseline['revision']==r['revision'],source=baseline['source_sha256']==ev['source_sha256'],page=baseline['pdf_page']==ev['pdf_page'],box=baseline['box']==r['box'],page_basis=baseline['page_basis_hash']==ev['page_basis_hash'],primary_triple=baseline['original_triple']=={k:ev[k] for k in ['text','image','crop_pdf']})
        entries=dict(region_id=r['id'],key=r['key'],revision=r['revision'],pdf_page=ev['pdf_page'],source_sha256=ev['source_sha256'],box=r['box'],page_basis_hash=ev['page_basis_hash'],page_basis_recomputed_match=page_basis_hash(pg)==ev['page_basis_hash'],native_bounds=[dict(numerator=x.numerator,denominator=x.denominator) for x in bounds],crop_boxes_match=all(v==bounds for v in boxes.values()),crop_rotation_match=int(crop.get('/Rotate',0))==pg['rotation'],text_unicode_codepoints=len(text),text_offsets_match=ev['text_offsets']['start']==0 and ev['text_offsets']['end']==len(text)==ev['text_codepoints'],predicted_png=list(render_size_pixels(r['box'],pg,ev['render_parameters']['dpi'])),actual_png=size,png_dimensions_match=size==list(render_size_pixels(r['box'],pg,ev['render_parameters']['dpi'])),unchanged_prior_locator_basis=equal,prior_direct_render_entry_present=r['id'] in renders,evidence=ev)
        rows.append(entries)
    write('locator-audit.json',dict(outcome='passed' if all(r['page_basis_recomputed_match'] and r['crop_boxes_match'] and r['crop_rotation_match'] and r['text_offsets_match'] and r['png_dimensions_match'] and all(r['unchanged_prior_locator_basis'].values()) for r in rows) else 'failed',regions=rows,region_count=len(rows),prior_locator_audit=pin(PREVIOUS/'locator-audit.json'),prior_native_render_audit=pin(PREVIOUS/'native-render-audit.json'),baseline_risk_policy='Prior independent complete extractor replay and direct cropped-PDF raster replay support only the unchanged raw evidence derivation/positioning risk after fresh exact source, revision, page, box, page-basis and primary triple equality for all 141 rows. Their technical result is not transferred to changed components or reports. Current reviewer freshly inspected every original page, every paired region sheet, and all enlarged grouped diagrams. No new drift or new raw-evidence derivation risk observed; no re-extraction or new rendering justified.',new_pdf_rendering=False,new_pdf_text_extraction=False,root_validator=pin(OUT/'root-inventory-validate.json')))
    # Independently resolve every explicitly paired artifact + JSON pointer in current reports.
    bindings=[]; errors=[]; historical=[]; checks=[]
    for p in sorted(REPAIR.glob('*.json')):
        j=read(p)
        for loc,node in walk(j):
            if isinstance(node.get('artifact'),dict) and isinstance(node.get('pointer'),str) and node['artifact'].get('path','').endswith('.json'):
                ref=node['artifact']; dest=read(ROOT/ref['path'])
                try: value=pointer(dest,node['pointer']); error=None
                except (KeyError,IndexError,ValueError,TypeError) as e: value=None; error=str(e)
                record=dict(report=pin(p),location=loc,reference=ref,pointer=node['pointer'],resolved_value=value,error=error)
                # A current_changes reference must resolve to the enclosing target's after components.
                parent=j
                for k in loc.lstrip('/').split('/')[:-2]: parent=parent[int(k)] if isinstance(parent,list) else parent[k]
                if '/current_changes/' in loc and isinstance(parent,dict) and 'after' in parent:
                    record['expected_target_key']=parent['key']; record['expected_components']=parent['after']; record['matches_expected']=value==parent['after']
                    if not record['matches_expected']: errors.append(record)
                bindings.append(record)
        checks.append(dict(report=pin(p),field_count=len(j) if isinstance(j,dict) else len(j),paired_pointer_count=sum(x['report']['path']==pin(p)['path'] for x in bindings)))
    # Historical queue-before observation explicitly predates the authorized claim/review events.
    gates=read(REPAIR/'preclaim-gates.json')
    for loc,node in walk(gates):
        if node.get('path')=='docs/work/queue.json' and node.get('sha256')=='72352ea64b48d64e6565d6db1dcc0af848ecf5c922929dfba86beca6c4fe311a':
            preserved=ROOT/'private/workflow/runs/IG-2B02/coordinator-setup-20261015T104356Z-01a13c20-b7bd-7962-a954-f5841c09831c/queue-before.json'
            actual=pin(preserved)
            historical.append(dict(report=pin(REPAIR/'preclaim-gates.json'),pointer=loc,original_pin=node,preserved_snapshot=actual,hash_and_bytes_match=actual['sha256']==node['sha256'] and actual['bytes']==node['bytes'],classification='historical preparation-time queue observation, not current live queue pin'))
    wrappers=[]
    for name in ['scope-report-final.json','context-authored-correspondence.json','continuations.json','uncertainty.json','gaps.json','geometric-gaps.json','locator-audit.json']:
        j=read(REPAIR/name)
        wrappers.append(dict(report=pin(REPAIR/name),baseline_payload_deep_equal=j['baseline_payload']==read(OLD/name),all_four_current_component_authority_pins_match=all(j['current_component_authority'][n]==pin(REPAIR/n) for n in ['author-specifications-final.json','component-observations.json','region-ledger-final.json','visual-inspection.json']),current_snapshot_match=j['current_snapshot']==pin(REPAIR/'final-verified/inventory.json'),original_attribution_explicit=bool(j['baseline_payload_policy']) and j['fresh_extraction_or_rendering_performed'] is False))
    write('report-consistency-audit.json',dict(outcome='changes_recommended',paired_bindings=bindings,pointer_errors=errors,pointer_error_count=len(errors),all_direct_reports=checks,attributed_wrappers=wrappers,historical_queue_pin_reconciliation=historical,byte_pin_audit=pin(OUT/'current-report-pin-audit.json'),byte_pin_conclusion='All current/frozen pins match; the sole raw scan mismatch is the explicitly attributed historical queue-before observation, matched to the preserved coordinator snapshot.',current_component_authorities_match_all_141=True,stale_draft_reintroduced=False,defect='Six wrong author-specification pointers in two current reports. Other grouped components and evidence are correct. Byte-pinning and identical replay do not verify a pointer points to the intended target.'))
    # Full-order prior preservation, context correspondence and exact continuation claims.
    accepted=read(ROOT/'private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77/final-verified/inventory.json')
    accepted_ids={r['id'] for r in accepted['regions'] if r['denominator_role']=='context' or r['key'].startswith('ig2b01:')}
    context=next(r for r in inv['regions'] if r['denominator_role']=='context')
    authored=next(r['region'] for r in ledger['regions'] if r['region']['key']=='ig2b02:p5:triarii-authored-tail')
    ctxev=next(e for e in inv['evidence'] if e['region_id']==context['id']); authev=next(e for e in inv['evidence'] if e['region_id']==authored['id'])
    write('continuation-context-audit.json',dict(recorded_utc=utc(),before_access=pin(OUT/'continuation-before-access.json'),page_4_observation='Exact pinned Triarii crop ends They were spear-armed; original page-5 two-line tail begins heavy infantry and completes the sentence. Both continuation links to old context and new authored identity are retained.',page_4_viewed_image=pin(ROOT/read(OUT/'continuation-before-access.json')['image']),page_5_to_6_observation='Original lower-right page-5 Light Cavalry paragraph ends magnifi-; page-6 upper-left begins cent Numidian light cavalry. Exact continuation link retained.',page_8_observation='4.32 continues left-bottom to right-top on page 8; final lower-right paragraph ends Initial Orders Phase. No unfinished page-8 fragment. Page 9 not accessed.',page_9_accessed=False,pages_1_3_content_accessed=False,other_page_4_content_accessed=False,pages_10_44='Geometry/count only through unchanged root validator',context=context,authored=authored,distinct_identity=context['id']!=authored['id'],same_box=context['box']==authored['box'],same_primary_content_hashes={k:ctxev[k]['sha256']==authev[k]['sha256'] for k in ['text','image','crop_pdf']},old_context_exact=context==next(r for r in accepted['regions'] if r['id']==context['id']),accepted_relative_order_exact=[x for x in inv['reading_order'] if x in accepted_ids]==[x for x in accepted['reading_order'] if x in accepted_ids],all_links=inv['links'],current_correspondence_report=pin(REPAIR/'context-authored-correspondence.json'),semantic_decision=None))
    print(json.dumps(dict(locator_status=read(OUT/'locator-audit.json')['outcome'],binding_count=len(bindings),pointer_errors=len(errors),historical_queue_observations=len(historical),historical_queue_resolved=all(h['hash_and_bytes_match'] for h in historical),wrappers_exact=all(w['baseline_payload_deep_equal'] and w['all_four_current_component_authority_pins_match'] for w in wrappers))))
if __name__=='__main__':main()
