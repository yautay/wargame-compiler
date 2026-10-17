# IG-2D: Partition and close full-corpus reconciliation

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-2C](IG-2C.md)
- Human semantic acceptance required: false.

## Goal

Partition all inventory targets and imported records into reviewable reconciliation tasks, then close the entire source ledger.

## Concrete deliverables

- Explicit child task partition and target ledger
- Reconciled source IG with every target accounted for

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Whole inventory and import IDs with frozen hashes
- IG-2C discrepancy format

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md

## Allowed write scope

- docs/work/queue.json
- private/ig/projects/spqr/reconcile/
- private/ig/projects/spqr/reports/reconciliation/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Expand into child tasks of at most 20 clauses with exact target IDs, source ranges, outputs and acceptance before execution.
- Children inherit prior dependencies; parent becomes closure depending on every child. No dropped or duplicate work targets.
- Resolve cross-batch references; full rulebook and all imported records are represented or explicit gaps, not just a sample.

## Required validation

- Validate partition set equality and DAG; check all cross-batch references and separate coverage/gap counts.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
