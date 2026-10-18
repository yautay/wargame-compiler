# Automatic IG-2 orchestration

For a clone on another Windows computer, follow [IG-2 restore](IG2-RESTORE.md).
Use an explicit `--host-runtime` binding to preserve historical toolchains while
running with this checkout's verified local tools. Run the resume audit and preflight
before launching a model.

The operator requested automatic executor and reviewer launches for IG-2 on
2026-10-15. This explicitly authorizes this local supervisor to launch fresh Codex
CLI processes sequentially. It does not authorize unrelated external services,
history access, commits, pushes, nested agents or automatic human acceptance.
The default manual workflow remains available.

```powershell
.\.venv\Scripts\python.exe scripts/orchestrate_ig2.py plan
.\.venv\Scripts\python.exe scripts/orchestrate_ig2.py run
.\.venv\Scripts\python.exe scripts/orchestrate_ig2.py start
```

Use the existing authenticated `codex` executable. No API key, SDK, installation,
global settings or provider change is introduced. A launch needs the existing
Codex connection and ordinary workspace write permission; it cannot bypass a
parent sandbox or network restriction. Run it in a terminal or an explicitly
authorized hidden background process, without adding a scheduled automation.
Child processes use `--approve-for-me`: their default remains `workspace-write`,
while individual required commands may request automatic approval. No full-access
or bypass flag is used. V01 explicitly authorizes permitted execution of unchanged
validation commands when the Windows restricted token cannot access pytest's
mode-0700 temporary directories. Do not change directory ACLs, pytest or tests.

Use `start` for background continuation. It redirects supervisor output to a unique
`private/workflow/launches/<UTC>-<id>/` directory and records the actual PID and
launch arguments. On Windows it detaches from the console, creates a new process
group and requests job breakaway so terminal cleanup cannot terminate the run with
the invoking job. A denied breakaway is a recorded launch failure, never a silent
fallback. Run the authorized start command with approved ordinary-user permissions
when the restricted token denies this operation. It preserves the CLI child sandbox
and all queue/review gates. An existing supervisor lock still requires explicit triage.
On Windows, background launch uses the installed base interpreter directly rather
than the venv redirector, so the recorded PID is the actual supervisor. This fixes
process identity; it does not prove the cause of an earlier abrupt termination.

`plan` validates the queue and shows the next role without starting a model or
changing product/queue state. `run` rereads `queue.json` after every session and
stops only with a recorded outcome: complete, blocked, or budget_stop. The initial
queue contains a frozen IG-2B02 repair awaiting independent rereview. This is an
observation at preparation time, not another status authority.

## Context and cost controls

Each executor, reviewer and refinement coordinator is a new ephemeral process;
conversation history is never resumed or copied. The process receives a short
role prompt, the selected task without its event history, a hash-pinned manifest,
and exact delivery or repair references when needed. Required contracts and source
evidence are read on demand; every assigned original page and acceptance criterion
still requires inspection. The existing 100 KB packet text ceiling is enforced
before active task launches. Binary inputs are references, not injected PDF text.

Use four-page inventory batches and at most 20 target clauses per reconciliation
child. Refine broad future cards only when their dependencies are done; reuse
accepted baselines, persisted identities and current frozen reports. A repair
reuses unchanged evidence and validates the precise findings and affected risks.
Never reread an entire source/attempt tree to locate a known artifact. Do not skip
source inspection, reduce the full-rulebook denominator or weaken checks to save
context. These policies reduce redundant context; no cost optimum is claimed.

Task sessions use `scripts/search_task.py` with an exact session search manifest,
its SHA-256 and task identity bound in the launch environment. The manifest selects
only stable public text from that packet and the named workflow control files.
Private evidence, volatile views, history, binary inputs and unlisted paths are
rejected. Ripgrep receives exact file operands and `--no-config`; match/output
limits report truncation explicitly. Private evidence requires exact authorized
locators or selected JSON fields. The frozen legacy `scripts/search.ps1` remains
byte-identical for accepted manifests and is explicitly forbidden in these sessions.
This operator-authorized search override replaces its repository-wide behavior.

The supervisor resolves and verifies ripgrep before starting each model, records
its absolute path, SHA-256 and version in the session's `tool-runtime.json`, and
passes `WGC_RIPGREP_PATH`/`WGC_RIPGREP_SHA256` to child tools. The search helper checks
that binding on every invocation and executes the absolute path. A missing or
changed binding never falls back to PATH. For an independent Windows host, resolve
the existing installed `rg.exe` in the invoking environment and pass both values
through its launch record before starting the supervisor; that host may have a
different PATH. No install or global environment change is required. Without an
explicit binding, dispatch tries the selected CLI's sibling rg then its own PATH,
and stops before a model launch if neither is available.
The verified rg directory is also prepended to the complete inherited process PATH
for unchanged tests that invoke `rg` by name. Pinned native dependency prefixes and
both PYTHONPATH entries remain intact. This applies to executor/reviewer checks and
the supervisor's final validation, without global environment changes.

