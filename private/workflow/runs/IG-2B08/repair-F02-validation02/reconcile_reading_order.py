"""Preserve reviewed order after complete independent evidence generation."""
import copy
import sys
from build_inventory import (ROOT, load, write, pin, metadata, baseline,
                             selected_regions, author_document, seal, validate, REPO)


def run(name):
    assert name in ('author', 'final-verified', 'replay-1', 'replay-2')
    path = ROOT/'author-inventory.json' if name == 'author' else ROOT/name/'inventory.json'
    old = load(path)
    snapshot = ROOT/f'pre-order-{name}.json'
    assert not snapshot.exists()
    snapshot.write_bytes(path.read_bytes())
    base, _ = baseline()
    registry = load(ROOT/'author-registry.json')
    regions = selected_regions(base, registry)
    fresh = author_document(base, registry, regions)
    if name != 'author':
        fresh_ids = {r['id'] for r in regions}
        generated = [e for e in old['evidence'] if e['region_id'] in fresh_ids]
        assert len(generated) == len(regions) == 269
        assert {e['region_id'] for e in generated} == fresh_ids
        assert old['evidence'][:len(base['evidence'])] == base['evidence']
        fresh['evidence'].extend(copy.deepcopy(generated))
    fresh = seal(fresh)
    # Keep the strict product invariant: this operation changes order and its
    # root canonical revision only, never source/region/evidence/registry data.
    assert set(old) == set(fresh)
    for field in old:
        if field not in ('reading_order', 'revision'):
            assert old[field] == fresh[field], field
    validate(fresh, REPO if name != 'author' else None)
    write(path, fresh)
    report = {**metadata(), 'name':name,
              'summary':'Reconstructed independently from accepted baseline and identical author registry/selections; preserved reviewed reading order and complete generated evidence.',
              'prior_inventory_snapshot':pin(snapshot), 'current_inventory':pin(path),
              'only_order_and_root_revision_changed':True,
              'all_region_and_evidence_objects_unchanged':True, 'exit_code':0}
    write(ROOT/f'order-reconciliation-{name}.json', report)
    print(f'{name}: reading order preserved; all region/evidence objects unchanged.')


if __name__ == '__main__':
    run(sys.argv[1])
