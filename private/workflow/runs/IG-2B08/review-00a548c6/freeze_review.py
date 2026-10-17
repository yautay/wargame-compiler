import json, pathlib, hashlib, re, datetime

ROOT=pathlib.Path('private/workflow/runs/IG-2B08/review-00a548c6')
DEL=pathlib.Path('private/workflow/runs/IG-2B08/repair-F03-F04-01')
SESSION=pathlib.Path('private/workflow/orchestrator/20261017T151724Z-86fb83c5/002-IG-2B08-reviewer-00a548c6')
def load(p): return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def pin(p):
    p=pathlib.Path(p); b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
runtime=SESSION/'runtime-configuration.json'; config=load(runtime)
assert config['status']=='confirmed' and config['model']=='gpt-6.1-sol' and config['reasoning']=='high'
meta=dict(role='reviewer',actor='ig2:002-IG-2B08-reviewer-00a548c6:reviewer',model=config['model'],reasoning=config['reasoning'],configuration_evidence=runtime.as_posix(),configuration_sha256=pin(runtime)['sha256'])
def save(name,data):
    p=ROOT/name; assert not p.exists(), 'Review evidence is append-only'
    p.write_text(json.dumps(dict(meta,**data),indent=2)+'\n',encoding='utf-8')
index=load(ROOT/'inspection-index.json')
index.update(meta)
(ROOT/'inspection-index.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
task=load(SESSION/'task.json'); delivery=load(DEL/'delivery.json')
criteria=task['acceptance']; assert delivery['criteria']==criteria
proof=load(ROOT/'component-proof.json'); rows={r['observation_index']:r for r in proof['results']}
for r in rows.values():
    assert all(x['source_pixels_outside_actual_image_with_1px_margin']>0 for x in r['runs'])
structural=load(ROOT/'independent-structural-check.json'); assert structural['status']=='pass'

fulltext=(ROOT/'full-check.log').read_text(encoding='utf-8-sig',errors='replace')
logroot=pathlib.Path(re.search(r'LOG_ROOT=([^\r\n]+)',fulltext).group(1).strip())
checkresult=load(logroot/'result.json')
assert all(checkresult[k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
sourcetext=(ROOT/'source-suite.log').read_text(encoding='utf-8-sig',errors='replace')
assert re.search(r'\b\d+ passed\b',sourcetext) and not re.search(r'\b[1-9]\d* (?:failed|errors?)\b',sourcetext)
validation_roots=['53593051bccf49fbad9f8468a0c37c1a','f7169730c13d4e7db7af356a06d6418e','db2440d80728410cbf2b46fad154d2c0']
checks=[]
for name,uuid in zip(['final-verified','replay-1','replay-2'],validation_roots):
    log=pathlib.Path('private/workflow/runs/IG-2B08/review-validation-002-IG-2B08-reviewer-00a548c6')/uuid
    checks.append(dict(command=f".venv/Scripts/python.exe scripts/task_access.py validate-source --file '{DEL.as_posix()}/{name}/inventory.json'",exit_code=0,inventory=pin(DEL/name/'inventory.json'),stdout=pin(log/'stdout.log'),stderr=pin(log/'stderr.log')))
sourcecommand='.venv/Scripts/python.exe -m pytest tests/sources -q --basetemp private/workflow/runs/IG-2B08/review-00a548c6/source-pytest -p no:cacheprovider --tb=short'
checks.extend([
    dict(command=sourcecommand,exit_code=0,log=pin(ROOT/'source-suite.log'),passed_count=int(re.search(r'(\d+) passed',sourcetext).group(1)),approved_exact_command_execution=True),
    dict(command='pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08',exit_code=0,log=pin(ROOT/'full-check.log'),result=pin(logroot/'result.json'),selected_result=checkresult,approved_exact_command_execution=True),
    dict(command='git diff --check',exit_code=0,log=pin(ROOT/'diff-check.log')),
    dict(command='.venv/Scripts/python.exe private/workflow/runs/IG-2B08/review-00a548c6/review_originals.py',exit_code=0,log=pin(ROOT/'originals-execution.log')),
    dict(command='.venv/Scripts/python.exe private/workflow/runs/IG-2B08/review-00a548c6/verify_review.py',exit_code=0,log=pin(ROOT/'independent-verification-final.log'),report=pin(ROOT/'independent-structural-check.json'),component_proof=pin(ROOT/'component-proof.json')),
])
save('validation-evidence.json',dict(task='IG-2B08',summary='Unchanged required reviewer source validation, source suite, full check and diff check passed. Raw logs remain private.',checks=checks,restricted_failures=[dict(command=sourcecommand,exit_code=1,selected_diagnosis='WinError 5 / PermissionError accessing the unchanged source-pytest temporary directory',resolution='Exact unchanged command approved through exec_command sandbox_permissions=require_escalated; passed.'),dict(command='pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08',exit_code=1,selected_diagnosis='PermissionError in pytest temporary directory; plan/dry-run/diff passed',result=pin('private/workflow/checks/active-956ec8a6f7bf44d1938cfffee938a74b/result.json'),resolution='Exact unchanged command approved through exec_command sandbox_permissions=require_escalated; passed.')],review_helper_corrections=['Renamed the initial reviewer inspect.py to avoid shadowing Python inspect during pdfplumber import; rerun succeeded.','Corrected reviewer component-kind membership to the delivered diagram/table/example/legend contract; clauses/headings/notes remain inspected through the complete region ledger.','Moved the narrow wheel-origin witness to its actual visible left vertex; no delivered artifact or test was modified.']))

descriptions={
29:'All paragraphs, 8.5 heading and two design notes, running header/footer, both complete hex diagrams, each tile/counter/label/marker/arrow inspected against every associated ledger entry. Incoming paragraph agrees with the bounded accepted page-28 dependency observation. Further intended detail clipping is reported below.',
30:'All 8.52-8.56 text, four diagram panels/captions, 8.6 heading, historical/play notes, pursuit paragraph/bullets and continuation inspected. Complete source Advance arrows (F01) remain captured; separate wheel arrows and Phalanx details have the reported omissions.',
31:'All continuation text, play notes, Break-Off and 8.63-8.66, Pursuit marker, example, rating key/value cells and modifiers, 8.7 heading and five chart descriptions, 9.0/9.1 headings, historical note, elephant counter and all 9.11 paragraphs/bullets/numbered steps inspected. This page describes charts; no chart contents were invented.',
32:'All 9.11 continuation steps/note, 9.12/9.13 paragraphs and note, 9.14 intro, all split-table header/key/result cells and borders, elephant diagram/counters/six labels/caption, remaining paragraphs/bullets, running header/footer and exact exit paragraph inspected.',
}
save('visual-inspection.json',dict(task='IG-2B08',summary='Independent physical source review of the entire assigned page/target scope and all 269 ledger observations; this is not semantic acceptance.',source=proof['source'],pages=[dict(physical_page=p,original=pin(ROOT/'originals'/f'page-{p}.png'),boundary_overlay=pin(ROOT/f'boundaries-{p}.png'),observation=descriptions[p],all_ledger_entries_compared=True) for p in [29,30,31,32]],complete_ledger_entries=269,component_ledger_entries=189,assigned_primary_regions=183,new_zero_denominator_details=85,page28=dict(access='Prepared hash-bound IG-2B07 boundary projection only; not rendered or extracted.',retained_context_id='region:720a5d03-c721-469b-8a5e-2b91cb653a02'),page33=dict(box_points=[45,50,306,80],image=pin(ROOT/'originals/page-33.png'),text=pin(ROOT/'originals/page-33.txt'),observation='Only the two initial continuation lines are present; they complete the page-32 last sentence. No following note or other page-33 content was released.',denominator_contribution=0),prior_findings=dict(F01='Full Advance arrow curves/heads and black forward arrow visually retained in region 229 in all three inventories; frozen full-source regression report verified.',F02='Full 4 marker and exposed frame visually retained in region 145 in all three inventories; frozen full-source regression report verified.',F03='Named refined detail 257 now includes full Tribune component, but the same component still loses its top frame in separate ledger group 150; ID retained as reopened.',F04='Repaired detail 198 includes the visible 3 marker and exposed frame in all three inventories; source-bound full-component regression verified.'),semantic_acceptance_granted=False,executable_readiness=False))

affected=[criteria[i] for i in [0,4,5,6,8,11]]
common_validation=[
 'Freshly inspect the entire intended physical component against original source, including all visible frame/outline extremities, rather than only the narrow witness. Correct or split the named detail in a new coordinator-authorized owned attempt; do not change disjoint primary tiles or denominator roles.',
 'Add source-bound full-component regression coverage rejecting each current incomplete crop and truncated top/right/bottom/left variants. Verify complete colored artwork, glyphs, frames and arrow masks as applicable; a key-set, single pixel, or broad primary tile is insufficient.',
 'Preserve F01/F02/F04 repairs, accepted baseline objects and registry history, all frozen attempts and zero context denominator. Recheck every authored component and the exact page-33 boundary.',
 'Generate two complete independent serial replays plus complete final evidence. Verify normalized evidence/locators, stable IDs, registry, reading order, complete region/component set, exhaustive current index and immutable preservation hashes.',
 'Run unchanged source suite, all three task_access source validators, owned complete batch/omission/stale-index verifier, scripts/check.ps1 -Task IG-2B08 and git diff --check; approved exact-command execution is required for observed Windows access failures. Obtain fresh independent review.'
]
specs=[
 ('F03','reopened','low',[150], 'Tribune top frame is still clipped in the separate V-group detail', 'The repaired named v-counter detail 257 is complete. However the same physical Tribune remains clipped in separately authored collapse-diagram-component-v [173,337,241,383]: its top frame lies above the crop. The original F03 full-component repair requirement includes the frame; retain F03 rather than allocating a fresh budget to the same Tribune completeness defect.'),
 ('F05','new','low',[139,142,190], 'Three intended 2-marker details omit their exposed right frames', 'The A and B 2-marker details in the first page-29 diagram, and B-hits-label detail in the second diagram, clip the visible lower-right frame behind the blue counters. Their digits remain visible, but complete intended marker frames do not.'),
 ('F06','new','low',[196], 'Advanced Celt C detail clips the rotated counter vertex', 'The page-29 advance-diagram-component-c-destination [435,370,476,410] cuts the rotated green counter at its right vertex and lower extent. The separately repaired 3-marker detail does not supply this intended counter crop.'),
 ('F07','new','low',[228,239], 'Opaque Phalanx details remain clipped in two page-30 panels', 'Advance component-phalanx [90,382,155,447] cuts the opaque red counter right vertex. Advance-with-Wheel component-destination [220,378,252,434] cuts its lower red edge/frame. Both intended destination details must contain their full visible counters.'),
 ('F08','new','low',[216,240], 'Translucent Phalanx origin details omit visible counter corners', 'Pivot Advance component-origin [233,201,282,258] clips the translucent red origin lower corner. Advance-with-Wheel component-origins [224,383,283,474] clips the lower translucent origin left corner and lower extent. The complete visible origin counter outlines must be retained.'),
 ('F09','new','medium',[241], 'Advance-with-Wheel arrow detail truncates the forward arrow tail', 'The page-30 advance-wheel-component-arrows [202,343,268,440] captures the cyan curves and turning arrow but ends before the black forward arrow tail. This differs from resolved F01, which concerned the separate Advance panel; broad primary tiles and the origin detail cannot complete the separately authored wheel-arrow evidence.'),
]
findings=[]
for fid,state,severity,indices,title,description in specs:
    data=[rows[i] for i in indices]
    findings.append(dict(id=fid,status=state,severity=severity,title=title,description=description,locations=[dict(path=(DEL/'region-ledger.json').as_posix(),pointer=f'/new_observations/{i}/points') for i in indices],components=data,consequence='Intended physical component evidence is incomplete in final-verified and both complete replays. Structural equality and complete primary denominator do not resolve the missing intended pixels.',affected_criteria=affected,evidence=[pin(ROOT/'component-proof.json')]+[pin(ROOT/f'compare-{i}.png') for i in indices],required_repair='Repair the listed intended details in a fresh authorized attempt and regenerate their dependent evidence, ledgers, indexes and complete replay sets. Preserve current immutable inputs.',repair_validation=common_validation,lifetime_note='Existing F03 ID retained for the same Tribune completeness issue; this review does not reset its repair count.' if fid=='F03' else 'New distinct physical component issue; allocate this previously unused ID without renumbering prior findings.'))
reviewfiles=['review_originals.py','verify_review.py','freeze_review.py','inspection-index.json','independent-structural-check.json','component-proof.json','validation-evidence.json','visual-inspection.json','originals-execution.log','independent-verification.log','independent-verification-2.log','independent-verification-final.log','source-suite.log','full-check.log','diff-check.log','wheel-origin-detail.png']
reviewfiles += [f'originals/page-{p}.{ext}' for p in [29,30,31,32,33] for ext in ['png','txt']]
reviewfiles += [f'boundaries-{p}.png' for p in [29,30,31,32]]
reviewfiles += [f'ledger-{p}-{i}.png' for p,count in [(29,7),(30,4),(31,3),(32,3)] for i in range(1,count+1)]
reviewfiles += [f'detail-boundaries-{i}.png' for i in range(1,7)]
reviewfiles += [f'compare-{i}.png' for i in [139,142,150,190,196,216,228,239,240,241]]
reviewfiles += [f'witness-{i}.png' for i in rows]
now=datetime.datetime.now(datetime.timezone.utc)
started=datetime.datetime.fromisoformat(config['observed_utc'])
save('review.json',dict(task='IG-2B08',outcome='changes_requested',summary='All frozen hashes, complete replay sets/indexes, 44-page preservation and unchanged required checks pass. F04 is resolved; named F03 detail is corrected but the same Tribune top frame is clipped in its V-group evidence, so F03 remains open. New F05-F09 identify further incomplete intended component crops on pages 29-30. No human semantic acceptance or executable readiness is granted.',criteria=criteria,criteria_assessment=[dict(criterion=c,status='changes_requested' if i in [0,4,5,6,8,11] else 'verified',basis='Physical intended component completeness findings below; replay set equality itself is verified.' if i in [0,4,5,6,8,11] else 'Independent original-page/complete-ledger review and whole-set structural/preservation checks documented in the pinned review evidence.') for i,c in enumerate(criteria)],artifacts=delivery['artifacts'],delivery_reference=pin(DEL/'delivery.json'),input_packet=pin(SESSION/'packet.json'),review_artifacts=[pin(ROOT/n) for n in reviewfiles],checks=checks,findings=findings,resolved_findings=['F01','F02','F04'],reopened_findings=['F03'],new_findings=['F05','F06','F07','F08','F09'],finding_budget_policy='Coordinator must apply existing per-finding cycle counts. No original finding is renumbered and no budget is reset.',denominators=dict(full_source=1028,assigned_four_pages=183,inherited_nonassigned=845,new_context_regions=86,context_contribution=0),measurement=dict(started_utc=started.isoformat(),ended_utc=now.isoformat(),elapsed_wall_seconds=(now-started).total_seconds(),input_tokens=None,output_tokens=None,operator_seconds=None,unknown_reason='Token counts and operator time were not exposed.'),semantic_acceptance_granted=False,executable_readiness=False,next_operation='Coordinator refines a bounded repair for the retained F03 and new F05-F09 findings; this reviewer does not mutate queue/status or launch another role.'))
review=load(ROOT/'review.json')
assert review['artifacts']==delivery['artifacts'] and review['criteria']==criteria
for item in review['review_artifacts']:
    assert pin(item['path'])==item
print(json.dumps({'outcome':review['outcome'],'evidence':(ROOT/'review.json').as_posix(),'review_sha256':pin(ROOT/'review.json')['sha256'],'finding_ids':[f['id'] for f in findings],'delivery_artifacts':len(delivery['artifacts']),'source_suite_passed':checks[3]['passed_count']}))
