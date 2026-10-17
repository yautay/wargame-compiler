# IG-5A: Deliver compact player decision protocol

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4I](IG-4I.md)
- Human semantic acceptance required: false.

## Goal

Provide a local compact interface with exact legal domains, safe details and revisioned deltas.

## Concrete deliverables

- Versioned player protocol, resynchronization and local client examples

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Visibility-safe runtime, budgets and package/state identities

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/player/protocol.py
- contracts/player/
- tests/player/protocol/
- docs/player/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Compression retains all player-available decision information and access to complete choices.
- Deltas detect missing revisions; cursors and IDs remain scoped; details respect visibility.
- Measure total decision context, including follow-up requests and resync.

## Required validation

- Round-trip view reconstruction, stale delta/cursor, large domains and paired-state privacy through the protocol.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
