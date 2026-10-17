"""Independent, task-scoped review checks; writes only this fresh review root."""
import argparse
import copy
import datetime
import hashlib
import json
from pathlib import Path

from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import assemble, coverage, file_pin, page_basis_hash, seal, validate
from wgc.sources.pdf import extract_evidence

ROOT = Path.cwd()
OUT = Path('private/workflow/runs/IG-2B06/review-089ffca5-01')
RUN = Path('private/workflow/runs/IG-2B06/continuation-21-24-serial02')
SESSION = Path('private/workflow/orchestrator/20261016T182116Z-202cea4c/002-IG-2B06-reviewer-089ffca5')
META = {k: json.loads((OUT/'checkpoint.json').read_text())[k] for k in
        ('role', 'actor', 'task', 'model', 'reasoning', 'configuration_evidence', 'configuration_sha256')}


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def pin(path):
    return file_pin(ROOT, Path(path).as_posix())


def write(name, data):
    p = OUT/name
    assert not p.exists(), str(p)
    p.write_text(json.dumps({**META, **data}, indent=2)+'\n', encoding='utf-8')


def check_pin(p):
    actual = pin(p['path'])
    assert actual['sha256'] == p['sha256'], p['path']
    if 'bytes' in p:
        assert actual['bytes'] == p['bytes'], p['path']


def stable_evidence(ev):
    return {k: ({q:v for q,v in value.items() if q!='path'}
                if k in ('text', 'image', 'crop_pdf') else value)
            for k,value in ev.items()}


args = argparse.ArgumentParser()
args.add_argument('mode', choices=['check', 'replay-a', 'replay-b', 'compare'])
mode = args.parse_args().mode
author = load(RUN/'authored/inventory.json')
registry = load(RUN/'authored/identity-registry.json')
ledger = load(RUN/'region-ledger.json')
ids = [r['id'] for r in ledger['regions']]
assert len(ids) == len(set(ids)) == 114
by_id = {r['id']:r for r in author['regions']}
chosen = [by_id[rid] for rid in ids]
assert author['registry'] == registry

if mode.startswith('replay-'):
    validate(author, ROOT)
    dest = OUT/mode
    dest.mkdir(exist_ok=False)
    doc = copy.deepcopy(author)
    geometry = copy.deepcopy(author['pages'])
    for page in geometry:
        page['label'] = {'status':'unknown', 'value':None,
                         'reason':'Temporary geometry-only evidence view; full pages remain unchanged.',
                         'evidence':None}
    geometry = [seal(p) for p in geometry]
    assert [page_basis_hash(p) for p in geometry] == [page_basis_hash(p) for p in author['pages']]
    for index, region in enumerate(chosen):
        view = assemble(author['source'], geometry, [region], registry,
                        reading_order=[region['id']], links=[], evidence=[], toolchain=author['toolchain'])
        assert view['regions'][0] == region
        ev = extract_evidence(view, region['id'], ROOT,
                              (dest/f'region-{index:03d}').as_posix(), dpi=144)
        assert stable_evidence(ev) == stable_evidence(ledger['regions'][index]['fresh_evidence'])
        doc['evidence'].append(ev)
        if (index+1)%10 == 0 or index+1 == len(chosen):
            print(json.dumps({'mode':mode, 'completed':index+1, 'total':len(chosen)}), flush=True)
    doc = seal(doc)
    result = validate(doc, ROOT)
    (dest/'inventory.json').write_bytes(canonical_bytes(doc)+b'\n')
    (dest/'identity-registry.json').write_bytes(canonical_bytes(registry)+b'\n')
    write(mode+'-report.json', {'summary':'Complete independent serial reviewer replay from frozen pre-evidence authored input.',
          'input_inventory':pin(RUN/'authored/inventory.json'), 'input_registry':pin(RUN/'authored/identity-registry.json'),
          'output_inventory':pin(dest/'inventory.json'), 'output_registry':pin(dest/'identity-registry.json'),
          'assigned_regions':112, 'context_regions':2, 'complete_region_ids':ids,
          'all_generated_stable_evidence_equal_frozen_final':True,
          'full_input_and_output_validation':True, 'serial_current_python_process':True,
          'generated_from_other_replay':False, 'coverage':result, 'exit_code':0})
