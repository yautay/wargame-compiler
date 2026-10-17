"""Freeze complete IG-1E technical review and exact-delivery acceptance evidence."""
import copy,hashlib,importlib.util,json,re,sys,time
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5];RUN=Path(__file__).resolve().parent
STAGE=ROOT/'private/workflow/runs/IG-1E/stage-20261013'
ACTOR='ig1e-independent-reviewer-20261013T150750Z'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def artifact(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def write(n,d):
    with (RUN/n).open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')

before,after=read(RUN/'verification-before.json'),read(RUN/'verification-after.json')
assert before['all_match'] and after['all_match'] and before['delivery']==after['delivery']
assert before['queue_sha256']==after['queue_sha256']==sha(ROOT/'docs/work/queue.json')
delivery=read(STAGE/'delivery.json');queue=read(ROOT/'docs/work/queue.json')
task=next(t for t in queue['tasks'] if t['id']=='IG-1E')
assert task['status']=='review' and task['acceptance']==delivery['criteria']
assert sha(STAGE/'delivery.json')=='5a2d7595085ef19877f921da96ea79647493ed73a813b5ce29b36d80b4f60e54'
audit=read(RUN/'independent-accounting.json');supp=read(RUN/'supplemental-accounting.json');seal=read(RUN/'independent-seal.json')
assert audit['result']==supp['result']==seal['result']=='pass'
checks=[read(p) for p in sorted(RUN.glob('*-check.json'))]
assert {p.name for p in RUN.glob('*-check.json')}=={n+'-check.json' for n in ['accounting','explicit','project','supplemental','seal','diff']}
assert all(c['command'] and c['exit_code']==0 for c in checks)
write('checks.json',checks)
config_path=ROOT/read(RUN/'checkpoint.json')['configuration_evidence']['path']
config=read(config_path);assert config['model']=='gpt-6.1-sol' and config['reasoning']=='high'
write('configuration-continuity.json',{'model':config['model'],'reasoning':config['reasoning'],'requested_model':'gpt-6.1-sol','requested_reasoning':'high',
    'same_reviewer_chat_continuity':True,'actor':ACTOR,'original_direct_confirmation':artifact(config_path),
    'confirmation_source':config['configuration_evidence'],'note':'Same reviewer chat directly confirmed by operator earlier. Executor and previous unavailable reviewer confirmation are not used as proof.'})
write('findings.json',[])
criteria=[
    {'criterion':task['acceptance'][0],'result':'pass','evidence':'Complete unique manifest/import/ledger path-set equality, exact raw bytes and full independently enumerated entities/fields/unknown roots/binding subtrees; independent processed/raw/error classification and two new complete imports equal accepted bytes. Entire delivered ledger matches independently generated ledger; direct representative mappings checked privately.'},
    {'criterion':task['acceptance'][1],'result':'pass','evidence':'Two independently reconstructed and physically published seals equal all frozen snapshot bytes. Directory/manifest identity, every file hash, retained exact draft lineage, original selected revisions and gap/readiness assessments independently verified. Structural seal has no semantic, source-coverage or executable acceptance.'},
    {'criterion':task['acceptance'][2],'result':'pass','evidence':'Every missing configured path and all edition/source/version claims independently compared with raw import/manifest; selected source identity to missing original and profile edition compatibility remain unknown. Full subsequent reconciliation and human review prerequisites are explicit.'}]
write('criteria.json',criteria)
write('dispositions.json',{'technical_result':'pass','actor':ACTOR,'criteria':criteria,'remaining_findings':[],'new_finding_ids':[],
    'repair_cycles_used':0,'maximum_repair_cycles_per_finding':2,'product_modified_by_reviewer':False})
write('reviewed-artifact-manifest.json',{'format':'wgc-reviewed-artifacts-1','task':'IG-1E','actor':ACTOR,
    'delivery':artifact(STAGE/'delivery.json'),'artifact_count':50,'artifacts':delivery['artifacts'],
    'before':artifact(RUN/'verification-before.json'),'after':artifact(RUN/'verification-after.json'),'all_exact_bytes_preserved':True})
end=datetime.now(timezone.utc);start=read(RUN/'checkpoint.json')['started_utc']
measurement={'started_utc':start,'ended_utc':end.isoformat(),'wall_seconds':(end-datetime.fromisoformat(start)).total_seconds(),
    'scope':'Fresh evidence run; earlier instruction reading unmeasured and excluded. Individual checks, full accounting and seal operations have actual UTC and monotonic wall measurements.',
    'input_tokens':None,'output_tokens':None,'tokens':None,'cost':None,'operator_seconds':None,'unknown_reason':'Usage/cost/operator time unavailable.'}
write('measurement.json',measurement)
project_root=Path(re.search(r'LOG_ROOT=(.+)',(RUN/'project.log').read_text()).group(1).strip())
project_files=[artifact(p) for p in sorted(project_root.rglob('*')) if p.is_file() and p.suffix in ['.json','.log']]
write('project-evidence.json',{'artifacts':project_files,'check':artifact(RUN/'project-check.json')})
summary='Independent technical PASS of exact IG-1E full-input structural acceptance delivery. Entire raw/file/record/field/unknown/binding ledger, two actual fresh imports/transforms/publications and two independently reconstructed actual seals verified. No findings. Coordinator acceptance/done pending; no semantic, publisher-coverage or executable approval.'
report=f'''# IG-1E independent technical review

Result: **technical PASS**, with no findings or repair requested. All three exact task criteria are met within full-input structural import/snapshot scope. Workflow-compatible acceptance-evidence.json pins exactly the 50 delivery artifacts and exact queue criteria. The coordinator owns any subsequent acceptance/done transition; this review does not change queue or product.

Reviewer `{ACTOR}` is distinct from executor `{delivery['actor']}`. This is the continuing replacement reviewer chat directly confirmed by the operator as GPT-6.1 Sol / high. Configuration continuity links the original unchanged confirmation (`potwierdzam`); executor settings and the unavailable previous reviewer's confirmation are not used as proof. Token usage, cost and operator time are null.

Frozen delivery: `private/workflow/runs/IG-1E/stage-20261013/delivery.json`, SHA256 `5a2d7595085ef19877f921da96ea79647493ed73a813b5ce29b36d80b4f60e54`, exactly 50 artifacts. Every artifact matched before and after review. Also verified 233 accepted foundation artifacts, all 22 input pins and all 58 artifacts of the finalized IG-1D review. Queue SHA256 stayed `{after['queue_sha256']}`: IG-1A/B/C/D done, IG-1E review. Current packet is recorded in verification evidence; the earlier executor readiness packet is preserved, with legitimately changed coordinator status projections not mistaken for source divergence.

Validation: 106 integration/adapter/export tests passed, required scripts/check.ps1 -Task IG-1E passed 102 project tests plus queue/DAG/projection/dry-run checks, and git diff --check passed. Full independent accounting, supplemental reference/unknown oracle and independent seal checks all exited 0. Exact commands/argv, process-local PYTHONPATH, UTC and elapsed wall times are in checks.json and logs. All basetemp/TEMP destinations were fresh and cacheprovider disabled. Native Windows no-follow execution used the previously justified narrow local scope without weakening assertions, reinstalling dependencies or changing global configuration. There were no failed setup or product check attempts in this IG-1E review.

The public invented integration tests exercise real snapshot/import/export with independently known processed/raw/error counts, exact binary and malformed bytes, raw metadata, nested escaped unknown keys, identity ambiguity, unresolved scopes, missing-source gaps, mixed-edition claims and repeat import/publication. Their structural sealing control retains all gaps/history/assessments and refuses to equate sealing with semantic or gameplay approval. Accepted source/adapter/schema/test bytes remain unchanged.

Independent raw inventory measured {audit['manifest_entries']} unique manifest entries, {audit['available_files']} available and {audit['missing_sources']} missing. Record classification is {audit['independent_record_status_counts']}; {audit['independent_record_count']:,} entities and {audit['independent_field_count']:,} YAML field/container locations are retained. The independently authored field contract enumerates {audit['independent_unknown_root_count']} unknown roots and {audit['independent_unknown_location_count']:,} distinct unknown subtree locations. Every exact raw hash/base64 payload, record value/parent, YAML mark/container coordinate, identity observation and {audit['binding_count']:,} binding subtrees is checked. The accepted draft has {audit['source_graph_records']:,} graph records and {supp['identity_count']:,} identities. All aspect/record hashes and active/historical typed references are independently closed.

The supplemental oracle independently reconstructs {supp['independent_reference_diagnostic_count']:,} diagnostic target/candidate sets ({supp['reference_status_counts']['resolved']:,} resolved and {supp['reference_status_counts']['unresolved']} unresolved) and cycles from raw declarations/current identity aliases, using separate mutual-reachability SCC calculations. Importer/executor counters are cross-checks, never the inventory denominator. Complete delivered file/record/field/binding/unknown ledgers are compared for equality against the independent ledger, not just totals. Six direct actual mapping samples span rule, step, term, terminology, relation and auxiliary kinds; raw value hashes, parent coordinates, allocated IDs/origin keys and exact target bindings are recorded privately in mapping-samples.json.

Two actual new complete imports match each other and exact accepted IG-1C import bytes. A fresh seeded full transform matches all accepted IG-1D canonical files; a second full persisted-state transform matches the first. Two real publications in this review run are byte-identical with distinct actual operational sidecars. The copied extended oracle retains all 69 original Assert ASTs exactly; only RUN output destination, operational actor and large-array stdout filtering changed. All arrays remain in the saved ledger, with no assertion removal.

Snapshot: `private/ig/projects/spqr/snapshots/sha256-4571340270f16519ee8207f0e474e6e71620ae11d74a1c787f273bb617a34fa7/`, manifest SHA256 `8c3da679b4cc3f5b08bf0f9ad4db633bf7ff037bceb96bb41be4f310577ba6b4`. Independently recomputed dedicated manifest content-addressed identity, canonical bytes, exact directory tree, every file size/hash and all raw-import-registry-reference-ledger closures. Source snapshot ID derives from sealed data; its exact historical lineage points to the preserved draft snapshot. Every original graph record and originally selected revision, conflict/gap, profile and readiness assessment remains unchanged, with precisely one additional sealed snapshot record ({seal['sealed_graph_record_count']:,} total). The snapshot state is sealed while source coverage remains not_verified, semantic approval not_granted and executable readiness blocked.

The reviewer independently reconstructs the sealed record/revision and packaging manifest without executing the executor's seal helper. Two separate actual exclusive publications under this new review run equal every frozen snapshot file byte-for-byte, including import, full coverage ledger, registry, references, source IG and manifest. Actual seal operation times/configuration live in distinct sidecars; canonical run/model/timestamps remain null. This verifies actual repeatability beyond reported booleans.

All {len(seal['missing_source_paths'])} missing configured paths and all {seal['edition_source_claim_count']} source/edition/version claim records are independently compared to raw import/manifest. The selected 5E source's identity to the unavailable WGU original stays unknown, and mixed-edition compatibility/precedence stays unknown. Original claims remain unaltered. Explicit next prerequisites cover complete selected-source inventory, missing material recovery/identity, exact KB/source reconciliation including tables/procedures, reference scope resolution, discrepancies and authorized human review of exact semantic revisions.

Measured fresh evidence run: {measurement['started_utc']} to {measurement['ended_utc']}, {measurement['wall_seconds']:.3f} seconds. Full accounting measured {audit['wall_seconds']:.3f} seconds; complete independent seal/closure run measured {seal['wall_seconds']:.3f} seconds. Earlier instruction reading was unmeasured and excluded.

Remaining gates: coordinator verifies exact frozen review/manifest/acceptance pins, records IG-1E accepted then done and prepares the separate full-stage closure handoff. Publisher-source coverage, human semantic/source-meaning acceptance and executable readiness are separate, ungranted gates. No IG-2/compiler/runtime/POC, gameplay legality decision, neighbouring repository/archive/Git history access, new chat/agent/worktree/automation, commit/push or message to another chat was performed. review-manifest.json includes acceptance-evidence.json; final-seal.json pins final outputs without circular hashes.
'''
with (RUN/'report.md').open('x',encoding='utf-8') as f:f.write(report)
evidence=[artifact(p) for p in sorted(RUN.rglob('*')) if p.is_file()]
review={'role':'reviewer','actor':ACTOR,'executor_actor':delivery['actor'],'task':'IG-1E','summary':summary,
    'technical_result':'pass','technical_pass':True,'independent_pass':True,'review_finalized':True,
    'model':config['model'],'reasoning':config['reasoning'],'requested_model':'gpt-6.1-sol','requested_reasoning':'high',
    'configuration_evidence':artifact(RUN/'configuration-continuity.json'),'same_reviewer_chat_continuity':True,
    'reviewed_delivery':{**artifact(STAGE/'delivery.json'),'artifact_count':50,'artifacts':delivery['artifacts']},
    'criteria':task['acceptance'],'criteria_results':criteria,'findings':[],'remaining_findings':[],'new_finding_ids':[],
    'defect_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'checks':checks,'failed_setup_attempts':[],
    'artifacts':evidence,'current_packet':after['packet'],'queue_sha256_before':before['queue_sha256'],'queue_sha256_after':after['queue_sha256'],
    'before_verification':artifact(RUN/'verification-before.json'),'after_verification':artifact(RUN/'verification-after.json'),
    'all_exact_bytes_preserved':True,'accepted_foundation_count':233,'task_input_pin_count':22,
    'independent_accounting':{k:v for k,v in audit.items() if k not in ['ledger','binding_ledger','unknown_locations','publications','independent_unknown_roots','independent_unknown_field_locations']},
    'supplemental_accounting':{k:v for k,v in supp.items() if k not in ['unknown_roots','diagnostics','cycles']},
    'independent_seal':seal,'measurement':measurement,'product_modified_by_reviewer':False,'queue_modified_by_reviewer':False,
    'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False,
    'remaining_gates':['Coordinator exact-hash acceptance/done and separate stage closure handoff','Separate publisher coverage, human semantic acceptance and executable readiness'],
    'final_manifest_path':(RUN/'review-manifest.json').relative_to(ROOT).as_posix(),
    'acceptance_evidence_path':(RUN/'acceptance-evidence.json').relative_to(ROOT).as_posix()}
write('review.json',review)
acceptance={'role':'reviewer','actor':ACTOR,'task':'IG-1E','summary':summary,'model':config['model'],'reasoning':config['reasoning'],
    'configuration_evidence':artifact(RUN/'configuration-continuity.json'),'criteria':task['acceptance'],'artifacts':delivery['artifacts'],'checks':checks,
    'technical_result':'pass','technical_pass':True,'independent_pass':True,'reviewed_delivery':artifact(STAGE/'delivery.json'),
    'independent_review':artifact(RUN/'review.json'),'full_report':artifact(RUN/'report.md'),
    'review_manifest_path':(RUN/'review-manifest.json').relative_to(ROOT).as_posix(),'final_seal_path':(RUN/'final-seal.json').relative_to(ROOT).as_posix(),
    'failed_setup_attempts':[],'measurement':measurement,'semantic_acceptance_granted':False,'publisher_source_coverage_granted':False,'executable_readiness_granted':False,
    'authority_scope':'Technical review only; coordinator owns queue acceptance/done. No human meaning decision.',
    'hash_closure_note':'Manifest includes this acceptance file; linked by path to avoid circular hashes. final-seal pins exact manifest/review/acceptance hashes.'}
assert acceptance['artifacts']==delivery['artifacts'] and acceptance['criteria']==task['acceptance'] and acceptance['actor']!=delivery['actor']
write('acceptance-evidence.json',acceptance)
compat_start=datetime.now(timezone.utc);compat_tick=time.perf_counter();qhash=sha(ROOT/'docs/work/queue.json')
spec=importlib.util.spec_from_file_location('ig1e_review_workflow',ROOT/'scripts/workflow.py');workflow=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=workflow;spec.loader.exec_module(workflow)
qc=copy.deepcopy(queue);workflow.transition(qc,ROOT,'IG-1E','accepted',(RUN/'acceptance-evidence.json').relative_to(ROOT).as_posix())
assert next(t for t in qc['tasks'] if t['id']=='IG-1E')['status']=='accepted' and sha(ROOT/'docs/work/queue.json')==qhash
write('workflow-compatibility.json',{'command':'finalize.py: workflow.transition on deepcopy(queue) only; no CLI or disk queue write','exit_code':0,
    'started_utc':compat_start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.perf_counter()-compat_tick,
    'real_workflow_gate_passed':True,'queue_unchanged':True,'queue_sha256':qhash,'acceptance':artifact(RUN/'acceptance-evidence.json')})
manifest_artifacts=[artifact(p) for p in sorted(RUN.rglob('*')) if p.is_file()]
write('review-manifest.json',{'format':'wgc-review-manifest-1','task':'IG-1E','actor':ACTOR,'technical_result':'pass',
    'artifacts':manifest_artifacts,'reviewed_delivery':artifact(STAGE/'delivery.json'),'reviewed_artifacts':delivery['artifacts'],
    'external_project_evidence':project_files,'self_hash_policy':'Manifest excludes itself and final-seal; final-seal pins every final output.'})
write('final-seal.json',{'format':'wgc-review-seal-1','actor':ACTOR,'utc':datetime.now(timezone.utc).isoformat(),'technical_result':'pass',
    'review':artifact(RUN/'review.json'),'report':artifact(RUN/'report.md'),'manifest':artifact(RUN/'review-manifest.json'),
    'acceptance':artifact(RUN/'acceptance-evidence.json'),'reviewed_artifact_manifest':artifact(RUN/'reviewed-artifact-manifest.json')})
for a in manifest_artifacts+delivery['artifacts']+project_files:assert sha(ROOT/a['path'])==a['sha256']
for a in read(RUN/'final-seal.json').values():
    if isinstance(a,dict) and 'sha256' in a:assert sha(ROOT/a['path'])==a['sha256']
assert sha(ROOT/'docs/work/queue.json')==qhash
print(json.dumps({'technical_result':'pass','review':artifact(RUN/'review.json'),'report':artifact(RUN/'report.md'),
    'manifest':artifact(RUN/'review-manifest.json'),'acceptance':artifact(RUN/'acceptance-evidence.json'),
    'seal':artifact(RUN/'final-seal.json'),'artifact_count':len(manifest_artifacts),'final_hash_recheck':'pass'}))
