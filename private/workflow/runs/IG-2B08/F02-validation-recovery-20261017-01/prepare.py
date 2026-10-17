"""Preserve the stopped F02 attempt and authorize fresh draft revalidation."""
import copy
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B08/F02-validation-recovery-20261017-01/'
OLD = 'private/workflow/runs/IG-2B08/repair-F02-7582f722/'
NEW = 'private/workflow/runs/IG-2B08/repair-F02-validation02/'
ORIGINAL_PREP = 'private/workflow/runs/IG-2B08/prepare-F02-7582f722/'
DENIAL = 'private/workflow/orchestrator/20261017T111422Z-80dfde30/003-IG-2B08-executor-ad7f232e/context-denied.json'
ACTOR = 'coordinator:operator-F02-validation-recovery-20261017-01'
CONFIG = 'Current coordinating model/reasoning metadata unavailable. Fresh executor/reviewer must confirm observed gpt-6.1-sol/high startup; no inherited identity or acceptance.'
REQUEST = 'Napraw zakres walidacji dla wykonawcy F02 i wznów orkiestrator od naprawy F02 w IG-2B08 w świeżej sesji. i czy orkiestrator moze automatycznie naprawiac aby pracowal a nie ciagle wymagal popychania i polecen ?'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def write(rel, body):
    target = w.safe_path(ROOT, rel)
    if target.exists():
        prior = w.read_json(target)
        comparable = lambda v: {k: x for k, x in v.items() if k != 'utc'}
        if comparable(prior) != comparable(body):
            raise ValueError('Existing preparation differs; preserve and use a new scope: ' + rel)
        return
    with target.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(body, stream, ensure_ascii=False, indent=2); stream.write('\n')


def record(summary, **extra):
    return dict(role='coordinator', actor=ACTOR, model=None, reasoning=None,
                configuration_evidence=CONFIG, utc=o.utc(), summary=summary, **extra)