Dependency reads use `scripts/dependency_context.py` and a per-session hash-bound
`dependency-view.json`. One command returns one section: summary, outputs, inventory,
boundary or toolchain. The view includes direct accepted dependencies only, normalized
path/SHA-256/byte-count pins, current declared report versions, assigned page/region
metadata, the prior range's exit observation and installed runtime metadata. It never
releases queue histories, closure/delivery envelopes, full artifact lists, unrelated
page content or arbitrary JSON fields. Its 24 KB ceiling rejects excess output rather
than silently truncating it. Ambiguous baseline/report selection and stale dependency
authority stop preparation. Ancestor and preparation artifacts cannot replace the
selected dependency's current inventory/toolchain. Raw dependency-record or closure
dumps are forbidden even when their exact paths are known; whole-file hashing and
structural copying of unchanged records remain available internally without output.

After a context incident, an operator-authorized fresh session receives new scope and
assessment references. `context_recovery_authorization` pins those and the immutable
incident; the supervisor verifies them before and after every role. It does not grant
readiness, source acceptance or permission to replay the interrupted transcript.

Defaults are 48 model sessions, one hour per session, eight hours overall. Override
with `--max-sessions`, `--session-seconds` and `--total-seconds`. The total wall-time
limit also bounds the next model session. A run may need multiple bounded windows
to complete the full stage. Model usage and money remain null when reliable billing
data are not exposed; session/time limits are not a monetary spending cap. Execution
and independent review both retain the repository's gpt-6.1-sol/high requirement.

## Quality gates and process evidence

The supervisor observes the CLI startup header before permitting a claim. Requested
flags alone do not establish actual configuration. Missing or mismatched observed
model, reasoning or session identity stops the run. Each session retains its command,
startup metadata, prompt, stdout/stderr, structured result and process timing. The
builder session's actual model/reasoning are unknown and are not represented as Sol/high.
Claim, delivery, readiness/partition and review evidence bind their unique actor and
`configuration_evidence` path plus `configuration_sha256` to that observed session.
The supervisor checks role-specific queue deltas before handling every outcome,
including blocked. An executor cannot change its contract or another task; a
coordinator preserves prior acceptance criteria, tests and human gates while refining.

An executor claims and delivers through `workflow.py`. A fresh reviewer verifies the
entire frozen delivery and writes a distinct review artifact. The deterministic
supervisor requires the exact manifest/criteria and independent actor, reruns
`scripts/check.ps1 -Task ID` and `git diff --check`, and uses the existing transition
gates for accepted and done. It never substitutes one model's self-review. Rule meaning,
source coverage, technical acceptance and executable readiness remain separate.
Tasks requiring human semantic acceptance stop for explicit owner verification.

Every new `changes_requested` finding first returns to a coordinator. A previous
repair packet cannot authorize another repair: `repair_authorization` must bind the
current review path/hash, a fresh scope and authorization evidence, and a new absent
owned attempt. The scope pins exact finding IDs, the immutable delivery, unchanged
acceptance/tests and the allowed repair mode. Coordinator refinement leaves status
and prior events unchanged; executors cannot claim until these checks pass.

For V01 the mode is `validation_only`. Every original frozen artifact remains
byte-identical, and its ordered manifest is the prefix of the new delivery; only new
operational validation evidence is appended. The supervisor captures that baseline
before launch and checks preservation after every outcome, including blocked.
An unchanged blocked coordinator preserves its diagnostic instead of losing it to
a missing-authorization error.

Without an explicit host binding, both the model process and supervisor checks
inherit process-local dependency paths from the task's pinned `toolchain.json`:
`process_pythonpath` includes repo `src` and
the bundled Python `Lib/site-packages` (including existing `reportlab`), while
`process_path_prefix` supplies Poppler. No package installation or persistent config
change is needed. A src-only PYTHONPATH is insufficient for the unchanged source suite.
`process_path_prefix` accepts a directory string or an ordered list of directory
strings, joined using the platform PATH separator. Lists preserve order, duplicates
and expired session-wrapper entries, which ordinary PATH lookup ignores; at least
one listed directory must be available. An unavailable single pinned directory or
entirely unavailable list still stops preparation. Invalid element types and empty
or separator-containing elements are rejected before launching a model. The inherited
PATH tail and source toolchain bytes are preserved; only the child environment changes.

For a restored Windows checkout, `--host-runtime` selects a separately observed local
record instead. Its root, exact Python library versions, Poppler version and executable
hashes are verified, and PATH shadowing of a pinned tool is rejected. The original
toolchain remains byte-identical. A bound runtime is inherited by detached launches,
model processes and supervisor validation; it is not an alternative task/status authority.

