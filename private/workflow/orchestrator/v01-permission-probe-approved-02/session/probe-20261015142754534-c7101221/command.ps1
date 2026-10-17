$ErrorActionPreference = 'Continue'
$env:PYTHONPATH = 'C:/repo/wargame-compiler/src'
$env:PATH = 'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin;' + $env:PATH
$env:PYTHONDONTWRITEBYTECODE = '1'
$probeStarted = [DateTime]::UtcNow.ToString('o')
& 'C:/repo/wargame-compiler/.venv/Scripts/python.exe' -m pytest tests/sources --basetemp 'C:/repo/wargame-compiler/private/workflow/checks/v01-approved-probe-20261015142754534-c7101221/pytest' -p no:cacheprovider --tb=short 1> 'C:/repo/wargame-compiler/private/workflow/orchestrator/v01-permission-probe-approved-02/session/probe-20261015142754534-c7101221/stdout.log' 2> 'C:/repo/wargame-compiler/private/workflow/orchestrator/v01-permission-probe-approved-02/session/probe-20261015142754534-c7101221/stderr.log'
$probeExit = $LASTEXITCODE
$probeExit | Set-Content -LiteralPath 'C:/repo/wargame-compiler/private/workflow/orchestrator/v01-permission-probe-approved-02/session/probe-20261015142754534-c7101221/exit-code.txt' -Encoding utf8
[ordered]@{command_file='C:/repo/wargame-compiler/private/workflow/orchestrator/v01-permission-probe-approved-02/session/probe-20261015142754534-c7101221/command.ps1'; exit_code=$probeExit; started_utc=$probeStarted; ended_utc=[DateTime]::UtcNow.ToString('o'); basetemp='C:/repo/wargame-compiler/private/workflow/checks/v01-approved-probe-20261015142754534-c7101221/pytest'; runtime_configuration='private/workflow/orchestrator/v01-permission-probe-approved-02/session/runtime-configuration.json'; model='gpt-6.1-sol'; reasoning='high'; semantic_acceptance=$false} | ConvertTo-Json | Set-Content -LiteralPath 'C:/repo/wargame-compiler/private/workflow/orchestrator/v01-permission-probe-approved-02/session/probe-20261015142754534-c7101221/result.json' -Encoding utf8
Write-Output ('PROBE_EXIT=' + $probeExit)
Write-Output 'EVIDENCE=C:/repo/wargame-compiler/private/workflow/orchestrator/v01-permission-probe-approved-02/session/probe-20261015142754534-c7101221'
exit $probeExit
