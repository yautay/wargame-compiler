"""Read-only PDF locator check for the 105 response quotes, no rule extraction."""
import hashlib
import json
import re
import sys
from pathlib import Path
import pdfplumber

sys.stdout.reconfigure(encoding='utf-8')
p=Path('private/poc/spqr-chapter9')
response=json.loads((p/'runs/first-001/first-001.json').read_bytes())
path=p/'source/original-pdf-20261008-01.pdf'
assert hashlib.sha256(path.read_bytes()).hexdigest()==response['scope']['source_sha256']
def norm(s, remove_splits):
    s=re.sub(r'[-\u00ad]\s*\n\s*(?=[A-Za-z])','' if remove_splits else '-',s)
    return re.sub(r'\s+',' ',s).strip()
results=[]
with pdfplumber.open(path) as pdf:
    for n,e in enumerate(response['evidence']):
        page=pdf.pages[e['pdf_page']-1]
        b=e['image']['bbox']
        box=[b[0]*page.width/1700,b[1]*page.height/2200,b[2]*page.width/1700,b[3]*page.height/2200]
        # within_bbox uses whole glyphs contained by the box, rather than clipped
        # glyphs from crop. No tolerance expansion or undocumented locator repair.
        inside=page.within_bbox(box).extract_text(x_tolerance=2,y_tolerance=3) or ''
        overlapping=page.crop(box).extract_text(x_tolerance=2,y_tolerance=3) or ''
        q=e['quote']['value'] if e['quote']['state']=='known' else None
        matched=isinstance(q,str) and any(norm(q,a) in norm(inside,b) for a in [False,True] for b in [False,True])
        overlap_match=isinstance(q,str) and any(norm(q,a) in norm(overlapping,b) for a in [False,True] for b in [False,True])
        results.append({'evidence_id':e['id'],'response_pointer':f'/evidence/{n}/image',
                        'bbox_pdf_points':box,'contained_glyph_text':inside,
                        'overlapping_glyph_text':overlapping,
                        'quote_status':'contained_glyph_match' if matched else 'needs_visual_review',
                        'overlap_quote_status':'overlapping_glyph_match' if overlap_match else 'needs_visual_review',
                        'normalization':'whitespace joining; either retain or remove end-of-line hyphen; case/punctuation/numbers unchanged',
                        'visual_content_status':'not_assessable'})
out={'source_path':str(path),'source_sha256':response['scope']['source_sha256'],
     'pdfplumber_version':pdfplumber.__version__,'method':'full-page pixels converted using actual PDF dimensions; whole contained glyphs only',
     'denominator':len(results),'contained_quote_matches':sum(x['quote_status']=='contained_glyph_match' for x in results),'overlapping_quote_matches':sum(x['overlap_quote_status']=='overlapping_glyph_match' for x in results),'results':results,
     'limitations':'Glyph matching verifies quote location; it does not establish all transcribed content, numeric graphic values, interpreted meaning or human acceptance.'}
(p/'measurement/M-POC3-first-001/bbox-analysis.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Contained quote matches',out['contained_quote_matches'],'/',len(results))
print('Overlapping quote matches',out['overlapping_quote_matches'],'/',len(results))
for x in results:
    if x['overlap_quote_status']!='overlapping_glyph_match':print(json.dumps(x,ensure_ascii=False))
