import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
DISPATCH = Path('private/workflow/orchestrator/20261017T151724Z-86fb83c5/003-IG-2B08-coordinator-1e0c3c94')
PREP = Path('private/workflow/runs/IG-2B08/prepare-F03-F05-F09-1e0c3c94')
ATTEMPT = 'private/workflow/runs/IG-2B08/repair-F03-F05-F09-1e0c3c94/'
ACTOR = 'ig2:003-IG-2B08-coordinator-1e0c3c94:coordinator'

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pin(path):
    p = Path(path)
    return {'path': p.as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}

def verify(p):
    assert sha(p['path']) == p['sha256'], 'Immutable artifact mismatch'

def write(name, value):
    p = PREP / name
    assert not p.exists(), 'Preparation output must be absent'
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    return pin(p)

configuration = DISPATCH / 'runtime-configuration.json'
runtime = read(configuration)
assert (runtime['status'], runtime['model'], runtime['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
identity = dict(role='coordinator', actor=ACTOR, model=runtime['model'], reasoning=runtime['reasoning'],
                configuration_evidence=configuration.as_posix(), configuration_sha256=sha(configuration))
task = read(DISPATCH / 'task.json')
packet = read(DISPATCH / 'packet.json')
refs = read(DISPATCH / 'references.json')
assert not Path(ATTEMPT).exists(), 'Fresh repair directory must remain absent'
assert sha('docs/work/queue.json') == packet['queue_sha256'], 'Queue changed since dispatch'
review_pin = dict(path=refs['findings']['evidence'], sha256=refs['findings']['sha256'])
delivery_pin = dict(path=refs['prior_delivery']['evidence'], sha256=refs['prior_delivery']['sha256'])
verify(review_pin)
verify(delivery_pin)
review = read(review_pin['path'])
delivery = read(delivery_pin['path'])
assert review['outcome'] == 'changes_requested'
assert review['delivery_reference']['sha256'] == delivery_pin['sha256']
findings = review['findings']
ids = [f['id'] for f in findings]
assert ids == ['F03', 'F05', 'F06', 'F07', 'F08', 'F09']
old_scope_pin = task['repair_authorization']['scope']
verify(old_scope_pin)
old_scope = read(old_scope_pin['path'])
assert old_scope['finding_ids'] == ['F03', 'F04']
assert task['repair_authorization']['attempt'] == 'private/workflow/runs/IG-2B08/repair-F03-F04-01/'
assert review['reopened_findings'] == ['F03']
assert review['resolved_findings'] == ['F01', 'F02', 'F04']

# Hash-only preservation inspection never releases source records or manifest contents.
verify(delivery['preservation_manifest'])
old_preserve = read(delivery['preservation_manifest']['path'])
preserved = {}
for p in old_preserve['artifacts'] + delivery['artifacts'] + review.get('review_artifacts', []) + [
        pin(delivery_pin['path']), pin(review_pin['path']), pin(old_scope_pin['path'])]:
    verify(p)
    if p['path'] in preserved:
        assert preserved[p['path']]['sha256'] == p['sha256']
    preserved[p['path']] = dict(path=p['path'], sha256=p['sha256'], bytes=Path(p['path']).stat().st_size)
preserve_pin = write('preserve-manifest.json', {
    'format': 'wgc-immutable-preservation-manifest-1',
    'artifacts': list(preserved.values()),
    'policy': 'Verify all pins internally before writes and at delivery; emit counts/status only. Never modify frozen inputs.'})

base = 'private/workflow/runs/IG-2B08/repair-F03-F04-01/'
names = ['author-selections.json', 'author-inventory.json', 'author-registry.json',
         'build_inventory.py', 'inspect_originals.py', 'verify_batch.py',
         'check_arrow_completeness.py', 'check_hit_completeness.py', 'check_component_completeness.py',
         'freeze_delivery.py', 'toolchain.json', 'region-ledger.json', 'component-ledger.json',
         'source-pins.json', 'F03-F04-completeness-report.json']
by_path = {p['path']: p for p in delivery['artifacts']}
candidates = [by_path[base + name] for name in names]
required = list(dict.fromkeys(x for f in findings for x in f['repair_validation']))
budgets = {'F03': {'completed_cycles': 1, 'authorized_cycle': 2, 'maximum_cycles': 2}}
budgets.update({i: {'completed_cycles': 0, 'authorized_cycle': 1, 'maximum_cycles': 2} for i in ids if i != 'F03'})
allowed = [
    'Only the fresh absent attempt owns writes. Copy/rebase the named frozen current delivery candidates into it before execution; never run helpers at frozen paths.',
    'Correct or split only the named intended component selections for F03 and F05-F09 after original-source inspection. Preserve unrelated selections, disjoint primary tiles, denominator roles, accepted baseline records, registry history, and resolved F01/F02/F04 corrections.',
    'Create fresh source-bound full-component regression checks in the owned run. Reject every named incomplete crop and deliberately truncated top/right/bottom/left variants; verify complete artwork, glyphs, frames and applicable arrow masks. Witness rectangles identify defects, not sufficient replacement bounds.',
    'Reinspect every assigned original page/boundary/component and the exact authorized page-33 crop; regenerate complete final evidence, two separate complete serial replays, path-dependent locators, ledgers, exhaustive indexes, reports, owned helpers and delivery envelope.',
    'No repository source/tool/schema/test edits, expanded source access, old blocked helper/transcript access, nested roles, semantic acceptance, status transition by the coordinator, or downstream work.'
]
scope = {
    'format': 'wgc-bounded-repair-scope-1', 'task': task['id'],
    'review_evidence': review_pin['path'], 'review_sha256': review_pin['sha256'],
    'finding_ids': ids, 'attempt': ATTEMPT, 'acceptance': task['acceptance'], 'tests': task['tests'],
    'immutable_delivery': pin(delivery_pin['path']), 'mode': 'content_repair',
    'preserve_manifest': preserve_pin, 'resolved_findings_to_preserve': review['resolved_findings'],
    'finding_cycles': budgets, 'allowed_changes': allowed, 'required_checks': required,
    'source_access': task['inventory_contract']['source_access'],
    'semantic_acceptance_granted': False, 'executable_readiness': False,
}
scope_pin = write('repair-scope.json', scope)
context = {
    'format': 'wgc-current-repair-context-1', 'task': task['id'], 'scope': scope_pin,
    'current_review': pin(review_pin['path']), 'immutable_delivery': pin(delivery_pin['path']),
    'preserve_manifest': preserve_pin, 'finding_cycles': budgets,
    'findings': [{k: f[k] for k in ['id', 'status', 'title', 'description', 'required_repair']} |
                 {'components': [{k: c[k] for k in ['observation_index', 'key', 'region_id', 'page', 'points', 'witness_points', 'label']} for c in f['components']]}
                 for f in findings],
    'candidates': candidates,
    'path_mapping': {'to': ATTEMPT, 'from': [base,
        'private/workflow/runs/IG-2B08/repair-F02-validation02/',
        'private/workflow/runs/IG-2B08/repair-F02-7582f722/',
        'private/workflow/runs/IG-2B08/repair-F01-manifest02/',
        'private/workflow/runs/IG-2B08/inventory-p33-scope02/',
        'private/workflow/runs/IG-2B08/inventory-8d84cd90-01/']},
    'operational_rules': [
        'This CURRENT scope replaces all initial continuation and earlier repair write ownership and operational mappings. Acceptance/tests remain verbatim; map command/output operands into the fresh attempt only.',
        'F03 has one remaining cycle. Do not renumber/reset findings; if unresolved after this cycle, block with the smallest operator decision. New F05-F09 each begin cycle one of two.',
        'Fresh actor, observed gpt-6.1-sol/high, current claim and checkpoint precede executor product writes. Prior green checks and inspection claims are not inherited.',
        'Use only the exact three task_access validate-source commands after claim. Keep validation logs private. Preserve complete inherited process_pythonpath and Poppler process_path_prefix from pinned toolchain; install nothing.',
        'Serial evidence generation in the current Python process; two complete independent replay runs remain required. No multiprocessing or worker pools.',
        'Unchanged suites/assertions remain binding. For an observed Windows restricted-token failure request approved execution of the exact unchanged command; no restricted retry, ACL/library/test changes or bypass flag.',
        'Only the supervisor launches roles. Independent review is required; model/code review grants no human semantic acceptance or executable readiness.'
    ]}
context_pin = write('repair-context.json', context)
report_pin = write('preparation-report.json', {
    **identity, 'task': task['id'], 'utc': datetime.now(timezone.utc).isoformat(),
    'summary': 'Verified current review/delivery, packet/control hashes and every preserved artifact; allocated a fresh absent repair attempt without claiming or changing status.',
    'preserved_artifact_count': len(preserved), 'preservation_status': 'verified',
    'attempt_absent': True, 'finding_cycles': budgets, 'queue_events_unchanged': True,
    'acceptance_and_tests_unchanged': True, 'semantic_acceptance_granted': False,
    'executable_readiness': False})
authorization = {
    **identity, 'task': task['id'], 'utc': datetime.now(timezone.utc).isoformat(),
    'summary': 'Authorize only the bounded fresh F03 cycle-two and F05-F09 cycle-one content repair. Coordinator prepares the contract; only the supervisor may launch the next executor.',
    'review_evidence': review_pin['path'], 'review_sha256': review_pin['sha256'],
    'scope': scope_pin, 'attempt': ATTEMPT, 'mode': 'content_repair',
    'criteria': task['acceptance'], 'artifacts': [scope_pin, context_pin, pin(review_pin['path']), report_pin],
    'finding_cycles': budgets, 'status_unchanged': 'changes_requested',
    'semantic_acceptance_granted': False, 'executable_readiness': False,
    'measurement': {'input_tokens': None, 'output_tokens': None, 'operator_seconds': None,
                    'unknown_reason': 'Token counts and operator time were not exposed.'}}
authorization_pin = write('authorization.json', authorization)

# The coordinator's structural edit reads the queue internally without emitting events.
queue_path = Path('docs/work/queue.json')
assert sha(queue_path) == packet['queue_sha256']
queue = read(queue_path)
live = next(t for t in queue['tasks'] if t['id'] == task['id'])
events_before = copy.deepcopy(live['events'])
assert {k:v for k,v in live.items() if k != 'events'} == task
assert live['events'][-1]['sha256'] == review_pin['sha256']
live['outputs'] = [p.replace(base, ATTEMPT) for p in task['outputs']] + [ATTEMPT + 'F03-F05-F09-completeness-report.json']
live['write_scope'] = [ATTEMPT]
live['inventory_contract']['attempt_root'] = ATTEMPT.rstrip('/')
live['inputs'] = task['inputs'][:4] + [
    'Original immutable input pins remain at ' + task['inventory_contract']['input_pins']['path'] + '; source/page limits are unchanged.',
    task['inputs'][5],
    'CURRENT F03 and F05-F09 review, frozen candidate pins, preservation and command mapping: ' + context_pin['path'] + '. All prior attempts and deliveries remain immutable.']
live['context'] = task['context'][:4] + [context_pin['path'], scope_pin['path'], authorization_pin['path']]
live['start_conditions'] = [
    'Dependencies are done. FIRST read CURRENT repair-context.json and repair-scope.json in ' + PREP.as_posix() + '/; preserve every original acceptance criterion/test and exact source limit.',
    'This later repair replaces all previous continuation/repair write ownership. Only the fresh absent ' + ATTEMPT + ' is writable after fresh actor, observed gpt-6.1-sol/high, claim and checkpoint.',
    'Use only the named frozen repair-F03-F04-01 helper/data candidates; read needed source in bounded windows and copy/rebase before execution. No blocked-attempt helpers, wrappers, transcripts or inherited green-check/inspection claims.',
    'Repair CURRENT F03 and F05-F09 named details with full source-bound regression checks; preserve resolved F01/F02/F04, all unrelated selections, disjoint primary tiles, accepted 44-page baseline objects, registry history and zero context denominator.',
    'Freshly inspect all assigned original pages/boundaries/components and the exact page-33 crop. Generate complete final and two separate independent serial replay sets, exhaustive current indexes and fresh reports. Run every unchanged required check.',
    'Hash-verify the current preserve-manifest before product writes and delivery, emitting counts/status only. F03 is cycle two of two; F05-F09 are cycle one of two. Keep stable IDs and block rather than silently exceeding budgets.',
    'Only the supervisor launches roles. No expanded source context, repository tooling/schema/test edits, global changes, nested agents, semantic acceptance or downstream IG-3 work. Obtain fresh independent review.']
live['repair_authorization'] = {
    'review_evidence': review_pin['path'], 'review_sha256': review_pin['sha256'],
    'scope': scope_pin, 'evidence': authorization_pin, 'attempt': ATTEMPT}
assert live['status'] == 'changes_requested' and live['events'] == events_before
assert live['acceptance'] == scope['acceptance'] and live['tests'] == scope['tests']
policy_path = Path('docs/work/context-policy.json')
policy = read(policy_path)
for p in [context_pin['path'], scope_pin['path'], authorization_pin['path']]:
    if p not in policy['allow']:
        policy['allow'].append(p)
policy_path.write_text(json.dumps(policy, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({'task': task['id'], 'prepared': True, 'status': live['status'],
                  'events_unchanged': live['events'] == events_before, 'preserved_artifacts': len(preserved),
                  'attempt_absent': not Path(ATTEMPT).exists(), 'authorization': authorization_pin['path']}))
