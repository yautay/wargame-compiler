# IG-2A: Build independent source inventory tooling

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `done`; kind: `implementation`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-1E](IG-1E.md)
- Human semantic acceptance required: false.

## Goal

Create page/region inventory, evidence locator and coverage-accounting tools.

## Concrete deliverables

- contracts/ig/regions.schema.json and documented wgc-inventory-1 contract
- Local source page/region inventory, coordinate/evidence/coverage tools and synthetic tests
- private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/ inventories, evidence, repeatability and regression reports
- private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/ frozen repair delivery and independent-review handoff

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Official PDF private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf SHA256 e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e; independent physical page count 44
- Fresh official provenance private/ig/sources/spqr-5e-official/revision-20261013T155212Z/provenance.json SHA256 90ca669ff57bd499975fbf29353175caff5ee583cb0f4be588f37cf21d57959b
- Synthetic public layout/geometry/coverage cases; real evidence verification physical pages 1-4 only; all-page geometry and embedded-label accounting.
- Final coordinator refinement private/workflow/runs/IG-2A/attempt-20261013T155212Z/refinement.json; stable persisted identity and evidence/coverage contracts.

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- contracts/ig/README.md
- src/wgc/contracts/source.py
- private/workflow/runs/IG-2A/attempt-20261013T155212Z/refinement.json
- private/ig/sources/spqr-5e-official/revision-20261013T155212Z/provenance.json
- private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf
- private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/configuration.json
- private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/scope.json
- private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/dispositions-before.json

## Allowed write scope

- src/wgc/sources/
- tests/sources/
- contracts/ig/regions.schema.json
- private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/

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
- Explicit tests/sources with fresh short basetemp and -p no:cacheprovider; check.ps1 -Task IG-2A while active; workflow validate; git diff --check.
- Two fresh structural inventories with reused persisted registry; compare identical canonical bytes and region identities; independent Poppler and pypdf count; inspect real rendered pages 1-4.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
