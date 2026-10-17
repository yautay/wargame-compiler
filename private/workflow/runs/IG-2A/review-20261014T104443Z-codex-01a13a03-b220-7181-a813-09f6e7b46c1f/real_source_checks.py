from support import *
from pypdf import PdfReader
from fractions import Fraction
from PIL import Image, ImageChops, ImageOps, ImageDraw
from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import validate
PDF='private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'
PROVENANCE='private/ig/sources/spqr-5e-official/revision-20261013T155212Z/provenance.json'
SHA='e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
REGISTRY='private/ig/projects/spqr/sources/inventory/ig2a-20261013T155212Z/seed/identity-registry.json'
rel=RUN.relative_to(ROOT).as_posix()
assert digest(ROOT/PDF)==SHA
checks=[]
checks.append(command('official-pdfinfo',[POPPLER/'pdfinfo.exe',ROOT/PDF]))
reader=PdfReader(ROOT/PDF,strict=True)
geometry=[]
for number,p in enumerate(reader.pages,1):
    geometry.append({'pdf_page':number,'media_box':[str(v) for v in p.mediabox],'crop_box':[str(v) for v in p.cropbox],'rotation':p.rotation%360,'user_unit':str(p.get('/UserUnit',1))})
assert len(reader.pages)==44
write('official-independent-structure.json',{'source':pin(ROOT/PDF),'pypdf_count':len(reader.pages),'poppler_count':44,'poppler_count_basis':'official-pdfinfo.stdout independently read Pages line','geometry':geometry,'content_inspection_pages':[1,2,3,4]})
for suffix in ['one','two']:
    registry=REGISTRY if suffix=='one' else rel+'/inventory-one/identity-registry.json'
    checks.append(command('official-inventory-'+suffix,[PYTHON,'-m','wgc.sources','inventory','--pdf',PDF,'--provenance',PROVENANCE,'--source-id','source:spqr:5e:core','--sha256',SHA,'--registry',registry,'--output',rel+'/inventory-'+suffix]))
    assert checks[-1]['exit_code']==0
one,two=read(RUN/'inventory-one/inventory.json'),read(RUN/'inventory-two/inventory.json')
assert canonical_bytes(one)==canonical_bytes(two)
assert (RUN/'inventory-one/inventory.json').read_bytes()==(RUN/'inventory-two/inventory.json').read_bytes()
assert one['registry']==read(ROOT/REGISTRY)
assert {(p['id'],p['pdf_page']) for p in one['pages']}=={(p['id'],p['pdf_page']) for p in two['pages']}
assert {(r['id'],r['key']) for r in one['regions']}=={(r['id'],r['key']) for r in two['regions']}
for row,p in zip(geometry,one['pages']):
    assert p['media_box']==[int(Fraction(v)*1000000) for v in row['media_box']]
    assert p['crop_box']==[int(Fraction(v)*1000000) for v in row['crop_box']]
    assert p['rotation']==row['rotation']
report=validate(one,ROOT)
assert report['denominator_regions']==44 and all(v['unprocessed']==44 and v['represented']==0 for v in report['levels'].values())
write('repeatability.json',{'canonical_bytes_identical':True,'serialized_bytes_identical':True,'persisted_registry_identical':True,'page_and_region_identity_identical':True,'all_44_placeholders_unprocessed':True,'represented_all_levels':0,'inventories':[pin(RUN/'inventory-one/inventory.json'),pin(RUN/'inventory-two/inventory.json')],'source_geometry_matches_independent_pypdf':True})
checks.append(command('official-evidence',[PYTHON,'-m','wgc.sources','evidence','--inventory',rel+'/inventory-one/inventory.json','--pages','1','2','3','4','--output',rel+'/real-evidence','--dpi','144']))
assert checks[-1]['exit_code']==0
(RUN/'direct').mkdir()
checks.append(command('official-original-render',[POPPLER/'pdftoppm.exe','-f','1','-l','4','-cropbox','-r','144','-png',ROOT/PDF,RUN/'direct/page']))
assert checks[-1]['exit_code']==0
document=read(RUN/'real-evidence/inventory.json');compare=[]
sheet=Image.new('RGB',(1700,1160),'#dddddd');draw=ImageDraw.Draw(sheet)
for n in [1,2,3,4]:
    ev=next(e for e in document['evidence'] if e['pdf_page']==n)
    original=RUN/f'direct/page-{n:02}.png';derived=ROOT/ev['image']['path']
    with Image.open(original) as a,Image.open(derived) as b:
        assert a.size==b.size and ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox() is None
        compare.append({'pdf_page':n,'original':pin(original),'derived':pin(derived),'pixel_identical':True,'dimensions':a.size})
        thumb=ImageOps.contain(a,(405,1090));x=(n-1)*425+10;sheet.paste(thumb,(x,35));draw.text((x,12),'Physical page '+str(n),fill='black')
sheet.save(RUN/'real-pages-contact.png')
write('real-render-comparison.json',compare);write('real-required-checks.json',checks)
assert digest(ROOT/PDF)==SHA
print('44 pages; two identical replays; four original/derived renders pixel-identical')
