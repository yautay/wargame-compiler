import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
CONFIG = ROOT / 'private/workflow/runs/IG-1C/review-20261013T071955Z/configuration-confirmed.json'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def ref(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)}

def write(name, data):
    with (RUN / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(data, stream, indent=2, ensure_ascii=False)
        stream.write('\n')

before, after = read(RUN / 'verification-before.json'), read(RUN / 'verification-after.json')
for key in ['delivery', 'artifacts', 'parent_preservation', 'prior_review_artifacts', 'prior_review_manifest_artifacts', 'foundation', 'packet', 'external_support', 'installed_wheel_files']:
    assert before[key] == after[key], key
assert after['all_match'] and after['embedded_schema_equals_exact_pin']
for a in after['artifacts']:
    assert sha(ROOT / a['path']) == a['sha256']
for category in ['parent_preservation', 'prior_review_artifacts', 'prior_review_manifest_artifacts', 'foundation']:
    for a in after[category]:
        assert sha(ROOT / a['verified_path']) == a['sha256']
configuration = read(CONFIG)
assert configuration['model'] == 'gpt-6.1-sol' and configuration['reasoning'] == 'high'
write('configuration.json', {'model': 'gpt-6.1-sol', 'reasoning': 'high', 'requested_model': 'gpt-6.1-sol', 'requested_reasoning': 'high', 'configuration_source': configuration['configuration_evidence'], 'original_confirmation': ref(CONFIG), 'same_independent_reviewer_chat': True, 'session_continuity': 'Earlier direct current-reviewer-chat operator UI confirmation remains applicable in this same ongoing reviewer chat; no configuration change requested or observed. Executor configuration is not used as proof.', 'runtime_metadata': None})
checks = [read(RUN / (name + '-check.json')) for name in ['original-probes', 'risk-probes', 'metadata-edges', 'adapter', 'affected', 'accounting', 'project', 'diff']]
assert all(c['exit_code'] == 0 for c in checks)
checks += [
    {'command': '.venv/Scripts/python.exe scripts/workflow.py validate', 'exit_code': 0, 'wall_seconds': 2.5712853},
    {'command': '.venv/Scripts/python.exe scripts/workflow.py packet --task IG-1C', 'exit_code': 0, 'wall_seconds': 4.344839, 'packet': after['packet']},
    {'command': '.venv/Scripts/python.exe -B private/workflow/runs/IG-1C/rereview-20261013T100001Z/verify_v2.py before', 'exit_code': 0, 'wall_seconds': 3.0936176},
    {'command': '.venv/Scripts/python.exe -B private/workflow/runs/IG-1C/rereview-20261013T100001Z/verify_v2.py after', 'exit_code': 0, 'wall_seconds': 3.7414439},
    {'command': 'Independent old/new full import compatibility comparison', 'exit_code': 0, 'wall_seconds': 1.4858492, 'report': ref(RUN / 'import-compatibility.json')},
]
accounting = read(RUN / 'independent-accounting.json')
assert accounting['result'] == 'pass'
project = ROOT / 'private/workflow/checks/active-ed49567acc5543f1a63b255664d20154'
project_result = read(project / 'result.json')
assert all(project_result[k] == 0 for k in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'])
queue = read(ROOT / 'docs/work/queue.json')
task = next(t for t in queue['tasks'] if t['id'] == 'IG-1C')
assert task['status'] == 'review'
assert all(next(t for t in queue['tasks'] if t['id'] == i)['status'] == 'planned' for i in ['IG-1D', 'IG-1E'])
dispositions = [
    {'finding_id': 'IG1C-R01', 'disposition': 'closed', 'repair_iteration': 1, 'maximum': 2,
     'reviewed_location': {'path': 'src/wgc/wgu_adapter/parser.py', 'start': 36, 'end': 54},
     'basis': 'Unchanged malformed bool/timestamp/int/float probes pass. Six new explicit scalar cases include invalid calendar values and binary Unicode; each returns exactly one raw-preserved error with escaped field pointer and exact line/column. Independent multi-file snapshot preserves both malformed files and all following valid/raw files. Unrelated string constructor KeyError still propagates.',
     'independent_controls': ['original-probes.log', 'risk-probes.log'], 'required_verification_complete': True},
    {'finding_id': 'IG1C-R02', 'disposition': 'closed', 'repair_iteration': 1, 'maximum': 2,
     'reviewed_location': {'path': 'src/wgc/wgu_adapter/importer.py', 'start': 45, 'end': 77},
     'basis': 'Embedded schema exactly equals the pinned WGU schema, independently extracted from a literal JSON AST without executing product code. All four original optional-field counterexamples pass. Fourteen new nested/file type/enum cases and three missing-manifest metadata cases produce located structural errors; missing chapter metadata uses its parent location. Valid extensions, unconstrained data and integer/string step numbering survive, while bool numbering fails. Complete actual corpus has zero errors and unchanged full field/record ledger.',
     'independent_controls': ['verification-before.json', 'original-probes.log', 'risk-probes.log', 'metadata-edges.log', 'independent-accounting.json'], 'required_verification_complete': True},
    {'finding_id': 'IG1C-R03', 'disposition': 'closed', 'repair_iteration': 1, 'maximum': 2,
     'reviewed_location': {'path': 'src/wgc/wgu_adapter/importer.py', 'start': 102, 'end': 116},
     'basis': 'Original scalar-confusables probe passes unchanged. New heterogeneous null/bool/integer/empty-string/list/mapping entries retain exact values without false errors; incidental confusable IDs do not cause duplicate entity identities. Genuine entity-record errors and cross-file/nested duplicate IDs remain covered by unchanged strict probes. Full actual corpus mappings/raw bytes remain unchanged.',
     'independent_controls': ['original-probes.log', 'risk-probes.log', 'independent-accounting.json', 'import-compatibility.json'], 'required_verification_complete': True},
]
write('finding-dispositions.json', {'result': 'pass', 'parent_review': after['parent_review'], 'dispositions': dispositions, 'remaining_findings': [], 'new_findings': [], 'product_repair_iterations_reviewed': 1, 'reviewer_product_edits': False})
started = datetime.fromisoformat('2026-10-13T10:00:01+00:00')
ended = datetime.now(timezone.utc)
measurements = {'start_utc': started.isoformat(), 'end_utc': ended.isoformat(), 'wall_seconds': (ended - started).total_seconds(), 'interval': 'Same-chat first bounded repair re-review including tool waits and reviewer harness corrections; earlier review/configuration waiting excluded.', 'input_tokens': None, 'output_tokens': None, 'cost': None, 'operator_time_seconds': None, 'native_file_symlink': None, 'native_directory_symlink': None, 'native_windows_junctions': 'Actual Windows junction rejection and redirected-handle tests passed in tests/inputs; no symlink claim.', 'defects_remaining_by_priority': {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0}, 'prior_P2_findings_closed': 3, 'new_findings': 0, 'tests': {'unchanged_reviewer_probes_passed': 35, 'new_risk_probes_passed': 24, 'new_metadata_edge_probes_passed': 3, 'adapter_tests_passed': 59, 'affected_input_tests_passed': 51, 'project_tests_passed': 102}}
write('measurements.json', measurements)
report = '''# IG-1C first repair independent re-review: technical PASS

**IG1C-R01, IG1C-R02 and IG1C-R03 are closed after repair iteration 1 of maximum 2.** The unchanged original probes and independently added affected-risk controls pass; no remaining or new technical finding was identified within this review scope. This is technical review only. No human semantic acceptance, publisher-source coverage or executable readiness is granted, and no queue transition or IG-1D work was performed.

## Exact delivery, reviewer and preservation

Reviewed delivery: `private/workflow/runs/IG-1C/repair-01-20261013/delivery.json`, SHA-256 `5392446d5e9d2112b048d4b74030b6a8790fd1848d2de1df4812590decedd7ad`. Its complete **34-artifact** list is embedded in review.json and independently rehashed before/after review. All hashes match. Parent delivery is `private/workflow/runs/IG-1C/resume-20261013/delivery.json`, SHA-256 `aefeac57292fcb742e8f7263d2ed30af56af01fd1da8282bc7e4baa3c78742b8`; parent review is `private/workflow/runs/IG-1C/review-20261013T092949Z/review.json`, SHA-256 `333ca0ae84342bffc103045c5ad1ea1ee2dbc8f104764d2ce4db2255a8c0f48e`.

All **53 parent artifact versions** are preserved and verified. The three replaced source/test files are checked against the explicit baseline mapping, not obsolete hashes demanded at live repaired paths. All **40 prior reviewer artifact references**, the prior reviewer manifest's 34 entries and **148 accepted foundation references** remain unchanged. Hash-only checks use exact current preservation references; no prior completed-task packet/dry-run or historical/Git/past-chat context was reopened. All four exactly scoped external support files and 23 installed non-RECORD PyYAML wheel files retain their pins.

Reviewer actor remains `ig1c-reviewer-20261013T071955Z`, distinct from executor `ig1-stage-executor-20261013`. Actual reviewer `gpt-6.1-sol` / `high` comes from the earlier direct operator observation of THIS reviewer chat UI, retained in this same ongoing chat. No configuration change was requested/observed; executor configuration is not proof. configuration.json pins the original confirmation. Usage/cost/operator time are unavailable/null.

Fresh reviewer packet: `private/workflow/packets/IG-1C-e53938d9f57544e8a8bd52c12430be50/manifest.json`. Its queue, context, named-file hashes/sizes were verified. Its complete context bytes are identical to the already fully read prior reviewer packet; unchanged named context is retained, and current manifest/card/delivery/source/regressions are inspected. The active skill remains docs/skills/wgc-review/SKILL.md. Queue is review; IG-1D/E are planned.

## Independent finding dispositions

**R01 — closed.** Built-in scalar-constructor failures are normalized within the scalar-tag boundary. Node pointers are inventoried before construction. All original malformed-tag assertions pass unchanged. Six new scalar cases check exact escaped pointers, CRLF line/column and raw bytes, including invalid calendar timestamp and malformed binary Unicode. A separately constructed canonical multi-file snapshot verifies both malformed files are error-accounted while subsequent terms, heterogeneous confusables, tables, relations and binary auxiliary data remain available. A deliberately injected unrelated string-constructor KeyError propagates instead of being masked. No no-follow check is bypassed.

**R02 — closed.** The schema embed is independently decoded from the source AST's literal json.loads argument and equals the exact pinned external/private WGU schema in full. The supported schema vocabulary covers that pin's refs, types, enums, constants, patterns, required keys, properties, additional-property shapes and array items. The four original counterexamples pass unchanged. Fourteen additional nested/file checks cover version/digital/source-translation/table-row/term/change/ambiguity/question/subprocedure shapes and manifest metadata; missing chapter uses a located parent fallback. Three additional mandatory-manifest cases cover missing schema, game and both, retaining the original raw metadata. Valid unknown extensions and untyped table/terminology data survive. Integer/string step.n support is explicit, retains values and excludes bool. The corrected shared-game-ID fixture supplies required manifest.schema, retains strict zero-error/duplicate assertions and strengthens exact accounting; it is not used as the sole correctness oracle.

**R03 — closed.** The unchanged string-confusables oracle passes. Independently chosen null, bool, integer, empty-string, list and extended mapping values survive without false malformed-record errors. Incidental confusable IDs are excluded from entity identity; a real terminology ID and repeated auxiliary IDs do not collide with them. Genuine malformed entity records and duplicate recognized IDs remain rejected by the unchanged strict controls.

finding-dispositions.json records each location, independent verification basis and repair count. risk_probes.py, metadata_edge_probes.py and complete logs preserve strict expectations. The reviewer made no product edits and did not alter prior probes.

## Independent full private accounting and compatibility

The complete raw-byte inventory was recomputed independently, using the prior reviewer oracle unchanged except for the two exact repaired import/report target references. It checks **59 manifest entries**, **23 available files**, **36 missing sources**, **1,233,389 available bytes**, **1,692 records** (1,655 processed, 37 raw, zero errors), **38,206 field/container locations**, and **8,904 conservatively defined unknown-field locations**. Every file byte, record value/parent/location/identity/navigation, YAML field tag/marks/character range and unknown value is checked against manifest-enumerated raw bytes via independent safe_load/compose. Representative mappings and record hashes are retained privately; no historical count, adapter counter or old gameplay answer generates expectations.

Two native-verified complete imports are byte-identical and match `private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json`, SHA-256 `2999d63c680b4c52a095e0edb18952c70eefdf4baf7c2e01481840cda18ca61a`. Direct old/new comparison additionally proves every parent import key/value (including the complete files/records/field ledger) is unchanged; the only added top-level keys are structural_schema_sha256 and structural_extensions. This compatibility assertion and all original full-accounting assertions remain strict.

The exact selected registry manifest, its source pin and two enumerated blobs are rehashed. Identity to WGU's missing original remains unknown. PDF bytes are hashed without source-meaning review. The offline PyYAML 6.0.3 wheel/source evidence remains pinned; no dependency install, external API or network operation was used.

## Every acceptance criterion

| Exact criterion | Independent assessment |
|---|---|
| Import rules, terms, nested procedures, tables, relations, ambiguities, changes, questions, terminology and auxiliary files. | Pass: complete actual corpus inventory/value equality plus independent malformed-file continuation and heterogeneous confusables. |
| Unsafe YAML tags and duplicate keys fail with locations; errors do not become empty collections. | Pass: unchanged strict unsafe/duplicate/recursion/depth/expansion controls and new located malformed-safe-scalar/multi-file probes. |
| Every unknown field/file is preserved or explicitly diagnosed; WGU verified/complete/resolved remains imported metadata. | Pass: every actual unknown location and raw byte accounted; extension/file controls pass and all acceptance/readiness markers remain not granted. |
| Refs/see remain navigation; questions are evaluation candidates, not battle scenarios or accepted expected results. | Pass: every applicable actual record plus unchanged independent controls retains navigation and evaluation-candidate roles. |

Both required validation groups are complete: adversarial YAML/duplicate IDs/keys/extension fields/anonymous terms/nested numbering/malformed records and private all-file independent accounting. Known optional structural contracts and canonical file metadata now have independent failure controls.

## Actual checks, measurement and limits

| Check | Result |
|---|---|
| Workflow validate / fresh packet / full before-after hashes | Exit 0; current delivery, preserved versions, packet, schema and dependency pins verified. |
| Unchanged independent reviewer probes | Exit 0; 35 pass. |
| New affected-risk probes | Exit 0; 24 pass. |
| New missing-manifest metadata probes | Exit 0; 3 pass. |
| Explicit tests/wgu_adapter | Exit 0; 59 pass. |
| Affected tests/inputs | Exit 0; 51 pass. |
| Independent full accounting and repeated import | Exit 0. |
| scripts/check.ps1 -Task IG-1C | Exit 0; plan/dry-run/tests/diff all 0; 102 project tests pass. |
| Independent git diff --check | Exit 0. |

Actual commands, exits and UTC/wall intervals are preserved in individual check records and review.json. Normally reviewed narrow local native escalation was used for real Windows handles/synthetic snapshots, based on the previously measured sandbox WinError 5. No native safety verification was bypassed. Real junction tests passed; file/directory symlink results remain unmeasured/null and are not inferred from junctions.

Two reviewer tooling corrections are preserved separately: the schema extraction harness initially assumed a Python dictionary literal, then verified the actual literal JSON encoding; a nested PowerShell quote error prevented creating an optional metadata runner, then an explicit saved runner executed the unchanged assertions. The failed operations/exits and changed hypotheses are recorded. Neither weakened a product assertion, changed product bytes or consumed a product repair cycle. No unchanged failure was retried.

Missing source materials and mixed editions still require downstream reconciliation. Structural import does not establish publisher-source coverage, accepted rule meaning or executable legality. Tokens, cost and operator time remain null. This review is bounded to IG-1C; it does not implement future identities/export or gameplay logic.

## Next exact action

Coordinator may use this independent technical PASS and pinned evidence to perform its own criterion/gate verification and record IG-1C technical acceptance/done under workflow. The reviewer performs no queue transition. Human semantic acceptance and executable readiness remain separate, ungranted gates. IG-1D starts only under a separate coordinator-authorized task cycle.
'''
with (RUN / 'report.md').open('x', encoding='utf-8', newline='\n') as stream:
    stream.write(report)
evidence = [ref(p) for p in sorted(RUN.iterdir()) if p.is_file()]
evidence += [ref(CONFIG), ref(ROOT / after['packet']['path']), ref(ROOT / 'private/workflow/packets/IG-1C-e53938d9f57544e8a8bd52c12430be50/context.txt')]
evidence += [ref(project / name) for name in ['plan.log', 'dry-run.log', 'pytest.log', 'result.json']]
review = {'role': 'reviewer', 'actor': 'ig1c-reviewer-20261013T071955Z', 'executor_actor': 'ig1-stage-executor-20261013', 'task': 'IG-1C',
    'summary': 'Independent first repair re-review technical PASS; all three prior P2 findings closed at iteration 1 after unchanged probes, additional strict risk/metadata controls and complete private accounting. No semantic approval or readiness.',
    'technical_result': 'pass', 'technical_pass': True, 'independent_pass': True,
    'model': 'gpt-6.1-sol', 'reasoning': 'high', 'requested_model': 'gpt-6.1-sol', 'requested_reasoning': 'high',
    'configuration_evidence': {**ref(RUN / 'configuration.json'), 'source': configuration['configuration_evidence'], 'same_reviewer_session': True},
    'reviewed_delivery': {**after['delivery'], 'artifact_count': after['artifact_count'], 'artifacts': [{'path': a['path'], 'sha256': a['sha256']} for a in after['artifacts']]},
    'parent_delivery': after['parent_delivery'], 'parent_review': after['parent_review'], 'all_frozen_versions_match_before_and_after': True,
    'finding_dispositions': dispositions, 'findings': [], 'criteria': task['acceptance'],
    'criterion_assessments': [{'criterion': c, 'status': 'pass', 'evidence': ['independent-accounting.json', 'original-probes.log', 'risk-probes.log', 'metadata-edges.log']} for c in task['acceptance']],
    'required_validation': {'adversarial_structural_controls': 'pass', 'full_private_independent_accounting': 'pass'},
    'input_packet': after['packet'], 'checks': checks, 'project_check_result': project_result,
    'accounting_summary': {k: accounting[k] for k in ['manifest_entries', 'available_files', 'missing_files', 'available_bytes', 'record_count', 'kind_counts', 'status_counts', 'field_count', 'unknown_location_count', 'two_imports_byte_identical', 'matches_frozen_import']},
    'parent_preservation': {'parent_artifact_count': 53, 'complete_baseline_mapping': after['baseline_mapping'], 'full_version_ledger': after['parent_preservation'], 'prior_review_artifacts': 40, 'prior_review_manifest_entries': 34, 'accepted_foundation_artifacts': 148, 'all_match': True},
    'reviewer_harness_corrections': [read(RUN / 'verification-harness-correction.json'), read(RUN / 'metadata-runner-correction.json')],
    'measurements': measurements, 'artifacts': evidence, 'semantic_decision': None,
    'semantic_acceptance_granted': False, 'publisher_source_coverage_granted': False, 'executable_readiness_granted': False,
    'queue_changed_by_reviewer': False, 'product_changed_by_reviewer': False, 'product_repair_iterations_reviewed': 1,
    'next_operation': 'Coordinator independently verifies criteria/evidence and performs technical acceptance/done under workflow. No reviewer queue transition, semantic approval or IG-1D implementation.'}
write('review.json', review)
write('review-manifest.json', {'format': 'wgc-independent-review-manifest-1', 'task': 'IG-1C', 'actor': review['actor'], 'delivery': after['delivery'], 'artifacts': [ref(p) for p in sorted(RUN.iterdir()) if p.is_file()]})
print(json.dumps({'result': 'pass', 'closed_findings': [d['finding_id'] for d in dispositions], 'review': ref(RUN / 'review.json'), 'report': ref(RUN / 'report.md'), 'manifest': ref(RUN / 'review-manifest.json'), 'wall_seconds': measurements['wall_seconds']}))
