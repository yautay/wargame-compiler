import datetime, json
from verify import ROOT, OUT, BASE, SESSION, CONFIG, META, load, save, sha, verify

task=load(SESSION/'task.json')
delivery=load(BASE/'delivery.json')
ledger=load(BASE/'region-ledger.json')
components=load(BASE/'component-ledger.json')
geometry=load(OUT.relative_to(ROOT)/'geometry-audit.json')
locators=load(OUT.relative_to(ROOT)/'locator-audit.json')
hashes=load(OUT.relative_to(ROOT)/'hash-preservation-report.json')
assert not locators['errors'] and all(c['exit_code']==0 for c in locators['checks'])
assert all(not g['errors'] for g in hashes['groups'].values()) and all(hashes['comparisons'].values())
assert all(not p['outside'] and p['gap_partition_matches'] and p['gap_area_matches'] for p in geometry['pages'])
assert sha(CONFIG)=='697d66bf79eff76acfdb4ee23403c905402111f3e4484023ba4bca3fba13a305'

key='spqr5e:p11:492-bullet-3'
entry=next(x for x in ledger['regions'] if x['region']['key']==key)
assert entry['raw_cross_references']==[] and 'as per the\nStacking rules.' in entry['raw_extracted_text']
assert not any(x['region_id']==entry['region']['id'] for x in load(BASE/'continuations.json')['unfollowed_references'])
finding=dict(
    id='R01',severity='medium',title='Explicit named reference missing from the raw reference indexes',
    affected_criteria=[task['acceptance'][4]],
    locations=[dict(path=(BASE/'region-ledger.json').as_posix(),selector="regions[region.key='spqr5e:p11:492-bullet-3'].raw_cross_references",actual=[]),dict(path=(BASE/'continuations.json').as_posix(),selector="unfollowed_references[region_id='region:e9d78c99-a171-42c6-89f1-fe09b46c47e6']",actual='absent')],
    source=dict(pdf_page=11,clause='4.92, third bullet',region_id=entry['region']['id'],region_revision=entry['region']['revision'],box=entry['region']['box'],literal='as per the Stacking rules.',text_artifact=entry['evidence']['text']),
    observation='The original page visibly refers to the Stacking rules. The pinned raw text retains this wording, but the explicit reference list is empty and the unfollowed-reference report has no entry for this region. Other named table/chart references are explicitly indexed.',
    consequence='The task requires raw cross-chapter references to be pinned. A consumer of the supplied reference indexes loses this explicit unresolved dependency even though the text bytes remain available. This is an indexing omission, not a missing source region or a gameplay ruling.',
    required_repair='In a fresh owned repair attempt, retain the literal named reference Stacking rules in this region raw_cross_references and the corresponding continuations unfollowed_references entry. Audit the already assigned pages for the same explicit named-reference omission. Do not infer a section number, resolve meaning, or follow the citation outside physical pages 9-12. Freeze changed reports and a new manifest/delivery envelope; preserve this delivery and all accepted/blocked bytes.',
    repair_validation=['Check the exact region ID/key and original page-11 wording against the repaired raw reference and unfollowed-reference records.','Verify every changed report hash and new envelope; preserve all 135 region IDs, boxes, evidence locators, full/task/context counts, prior accepted scope, complete ledger/order and all four literal continuations.','Re-run required named validations with unchanged tools/tests and approved permissions where needed. Re-review changed material and affected reference-index risks against the preserved complete source review.'],
    repair_cycle=0,maximum_repairs=2)

page_observations={
    9:'Both columns: 4.34, 4.35 and design note; 4.4 heading/counter/introduction, six individually bounded list items and historical note; 4.5 heading/introduction, 4.51-4.55 with exception/play note, and 4.56 opening fragment. Running title, label, separator and copyright are retained. No standalone table/legend observed.',
    10:'Both columns: 4.56 literal continuation and two bullets; 4.6 body, exception and historical digression; 4.7 heading and 4.71-4.75 with design note; 4.8 heading/introduction and 4.81-4.84 with design note. Page furniture retained. No standalone diagram/table/legend observed.',
    11:'Both columns: 4.85; 4.9 heading, complete elephant counter, 4.91 introduction/two bullets, 4.92 introduction/three bullets/closing, 4.93-4.94; 5.0 heading/introduction/important boxed note; 5.1 heading, 5.11 split across columns, 5.12-5.15 with exceptions, activation example, six bullets and closing; 5.2 heading, 5.21/example and 5.22 list introduction. Page furniture retained. R01 concerns the reference index for 4.92 third bullet.',
    12:'Both columns: seven 5.22 items and closing; 5.23 introduction/two items/closing; 5.24/example, 5.25, both 5.26 paragraphs split across columns plus example; 5.27, 5.28 introduction/two items/closing; 5.3 heading/play note; 5.31 introduction/three bullets, 5.32/example, 5.33 introduction/three result bullets and complete 5.34. Page furniture retained. No standalone table/diagram/legend observed.'}
