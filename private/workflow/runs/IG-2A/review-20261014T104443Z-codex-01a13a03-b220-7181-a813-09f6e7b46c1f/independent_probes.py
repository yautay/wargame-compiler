from support import *
import copy, math
from fractions import Fraction
from reportlab.pdfgen.canvas import Canvas
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, FloatObject, RectangleObject
from PIL import Image
from wgc.sources import inventory as inv
from wgc.sources.pdf import structural_inventory, extract_evidence
from wgc.contracts.source import canonical_bytes

RESULTS=[]
START=utc()
def rel(path): return Path(path).relative_to(ROOT).as_posix()
def reseal(doc):
    doc['pages']=[inv.seal(p) for p in doc['pages']]
    doc['regions']=[inv.seal(r) for r in doc['regions']]
    return inv.seal(doc)
def probe(name,doc,expected='reject',diagnostic=None,root=True):
    doc=reseal(copy.deepcopy(doc)); path=write('cases/'+name+'.json',doc)
    started,t=utc(),time.monotonic()
    try: report=inv.validate(doc,ROOT if root else None); actual='accept'; error=None
    except Exception as exc: report=None; actual='reject'; error=type(exc).__name__+': '+str(exc)
    ok=actual==expected and (diagnostic is None or error is not None and diagnostic in error)
    result={'name':name,'candidate':pin(path),'root_check':root,'expected':expected,'actual':actual,'required_diagnostic':diagnostic,'error':error,'expectation_met':ok,'report':report,'started_utc':started,'ended_utc':utc(),'wall_seconds':time.monotonic()-t}
    RESULTS.append(result);write('probe-results.json',{'started_utc':START,'results':RESULTS})
    print(name,actual,error or '',ok,flush=True)
    return report

# Separate fresh two-page synthetic source. Coordinates and page count are authored
# here; no fixture helpers or implementation coordinate conversions define oracles.
S=RUN/'s';S.mkdir(); original=S/'original.pdf'
c=Canvas(str(original),pagesize=(330,490),invariant=1,pageCompression=0)
for number in [1,2]:
    c.setFillColorRGB(0.1,0.2,0.8); c.rect(70,290,22,25,fill=1,stroke=0)
    c.setFillColorRGB(0.8,0.1,0.2); c.rect(165,245,25,22,fill=1,stroke=0)
    c.setFillColorRGB(0.1,0.7,0.2); c.rect(88,100,25,22,fill=1,stroke=0)
    c.setFillColorRGB(0.7,0.2,0.8); c.rect(177,122,22,25,fill=1,stroke=0)
    c.setFillColorRGB(0,0,0);c.drawString(65,335,'Synthetic page '+str(number));c.showPage()
c.save()
reader=PdfReader(original);writer=PdfWriter()
for p in reader.pages:
    p.mediabox=RectangleObject([-17.25,-31.5,330,490]);p.cropbox=RectangleObject([13.25,27.5,213.75,328.25]);p[NameObject('/UserUnit')]=FloatObject('1.5');writer.add_page(p)
pdf=S/'source.pdf'
with pdf.open('xb') as f:writer.write(f)
provenance=write('s/provenance.json',{'synthetic':True,'page_count':2,'publisher_content':False})
baseline=structural_inventory(ROOT,rel(pdf),rel(provenance),'source:independent-review',digest(pdf))
probe('structural_baseline',baseline,'accept')
baseline['evidence']=[extract_evidence(baseline,r['id'],ROOT,rel(S/f'evidence-{i}'),dpi=144) for i,r in enumerate(baseline['regions'])]
baseline=reseal(baseline);probe('fresh_evidence_baseline',baseline,'accept')

for change in ['crop','effective_crop','rotation','user_unit','media','address']:
    d=copy.deepcopy(baseline);p=d['pages'][0]
    if change=='crop': p['crop_box'][0]+=1000000;p['effective_crop_box'][0]+=1000000
    if change=='effective_crop': p['media_box'][2]=200000000;p['effective_crop_box'][2]=200000000
    if change=='media':p['media_box'][0]-=1000000
    if change=='rotation':p['rotation']=180
    if change=='user_unit':p['user_unit']['numerator']=2
    if change=='address':d['pages'][0]['pdf_page'],d['pages'][1]['pdf_page']=2,1
    probe('stale_'+change+'_internal',d,diagnostic='identity remapping' if change=='address' else 'stale evidence page geometry',root=False)
    probe('stale_'+change+'_source',d,diagnostic='identity remapping' if change=='address' else 'stale page geometry/source structure basis')
    if change!='address':
        # Forge the new basis deliberately: actual source geometry must still reject.
        d['evidence'][0]['page_basis_hash']=inv.page_basis_hash(p)
        probe('forged_basis_'+change,d,diagnostic='stale page geometry/source structure basis')

