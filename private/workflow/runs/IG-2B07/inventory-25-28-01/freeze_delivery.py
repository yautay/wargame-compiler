"""Freeze the exact owned task output indexes, with no recursive context discovery."""
import datetime
import json
from pathlib import Path
from wgc.sources.inventory import file_pin, digest

ROOT=Path.cwd()
A=Path(__file__).parent.relative_to(ROOT)
SESSION=Path('private/workflow/orchestrator/20261016T195516Z-332903f5/002-IG-2B07-executor-78a83e6c')
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):
    assert not Path(p).exists(),str(p)
    Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def pin(p): return file_pin(ROOT,Path(p).as_posix())
task=load(SESSION/'task.json')
scope=task['source_scope']
claim=load(A/'claim.json')
meta={k:claim[k] for k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256')}
assert pin(meta['configuration_evidence'])['sha256']==meta['configuration_sha256']
assert (load(meta['configuration_evidence'])['status'],meta['model'],meta['reasoning'])==('confirmed','gpt-6.1-sol','high')
inputs=[scope[k] for k in ('baseline_inventory','identity_registry','source_pdf','source_provenance')]+list(scope['current_reports'].values())+[task['refinement_evidence']]
assert all(pin(i['path'])==i for i in inputs)
observations=load(A/'validation-command-observations.json')
assert all(observations['repository_check_logs'][1]['result'][k]==0 for k in ('tests_exit','plan_exit','diff_exit','dry_run_exit'))
replay=load(A/'replay-report.json')
cov=load(A/'coverage-report.json')
preservation=load(A/'preservation-report.json')
glyph=load(A/'glyph-accounting-report.json')
assert replay['all_passed'] and glyph['all_passed']
assert cov['assigned_inventory_count']==100 and cov['context_denominator_contribution']==0
assert len(replay['runs'])==3 and all(r['output_count']==568 for r in replay['runs'])
checks=[r for r in observations['checks'] if r['exit_code']==0]
for name in ('final-verified','replay-1','replay-2'):
    checks.append({'command':'.venv/Scripts/python.exe '+(A/'run_inventory.py').as_posix()+' --output '+(A/name).as_posix(),
                   'exit_code':0,'report':pin(A/name/'derivation-report.json'),'log':pin(A/('final-generation.log' if name=='final-verified' else name+'.log'))})
checks.append({'command':'.venv/Scripts/python.exe '+(A/'report_inventory.py').as_posix(),'exit_code':0,'report':pin(A/'replay-report.json')})
validation={**meta,'format':'wgc-frozen-inventory-validation-1','checks':checks,
            'prior_environment_failures':pin(A/'validation-command-observations.json'),
            'input_pins_reverified':inputs,'packet':pin(SESSION/'packet.json'),
            'full_inventory_count':cov['full_inventory_count'],'task_inventory_count':100,
            'full_context_count':cov['full_context_count'],'new_nested_components':86,'new_boundary_contexts':2,
            'context_denominator_contribution':0,'source_structure':'All 44 actual PDF page geometries and both page counters validated; extraction restricted to assigned pages and exact boundary strips.',
            'glyph_accounting':pin(A/'glyph-accounting-report.json'),'preservation':pin(A/'preservation-report.json'),
            'complete_replays':pin(A/'replay-report.json'),'source_inspection':pin(A/'original-page-inspection.json'),
            'unresolved_limits':['Independent technical/source-accounting review is pending.','Full transcription and tiny raster counter glyph readings remain unverified.','Descriptive/formal semantic representation and executable readiness remain unprocessed.','Unassigned pages 29-44 retain their inherited unprocessed placeholders.'],
            'semantic_acceptance_granted':False,'executable_readiness':'unverified'}
write(A/'validation-report.json',validation)
handoff='''# IG-2B07 executor handoff

The assigned original physical pages 25-28 now have 100 independent inventory
regions, 86 nested component observations and two boundary-context observations.
The full sidecar has 849 inventory regions and 91 context regions. Context contributes
zero denominator units. Pages 29-44 retain their unprocessed placeholder memberships.

The accepted IG-2B06 source, all 44 page records, every nonretired region, inherited
evidence and links, and all existing registry entries are preserved exactly. Only
the four assigned placeholder memberships are retired. The inherited page-25 context
record and its evidence/links remain unchanged. Fresh evidence covers every new target.

All assigned originals, both columns, notes, examples, diagrams/artwork and permitted
boundary strips were freshly inspected. Every fresh crop was inspected in this role;
six corrected contact sheets were viewed again and 20 unchanged sheets compared byte
for byte with the images already viewed in this same session. Draft output bytes are
preserved under draft-01 and indexed in draft-preservation.json; they are superseded
candidate data and grant no delivery or acceptance claims.

Final generation and two separate complete serial replays regenerated all 188 targets.
Registry IDs, author fields, geometry, reading order, links, coverage, text/PNG/PDF
payload hashes and path-normalized sidecars compare exactly. No worker pool was used.
The independent glyph check found zero unassigned nonwhitespace text-glyph centers
on any assigned page. Raster diagrams retain separate visual component accounting.

Source validation passed. The unchanged explicit source suite passed 71 tests; the
unchanged repository check passed 274 tests plus queue, dry-run and diff checks.
Windows restricted-token pytest basetemp failures were resolved only through approved
execution of the exact unchanged commands. Tests, assertions, ACLs and dependencies
were not changed. Exact reports, failures and approved command results are frozen.

The observed configuration is gpt-6.1-sol/high with the exact runtime evidence and
SHA-256 recorded in delivery.json. Token counts and operator time are not exposed.

Next action: an independent reviewer must compare the entire frozen manifest, every
assigned original page, all region/component accounting and boundary evidence. No
source-semantic acceptance, gameplay legality or executable readiness is granted.
Full transcription, tiny counter glyph readings and later semantics remain explicit
gaps. The executor stops at review and does not launch another role or downstream task.
'''
assert not (A/'delivery-handoff.md').exists()
(A/'delivery-handoff.md').write_text(handoff,encoding='utf-8',newline='\n')
now=datetime.datetime.now(datetime.timezone.utc)
initial=load(A/'checkpoint-initial.json')
write(A/'checkpoint-final.json',{**meta,'task':task['id'],'attempt':A.name,'input_packet':pin(SESSION/'packet.json'),
                               'base_files':inputs,'changed_files':[pin(p) for p in task['outputs']],
                               'completed_criteria':[v for i,v in enumerate(task['acceptance']) if i not in (2,len(task['acceptance'])-1)],
                               'pending_criteria':[task['acceptance'][2],task['acceptance'][-1]],'checks':checks,'blocker':None,
                               'next_operation':'Freeze all indexed evidence and transition this task to independent review; stop this executor role.',
                               'started_utc':initial['started_utc'],'checkpoint_utc':now.isoformat()})
# Every delivery artifact is indexed explicitly. Test temporary trees are neither
# product deliverables nor context and are not searched or copied.
paths=[Path(p) for p in task['outputs']]
paths += [A/n for n in ('prepare_originals.py','author_inventory.py','run_inventory.py','report_inventory.py','check_accounting.py','freeze_delivery.py',
                        'claim.json','checkpoint-initial.json','checkpoint-inspected.json','checkpoint-final.json','author-input.json','author-registry.json','author-pins.json',
                        'glyph-accounting-report.json','visual-observations.json','validation-command-observations.json','draft-preservation.json',
                        'final-generation.log','replay-1.log','replay-2.log','source-validation.log','diff-check.log','originals/pins.json','inspection-sheets/index.json')]
paths += [Path(p['path']) for p in load(A/'originals/pins.json')]
paths += [Path(p['path']) for p in load(A/'inspection-sheets/index.json')]
paths += [Path(p['path']) for run in replay['runs'] for p in run['output_pins']]
paths += [Path(p['preserved']['path']) for p in load(A/'draft-preservation.json')['artifacts']]
paths += [Path(p['path']) for run in observations['repository_check_logs'] for p in run['reports']]
unique=list(dict.fromkeys(paths))
assert all(p.resolve().is_relative_to((ROOT/A).resolve()) for p in unique)
artifacts=[pin(p) for p in unique]
# Revalidate preserved candidate bytes and complete replay outputs against their
# already-frozen indexes, rather than silently pinning unexpected changed bytes.
for record in load(A/'draft-preservation.json')['artifacts']:
    assert pin(record['preserved']['path'])==record['preserved']
for run in replay['runs']:
    assert all(pin(p['path'])==p for p in run['output_pins'])
started=datetime.datetime.fromisoformat(initial['started_utc'])
delivery={**meta,'summary':'IG-2B07 pages 25-28 inventoried with fresh complete serial evidence, exact inherited preservation, two complete independent replays and passing unchanged validation; hand off for independent source-accounting review.',
          'criteria':task['acceptance'],'criterion_status':[{'criterion':criterion,'status':'pending_independent_review' if i in (2,len(task['acceptance'])-1) else 'executor_evidence_complete_pending_independent_review'} for i,criterion in enumerate(task['acceptance'])],
          'artifacts':artifacts,'checks':checks,'input_packet':pin(SESSION/'packet.json'),'input_pins':inputs,
          'measurement':{'started_utc':initial['started_utc'],'ended_utc':now.isoformat(),'wall_seconds':(now-started).total_seconds(),
                         'operator_seconds':None,'input_tokens':None,'output_tokens':None,'unknown_reason':'Operator time and token usage were not exposed to this executor.'},
          'defects':{'executor_draft_crop_findings':2,'resolved_before_delivery':2,'open_executor_source_accounting_findings':0,'independent_review':'pending'},
          'semantic_acceptance_granted':False,'executable_readiness':'unverified','next_operation':'Independent technical/source-accounting review of the entire immutable manifest and original assigned pages; supervisor owns any next process launch.'}
write(A/'delivery.json',delivery)
print(json.dumps({'delivery':(A/'delivery.json').as_posix(),'sha256':pin(A/'delivery.json')['sha256'],'artifacts':len(artifacts)}))
