"""Materialize approved scopes and propose a bounded measurement policy offline."""
import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
HERE = Path(__file__).resolve().parent
BASE = P / 'evaluation/eval-v1-candidate-20261008-02'
NEW = P / 'evaluation/eval-v1-candidate-20261009-03'

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def ref(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest, 'bytes': path.stat().st_size}

def verify(item):
    actual = ref(ROOT / item['path'])
    assert all(actual[key] == item[key] for key in ('path', 'sha256', 'bytes')), (actual, item)

def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def ids(numbers):
    return [f'EXP-{int(n):03d}' for n in numbers.split()]

assert not NEW.exists()
assert not (P / 'evaluation/eval-v1').exists()
assert not (P / 'evaluation/freeze-public-v1.json').exists()
now = datetime.now(timezone.utc).isoformat()
base_manifest = load(BASE / 'manifest.json')
for item in [*base_manifest['artifacts'], *base_manifest['provenance']]:
    verify(item)
state = load(HERE / 'review-state-after-decision-05.json')
overlays = []
for item in state['overlays_in_order']:
    verify(item)
    overlay = load(ROOT / item['path'])
    verify(overlay['authorizing_decision'])
    overlays.append(overlay)
assert len(overlays) == 5
assert ref(P / 'source/original-pdf-20261008-01.pdf')['sha256'] == 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'

NEW.mkdir()
artifacts = {name: load(BASE / (name + '.json')) for name in ('inventory', 'expectations', 'dependencies', 'situations')}
for name, value in artifacts.items():
    value.update({'artifact': f'candidate-{name}-03', 'candidate_id': NEW.name,
                  'status': 'candidate_waiting_scope_review', 'frozen': False, 'gold': False,
                  'freeze_authorized': False, 'recorded_at_utc': now,
                  'materialization_parent': ref(BASE / (name + '.json'))})

d = artifacts['dependencies']
added_ids = {o['confirmed_relation']['id'] for o in overlays}
assert added_ids == {'DEP-008', 'DEP-002', 'DEP-017', 'DEP-024', 'DEP-041'}
assert added_ids <= {r['id'] for r in d['unconfirmed_execution_candidates']}
d['confirmed_execution_relations'].extend(copy.deepcopy(o['confirmed_relation']) for o in overlays)
d['unconfirmed_execution_candidates'] = [r for r in d['unconfirmed_execution_candidates'] if r['id'] not in added_ids]
d['counts'].update({'confirmed_explicit_execution': 5, 'unconfirmed_explicit_execution': 94})
d['metric_denominators'] = {'explicit': 5, 'implicit': 3, 'explicit_metric': 'n/a until freeze and response',
                           'implicit_metric': 'n/a until freeze and response',
                           'recall_scope': 'exact frozen source/target/kind/explicitness and necessity scope; no complete-graph claim',
                           'full_output_precision': 'review every unique output relation; pending outside-set is neither TP nor certain FP; report TP_output separately from TP_gold'}
d['pending_internal_explicit_tuple_review'] = []
d['freeze_readiness'] = 'relation tuple review complete in bounded scopes; scope/policy approval and distinct freeze decision still required'
d['materialization_overlays_in_order'] = state['overlays_in_order']
assert Counter(r['explicitness'] for r in d['confirmed_execution_relations']) == {'explicit': 5, 'implicit': 3}
assert Counter(r['explicitness_proposal'] for r in d['unconfirmed_execution_candidates']) == {'explicit': 94, 'implicit': 11}
assert len({(r['from'], r['to'], r['kind'], r['explicitness']) for r in d['confirmed_execution_relations']}) == 8
assert len(d['mentions']) == len(d['continuations']) == 7
assert len(d['confirmed_execution_relations']) + len(d['unconfirmed_execution_candidates']) + len(d['mentions']) + len(d['continuations']) == 127

