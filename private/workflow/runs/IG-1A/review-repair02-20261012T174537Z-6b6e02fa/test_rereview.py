"""Independent bounded repair checks; generated evidence stays in this review."""
import copy
import json
from pathlib import Path

import pytest
from wgc.contracts.source import ContractError, load_json, seal_record, validate_bundle

HERE = Path(__file__).parent
FIX = Path('tests/contracts/fixtures')


def get(b, name):
    selected = next(r for r in b['records'] if r['record_type'] == 'snapshot')['data']['selected']
    revision = next((s['revision_id'] for s in selected if s['id'] == 'synthetic:' + name), None)
    return next(r for r in b['records'] if r['id'] == 'synthetic:' + name and (revision is None or r['revision_id'] == revision))


def ref(r, mode='historical', aspect=None):
    result = {'mode': mode, 'id': r['id'], 'record_type': r['record_type']}
    if mode == 'historical':
        result['revision_id'] = r['revision_id']
    if aspect:
        result['aspect_id'] = aspect
    return result


def change(b, name, fn, retain=False):
    old = get(b, name)
    new = copy.deepcopy(old)
    fn(new)
    new = seal_record(new)
    if retain:
        b['records'].append(new)
    else:
        b['records'][b['records'].index(old)] = new
    snapshot = next(r for r in b['records'] if r['record_type'] == 'snapshot')
    for s in snapshot['data']['selected']:
        if s['id'] == old['id']:
            s.update({k: new[k] for k in ('id', 'record_type', 'revision_id', 'content_hash')})
    b['records'][b['records'].index(snapshot)] = seal_record(snapshot)
    return new


def save(name, b):
    (HERE / (name + '.json')).write_text(json.dumps(b, indent=2) + '\n', encoding='utf-8')


@pytest.mark.parametrize('mode', ['active', 'historical'])
@pytest.mark.parametrize('family', ['source', 'region1', 'profile', 'run', 'review', 'identities', 'binding', 'coverage1', 'gap'])
def test_f1_metadata_and_gap_are_not_content(mode, family):
    b = load_json(FIX / 'valid-source.json')
    change(b, 'coverage0', lambda r: r['data'].update(target_refs=[ref(get(b, 'clause'), mode), ref(get(b, family), mode)]))
    save('f1-' + family + '-' + mode, b)
    with pytest.raises(ContractError):
        validate_bundle(b)


@pytest.mark.parametrize('mode', ['active', 'historical'])
@pytest.mark.parametrize('family', ['clause', 'evidence', 'history-link'])
def test_f1_each_source_content_family_passes(mode, family):
    b = load_json(FIX / 'valid-source.json')
    change(b, 'coverage0', lambda r: r['data'].update(target_refs=[ref(get(b, family), mode)]))
    report = validate_bundle(b)
    assert report['coverage_inventory_region_counts']['transcription']['represented'] == 2
    assert report['semantic_acceptance_granted'] is False


@pytest.mark.parametrize('status', ['partial', 'unprocessed'])
def test_f1_partial_and_unprocessed_keep_gap_accounting(status):
    b = load_json(FIX / 'valid-source.json')
    change(b, 'coverage0', lambda r: r['data'].update(status=status, target_refs=[], gap_refs=[ref(get(b, 'gap'), 'active')]))
    report = validate_bundle(b)
    assert report['coverage_inventory_region_counts']['transcription'][status] == 1
    assert report['coverage_inventory_region_counts']['transcription']['represented'] == 1
    assert report['semantic_acceptance_granted'] is False


@pytest.mark.parametrize('variant', ['missing-region-target', 'wrong-kind', 'unknown-basis', 'rejected', 'no-authorization', 'no-decision-artifact'])
def test_f2_other_invalid_decisions(variant):
    b = load_json(FIX / 'valid-exact-coverage-exclusion.json')
    def edit(r):
        d = r['data']
        if variant == 'missing-region-target':
            d['targets'] = [ref(get(b, 'region2'))]
        elif variant == 'wrong-kind':
            d['kind'] = 'technical'
        elif variant == 'unknown-basis':
            d['basis_completeness'] = 'unknown'
        elif variant == 'rejected':
            d['decision'] = 'rejected'
        elif variant == 'no-authorization':
            d['authorization'] = None
        else:
            d['decision_artifact'] = None
    decision = change(b, 'boundary-review', edit, retain=True)
    change(b, 'coverage0', lambda r: r['data'].update(scope_decision_ref=ref(decision)))
    save('f2-' + variant, b)
    with pytest.raises(ContractError):
        validate_bundle(b)


