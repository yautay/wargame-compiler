from support import *
import copy, math
from pypdf import PdfReader,PdfWriter
from pypdf.generic import RectangleObject,NameObject,FloatObject
from wgc.sources.pdf import structural_inventory,extract_evidence
from wgc.sources.inventory import seal,validate
from PIL import Image
out=RUN/'integer-boundary';out.mkdir()
writer=PdfWriter();p=writer.add_page(PdfReader(RUN/'s/original.pdf').pages[0])
p.cropbox=RectangleObject([13.25,27.5,213.25,327.5]);p[NameObject('/UserUnit')]=FloatObject('1.1')
pdf=out/'source.pdf'
with pdf.open('xb') as f:writer.write(f)
relative=pdf.relative_to(ROOT).as_posix();prov=(RUN/'s/provenance.json').relative_to(ROOT).as_posix()
base=structural_inventory(ROOT,relative,prov,'source:integer-boundary',digest(pdf));rows=[]
for x0,x1 in [(200000,500000),(100000,400000),(0,300000),(400000,700000)]:
    for dpi in [72,144]:
        d=copy.deepcopy(base);d['regions'][0]['box']=[x0,100000,x1,800000];d['regions'][0]=seal(d['regions'][0]);d=seal(d)
        ev=extract_evidence(d,d['regions'][0]['id'],ROOT,(out/f'x{x0}-d{dpi}').relative_to(ROOT).as_posix(),dpi=dpi)
        d['evidence']=[ev];d=seal(d);candidate=write(f'integer-boundary/x{x0}-d{dpi}.json',d)
        start,t=utc(),time.monotonic()
        try:report=validate(d,ROOT);error=None
        except Exception as exc:report=None;error=type(exc).__name__+': '+str(exc)
        width,height=Image.open(ROOT/ev['image']['path']).size
        rows.append({'x0_millionths':x0,'x1_millionths':x1,'dpi':dpi,'independent_exact_physical_dimensions_points':[66,231],'exact_mathematical_pixels':[66*dpi//72,231*dpi//72],'actual_pixels':[width,height],'validator_error':error,'candidate':pin(candidate),'started_utc':start,'ended_utc':utc(),'wall_seconds':time.monotonic()-t})
write('independent-integer-pixel-boundaries.json',{'basis':'Author CropBox native width 200, height 300; normalized span 0.3 by 0.7; UserUnit 1.1; exact physical dimensions 66 by 231 points. Potential floating subtraction at nonzero-origin Poppler ceiling boundary independently explored.','results':rows})
print(json.dumps(rows,indent=2))
