# IG-1E: Accept full KB input accounting

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `implementation`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-1D](IG-1D.md)
- Human semantic acceptance required: false.

## Goal

Deliver a reproducible complete private KB import and a technical acceptance report.

## Concrete deliverables

- Private full-input import report and sealed structural snapshot
- Public synthetic integration regression suite

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Complete frozen KB and all adapter outputs
- Independent input inventory, not only adapter counters

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md

## Allowed write scope

- tests/integration/
- private/ig/projects/spqr/runs/import-acceptance/
- private/ig/projects/spqr/snapshots/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- No file/record/unknown field silently disappears; report processed/raw/error counts separately.
- Structural snapshot can be sealed with gaps; no claim of source coverage or semantic correctness.
- Document missing sources and required subsequent reconciliation; preserve mixed editions.

## Required validation

- Full private accounting and reproducibility run; independent reviewer samples mappings and checks entire file/record ledger.
- No archived fixtures, answers or gold required.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
