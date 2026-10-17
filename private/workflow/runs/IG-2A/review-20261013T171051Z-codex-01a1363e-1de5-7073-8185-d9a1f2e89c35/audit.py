"""Independent acquisition, PDF geometry, replay and pixel checks. Pages 1-4 only for content."""
import copy, hashlib, json, logging, subprocess
from pathlib import Path
from fractions import Fraction
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject, NameObject, FloatObject
from reportlab.pdfgen.canvas import Canvas
from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import file_pin, seal, validate
from wgc.sources.pdf import structural_inventory, extract_evidence

OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[4];REL=OUT.relative_to(ROOT).as_posix()
SRC='private/ig/sources/spqr-5e-official/revision-20261013T155212Z'
INV=ROOT/'private/ig/projects/spqr/sources/inventory/ig2a-20261013T155212Z'
tc=json.loads((ROOT/'private/workflow/runs/IG-2A/attempt-20261013T155212Z/toolchain.json').read_text())
logging.basicConfig(filename=OUT/'pypdf-warnings.log',level=logging.WARNING)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,d): (OUT/n).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def cmd(name,args):
    p=subprocess.run(args,capture_output=True);(OUT/(name+'.stdout')).write_bytes(p.stdout);(OUT/(name+'.stderr')).write_bytes(p.stderr)
    assert p.returncode==0,(args,p.stderr)
    return {'argv':args,'exit_code':p.returncode}
prov=json.loads((ROOT/SRC/'provenance.json').read_text())
reader=PdfReader(ROOT/SRC/'rulebook.pdf',strict=True)
commands=[cmd('independent-pdfinfo',[tc['executables']['pdfinfo']['path'],str(ROOT/SRC/'rulebook.pdf')])]
assert len(reader.pages)==44 and '\nPages:           44' in (OUT/'independent-pdfinfo.stdout').read_text()
assert sha(ROOT/SRC/'rulebook.pdf')==prov['sha256']=='e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
assert (ROOT/SRC/'rulebook.pdf').stat().st_size==prov['bytes']==3965827
http=json.loads((ROOT/SRC/'rulebook-http.json').read_text());htmlhttp=json.loads((ROOT/SRC/'referring-page-http.json').read_text())
assert http==prov['http'] and int(http['headers']['Content-Length'])==prov['bytes']
html=(ROOT/SRC/'referring-page.html').read_text(encoding='utf-8')
assert sha(ROOT/SRC/'referring-page.html')==prov['referring_page_evidence']['sha256']==htmlhttp['sha256']
assert (ROOT/SRC/'referring-page.html').stat().st_size==htmlhttp['bytes']
assert 'SPQR+Deluxe_Rule+book_WEB.pdf' in html and '5th Edition Rulebook' in html
edition=(ROOT/SRC/'edition-page-001.txt').read_text(encoding='utf-8')
assert '5th Edition' in edition and '5th Edition' in reader.pages[0].extract_text()
assert sha(ROOT/SRC/'edition-page-001.txt')==prov['edition_evidence']['sha256']
registry=json.loads((INV/'seed/identity-registry.json').read_text())
one=structural_inventory(ROOT,SRC+'/rulebook.pdf',SRC+'/provenance.json',prov['source_id'],prov['sha256'],registry,pdfinfo=tc['executables']['pdfinfo']['path'])
two=structural_inventory(ROOT,SRC+'/rulebook.pdf',SRC+'/provenance.json',prov['source_id'],prov['sha256'],one['registry'],pdfinfo=tc['executables']['pdfinfo']['path'])
assert canonical_bytes(one)==canonical_bytes(two)
assert canonical_bytes(one)+b'\n'==(INV/'seed/inventory.json').read_bytes()
for name,d in [('replay-one',one),('replay-two',two)]:
    p=OUT/name;p.mkdir();(p/'inventory.json').write_bytes(canonical_bytes(d)+b'\n');(p/'registry.json').write_bytes(canonical_bytes(d['registry'])+b'\n')
doc=json.loads((INV/'verified-inventory.json').read_text());validate(doc,ROOT)
geom=[]
for index,p in enumerate(reader.pages):
    q=doc['pages'][index]
    expected_media=[int(Fraction(str(v))*1000000) for v in p.mediabox]
    expected_crop=[int(Fraction(str(v))*1000000) for v in p.cropbox]
    assert q['media_box']==expected_media and q['crop_box']==expected_crop and q['rotation']==p.rotation%360
    assert Fraction(q['user_unit']['numerator'],q['user_unit']['denominator'])==Fraction(str(p.get('/UserUnit',1)))
    geom.append({'pdf_page':index+1,'media_box':expected_media,'crop_box':expected_crop,'rotation':p.rotation%360,'user_unit':q['user_unit']})
