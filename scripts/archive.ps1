param(
    [ValidateSet('Inventory','VerifySource','Migrate','VerifyExternal','Restore')][string]$Mode = 'Inventory',
    [string]$Manifest = 'private/workflow/relocation.json',
    [string]$ArchiveRoot = 'C:\repo\wargame-compiler-archive',
    [string]$RestoreRoot = '',
    [switch]$RemoveVerifiedSources
)
$ErrorActionPreference = 'Stop'
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$archive = [IO.Path]::GetFullPath($ArchiveRoot)
$manifestPath = [IO.Path]::GetFullPath((Join-Path $repo $Manifest))
$script:checkedAncestors = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
function Assert-Within([string]$Path, [string]$Parent) {
    $p = [IO.Path]::GetFullPath($Path)
    $r = [IO.Path]::GetFullPath($Parent).TrimEnd('\','/') + [IO.Path]::DirectorySeparatorChar
    if (-not $p.StartsWith($r, [StringComparison]::OrdinalIgnoreCase)) { throw "Path outside boundary: $p" }
    # Reject junctions/symlinks in every existing ancestor, including the parent.
    $cursor = $p
    while ($cursor) {
        if ($script:checkedAncestors.Contains($cursor)) { break }
        if (Test-Path -LiteralPath $cursor) {
            if ((Get-Item -LiteralPath $cursor -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point: $cursor" }
        }
        $null = $script:checkedAncestors.Add($cursor)
        $cursor = Split-Path -Parent $cursor
    }
    return $p
}
function Hash([string]$Path) {
    $stream = [IO.File]::Open($Path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    try { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($stream)).ToLowerInvariant() }
    finally { $stream.Dispose() }
}
function Verify-Files($Entries, [string]$Base, [string]$Key) {
    # Revalidate link topology each verification pass; share ancestor checks within it.
    $script:checkedAncestors.Clear()
    $checked = 0
    foreach ($e in $Entries) {
        $p = Assert-Within (Join-Path $Base $e.$Key) $Base
        if (-not (Test-Path -LiteralPath $p -PathType Leaf)) { throw "Missing: $p" }
        if ((Get-Item -LiteralPath $p).Length -ne $e.bytes -or (Hash $p) -ne $e.sha256) { throw "Integrity mismatch: $p" }
        $checked++
        if ($checked % 10000 -eq 0) { Write-Output "Verified $checked / $($Entries.Count) files." }
    }
}
function Inventory-Paths($Roots) {
    foreach ($r in $Roots) {
        $p = Assert-Within (Join-Path $repo $r) $repo
        if (-not (Test-Path -LiteralPath $p)) { throw "Missing root: $p" }
        Get-Item -LiteralPath $p -Force
        if (Test-Path -LiteralPath $p -PathType Container) {
            Get-ChildItem -LiteralPath $p -Recurse -Force
        }
    }
}
if ($Mode -eq 'Inventory') {
    if (Test-Path -LiteralPath $manifestPath) { throw 'Refusing to replace an existing relocation manifest.' }
    $roots = @('archive','private/archive','docs/adr','docs/reviews','docs/prompts/IG-0-critical-review.md',
        'docs/work/tasks/IG-0.md','private/ig/migration','private/ig/research','private/ig/reviews','private/ig/_checks')
    $items = @(Inventory-Paths $roots)
    if (@($items | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw 'Reparse points are not supported.' }
    $batch = 'relocation-2026-10-11-' + [guid]::NewGuid().ToString('N')
    $entries = @(foreach ($f in $items | Where-Object { -not $_.PSIsContainer }) {
        $rel = [IO.Path]::GetRelativePath($repo,$f.FullName).Replace('\','/')
        $class = if ($rel.StartsWith('private/')) { 'private' } else { 'public' }
        @{ old_path=$rel; new_path="$batch/$class/$rel"; bytes=$f.Length; sha256=(Hash $f.FullName); visibility=$class }
    })
    $directories = @(foreach ($d in $items | Where-Object PSIsContainer) {
        $rel = [IO.Path]::GetRelativePath($repo,$d.FullName).Replace('\','/')
        $class = if ($rel.StartsWith('private/')) { 'private' } else { 'public' }
        @{ old_path=$rel; new_path="$batch/$class/$rel" }
    })
    @{format='wgc-relocation@1'; source_root=$repo; archive_root=$archive; batch=$batch;
      roots=$roots; directories=$directories; entries=$entries; status='inventoried_not_migrated';
      original_manifests='Preserved byte-for-byte as entries; old paths resolved through this manifest.'} |
        ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8
    Write-Output "Inventoried $($entries.Count) files. No copies removed."
    exit 0
}
$m = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if ($m.format -ne 'wgc-relocation@1' -or $m.source_root -ne $repo -or $m.archive_root -ne $archive) { throw 'Manifest root mismatch.' }
if ($m.batch -notmatch '^relocation-[0-9-]+[a-f0-9]{32}$') { throw 'Invalid batch name.' }
$batchRoot = Assert-Within (Join-Path $archive $m.batch) $archive
if ($Mode -eq 'VerifySource') {
    # Enumerate metadata once. Hash every file, without repeating ancestor I/O per entry.
    $actual = [Collections.Generic.Dictionary[string,object]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($item in (Inventory-Paths $m.roots)) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse point in source tree.' }
        if (-not $item.PSIsContainer) {
            $rel = [IO.Path]::GetRelativePath($repo,$item.FullName).Replace('\','/')
            if (-not $actual.TryAdd($rel,$item)) { throw 'Overlapping source roots.' }
        }
    }
    if ($actual.Count -ne $m.entries.Count) { throw 'Source file count changed.' }
    $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    $verified = 0
    foreach ($e in $m.entries) {
        if (-not $seen.Add($e.old_path) -or -not $actual.ContainsKey($e.old_path)) { throw 'Duplicate or missing source path.' }
        $item = $actual[$e.old_path]
        if ($item.Length -ne $e.bytes -or (Hash $item.FullName) -ne $e.sha256) { throw "Integrity mismatch: $($e.old_path)" }
        $verified++
        if ($verified % 10000 -eq 0) { Write-Output "Verified $verified / $($m.entries.Count) files." }
    }
    Write-Output "Verified $verified source files; migration remains pending."
    exit 0
}
$oldPaths = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$newPaths = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($e in $m.entries) {
    if (-not $oldPaths.Add($e.old_path) -or -not $newPaths.Add($e.new_path)) { throw 'Duplicate relocation paths.' }
    $null = Assert-Within (Join-Path $repo $e.old_path) $repo
    $null = Assert-Within (Join-Path $archive $e.new_path) $batchRoot
    $class = if ($e.old_path.StartsWith('private/')) { 'private' } else { 'public' }
    if ($e.new_path -cne "$($m.batch)/$class/$($e.old_path)") { throw 'Relocation must preserve path and visibility class.' }
    if (-not @($m.roots | Where-Object { $e.old_path -eq $_ -or $e.old_path.StartsWith($_ + '/') }).Count) { throw 'Entry outside inventoried roots.' }
}
if ($Mode -eq 'Migrate') {
    Verify-Files $m.entries $repo 'old_path'
    $actual = @(Inventory-Paths $m.roots | Where-Object { -not $_.PSIsContainer } | ForEach-Object { [IO.Path]::GetRelativePath($repo,$_.FullName).Replace('\','/') })
    if (Compare-Object @($m.entries.old_path | Sort-Object) @($actual | Sort-Object)) { throw 'Source file set changed. Prepare a new manifest.' }
    if (Test-Path -LiteralPath $batchRoot) { throw 'Batch already exists. Verify it; never overwrite it.' }
    New-Item -ItemType Directory -Path $batchRoot | Out-Null
    foreach ($d in $m.directories) {
        $p = Assert-Within (Join-Path $archive $d.new_path) $batchRoot
        New-Item -ItemType Directory -Path $p -Force | Out-Null
    }
    foreach ($e in $m.entries) {
        $dst = Assert-Within (Join-Path $archive $e.new_path) $batchRoot
        New-Item -ItemType Directory -Path (Split-Path $dst) -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $repo $e.old_path) -Destination $dst
    }
    Copy-Item -LiteralPath $manifestPath -Destination (Join-Path $batchRoot 'relocation.json')
    Verify-Files $m.entries $archive 'new_path'
    # Full independent restore rehearsal, retained alongside the external batch.
    $restore = Assert-Within (Join-Path $batchRoot 'restore-proof') $batchRoot
    New-Item -ItemType Directory -Path $restore | Out-Null
    foreach ($d in $m.directories) {
        $dst = Assert-Within (Join-Path $restore $d.old_path) $restore
        New-Item -ItemType Directory -Path $dst -Force | Out-Null
    }
    foreach ($e in $m.entries) {
        $dst = Assert-Within (Join-Path $restore $e.old_path) $restore
        New-Item -ItemType Directory -Path (Split-Path $dst) -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $archive $e.new_path) -Destination $dst
    }
    Verify-Files $m.entries $restore 'old_path'
    # Recheck originals immediately before any deletion; remove only listed files.
    Verify-Files $m.entries $repo 'old_path'
    if ($RemoveVerifiedSources) {
        foreach ($e in $m.entries) { $p = Assert-Within (Join-Path $repo $e.old_path) $repo; Remove-Item -LiteralPath $p }
        foreach ($d in ($m.directories | Sort-Object { $_.old_path.Length } -Descending)) {
            $p = Assert-Within (Join-Path $repo $d.old_path) $repo
            if (@(Get-ChildItem -LiteralPath $p -Force).Count -eq 0) { Remove-Item -LiteralPath $p }
        }
    }
    @{result='verified'; files=$m.entries.Count; relocation_sha256=(Hash $manifestPath);
      restored=$true; sources_removed=[bool]$RemoveVerifiedSources; utc=[DateTime]::UtcNow.ToString('o')} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $batchRoot 'verification.json') -Encoding utf8
    Write-Output "External copy and restore verified. Sources removed: $RemoveVerifiedSources"
    exit 0
}
if ($Mode -eq 'VerifyExternal') {
    Verify-Files $m.entries $archive 'new_path'
    if ((Hash $manifestPath) -ne (Hash (Join-Path $batchRoot 'relocation.json'))) { throw 'Relocation manifest mismatch.' }
    Write-Output "Verified $($m.entries.Count) external files."
    exit 0
}
if (-not $RestoreRoot) { throw 'Restore requires -RestoreRoot, a new directory outside the active repo.' }
$restore = [IO.Path]::GetFullPath($RestoreRoot)
if ($restore -eq $repo -or $restore.StartsWith($repo.TrimEnd('\','/') + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase) -or (Test-Path -LiteralPath $restore)) { throw 'Unsafe or existing restore root.' }
$null = Assert-Within $restore (Split-Path $restore)
Verify-Files $m.entries $archive 'new_path'
New-Item -ItemType Directory -Path $restore | Out-Null
foreach ($d in $m.directories) {
    $dst = Assert-Within (Join-Path $restore $d.old_path) $restore
    New-Item -ItemType Directory -Path $dst -Force | Out-Null
}
foreach ($e in $m.entries) {
    $dst = Assert-Within (Join-Path $restore $e.old_path) $restore
    New-Item -ItemType Directory -Path (Split-Path $dst) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $archive $e.new_path) -Destination $dst
}
Verify-Files $m.entries $restore 'old_path'
Write-Output "Restored and verified $($m.entries.Count) files."
