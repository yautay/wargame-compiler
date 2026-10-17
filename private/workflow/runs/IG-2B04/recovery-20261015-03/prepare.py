"""Operator-authorized recovery of the interrupted B04 writer; no source acceptance."""
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w
import orchestrate_ig2 as o

PREP = 'private/workflow/runs/IG-2B04/recovery-20261015-03/'
OLD = 'private/workflow/runs/IG-2B04/inventory-13-16-f870c628-01/'
NEW = 'private/workflow/runs/IG-2B04/continuation-13-16-recovery03/'
SESSION = 'private/workflow/orchestrator/20261015T200250Z-56a048a1/002-IG-2B04-executor-ad82c8e3/'
DOC = 'docs/work/repair-context/IG-2B04-interruption-recovery03.md'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def write(rel, value):
    p = w.safe_path(ROOT, rel)
    if p.exists():
        raise ValueError('Never overwrite recovery evidence: ' + rel)
    o.dump(p, value)
    return pin(rel)


q = w.read_json(ROOT / w.QUEUE)
task = next(t for t in q['tasks'] if t['id'] == 'IG-2B04')
assert task['status'] == 'in_progress'
assert not (ROOT / NEW).exists()
original_task = copy.deepcopy(task)
write(PREP + 'queue-before.json', q)
checkpoint = w.read_json(ROOT / OLD / 'checkpoint.json')
o.verify_artifacts(ROOT, {'artifacts': checkpoint['base_files']})
assert pin(checkpoint['input_packet']['path']) == checkpoint['input_packet']
assert pin(OLD + 'claim.json')['sha256'] == task['events'][-1]['sha256']
original_contract = w.read_json(ROOT / task['inventory_contract']['path'])
o.verify_artifacts(ROOT, {'artifacts': [task['inventory_contract']]})

common = {'role': 'coordinator', 'actor': 'operator-authorized-ig2-recovery-20261015-03',
          'task': task['id'], 'model': None, 'reasoning': None,
          'configuration_evidence': 'Builder model/reasoning metadata unavailable; no Sol/high claim.',
          'utc': o.utc(), 'criteria': task['acceptance'],
          'operator_request': 'Inspect why the orchestrator stopped, fix the problem and restart it to continue IG-2.'}
observed = write(PREP + 'assessment.json', {**common,
    'summary': 'Abrupt supervisor and executor loss left a stale lock and in_progress claim. Exact external termination cause is not recorded.',
    'facts': {'supervisor_pid': 20128, 'supervisor_and_exact_child_absent': True,
              'inspection': 'Approved Get-CimInstance Win32_Process matched neither PID 20128 nor the exact executor command; only the inspection command matched its own text.',
              'missing_final_files': ['process-result.json', 'response.json'],
              'status_last_write_utc': '2026-10-15T20:11:22Z',
              'executor_log_last_write_utc': '2026-10-15T20:24:42Z',
              'last_product_log_write_utc': '2026-10-15T20:24:45Z',
              'checkpoint_base_pins_verified': len(checkpoint['base_files']),
              'checkpoint_packet_verified': True, 'claim_hash_verified': True,
              'checkpoint_has_no_completed_criteria_or_output_hashes': True},
    'diagnosis': ['No normal supervisor exception/timeout finalization or lock cleanup was recorded.',
                  'Last source regeneration log ends with PDF xref warnings; they do not prove a fatal error.',
                  'Restricted-token check failures concern process-tree termination; approved unchanged checks are required before launch.',
                  'Console/job termination is a possible cause, not an established fact. Detached job-breakaway startup removes that launch dependency.'],
    'recovery': 'Preserve every current draft byte; a fresh observed Sol/high executor revalidates assigned originals and rebuilds path-dependent evidence in a separate attempt.',
    'artifacts': [pin(SESSION + 'runtime-configuration.json'), pin(OLD + 'checkpoint.json'), pin(OLD + 'claim.json')]})
originals = [pin(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT / OLD).rglob('*')) if p.is_file()]
manifest = write(OLD + 'blocked-state-manifest.json', {**common, 'artifacts': originals,
    'summary': 'Complete immutable draft snapshot before recovery; no accepted delivery exists.'})
blocked = write(OLD + 'blocked.json', {**common,
    'summary': 'Writer and supervisor no longer exist; preserve incomplete draft and require explicit recovery.',
    'artifacts': [manifest, observed, pin(OLD + 'checkpoint.json'), pin(OLD + 'claim.json')]})
w.transition(q, ROOT, task['id'], 'blocked', blocked['path'])
blocked_event = copy.deepcopy(task['events'][-1])
preserved = originals + [manifest, observed, blocked]
preserve = write(PREP + 'preserve.json', {**common, 'artifacts': preserved,
    'summary': 'Original snapshot prefix plus interruption evidence, preserved before every new role.'})
