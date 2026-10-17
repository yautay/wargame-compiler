"""Prepare the current F02 contract; never execute or mutate frozen product evidence."""
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path.cwd()
SESSION = Path('private/workflow/orchestrator/20261017T111422Z-80dfde30/002-IG-2B08-coordinator-7582f722')
PREP = Path('private/workflow/runs/IG-2B08/prepare-F02-7582f722')
ATTEMPT = 'private/workflow/runs/IG-2B08/repair-F02-7582f722/'
ACTOR = 'ig2:002-IG-2B08-coordinator-7582f722:coordinator'
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def pin(path):
    return {'path': str(path).replace('\\', '/'), 'sha256': digest(path), 'bytes': Path(path).stat().st_size}

def write_new(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')

def verify(pins):
    for item in pins:
        assert digest(item['path']) == item['sha256'], 'Pinned artifact changed'
    return len(pins)

configuration = SESSION / 'runtime-configuration.json'
runtime = read(configuration)
assert runtime['status'] == 'confirmed' and runtime['model'] == 'gpt-6.1-sol' and runtime['reasoning'] == 'high'
identity = {'role': 'coordinator', 'actor': ACTOR, 'model': runtime['model'], 'reasoning': runtime['reasoning'],
            'configuration_evidence': configuration.as_posix(), 'configuration_sha256': digest(configuration)}
task = read(SESSION / 'task.json')
references = read(SESSION / 'references.json')
review_pin = {'path': references['findings']['evidence'], 'sha256': references['findings']['sha256']}
delivery_pin = {'path': references['prior_delivery']['evidence'], 'sha256': references['prior_delivery']['sha256']}
verify([review_pin, delivery_pin])
review = read(review_pin['path'])
delivery = read(delivery_pin['path'])
assert review['outcome'] == 'changes_requested' and [f['id'] for f in review['findings']] == ['F02']
assert review['delivery']['sha256'] == delivery_pin['sha256']
recovery_scope = read(task['context_recovery_authorization']['scope']['path'])
preserve_pin = recovery_scope['preserve_manifest']
verify([preserve_pin])
preserved = read(preserve_pin['path'])['artifacts']
assert not Path(ATTEMPT).exists()
counts = {'delivery_artifacts': verify(delivery['artifacts']), 'preserved_artifacts': verify(preserved)}
verify([item for finding in review['findings'] for item in finding['evidence']])
current_context = read('private/workflow/runs/IG-2B08/validation-context-recovery-20261017-01/review-context.json')
named_inputs = copy.deepcopy(current_context['named_current_inputs'])
# Current frozen product helpers are candidate inputs, never inherited proof.
for item in delivery['artifacts']:
    if item['path'].endswith('.py'):
        named_inputs[Path(item['path']).name] = item
verify(list(named_inputs.values()))
required_checks = copy.deepcopy(review['findings'][0]['repair_validation'])
required_checks.extend([
    'All original task tests remain verbatim. For command operands and outputs, the NEW repair-F02-7582f722/ prefix supersedes every older inventory-8d84cd90-01/, inventory-p33-scope02/ and repair-F01-manifest02/ prefix under IG-2B08. Never run a frozen helper at its frozen path or write test artifacts into an old attempt.',
    'Hash-verify the complete immutable delivery and the current preserve-manifest internally before any executor product writes and again before delivery; print only counts/status. Preserve all old artifacts byte-for-byte.',
    'Generate final-verified and both complete independent replays at fresh owned paths, serially in the current Python process; no multiprocessing or worker pools. Preserve every region/component, all existing suites/assertions, all F01 full-arrow checks and accepted nonassigned baseline objects.',
    'Use inherited process_pythonpath with BOTH repo/src and bundled Python Lib/site-packages and process_path_prefix from the pinned toolchain. Do not replace PYTHONPATH, install dependencies, change ACLs or global settings.',
    'Keep check output private. For independent reviewer source CLI validation use task_access.py validate-source for each newly pinned inventory. Before executor dispatch the supervisor must prepare exact fresh output access; no raw validator log previews.',
    'If the restricted token denies the unchanged pytest temp access or terminating an owned context-guard synthetic process tree, request approved execution of the exact unchanged command. Do not retry that denied restricted command or weaken assertions. At most two repairs per finding and two retries of an unchanged failure.',
    'A fresh independent reviewer must inspect all assigned original pages, every boundary/component and the exact page-33 continuation, verify F02 completeness and preserved F01 correction, all frozen artifact hashes, baseline preservation, both complete replays, current indexes, original criteria and unchanged required checks. No human semantic acceptance or executable readiness is granted.'
])
scope = dict(identity, format='wgc-bounded-repair-scope-1', task=task['id'], utc=datetime.now(timezone.utc).isoformat(),
             summary='Authorize only the current F02 page-29 hit-marker component repair at a new absent attempt.',
             review_evidence=review_pin['path'], review_sha256=review_pin['sha256'], finding_ids=['F02'],
             attempt=ATTEMPT, acceptance=copy.deepcopy(task['acceptance']), tests=copy.deepcopy(task['tests']),
             immutable_delivery=delivery_pin, mode='source_component_repair',
             preserve_manifest=preserve_pin, finding=review['findings'][0], resolved_findings_to_preserve=review['resolved_findings'],
             allowed_changes=[
                 'Only inside the fresh owned attempt: correct or split the zero-denominator ig2b08:p29:collapse-diagram-component-c-hits selection so the complete visible digit 4 and marker are included in its intended detail evidence.',
                 'Create source-bound F02 regression evidence rejecting [106,496,133,527], including the 51-pixel source witness patch and full visible stem/marker extent; key-set equality or a single point is insufficient.',
                 'Copy/adapt only the named current frozen product helpers into the fresh owned attempt as candidate implementations. Rebase all write paths before execution. Regenerate the full final and two separately generated complete serial replay sets, affected ledgers/reports and exhaustive current source/delivery indexes.',
                 'Freshly inspect assigned original pages 29-32 and all proposed boundaries/components. Preserve primary tiles, F01 full-arrow evidence/checks, accepted baseline objects, retained order, registry history, page-28 reference-only continuation and zero context denominator.',
                 'Write fresh run-owned checkpoints, reports, exact unchanged validation logs, handoff and exhaustive ordered delivery pins. No repository source/tool/schema/test edits, no writes to any frozen attempt or prior delivery.'
             ], required_checks=required_checks, source_access=copy.deepcopy(task['inventory_contract']['source_access']),
             semantic_acceptance_granted=False, executable_readiness=False)
scope_path = PREP / 'repair-scope.json'
write_new(scope_path, scope)
index = {
    'format': 'wgc-current-repair-context-1', 'task': task['id'], 'review': review_pin, 'immutable_delivery': delivery_pin,
    'repair_scope': pin(scope_path), 'finding_ids': ['F02'], 'preserve_manifest': preserve_pin,
    'named_current_inputs': named_inputs,
    'input_pins': task['inventory_contract']['input_pins'],
    'private_read_policy': 'Read this compact index in full. Current finding is F02 from the pinned review. Large frozen envelopes/indexes are internal verification inputs only: emit counts/status, never whole artifact lists or unassigned records/text. Read assigned page/region/component fields and explicitly boundary-linked IDs only. No old review wrapper, transcript or derivation helper from blocked attempts.',
    'helper_policy': 'Only the named current repair-F01-manifest02 product helpers may be read in bounded windows and copied as candidate implementation to the new attempt. Never execute at frozen paths. Verify and rebase all writes first; frozen validators with broad console output must be adapted only in the new run to log privately. Prior green checks and observations are not inherited.',
    'precedence': 'This current F02 scope replaces obsolete F01 write ownership, output prefix and review-only start instructions. Operator context recovery source/output limits remain binding; earlier correction and frozen delivery remain immutable.'
}
index_path = PREP / 'repair-context.json'
write_new(index_path, index)
checks = [{'command': 'Verify current review, immutable delivery, complete preservation manifest and named current input hashes', 'exit_code': 0, **counts},
          {'command': 'Verify fresh owned attempt is absent and preserve exact acceptance/tests', 'exit_code': 0}]
authorization = dict(identity, format='wgc-coordinator-repair-authorization-1', task=task['id'],
                     utc=datetime.now(timezone.utc).isoformat(), summary='Authorize a bounded first F02 repair, preserving the current frozen F01 correction and every original acceptance criterion/test. No execution, status transition, acceptance or downstream readiness is granted by this preparation.',
                     criteria=copy.deepcopy(task['acceptance']), review_evidence=review_pin['path'], review_sha256=review_pin['sha256'],
                     finding_ids=['F02'], attempt=ATTEMPT, mode=scope['mode'], immutable_delivery=delivery_pin,
                     artifacts=[pin(scope_path), dict(review_pin), pin(index_path)], checks=checks,
                     semantic_acceptance_granted=False, executable_readiness=False,
                     next_operation='Supervisor validates this authorization and launches only the next fresh observed executor; executor first reads the current repair scope, claims the fresh attempt and records a checkpoint. Independent review remains required.')
authorization_path = PREP / 'authorization.json'
write_new(authorization_path, authorization)

lock = ROOT / 'private/workflow/queue.lock'
fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    queue_path = ROOT / 'docs/work/queue.json'
    before_hash = digest(queue_path)
    assert before_hash == read(SESSION / 'packet.json')['queue_sha256'], 'Queue authority changed since dispatch'
    before = read(queue_path)
    after = copy.deepcopy(before)
    live = next(t for t in after['tasks'] if t['id'] == task['id'])
    assert {k:v for k,v in live.items() if k != 'events'} == task, 'Selected contract differs from task snapshot'
    assert live['events'][-1]['evidence'] == review_pin['path'] and live['events'][-1]['sha256'] == review_pin['sha256']
    old_prefix = task['inventory_contract']['attempt_root'] + '/'
    live['outputs'] = [ATTEMPT + p.removeprefix(old_prefix) for p in task['outputs']]
    live['outputs'].append(ATTEMPT + 'F02-completeness-report.json')
    live['write_scope'] = [ATTEMPT]
    live['inventory_contract']['attempt_root'] = ATTEMPT.rstrip('/')
    live['inputs'] = [x for x in live['inputs'] if 'Current F01 findings and named frozen candidate' not in x]
    live['inputs'].append('CURRENT F02 finding, frozen delivery and named current candidate input pins: ' + index_path.as_posix() + '. Read only the bounded current context; the old delivery and all earlier corrections remain immutable.')
    live['context'] = [x for x in live['context'] if x != 'private/workflow/runs/IG-2B08/validation-context-recovery-20261017-01/review-context.json']
    live['context'].extend([scope_path.as_posix(), index_path.as_posix(), authorization_path.as_posix()])
    live['start_conditions'] = [
        'All dependencies are done; input revisions and assigned file scope are pinned.',
        'FIRST read the current F02 repair-scope.json and compact repair-context.json pinned by repair_authorization. Current F02 ownership and command mapping replace obsolete F01/review-only instructions. The operator context recovery source/output limits remain binding.',
        'Observed confirmed gpt-6.1-sol/high configuration and a distinct fresh actor are required. Claim only the exact new absent repair attempt, write a fresh checkpoint and verify all preserved inputs before product writes. Do not recreate or write any frozen root.',
        'Correct only the current F02 component and dependent evidence/reports in the fresh run; preserve resolved F01, all primary tiles, accepted nonassigned records, registry history and zero context denominator. Keep every original acceptance criterion and test unchanged; apply the latest scope command-prefix mapping.',
        'Original source scope remains pages 29-32, reference-only page 28 and exact page-33 continuation crop. Set clipping before text/pixel output. A context/helper refusal or indispensable extra source requirement stops the session for new coordinator scope.',
        'Generate the complete final and two independent serial replay artifact sets separately. No multiprocessing or worker pools. Do not inherit old observations or green checks; freshly inspect every assigned original/boundary/component and revalidate all required checks.',
        'Preserve the inherited pinned toolchain paths including bundled site-packages and Poppler. Capture all validation/check output in new private logs; release commands/exits and scoped summaries only. Use approved exact unchanged execution for observed Windows access failures; no denied restricted retry, ACL changes or weakened tests.',
        'Only the supervisor launches subsequent roles. No source/product tooling/schema/test edits outside the owned repair run, online services, global configuration, nested agents, unrelated tasks, semantic acceptance or downstream IG-3 work.'
    ]
    live['repair_authorization'] = {'review_evidence':review_pin['path'], 'review_sha256':review_pin['sha256'],
                                    'scope':pin(scope_path), 'evidence':pin(authorization_path), 'attempt':ATTEMPT}
    assert live['acceptance'] == task['acceptance'] and live['tests'] == task['tests']
    o.check_queue_delta(before, after, next(t for t in before['tasks'] if t['id']==task['id']), 'coordinator', outcome='progress')
    policy_path = ROOT / 'docs/work/context-policy.json'
    policy_before = read(policy_path)
    policy_after = copy.deepcopy(policy_before)
    for path in (scope_path, index_path, authorization_path):
        if path.as_posix() not in policy_after['allow']:
            policy_after['allow'].append(path.as_posix())
    # Preserve every preexisting record; append only exact small preparation files.
    assert policy_after['allow'][:len(policy_before['allow'])] == policy_before['allow']
    policy_pending = policy_path.with_name('context-policy.F02-7582f722.pending.json')
    queue_pending = queue_path.with_name('queue.F02-7582f722.pending.json')
    write_new(policy_pending, policy_after)
    write_new(queue_pending, after)
    assert digest(queue_path) == before_hash, 'Concurrent queue writer'
    os.replace(policy_pending, policy_path)
    os.replace(queue_pending, queue_path)
    w.validate(after, ROOT, check_views=False)
    w.render(after, ROOT)
    w.validate(after, ROOT)
    o.verify_repair_authorization(ROOT, live)
    write_new(PREP / 'preparation-result.json', dict(identity, task=task['id'], status='changes_requested', events_unchanged=True,
              acceptance_unchanged=True, tests_unchanged=True, attempt_absent=not Path(ATTEMPT).exists(),
              queue_sha256=digest(queue_path), scope=pin(scope_path), authorization=pin(authorization_path),
              checks=checks+[{'command':'Coordinator queue delta, render, view validation and repair authorization validation', 'exit_code':0}]))
    print(json.dumps({'status':'prepared','authorization':authorization_path.as_posix(),'attempt_absent':True, **counts}))
finally:
    os.close(fd)
    lock.unlink()
