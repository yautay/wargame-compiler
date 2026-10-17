"""Prepare the operator-authorized recovery without promoting blocked candidates."""
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w
import dependency_context as d

PREP = 'private/workflow/runs/IG-2B05/recovery-20261016-dependency03/'
OLD = 'private/workflow/runs/IG-2B05/inventory-17-20-01/'
NEW = 'private/workflow/runs/IG-2B05/continuation-17-20-dependency03/'


def write(rel, body):
    path = w.safe_path(ROOT, rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(body, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return pin(rel)


def pin(rel):
    path = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(path), 'bytes': path.stat().st_size}


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    queue_before = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B05')
    original = copy.deepcopy(task)
    if task['status'] != 'blocked' or task['events'][-1]['evidence'] != OLD + 'blocked.json':
        raise ValueError('Selected blocker changed; do not reuse this recovery')
    if (ROOT / NEW).exists() or (ROOT / 'private/workflow/ig2-orchestrator.lock').exists():
        raise ValueError('New ownership unavailable')
    blocked = task['events'][-1]
    incident = pin(blocked['evidence'])
    if incident['sha256'] != blocked['sha256']:
        raise ValueError('Blocked incident bytes changed')
    body = w.read_json(ROOT / blocked['evidence'])
    manifest = pin(OLD + 'blocked-attempt-preservation.json')
    if manifest not in body['artifacts']:
        raise ValueError('Preservation manifest is not the exact blocked-event artifact')
    original_files = w.read_json(ROOT / manifest['path'])['artifacts']
    o.verify_artifacts(ROOT, {'artifacts': original_files})
    preserved = list(original_files)
    for item in body['artifacts'] + [incident, {'path': incident['path'], 'sha256': incident['sha256']}]:
        if item not in preserved:
            preserved.append(item)
    for check in body.get('checks', []):
        for item in ([check['log']] if 'log' in check else []) + check.get('stage_logs', []):
            if item not in preserved:
                preserved.append(item)
    o.verify_artifacts(ROOT, {'artifacts': preserved})
    preserve = write(PREP + 'preserve-manifest.json', {
        'format': 'wgc-recovery-preservation-1', 'task': task['id'],
        'original_manifest': manifest, 'artifacts': preserved,
        'candidate_only': True, 'original_prefix_count': len(original_files)})
    drafts = [pin(OLD + name) for name in (
        'authored-partition.json', 'persisted-registry.json',
        'final-verified/inventory.json', 'final-verified/identity-registry.json')]
    assessment = write(PREP + 'assessment.json', {
        'format': 'wgc-context-incident-assessment-1', 'task': task['id'],
        'utc': datetime.now(timezone.utc).isoformat(),
        'operator_request': 'wznow prace',
        'incident': incident,
        'cause': 'The prior executor directly read dependency-inputs.json instead of using the pinned dependency projection.',
        'effect': 'The previous session cannot claim context compliance; all results remain unaccepted candidates.',
        'recovery': 'Fresh executor context and absent owned directory, exact draft JSON pins, fresh original-page inspection, regenerated path-dependent evidence, two complete fresh replays, fresh checks and independent review.',
        'process_evidence': {
            'previous_supervisor_pid': 18572, 'previous_executor_pid': 18612,
            'inspection': 'Approved Win32_Process query returned neither recorded PID; both supervisor and queue lock are absent.',
            'previous_run_state': 'blocked', 'previous_executor_state': 'exited'},
        'tooling_issue': 'The frozen original manifest is named blocked-attempt-preservation.json. The supervisor now accepts that exact blocked-event pin as well as blocked-state-manifest.json and still rejects missing or ambiguous manifests.',
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Current coordinating session does not expose trusted exact model/reasoning metadata; no executor configuration claim is made.',
        'source_inspection_inherited': False, 'checks_inherited': False,
        'human_semantic_acceptance': False, 'gameplay_readiness': False})
    # Preserve every criterion and test verbatim. Only the fresh execution operands
    # are mapped, because old test basetemp paths would write the frozen attempt.
    task['tests'] += [
        'Continuation execution binding: every literal inventory-17-20-01 path in the original commands above is a frozen prior-attempt operand. Execute the identical commands with only that attempt prefix replaced by continuation-17-20-dependency03. Never write a test basetemp or any artifact into the blocked attempt. All original assertions and suites remain required.',
    ]
    task['outputs'] = [p.replace(OLD, NEW) for p in task['outputs']]
    task['write_scope'] = [NEW]
    task['start_conditions'] = [s.replace('inventory-17-20-01', 'continuation-17-20-dependency03') for s in task['start_conditions']]
    task['start_conditions'] += [
        'The operator authorized recovery in this chat. Read the new continuation scope and assessment first. The blocked attempt is immutable and grants no inherited inspection, validation, delivery or acceptance.',
        'Dependency context must come only from the per-session hash-bound dependency_context.py projection. Never read coordinator dependency-inputs.json directly, even though its hash remains an internal input pin.',
    ]
    task['inputs'] += [
        'Recovery drafts are candidate-only exact JSON pins in the continuation scope. No old Python helpers, transcripts, inspection reports or check claims are authorized implementation context.',
    ]
    task['context'] = [p for p in task['context'] if p not in {
        task['inventory_batch']['input_reference']['path'],
        'private/workflow/runs/IG-2B05/coordinator-6daf4d13-01/page-navigation.json',
        'private/workflow/runs/IG-2B04/continuation-13-16-rg04/toolchain.json'}]
    task['inventory_batch']['owned_attempt'] = NEW.rstrip('/')
    task['inventory_batch']['independent_replay_outputs'] = [NEW + 'replay-1/', NEW + 'replay-2/']
    scope = write(PREP + 'scope.json', {
        'format': 'wgc-continuation-scope-1', 'mode': 'draft_revalidation',
        'task': task['id'], 'blocked_attempt': OLD,
        'blocked_evidence': blocked['evidence'], 'blocked_sha256': blocked['sha256'],
        'attempt': NEW, 'acceptance': task['acceptance'], 'tests': task['tests'],
        'drafts': drafts, 'preserve_manifest': preserve, 'assessment': assessment,
        'allowed_changes': ['Write only the fresh owned attempt; use candidate drafts only after fresh source inspection and revalidation.'],
        'required_work': [
            'Verify every source and accepted baseline/registry pin using the prepared dependency projections.',
            'Inspect all four assigned original pages and every proposed component/region; record fresh observations and uncertainty.',
            'Derive new final path-dependent PDF/PNG/text evidence and two complete independent fresh replays without old derivation scripts.',
            'Complete replay equality, region/component, continuation, coverage, source/reference, installed toolchain, validation and preservation reports.',
            'Run unchanged suites and checks using the fresh attempt path mapping, then freeze delivery for fresh independent review.'],
        'prohibited_reads': ['Old transcripts, derivation helpers, dependency-inputs.json content and old inspection/check conclusions.'],
        'execution_path_mapping': {'from': OLD, 'to': NEW, 'purpose': 'Fresh output/test paths only; no test assertions or suites change.'},
        'human_semantic_acceptance': False, 'gameplay_readiness': False})
    auth = write(PREP + 'authorization.json', {
        'role': 'coordinator', 'actor': 'coordinator:operator-resume-20261016-dependency03',
        'summary': 'Operator requested resuming work; authorize a fresh bounded draft-revalidation attempt after assessment of the dependency-access incident.',
        'operator_requested_recovery': True, 'operator_request_verbatim': 'wznow prace',
        'authorization_source': 'Current human message in the coordinating chat.',
        'criteria': task['acceptance'], 'artifacts': [scope, assessment, preserve, incident],
        'model': None, 'reasoning': None,
        'configuration_evidence': 'Exact model/reasoning is not exposed for this coordinator; observed gpt-6.1-sol/high is required separately for the next executor and reviewer.',
        'no_acceptance_granted': True})
    task['continuation_authorization'] = {'scope': scope, 'evidence': auth, 'attempt': NEW,
        'blocked_evidence': blocked['evidence'], 'blocked_sha256': blocked['sha256']}
    task['context_recovery_authorization'] = {'incident': incident, 'scope': scope, 'assessment': assessment}
    index = 'docs/work/repair-context/IG-2B05-dependency-continuation03.md'
    index_path = ROOT / index
    with index_path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write('# IG-2B05 dependency-access recovery\n\n'
            'The operator requested resuming work in the current coordinating chat.\n'
            f'Read only the new scope `{scope["path"]}` and assessment `{assessment["path"]}` first.\n'
            f'Write only `{NEW}`. The previous attempt is frozen and unaccepted.\n'
            'Use task-bound dependency projections only; never directly read the old dependency-inputs.json.\n'
            'Named draft JSON files are candidate inputs. No old transcripts, helper scripts, inspection or check claims are inherited.\n'
            'Reinspect the assigned original pages, regenerate path-dependent evidence and both complete replays, finish reports and fresh checks, then obtain independent review.\n'
            'Keep original acceptance criteria and suites. The scope maps old output/test operands into the fresh attempt to preserve frozen bytes.\n')
    task['context'] += [index, scope['path'], assessment['path']]
    # Never expose source drafts in packet text; the scope names their exact pins.
    policy_path = ROOT / 'docs/work/context-policy.json'
    policy_before = w.digest(policy_path)
    policy = w.read_json(policy_path)
    for rel in (scope['path'], assessment['path']):
        if rel not in policy['allow']:
            policy['allow'].append(rel)
    o.dump(policy_path, policy)
    o.continuation_preservation(ROOT, task, require_absent=True)
    dependency = d.build(ROOT, q, task)
    write(PREP + 'dependency-preflight.json', dependency)
    if task['acceptance'] != original['acceptance'] or task['tests'][:len(original['tests'])] != original['tests']:
        raise ValueError('Original criteria or tests changed')
    write(PREP + 'task-before.json', original)
    write(PREP + 'task-after.json', task)
    replan = write(PREP + 'replan.json', {
        'role': 'coordinator', 'actor': 'coordinator:operator-resume-20261016-dependency03',
        'summary': 'Resolve the context-access blocker with explicit current operator recovery authorization, pinned preservation and a fresh execution scope.',
        'criteria': task['acceptance'], 'artifacts': [auth, scope, assessment, preserve],
        'model': None, 'reasoning': None,
        'configuration_evidence': 'Coordinating session actual configuration unknown; no claim of executor Sol/high.',
        'queue_sha256_before': queue_before, 'context_policy_sha256_before': policy_before})
    if w.digest(ROOT / w.QUEUE) != queue_before:
        raise ValueError('Queue changed during preparation')
    # The workflow command owns state transitions and their append-only evidence.
    w.validate(q, ROOT, check_views=False)
    o.dump(ROOT / w.QUEUE, q)
    w.render(q, ROOT)
    print(json.dumps({'preparation': PREP, 'replan': replan['path'],
        'preserved_artifacts': len(preserved), 'draft_count': len(drafts),
        'fresh_attempt_absent': not (ROOT / NEW).exists()}))


if __name__ == '__main__':
    main()
