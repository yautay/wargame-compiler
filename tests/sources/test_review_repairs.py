"""Resealed candidate revisions exercise freshness, not malformed hashes."""
from math import ceil
import pytest
from tests.sources.test_inventory import source, seed, authored, reseal
from wgc.sources.inventory import seal, validate, partition_hash, file_pin, page_basis_hash
from wgc.sources.pdf import extract_evidence, structural_inventory


def evidenced(source):
    doc=seed(source)
    doc['evidence']=[extract_evidence(doc,r['id'],source[0],f'private/e-{i}') for i,r in enumerate(doc['regions'])]
    return seal(doc)


@pytest.mark.parametrize('field',['crop_box','effective_crop_box','rotation','user_unit'])
@pytest.mark.parametrize('root_check',[False,True])
def test_page_geometry_change_stales_evidence(source,field,root_check):
    doc=evidenced(source); page=doc['pages'][0]
    if field in ('crop_box','effective_crop_box'):
        page['crop_box'][0]=page['effective_crop_box'][0]=10_000_000
    elif field=='rotation': page['rotation']=90
    else: page['user_unit']['numerator']=2
    doc=reseal(doc)
    with pytest.raises(ValueError,match='stale .* (geometry|basis)|stale page geometry'):
        validate(doc,source[0] if root_check else None)


def test_resealing_geometry_and_evidence_basis_cannot_forge_source(source):
    doc=evidenced(source); page=doc['pages'][0]; page['rotation']=180
    doc['evidence'][0]['page_basis_hash']=page_basis_hash(page)
    with pytest.raises(ValueError,match='stale page geometry/source structure basis'):
        validate(reseal(doc),source[0])


def test_dpi_must_match_actual_physical_crop(source):
    doc=evidenced(source); doc['evidence'][0]['render_parameters']['dpi']=72
    with pytest.raises(ValueError,match='DPI/geometry'): validate(seal(doc),source[0])


def test_printed_label_requires_same_current_physical_page(source):
    doc=evidenced(source)
    page=doc['pages'][0]; page['label'].update(status='verified',value='2',evidence=doc['evidence'][1]['id'])
    with pytest.raises(ValueError,match='another physical page'): validate(reseal(doc),source[0])
    doc['pages'][0]['label']['evidence']=doc['evidence'][0]['id']
    validate(reseal(doc),source[0])  # Association only; this does not verify the glyph.


def exclusion(source):
    doc=authored(source); r=doc['regions'][0]
    path=source[0]/'private/decision.json'; path.write_text('{"synthetic":true}\n')
    r['coverage']['transcription'].update(status='excluded',gap=False,reason='Synthetic scope only',boundary={
        'source_revision':doc['source']['sha256'],'partition_hash':partition_hash(doc),
        'region_id':r['id'],'box':r['box'],'level':'transcription','actor':'Synthetic human claim',
        'actor_role':'human_owner','authorization':'Synthetic test, not authenticated',
        'rationale':'Synthetic boundary','decision':file_pin(source[0],'private/decision.json')})
    doc=reseal(doc); report=validate(doc,source[0])
    assert report['exclusion_claims'][0]['source_ig_review_freshness']=='unknown'
    assert report['exclusion_claims'][0]['human_authority']=='unverified'
    return doc


@pytest.mark.parametrize('change',['key','kind','uncertainty','registry','source','page','context','order','links'])
def test_exclusion_pins_whole_author_scope(source,change):
    doc=exclusion(source); r=doc['regions'][0]
    if change=='key':
        old=r['key']; r['key']='revised-key'
        next(e for e in doc['registry']['entries'] if e['kind']=='region' and e['key']==old)['key']=r['key']
    elif change=='kind': r['kind']='diagram'
    elif change=='uncertainty': r['uncertainty'].append('New source observation')
    elif change=='registry':
        next(e for e in doc['registry']['entries'] if e['kind']=='region' and e['key'].endswith('unprocessed-placeholder'))['key']='retired-revised'
    elif change=='source': doc['source']['id']=doc['registry']['source_id']='source:renamed'
    elif change=='page':
        doc['pages'][0]['pdf_page'],doc['pages'][1]['pdf_page']=2,1
    elif change=='context': doc['regions'][1]['denominator_role']='context'
    elif change=='order': doc['reading_order'].reverse()
    else: doc['links'][0]['reason']='Revised note attribution'
    with pytest.raises(ValueError,match='exclusion boundary|identity remapping'): validate(reseal(doc))


def test_all_coverage_fields_are_outside_scope_hash_to_avoid_cycles(source):
    doc=exclusion(source); basis=partition_hash(doc)
    doc['regions'][0]['coverage']['transcription']['reason']='Revised claim rationale'
    assert partition_hash(reseal(doc))==basis
    # Sidecar scope validity never replaces the exact source-IG whole-record decision.
    assert validate(reseal(doc))['exclusion_claims'][0]['source_ig_review_freshness']=='unknown'


def test_consistent_false_page_count_fails_against_actual_pdf(source):
    doc=seed(source); doc['source']['page_count']=1
    for c in doc['source']['independent_counts']: c['count']=1
    doc['pages']=doc['pages'][:1]; doc['regions']=doc['regions'][:1]; doc['reading_order']=doc['reading_order'][:1]
    with pytest.raises(ValueError,match='missing PDF page/source structure count'): validate(seal(doc),source[0])


def test_physical_addresses_cannot_move_under_persisted_identities(source):
    doc=seed(source); doc['pages'][0]['pdf_page'],doc['pages'][1]['pdf_page']=2,1
    with pytest.raises(ValueError,match='identity remapping'): validate(reseal(doc),source[0])


def test_reordering_array_keeps_addresses_and_identity(source):
    doc=seed(source); doc['pages'].reverse()
    assert validate(seal(doc),source[0])['source_structure_verification']=='verified'
    assert validate(seal(doc))['source_structure_verification']=='unverified'
    replay=seed(source,doc['registry'])
    assert {p['id']:p['pdf_page'] for p in replay['pages']}=={p['id']:p['pdf_page'] for p in doc['pages']}


@pytest.mark.parametrize('rotation',[0,90,180,270])
@pytest.mark.parametrize('dpi',[72,144])
def test_fractional_units_origins_rotations_and_rounding_oracle(source,rotation,dpi):
    from pypdf import PdfReader,PdfWriter
    from pypdf.generic import RectangleObject, NameObject, FloatObject
    root=source[0]; reader=PdfReader(root/'private/source/synthetic.pdf'); writer=PdfWriter()
    for page in reader.pages:
        page.mediabox=RectangleObject([-20,-30,400,600])
        page.cropbox=RectangleObject([13.25,27.5,213.75,328.25])
        page[NameObject('/UserUnit')]=FloatObject('1.5'); page.rotation=rotation; writer.add_page(page)
    with (root/'private/source/fractional.pdf').open('wb') as f: writer.write(f)
    doc=structural_inventory(root,'private/source/fractional.pdf','private/source/provenance.json',
                             'source:synthetic',file_pin(root,'private/source/fractional.pdf')['sha256'])
    # Independent physical oracle: crop widths 200.5 * 1.5 and 300.75 * 1.5 points.
    unrotated=(ceil(300.75*dpi/72),ceil(451.125*dpi/72))
    expected=unrotated[::-1] if rotation in (90,270) else unrotated
    ev=extract_evidence(doc,doc['regions'][0]['id'],root,'private/fractional-evidence',dpi=dpi)
    assert (ev['render_parameters']['width_pixels'],ev['render_parameters']['height_pixels'])==expected
    doc['evidence']=[ev]; validate(seal(doc),root)
