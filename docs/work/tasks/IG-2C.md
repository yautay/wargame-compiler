# IG-2C: Implement reconciliation and source lookup

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-2B11](IG-2B11.md)
- Human semantic acceptance required: false.

## Goal

Connect WGU records to source regions with many-to-many mappings and an explicit discrepancy queue.

## Concrete deliverables

- Reconciliation tool and lookup by WGU ID/source label/text
- Source-versus-KB difference packets

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Whole independent inventory and complete KB snapshot

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md

## Allowed write scope

- src/wgc/reconcile/
- tests/reconcile/
- contracts/ig/reconciliation.schema.json

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Candidate matching does not imply identity or acceptance.
- Distinguish exact/partial/contradictory/missing/duplicate and edition conflicts.
- Keep source evidence, untouched import and proposed correction separately; preserve external references.

## Required validation

- Cross-chapter exception, split clause, editorial summary table, conflicting edition, wildcard and absent table source.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
