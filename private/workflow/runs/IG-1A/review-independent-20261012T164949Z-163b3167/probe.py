"""Independent bounded synthetic mutations; never change product records on disk."""
import copy
import json
from pathlib import Path

from wgc.contracts.source import ContractError, load_json, seal_record, validate_bundle, _shape, _check_schema

HERE = Path(__file__).parent
BASE = load_json(Path('tests/contracts/fixtures/valid-source.json'))
RESULTS = []


def get(b, name):
    return next(r for r in b['records'] if r['id'] == 'synthetic:' + name)


def active(r):
    return {k: r[k] for k in ('id', 'record_type')} | {'mode': 'active'}


def historical(r):
    return active(r) | {'mode': 'historical', 'revision_id': r['revision_id']}


def change(b, name, fn, retain=False):
    old = get(b, name)
    new = copy.deepcopy(old)
    fn(new)
    new = seal_record(new)
    if retain:
        b['records'].append(new)
    else:
        b['records'][b['records'].index(old)] = new
    snap = get(b, 'snapshot')
    for entry in snap['data']['selected']:
        if entry['id'] == old['id']:
            entry.update({k: new[k] for k in ('id', 'record_type', 'revision_id', 'content_hash')})
    b['records'][b['records'].index(snap)] = seal_record(snap)
    return new


def probe(name, mutate, expected, basis, report_check=None):
    b = copy.deepcopy(BASE)
    mutate(b)
    # Save every complete counterexample, including valid hashes and snapshot pins.
    (HERE / (name + '.json')).write_text(json.dumps(b, indent=2) + '\n', encoding='utf-8')
    try:
        report = validate_bundle(b)
        actual = 'valid'
        error = None
    except ContractError as exc:
        actual, report, error = 'invalid', None, str(exc)
    ok = actual == expected and (report_check is None or actual == 'invalid' or report_check(report))
    RESULTS.append(dict(name=name, expected=expected, actual=actual, met=ok, basis=basis, error=error, report=report))


probe('gap-as-represented-target', lambda b: change(b, 'coverage0', lambda r: r['data'].update(target_refs=[active(get(b, 'gap'))])), 'invalid', 'Architecture: Gaps never count as represented content; criterion 3.')
probe('unrelated-exclusion-approval', lambda b: change(b, 'coverage0', lambda r: r['data'].update(status='excluded', target_refs=[], exclusion_reason='Exclude region 1 without a decision about that region.', scope_decision_ref=historical(get(b, 'review')))), 'invalid', 'Data model: exclusions need an approved scope boundary; scoped acceptance cannot accept siblings; criterion 3.')


def historical_dependency(b):
    def edit(r):
        r['data'].update(relation_type='procedure_use', requirement='required', target_ref=historical(get(b, 'procedure')))
        r['data']['applicability'] = copy.deepcopy(get(b, 'clause')['data']['aspects'][0]['statement'])
    change(b, 'history-link', edit)
    change(b, 'snapshot', lambda r: r['data'].update(selected=[s for s in r['data']['selected'] if s['id'] != 'synthetic:procedure']))


