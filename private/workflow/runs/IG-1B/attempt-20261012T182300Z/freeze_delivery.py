"""Freeze IG-1B executor evidence; no self-review or acceptance."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
HERE = Path(__file__).parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def pin(path):
    return {'path': path.absolute().relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


task = next(t for t in read(ROOT / 'docs/work/queue.json')['tasks'] if t['id'] == 'IG-1B')
assert task['status'] == 'in_progress'
checks = read(HERE / 'checks.json')
assert all(c['exit_code'] == 0 for c in checks)
initial = read(HERE / 'checkpoint.json')
verification = read(HERE / 'snapshot-verification.json')
snapshots = verification['snapshots']
products = [ROOT / p for p in ['src/wgc/inputs/__init__.py', 'src/wgc/inputs/snapshot.py',
                             'src/wgc/inputs/README.md', 'tests/inputs/test_snapshot.py',
                             'contracts/ig/input.schema.json']]
for key in ['input_snapshot', 'source_snapshot']:
    directory = Path(snapshots[key])
    manifest = read(directory / 'manifest.json')
    products.append(directory / 'manifest.json')
    products += [directory / f['blob_path'] for f in manifest['files'] if f['availability'] == 'available']
    if key == 'source_snapshot':
        products.append(directory / 'source-pin.json')
products.append(ROOT / verification['availability_report']['path'])
product_pins = [pin(p) for p in sorted(products)]
ended = datetime.now(timezone.utc)
started = datetime.fromisoformat(initial['started_utc'])
measurement = {'started_utc': started.isoformat(), 'ended_utc': ended.isoformat(),
               'wall_seconds': (ended - started).total_seconds(), 'input_tokens': None,
               'output_tokens': None, 'operator_seconds': None, 'monetary_cost': None,
               'peak_memory_bytes': None, 'gameplay_performance': None,
               'unknown_reason': 'Token counters, operator time, cost and peak memory are not exposed/reported. No game runtime was measured.',
               'interval_note': 'Claim-to-freeze elapsed UTC interval in this same ongoing session; not an active-work estimate.'}
checkpoint = {**initial, 'changed_files': product_pins, 'completed_criteria': task['acceptance'],
              'checks': checks, 'updated_utc': ended.isoformat(), 'measurement': measurement,
              'blocker': None, 'next_operation': 'Freeze delivery and transition only IG-1B to review. Obtain a separate independent technical review; do not self-accept or start IG-1C.'}
write('checkpoint-frozen.json', checkpoint)
assessments = [
    {'index': 1, 'criterion': task['acceptance'][0], 'executor_result': 'implemented_and_checked',
     'evidence': ['Input/source manifests and their copied files', 'snapshot-verification.json',
                  'tests/inputs/test_snapshot.py: byte oracles, changed pin, mutation and changed name set']},
    {'index': 2, 'criterion': task['acceptance'][1], 'executor_result': 'implemented_and_checked',
     'evidence': [verification['availability_report']['path'], 'Input manifest configured_source entries',
                  'tests/inputs/test_snapshot.py: missing/appearing/available configured source controls']},
    {'index': 3, 'criterion': task['acceptance'][2], 'executor_result': 'implemented_and_checked',
     'evidence': ['Exact source snapshot source-pin.json and registry provenance/PDF copies',
                  'Input manifest source_snapshot_id', 'tests/inputs/test_snapshot.py: pin/identity/metadata controls']},
    {'index': 4, 'criterion': task['acceptance'][3], 'executor_result': 'implemented_and_checked',
     'evidence': ['src/wgc/inputs/snapshot.py: plan, ancestry, descriptor/final-handle checks and disjoint destinations',
                  'tests/inputs/test_snapshot.py: traversal, ADS/device names, case/physical aliases, real junctions and opened-handle redirection']},
]
report = [
    '# IG-1B frozen executor delivery', '',
    '**Outcome: four task criteria implemented and checked; ready for separate independent technical review.** '
    'This executor does not grant acceptance, done, source meaning or executable readiness. No next task is started.', '',
    'The operator explicitly accepted IG-1A and authorized starting the next ready task in this same conversation. '
    'IG-1A completed through hashed accepted/done events; all 82 frozen delivery artifacts remain unchanged. '
    'IG-1B was made ready only after scoped input/hash enumeration, then claimed with pinned packet and ownership evidence. '
    'The local wgc-queue and wgc-execute skills were explicitly read and applied.', '',
    '## Delivery and measured inputs', '',
    '`src/wgc/inputs/snapshot.py` provides an offline, read-only byte snapshot facility and CLI. '
    '`contracts/ig/input.schema.json` specifies versioned input/source manifests; the source contract canonical profile and bounded evaluator are reused unchanged. '
    'Only the IG-1B owned paths were added. Existing pyproject/check integration paths remain unchanged; new tests are run explicitly.', '',
    f'- Measured WGU inputs: **{snapshots["game_files_available"]} files**, exactly `wgu.yaml` and `kb/`, rehashed from current bytes. '
    'They match the advisory 23 game-file entries. The prior inspection also cited four utility code-basis files, which are not this task input and were not read.',
    f'- Source registry: **2 copied files**, exactly promoted `rulebook.pdf` and `provenance.json`.',
    f'- Independent copied-byte verification: **{verification["available_files_measured"]} files, {verification["bytes_measured"]} bytes**; every copy matches current original bytes and request pins.',
    f'- Configured sources: **{verification["configured_sources_missing_measured"]} individually rechecked missing paths**, each with explicit role/availability and null bytes/hash/copy path. No promoted-source substitution.',
    f'- Input snapshot ID: `{snapshots["input_snapshot_id"]}`.',
    f'- Source snapshot ID: `{snapshots["source_snapshot_id"]}`.',
    '- Second real freeze produced identical IDs, manifests and results; existing snapshots were verified, not rewritten. No unsealed staging remains in the actual SPQR snapshot roots.', '',
    'The selected pin is a **new IG source** from the assigned promoted SPQR 5E registry, with '
    '`identity_to_wgu_original: unknown` and `semantic_acceptance: not_granted`. Its PDF SHA-256 is '
    '`e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`. '
    'Edition is declared registry provenance; this task did not read publisher meaning. A stored archive locator was preserved as metadata without archive access.', '',
    'The content-addressed availability report is `' + verification['availability_report']['path'] + '`; SHA-256 `' + verification['availability_report']['sha256'] + '`.', '',
    '## Criteria and required controls', '', '| Queue criterion | Executor coverage |', '|---|---|',
]
explanations = [
    'Every listed file has a relative path, role, availability and exact byte/hash evidence or explicit nulls. Required pins, same-handle stability, independent copy hashes, global origin rehash and KB name-set checks detect mutations.',
    'All 36 historical configured paths were individually rechecked during preflight, snapshot and independent verification. Missing originals remain missing, never substituted with selected promoted bytes.',
    'The source snapshot retains the exact promoted PDF/provenance and explicit new-source pin. The input manifest references its exact snapshot ID; original WGU identity remains unknown.',
    'Unsafe spellings, duplicate/case aliases, linked ancestors and physical aliases reject. All plan paths are checked before source bytes. Windows checks actual opened final paths/reparse attributes and shares only reads; POSIX uses descriptor-relative O_NOFOLLOW. Destinations are disjoint from origin roots.',
]
for item, explanation in zip(assessments, explanations):
    report.append(f'| {item["index"]}. {item["criterion"]} | Implemented and checked: {explanation} |')
report += ['', 'Unmet implementation criteria from the executor perspective: **none**. '
           'Unmet lifecycle gate: **separate independent technical review of these exact hashes**. No self-review or human source-meaning acceptance is fabricated.', '',
           'Synthetic tests derive expectations from the task byte/scope contract and architecture snapshot invariants: '
           'copy mutation and same-size/restored-mtime mutation reject; missing sources remain explicit; new KB names and newly appearing sources reject; '
           'duplicate/case/hardlink aliases and traversal/ADS/device names reject; actual directory junction/symlink escapes and opened-handle redirection reject before consuming content; '
           'read-only neighbour roots cannot become output destinations; independent byte/hash/manifest-ID oracles and repeatability pass. '
           'On Windows, attempted writes while a read handle is open are denied. Publisher content appears only in private copies.', '',
           '## Actual passing checks', '', '| Command/control | Exit | Result |', '|---|---:|---|',
           '| Explicit final tests/inputs suite, fresh test-temp-04, local require_escalated | 0 | 33 passed in 4.69 s; real Windows junction/hardlink tests included |',
           '| pwsh -NoProfile -File scripts/check.ps1 -Task IG-1B | 0 | 102 passed in 46.11 s; plan/dry-run/tests/diff all 0 |',
           '| Actual pinned snapshot CLI, two executions | 0, 0 | Identical snapshot IDs/results; existing bytes reused |',
           '| Independent private copy/origin/hash/availability/manifest-ID verification | 0 | 25 files, 5,199,801 bytes; 36 missing sources; no actual staging remains |',
           '| git diff --check | 0 | Existing line-ending warnings only; no whitespace errors |',
           '| workflow.py validate and next | 0, 0 | 39 tasks valid; No ready task |',
           '| IG-1A frozen delivery SHA-256 preservation | 0 | All 82 accepted delivery artifacts unchanged |', '',
           'Exact passing command records, logs and result JSON are in checks.json. Tests/inputs is outside the inherited explicit default testpaths, '
           'so it was run separately without an out-of-scope integration edit. The two suites are reported separately.', '',
           '## Development failures and resolution', '',
           'All earlier logs are preserved in development-check-history.json. First default-sandbox test run: 14 passed/13 failed, '
           '8.30 s; the environment denied final-handle path inspection (WinError 5), actual junction creation and hardlink creation. '
           'The library failed closed. The explicitly scoped require_escalated command was approved by automatic review; no rejection or workaround occurred.', '',
           'The first permitted native run: 16 passed/11 failed, 4.65 s. A newly created-file diagnostic established different ctime semantics '
           'between Windows fstat and pathname stat. Implementation was corrected to compare ctime within the same handle API, '
           'path identity/size/mtime separately and retain full copy/global origin SHA-256. This is a recorded changed hypothesis, '
           'not an unchanged-failure retry. Assertions were not weakened. The corrected suite passed 27 tests in 3.70 s; '
           'after additional publication/metadata/cleanup-boundary controls, the final 33 tests passed. '
           'No independent review repair cycle has occurred for IG-1B. IG-1A F2 has not been reopened or repaired again.', '',
           '## Configuration, measurements and limits', '',
           'Executor `executor-ig-1b-20261012T182300Z`; current model/reasoning **gpt-6.1-sol/high**. '
           'The same current chat was confirmed by the operator from its UI before substantive work; configuration.json records continuity '
           'and distinguishes direct current-session testimony from unavailable runtime metadata. No prior-session settings substitute for it.', '',
           f'UTC claim-to-freeze interval: `{measurement["started_utc"]}` to `{measurement["ended_utc"]}`; elapsed `{measurement["wall_seconds"]:.6f}` seconds. '
           'Token counts, operator seconds, monetary cost, peak memory and game performance are null. Test seconds are measured controls, not gameplay latency. '
           'Independent technical defect counts and source-meaning defect counts remain null until the appropriate separate review; no known unresolved executor defect is claimed fixed by self-acceptance.', '',
           'Snapshot immutability is append-only application behavior with revalidation, not OS-level protection against operator tampering. '
           'Source and input publication are separate; a failed input publication may leave a valid unreferenced source snapshot. '
           'Origins are not a global filesystem transaction; later origin changes do not rewrite frozen bytes. '
           'Destination directories require isolation from hostile concurrent writers. Failed staging is retained under its fresh run/test location as incomplete evidence. '
           'On this host, required Windows handle/link controls need a permitted local context; restricted execution rejects them rather than weakening them.', '',
           'Open decisions: obtain independent technical review; later tasks reconcile unavailable materials and source meaning. '
           'Missing configured material blocks only dependent source verification, not the available KB byte snapshot. '
           'No importer, interpreter, compiler or game mechanism was created. No archives/Git history, neighbour writes, new agents/chats, '
           'automation, external services, commits or pushes were used.', '',
           '## Frozen product files and SHA-256', '', '| Path | SHA-256 |', '|---|---|']
report += [f'| `{a["path"]}` | `{a["sha256"]}` |' for a in product_pins]
report += ['', '## Next exact action', '',
           'Transition only IG-1B to review with delivery.json. Supply review-prompt.md to a separately authorized independent reviewer. '
           'Confirm that reviewer current-session configuration, verify the complete frozen list first, rerun required native/synthetic and project controls, '
           'and report findings without implementation edits or self-acceptance. Do not start IG-1C.', '']
(HERE / 'report.md').write_text('\n'.join(report), encoding='utf-8')
run_files = ['report.md', 'checkpoint-frozen.json', 'configuration.json', 'input-request.json', 'preflight.json',
             'checks.json', 'development-check-history.json', 'snapshot-verification.json', 'ig-1a-preservation.json',
             'tests-01.log', 'tests-02.log', 'tests-03.log', 'tests-04.log', 'snapshot-01.log', 'snapshot-02.log',
             'project-check.log', 'diff-check.log', 'prepare.py', 'build_input_schema.py', 'freeze_delivery.py']
artifact_pins = product_pins + [pin(HERE / n) for n in run_files]
project = ROOT / checks[1]['log_root']
artifact_pins += [pin(project / n) for n in ['result.json', 'plan.log', 'dry-run.log', 'pytest.log', 'diff-check.log']]
assert len({a['path'] for a in artifact_pins}) == len(artifact_pins)
delivery = {'role': 'executor', 'actor': initial['actor'], 'task': 'IG-1B',
            'summary': 'Frozen read-only input/source byte snapshot facility, immutable private manifests and explicit promoted-source pin. Four criteria checked; 33 input tests and 102 inherited project tests pass. Independent technical review pending.',
            'criteria': task['acceptance'], 'criterion_assessments': assessments,
            'artifacts': artifact_pins, 'checks': checks, 'development_history': pin(HERE / 'development-check-history.json'),
            'model': 'gpt-6.1-sol', 'reasoning': 'high', 'configuration_evidence': pin(HERE / 'configuration.json'),
            'input_packet': initial['input_packet'], 'input_context': initial['input_context'],
            'measurement': measurement, 'review_readiness': 'ready', 'unmet_implementation_criteria': [],
            'unmet_lifecycle_gates': ['Separate independent technical review and appropriate coordinator disposition'],
            'independent_defect_counts': None, 'source_meaning_defect_counts': None,
            'semantic_acceptance_granted': False, 'executable_readiness_granted': False,
            'snapshot_ids': {'inputs': snapshots['input_snapshot_id'], 'sources': snapshots['source_snapshot_id']}}
write('delivery.json', delivery)
prompt = ['# Independent technical review: IG-1B', '',
          'Work locally in C:/repo/wargame-compiler; discuss in Polish and write code/docs/reports in English. '
          'Review only IG-1B, Freeze input and source manifests. Do not start another task.', '',
          'Read AGENTS.md, README.md, docs/STATUS.md, docs/HANDOFF.md, WORKFLOW and explicitly docs/skills/wgc-review/SKILL.md. '
          'Confirm your actual current GPT-6.1 Sol/high configuration from your own metadata or obtain operator UI confirmation before substantive review. '
          'Do not inherit this executor configuration as your own.', '',
          'Run workflow.py validate, next and packet --task IG-1B; queue.json is the only status authority. '
          'Expected status review. Do not claim or change task state. Read the card, named context and frozen report/checkpoint. '
          'The input packet retained here was created in ready state; compare any generated-card status change explicitly.', '',
          f'Frozen delivery: `{pin(HERE / "delivery.json")["path"]}`, SHA-256 `{pin(HERE / "delivery.json")["sha256"]}`.', '',
          'Verify EVERY artifact hash and exact list before assessment, including 25 copied files, both manifests, source pin and availability report. '
          'Independently validate copy/repeatability oracles, all four card criteria, mutation, missing/appearing source, path/case/physical aliases, '
          'actual Windows junctions, safe opened-handle path checks, disjoint output roots, canonical metadata and append-only reuse. '
          'Read the preserved development failures and distinguish resolved ctime implementation behavior from restricted execution.', '',
          'Run explicit tests/inputs with a fresh basetemp, scripts/check.ps1 -Task IG-1B and git diff --check. '
          'Sandbox denies native GetFinalPathNameByHandleW and link creation on this host: use only normally reviewed, explicitly scoped local escalation if needed; '
          'do not bypass approval or weaken protections/tests. Real private repeats must read only the frozen enumerated roots and write only assigned snapshot roots.', '',
          'Use a distinct reviewer identity and new review directory under private/workflow/runs/IG-1B. '
          'Write findings, exact hashes, criteria, commands/exits, actual current configuration and measurements/nulls. '
          'Do not modify implementation, tests or frozen reports; no archive/Git history or neighbouring writes; no agents/chats/automation/external services/commit/push. '
          'No self-granted SPQR meaning or executable acceptance. The operator/coordinator owns status disposition. IG-1A frozen files remain accepted and unchanged.', '']
(HERE / 'review-prompt.md').write_text('\n'.join(prompt), encoding='utf-8')
print(json.dumps({'delivery': pin(HERE / 'delivery.json'), 'artifacts': len(artifact_pins),
                  'product_artifacts': len(product_pins), 'measurement': measurement}, indent=2))
