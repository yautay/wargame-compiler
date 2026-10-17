"""Run exact required source CLI validations, retain output and actual exits."""
import subprocess
from datetime import datetime, timezone
from build_inventory import ROOT, load, write, pin, metadata

records=[]
for name in ('final-verified','replay-1','replay-2'):
    args=['.venv/Scripts/python.exe','-m','wgc.sources','validate',(ROOT/name/'inventory.json').as_posix()]
    started=datetime.now(timezone.utc).isoformat()
    run=subprocess.run(args,capture_output=True,text=True)
    log=ROOT/(name+'-cli-validation.log')
    log.write_text(run.stdout+'\n'+run.stderr,encoding='utf-8')
    records.append({'command':' '.join(args),'exit_code':run.returncode,'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),'log':pin(log),'root_source_access':True})
    print(name+': CLI validation exit '+str(run.returncode),flush=True)
    assert run.returncode==0
write(ROOT/'source-cli-validation.json',{**metadata(),'summary':'All three exact CLI source-backed validations passed.','checks':records})
