$ErrorActionPreference = 'Stop'
$reviewOutput = $PSScriptRoot
# Only redirect check.ps1's operational run directory; preserve its checks and bytes.
function Join-Path {
    param([string]$Path, [string]$ChildPath)
    if ($ChildPath.StartsWith('private\workflow\checks\active-')) {
        return Microsoft.PowerShell.Management\Join-Path -Path $reviewOutput -ChildPath 'c'
    }
    Microsoft.PowerShell.Management\Join-Path -Path $Path -ChildPath $ChildPath
}
& ./scripts/check.ps1 -Task IG-2A
