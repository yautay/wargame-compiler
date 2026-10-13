# Local task workflow

The only authoritative queue, dependencies, task content and status are in
[queue.json](queue.json). Cards, [roadmap](../ROADMAP.md) and the generated portions
of status/handoff are projections checked by `scripts/workflow.py validate`.
Edit queue.json, run `scripts/workflow.py render`, then `scripts/check.ps1`.
This tool is a local planner; it launches no model, chat, agent, scheduler or API.

## Roles and ownership

The coordinator selects ready work, refines future contracts, owns the queue, checks
handoffs and records acceptance evidence. The executor owns only the task's listed
write paths. The independent reviewer reads the frozen result and writes review findings;
they do not silently repair the executor's code. Source-meaning review is separately
identified. The owner (or explicitly authorized human) accepts exact semantic revisions.
Model review and green tests never substitute for that decision.

Default execution is sequential: one claimed task and one writer. A separate review
session may use the same requested Sol/high configuration but a fresh reviewer identity
and task context. No sessions are created automatically. Parallel work needs explicit
operator authorization, satisfied dependencies, disjoint writes, and a coordinator-owned
integration task. Two tasks writing queue.json are never parallel writers.

## State machine

| From | Allowed next states | Gate |
|---|---|---|
| planned | ready, blocked | Dependencies done; context available; refinement resolved |
| ready | in_progress, blocked | Executor identity, actual config evidence, exact scope and checkpoint |
| in_progress | review, blocked | Frozen delivery manifest, meaningful checks and handoff |
| review | changes_requested, accepted, blocked | Separate technical review; meaning review and human decision when required |
| changes_requested | in_progress, blocked | Bounded repair scope and new attempt |
| accepted | done, changes_requested | Coordinator verifies every criterion, evidence and required owner decisions |
| blocked | planned | New evidence resolves recorded blocker; reevaluate readiness, never jump to done |
| done | planned | Explicit reopening reason; prior acceptance preserved in event history |

`ready` is explicit and checked, not inferred from file existence. `next` prints the first
ready task in queue order. At most one task is in_progress/review/changes_requested/accepted.
`done` means its lasting deliverables, tests, independent review and applicable human
acceptance are complete. `blocked` records missing fact, failed assumption or unavailable
input, impact, smallest resolution action, and owner. Source gaps can be valid importer
outputs while still blocking later gameplay; do not mark import blocked for every missing PDF.

Use `transition --task ID --to STATE --evidence PATH`. Evidence is JSON with `role`,
`actor`, `summary`, `criteria`, `artifacts`, `model`, `reasoning`, `configuration_evidence`,
and optional `semantic_decision`. Unknown measured configuration is null with a reason.
For delivery/review/acceptance also supply `checks`, a nonempty list of command and
exit_code records. All required checks must have exit code zero. In-progress claims
require confirmed `model: gpt-6.1-sol` and `reasoning: high`; unknown configuration
is recorded as a blocker until the operator confirms the actual session settings.
The command checks structural gates and file hashes, not the truth or authority of a
human statement. Evidence is append-only by hash in queue events; changes invalidate checks.
See [evidence shapes](EVIDENCE.md) for a checkpoint/delivery example. Executor status
updates go through the transition command; the coordinator owns structural queue edits.
For a semantic task, accepted requires a human decision artifact from the owner or a
documented authorized reviewer. Do not fabricate one. Routine technical acceptance can
be recorded by the coordinator after independent review without another owner confirmation.

## One task cycle

1. Coordinator validates queue and chooses `next`. Resolve `refine` before readiness.
2. Generate a packet with exact allowed context. Binary source references are hashed,
   not dumped into text; read only pages/IDs named by the task. External WGU context is
   explicitly scoped in the card, never scanned through historical manifests.
3. Operator starts the selected executor manually using [the launch prompt](PROMPTS.md).
   Confirm Sol/high from UI/session metadata; requested settings are not evidence.
4. Record claim and checkpoint; implement only this increment; record changed files,
   checks, measured usage and unresolved assumptions. Preserve unrelated working changes.
5. Freeze delivery hashes and enter review. Operator supplies the review prompt to a
   separate reviewer. Evaluate source meaning separately from code mechanics.
6. Repair scoped findings, rerun affected checks and obtain a new review of changed hashes.
7. Coordinator records acceptance then done, renders views, makes the next eligible task
   ready, and prepares a new handoff. Do not start the next task just to finish this one.

## Refinement and corpus partitioning

`refine` tasks are not executable until exact prerequisites/paths/cases are pinned. Edit
the record to `implementation` or `content` after refinement; keep the decision in events.
For a corpus task, create bounded child records with explicit target IDs, context-only
IDs, source hashes/pages and disjoint output paths. The parent becomes a closure task
depending on children, while children inherit the parent's former dependencies (never
depend on the parent). Rewire downstream tasks through parent closure. Validate the DAG,
check target-set coverage without overlaps, and render child cards. No recursive platform
or agent manager is needed. Work partitions do not reduce the full-rulebook target.

## Checkpoints, interruption and conflicts

Write `private/workflow/runs/<task>/<attempt>/checkpoint.json` before starting and after
each usable increment: task/attempt, actor, actual config, base file hashes, changed-file
hashes, input packet hash, completed criteria, command results, blocker and next operation.
Freeze a delivery manifest of all reviewed files and record reports in the same run folder.
Do not overwrite prior attempts. A interrupted task remains in_progress until triaged.
Resume by comparing checkpoint hashes with disk and the current queue; record divergences,
retain both versions and resolve only owned files. Never reset, clean or stash the worktree.
If an unexpected writer changed an owned path, block that path and ask the coordinator
to integrate. A checkpoint is not a commit and never authorizes push.

At most two repair cycles per review finding and two retries for the same unchanged
failure. Then block with evidence and the smallest decision needed. A new hypothesis
or changed external condition must be recorded before another attempt. No silent scope
expansion or weakened tests to clear a blocker.

## Measurements and report

Record start/end UTC, elapsed wall time, executor/reviewer identities, requested and
observed configuration, token counts only if exposed, operator time only if reported,
tests and defect counts by severity. Unknown values are null, not zero. Separate code
quality from source meaning and full-profile readiness. No invented monetary cost.
Final handoff includes outcome, paths/hashes, criteria met/unmet, commands and exits,
independent review, human decisions where needed, remaining risks, and next exact action.

## Permissions and context limitations

Packets enforce their own allowlist and reject history paths, path escapes and symlinks.
They are not an OS sandbox for arbitrary tools. `.rgignore` controls default ripgrep only;
explicit paths, `--no-ignore`, other tools and Git can bypass search exclusions.
Read [archive isolation](../ARCHIVES.md) before any historical access. The current session
cannot migrate outside its writable roots or install under protected `.agents/`.
