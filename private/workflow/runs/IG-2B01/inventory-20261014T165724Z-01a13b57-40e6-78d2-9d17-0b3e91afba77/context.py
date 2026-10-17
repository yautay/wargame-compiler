from prepare import *
tool=read(f'{REL}/toolchain.json'); sys.path[:0]=tool['process_pythonpath'].split(';'); os.environ['PATH']=tool['process_path_prefix']+';'+os.environ['PATH']
from wgc.sources.inventory import make_region, assemble, seal
from wgc.sources.pdf import extract_evidence
from math import floor,ceil
b=read(f'{BASE}/inventory-one/inventory.json'); page=b['pages'][4]
box=[floor(44/612*1e6),floor(50/792*1e6),ceil(303/612*1e6),ceil(105/792*1e6)]
write(f'{REL}/context-access-authorization.json',{'page':5,'native_top_left_points':[44,50,303,105],'box':box,'reason':'Page 4 right column Triarii entry ends mid-sentence at spear-armed; inspect only the adjacent completion at page 5 top left.','denominator_role':'context','task_denominator_contribution':0,'further_page_5_content_analysis':False,'recorded_before_extraction_utc':datetime.now(timezone.utc).isoformat()})
r=make_region(b['registry'],'ig2b01:context:triarii-tail',page,box,kind='clause',role='context',reason='Boundary continuation context only; transcription not verified.')
b['regions'].append(r); b['reading_order'].append(r['id']); b=seal(b)
e=extract_evidence(b,r['id'],ROOT,f'{REL}/context-triarii',dpi=144)
write(f'{REL}/context-record.json',{'region':r,'evidence':e,'registry':b['registry']})
print((ROOT/e['text']['path']).read_text(encoding='utf-8'))
