# IG-4C: Compile reproducible rules packages

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4B](IG-4B.md)
- Human semantic acceptance required: false.

## Goal

Compile accepted, closed semantic scope into a versioned deterministic artifact.

## Concrete deliverables

- Compiler, package manifest, source map and load-time validation

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Accepted semantic snapshot, profile and reference oracle

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/compiler/
- contracts/package/
- tests/compiler/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Reject opaque/unaccepted/stale/unknown executable dependencies and incompatible materials.
- Reproducible bytes, versioned operations, exact source/review revisions and dependency manifest.
- No hand-edited compiled semantics or unsafe arbitrary evaluation.

## Required validation

- Rebuild equality, tamper detection, unsupported op, stale review and missing dependency; reference/compiled expression parity.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
