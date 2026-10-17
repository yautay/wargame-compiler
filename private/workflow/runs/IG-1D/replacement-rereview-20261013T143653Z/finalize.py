"""Freeze final technical pass and workflow-compatible exact-delivery acceptance."""
from datetime import datetime, timezone
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
BASE = ROOT / 'private/workflow/runs/IG-1D'
OLD = BASE / 'replacement-rereview-20261013T140127Z'
ACTOR = 'ig1d-replacement-reviewer-20261013T140127Z'
DELIVERY = BASE / 'repair-02-20261013/delivery.json'
def read(p): return json.loads(p.read_bytes())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def artifact(p): return {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
def write(n, d):
    with (RUN / n).open('x', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2); f.write('\n')

before, after = read(RUN / 'verification-before.json'), read(RUN / 'verification-after.json')
assert before['all_match'] and after['all_match']
assert before['reviewed_delivery'] == after['reviewed_delivery']
assert before['queue_sha256'] == after['queue_sha256'] == sha(ROOT / 'docs/work/queue.json')
delivery = read(DELIVERY)
assert sha(DELIVERY) == 'ea2d2cacf42939e516dfc8b65f6c0cffc2d2267478819233fb1f573fddd4275c'
queue = read(ROOT / 'docs/work/queue.json')
task = next(t for t in queue['tasks'] if t['id'] == 'IG-1D')
assert delivery['criteria'] == task['acceptance'] and task['status'] == 'review'
config = read(OLD / 'configuration-confirmed.json')
assert config['model'] == 'gpt-6.1-sol' and config['reasoning'] == 'high'
audit, supplement = read(RUN / 'independent-accounting.json'), read(RUN / 'supplemental-accounting.json')
assert audit['result'] == supplement['result'] == 'pass'
checks = [read(p) for p in sorted(RUN.glob('*-check.json'))]
by_name = {p.name.removesuffix('-check.json'): read(p) for p in RUN.glob('*-check.json')}
for key in ['original-native', 'explicit-native', 'risk', 'history', 'boundaries', 'accounting-native', 'project', 'diff']:
    assert by_name[key]['exit_code'] == 0
assert all(c['exit_code'] == 0 for c in checks)
checks.append({'command': '.venv/Scripts/python.exe -B ' + (RUN / 'supplemental_audit.py').relative_to(ROOT).as_posix(),
    'exit_code': 0, 'start_utc': supplement['started_utc'], 'end_utc': supplement['ended_utc'],
    'wall_seconds': supplement['wall_seconds'], 'result': artifact(RUN / 'supplemental-accounting.json'),
    'capture_note': 'Direct tool completion exit 0; complete measurements and output are in supplemental-accounting.json.'})
write('checks.json', checks)
failed_setup = [read(RUN / 'verification-setup-failure.json'), read(RUN / 'package-mapping-setup-failure.json')]
assert all(c['exit_code'] == 1 for c in failed_setup)
write('setup-attempts.json', {'failed_setup_attempts': failed_setup, 'required_product_checks': 'All passing in checks.json; failed attempts are not relabeled or included as passing required checks.',
    'successful_verifier': artifact(RUN / 'verify-final.py'), 'before':artifact(RUN / 'verification-before.json'), 'after':artifact(RUN / 'verification-after.json')})
configuration = {'model':config['model'],'reasoning':config['reasoning'],'requested_model':'gpt-6.1-sol','requested_reasoning':'high',
    'same_reviewer_chat_continuity':True,'independent_actor':ACTOR,
    'original_direct_confirmation':artifact(OLD / 'configuration-confirmed.json'),
    'confirmation_source':config['configuration_evidence'],
    'note':'Same replacement reviewer session confirmed directly by the operator earlier in this chat. Neither executor nor prior unavailable reviewer confirmation is used as proof.'}
write('configuration-continuity.json', configuration)

prior = read(OLD / 'dispositions.json')['dispositions']
dispositions = []
for d in prior[:3]:
    dispositions.append({'finding_id':d['finding_id'],'disposition':'closed','repair_iterations_used':1,
        'previous_closure_preserved':True,'prior_basis':d['basis'],
        'current_independent_verification':'All 15 original assertions and existing risk/receipt/history controls replayed unchanged and pass; full fresh byte/field/binding/hash and independently reconstructed reference/cycle oracle pass.',
        'evidence':['original-native.log','risk.log','history.log','explicit-native.log','independent-accounting.json','supplemental-accounting.json']})
dispositions.append({'finding_id':'IG1D-R04','disposition':'closed','repair_iterations_used':2,'maximum_repair_iterations':2,
    'basis':'The named receipt guard first enumerates all persisted receipt children (including inactive children), then requires compatible logical kind, resolved parent scope and persistent child key. Incompatible reuse raises ValueError on a private registry copy before a replacement allocation can be returned. The original strict changed-kind assertion and new kind/key/scope controls pass. A deliberately new decision identifier permits a different typed output; unchanged replay preserves it. Correction/rename, keyed reorder, locator/file move and exact historical revision/origin preservation pass.',
    'fresh_independent_boundaries':['Retired prior receipt child still enforces immutable kind contract',
        'Changed/removed persistent key rejects full build without mutating registry or bundle',
        'After rejection, new named typed output preserves old receipt history and repeats canonically',
        'Keyed merge correction with moved locator and parent order retains ID/origin_key, exact lineage/supersession and canonical replay'],
    'evidence':['original-native.log','risk.log','history.log','explicit-native.log','boundaries.log']})
write('findings.json', [])
write('dispositions.json', {'technical_result':'pass','actor':ACTOR,'reviewed_repair_iteration':2,
    'dispositions':dispositions,'remaining_findings':[],'new_finding_ids':[],'product_modified_by_reviewer':False,
    'repair_budget_note':'R04 consumed both repair iterations and is now closed. No further repair is requested.'})
criteria_results = [
    {'criterion': task['acceptance'][0], 'result':'pass', 'evidence':'Repeated synthetic replay and two actual complete canonical transforms/publications are byte-identical, including new repair-2 publication; operational clocks are separate and canonical timestamps remain null.'},
    {'criterion': task['acceptance'][1], 'result':'pass', 'evidence':'Unchanged original and public reorder/insert/delete/rename/file-move controls pass. Contradictory/indistinguishable rematches retain explicit gaps; key/scope/receipt changes reject atomically.'},
    {'criterion': task['acceptance'][2], 'result':'pass', 'evidence':'Unchanged many-to-many and scope assertions pass. Complete raw-file/field/binding coordinates and subtrees independently verified. All 2930 diagnostics and cycle components independently reconstructed; wildcard/subpoint scopes remain exact or explicitly unresolved.'},
    {'criterion': task['acceptance'][3], 'result':'pass', 'evidence':'Every graph/aspect hash and selected/historical typed reference resolves. Historical parent/child exact revisions retained under correction. No inherited semantic approval, coverage or executable acceptance.'}
]
write('criteria.json', criteria_results)
write('reviewed-artifact-manifest.json', {'format':'wgc-reviewed-artifacts-1','task':'IG-1D','actor':ACTOR,
    'delivery':artifact(DELIVERY),'artifact_count':51,'artifacts':delivery['artifacts'],
    'before_verification':artifact(RUN / 'verification-before.json'),'after_verification':artifact(RUN / 'verification-after.json'),
    'all_exact_bytes_match':True,'package_mapping':after['package_mapping']})
ended = datetime.now(timezone.utc)
start = read(RUN / 'checkpoint.json')['started_utc']
measurement = {'started_utc':start,'ended_utc':ended.isoformat(),'wall_seconds':(ended-datetime.fromisoformat(start)).total_seconds(),
    'scope':'Measured fresh evidence run, including failed setup and correction. Earlier instruction reading unmeasured and excluded.',
    'input_tokens':None,'output_tokens':None,'tokens':None,'cost':None,'operator_seconds':None,
    'unknown_reason':'Usage/cost/operator time not exposed or reported.'}
write('measurement.json', measurement)
project_root = Path(re.search(r'LOG_ROOT=(.+)',(RUN / 'project.log').read_text()).group(1).strip())
project_files = [artifact(p) for p in sorted(project_root.rglob('*')) if p.is_file() and p.suffix in ['.json','.log']]
write('project-evidence.json',{'artifacts':project_files,'check':artifact(RUN / 'project-check.json')})
summary = 'Independent technical PASS of exact IG-1D repair-2 delivery. R04 closed after its final repair; R01-R03 closure preserved. All strict controls and full independent corpus accounting/reproducibility pass. Coordinator transition pending; no semantic, publisher-coverage or executable approval.'
report = f'''# IG-1D repair iteration 2 independent final re-review

Result: **technical PASS**. Every original finding is closed. R01-R03 retain their iteration-1 closure; R04 is closed after iteration 2 of maximum 2. No remaining or new finding was identified. This review supplies exact-delivery acceptance evidence for the coordinator; it does not change queue state.

Reviewer: `{ACTOR}`, distinct from current executor `{delivery['actor']}`. This is the same replacement reviewer chat directly confirmed earlier by the operator as GPT-6.1 Sol / high (`potwierdzam`). Configuration continuity references the unchanged original confirmation; executor and unavailable reviewer's settings are not treated as proof.

Reviewed delivery: `private/workflow/runs/IG-1D/repair-02-20261013/delivery.json`, SHA256 `ea2d2cacf42939e516dfc8b65f6c0cffc2d2267478819233fb1f573fddd4275c`. Exactly 51 artifacts were checked before and after review; the exact list is in reviewed-artifact-manifest.json, review.json, review-manifest.json and acceptance-evidence.json. The queue remained review at SHA256 `{after['queue_sha256']}`; IG-1A/B/C done and IG-1E planned. No product, public test, queue or generated document was changed by this reviewer.

Preservation verified every mapped version: 50 repair-1 delivery artifacts, 119 checkpoint versions, 54 prior finalized review artifacts and 182 accepted foundation versions. Prior review/manifest/seal pins, original parent versions, original reviewer evidence and the unfinalized previous re-review all retain exact bytes. The prior identity.py version is checked at repair-02-20261013/baseline/identity.py, not at the now-repaired working path. Input pins, accepted import, original source-v1 schema/validator and approved source-export profile remain unchanged.

R04's guard checks all prior receipt children before filtering can turn a changed contract into a first allocation. It checks logical kind, resolved parent identity scope and persistent key and rejects incompatibility on a private copy. The unchanged receipt-edge failing control now passes. Key addition/removal/change and changed scope reject; keyed split reorder, unique-child correction/rename, parent reorder and moved file/locator replay retain identity and origins. A new decision ID permits a deliberate new output contract and retains prior receipt history. Six fresh independent controls also verify inactive persisted-child enforcement, whole-export registry/bundle immutability on rejection, rejection followed by valid new decision/replay and exact moved-child historical lineage/supersession with canonical repetition. Original ambiguity and many-to-many assertions remain unchanged.

R01 remains closed: contradictory anonymous label/body/number evidence retains explicit candidate/origin gaps, with positive local/three-way conflict and explicit no-allocation resolution controls. R02 remains closed: overlapping hint/lineage decisions reject atomically while disjoint decisions, keyed children and many-to-many mappings work. R03 remains closed: direct active IDs/aliases resolve only as a singleton union, retired or nonexistent IDs stay unresolved, alias collisions remain ambiguous, and exact scope/both-endpoint/navigation-cycle controls pass. Full independent diagnostics corroborate the reference behavior.

Required and affected validation:

- Public adapter/export suites: 101 passed, exit 0.
- Original reviewer probes: all 15 passed unchanged, exit 0.
- Existing risk/receipt-edge probes: all 10 passed unchanged, exit 0.
- Existing export-history probes: 2 passed unchanged, exit 0.
- Fresh independent receipt boundary/export controls: 6 passed, exit 0.
- scripts/check.ps1 -Task IG-1D: 102 passed, queue/DAG/projections/dry-run and diff passed, exit 0.
- git diff --check: exit 0.
- Full fresh independent accounting and two full canonical transforms/publications: exit 0.
- Supplemental independent unknown-location/reference/cycle accounting: exit 0.

Thus 128 preserved public/original/risk/history controls and 6 additional independent controls pass. The project suite is reported separately because test scopes overlap. Exact argv, UTC, process-local import paths, fresh short basetemp, disabled cache and wall times are in checks.json and logs. Native no-follow execution used the previously justified narrow local scope without bypassing assertions or changing global configuration.

Two reviewer setup failures are preserved separately, with actual exit 1 and unavailable individual timing as null: the initial operational actor normalizer omitted executor_actor -> review_actor, then the verifier assumed the new delivery listed the official package path instead of its new publication copy. Diff inspection corrected only operational normalization and exact package mapping in a separate verify-final.py. Both failed scripts/evidence are retained. No product/probe/accounting assertion was weakened. setup-attempts.json records those failures; acceptance required checks include only independently passing product/project/accounting checks.

Independent full accounting enumerated {audit['manifest_entries']} exact manifest entries, {audit['available_files']} available files and {audit['missing_sources']} missing configured sources. It verified {audit['independent_record_count']:,} records, {audit['independent_field_count']:,} YAML field/container coordinates, {audit['binding_count']:,} origin-binding subtrees, {audit['source_graph_records']:,} source graph records and {supplement['identity_count']:,} identities. Exact raw bytes, values, parent coordinates, observations, allocation keys, field marks, aspect/record hashes and active/historical reference closure are independently checked. Unknown roots: {supplement['unknown_root_count']}, covering {supplement['unknown_field_container_location_count']:,} field/container locations. The separate raw-input oracle reconstructs all {supplement['independent_reference_diagnostic_count']:,} diagnostic target/candidate sets ({supplement['reference_status_counts']['resolved']:,} resolved, {supplement['reference_status_counts']['unresolved']} unresolved) and cycles by mutual reachability. Importer counters are cross-checks, not the inventory oracle.

Current repair-2 publication is `private/workflow/runs/IG-1D/repair-02-20261013/packages/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc`. All four files are byte-identical to the unchanged canonical package used by the preserved accounting assertions; both copies are pinned explicitly before and after review. A fresh seeded complete transform equals those exact bytes, a second complete transform equals the first, and two actual publications in this new review run are byte-identical with distinct measured operational sidecars. Canonical profile clocks stay null; no pre-repair/pre-manifest output is selected.

All four exact task criteria are satisfied within structural import/identity/export scope; criterion-by-criterion evidence is in criteria.json. Publisher coverage, human source-meaning/semantic acceptance and executable readiness are not granted. Mixed-edition/identity-to-original uncertainty, 36 missing configured sources, unresolved scopes and blocking unreconciled content remain explicit.

Measured evidence run: {measurement['started_utc']} to {measurement['ended_utc']}, {measurement['wall_seconds']:.3f} seconds. Full accounting measured {audit['wall_seconds']:.3f} seconds. Usage, cost and operator time remain null. Earlier instruction reading was unmeasured and excluded.

Next action: coordinator verifies the frozen review/manifest/acceptance pins, records technical acceptance then done through workflow, and separately handles IG-1E readiness. No IG-1E/IG-2 execution, semantic decision, commit/push, new chat/agent/worktree/automation or message to another chat was performed here. review-manifest.json includes acceptance-evidence.json; final-seal.json pins final review/report/manifest/acceptance hashes without a circular hash dependency.
'''
with (RUN / 'report.md').open('x', encoding='utf-8') as f: f.write(report)
evidence = [artifact(p) for p in sorted(RUN.rglob('*')) if p.is_file()]
review = {'role':'reviewer','actor':ACTOR,'executor_actor':delivery['actor'],'task':'IG-1D','summary':summary,
    'technical_result':'pass','technical_pass':True,'independent_pass':True,'review_finalized':True,
    'model':config['model'],'reasoning':config['reasoning'],'requested_model':'gpt-6.1-sol','requested_reasoning':'high',
    'configuration_evidence':artifact(RUN / 'configuration-continuity.json'),'same_reviewer_chat_continuity':True,
    'reviewed_delivery':{**artifact(DELIVERY),'artifact_count':51,'artifacts':delivery['artifacts']},
    'criteria':task['acceptance'],'criteria_results':criteria_results,'findings':[],'dispositions':dispositions,
    'new_finding_ids':[],'remaining_finding_ids':[],'defect_counts':{'P0':0,'P1':0,'P2':0,'P3':0},
    'repair_iterations_used':delivery['repair_cycles'],'maximum_repair_iterations':2,
    'checks':checks,'failed_setup_attempts':failed_setup,'artifacts':evidence,
    'current_packet':after['packet'],'queue_sha256_before':before['queue_sha256'],'queue_sha256_after':after['queue_sha256'],
    'before_verification':artifact(RUN / 'verification-before.json'),'after_verification':artifact(RUN / 'verification-after.json'),
    'all_exact_reviewed_bytes_preserved':True,'all_prior_foundation_versions_preserved':True,
    'full_accounting':{k:v for k,v in audit.items() if k not in ['ledger','binding_ledger','unknown_locations','publications']},
    'supplemental_accounting':{k:v for k,v in supplement.items() if k not in ['unknown_roots','diagnostics','cycles']},
    'canonical_publication_mapping':after['package_mapping'],'measurement':measurement,
    'product_modified_by_reviewer':False,'queue_modified_by_reviewer':False,
    'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False,
    'remaining_gates':['Coordinator verifies exact technical acceptance and records accepted/done','Separate publisher coverage, human source meaning acceptance and executable readiness'],
    'acceptance_evidence_path':(RUN / 'acceptance-evidence.json').relative_to(ROOT).as_posix(),
    'final_manifest_path':(RUN / 'review-manifest.json').relative_to(ROOT).as_posix()}
write('review.json', review)
acceptance = {'role':'reviewer','actor':ACTOR,'task':'IG-1D','summary':summary,
    'model':config['model'],'reasoning':config['reasoning'],'configuration_evidence':artifact(RUN / 'configuration-continuity.json'),
    'criteria':task['acceptance'],'artifacts':delivery['artifacts'],'checks':checks,
    'technical_result':'pass','technical_pass':True,'independent_pass':True,
    'reviewed_delivery':artifact(DELIVERY),'independent_review':artifact(RUN / 'review.json'),
    'full_report':artifact(RUN / 'report.md'),'review_manifest_path':(RUN / 'review-manifest.json').relative_to(ROOT).as_posix(),
    'final_seal_path':(RUN / 'final-seal.json').relative_to(ROOT).as_posix(),
    'failed_setup_attempts':{'count':2,'evidence':artifact(RUN / 'setup-attempts.json'),'all_preserved_separately':True},
    'all_original_findings_closed':True,'closed_findings':['IG1D-R01','IG1D-R02','IG1D-R03','IG1D-R04'],
    'measurement':measurement,'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False,
    'authority_scope':'Technical review only; coordinator owns queue acceptance/done. No human source-meaning decision.',
    'hash_closure_note':'Manifest includes this acceptance file, so it is linked by path here; final-seal pins manifest, review and acceptance exact hashes.'}
assert acceptance['artifacts'] == delivery['artifacts'] and acceptance['criteria'] == task['acceptance']
assert acceptance['actor'] != delivery['actor']
write('acceptance-evidence.json',acceptance)
# Exercise the real workflow gate against an in-memory queue copy only. Never
# invoke the CLI transition (which writes queue/projections).
compat_start = datetime.now(timezone.utc); compat_clock = time.perf_counter()
queue_hash_before = sha(ROOT / 'docs/work/queue.json')
spec = importlib.util.spec_from_file_location('review_workflow_gate', ROOT / 'scripts/workflow.py')
workflow = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = workflow
spec.loader.exec_module(workflow)
queue_copy = copy.deepcopy(queue)
workflow.transition(queue_copy, ROOT, 'IG-1D', 'accepted', (RUN / 'acceptance-evidence.json').relative_to(ROOT).as_posix())
assert next(t for t in queue_copy['tasks'] if t['id'] == 'IG-1D')['status'] == 'accepted'
assert sha(ROOT / 'docs/work/queue.json') == queue_hash_before
write('workflow-compatibility.json', {'command': 'finalize.py: workflow.transition(copy.deepcopy(queue), ROOT, IG-1D, accepted, acceptance-evidence.json); no CLI or disk queue write',
    'exit_code':0,'started_utc':compat_start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
    'wall_seconds':time.perf_counter()-compat_clock,'real_workflow_gate_passed':True,'queue_unchanged':True,
    'queue_sha256':queue_hash_before,'acceptance':artifact(RUN / 'acceptance-evidence.json')})
manifest_artifacts = [artifact(p) for p in sorted(RUN.rglob('*')) if p.is_file()]
write('review-manifest.json', {'format':'wgc-review-manifest-1','task':'IG-1D','actor':ACTOR,'technical_result':'pass',
    'artifacts':manifest_artifacts,'reviewed_delivery':artifact(DELIVERY),'reviewed_artifacts':delivery['artifacts'],
    'external_project_evidence':project_files,'preserved_version_evidence':artifact(RUN / 'verification-after.json'),
    'self_hash_policy':'Manifest excludes itself and final-seal; acceptance links manifest by path. final-seal pins all final outputs.'})
write('final-seal.json',{'format':'wgc-review-seal-1','actor':ACTOR,'utc':datetime.now(timezone.utc).isoformat(),'technical_result':'pass',
    'review':artifact(RUN / 'review.json'),'report':artifact(RUN / 'report.md'),'manifest':artifact(RUN / 'review-manifest.json'),
    'acceptance':artifact(RUN / 'acceptance-evidence.json'),'reviewed_artifact_manifest':artifact(RUN / 'reviewed-artifact-manifest.json')})
for a in manifest_artifacts + delivery['artifacts'] + project_files:
    assert sha(ROOT / a['path']) == a['sha256']
for a in read(RUN / 'final-seal.json').values():
    if isinstance(a,dict) and 'sha256' in a: assert sha(ROOT / a['path']) == a['sha256']
assert sha(ROOT / 'docs/work/queue.json') == after['queue_sha256']
print(json.dumps({'technical_result':'pass','review':artifact(RUN / 'review.json'),'report':artifact(RUN / 'report.md'),
    'manifest':artifact(RUN / 'review-manifest.json'),'acceptance':artifact(RUN / 'acceptance-evidence.json'),
    'seal':artifact(RUN / 'final-seal.json'),'artifact_count':len(manifest_artifacts),'final_hash_recheck':'pass'}))
