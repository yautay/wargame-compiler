"""Task-owned complete serial derivation, preserving the byte-pinned baseline.

This is an operational batch adapter to the installed source contracts. It performs
the same exact crop/text/render derivation as wgc.sources.pdf, with whole-document
validation at each end of a batch instead of repeating it before each component.
No process pools or semantic decisions are used.
"""
import argparse
import copy
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from fractions import Fraction
import pdfplumber
import pypdf
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject, NameObject
from PIL import Image
from wgc.sources.geometry import box_to_pdf
from wgc.sources.inventory import (assign, make_region, seal, validate, file_pin,
                                   page_basis_hash, coverage)

ROOT=Path.cwd()
A=Path(__file__).parent.relative_to(ROOT)
SESSION=Path('private/workflow/orchestrator/20261016T195516Z-332903f5/005-IG-2B07-executor-32eedee6')
TASK=json.loads((SESSION/'task.json').read_text())
SCOPE=TASK['source_scope']
CFG=SESSION/'runtime-configuration.json'
META={'role':'executor','actor':'ig2:005-IG-2B07-executor-32eedee6:executor',
      'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':CFG.as_posix(),
      'configuration_sha256':file_pin(ROOT,CFG.as_posix())['sha256']}
def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def pin(path):
    return file_pin(ROOT,Path(path).as_posix())
def verify_inputs():
    pins=[SCOPE[k] for k in ('baseline_inventory','identity_registry','source_pdf','source_provenance')]+list(SCOPE['current_reports'].values())+[TASK['refinement_evidence']]
    for expected in pins:
        assert pin(expected['path'])==expected,expected['path']
    prior=Path('private/workflow/runs/IG-2B07/inventory-25-28-01/delivery.json')
    assert pin(prior)['sha256']=='cee94ecd856edb0da9439881a0e002f7515f45f334a1b4e02fcd16b3f20cab27'
    for expected in json.loads(prior.read_text())['artifacts']:
        assert pin(expected['path'])==expected,expected['path']
    current=[TASK['repair_authorization'][k] for k in ('scope','evidence')]
    current += [{'path':TASK['repair_authorization']['review_evidence'],'sha256':TASK['repair_authorization']['review_sha256']}]
    for expected in current:
        actual=pin(expected['path'])
        assert all(actual[k]==v for k,v in expected.items()),expected['path']
    pins += [pin(prior),*current,pin(SESSION/'packet.json')]
    cfg=json.loads(CFG.read_text())
    assert (cfg['status'],cfg['model'],cfg['reasoning'])==('confirmed','gpt-6.1-sol','high')
    return pins

def serial_evidence(doc, region, directory, reader, version):
    """Complete fresh crop PDF + clipped text + Poppler PNG for one region."""
    assert not directory.exists()
    directory.mkdir(parents=True,exist_ok=False)
    page=next(p for p in doc['pages'] if p['id']==region['page_id'])
    writer=PdfWriter()
    cropped=writer.add_page(reader.pages[page['pdf_page']-1])
    native=box_to_pdf(region['box'],page)
    cropped.mediabox=RectangleObject([float(v) for v in native])
    cropped.cropbox=RectangleObject([float(v) for v in native])
    unit=Fraction(page['user_unit']['numerator'],page['user_unit']['denominator'])
    if unit!=1:
        cropped.scale_by(float(unit))
    cropped.pop(NameObject('/UserUnit'),None)
    with (directory/'crop.pdf').open('xb') as stream:
        writer.write(stream)
    with pdfplumber.open(directory/'crop.pdf') as pdf:
        view=pdf.pages[0].crop(pdf.pages[0].bbox)
        text=view.extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
    (directory/'text.txt').write_text(text,encoding='utf-8',newline='\n')
    command=['pdftoppm','-f','1','-l','1','-singlefile','-cropbox','-r','144','-png',str(directory/'crop.pdf'),str(directory/'image')]
    subprocess.run(command,capture_output=True,text=True,check=True)
    with Image.open(directory/'image.png') as im:
        width,height=im.size
    basis=page_basis_hash(page)
    return {'id':'evidence:'+hashlib.sha256((region['id']+region['revision']+basis+'144').encode()).hexdigest(),
            'source_sha256':doc['source']['sha256'],'region_id':region['id'],'region_revision':region['revision'],
            'page_id':page['id'],'pdf_page':page['pdf_page'],'box':region['box'],'page_basis_hash':basis,
            'crop_pdf':pin(directory/'crop.pdf'),'text':pin(directory/'text.txt'),'image':pin(directory/'image.png'),
            'text_codepoints':len(text),'text_offsets':{'unit':'unicode_codepoints','bounds':'half_open','start':0,'end':len(text)},
            'text_parameters':{'engine':'pdfplumber','version':pdfplumber.__version__,'x_tolerance':3,'y_tolerance':3,'layout':False},
            'render_parameters':{'engine':'poppler-pdftoppm','version':version,'dpi':144,'cropbox':True,'format':'png','width_pixels':width,'height_pixels':height},
            'crop_parameters':{'engine':'pypdf','version':pypdf.__version__,'user_unit_normalized':True,'frame':'displayed-crop-top-left'},
            'uncertainty':['Machine text extraction; no verified transcription, OCR, reading order or source meaning.']},command

