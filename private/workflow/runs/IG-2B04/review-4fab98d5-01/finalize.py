"""Freeze an independent V01 rereview without changing queue or product files."""
from datetime import datetime, timezone
from pathlib import Path
from audit import OUT, ROOT, SESSION, base, load, pin, write

delivery_ref = load(SESSION / 'delivery-reference.json')
delivery = load(delivery_ref['evidence'])
task = load(SESSION / 'task.json')
initial = load(OUT / 'hash-audit-initial.json')
closing = load(OUT / 'hash-audit-final.json')
repository = load(OUT / 'repository.json')
sources = load(OUT / 'sources.json')
diff = load(OUT / 'diff.json')
assert all(v['exit_code'] == 0 for v in [repository, sources, diff])
assert all(repository['subchecks'][k] == 0 for k in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'])
assert initial['passed'] and closing['passed']
assert '247 passed' in (OUT / 'repository.log').read_text(encoding='utf-8-sig')
assert '71 passed' in (OUT / 'sources.log').read_text(encoding='utf-8-sig')
assert closing['counts']['current_delivery_artifacts'] == 2350
assert closing['counts']['protected_artifacts'] == 828
assert closing['counts']['prior_review_artifacts'] == 373
prior_review_path = ROOT / 'review-ce506337-01/review.json'
prior_review = load(prior_review_path)
assert prior_review['criteria'] == task['acceptance'] == delivery['criteria']
executor_validation = load(ROOT / 'repair-v01-e742d89b-01/validation-report.json')
assert all(c['exit_code'] == 0 for c in executor_validation['checks'])
assert all(executor_validation['repository_subchecks'][k] == 0 for k in ['plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'])

checkpoint = base('Independent V01 rereview complete: unchanged validation passes; every frozen delivery/protected/prior-review artifact preserved.')
checkpoint.update(completed_criteria=task['acceptance'], changed_files_scope=OUT.as_posix(),
                  source_inspection_or_regeneration_performed=False,
                  delivery=pin(delivery_ref['evidence']), closing_hash_audit=pin(OUT / 'hash-audit-final.json'),
                  blocker=None, next_operation='Freeze review.json, return pass, and stop this role. Coordinator owns any acceptance decision.')
write('checkpoint-final.json', checkpoint)

names = ['checkpoint-initial.json', 'audit.py', 'run_validation.py', 'finalize.py',
         'hash-audit-initial.json', 'repository.json', 'repository.log',
         'sources.json', 'sources.log', 'diff.json', 'diff.log',
         'hash-audit-final.json', 'checkpoint-final.json']
review_artifacts = [pin(OUT / name) for name in names]
review_artifacts += repository['check_artifacts']
for item in review_artifacts:
    assert pin(item['path']) == item

e = base('V01 resolved. Independent unchanged repository validation passes 247 tests; explicit source suite passes 71 tests and git diff --check passes. All 2350 frozen delivery artifacts, all 828 protected pins, all 373 prior review artifacts and the exact 2325-entry original prefix are preserved. Prior complete four-page/113-component source-review coverage is retained under the current validation-only authorization.')
e.update(outcome='pass', review_scope='validation_only_V01_rereview',
         criteria=task['acceptance'], artifacts=delivery['artifacts'],
         delivery=pin(delivery_ref['evidence']), input_packet=pin(SESSION / 'packet.json'),
         repair_scope=pin(ROOT / 'prepare-v01-e742d89b-01/scope.json'),
         context_recovery_scope=pin(ROOT / 'v01-recovery-20261016-01/scope.json'),
         context_recovery_assessment=pin(ROOT / 'v01-recovery-20261016-01/assessment.json'),
         prior_review=pin(prior_review_path), review_artifacts=review_artifacts,
         criteria_results=[{'criterion': c, 'result': 'met',
                            'basis': 'Current closing hash audit and preserved complete prior independent source/ledger, regeneration, replay, reference, coverage and preservation review; V01 checks now independently pass.',
                            'current_evidence': pin(OUT / 'hash-audit-final.json')} for c in task['acceptance']],
         checks=[{'command': '.venv/Scripts/python.exe private/workflow/runs/IG-2B04/review-4fab98d5-01/audit.py hash-audit-initial.json', 'exit_code': 0, 'report': pin(OUT / 'hash-audit-initial.json')}]
               + [{'command': r['command'], 'exit_code': r['exit_code'], 'report': pin(OUT / (name + '.json'))} for name,r in [('repository',repository),('sources',sources),('diff',diff)]]
               + [{'command': '.venv/Scripts/python.exe private/workflow/runs/IG-2B04/review-4fab98d5-01/audit.py hash-audit-final.json', 'exit_code': 0, 'report': pin(OUT / 'hash-audit-final.json')}],
         findings=[], resolved_findings=[{
             'id': 'V01', 'result': 'resolved',
             'observation': 'Hash-pinned installed rg resolves in both approved validation processes. The complete inherited PATH remains a suffix; both pinned PYTHONPATH entries are present. Unchanged repository, source suite and diff checks exit zero.',
             'affected_criteria': prior_review['findings'][0]['affected_criteria'],
             'repair_validation': [pin(OUT / 'repository.json'), pin(OUT / 'sources.json'), pin(OUT / 'diff.json'), pin(OUT / 'hash-audit-final.json')]}],
         preserved_source_review={
             'inspection': pin(ROOT / 'review-ce506337-01/source-inspection.json'),
             'pages': [13,14,15,16], 'ledger_components': 113,
             'page_component_counts': closing['preserved_page_counts'],
             'coverage_match': 'Every prior component review matches the current ledger key, region ID, page, kind and normalized box; all prior component/page comparisons pass.',
             'audit_reports': [pin(ROOT / 'review-ce506337-01' / name) for name in ['evidence-regeneration-audit.json','reference-offset-audit.json','preservation-audit.json','coverage-audit.json','replay-audit.json']],
             'entry_exit_and_five_continuations': 'Prior complete review retained byte-for-byte. No new source access, rebuilding or reinterpretation was performed.'},
         operational_observations=[
             'A prior-review metadata selection excluded artifacts but inadvertently included review_artifacts, yielding an overlarge truncated metadata output. Later selections were bounded. No transcripts, dependency contents or unassigned source pages were read.'
         ],
         measurement={
             'evidence_phase_started_utc': load(OUT / 'checkpoint-initial.json')['utc'],
             'ended_utc': datetime.now(timezone.utc).isoformat(),
             'input_tokens': None, 'output_tokens': None, 'operator_seconds': None,
             'unknown_reason': 'Token usage and operator time are not exposed.',
             'defects_by_severity': {}, 'resolved_finding_ids': ['V01']},
         source_inspection_or_regeneration_performed=False,
         semantic_acceptance_granted=False, executable_readiness='unverified',
         queue_or_product_mutations=False,
         next_operation='Coordinator may evaluate technical acceptance under workflow gates. Reviewer stops after this role; no accepted/done decision is granted.')
write('review.json', e)
print({'outcome': 'pass', 'evidence': (OUT / 'review.json').as_posix(), 'sha256': pin(OUT / 'review.json')['sha256'], 'delivery_artifact_count':len(e['artifacts'])})
