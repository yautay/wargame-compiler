"""Offline artifact assembly/audit for M-POC1C; no inference or extraction."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
HERE = Path(__file__).resolve().parent
OLD = P / 'evaluation/eval-v1-candidate-20261008-01'
NEW = P / 'evaluation/eval-v1-candidate-20261008-02'
R = P / 'evaluation/owner-review-002'


def read(path: Path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def reference(path: Path) -> dict:
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path), 'bytes': path.stat().st_size}


def save(path: Path, value) -> None:
    # All generated paths must be new. Existing candidates and history are immutable.
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def git(*args: str) -> str:
    return subprocess.run(
        ['git', '-c', 'safe.directory=C:/dev/wargame-compiler', *args],
        cwd=ROOT, check=True, capture_output=True, text=True,
        env={**__import__('os').environ, 'GIT_OPTIONAL_LOCKS': '0'},
    ).stdout.strip()


def header(artifact: str) -> dict:
    return {'artifact': artifact, 'candidate_id': NEW.name, 'card': 'M-POC1C',
            'status': 'candidate_incomplete_waiting_review', 'frozen': False,
            'gold': False, 'freeze_authorized': False, 'recorded_at_utc': now}


if NEW.exists() or (HERE / 'audit.json').exists():
    raise SystemExit('Refusing to overwrite a candidate or audit.')
now = datetime.now(timezone.utc).isoformat()
branch, head = git('branch', '--show-current'), git('rev-parse', 'HEAD')
assert branch == 'feature/tests'
assert git('merge-base', '--is-ancestor', '90535261a4498cabcd6abc0af33b56a4267b6193', 'HEAD') == ''
source = reference(P / 'source/original-pdf-20261008-01.pdf')
assert source['sha256'] == 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'

bmanifest = read(R / 'review-manifest-final-20261008.json')
checked = [*bmanifest['inputs'], *bmanifest['owner_review_files'],
           *bmanifest['public_documents'], *bmanifest['required_check_logs'],
           bmanifest['completion_measurement']]
failures = []
for item in checked:
    actual = reference(ROOT / item['path'])
    if actual != item:
        failures.append({'expected': item, 'actual': actual})
assert not failures, failures

old_manifest = read(OLD / 'manifest.json')
for item in [*old_manifest['artifacts'], *old_manifest['parents']]:
    assert reference(ROOT / item['path']) == item, item

baseline_paths = {ROOT / item['path'] for item in bmanifest['protected_file_inventory']}
baseline_paths.update(ROOT / item['path'] for item in checked)
baseline_paths.update(OLD.glob('*'))
baseline_paths.update(ROOT / name for name in (
    'CLAUDE.md', 'docs/SESSION-PLAYBOOK.md', 'docs/POC-PLAN.md',
    'docs/work/tasks/M-POC1C.md', 'docs/handoff/2026-10-08-M-POC1B-Final.md'))
baseline = [reference(path) for path in sorted(baseline_paths) if path.is_file()]
save(HERE / 'baseline.json', {'recorded_at_utc': now, 'files': baseline,
                            'allowed_public_updates': ['docs/STATUS.md', 'docs/ROADMAP.md', 'docs/HANDOFF.md']})
NEW.mkdir()

draft_e = read(P / 'evaluation/draft/expectations.json')
draft_e_by_id = {row['id']: row for row in draft_e['expectations']}
old_e = read(OLD / 'expectations.json')
context_ids = set(draft_e['sets']['requires_context'])
assert context_ids == {'EXP-010', 'EXP-019', 'EXP-031', 'EXP-033', 'EXP-050', 'EXP-064', 'EXP-066', 'EXP-074'}

# Explicit canonical scope ownership removes repeat approvals from the denominator.
# Grouping remains a proposed M-POC1C measurement policy, not owner freeze consent.
canonical = {
    'EXP-001': 'In the reviewed supplied case, Pass-Thru is allowed with LI defending Front, EL marker, no co-attacker, no initial enemy ZOC, a free Rear and an early decision. Initial enemy ZOC excludes it despite later exit. With two defenders both must meet the earlier conditions.',
    'EXP-002': 'For the reviewed supplied Pass-Thru result, defender Pre-Shock +1 DRM; infantry Hits 5 become 2 and EL Hits 3 become 2. Base-0 reduction floor and other modifier order remain unresolved.',
    'EXP-003': 'After supplied no-infantry-Rout and no-EL-Rampage outcomes, place EL in a free defender Rear hex chosen by the EL player, keeping facing. No complete Shock result inferred.',
    'EXP-004': 'The final Pass-Thru TQ check is separate from Pre-Shock; SK are exempt from that final check. For non-SK, positive DR-TQ gives Hits; DR<=TQ gives no excess. No minimum imported from 9.16.',
    'EXP-005': 'Elephant Screen uses the explicitly named Elephant Screen MRRC row and fires only as Reaction Fire, has its own supply markers, and is absent on Leader Elephant. Actual lookup and supply procedure remain context requirements.',
    'EXP-007': 'Ordinary EL Rout triggers immediate Rampage procedure. Ordinary EL roll 0 heads toward nearest friendly unit with opponent choosing a tie; first 7-9 moves away from cause, subsequent 7-9 eliminates. Concrete map and cause are not invented.',
    'EXP-008': 'Leader Elephant roll 0 eliminates it; subsequent 7-9 immediately rallies it with Hits=TQ-2 instead of elimination. This owns the subsequent-roll result; first Leader 7-9 is scored only in EXP-009.',
    'EXP-009': 'First Rampage-table 7-9 for Leader Elephant means movement away from the causing unit, without immediate special rally. Subsequent-roll result is referenced in EXP-008 and earns no second point here. Counting the 4.84 trigger die is unresolved.',
    'EXP-011': 'Complete each Rampage immediately before any other mechanic except OW under 6.51; no concurrent Rampages. Rampaging EL has no ZOC, triggers no Reaction Fire of any kind, and normally cannot rally. The special later Leader result is a reference to EXP-008, not a second scored result.',
    'EXP-012': 'Attempt 3 hexes per directional roll with supplied route/no early termination. At a would-be occupied hex stop adjacent; occupant gets 1 CH via Front, 2 via Flank/Rear, cavalry always 2. Both units of a stack get their Hits. A leader unable to withdraw under 4.72 dies without DR; actual inability requires context.',
    'EXP-016': 'Ordinary EL moving from nonadjacent to adjacent enemy cavalry forces an OW attempt. If cavalry can withdraw, no Reaction Fire; otherwise immediate TQ check, and routed cavalry eliminates without DR in the supplied cannot-withdraw branch. Leader EL excluded. Arithmetic belongs to EXP-017.',
    'EXP-021': 'Velites are LI, not SK; SK exceptions do not transfer by similarity. SK OW incurs Hits only via Rear; Velites via Flank or Rear. OW distance/MA condition belongs to EXP-022.',
    'EXP-022': 'SK may OW up to 2 hexes before an approaching unit with MA equal to or less than SK MA. OW angle costs belong to EXP-021; real routes remain context-dependent.',
    'EXP-024': 'SK cannot Shock attack; units attacking a defense consisting only of SK are exempt from Pre-Shock TQ even with the marker. With mixed defense use the other type and ignore SK Size. This owns the attacker exemption; EXP-004 owns the final Pass-Thru check.',
    'EXP-040': 'When one PH of DD Routs, both Rout and retreat separately. Eliminate each PH individually if it cannot complete legal Rout movement; the other may perform its own legal Rout if possible. Actual geometry, 6.69/10.22, order/shared sole destination and later D1 result are unclosed. Local 10.24/25/23 context is supporting evidence, not an additional scoring unit.',
    'EXP-073': 'Mounted LI uses Mounted Javelin MRRC, is exempt from Missile Supply 8.17 while mounted, removes LOW/NO on mounting, and uses H&D as cavalry. No post-dismount supply state or equivalence with the hypothesized 9.13 row is inferred.',
}
expectations = []
differences = []
for old in old_e['expectations']:
    exp_id = old['id']
    original = draft_e_by_id[exp_id]
    record = {key: copy.deepcopy(old[key]) for key in (
        'id', 'parent_record', 'inventory_refs', 'authorizing_scoped_decisions',
        'unreviewed_fields', 'parent_situation_ids', 'parent_dependency_ids_are_not_automatically_gold')}
    statements = [a['statement'] for a in old['reviewed_assertions']]
    record['reviewed_scope'] = canonical.get(exp_id, ' '.join(statements))
    record['classification'] = 'requires_context' if exp_id in context_ids else 'confirmed_local_content_scope'
    record['whole_parent_record_accepted'] = False
    record['scoring_unit'] = exp_id if exp_id not in context_ids else None
    record['context_requirement_unit'] = exp_id if exp_id in context_ids else None
    record['criticality'] = 'conditional_on_concrete_parameter_use' if exp_id == 'EXP-074' else 'critical_in_reviewed_scope'
    record['evidence'] = copy.deepcopy(original['evidence'])
    record['evidence_review_flags'] = 'Copied historic evidence flags are data; current scope comes only from the authorizing decisions.'
    record['dimensions_reference_only'] = original['dimensions']
    record['limits'] = list(dict.fromkeys(filter(None, [old.get('context_or_unresolved_limit'), original['local_scope_and_needed_context']])))
    record['assembly_policy_reviewed_by_owner'] = False
    expectations.append(record)
    differences.append({'id': exp_id, 'old_assertion_ids': [a['id'] for a in old['reviewed_assertions']],
                        'new_scoring_unit': record['scoring_unit'], 'new_context_requirement_unit': record['context_requirement_unit'],
                        'operation': 'scope consolidation; duplicate approvals are provenance, not new samples',
                        'semantic_owner_approval_extended': False})

exp_artifact = {**header('candidate-expectations-02'), 'source': source,
               'parent': reference(P / 'evaluation/draft/expectations.json'),
               'supersedes_candidate': reference(OLD / 'manifest.json'),
               'counts': {'tracked_ids': 74, 'confirmed_local_content_scope_groups': 66,
                          'requires_context_groups': 8, 'whole_records_accepted': 0},
               'denominator_policy': {'grouped_scope_only': True, 'atomic_norm_count': 'unknown',
                                      'content_grouping_needs_freeze_review': True,
                                      'context_requirements_scored_separately': True,
                                      'all_draft_fields_are_gold': False,
                                      'content_dimensions_need_explicit_scoped_rubric': True},
               'expectations': expectations}
assert Counter(row['classification'] for row in expectations) == {'confirmed_local_content_scope': 66, 'requires_context': 8}
save(NEW / 'expectations.json', exp_artifact)

inventory = read(OLD / 'inventory.json')
inventory.update(header('candidate-inventory-02'))
inventory['supersedes_candidate'] = reference(OLD / 'inventory.json')
inventory['counts']['owner_reviewed_base_structural_records'] = None
inventory['counts']['base_records_not_individually_owner_reviewed'] = None
inventory['counts']['review_coverage_unit'] = 'decision scope; not a claimed count of fully reviewed base records'
for row in inventory['items']:
    row['candidate_review']['scoring_eligible'] = False
inventory['measurement_policy']['rule_completeness_denominator'] = '66 proposed grouped reviewed content scopes; full 41-label/98-clause-group completeness not certified'
save(NEW / 'inventory.json', inventory)

draft_d = read(P / 'evaluation/draft/dependencies.json')
draft_d_map = {row['id']: row for row in draft_d['dependencies']}
old_d = read(OLD / 'dependencies.json')
confirmed = []
scopes = {'DEP-NEW-001': 'Retain both move+Shock gates only.',
          'DEP-NEW-002': 'Subsequent Leader 7-9 special rally only.',
          'DEP-NEW-003': 'Scorpio special Reaction Fire limited by Rampaging EL no-Reaction-Fire condition only.'}
for row in old_d['confirmed_execution_relations']:
    dep_id = row['id']
    confirmed.append({**{key: copy.deepcopy(row[key]) for key in ('id', 'from', 'to', 'kind', 'explicitness', 'evidence', 'parent_record')},
                      'executable': True, 'target_status': 'internal', 'review_status': 'owner_confirmed_exact_scope',
                      'scoring_scope': scopes[dep_id], 'criticality': 'critical_in_reviewed_scope',
                      'necessity_scope': 'Only the stated local relation; no full real-state execution certificate.',
                      'authorizing_refs': row['candidate_review']['provenance']})
tuple_keys = {(row['from'], row['to'], row['kind'], row['explicitness']) for row in confirmed}
assert len(tuple_keys) == 3
excluded = []
for row in draft_d['dependencies']:
    if not row['executable'] or row['id'] in scopes:
        continue
    excluded.append({'id': row['id'], 'classification': 'unresolved_hypothesis' if row['id'] == 'DEP-031' else 'unconfirmed_relation_fields',
                     'explicitness_proposal': row['explicitness'], 'scoring_eligible': False,
                     'context_needed_in_draft': row['status'] == 'requires_context',
                     'parent_record': {**reference(P / 'evaluation/draft/dependencies.json'), 'id': row['id']}})
dep_artifact = {**header('candidate-dependencies-02'), 'source': source,
               'parent': reference(P / 'evaluation/draft/dependencies.json'),
               'counts': {'parent_facets': 127, 'parent_execution_proposals': 113,
                         'parent_explicit_execution_proposals': 99, 'parent_implicit_execution_proposals': 14,
                         'confirmed_explicit_execution': 0, 'confirmed_implicit_execution': 3,
                         'unconfirmed_explicit_execution': 99, 'unconfirmed_implicit_execution': 11,
                         'mentions_separate': 7, 'physical_continuations_separate': 7},
               'metric_denominators': {'explicit': 0, 'implicit': 3, 'explicit_metric': 'n/a',
                                      'implicit_metric': 'n/a until freeze and response; then scoped TP_gold/FN only',
                                      'full_output_precision': 'requires review of every output relation; outside-set pending is neither TP nor certain FP'},
               'confirmed_execution_relations': confirmed,
               'mentions': [{**{key: copy.deepcopy(row[key]) for key in ('id','from','to','target_candidate','kind','explicitness','evidence','parent_record')},
                             'review_status': 'owner_confirmed_mention_occurrence', 'executable': False,
                             'criticality': 'noncritical_at_this_occurrence',
                             'alias_and_external_target_identity_confirmed': False,
                             'owner_decision': reference(R / 'decision-05-RQ-04.json')} for row in old_d['confirmed_mentions']],
               'continuations': [{**{key: copy.deepcopy(row[key]) for key in ('id','from','to','kind','evidence','parent_record')},
                                  'classification': 'physical_source_continuation', 'execution_gold': False,
                                  'whole_record_owner_accepted': False} for row in old_d['physical_continuations']],
               'unconfirmed_execution_candidates': excluded,
               'pending_internal_explicit_tuple_review': ['DEP-008','DEP-002','DEP-017','DEP-024','DEP-041'],
               'freeze_readiness': 'incomplete: explicit reviewed denominator missing; no change to POC-PLAN authorized'}
save(NEW / 'dependencies.json', dep_artifact)

situations = read(OLD / 'situations.json')
situations.update(header('candidate-situations-02'))
for row in situations['situations']:
    refs = row['overlay_provenance']
    overlay = read(ROOT / refs['path'])
    decision_path = R / overlay['authorizing_decision']
    row['authorizing_decision'] = reference(decision_path)
    row['criticality_basis'] = reference(R / 'decision-24-RQ-15e-closing.json') if row['id'] in {'SIT-05','SIT-07'} else reference(decision_path)
    row['criticality_author'] = 'owner for the stated local scope; exact decision attached'
    if row['id'] == 'SIT-04':
        row['expected']['result'] = 'Ordinary EL: first DR8 moves away from cause and attempts 3 hexes under supplied route/no early termination; subsequent DR8 eliminates. First Leader 7-9 is outside this situation.'
        row['expected']['rationale'] = 'Decision 15 accepts ordinary EL first/subsequent result; later decision 21 resolves a separate Leader case, without adding a situation.'
assert Counter(row['expected']['kind'] for row in situations['situations']) == {'local_result': 17, 'justified_block': 3}
save(NEW / 'situations.json', situations)

save(NEW / 'change-map.json', {'previous_candidate': reference(OLD / 'manifest.json'), 'current_candidate': NEW.name,
                             'operations': differences, 'new_owner_decisions': [], 'originals_modified': [],
                             'retired_claims': ['86 unique confirmed assertions', '29 fully reviewed base inventory records',
                                                'candidate 01 ready for freeze', 'all copied draft metadata owner-confirmed']})

question_dep = draft_d_map['DEP-008']
inv = read(P / 'evaluation/draft/inventory.json')
target = next(row for row in inv['items'] if row['id'] == question_dep['to'])
question = {'id': 'M-POC1C-RQ-01-DEP008', 'status': 'waiting_owner_decision',
            'topic': 'missing explicit relation tuple confirmation only',
            'source_quote': question_dep['evidence'][0], 'target_quote': target['evidence'][0],
            'proposed_tuple': {key: question_dep[key] for key in ('id','from','to','kind','explicitness')},
            'proposed_necessity_scope': 'Exception linking SK to the final Pass-Thru check exemption only; no other TQ tests or full external procedure.',
            'proposed_criticality': 'critical: losing the exception wrongly requires a final SK TQ check',
            'previous_decision_scope': reference(R / 'decision-04-RQ-03.json'),
            'missing_fields': ['exact target identity and scope', 'kind', 'explicitness', 'necessity_scope'],
            'freeze_authorization_requested': False, 'actual_owner_answer': None}
save(HERE / 'pending-question.json', question)

save(HERE / 'audit.json', {'card': 'M-POC1C', 'recorded_at_utc': now,
                         'branch': branch, 'head': head, 'source': source,
                         'B_manifest_refs_checked': len(checked), 'B_manifest_hash_mismatches': failures,
                         'previous_candidate_manifest': reference(OLD / 'manifest.json'),
                         'previous_candidate_files_and_parents_hashes_valid': True,
                         'candidate_01_semantic_findings': [
                             '86 is a count of overlapping review fragments, not a checked unique scoring denominator.',
                             'EXP-021 and EXP-022 repeated the same combined statement.',
                             'EXP-008 repeated the later Leader result and retained obsolete first-roll pending wording.',
                             'EXP-073 repeated an MRRC assertion and retained obsolete partial review language.',
                             'Full inventory review cannot be inferred from membership in a hand-selected 29-ID list.',
                             'Inherited relation human_review/necessity fields were historical proposals.',
                             'Freezing an incomplete diagnostic set would not meet the present card/plan.'],
                         'new_candidate': NEW.name, 'new_candidate_freeze_ready': False,
                         'owner_message_received': 'Podbiłem model na sol',
                         'interpretation_of_owner_message': 'User reports selector change; no semantic decision or freeze authorization.',
                         'actual_model_selector': 'sol (owner report; exact version unknown)',
                         'reasoning_selector': 'unknown', 'active_work_time': 'unknown',
                         'user_active_time': 'unknown', 'tokens': 'unknown', 'cost': 'unknown',
                         'required_check_status': 'pending; will be recorded separately in completion.json',
                         'historical_git_snapshot_policy': 'HEAD/index in B manifests are historical; the supplied current baseline is authoritative, no restore.',
                         'no_freeze_or_extraction': True})
print(json.dumps({'new_candidate': NEW.relative_to(ROOT).as_posix(), 'counts': exp_artifact['counts'],
                  'relations': dep_artifact['counts'], 'manifest_refs_valid': len(checked),
                  'audit_sha256': digest(HERE / 'audit.json')}, indent=2))
