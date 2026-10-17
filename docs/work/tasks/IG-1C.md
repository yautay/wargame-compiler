# IG-1C: Import all WGU collections losslessly

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `done`; kind: `implementation`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-1B](IG-1B.md)
- Human semantic acceptance required: false.

## Goal

Implement a safe directory adapter for wgu/kb@1 against the frozen complete input.

## Concrete deliverables

- Import records with raw bytes/unknown-field preservation
- Per-file and per-record accounting report

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Complete frozen input: private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json SHA-256 67ac53869ea80ea4d84018e253a9033e48fe89823d0a9a397ab8fe41b91d33d5
- Selected source registry: private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json SHA-256 615b1ae1cbeebf894c7f8dbbb7c3f2bcb0819427a342b3fa05bc690c33b9eed8
- Read-only support: C:/repo/wargame-utils/wgu/schemas/kb.schema.json SHA-256 0a93858ed3e0d99382ea962350e3b2994fab90b872a8b86584519b5a9e33a551
- Read-only support: C:/repo/wargame-utils/wgu/kb/store.py SHA-256 b7f3a6fc94c3b2bee27ccdb6bc82db0cecd1e3b3aafcf4aa3cf85726e1ed2bbe
- Read-only support: C:/repo/wargame-utils/wgu/kb/export.py SHA-256 b0735f52350abb7dfb8bd6e3f94bbe63789a0ffc2e7ae2eac040f00eede24b00
- Read-only support: C:/repo/wargame-utils/wgu/kb/lint.py SHA-256 78f5b2ade91eb1f69e5ef7f389077a6aba27e4b6f633780099e3abc5911cfabf
- Operator-authorized dependency exception: project-local pinned PyYAML safe parser only in .venv; obtain official PyPI metadata/wheel if no local wheel exists; record version/source/hash. No foundation edits.

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- src/wgc/inputs/snapshot.py

## Allowed write scope

- src/wgc/wgu_adapter/parser.py
- src/wgc/wgu_adapter/importer.py
- tests/wgu_adapter/
- private/ig/projects/spqr/runs/import/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Import rules, terms, nested procedures, tables, relations, ambiguities, changes, questions, terminology and auxiliary files.
- Unsafe YAML tags and duplicate keys fail with locations; errors do not become empty collections.
- Every unknown field/file is preserved or explicitly diagnosed; WGU verified/complete/resolved remains imported metadata.
- Refs/see remain navigation; questions are evaluation candidates, not battle scenarios or accepted expected results.

## Required validation

- Adversarial YAML, duplicate IDs/keys, extension fields, anonymous terms, nested step numbering and malformed records.
- Private integration checks all frozen files against independent manifest accounting.

## Blockers and escalation

- If a safe YAML parser is unavailable, record dependency failure; do not implement unsafe ad-hoc parsing.
- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