save('source-comparison.json',dict(
    original_pdf=load(BASE/'final-verified/inventory.json')['source']['pdf'],
    method='Independently rendered original physical pages 9-12 at 144 DPI, visually read every page and both columns, compared all 135 ledger entries including raw text and all region rectangles using reviewer-generated overlays. Independently rendered counter neighborhoods from original pages 9 and 11 at 600 DPI and compared all 22 component boundaries and observations. Root validation and independent arithmetic/character/gap checks supplement this visual review.',
    pages=[dict(pdf_page=p,observation=page_observations[p],region_count=sum(x['pdf_page']==p for x in ledger['regions']),original_image=(OUT/'original-pages'/f'page-{p:02}.png').relative_to(ROOT).as_posix(),boundary_image=(OUT/'original-pages'/f'boundaries-{p:02}.png').relative_to(ROOT).as_posix()) for p in [9,10,11,12]],
    region_comparisons=[dict(region_id=x['region']['id'],key=x['region']['key'],revision=x['region']['revision'],box=x['region']['box'],page_reading_order_index=x['page_reading_order_index'],boundary_and_raw_text='compared with original assigned page',reference_index='R01' if x['region']['key']==key else 'checked against retained raw text') for x in ledger['regions']],
    component_comparisons=[dict(region_id=x['region_id'],key=x['key'],box=x['box'],observation=x['observation'],result='compared with original counter; retained source raster uncertainty and zero denominator') for x in components['components']],
    continuations=[dict(from_key='spqr5e:p09:456-start',to_key='spqr5e:p10:456-continuation',result='literal sentence continuation verified'),dict(from_key='spqr5e:p11:511-start',to_key='spqr5e:p11:511-continuation',result='literal column continuation verified'),dict(from_key='spqr5e:p11:522-introduction',to_key='spqr5e:p12:522-item-1',result='list introduction and all seven items verified'),dict(from_key='spqr5e:p12:526-paragraph-2-start',to_key='spqr5e:p12:526-paragraph-2-continuation',result='literal column continuation verified')],
    standalone_examples=5,missing_visible_source_regions_observed=0,findings=[finding],
    boundaries=dict(entry='Page 9 begins with complete numbered 4.34; no page-8 content inspected.',exit='Page 12 ends with complete visible 5.34; no page-13 access or inference.'),
    semantic_acceptance_granted=False,executable_readiness='unverified'))

check_root='private/workflow/checks/active-75e8e322e9c141928400b310de95851c'
result=load(check_root+'/result.json')
assert all(result[k]==0 for k in ['diff_exit','tests_exit','plan_exit','dry_run_exit'])
checks=[
 dict(command='.venv/Scripts/python.exe -B -m pytest -q tests/sources --basetemp private/workflow/checks/b03-b3172589 -p no:cacheprovider --tb=short',exit_code=0,result='71 passed in 14.13s',permissions='require_escalated; approved exact unchanged retry after restricted-token WinError 5'),
 dict(command='pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B03',exit_code=0,result='184 passed in 65.21s; plan/dry-run/tests/diff all zero',permissions='require_escalated; approved exact unchanged retry after restricted-token WinError 5',report=check_root+'/result.json'),
 dict(command='.venv/Scripts/python.exe -B scripts/workflow.py validate',exit_code=0,result='Validated 39 tasks, DAG, scope, context and derived views.'),
 dict(command='git diff --check',exit_code=0,result='Approved read-only execution: no diff errors or access failures; existing CRLF normalization warnings only.',permissions='require_escalated after restricted-token access warnings'),
 dict(command='.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/review-b3172589-20261015/verify.py',exit_code=0,result='All exact packet, dependency, blocked and frozen delivery hashes match; preservation/ledger/canonical replay assertions pass.'),
 dict(command='.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/review-b3172589-20261015/validate_detail.py',exit_code=0,result='Six complete root validations; 135 region and 22 component locator audits; all four independent character and exact geometric gap partitions pass.'),
]+locators['checks']
save('checks.json',dict(checks=checks,environment_failures=[dict(command=checks[0]['command'],exit_code=1,reason='Restricted Windows token: WinError 5 on pytest basetemp; exact approved retry passed.'),dict(command=checks[1]['command'],exit_code=1,reason='Restricted Windows token: WinError 5 on pytest basetemp; exact approved retry passed.')],semantic_acceptance_granted=False))