def ordered_rows(author):
    result=[]
    for number in (24,25,26,27,28,29):
        page=[r for r in author['regions'] if r['page']==number]
        for row in page:
            if row['category']=='component':
                continue
            result.append(row)
            result.extend(c for c in page if c.get('parent_key')==row['key'])
    assert len(result)==len(author['regions'])
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare-registry',action='store_true')
    parser.add_argument('--output')
    args=parser.parse_args()
    started=time.time()
    inputs=verify_inputs()
    author=json.loads((A/'author-input.json').read_text())
    rows=ordered_rows(author)
    if args.prepare_registry:
        destination=A/'author-registry.json'
        assert not destination.exists()
        registry=json.loads(Path('private/workflow/runs/IG-2B07/inventory-25-28-01/author-registry.json').read_text())
        for row in rows:
            assign(registry,'region',row['key'])
        write(destination,registry)
        write(A/'author-pins.json',{'author':pin(A/'author-input.json'),'registry':pin(destination),'generator':pin(A/'run_inventory.py')})
        print('Persisted identities for every authored region and component.')
        return
    destination=Path(args.output)
    assert destination.parent==A and not destination.exists()
    destination.mkdir(exist_ok=False)
    author_pins=json.loads((A/'author-pins.json').read_text())
    assert author_pins['author']==pin(A/'author-input.json')
    assert author_pins['registry']==pin(A/'author-registry.json')
    assert author_pins['generator']==pin(A/'run_inventory.py')
    # Complete accepted baseline is loaded only inside this exact transformation and
    # preservation comparison; no unassigned text or dependency history is emitted.
    baseline=json.loads(Path(SCOPE['baseline_inventory']['path']).read_text())
    registry=json.loads((A/'author-registry.json').read_text())
    pages={p['pdf_page']:p for p in baseline['pages']}
    new=[]
    for row in rows:
        region=make_region(registry,row['key'],pages[row['page']],row['box'],kind=row['kind'],role=row['role'],
                           reason='Source inventory observation only; transcription and semantic representation require separate work.')
        region['uncertainty']=['Machine-extracted text is not a verified full transcription; tiny diagram glyphs remain unverified.']
        region['coverage']['transcription']={'status':'partial','gap':True,'reason':'Fresh clipped machine text/image retained; no verified full transcription.','boundary':None}
        new.append(seal(region))
    retired=set(SCOPE['replace_only_region_ids'])
    retained=[r for r in baseline['regions'] if r['id'] not in retired]
    bykey={r['key']:r for r in new}
    new_links=[{'kind':l['kind'],'from':bykey[l['left']]['id'],'to':bykey[l['right']]['id'],'reason':l['reason']} for l in author['links']]
    order=[]
    for identity in baseline['reading_order']:
        if identity in retired:
            number=next(p['pdf_page'] for p in baseline['pages'] if p['id']==next(r['page_id'] for r in baseline['regions'] if r['id']==identity))
            if number==25:
                order.extend(r['id'] for r in new if r['key']=='ig2b07:entry-context')
            order.extend(r['id'] for r in new if r['page_id']==pages[number]['id'])
            if number==28:
                order.extend(r['id'] for r in new if r['key']=='ig2b07:exit-context')
        else:
            order.append(identity)
    doc=seal({**baseline,'registry':registry,'regions':retained+new,'reading_order':order,'links':baseline['links']+new_links})
    validate(doc,ROOT)
    reader=PdfReader(SCOPE['source_pdf']['path'],strict=True)
    version_result=subprocess.run(['pdftoppm','-v'],capture_output=True,text=True,check=True)
    version=(version_result.stderr+version_result.stdout).strip()
    evidence=[]
    invocations=[]
    for index,region in enumerate(new,1):
        ev,command=serial_evidence(doc,region,destination/'evidence'/region['key'].replace(':','-'),reader,version)
        evidence.append(ev)
        invocations.append({'region_id':region['id'],'command':command,'exit_code':0})
        if index%20==0:
            print(f'{destination.name}: {index}/{len(new)} serial regions/components',flush=True)
    doc=seal({**doc,'evidence':baseline['evidence']+evidence})
    result=validate(doc,ROOT)
    # Exact preservation, not a structural/sample proxy.
    assert doc['source']==baseline['source'] and doc['pages']==baseline['pages']
    result_byid={r['id']:r for r in doc['regions']}
    assert all(result_byid[r['id']]==r for r in baseline['regions'] if r['id'] not in retired)
    assert set(r['id'] for r in baseline['regions'])-set(result_byid)==retired
    assert doc['evidence'][:len(baseline['evidence'])]==baseline['evidence']
    assert doc['links'][:len(baseline['links'])]==baseline['links']
    old_registry=json.loads(Path(SCOPE['identity_registry']['path']).read_text())
    assert all(e in registry['entries'] for e in old_registry['entries'])
    assert [x for x in order if x in set(baseline['reading_order'])]==[x for x in baseline['reading_order'] if x not in retired]
    assert all(r['denominator_role']=='context' or pages[next(p['pdf_page'] for p in baseline['pages'] if p['id']==r['page_id'])]['pdf_page'] in (25,26,27,28) for r in new)
    write(destination/'inventory.json',doc)
    write(destination/'identity-registry.json',registry)
    report_rows=[]
    for row,region,ev in zip(rows,new,evidence):
        assert row['key']==region['key'] and ev['region_id']==region['id']
        report_rows.append({**row,'region':region,'evidence':ev,'parent_region_id':bykey[row['parent_key']]['id'] if 'parent_key' in row else None})
    write(destination/'region-accounting.json',report_rows)
    write(destination/'derivation-report.json',{**META,'input_pins':inputs,'author_pins':author_pins,'command':subprocess.list2cmdline([sys.executable,*sys.argv]),'serial':True,'complete_target_ids':[r['id'] for r in new],'component_ids':[r['id'] for row,r in zip(rows,new) if row['category']=='component'],'invocations':invocations,'validation':result,'preservation':{'all_nonretired_records_exact':True,'all_pages_exact':True,'source_exact':True,'all_inherited_evidence_exact':True,'all_inherited_links_exact':True,'all_existing_registry_entries_exact':True,'inherited_reading_order_exact':True,'retired_only':sorted(retired)},'elapsed_seconds':time.time()-started})
    verify_inputs()
    print(json.dumps({'output':destination.as_posix(),'new_evidence':len(evidence),'denominator':result['denominator_regions'],'context':result['context_regions'],'elapsed_seconds':time.time()-started}),flush=True)

if __name__=='__main__':
    main()