elif mode == 'check':
    delivery = load(RUN/'delivery.json')
    for p in delivery['artifacts']:
        check_pin(p)
    task = load(SESSION/'task.json')
    contract = load(task['refinement_contract']['path'])
    for p in contract['input_pins']:
        check_pin(p)
    scope = load(task['continuation_authorization']['scope']['path'])
    check_pin(scope['preserve_manifest'])
    preserved = load(scope['preserve_manifest']['path'])
    for p in preserved['artifacts']:
        check_pin(p)
    docs = {x:load(RUN/x/'inventory.json') for x in ('replay-a','replay-b','final-verified')}
    for name,doc in docs.items():
        assert doc['registry'] == registry == load(RUN/name/'identity-registry.json')
        for key in ('regions','pages','source','registry','reading_order','links','toolchain'):
            assert doc[key] == author[key], (name,key)
        assert doc['evidence'][:622] == author['evidence'] and len(author['evidence']) == 622
        assert len(doc['evidence'][622:]) == 114
        new = {e['region_id']:e for e in doc['evidence'][622:]}
        for row in ledger['regions']:
            assert stable_evidence(new[row['id']]) == stable_evidence(row['fresh_evidence'])
            assert f'/{name}/' in new[row['id']]['image']['path']
    final = docs['final-verified']
    assert len(final['pages']) == 44 and len(final['regions']) == 756
    assert len(final['links']) == 158 and len(final['evidence']) == 736
    assert len(final['registry']['entries']) == 824
    retired = {x['id'] for x in contract['placeholder_targets']}
    assert not retired.intersection(r['id'] for r in final['regions'])
    assert retired.issubset(e['id'] for e in registry['entries'])
    fr = {r['id']:r for r in final['regions']}
    for row in ledger['regions']:
        for k in fr[row['id']]:
            assert fr[row['id']][k] == row[k], (row['id'], k)
        for component in row['components']:
            a,b,c,d = component['box']; x,y,z,w = row['box']
            assert x <= a < c <= z and y <= b < d <= w
    assert [rid for rid in final['reading_order'] if rid in set(ids)] == ids
    for ev in final['evidence']:
        for key in ('text','image','crop_pdf'):
            check_pin(ev[key])
    cont = load(RUN/'continuations.json')
    for link in cont['links']:
        assert {k:link[k] for k in ('from','to','kind','reason')} in final['links']
        for endpoint, rid in [('source_endpoint',link['from']), ('target_endpoint',link['to'])]:
            p = link[endpoint]
            assert p['region_id'] == rid and p['region_revision'] == fr[rid]['revision']
            assert p['box'] == fr[rid]['box'] and p['page_id'] == fr[rid]['page_id']
            assert p['evidence'] in final['evidence']
    # Recompute denominators, disjointness and explicit complements without assuming gaps are content.
    report = load(RUN/'coverage-report.json')
    counts = coverage(final)
    assigned = [r for r in ledger['regions'] if r['denominator_role']=='inventory']
    assert len(assigned) == 112
    assert sum(len(r['components']) for r in assigned) == 158
    assert report['full_inventory']['denominator_regions'] == 753
    assert report['full_inventory']['context_regions'] == 3
    assert report['assigned']['denominator_regions'] == 112
    assert report['task_context']['denominator_regions'] == report['task_context']['denominator_area_trillionths'] == 0
    for page in ledger['page_accounting']:
        boxes = [r['box'] for r in assigned if r['pdf_page']==page['pdf_page']]
        boxes += page['gap_boxes']
        assert sum((c-a)*(d-b) for a,b,c,d in boxes) == 10**12
        for i,(a,b,c,d) in enumerate(boxes):
            assert 0<=a<c<=1000000 and 0<=b<d<=1000000
            for x,y,z,w in boxes[i+1:]:
                assert min(c,z)<=max(a,x) or min(d,w)<=max(b,y)
    # The accepted dependency is accessed through its prepared projection for context.
    # Review the frozen baseline comparator and its exact input pins; do not dump baseline records.
    preservation = load(RUN/'preservation-report.json')
    assert preservation['all_passed'] and all(all(v.values()) for v in preservation['checks'].values())
    assert preservation['nonassigned_region_count'] == 642
    assert preservation['original_evidence_count'] == 622
    assert preservation['original_link_count'] == 126
    assert preservation['retired_placeholder_ids'] == sorted(retired)
    write('machine-checks.json', {'summary':'Independent frozen-pin, full author/output preservation, registry, ledger/component, boundary, evidence and complement checks.',
          'frozen_artifacts_verified':len(delivery['artifacts']), 'input_pins_verified':len(contract['input_pins']),
          'blocked_artifacts_rehashed':len(preserved['artifacts']), 'preserved_evidence_files_rehashed':622*3,
          'complete_regions_compared_per_output':756, 'complete_pages_compared_per_output':44,
          'stable_frozen_replay_comparisons':114, 'assigned_regions':112, 'assigned_components':158,
          'context_regions':2, 'continuation_endpoint_pairs_checked':len(cont['links']),
          'baseline_preservation_basis':'Hash-pinned accepted input projections; reviewed exact baseline comparison assertions at frozen reports.py lines 54-83 and their immutable passing preservation report. Full author-to-three-output structural equality and all preserved evidence bytes independently rechecked here.',
          'all_passed':True, 'exit_code':0})
else:
    docs = [load(OUT/n/'inventory.json') for n in ('replay-a','replay-b')]
    final = load(RUN/'final-verified/inventory.json')
    for doc in docs:
        for key in ('regions','pages','source','registry','reading_order','links','toolchain'):
            assert doc[key] == final[key]
        for ev, expected in zip(doc['evidence'],final['evidence']):
            assert stable_evidence(ev) == stable_evidence(expected)
    assert docs[0]['revision'] != docs[1]['revision'] != final['revision']
    write('reviewer-replay-comparison.json', {'summary':'Both complete independent reviewer replays match every frozen stable author/evidence field and generated byte.',
          'independent_inputs':[pin(RUN/'authored/inventory.json')]*2,
          'outputs':[pin(OUT/n/'inventory.json') for n in ('replay-a','replay-b')],
          'final_inventory':pin(RUN/'final-verified/inventory.json'), 'assigned_regions':112,
          'context_regions':2, 'all_three_artifact_bytes_equal_per_region':True,
          'all_736_stable_evidence_records_equal':True,
          'path_dependent_differences':'Evidence paths and enclosing inventory revisions differ; region/page/registry identities, bases, engine settings, text/crop/PNG bytes and pixel dimensions agree.',
          'all_passed':True, 'exit_code':0})
print(json.dumps({'mode':mode, 'exit_code':0}), flush=True)