scope=load(task['continuation_authorization']['scope']['path'])
preserve=load(scope['preserve_manifest']['path'])
dependency=load(SESSION/'references.json')['dependencies']['IG-2B02']
done=load(dependency['evidence'])
end_groups={k:verify(v) for k,v in dict(delivery=delivery['artifacts'],blocked=preserve['artifacts'],accepted_dependency=done['artifacts'],queue=[dict(path='docs/work/queue.json',sha256=load(SESSION/'packet.json')['queue_sha256'])],configuration=[dict(path=CONFIG.as_posix(),sha256=META['configuration_sha256'])]).items()}
assert all(not v['errors'] for v in end_groups.values())
save('end-integrity.json',dict(groups=end_groups,product_writes=[],queue_status_mutated=False,old_attempts_mutated=False))

names=['verify.py','validate_detail.py','finalize_review.py','checkpoint.json','hash-preservation-report.json','locator-audit.json','geometry-audit.json','source-comparison.json','checks.json','end-integrity.json']
names += ['root-'+name+'.log' for name in ['final-verified','replay-a-verified','replay-b-verified','components','components-replay-a','components-replay-b']]
names += ['original-pages/'+f'{prefix}-{p:02}.png' for p in [9,10,11,12] for prefix in ['page','boundaries']]
names += ['original-pages/'+f'{prefix}-{p:02}.png' for p in [9,11] for prefix in ['counter','component-boundaries']]
names += ['original-pages/counter-11-expanded.png','original-pages/component-boundaries-11-expanded.png']
def artifact(p):
    return dict(path=p.as_posix(),bytes=(ROOT/p).stat().st_size,sha256=sha(p))
support=[artifact(OUT.relative_to(ROOT)/name) for name in names]
support += [artifact(__import__('pathlib').Path(check_root)/name) for name in ['plan.log','dry-run.log','pytest.log','diff-check.log','result.json']]
ended=datetime.datetime.now(datetime.timezone.utc)
save('review.json',dict(
    format='wgc-independent-review-1',outcome='changes_requested',summary='R01: page-11 4.92 third bullet explicitly refers to Stacking rules, but both structured raw-reference indexes omit it. All frozen artifact hashes, preserved baseline records, complete source-region/component inspection and required validations otherwise pass.',
    criteria=task['acceptance'],artifacts=delivery['artifacts'],
    criteria_results=[dict(criterion=c,result='changes_requested' if i==4 else 'pass',finding_ids=['R01'] if i==4 else []) for i,c in enumerate(task['acceptance'])],
    checks=checks,findings=[finding],review_artifacts=support,
    reviewed_delivery=artifact(BASE/'delivery.json'),reviewed_manifest=artifact(BASE/'delivery-manifest.json'),input_packet=artifact(SESSION/'packet.json'),
    source_review=(OUT/'source-comparison.json').relative_to(ROOT).as_posix(),
    measurement=dict(started_utc='2026-10-15T17:24:42+00:00',ended_utc=ended.isoformat(),elapsed_wall_seconds=int((ended-datetime.datetime.fromisoformat('2026-10-15T17:24:42+00:00')).total_seconds()),input_tokens=None,output_tokens=None,token_unknown_reason='Session token telemetry is not exposed to this role.',operator_seconds=None,operator_time_unknown_reason='Not reported.',defects_by_severity=dict(medium=1)),
    preservation='All 2334 frozen delivery artifacts, 666 blocked-attempt artifacts and 4409 accepted dependency artifacts rehashed at end. Queue and runtime pins unchanged.',
    semantic_acceptance_granted=False,technical_acceptance_granted=False,executable_readiness='unverified',
    next_action='Supervisor/coordinator scopes a fresh repair for R01 and requests independent review of the new frozen hashes. Reviewer performed no queue transition or product repair.'))
review=load(OUT.relative_to(ROOT)/'review.json')
assert review['artifacts']==delivery['artifacts'] and review['criteria']==task['acceptance'] and not verify(review['review_artifacts'])['errors']
print(json.dumps(dict(outcome=review['outcome'],evidence=(OUT/'review.json').relative_to(ROOT).as_posix(),sha256=sha(OUT.relative_to(ROOT)/'review.json'),finding='R01',criteria=len(review['criteria']),artifacts=len(review['artifacts']),support=len(support))))
