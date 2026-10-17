"""Fresh, serial rendering of assigned originals and exact boundary context only."""
import json
import subprocess
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
import pdfplumber
from wgc.sources.inventory import file_pin, page_basis_hash
from wgc.sources.geometry import box_to_pdf

ROOT = Path.cwd()
RUN = Path(__file__).parent.relative_to(ROOT).as_posix()
PINS = json.loads(Path('private/workflow/runs/IG-2B08/refine-8d84cd90-01/input-pins.json').read_text())
baseline = json.loads(Path(PINS['baseline_inventory']['path']).read_text())
reader = PdfReader(PINS['source']['pdf']['path'], strict=True)
entries = []

def render(number, box, name, scope):
    directory = Path(RUN)/'original-pages'/name
    directory.mkdir(parents=True, exist_ok=False)
    writer = PdfWriter()
    page = writer.add_page(reader.pages[number-1])
    x0,y0,x1,y1 = box
    page.mediabox = RectangleObject([x0,792-y1,x1,792-y0])
    page.cropbox = RectangleObject([x0,792-y1,x1,792-y0])
    with (directory/'original-crop.pdf').open('xb') as stream:
        writer.write(stream)
    subprocess.run(['pdftoppm','-singlefile','-cropbox','-r','144','-png',str(directory/'original-crop.pdf'),str(directory/'original')],check=True,capture_output=True)
    with pdfplumber.open(directory/'original-crop.pdf') as pdf:
        text=pdf.pages[0].crop(pdf.pages[0].bbox).extract_text(x_tolerance=3,y_tolerance=3) or ''
    (directory/'text.txt').write_text(text,encoding='utf-8',newline='\n')
    metadata=next(p for p in baseline['pages'] if p['pdf_page']==number)
    entries.append({'pdf_page':number,'page_id':metadata['id'],'page_basis_hash':page_basis_hash(metadata),'source_sha256':PINS['source']['sha256'],'top_left_points':box,'scope':scope,'artifacts':[file_pin(ROOT,(directory/n).as_posix()) for n in ['original-crop.pdf','original.png','text.txt']]})

for number in [29,30,31,32]:
    render(number,[0,0,612,792],f'page-{number}','Entire assigned original physical page')
context_id='region:720a5d03-c721-469b-8a5e-2b91cb653a02'
boundary_ids={link['from'] for link in baseline['links'] if link['to']==context_id and link['kind']=='continuation'}
assert len(boundary_ids)==1
boundary=next(r for r in baseline['regions'] if r['id'] in boundary_ids)
metadata=next(p for p in baseline['pages'] if p['id']==boundary['page_id'])
assert metadata['pdf_page']==28
native=box_to_pdf(boundary['box'],metadata)
render(28,[float(native[0]),792-float(native[3]),float(native[2]),792-float(native[1])],'page-28-boundary','Only linked bottom paragraph ending further; context denominator zero')
render(33,[45,50,298,127],'page-33-upper-edge','Only upper-left initial continuation to establish page-32/33 boundary; context denominator zero')
Path(RUN,'original-render-pins.json').write_text(json.dumps({'entries':entries},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'rendered_assigned_pages':[29,30,31,32],'bounded_context_pages':[28,33],'manifest':RUN+'/original-render-pins.json'}))
