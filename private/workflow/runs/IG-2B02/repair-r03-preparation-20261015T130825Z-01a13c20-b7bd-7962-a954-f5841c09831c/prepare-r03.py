"""Prepare R03 instructions and a queue proposal only. Never repair or transition."""
import copy, hashlib, importlib.util, json, time
from datetime import datetime, timezone
from pathlib import Path

R=Path('C:/repo/wargame-compiler'); P=Path(__file__).resolve().parent
D=R/'private/workflow/runs/IG-2B02/inventory-20261014T201344Z-reserved-by-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'
B=R/'private/workflow/runs/IG-2B02/repair-r01-r02-20261015T091559Z-reserved-by-01a13c20-b7bd-7962-a954-f5841c09831c'
V=R/'private/workflow/runs/IG-2B02/rereview-20261015T123502Z-01a13f8d-fa1f-7991-92c2-0c64bfe3a157'
A=R/'private/workflow/runs/IG-2B02/repair-r03-20261015T130825Z-reserved-by-01a13c20-b7bd-7962-a954-f5841c09831c'
INDEX='docs/work/repair-context/IG-2B02-R03-20261015T130825Z.json'
def now(): return datetime.now(timezone.utc).isoformat()
def rel(path): return path.relative_to(R).as_posix()
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()
def pin(path): return dict(path=rel(path),bytes=path.stat().st_size,sha256=sha(path))
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as stream: json.dump(value,stream,indent=2,ensure_ascii=False); stream.write('\n')

started=now(); clock=time.monotonic(); assert not A.exists()
q=read(R/'docs/work/queue.json'); task=next(t for t in q['tasks'] if t['id']=='IG-2B02')
assert task['status']=='review' and len(task['events'])==6
assert sha(R/'docs/work/queue.json')=='99e272c17c3549f49986df241327e21c66ee979c034043c7e2544aa81ebcd2f2'
assert sha(B/'final-seal.json')=='e8a6dafff6de73761a7422d8a6fe6ad161320d8bcdbddc85ab4f5be67ac8b598'
assert sha(V/'review-seal.json')=='d7c2b08bba2279ce34dabca6192db2935fdb608be93abd1303e5dcf98f300de0'
with (P/'queue-before-preparation.json').open('xb') as stream: stream.write((R/'docs/work/queue.json').read_bytes())
spec=importlib.util.spec_from_file_location('workflow',R/'scripts/workflow.py'); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w); w.validate(q,R)
seen={}
def visit(obj):
    if isinstance(obj,dict):
        if all(k in obj for k in ('path','bytes','sha256')) and isinstance(obj['sha256'],str):
            row=dict(path=obj['path'],bytes=obj['bytes'],sha256=obj['sha256']); assert seen.setdefault(row['path'],row)==row,row['path']
        for value in obj.values(): visit(value)
    elif isinstance(obj,list):
        for value in obj: visit(value)
for base,names in [(B,['final-seal.json','delivery.json','delivery-manifest.json','rereview-input-pins.json']),(V,['review-seal.json','review.json','review-manifest.json','findings.json','criteria-matrix.json'])]:
    for name in names: visit(read(base/name)); seen[rel(base/name)]=pin(base/name)
mutable=set(w.views(q))|{'docs/work/queue.json'}; controls=[]; frozen=[]
for path,row in sorted(seen.items()):
    target=Path(path); target=target if target.is_absolute() else R/target
    assert target.is_file() and target.stat().st_size==row['bytes'] and sha(target)==row['sha256'],path
    (controls if path in mutable else frozen).append(row)
write(P/'frozen-base-pins.json',dict(task='IG-2B02',purpose='Exact immutable original delivery, R01/R02 repair and completed independent R03 review inputs. Current mutable queue/projections are separate control observations, not future frozen files.',frozen_pins=frozen,mutable_control_observations=controls,self_exclusion='Catalogue excludes itself; its exact pin is issued separately.'))
write(P/'frozen-base-verification-before.json',dict(outcome='passed_bytes_only',verified_utc=now(),unique_frozen_refs=len(frozen),current_mutable_control_pins_verified=len(controls),catalogue=pin(P/'frozen-base-pins.json'),meaning_review_performed=False,repair_performed=False))
metadata=Path('C:/Users/yauta/.codex/sessions/2026/10/14/rollout-2026-10-14T22-35-39-01a13c20-b7bd-7962-a954-f5841c09831c.jsonl'); own=None; turn=None
with metadata.open('r',encoding='utf-8') as stream:
    for number,line in enumerate(stream,1):
        if '"session_meta"' not in line[:180] and '"turn_context"' not in line[:180]: continue
        record=json.loads(line); data=record.get('payload',{}); row=dict(line=number,raw_record_sha256=hashlib.sha256(line.encode('utf-8')).hexdigest())
        if record.get('type')=='session_meta': own=dict(row,**{k:data.get(k) for k in ('id','cwd','source','model_provider')})
        if record.get('type')=='turn_context': turn=dict(row,**{k:data.get(k) for k in ('model','effort','cwd')})
