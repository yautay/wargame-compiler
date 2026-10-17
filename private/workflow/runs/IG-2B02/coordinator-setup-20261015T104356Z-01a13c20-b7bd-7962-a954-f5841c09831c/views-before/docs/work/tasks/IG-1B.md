# IG-1B: Freeze input and source manifests

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `done`; kind: `implementation`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-1A](IG-1A.md)
- Human semantic acceptance required: false.

## Goal

Create a read-only snapshot facility for an explicitly enumerated WGU game directory and source registry.

## Concrete deliverables

- Immutable byte snapshot and manifest
- Source availability/edition/identity report
- Active SPQR source pin record

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- C:/repo/wargame-projects/games/spqr/wgu.yaml and kb/ (read-only)
- private/ig/sources/spqr-5e/provenance.json and PDF
- Prior inspection inventory is advisory, rehash actual input

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- private/ig/planning/wgu-spqr-2026-10-11/input-inventory.json
- private/ig/sources/spqr-5e/provenance.json

## Allowed write scope

- src/wgc/inputs/
- tests/inputs/
- private/ig/projects/spqr/inputs/
- private/ig/projects/spqr/sources/
- contracts/ig/input.schema.json

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Every input file has path, bytes, hash, role and availability; detect change during copy.
- Missing 36 historically configured source paths are rechecked and reported, not silently substituted.
- Pin the promoted PDF as a new selected source with identity_to_wgu_original unknown.
- Reject path escapes, linked paths and unintended source reads; no neighbour writes.

## Required validation

- Simulate mutation during snapshot, missing source, duplicate path/case alias, traversal and symlink/junction escape.
- Verify independent copy hashes and repeatability; full private snapshot count is measured, not hard-coded.

## Blockers and escalation

- Source selection needs an explicit record; missing auxiliary sources block only dependent verification, not the available KB snapshot.
- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
