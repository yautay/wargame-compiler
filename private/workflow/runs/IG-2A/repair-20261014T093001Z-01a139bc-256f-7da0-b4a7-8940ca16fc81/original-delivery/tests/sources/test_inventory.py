"""Public fixtures are synthetic; expected geometry and coverage are independent."""
import copy
from pathlib import Path
from types import SimpleNamespace
import pytest
from wgc.sources.geometry import (SCALE, pdf_to_box, box_to_pdf, display_box,
                                  display_size_points, effective_crop)
from wgc.sources.inventory import (new_registry, make_region, assemble, seal, validate,
                                   safe_artifact, partition_hash, LEVELS, file_pin)
from wgc.sources.pdf import structural_inventory, extract_evidence


@pytest.fixture
def source(tmp_path):
    from reportlab.pdfgen.canvas import Canvas
    path=tmp_path/'private/source'; path.mkdir(parents=True)
    canvas=Canvas(str(path/'synthetic.pdf'),pagesize=(400,600),invariant=1)
    canvas.drawString(30,550,'Left column first'); canvas.drawString(230,550,'Right column second')
    canvas.drawString(30,480,'Table A: cell alpha'); canvas.drawString(30,450,'Note A: synthetic annotation')
    canvas.drawString(30,50,'Continuation starts here'); canvas.showPage()
    canvas.drawString(30,550,'Continuation ends here'); canvas.showPage(); canvas.save()
    (path/'provenance.json').write_text('{"synthetic":true}\n',encoding='utf-8')
    pin=file_pin(tmp_path,'private/source/synthetic.pdf')
    return tmp_path,pin['sha256']


def seed(source, registry=None):
    root,sha=source
    return structural_inventory(root,'private/source/synthetic.pdf','private/source/provenance.json',
                                'source:synthetic',sha,registry)


def reseal(doc):
    doc['pages']=[seal(p) for p in doc['pages']]
    doc['regions']=[seal(r) for r in doc['regions']]
    return seal(doc)


def authored(source):
    doc=seed(source); registry=doc['registry']; p1,p2=doc['pages']
    regions=[make_region(registry,'left',p1,[0,0,500000,500000],kind='clause'),
             make_region(registry,'right',p1,[500000,0,1000000,500000],kind='clause'),
             make_region(registry,'table',p1,[0,500000,1000000,700000],kind='table'),
             make_region(registry,'note',p1,[0,700000,1000000,800000],kind='note'),
             make_region(registry,'start',p1,[0,800000,1000000,1000000],kind='clause'),
             make_region(registry,'end',p2,[0,0,1000000,1000000],kind='clause')]
    return assemble(doc['source'],doc['pages'],regions,registry,
                    reading_order=[r['id'] for r in regions],
                    links=[{'kind':'note_for','from':regions[3]['id'],'to':regions[2]['id'],'reason':'Synthetic note belongs to table A'},
                           {'kind':'continuation','from':regions[4]['id'],'to':regions[5]['id'],'reason':'Synthetic content spans pages'}])


def test_independent_page_count_and_replay(source):
    first=seed(source); second=seed(source,first['registry'])
    assert first==second
    assert first['source']['independent_counts']==[{'tool':'pypdf','count':2},{'tool':'poppler-pdfinfo','count':2}]
    assert [p['pdf_page'] for p in first['pages']]==[1,2]
    assert all(p['label']['status']=='unknown' and p['label']['value'] is None for p in first['pages'])
    assert validate(first)['levels']['transcription']=={'represented':0,'partial':0,'unprocessed':2,'excluded':0}


def test_multicolumn_table_note_cross_page_and_edit(source):
    doc=authored(source)
    assert len(doc['links'])==2
    assert [r['key'] for r in doc['regions']]==['left','right','table','note','start','end']
    assert validate(doc)['denominator_regions']==6
    assert all(p['unaccounted_area_trillionths']==0 for p in validate(doc)['pages'])
    changed=copy.deepcopy(doc); changed['regions'][0]['uncertainty'].append('Changed observation')
    changed=reseal(changed)
    assert changed['regions'][0]['id']==doc['regions'][0]['id']
    assert changed['regions'][0]['revision']!=doc['regions'][0]['revision']
    assert validate(changed)['denominator_regions']==6
    changed['regions'].reverse(); changed=seal(changed)
    assert changed['reading_order']==doc['reading_order']; validate(changed)


