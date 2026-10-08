$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath('C:\dev\wargame-compiler')
$snapshotRoot = Join-Path $repoRoot 'private\archive\2026-10-07-pre-poc'
$verified = Get-Content -LiteralPath (Join-Path $snapshotRoot 'verification.json') -Raw | ConvertFrom-Json
if (-not $verified.reorganization_allowed -or $verified.mismatches.Count -ne 0) { throw 'Snapshot not verified' }
$legacyRoot = Join-Path $repoRoot 'archive\legacy-2026-10-07\project'
$stateRoot = Join-Path $repoRoot 'private\archive\legacy-2026-10-07-state'
if ((Test-Path -LiteralPath $legacyRoot) -or (Test-Path -LiteralPath $stateRoot)) { throw 'Archive destination already exists' }
$publicNames = @('.gitattributes', '.gitignore', 'CLAUDE.md', 'README.md', 'COPYRIGHT.md', 'pyproject.toml', 'requirements.txt', 'bench', 'contracts', 'docs', 'glu', 'tests', 'wgc')
$stateNames = @('.glu', '.pytest_cache', 'wargame_compiler.egg-info')
$moves = @()
foreach ($name in $publicNames + $stateNames) {
    $src = [IO.Path]::GetFullPath((Join-Path $repoRoot $name))
    $base = if ($publicNames -contains $name) { $legacyRoot } else { $stateRoot }
    $dst = [IO.Path]::GetFullPath((Join-Path $base $name))
    if (-not $src.StartsWith($repoRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Source outside workspace' }
    if (-not $dst.StartsWith($repoRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Target outside workspace' }
    if ($src -eq $repoRoot -or $dst.StartsWith($src + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Recursive target or root move' }
    $item = Get-Item -LiteralPath $src -Force
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point: $src" }
    if (Test-Path -LiteralPath $dst) { throw "Target exists: $dst" }
    $moves += [PSCustomObject]@{ source = $src; destination = $dst }
}
# All absolute source and destination paths have been validated before any move.
$moves | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $snapshotRoot 'planned-root-moves.json') -Encoding utf8
New-Item -ItemType Directory -Path $legacyRoot | Out-Null
New-Item -ItemType Directory -Path $stateRoot | Out-Null
foreach ($move in $moves) {
    Move-Item -LiteralPath $move.source -Destination $move.destination
    Write-Output ($move.source + ' -> ' + $move.destination)
}
