from review_driver import *
import pdfplumber
from wgc.contracts.source import canonical_bytes
doc=load(D/'final-verified/inventory.json');base=load(B/'final-verified/inventory.json');ledger=load(D/'region-ledger-final.json')['regions']
regions={r['id']:r for r in doc['regions']};evs={e['region_id']:e for e in doc['evidence']};pages={p['id']:p for p in doc['pages']}
for path in (D/'authored/inventory.json',D/'authored/identity-registry.json',D/'final-verified/inventory.json',D/'final-verified/identity-registry.json'):
    assert path.read_bytes()==canonical_bytes(load(path))+b'\n',str(path)
ctx=regions['region:e8d77349-41ce-47d0-b678-eab1d0c8e8ed'];auth=next(r for r in regions.values() if r['key']=='ig2b02:p5:triarii-authored-tail')
assert ctx==next(r for r in base['regions'] if r['id']==ctx['id']) and ctx['denominator_role']=='context'
assert ctx['revision']=='af2a41ef3c500858f945d9a813c185f8ca3bc6fbc142e61348e6da5964d011c1'
assert ctx['box']==[71895,63131,495099,98485] and auth['id']!=ctx['id'] and auth['box']!=ctx['box']
ct=(ROOT/evs[ctx['id']]['text']['path']).read_bytes();at=(ROOT/evs[auth['id']]['text']['path']).read_bytes()
assert ct==at and at.startswith(b'heavy infantry,') and at.endswith(b'as a unit class.')
p4=regions['region:ba4a5094-22f5-4a67-8a19-6cc598a17b1b'];e4=evs[p4['id']]
assert p4['revision']=='49cc860a420db660e06df00c2d903b80ce40b66e2ee3296732f93df7a68927a0' and p4['box']==[586601,878787,929738,928030]
t4=(ROOT/e4['text']['path']).read_text(encoding='utf-8');assert t4.endswith('spear-armed')
added=[l for l in doc['links'] if l not in base['links']];link_rows=[]
for link in added:
    a,b=regions[link['from']],regions[link['to']]
    if a['id']==p4['id']:
        observed='Exact accepted page-4 crop ends spear-armed; original page-5/new authored tail begins heavy infantry. Both old-context and new-authored links retained as distinct identities.'
    elif a['key']=='ig2b02:p5:light-cavalry:text-a':
        observed='Page 5 visually ends magnifi-; page 6 begins cent Numidian light cavalry. Exact raw offsets/pins are recorded below, without joining stored text.'
    elif a['key']=='ig2b02:p8:line-composition-left':
        observed='4.32 begins at lower left and continues in full at upper right of the same page. No adjacent page needed.'
    elif link['kind']=='continuation':
        observed='Original paragraph wraps around adjacent counter. Beside-counter opening and full-width remainder are disjoint and source-contiguous in the paired sheets.'
    elif link['kind']=='illustrates':
        observed='Counter/diagram is visually adjacent to its named text/introduction in the original; source group includes all graphic boundaries and callouts.'
    elif link['kind']=='note_for':
        observed='Source note/example follows the referenced paragraph/section in the original. Full colored panel or italic example retained as a separate region.'
    else:raise AssertionError(link)
    assert link['kind'] in ('continuation','illustrates','note_for')
    link_rows.append({'link':link,'from':{'id':a['id'],'key':a['key'],'revision':a['revision'],'pdf_page':pages[a['page_id']]['pdf_page'],'box':a['box']},'to':{'id':b['id'],'key':b['key'],'revision':b['revision'],'pdf_page':pages[b['page_id']]['pdf_page'],'box':b['box']},'observed_result':observed,'result':'source_supported','evidence':[evs[a['id']],evs[b['id']]]})
def literal(key,value):
    r=next(r for r in regions.values() if r['key']==key);e=evs[r['id']];raw=(ROOT/e['text']['path']).read_bytes();text=raw.decode('utf-8');i=text.index(value)
    return {'region_id':r['id'],'revision':r['revision'],'key':key,'text':e['text'],'literal':value,'start':i,'end':i+len(value),'unit':'unicode_codepoints','bounds':'half_open'}
literal_joins=[literal(p4['key'],'spear-armed'),literal(auth['key'],'heavy infantry'),literal('ig2b02:p5:light-cavalry:text-a','magnifi-'),literal('ig2b02:p6:light-cavalry-tail','cent Numidian')]
out=R/'assigned-extraction-observations';out.mkdir()
extraction=[]
with pdfplumber.open(ROOT/doc['source']['pdf']['path']) as pdf:
    for n in (5,6,7,8):
        page=pdf.pages[n-1]
        text=page.extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
        path=out/f'page-{n}-raw.txt';path.write_text(text,encoding='utf-8',newline='\n')
        columns={}
        for label,box in [('left',(0,0,page.width/2,page.height)),('right',(page.width/2,0,page.width,page.height))]:
            clipped=page.crop(box).extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
            cp=out/f'page-{n}-{label}.txt';cp.write_text(clipped,encoding='utf-8',newline='\n');columns[label]=pin(cp)
        keys=[regions[i]['key'] for i in doc['reading_order'] if regions[i]['key'].startswith(f'ig2b02:p{n}:')]
        expected=[l['region']['key'] for l in ledger if l['pdf_page']==n];assert keys==expected
        extraction.append({'pdf_page':n,'raw_full_page':pin(path),'raw_columns':columns,'first_eight_raw_lines':text.splitlines()[:8],'explicit_reading_order':keys,'visual_review':'Source reviewed left column then right; diagrams accompany nearby entries; furniture explicitly ordered separately. Raw full-page extraction visibly interleaves corresponding column lines and is not adopted as reading order.'})
write('continuation-audit.json',{'outcome':'passed','observed_utc':utc(),'preserved_context':ctx,'authored_tail':auth,'correspondence_report':pin(D/'context-authored-correspondence.json'),'same_raw_tail_bytes':True,'context_zero_denominator':True,'no_review_transfer':True,'pinned_page_4_region':p4,'page_4_access':'Only existing exact text/PNG/crop-PDF pins; text/PNG directly viewed. No whole-page-4 render or source extraction.','added_links':link_rows,'preserved_links':base['links'],'literal_join_offsets':literal_joins,'page_9':{'accessed':False,'reason':'Independently viewed final page-8 paragraph ends complete at his Initial Orders Phase.; no originating unfinished fragment or need.'},'pages_10_44':'Geometry/count checks only.','reading_order':extraction,'original_first_note_refinement':'Initial full-page visual notes abbreviated the bottom word as magni-. Enlarged comparison and exact raw extraction establish magnifi- / cent. The original-first note is preserved; no publisher bytes or extraction were normalized.','readiness':'Structural links only, no game-rule legality decisions or semantic acceptance.'})
print('CONTINUATIONS',len(link_rows),'all source-supported; context exact; page 9 untouched')