def test_missing_page_fails(source):
    doc=seed(source); doc['pages'].pop()
    with pytest.raises(ValueError,match='missing PDF page'): validate(seal(doc))


def test_missing_regions_visible_as_page_area_gap(source):
    doc=seed(source); doc['regions']=[]; doc['reading_order']=[]
    report=validate(seal(doc))
    assert report['denominator_regions']==0
    assert all(p['gap_reason'] and p['unaccounted_area_trillionths']==10**12 for p in report['pages'])


def test_duplicate_region_rejected(source):
    doc=authored(source); doc['regions'].append(copy.deepcopy(doc['regions'][0]))
    with pytest.raises(ValueError,match='duplicate region'): validate(seal(doc))


def test_overlapping_inventory_rejected_context_not_counted(source):
    doc=authored(source); region=make_region(doc['registry'],'overlap',doc['pages'][0],[0,0,1000000,1000000])
    doc['regions'].append(region); doc['reading_order'].append(region['id'])
    with pytest.raises(ValueError,match='overlapping'): validate(seal(doc))
    doc['regions'][-1]['denominator_role']='context'; doc=reseal(doc)
    report=validate(doc); assert report['denominator_regions']==6; assert report['context_regions']==1
    assert report['levels']['transcription']['unprocessed']==6


def test_partial_never_represented_and_gaps_rejected(source):
    doc=seed(source); cov=doc['regions'][0]['coverage']['transcription']; cov['status']='partial'
    doc=reseal(doc); report=validate(doc)
    assert report['levels']['transcription']=={'represented':0,'partial':1,'unprocessed':1,'excluded':0}
    doc['regions'][0]['coverage']['transcription']['status']='represented'
    with pytest.raises(ValueError,match='represented'): validate(reseal(doc))
    doc['regions'][0]['coverage']['transcription'].update(status='represented',gap=False,reason=None)
    assert validate(reseal(doc))['levels']['transcription']['represented']==1


def test_exclusion_needs_exact_partition_boundary_and_human_claim(source):
    doc=authored(source); region=doc['regions'][0]
    cov=region['coverage']['transcription']; cov.update(status='excluded',gap=False,reason='Synthetic editorial boundary')
    with pytest.raises(ValueError,match='exclusion boundary'): validate(reseal(doc))
    decision=source[0]/'private/decision.json'; decision.write_text('{"synthetic_human_claim":true}\n')
    region=doc['regions'][0]; cov=region['coverage']['transcription']
    cov['boundary']={'source_revision':doc['source']['sha256'],'partition_hash':partition_hash(doc),
                     'region_id':region['id'],'box':region['box'],'level':'transcription',
                     'actor':'synthetic owner','actor_role':'human_owner','authorization':'Synthetic test claim only',
                     'rationale':'Synthetic editorial scope','decision':file_pin(source[0],'private/decision.json')}
    doc=reseal(doc); assert validate(doc,source[0])['levels']['transcription']['excluded']==1
    doc['regions'][1]['box'][2]=900000
    with pytest.raises(ValueError,match='exclusion boundary'): validate(reseal(doc))


@pytest.mark.parametrize('rotation,expected',[(0,[100000,200000,400000,600000]),
    (90,[400000,100000,800000,400000]),(180,[600000,400000,900000,800000]),
    (270,[200000,600000,600000,900000])])
def test_rotation_conversion(rotation,expected):
    assert display_box([100000,200000,400000,600000],rotation)==expected


def test_crop_media_nonzero_origin_units_and_roundtrip():
    page={'media_box':[0,0,300000000,400000000],'crop_box':[20000000,30000000,220000000,330000000],
          'effective_crop_box':[20000000,30000000,220000000,330000000],'rotation':90,
          'user_unit':{'numerator':2,'denominator':1}}
    assert pdf_to_box([40,90,100,270],page)==[100000,200000,400000,800000]
    assert box_to_pdf([100000,200000,400000,800000],page)==[40,90,100,270]
    assert display_size_points(page)==(600,400)
    assert effective_crop([0,0,100,200],[-10,20,90,250])==[0,20,90,200]
    with pytest.raises(ValueError,match='outside'): pdf_to_box([0,0,100,100],page)
    with pytest.raises(ValueError): effective_crop([0,0,10,10],[20,20,30,30])


