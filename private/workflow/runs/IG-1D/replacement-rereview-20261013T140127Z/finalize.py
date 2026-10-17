"""Freeze a complete replacement review with exact evidence and no queue transition."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
BASE = ROOT / 'private/workflow/runs/IG-1D'
ACTOR = 'ig1d-replacement-reviewer-20261013T140127Z'

def read(p): return json.loads(p.read_bytes())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def artifact(p): return {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
def write(name, data):
    with (RUN / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')

before, after = read(RUN / 'verification-before.json'), read(RUN / 'verification-after.json')
assert before['all_match'] and after['all_match']
assert before['reviewed_delivery'] == after['reviewed_delivery']
assert before['queue_sha256'] == after['queue_sha256']
config = read(RUN / 'configuration-confirmed.json')
assert config['model'] == 'gpt-6.1-sol' and config['reasoning'] == 'high'
audit = read(RUN / 'independent-accounting.json')
supplement = read(RUN / 'supplemental-accounting.json')
assert audit['result'] == supplement['result'] == 'pass'
checks = [read(p) for p in sorted(RUN.glob('*-check.json'))]
by_name = {p.name.removesuffix('-check.json'): read(p) for p in RUN.glob('*-check.json')}
for key in ['original-native', 'explicit-native', 'history', 'accounting-native', 'project', 'diff']:
    assert by_name[key]['exit_code'] == 0
assert by_name['risk']['exit_code'] == 1
assert '1 failed, 9 passed' in (RUN / 'risk.log').read_text()
assert 'test_named_merge_receipt_changed_child_kind_is_not_silently_reallocated' in (RUN / 'risk.log').read_text()
assert 'WinError 5' in (RUN / 'accounting.log').read_text()
checks.append({'command': '.venv/Scripts/python.exe -B ' + (RUN / 'supplemental_audit.py').relative_to(ROOT).as_posix(),
    'exit_code': 0, 'start_utc': supplement['started_utc'], 'end_utc': supplement['ended_utc'],
    'wall_seconds': supplement['wall_seconds'], 'result': artifact(RUN / 'supplemental-accounting.json'),
    'capture_note': 'Direct tool completion exit 0; command output also included in result JSON. No separate stdout log.'})
write('checks.json', checks)

finding = {
    'id': 'IG1D-R04', 'priority': 'P2', 'repair_iteration_reviewed': 1, 'maximum_repair_iterations': 2,
    'remaining_repair_iterations': 1, 'disposition': 'partially_repaired_changes_required',
    'title': 'Validate the persisted named child contract before filtering receipt children',
    'location': {'path': 'src/wgc/wgu_adapter/identity.py', 'start': 139, 'end': 147},
    'related_location': {'path': 'src/wgc/wgu_adapter/identity.py', 'start': 230, 'end': 239},
    'consequence': 'The named receipt key pins decision_id, operation, sorted parent IDs and basis, but does not pin the typed child contract. The replay branch filters existing children by current kind and scope before deciding whether prior children exist. Reusing a one-child merge receipt for a term-to-rule change filters away the persisted child and silently allocates a replacement under the same named receipt, with no contract conflict. Persisted lineage decision provenance becomes inconsistent.',
    'reproducer': 'Merge North/South terms into one Together term using decision_id merge-child-contract. Reuse its decision ID, operation, parent IDs and basis with the child locator changed from /terms/0 to /rules/0, supplying a rule child R-Together. The current result assigns the new rule child instead of rejecting or leaving an explicit unresolved contract conflict.',
    'evidence': {'test': 'receipt_edge_probes.py::test_named_merge_receipt_changed_child_kind_is_not_silently_reallocated',
        'log': artifact(RUN / 'risk.log'), 'check': artifact(RUN / 'risk-check.json'),
        'observed': 'The unchanged assertion requiring every assignment to have no ids and a gap_id fails; no ValueError rejects changed receipt reuse.',
        'execution_count_this_review': 1, 'assertions_preserved': True},
    'expected_result_justification': 'Original R04 requires reuse of the persisted receipt/decision with the exact child contract, and verification of changed/colliding decision rejection. Logical kind and parent scope already discriminate persisted children. A same-named output cannot acquire an incompatible kind contract merely because a filter hid its previous allocation. This is an identity/provenance boundary independent of publisher meaning.',
    'repaired_behavior': 'Unique merged-child content correction, rename, further correction, origin history, origin_key, unchanged replay and exact historical parent/child revision closure pass. Those behaviors must remain intact.',
    'required_change': 'For the bounded second repair, compare the persisted named child contract before filtering prior receipt children and before allocating a replacement. Preserve logical kind, parent scope and persistent child-key contract independently of locators, list positions and corrected content. Reject incompatible same-ID reuse atomically, or return an explicit unresolved receipt-contract gap retaining the prior allocation and new observation. Use a separately named decision for a deliberately different child contract.',
    'required_verification': [
        'Preserve all 15 original probes and every existing risk, receipt-edge and export-history assertion unchanged.',
        'Make the unchanged changed-child-kind receipt control reject or return an explicit unresolved conflict, with prior registry/bundle immutable.',
        'Add meaningful controls for relevant logical scope and persistent child-key contract changes, plus a new decision identifier for a deliberately different output contract; do not blanket-reject valid new decisions.',
        'Retain correction/rename, allocation and origin_key stability, exact parent/child revision history, unchanged replay, keyed indistinguishable split children and multi-child ambiguity.',
        'Preserve R01-R03 closure and all source/foundation/prior-review bytes; freeze iteration 1 before a separate bounded iteration-2 claim.',
        'Rerun adapter/export suites, unchanged original/risk/history probes, complete independent raw/field/binding/reference accounting, two full canonical transforms/publications, scripts/check.ps1 -Task IG-1D and git diff --check; obtain independent re-review of the new exact hashes.'
    ],
    'new_finding': False, 'retry_policy': 'One reproduction in this replacement review; no unchanged defect retry. Repair cycle 1 of maximum 2 has been consumed.'}

dispositions = [
    {'finding_id': 'IG1D-R01', 'disposition': 'closed', 'repair_iteration_reviewed': 1,
        'basis': 'The current rematch phase builds label/endpoint/number and substantive evidence maps against the same available prior IDs before those heuristic assignments. Contradictions create gaps and reserve candidates. The unchanged two-term control, independent local and three-way conflicts, candidate/origin retention, explicit no-allocation resolution, non-term step conflict and unambiguous edits/reorder/insertion/deletion/move/rename controls pass.',
        'evidence': ['original-native.log', 'risk.log', 'explicit-native.log'],
        'fixture_assessment': 'The public step insertion/renumber test now supplies explicit authoring hints for contradictory number/body evidence. Its exact prior-ID assertions remain unchanged; separate strict negative controls require gaps without hints. This fixture adjustment is consistent with R01, and original reviewer assertions remain byte-identical.'},
    {'finding_id': 'IG1D-R02', 'disposition': 'closed', 'repair_iteration_reviewed': 1,
        'basis': 'Validation rejects every locator shared by hints and forced lineage before assignments and operates on a deep copy of previous state. Split and merge conflict controls pass with prior registry immutability. Disjoint hints/lineage, many-to-many bindings, keyed children and unchanged replay pass. Compatible overlap is deliberately unsupported, so no duplicated-decision precedence is silently assumed.',
        'evidence': ['original-native.log', 'risk.log', 'explicit-native.log']},
    {'finding_id': 'IG1D-R03', 'disposition': 'closed', 'repair_iteration_reviewed': 1,
        'basis': 'Resolution unions exact active IDs with active aliases and accepts only a singleton. Original exact-ID, independent direct relation endpoints/navigation-cycle, retired/nonexistent-ID and direct-ID/alias collision controls pass. Explicit scope and both-endpoint controls pass. Full raw-input enumeration independently reproduces every diagnostic target/candidate set and cycle component.',
        'evidence': ['original-native.log', 'risk.log', 'explicit-native.log', 'supplemental-accounting.json']},
    {'finding_id': 'IG1D-R04', 'disposition': 'partially_repaired_changes_required', 'repair_iteration_reviewed': 1,
        'basis': finding['repaired_behavior'], 'remaining_requirement': finding['required_change'],
        'evidence': ['original-native.log', 'risk.log', 'history.log', 'explicit-native.log']}
]
write('findings.json', [finding])
write('dispositions.json', {'technical_result': 'changes_requested', 'actor': ACTOR,
    'repair_iteration_reviewed': 1, 'maximum_repair_iterations': 2, 'dispositions': dispositions,
    'remaining_findings': [finding], 'new_finding_ids': [], 'product_modified_by_reviewer': False})
with (RUN / 'expectations.md').open('x', encoding='utf-8') as f:
    f.write('# Replacement technical review expectations\n\nThe original four findings were read from the frozen review.json. Expected identity behavior is grounded in the task and original R04 exact-child-contract requirement, not the implementation output or previous dispositions. A single unchanged named receipt with the same operation, parents and basis cannot silently describe an incompatible typed child output. Rejection or an explicit unresolved conflict is allowed. A deliberately different contract can use a new decision identifier. Text correction/rename keeps identity within the same child contract.\n\nOriginal probes are executed at their exact preserved paths. Risk/receipt/history probes are exact byte copies. The full accounting helper changes only its operational reviewer identity; its output directory is inferred from its new path. Every old assertion is preserved. The supplemental oracle independently enumerates raw YAML, unknown subtrees, current reference declarations/targets and SCCs; no importer counters or production reference function establish expected answers.\n\nThe public step renumber fixture retains its original ID assertions and adds explicit hints under contradictory number/body evidence. Separate unchanged negative controls enforce gaps without hints. No source or gameplay meaning is accepted.\n')

delivery = read(BASE / 'repair-01-20261013/delivery.json')
write('reviewed-artifact-manifest.json', {'format': 'wgc-reviewed-artifacts-1', 'task': 'IG-1D',
    'actor': ACTOR, 'delivery': artifact(BASE / 'repair-01-20261013/delivery.json'),
    'artifact_count': len(delivery['artifacts']), 'artifacts': delivery['artifacts'],
    'before_verification': artifact(RUN / 'verification-before.json'),
    'after_verification': artifact(RUN / 'verification-after.json'), 'all_exact_bytes_match': True})
ended = datetime.now(timezone.utc)
start = read(RUN / 'checkpoint.json')['evidence_run_started_utc']
measurements = {'started_utc': start, 'ended_utc': ended.isoformat(),
    'wall_seconds': (ended - datetime.fromisoformat(start)).total_seconds(),
    'measurement_scope': 'Measured evidence run. Earlier instruction reading was not timed and is excluded; see measurement-correction.json. Individual commands and full accounting have their own actual UTC and monotonic wall measurements.',
    'tokens': None, 'cost': None, 'operator_seconds': None}
write('measurement.json', measurements)
project_log = (RUN / 'project.log').read_text()
project_root = Path(re.search(r'LOG_ROOT=(.+)', project_log).group(1).strip())
project_files = [artifact(p) for p in sorted(project_root.rglob('*')) if p.is_file() and p.suffix in ['.json', '.log']]
write('project-evidence.json', {'files': project_files, 'check': artifact(RUN / 'project-check.json')})
summary = 'Independent replacement review of frozen IG-1D repair iteration 1: R01-R03 closed; R04 partially repaired but same-named changed child-kind contract silently reallocates. Changes requested for one bounded second repair. Full structural accounting and reproducibility pass; no semantic, publisher-coverage or executable acceptance.'
report = f'''# IG-1D repair iteration 1 replacement technical review

Result: **changes_requested**. R01, R02 and R03 are closed. R04's correction/rename behavior is fixed, but its exact named child-contract boundary remains incomplete. No new finding ID was introduced. One P2 finding remains, with one bounded repair iteration available (iteration 1 of maximum 2 already used).

Reviewer: `{ACTOR}`, distinct from executor `ig1-stage-executor-20261013` and the unavailable previous reviewer. Actual configuration: GPT-6.1 Sol / high, freshly confirmed by the operator in this replacement chat (`potwierdzam`), recorded in configuration-confirmed.json. Previous reviewer/executor confirmation was not used as proof. This review uses the operator-authorized replacement exception; the previous re-review has no final review.json and was never treated as accepted.

Reviewed delivery: private/workflow/runs/IG-1D/repair-01-20261013/delivery.json, SHA256 `3ebef08719717c41043cb4df8bb98874d214e38d0e8fdbf21de6e35a9adfaa73`, exactly 50 artifacts, enumerated in reviewed-artifact-manifest.json and review.json. Every exact byte matched before and after review. The 119 checkpoint entries were verified through each verified_path; 69 parent versions, 182 foundation artifacts, 42 prior review artifacts, 43 prior review-manifest artifacts and all 36 previous re-review files also matched. Queue SHA256 remained `07cb9707259e91d1f779360ba4eb8606a3d2ae51502aaba53c4961a7e264e1e3`: IG-1A/B/C done, IG-1D review, IG-1E planned.

R04: identity.py:139-147 guards decision ID/operation/parents/basis, while identity.py:230-239 filters receipt children by kind/scope before deciding to allocate. Replaying a term merge receipt as a rule child filters out the old term; the empty candidate set allocates another child under the same named receipt. The unchanged receipt_edge_probes.py::test_named_merge_receipt_changed_child_kind_is_not_silently_reallocated fails once. This violates original R04's exact child-contract and changed/colliding-decision boundary. Require an atomic rejection or explicit retained conflict before allocation, with independent logical kind/scope/persistent-key checking and controls for deliberately new decision IDs. Preserve valid text correction/rename and keyed/multiple-child behavior. Detailed bounded requirements are in findings.json and dispositions.json.

R01 closure: contradictory term and step evidence retains candidates/origins as gaps; local and three-way controls pass, explicit hints resolve without extra allocation, and ordinary edit/reorder/rename/move controls pass. The public step-renumber fixture adds explicit authoring hints while retaining exact prior-ID assertions; strict negative gap controls remain. R02 closure: overlap is rejected before assignment with unchanged prior state; disjoint/many-to-many/lineage replay pass. R03 closure: exact active IDs and aliases use a singleton union, retaining ambiguity and excluding retired IDs; endpoint/navigation/scope/cycle/no-approval controls and full independently reconstructed diagnostics pass.

Validation:

- Public adapter/export suites: 93 passed, native execution exit 0.
- All 15 original reviewer probes: 15 passed, native execution exit 0, original bytes unchanged.
- Existing risk/receipt-edge probes: 9 passed, 1 failed (R04), exit 1; no unchanged defect retry.
- Existing export-history probes: 2 passed, exit 0.
- Required scripts/check.ps1 -Task IG-1D: 102 passed, exit 0; queue validation and dry-run passed.
- git diff --check: exit 0.
- Full independent accounting/two complete canonical transforms and publications: exit 0.
- Supplemental raw YAML unknown-location/reference/cycle oracle: exit 0.

Initial sandbox runs are retained: adapter/export 91 passed and 2 WinError 5 failures; original probes 14 passed and 1 WinError 5 failure; full accounting stopped with WinError 5 before inventory. Narrow local native runs with fresh directories passed all those unchanged assertions. No no-follow bypass, reinstall, or global configuration change was made. Exact argv, process-local PYTHONPATH, UTC, wall time and all exit codes/failures are in checks.json and individual logs. Cache disabled; fresh short basetemp per run.

Independent accounting measured {audit['independent_record_count']:,} records and {audit['independent_field_count']:,} YAML field/container locations across {audit['manifest_entries']} manifest entries ({audit['available_files']} available, {audit['missing_sources']} configured sources missing). It verified exact raw bytes, every entity value/parent/origin observation, {audit['binding_count']:,} binding subtrees, aspect/record hashes and selected/historical reference closure. The frozen package has {audit['source_graph_records']:,} source graph records and {supplement['identity_count']:,} identities. Supplemental inspection independently found {supplement['unknown_root_count']} unknown roots encompassing {supplement['unknown_field_container_location_count']:,} field/container locations, reconstructed {supplement['independent_reference_diagnostic_count']:,} diagnostics ({supplement['reference_status_counts']['resolved']:,} resolved, {supplement['reference_status_counts']['unresolved']} unresolved) and independently matched cycle components. Counts follow enumerated raw inputs; importer counters were only cross-checked afterwards.

The selected current canonical package is `sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc`, taken from repair-01-20261013/full-export-accounting-final.json. Fresh seeded transform equals those exact canonical files; repeated transform and two real publications are byte-identical. Publications use separate actual operational sidecars under this review run. The operator-approved wgc-source-export-1 profile retains null canonical timestamps; original source-v1 schema/validator bytes remain frozen.

Measured evidence run: {measurements['started_utc']} to {measurements['ended_utc']}; {measurements['wall_seconds']:.3f} seconds. Earlier read-only instruction inspection was unmeasured and excluded. Full accounting wall time: {audit['wall_seconds']:.3f} seconds. Tokens, cost and operator time are null. Configuration initially null was replaced only by a fresh operator-confirmation artifact, without overwriting the checkpoint.

Remaining gates: bounded R04 iteration-2 claim/repair, exact new delivery, independent re-review, then coordinator technical acceptance/done. IG-1E remains planned and was not run. Publisher coverage, source meaning/human semantic acceptance and executable readiness are separate and not granted; mixed-edition uncertainty and missing originals remain. The product, public tests, queue, generated documents and prior evidence were not modified. No commit, push, new chat, agent, worktree, automation, neighbouring repository access, Git/archive history inspection or external API was used.

All final review evidence is frozen by review-manifest.json; final-seal.json separately pins review.json and review-manifest.json to avoid circular hashes. The reviewer did not change queue state; the coordinator owns any later transition.
'''
with (RUN / 'report.md').open('x', encoding='utf-8') as f: f.write(report)
evidence = [artifact(p) for p in sorted(RUN.rglob('*')) if p.is_file()]
review = {'role': 'reviewer', 'actor': ACTOR, 'executor_actor': 'ig1-stage-executor-20261013',
    'task': 'IG-1D', 'summary': summary, 'technical_result': 'changes_requested',
    'technical_pass': False, 'independent_pass': False, 'review_finalized': True,
    'requested_model': 'gpt-6.1-sol', 'requested_reasoning': 'high',
    'model': config['model'], 'reasoning': config['reasoning'],
    'configuration_evidence': artifact(RUN / 'configuration-confirmed.json'),
    'replacement_reviewer_exception': 'Direct operator assignment replaces unavailable archived reviewer finalization, without inheriting its acceptance or configuration.',
    'reviewed_delivery': {**artifact(BASE / 'repair-01-20261013/delivery.json'), 'artifact_count': 50, 'artifacts': delivery['artifacts']},
    'reviewed_artifact_manifest': artifact(RUN / 'reviewed-artifact-manifest.json'),
    'original_review': artifact(BASE / 'review-20261013T122807Z/review.json'),
    'prior_unfinalized_rereview': {'path': 'private/workflow/runs/IG-1D/rereview-20261013T131151Z', 'final_review_exists': False, 'accepted': False},
    'current_packet': after['packet'], 'queue_sha256_before': before['queue_sha256'], 'queue_sha256_after': after['queue_sha256'],
    'criteria': delivery['criteria'], 'criteria_results': [
        {'criterion': delivery['criteria'][0], 'result': 'pass_for_frozen_corpus_and_unchanged_inputs', 'limitation': 'Changed named lineage contract boundary remains R04.'},
        {'criterion': delivery['criteria'][1], 'result': 'pass_for_reviewed_controls'},
        {'criterion': delivery['criteria'][2], 'result': 'pass_for_reviewed_controls_and_full_frozen_corpus'},
        {'criterion': delivery['criteria'][3], 'result': 'pass_for_reviewed_controls_and_full_frozen_corpus'}],
    'findings': [finding], 'dispositions': dispositions, 'new_finding_ids': [],
    'defect_counts': {'P0': 0, 'P1': 0, 'P2': 1, 'P3': 0},
    'repair_iteration_reviewed': 1, 'maximum_repair_iterations': 2, 'remaining_repair_iterations': 1,
    'checks': checks, 'artifacts': evidence,
    'full_accounting': {k: v for k, v in audit.items() if k not in ['ledger', 'binding_ledger', 'unknown_locations', 'publications']},
    'supplemental_accounting': {k: v for k, v in supplement.items() if k not in ['unknown_roots', 'diagnostics', 'cycles']},
    'before_verification': artifact(RUN / 'verification-before.json'), 'after_verification': artifact(RUN / 'verification-after.json'),
    'all_exact_reviewed_bytes_preserved': True, 'all_prior_foundation_versions_preserved': True,
    'product_modified_by_reviewer': False, 'queue_modified_by_reviewer': False,
    'measurement': measurements, 'semantic_acceptance_granted': False,
    'publisher_source_coverage_granted': False, 'executable_readiness_granted': False,
    'remaining_gates': ['Bounded R04 iteration-2 claim and repair', 'New frozen delivery and independent re-review', 'Coordinator technical acceptance and done', 'Separate publisher coverage, human meaning acceptance and executable readiness'],
    'next_exact_action': 'Coordinator verifies this frozen changes_requested review and, if proceeding, claims only the bounded second R04 repair under a new attempt preserving iteration-1 bytes. Do not run IG-1E or IG-2 in this reviewer chat.',
    'final_manifest_path': (RUN / 'review-manifest.json').relative_to(ROOT).as_posix()}
write('review.json', review)
manifest_artifacts = [artifact(p) for p in sorted(RUN.rglob('*')) if p.is_file()]
write('review-manifest.json', {'format': 'wgc-review-manifest-1', 'task': 'IG-1D', 'actor': ACTOR,
    'technical_result': 'changes_requested', 'artifacts': manifest_artifacts,
    'reviewed_delivery': artifact(BASE / 'repair-01-20261013/delivery.json'),
    'reviewed_artifacts': delivery['artifacts'], 'external_project_evidence': project_files,
    'self_hash_policy': 'Manifest excludes itself and final-seal.json; final-seal pins both final review and manifest.'})
write('final-seal.json', {'format': 'wgc-review-seal-1', 'actor': ACTOR,
    'utc': datetime.now(timezone.utc).isoformat(), 'technical_result': 'changes_requested',
    'review': artifact(RUN / 'review.json'), 'manifest': artifact(RUN / 'review-manifest.json'),
    'report': artifact(RUN / 'report.md'), 'reviewed_artifact_manifest': artifact(RUN / 'reviewed-artifact-manifest.json')})
# Re-read every frozen reviewed/evidence artifact after finalization, without changing it.
for a in manifest_artifacts + delivery['artifacts'] + project_files:
    assert sha(ROOT / a['path']) == a['sha256']
for a in read(RUN / 'final-seal.json').values():
    if isinstance(a, dict) and 'sha256' in a: assert sha(ROOT / a['path']) == a['sha256']
print(json.dumps({'result': 'changes_requested', 'review': artifact(RUN / 'review.json'),
    'manifest': artifact(RUN / 'review-manifest.json'), 'seal': artifact(RUN / 'final-seal.json'),
    'review_artifacts': len(manifest_artifacts), 'reviewed_delivery_artifacts': 50, 'final_hash_recheck': 'pass'}))