e = artifacts['expectations']
by_id = {row['id']: row for row in e['expectations']}
scored = {row['id'] for row in e['expectations'] if row['classification'] == 'confirmed_local_content_scope'}
context = set(by_id) - scored
assert len(scored) == 66 and context == set(ids('10 19 31 33 50 64 66 74'))

# These are NEW measurement proposals based on reviewed_scope, not copied draft tags.
# One (category, EXP-ID) is one bounded content group, never an atomic/glyph count.
categories = {
    'numbers': ids('2 4 7 8 9 12 13 15 17 20 22 23 25 27 28 30 32 34 35 36 37 38 39 41 42 43 45 47 48 49 51 52 55 57 58 61 62 63 65 68 69'),
    'units': ids('2 4 8 12 13 15 17 20 22 23 25 27 28 30 32 34 35 36 37 38 39 41 42 43 45 47 48 51 52 55 57 58 61 62 63 65 68 69'),
    'negations': ids('1 3 4 5 6 9 11 14 15 18 21 23 24 26 27 28 29 32 35 36 40 41 44 46 47 48 49 51 52 53 54 55 56 57 58 59 60 61 67 70 71 72 73'),
    'conditions': ids('1 2 3 4 5 6 7 8 9 11 12 13 14 15 16 17 18 20 21 22 23 24 25 26 27 28 29 30 32 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 51 52 53 54 55 56 57 58 59 60 61 62 63 65 67 68 69 70 71 72 73'),
    'exceptions': ids('4 5 6 8 9 11 12 14 15 16 18 20 21 23 24 26 27 29 32 35 36 37 38 39 40 41 42 44 46 47 48 49 51 52 53 54 55 56 57 58 59 60 61 62 63 65 67 69 70 71 72 73'),
    'time': ids('1 3 9 11 13 14 16 24 34 35 40 44 47 48 49 51 52 54 57 58 59 61 62 63 65 67 69 71 73'),
    'tables': ids('5 7 8 9 20 70 73'),
    'diagrams': ids('46'),
}
descriptions = {
    'numbers': 'Only numeric values, formulas, signs, rounding, comparisons and limits explicitly present in the reviewed scope; publisher rule numbers and unknown ratings are not numeric gold.',
    'units': 'Preserve the reviewed meaning of Hits/CH, MP/MA, hex distances/counts, die modifiers/shifts, TQ/Size/Initiative and phase/turn rate denominators as applicable; never infer actual counter values.',
    'negations': 'Preserve prohibition/exclusion and its exact actor, target and scope; do not convert no full permission/no waiver into an invented blanket ban.',
    'conditions': 'Preserve applicability gates, actors, targets and conjunction/disjunction only within reviewed scope; supplied facts are not source-certified real state.',
    'exceptions': 'Preserve narrowed/alternative treatment and its applicable population/conditions; do not generalize it to unreviewed procedures or negate unresolved context.',
    'time': 'Preserve the reviewed trigger, phase/turn, before/after/first/subsequent and duration constraints; unresolved sequencing (4.84, AS, full Rout, depleted BI) is excluded.',
    'tables': 'Preserve only local reviewed row outcomes or the obligation to use a named table/retain its notes. 9.14 local row fragments are reviewed separately. MRRC/CRT/Movement Cost Chart actual lookups remain unclosed; no claimed broad table-reading benchmark.',
    'diagrams': 'Only EXP-046: reviewed Original top/After bottom and the unstacking direction. No full coordinates/hex geometry or all glyph/rating coverage.',
}
category_rows = []
for category, members in categories.items():
    assert len(set(members)) == len(members) and set(members) <= scored
    category_rows.append({'id': category, 'denominator_proposed': len(members), 'scope': descriptions[category],
                          'units': [{'id': f'{category}:{exp_id}', 'expectation_id': exp_id,
                                     'scoped_content': by_id[exp_id]['reviewed_scope'],
                                     'authorizing_scoped_decisions': by_id[exp_id]['authorizing_scoped_decisions'],
                                     'do_not_score': ['limits', 'unreviewed fields', 'context lookup', 'reference-only repeated result']} for exp_id in members]})
