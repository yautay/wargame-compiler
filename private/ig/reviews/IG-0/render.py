from pathlib import Path
import json,pypdfium2 as pdf
r=Path('private/ig/reviews/IG-0'); (r/'renders').mkdir(exist_ok=True)
sources={e['id']:e['path'] for e in json.loads((r/'sources-manifest.json').read_text())}
for k,n in [('spqr',13),('spqr',26),('tlnb',9),('nab',3),('lastdays',10),('gcacw',12),('gcacw-tables',1)]:
 d=pdf.PdfDocument(sources[k]); d[n-1].render(scale=1.5).to_pil().save(r/'renders'/f'{k}-p{n}.png')
print('Rendered 7 pages using pypdfium2 fallback')