def main():
    q = w.read_json(ROOT / w.QUEUE); w.validate(q, ROOT)
    before = copy.deepcopy(q); disk_hash = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B08')
    assert task['status'] == 'in_progress' and task['write_scope'] == [OLD]
    assert not (ROOT / NEW).exists() and not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
    write(PREP + 'task-before.json', task)
    denial = w.read_json(ROOT / DENIAL)
    assert denial['helper'] == 'task_access.validate_source'
    assert denial['reason'] == 'Inventory is not in the pinned validation scope'
    process = w.read_json((ROOT / DENIAL).with_name('process.json'))
    assert process['state'] == 'exited'
    write(PREP + 'process-triage.json', record('Approved OS inspection found no old supervisor/executor or F02 validation workers; the process record confirms exit.',
          old_pids=[9056, 11896], matching_processes=0, old_process=pin((Path(DENIAL).parent / 'process.json').as_posix())))
    write(PREP + 'incident.json', record('Executor validation was refused because only reviewer dispatch populated validation operands.',
          format='wgc-executor-validation-scope-incident-1', task=task['id'], original_denial=pin(DENIAL),
          denial=denial, source_context_expanded=False, guard_stopped_before_fallback=True))
    # Preserve this exact stopped attempt without releasing its source/manifests.
    if (ROOT / OLD / 'blocked-state-manifest.json').exists():
        original = w.read_json(ROOT / OLD / 'blocked-state-manifest.json')['artifacts']
        o.verify_artifacts(ROOT, {'artifacts': original})
    else:
        original = []
        for base, dirs, files in os.walk(ROOT / OLD):
            dirs[:] = [d for d in dirs if d not in {'source-pytest', 'pytest', '__pycache__', 'temp'}]
            for name in sorted(files): original.append(pin((Path(base) / name).relative_to(ROOT).as_posix()))
        original.sort(key=lambda p: p['path'])
    write(OLD + 'blocked-state-manifest.json', {'format': 'wgc-blocked-state-1', 'artifacts': original,
          'policy': 'Frozen candidate bytes; no accepted output or inherited inspection. Pytest scratch retained but excluded.'})
    blocked = record('F02 executor stopped on a validation-scope configuration defect; preserve its draft attempt for operator-authorized fresh revalidation.',
          task=task['id'], criteria=task['acceptance'],
          artifacts=[pin(OLD + 'blocked-state-manifest.json'), pin(OLD + 'checkpoint.json'), pin(OLD + 'claim.json'), pin(DENIAL), pin(PREP + 'incident.json')],
          blocker='Executor had no pinned owned-output validation operands.',
          checks=[{'command': 'Approved process exit/ownership inspection and exact denial assessment', 'exit_code': 0}],
          next_operation='Fresh owned-output validation binding, fresh draft-revalidation executor and independent review.')
    write(OLD + 'blocked.json', blocked)
    w.transition(q, ROOT, task['id'], 'blocked', OLD + 'blocked.json')

    prior_auth = copy.deepcopy(task['repair_authorization'])
    old_scope = w.read_json(ROOT / prior_auth['scope']['path'])
    prior_manifest = w.read_json(ROOT / old_scope['preserve_manifest']['path'])
    review = w.read_json(ROOT / prior_auth['review_evidence'])
    protected = original + blocked['artifacts'] + [pin(OLD + 'blocked.json')] + prior_manifest['artifacts']
    protected += review.get('review_artifacts', []) + [pin(prior_auth['review_evidence']), prior_auth['scope'], prior_auth['evidence']]
    protected += [task['context_recovery_authorization'][k] for k in ('incident', 'scope', 'assessment')]
    unique = {}
    for item in protected:
        if item['path'] in unique: assert unique[item['path']]['sha256'] == item['sha256']
        unique[item['path']] = item
    preserved = {'format': 'wgc-F02-recovery-preservation-1', 'artifacts': list(unique.values()),
                 'policy': 'Internal verification only; counts/status, never manifest output.'}
    o.verify_artifacts(ROOT, preserved)
    write(PREP + 'preserve-manifest.json', preserved)
    write(PREP + 'assessment.json', record('The source scope was correct; the tool dispatch omitted executor validation authority. Bind generated outputs to the exact current claim and observed runtime.',
          task=task['id'], operator_request=REQUEST, incident=pin(PREP + 'incident.json'),
          fix='Executor dispatch lists exactly final-verified/replay-1/replay-2 inventory paths under its owned attempt. The helper requires current claim/session/runtime ownership and snapshots/checks the bytes and queue for each call. Reviewer hash pins remain strict.',
          source_scope_unchanged=True, acceptance_and_tests_unchanged=True,
          fresh_execution_policy='Candidate authored JSON only; regenerate evidence and complete replays, re-inspect all assigned sources, re-run checks. No old F02 helper/transcript or completed-state reuse.',
          automatic_recovery='Role-appropriate validation scopes are generated automatically. Pre-model Windows sharing/access I/O may retry at most twice in fresh dispatch directories with an unchanged queue. Context/source refusals and unknown errors remain stops.',
          semantic_acceptance=False, executable_readiness=False))
    repair = copy.deepcopy(old_scope)
    for k in ['configuration_sha256']: repair.pop(k, None)
    repair.update(actor=ACTOR, model=None, reasoning=None, configuration_evidence=CONFIG,
                  utc=o.utc(), attempt=NEW, summary='Retain the exact F02 finding/gates in a fresh operator-authorized continuation attempt.',
                  preserve_manifest=pin(PREP + 'preserve-manifest.json'))
    repair['required_checks'] = old_scope['required_checks'] + [
          'CURRENT continuation command mapping: all older IG-2B08 inventory/repair output and test operands, including repair-F02-7582f722/, map to repair-F02-validation02/. Keep every original suite/assertion; no writes to frozen roots.',
          'Executor and reviewer both use task_access.py validate-source for the exact three current inventories. Executor dispatch supplies owned paths, claims bind fresh observed runtime, and check output stays private.']
    write(PREP + 'repair-scope.json', repair)
    candidates = [pin(OLD + name) for name in ['author-selections.json', 'author-inventory.json', 'author-registry.json']]
    context = {'format': 'wgc-F02-recovery-context-1', 'task': task['id'],
          'current_repair_scope': pin(PREP + 'repair-scope.json'),
          'frozen_F02_review': {'path': prior_auth['review_evidence'], 'sha256': prior_auth['review_sha256']},
          'finding': old_scope['finding'], 'resolved_findings_to_preserve': old_scope['resolved_findings_to_preserve'],
          'candidate_drafts': candidates,
          'frozen_helper_context': pin(ORIGINAL_PREP + 'repair-context.json'),
          'original_accepted_input_contract': task['inventory_contract']['input_pins'],
          'protocol': 'Read the compact CURRENT finding and exact named candidate fields only. The frozen helper context names F01 delivered helper candidates; bounded read/copy/adaptation of ONLY those reviewed helper files remains permitted. Do not read or execute stopped F02 helpers, wrappers or transcripts. Draft JSON is not source proof; fresh original inspection and full evidence/replay rebuilding are required. Hash/copy full records internally without output.',
          'source_access': task['inventory_contract']['source_access']}
    write(PREP + 'repair-context.json', context)
    continuation = {'format': 'wgc-draft-revalidation-scope-1', 'task': task['id'], 'mode': 'draft_revalidation',
          'blocked_evidence': OLD + 'blocked.json', 'blocked_sha256': pin(OLD + 'blocked.json')['sha256'],
          'blocked_attempt': OLD, 'attempt': NEW, 'acceptance': task['acceptance'], 'tests': task['tests'],
          'preserve_manifest': pin(PREP + 'preserve-manifest.json'), 'drafts': candidates,
          'repair_context': pin(PREP + 'repair-context.json'), 'current_repair_scope': pin(PREP + 'repair-scope.json'),
          'assessment': pin(PREP + 'assessment.json'), 'source_access': task['inventory_contract']['source_access'],
          'validation_protocol': 'Use task_access.py validate-source for the three exact fresh generated outputs after a fresh observed claim. It snapshots each generated input and rejects ownership changes; logs remain private. No arbitrary paths or raw output.',
          'restart_protocol': 'Fresh absent directory and fresh executor actor/runtime/claim. Use the named draft JSON as candidates only. Reinspect all assigned original pages and boundaries/components, preserve F01, regenerate complete final and two serial replays plus reports/indexes, run unchanged checks, then obtain independent review.',
          'path_mapping': {'to': NEW, 'from': [OLD, 'private/workflow/runs/IG-2B08/repair-F01-manifest02/',
              'private/workflow/runs/IG-2B08/inventory-p33-scope02/', 'private/workflow/runs/IG-2B08/inventory-8d84cd90-01/']},
          'preservation_policy': 'Preserved bytes are verified before/after every role and on later dispatch. Read no stopped F02 helper/transcript; retain exact source/page clipping and unchanged criteria/tests. No previous green check or inspection claim is inherited.',
          'semantic_acceptance': False}
    write(PREP + 'scope.json', continuation)
    auth = record('Operator authorizes fresh F02 draft revalidation after the executor validation binding was corrected.',
          task=task['id'], operator_request=REQUEST, criteria=task['acceptance'],
          artifacts=[pin(PREP + name) for name in ['scope.json', 'assessment.json', 'repair-scope.json', 'repair-context.json', 'preserve-manifest.json', 'incident.json']] + [pin(OLD + 'blocked.json')],
          checks=[{'command': 'Preserved-byte verification, exact F02 review binding, no live prior writer and 138 passing context/orchestrator regression tests', 'exit_code': 0}],
          semantic_acceptance=False)
    write(PREP + 'authorization.json', auth)
    task['outputs'] = [p.replace(OLD, NEW) for p in task['outputs']]
    task['write_scope'] = [NEW]
    task['inventory_contract']['attempt_root'] = NEW.rstrip('/')
    task['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md', 'src/wgc/sources/README.md',
          'docs/work/EVIDENCE.md', PREP + 'scope.json', PREP + 'assessment.json', PREP + 'repair-context.json']
    task['context_recovery_authorization'] = {'incident': pin(PREP + 'incident.json'), 'scope': pin(PREP + 'scope.json'),
                                             'assessment': pin(PREP + 'assessment.json')}
    task['continuation_authorization'] = {'scope': pin(PREP + 'scope.json'), 'evidence': pin(PREP + 'authorization.json'),
          'blocked_evidence': OLD + 'blocked.json', 'blocked_sha256': pin(OLD + 'blocked.json')['sha256'], 'attempt': NEW}
    task['repair_authorization'].update(scope=pin(PREP + 'repair-scope.json'), evidence=pin(PREP + 'authorization.json'), attempt=NEW)
    task['start_conditions'] = [
          'Dependencies are done; preserve every original criterion, test and source-access limit.',
          'FIRST read CURRENT continuation scope/assessment and repair-context.json. This authorizes only F02 draft revalidation under the exact fresh root; older operational write/test prefixes are superseded by the current scope mapping.',
          'Claim only the new absent ' + NEW + ' with a new actor, observed confirmed gpt-6.1-sol/high runtime and fresh packet/checkpoint. Old F02 files remain immutable candidate data, with no inherited inspection/check/acceptance.',
          'Read only named JSON draft fields and the frozen reviewed F01 helper candidates named by the pinned original F02 helper context. Do not read stopped F02 derivation helpers, wrappers or transcripts. Copy/rebase reviewed helper candidates into the new root before execution.',
          'Reinspect every assigned original page, boundary/component and exact page-33 context. Preserve F01 full-arrow checks, unrelated selections, primary tiles, accepted baseline objects, registry history and zero context denominator; regenerate complete final and both independent serial replay sets.',
          'After claiming, use task_access.py validate-source for the three generated current inventory paths. Exact owned-output authority is dispatched automatically. Capture all check output privately; commands/exits/pins only.',
          'Verify every preserved byte pin before writes and before delivery; run unchanged required suites and fresh independent review. No extra source context, product tooling/schema/test edits outside this run, global configuration, nested agents or downstream work.']
    task['inputs'].append('CURRENT operator recovery and F02 candidate draft/input references: ' + PREP + 'repair-context.json. Current scope maps old command/output prefixes to the fresh continuation root.')
    # workflow.transition validates current context immediately. Register exactly
    # these new private references before publishing any transition using them.
    policy_path = ROOT / 'docs/work/context-policy.json'; policy = w.read_json(policy_path)
    for rel in task['context'] + [PREP + 'repair-scope.json', PREP + 'authorization.json']:
        if rel not in policy['allow']: policy['allow'].append(rel)
    policy_path.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    # The actual task state transitions remain standard workflow events.
    write(PREP + 'planned.json', record('Corrected executor binding and exact current recovery scope resolve the recorded blocker.',
          criteria=task['acceptance'], artifacts=[pin(PREP + 'authorization.json')]))
    w.transition(q, ROOT, task['id'], 'planned', PREP + 'planned.json')
    write(PREP + 'ready.json', record('F02 draft-revalidation inputs, source scope and fresh ownership are pinned; execution awaits new observed runtime.',
          criteria=task['acceptance'], artifacts=[pin(PREP + 'authorization.json'), pin(PREP + 'scope.json')]))
    w.transition(q, ROOT, task['id'], 'ready', PREP + 'ready.json')
    old_task = next(t for t in before['tasks'] if t['id'] == task['id'])
    assert task['acceptance'] == old_task['acceptance'] and task['tests'] == old_task['tests']
    assert [t for t in q['tasks'] if t['id'] != task['id']] == [t for t in before['tasks'] if t['id'] != task['id']]
    assert w.digest(ROOT / w.QUEUE) == disk_hash
    (ROOT / w.QUEUE).write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for rel, body in w.views(q).items(): (ROOT / rel).write_text(body, encoding='utf-8')
    w.validate(q, ROOT)
    packet = w.packet(q, ROOT, task['id'], output=False)
    write(PREP + 'task-after.json', task)
    result = {'task': task['id'], 'status': task['status'], 'next_role': o.select(q)[1],
          'fresh_attempt': NEW, 'preserved_artifacts': len(preserved['artifacts']), 'frozen_F02_drafts': len(original),
          'packet_text_bytes': packet['text_bytes'], 'queue_sha256': w.digest(ROOT / w.QUEUE)}
    write(PREP + 'preparation-result.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
