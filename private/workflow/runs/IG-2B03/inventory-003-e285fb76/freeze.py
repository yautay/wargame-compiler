"""Create one immutable executor delivery envelope; transition is separate."""
import pathlib,json,datetime,hashlib,re
from author import OUT, ROOT, META
from wgc.sources.inventory import file_pin
from wgc.contracts.source import canonical_bytes

def pin(path):return file_pin(ROOT,path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix())
def save(path,data):
 with path.open('xb') as stream:stream.write(canonical_bytes(data)+b'\n')

def main():
 config=pathlib.Path(META['configuration_evidence']);assert pin(config)['sha256']==META['configuration_sha256']
 task=json.loads((config.parent/'task.json').read_text());queue=json.loads(pathlib.Path('docs/work/queue.json').read_text());current=next(t for t in queue['tasks'] if t['id']=='IG-2B03')
 assert current['status']=='in_progress' and current['events'][-1]['evidence']==(OUT/'claim.json').relative_to(ROOT).as_posix()
 doc=json.loads((OUT/'final-verified/inventory.json').read_text());cover=json.loads((OUT/'coverage-report.json').read_text());rep=json.loads((OUT/'registry-replay-report.json').read_text());assert len(rep['runs'])==3
 checks=[
  {'command':'.venv/Scripts/python.exe -B -m wgc.sources validate private/workflow/runs/IG-2B03/inventory-003-e285fb76/final-verified/inventory.json','exit_code':0,'report':pin(OUT/'final-validation.log')},
  {'command':'.venv/Scripts/python.exe -B -m pytest -q tests/sources --basetemp private/workflow/checks/b03-004a -p no:cacheprovider --tb=short','exit_code':0,'report':pin(OUT/'sources-tests.log'),'result':'71 passed','permissions':'approved exact unchanged execution after restricted-token WinError 5'},
  {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B03','exit_code':0,'report':pin(OUT/'project-check.log'),'result':'151 passed; plan=0 dry-run=0 pytest=0 diff=0','permissions':'approved exact unchanged execution after restricted-token WinError 5'},
  {'command':'.venv/Scripts/python.exe -B scripts/workflow.py validate','exit_code':0,'report':pin(OUT/'workflow-validation.log')},
  {'command':'git diff --check','exit_code':0,'report':pin(OUT/'diff-check.log')},
  {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/inventory-003-e285fb76/author.py','exit_code':0,'result':'135 disjoint regions; internally validated full inventory'},
  {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/inventory-003-e285fb76/derive.py','exit_code':0,'report':pin(OUT/'registry-replay-report.json'),'result':'Final and both fresh evidence replays root-validated; canonical authored bytes and IDs equal'},
  {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/inventory-003-e285fb76/report.py','exit_code':0,'report':pin(OUT/'preservation-report.json'),'result':'Exact preservation, all current locators, rational crops, IHDR sizes and explicit gaps verified'}]
 # Successful logs and their result records must substantiate each claimed exit.
 assert '71 passed' in (OUT/'sources-tests.log').read_text(encoding='utf-8-sig')
 project=(OUT/'project-check.log').read_text(encoding='utf-8-sig');assert '151 passed' in project
 project_root=re.search(r'LOG_ROOT=(.+)',project)[1].strip()
 result=json.loads((pathlib.Path(project_root)/'result.json').read_text(encoding='utf-8-sig'));assert all(result[k]==0 for k in ['diff_exit','tests_exit','dry_run_exit','plan_exit'])
 save(OUT/'validation-evidence.json',dict(META,checks=checks,restricted_attempts=[{'command':checks[1]['command'],'exit_code':1,'report':pin(OUT/'sources-tests-restricted.log'),'failure':'WinError 5 accessing mode-0700 basetemp; exact unchanged approved retry passed.'},{'command':checks[2]['command'],'exit_code':1,'report':pin(OUT/'project-check-restricted.log'),'failure':'WinError 5 accessing mode-0700 basetemp; exact unchanged approved retry passed.'}],project_result=pin(pathlib.Path(project_root)/'result.json'),changes_to_tests_tools_acl_or_assertions=[]))
 handoff='''# IG-2B03 executor handoff

The full 44-page sidecar now inventories physical pages 9-12 with 135 new regions
(27 / 25 / 42 / 41). The complete region ledger preserves both-column order,
numbered and bulleted items, notes, exceptions, examples, counter components and
editorial furniture. Four literal page/column continuations are linked. Raw
cross-chapter citations remain unresolved and were not followed.

All accepted nested records outside replaced placeholder memberships are unchanged.
All inherited evidence and links, existing context and registry bindings are kept;
retired placeholder bindings remain persisted. All 4,409 artifacts pinned by the
accepted dependency event match their hashes. Only page-label evidence and enclosing
page revisions changed on pages 9-12. No other source content was analyzed.

Every new region has exact text/PNG/crop-PDF evidence, current page-basis and revision
pins, Unicode offsets, rational crop bounds and checked PNG IHDR dimensions.
Two fresh registry replays reproduce identical canonical authored bytes and IDs;
each distinct evidence output root-validates independently. Geometric and all
transcription/descriptive/formal representation gaps remain explicit. Components
are raster sublocator annotations and add zero denominator units. Optional page-8
context was not needed and contributes zero task units.

Validation: 71 source tests and 151 repository tests passed. The initial restricted
attempts hit Windows mode-0700 temporary-directory access errors; approved execution
of the exact unchanged commands passed. No tests, tools, ACLs, libraries, assertions
or global settings changed. Root source validation, workflow validation and
git diff --check passed.

Next action: a fresh independent reviewer inspects every original assigned page,
all 135 region boundaries and both counters' components against region-ledger.json,
checks every frozen artifact and preservation report, and reviews the exact hashes.
Executor self-inspection does not satisfy that independent review criterion.
No human semantic acceptance or executable gameplay readiness is granted.
The executor stops after entering review; only the supervisor launches another role.
'''
 with (OUT/'delivery-handoff.md').open('x',encoding='utf-8',newline='\n') as stream:stream.write(handoff)
 # Freeze every file created in this owned attempt, including raw logs, page renders,
 # authored/replay snapshots and all current evidence. The envelope itself is pinned
 # by the queue transition event and cannot include its own hash.
 artifacts=[];seen=set()
 def add(a):
  if a['path'] not in seen:artifacts.append(a);seen.add(a['path'])
 for path in sorted(OUT.rglob('*')):
  if path.is_file() and path.name not in ['delivery.json','delivery-manifest.json']:add(pin(path))
 for e in doc['evidence']:
  for k in ['text','image','crop_pdf']:add(e[k])
 for a in [doc['source']['pdf'],doc['source']['provenance'],pin(config),pin(config.parent/'packet.json'),pin(config.parent/'task.json'),pin(config.parent/'references.json'),pin(pathlib.Path(project_root)/'result.json')]:add(a)
 for path in ['tests/sources/test_inventory.py','tests/sources/test_review_repairs.py','scripts/check.ps1','src/wgc/sources/inventory.py','src/wgc/sources/pdf.py','src/wgc/sources/geometry.py','contracts/ig/regions.schema.json']:
  add(pin(pathlib.Path(path)))
 for a in artifacts:assert file_pin(ROOT,a['path'])==a
 save(OUT/'delivery-manifest.json',dict(META,format='wgc-ig2b03-delivery-manifest-1',artifacts=artifacts,policy='All owned files, all inherited and new inventory evidence and exact input/runtime/check pins. No mutable queue projection is frozen. Envelope and this manifest are pinned separately to avoid circular hashes.'))
 artifacts.append(pin(OUT/'delivery-manifest.json'))
 start=json.loads((OUT/'checkpoint-start.json').read_text())['started_utc'];end=datetime.datetime.now(datetime.timezone.utc);elapsed=int((end-datetime.datetime.fromisoformat(start)).total_seconds())
 results=[{'criterion':c,'executor_status':('pending_independent_review' if c.startswith('Independent review') or 'fresh independent reviewer' in c.lower() else 'executor_evidence_ready'),'basis':'Frozen complete ledger, locators, coverage, visual self-inspection, preservation and replay reports; fresh independent review remains required.'} for c in task['acceptance']]
 save(OUT/'delivery.json',dict(META,summary='Inventory pages 9-12 delivered: 135 independent regions, complete byte-pinned evidence, preserved full sidecar and two validated registry replays. Ready for fresh independent technical review.',criteria=task['acceptance'],criteria_results=results,artifacts=artifacts,checks=checks,input_packet=pin(config.parent/'packet.json'),semantic_acceptance_granted=False,executable_readiness='unverified',independent_review='pending',remaining_gates=['Fresh independent technical review of exact frozen bytes and every original assigned page/region/component.','Later source-IG reconciliation and human semantic acceptance are separate from inventory accounting.'],measurement={'started_utc':start,'ended_utc':end.isoformat(),'wall_seconds':elapsed,'input_tokens':None,'output_tokens':None,'operator_seconds':None,'unknown_reason':'Token usage and operator time are not exposed to this executor.'},immutability='Delivery artifacts are frozen by path, byte count and SHA-256. Do not overwrite; repairs require a new attempt/envelope.'))
 print((OUT/'delivery.json').relative_to(ROOT).as_posix())

if __name__=='__main__':main()
