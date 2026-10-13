param([string]$Python = '', [string]$Task = '')
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not $Python) { $Python = Join-Path $repoRoot '.venv\Scripts\python.exe' }
if (-not (Test-Path -LiteralPath $Python)) { throw 'Specify an existing interpreter with pytest using -Python.' }
$runRoot = Join-Path $repoRoot ('private\workflow\checks\active-' + [guid]::NewGuid().ToString('N'))
$baseTemp = Join-Path $runRoot 'pytest'
if ((Test-Path -LiteralPath $runRoot) -or (Test-Path -LiteralPath $baseTemp)) { throw 'The check directory must be new.' }
$savedTemp = $env:TEMP
$savedTmp = $env:TMP
$savedBytecode = $env:PYTHONDONTWRITEBYTECODE
$savedLocks = $env:GIT_OPTIONAL_LOCKS
Push-Location -LiteralPath $repoRoot
try {
    New-Item -ItemType Directory -Path (Join-Path $runRoot 'temp') | Out-Null
    $env:TEMP = Join-Path $runRoot 'temp'
    $env:TMP = $env:TEMP
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:GIT_OPTIONAL_LOCKS = '0'
    Write-Output ('LOG_ROOT=' + $runRoot)
    & $Python scripts/workflow.py validate 2>&1 | Tee-Object -FilePath (Join-Path $runRoot 'plan.log')
    $planCode = $LASTEXITCODE
    if (-not $Task) {
        $queue = Get-Content -LiteralPath 'docs/work/queue.json' -Raw | ConvertFrom-Json
        $candidate = @($queue.tasks | Where-Object { $_.status -eq 'ready' }) | Select-Object -First 1
        if (-not $candidate) {
            $candidate = @($queue.tasks | Where-Object { $_.status -in @('in_progress', 'review', 'changes_requested', 'accepted') }) | Select-Object -First 1
        }
        if (-not $candidate) { $candidate = $queue.tasks | Select-Object -First 1 }
        $Task = $candidate.id
    }
    & $Python scripts/workflow.py dry-run --task $Task 2>&1 | Tee-Object -FilePath (Join-Path $runRoot 'dry-run.log')
    $dryCode = $LASTEXITCODE
    & $Python -m pytest -q --basetemp $baseTemp -p no:cacheprovider --tb=short 2>&1 | Tee-Object -FilePath (Join-Path $runRoot 'pytest.log')
    $testCode = $LASTEXITCODE
    & git diff --check 2>&1 | Tee-Object -FilePath (Join-Path $runRoot 'diff-check.log')
    $diffCode = $LASTEXITCODE
    @{ plan_exit=$planCode; dry_run_exit=$dryCode; tests_exit = $testCode; diff_exit = $diffCode; basetemp = $baseTemp } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runRoot 'result.json') -Encoding utf8
    if ($planCode -ne 0 -or $dryCode -ne 0 -or $testCode -ne 0 -or $diffCode -ne 0) { throw "Checks failed: plan=$planCode dry-run=$dryCode pytest=$testCode diff=$diffCode" }
}
finally {
    $env:TEMP = $savedTemp
    $env:TMP = $savedTmp
    $env:PYTHONDONTWRITEBYTECODE = $savedBytecode
    $env:GIT_OPTIONAL_LOCKS = $savedLocks
    Pop-Location
}
