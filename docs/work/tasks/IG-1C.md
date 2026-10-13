# IG-1C: Import all WGU collections losslessly

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `implementation`.
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

- Frozen input manifest from IG-1B
- WGU schema and store/export/lint code, read-only scoped files in C:/repo/wargame-utils/wgu/

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md

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