Each stable finding ID has at most two changes_requested cycles from the
authoritative event chain. The supervisor hash-verifies prior review evidence and
counts each finding once per review; a combined repair consumes one cycle for each
finding it contains. New findings have independent budgets, and restarting the
supervisor does not reset counts. Missing/duplicate IDs or changed prior evidence
stop budget evaluation. Reviewers retain IDs for unresolved/reopened issues and use
unused IDs for new issues; renumbering does not authorize another cycle. A failed launch,
unchanged refinement or model process error is not retried automatically. Transient
Windows preparation I/O errors (5/32/33) before a model starts may retry at most twice
per task/role/error in the current run. Each retry uses a fresh dispatch directory,
preserves the failed preparation, and requires the queue to remain byte-identical.
Context refusals, changed pins, changed ownership and other errors still stop. This
bounded operator-authorized recovery never expands source access or repairs code at
runtime. Preparation state is recorded before expensive pin checks. Child prompts
also retain the existing two-retries-per-unchanged-failure limit. Changed circumstances
need a documented coordinator decision rather than another blind retry.

IG-2D refinement must partition the full inventory and import targets, check exact
set equality/no duplicate targets, resolve cross-batch references, and leave the
parent as closure depending on all children. Completion requires every current
IG-2 task, including dynamically added children, to be done. No IG-3 work is launched.
Queue records carry parent `target_ids` (the universe), child `target_ids` (1-20
assigned IDs) and separate `context_only_ids`; duplicate/missing targets stop dispatch.
IG-2C must deliver `reconciliation-universe.json`, format
`wgc-reconciliation-universe-1`, with unique `target_ids` for the complete source and
import universe and `inputs` containing both pinned input path/SHA-256 references.
Its independent acceptance must verify equality against the complete inventory and
import. Before launching the IG-2D coordinator, the supervisor freezes this exact
artifact from IG-2C's accepted manifest and verifies its provenance. Partition sets
are checked against that frozen dependency, not a coordinator-edited parent list.

## Monitoring and recovery

Inventory coordinators receive exact, hash-pinned tool documentation and source
interfaces as lazy references, including the source CLI README, evidence guidance,
region schema, inventory/geometry/PDF modules and execution/review skills. Read
stable public files through `scripts/task_access.py read` in bounded line windows;
the full module text is not injected into the initial packet. Dependency data
still uses only the typed `scripts/dependency_context.py` projections.

Required reads of `docs/STATUS.md` and `docs/HANDOFF.md` use immutable dispatch copies
under the session's `bootstrap/` directory, pinned separately in the access manifest.
The same bounded read helper reports their snapshot basis and non-authoritative
status. Later live view updates do not invalidate these navigation copies. Only these
two named generated views are allowed through this exception; generic searching of
volatile views and arbitrary private snapshot paths remains forbidden. The selected
task contract and workflow queue gates remain the task/status authority.

Git state uses only `scripts/task_access.py git-status`: the session manifest fixes
literal paths for its task run, declared outputs and exact packet/control files.
There is no command-line path override or unscoped fallback. Unrelated task paths
are rejected before release; results are bounded and explicitly mark truncation.
Raw Git status and recursive path listings are outside the supported protocol.

Executor and reviewer source validation use `scripts/task_access.py validate-source --file
'<exact inventory path>'` with the inherited access binding. Dispatch pins only the
current final inventory and both complete replay inventories; older inventories in
the delivery do not become additional validation operands. Reviewer inputs have
immutable dispatch-time hashes. Executor inputs are the three exact generated paths
under its current owned attempt: the helper requires a current in-progress claim
bound to that session's observed Sol/high runtime, hashes the generated inventory
for each call, and rejects any input or queue/ownership change during validation.
Missing output files do not authorize another path. The helper runs the
unchanged full `python -m wgc.sources validate` command, captures stdout and stderr
in new task-owned private logs, and returns only the command, exit code and log pins.
It preserves the validator's exit code, including failure; a validation failure is
not itself a context denial. No log tail, raw traceback or per-page coverage rows
are released. Additional diagnostic reads require an explicit assigned-page/field
selection or fresh coordinator scope. Other check wrappers follow the same output
policy; logs are preserved without generic last-line/character previews.

Context helpers bind a per-session guard. A refusal publishes a denial marker and
holds the request; the supervisor stops its owned CLI process tree and accepts no
result. A streamed denial signal supplies a second notification channel. Invalid
guard configuration and failed marker writes also hold, never return a completed
refusal. If all notifications fail, the session deadline still stops the held call.
Context requests must be serial; direct reads, raw searches or alternate commands
after a refusal are forbidden. Missing documentation requires a new pinned packet
and a fresh session. These controls enforce the helper protocol; the sandbox remains
the operating-system boundary for arbitrary tool commands.

