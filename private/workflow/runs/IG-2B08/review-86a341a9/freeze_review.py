import datetime
import hashlib
import json
import pathlib
import re

ROOT=pathlib.Path('private/workflow/runs/IG-2B08/review-86a341a9')
PRODUCT=pathlib.Path('private/workflow/runs/IG-2B08/repair-F01-manifest02')
SESSION=pathlib.Path('private/workflow/orchestrator/20261017T111422Z-80dfde30/001-IG-2B08-reviewer-86a341a9')
def load(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def pin(p):
    p=pathlib.Path(p);return {'path':p.as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
configuration=load(SESSION/'runtime-configuration.json')
assert configuration['status']=='confirmed' and configuration['model']=='gpt-6.1-sol' and configuration['reasoning']=='high'
meta={'role':'reviewer','actor':'ig2:001-IG-2B08-reviewer-86a341a9:reviewer','model':configuration['model'],'reasoning':configuration['reasoning'],'configuration_evidence':(SESSION/'runtime-configuration.json').as_posix(),'configuration_sha256':sha(SESSION/'runtime-configuration.json')}
task=load(SESSION/'task.json');delivery=load(PRODUCT/'delivery.json')
assert sha(PRODUCT/'delivery.json')=='4898ab3b4ed73bc33a766fa93cfe22dd09a19f8d2919b742fdb8d9f13345384f'
scope=load('private/workflow/runs/IG-2B08/validation-context-recovery-20261017-01/scope.json')
preserve=load(scope['preserve_manifest']['path'])
assert sha(scope['preserve_manifest']['path'])==scope['preserve_manifest']['sha256']
for artifact in delivery['artifacts']+preserve['artifacts']:
    assert pin(artifact['path'])==artifact
independent=load(ROOT/'independent-verification.json')
assert independent['exit_code']==0
assert all(x['missing_visible_stem_pixels']==51 for x in independent['F02_probe']['runs'])

# Add runtime attribution to the earlier locally generated source index before freeze.
fresh=load(ROOT/'fresh-source-artifacts.json')
(ROOT/'fresh-source-artifacts.json').write_text(json.dumps({**meta,**fresh},indent=2)+'\n',encoding='utf-8')
rows=load(PRODUCT/'region-ledger.json')['new_observations']
components=load(PRODUCT/'component-ledger.json')['components']
visual={**meta,'task':'IG-2B08','summary':'Fresh assigned originals, every primary boundary, all authored detail crops and exact page-33 continuation inspected against the complete assigned ledger. F02 confirmed; F01 repaired.',
    'source':pin('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'),
    'assigned_originals':[pin(ROOT/f'originals/page-{p}.png') for p in [29,30,31,32]],
    'context_page33':{'image':pin(ROOT/'originals/page-33-continuation.png'),'text':pin(ROOT/'originals/page-33-continuation.txt'),'box_points':[45,50,306,80],'protocol':'Original native raster crop; pdfplumber original-page crop before extraction. No later note or whole page-33 access.'},
    'page28':'Reference only: prepared hash-bound IG-2B07 boundary projection; no page-28 render or extraction.',
    'observations':[
        {'physical_page':29,'observation':'Header/footer, incoming page-28 example, Celt C calculation, Collapse paragraphs, both combat diagrams with A-D/T-Z counters/labels/hit stacks/arrows, 8.5 heading and 8.51 notes accounted. C 4-marker detail clips the visible right stem (F02).'},
        {'physical_page':30,'observation':'8.52-8.56 with four diagram panels/captions, disjoint primary tiles and all counter/motion details inspected. Corrected Advance arrow detail contains both cyan curves/heads and black forward arrow (F01 resolved). Pursuit heading/notes, five exceptions and two direction bullets, column/page continuation retained.'},
        {'physical_page':31,'observation':'Pursue continuation, notes, Break-Off, wrapped 8.63 text/Finished marker, Zama example, 8.64-8.66, separate pursuit key/value cells and four modifiers inspected. Five chart-description clauses, 9.0/9.1 headings/history, elephant artwork and wrapped 9.11 restrictions/steps retained.'},
        {'physical_page':32,'observation':'Pass-Thru steps 3-4, notes, 9.12-9.14, all split table header/key/result cells, both elephant compass tiles/counters and six labels, example caption, rampage paragraphs/four ending bullets/leader paragraph and exit inspected.'}],
    'ledger_inspection':[{'key':r['key'],'region_id':r['region_id'],'page':r['page'],'points':r['points'],'denominator_role':r['role'],'result':'F02: intended marker detail incomplete' if r['key']=='ig2b08:p29:collapse-diagram-component-c-hits' else 'Compared against fresh authorized original and boundary overlay; no additional defect identified'} for r in rows],
    'component_entries_inspected':len(components),'all_ledger_entries_inspected':len(rows),'component_sheets':[pin(ROOT/f'boundary-aids/components-{i:02d}.png') for i in range(1,17)],
    'geometric_gaps':'Explicit geometric gaps remain gaps; thresholded ink and word-center probes do not establish transcription or source meaning completeness.',
    'semantic_acceptance_granted':False,'executable_readiness':False}
(ROOT/'visual-inspection.json').write_text(json.dumps(visual,indent=2)+'\n',encoding='utf-8')

source_log=(ROOT/'source-suite-approved.log').read_text(encoding='utf-8-sig',errors='replace')
full_log=(ROOT/'full-check-approved.log').read_text(encoding='utf-8-sig',errors='replace')
assert '71 passed' in source_log and '297 passed' in full_log
checkroot=pathlib.Path(re.findall(r'LOG_ROOT=(.+)',full_log)[-1].strip())
full_result=load(checkroot/'result.json');assert all(full_result[x]==0 for x in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
checks=[
    {'command':'Hash verification of all exact frozen delivery and current preservation-manifest artifacts, before review and before freeze','exit_code':0,'delivery_artifacts':5302,'preserved_artifacts':10358},
    {'command':'.venv/Scripts/python.exe private/workflow/runs/IG-2B08/review-86a341a9/inspect_sources.py','exit_code':0,'evidence':pin(ROOT/'fresh-source-artifacts.json')},
    {'command':'.venv/Scripts/python.exe private/workflow/runs/IG-2B08/review-86a341a9/inspect_boundaries.py','exit_code':0,'evidence':pin(ROOT/'visual-inspection.json')},
    {'command':'.venv/Scripts/python.exe private/workflow/runs/IG-2B08/review-86a341a9/verify_independent.py','exit_code':0,'evidence':pin(ROOT/'independent-verification.json')},
    {'command':'Independent complete assigned-original/component completeness comparison','exit_code':1,'finding':'F02','evidence':pin(ROOT/'visual-inspection.json')},
    {'command':'.venv/Scripts/python.exe -m pytest tests/sources -q --basetemp private/workflow/runs/IG-2B08/review-86a341a9/source-pytest -p no:cacheprovider --tb=short','exit_code':0,'execution':'Approved unchanged command after restricted-token WinError 5; assertions unchanged.','tests_passed':71,'log':pin(ROOT/'source-suite-approved.log')},
    {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08','exit_code':0,'execution':'Approved unchanged command after restricted-token PermissionError/WinError 5.','tests_passed':297,'log':pin(ROOT/'full-check-approved.log'),'result':pin((checkroot/'result.json').relative_to(pathlib.Path.cwd()))},
    {'command':'git diff --check','exit_code':0,'log':pin(ROOT/'diff-check.log')}]
validator_roots=[('final-verified','877b4094527c4830a1eb8116e0abab68'),('replay-1','e4be3e4469b3403681d35f53707a290f'),('replay-2','8a4f7bca801447a3ae4294c16b38f7d6')]
for name,identifier in validator_roots:
    p=pathlib.Path('private/workflow/runs/IG-2B08/review-validation-001-IG-2B08-reviewer-86a341a9')/identifier
    checks.append({'command':f".venv/Scripts/python.exe scripts/task_access.py validate-source --file '{PRODUCT.as_posix()}/{name}/inventory.json'",'underlying_command':f'.venv/Scripts/python.exe -m wgc.sources validate {PRODUCT.as_posix()}/{name}/inventory.json','exit_code':0,'stdout':pin(p/'stdout.log'),'stderr':pin(p/'stderr.log'),'output_policy':'No raw validator output released.'})

affected=[task['acceptance'][i] for i in [0,5,6,8]]
component=next(x for x in components if x['key']=='ig2b08:p29:collapse-diagram-component-c-hits')
finding={'id':'F02','severity':'medium','title':'Page-29 Celt C hit-marker detail truncates the visible 4 digit',
    'locations':[{'path':(PRODUCT/'component-ledger.json').as_posix(),'pointer':'/components/65/points'},{'path':(PRODUCT/'region-ledger.json').as_posix(),'pointer':'/new_observations/145/points'},{'path':(PRODUCT/'original-page-inspection.json').as_posix(),'pointer':'/observations/145/points'}],
    'region_key':component['key'],'region_id':component['region_id'],'region_revision':component['revision'],'physical_page':29,'points':[106,496,133,527],
    'description':'Fresh original inspection shows the intended visible 4 hit-marker crop cuts through the right stem. In the independently selected original-source window [130,513,138,523] points, 51 red/yellow visible stem pixels lie outside the intended component; missing 144-DPI pixel bounds are [266,1026,272,1040]. The same region revision and incomplete intended crop appear in final-verified and both complete replays.',
    'consequence':'The authored component and exact evidence are incomplete. Whole-page primary tiles retain the marker, and preservation/denominators pass; those do not satisfy the intended detail-component completeness criterion.',
    'affected_criteria':affected,
    'evidence':[pin(ROOT/'boundary-aids/c-hit-original-boundary.png'),pin(ROOT/'boundary-aids/c-hit-delivered.png'),pin(ROOT/'independent-verification.json'),pin(ROOT/'originals/page-29.png')],
    'required_repair':'In a new coordinator-authorized repair attempt, correct or split the zero-denominator C hit-marker selection so the full visible 4 and marker are included in intended component evidence. Preserve all disjoint primary tiles, accepted baseline objects, registry history and frozen attempts. Regenerate affected evidence and dependent reports/indexes plus complete final/replay artifact sets at fresh paths.',
    'repair_validation':[
        'Freshly compare the complete visible digit and marker against original physical page 29. Add a source-bound regression that rejects [106,496,133,527] and checks the full visible stem/marker extent; a key-set or single-pixel check is insufficient. Verify the 51-pixel witness patch is included in the intended detail, not merely a primary tile or adjacent counter.',
        'Recheck every assigned component and context boundary; preserve the resolved F01 full-arrow masks and page-33 exact clipping. Keep context denominator zero.',
        'Generate the complete final and two independent serial replay sets separately, and verify stable identities, registry history, normalized bytes/locators, complete current indexes, baseline preservation and all delivery hashes.',
        'Rerun unchanged source suite, the three pinned source CLI validators via task_access, owned batch verifier, scripts/check.ps1 -Task IG-2B08 and git diff --check. Use approved exact-command execution for observed Windows access failures. Obtain fresh independent review.']}

assess=[]
for i,criterion in enumerate(task['acceptance']):
    if i in [0,5,6,8]:status='unmet';reason='F02: intended page-29 C hit-marker detail is truncated in final and both replays.'
    elif i==11:status='review_completed_changes_requested';reason='This fresh independent review inspected the complete assigned scope and preserved prior coverage; F02 prevents a passing outcome.'
    else:status='met';reason={1:'Exact locators, uncertainty and boundary links retained; component completeness is separately rejected under F02.',3:'44-page baseline, 937 retained regions, 925 evidence objects, 229 links, 1013 registry entries and retained order verified internally.',4:'Fresh originals and every proposed boundary/component independently inspected; all current pin/path checks pass.',7:'Page-28 reference-only projection and retained context preserved; exact page-33 continuation freshly clipped before text/pixel output; zero context denominator.',9:'Full/assigned/inherited/context denominators remain separate, with partial/unprocessed statuses and explicit gaps; no semantic or executable claim.',10:'All 5302 frozen artifacts verified, including required reports and both complete replay sets; 5229 source-index artifacts and 22 current reports match pins.'}.get(i,'Complete assigned ledger compared against fresh original source evidence.')
    assess.append({'criterion':criterion,'status':status,'reason':reason})
ended=datetime.datetime.now(datetime.timezone.utc)
review={**meta,'task':'IG-2B08','outcome':'changes_requested','summary':'F01 is resolved, but F02 is independently confirmed: the page-29 C hit-marker detail truncates the visible 4 in final and both replays. Structural validation, preservation, exhaustive pins and required suites pass; repair and fresh independent review are required.',
    'criteria':task['acceptance'],'criteria_assessment':assess,'artifacts':delivery['artifacts'],'delivery':pin(PRODUCT/'delivery.json'),'input_packet':pin(SESSION/'packet.json'),'selected_contract':pin(SESSION/'task.json'),'checks':checks,'findings':[finding],
    'resolved_findings':[{'id':'F01','result':'resolved','evidence':pin(ROOT/'independent-verification.json'),'basis':'Fresh full-arrow visual comparison and all 199/194 cyan-mask plus 458 black-arrow source pixels verified inside intended final/replay evidence; old truncated crop rejected.'}],
    'review_evidence':[pin(ROOT/x) for x in ['inspect_sources.py','inspect_boundaries.py','verify_independent.py','freeze_review.py','fresh-source-artifacts.json','independent-verification.json','visual-inspection.json']],
    'validation_attempts':[{'command':'Unchanged source suite in restricted token','exit_code':1,'reason':'PermissionError / WinError 5 in temporary-directory access','log':pin(ROOT/'source-suite.log'),'resolution':'Approved exact-command run passed 71 tests.'},{'command':'Unchanged full task check in restricted token','exit_code':1,'reason':'PermissionError / WinError 5; plan, dry-run and diff checks passed','log':pin(ROOT/'full-check.log'),'resolution':'Approved exact-command run passed 297 tests.'},{'command':'Initial reviewer comparison harness','exit_code':1,'reason':'Reviewer harness expected a boolean executable-readiness field; actual contract value is the string unverified. Corrected that reviewer-owned field assertion; product and repository tests unchanged.','log':pin(ROOT/'independent-verification.log')},{'command':'Initial visual aid generation','exit_code':0,'reason':'Initial helper selected a nonexistent detail role and produced zero detail sheets. Corrected fresh boundary helper selected context-role details and inspected all 189 component entries.'}],
    'preservation_recheck':{'delivery_count':len(delivery['artifacts']),'preserved_count':len(preserve['artifacts']),'all_hashes_verified_before_freeze':True,'manifest':scope['preserve_manifest']},
    'semantic_acceptance_granted':False,'executable_readiness':False,'queue_mutated':False,'product_mutated':False,'next_operation':'Coordinator may scope a new F02 repair; this reviewer grants no execution, acceptance or downstream readiness.',
    'measurement':{'started_utc':configuration['observed_utc'],'ended_utc':ended.isoformat(),'wall_seconds':None,'input_tokens':None,'output_tokens':None,'unknown_reason':'Exact role-start wall timer and token usage are not exposed; start records observed runtime UTC.'}}
assert review['artifacts']==delivery['artifacts'] and review['criteria']==task['acceptance']
target=ROOT/'review.json';assert not target.exists()
target.write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'outcome':'changes_requested','evidence':target.as_posix(),'sha256':sha(target),'finding':'F02','frozen_delivery_artifacts':len(review['artifacts']),'preserved_artifacts':len(preserve['artifacts'])}))
