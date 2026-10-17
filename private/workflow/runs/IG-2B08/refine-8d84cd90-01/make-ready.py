"""Freeze coordinator readiness after actual contract/input and sources checks."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
OWN = 'private/workflow/runs/IG-2B08/refine-8d84cd90-01'
SESSION = 'private/workflow/orchestrator/20261017T064446Z-f1a71866/001-IG-2B08-coordinator-8d84cd90'
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w


def pin(rel):
    return {'path': rel, 'sha256': w.digest(ROOT / rel), 'bytes': (ROOT / rel).stat().st_size}


def freeze(name, obj):
    with (ROOT / OWN / name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    config_path = SESSION + '/runtime-configuration.json'
    common = {'role': 'coordinator', 'actor': 'ig2:001-IG-2B08-coordinator-8d84cd90:coordinator',
              'model': 'gpt-6.1-sol', 'reasoning': 'high', 'configuration_evidence': config_path,
              'configuration_sha256': w.digest(ROOT / config_path)}
    assert common['configuration_sha256'] == '6c19c296fa6ae7aeb13455fa4baf8e3c500b018d22bd793b17c53706c776e168'
    q = w.read_json(ROOT / w.QUEUE)  # Selected-task edit/check only.
    t = next(x for x in q['tasks'] if x['id'] == 'IG-2B08')
    check = w.read_json(ROOT / OWN / 'refinement-check.json')
    assert w.digest(ROOT / w.QUEUE) == check['queue_after_refinement']['sha256']
    assert check['result'] == 'passed' and t['status'] == 'planned'
    assert all(next(x for x in q['tasks'] if x['id'] == d)['status'] == 'done' for d in t['depends'])
    assert not (ROOT / t['inventory_contract']['attempt_root']).exists()
    original = w.read_json(ROOT / SESSION / 'task.json')
    for field in ('acceptance', 'tests'):
        assert t[field][:len(original[field])] == original[field]
    freeze('refined-contract.json', {k: v for k, v in t.items() if k != 'events'})
    sources_command = '.venv/Scripts/python.exe -m pytest tests/sources -q --basetemp ' + OWN + '/source-pytest -p no:cacheprovider --tb=short'
    freeze('prechecks.json', {
        **common, 'format': 'wgc-coordinator-prechecks-1', 'task': t['id'],
        'checks': [
            {'command': '.venv/Scripts/python.exe ' + OWN + '/refine.py', 'exit_code': 0,
             'report': pin(OWN + '/refinement-check.json')},
            {'command': sources_command, 'exit_code': 1, 'sandbox_permissions': 'use_default',
             'failure': 'Windows restricted token: PermissionError WinError 5 accessing pytest basetemp during setup/cleanup; no assertions changed.'},
            {'command': sources_command, 'exit_code': 0, 'sandbox_permissions': 'require_escalated',
             'automatic_review': 'approved execution occurred', 'result': '71 passed in 22.52s'},
            {'command': 'git diff --check', 'exit_code': 0, 'sandbox_permissions': 'use_default',
             'observation': 'No whitespace errors returned; stderr contained restricted-token permission warnings for preexisting private test artifacts and line-ending notices. The full required check remains to run.'}],
        'source_test_assertions_unchanged': True, 'source_test_retry_count': 1,
        'product_completion_or_source_inspection_claimed': False})
    ready = {
        **common, 'format': 'wgc-inventory-ready-1', 'task': t['id'],
        'summary': 'IG-2B08 is refined for fresh execution on physical pages 29-32 from accepted IG-2B07 inputs; preserve the complete 44-page baseline and registry. No product inventory, inspection, semantic acceptance or gameplay readiness is claimed.',
        'criteria': [
            'IG-2B07 is done with its exact accepted baseline, registry, current reports, official source and provenance pins verified locally.',
            'Exact assigned pages/placeholder IDs, bounded context-only access, fresh disjoint outputs, complete preservation, original-page/component inspection, serial evidence and two complete independent replays are pinned.',
            'Every original acceptance criterion and test is retained verbatim; fresh independent technical review and separate semantic/human gates remain binding.',
            'Exact available context is allowlisted and below 100 KB; inherited pinned toolchain and unchanged source validation passed; future owned attempt is absent.'],
        'artifacts': [pin(OWN + '/' + n) for n in [
            'checkpoint-initial.json', 'input-pins.json', 'refined-contract.json',
            'refine.py', 'make-ready.py', 'refinement-check.json', 'prechecks.json']],
        'checks': [
            {'command': '.venv/Scripts/python.exe ' + OWN + '/refine.py', 'exit_code': 0},
            {'command': sources_command, 'exit_code': 0, 'sandbox_permissions': 'require_escalated', 'result': '71 passed'},
            {'command': 'git diff --check', 'exit_code': 0, 'limitation': 'Restricted-token stderr warnings retained in prechecks; full check pending.'}],
        'readiness_scope': 'Executor may claim only the frozen refined contract; no implementation or acceptance is inherited.',
        'measurement': {'ended_utc': datetime.now(timezone.utc).isoformat(), 'input_tokens': None,
                        'output_tokens': None, 'operator_seconds': None,
                        'unknown_reason': 'Token counters and operator time were not exposed.'},
        'next_operation': 'Run scripts/check.ps1 -Task IG-2B08, preserve all actual validation results, then return the immutable coordinator report. Only the supervisor launches the executor.'}
    freeze('ready.json', ready)
    # The supported transition owns locking, append-only event evidence and view rendering.
    print('Frozen readiness evidence: ' + OWN + '/ready.json')


if __name__ == '__main__':
    main()