Search, public-read, Git-status and dependency helper results use ASCII JSON with
Unicode escapes. Parsing the JSON preserves the original Unicode text even when
Windows pipes use a legacy code page. Output ceilings count this exact serialized
representation, including escapes and the terminating newline. Source files and
evidence remain unchanged; no console, global or persistent encoding setting is needed.

Synthetic refusal tests isolate inherited live-session guard variables and verify
that a subsequent direct-read fallback never executes, including invalid guard
digests/JSON and failed marker open/rename/publication. On Windows, restricted-token
denial of owned process-tree termination requires approved execution of the exact
unchanged checks, as with the earlier pytest temporary-directory restriction; it
does not justify weaker assertions, guard removal, ACL or global configuration edits.

Each run is under `private/workflow/orchestrator/<UTC>-<id>/`; `status.json` is a
disposable operational view, not a task queue. Session evidence is preserved in
uniquely named subdirectories. `private/workflow/ig2-orchestrator.lock` prevents
two supervisors. Normal exit releases it; an abandoned lock is never stolen.
Each CLI session also records `process.json` with supervisor/child PIDs and a
five-second heartbeat, followed by its exit state. A stale `running` view or lock
alone proves no process liveness. Compare the recorded identities with OS process
state using approved process inspection when the restricted token cannot enumerate
the processes. Missing final process evidence indicates an abrupt interruption;
it does not identify the external cause. Preserve that evidence before recovery.
Atomic supervisor JSON writes retry the same closed candidate at most twice for
Windows access/sharing/lock errors (5, 32, 33), with 50/100 ms waits. Persistent
denials remain failures, preserving the prior destination and pending candidate;
there is no truncation fallback, ACL change or relaxed context guard.

After supervisor-only validation fails, an operator-authorized recovery can reuse
the exact passing independent review through `finish_review` with its original
review session and a fresh `validation_session` under the selected task run.
Observed review identity/configuration, every frozen artifact and all criteria are
rechecked before unchanged supervisor checks. New logs and closure evidence use
the fresh directory; old review/session evidence is retained byte-for-byte. This
does not grant semantic acceptance or retry a failed model role automatically.
Task claims/checkpoints remain under their ordinary `private/workflow/runs/<task>/`
locations. No existing attempts or staged/unstaged changes are overwritten.

After budget_stop run the same command for a fresh launch window; it selects from
the current queue. After an interrupted in_progress or accepted task, do not blindly
restart: reconcile checkpoint, owner/process liveness and disk/queue hashes first.
Resolve abandoned locks only after proving their process is no longer running.

A blocked attempt can resume only after explicit operator recovery authorization.
`continuation_authorization` binds the exact blocked event path/hash, a new scope,
assessment evidence and a separate absent owned output directory. Draft recovery
uses `draft_revalidation`: criteria/tests remain exact, the original blocked-state
manifest and blocked-event evidence are preserved in full, and named draft files
are individually pinned. Old scripts/transcripts and prior inspection/check claims
are not inherited. Reinspect all assigned original pages, regenerate path-dependent
evidence, complete two independent replays and missing reports, run fresh checks,
then obtain fresh independent review. The supervisor checks the preserved bytes
before dispatch, after every outcome and on later preparation/restart. Preservation
and structural consistency do not establish source completeness or acceptance.

After a continuation delivery receives review findings, its old directory becomes
a frozen input. A verified `repair_authorization` owns a separate fresh directory;
the old continuation directory need not remain in the current `write_scope`.
Preservation checks verify that repair lineage against its actual review/delivery
and snapshot both the blocked attempt and frozen continuation for post-role/restart
checks. New repair claims still require an absent output root. A later new finding
returns to a coordinator before another executor can run. Current repair scope
governs work: an index repair revalidates existing evidence and does not repeat the
initial draft rebuilding or unchanged replays.
Timeout terminates the supervisor-owned child process tree on Windows, preserving
all files for recovery. A failed process does not automatically change task status.
Validation subprocesses also have deadlines. Cleanup has bounded additional waits;
if Windows denies tree termination, the supervisor terminates its owned process
handle, records the failure and stops for descendant-process inspection.

The sandbox remains the real permission boundary. Manifests, write scopes and
instructions constrain the intended workflow; they do not technically prevent an
arbitrary child tool from reading another path or writing outside its task scope.
Source-region evidence generation is serial in the task process: Windows restricted
tokens can deny the named pipes used by Python worker-process pools. Both complete
independent replays and all source/component checks remain required. Unexpected
Python exceptions record a blocked final status and retain their traceback; a hard
external process termination can still leave stale views requiring OS inspection.
Out-of-stage queue changes and frozen-artifact changes stop further dispatch; the
supervisor preserves them for triage instead of silently rolling them back.
