"""Freeze the completed independent review, without changing the real task state."""
from reviewer import *
import re

def main():
    index=read(REPAIR/'rereview-input-pins.json'); delivery=read(REPAIR/'delivery.json')
    queue=read(ROOT/'docs/work/queue.json'); task=next(t for t in queue['tasks'] if t['id']=='IG-2B02')
    assert task['status']=='review' and delivery['artifacts']==index['ordered_delivery_artifacts']
    checks=read(OUT/'required-checks.json')['checks']; assert len(checks)==5 and all(c['exit_code']==0 for c in checks)
    assert len(read(OUT/'region-review-ledger.json')['regions'])==141
    assert read(OUT/'locator-audit.json')['outcome']=='passed'
    delta=read(OUT/'component-delta-audit.json')
    assert delta['unchanged_138_exact'] and delta['seven_prior_overrides_exact']
    assert all(r['all_other_nested_row_fields_exact'] and r['effective_authority_match'] and r['visual_components_match'] and r['canonical_region_match'] for r in delta['regions'])
    assert all(r.get('matches_declared_delta',True) for r in delta['regions'])
    assert all(p['byte_identical'] for r in read(OUT/'replay-audit.json')['runs'] for p in r['products'])
    objects=[index,delivery,read(REPAIR/'delivery-manifest.json'),read(REPAIR/'final-seal.json'),read(PACKET/'manifest.json'),[pin(REPAIR/'independent-rereview-launch.txt'),pin(REPAIR/'final-seal.json')]]
    audit=check_pins(objects)
    assert not audit['errors'],audit['errors']
    expected_queue=read(OUT/'checkpoint.json')['queue']
    assert pin(ROOT/'docs/work/queue.json')==expected_queue
    audit.update(queue_unchanged=pin(ROOT/'docs/work/queue.json'),real_task_status=task['status'],ordered_delivery_artifacts_count=len(delivery['artifacts']),ordered_delivery_artifacts_exact=True,frozen_original_and_repair_byte_drift=False)
    write('final-byte-audit.json',audit)
    # Reobserve only own runtime configuration metadata. Never read other chats' logs.
    runtime=[]
    for line in RUNTIME.open(encoding='utf-8'):
        j=json.loads(line)
        if j['type']=='turn_context': runtime.append(dict(timestamp=j['timestamp'],model=j['payload'].get('model'),effort=j['payload'].get('effort')))
    assert runtime and all(r['model']=='gpt-6.1-sol' and r['effort']=='high' for r in runtime)
    write('configuration-reobservation.json',dict(session_id=SID,observed_utc=utc(),own_runtime_path=str(RUNTIME),turn_context_records=runtime,original_configuration=pin(OUT/'configuration.json'),model='gpt-6.1-sol',reasoning='high',requested_flags_are_not_proof=True))
    end=utc(); start='2026-10-15T12:33:55.587Z'
    measurement=dict(started_utc=start,ended_utc=end,wall_seconds=(datetime.fromisoformat(end)-datetime.fromisoformat(start.replace('Z','+00:00'))).total_seconds(),input_tokens=None,output_tokens=None,operator_seconds=None,monetary_cost=None,unavailable_reason='Reliable review-only usage/cost/operator time not exposed.')
    write('checkpoint-final.json',dict(task='IG-2B02',actor='codex-'+SID,session_id=SID,model='gpt-6.1-sol',reasoning='high',configuration=pin(OUT/'configuration.json'),configuration_reobservation=pin(OUT/'configuration-reobservation.json'),stage='completed_independent_rereview_changes_recommended',measurement=measurement,completed=['4375 ordered delivered artifacts independently hashed','All current reports/pins and all four pages/141 regions/17 diagrams reviewed','Both R01/R02 source corrections checked at all three distinct identities','423 primary artifacts and all nested canonical/source/order/coverage bytes rechecked','Complete nine-product metadata replay in two reviewer-owned outputs','All five required commands passed','Six wrong report bindings independently resolved and frozen as P2/R03'],unmet=['Clean current report traceability: R03'],queue=pin(ROOT/'docs/work/queue.json'),queue_status='review',queue_transition_performed=False,acceptance_granted=False,next_operation='Operator/coordinator decision on new bounded report-reference repair; no downstream work.'))
    project_log=(OUT/'project-check.stdout').read_text(encoding='utf-8')
    check_root=Path(re.search(r'^LOG_ROOT=(.*)$',project_log,re.M).group(1).strip())
    short=ROOT/'private/workflow/checks/rr8d-20261015T123502Z'
    check_files=[pin(p) for base in [check_root,short] for p in sorted(base.rglob('*')) if p.is_file()]
    write('fresh-check-output-index.json',dict(check_roots=[str(check_root),str(short)],files=check_files,count=len(check_files),policy='All actual fresh check files pinned, including synthetic test fixtures and logs. They are not primary game evidence and imply no gameplay correctness or semantic acceptance.'))
    excluded=['review-manifest.json','review.json','review-handoff.md','review-seal.json']
    own_files=[pin(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts and p.suffix!='.pyc']
    manifest=dict(format='wgc-independent-rereview-manifest-1',task='IG-2B02',actor='codex-'+SID,session_id=SID,created_utc=utc(),technical_result='changes_recommended',reviewed_delivery=pin(REPAIR/'delivery.json'),reviewed_manifest=pin(REPAIR/'delivery-manifest.json'),reviewed_final_seal=pin(REPAIR/'final-seal.json'),issued_instruction=pin(REPAIR/'independent-rereview-launch.txt'),input_index=pin(REPAIR/'rereview-input-pins.json'),packet=dict(manifest=pin(PACKET/'manifest.json'),context=pin(PACKET/'context.txt')),ordered_reviewed_artifact_count=len(delivery['artifacts']),reviewer_outputs=own_files,fresh_check_outputs=check_files,self_exclusion_policy='Manifest excludes itself, review.json, review-handoff.md and review-seal.json to avoid cycles; final seal pins all four except itself. __pycache__/*.pyc are incidental runtime caches, never review evidence. No post-freeze output files are permitted. Read-only seal verification prints its result in the session transcript.',source_scope='Pages 5-8 complete; only exact pinned page-4 Triarii crop for continuation. Page 9 not accessed; pages 10-44 geometry/count only. No archive, Git history, neighboring repository, online API, agent, new chat, messaging, automation, commit or push.',acceptance_granted=False)
    write('review-manifest.json',manifest)
    review=dict(role='reviewer',task='IG-2B02',actor='codex-'+SID,session_id=SID,attempt=OUT.relative_to(ROOT).as_posix(),model='gpt-6.1-sol',reasoning='high',configuration_evidence='Own runtime session_meta and turn_context, independently read in this new session; requested creation flags and earlier session proof are not used as confirmation.',configuration=pin(OUT/'configuration.json'),configuration_reobservation=pin(OUT/'configuration-reobservation.json'),summary='R01 and R02 component corrections are correct at all three distinct counters. Full independent 141-region rereview and byte/preservation/locator/replay checks completed. P2/R03 identifies six wrong current author-specification JSON pointers in affected-component-audit and finding-dispositions. Changes recommended; no task transition or acceptance.',technical_result='changes_recommended',criteria=task['acceptance'],criteria_results=read(OUT/'criteria-matrix.json')['criteria'],findings=read(OUT/'findings.json')['findings'],finding_ids=['IG-2B02-R03'],original_finding_rechecks=pin(OUT/'r01-r02-rechecks.json'),artifacts=delivery['artifacts'],reviewed_delivery=pin(REPAIR/'delivery.json'),reviewed_final_seal=pin(REPAIR/'final-seal.json'),reviewed_order_policy='artifacts equals the new real review event delivery.artifacts in complete original order, not the old original envelope. Reviewer outputs are separate.',review_outputs=own_files,review_manifest=pin(OUT/'review-manifest.json'),checks=checks,review_scope=dict(original_pages=[5,6,7,8],all_regions=141,all_grouped_diagrams=17,exact_changed_counter_regions=3,raw_primary_artifacts=423,task_denominator=141,full_denominator=307,context_denominator=0,prior_authored_preserved=130,placeholders_preserved=36,original_unchanged_locator_render_baseline_policy=read(OUT/'locator-audit.json')['baseline_risk_policy']),limitations=read(OUT/'reviewer-errors-and-limits.json')['limitations'],measurement=measurement,queue_observation=pin(ROOT/'docs/work/queue.json'),review_event=index['actual_review_event'],queue_transition_performed=False,acceptance_granted=False,semantic_decision=None,semantic_decision_null_reason='No human semantic decision requested or issued by this technical model review.',whole_record_source_IG_review='not established',approved_exclusion=False,executable_readiness='unverified',next_operation='Operator/coordinator decides on a new bounded R03 report-reference repair and fresh review of changed evidence. Leave IG-2B02 in review; do not start IG-2B03.')
    assert review['artifacts']==delivery['artifacts']==index['ordered_delivery_artifacts']
    write('review.json',review)
    handoff=f'''# IG-2B02 independent R01/R02 rereview

Result: **changes_recommended**. New finding **IG-2B02-R03 (P2)**.
Original R01 and R02 source component corrections are confirmed, including both
separate Thrace identities. No blocking source component defect was observed in the
current 141-region ledger. This is a complete independent rereview, not an executor
self-check or transfer of the old review result.

The current affected-component audit and finding dispositions each use specification
indices 5/24/28 for the three targets. Those pointers resolve to unrelated regions.
Correct indices in the pinned specification are 18/37/41. Six bindings are wrong in
total. The generator uses ledger enumeration order for specification pointers at
audit-and-report.py:99. Full reproducible cases, exact paths/lines/pins, consequence
and minimum verification are in findings.json and report-consistency-audit.json.
Repair source components, canonical objects, identities and raw evidence are correct
and must remain preserved in a new coordinator-authorized report repair attempt.

All four original pages, all 141 region boundary/crop pairs and all 17 enlarged grouped
diagrams were freshly inspected. Exact page-4 Triarii crop alone was viewed for the
continuation. Page 8 ends with a complete sentence; page 9 was not accessed. No other
page-1-4 content or page-10-44 content was analyzed. Existing locator/render audits
support only unchanged raw derivation risks after fresh equality checks; they do not
review changed metadata on this session's behalf.

All 4375 ordered delivery artifacts and frozen inputs rehash correctly. The complete
ordered list is retained in review.json.artifacts. All 423 primary files, all nested
canonical records and five canonical snapshots remain exact. Counts are 141 task /
307 full / 0 context, with 130 preserved authored regions and 36 placeholders. Both
fresh reviewer-owned nine-product metadata replays are byte-identical to the repair.
All current report pins verify. The preparation-time historical queue pin is separately
matched to the preserved coordinator queue-before.json; it is not a live-queue claim.

Criteria 1-4 meet this technical inventory/preservation scope. Criterion 5's independent
review has been performed completely, but clean delivery verification fails on R03.
See criteria-matrix.json for all five exact unchanged criteria and individual evidence.

Required checks all exited 0: unchanged tests/sources (71 passed), root inventory CLI
validation with original PDF reopened and strict-pypdf/Poppler 44-page structural checks,
workflow validate, scripts/check.ps1 -Task IG-2B02 (102 tests passed), git diff --check.
Fresh command logs record argv, stdout/stderr, UTC and elapsed wall time. The original
Xref warning and Git line-ending warnings are retained. No tool/test/contract edits.

Reviewer: codex-{SID}; own session {SID}.
Actual gpt-6.1-sol/high confirmed from own runtime metadata and reobserved before freeze.
Started {start}; review measurements ended {end}; wall {measurement['wall_seconds']:.3f}s.
Reliable review-only token/cost/operator-time measurements are unavailable (null).

Review pin: {json.dumps(pin(OUT/'review.json'))}
Manifest pin: {json.dumps(pin(OUT/'review-manifest.json'))}
Findings pin: {json.dumps(pin(OUT/'findings.json'))}
Criteria pin: {json.dumps(pin(OUT/'criteria-matrix.json'))}

The final review-seal.json pins this handoff, review, manifest, reports, scripts, replay
outputs and all fresh check evidence. Only the seal itself is self-excluded; incidental
Python bytecode caches are not review evidence. No post-freeze writes are authorized.

The real task remains **review**. No queue/projection change, acceptance, done, human
semantic acceptance, whole-record source-IG approval, exclusion approval or executable
readiness was granted. No downstream task was started. Next: operator/coordinator
decision on the bounded R03 report-reference finding. Stop here.
'''
    (OUT/'review-handoff.md').write_text(handoff,encoding='utf-8')
    final_outputs=own_files+[pin(OUT/n) for n in ['review-manifest.json','review.json','review-handoff.md']]
    seal=dict(format='wgc-independent-rereview-seal-1',task='IG-2B02',actor='codex-'+SID,session_id=SID,model='gpt-6.1-sol',reasoning='high',sealed_utc=utc(),technical_result='changes_recommended',findings=['IG-2B02-R03'],original_findings_rechecked=['IG-2B02-R01','IG-2B02-R02'],review=pin(OUT/'review.json'),manifest=pin(OUT/'review-manifest.json'),handoff=pin(OUT/'review-handoff.md'),criteria=pin(OUT/'criteria-matrix.json'),configuration=pin(OUT/'configuration.json'),configuration_reobservation=pin(OUT/'configuration-reobservation.json'),reviewer_outputs=final_outputs,fresh_check_outputs=check_files,ordered_delivery_artifact_count=4375,all_frozen_input_pins_verified=pin(OUT/'final-byte-audit.json'),queue_status='review',queue_pin=pin(ROOT/'docs/work/queue.json'),queue_transition_performed=False,acceptance_granted=False,semantic_acceptance_granted=False,whole_record_source_IG_review='not established',executable_readiness='unverified',downstream_work_started=False,measurement=measurement,self_exclusion_policy='This seal excludes its own hash to avoid a cycle; its final SHA256 is returned in the review session transcript. Every substantive reviewer output, including the manifest/review/handoff, and all fresh check outputs are pinned. Incidental __pycache__/*.pyc are not review evidence. No post-freeze output files allowed.',seal_command=[sys.executable,'-B',str(OUT/'freeze.py')],stop=True)
    write('review-seal.json',seal)
    verification=check_pins([seal])
    assert not verification['errors'],verification['errors']
    assert read(OUT/'review.json')['artifacts']==read(REPAIR/'delivery.json')['artifacts']
    print(json.dumps(dict(outcome='frozen_and_read_only_verified',technical_result=review['technical_result'],finding_ids=['IG-2B02-R03'],review=pin(OUT/'review.json'),handoff=pin(OUT/'review-handoff.md'),manifest=pin(OUT/'review-manifest.json'),seal=pin(OUT/'review-seal.json'),reviewer_output_count=len(final_outputs),fresh_check_file_count=len(check_files),seal_pin_count=verification['unique_pin_count'],queue_status=task['status'],queue_unchanged=True,acceptance_granted=False),indent=2))
if __name__=='__main__':main()
