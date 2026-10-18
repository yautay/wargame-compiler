# Resume IG-2B08 on another Windows computer

This guide restores the tracked task state and an explicitly observed local runtime.
`docs/work/queue.json` remains the only queue/status authority. At preparation on
2026-10-18 it selects the IG-2B08 repair executor for F03 and F05-F09; the task is
`changes_requested`. No task has been accepted or completed by this migration.
Restoration and preflight do not launch models or claim the task.

## Clone the correct branch with long paths

Install Git for Windows and provide access to the private GitHub repository. Use a
short destination. The clone's `-c` option below stores a repository-local long-path
setting; it makes no global configuration change. GitHub's default branch may differ.

```powershell
git clone -c core.longpaths=true --single-branch --branch feature/tests git@github.com:yautay/wargame-compiler.git C:\repo\wargame-compiler
Set-Location C:\repo\wargame-compiler
git status --short
```

The repository includes the exact PDF, source evidence, repair scopes, reviews and
original hash-pinned validation reports needed by the current resume audit. Local
`.venv`, caches, credentials, new check output and machine bindings are excluded.
Do not edit frozen manifests, queue event hashes, old toolchains, source documents
or original reports to fit the new machine. Rerunning tests cannot recreate a report
whose exact historical bytes are already pinned. Only selected required reports
under the generally ignored `private/workflow/checks/` are explicitly versioned.

## Restore Python and native dependencies

Use Windows and Python 3.12 (the measured original patch was 3.12.14). Create a new
venv inside this clone; copying another machine's `.venv` does not restore it.
The following package installation is an operator setup step, not a model task action.
The version list includes the observed transitive dependencies; configure verifies
all listed versions. No setup script downloads packages or changes global settings.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r docs/work/ig2-runtime-requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Make these installed tools available locally:

- Poppler **26.07.0**: `pdfinfo.exe`, `pdftoppm.exe` and their required DLLs.
  Configure rejects another Poppler version. Keep the distribution together.
- PowerShell 7 (`pwsh.exe`; the measured original was 7.6.5).
- ripgrep (`rg.exe`).
- The authenticated Codex CLI (`codex.exe`) with access to the required model.
  Sign in using the CLI's supported account flow before launching work. Credentials
  belong to the new machine and must never be copied into Git. Merely requesting
  gpt-6.1-sol/high is not evidence of its actual session configuration; the supervisor
  still verifies the observed startup header before permitting a claim.

Existing Codex-bundled Python/native libraries may also be reused. If libraries live
outside this venv, explicitly pass `--python-library-path '<installed site-packages>'`
at configure time. Their paths and package versions are verified and recorded; no
path from the old `C:\Users\yauta\...` snapshot is assumed on the new computer.
A matching native version alone does not certify identical rendering. Unchanged
source/component checks and complete fresh replays remain required for delivery.

## Bind this checkout to its installed runtime

Configure resolves tools on the current PATH. Each tool also accepts an explicit
absolute path, for example `--codex 'C:\Tools\Codex\codex.exe'`, `--rg`, `--pwsh`,
`--pdfinfo` or `--pdftoppm`. Version probes are local; this step launches no model.

```powershell
.\.venv\Scripts\python.exe scripts/host_runtime.py configure --file private/workflow/hosts/local-runtime.json
.\.venv\Scripts\python.exe scripts/host_runtime.py check --file private/workflow/hosts/local-runtime.json
```

The ignored host record pins this checkout's root, Python and base interpreter,
Python library directories/versions, and every native tool's path, version and
SHA-256. Both interpreter paths matter because the detached Windows supervisor uses
the base interpreter for accurate PID tracking. Its inherited PYTHONPATH still
contains this clone's src and all configured site-packages.

The binding is process-local. The supervisor rejects a changed executable, modified
record, missing dependency, changed requirements or a record from another checkout.
After updating a tool or moving the checkout, configure a **new** filename and use
that record. Never rewrite accepted toolchain evidence. The original dependency
toolchain is preserved; its typed projection adds `current_host_runtime` when a
new host binding is active, and the dispatch saves its own current host snapshot.

## Audit and prepare the next session without launching it

```powershell
.\.venv\Scripts\python.exe scripts/ig2_resume_check.py --task IG-2B08 --host-runtime private/workflow/hosts/local-runtime.json --preflight
.\.venv\Scripts\python.exe scripts/host_runtime.py exec --file private/workflow/hosts/local-runtime.json -- pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08
git -c core.longpaths=true diff --check
```

The audit verifies original hashes and Git inclusion for the selected task's named
inputs, direct dependency event evidence and referenced preservation/delivery metadata.
It prints paths/counts only, never source text or session transcripts. Preflight also
exercises the real scoped repair authorization, context recovery, continuation,
packet generation, dependency projection, executable bindings and launch environment.
It writes only a unique ignored `private/workflow/checks/migration-preflight-*`
dispatch, keeps the queue unchanged and reports `models_launched: 0`.

Require `portable_inputs_complete: true`, empty missing/changed/not-in-Git lists,
a successful preflight and all project checks passing. If a frozen artifact is
missing, recover its **original bytes** from this repository/the preserved source
computer. Do not weaken a hash check or regenerate old evidence to clear the error.
The audit is a checkpoint completeness check, not an archive integrity or source
meaning review. It does not certify unimplemented gameplay or later IG-2C inputs.

## Launch the fresh IG-2B08 executor

```powershell
.\.venv\Scripts\python.exe scripts/orchestrate_ig2.py plan --host-runtime private/workflow/hosts/local-runtime.json
.\.venv\Scripts\python.exe scripts/orchestrate_ig2.py start --host-runtime private/workflow/hosts/local-runtime.json
```

Use `run` in place of `start` for a foreground supervisor. `start` requires ordinary
user permission for Windows process/job breakaway; it never uses a full-access bypass.
Each role gets a fresh ephemeral session. The selected repair attempt must still be
absent and unclaimed; do not copy active processes or restore old session conversations.
If the queue or ownership has changed, stop and triage the current checkpoint instead
of forcing IG-2B08 or deleting a lock. A stale lock is not migration configuration.

The fresh executor copies only named allowed helpers/selections to its new owned
attempt, rebases copied helper paths to this checkout and uses the current host runtime.
Old drafts, reports and observations remain immutable candidates, not inherited green
checks or acceptance. All assigned source limits, repair budgets, fresh source
inspection, full replays, independent review and human gates still apply. Models may
not install libraries, change global configuration or alter frozen host evidence.

Monitor the new paths returned by `start`: its launch record and the corresponding
orchestrator `status.json`. A new `blocked` outcome requires its specific diagnostic;
preflight is not a promise that future model/content work cannot produce new findings.
