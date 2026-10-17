"""Assess the output incident and authorize a fresh bounded review, without acceptance."""
import copy
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B08/validation-context-recovery-20261017-01/'
PRIOR = 'private/workflow/runs/IG-2B08/manifest-recovery-20261017-F01-01/'
STOPPED = 'private/workflow/runs/IG-2B08/review-4705d02f/'
INCIDENT = STOPPED + 'context-incident.json'
ACTOR = 'coordinator:operator-validation-context-recovery-20261017-01'
CONFIG = 'Current coordinating model/reasoning metadata unavailable. This is not an executor/reviewer claim; a fresh observed gpt-6.1-sol/high session is required.'
REQUEST = 'Oceń incydent z metadanymi stron spoza kontekstu, popraw zakres odczytu walidacji i wznów recenzję naprawy F01 oraz IG-2B08 w świeżej sesji.'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def write(name, body):
    with (ROOT / PREP / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(body, f, ensure_ascii=False, indent=2)
        f.write('\n')


def evidence(summary, **extra):
    return dict(role='coordinator', actor=ACTOR, model=None, reasoning=None,
                configuration_evidence=CONFIG, utc=o.utc(), summary=summary, **extra)


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    before = copy.deepcopy(q)
    queue_sha = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B08')
    assert task['status'] == 'review'
    assert not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
    write('task-before.json', task)
    incident = w.read_json(ROOT / INCIDENT)
    event = task['events'][-1]
    assert event['to'] == 'review' and pin(event['evidence'])['sha256'] == event['sha256']
    assert incident['review_state']['delivery_sha256'] == event['sha256']
    assert not incident['incident']['frozen_product_mutation']
    assert not incident['incident']['queue_mutation']
    delivery = w.read_json(ROOT / event['evidence'])
    current = task['inventory_contract']['attempt_root'] + '/'
    rows = {a['path']: a for a in delivery['artifacts']}
    prior = w.read_json(ROOT / PRIOR / 'preserve-manifest.json')
    protected = prior['artifacts'] + delivery['artifacts'] + [pin(event['evidence'])]
    protected += [task['context_recovery_authorization'][k] for k in ('incident', 'scope', 'assessment')]
    protected += [task['repair_authorization'][k] for k in ('scope', 'evidence')]
    protected += [pin(PRIOR + 'preserve-manifest.json')]
    # Snapshot only this explicitly assessed review attempt; no transcript or
    # source content is released. Mutable pytest scratch is retained, not read.
    stopped_count = 0
    for base, dirs, files in os.walk(ROOT / STOPPED):
        dirs[:] = [d for d in dirs if d not in {'source-pytest', 'pytest', '__pycache__', 'temp'}]
        for name in sorted(files):
            rel = (Path(base) / name).relative_to(ROOT).as_posix()
            protected.append(pin(rel)); stopped_count += 1
    unique = {}
    for p in protected:
        if p['path'] in unique: assert unique[p['path']]['sha256'] == p['sha256']
        unique[p['path']] = p
    preservation = {'format': 'wgc-review-recovery-preservation-1', 'artifacts': list(unique.values()),
                    'policy': 'Internal byte verification; counts/status only. No manifest output. Pytest scratch retained unchanged and excluded from the frozen-input set.'}
    o.verify_artifacts(ROOT, preservation)
    write('preserve-manifest.json', preservation)
    write('process-triage.json', evidence('Approved process inspection found no supervisor/reviewer or stopped-review validation workers; no lock exists.',
          old_pids=[17236, 2648], observed_matching_processes=0,
          stopped_validation_process_query='python.exe/codex.exe command line containing review-4705d02f',
          stopped_attempt_files_pinned=stopped_count))
    write('assessment.json', evidence('The full validator ran within its structural remit, but the review wrapper released an unscoped stdout tail. Fresh review is required.',
          format='wgc-validation-context-assessment-1', task=task['id'], operator_request=REQUEST,
          incident=pin(INCIDENT), immutable_delivery=pin(event['evidence']),
          cause='The wrapper printed its last 3000 output characters, including coverage rows for unassigned physical pages. File-local validation authority did not authorize releasing all of its report fields.',
          impact={'unassigned_coverage_metadata_released': True, 'source_text_released': False,
                  'extra_source_render_or_extraction': False, 'product_mutated': False,
                  'queue_mutated': False, 'completed_independent_review': False},
          resolution='Use the pinned task_access validate-source operation. Preserve full stdout/stderr privately for both success and failure; release only command, exit code and log pins. No raw tails or global coverage rows.',
          retained_validation_scope='Full 44-page structural validation, preservation and source hash checks remain required internally. No test, acceptance criterion or source inspection is reduced.',
          incomplete_review_policy='No claim/check/source inspection from the stopped review is a fresh review result. Candidate F02 is a lead for fresh assigned-page verification, not a confirmed finding.',
          actual_model=None, actual_reasoning=None, semantic_acceptance=False, executable_readiness=False))
    names = ['region-ledger.json', 'component-ledger.json', 'original-page-inspection.json',
             'continuations.json', 'coverage-report.json', 'source-pins.json', 'toolchain.json',
             'preservation-report.json', 'replay-report.json', 'validation-report.json', 'delivery-handoff.md',
             'check_arrow_completeness.py', 'verify_batch.py',
             'final-verified/inventory.json', 'final-verified/identity-registry.json',
             'replay-1/inventory.json', 'replay-2/inventory.json']
    old_findings = w.read_json(ROOT / task['repair_authorization']['review_evidence'])['findings']
    review_context = {'format': 'wgc-current-review-context-1', 'task': task['id'],
          'delivery_reference': pin(event['evidence']), 'delivery_summary': delivery['summary'],
          'delivery_actor': delivery['actor'], 'delivery_artifact_count': len(delivery['artifacts']),
          'F01': old_findings, 'candidate_for_fresh_verification': incident['candidate_finding_for_fresh_review'],
          'candidate_diagnostic': pin(incident['candidate_finding_for_fresh_review']['diagnostic']),
          'named_current_inputs': {name: rows[current + name] for name in names},
          'private_read_policy': 'This compact projection may be read in full. Frozen manifests/indexes are internal verification inputs only; emit counts/hashes, never full artifact lists, unassigned-page records or source text. Read assigned page/region/component fields and explicitly boundary-linked IDs only.',
          'helper_policy': 'The two named product verifiers may be inspected in bounded code windows as untrusted candidate checks, never as independent source proof. Do not execute any frozen helper that could write its old directory; create independent reviewer checks/logs in a fresh owned review root. No stopped-review wrapper/helper/transcript reuse.'}
    write('review-context.json', review_context)
    write('scope.json', evidence('Fresh independent review of the exact F01 delivery with bounded validation output.',
          format='wgc-review-output-recovery-1', task=task['id'], mode='fresh_independent_review',
          incident=pin(INCIDENT), assessment=pin(PREP + 'assessment.json'),
          review_context=pin(PREP + 'review-context.json'), immutable_delivery=pin(event['evidence']),
          preserve_manifest=pin(PREP + 'preserve-manifest.json'), prior_context_authorization=task['context_recovery_authorization'],
          source_access=task['inventory_contract']['source_access'],
          validation_protocol='For final-verified/replay-1/replay-2 CLI validation, use only scripts/task_access.py validate-source --file <exact current inventory>. The inherited access manifest pins allowed paths and hashes. The unchanged validator still checks the complete source internally. Console output is command/exit and log pins only; no stdout/stderr/tail preview on success or failure. Other required checks also log privately and return scoped summaries.',
          diagnostic_policy='Full validator logs may be hashed/copied internally. Do not release their contents into context. Additional error diagnosis needs explicit assigned-page/field selection or a new coordinator scope; failure never authorizes a raw log tail.',
          review_policy='New absent reviewer-owned directory, new observed runtime and distinct actor. Reinspect all assigned originals/boundaries/components and the exact page-33 crop, independently verify F01 and candidate F02, both complete replays, current evidence indexes, all criteria and unchanged tests. No previous green checks or inspection claims are inherited.',
          preservation_policy='Internally verify every preserved artifact before review and before final response, printing counts/status only. Verify the exact exhaustive current delivery; preserve its ordered artifact list in the new review. Frozen source/product/evidence, stopped reviews, tests and both prior attempts remain unchanged.',
          source_limits='Physical pages 29-32 only; page 28 reference-only; page 33 only PDF points [45,50,306,80] / normalized [73529,63131,500000,101011], clip before text/pixel output. No automatic crop expansion or gameplay/source-meaning approval.',
          followup_policy='After a valid independent outcome, the supervisor follows normal queue gates, including a fresh coordinator for any current finding; this scope grants no repair or acceptance in advance.',
          semantic_acceptance=False, executable_readiness=False))
    task['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md',
          'src/wgc/sources/README.md', 'docs/work/EVIDENCE.md',
          PRIOR + 'input-pins.json', PREP + 'scope.json', PREP + 'assessment.json', PREP + 'review-context.json']
    task['context_recovery_authorization'] = {'incident': pin(INCIDENT), 'scope': pin(PREP + 'scope.json'),
                                             'assessment': pin(PREP + 'assessment.json')}
    task['start_conditions'] = task['start_conditions'][:2] + [
          'CURRENT state is review: do not claim execution, recreate the F01 repair root or alter frozen product files. The prior execution start conditions have been fulfilled and are preserved in the old task packet.',
          'FIRST read the current context recovery scope/assessment and compact review-context.json. Start a fresh independent reviewer with confirmed observed gpt-6.1-sol/high runtime and a new actor/root.',
          'Use only task-bound context helpers. Run the exact full source validator through task_access.py validate-source for each of the three pinned current inventories. Keep every check stdout/stderr in new private logs; no raw output/tail or unassigned-page coverage metadata is released.',
          'Internally verify the complete frozen delivery and preserved inputs before review and final response; no prior check, source inspection or approval is inherited. Candidate F02 requires fresh verification on assigned page 29.',
          'Original source scope remains pages 29-32, reference-only page 28, and exact page-33 continuation crop. Context/helper refusal or extra source requirement stops the session.',
          'Only the supervisor launches subsequent roles. No source/product/schema edits, online services, global configuration, nested agents, unrelated tasks or downstream IG-3 work in this review.']
    write('authorization.json', evidence('Operator authorizes the assessed fresh reviewer restart; no review result or semantic acceptance is granted.',
          task=task['id'], operator_request=REQUEST, criteria=task['acceptance'],
          artifacts=[pin(PREP + name) for name in ['assessment.json', 'scope.json', 'review-context.json', 'preserve-manifest.json', 'process-triage.json']] + [pin(INCIDENT), pin(event['evidence'])],
          checks=[{'command': 'Internal frozen-input hash verification and approved process/ownership inspection', 'exit_code': 0}],
          semantic_acceptance=False, task_status_unchanged=True))
    old = next(t for t in before['tasks'] if t['id'] == task['id'])
    assert task['status'] == old['status'] and task['events'] == old['events']
    for key in ['acceptance', 'tests', 'outputs', 'write_scope', 'inventory_contract', 'repair_authorization']:
        assert task[key] == old[key]
    assert [t for t in before['tasks'] if t['id'] != task['id']] == [t for t in q['tasks'] if t['id'] != task['id']]
    assert w.digest(ROOT / w.QUEUE) == queue_sha
    policy_file = ROOT / 'docs/work/context-policy.json'; policy = w.read_json(policy_file)
    for rel in task['context'] + [PREP + 'authorization.json']:
        if rel not in policy['allow']: policy['allow'].append(rel)
    policy_file.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / w.QUEUE).write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for rel, body in w.views(q).items(): (ROOT / rel).write_text(body, encoding='utf-8')
    w.validate(q, ROOT)
    packet = w.packet(q, ROOT, task['id'], output=False)
    write('task-after.json', task)
    result = {'task': task['id'], 'status': task['status'], 'next_role': o.select(q)[1],
              'preserved_artifact_count': len(preservation['artifacts']), 'stopped_review_files': stopped_count,
              'packet_text_bytes': packet['text_bytes'], 'queue_sha256': w.digest(ROOT / w.QUEUE)}
    write('preparation-result.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
