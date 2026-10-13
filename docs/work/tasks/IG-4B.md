# IG-4B: Execute procedures reactions and chance by reference

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4A](IG-4A.md)
- Human semantic acceptance required: false.

## Goal

Extend the reference interpreter through decision/chance boundaries with explicit event semantics.

## Concrete deliverables

- Reference procedure executor, event log and replay

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Accepted procedure IR, state evaluator and recorded random outcomes

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/reference/procedures.py
- src/wgc/reference/events.py
- src/wgc/reference/replay.py
- tests/reference/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Preserve invocation-local bindings, causes, costs once, reactions, cancellation policy and authoritative draw results.
- Replay with same package/state/actions/draws yields identical state and event hashes.

## Required validation

- Nested reactions, interrupted attempts, duplicate application, invalid chance result, cancellation and replay tampering.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
