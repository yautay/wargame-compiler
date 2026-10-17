"""Owned serial derivation from the accepted baseline and authorized F03/F04 candidate selections.

Named frozen candidate selections and their persisted identities are authorized
inputs; all original observations, source derivatives and validation are fresh.
"""
from __future__ import annotations
import copy
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pdfplumber
import pypdf
from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from wgc.sources.geometry import box_to_pdf, render_size_pixels, overlaps
from wgc.sources.inventory import (assign, make_region, seal, validate,
    file_pin, page_basis_hash, digest)

ROOT = Path(__file__).resolve().parent.relative_to(Path.cwd())
REPO = Path.cwd()
SESSION = Path('private/workflow/orchestrator/20261017T151724Z-86fb83c5/001-IG-2B08-executor-4f6fdb30')
CONTRACT = Path('private/workflow/runs/IG-2B08/manifest-recovery-20261017-F01-01/input-pins.json')
PIN = json.loads(CONTRACT.read_text(encoding='utf-8'))
TASK = json.loads((SESSION/'task.json').read_text(encoding='utf-8'))
SPECS = json.loads((ROOT/'author-selections.json').read_text(encoding='utf-8'))


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=True, indent=2)+'\n', encoding='utf-8')


def pin(path):
    return file_pin(REPO, Path(path).as_posix())


def metadata():
    return dict(role='executor', actor='ig2:001-IG-2B08-executor-4f6fdb30:executor',
                model='gpt-6.1-sol', reasoning='high',
                configuration_evidence=(SESSION/'runtime-configuration.json').as_posix(),
                configuration_sha256=pin(SESSION/'runtime-configuration.json')['sha256'])


def old_preservation():
    scope=load(TASK['repair_authorization']['scope']['path'])
    m=load(scope['preserve_manifest']['path'])
    count=0
    def walk(o):
        nonlocal count
        if isinstance(o,dict):
            if 'path' in o and 'sha256' in o:
                assert pin(o['path'])['sha256']==o['sha256'],o['path']
                count+=1
            for v in o.values(): walk(v)
        elif isinstance(o,list):
            for v in o: walk(v)
    walk(m)
    return count


def baseline():
    for field in ('baseline_inventory','identity_registry'):
        assert pin(PIN[field]['path'])==PIN[field]
    base=load(PIN['baseline_inventory']['path'])
    registry=load(PIN['identity_registry']['path'])
    assert base['registry']==registry
    assert len(base['pages'])==44
    assert {k:len(base[k]) for k in ('pages','regions','evidence','links')}==PIN['counts']
    return base,registry


def normalized(s):
    if s['page']==33: return [73529,63131,500000,101011]
    return [round(s['points'][0]*1000000/612),round(s['points'][1]*1000000/792),
            round(s['points'][2]*1000000/612),round(s['points'][3]*1000000/792)]


def selected_regions(base, registry):
    pages={p['pdf_page']:p for p in base['pages']}
    result=[]
    for s in SPECS:
        r=make_region(registry,s['key'],pages[s['page']],normalized(s),kind=s['kind'],role=s['role'],reason='')
        r['uncertainty']=['Physical source observation only. No verified transcription or accepted source meaning.']
        r['coverage']={
            'transcription':dict(status='partial',reason='Fresh clipped machine text and pixels; punctuation/counter glyphs and reading order remain unverified.',gap=True,boundary=None),
            'descriptive_semantics':dict(status='partial',reason='Physical classification and component observation only; meaning remains unaccepted.',gap=True,boundary=None),
            'formal_semantics':dict(status='unprocessed',reason='Outside physical inventory scope; no gameplay formalization.',gap=True,boundary=None)}
        result.append(seal(r))
    for i,r in enumerate(result):
        if r['denominator_role']=='inventory':
            for q in result[:i]:
                if q['page_id']==r['page_id'] and q['denominator_role']=='inventory':
                    assert not overlaps(q['box'],r['box']),(q['key'],r['key'])
    return result


