# IG-1D: Persist identities and deterministic exports

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `implementation`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-1C](IG-1C.md)
- Human semantic acceptance required: false.

## Goal

Add stable identity mapping, reference diagnostics and deterministic source IG export.

## Concrete deliverables

- Identity/origin registry with split/merge lineage
- Validated snapshot export and reference report

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- IG-1C import records
- Versioned source contract and previous identity map

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md

## Allowed write scope

- src/wgc/wgu_adapter/identity.py
- src/wgc/wgu_adapter/references.py
- src/wgc/export/
- tests/wgu_adapter/
- tests/export/
- private/ig/projects/spqr/records/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Repeated identical bytes yield identical identities and export content; timestamps are outside canonical hashes.
- Reordering anonymous terms/relations preserves identities when unambiguous; collisions become review gaps.
- Many-to-many origin bindings preserve file/field locations; wildcard and subpoint references have exact targets or explicit unresolved scope.
- Export validates revision/hash closure and never inherits semantic approval.

## Required validation

- Reorder, insert, rename, delete, split/merge and ambiguous rematch sequences.
- Byte-level deterministic export; unresolved reference and cycle diagnostics without falsely requiring rule DAGs.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
