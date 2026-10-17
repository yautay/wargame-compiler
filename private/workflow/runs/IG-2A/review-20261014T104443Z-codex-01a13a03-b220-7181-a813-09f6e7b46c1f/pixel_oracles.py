from support import *
from reportlab.pdfgen.canvas import Canvas
from pypdf import PdfReader, PdfWriter
from PIL import Image, ImageChops
output=RUN/'pixel-oracle';output.mkdir()
# An independently drawn, zero-origin physical PDF, already 180.45 x 338.34375
# points, provides the crop oracle. No WGC conversion or pypdf scaling is used.
reference=output/'physical-reference.pdf'
c=Canvas(str(reference),pagesize=(180.45,338.34375),invariant=1,pageCompression=0)
c.scale(1.5,1.5);c.translate(-53.35,-72.6125)
for color,box in [((0.1,0.2,0.8),(70,290,22,25)),((0.8,0.1,0.2),(165,245,25,22)),((0.1,0.7,0.2),(88,100,25,22)),((0.7,0.2,0.8),(177,122,22,25))]:
    c.setFillColorRGB(*color);c.rect(*box,fill=1,stroke=0)
c.setFillColorRGB(0,0,0);c.drawString(65,335,'Synthetic page 1');c.showPage();c.save()
rows=[]
for rotation in [0,90,180,270]:
    writer=PdfWriter();p=writer.add_page(PdfReader(reference).pages[0]);p.rotation=rotation
    pdf=output/f'reference-r{rotation}.pdf'
    with pdf.open('xb') as f:writer.write(f)
    for dpi in [72,144]:
        stem=output/f'r{rotation}-d{dpi}'
        check=command(f'oracle-render-r{rotation}-d{dpi}',[POPPLER/'pdftoppm.exe','-singlefile','-cropbox','-r',str(dpi),'-png',pdf,stem])
        original=stem.with_suffix('.png');candidate=RUN/f's/r{rotation}-d{dpi}/image.png'
        with Image.open(original) as a,Image.open(candidate) as b:
            diff=ImageChops.difference(a.convert('RGB'),b.convert('RGB'))
            extrema=diff.getextrema();max_error=max(v[1] for v in extrema)
            # Persist full difference image even for an exact match.
            diff.save(output/f'difference-r{rotation}-d{dpi}.png')
            row={'rotation':rotation,'dpi':dpi,'reference':pin(original),'derived':pin(candidate),'same_dimensions':a.size==b.size,'max_channel_error':max_error,'pixel_identical':diff.getbbox() is None,'check':check,'expectation_met':a.size==b.size and max_error==0}
            rows.append(row)
write('independent-pixel-oracles.json',{'basis':'Independently redraw known synthetic objects in a zero-origin physical page, Canvas transforms explicit source coordinates. WGC box/size/scaling functions not used in oracle. Exact full-image comparison, zero tolerance.','results':rows})
assert all(x['expectation_met'] for x in rows)
