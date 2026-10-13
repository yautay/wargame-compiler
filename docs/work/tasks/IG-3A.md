# IG-3A: Define typed semantic IR and validation

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-2D](IG-2D.md)
- Human semantic acceptance required: false.

## Goal

Specify a bounded executable language sufficient for SPQR with explicit source links.

## Concrete deliverables

- Versioned typed IR contract and static validator
- Operator semantics and unsupported-feature diagnostics

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Reconciled source IG; mechanical requirements and unresolved gaps

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- contracts/semantics/
- src/wgc/semantics/types.py
- src/wgc/semantics/validate.py
- tests/semantics/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Define typed state/history, actions/parameters, effects, windows, bindings, geometry policies, tables, chance and visibility.
- Specify evaluation order, units, unknown propagation and causal history; no arbitrary code or opaque runtime callbacks.
- Reject unbound variables, unit mismatch, unknown operation and incomplete executable dependencies.

## Required validation

- Independent positive/negative IR examples, typing and dependency-closure failures.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
