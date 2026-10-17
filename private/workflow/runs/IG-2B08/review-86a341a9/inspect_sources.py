"""Fresh, serial, task-scoped original source inspection aids."""
import hashlib
import json
import pathlib
import subprocess

from PIL import Image, ImageDraw
import pdfplumber

ROOT = pathlib.Path(__file__).resolve().parent
PRODUCT = pathlib.Path('private/workflow/runs/IG-2B08/repair-F01-manifest02')
SOURCE = pathlib.Path('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf')
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
out = ROOT / 'originals'
out.mkdir(exist_ok=False)
rows = json.loads((PRODUCT / 'region-ledger.json').read_text(encoding='utf-8'))['new_observations']
for page in [29, 30, 31, 32]:
    prefix = out / f'page-{page}'
    result = subprocess.run(['pdftoppm', '-f', str(page), '-l', str(page), '-singlefile', '-r', '144', '-png', str(SOURCE), str(prefix)], capture_output=True)
    (out / f'page-{page}-render.log').write_bytes(result.stdout + result.stderr)
    assert result.returncode == 0
    original = Image.open(prefix.with_suffix('.png')).convert('RGB')
    assert original.size == (1224, 1584)
    for role in ['inventory', 'detail']:
        selected = [r for r in rows if r['page'] == page and r['role'] == role]
        overlay = original.copy()
        draw = ImageDraw.Draw(overlay)
        for i, row in enumerate(rows):
            if row not in selected:
                continue
            box = [int(x * 2) for x in row['points']]
            draw.rectangle(box, outline='red', width=1)
            draw.text((box[0]+1, box[1]+1), str(i), fill='red', stroke_width=1, stroke_fill='white')
        overlay.save(out / f'page-{page}-{role}.png')
    # Two columns, three vertical panels, original pixels at native scale.
    for y in range(3):
        for x in range(2):
            original.crop((x*612,y*528,(x+1)*612,(y+1)*528)).save(out / f'page-{page}-panel-{y*2+x+1}.png')

result = subprocess.run(['pdftoppm', '-f', '33', '-l', '33', '-singlefile', '-r', '144', '-x', '90', '-y', '100', '-W', '522', '-H', '60', '-png', str(SOURCE), str(out / 'page-33-continuation')], capture_output=True)
(out / 'page-33-render.log').write_bytes(result.stdout + result.stderr)
assert result.returncode == 0
with pdfplumber.open(SOURCE) as pdf:
    # Crop the original page before text extraction; never extract the page-33 stream.
    text = pdf.pages[32].crop((45,50,306,80), strict=True).extract_text() or ''
(out / 'page-33-continuation.txt').write_text(text, encoding='utf-8')

# Render every authored detail crop into serial sheets, labelled with ledger index.
details = [(i,r) for i,r in enumerate(rows) if r['role']=='detail']
for start in range(0, len(details), 12):
    sheet=Image.new('RGB',(1200,1000),'#dddddd'); draw=ImageDraw.Draw(sheet)
    for cell,(i,r) in enumerate(details[start:start+12]):
        im=Image.open(r['evidence']['image']['path']).convert('RGB')
        im.thumbnail((390,205))
        x=(cell%3)*400; y=(cell//3)*250
        draw.text((x+5,y+3),f"{i} p{r['page']} {r['key'].split(':')[-1]}",fill='black')
        sheet.paste(im,(x+5,y+35))
    sheet.save(out/f'details-{start//12+1:02d}.png')

def pin(p):
    return {'path':p.relative_to(pathlib.Path.cwd()).as_posix(), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
artifacts=[pin(p) for p in sorted(out.iterdir()) if p.is_file()]
(ROOT/'fresh-source-artifacts.json').write_text(json.dumps({'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'artifacts':artifacts,'scope':{'assigned':[29,30,31,32],'context33':[45,50,306,80],'page28':'reference only'},'serial':True},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'pages_rendered':[29,30,31,32],'context33_dimensions':Image.open(out/'page-33-continuation.png').size,'details':len(details),'sheets':(len(details)+11)//12}))