probe('historical-required-dependency', historical_dependency, 'invalid', 'Data model: references used as active rules resolve only in selected snapshot; historical retention does not activate rules; criterion 2.')
probe('unknown-normative-formal', lambda b: change(b, 'clause', lambda r: r['data']['aspects'][0].update(statement=copy.deepcopy(get(b, 'parameter')['data']['description']['unit']), execution_impact='formal'), retain=True), 'invalid', 'Opaque/unknown meaning cannot claim formal execution impact; criterion 3.')
probe('wrong-table-coordinate', lambda b: change(b, 'table', lambda r: r['data']['description']['cells'][0]['coordinates'][0].update(axis_id='absent-axis')), 'invalid', 'Data model: table coordinates resolve to participating axes; criterion 4.')
probe('empty-table-note-scope', lambda b: change(b, 'table', lambda r: r['data']['description']['notes'][0].update(axis_ids=[], cell_ids=[])), 'invalid', 'Mechanics: note scope must be explicit; criterion 4.')
probe('empty-group-effect', lambda b: change(b, 'clause', lambda r: r['data']['semantic_groups'][0].update(effects=[]), retain=True), 'invalid', 'Data model: explicit condition/effect composition; criterion 1.')
probe('duplicated-group-condition', lambda b: change(b, 'clause', lambda r: r['data']['semantic_groups'][0].update(conditions=['lit-condition', 'lit-condition']), retain=True), 'invalid', 'Stable aspect composition cannot contain duplicate members; criterion 1.')
probe('complete-empty-review-basis', lambda b: change(b, 'review', lambda r: r['data'].update(basis=[])), 'invalid', 'Data model: incomplete basis cannot prove current freshness; criterion 3.')
probe('unknown-review-basis', lambda b: change(b, 'review', lambda r: r['data'].update(basis_completeness='unknown')), 'valid', 'Data model: unknown completeness gives unknown freshness.', lambda r: r['reviews'][0]['freshness'] == 'unknown')
probe('model-observation', lambda b: change(b, 'review', lambda r: r['data'].update(actor_role='model', authorization=None, decision_artifact=None, decision='observation')), 'valid', 'Model observations are distinct from human acceptance.', lambda r: not r['semantic_acceptance_granted'])
probe('validator-acceptance', lambda b: change(b, 'review', lambda r: r['data'].update(actor_role='validator')), 'invalid', 'Only human authority metadata can record accepted decisions.')
probe('unrelated-aspect-change', lambda b: change(b, 'clause', lambda r: r['data']['aspects'][1]['statement']['value'].update(text='A changed effect only.'), retain=True), 'valid', 'Data model: scoped decisions do not accept sibling aspects; unchanged scoped target can remain current.', lambda r: r['reviews'][0]['freshness'] == 'current')
probe('changed-target-description-whole-review', lambda b: (change(b, 'review', lambda r: r['data']['targets'][0].pop('aspect_id')), change(b, 'clause', lambda r: r['data']['description']['description']['value'].update(text='Changed whole description.'), retain=True)), 'valid', 'Whole-record target changes must make review stale.', lambda r: r['reviews'][0]['freshness'] == 'stale')
probe('missing-selected-basis', lambda b: change(b, 'snapshot', lambda r: r['data'].update(selected=[s for s in r['data']['selected'] if s['id'] != 'synthetic:source'])), 'valid', 'Historical source evidence persists but missing selected basis is stale.', lambda r: r['reviews'][0]['freshness'] == 'stale')
probe('reordered-store', lambda b: b['records'].reverse(), 'valid', 'Stable identities do not depend on record store order.')

# Independently exercise each supported structural keyword family used by this schema.
schema_cases = [
    ('boolean-not-integer-const', True, {'const': 1}, False),
    ('boolean-not-integer-type', True, {'type': 'integer'}, False),
    ('strict-oneOf-overlap', 1, {'oneOf': [{'type': 'integer'}, {'minimum': 0}]}, False),
    ('local-ref-with-sibling', 1, {'$ref': '#/$defs/int', 'maximum': 0}, False),
    ('if-then', {'a': 1}, {'if': {'properties': {'a': {'const': 1}}}, 'then': {'required': ['b']}}, False),
    ('additional-property', {'a': 1}, {'type': 'object', 'properties': {}, 'additionalProperties': False}, False),
    ('items-minItems', [], {'type': 'array', 'items': {'type': 'integer'}, 'minItems': 1}, False),
    ('bounds-valid', 0, {'type': 'integer', 'minimum': 0, 'maximum': 1}, True),
    ('pattern-maxLength', 'abc', {'type': 'string', 'pattern': '^a', 'maxLength': 2}, False),
]
for name, value, schema, expected in schema_cases:
    root = {'$defs': {'int': {'type': 'integer'}}}
    actual = not _shape(value, schema, root, '$')
    RESULTS.append(dict(name=name, expected=expected, actual=actual, met=actual == expected, basis='Bundled offline schema keyword semantics.'))
bundled = load_json(Path('contracts/ig/source.schema.json'))
_check_schema(bundled, bundled)

# Re-run every frozen catalogue fixture, checking its declared outcome and measurements.
catalogue = load_json(Path('tests/contracts/fixtures/catalog.json'))
for c in catalogue['cases']:
    try:
        r = validate_bundle(load_json(Path('tests/contracts/fixtures') / c['file']))
        actual = True
        err = None
    except ContractError as exc:
        actual, r, err = False, None, str(exc)
    met = actual == c['valid']
    if r:
        exp = c['report']
        met &= not r['semantic_acceptance_granted']
        met &= 'execution' not in exp or r['executable']['status'] == exp['execution']
        met &= 'review_freshness' not in exp or r['reviews'][0]['freshness'] == exp['review_freshness']
        met &= 'transcription_represented' not in exp or r['coverage_inventory_region_counts']['transcription']['represented'] == exp['transcription_represented']
    RESULTS.append(dict(name=c['file'], expected=c['valid'], actual=actual, met=met, basis=c['basis'], error=err))

(HERE / 'probe-results.json').write_text(json.dumps(RESULTS, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'checks': len(RESULTS), 'unmet': [r['name'] for r in RESULTS if not r['met']]}, indent=2))
raise SystemExit(1 if any(not r['met'] for r in RESULTS) else 0)
