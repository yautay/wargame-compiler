# IG-4D: Validate and apply actions atomically

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4C](IG-4C.md)
- Human semantic acceptance required: false.

## Goal

Expose revision-bound action validation and deterministic state changes through the compiled runtime.

## Concrete deliverables

- validate_action/apply_action and chance boundary interface

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Pinned package, authoritative state/history, actor and full parameters

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/runtime/validation.py
- src/wgc/runtime/engine.py
- tests/runtime/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Validate current package/revision/actor/window and parameters again at application; stale action has no effects.
- legal/illegal/blocked are distinct; costs apply once, source links preserved.
- Compiled traces equal reference traces for accepted source cases.

## Required validation

- Stale revision, wrong actor, malformed params, duplicate submission, concurrent revision change and reference differential traces.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
