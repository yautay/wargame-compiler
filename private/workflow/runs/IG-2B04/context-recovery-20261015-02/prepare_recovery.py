"""Operator-authorized B04 context repair; no product readiness or acceptance."""
import copy
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o
import task_access as access

HERE = Path(__file__).resolve().parent
REL = HERE.relative_to(ROOT).as_posix()
INDEX = 'docs/work/repair-context/IG-2B04-context-access-02.md'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


assert not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
assert not (HERE / 'scope.json').exists(), 'Never replace a recovery attempt'
q = w.read_json(ROOT / w.QUEUE)
original_queue_hash = w.digest(ROOT / w.QUEUE)
t = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert t['status'] == 'planned' and not t['events']
original_task = copy.deepcopy(t)
incident = pin('private/workflow/runs/IG-2B04/coordinator-ed46c8b3-context-block/blocked.json')
previous = t['context_recovery_authorization']
preserved = [pin(previous[k]['path']) for k in ('incident', 'scope', 'assessment')]
preserved.append(pin('docs/work/repair-context/IG-2B04-bounded-dependencies.md'))
old_run = 'private/workflow/orchestrator/20261015T184406Z-2af64d3b/'
preserved.append(pin(old_run + 'status.json'))
for name in ['task.json', 'packet.json', 'references.json', 'runtime-configuration.json',
             'response.json', 'process-result.json']:
    preserved.append(pin(old_run + '001-IG-2B04-coordinator-ed46c8b3/' + name))
done = pin('private/workflow/runs/IG-2B03/closure-002-IG-2B03-reviewer-cabf2418/done.json')
assert done['sha256'] == 'ec152545a09d183c3ee0eed31adea0421cf0b567a2501be15a95c5a418a5c950'
assert w.read_json(ROOT / old_run / 'status.json')['state'] == 'blocked'
facts = w.read_json(ROOT / incident['path'])
assert facts['queue_unchanged'] and facts['queue_sha256'] == original_queue_hash
assert facts['original_pdf_pages_inspected'] == [] and facts['product_files_written'] == 0

actor = {'role': 'coordinator', 'actor': 'operator-b04-context-access-recovery-20261015',
         'task': 'IG-2B04', 'model': None, 'reasoning': None,
         'configuration_evidence': 'Builder model/reasoning are not exposed; no Sol/high claim.',
         'operator_request': 'Complete B04 documentation, prevent helper-refusal fallback, scope Git status, verify and launch a fresh coordinator.'}
assessment = dict(actor, format='wgc-context-assessment-1', observed_utc=o.utc(),
    incident=incident, preserved=preserved, dependency_done=done,
    summary='The stopped coordinator bypassed a missing-document refusal and printed broad Git metadata. No source-page inspection, product work or queue change is inherited.',
    facts={'prior_supervisor_stopped': True, 'prior_task_status': 'planned', 'prior_events': 0,
           'B03_status': 'done', 'B03_review': 'pass', 'fresh_session_required': True},
    fixes=['Exact lazy documentation/tool pins, including the sources README and evidence/schema interfaces.',
           'Guard-bound helper refusals hold the request; marker/stream notification stops the owned session, including configuration/publication failures.',
           'Fixed literal task Git paths, validated bounded output, no raw/global status or alternate read after refusal.'],
    limits=['Helpers enforce the supported serial protocol; the OS sandbox remains the permission boundary for arbitrary commands.',
            'No prior source inspection, readiness, review or semantic acceptance is inherited.',
            'Full task execution dry-run remains gated on genuine coordinator refinement and readiness.'],
    verification={'targeted_tests_before_final_type_regression': '124 passed; unchanged assertions and approved normal-user process-tree termination.',
                  'required_final_checks': 'Recorded separately in validation.json before launch.'})
