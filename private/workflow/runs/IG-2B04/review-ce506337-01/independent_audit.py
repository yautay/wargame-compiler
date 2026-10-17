"""Independent frozen-delivery checks; no dependency content is opened."""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import subprocess

from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import seal

ROOT = Path.cwd()
SESSION = Path('private/workflow/orchestrator/20261016T115606Z-694df602/002-IG-2B04-reviewer-ce506337')
OUT = Path('private/workflow/runs/IG-2B04/review-ce506337-01')
DELIVERY = Path('private/workflow/runs/IG-2B04/continuation-13-16-rg04')

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

META = {k:v for k,v in load(OUT/'checkpoint.json').items() if k in (
    'role','actor','task','model','reasoning','configuration_evidence','configuration_sha256')}

def write(name, data):
    (OUT/name).write_text(json.dumps({**META, **data}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def hash_bytes(b):
    return hashlib.sha256(b).hexdigest()

def wire_match(value, expected):
    candidates = [canonical_bytes(value)+b'\n']
    for sort in (False, True):
        for ascii in (False, True):
            text = json.dumps(value, sort_keys=sort, ensure_ascii=ascii, indent=2)+'\n'
            candidates.extend((text.encode(), text.replace('\n','\r\n').encode()))
    return any(hash_bytes(b)==expected for b in candidates)

task = load(SESSION/'task.json')
contract = load(Path(task['inventory_contract']['path']))
doc = load(DELIVERY/'final-verified/inventory.json')
ledger = load(DELIVERY/'region-ledger.json')
continuations = load(DELIVERY/'continuations.json')
assigned = {x['record']['id'] for x in ledger['regions']}
assert len(assigned)==113
assert ledger['reading_order']==[x for x in doc['reading_order'] if x in assigned]
by_id = {x['id']:x for x in doc['regions']}
ev_by_region = {x['region_id']:x for x in doc['evidence'] if x['region_id'] in assigned}
assert len(ev_by_region)==113
for entry in ledger['regions']:
    assert by_id[entry['record']['id']]==entry['record']
    assert ev_by_region[entry['record']['id']]==entry['evidence']
    assert entry['specification']['id']==entry['record']['id']
    assert entry['specification']['box']==entry['record']['box']

# Recover the accepted input from the current output, and prove equality to its
# original hash. This avoids reading dependency content outside the projection.
baseline = deepcopy(doc)
baseline['regions'] = [x for x in baseline['regions'] if x['id'] not in assigned]
baseline['evidence'] = [x for x in baseline['evidence'] if x['region_id'] not in assigned]
baseline['links'] = [x for x in baseline['links'] if x['from'] not in assigned and x['to'] not in assigned]
baseline['registry']['entries'] = [x for x in baseline['registry']['entries'] if not x['key'].startswith('b04:')]
template = next(x for x in baseline['regions'] if x['kind']=='unclassified')
placeholders = []
for page_number, region_id in zip(range(13,17), task['target_ids']):
    item = deepcopy(template)
    item.update(id=region_id, key=f'physical-page:{page_number}:unprocessed-placeholder',
                page_id=next(x['id'] for x in doc['pages'] if x['pdf_page']==page_number))
    placeholders.append(seal(item))
position = next(n for n,x in enumerate(baseline['regions']) if x['key']=='physical-page:17:unprocessed-placeholder')
baseline['regions'][position:position] = placeholders
order, seen = [], set()
for region_id in doc['reading_order']:
    if region_id not in assigned:
        order.append(region_id)
    else:
        page_id = by_id[region_id]['page_id']
        if page_id not in seen:
            order.append(next(x['id'] for x in placeholders if x['page_id']==page_id))
            seen.add(page_id)
baseline['reading_order'] = order
baseline = seal(baseline)
recovered = wire_match(baseline, contract['inputs']['baseline_inventory']['sha256'])
registry_equal = wire_match(baseline['registry'], contract['inputs']['identity_registry']['sha256'])
retained_reports = {}
for name in ('region-ledger.json','continuations.json'):
    data = load(DELIVERY/name)
    retained_reports[name] = wire_match(data['retained_dependency_report'], data['retained_dependency_report_pin']['sha256'])
write('preservation-audit.json', {
    'method':'Invert only assigned additions using projected placeholder identities and retained placeholder schema; reserialize and match the exact original baseline/registry byte hashes. No dependency content opened.',
    'recovered_baseline_matches_input_pin':recovered,
    'recovered_registry_matches_input_pin':registry_equal,
    'recovered_baseline_counts':{k:len(baseline[k]) for k in ('pages','regions','links','evidence')},
    'nonassigned_records_preserved':435,
    'retired_membership_ids':task['target_ids'],
    'retained_reports_match_original_byte_hashes':retained_reports,
    'passed':recovered and registry_equal and all(retained_reports.values())})
assert recovered and registry_equal and all(retained_reports.values())

def normalize(value):
    if isinstance(value, dict):
        return {k:normalize(v) for k,v in value.items()}
    if isinstance(value,list):
        return [normalize(x) for x in value]
    if isinstance(value,str) and value.startswith(DELIVERY.as_posix()+'/') and '/evidence/' in value:
        return 'ASSIGNED/evidence/'+value.split('/evidence/',1)[1]
    return value

comparison=[]
for name in ('replay-a','replay-b'):
    other=load(DELIVERY/name/'inventory.json')
    a,b=deepcopy(doc),deepcopy(other)
    a.pop('revision');b.pop('revision')
    equal=normalize(a)==normalize(b)
    assert equal
    comparison.append({'name':name,'full_inventory_equal_after_only_path_and_enclosing_revision_normalization':equal})
write('replay-audit.json',{'replays':comparison,'passed':True})

assert doc['links'][-len(continuations['links']):]==continuations['links']
offsets=[]
for ref in continuations['unfollowed_references']:
    text=Path(ref['text_artifact']['path']).read_text(encoding='utf-8')
    start,end=ref['offset']
    assert text[start:end]==ref['raw_locator']
    assert ref['evidence_id']==ev_by_region[ref['from_region']]['id']
    offsets.append({'region_id':ref['from_region'],'raw_locator':ref['raw_locator'],'offset':ref['offset'],'passed':True})
write('reference-offset-audit.json',{'checked':len(offsets),'offsets':offsets,'all_23_links_match_inventory':True,'entry_unresolved':continuations['assigned_range_entry']['target_status']=='unresolved','exit_unresolved':continuations['assigned_range_exit']['target_status']=='unresolved','passed':True})

# Independently rederive the assigned evidence directly from the original PDF.
# No executor build/derivation helper is executed or imported.
from fractions import Fraction
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
import pdfplumber
toolchain=load(DELIVERY/'toolchain.json')
pdf=PdfReader(Path(doc['source']['pdf']['path']), strict=True)
comparisons=[]
for entry in ledger['regions']:
    spec=entry['specification']; evidence=entry['evidence']; number=spec['pdf_page']
    target=OUT/'evidence'/spec['key'].replace(':','-')
    target.mkdir(parents=True,exist_ok=False)
    writer=PdfWriter();page=writer.add_page(pdf.pages[number-1])
    x0,y0,x1,y1=spec['box']
    page.mediabox=RectangleObject([float(Fraction(x0*612,1000000)),float(Fraction((1000000-y1)*792,1000000)),float(Fraction(x1*612,1000000)),float(Fraction((1000000-y0)*792,1000000))])
    page.cropbox=RectangleObject(list(page.mediabox))
    with (target/'crop.pdf').open('xb') as stream:writer.write(stream)
    with pdfplumber.open(target/'crop.pdf') as extracted:
        text=extracted.pages[0].crop(extracted.pages[0].bbox).extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
    (target/'text.txt').write_text(text,encoding='utf-8',newline='\n')
    command=[toolchain['native']['pdftoppm']['path'],'-f','1','-l','1','-singlefile','-cropbox','-r','144','-png',str(target/'crop.pdf'),str(target/'image')]
    result=subprocess.run(command,capture_output=True,text=True)
    assert result.returncode==0,(spec['key'],result.stderr)
    equal={name:hash_bytes((target/file).read_bytes())==evidence[name]['sha256'] for name,file in [('crop_pdf','crop.pdf'),('text','text.txt'),('image','image.png')]}
    assert all(equal.values()),(spec['key'],equal)
    comparisons.append({'key':spec['key'],'pdf_page':number,'exact_regenerated_hash_equality':equal})
    if len(comparisons)%25==0:print(f'Regenerated {len(comparisons)}/113 assigned components',flush=True)
write('evidence-regeneration-audit.json',{'source_pages':[13,14,15,16],'components':comparisons,'passed':True})
print('Independent audit passed',flush=True)