def ordered_specs(page):
    items=[s for s in SPECS if s['page']==page]
    # Explicit column-first physical reading order. Diagram details follow their
    # field tiles; all overlapping detail crops remain outside the denominator.
    left=[];right=[];head=[];foot=[]
    for s in items:
        key=s['key'].split(':',2)[2]
        if key=='running-header':head.append(s)
        elif key=='copyright':foot.append(s)
        elif s['points'][0]<306:left.append(s)
        else:right.append(s)
    def order(seq):
        # Group every panel's components after that panel's tiles.
        groups={}
        for s in seq:
            group=s['group'] if s['kind']=='diagram' and s['group'] else s['key']
            groups.setdefault(group,[]).append(s)
        chunks=list(groups.values())
        chunks.sort(key=lambda g:(min(x['points'][1] for x in g),min(x['points'][0] for x in g)))
        return [x for g in chunks for x in sorted(g,key=lambda s:(s['role']=='context',s['points'][1],s['points'][0],s['key']))]
    return head+order(left)+order(right)+foot


def author_document(base, registry, regions):
    result=copy.deepcopy(base)
    retired=set(TASK['inventory_contract']['placeholder_target_ids'])
    result['regions']=[r for r in result['regions'] if r['id'] not in retired]+copy.deepcopy(regions)
    ids={r['key']:r['id'] for r in regions}
    old={r['id']:r for r in base['regions']}
    pages={p['id']:p['pdf_page'] for p in base['pages']}
    order=[]
    for identity in base['reading_order']:
        if identity in retired:
            page=pages[old[identity]['page_id']]
            order.extend(ids[s['key']] for s in ordered_specs(page))
            if page==32:order.append(ids['ig2b08:p33:exit-context'])
        else:order.append(identity)
    result['reading_order']=order
    result['registry']=copy.deepcopy(registry)
    def link(kind,a,b,reason):
        result['links'].append({'kind':kind,'from':ids[a],'to':ids[b],'reason':reason})
    for a,b in [('p30:advance-854-start','p30:advance-854-end'),('p30:pursue-next-page','p31:pursue-continuation'),('p31:finished-upper','p31:finished-close'),('p31:pass-through-upper','p31:pass-through-lower'),('p31:pass-through-step2','p32:pass-through-step3'),('p32:table-one-six-result','p32:table-seven-nine-result'),('p32:rampage-exit','p33:exit-context')]:
        link('continuation','ig2b08:'+a,'ig2b08:'+b,'Visible column/page continuation, not an executable relation.')
    # Preserve inherited entry link and reference the fresh inspected paragraph.
    result['links'].append({'kind':'continuation','from':TASK['inventory_contract']['retained_context_ids'][0],
                            'to':ids['ig2b08:p29:incoming-example'],'reason':'Accepted page-28 exit context is retained; freshly inspected page-29 paragraph matches the incoming continuation.'})
    # Geometry margins must not reorder the reviewed physical source sequence.
    reviewed_order = load('private/workflow/runs/IG-2B08/repair-F02-validation02/region-ledger.json')['reading_order']
    assert set(reviewed_order) == set(result['reading_order'])
    assert len(reviewed_order) == len(result['reading_order'])
    result['reading_order'] = list(reviewed_order)
    return seal(result)


def evidence(doc, r, directory, reader, original):
    """Serial derivative; text always clipped on original before extraction.

    In particular, never extract retained out-of-clip streams from page-33 crop PDF.
    Native raster output is restricted to the normalized authorized crop dimensions.
    """
    page=next(p for p in doc['pages'] if p['id']==r['page_id'])
    directory.mkdir(parents=True,exist_ok=False)
    writer=PdfWriter()
    # PdfWriter.add_page clones the page into this fresh writer, matching the
    # installed source tooling. Do not deepcopy the reader's entire object graph.
    cropped=writer.add_page(reader.pages[page['pdf_page']-1])
    native=box_to_pdf(r['box'],page)
    cropped.mediabox=RectangleObject([float(x) for x in native]);cropped.cropbox=RectangleObject([float(x) for x in native])
    with (directory/'crop.pdf').open('xb') as stream:writer.write(stream)
    x0,y0,x1,y1=r['box']
    original_box=(x0*612/1000000,y0*792/1000000,x1*612/1000000,y1*792/1000000)
    text=original.pages[page['pdf_page']-1].crop(original_box,strict=True).extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
    (directory/'text.txt').write_text(text,encoding='utf-8',newline='\n')
    width,height=render_size_pixels(r['box'],page,144)
    subprocess.run(['pdftoppm','-f','1','-l','1','-singlefile','-cropbox','-r','144','-x','0','-y','0','-W',str(width),'-H',str(height),'-png',str(directory/'crop.pdf'),str(directory/'image')],capture_output=True,check=True)
    with Image.open(directory/'image.png') as im: assert im.size==(width,height)
    basis=page_basis_hash(page)
    version=subprocess.run(['pdftoppm','-v'],capture_output=True,text=True,check=True)
    return {'id':'evidence:'+hashlib.sha256((r['id']+r['revision']+basis+'144').encode()).hexdigest(),
        'source_sha256':doc['source']['sha256'],'region_id':r['id'],'region_revision':r['revision'],
        'page_id':page['id'],'pdf_page':page['pdf_page'],'box':r['box'],'page_basis_hash':basis,
        'crop_pdf':pin(directory/'crop.pdf'),'text':pin(directory/'text.txt'),'image':pin(directory/'image.png'),
        'text_codepoints':len(text),'text_offsets':{'unit':'unicode_codepoints','bounds':'half_open','start':0,'end':len(text)},
        'text_parameters':{'engine':'pdfplumber','version':pdfplumber.__version__,'x_tolerance':3,'y_tolerance':3,'layout':False},
        'render_parameters':{'engine':'poppler-pdftoppm','version':(version.stderr+version.stdout).strip(),'dpi':144,'cropbox':True,'format':'png','width_pixels':width,'height_pixels':height},
        'crop_parameters':{'engine':'pypdf','version':pypdf.__version__,'user_unit_normalized':True,'frame':'displayed-crop-top-left'},
        'uncertainty':['Original-page clipped machine extraction; punctuation, diagram labels and counter glyphs unverified; no accepted source meaning.']}


