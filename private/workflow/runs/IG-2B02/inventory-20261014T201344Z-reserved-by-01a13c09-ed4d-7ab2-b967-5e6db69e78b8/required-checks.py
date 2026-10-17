from ops import *
doc=load(AR+'/final-verified/inventory.json');assert (A/'locator-audit.json').is_file()
checks=[]
for label,args in [('final-root-validate',[PY,'-B','-m','wgc.sources','validate',AR+'/final-verified/inventory.json']),('repository-check',[PW,'-NoProfile','-File','scripts/check.ps1','-Task','IG-2B02']),('final-workflow-validate',[PY,'-B','scripts/workflow.py','validate']),('final-diff-check',['git','diff','--check'])]:
 c=run(label,args);checks.append(c)
 if c['exit_code']!=0:
  checkpoint('check-failed-'+label,['Final inventory, preservation, replay and locator audit'],'Reproduce bounded failure and escalate without modifying frozen checks',{'command':args,'exit_code':c['exit_code'],'logs':[c['stdout'],c['stderr']]});raise RuntimeError(label+' failed; no automatic retry')
for f in ('source-tests','replay-one','replay-two','finalize-run','audit-run'):
 c=load(AR+'/'+f+'.command.json');assert c['exit_code']==0;checks.append(c)
write('required-checks.json',checks)
stdout=(A/'repository-check.stdout').read_text(encoding='utf-8-sig')
line=next(line for line in stdout.splitlines() if line.startswith('LOG_ROOT='));root=Path(line[len('LOG_ROOT='):]);assert root.resolve().is_relative_to((R/'private/workflow/checks').resolve())
result=json.loads((root/'result.json').read_text(encoding='utf-8-sig'));assert all(result[k]==0 for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
write('repository-check-output-pins.json',{'root':root.relative_to(R).as_posix(),'result':result,'outputs':[pin(p) for p in root.iterdir() if p.is_file()],'fixture_policy':'Synthetic pytest basetemp/temp files are operational fixtures, not submitted product/review deliverables; required check logs/result are pinned.'})
checkpoint('checks-passed',['Four executor criteria implemented','All exact locators, replay, preservation and required unchanged checks passed'],'Freeze complete review delivery manifest/handoff, transition in_progress to review once, inspect event/hash, write final seal and stop')
print('REQUIRED CHECKS PASSED')
