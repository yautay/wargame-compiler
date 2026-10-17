"""Freeze a new envelope with the immutable original artifact list as prefix."""
from datetime import datetime, timezone
from repair_indexes import META, OLD, ROOT, RUN, SESSION, load, pin, write
from verify_repair import verify


def main():
    task = load(SESSION / 'task.json')
    old = load(OLD / 'delivery.json')
    roots = load(RUN / 'root-validations.json')
    assert all(check['exit_code'] == 0 for check in roots['checks'])
    approved_root = ROOT / 'private/workflow/checks/active-ee91fe8bfff4441c953eba190e20851d'
    restricted_root = ROOT / 'private/workflow/checks/active-fdc1b72725954015bd1ff696f1d15b55'
    result = load(approved_root / 'result.json')
    assert all(result[key] == 0 for key in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'])
    assert '71 passed in 22.13s' in (RUN / 'tests-sources-approved.log').read_text(encoding='utf-8')
    assert '192 passed in 34.78s' in (approved_root / 'pytest.log').read_text(encoding='utf-8')
    command = '.venv/Scripts/python.exe -B -m pytest -q tests/sources --basetemp private/workflow/checks/b03-r01-1dcc40e4 -p no:cacheprovider --tb=short'
    checks = roots['checks'] + [
        {'command': command, 'exit_code': 0, 'permissions': 'approved require_escalated execution', 'log': pin(RUN / 'tests-sources-approved.log')},
        {'command': 'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B03', 'exit_code': 0, 'permissions': 'approved require_escalated execution', 'log': pin(RUN / 'repository-check-approved.log'), 'result': pin(approved_root / 'result.json')},
        {'command': '.venv/Scripts/python.exe -B scripts/workflow.py validate', 'exit_code': 0, 'log': pin(RUN / 'workflow-validate.log')},
        {'command': 'git diff --check', 'exit_code': 0, 'log': pin(RUN / 'diff-check.log')},
        {'command': '.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/repair-r01-f684f3e2-01/verify_repair.py', 'exit_code': 0, 'report': pin(RUN / 'index-validation.json')}]
    failures = [
        {'command': command, 'exit_code': 1, 'cause': 'Restricted Windows token: pytest mode-0700 basetemp WinError 5.', 'log': pin(RUN / 'tests-sources-restricted.log'), 'resolution': 'Same unchanged command rerun once with approved permissions; 71 passed.'},
        {'command': 'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B03', 'exit_code': 1, 'cause': 'Restricted Windows token: pytest mode-0700 basetemp WinError 5; plan/dry-run/diff passed.', 'log': pin(RUN / 'repository-check-restricted.log'), 'result': pin(restricted_root / 'result.json'), 'resolution': 'Same unchanged command rerun once with approved permissions; all checks passed, 192 tests passed.'}]
    write('test-report.json', {**META, 'format': 'wgc-repair-test-report-1',
          'checks': checks, 'failed_initial_executions': failures,
          'tests_or_tools_changed': False, 'acl_or_global_settings_changed': False,
          'source_tests_passed': 71, 'repository_tests_passed': 192,
          'replay_policy': 'Revalidated all six existing root inventories independently; no new extraction, rendering or replay rebuild authorized or performed.',
          'independent_review_pending': True, 'semantic_acceptance_granted': False})
    preflight = load(RUN / 'preflight.json')
    ended = datetime.now(timezone.utc)
    started = datetime.fromisoformat(preflight['started_utc'])
    measurement = {'started_utc': started.isoformat(), 'ended_utc': ended.isoformat(),
                   'elapsed_wall_seconds': (ended - started).total_seconds(),
                   'input_tokens': None, 'output_tokens': None,
                   'token_unknown_reason': 'Token telemetry is not exposed to this role.',
                   'operator_seconds': None, 'operator_time_unknown_reason': 'Not reported.',
                   'review_findings_addressed': ['R01'],
                   'defects_by_severity': {'medium': 1}, 'repair_cycle': 1}
    (RUN / 'delivery-handoff.md').open('x', encoding='utf-8', newline='\n').write(
        '# IG-2B03 R01 repair handoff\n\n'
        'The repaired region ledger and continuation reference index add eight source-visible literal unresolved references in seven of the existing 135 regions. '
        'The required Stacking rules reference is retained for region:e9d78c99-a171-42c6-89f1-fe09b46c47e6. '
        'The assigned-page audit also retains Momentum rule, Trump Option, Trumping, below, and explicit labeled phase destinations. '
        'No citation was followed and no section number or gameplay meaning was inferred.\n\n'
        'Use this attempt\'s region-ledger.json raw_cross_references and continuations.json unfollowed_references as the repaired report indexes. '
        'These supersede only the corresponding old indexes; all old files remain frozen. The full original artifact list is the exact ordered prefix of this new manifest and delivery. '
        'All region records, evidence bytes and locators, inventory/registry bytes, reading order, counts, components and four literal continuations are unchanged.\n\n'
        'Fresh validation passed: six root inventories, 71 source tests, 192 repository tests, workflow validation and git diff --check. '
        'Both initial restricted-token pytest failures are preserved; the exact unchanged commands passed on their single approved reruns. '
        'See test-report.json, reference-audit.json, index-validation.json and preservation-report.json.\n\n'
        'Fresh independent review must assess the changed indexes, inclusion policy and all assigned-page named-reference risks against the preserved complete source review. '
        'No new boundary review, semantic acceptance or executable readiness is granted. Existing gaps and downstream gates remain.\n\n'
        'An initial current-review JSON read included its artifact list and produced truncated output; later reads selected bounded fields. '
        'No transcript, derivation helper, archive or out-of-scope source page was read. This deviation is recorded in preflight.json.\n')
    # Final byte check includes accepted/blocked/review inputs after all tests.
    prior = load(OLD / 'preservation-report.json')
    groups = {'old_delivery': old['artifacts'],
              'blocked_attempt': load(ROOT / prior['blocked_artifact_manifest']['path'])['artifacts'],
              'accepted_dependency': load(ROOT / prior['accepted_dependency_event']['path'])['artifacts'],
              'review_reports': load(ROOT / task['repair_authorization']['review_evidence'])['review_artifacts']}
    for group in groups.values():
        for record in group:
            verify(record)
    assert pin(ROOT / META['configuration_evidence'])['sha256'] == META['configuration_sha256']
    write('checkpoint-final.json', {**META, 'format': 'wgc-checkpoint-1',
          'input_packet': pin(SESSION / 'packet.json'), 'attempt': RUN.relative_to(ROOT).as_posix(),
          'completed_criteria': ['R01 literal indexes repaired and assigned-page named-reference audit frozen.', 'Complete report structures preserved except justified literal additions and current provenance.', 'All required fresh checks pass; old accepted, blocked, continuation and review bytes preserved.'],
          'final_preservation_counts': {key: len(value) for key, value in groups.items()},
          'changed_files': [pin(RUN / name) for name in ['region-ledger.json', 'continuations.json', 'reference-audit.json']],
          'checks': checks, 'blocker': None, 'next_operation': 'Freeze new manifest and envelope, transition only this task to review, then stop.',
          'measurement': measurement})
    names = ['initial-worktree-status.txt', 'preflight.json', 'checkpoint.json', 'claim.json',
             'repair_indexes.py', 'validate_roots.py', 'verify_repair.py', 'freeze_delivery.py',
             'region-ledger.json', 'continuations.json', 'reference-audit.json',
             'root-validations.json', 'preservation-report.json', 'index-validation.json',
             'test-report.json', 'checkpoint-final.json', 'delivery-handoff.md',
             'tests-sources-restricted.log', 'tests-sources-approved.log',
             'repository-check-restricted.log', 'repository-check-approved.log',
             'workflow-validate.log', 'diff-check.log']
    names += ['root-' + name + '.log' for name in ['final-verified', 'replay-a-verified', 'replay-b-verified', 'components', 'components-replay-a', 'components-replay-b']]
    new_artifacts = [pin(RUN / name) for name in names]
    new_artifacts.append(pin(OLD / 'delivery.json'))
    for folder in [restricted_root, approved_root]:
        new_artifacts.extend(pin(folder / name) for name in ['plan.log', 'dry-run.log', 'pytest.log', 'diff-check.log', 'result.json'])
    artifacts = old['artifacts'] + new_artifacts
    assert artifacts[:len(old['artifacts'])] == old['artifacts']
    assert len({record['path'] for record in artifacts}) == len(artifacts)
    write('delivery-manifest.json', {**META, 'format': 'wgc-delivery-manifest-1',
          'input_packet': pin(SESSION / 'packet.json'), 'artifacts': artifacts,
          'immutability': 'Append-only new attempt; all old artifacts remain byte-identical.',
          'original_artifact_prefix_count': len(old['artifacts']),
          'superseded_indexes_only': [
              {'old': pin(OLD / name), 'new': pin(RUN / name), 'field': field}
              for name, field in [('region-ledger.json', 'regions[].raw_cross_references'), ('continuations.json', 'unfollowed_references')]]})
    delivery_artifacts = artifacts + [pin(RUN / 'delivery-manifest.json')]
    write('delivery.json', {**META,
          'summary': 'R01 reference-index repair delivered: eight literal unresolved-reference additions across seven rows; complete frozen prior artifact prefix and all non-index structures preserved. Fresh required validations passed; independent review pending.',
          'criteria': task['acceptance'],
          'criteria_results': [{'criterion': criterion, 'executor_result': 'Existing immutable evidence retained and revalidated; R01 assigned-page reference-index audit and repair complete.', 'independent_review': 'Fresh review required; no acceptance granted.'} for criterion in task['acceptance']],
          'artifacts': delivery_artifacts, 'checks': checks,
          'input_packet': pin(SESSION / 'packet.json'),
          'repair_scope': pin(ROOT / task['repair_authorization']['scope']['path']),
          'prior_delivery': pin(OLD / 'delivery.json'),
          'original_artifact_prefix_count': len(old['artifacts']),
          'preferred_report_indexes': [pin(RUN / 'region-ledger.json'), pin(RUN / 'continuations.json')],
          'counts': old['counts'], 'measurement': measurement,
          'remaining_gates': ['Fresh independent R01 review of repaired indexes and all assigned-page named-reference risks.', 'Later exact source-IG reconciliation and separately authorized human semantic acceptance.'],
          'semantic_acceptance_granted': False, 'technical_acceptance_granted': False,
          'executable_readiness': 'unverified',
          'next_action': 'Supervisor launches a fresh independent reviewer; executor stops after transition to review.'})
    envelope = load(RUN / 'delivery.json')
    assert envelope['artifacts'][:len(old['artifacts'])] == old['artifacts']
    for record in envelope['artifacts']:
        verify(record)
    print('Frozen new delivery:', (RUN / 'delivery.json').relative_to(ROOT).as_posix())
    print('Original ordered artifact prefix:', len(old['artifacts']), '; total artifacts:', len(delivery_artifacts))


if __name__ == '__main__':
    main()
