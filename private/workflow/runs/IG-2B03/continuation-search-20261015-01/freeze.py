"""Freeze this one executor delivery after all builders and reports complete."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from build import ROOT, OUT, SESSION, SCOPE, COMMON, load, write
from wgc.sources.inventory import file_pin

def main():
    task=load(SESSION/'task.json');config=load(COMMON['configuration_evidence'])
    assert config['status']=='confirmed' and config['model']==COMMON['model'] and config['reasoning']==COMMON['reasoning']
    assert file_pin(ROOT,COMMON['configuration_evidence'])['sha256']==COMMON['configuration_sha256']
    queue=load('docs/work/queue.json')
    current=next(t for t in queue['tasks'] if t['id']=='IG-2B03')
    assert current['status']=='in_progress' and current['events'][-1]['evidence']==(OUT/'claim.json').as_posix()
    assert all(next(t for t in queue['tasks'] if t['id']==dep)['status']=='done' for dep in task['depends'])
    cmd=['.venv/Scripts/python.exe','-B','-m','wgc.sources','validate',(OUT/'final-verified/inventory.json').as_posix()]
    result=subprocess.run(cmd,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    write(OUT/'cli-validation.json',{**COMMON,'command':' '.join(cmd),'exit_code':result.returncode,'result':json.loads(result.stdout),'stderr':result.stderr})
    result2=subprocess.run(['.venv/Scripts/python.exe','-B','scripts/workflow.py','validate'],capture_output=True,text=True)
    assert result2.returncode==0,result2.stderr
    checks=load(OUT/'test-report.json')['checks']+[
      {'command':' '.join(cmd),'exit_code':0,'report':(OUT/'cli-validation.json').as_posix()},
      {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/continuation-search-20261015-01/build.py','exit_code':0,'result':'Three complete independently validated evidence builds; two complete independent replays.'},
      {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/continuation-search-20261015-01/components.py','exit_code':0,'result':'22 fresh source-pinned zero-denominator component locators.'},
      {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/continuation-search-20261015-01/components_replay.py','exit_code':0,'result':'Two complete component replays; each independently validated.'},
      {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/continuation-search-20261015-01/preserve_order.py','exit_code':0,'result':'Accepted inherited region-array order restored before freeze in all builds; all complete current evidence outputs revalidated. Individual records, evidence artifact bytes, explicit IDs and reading order unchanged.'},
      {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/continuation-search-20261015-01/geometry_audit.py','exit_code':0,'result':'All four assigned pages: zero nonspace character boxes outside region boundaries.'},
      {'command':'.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/continuation-search-20261015-01/reports.py','exit_code':0,'result':'Coverage, complete ledger, visual, preservation, source/tool and replay assertions passed.'}]
    coverage=load(OUT/'coverage-report.json');preserved=load(OUT/'preservation-report.json')
    started=load(OUT/'checkpoint.json')['started_utc'];ended=datetime.now(timezone.utc).isoformat()
    measurement={'started_utc':started,'ended_utc':ended,'elapsed_wall_seconds':int((datetime.fromisoformat(ended)-datetime.fromisoformat(started)).total_seconds()),'input_tokens':None,'output_tokens':None,'token_unknown_reason':'Session token telemetry is not exposed to this role.','operator_seconds':None,'operator_time_unknown_reason':'Not reported.','independent_reviewer':None,'observed_executor_defects_by_severity':{'minor':1},'defect_basis':'One pre-freeze packaging issue: inherited region records were unchanged but their array order was reordered. preserve_order.py restores exact accepted array order and reruns complete validation. No independent review findings have been issued for this delivery.','environment_validation_failures_recovered':2}
    write(OUT/'checkpoint-02.json',{**COMMON,'input_packet':file_pin(ROOT,(SESSION/'packet.json').as_posix()),'summary':'Fresh original-page/boundary/component inspection, complete evidence and two independent replays, source/repository checks and preservation comparisons completed.','completed_criteria':task['acceptance'],'criteria_pending_external_review':[task['acceptance'][2],task['acceptance'][7]],'checks':checks,'measurement':measurement,'blocker':None,'next_operation':'Freeze delivery and transition this task to independent review; supervisor owns next session.'})
    handoff='''# IG-2B03 executor delivery\n\nFresh inventory of original physical pages 9-12, with 135 source regions and 22 separately pinned counter-component observations. The 44-page sidecar and all prior accepted scope are retained. No rule meaning or gameplay legality was decided.\n\n## Validation\n\n- Every original assigned page, both columns, all region rectangles and counter components were inspected in this session.\n- Main build plus two complete independent evidence replays validate against exact source bytes. Canonical author inventory/registry bytes and IDs match; path-dependent final evidence is validated separately. Components also have two complete independent replays.\n- Unchanged source suite: 71 passed. Unchanged repository check: 184 passed; plan, dry run and diff check passed. Restricted-token pytest failures were resolved by approved execution of the exact unchanged commands, with no test/tool/ACL changes.\n- All unassigned page/region records, old evidence/links, registry bindings and old artifacts remain exact. Geometric gaps and all unprocessed representation gaps stay explicit.\n\n## Review request\n\nA fresh independent reviewer must compare original pages 9-12 against every entry and boundary in region-ledger.json and component-ledger.json, verify all frozen artifacts, continuations, source locators, all three builds and preservation-report.json. Optional page-8 content was not accessed; it contributes zero task denominator. No page 13 or cross-chapter source was opened. Raw citations remain unresolved.\n\nTranscription, descriptive semantics and formal semantics remain unprocessed for this increment. Editorial classification grants no exclusion. Source import/accounting, coverage, human semantic acceptance and executable readiness remain separate. Technical acceptance and semantic acceptance are not granted by this executor.\n\nThe next action is a supervisor-launched independent reviewer session. Stop this executor role after transition to review.\n'''
    with (OUT/'delivery-handoff.md').open('x',encoding='utf-8',newline='\n') as stream:stream.write(handoff)
    # Enumerate only exact files created here and pinned evidence references; no tree search.
    paths=[]
    def own(relative):paths.append((OUT/relative).as_posix())
    for name in ('build.py','components.py','components_replay.py','preserve_order.py','geometry_audit.py','reports.py','freeze.py','checkpoint.json','claim.json','checkpoint-02.json','partition-plan.json','component-ledger.json','region-ledger.json','continuations.json','coverage-report.json','visual-review.json','preservation-report.json','registry-replay-report.json','source-pins.json','toolchain.json','test-report.json','text-geometry-audit.json','cli-validation.json','delivery-handoff.md'):own(name)
    for n in (9,10,11,12):
        for name in (f'page-{n:02}.png',f'boundaries-{n:02}.png',f'page-{n:02}-left.png',f'page-{n:02}-right.png'):own('original-pages/'+name)
    for n in (9,11):own(f'original-pages/counter-{n:02}.png')
    for name in ('authored','replay-a-authored','replay-b-authored'):
        for f in ('inventory.json','identity-registry.json'):own(name+'/'+f)
    for name in ('final-verified','replay-a-verified','replay-b-verified'):
        for f in ('inventory.json','identity-registry.json','coverage.json','validation.json'):own(name+'/'+f)
        doc=load(OUT/name/'inventory.json')
        for ev in doc['evidence']:
            paths.extend(ev[k]['path'] for k in ('text','image','crop_pdf'))
    for name in ('components','components-replay-a','components-replay-b'):
        for f in ('authored-inventory.json','identity-registry.json','inventory.json','validation.json'):own(name+'/'+f)
        for ev in load(OUT/name/'inventory.json')['evidence']:
            paths.extend(ev[k]['path'] for k in ('text','image','crop_pdf'))
    own('components/contact-sheet.png')
    paths.extend(r['path'] for r in load(SCOPE['input_pins']['path'])['files'])
    paths.extend([COMMON['configuration_evidence'],(SESSION/'packet.json').as_posix(),(SESSION/'task.json').as_posix(),(SESSION/'references.json').as_posix(),SCOPE['input_pins']['path'],SCOPE['toolchain']['path'],SCOPE['accepted_dependency']['path'],SCOPE['preserve_manifest']['path'],SCOPE['assessment']['path'],'private/workflow/runs/IG-2B03/recovery-20261015-search-01/scope.json','private/workflow/runs/IG-2B03/recovery-20261015-search-01/authorization.json'])
    for check in checks:
        for pin in check.get('reports',[]):paths.append(pin['path'])
    artifacts=[file_pin(ROOT,p) for p in dict.fromkeys(paths)]
    write(OUT/'delivery-manifest.json',{**COMMON,'format':'wgc-delivery-manifest-1','artifacts':artifacts,'immutability':'All listed bytes are frozen. This manifest is pinned by delivery.json, which is pinned by the queue review event. Neither file includes its own hash. Old accepted artifacts are referenced/verified without mutation.','input_packet':file_pin(ROOT,(SESSION/'packet.json').as_posix())})
    artifacts=artifacts+[file_pin(ROOT,(OUT/'delivery-manifest.json').as_posix())]
    write(OUT/'delivery.json',{**COMMON,'summary':'Fresh IG-2B03 pages 9-12 inventory and source evidence, complete region/component ledgers, two independent main and component replays, preservation and passing checks frozen for fresh independent review.','criteria':task['acceptance'],'criteria_results':[{'criterion':c,'executor_result':'delivered for fresh independent source/technical review','independent_review':'pending' if i in (2,7) else 'required before acceptance'} for i,c in enumerate(task['acceptance'])],'artifacts':artifacts,'checks':checks,'input_packet':file_pin(ROOT,(SESSION/'packet.json').as_posix()),'counts':{'full_physical_pages':44,'task_denominator':coverage['task']['denominator_regions'],'component_context_locators':22,'main_complete_builds':3,'component_complete_builds':3},'preservation':preserved,'measurement':measurement,'semantic_acceptance_granted':False,'technical_acceptance_granted':False,'executable_readiness':'unverified','remaining_gates':['Fresh independent original-page and complete-ledger technical review.','Later exact source-IG reconciliation and separately authorized human semantic acceptance.'],'next_action':'Supervisor launches fresh independent reviewer for this frozen delivery.'})
    # Confirm complete frozen list and prior blocked evidence immediately before handoff.
    for r in artifacts:assert file_pin(ROOT,r['path'])==r,r['path']
    for r in load(SCOPE['preserve_manifest']['path'])['artifacts']:
        a=file_pin(ROOT,r['path']);assert all(a[k]==v for k,v in r.items() if k in ('path','bytes','sha256')),r['path']
    print('Frozen delivery:',(OUT/'delivery.json').as_posix(),'artifacts:',len(artifacts))

if __name__=='__main__':main()
