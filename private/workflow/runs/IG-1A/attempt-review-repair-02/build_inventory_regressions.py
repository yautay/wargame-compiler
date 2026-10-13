"""Whole-inventory boundary oracles for F2-R1, without changing generic aspect review."""
import copy
import json
from pathlib import Path
from build_regressions import (
    OUT, catalog, exclusion_case, get, historical, replace, save, seal,
)

REVIEW = Path('private/workflow/runs/IG-1A/review-repair01-20261012T172231Z-9f8db531')
for original, name in [
    ('f2-aspect-inventory-basis.json', 'invalid-exclusion-inventory-aspect'),
    ('f2-aspect-inventory-stale-boundary.json', 'invalid-exclusion-inventory-aspect-stale')]:
    bundle = json.loads((REVIEW / original).read_text())
    save(name, bundle, False,
         'Inventory revision pins for coverage/exclusion must be whole records; an aspect cannot stand for the partition.',
         'Independent F2-R1 counterexample; README full-record inventory basis and whole revision freshness.', error='schema')


def selected(bundle, key):
    snapshot = get(bundle, 'snapshot')
    entry = next(e for e in snapshot['data']['selected'] if e['id'] == 'synthetic:' + key)
    return next(r for r in bundle['records'] if r['id'] == entry['id'] and r['revision_id'] == entry['revision_id'])


def change_selected(bundle, key, mutation):
    old = selected(bundle, key)
    new = copy.deepcopy(old)
    mutation(new)
    new = seal(new)
    bundle['records'].append(new)
    snapshot = get(bundle, 'snapshot')
    entry = next(e for e in snapshot['data']['selected'] if e['id'] == old['id'])
    entry.update({k: new[k] for k in ['id', 'record_type', 'revision_id', 'content_hash']})
    bundle['records'][bundle['records'].index(snapshot)] = seal(snapshot)
    return new


b = exclusion_case()
aspect = copy.deepcopy(get(b, 'clause')['data']['aspects'][0])
inventory = change_selected(b, 'inventory', lambda r: r['data']['aspects'].append(aspect))
decision = change_selected(b, 'boundary-review', lambda r: r['data'].update(
    coverage_boundary={**r['data']['coverage_boundary'], 'inventory_ref': historical(inventory)},
    basis=[historical(inventory), r['data']['basis'][1]]))
replace(b, 'coverage0', lambda r: r['data'].update(inventory_ref=historical(inventory),
    scope_decision_ref=historical(decision)))
save('valid-exclusion-full-inventory-with-aspect', b, True,
     'An inventory may contain aspects while its exclusion decision pins the whole record.',
     'F2-R1 preserves aspects as content but requires a full-record boundary basis.',
     {'transcription_represented': 1, 'transcription_excluded': 1})

stale = copy.deepcopy(b)
change_selected(stale, 'inventory', lambda r: r['data']['description']['description']['value'].update(
    text='Changed fictional inventory partition; its existing aspect is unchanged.'))
save('invalid-exclusion-full-inventory-changed', stale, False,
     'A changed whole inventory revision invalidates its old exclusion even when the reviewed aspect hash is unchanged.',
     'F2-R1 whole-revision freshness; no scope transfer through stable aspects.',
     error='exact inventory/region/level boundary')

partial_basis = copy.deepcopy(b)
old_basis = selected(partial_basis, 'boundary-review')['data']['basis'][0]
changed = change_selected(partial_basis, 'boundary-review', lambda r: r['data'].update(
    basis=[{**old_basis, 'aspect_id': 'lit-condition'}, r['data']['basis'][1]]))
replace(partial_basis, 'coverage0', lambda r: r['data'].update(scope_decision_ref=historical(changed)))
save('invalid-exclusion-aspect-only-review-basis', partial_basis, False,
     'Whole boundary pins cannot be authorized by an aspect-only inventory basis.',
     'F2-R1 requires the exact full-record inventory reference in the decision basis.',
     error='exact inventory/region/level boundary')

boundary_only = copy.deepcopy(b)
inventory_ref = selected(boundary_only, 'boundary-review')['data']['coverage_boundary']['inventory_ref']
changed = change_selected(boundary_only, 'boundary-review', lambda r: r['data']['coverage_boundary'].update(
    inventory_ref={**inventory_ref, 'aspect_id': 'lit-condition'}))
replace(boundary_only, 'coverage0', lambda r: r['data'].update(scope_decision_ref=historical(changed)))
save('invalid-exclusion-aspect-only-boundary-pin', boundary_only, False,
     'Boundary metadata independently forbids an aspect pin even when coverage and basis use whole records.',
     'F2-R1 full-record boundary shape.', error='schema')

(OUT / 'catalog.json').write_text(json.dumps({'format': 'wgc-synthetic-oracles-1', 'cases': catalog}, indent=2) + '\n', encoding='utf-8')
print('Frozen', len(catalog), 'oracles including whole-inventory regressions.')
