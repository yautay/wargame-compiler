"""Deterministic metadata-only repair. Copies canonical bytes; never allocates IDs."""
import argparse
import copy
from importlib.machinery import SourceFileLoader
import json
from pathlib import Path

u = SourceFileLoader('repair_common', str(Path(__file__).with_name('repair-common.py'))).load_module()
PRODUCTS = ['authored/inventory.json', 'authored/identity-registry.json',
            'final-verified/inventory.json', 'final-verified/identity-registry.json',
            'final-verified/coverage.json', 'author-specifications-final.json',
            'component-observations.json', 'region-ledger-final.json', 'visual-inspection.json']

def logical_pin(name, data):
    return dict(path=(u.A / name).relative_to(u.R).as_posix(), bytes=len(data),
                sha256=u.hashlib.sha256(data).hexdigest())

def generate():
    catalogue = {p['path']: p for p in u.load(u.P / 'frozen-base-pins.json')['frozen_pins']}
    inputs = ['author-specifications-final.json','component-observations.json',
              'region-ledger-final.json','visual-inspection.json']
    for name in inputs + PRODUCTS[:5]:
        u.verify(catalogue[(u.D / name).relative_to(u.R).as_posix()])
    u.verify(u.load(u.A / 'repair-plan.json')['source_observations'])
    output = {n: (u.D / n).read_bytes() for n in PRODUCTS[:5]}
    original_spec = u.load(u.D / 'author-specifications-final.json')
    # Proven identical serializer: no unrelated string or formatting normalization.
    assert u.encoded(original_spec) == (u.D / 'author-specifications-final.json').read_bytes()
    specs = copy.deepcopy(original_spec)
    by_key = {s['key']: s for s in specs['specifications']}
    assert len(by_key) == 141
    for key,t in u.TARGETS.items():
        assert by_key[key]['components'] == t['before_components']
        by_key[key]['components'] = t['required_after_components']
    output['author-specifications-final.json'] = u.encoded(specs)
    original_observations = (u.D / 'component-observations.json').read_text(encoding='utf-8')
    observations = u.load(u.D / 'component-observations.json')
    assert all(k not in observations['corrections_after_enlargement'] for k in u.TARGETS)
    # Insert only new map members and provenance; preserve the seven original lines verbatim.
    marker = '\n  },\n  "limits"'
    assert original_observations.count(marker) == 1
    additions = ''.join(',\n    ' + json.dumps(k) + ': ' + json.dumps(t['required_after_components'], ensure_ascii=False)
                        for k,t in u.TARGETS.items())
    text = original_observations.replace(marker, additions + marker)
    provenance = dict(actor=u.CFG['actor'], original_basis_attribution=u.pin(u.D / 'component-observations.json'),
                      original_basis_policy='The unchanged basis and seven existing corrections are original executor observations, not new all-page viewing.',
                      new_observations=u.pin(u.A / 'source-observations.json'),
                      effective_components_rule=u.RULE, scope=u.pin(u.P / 'repair-scope.json'))
    assert text.endswith('\n}\n')
    text = text[:-3] + ',\n  "repair_provenance": ' + json.dumps(provenance, ensure_ascii=False, indent=2).replace('\n','\n  ') + '\n}\n'
    output['component-observations.json'] = text.encode('utf-8')
    current_observations = json.loads(text)
    effective = {s['key']: current_observations['corrections_after_enlargement'].get(s['key'], s['components'])
                 for s in specs['specifications']}
    ledger = u.load(u.D / 'region-ledger-final.json')
    assert u.encoded(ledger) == (u.D / 'region-ledger-final.json').read_bytes()
    for row in ledger['regions']:
        key = row['region']['key']
        if key in u.TARGETS:
            t = u.TARGETS[key]
            assert row['region'] == t['region'] and row['components'] == t['before_components']
            row['components'] = t['required_after_components']
        assert row['components'] == effective[key], key
    ledger['inventory_pin'] = logical_pin('final-verified/inventory.json', output['final-verified/inventory.json'])
    ledger['registry_pin'] = logical_pin('final-verified/identity-registry.json', output['final-verified/identity-registry.json'])
    ledger['repair_attribution'] = dict(actor=u.CFG['actor'], original_ledger=u.pin(u.D / 'region-ledger-final.json'),
                                      original_visual_inspection=u.pin(u.D / 'visual-inspection.json'),
                                      original_visual_status_policy='Per-region visual_status is retained as original executor attribution; this repair views only the three targets.',
                                      new_source_observations=u.pin(u.A / 'source-observations.json'),
                                      effective_components_rule=u.RULE,
                                      component_observations=logical_pin('component-observations.json', output['component-observations.json']),
                                      independent_review='Fresh independent rereview pending; original review does not approve repaired metadata.')
    output['region-ledger-final.json'] = u.encoded(ledger)
    old_visual = u.load(u.D / 'visual-inspection.json')
    old_rows = {x['key']: (i,x) for i,x in enumerate(old_visual['every_region'])}
    visual_rows = []
    for row in ledger['regions']:
        key = row['region']['key']; index,old = old_rows[key]
        assert old['region_id'] == row['region']['id'] and old['revision'] == row['region']['revision']
        visual_rows.append(dict(region_id=old['region_id'], revision=old['revision'], key=key,
                                components=row['components'], component_evidence_id=old['component_evidence_id'],
                                original_observation_json_pointer=f'/every_region/{index}',
                                boundary_observation_attribution='Original executor; retained immutable baseline, not newly viewed here.',
                                current_executor_viewed_exact_counter=key in u.TARGETS,
                                current_component_status='implemented_pending_independent_review' if key in u.TARGETS else 'unchanged_original_observation'))
    visual = dict(actor=u.CFG['actor'], model=u.CFG['model'], reasoning=u.CFG['reasoning'],
                  inspection_kind='Bounded executor repair observations, not independent rereview.',
                  own_source_observations=u.pin(u.A / 'source-observations.json'),
                  own_view_scope=list(u.TARGETS), own_full_page_viewing=False,
                  original_executor_inspection=u.pin(u.D / 'visual-inspection.json'),
                  original_executor_actor=old_visual['actor'],
                  original_independent_review=u.pin(u.V / 'review.json'),
                  inherited_scope='All unchanged original pages/overlays/bounds are attributed solely to the pinned original executor/reviewer; no inherited viewing by this actor.',
                  component_observations=logical_pin('component-observations.json', output['component-observations.json']),
                  current_ledger=logical_pin('region-ledger-final.json', output['region-ledger-final.json']),
                  effective_components_rule=u.RULE, every_region=visual_rows,
                  page_4_or_9_accessed=False, other_page_content_accessed=False,
                  independent_review='pending_fresh_separate_session')
    output['visual-inspection.json'] = u.encoded(visual)
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = (u.R / args.output).resolve()
    assert out == u.A or out.parent == u.A, 'Only primary attempt or fresh direct child output allowed.'
    if out != u.A:
        out.mkdir(exist_ok=False)
    output = generate()
    assert all(not (out / name).exists() for name in output), 'Never overwrite repair product.'
    for name,data in output.items():
        p = out / name; p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f: f.write(data)
    print(json.dumps({'result':'generated_exact_metadata_repair','output':out.relative_to(u.R).as_posix(),
                      'files':[u.pin(out/name) for name in output]},indent=2))