render=OUT/'d';render.mkdir()
commands.append(cmd('real-direct-render',[tc['executables']['pdftoppm']['path'],'-f','1','-l','4','-cropbox','-r','144','-png',str(ROOT/SRC/'rulebook.pdf'),str(render/'page')]))
comparisons=[]
for number in range(1,5):
    ev=next(e for e in doc['evidence'] if e['pdf_page']==number)
    direct=render/f'page-{number:02d}.png'
    with Image.open(direct) as a,Image.open(ROOT/ev['image']['path']) as b:
        assert a.size==b.size and a.convert('RGB').tobytes()==b.convert('RGB').tobytes()
        comparisons.append({'pdf_page':number,'size':a.size,'pixels_identical':True,'direct_sha256':sha(direct),'delivery_png_sha256':ev['image']['sha256']})
    crop=PdfReader(ROOT/ev['crop_pdf']['path'],strict=True)
    assert len(crop.pages)==1 and [float(v) for v in crop.pages[0].cropbox]==[float(v) for v in reader.pages[number-1].cropbox]
save('source-audit.json',{'source_sha256':prov['sha256'],'bytes':prov['bytes'],'counts':{'pypdf':44,'poppler':44},'edition':'5th Edition','local_http_evidence_consistent':True,'acquisition_utc':http['acquired_utc'],'referring_page_link_verified':True,'no_redownload':True,'geometry':geom,'replay_identical_to_frozen_seed':True,'render_comparisons':comparisons,'commands':commands,'source_content_pages':[1,2,3,4],'semantic_acceptance_granted':False,'provenance_limit':'Saved HTTP capture is locally internally consistent; no network authentication or prior-source history access performed.'})

g=OUT/'g';g.mkdir();c=Canvas(str(g/'base.pdf'),pagesize=(300,400),invariant=1)
c.setFillColorRGB(1,0,0);c.rect(30,200,70,115,stroke=0,fill=1)
c.setFillColorRGB(0,0,0);c.drawString(40,250,'INSIDE');c.drawString(170,100,'OUTSIDE');c.showPage();c.save()
(g/'provenance.json').write_text('{"synthetic":true}\n')
geometry_results=[]
for rotation in (0,90,180,270):
    w=PdfWriter();p=w.add_page(PdfReader(g/'base.pdf').pages[0])
    p.mediabox=RectangleObject([10,10,300,400]);p.cropbox=RectangleObject([20,30,220,330]);p.rotation=rotation
    p[NameObject('/UserUnit')]=FloatObject(1.5)
    path=g/f'r{rotation}.pdf'
    with path.open('xb') as f:w.write(f)
    rel=path.relative_to(ROOT).as_posix()
    d=structural_inventory(ROOT,rel,REL+'/g/provenance.json','source:geometry',sha(path),pdfinfo=tc['executables']['pdfinfo']['path'])
    d['regions'][0]['box']=[0,0,500000,500000];d['regions'][0]=seal(d['regions'][0]);d=seal(d)
    ev=extract_evidence(d,d['regions'][0]['id'],ROOT,REL+f'/g/e{rotation}',dpi=72,pdftoppm=tc['executables']['pdftoppm']['path'])
    with Image.open(ROOT/ev['image']['path']) as im:
        size=im.size
        mask=im.convert('RGB').point(lambda v:v) # Construct a color mask independent of implementation geometry.
        pixels=mask.load();red=[]
        for y in range(size[1]):
            for x in range(size[0]):
                r,green,b=pixels[x,y]
                if r>200 and green<30 and b<30:red.append((x,y))
        actual=[min(x for x,y in red),min(y for x,y in red),max(x for x,y in red)+1,max(y for x,y in red)+1]
    expected_size=(150,225) if rotation in (0,180) else (225,150)
    expected={0:[15,22.5,120,195],90:[30,15,202.5,120],180:[30,30,135,202.5],270:[22.5,30,195,135]}[rotation]
    assert size==expected_size and all(abs(a-b)<=1 for a,b in zip(actual,expected)),(rotation,size,actual,expected)
    text=(ROOT/ev['text']['path']).read_text()
    assert 'OUTSIDE' not in text
    geometry_results.append({'rotation':rotation,'userunit':'3/2','native_crop':[20,180,120,330],'size':size,'expected_size':expected_size,'red_bbox':actual,'expected_red_bbox':expected,'outside_text_absent':True,'inside_text':text,'evidence':ev})
save('geometry-oracle.json',{'cases':geometry_results,'all_passed':True})
print('Source audit: 44 pages, 3965827 bytes, fresh replay exact, all four real PNGs match original; four asymmetric crop/rotation/UserUnit pixel oracles passed.')
