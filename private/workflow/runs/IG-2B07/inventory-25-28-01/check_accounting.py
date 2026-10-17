"""Independent assigned-page glyph accounting plus complete preservation assertions."""
import hashlib
import json
from pathlib import Path
import pdfplumber
from wgc.sources.inventory import file_pin

ROOT=Path.cwd()
A=Path(__file__).parent.relative_to(ROOT)
doc=json.loads((A/'final-verified/inventory.json').read_text())
claim=json.loads((A/'claim.json').read_text())
meta={k:claim[k] for k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256')}
results=[]
for number in (25,26,27,28):
    page=next(p for p in doc['pages'] if p['pdf_page']==number)
    regions=[r for r in doc['regions'] if r['page_id']==page['id'] and r['denominator_role']=='inventory']
    source=A/'originals'/f'page-{number}.pdf'
    missing=[]
    observed=0
    with pdfplumber.open(source) as pdf:
        for glyph in pdf.pages[0].chars:
            if not glyph['text'].strip():
                continue
            observed+=1
            x=(glyph['x0']+glyph['x1'])*1000000/(2*612)
            y=(glyph['top']+glyph['bottom'])*1000000/(2*792)
            if not any(r['box'][0]<=x<r['box'][2] and r['box'][1]<=y<r['box'][3] for r in regions):
                missing.append({'glyph':glyph['text'],'box_points':[glyph[k] for k in ('x0','top','x1','bottom')]})
    results.append({'physical_page':number,'visible_text_glyph_count':observed,'unassigned_glyph_count':len(missing),'unassigned_glyphs':missing,'original_page_pdf':file_pin(ROOT,source.as_posix())})
report={**meta,'command':'.venv/Scripts/python.exe '+(A/'check_accounting.py').as_posix(),
        'inventory':file_pin(ROOT,(A/'final-verified/inventory.json').as_posix()),'pages':results,
        'method':'Independently extract nonwhitespace source glyph centers from each exact assigned original-page PDF and require each center inside an inventory region. Raster diagrams require separate visual component accounting. This does not certify transcription or semantic completeness.',
        'all_passed':all(r['unassigned_glyph_count']==0 for r in results)}
(A/'glyph-accounting-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'all_passed':report['all_passed'],'pages':[{k:r[k] for k in ('physical_page','visible_text_glyph_count','unassigned_glyph_count')} for r in results]}))
assert report['all_passed'],'Assigned source glyphs lie outside the inventory regions; inspect exact missing boxes.'