d=copy.deepcopy(baseline);d['evidence'][0]['render_parameters']['dpi']=72
probe('false_dpi',d,diagnostic='render DPI/geometry pixel dimensions mismatch')
d=copy.deepcopy(baseline);d['evidence'][0]['render_parameters']['width_pixels']+=1
probe('false_pixel_rounding',d,diagnostic='render DPI/geometry pixel dimensions mismatch')
d=copy.deepcopy(baseline);d['pages'][0]['label'].update(status='verified',value='S1',evidence=d['evidence'][1]['id'])
probe('cross_page_label',d,diagnostic='printed label evidence belongs to another physical page')
d['pages'][0]['label']['evidence']=d['evidence'][0]['id'];probe('same_page_label',d,'accept')
d['pages'][0]['label'].update(status='embedded_unverified',value='metadata-only',evidence=None)
report=probe('embedded_label_not_visual_confirmation',d,'accept')
assert d['pages'][0]['label']['status']=='embedded_unverified'

# Exclusion baseline uses a synthetic authority claim, never real approval.
excluded=copy.deepcopy(baseline);excluded['evidence']=[]
decision=write('s/decision.json',{'synthetic':True,'human_authority_authenticated':False})
r=excluded['regions'][0]
r['coverage']['transcription'].update(status='excluded',gap=False,reason='Synthetic scope test',boundary={'source_revision':excluded['source']['sha256'],'partition_hash':inv.partition_hash(excluded),'region_id':r['id'],'box':r['box'],'level':'transcription','actor':'Synthetic claim','actor_role':'human_owner','authorization':'Unverified fixture only','rationale':'Scope check only','decision':inv.file_pin(ROOT,rel(decision))})
excluded=reseal(excluded);report=probe('unchanged_exclusion_basis',excluded,'accept')
assert report['exclusion_claims'][0]['source_ig_review_freshness']=='unknown' and report['exclusion_claims'][0]['human_authority']=='unverified'
for change in ['kind','uncertainty','key','registry','source_id','source_revision','address','partition','denominator','order','link']:
    d=copy.deepcopy(excluded);r=d['regions'][0]
    if change=='kind':r['kind']='diagram'
    if change=='uncertainty':r['uncertainty'].append('Independent changed uncertainty')
    if change=='key':
        old=r['key'];r['key']='author-key-changed'
        next(e for e in d['registry']['entries'] if e['kind']=='region' and e['key']==old)['key']=r['key']
    if change=='registry':d['registry']['entries'].append({'kind':'region','key':'retired-extra','id':'region:5eab769b-c268-40a0-90fd-2e68c775e35f'})
    if change=='source_id':d['source']['id']=d['registry']['source_id']='source:changed-author-scope'
    if change=='source_revision':
        sha='1'*64;d['source']['sha256']=d['source']['pdf']['sha256']=d['registry']['source_revision']=sha
        for x in d['pages']+d['regions']:x['source_revision']=sha
    if change=='address':d['pages'][0]['pdf_page'],d['pages'][1]['pdf_page']=2,1
    if change=='partition':r['box'][2]=900000
    if change=='denominator':d['regions'][1]['denominator_role']='context'
    if change=='order':d['reading_order'].reverse()
    if change=='link':d['links']=[{'kind':'continuation','from':d['regions'][0]['id'],'to':d['regions'][1]['id'],'reason':'Changed author link'}]
    expected='physical page identity remapping' if change=='address' else 'exclusion boundary is not exact/current'
    probe('stale_exclusion_'+change,d,diagnostic=expected,root=False)
    report=inv.coverage(reseal(d))
    assert report['exclusion_claims'][0]['author_scope_freshness']=='stale'
    assert report['exclusion_claims'][0]['source_ig_review_freshness']=='unknown'

# Whole-record changes intentionally outside author basis: do not imply approval.
d=copy.deepcopy(excluded);d['regions'][0]['coverage']['transcription']['reason']='Changed coverage record rationale'
report=probe('coverage_only_change_not_ig1a_approval',d,'accept')
assert report['exclusion_claims'][0]['source_ig_review_freshness']=='unknown' and report['exclusion_claims'][0]['human_authority']=='unverified'
d=copy.deepcopy(baseline);d['pages'].reverse();probe('reordered_pages',d,'accept')
d=copy.deepcopy(baseline);d['source']['page_count']=1
for count in d['source']['independent_counts']:count['count']=1
d['pages']=d['pages'][:1];d['regions']=d['regions'][:1];d['reading_order']=d['reading_order'][:1];d['evidence']=d['evidence'][:1]
probe('concealed_missing_actual_page',d,diagnostic='missing PDF page/source structure count mismatch')
# Keep source-revision identity distinct from UUID allocation.
try:structural_inventory(ROOT,rel(original),rel(provenance),'source:independent-review',digest(original),baseline['registry'])
except ValueError as exc:RESULTS.append({'name':'changed_pdf_registry_reuse','expectation_met':'explicit page/region remapping required' in str(exc),'error':str(exc)})
else:RESULTS.append({'name':'changed_pdf_registry_reuse','expectation_met':False})

