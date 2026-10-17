from pathlib import Path
import sys
root=Path.cwd()
sys.path.insert(0,str(root/'scripts'))
import orchestrate_ig2 as o
session=Path(__file__).parent/'session'
session.mkdir(exist_ok=False)
prompt="This is an operator-authorized V01 permissions validation probe only. Do not change queue, source, tests, dependencies, ACLs or existing attempts. No nested agents, external services or history reads.\nFirst read the runtime-configuration.json in your session directory and require supervisor-confirmed gpt-6.1-sol/high.\nRun the UNCHANGED tests/sources suite once with fresh basetemp under private/workflow/checks/v01-approved-probe-<unique>, -p no:cacheprovider and --tb=short. Use the existing .venv/Scripts/python.exe, PYTHONPATH=C:/repo/wargame-compiler/src and prepend C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin to process PATH. Save command, exit code, stdout/stderr under this probe session. The Windows restricted token cannot access pytest mode0700 directories: request sandbox_permissions=require_escalated for this exact unchanged test command with the user's authorized V01 reason. Automatic approval is enabled. Do not first repeat the known failing restricted-token invocation. Verify no source/test files changed. Return progress with evidence path if the permitted command exits zero; otherwise blocked with exact reason. Do not grant IG-2 acceptance."
prompt+='\nYour session directory is '+session.relative_to(root).as_posix()
try:
 result=o.launch('codex',root,session,prompt,300)
 o.dump(session/'probe-result.json',result)
 print(result,flush=True)
except Exception as e:
 o.dump(session/'probe-result.json',{'outcome':'blocked','summary':str(e)})
 raise
