# IG-1A: Establish the source IG contract

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `done`; kind: `implementation`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: None.
- Human semantic acceptance required: false.

## Goal

Turn the current proposal into a small versioned source-record contract that preserves all required mechanical concepts without implementing rules.

## Concrete deliverables

- contracts/ig/source.schema.json
- contracts/ig/README.md with canonicalization and reference rules
- Synthetic valid/invalid fixtures and validator entry point

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Current architecture/data proposal
- Synthetic clauses, evidence, groups, gaps and review records

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- contracts/ig/
- src/wgc/contracts/
- tests/contracts/
- pyproject.toml
- scripts/check.ps1

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Schema represents sources/regions, clauses with stable aspects and semantic groups, relations, gaps, origin bindings, coverage, profiles, runs, reviews and snapshots.
- ID and revision hash rules are explicit and deterministic; anonymous identities do not depend on array position.
- Source representation distinguishes review, coverage and executable readiness; source-level opaque is accepted without granting execution.
- State, causal history, parameters, persistent choices, reactions, continuations, costs, geometry, tables, chance and visibility have addressable source representations; no generic payload-only claim.
- No importer, formal interpreter, compiler or game logic is implemented; record open formal-language decisions for IG-3A.

## Required validation

- Use independent valid/invalid fixture cases for unknown value without gap, changed aspect, model approval, dangling active versus historical reference, duplicate identity and opaque execution blocker.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
