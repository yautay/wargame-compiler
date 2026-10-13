"""Record final handoff verification, with no workflow transition."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[4]
REL = str(HERE.relative_to(ROOT)).replace('\\', '/')


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def pin(path):
    return {'path': str(path.relative_to(ROOT)).replace('\\', '/'),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


audit = read(HERE / 'hash-verification.json')
checks = read(HERE / 'checks.json')
preservation = read(HERE / 'preservation.json')
configuration = read(HERE / 'configuration.json')
task = next(t for t in read(ROOT / 'docs/work/queue.json')['tasks'] if t['id'] == 'IG-1A')
assert audit['integrity_pass'] and all(c['exit_code'] == 0 for c in checks)
assert preservation['all_observed_files_unchanged'] and preservation['queue_unchanged']
assert preservation['git_status_porcelain_unchanged']
assert task['status'] == 'review'

assessments = [
    {'index': 1, 'criterion': task['acceptance'][0], 'result': 'pass',
     'evidence': ['contracts/ig/source.schema.json: record oneOf, 13 families, node aspects/groups',
                  'tests/contracts/test_source.py: static catalogue, page/evidence and group/table checks'],
     'assessment': 'All required record families have explicit shapes and source-layer examples. Origins, coverage, reviews and snapshot assessments are distinct.'},
    {'index': 2, 'criterion': task['acceptance'][1], 'result': 'pass',
     'evidence': ['contracts/ig/README.md: identity, WGC-C14N-1 and reference rules',
                  'src/wgc/contracts/source.py: canonical_bytes, content_hash, aspect_hash, selected/store uniqueness',
                  'tests/contracts/test_source.py: fixed byte/hash vectors, strict JSON and registry reorder'],
     'assessment': 'Integer/scalar canonicalization is explicit and deterministic; fixed independent byte/hash expectations and duplicate/reorder controls pass. F3 exact selected endpoints pass.'},
    {'index': 3, 'criterion': task['acceptance'][2], 'result': 'pass',
     'evidence': ['contracts/ig/source.schema.json: statement, content_ref, whole_historical_ref, review_data, snapshot_data',
                  'src/wgc/contracts/source.py: review_freshness, exact exclusion boundary and blocker reports',
                  'tests/contracts/fixtures/catalog.json: model approval, opaque, unknown, review basis and coverage cases',
                  REL + '/independent-suites.log'],
     'assessment': 'Source-level opacity can be structurally valid while execution is blocked. Review/coverage/import do not grant semantic acceptance. F1 and F2/F2-R1 are closed within structural scope.'},
    {'index': 4, 'criterion': task['acceptance'][3], 'result': 'pass',
     'evidence': ['contracts/ig/source.schema.json: 30 node_description alternatives with named fields',
                  'tests/contracts/test_source.py: test_every_required_mechanism_has_named_source_fields_and_addressable_examples',
                  'tests/contracts/fixtures/valid-source.json'],
     'assessment': 'Dedicated named source fields cover all requested mechanisms. They are addressable descriptions and uncertainty records; no executable SPQR interpretation is inferred.'},
    {'index': 5, 'criterion': task['acceptance'][4], 'result': 'pass',
     'evidence': ['src/wgc/contracts/source.py: full module inspected', 'src/wgc/contracts/__init__.py',
                  'contracts/ig/README.md: Open formal-language decisions for IG-3A',
                  'pyproject.toml', 'scripts/check.ps1'],
     'assessment': 'Delivered code parses, hashes and validates source structures locally. It does not evaluate game rules. Future formal operators, execution algorithms and readiness decisions remain explicitly open.'},
]
required_cases = [
    {'requirement': 'Unknown value without gap', 'contract_basis': 'IG-DATA-MODEL Knowledge and representation', 'files': ['invalid-unknown-without-gap.json'], 'expected': 'reject'},
    {'requirement': 'Changed aspect integrity/freshness', 'contract_basis': 'IG-1A deterministic revisions; architecture: changed aspects do not inherit acceptance', 'files': ['invalid-changed-aspect-hash.json', 'valid-changed-aspect.json', 'valid-changed-dependency.json'], 'expected': 'reject stale hash; accept storage but report stale reviews'},
    {'requirement': 'Model approval', 'contract_basis': 'IG-DATA-MODEL: only authorized human acceptance', 'files': ['invalid-model-approval.json'], 'expected': 'reject'},
    {'requirement': 'Dangling active versus historical reference', 'contract_basis': 'IG-DATA-MODEL selected snapshot versus immutable revision store', 'files': ['invalid-dangling-active.json', 'invalid-dangling-historical.json', 'valid-historical-reference.json'], 'expected': 'reject unresolved exact pins; allow retained historical informational mention'},
    {'requirement': 'Duplicate identity', 'contract_basis': 'IG-DATA-MODEL identity/revision uniqueness', 'files': ['invalid-duplicate-selection.json', 'invalid-duplicate-store.json'], 'expected': 'reject'},
    {'requirement': 'Opaque execution blocker', 'contract_basis': 'IG-1A criterion 3 and IG-LEGAL-ACTIONS unknowns', 'files': ['valid-source.json', 'invalid-opaque-formal.json', 'invalid-opaque-ready.json'], 'expected': 'allow opaque source while reporting blocked execution; reject false formal/ready claims'},
]
ended = datetime.now(timezone.utc)
started = datetime.fromisoformat(configuration['substantive_interval_start_utc'])
measurement = {'started_utc': started.isoformat(), 'ended_utc': ended.isoformat(),
               'wall_seconds': (ended - started).total_seconds(),
               'interval_note': configuration['start_note'], 'input_tokens': None,
               'output_tokens': None, 'operator_seconds': None, 'monetary_cost': None,
               'peak_memory_bytes': None, 'gameplay_latency': None, 'unique_test_total': None,
               'unknown_reason': 'Token counters, operator time, cost and peak memory are not exposed/reported. No gameplay system is measured. Suites overlap, so a unique-test aggregate is not claimed.'}
artifacts = [pin(HERE / name) for name in ['configuration.json', 'preflight.json', 'hash-verification.json',
             'hash-verification-before.json', 'preservation.json', 'checks.json', 'suite-copy-provenance.json',
             'project-check.log', 'independent-suites.log', 'diff-check.log', 'hash-verification.log',
             'git-status-before.txt', 'git-status-after.txt', 'verify_handoff.py', 'run_checks.py',
             'write_report.py', 'test_rereview.py', 'test_final_boundaries.py', 'original-f2-disposition.json']]
project_root = ROOT / checks[0]['log_root']
artifacts += [pin(project_root / n) for n in ['result.json', 'pytest.log', 'plan.log', 'dry-run.log', 'diff-check.log']]
decisions = [
    'Operator/coordinator technical acceptance and any later accepted/done transition remain a separate explicitly authorized action. This session records only a recommendation.',
    'No third F2 repair is authorized. Any recurrence requires an operator decision and new documented hypothesis/scope before repair.',
    'The formal-language choices recorded for IG-3A remain future work; this session starts no downstream task.',
    'Real source coverage, authorized human source-meaning decisions, compilation and gameplay readiness remain separate future gates. IG-1A itself requires no SPQR semantic acceptance.',
]
result = {'role': 'reviewer', 'actor': configuration['actor'], 'task': 'IG-1A',
          'review_scope': 'Final verification of the already frozen handoff; no implementation/test repair or task transition',
          'technical_result': 'pass', 'recommendation': 'Recommend operator/coordinator technical acceptance of the exact pinned IG-1A delivery.',
          'acceptance_recorded': False, 'criteria': task['acceptance'], 'criterion_assessments': assessments,
          'unmet_task_criteria': [], 'unmet_lifecycle_decisions': [decisions[0]], 'required_validation': required_cases,
          'findings': [], 'defect_counts': {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0}, 'source_meaning_defect_counts': None,
          'model': configuration['model'], 'reasoning': configuration['reasoning'],
          'configuration_evidence': pin(HERE / 'configuration.json'), 'measurement': measurement,
          'frozen_delivery': audit['pins'][0], 'frozen_review': audit['pins'][1],
          'queue_status_before': 'review', 'queue_status_after': task['status'], 'queue_sha256': audit['queue_sha256'],
          'queue_transition_performed': False, 'checks': checks,
          'preflight': read(HERE / 'preflight.json'), 'finding_dispositions': audit['finding_dispositions'],
          'repair_cycles': audit['repair_cycles'], 'open_decisions': decisions,
          'expected_input_projection_differences': audit['expected_input_projection_differences'],
          'unexpected_hash_mismatches': [], 'semantic_acceptance_granted': False, 'executable_readiness_granted': False,
          'limitations': ['Bounded technical verification does not prove absence of all possible defects.',
                         'Structural metadata does not authenticate human identities, authority or decision artifacts.',
                         'Review basis completeness is declared; contradictory decisions are not automatically aggregated.',
                         'Synthetic region counts are not complete real-rulebook coverage; mixed coordinate partitions need author justification.',
                         'Current session configuration is operator UI testimony, not machine-extracted runtime metadata. Prior reviewer metadata are read only from their frozen evidence artifact.'],
          'artifacts': artifacts}

lines = ['# IG-1A final handoff verification', '',
         '**Technical result: PASS. Recommend technical acceptance of the exact frozen delivery.**', '',
         'All five queue criteria are satisfied within the source-contract scope. No actionable technical finding remains. '
         'This is a recommendation only: queue stays `review`, with no accepted/done transition. No SPQR semantic acceptance or executable readiness is granted.', '',
         'Reviewer identity: `review-handoff-20261012T180728Z`, distinct from executor `ig-1a-executor-20261012-0540` and the earlier independent reviewer. '
         'Only IG-1A final handoff verification was performed. The local `docs/skills/wgc-review/SKILL.md` was explicitly read and applied.', '',
         '## Configuration and measurements', '',
         'Current session: **GPT-6.1 Sol / reasoning high**. Exact runtime metadata were unavailable; before substantive verification, '
         'the operator answered “potwierdzam” to the explicit question confirming both settings from this current chat UI. '
         '`configuration.json` preserves that evidence. No earlier-session confirmation was used to confirm this session.', '',
         f'Measured UTC interval: `{measurement["started_utc"]}` to `{measurement["ended_utc"]}`; elapsed `{measurement["wall_seconds"]:.6f}` seconds. '
         'The interval begins with the first explicit UTC clock read after confirmation; prior reads, initial commands and the operator wait have no invented duration. '
         'Tokens, operator seconds, cost, peak memory and gameplay latency are `null`. Check runtimes are not game performance measurements.', '',
         '## Integrity, queue and provenance', '',
         '| Pinned evidence | Actual SHA-256 |', '|---|---|']
for entry in audit['pins'] + audit['observed_files']:
    lines.append(f'| `{entry["path"]}` | `{entry["actual_sha256"]}` |')
lines += ['', 'Both operator-specified main hashes match exactly. All **82/82 delivery artifacts** match; all paths are unique and '
          'the complete reviewer-frozen list matches the delivery list exactly, including order and hashes. All **60/60 final-review artifacts**, '
          '**56/56 prior-review artifacts** and **35/35 original-review artifacts** match. All 60 preserved baseline copies, '
          '76 prior-delivery artifacts via explicit baseline mapping, 66 checkpoint changed files and current packet pins also match.', '',
          'All 12 IG-1A queue-event JSON hashes match. Event states form a contiguous chain with ordered timestamps ending in `review`; '
          'the latest event pins the current delivery hash. The independent final PASS is retained in its pinned review artifact, '
          'and has not been converted into acceptance. `validate` confirms all 39 tasks and generated views; `next` reports no ready task. '
          'The newly generated packet was read with its card and four named design documents. No new claim was made.', '',
          'One expected input projection difference exists: the old frozen input packet pins `docs/work/tasks/IG-1A.md` at '
          '`788df9bd2d5ee6650975b2d8c5ada45391835b23bfb6155aad05c165362bed34`; current bytes hash to '
          '`c3f7ef9dc8a9c8251e6ffcae3f2ce19962a28e61b5361daa23ade8205bf5d7c6`. '
          'Comparison against the embedded original card proves the only content change is `changes_requested` → `review`. '
          'Criteria and all design input hashes are unchanged. This expected workflow projection update does not alter the frozen delivery or PASS. '
          'Unexpected hash discrepancies: **none**.', '',
          'The executor frozen report correctly says independent closure was pending at its earlier freeze. The later independently pinned report/review and final handoff record that closure. '
          'Their chronology is consistent; earlier reports were preserved rather than rewritten.', '',
          '## Criteria and required cases', '', '| Criterion | Assessment and evidence |', '|---|---|']
for assessment in assessments:
    lines.append(f'| {assessment["index"]}. {assessment["criterion"]} | **PASS.** {assessment["assessment"]} |')
lines += ['', 'Unmet task criteria: **none**. Pending lifecycle decision: operator/coordinator disposition. '
          'Exact evidence locations and the required-case mapping are recorded in `review.json`.', '',
          'Required cases were checked against their contract-derived expectations: unknown values without gaps reject; stale aspect hashes reject; '
          'changed target/dependency revisions make old reviews stale; model approval rejects; active resolution cannot borrow retained history; '
          'missing exact historical pins and duplicate identities reject; opaque source content remains valid only with execution blocked. '
          'The independent suite and the 56-case frozen catalogue cover positive and negative cases. Expectations come from the task card and '
          'the architecture/data/mechanics/legal-action contracts, plus the independently documented findings; validator agreement is not treated as source truth.', '',
          '## Finding closure', '',
          '- **F1: fixed, one repair cycle.** Gap/metadata targets cannot represent source content, including active/historical and mixed target lists. '
          'Node/evidence/relation positives and partial/unprocessed gap accounting pass.',
          '- **F2/F2-R1: fixed, two repair cycles.** Coverage exclusions require the exact inventory/region/level boundary, full-record region target and full-record inventory basis. '
          '`whole_historical_ref` forbids `aspect_id` on both inventory pin locations, including retained records. '
          'Both unchanged original F2-R1 counterexamples reject at schema validation. Full inventory-with-aspects positives pass; '
          'a whole inventory change invalidates the prior exclusion even with unchanged aspect hash; ordinary aspect-scoped freshness retains its valid behavior. '
          'No third repair was initiated.',
          '- **F3: fixed, one repair cycle.** Required/conditional endpoints must resolve to the exact selected revision in both directions. '
          'Unselected/superseded same-aspect revisions reject; informational historical mentions and unresolved candidates remain preserved.', '',
          'Current technical defects in this bounded verification: P0=0, P1=0, P2=0, P3=0. Source-meaning defect counts: `null`, outside this assignment.', '',
          '## Actual controls', '', '| Control | Exit | Measured result |', '|---|---:|---|',
          '| workflow.py validate | 0 | 39 tasks, DAG, scope, context and generated views valid |',
          '| workflow.py next | 0 | No ready task |',
          '| workflow.py packet --task IG-1A | 0 | Fresh read-only context packet generated |']
for c in checks:
    if c['tests_passed'] is not None:
        value = f'{c["tests_passed"]} passed in {c["reported_pytest_seconds"]:.2f} s; wall {c["wall_seconds"]:.6f} s'
    else:
        value = f'PASS; wall {c["wall_seconds"]:.6f} s'
    label = 'Existing independent suites (95 augmented + 16 original + 9 final boundaries)' if '-m pytest' in c['command'] else c['command']
    lines.append(f'| `{label}` | {c["exit_code"]} | {value} |')
lines += ['', 'Project plan/dry-run/tests/diff exits are all zero. The 102 project tests include 76 contract controls; '
          'the 120 independent tests include catalogue replay and overlap with product checks, so they are not summed into a unique total. '
          'Frozen reviewer test files were copied byte-for-byte into this new review directory because their helpers emit evidence beside themselves. '
          'Original assertions were not changed. The original 16-case suite was executed read-only with fresh temporary paths. '
          'Copy provenance, exact argv, exits, durations and logs are in `suite-copy-provenance.json` and `checks.json`.', '',
          'Standalone `git diff --check` passes. Its 43 existing line-ending warning lines do not report whitespace errors; no normalization or configuration change was made. '
          'The project dry-run reports unchanged queue, zero models launched and zero product files written.', '',
          '## Preservation and open decisions', '',
          'Post-check integrity passes for the complete frozen lists, reports, named evidence and queue. Queue SHA-256 remains '
          '`85b06d2fdc49c4e83e928ffb1642c6b14b36146d75c80ec15e5982155c0b1821`. '
          'The observed handoff/report/input bytes and porcelain Git status remain unchanged; new review evidence is under the already untracked run directory. '
          'All writes in this session are fresh review evidence, the required generated packet, or fresh check outputs. '
          'No implementation/product test was edited, and no frozen report was overwritten.', '',
          'The only three changed existing product files relative to the prior repair baseline are the already-delivered schema, README and catalogue; '
          'the six added fixtures are already part of the frozen delivery. These changes predate this verification.', '']
lines += ['- ' + decision for decision in decisions]
lines += ['', 'Known source-layer limits remain explicit: human authority/artifacts are not authenticated by structural metadata; '
          'basis completeness is declared; contradictory review decisions need explicit handling; synthetic counts do not certify full source coverage; '
          'mixed coordinate partitions need author justification. These do not create an unmet IG-1A source-contract criterion. '
          'Technical PASS does not certify actual SPQR meaning, legality, full-profile readiness or all possible defects.', '',
          'No archives or Git history were read; no neighbouring repository was modified; no agent, new chat, automation, external API, commit or push was used. '
          'No importer, interpreter, compiler or game mechanism was created. Next task was not started.', '',
          '## Verified delivery files', '',
          'All 82 rows below are independently hashed from current disk bytes and match both frozen lists. '
          '`hash-verification.json` additionally records every verified review artifact, baseline copy, prior-delivery mapping, event and input with its expected and actual SHA-256.', '',
          '| File | Verified SHA-256 |', '|---|---|']
for entry in audit['delivery_artifacts']:
    lines.append(f'| `{entry["path"]}` | `{entry["actual_sha256"]}` |')
lines += ['', '## Evidence index', '',
          '- `review.json`: structured result, criterion/case mapping, checks, measurements, current configuration and artifact hashes.',
          '- `hash-verification.json`: complete byte-integrity and workflow-event verification, including the expected generated-card delta.',
          '- `preservation.json`: post-test queue, report and Git-status preservation.',
          '- `checks.json`, `preflight.json` and logs: current-session actual commands/results.',
          '- `configuration.json`: current operator UI confirmation, explicitly distinguished from unavailable runtime metadata.', '']
(HERE / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
result['artifacts'].append(pin(HERE / 'report.md'))
(HERE / 'review.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
(HERE / 'report-manifest.json').write_text(json.dumps({'report': pin(HERE / 'report.md'), 'review': pin(HERE / 'review.json'),
                                                     'note': 'Integrity index only; no workflow transition or acceptance.'}, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'technical_result': result['technical_result'], 'measurement': measurement,
                  'report': pin(HERE / 'report.md'), 'review': pin(HERE / 'review.json')}, indent=2))
