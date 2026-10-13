"""New independent cases for whole inventory pins and generic aspect review."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest
from wgc.contracts.source import ContractError, load_json, seal_record, validate_bundle

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('final_review_helpers', HERE / 'test_rereview.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
get, ref, change = helpers.get, helpers.ref, helpers.change
FIX = Path('tests/contracts/fixtures')


def save(name, bundle):
    (HERE / (name + '.json')).write_text(json.dumps(bundle, indent=2) + '\n', encoding='utf-8')


@pytest.mark.parametrize('field', ['coverage', 'boundary'])
@pytest.mark.parametrize('retained', [False, True])
def test_inventory_aspect_shape_rejects_current_and_retained(field, retained):
    b = load_json(FIX / 'valid-exclusion-full-inventory-with-aspect.json')
    name = 'coverage0' if field == 'coverage' else 'boundary-review'
    def edit(r):
        d = r['data'] if field == 'coverage' else r['data']['coverage_boundary']
        d['inventory_ref']['aspect_id'] = 'lit-condition'
    if retained:
        old = copy.deepcopy(get(b, name))
        edit(old)
        b['records'].append(seal_record(old))
    else:
        change(b, name, edit, retain=True)
    save('whole-pin-' + field + ('-retained' if retained else '-current'), b)
    with pytest.raises(ContractError, match='schema'):
        validate_bundle(b)


@pytest.mark.parametrize('change_aspect', [False, True])
def test_generic_aspect_basis_still_has_scoped_freshness(change_aspect):
    b = load_json(FIX / 'valid-source.json')
    aspect = copy.deepcopy(get(b, 'clause')['data']['aspects'][0])
    inventory = change(b, 'inventory', lambda r: r['data'].update(aspects=[aspect]), retain=True)
    change(b, 'review', lambda r: r['data'].update(basis=[ref(inventory, aspect='lit-condition')]))
    def edit(r):
        if change_aspect:
            r['data']['aspects'][0]['statement']['value']['text'] = 'The inventory aspect itself changed.'
        else:
            r['data']['description']['description']['value']['text'] = 'Other inventory text changed, outside the explicitly scoped ordinary review basis.'
    change(b, 'inventory', edit, retain=True)
    save('ordinary-aspect-basis-' + ('changed' if change_aspect else 'unrelated-change'), b)
    report = validate_bundle(b)
    assert report['reviews'][0]['freshness'] == ('stale' if change_aspect else 'current')
    assert report['semantic_acceptance_granted'] is False


def test_full_record_exclusion_accepts_inventory_with_aspects():
    b = load_json(FIX / 'valid-exclusion-full-inventory-with-aspect.json')
    assert get(b, 'inventory')['data']['aspects']
    report = validate_bundle(b)
    boundary = next(r for r in report['reviews'] if r['id'] == 'synthetic:boundary-review')
    assert boundary['freshness'] == 'current'
    assert report['coverage_inventory_region_counts']['transcription']['excluded'] == 1
    assert report['semantic_acceptance_granted'] is False


def test_whole_inventory_revision_change_invalidates_exclusion():
    b = load_json(FIX / 'valid-exclusion-full-inventory-with-aspect.json')
    before = get(b, 'inventory')['data']['aspects'][0]['aspect_hash']
    change(b, 'inventory', lambda r: r['data']['description']['description']['value'].update(text='The whole inventory boundary changed.'), retain=True)
    assert get(b, 'inventory')['data']['aspects'][0]['aspect_hash'] == before
    save('whole-inventory-changed-unchanged-aspect', b)
    with pytest.raises(ContractError, match='exact inventory/region/level boundary'):
        validate_bundle(b)


def test_saved_original_f2_reproductions_reject_without_modification():
    original = Path('private/workflow/runs/IG-1A/review-repair01-20261012T172231Z-9f8db531')
    results = []
    for name in ['f2-aspect-inventory-basis', 'f2-aspect-inventory-stale-boundary']:
        with pytest.raises(ContractError, match='schema') as caught:
            validate_bundle(load_json(original / (name + '.json')))
        results.append({'case': name, 'actual': 'rejected', 'error': str(caught.value)})
    (HERE / 'original-f2-disposition.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