# Independent coverage/order/error boundaries beyond R01-R05.
plain=copy.deepcopy(baseline);plain['evidence']=[]
context=inv.make_region(plain['registry'],'context-overlap',plain['pages'][0],[0,0,1000000,1000000],role='context')
plain['regions'].append(context);plain['reading_order'].append(context['id'])
report=probe('overlapping_context_denominator',plain,'accept');assert report['denominator_regions']==2 and report['context_regions']==1
d=copy.deepcopy(plain);d['regions'][-1]['denominator_role']='inventory';probe('overlapping_inventory',d,diagnostic='overlapping inventory denominator')
d=copy.deepcopy(baseline);d['evidence']=[];d['regions'].append(copy.deepcopy(d['regions'][0]));probe('duplicate_region',d,diagnostic='duplicate region identity/key')
d=copy.deepcopy(baseline);d['evidence']=[];d['regions']=d['regions'][:1];d['reading_order']=d['reading_order'][:1]
report=probe('uncovered_page_area_visible',d,'accept');assert report['pages'][1]['unaccounted_area_trillionths']==1000000000000
d=copy.deepcopy(baseline);d['evidence']=[];d['regions'][0]['coverage']['transcription'].update(status='partial',gap=True,reason='Synthetic partial')
report=probe('partial_not_represented',d,'accept');assert report['levels']['transcription']['represented']==0 and report['levels']['transcription']['partial']==1
d['regions'][0]['coverage']['transcription']['gap']=False;probe('partial_requires_gap',d,diagnostic='partial/unprocessed must retain a gap')
d=copy.deepcopy(baseline);d['reading_order']=d['reading_order'][:1];probe('reading_order_missing',d,diagnostic='reading order must name each region exactly once')

# Fractional, nonzero-origin, partial normalized crop and all clockwise rotations.
# Native expected region [53.35,72.6125,173.65,298.175] was calculated from the
# authored [13.25,27.5,213.75,328.25] CropBox and [0.2,0.1,0.8,0.85] fractions.
# Physical dimensions are independently 180.45 by 338.34375 points (UserUnit 1.5).
# Four color centers are transformed independently into raster coordinates.
geometry=[]
for rotation in [0,90,180,270]:
    writer=PdfWriter();p=writer.add_page(PdfReader(pdf).pages[0]);p.rotation=rotation
    variant=S/f'rotation-{rotation}.pdf'
    with variant.open('xb') as f:writer.write(f)
    doc=structural_inventory(ROOT,rel(variant),rel(provenance),'source:oracle-'+str(rotation),digest(variant))
    doc['regions'][0]['box']=[200000,100000,800000,850000];doc=reseal(doc)
    for dpi in [72,144]:
        ev=extract_evidence(doc,doc['regions'][0]['id'],ROOT,rel(S/f'r{rotation}-d{dpi}'),dpi=dpi)
        expected=[math.ceil(Fraction(3609,20)*dpi/72),math.ceil(Fraction(10827,32)*dpi/72)]
        if rotation in [90,270]:expected.reverse()
        image=Image.open(ROOT/ev['image']['path']).convert('RGB')
        samples=[]
        for x,y,color in [(81,302.5,(26,51,204)),(177.5,256,(204,26,51)),(100.5,111,(26,179,51)),(188,134.5,(179,51,204))]:
            if not 53.35<x<173.65 or not 72.6125<y<298.175:continue
            px=(x-53.35)*1.5;py=(298.175-y)*1.5;w,h=180.45,338.34375
            if rotation==90:px,py=h-py,px
            elif rotation==180:px,py=w-px,h-py
            elif rotation==270:px,py=py,w-px
            point=(int(px*dpi/72),int(py*dpi/72));actual=image.getpixel(point)
            samples.append({'pixel':point,'expected':color,'actual':actual,'matches':max(abs(a-b) for a,b in zip(actual,color))<=1})
        candidate=copy.deepcopy(doc);candidate['evidence']=[ev];candidate=reseal(candidate)
        report=probe(f'fractional_crop_r{rotation}_dpi{dpi}',candidate,'accept')
        row={'rotation':rotation,'dpi':dpi,'native_crop':['53.35','72.6125','173.65','298.175'],'physical_size_points':['180.45','338.34375'],'expected_pixels':expected,'actual_pixels':image.size,'samples':samples,'dimension_match':list(image.size)==expected,'candidate':pin(RUN/f'cases/fractional_crop_r{rotation}_dpi{dpi}.json')}
        geometry.append(row)
        assert row['dimension_match'] and all(s['matches'] for s in samples)
write('geometry-oracles.json',{'basis':'Independently authored native coordinates, exact physical rationals, per-axis ceiling, manually transformed interior color landmarks. No WGC geometry helpers used for expected values.','results':geometry})
write('probe-results.json',{'started_utc':START,'ended_utc':utc(),'results':RESULTS})
assert all(r['expectation_met'] for r in RESULTS)
