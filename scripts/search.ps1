param([Parameter(Mandatory=$true)][string]$Pattern)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
Push-Location -LiteralPath $root
try {
    $files = @(& ./.venv/Scripts/python.exe scripts/workflow.py files)
    if ($LASTEXITCODE -ne 0) { throw 'Cannot build active file allowlist.' }
    & rg --line-number -- $Pattern @files
    if ($LASTEXITCODE -gt 1) { throw 'Search failed.' }
}
finally { Pop-Location }