o.dump(HERE / 'assessment.json', assessment)
scope = dict(actor, format='wgc-context-recovery-scope-1', mode='bounded_dependency_and_task_access',
    incident=incident, assessment=pin(REL + '/assessment.json'), preserved=preserved,
    dependency_done=done, physical_pages=[13,14,15,16],
    sections=['summary','outputs','inventory','boundary','toolchain'],
    acceptance=t['acceptance'], tests=t['tests'], tool_context=o.INVENTORY_TOOL_CONTEXT,
    allowed_changes=[
        'Refine only the planned B04 contract, exact context policy and generated views; create new task-owned preparation evidence.',
        'Read exact pinned public documentation/code through task_access read in bounded windows; retrieve dependency fields only through dependency_context.',
        'Use only fixed task_access git-status paths; never dump global Git status, recursive listings, old transcripts, queue histories or full manifests.',
        'Inspect original physical pages13-16 only when necessary. Accepted page12 exit observation is metadata only; do not follow cross-chapter references.',
        'Preserve the full44-page baseline and registry structurally without printing unassigned content; modify only assigned placeholders in a new exclusively owned attempt.',
        'Pin fresh original inspection/evidence, two independent replays, exact output layout, toolchain, criteria/tests and independent review before readiness.'],
    forbidden=['Any command, direct read or alternate helper after a helper refusal; stop and require a new packet/session.',
               'Changing accepted B03, prior incidents/attempts, frozen evidence or original acceptance/tests.',
               'Weakening checks, gameplay legality by an LLM, inherited readiness or automatic human semantic acceptance.'],
    readiness_granted=False, semantic_acceptance_granted=False)
o.dump(HERE / 'scope.json', scope)
(ROOT / INDEX).write_text(
    '# IG-2B04 context access recovery\n\n'
    'The operator authorized a fresh coordinator after missing-document fallback and broad Git metadata output.\n'
    'Use only bounded dependency sections, exact lazy public tool pins and fixed task Git paths.\n'
    'Context requests are serial. A refusal holds the helper and stops the session; no alternate read/command is permitted.\n\n'
    + '\n'.join('- ' + p['path'] + ' SHA256 ' + p['sha256'] for p in [pin(REL + '/scope.json'), pin(REL + '/assessment.json')])
    + '\n\nNo inherited inspection, readiness, review or semantic acceptance. All original criteria and tests remain binding.\n',
    encoding='utf-8')
t['context_recovery_authorization'] = {'incident': incident,
    'scope': pin(REL + '/scope.json'), 'assessment': pin(REL + '/assessment.json')}
t['tool_context'] = list(o.INVENTORY_TOOL_CONTEXT)
t['context'] = [INDEX if p == 'docs/work/repair-context/IG-2B04-bounded-dependencies.md' else p for p in t['context']]
allowed = {'context', 'context_recovery_authorization', 'tool_context'}
assert {k:v for k,v in t.items() if k not in allowed} == {k:v for k,v in original_task.items() if k not in allowed}
policy_path = ROOT / 'docs/work/context-policy.json'
policy = w.read_json(policy_path)
for rel in [REL + '/scope.json', REL + '/assessment.json', incident['path']]:
    if rel not in policy['allow']: policy['allow'].append(rel)
lock = ROOT / 'private/workflow/queue.lock'
fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
try:
    assert w.digest(ROOT / w.QUEUE) == original_queue_hash
    o.dump(policy_path, policy)
    w.validate(q, ROOT, check_views=False)
    o.dump(ROOT / w.QUEUE, q)
    w.render(q, ROOT)
    w.validate(q, ROOT)
finally:
    os.close(fd)
    lock.unlink()
for p in preserved + [done, incident]:
    assert w.digest(ROOT / p['path']) == p['sha256'], 'Preserved evidence changed'
session = HERE / 'preflight'
o.prepare(ROOT, q, t, 'coordinator', session)
manifest = session / 'access-manifest.json'
for rel in o.INVENTORY_TOOL_CONTEXT:
    result = access.read_public(ROOT, manifest.relative_to(ROOT).as_posix(), w.digest(manifest), 'IG-2B04', rel, lines=3)
    assert result['path'] == rel
status = access.git_status(ROOT, manifest.relative_to(ROOT).as_posix(), w.digest(manifest), 'IG-2B04')
env = o.launch_environment(ROOT, t, session)
o.dump(HERE / 'preflight-result.json', dict(queue_valid=True, selected_status=t['status'],
    public_documents_verified=len(o.INVENTORY_TOOL_CONTEXT),
    dependency_view_bytes=(session / 'dependency-view.json').stat().st_size,
    task_git_status_items=len(status['entries']), git_status_truncated=status['truncated'],
    guard_bound=bool(env['WGC_CONTEXT_GUARD_SHA256']),
    process_pythonpath=env.get('PYTHONPATH'), process_path_prefix=env['PATH'].split(os.pathsep)[0],
    preserved_artifacts=len(preserved) + 2, source_pages_inspected=[], models_launched=0))
print(json.dumps(w.read_json(HERE / 'preflight-result.json'), indent=2))
