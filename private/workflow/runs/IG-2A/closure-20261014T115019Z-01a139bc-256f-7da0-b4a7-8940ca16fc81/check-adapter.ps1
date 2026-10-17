$ErrorActionPreference = 'Stop'
$closureOutput = $PSScriptRoot
# Only relocate operational output; preserve original checks and workflow bytes.
function Join-Path {
    param([string]$Path, [string]$ChildPath)
    if ($ChildPath.StartsWith('private\workflow\checks\active-')) {
        return Microsoft.PowerShell.Management\Join-Path -Path $closureOutput -ChildPath 'c'
    }
    Microsoft.PowerShell.Management\Join-Path -Path $Path -ChildPath $ChildPath
}
& ./scripts/check.ps1 -Task IG-2A
