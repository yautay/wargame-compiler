param([Parameter(Mandatory=$true)][string]$LaunchDirectory)
$ErrorActionPreference = 'Stop'
$wgcRoot = 'C:\repo\wargame-compiler'
$wgcLaunchRoot = [IO.Path]::GetFullPath((Join-Path $wgcRoot 'private\workflow\launches')) + [IO.Path]::DirectorySeparatorChar
$wgcLaunch = [IO.Path]::GetFullPath($LaunchDirectory)
if (-not $wgcLaunch.StartsWith($wgcLaunchRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Launch directory must belong to this repository'
}
$wgcRecord = Get-Content -LiteralPath (Join-Path $wgcLaunch 'launch.json') -Raw | ConvertFrom-Json
if ($wgcRecord.python -ne (Join-Path $wgcRoot '.venv\Scripts\python.exe')) { throw 'Unexpected interpreter' }
if (Test-Path -LiteralPath (Join-Path $wgcLaunch 'worker-start.json')) { throw 'Worker already started' }
@{worker_pid=$PID;started_utc=[DateTime]::UtcNow.ToString('o');launch_mode='local-WMI-independent-host'} |
    ConvertTo-Json | Set-Content -LiteralPath (Join-Path $wgcLaunch 'worker-start.json') -Encoding utf8
$wgcResult = @{worker_pid=$PID;state='starting';exit_code=$null}
try {
    if (-not [IO.Path]::IsPathRooted($wgcRecord.ripgrep.path)) { throw 'Absolute ripgrep path required' }
    if ((Get-FileHash -LiteralPath $wgcRecord.ripgrep.path -Algorithm SHA256).Hash.ToLower() -ne $wgcRecord.ripgrep.sha256) { throw 'Ripgrep hash changed' }
    $env:WGC_RIPGREP_PATH = $wgcRecord.ripgrep.path
    $env:WGC_RIPGREP_SHA256 = $wgcRecord.ripgrep.sha256
    & $wgcRecord.python 'C:\repo\wargame-compiler\private\workflow\runs\IG-2B05\boundary-recovery-20261016-01\preflight.py' $wgcRecord.codex $wgcLaunch
    if ($LASTEXITCODE -ne 0) { throw 'Independent host preflight failed; no model launched' }

    $wgcArguments = @('-u', ('"' + (Join-Path $wgcRoot 'scripts\orchestrate_ig2.py') + '"'),
        'run', '--codex', ('"' + $wgcRecord.codex + '"'))
    $wgcProcess = Start-Process -FilePath $wgcRecord.python -ArgumentList $wgcArguments -WorkingDirectory $wgcRoot `
        -WindowStyle Hidden -RedirectStandardOutput (Join-Path $wgcLaunch 'stdout.log') `
        -RedirectStandardError (Join-Path $wgcLaunch 'stderr.log') -PassThru
    $wgcResult.supervisor_launcher_pid = $wgcProcess.Id
    $wgcProcess.WaitForExit()
    $wgcResult.exit_code = $wgcProcess.ExitCode
    $wgcResult.state = 'exited'
}
catch {
    $wgcResult.state = 'failed'
    $wgcResult.error = $_.Exception.Message
}
finally {
    $wgcResult.ended_utc = [DateTime]::UtcNow.ToString('o')
    $wgcResult | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $wgcLaunch 'worker-result.json') -Encoding utf8
}


