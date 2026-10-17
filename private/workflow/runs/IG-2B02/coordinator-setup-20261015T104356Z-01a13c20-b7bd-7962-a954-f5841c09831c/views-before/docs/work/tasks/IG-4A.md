# IG-4A: Implement reference state and expression evaluation

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-3H](IG-3H.md)
- Human semantic acceptance required: false.

## Goal

Build a simple deterministic semantic oracle before compilation or optimization.

## Concrete deliverables

- Reference typed expression evaluator and state/history representation

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Accepted typed IR and independent source-backed expression cases

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/reference/state.py
- src/wgc/reference/expressions.py
- tests/reference/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Explicit arithmetic/unknown semantics, no input mutation and stable evaluation order.
- Runtime imports no provider or LLM client.

## Required validation

- Boundary arithmetic, unit errors, missing history, deterministic state serialization and mutation checks.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
