from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def ref(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path)}

def write(name, value):
    with (RUN / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')

before, after = read(RUN / 'verification-before.json'), read(RUN / 'verification-after.json')
for key in ['delivery', 'artifacts', 'packet', 'input_pins', 'approved_profile_delta', 'operator_profile_approval', 'foundation_artifacts', 'reviewer_configuration']:
    assert before[key] == after[key], key
for category in ['artifacts', 'foundation_artifacts']:
    for artifact in after[category]:
        assert sha(ROOT / artifact['verified_path']) == artifact['sha256']
findings = read(RUN / 'findings.json')['findings'] + [read(RUN / 'finding-IG1D-R04.json')]
assert len(findings) == 4 and len({f['id'] for f in findings}) == 4
accounting = read(RUN / 'independent-accounting.json')
assert accounting['result'] == 'pass'
assert accounting['two_complete_outputs_and_packages_byte_identical']
configuration = after['reviewer_configuration']
write('configuration.json', configuration)
checks = [read(RUN / (name + '-check.json')) for name in ['explicit', 'project', 'accounting', 'probes', 'lineage-probes', 'diff']]
assert [c['exit_code'] for c in checks] == [0, 0, 0, 1, 1, 0]
checks += [
    {'command': '.venv/Scripts/python.exe scripts/workflow.py validate', 'exit_code': 0, 'wall_seconds': 2.2642293},
    {'command': '.venv/Scripts/python.exe scripts/workflow.py packet --task IG-1D', 'exit_code': 0, 'wall_seconds': 3.7751546, 'packet': after['packet']},
    {'command': '.venv/Scripts/python.exe -B private/workflow/runs/IG-1D/review-20261013T122807Z/verify.py before', 'exit_code': 0, 'wall_seconds': 2.0679206},
    {'command': '.venv/Scripts/python.exe -B private/workflow/runs/IG-1D/review-20261013T122807Z/verify.py after', 'exit_code': 0, 'wall_seconds': 1.9737393},
]
project = ROOT / 'private/workflow/checks/active-3d511c7844d248c8928fc9b6c06d01c5'
project_result = read(project / 'result.json')
assert all(project_result[k] == 0 for k in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'])
queue = read(ROOT / 'docs/work/queue.json')
task = next(t for t in queue['tasks'] if t['id'] == 'IG-1D')
assert task['status'] == 'review' and next(t for t in queue['tasks'] if t['id'] == 'IG-1E')['status'] == 'planned'
started = datetime.fromisoformat('2026-10-13T12:28:07+00:00')
ended = datetime.now(timezone.utc)
measurements = {'start_utc': started.isoformat(), 'end_utc': ended.isoformat(), 'wall_seconds': (ended - started).total_seconds(),
    'interval': 'Independent IG-1D review including tool waits, full native audit/transforms/publications and extra merge coverage; previous IG-1C work excluded.',
    'input_tokens': None, 'output_tokens': None, 'cost': None, 'operator_time_seconds': None,
    'native_file_symlink': None, 'native_directory_symlink': None,
    'defect_counts': {'P0': 0, 'P1': 0, 'P2': 4, 'P3': 0}, 'repair_cycles_used': 0, 'unchanged_failure_retries': 0,
    'tests': {'explicit_adapter_export_passed': 84, 'project_passed': 102, 'independent_probes_passed': 11, 'independent_probes_failed': 4},
    'full_accounting_wall_seconds': accounting['wall_seconds']}
write('measurements.json', measurements)
criteria = [
    {'criterion': task['acceptance'][0], 'assessment': 'pass', 'evidence': 'Two actual full transformations and canonical publications match every frozen package byte; approved clocks null and operational sidecars separate.'},
    {'criterion': task['acceptance'][1], 'assessment': 'partial', 'findings': ['IG1D-R01', 'IG1D-R04'], 'evidence': 'Ordinary reorder/edit/rename/insert/delete and collision/keyed-child controls pass; contradictory anonymous evidence is guessed and a unique merge-child correction loses identity.'},
    {'criterion': task['acceptance'][2], 'assessment': 'partial', 'findings': ['IG1D-R02', 'IG1D-R03'], 'evidence': 'Every current raw origin/binding/subtree and wildcard/subpoint control passes; contradictory explicit decisions are silently prioritized and direct active IDs are falsely unresolved.'},
    {'criterion': task['acceptance'][3], 'assessment': 'pass', 'evidence': 'Independent every-record/aspect hash, selected and historical reference closure, strict corruption probes, draft/readiness/unknown checks; no inherited semantic approval.'},
]
report = '''# IG-1D independent technical review: changes requested

**Four P2 findings remain: IG1D-R01/R02/R03/R04.** Full current private accounting, canonical reproducibility and required executor/project controls pass, but independent mutation/reference controls identify unresolved contract failures. No technical PASS, semantic acceptance, publisher-source coverage or executable readiness is granted. The reviewer made no product, queue, frozen artifact or neighboring repository changes.

## Exact delivery, profile and reviewer configuration

Frozen delivery: `private/workflow/runs/IG-1D/preflight-20261013/delivery.json`, SHA-256 `f510ae8830d5a5cbf1311c8383a4a8e0581d3e5421e64283b4d4820cae8f4154`. All **69 artifacts** are independently verified before, after and at review freezing; the exact full list is embedded in review.json and verification-before/after.json. All **182 protected accepted foundation artifact references** remain unchanged. The original source-v1 schema/validator and accepted IG-1A/B/C product/report bytes were only hash-checked through exact current preservation references, not reopened as completed-task context.

The current operator approved the exact `wgc-source-export-1` proposal/patch. Independent full deep-schema comparison verifies only the root version ID/title, **14 schema-version constants**, and **two canonical run clock shapes** change; every other mechanical, hash, reference, review and readiness rule is unchanged. The profile matches the pinned proposal SHA-256 `2a1f619eb4773d1432470cf0a340ac55c2f74451661c92002a6c89a7864bd768`. Canonical started_utc/ended_utc are required null; real operation clocks/configuration remain separate sidecars. This narrow approval grants no source meaning.

Reviewer actor remains `ig1c-reviewer-20261013T071955Z`, distinct from executor `ig1-stage-executor-20261013`. Actual reviewer **gpt-6.1-sol / high** uses this same reviewer chat's earlier direct operator UI confirmation, preserved by path/hash in configuration.json. Same-chat continuity is intact, with no requested/observed configuration change; executor/requested configuration is not substituted as proof. Tokens, cost and operator time are unavailable/null.

Fresh reviewer packet: `private/workflow/packets/IG-1D-e2dc4314bbd94e2f86db733486d95700/manifest.json`. Queue/context/named-file hashes/sizes and all nine task input pins match. AGENTS/README/status/handoff/workflow/current queue/card, explicit wgc-review skill and exact named contracts/context were read (unchanged architecture/data context retained from this same review sequence). The packet's generated execution-skill text does not change the reviewer role. Source validator, source contract README, identity/reference/export/storage implementation and delivered regression controls were inspected. Queue remains IG-1D review, IG-1E planned.

## Findings and independent oracles

1. **IG1D-R01 — identity.py:253–270.** Unique substantive rename evidence is assigned before contradictory unique label evidence can be evaluated. Two anonymous terms keeping names while exchanging definitions silently exchange IDs. Those exact bytes support either keeping names/identities and editing definitions, or keeping bodies/identities and exchanging names. No external ID or explicit binding disambiguates the histories. An ordered heuristic is not an unambiguous identity decision. Preserve conflicting candidates/origins as gaps until explicitly resolved.
2. **IG1D-R02 — identity.py:146–151 (dispatch at 215–228).** A forced split/merge child locator may also carry an incompatible explicit hint to an unrelated existing ID. Validation accepts both; lineage dispatch allocates its child and silently ignores the hint/basis. Reject incompatible overlap or preserve an explicit conflict gap instead of discarding a recorded caller decision.
3. **IG1D-R03 — references.py:61–70.** Exact active allocated IDs are not checked against the active identity map, only external aliases/scopes. A refs value equal to an existing active ID is falsely unresolved, removing a justified edge and related cycle diagnostics. Resolve direct active identities explicitly; retain retired-ID, alias collision and scope safeguards and no-approval/navigation roles.
4. **IG1D-R04 — identity.py:219–225.** Replaying a one-child merge with the same persistent decision/parents/kind/scope and only a corrected definition loses the unique child's assigned ID and creates a gap. A one-child persisted receipt identifies the child independently of its current text. Preserve that allocation through correction; retain ambiguity for genuinely indistinguishable multiple children and conflicting receipts.

findings.json preserves the first three findings; finding-IG1D-R04.json appends the fourth without overwriting the original observation. review.json contains the complete set. Every finding has an exact location, consequence, reproducer, evidence, independent expectation basis and required verification. All are at **zero independent repair cycles**, maximum two per finding. No failed assertion was weakened or retried.

The first independent suite has 9 passes/3 failures; the additional merge suite has 2 passes/1 failure. Its addition closes a previously unresolved merge-correction coverage concern, not an unchanged retry. Positive controls prove ordinary correction/reorder/insert/delete/file move, unambiguous rename, keyed identical-child edits/replay, many-to-many subtree binding, exact historical split/merge revisions, alias collision honesty, explicit wildcard/subpoint scopes, both-endpoint relationship resolution, allowed rule/procedure cycles, strict clock/hash/selected-revision failures, package repeatability and corruption preservation. expected-results.md and lineage-expectations.md justify each oracle independently of executor fixtures.

## Complete current private accounting

Independent raw-byte inventory checks all **59 manifest entries**, **23 available WGU files**, **36 missing configured sources**, **1,692 input records**, **38,206 YAML field/container locations**, **16,276 binding observations**, and **18,303 source graph records**. Every available raw blob matches its manifest and base64 import evidence. Independent YAML safe_load/compose verifies all record values, parent locators, every YAML field tag/source/key mark/character range and nested/unknown subtree. Every registry entity observation is matched to the exact current input record; every binding is independently located in the actual document or actual `/files/index` manifest entry/subfield. Whole-file bindings carry complete actual document values, including null for opaque bytes. No adapter counter alone generates expectations.

Every source record/aspect hash and selected/historical reference closure is independently recomputed. All projected aspects remain unknown/blocking with explicit reconciliation gaps; dedicated procedure/step/table descriptions do not invent publisher rules, actual table axes/cells, PDF evidence or accepted question answers. Current coverage/review/evidence/region records are absent and snapshot is structural draft with execution blocked. The original literal values and all unknown subtrees remain in current registry/import/source bindings.

A fresh full transform from the exact pinned empty namespace registry seed matches frozen source-ig, identity-registry and references bytes. A second full transform using the first persisted outputs is byte-identical. Two actual publications in the new review directory reuse the same exact canonical package/manifest while producing separate real operational sidecars. The package ID equals the frozen `sha256:ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc`. The pure audit reports 304.4794168001972 wall seconds; its logged wrapper measured 307.4985666999128 seconds. All produced package/operation evidence is included in the independent review manifest.

Selected source registry metadata/blobs/source pin are verified by native no-follow snapshot checks. Identity to WGU's missing original remains unknown. Missing/mixed-edition materials are downstream reconciliation work and do not become claimed source coverage. No publisher meaning, gameplay gold, past-chat history, Git history, archive or external service was used.

## Every exact acceptance criterion

| Exact criterion | Independent assessment |
|---|---|
| Repeated identical bytes yield identical identities and export content; timestamps are outside canonical hashes. | Pass: fresh seeded and persisted repeated full outputs/packages match exact bytes; null canonical clocks and separate operation sidecars verified. |
| Reordering anonymous terms/relations preserves identities when unambiguous; collisions become review gaps. | Partial: ordinary mutations and collisions pass; contradictory rematch evidence is guessed (R01), and a uniquely identified merge child cannot be corrected under replay (R04). |
| Many-to-many origin bindings preserve file/field locations; wildcard and subpoint references have exact targets or explicit unresolved scope. | Partial: every current origin/subtree plus positive scopes/many-to-many controls passes; conflicting explicit decisions are dropped (R02), and direct current IDs are falsely unresolved (R03). |
| Export validates revision/hash closure and never inherits semantic approval. | Pass: independently recomputed full hash/reference closure and strict corruption controls; no accepted review transfer, snapshot draft and all execution/meaning blockers retained. |

Required mutation validation is complete as a review but exposes R01/R02/R04. Required reference validation exposes R03. Byte determinism, unresolved scope controls and cyclic source descriptions pass without imposing a rule DAG.

## Actual checks, limitations and next action

| Check | Actual result |
|---|---|
| Workflow validate / fresh reviewer packet / all delivery/input/profile/foundation hashes | Exit 0. |
| Explicit tests/wgu_adapter and tests/export | Exit 0; 84 pass. |
| Independent identity/reference/source/package probes | Exit 1; 9 pass, 3 fail. |
| Additional merge lineage probes | Exit 1; 2 pass, 1 fail. |
| Full private independent accounting and two transforms/publications | Exit 0. |
| scripts/check.ps1 -Task IG-1D | Exit 0; plan/dry-run/tests/diff all 0; 102 project tests pass. |
| Independent git diff --check | Exit 0. |

Each actual command/exit/UTC/wall interval is retained in its log/check record and review.json. Normally reviewed narrow local native escalation was used for no-follow handles and synthetic package reads because sandbox WinError 5 was previously measured. No native check was bypassed, no global configuration changed and no dependencies installed. Native file/directory symlink measurements remain null; no symlink result is inferred from earlier junction tests. Unknown tokens/cost/operator time remain null.

Coordinator should request bounded fixes for IG1D-R01/R02/R03/R04, preserve this delivery/review and freeze changed product hashes for independent re-review. Preserve all strict probes and full raw/binding/closure/reproducibility assertions. At most two repair cycles per finding and two unchanged retries apply; this review consumed zero. IG-1E stays planned pending technical closure and coordinator acceptance/done. The reviewer performs no queue transition, product repair or semantic acceptance and messages no other chat.
'''
with (RUN / 'report.md').open('x', encoding='utf-8', newline='\n') as stream:
    stream.write(report)
own_paths = sorted(p for p in RUN.iterdir() if p.is_file())
for publication in accounting['publications']:
    package = Path(publication['package'])
    own_paths += [package / name for name in ['manifest.json', 'source-ig.json', 'identity-registry.json', 'references.json']]
    own_paths += [Path(publication['operation'])]
own_paths = sorted(set(own_paths))
artifacts = [ref(p) for p in own_paths]
artifacts += [ref(ROOT / after['packet']['path']), ref(ROOT / 'private/workflow/packets/IG-1D-e2dc4314bbd94e2f86db733486d95700/context.txt')]
artifacts += [ref(project / name) for name in ['plan.log', 'dry-run.log', 'pytest.log', 'result.json']]
review = {'role': 'reviewer', 'actor': 'ig1c-reviewer-20261013T071955Z', 'executor_actor': 'ig1-stage-executor-20261013', 'task': 'IG-1D',
    'summary': 'Independent technical review requests four P2 identity/decision/reference corrections. Full current file/record/field/binding/hash closure and two full canonical transform/publication checks pass; no approval or readiness.',
    'technical_result': 'changes_requested', 'technical_pass': False, 'independent_pass': False,
    'model': configuration['model'], 'reasoning': configuration['reasoning'], 'requested_model': 'gpt-6.1-sol', 'requested_reasoning': 'high',
    'configuration_evidence': {**ref(RUN / 'configuration.json'), 'source': configuration['source'], 'same_reviewer_chat_continuity': True},
    'reviewed_delivery': {**after['delivery'], 'artifact_count': 69, 'artifacts': [{'path': a['path'], 'sha256': a['sha256']} for a in after['artifacts']]},
    'all_frozen_delivery_hashes_match_before_after_and_at_freeze': True,
    'input_packet': after['packet'], 'input_pins': after['input_pins'], 'approved_profile_delta': after['approved_profile_delta'], 'operator_profile_approval': after['operator_profile_approval'],
    'criteria': task['acceptance'], 'criterion_assessments': criteria, 'findings': findings,
    'checks': checks, 'project_check_result': project_result,
    'independent_accounting_summary': {k: accounting[k] for k in ['independent_record_count', 'independent_field_count', 'kind_counts', 'manifest_entries', 'available_files', 'missing_sources', 'source_graph_records', 'binding_count', 'two_complete_outputs_and_packages_byte_identical', 'fresh_seeded_transform_matches_frozen']},
    'foundation_preservation': {'count': 182, 'all_match': True, 'exact_ledger': after['foundation_artifacts']},
    'measurements': measurements, 'artifacts': artifacts, 'semantic_decision': None,
    'semantic_acceptance_granted': False, 'publisher_source_coverage_granted': False, 'executable_readiness_granted': False,
    'queue_changed_by_reviewer': False, 'product_changed_by_reviewer': False, 'independent_repair_cycles_used': 0,
    'next_operation': 'Coordinator requests bounded repairs IG1D-R01/R02/R03/R04 and returns changed frozen hashes for independent re-review; no acceptance/done or IG-1E execution until technical gates pass.'}
write('review.json', review)
write('review-manifest.json', {'format': 'wgc-independent-review-manifest-1', 'task': 'IG-1D', 'actor': review['actor'], 'delivery': after['delivery'], 'artifacts': artifacts + [ref(RUN / 'review.json')]})
print(json.dumps({'result': review['technical_result'], 'findings': [f['id'] for f in findings], 'review': ref(RUN / 'review.json'), 'report': ref(RUN / 'report.md'), 'manifest': ref(RUN / 'review-manifest.json'), 'wall_seconds': measurements['wall_seconds']}))