policy = {
    'id': 'M-POC1C-scoped-measurement-policy-03', 'status': 'proposal_waiting_owner_scope_review',
    'owner_approved': False, 'card': 'M-POC1C', 'candidate': NEW.name, 'plan': ref(ROOT / 'docs/POC-PLAN.md'),
    'content_group_denominator': 66, 'context_requirement_denominator': 8,
    'atomic_norm_count': 'unknown', 'full_source_completeness_certified': False,
    'content_matching': 'A group earns one correct result only if ALL owned, confirmed scope components are accurately represented with evidence and no critical contradiction. References to a component owned by another EXP-ID earn no second point. Limits and unresolved/context/unreviewed fields are not answer gold. Partial groups are reported component-by-component but do not get fractional success.',
    'category_matching': 'One category/EXP-ID pair earns one correct count only if every confirmed component relevant to that category within reviewed_scope is correct. Multi-category membership is intentional diagnostic tagging, not extra rule points; counts may not be summed into rule completeness. Missing applicable components are omissions, wrong ones errors; unreviewed/context details excluded. Reviewer records exact compared spans and error list.',
    'categories': category_rows,
    'category_numeric_thresholds': 'POC-PLAN has no independent percentage threshold for each content category; report correct/errors/omitted/blocked/unassessed. Zero critical errors is the overriding gate. Do not invent category-specific cutoffs.',
    'illustration_states_separate': {'denominator': 2, 'expectation_ids': ids('54 57'), 'scope': 'Only reviewed Fire/Move counter sides and Once/Finished marker states, not the diagram category or all numeric glyphs.'},
    'context_matching': 'Report local known instruction and needed source separately for all eight groups; no real value/outcome invented. Missing critical source must block the relevant concrete question. After context, re-evaluate solvability without changing frozen gold.',
    'relations': {'explicit_denominator': 5, 'implicit_denominator': 3,
                  'tuple_matching': 'Match semantic source scope, target identity/scope, direction, kind and explicitness with evidence; local IDs may differ with documented source mapping. Wrong direction/kind is not full TP. Same tuple duplicates never add TP.',
                  'recall': 'TP_gold/(TP_gold+FN) on the frozen checked set only; extra correct edges do not enlarge gold.',
                  'precision': 'TP_output/(TP_output+FP) after human review of every unique output edge including outside-set edges; pending edges neither TP nor certain FP, so final precision remains not_assessable until reviewed.',
                  'mentions_denominator': 7, 'mentions_scope': 'Occurrence/role only; inherited aliases/external target identities unconfirmed.',
                  'continuations_denominator': 7, 'continuations_scope': 'Physical source control only, not execution TP/FN.',
                  'unknown_candidates': 105, 'complete_graph_certified': False},
    'situations': {'denominator': 20, 'local_results': 17, 'expected_blocks': 3,
                   'matching': 'Every supplied variant and required local conclusion must be correct; one situation ID remains one sample. No partial variant inflation. Distinguish correct local result, wrong result, justified block, unjustified block and unassessed. All remain in denominator.',
                   'block_ids': ['SIT-06', 'SIT-11', 'SIT-18'],
                   'block_policy': 'Correct expected block is not a meaningful result for the 80%/70% gates. After supplied critical context do not reward a stale blanket block; report local known facts and the current unresolved remainder.'},
    'criticality': 'Preserve attached owner decisions in exact local scopes; all 66 content groups and 20 situations currently have critical local scopes. EXP-074 context criticality is conditional on concrete parameter use. No whole-record gold extension.',
    'thresholds': {'continue': {'all_critical_correct': True, 'critical_errors': 0, 'unmarked_gaps': 0,
                               'unsupported_facts': 0, 'situations_all_assessed': 20, 'meaningful_results_min': 16,
                               'rules_completeness_min': 0.95, 'relations_explicit_precision_recall_min': 0.95,
                               'relations_implicit_precision_recall_min': 0.95,
                               'rounded_recall_min': {'content_groups': 63, 'explicit': 5, 'implicit': 3},
                               'critical_override': 'Numerically 63/66 meets 95%, but all 66 groups have critical scoped components; critical correctness remains mandatory, not waived by that percentage.'},
                   'repair': {'rules_and_relations_min': 0.80, 'meaningful_situations_min': 14,
                              'after_last_allowed_iteration': True, 'no_uncontrolled_guessing': True,
                              'rounded_recall_min': {'content_groups': 53, 'explicit': 4, 'implicit': 3}},
                   'reject': 'Below repair thresholds with a credible assessment after exhausted limits, persistent critical guessing or dominant manual reconstruction cost; no claim of model failure from missing gold/source/measurement.'},
    'limits': {'core_pages': 7, 'extra_unique_pages': 8, 'extra_rules': 20, 'extra_tables': 4,
               'dependency_depth': 2, 'context_rounds': 2, 'first_reached_limit_applies': True,
               'corrective_responses_total': 3, 'early_format_repairs_max': 1,
               'user_hours_total': 8, 'user_hours_after_first': 4, 'complete_first_responses': 1,
               'retry_requires_new_id': True, 'M_POC0_cost_separate': True},
    'cost_reporting': 'Active user/model time, documented tokens/cost, context size, iterations, failed replies, corrections and regressions by stage; unknown remains unknown, not zero. Recorded/calender times do not establish remaining budget.',
    'measurement_available': 'No extraction or quality result yet. Scoped comparison possible after scope approval and freeze; no generalization to full game or model superiority. Unknown active budget prevents asserting compliance without later evidence/owner decision.',
    'plan_thresholds_changed': False, 'plan_limits_changed': False,
}
save(NEW / 'measurement-policy.json', policy)
for row in e['expectations']:
    row['scoring_rubric'] = {'whole_group_success': row['id'] in scored,
                             'categories_proposed': [name for name, members in categories.items() if row['id'] in members],
                             'policy': ref(NEW / 'measurement-policy.json'), 'owner_approved': False}
