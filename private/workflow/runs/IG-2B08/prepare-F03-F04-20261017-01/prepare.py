"""Authorize the two current independent findings, retaining the complete frozen lineage."""
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B08/prepare-F03-F04-20261017-01/'
OLD = 'private/workflow/runs/IG-2B08/repair-F02-validation02/'
NEW = 'private/workflow/runs/IG-2B08/repair-F03-F04-01/'
REVIEW = 'private/workflow/runs/IG-2B08/review-18a665c9/review.json'
SESSION = 'private/workflow/orchestrator/20261017T125512Z-933976c1/002-IG-2B08-reviewer-18a665c9/'
ACTOR = 'coordinator:operator-F03-F04-preparation-20261017-01'
CONFIG = 'Current coordinating model/reasoning metadata unavailable; this is not an executor claim. Fresh observed gpt-6.1-sol/high runtime is required for execution/review.'
REQUEST = 'Popraw limit napraw, żeby dotyczył każdego ustalenia osobno, przygotuj naprawy F03 i F04 i wznów orkiestrator od IG-2B08 w świeżej sesji.'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def write(name, body):
    with (ROOT / PREP / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(body, f, ensure_ascii=False, indent=2); f.write('\n')


def record(summary, **extra):
    return dict(role='coordinator', actor=ACTOR, model=None, reasoning=None,
                configuration_evidence=CONFIG, utc=o.utc(), summary=summary, **extra)


def main():
    q = w.read_json(ROOT / w.QUEUE); w.validate(q, ROOT)
    before = copy.deepcopy(q); disk_hash = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B08')
    assert task['status'] == 'review' and task['write_scope'] == [OLD]
    assert not (ROOT / NEW).exists() and not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
    write('task-before.json', task)
    event = task['events'][-1]
    assert event['to'] == 'review' and pin(event['evidence'])['sha256'] == event['sha256']
    delivery = w.read_json(ROOT / event['evidence'])
    review = w.read_json(ROOT / REVIEW)
    o.configuration_binding(ROOT, ROOT / SESSION, review)
    assert review['actor'] == 'ig2:002-IG-2B08-reviewer-18a665c9:reviewer'
    assert review['actor'] != delivery['actor'] and review['role'] == 'reviewer'
    assert review['artifacts'] == delivery['artifacts'] and review['criteria'] == task['acceptance']
    assert [f['id'] for f in review['findings']] == ['F03', 'F04']
    budget = o.finding_repair_budget(ROOT, task, review)
    assert not budget['exhausted'] and budget['prior_requests'] == {'F01': 1, 'F02': 1}
    write('repair-budget-before-request.json', budget)
    write('process-triage.json', record('Approved OS inspection found no old supervisor PID 19884 or reviewer PID 19508; no lock remains.',
          observed_matching_processes=0, old_pids=[19884, 19508],
          old_process=pin(SESSION + 'process.json')))
    previous_scope = w.read_json(ROOT / task['continuation_authorization']['scope']['path'])
    previous_preservation = w.read_json(ROOT / previous_scope['preserve_manifest']['path'])
    protected = previous_preservation['artifacts'] + delivery['artifacts'] + review.get('review_artifacts', [])
    protected += [pin(REVIEW), pin(event['evidence']), pin(SESSION + 'runtime-configuration.json'),
                  task['continuation_authorization']['scope'], task['continuation_authorization']['evidence']]
    protected += [task['context_recovery_authorization'][k] for k in ('incident', 'scope', 'assessment')]
    unique = {}
    for p in protected:
        if p['path'] in unique: assert unique[p['path']]['sha256'] == p['sha256']
        unique[p['path']] = p
    preserved = {'format': 'wgc-current-repair-preservation-1', 'artifacts': list(unique.values()),
                 'policy': 'Internal verification only; emit counts/status, never full manifests or unassigned records.'}
    o.verify_artifacts(ROOT, preserved)
    write('preserve-manifest.json', preserved)
    write('decision.json', record('The prior task-wide cap incorrectly blocked new F03/F04. The corrected limit counts each stable finding ID separately; existing review and source scope stay valid.',
          task=task['id'], operator_request=REQUEST, budget_before_current_request=budget,
          immutable_review=pin(REVIEW), immutable_delivery=pin(event['evidence']),
          correction='At most two repair requests for each stable finding ID across hash-verified authoritative prior reviews; combined requests count once per included ID. Missing/duplicate IDs or changed history stop evaluation. New IDs do not consume F01/F02 budgets.',
          current_resolution='Prepare only F03/F04 at a fresh absent root; retain resolved F01/F02, all original criteria/tests/source clipping and independent review.',
          semantic_acceptance=False, executable_readiness=False))
    # This is the already completed independent review, not a fabricated new one.
    # The existing transition gate verifies its entire frozen artifact list again.
    w.transition(q, ROOT, task['id'], 'changes_requested', REVIEW)
    task['outputs'] = [path.replace(OLD, NEW) for path in task['outputs']]
    task['outputs'].append(NEW + 'F03-F04-completeness-report.json')
    task['write_scope'] = [NEW]
    task['inventory_contract']['attempt_root'] = NEW.rstrip('/')
    scope = {'format': 'wgc-bounded-repair-scope-1', 'task': task['id'],
          'review_evidence': REVIEW, 'review_sha256': pin(REVIEW)['sha256'],
          'finding_ids': ['F03', 'F04'], 'attempt': NEW, 'acceptance': task['acceptance'], 'tests': task['tests'],
          'immutable_delivery': {'path': event['evidence'], 'sha256': event['sha256']},
          'mode': 'source_component_repair', 'preserve_manifest': pin(PREP + 'preserve-manifest.json'),
          'resolved_findings_to_preserve': ['F01', 'F02'],
          'allowed_changes': [
              'Repair or split only the zero-denominator intended page-29 V-counter/Tribune detail (F03) and later C 3-marker detail/frame (F04). Freshly determine complete original boundaries; preserve unrelated authored selections and all disjoint primary tiles.',
              'Adapt named current frozen delivery helpers into the new owned root; rebase all writes and runtime/claim bindings before running them. Never run a frozen helper at its old path.',
              'Regenerate affected evidence/ledgers/reports/indexes and full final plus two independent complete serial replay artifact sets at fresh paths. Preserve stable identities, registry history, accepted nonassigned records and retained reading order.',
              'Create source-bound full-component regressions rejecting both old clips; witness pixels alone or broader primary crops cannot establish intended component completeness. Preserve F01 full-arrow and F02 full-4-marker tests and evidence.',
              'Write fresh checks, checkpoint, exhaustive delivery and handoff only in the new attempt. No repository product/source/tool/schema/test edits or expanded source scope.'],
          'required_checks': list(dict.fromkeys(check for finding in review['findings'] for check in finding['repair_validation'])) + [
              'CURRENT operational prefix mapping: every older IG-2B08 output/test/helper command prefix, including repair-F02-validation02/, maps to repair-F03-F04-01/. Preserve all original suites/assertions; never write frozen attempts.',
              'Run source CLI validation via task_access.py validate-source for final-verified and both replay inventories with current executor ownership; keep raw check output private and release only command/exit/log pins.',
              'Hash-verify the complete current delivery and preserve-manifest before writes and delivery, emitting only counts/status; the independent reviewer rechecks them.'],
          'source_access': task['inventory_contract']['source_access'],
          'semantic_acceptance_granted': False, 'executable_readiness': False}
    write('repair-scope.json', scope)
    rows = {p['path']: p for p in delivery['artifacts']}
    helpers = ['build_inventory.py', 'check_arrow_completeness.py', 'check_hit_completeness.py',
               'freeze_delivery.py', 'inspect_originals.py', 'probe_geometry.py',
               'reconcile_reading_order.py', 'verify_batch.py']
    names = helpers + ['author-selections.json', 'author-inventory.json', 'author-registry.json',
          'region-ledger.json', 'component-ledger.json', 'original-page-inspection.json',
          'continuations.json', 'coverage-report.json', 'source-pins.json', 'toolchain.json',
          'preservation-report.json', 'replay-report.json', 'validation-report.json', 'delivery-handoff.md',
          'final-verified/inventory.json', 'final-verified/identity-registry.json']
    write('repair-context.json', {'format': 'wgc-current-repair-context-1', 'task': task['id'],
          'repair_scope': pin(PREP + 'repair-scope.json'), 'decision': pin(PREP + 'decision.json'),
          'review_reference': pin(REVIEW), 'review_summary': review['summary'], 'findings': review['findings'],
          'resolved_findings_to_preserve': ['F01', 'F02'], 'immutable_delivery': pin(event['evidence']),
          'named_current_inputs': {name: rows[OLD + name] for name in names},
          'accepted_baseline_contract': task['inventory_contract']['input_pins'],
          'private_read_protocol': 'This compact current context may be read in full. Read named helper source in bounded windows, copy/rebase to the new root before execution, and treat candidate implementations as untrusted. Select assigned-page/current component fields only; copy/hash/validate whole documents internally without emitting histories, manifest rows or unassigned source text. Source-pins/preservation indexes are internal inputs; counts/status only.',
          'scope_precedence': 'This LATER independent review repair supersedes initial F02 draft-revalidation ownership and draft/helper restrictions only for named reviewed repair-F02-validation02 candidate inputs. The stopped repair-F02-7582f722 helpers/transcripts remain forbidden. Frozen continuation/delivery and all earlier attempts stay immutable.',
          'source_access': task['inventory_contract']['source_access']})
    auth = record('Operator-authorized fresh F03/F04 repair after corrected per-finding budget evaluation.',
          task=task['id'], operator_request=REQUEST, criteria=task['acceptance'],
          artifacts=[pin(PREP + name) for name in ['repair-scope.json', 'repair-context.json', 'decision.json', 'preserve-manifest.json', 'repair-budget-before-request.json']] + [pin(REVIEW), pin(event['evidence'])],
          checks=[{'command': 'Independent runtime/identity, entire frozen delivery/preservation hashes and per-finding budget verified; 115 supervisor regression tests passed', 'exit_code': 0}],
          semantic_acceptance=False)
    write('authorization.json', auth)
    task['repair_authorization'] = {'review_evidence': REVIEW, 'review_sha256': pin(REVIEW)['sha256'],
          'scope': pin(PREP + 'repair-scope.json'), 'evidence': pin(PREP + 'authorization.json'), 'attempt': NEW}
    task['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md',
          'src/wgc/sources/README.md', 'docs/work/EVIDENCE.md', PREP + 'repair-context.json', PREP + 'decision.json']
    task['start_conditions'] = [
          'Dependencies are done. FIRST read CURRENT F03/F04 repair-context.json and the current repair scope; preserve all original criteria/tests and source limits.',
          'This is a later independent review repair. Current F03/F04 scope replaces initial continuation/F02 write ownership; only the new absent ' + NEW + ' is writable. Claim with a new actor, fresh observed gpt-6.1-sol/high runtime and checkpoint.',
          'Use only the named frozen delivered F02-validation02 helper/data candidates; read helper source in bounded windows and copy/rebase before execution. Do not use stopped F02-7582f722 helpers, wrappers, transcripts or old green-check/inspection claims.',
          'Freshly inspect all assigned original pages/boundaries/components and the exact page-33 crop. Repair complete F03 Tribune artwork/label/0 and F04 full 3-marker frame, retaining resolved F01/F02, unrelated selections, primary tiles, baseline objects, registry history and zero context denominator.',
          'Generate complete final and two separate independent serial replay sets, with exhaustive evidence indexes and fresh reports. Run unchanged source suites and exact task_access validators with private logs and current executor ownership.',
          'Verify all preservation bytes before writes and delivery, then obtain fresh independent review. Each stable finding ID has its own two-cycle budget; keep IDs stable across unresolved/reopened findings.',
          'Only the supervisor launches roles. No expanded source context, repository tooling/schema/test edits outside this owned run, global changes, nested agents, semantic acceptance or downstream IG-3 work.']
    task['blockers'] = ['A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.',
          'After two unchanged retries or two repair cycles for the same stable finding ID, block with evidence and the smallest decision needed. New distinct findings have independent budgets.']
    task['inputs'].append('CURRENT F03/F04 findings, exact frozen candidate inputs and operational mapping: ' + PREP + 'repair-context.json. Old attempts remain immutable.')
    old_task = next(t for t in before['tasks'] if t['id'] == task['id'])
    assert task['acceptance'] == old_task['acceptance'] and task['tests'] == old_task['tests']
    assert task['continuation_authorization'] == old_task['continuation_authorization']
    assert task['context_recovery_authorization'] == old_task['context_recovery_authorization']
    assert [t for t in q['tasks'] if t['id'] != task['id']] == [t for t in before['tasks'] if t['id'] != task['id']]
    assert w.digest(ROOT / w.QUEUE) == disk_hash
    policy_file = ROOT / 'docs/work/context-policy.json'; policy = w.read_json(policy_file)
    for rel in task['context'] + [PREP + 'repair-scope.json', PREP + 'authorization.json']:
        if rel not in policy['allow']: policy['allow'].append(rel)
    policy_file.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / w.QUEUE).write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for rel, body in w.views(q).items(): (ROOT / rel).write_text(body, encoding='utf-8')
    w.validate(q, ROOT); packet = w.packet(q, ROOT, task['id'], output=False)
    write('task-after.json', task)
    result = {'task': task['id'], 'status': task['status'], 'next_role': o.select(q)[1], 'fresh_attempt': NEW,
          'findings': scope['finding_ids'], 'preserved_artifacts': len(preserved['artifacts']),
          'packet_text_bytes': packet['text_bytes'], 'queue_sha256': w.digest(ROOT / w.QUEUE)}
    write('preparation-result.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__': main()