def aspect_inventory_boundary(changed_inventory=False):
    b = load_json(FIX / 'valid-exact-coverage-exclusion.json')
    # Give the inventory an addressable aspect without changing the record family.
    aspect = copy.deepcopy(get(b, 'clause')['data']['aspects'][0])
    inv = change(b, 'inventory', lambda r: r['data'].update(aspects=[aspect]), retain=True)
    pin = ref(inv, aspect='lit-condition')
    def edit_review(r):
        r['data']['coverage_boundary']['inventory_ref'] = pin
        r['data']['basis'] = [pin if t['id'] == inv['id'] else t for t in r['data']['basis']]
    decision = change(b, 'boundary-review', edit_review, retain=True)
    change(b, 'coverage0', lambda r: r['data'].update(inventory_ref=pin, scope_decision_ref=ref(decision)))
    if changed_inventory:
        change(b, 'inventory', lambda r: r['data']['description']['description']['value'].update(text='The inventory partition boundary changed; the aspect did not.'), retain=True)
    return b


@pytest.mark.parametrize('changed_inventory', [False, True])
def test_f2_inventory_basis_must_be_a_full_record(changed_inventory):
    b = aspect_inventory_boundary(changed_inventory)
    name = 'f2-aspect-inventory-stale-boundary' if changed_inventory else 'f2-aspect-inventory-basis'
    save(name, b)
    # Exact full-record inventory basis is an explicit repair contract requirement.
    with pytest.raises(ContractError):
        validate_bundle(b)


@pytest.mark.parametrize('requirement', ['required', 'conditional'])
@pytest.mark.parametrize('endpoint', ['from_ref', 'target_ref'])
def test_f3_superseded_same_aspect_endpoints_do_not_count(requirement, endpoint):
    b = load_json(FIX / 'valid-source.json')
    old = copy.deepcopy(get(b, 'clause'))
    change(b, 'clause', lambda r: r['data']['description']['description']['value'].update(text='New container, unchanged aspects.'), retain=True)
    def edit(r):
        r['data'].update(requirement=requirement, relation_type='procedure_use', from_ref=ref(get(b, 'clause')), target_ref=ref(get(b, 'procedure')))
        r['data'][endpoint] = ref(old, aspect='lit-condition')
    change(b, 'history-link', edit)
    save('f3-' + requirement + '-' + endpoint, b)
    with pytest.raises(ContractError, match='selected revision'):
        validate_bundle(b)


def test_f3_unresolved_candidates_do_not_activate_history():
    b = load_json(FIX / 'valid-source.json')
    change(b, 'history-link', lambda r: r['data'].update(requirement='conditional', relation_type='procedure_use', target_status='unresolved', target_ref=None, raw_locator='An unresolved procedure locator', gap_refs=[ref(get(b, 'gap'), 'active')], candidate_refs=[ref(get(b, 'retired-concept'))]))
    report = validate_bundle(b)
    assert 'synthetic:history-link' in report['executable']['source_blocker_ids']
    assert report['semantic_acceptance_granted'] is False


@pytest.mark.parametrize('case', load_json(FIX / 'catalog.json')['cases'], ids=lambda c: c['file'])
def test_frozen_catalogue_contract_expectations(case):
    b = load_json(FIX / case['file'])
    if not case['valid']:
        with pytest.raises(ContractError, match=case['error_contains']):
            validate_bundle(b)
    else:
        r = validate_bundle(b)
        e = case['report']
        assert r['semantic_acceptance_granted'] is False
        if 'execution' in e:
            assert r['executable']['status'] == e['execution']
        if 'review_freshness' in e:
            assert r['reviews'][0]['freshness'] == e['review_freshness']
        for field, status in [('transcription_represented', 'represented'), ('transcription_excluded', 'excluded')]:
            if field in e:
                assert r['coverage_inventory_region_counts']['transcription'][status] == e[field]
