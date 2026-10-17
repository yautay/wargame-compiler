$ErrorActionPreference = 'Stop'
$reviewRoot = $PSScriptRoot
$checkScript = 'C:\repo\wargame-compiler\scripts\check.ps1'
$beforeHash = (Get-FileHash -LiteralPath $checkScript -Algorithm SHA256).Hash.ToLowerInvariant()
# Redirect only the generated operational directory. Execute original script bytes.
function global:Join-Path {
    param([Parameter(Position=0,Mandatory=$true)]$Path, [Parameter(Position=1,Mandatory=$true)]$ChildPath)
    if ($Path -eq 'C:\repo\wargame-compiler' -and $ChildPath -like 'private\workflow\checks\active-*') {
        return [IO.Path]::Combine($reviewRoot, 'c')
    }
    Microsoft.PowerShell.Management\Join-Path -Path $Path -ChildPath $ChildPath
}
try {
    & $checkScript -Task IG-2A
    $afterHash = (Get-FileHash -LiteralPath $checkScript -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($beforeHash -ne $afterHash) { throw 'Original check script changed' }
    @{original_script=$checkScript; before_sha256=$beforeHash; after_sha256=$afterHash; output_only_redirect=[IO.Path]::Combine($reviewRoot,'c'); validations='Original workflow validate, IG-2A dry-run, project pytest, git diff --check all executed unchanged'} | ConvertTo-Json | Set-Content -LiteralPath ([IO.Path]::Combine($reviewRoot,'check-adapter-evidence.json')) -Encoding utf8
}
finally { Remove-Item Function:\Join-Path }
