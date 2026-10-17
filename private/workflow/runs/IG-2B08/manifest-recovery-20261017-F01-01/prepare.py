"""Prepare the operator-authorized bounded F01 repair; never print a manifest."""
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B08/manifest-recovery-20261017-F01-01/'
OLD = 'private/workflow/runs/IG-2B08/inventory-p33-scope02/'
NEW = 'private/workflow/runs/IG-2B08/repair-F01-manifest02/'
PRIOR = 'private/workflow/runs/IG-2B08/context-recovery-20261017-p33-01/'
INCIDENT = 'private/workflow/runs/IG-2B08/coordinator-context-incident-b6a7690c/incident.json'
ACTOR = 'coordinator:operator-manifest-F01-recovery-20261017-01'
CONFIG = 'Current coordinating model/reasoning metadata unavailable; this is not an executor claim. New execution/review requires observed gpt-6.1-sol/high startup metadata.'
REQUEST = 'Oceń incydent z odczytem manifestu, popraw zakres kontekstu, przygotuj naprawę F01 i wznów orkiestrator od IG-2B08 w świeżej sesji.'


def write(name, value):
    target = ROOT / PREP / name
    if target.exists():
        prior = w.read_json(target)
        # A preparation interrupted before queue publication may continue only
        # with the identical contract. Keep the first recorded timestamp/bytes.
        comparable = lambda v: {k: x for k, x in v.items() if k != 'utc'}
        if comparable(prior) != comparable(value):
            raise ValueError('Prepared evidence differs; preserve and use a new preparation: ' + name)
        return
    with target.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def record(summary, **extra):
    return dict(role='coordinator', actor=ACTOR, model=None, reasoning=None,
                configuration_evidence=CONFIG, utc=o.utc(), summary=summary, **extra)


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    original_q = copy.deepcopy(q)
    initial_hash = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B08')
    assert task['status'] == 'changes_requested'
    assert not (ROOT / NEW).exists()
    assert not (ROOT / 'private/workflow/ig2-orchestrator.lock').exists()
    write('task-before.json', task)
    incident = w.read_json(ROOT / INCIDENT)
    assert incident['preservation']['queue_mutated'] is False
    review_event = task['events'][-1]
    assert review_event['to'] == 'changes_requested'
    assert pin(review_event['evidence'])['sha256'] == review_event['sha256']
    review = w.read_json(ROOT / review_event['evidence'])
    assert [f['id'] for f in review['findings']] == ['F01']
    event = next(e for e in reversed(task['events']) if e['to'] == 'review')
    assert pin(event['evidence'])['sha256'] == event['sha256']
    delivery = w.read_json(ROOT / event['evidence'])
    assert delivery['artifacts'] == review['artifacts']
    artifacts = {a['path']: a for a in delivery['artifacts']}
    prior_preserved = w.read_json(ROOT / PRIOR / 'preserve-manifest.json')
    protected = list(delivery['artifacts']) + list(review['review_artifacts']) + list(prior_preserved['artifacts'])
    protected += [pin(event['evidence']), pin(review_event['evidence']), pin(INCIDENT)]
    protected += [task['context_recovery_authorization'][k] for k in ('incident', 'scope', 'assessment')]
    protected += [pin(PRIOR + 'preserve-manifest.json'), pin(PRIOR + 'input-pins.json')]
    unique = {}
    for p in protected:
        if p['path'] in unique:
            assert unique[p['path']]['sha256'] == p['sha256']
        unique[p['path']] = p
    preserved = {'format': 'wgc-frozen-repair-inputs-1', 'artifacts': list(unique.values()),
                 'policy': 'Internal hash verification only; emit counts/status, never manifest rows or source content.'}
    o.verify_artifacts(ROOT, preserved)
    write('preserve-manifest.json', preserved)
    write('process-triage.json', record('Approved OS inspection found no old supervisor PID 5560 or coordinator PID 17068; no supervisor lock exists.',
          process_ids=[5560, 17068], observed_matching_processes=0,
          inspection='Get-CimInstance Win32_Process -Filter ProcessId=5560 OR ProcessId=17068',
          original_status=pin('private/workflow/orchestrator/20261017T071640Z-9e122b0d/status.json')))
    assessment = record('The coordinator printed the exhaustive current review manifest instead of selected fields. The session correctly stopped; prepare a fresh bounded F01 repair.',
          format='wgc-manifest-context-assessment-1', task=task['id'], operator_request=REQUEST,
          incident=pin(INCIDENT), review=pin(review_event['evidence']),
          cause='Exact file location was mistaken for permission to release all JSON fields; the 7719-entry artifact list was irrelevant to repair reasoning.',
          impact={'excess_manifest_metadata_in_context': True, 'extra_source_render_or_extraction': False,
                  'frozen_product_mutation': False, 'queue_mutation_by_incident_session': False,
                  'repair_authorization_by_incident_session': False},
          disposition='Retain all evidence; reject the stopped session as a repair authorization. Current independent F01 remains valid; no acceptance is inferred.',
          correction='Supply a compact explicit projection of current findings and named input pins. Full review/delivery/preservation manifests are internal hash/copy inputs only, never console/model output.',
          model_session_policy='Fresh ephemeral executor, then independent reviewer; do not resume/copy coordinator transcript.',
          semantic_acceptance=False, executable_readiness=False)
    write('assessment.json', assessment)

    helpers = ['author_specs.py', 'build_inventory.py', 'verify_batch.py', 'inspect_originals.py',
               'freeze_delivery.py', 'validate_delivery.py']
    reports = ['author-selections.json', 'component-ledger.json', 'region-ledger.json',
               'original-page-inspection.json', 'continuations.json', 'coverage-report.json',
               'source-pins.json', 'toolchain.json', 'preservation-report.json', 'replay-report.json',
               'validation-report.json', 'delivery-handoff.md',
               'final-verified/inventory.json', 'final-verified/identity-registry.json']
    selected_pins = {name: artifacts[OLD + name] for name in helpers + reports}
    context = {'format': 'wgc-current-repair-context-1', 'task': task['id'],
          'review_reference': pin(review_event['evidence']), 'delivery_reference': pin(event['evidence']),
          'review': {k: review[k] for k in ('outcome', 'summary', 'findings')},
          'frozen_delivery': {'summary': delivery['summary'], 'artifact_count': len(delivery['artifacts']),
                              'status': 'changes_requested; reusable candidate inputs, not accepted output'},
          'named_inputs': selected_pins,
          'read_protocol': ['This small projection is authorized for full reading; never print the source review/delivery envelopes.',
              'Read named helper source at these exact paths in bounded line windows (at most 120 lines per command); do not execute any helper at its frozen path.',
              'Copy only these named helpers to the new owned root, then adapt output/runtime/packet/claim bindings before execution. Never inherit old actor, configuration, completion or validation claims.',
              'Select authored JSON by assigned pages 29-32 or F01 component keys/IDs; inspect report metadata/selected fields only. Full copying/hashing/validation may run internally without emitting source text or manifest rows.',
              'source-pins.json and preservation manifests are internal verification/index inputs; print only aggregate counts and statuses. No recursive private listings or private search.',
              'Review F01 evidence paths named inside the finding are authorized diagnostics. Their content is input evidence, not fresh source inspection or acceptance.',
              'Old failed inventory-8d84cd90-01 helpers, text, images and transcripts remain forbidden. The later frozen inventory-p33-scope02 named candidate inputs are explicitly permitted by this CURRENT repair contract.'],
          'allowed_source_access': task['inventory_contract']['source_access']}
    write('repair-context.json', context)
    inputs = w.read_json(ROOT / PRIOR / 'input-pins.json')
    inputs['prior_effective_contract'] = pin(PRIOR + 'input-pins.json')
    inputs.update(actor=ACTOR, model=None, reasoning=None, configuration_evidence=CONFIG,
                  summary='F01 repair operational contract; accepted baseline/source/report pins unchanged.',
                  executor_attempt_root=NEW.rstrip('/'),
                  product_outputs=[p.replace(OLD, NEW) for p in inputs['product_outputs']])
    inputs['source_access']['forbidden'] = ('No transcripts, old failed-attempt helpers, archives/history, whole-PDF analysis, private search, '
          'manifest/envelope dumps or other dependency records. Only the named frozen B08 candidate helpers in repair-context.json may be read/copied; never execute them at frozen paths.')
    write('input-pins.json', inputs)

    recovery_scope = record('Fresh F01 repair context after the manifest incident; exact private field and source limits.',
          format='wgc-manifest-context-recovery-1', task=task['id'], mode='bounded_review_repair',
          incident=pin(INCIDENT), assessment=pin(PREP + 'assessment.json'),
          repair_context=pin(PREP + 'repair-context.json'), effective_input_contract=pin(PREP + 'input-pins.json'),
          preserve_manifest=pin(PREP + 'preserve-manifest.json'), prior_source_recovery=task['context_recovery_authorization'],
          fresh_attempt=NEW, assigned_physical_pages=[29, 30, 31, 32],
          source_access=inputs['source_access'],
          context_protocol='FIRST read assessment.json and repair-context.json. Use this selected projection for findings/delivery metadata. Never print a full review, delivery, source-pin or preservation manifest, even at an exact path. Internal verification emits only counts/status.',
          reuse_policy='Only named inventory-p33-scope02 helpers and candidate records may be copied/adapted in the fresh repair root; no inherited inspection, checks, identity or acceptance. All frozen inputs remain byte-identical. Prior source scope remains unchanged; its initial no-draft-reuse policy applies to inventory-8d84cd90-01, not the explicitly named later frozen delivery.',
          preservation_checks='Verify every preserve-manifest artifact internally before product writes and before delivery; independent review verifies again. Print counts/status only.',
          stop_policy='Any helper refusal, extra source scope requirement, stale pin or competing writer stops the session. No fallback or automatic page-33 crop expansion.',
          semantic_acceptance=False, executable_readiness=False)
    write('scope.json', recovery_scope)

    task['outputs'] = [p.replace(OLD, NEW) for p in task['outputs']]
    task['write_scope'] = [NEW]
    task['inventory_contract'].update(attempt_root=NEW.rstrip('/'), input_pins=pin(PREP + 'input-pins.json'),
                                      source_access=inputs['source_access'])
    task['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md',
                       'src/wgc/sources/README.md', 'docs/work/EVIDENCE.md',
                       PREP + 'input-pins.json', PREP + 'scope.json', PREP + 'assessment.json', PREP + 'repair-context.json']
    task['inputs'] = [p.replace(PRIOR + 'input-pins.json', PREP + 'input-pins.json') for p in task['inputs']]
    task['inputs'].append('Current F01 findings and named frozen candidate input pins: ' + PREP + 'repair-context.json. No full manifest dump is authorized.')
    task['start_conditions'] = task['start_conditions'][:2] + [
          'FIRST read the CURRENT context recovery scope/assessment and compact repair-context.json, then session repair-scope.json. Current F01 repair supersedes initial fresh-rebuild ownership and helper-reuse instructions only as explicitly stated.',
          'Claim fresh absent ' + NEW + ' with a new actor, confirmed observed gpt-6.1-sol/high runtime, packet hash and checkpoint. The frozen original delivery and both incidents remain immutable.',
          'Use only task-bound access/search/dependency helpers, exact named frozen repair inputs and assigned source scope. Read helper source in bounded windows; copy/adapt to the new root before execution.',
          'Verify every preserved input hash before product writes and delivery; no previous inspection, tests, acceptance or semantic claims are inherited.',
          'Source access: pages 29-32; page 28 reference-only; page 33 only [45,50,306,80] PDF points, normalized [73529,63131,500000,101011]. Clip before output; no expansion.',
          'Only the supervisor launches subsequent roles. No product code/schema changes, online services, global configuration, nested agents, unrelated tasks or IG-3 work.']
    task['tests'] += [
          'CURRENT F01 repair command mapping: for all original/appended test and output command operands, map inventory-8d84cd90-01/ and inventory-p33-scope02/ under this task to repair-F01-manifest02/. Preserve every suite/assertion; never write test artifacts into either frozen attempt.',
          'F01: independently inspect the complete page-30 Advance arrows; corrected detail component evidence in final and both complete serial replays must include PDF point [94,367], both complete cyan curves/heads and the black forward arrow. Do not satisfy this using a primary tile or neighboring counter crop.',
          'Add a source-bound component-completeness regression check which rejects the original [104,345,141,476] crop and proves full visible arrow coverage; key-set equality or checking only a single point is insufficient.',
          'Recheck all assigned components and exact page-33 context; verify unchanged disjoint primary tiles, accepted 44-page baseline, registry history and zero context denominator. Regenerate affected final/replay evidence, ledgers, current indexes and all changed reports, then obtain fresh independent review.',
          'Hash-verify every artifact in the CURRENT pinned preserve-manifest internally before writes and delivery, emitting only counts/status. The independent reviewer rechecks all preserved inputs.']
    task['context_recovery_authorization'] = {'incident': pin(INCIDENT), 'scope': pin(PREP + 'scope.json'),
                                               'assessment': pin(PREP + 'assessment.json')}
    scope = {'format': 'wgc-bounded-repair-scope-1', 'task': task['id'],
          'review_evidence': review_event['evidence'], 'review_sha256': review_event['sha256'],
          'finding_ids': ['F01'], 'attempt': NEW, 'acceptance': task['acceptance'], 'tests': task['tests'],
          'immutable_delivery': {'path': event['evidence'], 'sha256': event['sha256']},
          'mode': 'component_evidence_repair', 'repair_context': pin(PREP + 'repair-context.json'),
          'recovery_scope': pin(PREP + 'scope.json'), 'preserve_manifest': pin(PREP + 'preserve-manifest.json'),
          'allowed_changes': ['Correct or split only the page-30 Advance zero-denominator arrow detail selection to account for its entire visible components, after fresh original inspection.',
              'Adapt named candidate helpers into the fresh root; add a source-bound completeness check rejecting the original crop. Keep source suites/assertions unchanged.',
              'Regenerate affected component geometry/revisions/evidence and reports at fresh paths, plus both COMPLETE serial independent replays, exhaustive indexes and fresh operational checks.',
              'Preserve the disjoint primary field tiles, all unrelated authored selections, accepted baseline objects/nonassigned records, retained reading order and complete registry history; document necessary path normalization. No game semantics or new page scope.'],
          'required_checks': review['findings'][0]['repair_validation'],
          'source_access': inputs['source_access'], 'semantic_acceptance': False, 'executable_readiness': False}
    write('repair-scope.json', scope)
    auth = record('Operator-authorized bounded F01 repair and fresh sequential supervisor restart after manifest-context assessment.',
          task=task['id'], operator_request=REQUEST, criteria=task['acceptance'],
          artifacts=[pin(PREP + p) for p in ['repair-scope.json', 'scope.json', 'assessment.json', 'repair-context.json', 'input-pins.json', 'preserve-manifest.json']] + [pin(review_event['evidence']), pin(event['evidence']), pin(INCIDENT)],
          checks=[{'command': 'Internally verify current frozen delivery/review and prior failed-attempt artifacts; compare exact independent finding and no live prior process', 'exit_code': 0}],
          requested_next_operation='Fresh executor for F01, then fresh independent reviewer, then normal queue-selected sequential IG-2 work.',
          task_status_unchanged=True, semantic_acceptance=False)
    write('authorization.json', auth)
    task['repair_authorization'] = {'review_evidence': review_event['evidence'], 'review_sha256': review_event['sha256'],
          'scope': pin(PREP + 'repair-scope.json'), 'evidence': pin(PREP + 'authorization.json'), 'attempt': NEW}
    assert task['acceptance'] == next(t for t in original_q['tasks'] if t['id'] == task['id'])['acceptance']
    # A routine model coordinator cannot replace operator context authorization.
    # Here the current explicit operator request authorizes precisely that change;
    # validate every other role restriction against the newly authorized pins.
    guard_before = copy.deepcopy(original_q)
    before_task = next(t for t in guard_before['tasks'] if t['id'] == task['id'])
    before_task['context_recovery_authorization'] = task['context_recovery_authorization']
    o.check_queue_delta(guard_before, q, before_task, 'coordinator')
    o.verify_repair_authorization(ROOT, task)
    assert w.digest(ROOT / w.QUEUE) == initial_hash
    policy_path = ROOT / 'docs/work/context-policy.json'
    policy = w.read_json(policy_path)
    for rel in task['context'] + [PREP + 'repair-scope.json', PREP + 'authorization.json']:
        if rel not in policy['allow']: policy['allow'].append(rel)
    policy_path.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / w.QUEUE).write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for rel, body in w.views(q).items(): (ROOT / rel).write_text(body, encoding='utf-8')
    w.validate(q, ROOT)
    packet = w.packet(q, ROOT, task['id'], output=False)
    write('task-after.json', task)
    result = {'task': task['id'], 'status': task['status'], 'next_role': o.select(q)[1],
              'fresh_attempt': NEW, 'preserved_artifacts': len(preserved['artifacts']),
              'packet_text_bytes': packet['text_bytes'], 'queue_sha256': w.digest(ROOT / w.QUEUE)}
    write('preparation-result.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
