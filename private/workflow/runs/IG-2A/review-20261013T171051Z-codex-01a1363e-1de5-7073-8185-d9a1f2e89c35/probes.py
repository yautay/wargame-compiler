"""Independent boundary probes; expected rejection is recorded, never repaired."""
import copy, json, sys
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from wgc.sources.inventory import seal, validate, file_pin, make_region, partition_hash, LEVELS
from wgc.sources.pdf import structural_inventory, extract_evidence

OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[4]
if len(sys.argv)>1:
    OUT=OUT/sys.argv[1];OUT.mkdir(exist_ok=False)
REL=OUT.relative_to(ROOT).as_posix()
S=OUT/'s';S.mkdir(exist_ok=False)
c=Canvas(str(S/'source.pdf'),pagesize=(200,300),invariant=1)
for page in (1,2):
    c.drawString(20,260,f'SYNTHETIC PAGE {page} TOP LEFT')
    c.drawString(110,80,f'BOTTOM RIGHT {page}')
    c.showPage()
c.save();(S/'provenance.json').write_text('{"synthetic":true}\n')
pin=file_pin(ROOT,REL+'/s/source.pdf')
base=structural_inventory(ROOT,REL+'/s/source.pdf',REL+'/s/provenance.json','source:review-synthetic',pin['sha256'])
evs=[extract_evidence(base,r['id'],ROOT,REL+f'/e{i}') for i,r in enumerate(base['regions'])]
base['evidence']=evs;base=seal(base);validate(base,ROOT)
results=[]
def reseal(d):
    d['pages']=[seal(p) for p in d['pages']];d['regions']=[seal(r) for r in d['regions']]
    return seal(d)
def probe(name,mutate,expected='reject',root=ROOT):
    d=copy.deepcopy(base)
    mutate(d);d=reseal(d)
    (OUT/(name+'.input.json')).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
    try:
        report=validate(d,root);actual='accept';err=None
    except Exception as e:
        report=None;actual='reject';err=type(e).__name__+': '+str(e)
    result={'name':name,'expected':expected,'actual':actual,'expectation_met':expected==actual,'error':err,'report':report}
    results.append(result);print(name,actual,'OK' if expected==actual else 'DEFECT',err or '',flush=True)
    return d

probe('baseline',lambda d:None,'accept')
report=validate(base,ROOT)
assert report['denominator_regions']==2 and all(report['levels'][l]['represented']==0 and report['levels'][l]['unprocessed']==2 for l in LEVELS)
assert all(p['unaccounted_area_trillionths']==0 for p in report['pages'])
results.append({'name':'placeholders_are_not_represented','expectation_met':True,'independent_expected':{'unprocessed':2,'represented':0,'area_per_page':10**12},'report':report})
def partial(d): d['regions'][0]['coverage']['transcription']['status']='partial';d['evidence']=[]
probe('partial_retains_gap',partial,'accept')
def missing(d): d['pages'].pop();d['evidence']=[]
probe('missing_page',missing)
def empty(d): d['regions']=[];d['reading_order']=[];d['evidence']=[]
gap=probe('empty_pages_visible',empty,'accept')
assert all(p['unaccounted_area_trillionths']==10**12 and p['gap_reason'] for p in validate(gap,ROOT)['pages'])
def duplicate(d): d['regions'].append(copy.deepcopy(d['regions'][0]))
probe('duplicate_region',duplicate)
def contexts(d):
    for key in ('context-a','context-b'):
        r=make_region(d['registry'],key,d['pages'][0],[0,0,1000000,1000000],role='context')
        d['regions'].append(r);d['reading_order'].append(r['id'])
context=probe('overlapping_contexts',contexts,'accept')
assert validate(context,ROOT)['denominator_regions']==2
def overlap(d):
    r=make_region(d['registry'],'overlap',d['pages'][0],[0,0,500000,500000]);d['regions'].append(r);d['reading_order'].append(r['id'])
