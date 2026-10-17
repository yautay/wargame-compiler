"""Validate F02 draft recovery and role-bound output access, then dispatch fresh work."""
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B08/F02-validation-recovery-20261017-01/'


def write(name, body):
    with (ROOT / PREP / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(body, f, ensure_ascii=False, indent=2); f.write('\n')


def main():
    q = w.read_json(ROOT / w.QUEUE); w.validate(q, ROOT)
    task, role = o.select(q)
    prepared = w.read_json(ROOT / PREP / 'preparation-result.json')
    assert (task['id'], task['status'], role) == ('IG-2B08', 'ready', 'executor')
    assert prepared['queue_sha256'] == w.digest(ROOT / w.QUEUE)
    assert not (ROOT / prepared['fresh_attempt']).exists()
    installed = w.read_json(ROOT / 'private/workflow/launches/20261016T150141Z-3c1e178b/launch.json')
    rg = installed['ripgrep']
    assert Path(installed['codex']).is_file() and w.digest(Path(rg['path'])) == rg['sha256']
    os.environ.update(WGC_RIPGREP_PATH=rg['path'], WGC_RIPGREP_SHA256=rg['sha256'],
                      PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0')
    preflight = ROOT / PREP / 'dispatch-preflight-02'; preflight.mkdir(exist_ok=False)
    packet = o.prepare(ROOT, q, task, role, preflight)
    o.launch_environment(ROOT, task, preflight, installed['codex'])
    scope = w.read_json(preflight / 'access-manifest.json')['source_validation']
    expected = [prepared['fresh_attempt'] + name + '/inventory.json'
                for name in ('final-verified', 'replay-1', 'replay-2')]
    assert scope['mode'] == 'owned_attempt' and scope['attempt'] == prepared['fresh_attempt']
    assert [p['path'] for p in scope['inputs']] == expected and all('sha256' not in p for p in scope['inputs'])
    print('Fresh F02 continuation, complete preservation and exact executor output-validation authority verified.', flush=True)
    view = w.read_json(preflight / 'dependency-view.json')
    tool = view['dependencies']['IG-2B07']['inventory']['reports']['toolchain.json']
    env = o.validation_environment(ROOT, dict(task, context=task['context'] + [tool['path']]), rg)
    log = ROOT / PREP / 'full-check.log'
    code = o.run_check(['pwsh', '-NoProfile', '-File', 'scripts/check.ps1', '-Task', task['id']],
                       ROOT, log, time.monotonic() + 1200, env)
    lines = log.read_text(encoding='utf-8-sig').splitlines()
    logs = Path(next(line.partition('=')[2] for line in lines if line.startswith('LOG_ROOT=')))
    assert logs.resolve().is_relative_to(ROOT)
    checks = w.read_json(logs / 'result.json')
    write('check-result.json', {'exit_code': code, 'checks': checks, 'logs': logs.relative_to(ROOT).as_posix()})
    assert code == 0 and all(checks[k] == 0 for k in ('plan_exit', 'dry_run_exit', 'tests_exit', 'diff_exit'))
    assert prepared['queue_sha256'] == w.digest(ROOT / w.QUEUE)
    protected = w.read_json(ROOT / PREP / 'preserve-manifest.json')
    o.verify_artifacts(ROOT, protected)
    write('launch-authorization.json', {
        'utc': o.utc(), 'task': task['id'], 'role': role, 'operator_authorized': True,
        'queue_sha256': prepared['queue_sha256'], 'fresh_attempt': prepared['fresh_attempt'],
        'validation_inputs': expected, 'validation_mode': 'owned_attempt',
        'packet_text_bytes': packet['text_bytes'], 'preserved_artifacts': len(protected['artifacts']),
        'checks': checks, 'logs': logs.relative_to(ROOT).as_posix(),
        'actual_model': None, 'actual_reasoning': None,
        'configuration_evidence': 'Coordinating configuration unavailable; fresh executor must confirm observed gpt-6.1-sol/high.',
        'semantic_acceptance': False})
    result = o.start_background(ROOT, installed['codex'], 48, 3600, 28800)
    write('start-result.json', result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
