# IG-3B: Build revision-scoped review packets

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-3A](IG-3A.md)
- Human semantic acceptance required: false.

## Goal

Make source-meaning review and human acceptance practical without losing exact scope.

## Concrete deliverables

- Evidence/diff packet builder and decision ledger
- Freshness calculation and conflict diagnostics

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Source IG, typed proposals, profile revisions and human actor authorization record

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md

## Allowed write scope

- src/wgc/review/
- tests/review/
- contracts/ig/review.schema.json

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Packets show source, old/new proposal, exact aspects, dependencies and impact.
- Separate model observation, technical review and human semantic decisions.
- Changed basis becomes stale; incomplete basis unknown; contradictory decisions require explicit supersession.

## Required validation

- Partial acceptance, source/profile change, aspect reordering, conflicting reviewers and forged model-as-human decision.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