assert own and own['id']=='01a13c20-b7bd-7962-a954-f5841c09831c' and turn
write(P/'configuration.json',dict(role='instruction_preparer',actor='codex-'+own['id'],actual_model=turn['model'],actual_reasoning=turn['effort'],observed_utc=now(),source=str(metadata),scope='Own identity/configuration session_meta and turn_context fields only; no conversation history.',session_record=own,turn_record=turn,future_executor_configuration=None,future_reason='Future executor session is not created and must confirm its own runtime model/reasoning.'))
findings=read(V/'findings.json'); finding=findings['findings'][0]; assert finding['id']=='IG-2B02-R03' and findings['technical_result']=='changes_recommended'
specifications=read(B/'author-specifications-final.json')['specifications']; bykey={}
for index,row in enumerate(specifications):
    assert row['key'] not in bykey; bykey[row['key']]=(index,row)
targets=[]
for case in finding['cases']:
    index,row=bykey[case['key']]; assert case['expected_pointer']==f'/specifications/{index}/components' and row['components']==case['expected_components']
    targets.append(dict(case,specification_index_derived_by_exact_key=index))
assert [t['specification_index_derived_by_exact_key'] for t in targets]==[18,37,41]
scope=dict(format='wgc-r03-report-reference-repair-scope-1',task='IG-2B02',finding_id='IG-2B02-R03',severity='P2',status='prepared_only',repair_attempt=rel(A),repair_attempt_must_be_absent=True,reviewed_repair_base=rel(B),independent_review=rel(V),finding_pin=pin(V/'findings.json'),targets=targets,root_cause=finding['root_cause'],affected_reports=finding['artifacts'],unchanged_current_product_pins={name:pin(B/name) for name in ['authored/inventory.json','authored/identity-registry.json','final-verified/inventory.json','final-verified/identity-registry.json','final-verified/coverage.json','author-specifications-final.json','component-observations.json','region-ledger-final.json','visual-inspection.json']},allowed_domain_delta='Only six specification-pointer string corrections in new full copies of two reports, plus replacement report generator and necessary separately audited provenance/current report claims/pins/checks/delivery/review handoff. All component/canonical/source/evidence files stay byte-identical at existing immutable base paths. No product duplication or regeneration.',expected_binding_count=24,expected_corrected_binding_count=6,expected_unchanged_binding_count=18,executor_source_content_access='None needed/authorized for R03 report repair. JSON metadata and byte hashing only; unchanged root validator may reopen PDF for structural count/geometry without new substantive content extraction.',criteria=task['acceptance'],future_packet=None,future_packet_reason='Authorized coordinator must change exact task scope and record review -> changes_requested, then issue actual fresh packet/handoff; preparation is not claim readiness.',future_repair_hashes=None,future_hashes_reason='Repair has not run; no future delivery hash or reviewer identity/result may be fabricated.')
write(P/'repair-scope.json',scope)
write(R/INDEX,dict(task='IG-2B02',purpose='Workflow metadata only: R03 bounded report-reference repair. No publisher content.',scope=pin(P/'repair-scope.json'),findings=pin(V/'findings.json'),review_seal=pin(V/'review-seal.json'),repair_base_seal=pin(B/'final-seal.json'),reserved_repair_attempt=rel(A),gate='Preparation only; authorized coordinator must apply exact new scope and record changes_requested before a new actual-configuration-confirmed executor claims.'))
new_context=[INDEX if path=='docs/work/repair-context/IG-2B02-R01-R02-20261015T091559Z.json' else path for path in task['context']]
updates=dict(write_scope=[rel(A)+'/', 'private/workflow/packets/','private/workflow/checks/'],outputs=[rel(A)+'/affected-component-audit.json and finding-dispositions.json (new complete reports; exact six corrected specification pointers; preserved source observations and explicit provenance)',rel(A)+'/report-reference-repair.py, binding-resolution-audit.json (all 24 bindings), negative-controls.json, r03-disposition.json, delta-audit.json, preservation-report.json, report-consistency-audit.json and replay-report.json',rel(A)+'/configuration.json, toolchain.json, checkpoint.json, criteria.json, required-checks.json, delivery-manifest.json, delivery.json, delivery-handoff.md and final-seal.json',rel(A)+'/independent-rereview-launch.txt and rereview-input-pins.json (actual future hashes after successful review event; operator starts independent reviewer separately)','Existing immutable R01/R02 canonical/component product files remain unchanged current targets by exact base path/hash; no new inventory or evidence generation.'],context=new_context,inputs=[f'Current immutable R01/R02 repair: {rel(B)}/delivery.json SHA256 {sha(B/"delivery.json")}; complete manifest/seal, current component files and all prior evidence remain unchanged.',f'Completed independent changes_recommended review: {rel(V)}/review.json SHA256 {sha(V/"review.json")}; findings.json contains R03 only and confirms original R01/R02 source corrections.',f'Bounded R03 report-reference scope: {rel(P)}/repair-scope.json SHA256 {sha(P/"repair-scope.json")}; three exact keys, six wrong pointers, 24 bindings; derive specification indices by unique key, never ledger position.',f'Complete immutable input catalogue: {rel(P)}/frozen-base-pins.json SHA256 {sha(P/"frozen-base-pins.json")}; old historical snapshots are not current mutable queue claims.','All original source, accepted dependency, provenance, geometry, identity, evidence, order, continuation and coverage contracts remain exact; 141 task / 307 full / zero context denominator. No new source-content analysis for report repair.'],start_conditions=['IG-2A/IG-2B01 remain done. Authorized coordinator applies only prepared R03 task fields and records review -> changes_requested with exact current R03 review evidence.','New local executor confirms its own actual gpt-6.1-sol/high and new identity, exact fresh packet/handoff and absent exclusively owned repair directory before claim.','All existing original/R01-R02 repair/review files are immutable. Existing corrected canonical/component products remain exact current targets at old paths; only report references and necessary dependent operational evidence change.'],exclusions=task['exclusions']+['R03 execution is report-reference repair only. No new source-content viewing/render/extraction or component edits, no product copies/regeneration, and no write to any old delivery/review/preparation directory. Full independent rereview retains original criterion-5 source scope later.'])
patch=dict(mode='proposal_only_not_applied',task='IG-2B02',expected_queue=pin(R/'docs/work/queue.json'),expected_task_status='review',expected_event=task['events'][-1],task_field_updates=updates,preserve_fields=[key for key in task if key not in updates],context_index=pin(R/INDEX),status_policy='Do not directly edit status/events. A separately authorized coordinator applies exact fields, renders/checks, then workflow transition review -> changes_requested with real coordinator evidence.',authorization='Current user requested preparation only. No queue edit, repair execution, session creation or acceptance performed.')
write(P/'coordinator-queue-patch.json',patch)
draft=copy.deepcopy(q); d=next(t for t in draft['tasks'] if t['id']=='IG-2B02'); d.update(copy.deepcopy(updates)); w.validate(draft,R,check_views=False)
def estimate(status):
    candidate=copy.deepcopy(draft); selected=next(t for t in candidate['tasks'] if t['id']=='IG-2B02'); selected['status']=status; views=w.views(candidate)
    paths=list(dict.fromkeys(w.BASE_CONTEXT+['docs/work/tasks/IG-2B02.md']+selected['context'])); sections=[]
    for path in paths:
        assert w.permitted(R,path)
        target=R/path
        if target.suffix.lower() in {'.md','.json','.py','.ps1','.toml'}: sections.append('\n--- FILE: '+path+' ---\n'+(views[path] if path in views else target.read_text(encoding='utf-8-sig')))
    return len('\n'.join(sections).encode('utf-8'))