e['denominator_policy'].update({'content_grouping_needs_freeze_review': True, 'content_dimensions_need_explicit_scoped_rubric': False,
                               'category_rubric_proposed_requires_owner_review': True, 'full_source_completeness_certified': False})
artifacts['inventory']['measurement_policy']['rule_completeness_denominator'] = '66 proposed grouped reviewed content scopes; category rubrics in measurement-policy.json; no full 41-label/98-clause-group gold certificate'
s = artifacts['situations']
s['denominator_policy'] = copy.deepcopy(policy['situations'])
sit16 = next(r for r in s['situations'] if r['id'] == 'SIT-16')
sit16['expected']['rationale'] = 'At least half round down and without moving exception retained. DEP-NEW-001 has a separate actual scoped owner approval; the local supplied-case result does not certify real battle parameters.'
assert Counter(row['expected']['kind'] for row in s['situations']) == {'local_result': 17, 'justified_block': 3}
for name, value in artifacts.items():
    save(NEW / (name + '.json'), value)
save(NEW / 'change-map.json', {
    'base_candidate': ref(BASE / 'manifest.json'), 'operations': [
        {'id': r['id'], 'operation': 'unconfirmed to owner-confirmed exact local tuple', 'overlay': state['overlays_in_order'][n],
         'authorizing_decision': overlays[n]['authorizing_decision']} for n, r in enumerate(o['confirmed_relation'] for o in overlays)],
    'content_groups_unchanged': 74, 'new_semantic_expectations': 0, 'new_situations': 0,
    'measurement_policy_added': ref(NEW / 'measurement-policy.json'),
    'semantic_content_unchanged_except': 'SIT-16 rationale metadata now states already accepted relation, no case result change.',
    'historical_artifacts_modified': [], 'owner_approval_extended': False,
})
review = (HERE / 'scope-review-template.md').read_text(encoding='utf-8')
table = '\n'.join(f"| {row['id']} | {row['denominator_proposed']} |" for row in category_rows)
review = review.replace('{{CATEGORY_COUNTS}}', table)
with (NEW / 'review.md').open('x', encoding='utf-8', newline='\n') as stream:
    stream.write(review)
