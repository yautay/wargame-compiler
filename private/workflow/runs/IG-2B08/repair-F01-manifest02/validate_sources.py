"""Run every required source-backed inventory CLI validation unchanged."""
import subprocess,json
from build_inventory import ROOT,load,write,pin,metadata

checks=[]
for name in ('final-verified','replay-1','replay-2'):
    path=ROOT/name/'inventory.json'
    args=['.venv/Scripts/python.exe','-m','wgc.sources','validate',path.as_posix()]
    result=subprocess.run(args,capture_output=True,text=True)
    log=ROOT/f'{name}-cli-validation.log'
    log.write_text(result.stdout+result.stderr,encoding='utf-8')
    checks.append({'command':' '.join(args),'exit_code':result.returncode,'log':pin(log)})
    assert result.returncode==0,result.stdout+result.stderr
    doc=load(path)
    assert doc['registry']==load(ROOT/name/'identity-registry.json')
write(ROOT/'source-cli-validation.json',{**metadata(),'summary':'All three inventories passed unchanged CLI validation with actual repository/source access and matching companion registries.','checks':checks})
print(json.dumps({'source_cli_validation':'pass','inventories_validated':len(checks)}))