estimates={status:estimate(status) for status in ('review','changes_requested','in_progress')}; assert max(estimates.values())<100000
write(P/'proposal-validation.json',dict(outcome='passed_draft_only',selected_patch=pin(P/'coordinator-queue-patch.json'),context_policy_unchanged=True,packet_logical_byte_estimates=estimates,limit=100000,note='Projection sizing only; no synthetic event created or persisted. Actual future packet/handoff hashes remain unavailable.',queue_written=False,status_changed=False,session_created=False))
write(P/'preparation.json',dict(task='IG-2B02',finding='IG-2B02-R03',purpose='Complete repair instruction preparation only',started_utc=started,recorded_utc=now(),wall_seconds=time.monotonic()-clock,actor='codex-01a13c20-b7bd-7962-a954-f5841c09831c',queue_snapshot=pin(R/'docs/work/queue.json'),saved_queue_snapshot=pin(P/'queue-before-preparation.json'),review_event=task['events'][-1],event_count=len(task['events']),reserved_absent_repair_attempt=rel(A),directories=dict(original_delivery=rel(D),reviewed_repair=rel(B),latest_independent_review=rel(V),preparation=rel(P)),context_index=pin(R/INDEX),catalogue=pin(P/'frozen-base-pins.json'),unchanged_acceptance=task['acceptance'],queue_changed=False,repair_performed=False,session_created=False,acceptance_granted=False))
assert pin(R/'docs/work/queue.json')==patch['expected_queue'] and not A.exists()
print(json.dumps(dict(outcome='prepared_scope_and_exact_queue_proposal_only',unique_frozen_refs=len(frozen),mutable_controls=len(controls),draft_packet_bytes=estimates,scope=pin(P/'repair-scope.json'),patch=pin(P/'coordinator-queue-patch.json'),context_index=pin(R/INDEX),repair_attempt_absent=True),indent=2),flush=True)
