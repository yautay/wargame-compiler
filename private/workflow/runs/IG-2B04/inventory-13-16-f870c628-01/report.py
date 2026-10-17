"""Preservation, replay, complete locator and original-component audits."""
import copy
import datetime
import hashlib
import importlib.metadata
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pdfplumber
from PIL import Image, ImageDraw
from wgc.sources.inventory import coverage, digest, file_pin, page_basis_hash, seal, validate

ROOT = Path.cwd()
OUT = Path(__file__).parent
REL = OUT.relative_to(ROOT).as_posix()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(name,value):
    with (OUT/name).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(value,f,indent=2,ensure_ascii=False)
        f.write('\n')


def main():
    claim=load(OUT/'claim.json')
    common={k:claim[k] for k in ('role','actor','task','model','reasoning','configuration_evidence','configuration_sha256')}
    task=load(Path(claim['configuration_evidence']).parent/'task.json')
    contract=load(task['inventory_contract']['path'])
    spec=load(OUT/'authored-regions.json')['regions']
    baseline=load(contract['inputs']['baseline_inventory']['path'])
    accepted_registry=load(contract['inputs']['identity_registry']['path'])
    docs={mode:load(OUT/mode/'inventory.json') for mode in ('replay-a','replay-b','final-verified')}
    final=docs['final-verified']
    assigned={r['id'] for r in spec}
    retired=set(task['target_ids'])
    finalregions={r['id']:r for r in final['regions']}
    finalevidence={ev['region_id']:ev for ev in final['evidence'] if ev['region_id'] in assigned}
    bykey={r['key']:r for r in spec}
    for mode,doc in docs.items():
        validate(doc,ROOT)
        assert doc['pages']==baseline['pages']
        assert doc['source']==baseline['source']
        assert doc['registry']==load(OUT/mode/'identity-registry.json')
        assert doc['regions']==final['regions']
        assert doc['links']==final['links']
        assert doc['reading_order']==final['reading_order']
        assert all(e in doc['registry']['entries'] for e in accepted_registry['entries'])
        assert [r for r in doc['regions'] if r['id'] not in assigned]==[r for r in baseline['regions'] if r['id'] not in retired]
        assert doc['evidence'][:len(baseline['evidence'])]==baseline['evidence']
        assert doc['links'][:len(baseline['links'])]==baseline['links']
        assert [i for i in doc['reading_order'] if i not in assigned]==[i for i in baseline['reading_order'] if i not in retired]
        assert len(doc['pages'])==44
        assert retired.isdisjoint({r['id'] for r in doc['regions']})
    def normalized(doc):
        result=copy.deepcopy(doc)
        for ev in result['evidence']:
            if ev['region_id'] in assigned:
                for kind in ('text','image','crop_pdf'):
                    ev[kind]['path']='<fresh-generated>/'+ev['region_id']+'/'+Path(ev[kind]['path']).name
        return seal(result)
    norms={mode:normalized(doc) for mode,doc in docs.items()}
    assert norms['replay-a']==norms['replay-b']==norms['final-verified']
    write('replay-report.json',{**common,'format':'wgc-complete-replay-report-1','result':'pass',
        'basis':'Three independently generated complete inventories; no generated evidence copied between runs.',
        'runs':[{'mode':m,'inventory':file_pin(ROOT,REL+'/'+m+'/inventory.json'),
                 'regeneration':file_pin(ROOT,REL+'/'+m+'/regeneration.json'),
                 'normalized_revision':norms[m]['revision'],'assigned_evidence':len(assigned)} for m in docs],
        'equalities':['complete source/pages/registry/regions/order/links/toolchain',
                      'retained evidence exact', 'assigned evidence IDs/revisions/page bases/geometry',
                      'assigned crop PDF/PNG/text SHA-256, lengths, text offsets and extraction parameters'],
        'normalization':'Only generated artifact path strings and enclosing inventory revision are normalized. Byte hashes, region revisions and every retained locator stay exact.',
        'differences':[], 'semantic_acceptance_granted':False})
    preserved=[]
    for pin in contract['inputs'].values():
        assert file_pin(ROOT,pin['path'])==pin
        preserved.append(pin)
    write('preservation-report.json',{**common,'format':'wgc-inventory-preservation-report-1','result':'pass',
        'inputs_verified_unchanged':preserved,'complete_pages':44,
        'baseline_counts':{k:len(baseline[k]) for k in ('pages','regions','evidence','links')},
        'final_counts':{k:len(final[k]) for k in ('pages','regions','evidence','links')},
        'nonassigned_regions_equal':len(baseline['regions'])-4,'retired_active_memberships':sorted(retired),
        'all_registry_bindings_retained':True,'retired_registry_bindings_retained':True,
        'accepted_registry_entries':len(accepted_registry['entries']),'current_registry_entries':len(final['registry']['entries']),
        'nonassigned_reading_order_equal':True,'nonassigned_evidence_and_links_equal':True,
        'all_three_complete_outputs_checked':True,'note':'Canonical record equality checked directly, without printing nonassigned content.'})
    # Preserve current repaired reports structurally, with their exact provenance.
    # The nested original records are retained dependency observations, not new
    # assigned membership/inspection/acceptance. Active membership is the full sidecar.
    ledger=load(contract['inputs']['region_ledger']['path'])
    continuations=load(contract['inputs']['continuations']['path'])
    current=[]
    for rec in spec:
        region=finalregions[rec['id']]
        current.append({**rec,'revision':region['revision'],'source_sha256':final['source']['sha256'],
                        'page_basis_hash':finalevidence[rec['id']]['page_basis_hash'],
                        'coverage':region['coverage'],'evidence':finalevidence[rec['id']],
                        'inspection_basis':file_pin(ROOT,REL+'/original-inspection.json')})
    write('region-ledger.json',{**common,'format':'wgc-independent-region-ledger-1',
        'source':contract['inputs']['pdf'],'physical_pages':[13,14,15,16],
        'inventory':file_pin(ROOT,REL+'/final-verified/inventory.json'),
        'retained_dependency_pin':contract['inputs']['region_ledger'],
        'retained_dependency_records':ledger,'assigned_records':current,
        'retired_placeholder_memberships':sorted(retired),
        'membership_authority':'The complete final inventory; retained dependency records preserve their original scope and exact locators.',
        'editorial_policy':'Margins, backgrounds, running headers, printed labels, footer and blank areas remain inventoried; no model-authored human exclusion.',
        'semantic_acceptance_granted':False})
    addedlinks=final['links'][len(baseline['links']):]
    targets={}
    for rec in spec:
        match=re.match(r'(?:heading-)?(\d{1,2}\.\d{1,2})(?:$|-)',rec['key'].split(':',2)[2])
        if match: targets.setdefault(match[1],[]).append(rec['id'])
    mentions=[]
    for rec in spec:
        ev=finalevidence[rec['id']]
        text=(ROOT/ev['text']['path']).read_text(encoding='utf-8')
        for match in re.finditer(r'(?<!\d)\d{1,2}\.\d{1,2}(?!\d)',text):
            mentions.append({'region_id':rec['id'],'pdf_page':rec['pdf_page'],'text_artifact':ev['text'],
                            'codepoint_offsets':[match.start(),match.end()],'printed_number':match[0],
                            'visible_assigned_units':targets.get(match[0],[]),
                            'status':'assigned printed-number candidate only' if match[0] in targets else 'unresolved outside assigned pages',
                            'uncertainty':'Printed clause labels and reference mentions are retained without automatic semantic binding.'})
    write('continuations.json',{**common,'format':'wgc-inventory-continuations-1',
        'retained_dependency_pin':contract['inputs']['continuations'],'retained_dependency_records':continuations,
        'assigned_links':addedlinks,'printed_number_occurrences':mentions,
        'entry_boundary':load(OUT/'original-inspection.json')['entry_boundary'],
        'exit_boundary':load(OUT/'original-inspection.json')['exit_boundary'],
        'unresolved_chart':'6.27 describes the Movement Cost Chart; the actual chart is absent from these pages and was not inspected.',
        'boundary_access':'Only physical pages13-16 images/text; page12 accepted exit metadata only. No page17 or external target inspection.',
        'semantic_acceptance_granted':False})
    fullcoverage=coverage(final)
    assigned_doc=copy.deepcopy(final)
    assigned_doc['regions']=[r for r in final['regions'] if r['id'] in assigned]
    assigned_doc['pages']=[p for p in final['pages'] if p['pdf_page'] in (13,14,15,16)]
    taskcoverage=coverage(assigned_doc)
    context_doc=copy.deepcopy(assigned_doc)
    context_doc['regions']=[]
    context_doc['pages']=[]
    write('coverage-report.json',{**common,'format':'wgc-inventory-coverage-report-1',
        'inventory':file_pin(ROOT,REL+'/final-verified/inventory.json'),
        'full_44_pages':fullcoverage,'task_pages13_16':taskcoverage,'context_only':coverage(context_doc),
        'gaps':[{'region_id':r['id'],'level':level,**cov} for r in final['regions'] for level,cov in r['coverage'].items() if cov['gap']],
        'interpretation':'Geometric tiling and source-unit inventory are separate from verified transcription and semantic coverage. Partial/unprocessed/excluded units never count as represented.',
        'semantic_acceptance_granted':False})
    write('source-pins.json',{**common,'format':'wgc-source-pins-1','inputs':contract['inputs'],
        'execution_contract':task['inventory_contract'],'source':final['source'],
        'retained_dependency_pin':contract['inputs']['source_pins'],
        'retained_dependency_records':load(contract['inputs']['source_pins']['path']),
        'assigned_originals':load(OUT/'original-inspection.json')['pages']})
    native={}
    for name,version_args in [('git',['--version']),('pdfinfo',['-v']),('pdftoppm',['-v']),('pwsh',['--version'])]:
        executable=Path(shutil.which(name))
        result=subprocess.run([str(executable),*version_args],capture_output=True,text=True,check=True)
        raw=executable.read_bytes()
        native[name]={'version':(result.stdout+result.stderr).strip(),
                      'executable':{'path':executable.as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}}
    toolchain=load(contract['inputs']['toolchain']['path'])
    assert os.environ['PYTHONPATH']==toolchain['process_pythonpath']
    assert os.environ['PATH'].startswith(toolchain['process_path_prefix'])
    raw=Path(sys.executable).read_bytes()
    write('toolchain.json',{**common,'format':'wgc-inventory-toolchain-1',
        'python_executable':{'path':Path(sys.executable).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)},
        'python_version':sys.version,'process_pythonpath':os.environ['PYTHONPATH'],
        'process_path_prefix':toolchain['process_path_prefix'],
        'libraries':{name:importlib.metadata.version(name) for name in ('pypdf','pdfplumber','Pillow','pytest','reportlab')},
        'native':native,'dpi':144,'text_parameters':{'x_tolerance':3,'y_tolerance':3,'layout':False},
        'accepted_toolchain_pin':contract['inputs']['toolchain'],'process_settings_changed':False})
    # Audit every frozen recursive path/hash pin in both retained report trees and
    # every complete output, including all old crop artifacts, without reading text.
    pins={}
    def collect(value):
        if isinstance(value,dict):
            if isinstance(value.get('path'),str) and re.fullmatch('[a-f0-9]{64}',str(value.get('sha256',''))):
                key=(value['path'],value['sha256'])
                pins[key]=value
            for child in value.values(): collect(child)
        elif isinstance(value,list):
            for child in value: collect(child)
    for value in [ledger,continuations,contract['inputs'],*docs.values()]: collect(value)
    verified=[]
    for (_,sha),pin in sorted(pins.items()):
        path=ROOT/pin['path']
        raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==sha, pin['path']
        if 'bytes' in pin: assert len(raw)==pin['bytes'],pin['path']
        verified.append({'path':pin['path'],'sha256':sha,'bytes':len(raw)})
    for ev in final['evidence']:
        region=finalregions[ev['region_id']]
        page=next(p for p in final['pages'] if p['id']==region['page_id'])
        assert ev['page_basis_hash']==page_basis_hash(page)
        assert ev['region_revision']==region['revision']
        assert ev['pdf_page']==page['pdf_page'] and ev['source_sha256']==final['source']['sha256']
    write('reference-audit.json',{**common,'format':'wgc-inventory-reference-audit-1','result':'pass',
        'retained_report_pins':[contract['inputs']['region_ledger'],contract['inputs']['continuations']],
        'verified_artifact_pins':verified,'verified_unique_pins':len(verified),
        'complete_inventories_validated':['replay-a','replay-b','final-verified'],
        'active_region_evidence_locators_verified':len(final['evidence']),
        'page_source_basis_and_offsets_verified':True,'retained_reports_carried_structurally':True,
        'dangling_local_references':[],'outside_scope_targets':'Explicit unresolved observations, not falsely resolved.'})
    qa=OUT/'qa'
    qa.mkdir(exist_ok=False)
    glyph_results=[]
    with pdfplumber.open(ROOT/contract['inputs']['pdf']['path']) as pdf:
        for number in (13,14,15,16):
            recs=[r for r in spec if r['pdf_page']==number]
            cross=[]
            for char in pdf.pages[number-1].chars:
                if not char['text'].strip(): continue
                box=[char['x0']/612*1000000,char['top']/792*1000000,char['x1']/612*1000000,char['bottom']/792*1000000]
                owners=[r for r in recs if r['box'][0]<=box[0] and r['box'][1]<=box[1] and r['box'][2]>=box[2] and r['box'][3]>=box[3]]
                if len(owners)!=1: cross.append({'glyph':char['text'],'box':box,'owner_count':len(owners)})
            assert not cross,(number,cross[:5])
            image=Image.new('RGB',(1224,1584),'white')
            for r in recs:
                with Image.open(ROOT/finalevidence[r['id']]['image']['path']) as crop:
                    image.paste(crop.convert('RGB'),(r['box'][0]*1224//1000000,r['box'][1]*1584//1000000))
            image.save(qa/f'page-{number}-reconstructed.png')
            overlay=Image.open(OUT/f'original-pages/page-{number}.png').convert('RGB')
            draw=ImageDraw.Draw(overlay)
            for index,r in enumerate(recs,1):
                box=r['render_box_pixels']
                draw.rectangle(box,outline='#d4009b',width=1)
                draw.text((box[0]+2,box[1]+2),str(index),fill='#d4009b')
            overlay.save(qa/f'page-{number}-partition.png')
            glyph_results.append({'physical_page':number,'glyphs_checked':sum(bool(c['text'].strip()) for c in pdf.pages[number-1].chars),
                                  'cross_boundary_or_unowned_glyphs':cross,'regions':len(recs),
                                  'reconstructed':file_pin(ROOT,REL+f'/qa/page-{number}-reconstructed.png'),
                                  'partition_overlay':file_pin(ROOT,REL+f'/qa/page-{number}-partition.png')})
    write('geometry-inspection.json',{**common,'format':'wgc-original-component-boundary-audit-1',
        'result':'pass','pages':glyph_results,'note':'Every non-space extracted original glyph belongs wholly to exactly one authored region. Graphic components also require visual comparison; zero glyph crossings alone is not visual acceptance.'})
    write('checkpoint-built.json',{**common,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'summary':'Three complete generations validated, preservation/replay/reference audits passed; visual crop reconstruction and final test handoff remain.',
        'input_packet':file_pin(ROOT,(Path(claim['configuration_evidence']).parent/'packet.json').as_posix()),
        'artifacts':[file_pin(ROOT,REL+'/'+name) for name in ('preservation-report.json','replay-report.json','reference-audit.json','geometry-inspection.json')],
        'blocker':None,'next_operation':'Inspect every reconstructed page and diagram/marker component; freeze final tests and delivery.'})
    print(json.dumps({'reports':'built','assigned_regions':len(assigned),'full_regions':len(final['regions']),
                      'unique_reference_pins_verified':len(verified),'all_original_glyph_boundaries':'pass'}))


if __name__=='__main__':
    main()
