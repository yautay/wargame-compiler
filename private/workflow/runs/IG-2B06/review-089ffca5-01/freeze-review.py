"""Freeze this independent review after all observed checks have completed."""
import datetime
import json
from pathlib import Path

from wgc.sources.inventory import file_pin

ROOT = Path.cwd()
OUT = Path('private/workflow/runs/IG-2B06/review-089ffca5-01')
RUN = Path('private/workflow/runs/IG-2B06/continuation-21-24-serial02')
SESSION = Path('private/workflow/orchestrator/20261016T182116Z-202cea4c/002-IG-2B06-reviewer-089ffca5')


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def pin(path):
    return file_pin(ROOT, Path(path).as_posix())


checkpoint = load(OUT/'checkpoint.json')
meta = {k: checkpoint[k] for k in ('role','actor','task','model','reasoning','configuration_evidence','configuration_sha256')}
assert pin(meta['configuration_evidence'])['sha256'] == meta['configuration_sha256']
configuration = load(meta['configuration_evidence'])
assert configuration['status'] == 'confirmed' and configuration['model'] == meta['model'] == 'gpt-6.1-sol'
assert configuration['reasoning'] == meta['reasoning'] == 'high'
task = load(SESSION/'task.json')
reference = load(SESSION/'delivery-reference.json')
assert pin(reference['evidence'])['sha256'] == reference['sha256']
delivery = load(reference['evidence'])
assert meta['actor'] != delivery['actor']
assert task['acceptance'] == delivery['criteria']
for artifact in delivery['artifacts']:
    assert pin(artifact['path']) == artifact, artifact['path']
for name in ('machine-checks.json','replay-a-report.json','replay-b-report.json','reviewer-replay-comparison.json'):
    report = load(OUT/name)
    assert report['exit_code'] == 0
    assert all(report[k] == v for k,v in meta.items())
