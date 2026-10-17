"""Prepare only the current IG-2B07 F01 repair contract; never execute it."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
SESSION = 'private/workflow/orchestrator/20261016T195516Z-332903f5/004-IG-2B07-coordinator-2aa0a4f8'
PREP = 'private/workflow/runs/IG-2B07/repair-preparation-2aa0a4f8-01'
ATTEMPT = 'private/workflow/runs/IG-2B07/repair-F01-2aa0a4f8-01/'
ACTOR = 'ig2:004-IG-2B07-coordinator-2aa0a4f8:coordinator'
CONFIG = SESSION + '/runtime-configuration.json'
OLD_ROOT = 'private/workflow/runs/IG-2B07/inventory-25-28-01'


def read(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8-sig'))


def sha(rel):
    with (ROOT / rel).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pin(rel):
    return {'path': rel, 'sha256': sha(rel), 'bytes': (ROOT / rel).stat().st_size}


def freeze(rel, data):
    path = ROOT / rel
    assert not path.exists(), f'Immutable preparation output already exists: {rel}'
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    return pin(rel)


def verify(p):
    assert sha(p['path']) == p['sha256'], f'Pin changed: {p["path"]}'


def load_workflow():
    spec = importlib.util.spec_from_file_location('wgc_repair_workflow', ROOT / 'scripts/workflow.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    config = read(CONFIG)
    assert (config['status'], config['model'], config['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
    assert not (ROOT / ATTEMPT).exists(), 'Executor attempt must remain absent'
    refs = read(SESSION + '/references.json')
    review_pin = {'path': refs['findings']['evidence'], 'sha256': refs['findings']['sha256']}
    delivery_pin = {'path': refs['prior_delivery']['evidence'], 'sha256': refs['prior_delivery']['sha256']}
    verify(review_pin)
    verify(delivery_pin)
    review = read(review_pin['path'])
    delivery = read(delivery_pin['path'])
    assert review['outcome'] == 'changes_requested'
    assert [f['id'] for f in review['findings']] == ['F01']
    assert review['delivery']['path'] == delivery_pin['path']
    assert review['delivery']['sha256'] == delivery_pin['sha256']
    for artifact in delivery['artifacts']:
        verify(artifact)
    for evidence in review['findings'][0]['evidence']:
        verify(evidence)
    selected = read(SESSION + '/task.json')
    verify(selected['source_scope']['source_pdf'])
    verify(selected['source_scope']['source_provenance'])
    verify(selected['refinement_evidence'])

    # Queue is read only within this bounded structural edit/check process.
    queue_rel = 'docs/work/queue.json'
    before_sha = sha(queue_rel)
    assert before_sha == read(SESSION + '/packet.json')['queue_sha256'], 'Stale dispatch queue'
    q = read(queue_rel)
    before = deepcopy(q)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B07')
    assert {k: v for k, v in task.items() if k != 'events'} == selected
    current = task['events'][-1]
    assert (current['to'], current['evidence'], current['sha256']) == (
        'changes_requested', review_pin['path'], review_pin['sha256'])
    latest_delivery = next(e for e in reversed(task['events']) if e['to'] == 'review')
    assert (latest_delivery['evidence'], latest_delivery['sha256']) == (delivery_pin['path'], delivery_pin['sha256'])
    assert task['status'] == 'changes_requested'
    previous_cycles = sum(e['to'] == 'in_progress' and e['from'] == 'changes_requested' for e in task['events'])
    assert previous_cycles < 2, 'Repair cycle limit requires coordinator/operator decision'

    identity = {
        'role': 'coordinator', 'actor': ACTOR, 'task': 'IG-2B07',
        'model': config['model'], 'reasoning': config['reasoning'],
        'configuration_evidence': CONFIG, 'configuration_sha256': sha(CONFIG),
    }
    new_root = ATTEMPT.rstrip('/')
    mapped_outputs = [p.replace(OLD_ROOT, new_root, 1) for p in selected['outputs']]
    commands = [
        '.venv/Scripts/python.exe -m wgc.sources validate ' + new_root + '/final-verified/inventory.json',
        '.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp ' + new_root + '/pytest-sources -p no:cacheprovider --tb=short',
        'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B07',
        'git diff --check',
    ]
    scope = {
        **identity, 'format': 'wgc-bounded-repair-scope-1',
        'review_evidence': review_pin['path'], 'review_sha256': review_pin['sha256'],
        'finding_ids': ['F01'], 'attempt': ATTEMPT,
        'acceptance': deepcopy(selected['acceptance']), 'tests': deepcopy(selected['tests']),
        'immutable_delivery': delivery_pin, 'mode': 'source_component_accounting',
        'finding': deepcopy(review['findings'][0]),
        'allowed_changes': [
            'Only new files inside the fresh owned attempt. Preserve the entire previous delivery, its envelope, every frozen artifact and all inherited IDs/registry entries byte-for-byte.',
            'Add one stable nested context component for the complete upper black arrow beside B in the second physical-page-28 diagram, linked to parent region:93a4c97f-54e6-4b11-95c2-f0a704491226. Independently verify the original source box before authoring; the review box is an inspection locator, not a substitute for inspection.',
            'Prepare revised copies of author input, inventory/registry, complete region/component ledgers, source pins, inspection sheets, coverage and continuation endpoint indices, preservation/replay/validation reports, handoff and a new delivery envelope consistently inside the new attempt.',
            'Regenerate path-dependent evidence for the complete revised target/component sets serially in the current Python process. Run two separate complete independent serial replays in fresh replay-1 and replay-2 directories; do not sample or copy replay evidence.',
            'Retain all previous logical IDs, source observations, evidence byte pins and inherited records. Path normalization must be explicit and limited to output-path-dependent fields. New paths do not authorize changes to prior frozen bytes.',
        ],
        'prohibited_changes': [
            'No writes to the old inventory-25-28-01 attempt, current review attempt, accepted dependency, source PDF/provenance, public source/tool/test code, prior preparation runs or supervisor metadata.',
            'No altered parent boxes, task/full inventory denominators, gameplay legality decisions, human semantic acceptance, status transitions, downstream work, worker pools, installs, global settings or external APIs.',
        ],
        'required_checks': {
            'finding_validation': deepcopy(review['findings'][0]['repair_validation']),
            'commands': commands,
            'unchanged_original_tests': 'The acceptance and tests arrays above are copied verbatim. The executable command paths above redirect only output/input ownership into the fresh repair attempt; never reuse the frozen pytest basetemp or overwrite old outputs.',
            'source_inspection': 'Freshly inspect the affected original physical-page-28 second diagram and every nested component, including the entire new arrow. Retain and revalidate the prior complete four-page and permitted-boundary inspection records, without inheriting a fresh inspection claim. No wider source scope is authorized.',
            'target_counts': {'new_nested_components': 87, 'new_total_targets': 189, 'full_context_regions': 92, 'total_region_records': 941, 'assigned_inventory': 100, 'full_inventory': 849},
            'preservation': 'Hash-verify the entire previous delivery and all pinned inputs before and after repair. Check exact logical inherited preservation against the accepted dependency using only prepared projections and authorized pinned artifacts. Context/component additions contribute zero inventory denominator.',
            'replays': 'Two separate complete serial regenerations of all revised regions/components with exact invocations, output pins, stable IDs, freshness, geometry, reading order, links, complete target/component set equality and path-normalized comparison reports.',
            'approval_path': 'Keep tests/assertions unchanged. If the restricted Windows token denies pytest temporary-directory access or termination of the owned synthetic context-guard process tree, request approved execution of that exact unchanged command with require_escalated; do not retry the same restricted denial, change ACLs or use bypass flags.',
            'rereview': 'Freeze a new complete delivery and request a fresh independent original-source/component-accounting review. This preparation grants no acceptance or executable readiness.',
        },
        'outputs': mapped_outputs,
        'source_scope': {'physical_page': 28, 'parent_region_id': review['findings'][0]['location']['parent_region_id'], 'inspection_box': review['findings'][0]['location']['inspection_box'], 'source_sha256': review['findings'][0]['location']['source_sha256'], 'unchanged_assigned_scope': [25, 26, 27, 28], 'boundary_context': deepcopy(selected['source_scope']['context_only_boxes'])},
        'toolchain': 'Preserve inherited process_pythonpath containing BOTH repo/src and bundled site-packages and process_path_prefix supplying installed Poppler. No environment replacement or dependency installation.',
        'precedence': 'This current F01 scope replaces obsolete initial write ownership, attempt/output instructions and start conditions. Verbatim acceptance/tests retain their historical paths as frozen contract text; new executable paths and outputs are explicitly listed here. The prior refined contract remains immutable technical context.',
        'repair_limits': {'cycle_for_current_finding': 1, 'maximum_cycles_per_finding': 2, 'maximum_retries_same_unchanged_failure': 2},
    }
    scope_pin = freeze(PREP + '/repair-scope.json', scope)
    verification = {
        **identity, 'summary': 'Current review/delivery and all immutable delivery artifacts verified before bounded structural edit.',
        'review': review_pin, 'immutable_delivery': delivery_pin,
        'frozen_artifacts_verified': len(delivery['artifacts']),
        'finding_evidence_verified': len(review['findings'][0]['evidence']),
        'queue_before_sha256': before_sha, 'prior_repair_cycles': previous_cycles,
        'new_attempt_absent': True, 'events_sha256': hashlib.sha256(json.dumps(task['events'], sort_keys=True).encode()).hexdigest(),
        'source_pdf': selected['source_scope']['source_pdf'],
        'source_provenance': selected['source_scope']['source_provenance'],
    }
    verification_pin = freeze(PREP + '/input-verification.json', verification)
    authorization = {
        **identity, 'format': 'wgc-coordinator-repair-authorization-1',
        'outcome': 'progress',
        'summary': 'Authorize only fresh bounded F01 component-accounting repair; task remains changes_requested and all prior events/artifacts remain immutable.',
        'review_evidence': review_pin['path'], 'review_sha256': review_pin['sha256'],
        'finding_ids': ['F01'], 'attempt': ATTEMPT, 'mode': scope['mode'],
        'criteria': deepcopy(selected['acceptance']),
        'artifacts': [scope_pin, pin(review_pin['path']), pin(delivery_pin['path']), verification_pin],
        'checks': [{'command': 'Local SHA-256 verification of current review, latest frozen delivery, all 2956 artifact pins, four finding evidence pins and source/refinement pins', 'exit_code': 0}],
        'context_access_error': 'Coordinator mistakenly requested the entire current review JSON with Get-Content; tool output was truncated. Subsequent review/delivery reads used selected JSON fields. No prior transcript or dependency closure was requested. Supervisor must retain this observation when evaluating the session.',
        'measurement': {'prepared_utc': datetime.now(timezone.utc).isoformat(), 'tokens': None, 'operator_seconds': None, 'unknown_reason': 'Not exposed to this coordinator.'},
        'semantic_acceptance_granted': False,
        'validation_report': PREP + '/validation-report.json',
        'next_operation': 'Run coordinator checks, preserving this authorization and the new attempt absence; supervisor alone selects and launches any subsequent role.',
    }
    auth_pin = freeze(PREP + '/coordinator-authorization.json', authorization)

    task['write_scope'] = [ATTEMPT]
    task['outputs'] = mapped_outputs
    task['source_scope']['attempt_root'] = new_root
    task['source_scope']['replays']['directories'] = [new_root + '/replay-1', new_root + '/replay-2']
    task['start_conditions'] = [
        'Task remains changes_requested. Read and hash-verify the CURRENT F01 repair scope and coordinator authorization before a new claim; do not use obsolete initial ownership.',
        'The new repair attempt must be absent before claim. Record fresh observed gpt-6.1-sol/high configuration, unique executor ownership and a fresh checkpoint.',
        'Verify current review, frozen prior delivery and all artifact/input pins before and after repair. Prior delivery, review and accepted dependency artifacts are immutable.',
        'Only the current bounded source-component accounting repair is authorized. Preserve exact acceptance/tests, source boundaries and human gates; two complete serial replays and fresh independent rereview remain required.',
        'Use only prepared dependency projections and assigned source scope. Preserve inherited process-local PYTHONPATH with both repo/src and bundled site-packages and installed Poppler paths.',
    ]
    task['handoff'] = [
        'Freeze a NEW complete delivery under the owned F01 attempt, with exact paths/SHA-256, current input packet pin, criteria met/unmet, commands/exits, reports and fresh independent review request.',
        'Record exact inherited preservation, complete revised region/component and continuation endpoint indices, unchanged full/task inventory denominators, all fresh evidence and both complete independent serial replay sets.',
        'Record actual actor/model/reasoning/configuration path and SHA-256, UTC/wall time, exposed tokens or null, defects and unresolved decisions. No semantic acceptance or executable readiness is granted.',
    ]
    task['context'] = [p for p in task['context'] if '/repair-' not in p]
    task['context'].extend([scope_pin['path'], auth_pin['path']])
    task['repair_authorization'] = {
        'review_evidence': review_pin['path'], 'review_sha256': review_pin['sha256'],
        'scope': scope_pin, 'evidence': auth_pin, 'attempt': ATTEMPT,
    }
    assert task['status'] == 'changes_requested'
    old_task = next(t for t in before['tasks'] if t['id'] == 'IG-2B07')
    for field in ('acceptance', 'tests', 'events'):
        assert task[field] == old_task[field]
    assert all(t == next(old for old in before['tasks'] if old['id'] == t['id']) for t in q['tasks'] if t['id'] != 'IG-2B07')
    policy_rel = 'docs/work/context-policy.json'
    policy_before = (ROOT / policy_rel).read_bytes()
    policy = json.loads(policy_before.decode('utf-8-sig'))
    for rel in (scope_pin['path'], auth_pin['path']):
        if rel not in policy['allow']:
            policy['allow'].append(rel)
    workflow = load_workflow()
    (ROOT / policy_rel).write_text(json.dumps(policy, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    workflow.validate(q, ROOT, check_views=False)
    assert sha(queue_rel) == before_sha, 'Unexpected queue writer'
    (ROOT / queue_rel).write_text(json.dumps(q, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    workflow.render(q, ROOT)
    workflow.validate(q, ROOT)
    assert not (ROOT / ATTEMPT).exists()
    for artifact in delivery['artifacts']:
        verify(artifact)
    verify(review_pin)
    verify(delivery_pin)
    freeze(PREP + '/structural-verification.json', {
        **identity, 'summary': 'Bounded queue edit and derived views validate; no status/event/acceptance/test or other-task changes; frozen delivery reverified.',
        'scope': scope_pin, 'authorization': auth_pin, 'queue_before_sha256': before_sha,
        'queue_after_sha256': sha(queue_rel),
        'context_policy_before_sha256': hashlib.sha256(policy_before).hexdigest(),
        'context_policy_after_sha256': sha(policy_rel),
        'unchanged_fields': ['status', 'events', 'acceptance', 'tests'],
        'other_task_records_unchanged': True, 'new_attempt_absent': True,
        'immutable_artifacts_reverified': len(delivery['artifacts']),
        'checks': [{'command': 'workflow.validate(q, ROOT, check_views=False); workflow.render(q, ROOT); workflow.validate(q, ROOT)', 'exit_code': 0}],
    })
    print(json.dumps({'outcome': 'progress', 'authorization': auth_pin, 'scope': scope_pin, 'attempt_absent': ATTEMPT}))


if __name__ == '__main__':
    main()
