"""Pinned local PDF geometry, independent page count, crop render/text evidence."""
from __future__ import annotations
import copy
from fractions import Fraction
import hashlib
from pathlib import Path
import re
import subprocess
from .geometry import micro_points, effective_crop, box_to_pdf
from .inventory import assign, assemble, file_pin, make_region, new_registry, safe_artifact, seal, validate_registry, page_basis_hash


def source_structure(pdf, *, pdfinfo='pdfinfo'):
    """Read count/geometry only; never extract source text or images."""
    from pypdf import PdfReader
    reader = PdfReader(pdf, strict=True)
    result = subprocess.run([str(pdfinfo),str(pdf)],capture_output=True,text=True,check=True)
    match = re.search(r'^Pages:\s+(\d+)\s*$',result.stdout,re.M)
    if match is None or int(match[1])!=len(reader.pages):
        raise ValueError('independent PDF page count disagreement')
    geometry = {}
    for number,page in enumerate(reader.pages,1):
        media = [micro_points(v) for v in page.mediabox]
        crop = [micro_points(v) for v in page.cropbox]
        rotation = page.rotation % 360
        if rotation not in (0,90,180,270): raise ValueError('unsupported page rotation')
        unit = Fraction(str(page.get('/UserUnit',1)))
        if unit<=0: raise ValueError('nonpositive PDF UserUnit')
        geometry[number] = {'media_box':media,'crop_box':crop,
                            'effective_crop_box':effective_crop(media,crop),'rotation':rotation,
                            'user_unit':{'numerator':unit.numerator,'denominator':unit.denominator}}
    return geometry, int(match[1])


def inspect_pdf(root, pdf_path, provenance_path, source_id, expected_sha256, registry=None, *, pdfinfo='pdfinfo'):
    from pypdf import PdfReader, __version__ as version
    pdf = safe_artifact(root,pdf_path)
    pin = file_pin(root,pdf_path)
    if pin['sha256']!=expected_sha256: raise ValueError('PDF input hash changed')
    reader = PdfReader(pdf, strict=True)
    geometry, count = source_structure(pdf,pdfinfo=pdfinfo)
    poppler = subprocess.run([str(pdfinfo),'-v'],capture_output=True,text=True,check=True)
    registry = copy.deepcopy(registry) if registry is not None else new_registry(source_id,expected_sha256)
    validate_registry(registry)
    if (registry['source_id'],registry['source_revision'])!=(source_id,expected_sha256):
        raise ValueError('source changed; explicit page/region remapping required')
    labels=reader.page_labels if '/PageLabels' in reader.trailer['/Root'] else None
    pages=[]
    for number,page in enumerate(reader.pages,1):
        key=f'physical-page:{number}'
        label = {'status':'embedded_unverified','value':str(labels[number-1]),'reason':'PDF PageLabels metadata, not visual printed-label verification','evidence':None} if labels else {'status':'unknown','value':None,'reason':'No verified printed label; PDF page number is separate','evidence':None}
        pages.append(seal({'id':assign(registry,'page',key),'key':key,'source_revision':expected_sha256,
                           'pdf_page':number,'label':label,**geometry[number]}))
    if file_pin(root,pdf_path)!=pin: raise ValueError('PDF changed during inspection')
    source={'id':source_id,'sha256':expected_sha256,'pdf':pin,'provenance':file_pin(root,provenance_path),
            'page_count':count,'independent_counts':[{'tool':'pypdf','count':count},{'tool':'poppler-pdfinfo','count':count}]}
    tools=[{'name':'pypdf','version':version},{'name':'poppler-pdfinfo','version':(poppler.stderr+poppler.stdout).strip()}]
    return source,pages,registry,tools


def structural_inventory(root, pdf_path, provenance_path, source_id, expected_sha256, registry=None, **options):
    source,pages,registry,tools=inspect_pdf(root,pdf_path,provenance_path,source_id,expected_sha256,registry,**options)
    regions=[make_region(registry,f'physical-page:{p["pdf_page"]}:unprocessed-placeholder',p,[0,0,1_000_000,1_000_000],reason='Structural placeholder only; substantive inventory pending IG-2B') for p in pages]
    return assemble(source,pages,regions,registry,toolchain=tools)


