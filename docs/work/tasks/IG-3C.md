# IG-3C: Formalize state and causal history

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-3B](IG-3B.md)
- Human semantic acceptance required: true.

## Goal

Formalize state variables, temporal instances and causal event/history requirements for the full assigned SPQR rule set.

## Concrete deliverables

- Private typed state/history definitions and clause bindings
- Source-justified transition/history cases

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Exact reconciled clause IDs assigned during refinement
- IG-3A IR and IG-3B review format

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- private/ig/projects/spqr/semantics/state/
- private/ig/projects/spqr/evaluation/state/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Partition assigned clauses into bounded children if more than 20; pin source evidence and complete ownership.
- Different event causes, attempt/commit/cancel and reset scopes remain distinct.
- Missing history blocks dependent conclusions; no default-zero substitution.

## Required validation

- Source-backed cases with same present state but different histories/causes and expected outcomes.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
