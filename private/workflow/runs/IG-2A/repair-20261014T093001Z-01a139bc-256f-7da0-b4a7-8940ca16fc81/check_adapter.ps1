$ErrorActionPreference = 'Stop'
$repairOutput = $PSScriptRoot
# Redirect only operational output; check.ps1 and all validation logic stay frozen.
function Join-Path {
    param([string]$Path, [string]$ChildPath)
    if ($ChildPath.StartsWith('private\workflow\checks\active-')) {
        return Microsoft.PowerShell.Management\Join-Path -Path $repairOutput -ChildPath 'c'
    }
    Microsoft.PowerShell.Management\Join-Path -Path $Path -ChildPath $ChildPath
}
& ./scripts/check.ps1 -Task IG-2A
