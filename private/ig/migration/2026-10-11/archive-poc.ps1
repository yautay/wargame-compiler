param([string]$Repo = 'C:\repo\wargame-compiler')
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath $Repo).Path
$publicRoot = [IO.Path]::GetFullPath((Join-Path $repoRoot 'archive\poc-2026-10-11'))
$privateRoot = [IO.Path]::GetFullPath((Join-Path $repoRoot 'private\archive\poc-2026-10-11'))
function Assert-InRepo([string]$Path) {
    $resolved = [IO.Path]::GetFullPath($Path)
    if (-not $resolved.StartsWith($repoRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Target outside repository: $resolved"
    }
    return $resolved
}
function Get-Rel([string]$Path) { return [IO.Path]::GetRelativePath($repoRoot, $Path).Replace('\', '/') }
foreach ($path in @($publicRoot, $privateRoot)) {
    $null = Assert-InRepo $path
    if (Test-Path -LiteralPath $path) { throw "Archive destination already exists: $path" }
}
$moves = @(
    @{ source = 'docs'; target = 'archive\poc-2026-10-11\project\docs'; category = 'public' },
    @{ source = 'scripts'; target = 'archive\poc-2026-10-11\project\scripts'; category = 'public' },
    @{ source = 'tests'; target = 'archive\poc-2026-10-11\project\tests'; category = 'public' },
    @{ source = 'private\poc'; target = 'private\archive\poc-2026-10-11\payload\private\poc'; category = 'private' },
    @{ source = 'private\source-artifacts'; target = 'private\archive\poc-2026-10-11\payload\private\source-artifacts'; category = 'private' }
)
$topFiles = @('README.md', 'CLAUDE.md', 'pyproject.toml', '.gitignore', '.gitattributes')
$entries = [Collections.Generic.List[object]]::new()
foreach ($move in $moves) {
    $source = Assert-InRepo (Join-Path $repoRoot $move.source)
    $target = Assert-InRepo (Join-Path $repoRoot $move.target)
    if (-not (Test-Path -LiteralPath $source -PathType Container)) { throw "Missing source: $source" }
    $items = @(Get-ChildItem -LiteralPath $source -Recurse -Force)
    if ($items | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }) { throw "Reparse point in $source" }
    foreach ($item in ($items | Where-Object { -not $_.PSIsContainer })) {
        $relative = [IO.Path]::GetRelativePath($source, $item.FullName)
        $entries.Add(@{
            original_path = Get-Rel $item.FullName
            archive_path = Get-Rel (Assert-InRepo (Join-Path $target $relative))
            bytes = $item.Length
            sha256 = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            category = $move.category
        })
    }
}
foreach ($name in $topFiles) {
    $source = Assert-InRepo (Join-Path $repoRoot $name)
    $target = Assert-InRepo (Join-Path $publicRoot ('project\' + $name))
    $item = Get-Item -LiteralPath $source
    $entries.Add(@{ original_path = $name; archive_path = Get-Rel $target; bytes = $item.Length;
        sha256 = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant(); category = 'public' })
}
$migrationRoot = Assert-InRepo (Join-Path $repoRoot 'private\ig\migration\2026-10-11')
$planPath = Join-Path $migrationRoot 'preflight-manifest.json'
$manifest = @{
    archive_id = 'poc-2026-10-11'; captured_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
    user_date = '2026-10-11'; user_timezone = 'Europe/Warsaw'
    requested_action = 'Archive the entire current POC; make the IG plan the active seed of the game digitization tool.'
    completion_state = 'incomplete_experiment_archived'; entries = @($entries.ToArray())
    excluded_roots = @('.git', '.venv', 'archive\legacy-2026-10-07', 'private\archive (existing)', 'private\ig')
}
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $planPath -Encoding utf8
& git -C $repoRoot status --porcelain=v1 --untracked-files=all | Set-Content -LiteralPath (Join-Path $migrationRoot 'git-status-before.txt') -Encoding utf8
if ($LASTEXITCODE -ne 0) { throw 'Git status capture failed' }
Write-Output "PREFLIGHT_FILES=$($entries.Count)"
foreach ($move in $moves) {
    $source = Assert-InRepo (Join-Path $repoRoot $move.source)
    $target = Assert-InRepo (Join-Path $repoRoot $move.target)
    # Check absolute source and destination immediately before each recursive move.
    if (Test-Path -LiteralPath $target) { throw "Destination exists: $target" }
    New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
    Move-Item -LiteralPath $source -Destination $target
}
foreach ($name in $topFiles) {
    Copy-Item -LiteralPath (Join-Path $repoRoot $name) -Destination (Join-Path $publicRoot ('project\' + $name))
}
$errors = [Collections.Generic.List[string]]::new()
foreach ($entry in $entries) {
    $path = Assert-InRepo (Join-Path $repoRoot $entry.archive_path)
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { $errors.Add("Missing: $path"); continue }
    if ((Get-Item -LiteralPath $path).Length -ne $entry.bytes) { $errors.Add("Length mismatch: $path") }
    if ((Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) { $errors.Add("Hash mismatch: $path") }
}
if ($errors.Count) { throw ($errors -join "`n") }
$manifestPath = Join-Path $privateRoot 'manifest.json'
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8
$publicEntries = @($entries | Where-Object { $_.category -eq 'public' })
$privateEntries = @($entries | Where-Object { $_.category -eq 'private' })
$verification = @{
    archive_id = 'poc-2026-10-11'; result = 'verified'; files_checked = $entries.Count
    public_files = $publicEntries.Count; private_files = $privateEntries.Count
    public_bytes = ($publicEntries | Measure-Object -Property bytes -Sum).Sum
    private_bytes = ($privateEntries | Measure-Object -Property bytes -Sum).Sum
    mismatches = 0; verified_at_utc = [DateTimeOffset]::UtcNow.ToString('o')
    full_manifest = 'private/archive/poc-2026-10-11/manifest.json'
    full_manifest_sha256 = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
}
$verification | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $publicRoot 'verification.json') -Encoding utf8
$verification | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $migrationRoot 'verification.json') -Encoding utf8
# Retain the current IG proposal as active documentation; the captured copy stays immutable.
New-Item -ItemType Directory -Path (Join-Path $repoRoot 'docs') -Force | Out-Null
foreach ($name in @('IG-DATA-MODEL.md', 'IG-MECHANICS-PROFILES.md')) {
    Copy-Item -LiteralPath (Join-Path $publicRoot ('project\docs\' + $name)) -Destination (Join-Path $repoRoot ('docs\' + $name))
}
Write-Output "ARCHIVE_VERIFIED=$($entries.Count)"
Write-Output 'MISMATCHES=0'
