"""Freeze the first bounded F1 repair with exact current product hashes."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
HERE = Path(__file__).parent
PROBES = ROOT / 'private/workflow/runs/IG-1B/repair01-probes-20261012T193641Z'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def pin(path):
    return {'path': path.absolute().relative_to(ROOT).as_posix(),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


task = next(t for t in read(ROOT / 'docs/work/queue.json')['tasks'] if t['id'] == 'IG-1B')
assert task['status'] == 'in_progress'
initial = read(HERE / 'checkpoint-initial.json')
checks = read(HERE / 'checks.json')
assert all(c['exit_code'] == 0 for c in checks)
baseline = read(HERE / 'baseline-manifest.json')
product_pins = [pin(ROOT / b['original']['path']) for b in baseline]
private_audit = read(PROBES / 'private-audit.json')
controls = read(PROBES / 'review-controls.json')
assert len(controls) == 14 and all(c['conforms'] for c in controls)
ended = datetime.now(timezone.utc)
started = datetime.fromisoformat(initial['started_utc'])
measurement = {'started_utc': started.isoformat(), 'ended_utc': ended.isoformat(),
               'wall_seconds': (ended - started).total_seconds(), 'input_tokens': None, 'output_tokens': None,
               'operator_seconds': None, 'monetary_cost': None, 'peak_memory_bytes': None,
               'gameplay_performance': None, 'unknown_reason': 'Not exposed/reported; no game runtime measured.',
               'interval_note': 'UTC claim-to-freeze interval, not an active-work estimate.'}
checkpoint = {**initial, 'changed_files': product_pins, 'completed_criteria': task['acceptance'],
              'checks': checks, 'measurement': measurement, 'updated_utc': ended.isoformat(),
              'next_operation': 'Transition only IG-1B to review and send exact frozen repair to the existing authorized independent reviewer for F1 closure. No self-acceptance or IG-1C start.'}
(HERE / 'checkpoint-frozen.json').write_text(json.dumps(checkpoint, indent=2) + '\n', encoding='utf-8')
lines = ['# IG-1B first bounded F1 repair delivery', '',
         '**Executor outcome: F1 repair implemented and checks pass; independent closure remains pending.** '
         'All four source-input task criteria are covered from the executor perspective. No accepted/done or source-meaning/executable readiness decision is made here.', '',
         'The operator instructed “Kontynuuj” after the stated next action, bounded F1 repair and independent re-review. '
         'Only this repair was claimed through `review -> changes_requested -> in_progress`. The existing reviewer session is authorized; '
         'no new session or agent is created. IG-1A remains done and its 82 frozen artifacts are unchanged.', '',
         '## Finding and exact repair scope', '',
         'Independent finding F1 (P2) demonstrated that extra KB bytes, a blob for a missing entry, or an unlisted junction '
         'could remain in a sealed directory while verification/reuse returned its unchanged ID. '
         'The original reviewer report/evidence are preserved: `private/workflow/runs/IG-1B/review-confirmed-20261012T185333Z/review.json`, '
         'SHA-256 `d5cc08accd4da84660ef3b451022758312e14b0f5c1e4d543de79458b9f22af4`.', '',
         'Only `src/wgc/inputs/snapshot.py`, its local README, and `tests/inputs/test_snapshot.py` changed. '
         'The schema, canonical identity rules, native opened-handle controls, input plans, copied private bytes, source pin and availability report are unchanged. '
         'Original 33-test source bytes remain an exact prefix of the augmented file; 18 new tests were appended, with no original assertion edits.', '',
         '`verify_tree_names` derives permitted files from available manifest blobs plus root manifest.json and the source-only source-pin.json. '
         'Permitted directories are exactly the required parents. It inventories names with no-follow metadata and rejects unknown files, '
         'metadata, empty directories, nonregular entries, symlinks and Windows reparse points before opening copied content or the pin. '
         'A manifest-declared missing entry contributes no allowed blob. The check gates staging verification, published verification and existing-target reuse. '
         'A corrupt existing snapshot is rejected and left unchanged.', '',
         'This addresses ordinary static tampering; the documented need to isolate destinations from hostile concurrent writers remains. '
         'No new importer, interpreter, compiler, game mechanism or source semantics is introduced. F1 repair-cycle count is **1**; '
         'there has been no second cycle or unchanged-failure retry in this repair.', '',
         '## Criterion coverage', '', '| Queue criterion | Executor assessment |', '|---|---|']
assessments = [
    'Covered. Exact file/parent-directory closure now complements size/hash/availability accounting and all original mutation/copy integrity controls.',
    'Covered and unchanged. The private audit rechecks the exact current WGU configured path set, all 36 missing paths, null evidence and no substitution.',
    'Covered and unchanged. Exact promoted PDF/provenance/source pin retain new_ig_source and identity_to_wgu_original unknown; no meaning acceptance.',
    'Covered. New static sealed-tree link/addition rejection is exercised in both snapshot kinds and verify/reuse modes; original path/handle/alias/disjoint-output controls remain strict.',
]
for index, (criterion, assessment) in enumerate(zip(task['acceptance'], assessments), 1):
    lines.append(f'| {index}. {criterion} | {assessment} |')
lines += ['', 'Unmet implementation criteria from the executor perspective: none. Unmet lifecycle gate: separate independent '
          'technical closure on these new hashes. The previous independent P2 remains formally open until that reviewer disposition. '
          'Source-meaning defect counts are null; source meaning was not reviewed.', '',
          '## Actual controls and preservation', '', '| Control | Exit/result |', '|---|---|',
          '| Final explicit input suite, fresh basetemp, reviewed native execution | 0; 51 passed in 5.56 s |',
          '| Byte-identical reviewer review_controls.py replay in a fresh evidence directory | 0; all 14 expectations conform, including all three saved F1 reproductions |',
          '| Byte-identical native_handle_probe.py replay | 0; redirected junction handle rejects before yielding content; normal read handle denies writes |',
          '| Byte-identical private_audit.py replay | 0; 25 copies, 5,199,801 bytes; exact tree sets; two repeats preserve all IDs/bytes |',
          '| scripts/check.ps1 -Task IG-1B | 0; 102 passed in 57.38 s; plan/dry-run/tests/diff all zero |',
          '| git diff --check and workflow.py validate | 0, 0 |',
          '| Preserved original product/delivery/reviewer/IG-1A hashes | 0; all comparisons match |', '',
          'Checks and durations are recorded in checks.json/replayed-checks.json; logs are retained. Native tests/probes require '
          'normally reviewed local escalation on this host because the sandbox denies final-handle inspection and actual links. '
          'No safeguard or expected result was weakened. Replayed reviewer scripts are executor validation, not a new independent review; '
          'all generated evidence is in a fresh directory and the original reviewer files remain immutable.', '',
          'All 34 original product files were copied byte-for-byte into baseline/ before the claim. The entire original 59-artifact delivery '
          'is reverified through that explicit mapping for old product revisions. Original reports/manifests and all 30 reviewer artifacts remain unchanged. '
          'Only the three stated live product paths now have new hashes. Snapshot IDs are unchanged: inputs '
          '`sha256:0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df`; sources '
          '`sha256:86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008`. '
          'The private set contains 23 WGU files, two registry files and 36 individually missing configured sources.', '',
          '## Configuration, measurements and open decisions', '',
          'Executor identity: `executor-ig-1b-repair01-20261012T193641Z`. Current configuration: gpt-6.1-sol/high from the operator UI '
          'confirmation for this same ongoing chat, retained with explicit continuity in configuration.json. Runtime metadata are unavailable; '
          'reviewer-session settings are not used to confirm executor settings.', '',
          f'UTC claim-to-freeze interval `{measurement["started_utc"]}` to `{measurement["ended_utc"]}`; wall `{measurement["wall_seconds"]:.6f}` seconds. '
          'Tokens, operator seconds, cost, peak memory and game performance remain null. Test durations do not measure gameplay.', '',
          'Open decision: independently close F1 and assess all four criteria on the new complete frozen list. '
          'At most two repair cycles are allowed for F1; if a later unchanged failure exhausts that limit, escalate rather than silently repair again. '
          'No semantic or executable acceptance follows from technical controls. Archives/Git history, neighbouring writes, additional chats/agents, '
          'automation, external services, commits and pushes were not used.', '',
          '## Complete current product SHA-256', '', '| File | SHA-256 |', '|---|---|']
lines += [f'| `{p["path"]}` | `{p["sha256"]}` |' for p in product_pins]
lines += ['', 'Next exact action: transition this delivery to review and pass the pinned rereview-prompt.md to the already authorized '
          'independent reviewer. Preserve the old report and write a new reviewer result. Do not start IG-1C.', '']
(HERE / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
owned_run_files = ['report.md', 'checkpoint-frozen.json', 'configuration.json', 'operator-scope.json',
                   'baseline-manifest.json', 'evidence-before.json', 'preservation.json', 'suite-provenance.json',
                   'checks.json', 'replayed-checks.json', 'input-tests.log', 'project-check.log', 'diff-check.log',
                   'review_controls.log', 'native_handle_probe.log', 'private_audit.log',
                   'run_reviewer_checks.py', 'freeze_repair.py',
                   'src_wgc_inputs_snapshot.py.diff', 'src_wgc_inputs_README.md.diff', 'tests_inputs_test_snapshot.py.diff']
artifacts = product_pins + [pin(HERE / name) for name in owned_run_files]
artifacts += [pin(PROBES / name) for name in ['review_controls.py', 'native_handle_probe.py', 'private_audit.py',
                                             'review-controls.json', 'native-handle-probe.json', 'private-audit.json']]
project = ROOT / next(c['log_root'] for c in checks if 'log_root' in c)
artifacts += [pin(project / n) for n in ['result.json', 'plan.log', 'dry-run.log', 'pytest.log', 'diff-check.log']]
assert len({p['path'] for p in artifacts}) == len(artifacts)
delivery = {'role': 'executor', 'actor': initial['actor'], 'task': 'IG-1B',
            'summary': 'First bounded F1 repair: exact sealed-tree file and parent-directory closure, no-follow rejection of additional files/metadata/links, and unchanged corrupt-target preservation. All 51 input tests, 14 saved probes and 102 project tests pass under executor validation; independent closure pending.',
            'criteria': task['acceptance'], 'artifacts': artifacts, 'checks': checks,
            'model': 'gpt-6.1-sol', 'reasoning': 'high', 'configuration_evidence': pin(HERE / 'configuration.json'),
            'input_packet': initial['input_packet'], 'input_context': initial['input_context'],
            'prior_review': initial['review_evidence'], 'prior_delivery': initial['prior_delivery'],
            'repair_cycles': {'F1': 1}, 'repair_findings': ['F1'], 'measurement': measurement,
            'unmet_implementation_criteria': [], 'unmet_lifecycle_gates': ['Independent re-review and coordinator disposition'],
            'semantic_acceptance_granted': False, 'executable_readiness_granted': False}
(HERE / 'delivery.json').write_text(json.dumps(delivery, indent=2) + '\n', encoding='utf-8')
prompt = f'''# Independent re-review of IG-1B F1, repair cycle 1

Continue only IG-1B in your existing independently authorized reviewer session. The operator instructed "Kontynuuj" after the stated next step: bounded F1 repair and independent re-review. Do not create another session or agent.

Read AGENTS.md, README, STATUS, HANDOFF, WORKFLOW and the local wgc-review skill. Confirm your own actual current Sol/high configuration using current-session evidence; requested settings and executor confirmation are not proof. Preserve earlier UI/configuration evidence with any explicit same-session continuity; do not read archives or Git history.

Run workflow.py validate, next and packet --task IG-1B. Expected queue state review. Read the card/context, new report/checkpoint and prior review. Do not claim, repair, change queue, accept/done or start IG-1C.

New frozen delivery: {pin(HERE / 'delivery.json')['path']}
SHA-256: {pin(HERE / 'delivery.json')['sha256']}
Complete artifacts: {len(artifacts)}. Verify every hash before review. All 34 prior product copies are preserved in baseline/ with baseline-manifest.json. Verify the prior 59-artifact delivery through that mapping; all original reviewer artifacts remain immutable.

Re-review F1 and affected risks independently: exact allowed metadata/blob/file/parent-directory sets; unknown bytes, metadata, empty directories, nonregular entries, missing-entry blobs and actual junction/symlink rejection without following or reading them; input/source verification, staging and existing-target reuse; no overwrite of corrupt snapshots. Original 33 test-source bytes remain an unchanged prefix; 18 cases were appended. Review their expectations from the contract, not validator agreement alone.

Independently execute your original three counterexamples and other saved probes into a NEW review directory, using byte-identical copies of scripts whose output paths are relative to __file__. Do not execute them in their old location. Run explicit tests/inputs with a fresh basetemp, native opened-handle proof, private repeat/copy audit, scripts/check.ps1 -Task IG-1B and git diff --check. Native Windows operations may need normally reviewed exact local escalation; do not bypass rejection or weaken safeguards. Real private repeats may read only the pinned roots/files and write only the task's assigned snapshot roots.

Record a new report.md and review.json with PASS/FAIL, F1 disposition, every criterion, complete matching frozen list, actual configuration/source, commands/exits, measurements/nulls and preservation. Executor replay results are not your independent disposition. F1 has used one repair cycle. Preserve old reports and IG-1A's 82 accepted hashes. Human source meaning and executable readiness are separate gates. Return paths/hashes in this chat; no other-chat messages or additional agents/chats, automation, external services, archive/history reads, neighbouring writes or commit/push.
'''
(HERE / 'rereview-prompt.md').write_text(prompt, encoding='utf-8')
print(json.dumps({'delivery': pin(HERE / 'delivery.json'), 'artifacts': len(artifacts),
                  'product_count': len(product_pins), 'measurement': measurement}, indent=2))
