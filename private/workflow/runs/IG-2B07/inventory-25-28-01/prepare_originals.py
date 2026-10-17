"""Fresh serial renders of the exact assigned source scope; no other content."""
import hashlib
import json
import subprocess
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

ROOT = Path.cwd()
ATTEMPT = Path(__file__).parent.relative_to(ROOT)
SESSION = Path('private/workflow/orchestrator/20261016T195516Z-332903f5/002-IG-2B07-executor-78a83e6c')
task = json.loads((SESSION / 'task.json').read_text())
scope = task['source_scope']
pdf = Path(scope['source_pdf']['path'])
assert hashlib.sha256(pdf.read_bytes()).hexdigest() == scope['source_pdf']['sha256']
reader = PdfReader(pdf, strict=True)
directory = ATTEMPT / 'originals'
directory.mkdir(exist_ok=False)
pins = []
for number, box in [(25,[0,0,1000000,1000000]),(26,[0,0,1000000,1000000]),(27,[0,0,1000000,1000000]),(28,[0,0,1000000,1000000]),(24,scope['context_only_boxes']['24']),(29,scope['context_only_boxes']['29'])]:
    writer = PdfWriter()
    page = writer.add_page(reader.pages[number-1])
    x0,y0,x1,y1 = box
    bounds = [612*x0/1000000,792*(1-y1/1000000),612*x1/1000000,792*(1-y0/1000000)]
    page.mediabox = RectangleObject(bounds)
    page.cropbox = RectangleObject(bounds)
    prefix = directory / f'page-{number}'
    with prefix.with_suffix('.pdf').open('xb') as stream:
        writer.write(stream)
    subprocess.run(['pdftoppm','-f','1','-l','1','-singlefile','-cropbox','-r','144','-png',str(prefix.with_suffix('.pdf')),str(prefix)],check=True,capture_output=True)
    for suffix in ('.pdf','.png'):
        path = prefix.with_suffix(suffix)
        pins.append({'path':path.as_posix(),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'physical_page':number,'box':box,'source_sha256':scope['source_pdf']['sha256']})
(directory/'pins.json').write_text(json.dumps(pins,indent=2)+'\n')
assert hashlib.sha256(pdf.read_bytes()).hexdigest() == scope['source_pdf']['sha256']
print('Rendered four assigned original pages and two exact boundary strips serially.')
