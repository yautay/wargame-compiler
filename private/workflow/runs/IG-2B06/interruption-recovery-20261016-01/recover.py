"""Triage interrupted B06, preserve its bytes, and authorize a fresh serial attempt."""
import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B06/interruption-recovery-20261016-01/'
OLD = 'private/workflow/runs/IG-2B06/inventory-21-24-01/'
NEW = 'private/workflow/runs/IG-2B06/continuation-21-24-serial02/'
ACTOR = 'coordinator:operator-interruption-recovery-20261016-01'
CONFIG = 'Exact model/reasoning metadata unavailable for this coordinating session; no executor configuration claim is made. Fresh observed Sol/high remains mandatory.'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def write(rel, body):
    p = w.safe_path(ROOT, rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(body, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return pin(rel)


def evidence(summary, artifacts, criteria):
    return {'role': 'coordinator', 'actor': ACTOR, 'model': None, 'reasoning': None,
            'configuration_evidence': CONFIG, 'summary': summary,
            'criteria': criteria, 'artifacts': artifacts}


def transition(state, rel):
    subprocess.run([sys.executable, 'scripts/workflow.py', 'transition', '--task', 'IG-2B06',
                    '--to', state, '--evidence', rel], cwd=ROOT, check=True)


def remap(value):
    if isinstance(value, str):
        return value.replace(OLD.rstrip('/'), NEW.rstrip('/'))
    if isinstance(value, list):
        return [remap(v) for v in value]
    if isinstance(value, dict):
        return {k: remap(v) for k, v in value.items()}
    return value


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B06')
    if task['status'] != 'in_progress' or task['events'][-1]['evidence'] != OLD + 'claim.json':
        raise ValueError('Original ownership changed; fresh triage required')
    if (ROOT / NEW).exists():
        raise ValueError('Fresh attempt must be absent')
    process_pin = pin(PREP + 'process-triage.json')
    triage = w.read_json(ROOT / process_pin['path'])
    if triage['matching_processes'] or triage['lock_pid'] != 2084:
        raise ValueError('Old process ownership unresolved')
    observed = datetime.fromisoformat(triage['observed_utc'].replace('Z', '+00:00'))
    if (datetime.now(timezone.utc) - observed).total_seconds() > 600:
        raise ValueError('Refresh process liveness before recovery')
    lock = ROOT / 'private/workflow/ig2-orchestrator.lock'
    lock_bytes = lock.read_bytes()
    if w.read_json(lock)['pid'] != 2084 or (ROOT / 'private/workflow/queue.lock').exists():
        raise ValueError('Lock ownership changed')
    with (ROOT / (PREP + 'abandoned-lock.json')).open('xb') as f:
        f.write(lock_bytes)
    original = copy.deepcopy(task)
    write(PREP + 'task-before.json', original)
    checkpoint = w.read_json(ROOT / (OLD + 'checkpoint-authored.json'))
    geometry = w.read_json(ROOT / (OLD + 'geometry-refinement.json'))
    o.verify_artifacts(ROOT, checkpoint)
    o.verify_artifacts(ROOT, {'artifacts': geometry['output_pins']})
    # Hash only the explicitly selected interrupted attempt. Disposable pytest
    # trees/cache contents remain untouched and are not promoted to evidence.
    files = []
    excluded = {'__pycache__', '.pytest_cache', 'pytest-sources-01'}
    for folder, dirs, names in os.walk(ROOT / OLD):
        dirs[:] = sorted(n for n in dirs if n not in excluded)
        for name in sorted(names):
            p = Path(folder) / name
            if p.is_symlink() or p.is_junction():
                raise ValueError('Linked candidate file; scope triage required')
            files.append(pin(p.relative_to(ROOT).as_posix()))
    files.sort(key=lambda p: p['path'])
    snapshot = write(OLD + 'blocked-state-manifest.json', {
        'format': 'wgc-blocked-state-manifest-1', 'artifacts': files,
        'candidate_only': True, 'excluded_disposable_directory_names': sorted(excluded)})
    diagnostic = write(PREP + 'diagnosis.json', {
        'operator_request': 'Investigate the stopped orchestrator, fix the problem and resume IG-2B06.',
        'confirmed': [
            'The recorded supervisor/CLI and exact attempt-owned process scope have no live OS process.',
            'Last heartbeat was 2026-10-16T17:08:01Z; no final process/result or supervisor exception was recorded.',
            'Corrected replay failed creating a multiprocessing named pipe with WinError 5 under the restricted token.',
            'A synthetic regression reproduced different Windows venv-launcher and actual-supervisor PIDs. Direct base-interpreter launch now passes the same PID test.'],
        'not_established': 'The external cause terminating both old supervisor and CLI is unknown. No matching System/Application crash, sleep or restart event was returned in the bounded 19:05-19:11 local inspection. Do not claim the pipe failure caused supervisor termination.',
        'changes': [
            'Serial source evidence generation in child instructions; two complete independent replays remain required.',
            'Launch the installed base interpreter directly on Windows so launch PID equals actual supervisor PID.',
            'Record a blocked status and preserve traceback for unexpected Python exceptions.'],
        'checkpoint_reconciliation': 'All authored-checkpoint pins and all later corrected-geometry output pins match disk. Later corrected geometry is a candidate only; no inspection/check or acceptance claims are inherited.',
        'artifacts': [snapshot, process_pin], 'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': CONFIG})
    blocked_body = evidence('Interrupted executor has no live owner; preserve its unaccepted candidates and require fresh serial recovery.',
                            [snapshot, diagnostic, process_pin], task['acceptance'])
    blocked_body.update(owner='coordinator/operator', delivery_or_acceptance=False,
        next_operation='Fresh absent attempt, original-page reinspection, sequential evidence and two complete independent replays, reports/checks and independent review.')
    blocked = write(OLD + 'blocked.json', blocked_body)
    transition('blocked', blocked['path'])
    q = w.read_json(ROOT / w.QUEUE)
    before_hash = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B06')
    old_contract_pin = copy.deepcopy(task['refinement_contract'])
    if w.digest(ROOT / old_contract_pin['path']) != old_contract_pin['sha256']:
        raise ValueError('Original refinement contract changed')
    old_contract = w.read_json(ROOT / old_contract_pin['path'])
    for item in old_contract['input_pins']:
        if w.digest(w.safe_path(ROOT, item['path'])) != item['sha256']:
            raise ValueError('Pinned task input changed: ' + item['path'])
    contract = remap(old_contract)
    contract.update(role='coordinator', actor=ACTOR, model=None, reasoning=None,
                    configuration_evidence=CONFIG, configuration_sha256=None,
                    origin_contract=old_contract_pin,
                    summary='Operational continuation of the unchanged B06 source contract, with fresh output paths and serial evidence generation after interruption.')
    contract['fresh_evidence_and_replays'] += [
        'Generate evidence serially in the current Python process. Do not use multiprocessing, ProcessPoolExecutor or worker-process pools. Run both complete independent replays separately, retaining every assigned/context region and all original equivalence checks.']
    effective = write(PREP + 'refinement-contract.json', contract)
    preserved = list(files)
    for p in [snapshot, diagnostic, process_pin, {'path': blocked['path'], 'sha256': blocked['sha256']}]:
        if p not in preserved:
            preserved.append(p)
    preserve = write(PREP + 'preserve-manifest.json', {'artifacts': preserved, 'candidate_only': True})
    assessment = write(PREP + 'assessment.json', {
        'operator_requested_recovery': True, 'operator_request_verbatim': 'sprawdz dlaczego orkiestrator sie zatrzymal, napraw problem i wznow prace od IG-2B06',
        'diagnosis': diagnostic, 'effective_refinement_contract': effective,
        'unchanged_acceptance': task['acceptance'], 'unchanged_tests': task['tests'],
        'recovery': 'Reinspect original assigned pages and exact allowed continuation boxes, revalidate corrected draft geometry/components and persisted identities, derive fresh path-dependent final evidence and both full independent replays serially. Finish all reports/checks and obtain fresh independent review.',
        'unknown_external_termination_cause': True, 'source_meaning_or_acceptance_granted': False,
        'actual_model': None, 'actual_reasoning': None, 'configuration_evidence': CONFIG})
    drafts = [pin(OLD + 'authored-corrected/' + n) for n in ('inventory.json', 'identity-registry.json', 'regions.json')]
    scope = write(PREP + 'scope.json', {
        'mode': 'draft_revalidation', 'blocked_attempt': OLD,
        'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256'],
        'attempt': NEW, 'acceptance': task['acceptance'], 'tests': task['tests'],
        'preserve_manifest': preserve, 'drafts': drafts, 'assessment': assessment,
        'effective_refinement_contract': effective,
        'required_work': contract['fresh_evidence_and_replays'],
        'no_inherited_inspection_or_checks': True,
        'old_transcripts_and_derivation_helpers_are_not_executor_context': True,
        'prior_corrected_geometry_requires_fresh_original_page_validation': True,
        'execution_mode': 'Serial evidence generation; no multiprocessing or process pools.',
        'human_semantic_acceptance': False, 'gameplay_readiness': False})
    auth = write(PREP + 'authorization.json', dict(
        evidence('Current operator explicitly authorized repair and resumption of interrupted IG-2B06 in a fresh serial attempt.',
                 [scope, assessment, preserve, effective], task['acceptance']),
        operator_requested_recovery=True, source='Current human request in the coordinating chat.'))
    task['outputs'] = remap(task['outputs'])
    task['write_scope'] = [NEW, 'private/workflow/runs/IG-2B06/review-continuation-serial02/', 'private/workflow/checks/']
    task['inputs'] = [s.replace(old_contract_pin['path'], effective['path']).replace(old_contract_pin['sha256'], effective['sha256']) for s in task['inputs']]
    task['context'] = [effective['path'] if p == old_contract_pin['path'] else p for p in task['context']]
    task['refinement_contract'] = effective
    task['continuation_authorization'] = {'scope': scope, 'evidence': auth, 'attempt': NEW,
        'blocked_evidence': blocked['path'], 'blocked_sha256': blocked['sha256']}
    task['start_conditions'] += [
        'Read the new continuation scope/assessment first. The prior interrupted attempt is frozen and unaccepted; original source inspection and checks must be fresh.',
        'Generate source evidence serially without multiprocessing or process pools; both complete independent replays and original assertions remain required.']
    task['context'] += [scope['path'], assessment['path']]
    policy = w.read_json(ROOT / 'docs/work/context-policy.json')
    for rel in (scope['path'], assessment['path'], effective['path']):
        if rel not in policy['allow']:
            policy['allow'].append(rel)
    o.dump(ROOT / 'docs/work/context-policy.json', policy)
    o.continuation_preservation(ROOT, task, require_absent=True)
    if original['acceptance'] != task['acceptance'] or original['tests'] != task['tests']:
        raise ValueError('Original gates changed')
    if w.digest(ROOT / w.QUEUE) != before_hash:
        raise ValueError('Queue changed during recovery preparation')
    w.validate(q, ROOT, check_views=False)
    o.dump(ROOT / w.QUEUE, q)
    w.render(q, ROOT)
    replan = write(PREP + 'replan.json', evidence(
        'Interruption triaged, candidate/checkpoint hashes reconciled, current operator recovery authority pinned; return to planning for fresh execution.',
        [scope, assessment, auth, preserve, effective], task['acceptance']))
    transition('planned', replan['path'])
    ready = write(PREP + 'ready.json', evidence(
        'Verified accepted dependency and source contracts, fresh absent ownership and frozen prior candidate bytes; ready for a fresh observed Sol/high executor.',
        [scope, assessment, auth, preserve, effective], task['acceptance']))
    transition('ready', ready['path'])
    # Preserve the abandoned lock exactly, then remove only that verified lock.
    if lock.read_bytes() != lock_bytes:
        raise ValueError('Supervisor lock changed during triage')
    lock.unlink()
    write(PREP + 'recovery-result.json', {'preserved_files': len(preserved), 'drafts': drafts,
        'fresh_attempt': NEW, 'old_lock_preserved': PREP + 'abandoned-lock.json',
        'queue_sha256': w.digest(ROOT / w.QUEUE), 'ready': True})
    print(json.dumps({'ready': True, 'task': task['id'], 'preserved_files': len(preserved), 'fresh_attempt': NEW}))


if __name__ == '__main__':
    main()
