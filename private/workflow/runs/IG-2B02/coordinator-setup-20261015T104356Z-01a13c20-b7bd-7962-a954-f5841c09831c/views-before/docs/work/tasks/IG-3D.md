# IG-3D: Formalize action choices and continuations

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-3C](IG-3C.md)
- Human semantic acceptance required: true.

## Goal

Formalize action parameters, dependent choices, persistent participant bindings, reactions and costs.

## Concrete deliverables

- Private action/procedure IR and review packets
- Cancellation and continuation examples

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Pinned state/history contract and exact assigned source clauses

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- private/ig/projects/spqr/semantics/actions/
- private/ig/projects/spqr/evaluation/actions/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Partition into at most 20 clauses per child with exact IDs; cover all assigned action and reaction clauses.
- Define decision owners, binding lifetimes, invocation frames, priorities, resume/replace/cancel/restart, attempt/success costs and committed effects.
- Unknown ordering remains a blocker; no inferred global rollback or reselecting advantageous participants.

## Required validation

- Nested reactions, interrupted attempt, double-cost prevention, stale binding and competing triggers, with source-justified expected traces.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
