"""Source/quote and glyph locator checks for new context evidence only."""
from pathlib import Path
import json,hashlib,re
import pdfplumber
from PIL import Image
P=Path('private/poc/spqr-chapter9');M=P/'measurement/M-POC4B-context-01'
T=P/'transfer/context-v1';d=json.loads((P/'runs/context-01/response.raw.txt').read_bytes())
base=json.loads((P/'runs/first-001/first-001.json').read_bytes())
old={e['id']:e for e in base['evidence']}
scope=json.loads((T/'context/pass-01/evidence/8.46-step-4-scope.json').read_bytes())
render=Path(scope['full_render']['path'])
assert hashlib.sha256(render.read_bytes()).hexdigest()==scope['full_render']['sha256']
w,h=Image.open(render).size;offset=scope['pixel_bbox_on_reviewer_render'][:2]
src=P/'source/original-pdf-20261008-01.pdf'
assert hashlib.sha256(src.read_bytes()).hexdigest()==d['scope']['source_sha256']
def norm(s):
    s=re.sub(r'[-\u00ad]\s*\n\s*(?=[A-Za-z])','',s)
    return re.sub(r'\s+',' ',s).strip()
results=[]
with pdfplumber.open(src) as pdf:
    page=pdf.pages[26]
    for n,e in enumerate(d['evidence']):
        if e['id'] in old:
            assert old[e['id']]==e
            continue
        im=e['image'];b=im['bbox']
        box=[(b[0]+offset[0])*612/w,(b[1]+offset[1])*792/h,
             (b[2]+offset[0])*612/w,(b[3]+offset[1])*792/h]
        inside=page.within_bbox(box).extract_text(x_tolerance=2,y_tolerance=3) or ''
        overlap=page.crop(box).extract_text(x_tolerance=2,y_tolerance=3) or ''
        q=e['quote']['value']
        results.append(dict(id=e['id'],response_pointer=f'/evidence/{n}',
            crop_bbox=b,source_pdf_bbox=box,contained_glyph_text=inside,overlapping_glyph_text=overlap,
            contained_quote_match=norm(q) in norm(inside),overlap_quote_match=norm(q) in norm(overlap),
            normalization='Whitespace joining and source line-split removal; no punctuation/numeric changes',
            source_scope='Exact supplied crop only; no semantic acceptance'))
out=dict(source_sha256=d['scope']['source_sha256'],new_evidence=len(results),
    inherited_evidence_byte_equal=105,coordinate_mapping='Crop-local pixels -> actual reviewer render pixel offset -> PDF points; offset and size from hash-verified source-scope metadata',
    contained_matches=sum(x['contained_quote_match'] for x in results),
    overlapping_matches=sum(x['overlap_quote_match'] for x in results),results=results,
    semantic_acceptance='not_performed')
path=M/'new-evidence-analysis.json';assert not path.exists();path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(new=out['new_evidence'],contained=out['contained_matches'],overlap=out['overlapping_matches']),indent=2))
for x in results:
    if not x['contained_quote_match']:print(json.dumps(x,ensure_ascii=False))
