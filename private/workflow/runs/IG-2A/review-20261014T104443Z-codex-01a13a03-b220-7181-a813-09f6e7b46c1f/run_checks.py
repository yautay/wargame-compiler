from support import *
checks=[]
checks.append(command('sources-tests',[PYTHON,'-m','pytest','tests/sources','-q','--basetemp',RUN/'t','-p','no:cacheprovider','--tb=short']))
checks.append(command('project-check',['pwsh','-NoProfile','-File',RUN/'check-adapter.ps1']))
checks.append(command('workflow-validate',[PYTHON,'scripts/workflow.py','validate']))
checks.append(command('git-diff-check',['git','diff','--check']))
write('required-checks.json',checks)
assert all(c['exit_code']==0 for c in checks)
