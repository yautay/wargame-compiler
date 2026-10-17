# IG-1D: Persist identities and deterministic exports

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `done`; kind: `implementation`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-1C](IG-1C.md)
- Human semantic acceptance required: false.

## Goal

Add stable identity mapping, reference diagnostics and deterministic source IG export.

## Concrete deliverables

- Identity/origin registry with split/merge lineage
- Validated snapshot export and reference report
- Operator-approved versioned source-export schema/profile with null canonical run timestamps and separate operational evidence

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json SHA-256 2999d63c680b4c52a095e0edb18952c70eefdf4baf7c2e01481840cda18ca61a
- contracts/ig/source.schema.json SHA-256 8593fb5f3929f72a97657593272c9089a34faeac74ce10a2f7a925a00fddab13
- contracts/ig/README.md SHA-256 c2d05b9cb20da646de21dc8b3f715799fae2006f06f322c7be800f0cb7e8db57
- src/wgc/contracts/source.py SHA-256 14aa5fd5129ed5f6ae65937a3f646407c3f1433483aa2145b53f942ed43509b1
- private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json SHA-256 67ac53869ea80ea4d84018e253a9033e48fe89823d0a9a397ab8fe41b91d33d5
- private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json SHA-256 615b1ae1cbeebf894c7f8dbbb7c3f2bcb0819427a342b3fa05bc690c33b9eed8
- private/workflow/runs/IG-1D/preflight-20261013/initial-registry.json SHA-256 37d6ae2aef4a5ba533b390e331ce748c6b84a3f13c857e799533195f1f903934
- private/workflow/runs/IG-1D/preflight-20261013/source-export.schema.proposed.json SHA-256 2a1f619eb4773d1432470cf0a340ac55c2f74451661c92002a6c89a7864bd768
- private/workflow/runs/IG-1D/preflight-20261013/operator-profile-approval.json SHA-256 201756c3941b21d8d2a73a23fbc77cc8aa8c5555bba793acacc7261319d0e512
- Approved deterministic source-export profile: wgc-source-export-1, mechanical/hash/reference rules unchanged; actual operational timestamps/configuration/measurements sidecar outside canonical artifact hashes. No frozen foundation edits.
- No previous identity registry exists; explicitly pinned empty namespace wgu.spqr seed. Persist allocations/aliases/lineage; array positions/content hashes/titles/filenames are never ID generators.
- Only NEW assigned test files; preserve IG-1C parser.py/importer.py and its accepted tests unchanged.

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- contracts/ig/README.md
- src/wgc/contracts/source.py

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
