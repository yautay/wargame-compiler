# IG-2A: Build independent source inventory tooling

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-1E](IG-1E.md)
- Human semantic acceptance required: false.

## Goal

Create page/region inventory, evidence locator and coverage-accounting tools.

## Concrete deliverables

- Source inventory contract and local tool
- Render/text provenance and coverage report

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Pinned full PDF and source manifest
- Synthetic multi-column, table/note and cross-page examples

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md

## Allowed write scope

- src/wgc/sources/
- tests/sources/
- contracts/ig/regions.schema.json

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Every PDF page and region is addressable with coordinate conventions and printed-label mapping.
- Text, images, uncertainty and reading order remain separate; duplicate context does not increase coverage.
- Unknown or excluded areas are visible; partial/gap is never represented.

## Required validation

- Synthetic missing-page, duplicate-region, overlapping-context, table-note and coordinate-conversion cases.
- Check independent PDF page count and stable region IDs.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