def test_outward_rounding_encloses_fractional_coordinates():
    page={'effective_crop_box':[0,0,3000000,7000000]}
    box=pdf_to_box(['0.1','0.2','2.9','6.8'],page)
    assert box==[33333,28571,966667,971429]
    x0,y0,x1,y1=box_to_pdf(box,page)
    assert x0<=0.1 and y0<=0.2 and x1>=2.9 and y1>=6.8


@pytest.mark.parametrize('path',['../escape','private/a/../b','C:/file','private/a\\b','/abs','private/file.','private/NUL.txt','private/a//b'])
def test_safe_paths(tmp_path,path):
    with pytest.raises(ValueError,match='unsafe'): safe_artifact(tmp_path,path)


def test_registry_does_not_remap_changed_source(source):
    doc=seed(source); registry=copy.deepcopy(doc['registry']); registry['source_revision']='a'*64
    with pytest.raises(ValueError,match='source changed'): seed(source,registry)


def test_revision_and_registry_tampering(source):
    doc=seed(source); doc['regions'][0]['box'][2]=500000
    with pytest.raises(ValueError,match='revision hash'): validate(seal(doc))
    doc=seed(source); doc['registry']['entries'].append(copy.deepcopy(doc['registry']['entries'][0]))
    with pytest.raises(ValueError,match='duplicate registry'): validate(seal(doc))


def test_evidence_exact_text_render_pins_and_tampering(source):
    root=source[0]; doc=seed(source)
    ev=extract_evidence(doc,doc['regions'][0]['id'],root,'private/evidence')
    text=safe_artifact(root,ev['text']['path']).read_text(encoding='utf-8')
    assert 'Left column first' in text and 'Right column second' in text
    assert 'Table A' in text and 'Note A' in text
    assert ev['render_parameters']['width_pixels']==800
    assert ev['render_parameters']['height_pixels']==1200
    doc['evidence']=[ev]; doc=seal(doc); validate(doc,root)
    safe_artifact(root,ev['text']['path']).write_text('tampered',encoding='utf-8')
    with pytest.raises(ValueError,match='artifact hash'): validate(doc,root)


def test_region_crop_excludes_other_column(source):
    root=source[0]; doc=seed(source)
    region=doc['regions'][0]; region['box']=[0,0,500000,1000000]; doc=reseal(doc)
    ev=extract_evidence(doc,region['id'],root,'private/column-evidence')
    text=safe_artifact(root,ev['text']['path']).read_text(encoding='utf-8')
    assert 'Left column first' in text and 'Right column second' not in text
    assert ev['render_parameters']['width_pixels']==400


@pytest.mark.parametrize('rotation,expected',[(0,(400,600)),(90,(600,400)),(180,(400,600)),(270,(600,400))])
def test_pdf_crop_rotation_userunit_evidence(source,rotation,expected):
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject, NameObject, NumberObject
    root=source[0]; reader=PdfReader(root/'private/source/synthetic.pdf'); writer=PdfWriter()
    for page in reader.pages:
        page.cropbox=RectangleObject([20,30,220,330]); page[NameObject('/UserUnit')]=NumberObject(2); page.rotation=rotation
        writer.add_page(page)
    modified=root/'private/source/rotated.pdf'
    with modified.open('wb') as f: writer.write(f)
    doc=structural_inventory(root,'private/source/rotated.pdf','private/source/provenance.json','source:synthetic',file_pin(root,'private/source/rotated.pdf')['sha256'])
    ev=extract_evidence(doc,doc['regions'][0]['id'],root,'private/rotation-evidence',dpi=72)
    assert (ev['render_parameters']['width_pixels'],ev['render_parameters']['height_pixels'])==expected
    assert doc['pages'][0]['rotation']==rotation


def test_stale_evidence_rejected(source):
    root=source[0]; doc=seed(source); doc['evidence']=[extract_evidence(doc,doc['regions'][0]['id'],root,'private/ev')]; doc=seal(doc)
    doc['regions'][0]['uncertainty'].append('changed')
    with pytest.raises(ValueError,match='stale evidence'): validate(reseal(doc),root)