manifest = {
    'id': NEW.name, 'card': 'M-POC1C', 'status': 'candidate_waiting_scope_review',
    'date': '2026-10-09', 'timezone': 'Europe/Warsaw', 'recorded_at_utc': now,
    'frozen': False, 'gold': False, 'freeze_authorized': False, 'owner_freeze_response': None,
    'source': ref(P / 'source/original-pdf-20261008-01.pdf'),
    'artifacts': [ref(path) for path in sorted(NEW.iterdir()) if path.is_file()],
    'provenance': [ref(BASE / 'manifest.json'), *state['overlays_in_order'],
                   *(o['authorizing_decision'] for o in overlays), ref(ROOT / 'docs/POC-PLAN.md'),
                   ref(HERE / 'assemble_candidate.py'), ref(HERE / 'scope-review-template.md')],
    'counts': {'reference_inventory': 207, 'local_content_scope_groups': 66, 'context_requirement_groups': 8,
               'situations': 20, 'local_results': 17, 'blocks': 3,
               'confirmed_explicit_execution': 5, 'confirmed_implicit_execution': 3,
               'unconfirmed_execution_candidates': 105, 'mentions_separate': 7, 'continuations_separate': 7,
               'content_categories_proposed': {r['id']: r['denominator_proposed'] for r in category_rows}},
    'open_gates': ['Actual owner scope/grouping/rubric/limits approval', 'Distinct actual owner freeze decision'],
    'scope_readiness': 'Technical artifact assembly and exact relation tuple review complete; proposed policy pending owner review, not permission to freeze.',
    'quality_results': 'n/a: no frozen evaluation and no extraction response',
    'plan_thresholds_unchanged': True, 'plan_limits_unchanged': True, 'forbidden_work_performed': [],
}
save(NEW / 'manifest.json', manifest)
for item in [*manifest['artifacts'], *manifest['provenance']]:
    verify(item)
save(HERE / 'candidate-validation.json', {
    'recorded_at_utc': now, 'candidate_manifest': ref(NEW / 'manifest.json'),
    'checked_artifacts_and_provenance': len(manifest['artifacts']) + len(manifest['provenance']),
    'source_hash_valid': True, 'relation_partition_sum': 127, 'unique_confirmed_execution_tuples': 8,
    'expectation_classification': dict(Counter(r['classification'] for r in e['expectations'])),
    'situation_classification': dict(Counter(r['expected']['kind'] for r in s['situations'])),
    'category_counts': manifest['counts']['content_categories_proposed'], 'new_semantic_scopes': 0,
    'scope_policy_approved': False, 'freeze_authorized': False, 'frozen': False,
})
save(HERE / 'pending-question-06-scope.json', {
    'id': 'M-POC1C-RQ-06-scope', 'status': 'waiting_owner_decision',
    'candidate_manifest': ref(NEW / 'manifest.json'), 'measurement_policy': ref(NEW / 'measurement-policy.json'),
    'review': ref(NEW / 'review.md'), 'proposed_counts': manifest['counts'],
    'topic': 'Accept concrete bounded assessment scope, grouping, category rubrics, retained limitations and unchanged POC-PLAN thresholds/limits; no freeze authorization yet.',
    'plain_language_question': 'Czy zatwierdzasz ten ograniczony zakres i sposób oceny wraz z podanymi progami, limitami i wyłączeniami? To nie jest jeszcze zgoda na freeze.',
    'actual_owner_answer': None, 'freeze_authorization_requested': False,
})
print(json.dumps({'candidate_manifest': ref(NEW / 'manifest.json'), 'counts': manifest['counts']}, indent=2))