def extract_evidence(document, region_id, root, output_directory, *, dpi=144, pdftoppm='pdftoppm'):
    """Write a new cropped PDF, UTF-8 text and PNG with independent exact pins.

    Extraction order and OCR/meaning confidence are not reading-order decisions.
    The clipped PDF is a derived artifact; original publisher bytes stay unchanged.
    """
    from pypdf import PdfReader, PdfWriter, __version__ as pypdf_version
    from pypdf.generic import RectangleObject, NameObject
    import pdfplumber
    from PIL import Image
    from .inventory import validate
    validate(document,root)
    if type(dpi) is not int or not 36<=dpi<=600: raise ValueError('DPI must be an integer in 36..600')
    region = next((r for r in document['regions'] if r['id']==region_id),None)
    if region is None: raise ValueError('unknown evidence region')
    page = next(p for p in document['pages'] if p['id']==region['page_id'])
    directory = safe_artifact(root,output_directory)
    if directory.exists(): raise ValueError('evidence output must be new')
    pdf_pin=document['source']['pdf']; input_pdf=safe_artifact(root,pdf_pin['path'])
    reader=PdfReader(input_pdf,strict=True); writer=PdfWriter()
    cropped=writer.add_page(reader.pages[page['pdf_page']-1])
    native=box_to_pdf(region['box'],page)
    cropped.mediabox=RectangleObject([float(v) for v in native]); cropped.cropbox=RectangleObject([float(v) for v in native])
    # Normalize UserUnit in the derived copy for consistent Poppler/pdfplumber frames.
    unit=Fraction(page['user_unit']['numerator'],page['user_unit']['denominator'])
    if unit != 1: cropped.scale_by(float(unit))
    cropped.pop(NameObject('/UserUnit'),None)
    directory.mkdir(parents=True,exist_ok=False)
    crop_rel=output_directory+'/crop.pdf'; text_rel=output_directory+'/text.txt'; image_rel=output_directory+'/image.png'
    with safe_artifact(root,crop_rel).open('xb') as stream: writer.write(stream)
    with pdfplumber.open(safe_artifact(root,crop_rel)) as pdf:
        view=pdf.pages[0].crop(pdf.pages[0].bbox)
        text=view.extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
    safe_artifact(root,text_rel).write_text(text,encoding='utf-8',newline='\n')
    args=[str(pdftoppm),'-f','1','-l','1','-singlefile','-cropbox','-r',str(dpi),'-png',str(safe_artifact(root,crop_rel)),str(directory/'image')]
    subprocess.run(args,capture_output=True,text=True,check=True)
    version=subprocess.run([str(pdftoppm),'-v'],capture_output=True,text=True,check=True)
    with Image.open(safe_artifact(root,image_rel)) as image: width,height=image.size
    if file_pin(root,pdf_pin['path'])!=pdf_pin: raise ValueError('PDF changed during evidence extraction')
    basis_hash = page_basis_hash(page)
    return {'id':'evidence:'+hashlib.sha256((region['id']+region['revision']+basis_hash+str(dpi)).encode()).hexdigest(),
            'source_sha256':document['source']['sha256'],'region_id':region_id,'region_revision':region['revision'],
            'page_id':page['id'],'pdf_page':page['pdf_page'],'box':region['box'],'page_basis_hash':basis_hash,
            'crop_pdf':file_pin(root,crop_rel),'text':file_pin(root,text_rel),'image':file_pin(root,image_rel),
            'text_codepoints':len(text),'text_offsets':{'unit':'unicode_codepoints','bounds':'half_open','start':0,'end':len(text)},
            'text_parameters':{'engine':'pdfplumber','version':pdfplumber.__version__,'x_tolerance':3,'y_tolerance':3,'layout':False},
            'render_parameters':{'engine':'poppler-pdftoppm','version':(version.stderr+version.stdout).strip(),
                                 'dpi':dpi,'cropbox':True,'format':'png','width_pixels':width,'height_pixels':height},
            'crop_parameters':{'engine':'pypdf','version':pypdf_version,'user_unit_normalized':True,'frame':'displayed-crop-top-left'},
            'uncertainty':['Machine text extraction; no verified transcription, OCR, reading order or source meaning.']}
