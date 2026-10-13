"""Static synthetic regression oracles for independent findings F1-F3."""
import copy
import json
from build_fixtures import (
    OUT, active, base, catalog, get, historical, known, replace, save, seal, unknown,
)

# F1: source-content families are node/evidence/relation, in either mode.
for mode in ['active', 'historical']:
    for mixed in [False, True]:
        b = copy.deepcopy(base)
        target = active(get(b, 'gap')) if mode == 'active' else historical(get(b, 'gap'))
        replace(b, 'coverage0', lambda r: r['data'].update(
            target_refs=([active(get(b, 'clause'))] if mixed else []) + [target]))
        save('invalid-coverage-gap-target-' + mode + ('-mixed' if mixed else ''), b, False,
             'A gap cannot represent source content, even mixed with a node or reached historically.',
             'Independent review F1; architecture: gaps never count as represented content.', error='schema')
for family in ['evidence', 'history-link']:
    b = copy.deepcopy(base)
    replace(b, 'coverage0', lambda r: r['data'].update(target_refs=[historical(get(b, family))]))
    save('valid-coverage-content-' + family, b, True,
         'Evidence and relations are source-content targets; their metadata do not grant execution.',
         'F1 allowed content families; IG-DATA-MODEL collections.', {'transcription_represented': 2})


def exclusion_case():
    b = copy.deepcopy(base)
    coverage = get(b, 'coverage0')['data']
    decision = copy.deepcopy(get(b, 'review'))
    decision['id'] = 'synthetic:boundary-review'
    decision['data'].update(kind='source_composition', targets=[coverage['region_ref']],
        basis=[coverage['inventory_ref'], historical(get(b, 'source'))],
        scope='Only region 1 at transcription level in this inventory is excluded.',
        coverage_boundary={'purpose': 'coverage_exclusion', 'inventory_ref': coverage['inventory_ref'],
                           'region_ref': coverage['region_ref'], 'level': 'transcription'})
    decision = seal(decision)
    b['records'].insert(-1, decision)
    get(b, 'snapshot')['data']['selected'].append(
        {k: decision[k] for k in ['id', 'record_type', 'revision_id', 'content_hash']})
    replace(b, 'coverage0', lambda r: r['data'].update(status='excluded',
        exclusion_reason='Explicitly approved fictional scope boundary.', target_refs=[],
        scope_decision_ref=historical(decision)))
    return b


# F2: targets/bases describe the exact boundary without a hash cycle.
b = exclusion_case()
save('valid-exact-coverage-exclusion', b, True,
     'Current complete authorized composition metadata approves exactly the inventory/region/level boundary.',
     'Independent review F2; IG-DATA-MODEL: exclusions require an approved scope boundary.',
     {'transcription_represented': 1, 'transcription_excluded': 1})
for variant in ['unrelated', 'other-region', 'other-level', 'other-inventory', 'partial',
                'stale', 'model', 'missing-inventory-basis']:
    b = exclusion_case()
    if variant == 'unrelated':
        replace(b, 'coverage0', lambda r: r['data'].update(scope_decision_ref=historical(get(b, 'review'))))
    elif variant == 'stale':
        replace(b, 'source', lambda r: r['data'].update(edition='synthetic-2'), preserve=True)
    else:
        def mutate(r):
            if variant == 'other-region':
                r['data']['coverage_boundary']['region_ref'] = historical(get(b, 'region2'))
                r['data']['targets'] = [historical(get(b, 'region2'))]
            elif variant == 'other-level':
                r['data']['coverage_boundary']['level'] = 'descriptive_semantics'
            elif variant == 'other-inventory':
                r['data']['coverage_boundary']['inventory_ref'] = historical(get(b, 'clause'))
                r['data']['basis'] = [historical(get(b, 'clause')), historical(get(b, 'source'))]
            elif variant == 'partial':
                r['data']['basis_completeness'] = 'partial'
            elif variant == 'model':
                r['data']['actor_role'] = 'model'
            elif variant == 'missing-inventory-basis':
                r['data']['basis'] = [historical(get(b, 'source'))]
        changed = replace(b, 'boundary-review', mutate)
        replace(b, 'coverage0', lambda r: r['data'].update(scope_decision_ref=historical(changed)))
    save('invalid-coverage-exclusion-' + variant, b, False,
         'Exclusion cannot inherit an unrelated/incomplete/stale/unauthorized boundary: ' + variant + '.',
         'Independent review F2; exact scope and review basis rules.',
         error='schema' if variant == 'model' else 'exact inventory/region/level boundary')

# F3: historical navigation remains valid; semantic endpoints pin selection.
for requirement in ['required', 'conditional']:
    for variant in ['unselected', 'superseded', 'selected', 'unselected-source']:
        b = copy.deepcopy(base)
        old_procedure = copy.deepcopy(get(b, 'procedure'))
        if variant == 'superseded':
            replace(b, 'procedure', lambda r: r['data']['description'].update(
                actor=known('A different fictional participant.', get(b, 'evidence'))), preserve=True)
        if variant == 'unselected':
            s = get(b, 'snapshot')
            s['data']['selected'] = [x for x in s['data']['selected'] if x['id'] != old_procedure['id']]
            b['records'][b['records'].index(s)] = seal(s)
        from_ref = historical(get(b, 'retired-concept')) if variant == 'unselected-source' else active(get(b, 'clause'))
        replace(b, 'history-link', lambda r: r['data'].update(relation_type='procedure_use',
            requirement=requirement, from_ref=from_ref, target_ref=historical(old_procedure),
            applicability=known('This fictional invocation uses the procedure.', get(b, 'evidence'))))
        valid = variant == 'selected'
        save(('valid' if valid else 'invalid') + '-' + requirement + '-historical-' + variant, b, valid,
             'A selected ' + requirement + ' dependency requires selected exact endpoint revisions: ' + variant + '.',
             'Independent review F3; IG-DATA-MODEL selected-rule resolution.',
             {'execution': 'blocked'} if valid else None, error=None if valid else 'semantic dependency endpoint')
b = copy.deepcopy(base)
replace(b, 'history-link', lambda r: r['data'].update(relation_type='procedure_use', requirement='conditional',
    target_status='unresolved', target_ref=None, raw_locator='An unavailable fictional procedure',
    gap_refs=[active(get(b, 'gap'))], applicability=unknown(get(b, 'gap'), 'Applicability is not established.')))
save('valid-unresolved-conditional-dependency', b, True,
     'An unresolved link with raw locator/gap is retained and blocks execution rather than activating history.',
     'F3 preservation of unresolved source links; unknown applicability is not false.', {'execution': 'blocked'})
(OUT / 'catalog.json').write_text(json.dumps({'format': 'wgc-synthetic-oracles-1', 'cases': catalog}, indent=2) + '\n', encoding='utf-8')
print('Frozen', len(catalog), 'contract oracles including F1-F3 regressions.')
