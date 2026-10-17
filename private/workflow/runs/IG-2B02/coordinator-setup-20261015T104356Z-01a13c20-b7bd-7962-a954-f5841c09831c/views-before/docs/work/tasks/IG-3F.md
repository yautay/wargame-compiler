# IG-3F: Formalize calculations tables and chance

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-3E](IG-3E.md)
- Human semantic acceptance required: true.

## Goal

Formalize ordered calculations, table lookup/legend, loss allocation and random processes.

## Concrete deliverables

- Calculation/table/chance IR
- Exact arithmetic and probability cases

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Exact assigned clauses and pinned table/card source revisions

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- private/ig/projects/spqr/semantics/calculations/
- private/ig/projects/spqr/evaluation/calculations/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Bounded batches preserve units, ordered modifiers, rational values, rounding stage, raw/modified rolls and table notes.
- Pool multiplicity, shared draws and rerolls are explicit; unknown source values block compilation.
- Original symbols and conditional outcomes retain source links.

## Required validation

- Boundary cells, clamping, column shifts, noncommuting modifiers, duplicate symbols, rerolls and loss overflow, independently justified.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
