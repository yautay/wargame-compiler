"""Freeze completed task checks and all submitted files before entering review."""
import datetime
import hashlib
import json
from pathlib import Path

from wgc.sources.inventory import file_pin

ROOT=Path.cwd()
RUN=Path('private/workflow/runs/IG-2B06/continuation-21-24-serial02')
SESSION=Path('private/workflow/orchestrator/20261016T182116Z-202cea4c/001-IG-2B06-executor-f2379326')
task=json.loads((SESSION/'task.json').read_text())
claim=json.loads((RUN/'claim.json').read_text())
meta={k:claim[k] for k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256','task')}
def pin(path):return file_pin(ROOT,Path(path).as_posix())
assert pin(meta['configuration_evidence'])['sha256']==meta['configuration_sha256']
common={'final_inventory':pin(RUN/'final-verified/inventory.json'),'final_registry':pin(RUN/'final-verified/identity-registry.json'),
        'input_packet':pin(SESSION/'packet.json'),'selected_task':pin(SESSION/'task.json')}
results=json.loads((RUN/'command-results.json').read_text())
assert results['role']=='executor' and results['actor']==meta['actor']
assert all(c['exit_code']==0 for c in results['checks'])
check_log=(RUN/'check-approved.log').read_text(encoding='utf-8-sig')
log_root=Path(next(line.split('=',1)[1].strip() for line in check_log.splitlines() if line.startswith('LOG_ROOT=')))
assert log_root.resolve().is_relative_to((ROOT/'private/workflow/checks').resolve())
check_result=json.loads((log_root/'result.json').read_text(encoding='utf-8-sig'))
assert all(check_result[k]==0 for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
check_files=[pin(p.relative_to(ROOT) if p.is_absolute() else p) for p in [log_root/name for name in ('plan.log','dry-run.log','pytest.log','diff-check.log','result.json')]]
validation={**meta,'summary':'Actual unchanged required validation results, including approved execution after observed Windows restricted-token denial.',**common,
    'checks':results['checks'],'logs':results['logs'],'repository_check_files':check_files,
    'resolved_failures':[
        {'command':'.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp private/workflow/runs/IG-2B06/continuation-21-24-serial02/pytest-sources-01 -p no:cacheprovider --tb=short','exit_code':1,'cause':'Windows restricted token denied pytest mode-0700 temporary directory access. Exact unchanged validation passed with approved permissions; no ACL/test changes.','log':pin(RUN/'pytest-sources-restricted.log')},
        {'cause':'Initial one-region extraction view retained verified page labels without their out-of-view evidence. Stopped before generation; corrected geometry-only views make no label claim. Full original input/output validations retained.','report':pin(RUN/'generation-failure-01.json'),'log':pin(RUN/'replay-a-failed-01.log')}],
    'source_tests':'71 passed','repository_tests':'267 passed','machine_checks':pin(RUN/'machine-checks.json'),
    'reports':[pin(RUN/name) for name in ('preservation-report.json','replay-report.json','region-ledger.json','continuations.json','coverage-report.json','source-pins.json','toolchain.json','original-page-inspection.json')],
    'unresolved_failures':[],'assertions_unchanged':True,'semantic_acceptance':False,'executable_readiness':'unverified'}
(RUN/'validation-report.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
ended=datetime.datetime.now(datetime.timezone.utc)
checkpoint=json.loads((RUN/'checkpoint.json').read_text())
started=datetime.datetime.fromisoformat(checkpoint['started_utc'])
handoff='''# IG-2B06 delivery for independent review

The fresh complete 44-page inventory preserves every accepted nonassigned record,
link, page, evidence artifact and registry mapping. Exactly the four page-21–24
placeholder memberships are retired; their registry entries remain. The task adds
112 assigned source regions and two context-only regions, with complete component
accounting, explicit geometric gaps, and fresh text/PNG/cropped-PDF locators.

All four original pages, all proposed regions/components and both exact adjacent
context crops were freshly inspected. Two independent complete serial replays and
a separate final derivation agree on every stable locator and generated artifact
byte. Inventory revisions differ because their output paths differ. Evidence IDs
are observed stable under the installed identity function. No inherited inspection
or validation pass is used.

All executor acceptance work is complete for review. The source suite passes 71
tests; the repository check, actual-source locator validation, task machine
assertions and `git diff --check` pass. Windows restricted-token pytest failure and
the resolved extraction-view assembly failure remain preserved in validation
evidence. Approved execution kept the exact tests/assertions unchanged.

`delivery.json` is the immutable ordered artifact manifest. `validation-report.json`
pins actual commands, exits and logs; `replay-report.json` pins all three complete
derivations and every byte comparison. Source, preservation, component, boundary and
coverage reports bind the exact final inventory and companion registry.

The next action is a fresh distinct reviewer inspecting all assigned original pages,
every ledger region/component and continuation boundary, revalidating preservation,
pins and replay comparisons, and running the required checks against these frozen
hashes. Independent review remains pending. There is no human semantic decision,
semantic acceptance, complete transcription claim or executable gameplay readiness.
Machine extraction uncertainty, explicit geometric gaps and remaining unprocessed
pages remain visible. No downstream task may be started by this executor.

Observed configuration: gpt-6.1-sol/high, bound to the supervisor runtime evidence.
Token counts and operator seconds are unknown (null); no cost is inferred.
'''
(RUN/'delivery-handoff.md').write_text(handoff,encoding='utf-8')
# Fixed task outputs retain their original required order. Additional evidence is
# enumerated from exact locators/known filenames, never a recursive tree scan.
paths=[Path(p) for p in task['outputs']]
paths += [RUN/p for p in ('prepare.py','generate.py','reports.py','freeze.py','checkpoint.json','claim.json','checkpoint-authored.json','checkpoint-validated.json','author-regions.json','glyph-audit.json',
    'authored/inventory.json','authored/identity-registry.json','generation-failure-01.json','replay-a-failed-01.log',
    'replay-a.log','replay-b.log','final-generation.log','machine-checks.json','reports.log','command-results.json',
    'pytest-sources-restricted.log','pytest-sources-approved.log','check-approved.log','validate.log','diff-check.log')]
for name in ('replay-a','replay-b','final-verified'):
    paths += [RUN/name/p for p in ('inventory.json','identity-registry.json','coverage.json','generation-report.json')]
    doc=json.loads((RUN/name/'inventory.json').read_text())
    ids={r['id'] for r in doc['regions'] if r['key'].startswith('ig2b06:')}
    for e in doc['evidence']:
        if e['region_id'] in ids:paths += [Path(e[k]['path']) for k in ('text','image','crop_pdf')]
for n in [21,22,23,24]:paths += [RUN/f'original-renders/page-{n}.png',RUN/f'original-renders/overlay-{n}.png']
for n in [20,25]:paths += [RUN/f'original-renders/context-{n}.pdf',RUN/f'original-renders/context-{n}.png']
paths += [Path(p['path']) for p in check_files]
unique=[]
for p in paths:
    if p not in unique:unique.append(p)
artifacts=[pin(p) for p in unique]
delivery={**meta,'summary':'Fresh IG-2B06 serial continuation delivered for independent whole-batch source inventory and technical review; every required executor criterion/check is covered without semantic acceptance.',
    'criteria':task['acceptance'],'artifacts':artifacts,'checks':results['checks'],**common,
    'measurement':{'started_utc':checkpoint['started_utc'],'ended_utc':ended.isoformat(),'wall_seconds':round((ended-started).total_seconds(),3),
        'input_tokens':None,'output_tokens':None,'operator_seconds':None,'unknown_reason':'Token counts and operator time are not exposed to this executor.'},
    'independent_review':'pending fresh distinct reviewer','human_semantic_acceptance':False,'executable_readiness':'unverified',
    'defects':{'observed_executor_defects_by_severity':{'critical':0,'high':0,'medium':0,'low':1},'resolved_executor_defects':1,'unresolved_executor_defects':0,'environment_validation_failures_resolved':1,'independent_reviewer_findings':None,'note':'One low-severity task-local extraction-view assembly defect was resolved before any evidence generation; no product record or assertion was weakened.'},
    'unmet_executor_criteria':[],'remaining_risks':['Machine transcription remains unverified; geometric gaps are explicit and not represented content.','Independent whole-batch review is pending.'],
    'executor_completed_criteria':[task['acceptance'][i] for i in (0,1,3,4)],
    'pending_independent_review_criteria':[task['acceptance'][i] for i in (2,5)],
    'next_operation':'Fresh independent reviewer verifies all exact frozen outputs, original-page/component/boundary inspections, preservation/replays and required checks.'}
path=RUN/'delivery.json'; assert not path.exists();path.write_text(json.dumps(delivery,indent=2)+'\n',encoding='utf-8')
for a in artifacts:assert pin(a['path'])==a
print(json.dumps({'delivery':pin(path),'artifact_count':len(artifacts),'checks':len(results['checks'])}))
