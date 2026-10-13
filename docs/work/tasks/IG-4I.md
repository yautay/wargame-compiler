# IG-4I: Optimize indexes and caches without semantic drift

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4H](IG-4H.md)
- Human semantic acceptance required: false.

## Goal

Meet agreed budgets using measured indexing/cache improvements.

## Concrete deliverables

- Optimized runtime with invalidation model
- Before/after performance and correctness report

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Measured hotspots, approved thresholds and reference implementation

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/runtime/
- src/wgc/compiler/indexes.py
- tests/runtime/
- bench/runtime/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Cache keys/invalidation include package/profile/relevant state/window/viewer dependencies.
- Action sets, reasons, event traces and privacy match reference; performance meets pinned budgets.
- No strategic pruning masquerades as complete legality.

## Required validation

- Differential warm/cold/invalidated tests, source-update invalidation, cross-viewer isolation and benchmark threshold checks.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
