"""Independent re-read of delivered source regions and fictional example."""
from prepare import P, I, M, load, write, now
import hashlib
import pdfplumber
from PIL import Image

scope = load(I / 'scope.json')
helper = load(I / 'helper-regions.json')
assert [r['region_id'] for r in helper['regions'] if r['role'] == 'core'] == scope['reading_order']
assert scope['pdf_pages'] == list(range(31,38))
assert scope['core_start']['core_bbox'] == [315,309.4529,567,744]
assert scope['core_end']['core_bbox'] == [45,45,297,392.6396]
with pdfplumber.open(P / 'source/original-pdf-20261008-01.pdf') as pdf:
    for region in helper['regions']:
        page = pdf.pages[region['pdf_page'] - 1]
        text = page.crop(tuple(region['pdf_bbox'])).extract_text(x_tolerance=2,y_tolerance=3) or ''
        assert text == region['text'], region['region_id']
        with Image.open(P / f"inputs/v1/pages/pdf-{region['pdf_page']}.png") as full, Image.open(P / region['image']) as crop:
            expected = full.crop(region['pixel_bbox_on_full_page'])
            assert expected.size == crop.size and expected.tobytes() == crop.tobytes(), region['region_id']

example = load(P / 'formats/synthetic-example-v1.json')
assert hashlib.sha256(example['sources'][0]['embedded_utf8_text'].encode('utf-8')).hexdigest() == example['sources'][0]['sha256']
objects = [*example['rules'], *example['nodes']]
all_records = [*objects, *example['evidence'], *example['dependencies'], *example['gaps']]
ids = [r['id'] for r in all_records]
assert len(ids) == len(set(ids))
entity_ids = {r['id'] for r in objects}
evidence_ids = {r['id'] for r in example['evidence']}
gap_ids = {r['id'] for r in example['gaps']}
for dependency in example['dependencies']:
    assert dependency['from'] in entity_ids
    assert dependency['to'] in entity_ids or (dependency['to'] is None and dependency['target_candidate'] and dependency['gap_ids'])

def visit(value):
    if isinstance(value, dict):
        if 'state' in value:
            assert set(value) == {'state','value','evidence_ids','reason','gap_ids'}
            assert value['state'] in {'known','established_absent','unknown','not_applicable'}
            if value['state'] == 'unknown':
                assert value['value'] is None and value['reason'] and value['gap_ids']
            if value['state'] == 'established_absent':
                assert value['value'] in (None, []) and value['evidence_ids'] and value['reason']
        if 'review_status' in value:
            assert value['review_status'] == 'unreviewed'
        if 'evidence_ids' in value:
            assert set(value['evidence_ids']) <= evidence_ids
        if 'gap_ids' in value:
            assert set(value['gap_ids']) <= gap_ids
        for child in value.values():
            visit(child)
    elif isinstance(value, list):
        for child in value:
            visit(child)
visit(example)
write(M / 'source-validation.json', {'recorded_at_utc':now(),'text_regions_rederived_from_pdf':16,'crops_pixel_equal_to_full_renders':16,'core_boundaries_match_source_v1':True,'reading_order_verified':True,'synthetic_json_parses':True,'synthetic_source_hash_valid':True,'synthetic_ids_and_references_valid':True,'synthetic_value_states_valid':True,'model_response_created':False})
print('Source validation passed: 16 text/crop regions; bounds, order and synthetic example')