drafts = [pin(OLD + name) for name in ['authored-regions.json', 'authored-registry.json', 'original-inspection.json']]
scope = write(PREP + 'scope.json', {**common, 'mode': 'draft_revalidation',
    'blocked_attempt': OLD, 'blocked_evidence': blocked_event['evidence'],
    'blocked_sha256': blocked_event['sha256'], 'attempt': NEW,
    'acceptance': task['acceptance'], 'tests': task['tests'], 'assessment': observed,
    'preserve_manifest': preserve, 'drafts': drafts, 'physical_pages': [13, 14, 15, 16],
    'required': ['Inspect all four assigned original pages and every proposed component again.',
                 'Draft JSON is candidate data only; do not read old transcripts or derivation scripts.',
                 'Rebuild fresh locators, two full independent replays and every required report.',
                 'Preserve complete accepted nonassigned baseline and registry; keep exact original gates.',
                 'Run unchanged repository/source checks with approved permissions where required.',
                 'Freeze full manifest and obtain fresh independent review; no semantic acceptance.']})

def relocated(value):
    if isinstance(value, str):
        return value.replace(OLD, NEW)
    if isinstance(value, list):
        return [relocated(v) for v in value]
    if isinstance(value, dict):
        return {k: relocated(v) for k, v in value.items()}
    return value

contract = relocated(original_contract)
contract.update({k: v for k, v in common.items() if k not in {'criteria'}})
contract.pop('configuration_sha256', None)
contract.update(summary='Exact original inventory gates retained; fresh output ownership after interruption.',
                recovery_scope=scope, original_contract=task['inventory_contract'])
contract_pin = write(PREP + 'execution-contract.json', contract)
authorization = write(PREP + 'authorization.json', {**common,
    'summary': 'Operator-authorized fresh continuation; base inputs and ownership triaged, readiness has no source inspection or semantic acceptance.',
    'artifacts': [scope, observed, preserve, contract_pin], 'readiness_granted': True,
    'semantic_acceptance_granted': False})
task['continuation_authorization'] = {'scope': scope, 'evidence': authorization, 'attempt': NEW,
    'blocked_evidence': blocked_event['evidence'], 'blocked_sha256': blocked_event['sha256']}
task['inventory_contract'] = contract_pin
task['outputs'] = relocated(task['outputs'])
task['write_scope'] = [NEW, 'private/workflow/runs/IG-2B04/', 'private/workflow/checks/', 'private/workflow/packets/']
task['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md',
                   'docs/work/repair-context/IG-2B04-context-access-02.md', DOC]
task['inputs'] = [s for s in task['inputs'] if not s.startswith('Exact execution contract:')]
task['inputs'].append('Exact recovery contract: ' + contract_pin['path'] + ' SHA256 ' + contract_pin['sha256'])
task['start_conditions'].append('Recovery03 supersedes the interrupted output path; preserve the blocked attempt, use only named draft JSON and a fresh absent continuation root.')
doc = f'''# IG-2B04 interruption recovery03

The operator requested repair and restart of IG-2 after abrupt process loss.
The authoritative inventory contract is `{contract_pin['path']}`
SHA-256 `{contract_pin['sha256']}`. It preserves the original exact criteria,
source input pins, assigned physical pages13-16, two full independent replays,
complete44-page preservation and independent source review requirements.

Read `continuation_authorization.scope` and its named assessment by exact locators.
The old attempt `{OLD}` is frozen, incomplete and unaccepted. Only the three named
draft JSON files are candidate inputs; inspect their assigned fields as needed.
No old helper, session transcript, prior inspection or test claim is inherited.
Reinspect all four original pages and every proposed component; rebuild fresh
path-dependent evidence, both complete replays and all required reports under
`{NEW}`. This directory must be absent before your fresh claim.
The accepted B03 baseline and current repaired reports stay byte-identical;
nonassigned records are carried structurally without printing their content.
Page17 and cross-reference targets remain outside scope. Page12 exit metadata is
the only adjacent boundary context. Never resolve gameplay legality with an LLM.

Use the installed pinned process toolchain with both Python path entries and
Poppler. Run all unchanged required checks; request approved execution when Windows
denies temporary-directory access or synthetic owned-tree termination. Never weaken
tests or alter ACLs. Freeze every actual artifact and obtain fresh independent review.
Technical acceptance does not grant human semantic acceptance.
'''
path = ROOT / DOC
assert not path.exists()
path.write_text(doc, encoding='utf-8')
policy = w.read_json(ROOT / 'docs/work/context-policy.json')
if DOC not in policy['allow']:
    policy['allow'].append(DOC)
o.dump(ROOT / 'docs/work/context-policy.json', policy)
w.transition(q, ROOT, task['id'], 'planned', authorization['path'])
w.transition(q, ROOT, task['id'], 'ready', authorization['path'])
assert task['acceptance'] == original_task['acceptance'] and task['tests'] == original_task['tests']
o.continuation_preservation(ROOT, task, require_absent=True)
o.dump(ROOT / w.QUEUE, q)
w.render(q, ROOT)
w.validate(q, ROOT)
print(json.dumps({'task': task['id'], 'status': task['status'], 'preserved_files': len(originals),
                  'new_attempt': NEW, 'assessment': observed, 'scope': scope}, indent=2))