inspection = load(OUT/'source-inspection.json')
assert inspection['assigned_regions_reviewed'] == 112 and inspection['assigned_components_reviewed'] == 158
assert not inspection['findings']
approved = Path('private/workflow/checks/active-3b56c93cba4348d9ad27ffd234bf6752')
restricted = Path('private/workflow/checks/active-ae9352d7704842fa8c2bb66637b22f95')
assert all(load(approved/'result.json')[k] == 0 for k in ('tests_exit','diff_exit','dry_run_exit','plan_exit'))
assert '267 passed in 52.36s' in (approved/'pytest.log').read_text(encoding='utf-8-sig')
assert '71 passed in 29.52s' in (OUT/'pytest-sources-approved.log').read_text()
validate_log = (OUT/'validate.log').read_text(encoding='utf-8-sig')
assert validate_log.strip()
checks = [
    {'command':f'.venv/Scripts/python.exe {OUT.as_posix()}/verify.py check', 'exit_code':0, 'report':pin(OUT/'machine-checks.json')},
    {'command':f'.venv/Scripts/python.exe {OUT.as_posix()}/verify.py replay-a', 'exit_code':0, 'report':pin(OUT/'replay-a-report.json')},
    {'command':f'.venv/Scripts/python.exe {OUT.as_posix()}/verify.py replay-b', 'exit_code':0, 'report':pin(OUT/'replay-b-report.json'), 'log':pin(OUT/'replay-b.log')},
    {'command':f'.venv/Scripts/python.exe {OUT.as_posix()}/verify.py compare', 'exit_code':0, 'report':pin(OUT/'reviewer-replay-comparison.json')},
    {'command':f'.venv/Scripts/python.exe -m wgc.sources validate {RUN.as_posix()}/final-verified/inventory.json', 'exit_code':0, 'log':pin(OUT/'validate.log')},
    {'command':f'.venv/Scripts/python.exe -m pytest -q tests/sources --basetemp {OUT.as_posix()}/pytest-sources-01 -p no:cacheprovider --tb=short', 'exit_code':0, 'result':'71 passed in 29.52s', 'execution':'Approved exact unchanged validation command after restricted-token temporary-directory denial.', 'log':pin(OUT/'pytest-sources-approved.log')},
    {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B06', 'exit_code':0, 'result':'267 passed in 52.36s; planning, dry-run and diff checks passed.', 'execution':'Approved exact unchanged validation command after restricted-token temporary-directory denial.', 'report':pin(approved/'result.json')},
    {'command':'git diff --check', 'exit_code':0, 'log':pin(OUT/'diff-check.log')},
]
review_paths = [OUT/name for name in (
    'checkpoint.json','checkpoint-inspected.json','verify.py','freeze-review.py',
    'machine-checks.json','glyph-audit.json','toolchain-verification.json','source-inspection.json',
    'replay-a-report.json','replay-b-report.json','reviewer-replay-comparison.json','replay-b.log',
    'pytest-sources-restricted.log','pytest-sources-approved.log','validate.log','diff-check.log')]
review_paths += [OUT/f'page-{n}.png' for n in (21,22,23,24)]
for name in ('replay-a','replay-b'):
    review_paths += [OUT/name/'inventory.json', OUT/name/'identity-registry.json']
    review_paths += [OUT/name/f'region-{n:03d}'/f for n in range(114) for f in ('text.txt','image.png','crop.pdf')]
for directory in (restricted,approved):
    review_paths += [directory/f for f in ('plan.log','dry-run.log','pytest.log','diff-check.log','result.json')]
review_artifacts = [pin(p) for p in review_paths]
ended = datetime.datetime.now(datetime.timezone.utc)
review = {**meta,
    'outcome':'pass',
    'summary':'Independent technical and source-inventory review passes the exact frozen IG-2B06 delivery. All four originals, 112 assigned regions/158 components, two scoped context crops and 32 new structural links were inspected. Both fresh complete serial reviewer replays match the frozen evidence. No source-meaning acceptance or executable readiness is granted.',
    'criteria':task['acceptance'],
    'artifacts':delivery['artifacts'],
    'checks':checks,
    'input_packet':pin(SESSION/'packet.json'),
    'selected_task':pin(SESSION/'task.json'),
    'frozen_delivery':pin(reference['evidence']),
    'independent_actor':True,
    'review_scope':'Entire assigned physical pages 21-24, complete assigned ledger/components, and only page-20/page-25 contracted context boxes.',
    'source_inspection':pin(OUT/'source-inspection.json'),
    'review_artifacts':review_artifacts,
    'criteria_results':[
        {'criterion':task['acceptance'][0], 'result':'pass', 'basis':'Originals and all four overlays inspected; 37/26/26/23 regions and 39/42/28/49 components reviewed; both compound diagrams, counter/marker faces, text, notes, examples and editorial material accounted for. Complements independently partition every page without counting gaps as content.'},
        {'criterion':task['acceptance'][1], 'result':'pass', 'basis':'Every exact final region/revision/box and evidence binding checked; 32 endpoint pairs verified; incoming, internal and outgoing continuations inspected. Unverified machine transcription and clipped context remain explicit uncertainties.'},
        {'criterion':task['acceptance'][2], 'result':'pass', 'basis':'Fresh independent reviewer compared every assigned original page with the complete 112-region/158-component ledger and frozen evidence.'},
        {'criterion':task['acceptance'][3], 'result':'pass', 'basis':'Accepted dependency accessed through the prepared projection; exact accepted input hashes and frozen preservation report revalidated. Reviewed current prepare.py baseline construction and reports.py exact preservation assertions. Independently checked all 44 pages, all 756 output region records and complete author/output structures across all frozen and reviewer replays, retained retired IDs and registry, and all 1866 preserved evidence file pins.'},
        {'criterion':task['acceptance'][4], 'result':'pass', 'basis':'All 1090 frozen artifacts verified twice, including all required reports/logs and fresh final inventory/registry. Two frozen and two fresh reviewer replays cover the complete 114-region set and match all stable author/evidence fields, generated bytes and dimensions. Full/task/context denominators are 753/112/zero-contribution context respectively; all 20 remaining placeholders stay visible.'},
        {'criterion':task['acceptance'][5], 'result':'pass', 'basis':'Distinct observed Sol/high reviewer performed the complete original, component and boundary inspection, pin/preservation/replay assessment and required checks. Technical/source-inventory pass is separate from source meaning and gameplay readiness.'},
    ],
    'findings':[],
    'unmet_criteria':[],
    'defects_by_severity':{'critical':0,'high':0,'medium':0,'low':0},
    'resolved_validation_environment_failures':[
        {'command':checks[5]['command'],'restricted_exit_code':1,'cause':'Windows restricted token denied pytest mode-0700 temporary-directory access.','resolution':'Exact unchanged validation command passed with approved execution.','restricted_log':pin(OUT/'pytest-sources-restricted.log')},
        {'command':checks[6]['command'],'restricted_exit_code':1,'cause':'Windows restricted token denied pytest mode-0700 temporary-directory access.','resolution':'Exact unchanged validation command passed with approved execution.','restricted_report':pin(restricted/'result.json')},
    ],
    'preservation_verification_basis':load(OUT/'machine-checks.json')['baseline_preservation_basis'],
    'delivery_artifacts_unchanged':True,
    'assertions_unchanged':True,
    'human_semantic_acceptance':False,
    'source_meaning_review':'Not accepted by this model review.',
    'executable_readiness':'unverified',
    'remaining_risks':['Machine extraction remains unverified transcription; descriptive and formal semantics retain their explicit gaps.','The other 20 physical pages remain unprocessed placeholders; this four-page review grants no full-rulebook or gameplay readiness.'],
    'measurement':{'started_utc':checkpoint['started_utc'],'ended_utc':ended.isoformat(),
        'wall_seconds':round((ended-datetime.datetime.fromisoformat(checkpoint['started_utc'])).total_seconds(),3),
        'input_tokens':None,'output_tokens':None,'operator_seconds':None,
        'unknown_reason':'Token counts and operator time are not exposed to this reviewer.'},
    'next_operation':'Coordinator may evaluate this exact technical/source-inventory review under workflow gates; no queue transition, acceptance, done state or next session is performed here.',
}
assert review['artifacts'] == delivery['artifacts']
assert all(x['exit_code']==0 for x in review['checks'])
out = OUT/'review.json'
assert not out.exists()
out.write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'outcome':'pass','evidence':out.as_posix(),'sha256':pin(out)['sha256'],
                  'delivery_artifacts':len(review['artifacts']),'review_artifacts':len(review_artifacts)}))