def test_order_and_link_fail_closed(source):
    doc=authored(source); doc['reading_order'].pop()
    with pytest.raises(ValueError,match='reading order'): validate(seal(doc))
    doc=authored(source); doc['links'][0]['to']='unknown'
    with pytest.raises(ValueError,match='dangling'): validate(seal(doc))


def test_independent_count_disagreement(source,monkeypatch):
    import wgc.sources.pdf as pdf
    real=pdf.subprocess.run
    def wrong(args,**kwargs):
        if args[0]=='pdfinfo' and '-v' not in args: return SimpleNamespace(stdout='Pages: 3\n',stderr='')
        return real(args,**kwargs)
    monkeypatch.setattr(pdf.subprocess,'run',wrong)
    with pytest.raises(ValueError,match='count disagreement'): seed(source)


def test_source_mutation_during_inspection(source,monkeypatch):
    import wgc.sources.pdf as pdf
    real=pdf.subprocess.run
    def mutate(args,**kwargs):
        result=real(args,**kwargs)
        if '-v' in args:
            path=source[0]/'private/source/synthetic.pdf'; path.write_bytes(path.read_bytes()+b'\n% mutation')
        return result
    monkeypatch.setattr(pdf.subprocess,'run',mutate)
    with pytest.raises(ValueError,match='changed during'): seed(source)


def test_schema_rejects_floats_and_unknown_fields(source):
    doc=seed(source); doc['unknown_field']=True
    with pytest.raises(ValueError,match='unexpected property'): validate(seal(doc))
    doc=seed(source); doc['regions'][0]['box'][0]=0.5
    with pytest.raises(ValueError,match='integer'): validate(doc)


def test_cli_two_page_evidence_and_immutable_output(source,monkeypatch,capsys):
    import sys
    from wgc.sources.__main__ import main
    root,sha=source
    monkeypatch.setattr(sys,'argv',['wgc.sources','--root',str(root),'inventory','--pdf','private/source/synthetic.pdf','--provenance','private/source/provenance.json','--source-id','source:synthetic','--sha256',sha,'--output','private/cli-inventory'])
    assert main()==0
    assert main()==1
    monkeypatch.setattr(sys,'argv',['wgc.sources','--root',str(root),'evidence','--inventory','private/cli-inventory/inventory.json','--pages','1','2','--output','private/cli-evidence'])
    assert main()==0
    from wgc.contracts.source import load_json
    doc=load_json(root/'private/cli-evidence/inventory.json')
    assert len(doc['evidence'])==2
    assert validate(doc,root)['levels']['transcription']['represented']==0


def test_embedded_label_does_not_verify_printed_label(source):
    from pypdf import PdfReader,PdfWriter
    from pypdf.constants import PageLabelStyle
    root,sha=source; writer=PdfWriter(); reader=PdfReader(root/'private/source/synthetic.pdf')
    for page in reader.pages: writer.add_page(page)
    writer.set_page_label(0,1,style=PageLabelStyle.LOWERCASE_ROMAN)
    with (root/'private/source/labeled.pdf').open('wb') as f: writer.write(f)
    doc=structural_inventory(root,'private/source/labeled.pdf','private/source/provenance.json','source:synthetic',file_pin(root,'private/source/labeled.pdf')['sha256'])
    assert [p['label']['value'] for p in doc['pages']]==['i','ii']
    assert all(p['label']['status']=='embedded_unverified' for p in doc['pages'])
    doc['pages'][0]['label']['status']='verified'
    with pytest.raises(ValueError,match='printed label needs'): validate(reseal(doc))


def test_duplicate_context_geometry_never_inflates_denominator(source):
    doc=authored(source)
    for key in ['context-a','context-b']:
        r=make_region(doc['registry'],key,doc['pages'][0],doc['regions'][0]['box'],role='context')
        doc['regions'].append(r); doc['reading_order'].append(r['id'])
    report=validate(seal(doc)); assert report['context_regions']==2; assert report['denominator_regions']==6


def test_linked_artifact_is_rejected(tmp_path,monkeypatch):
    target=tmp_path/'private'/'linked'/'file.json'
    real=Path.is_symlink
    monkeypatch.setattr(Path,'is_symlink',lambda p: p==target.parent or real(p))
    with pytest.raises(ValueError,match='linked'): safe_artifact(tmp_path,'private/linked/file.json')
