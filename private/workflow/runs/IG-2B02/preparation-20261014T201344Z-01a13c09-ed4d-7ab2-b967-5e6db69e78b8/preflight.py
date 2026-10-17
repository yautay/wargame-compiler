import runpy, os, sys
from pathlib import Path
r=Path(__file__).resolve().parent
m=runpy.run_path(str(r/'prepare-refined.py')); cmd=m['command']; write=m['write']; pin=m['pin']; read=m['read']
write('preflight-launch-failure.json',{'command':'Inline preflight runner using runpy.run_path(relative script path)','exit_code':1,'error':'ValueError: relative __file__ parent is not in the subpath of absolute cwd','impact':'No checks or status transition ran in failed launch.','resolution':'Supply resolved absolute path to runpy; no repository tool was changed.'})
env=os.environ.copy(); t=read(r/'toolchain.json'); env['PYTHONPATH']=t['process_pythonpath']; env['PATH']=t['process_path_prefix']+';'+env['PATH']; env['PYTHONDONTWRITEBYTECODE']='1'
checks=[]
for n,a in [('refined-render',[sys.executable,'-B','scripts/workflow.py','render']),('refined-validate',[sys.executable,'-B','scripts/workflow.py','validate']),('baseline-root-validate',[sys.executable,'-B','-m','wgc.sources','validate',str(m['B']/'final-verified/inventory.json')])]:
    c=cmd(n,a,env); checks.append(c); assert c['exit_code']==0
q=read('docs/work/queue.json'); before=read(r/'queue-before.json')
assert [t for t in q['tasks'] if t['id']!='IG-2B02']==[t for t in before['tasks'] if t['id']!='IG-2B02']
sys.path.insert(0,'scripts'); import workflow
task=next(t for t in q['tasks'] if t['id']=='IG-2B02')
paths=list(dict.fromkeys(workflow.BASE_CONTEXT+['docs/work/tasks/IG-2B02.md']+task['context']))
sections=[]
for rel in paths:
    assert workflow.permitted(Path.cwd(),rel)
    p=Path(rel)
    if p.suffix.lower() in {'.md','.json','.py','.ps1','.toml'}: sections.append('\n--- FILE: '+rel+' ---\n'+p.read_text(encoding='utf-8-sig'))
size=len('\n'.join(sections).encode('utf-8')); assert size<=100000
write('readiness-preflight.json',{'context_bytes':size,'paths':paths,'other_38_tasks_unchanged':True,'no_claim':True,'checks':checks})
write('ready.json',{'role':'coordinator','actor':m['ACTOR'],'summary':'IG-2B02 refined and eligible for readiness only: exact verified IG-2B01 closure, source/accepted contract/registry pins, full structural representation, bounded continuation context and reserved absent executor scope. No claim or authoring.','model':None,'reasoning':None,'configuration_evidence':pin(r/'configuration.json') | {'path':(m['RUN']/'configuration.json').as_posix()},'criteria':task['acceptance'],'artifacts':[pin(m['RUN']/p) for p in ['configuration.json','dependency-verification.json','source-pins.json','scope.json','toolchain.json','refinement.json','readiness-preflight.json']],'checks':checks,'semantic_acceptance_granted':False})
print('preflight bytes',size,'immutable dependency pins',read(r/'dependency-verification.json')['immutable_files_verified'])
