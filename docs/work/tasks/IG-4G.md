# IG-4G: Apply source updates and replay regressions

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4F](IG-4F.md)
- Human semantic acceptance required: false.

## Goal

Support three-way source updates without losing identities, decisions or reproducibility.

## Concrete deliverables

- Update/impact report and rebuilt-package regression workflow

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Old/new WGU snapshots, current WGC corrections, profiles and accepted package

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/updates/
- tests/updates/
- private/ig/projects/spqr/runs/update-regression/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Unchanged identity persists; split/merge/delete and conflicts are explicit.
- Affected source/semantic reviews become stale/unknown conservatively across all dependency kinds.
- Old replay pins old package; new package runs declared regressions; no silent state/package migration.

## Required validation

- Change modifier/table/profile/binding/cause, conflicting local correction and incomplete graph; compare independent impact expectations.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
