"""Refine only the dispatched IG-2B08 contract; never emit dependency records."""
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'scripts'))
import workflow as w

SESSION = 'private/workflow/orchestrator/20261017T064446Z-f1a71866/001-IG-2B08-coordinator-8d84cd90'
OWN = 'private/workflow/runs/IG-2B08/refine-8d84cd90-01'
FUTURE = 'private/workflow/runs/IG-2B08/inventory-8d84cd90-01'
ACTOR = 'ig2:001-IG-2B08-coordinator-8d84cd90:coordinator'
CONFIG = SESSION + '/runtime-configuration.json'


def load(rel):
    return w.read_json(ROOT / rel)


def pin(rel):
    p = ROOT / rel
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def common():
    return {'actor': ACTOR, 'role': 'coordinator', 'model': 'gpt-6.1-sol',
            'reasoning': 'high', 'configuration_evidence': CONFIG,
            'configuration_sha256': w.digest(ROOT / CONFIG)}


def freeze(name, value):
    with (ROOT / OWN / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def find_inventory(x):
    if isinstance(x, dict):
        if {'baseline_inventory', 'identity_registry', 'assigned_page_metadata'} <= x.keys():
            return x
        for v in x.values():
            found = find_inventory(v)
            if found is not None:
                return found
    elif isinstance(x, list):
        for v in x:
            found = find_inventory(v)
            if found is not None:
                return found
    return None


def main():
    config = load(CONFIG)
    assert (config['status'], config['model'], config['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
    assert w.digest(ROOT / CONFIG) == '6c19c296fa6ae7aeb13455fa4baf8e3c500b018d22bd793b17c53706c776e168'
    packet = load(SESSION + '/packet.json')
    task = load(SESSION + '/task.json')
    assert w.digest(ROOT / w.QUEUE) == packet['queue_sha256'], 'Concurrent queue change'
    q = load(w.QUEUE)  # Edit/check scope only; no queue records are emitted.
    before = copy.deepcopy(q)
    t = next(t for t in q['tasks'] if t['id'] == 'IG-2B08')
    assert {k: v for k, v in t.items() if k != 'events'} == task
    assert t['status'] == 'planned' and t['depends'] == ['IG-2B07']
    assert all(next(x for x in q['tasks'] if x['id'] == d)['status'] == 'done' for d in t['depends'])
    assert not (ROOT / FUTURE).exists()
    dep_path = SESSION + '/dependency-view.json'
    assert w.digest(ROOT / dep_path) == '8ffe9a7c68dee816da8cb93bf016a2c4f9a9e80e6edb2b562083dbe59a0aff64'
    inventory = find_inventory(load(dep_path))
    assert inventory is not None
    assert inventory['assigned_physical_pages'] == [29, 30, 31, 32]
    assert inventory['source']['page_count'] == 44
    selected_pins = [inventory['baseline_inventory'], inventory['identity_registry']]
    selected_pins += list(inventory['reports'].values())
    selected_pins += [inventory['source']['pdf'], inventory['source']['provenance']]
    for p in selected_pins:
        assert w.digest(ROOT / p['path']) == p['sha256']
    refs = load(SESSION + '/references.json')
    for e in refs['dependencies'].values():
        assert w.digest(ROOT / e['evidence']) == e['sha256']
    freeze('checkpoint-initial.json', {
        **common(), 'format': 'wgc-coordinator-checkpoint-1', 'task': t['id'],
        'started_utc': datetime.now(timezone.utc).isoformat(), 'input_packet': pin(SESSION + '/packet.json'),
        'dispatched_task': pin(SESSION + '/task.json'), 'base_queue': pin(w.QUEUE),
        'base_context_policy': pin('docs/work/context-policy.json'),
        'completed_criteria': [], 'blocker': None,
        'next_operation': 'Refine exact input, output, preservation and validation contract; do not execute source inventory.'})
    input_pins = {
        **common(), 'format': 'wgc-inventory-batch-inputs-1', 'task': t['id'],
        'dependency': {'id': 'IG-2B07', 'status': 'done', 'done_evidence': {
            'path': refs['dependencies']['IG-2B07']['evidence'],
            'sha256': refs['dependencies']['IG-2B07']['sha256']}},
        **copy.deepcopy(inventory),
        'boundary': {'physical_page': 28,
                     'observation': 'Phalanx B paragraph ends with further; page-29 upper-left paragraph continues rounded up to 4:1 through not routing yet.'},
        'source_access': {
            'inventory_physical_pages': [29, 30, 31, 32],
            'context_only': [
                {'physical_page': 28, 'scope': 'Only the bottom paragraph ending further and its immediately identifying paragraph/figure label, to confirm the page-28/29 continuation.'},
                {'physical_page': 33, 'scope': 'Only the initial continuation of the last page-32 block, if it continues. Inspect the upper edge/initial block to establish the boundary; expand no further.'}],
            'json_access': 'Selected assigned-page/region fields and boundary-linked IDs only. Code may internally copy and validate all records and their byte pins without emitting unassigned records, source text or complete manifests.',
            'forbidden': 'No old sessions/transcripts/helpers, archive/history, whole-PDF analysis, private search, accepted closure/delivery envelope dumps or other dependency records.'},
        'expected_baseline_counts': {'pages': 44, 'regions': 941, 'evidence': 925, 'links': 229},
        'executor_attempt_root': FUTURE,
        'product_outputs': [FUTURE + '/final-verified/inventory.json', FUTURE + '/final-verified/identity-registry.json'],
        'required_reports': ['region-ledger.json', 'continuations.json', 'coverage-report.json',
                             'source-pins.json', 'toolchain.json', 'original-page-inspection.json',
                             'component-ledger.json', 'preservation-report.json', 'replay-report.json',
                             'validation-report.json', 'delivery-handoff.md'],
        'toolchain_policy': 'Use the accepted pinned process_pythonpath including BOTH repo/src and bundled Lib/site-packages, and process_path_prefix with Poppler. These process-local settings are inherited; do not replace PYTHONPATH with src alone, install packages or change global settings.'}
    freeze('input-pins.json', input_pins)
    t['outputs'] = input_pins['product_outputs'] + [FUTURE + '/' + name for name in input_pins['required_reports']]
    t['write_scope'] = [FUTURE + '/']
    t['inputs'] = [
        f"Accepted IG-2B07 complete 44-page inventory: {inventory['baseline_inventory']['path']} (SHA-256 {inventory['baseline_inventory']['sha256']}).",
        f"Persisted companion identity registry: {inventory['identity_registry']['path']} (SHA-256 {inventory['identity_registry']['sha256']}).",
        f"Official source: {inventory['source']['pdf']['path']} (SHA-256 {inventory['source']['pdf']['sha256']}); physical pages 29-32 only, with bounded page-28/33 continuation context as pinned in {OWN}/input-pins.json.",
        f"Official provenance: {inventory['source']['provenance']['path']} (SHA-256 {inventory['source']['provenance']['sha256']}).",
        f"Exact current region ledger, continuations, coverage, source-pins and installed toolchain reports are pinned in {OWN}/input-pins.json; no ancestor inventory or obsolete source placeholder is authoritative.",
        'IG-2A locator contract as implemented by the current hash-pinned contracts/ig/regions.schema.json and src/wgc/sources/ tooling; all 44 pages remain present.'
    ]
    t['context'] = ['docs/IG-WGU-ARCHITECTURE.md', 'docs/IG-DATA-MODEL.md',
                    OWN + '/input-pins.json', 'src/wgc/sources/README.md', 'docs/work/EVIDENCE.md']
    t['tool_context'] = [p['path'] for p in packet['control_files']]
    t['dependency_scope'] = {'physical_pages': [29, 30, 31, 32]}
    t['inventory_contract'] = {
        'format': 'wgc-inventory-batch-contract-1', 'input_pins': pin(OWN + '/input-pins.json'),
        'attempt_root': FUTURE, 'physical_pages': [29, 30, 31, 32],
        'context_only_physical_pages': [28, 33],
        'placeholder_target_ids': [r['id'] for r in inventory['assigned_region_metadata'] if r['key'].endswith(':unprocessed-placeholder')],
        'retained_context_ids': [r['id'] for r in inventory['assigned_region_metadata'] if r['denominator_role'] == 'context'],
        'full_source_page_count': 44, 'independent_replay_count': 2,
        'evidence_generation': 'Serial in the current Python process; no multiprocessing, ProcessPoolExecutor or worker process pools.',
        'scope': 'Physical source inventory and transcription/descriptive observations only; no source-meaning approval or executable gameplay claims.'}
    assert len(t['inventory_contract']['placeholder_target_ids']) == 4
    t['acceptance'] += [
        'Retain the complete accepted 44-page inventory and persisted companion registry. Replace only the four page-29/30/31/32 unprocessed placeholders; remove their active membership but keep every retired registry entry. Preserve every nonassigned record, prior context region, link, evidence object, registry binding and retained reading-order subsequence unchanged; document exact before/after preservation counts and hashes.',
        'Freshly inspect every assigned ORIGINAL physical page 29-32, every proposed region boundary, and every table/diagram/example component. Pin original-page renders and observations to source SHA-256, page IDs and fresh paths in original-page-inspection.json and component-ledger.json; inherited observations never substitute for inspection.',
        'Author disjoint regions independently of KB headings, including headings, clauses, notes, examples, tables/cells/legends, diagrams/components and editorial material. Do not use broad mixed regions to hide components; record uncertainty and any uncovered geometric area explicitly. Gaps and placeholders never count as represented source content.',
        'Fresh source-region evidence includes exact crop PDF, PNG, text, page_basis_hash, region revision, offsets, engines, DPI, dimensions, safe paths and SHA-256. The root source-pins.json exhaustively indexes every assigned original-page and new region/component artifact and both replays; each referenced artifact exists at its pinned path and is included in the frozen delivery.',
        'Preserve page-28/29 continuation references from the accepted baseline and inspect the page-32/33 exit using only the bounded context scope. Report context-only IDs separately; their denominator contribution is zero. Cross-boundary references and inherited context regions remain present, without assigning uninspected source content to inventory.',
        'Run two COMPLETE independent replays separately from the pinned baseline and same persisted registry/author selections into fresh replay-1 and replay-2 directories. Generate evidence serially for the entire region/component set in each. Compare stable IDs, author fields, reading order, links, registry and path-normalized artifact bytes/locators; report actual path-dependent inventory hashes without claiming they must be identical.',
        'Report full 44-page, assigned four-page, inherited/nonassigned and context-only denominators separately in coverage-report.json, with gaps/unprocessed and transcription/descriptive/formal statuses. Never equate geometric area or inventory completion with source meaning, semantic acceptance or executable readiness.',
        'Freeze final-verified/inventory.json and its companion identity-registry.json plus all root reports, derivations, helpers, required evidence files and two complete replay artifact sets in an exhaustive ordered path/SHA-256 delivery. Every declared output must be present and current; repair source-reference indexes only for named current reports.',
        'A fresh independent reviewer inspects every assigned original page, proposed boundary/component, context-only boundary and complete region ledger against the final frozen hashes; independently checks evidence freshness/index completeness, both complete replays, 44-page preservation and all original/appended criteria. Technical review does not grant human semantic acceptance.'
    ]
    t['tests'] += [
        f"Run .venv/Scripts/python.exe -m pytest tests/sources -q --basetemp {FUTURE}/source-pytest -p no:cacheprovider --tb=short with the inherited pinned toolchain. Keep tests/assertions unchanged; if restricted-token temp access fails, request approved execution of that exact unchanged command.",
        f"Run .venv/Scripts/python.exe -m wgc.sources validate {FUTURE}/final-verified/inventory.json and validate both replay inventories with actual root/source access. Validate final companion registry equality and canonical hashes; pin commands/exits in validation-report.json.",
        'Add and run an owned batch verifier over the complete accepted baseline and result: source/44-page set equality, preserved nonassigned record/link/evidence objects and registry entries, retained reading-order subsequence, exactly four placeholders retired, assigned/context target set separation, disjoint positive geometry, complete new evidence/component index and all artifact hashes. It must fail for missing regions/components, stale/missing index paths or a replay that omits any assigned component.',
        'Run complete replay-1 and replay-2 separately; require equal full assigned region/component sets and stable identities, complete registry bindings, normalized evidence bytes/locators and zero missing artifact references. Check fresh original-page renders plus visual inspection on every assigned page and each authorized context boundary.',
        'Run scripts/check.ps1 -Task IG-2B08 and git diff --check; preserve reports, actual exits and any approved exact-command execution evidence. If context-guard process termination is denied by the restricted token, request approved execution of the exact unchanged validation command without changing tests, ACLs or assertions.'
    ]
    t['start_conditions'] += [
        f"Claim a fresh absent owned directory {FUTURE}; record a new observed gpt-6.1-sol/high runtime, actor, packet hash, exact input pins and checkpoint before product writes. No inherited completion, source inspection, semantic acceptance or green checks.",
        'Hash-verify every pinned input and current accepted report, confirm the complete 44-page baseline and companion registry, and use only the task-bound dependency/search/access helpers. Available exact context and bounded page/ID authorization are mandatory; helper refusal ends the session, with no fallback.',
        'Only the supervisor launches the next sequential role. No product code/schema changes, online services, global configuration, nested agents, unrelated tasks or downstream IG-3 work are authorized.'
    ]
    t['handoff'] += [
        'Provide complete source-pins, preservation and replay reports; exact full/task/context denominator counts, source uncertainties and entry/exit continuation IDs; the independent reviewer must validate the exhaustive frozen artifact set and all original/appended criteria.',
        'Actual runtime configuration_evidence/configuration_sha256 and actor/model/reasoning belong on every claim/delivery/review. Record UTC/wall time, tokens only when exposed (otherwise null), failures/retries and unresolved decisions without inventing semantic approval.'
    ]
    # Preserve every other task and all prior evidence, without serializing it to context.
    assert all(a == b for a, b in zip(before['tasks'], q['tasks']) if a['id'] != t['id'])
    for key in ('acceptance', 'tests'):
        assert t[key][:len(task[key])] == task[key]
    assert t['semantic_acceptance_required'] == task['semantic_acceptance_required']
    policy_path = ROOT / 'docs/work/context-policy.json'
    policy = load('docs/work/context-policy.json')
    for rel in t['context'] + t['tool_context'] + [p['path'] for p in selected_pins]:
        if rel not in policy['allow']:
            policy['allow'].append(rel)
    assert w.digest(ROOT / w.QUEUE) == packet['queue_sha256']
    policy_path.write_text(json.dumps(policy, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    q['updated'] = datetime.now(timezone.utc).date().isoformat()
    w.validate(q, ROOT, check_views=False)
    (ROOT / w.QUEUE).write_text(json.dumps(q, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    w.render(q, ROOT)
    w.validate(q, ROOT)
    # Packet budget is checked without writing a context dump or changing task state.
    prospective = copy.deepcopy(q)
    next(x for x in prospective['tasks'] if x['id'] == t['id'])['status'] = 'ready'
    # Current planned task has no event; simulate readiness only in memory for budget checking.
    for rel in t['context']:
        assert w.permitted(ROOT, rel) and (ROOT / rel).is_file()
    paths = list(dict.fromkeys(w.BASE_CONTEXT + ['docs/work/tasks/IG-2B08.md'] + t['context']))
    text_bytes = sum(len((ROOT / rel).read_bytes()) + len(rel) + 20 for rel in paths)
    assert text_bytes < 100_000
    freeze('refinement-check.json', {
        **common(), 'format': 'wgc-inventory-refinement-check-1', 'task': t['id'],
        'result': 'passed', 'criteria': t['acceptance'], 'assigned_pages': [29, 30, 31, 32],
        'placeholder_count': 4, 'baseline_counts': inventory['counts'],
        'input_pin_count': len(selected_pins), 'input_hashes_verified': True,
        'dependency_done_pin_verified': True, 'other_tasks_unchanged': True,
        'original_acceptance_and_tests_preserved_verbatim': True,
        'human_gate_unchanged': True, 'future_executor_directory_absent': True,
        'estimated_packet_bytes_upper_bound': text_bytes,
        'product_writes': 0, 'source_inspection_claims': 0,
        'queue_after_refinement': pin(w.QUEUE), 'context_policy_after_refinement': pin('docs/work/context-policy.json'),
        'input_pins': pin(OWN + '/input-pins.json'),
        'next_operation': 'Run unchanged sources tests and diff check; freeze real ready evidence and transition only this task.'})
    print(json.dumps({'task': t['id'], 'status': t['status'], 'input_pins_verified': len(selected_pins),
                      'assigned_pages': [29, 30, 31, 32], 'packet_bytes_bound': text_bytes,
                      'other_tasks_unchanged': True, 'product_writes': 0}))


if __name__ == '__main__':
    main()
