from reviewer import *
import importlib.metadata, shutil
bundle=Path('C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies')
site=bundle/'python/Lib/site-packages'
sys.path.insert(0,str(site))
env=os.environ.copy()
env['PYTHONPATH']=str(ROOT/'src')+os.pathsep+str(site)
env['PYTHONDONTWRITEBYTECODE']='1'
env['GIT_OPTIONAL_LOCKS']='0'
env['PATH']=str(bundle/'native/poppler/Library/bin')+os.pathsep+env['PATH']
baseline=read(REPAIR/'toolchain.json')
native={}
for name,args in [('pdfinfo',['-v']),('pdftoppm',['-v']),('pwsh',['--version']),('git',['--version'])]:
    p=Path(baseline['native'][name]['executable']['path'])
    record=run('version-'+name,[str(p),*args],env)
    native[name]=dict(executable=pin(p),check=record,baseline_hash_match=pin(p)['sha256']==baseline['native'][name]['executable']['sha256'])
write('toolchain.json',dict(observed_utc=utc(),python=sys.version,python_executable=pin(Path(sys.executable)),libraries={n:importlib.metadata.version(n) for n in ['pypdf','pdfplumber','Pillow','pytest']},native=native,process_environment={k:env[k] for k in ['PATH','PYTHONPATH','PYTHONDONTWRITEBYTECODE','GIT_OPTIONAL_LOCKS']},global_configuration_changed=False,initial_probe_failure='Before process-only PYTHONPATH setup, an import probe raised ModuleNotFoundError: pypdf. Resolved using existing bundled libraries; no installation.'))
short=ROOT/'private/workflow/checks/rr8d-20261015T123502Z'
short.mkdir(exist_ok=False)
commands=[('sources-tests',[sys.executable,'-m','pytest','tests/sources','-q','--basetemp',str(short/'s'),'-p','no:cacheprovider','--tb=short']),('root-inventory-validate',[sys.executable,'-m','wgc.sources','validate',(REPAIR/'final-verified/inventory.json').relative_to(ROOT).as_posix()]),('workflow-validate',[sys.executable,'scripts/workflow.py','validate']),('project-check',[baseline['native']['pwsh']['executable']['path'],'-NoProfile','-File','scripts/check.ps1','-Task','IG-2B02']),('git-diff-check',['git','diff','--check'])]
checks=[]
for name,args in commands:
    r=run(name,args,env); checks.append(r)
    print(name,r['exit_code'],round(r['wall_seconds'],2),flush=True)
write('required-checks.json',dict(checks=checks,retries=0,retry_limit=2,unchanged_source_tools_and_tests=True,completed_utc=utc()))