probe('inventory_overlap',overlap)
probe('registry_source_change',lambda d:d['registry'].update(source_revision='f'*64))
probe('registry_duplicate',lambda d:d['registry']['entries'].append(copy.deepcopy(d['registry']['entries'][0])))
probe('stale_region',lambda d:d['regions'][0]['uncertainty'].append('new observation'))
probe('reading_order_missing',lambda d:d['reading_order'].pop())
probe('dangling_note',lambda d:d['links'].append({'kind':'note_for','from':d['regions'][0]['id'],'to':'unknown','reason':'Synthetic note'}))
probe('stale_page_rotation',lambda d:d['pages'][0].update(rotation=90))
probe('stale_page_userunit',lambda d:d['pages'][0]['user_unit'].update(numerator=2))
def crop(d):
    p=d['pages'][0];p['crop_box'][0]=10000000;p['effective_crop_box'][0]=10000000
probe('stale_page_crop',crop)
probe('false_render_dpi',lambda d:d['evidence'][0]['render_parameters'].update(dpi=72))
probe('false_pixel_size',lambda d:d['evidence'][0]['render_parameters'].update(width_pixels=401))
probe('wrong_page_printed_label',lambda d:d['pages'][0]['label'].update(status='verified',value='2',reason='Synthetic wrong-page claim',evidence=d['evidence'][1]['id']))
def swap(d):
    d['evidence']=[];d['pages'][0]['pdf_page'],d['pages'][1]['pdf_page']=2,1
probe('physical_page_remapping',swap)
def outside(d): d['evidence'][0]['text']['path']='private/../escape.txt'
probe('unsafe_path',outside)
def tamper_pin(d): d['evidence'][0]['text']['sha256']='f'*64
probe('tampered_pin',tamper_pin)

decision=S/'decision.json';decision.write_text('{"synthetic_claim":"Scope page one only; not real acceptance"}\n')
def exclusion(d):
    d['evidence']=[];r=d['regions'][0];cov=r['coverage']['transcription']
    cov.update(status='excluded',gap=False,reason='Synthetic page-one boundary')
    cov['boundary']={'source_revision':d['source']['sha256'],'partition_hash':partition_hash(d),'region_id':r['id'],'box':r['box'],'level':'transcription','actor':'synthetic human','actor_role':'human_owner','authorization':'Synthetic claim only','rationale':'Page one only','decision':file_pin(ROOT,REL+'/s/decision.json')}
excluded=probe('exact_exclusion_claim',exclusion,'accept')
def excluded_swap(d): exclusion(d);d['pages'][0]['pdf_page'],d['pages'][1]['pdf_page']=2,1
probe('exclusion_after_page_remap',excluded_swap)
def excluded_partition(d): exclusion(d);d['regions'][1]['box'][2]=500000
probe('exclusion_after_partition_change',excluded_partition)
def excluded_revision(d): exclusion(d);d['regions'][0]['kind']='editorial';d['regions'][0]['uncertainty'].append('Changed scope characterization')
probe('exclusion_after_region_revision',excluded_revision)
def excluded_key(d):
    exclusion(d);r=d['regions'][0];old=r['key'];r['key']='new-scope-key'
    next(e for e in d['registry']['entries'] if e['kind']=='region' and e['key']==old)['key']=r['key']
probe('exclusion_after_registry_change',excluded_key)
def false_count(d):
    d['evidence']=[];d['source']['page_count']=1;d['source']['independent_counts']=[{'tool':'pypdf','count':1},{'tool':'poppler-pdfinfo','count':1}]
    d['pages']=d['pages'][:1];d['regions']=d['regions'][:1];d['reading_order']=d['reading_order'][:1]
probe('false_consistent_page_count',false_count)
out={'probes':results,'total':len(results),'unmet':sum(not r['expectation_met'] for r in results),'semantic_acceptance':False}
(OUT/'probe-results.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
sys.exit(1 if out['unmet'] else 0)