def prepare():
    assert old_preservation()==19579
    base,registry=baseline()
    if (ROOT/'author-registry.json').exists():
        registry=load(ROOT/'author-registry.json')
    regions=selected_regions(base,registry)
    doc=author_document(base,registry,regions)
    validate(doc)
    write(ROOT/'author-registry.json',registry)
    write(ROOT/'author-inventory.json',doc)
    # Boundary overlays show ALL primary and detail rectangles against fresh originals.
    for page in (29,30,31,32):
        im=Image.open(ROOT/'originals'/f'page-{page}.png').convert('RGB')
        d=ImageDraw.Draw(im)
        rows=[s for s in SPECS if s['page']==page]
        for s in rows:
            box=tuple(round(x*2) for x in s['points'])
            d.rectangle(box,outline='red' if s['role']=='inventory' else 'blue',width=1)
        im.save(ROOT/'originals'/f'page-{page}-boundaries.png')
    tools={**metadata(),'process_pythonpath':os.environ.get('PYTHONPATH'),'process_path_prefix':os.environ.get('PATH','').split(';'),
           'libraries':{x:importlib.metadata.version(x) for x in ('pypdf','pdfplumber','Pillow','pytest','reportlab')},
           'native':{x:pin(Path(shutil.which(x)).relative_to(REPO)) if Path(shutil.which(x)).is_relative_to(REPO) else {'path':shutil.which(x),'sha256':hashlib.sha256(Path(shutil.which(x)).read_bytes()).hexdigest()} for x in ('pdftoppm','pdfinfo','pwsh')},
           'evidence_generation':'Serial current-process Python; one native CLI per artifact; no worker pools.',
           'text_access':'Original-page crop before extract_text for every new region; page 33 only authorized outward normalized rounding of exact rectangle.'}
    write(ROOT/'toolchain.json',tools)
    print(json.dumps({'prepared':True,'regions':len(regions),'preserved_old_artifacts':19579}))


def run(name):
    assert name in ('final-verified','replay-1','replay-2')
    base,_=baseline()
    registry=load(ROOT/'author-registry.json')
    regions=selected_regions(base,registry)
    doc=author_document(base,registry,regions)
    directory=ROOT/name;directory.mkdir(exist_ok=False)
    pdf=PIN['source']['pdf']['path'];reader=PdfReader(pdf,strict=True)
    with pdfplumber.open(pdf) as original:
        for i,r in enumerate(regions,1):
            ev=evidence(doc,r,directory/'evidence'/r['key'].replace(':','-'),reader,original)
            doc['evidence'].append(ev)
            if i%50==0: print(f'{name}: {i}/{len(regions)} serial regions',flush=True)
    doc=seal(doc)
    write(directory/'inventory.json',doc);write(directory/'identity-registry.json',registry)
    validate(doc,REPO)
    assert doc['registry']==load(directory/'identity-registry.json')
    print(json.dumps({'replay':name,'regions_generated':len(regions),'inventory':pin(directory/'inventory.json'),'validated':True}),flush=True)


if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run(sys.argv[1])
