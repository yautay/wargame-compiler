from review_driver import *
from fractions import Fraction
from PIL import Image
from pypdf import PdfReader
from wgc.sources.pdf import extract_evidence
from wgc.sources.geometry import box_to_pdf,render_size_pixels
from wgc.sources.inventory import page_basis_hash
doc=load(D/'final-verified/inventory.json');ledger=load(D/'region-ledger-final.json')['regions']
assert len(ledger)==141
(R/'locator-increments').mkdir()
rows=[];anomalies=[]
for i,l in enumerate(ledger,1):
    started=utc();clock=time.monotonic();r=l['region'];p=next(p for p in doc['pages'] if p['id']==r['page_id']);e=l['evidence']
    assert r['key'].startswith('ig2b02:') and p['pdf_page'] in (5,6,7,8)
    directory=(R/'locator-replay'/r['id'].split(':')[1]).relative_to(ROOT).as_posix()
    fresh=extract_evidence(doc,r['id'],ROOT,directory,dpi=144,pdftoppm=POP/'pdftoppm.EXE')
    for k in e:
        if k in ('text','image','crop_pdf'):
            assert fresh[k]['bytes']==e[k]['bytes'] and fresh[k]['sha256']==e[k]['sha256'],(r['key'],k)
        else:assert fresh[k]==e[k],(r['key'],k)
    assert e['page_basis_hash']==page_basis_hash(p) and e['region_revision']==r['revision'] and e['box']==r['box']
    native=box_to_pdf(r['box'],p);cr=PdfReader(ROOT/fresh['crop_pdf']['path'],strict=True).pages[0]
    assert [Fraction(str(v)) for v in cr.mediabox]==[Fraction(str(v)) for v in cr.cropbox]==native
    assert cr.rotation%360==p['rotation'] and Fraction(str(cr.get('/UserUnit',1)))==1
    predicted=render_size_pixels(r['box'],p,144)
    with Image.open(ROOT/fresh['image']['path']) as im:actual=im.size
    assert predicted==actual==(e['render_parameters']['width_pixels'],e['render_parameters']['height_pixels'])
    raw=(ROOT/fresh['text']['path']).read_bytes();text=raw.decode('utf-8')
    assert not raw.startswith(b'\xef\xbb\xbf') and '\r' not in text
    assert e['text_offsets']=={'unit':'unicode_codepoints','bounds':'half_open','start':0,'end':len(text)}
    a=[];cursor=0
    for line in text.splitlines(keepends=True):
        literal=line.rstrip('\n')
        if literal.endswith('-'):a.append({'kind':'line_end_hyphen','start':cursor+len(literal)-1,'end':cursor+len(literal),'literal':'-','line':literal})
        cursor+=len(line)
    for offset,char in enumerate(text):
        if char in ('\ufffd','\x00','\ufb01','\ufb02'):
            a.append({'kind':'literal_extraction_glyph','start':offset,'end':offset+1,'literal':char,'codepoint':f'U+{ord(char):04X}'})
    if not text:a.append({'kind':'empty_extraction','start':0,'end':0,'policy':'Graphic may validly have no extraction; no representation inferred.'})
    if a:anomalies.append({'region_id':r['id'],'revision':r['revision'],'key':r['key'],'text':e['text'],'unit':'unicode_codepoints','bounds':'half_open','observations':a})
    row={'index':i,'id':r['id'],'key':r['key'],'revision':r['revision'],'pdf_page':p['pdf_page'],'box':r['box'],'page_basis_hash':e['page_basis_hash'],'source_sha256':doc['source']['sha256'],'original_triple':{k:e[k] for k in ('text','image','crop_pdf')},'fresh_evidence':fresh,'native_bounds':[{'numerator':v.numerator,'denominator':v.denominator} for v in native],'crop_boxes_exact':True,'rotation_exact':True,'user_unit_normalized':True,'predicted_pixels':list(predicted),'actual_pixels':list(actual),'text_offsets':e['text_offsets'],'triple_bytes_exact':True,'started_utc':started,'ended_utc':utc(),'wall_seconds':time.monotonic()-clock,'method':'Unchanged extract_evidence for this exact new ID only; fresh reviewer output. Native crop bounds independently compared as exact rationals.'}
    write(f'locator-increments/{i:03}.json',row);rows.append(row)
    if i%10==0 or i in (39,72,111,141):print('LOCATOR',i,'/141',flush=True)
    if i in (39,72,111,141):checkpoint('locator-'+str(i),['Input/runtime/structure/preservation/denominator gates',f'{i} exact new locator replays'], 'Continue full locator/visual review; no source expansion.')
write('locator-audit.json',{'outcome':'passed','audited_locators':len(rows),'primary_files':3*len(rows),'regions':rows,'literal_anomalies':anomalies,'normalization':'None. Exact raw extraction UTF-8 bytes retained; anomalies are observations, not corrected transcription.','old_evidence':'Not regenerated; preserved byte/metadata audit in preservation-audit.json.'})
print('ALL LOCATORS EXACT',len(rows),flush=True)
