"""Bounded original-page character geometry and explicit complement rectangles."""
from pathlib import Path
import pdfplumber
from build import OUT, COMMON, load, write

doc=load(OUT/'authored/inventory.json')
pages=[]
with pdfplumber.open(doc['source']['pdf']['path']) as pdf:
    for n in (9,10,11,12):
        page=next(p for p in doc['pages'] if p['pdf_page']==n)
        regions=[r for r in doc['regions'] if r['page_id']==page['id'] and r['denominator_role']=='inventory']
        # Rational comparison at original PDF points; no text from other pages.
        chars=pdf.pages[n-1].chars
        missing=[];edge=[]
        for ch in chars:
            if not ch['text'].strip(): continue
            x0,x1=ch['x0']/612*1000000,ch['x1']/612*1000000
            y0,y1=ch['top']/792*1000000,ch['bottom']/792*1000000
            enclosing=[r['id'] for r in regions if r['box'][0]<=x0 and x1<=r['box'][2] and r['box'][1]<=y0 and y1<=r['box'][3]]
            centered=[r['id'] for r in regions if r['box'][0]<=(x0+x1)/2<r['box'][2] and r['box'][1]<=(y0+y1)/2<r['box'][3]]
            if not enclosing:
                record={'glyph':ch['text'],'box_millionths_outward':[int(x0//1),int(y0//1),int(-(-x1//1)),int(-(-y1//1))],'center_region_ids':centered}
                (edge if centered else missing).append(record)
        # Disjoint full complement of authored boxes, retained as geometric gaps.
        xs=sorted({0,1000000,*[r['box'][0] for r in regions],*[r['box'][2] for r in regions]})
        gaps=[]
        for x0,x1 in zip(xs,xs[1:]):
            spans=sorted((r['box'][1],r['box'][3]) for r in regions if r['box'][0]<=x0 and x1<=r['box'][2])
            cursor=0
            for y0,y1 in spans:
                if cursor<y0:gaps.append([x0,cursor,x1,y0])
                cursor=max(cursor,y1)
            if cursor<1000000:gaps.append([x0,cursor,x1,1000000])
        pages.append({'pdf_page':n,'page_id':page['id'],'nonspace_character_count':sum(bool(c['text'].strip()) for c in chars),'characters_outside_all_region_centers':missing,'characters_with_center_inside_but_font_box_crossing_boundary':edge,'geometric_gap_rectangles':gaps,'unaccounted_area_trillionths':sum((b[2]-b[0])*(b[3]-b[1]) for b in gaps),'gap_reason':'Unassigned margins, gutter, inter-region spacing and remaining page area. Explicit geometry gaps are not represented or excluded content. Character bounds are a mechanical cross-check, not proof of visual/substantive completeness.'})
write(OUT/'text-geometry-audit.json',{**COMMON,'assigned_pages':[9,10,11,12],'method':'Original assigned pdfplumber character boxes compared against integer millionth author boxes; full disjoint rectangle complement calculated independently. No other page content extracted.','pages':pages})
print([(p['pdf_page'],len(p['characters_outside_all_region_centers']),len(p['characters_with_center_inside_but_font_box_crossing_boundary'])) for p in pages])
