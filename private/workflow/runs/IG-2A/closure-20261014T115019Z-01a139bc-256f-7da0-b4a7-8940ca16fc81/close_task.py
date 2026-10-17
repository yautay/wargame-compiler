"""Operator-authorized technical closure based on immutable independent PASS."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path.cwd(); RUN=Path(__file__).resolve().parent
COORD=ROOT/'private/workflow/runs/IG-2A/coordinator-20261014T114453Z-01a139bc-256f-7da0-b4a7-8940ca16fc81'
REPAIR=ROOT/'private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81'
REVIEW=ROOT/'private/workflow/runs/IG-2A/review-20261014T104443Z-codex-01a13a03-b220-7181-a813-09f6e7b46c1f'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p): return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
def write(name,value): (RUN/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def command(name,argv):
    start=datetime.now(timezone.utc); clock=time.monotonic(); result=subprocess.run(argv,capture_output=True,text=True)
    (RUN/(name+'.stdout')).write_text(result.stdout,encoding='utf-8',newline='\n')
    (RUN/(name+'.stderr')).write_text(result.stderr,encoding='utf-8',newline='\n')
    row={'command':subprocess.list2cmdline(argv),'argv':argv,'exit_code':result.returncode,
         'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
         'wall_seconds':time.monotonic()-clock,'stdout':name+'.stdout','stderr':name+'.stderr'}
    write(name+'.json',row); return row
spec=importlib.util.spec_from_file_location('workflow',ROOT/'scripts/workflow.py'); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
def normalize_governance(update_date=False):
    q=w.read_json(ROOT/w.QUEUE)
    if update_date: q['updated']='2026-10-14'
    (ROOT/w.QUEUE).write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    for path,body in w.views(q).items(): (ROOT/path).write_text(body,encoding='utf-8',newline='\n')
    return q
def phase_accept():
    start=datetime.now(timezone.utc); actor='codex-'+os.environ['CODEX_THREAD_ID']
    config=read(COORD/'configuration.json'); assert config['actor']==actor
    q=w.read_json(ROOT/w.QUEUE); task=next(t for t in q['tasks'] if t['id']=='IG-2A'); assert task['status']=='review'
    for p in (COORD,REVIEW):
        manifest=read(p/('manifest.json' if p==COORD else 'review-final-manifest.json'))
        for a in manifest['artifacts']: assert sha(ROOT/a['path'])==a['sha256'],a['path']
    delivery=read(REPAIR/'delivery.json')
    for a in delivery['artifacts']: assert sha(ROOT/a['path'])==a['sha256']
    write('configuration.json',{'actor':actor,'role':'coordinator','session_id':os.environ['CODEX_THREAD_ID'],
          'model':config['model'],'reasoning':config['reasoning'],'configuration_evidence':pin(COORD/'configuration.json'),'started_utc':start.isoformat()})
    write('operator-authorization.json',{'role':'human_operator','statement':'Tak, zamknij technicznie IG-2A do done',
          'evidence':'Direct user reply to current coordinator question authorizing review -> accepted -> done on IG-2A only',
          'scope':['IG-2A technical accepted','IG-2A technical done'],'IG2B_authorized':False,
          'semantic_acceptance':False,'recorded_utc':start.isoformat(),
          'supersedes':'Earlier prohibition on acceptance/done only for the explicitly authorized technical closure of IG-2A.'})
    (RUN/'queue-before.json').write_bytes((ROOT/w.QUEUE).read_bytes())
    write('governance-before.json',[pin(ROOT/path) for path in w.views(q)])
    write('packet-manifest.json',w.packet(q,ROOT,'IG-2A',output=False))
    accepted=read(COORD/'accepted-proposal.json'); accepted['application_status']='OPERATOR_AUTHORIZED'
    accepted['operator_authorization']=pin(RUN/'operator-authorization.json')
    accepted['prepared_by']={'role':'coordinator','actor':actor,'configuration':pin(RUN/'configuration.json')}
    accepted['proposal_provenance']=pin(COORD/'accepted-proposal.json')
    write('accepted.json',accepted)
    result=command('accepted-transition',[sys.executable,'scripts/workflow.py','transition','--task','IG-2A','--to','accepted','--evidence',(RUN/'accepted.json').relative_to(ROOT).as_posix()])
    assert result['exit_code']==0, 'Inspect queue before retrying a partial transition'
    phase_accepted_checks()
def phase_accepted_checks():
    q=w.read_json(ROOT/w.QUEUE); task=next(t for t in q['tasks'] if t['id']=='IG-2A')
    assert task['status']=='accepted' and task['events'][-1]['sha256']==sha(RUN/'accepted.json')
    q=normalize_governance(update_date=True)
    assert next(t for t in q['tasks'] if t['id']=='IG-2A')['status']=='accepted'
    print('IG-2A accepted; running unchanged project checks before done.',flush=True)
    tc=read(REPAIR/'toolchain.json'); os.environ['PYTHONPATH']=tc['process_pythonpath']
    os.environ['PATH']=tc['process_path_poppler']+os.pathsep+os.environ['PATH']
    os.environ['PYTHONDONTWRITEBYTECODE']='1'
    result=command('project-check',['pwsh','-NoProfile','-File',str(RUN/'check-adapter.ps1')])
    print('Project check exit',result['exit_code'],flush=True)
    assert result['exit_code']==0
    print((RUN/'project-check.stdout').read_text(encoding='utf-8'),flush=True)
def phase_done():
    q=w.read_json(ROOT/w.QUEUE); assert next(t for t in q['tasks'] if t['id']=='IG-2A')['status']=='accepted'
    checks=[read(RUN/'project-check.json'),command('before-done-workflow',[sys.executable,'scripts/workflow.py','validate']),command('before-done-diff',['git','diff','--check'])]
    assert all(c['exit_code']==0 for c in checks)
    done=read(COORD/'done-proposal.json'); done['application_status']='OPERATOR_AUTHORIZED'
    done['operator_authorization']=pin(RUN/'operator-authorization.json')
    done['configuration_evidence']=pin(RUN/'configuration.json')['path']; done['checks']=checks
    done['proposal_provenance']=pin(COORD/'done-proposal.json'); write('done.json',done)
    result=command('done-transition',[sys.executable,'scripts/workflow.py','transition','--task','IG-2A','--to','done','--evidence',(RUN/'done.json').relative_to(ROOT).as_posix()])
    assert result['exit_code']==0, 'Inspect queue before retrying a partial transition'
    phase_finish()
def phase_finish():
    q=w.read_json(ROOT/w.QUEUE); task=next(t for t in q['tasks'] if t['id']=='IG-2A')
    assert task['status']=='done' and task['events'][-1]['sha256']==sha(RUN/'done.json')
    checks=read(RUN/'done.json')['checks']
    q=normalize_governance()
    task=next(t for t in q['tasks'] if t['id']=='IG-2A'); assert task['status']=='done'
    base=read(RUN/'queue-before.json')
    assert [t for t in q['tasks'] if t['id']!='IG-2A']==[t for t in base['tasks'] if t['id']!='IG-2A']
    after=[command('final-workflow',[sys.executable,'scripts/workflow.py','validate']),command('final-diff',['git','diff','--check'])]
    assert all(c['exit_code']==0 for c in after)
    for folder,name in [(COORD,'manifest.json'),(REVIEW,'review-final-manifest.json')]:
        for a in read(folder/name)['artifacts']: assert sha(ROOT/a['path'])==a['sha256'],a['path']
    # Frozen queue/derived pins are historical observations; authorized governance
    # changes are the only intentionally superseded live paths.
    governance=set(w.views(q))|{w.QUEUE}
    delivery=read(REPAIR/'delivery.json')
    for a in delivery['artifacts']: assert sha(ROOT/a['path'])==a['sha256'],a['path']
    for a in read(REPAIR/'final-seal.json')['governance_artifacts']:
        if a['path'] not in governance: assert sha(ROOT/a['path'])==a['sha256']
    end=datetime.now(timezone.utc); config=read(RUN/'configuration.json'); start=datetime.fromisoformat(config['started_utc'])
    write('preservation.json',{'all_273_delivery_artifacts_unchanged':True,'independent_review_and_coordinator_evidence_unchanged':True,
          'other_38_task_records_unchanged':True,'IG2B_not_started_or_marked_ready':True,
          'authorized_governance_changes':['IG-2A accepted/done events','Queue updated date','Generated views'],
          'workflow_tools_unchanged':True})
    write('measurement.json',{'actor':config['actor'],'started_utc':start.isoformat(),'ended_utc':end.isoformat(),
          'wall_seconds':(end-start).total_seconds(),'tokens':None,'cost':None,'operator_seconds':None,
          'unknown_reason':'No task counters/cost/operator time available.'})
    write('checks.json',checks+after)
    (RUN/'closure-handoff.md').write_text(f'''# IG-2A technical closure

IG-2A is done, after operator-authorized review -> accepted -> done through the unchanged workflow. Independent reviewer {read(REVIEW/'review-final.json')['actor']} supplied the PASS; coordinator {config['actor']} verified all 954 review artifacts, all 273 delivery artifacts, all exact criteria and R01-R05 closure evidence before applying transitions. Mandatory acceptance artifacts match the exact delivery list, with supporting reviewer reports separately pinned and decision attribution preserved.

The unchanged project check ran while IG-2A was accepted: 102 tests, workflow validation, task dry-run and diff checks passed. Source-specific 71-test and independent probe results were verified against the unchanged delivery; no product changes justified rerunning them. Final workflow validation and git diff --check passed after done. Output-only check adapter preserves all check logic and keeps logs/scratch in this closure directory.

The accepted transition committed its queue event but its CLI then exited 1 on Windows OSError Errno 22 writing docs/ROADMAP.md. A separate render failed with the same error. The coordinator verified the committed event and installed exact workflow-generated ROADMAP bytes by atomic replacement, preserving its previous bytes in roadmap-before-recovery.md. No transition was repeated and no additional acceptance event was appended. The failed commands and the recovery hypothesis/result are retained in accepted-transition-recovery.json, accepted-render-recovery.json and roadmap-atomic-recovery.json. Subsequent project checks and generated-view validation passed. The underlying Windows write failure's specific cause was not observed.

The done transition also committed its authorized queue event before the same ROADMAP projection write error. done-transition-recovery.json records verification of that exact event/evidence and projection-only atomic recovery. No done transition was repeated. Final workflow and diff checks passed against the actual done queue and regenerated projections.

All prior product/delivery/reviewer/coordinator evidence bytes are unchanged. Queue updated date is 2026-10-14; its two authorized events and generated views changed. The other 38 task records are unchanged, including all IG-2B states. No downstream readiness promotion or execution occurred.

This is technical tooling completion. All 44 source placeholders remain substantively unprocessed; source-IG exclusions/human authority are not approved by this closure. Source meaning, semantic acceptance, compilation and gameplay readiness remain separate. No commit/push, external API, new chat or agent occurred in this closure.

UTC {start.isoformat()} to {end.isoformat()}; elapsed {(end-start).total_seconds():.3f} seconds. Tokens, cost and operator time are null. Next operation requires a separate instruction for the next bounded task; do not infer authorization to execute IG-2B.
''',encoding='utf-8',newline='\n')
    gov=[pin(ROOT/path) for path in [w.QUEUE,*w.views(q)]]
    write('governance-manifest.json',{'task':'IG-2A','status':'done','artifacts':gov})
    artifacts=[]
    for p in sorted(RUN.rglob('*')):
        if not p.is_file() or p.relative_to(RUN).parts[:2] in [('c','pytest'),('c','temp')]: continue
        if p.name in {'manifest.json','final-seal.json'}: continue
        artifacts.append(pin(p))
    write('manifest.json',{'task':'IG-2A','status':'done','actor':config['actor'],'artifacts':artifacts,
          'excluded_operational_scratch':['c/pytest/','c/temp/']})
    write('final-seal.json',{'task':'IG-2A','status':'done','actor':config['actor'],'manifest':pin(RUN/'manifest.json'),
          'handoff':pin(RUN/'closure-handoff.md'),'accepted':pin(RUN/'accepted.json'),'done':pin(RUN/'done.json'),
          'operator_authorization':pin(RUN/'operator-authorization.json'),'queue':pin(ROOT/w.QUEUE),
          'independent_review_seal':pin(REVIEW/'final-seal-corrected.json'),'checks':checks+after,
          'semantic_acceptance_granted':False,'IG2B_executed':False,'ended_utc':end.isoformat()})
    print('IG-2A done; all checks pass, frozen evidence preserved and other 38 tasks unchanged.',flush=True)

if __name__=='__main__':
    if sys.argv[1]=='accept': phase_accept()
    elif sys.argv[1]=='accepted-checks': phase_accepted_checks()
    elif sys.argv[1]=='done': phase_done()
    elif sys.argv[1]=='finish': phase_finish()
    else: raise ValueError('Expected accept or done phase')
