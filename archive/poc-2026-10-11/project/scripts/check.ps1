param([string]$Python = '')
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not $Python) { $Python = Join-Path $repoRoot '.venv\Scripts\python.exe' }
if (-not (Test-Path -LiteralPath $Python)) { throw 'Wskaż istniejący interpreter z pytest przez -Python.' }
$runRoot = Join-Path $repoRoot ('private\poc\_checks\active-' + [guid]::NewGuid().ToString('N'))
$baseTemp = Join-Path $runRoot 'pytest'
if ((Test-Path -LiteralPath $runRoot) -or (Test-Path -LiteralPath $baseTemp)) { throw 'Katalog kontroli musi być nowy.' }
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
    & $Python -m pytest -q --basetemp $baseTemp -p no:cacheprovider --tb=short 2>&1 | Tee-Object -FilePath (Join-Path $runRoot 'pytest.log')
    $testCode = $LASTEXITCODE
    & git -c "safe.directory=$($repoRoot.Replace('\', '/'))" diff --check 2>&1 | Tee-Object -FilePath (Join-Path $runRoot 'diff-check.log')
    $diffCode = $LASTEXITCODE
    @{ tests_exit = $testCode; diff_exit = $diffCode; basetemp = $baseTemp } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runRoot 'result.json') -Encoding utf8
    if ($testCode -ne 0 -or $diffCode -ne 0) { throw "Kontrole nie przeszły: pytest=$testCode diff=$diffCode" }
}
finally {
    $env:TEMP = $savedTemp
    $env:TMP = $savedTmp
    $env:PYTHONDONTWRITEBYTECODE = $savedBytecode
    $env:GIT_OPTIONAL_LOCKS = $savedLocks
    Pop-Location
}
