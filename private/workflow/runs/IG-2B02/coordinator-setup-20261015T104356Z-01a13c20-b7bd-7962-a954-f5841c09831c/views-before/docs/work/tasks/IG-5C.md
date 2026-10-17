# IG-5C: Accept the full SPQR profile release

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-5B](IG-5B.md)
- Human semantic acceptance required: true.

## Goal

Release the full declared SPQR profile only when coverage, meaning and execution gates are independently met.

## Concrete deliverables

- Versioned release manifest and readiness report
- Reproducible end-to-end replay, privacy and benchmark evidence

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Complete core instruction coverage, compatible required materials, accepted semantics, package and strategy protocol

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- private/ig/projects/spqr/releases/
- docs/releases/
- tests/integration/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Report import, coverage, human acceptance, compiled closure and playable-profile readiness separately.
- All scope dependencies are available; blocking opaque, missing materials and stale acceptance prevent release.
- Independent review and owner acceptance name exact profile/revisions; future scenarios/OSG/GCACW need new tasks.

## Required validation

- Full-source ledger audit, source-based situation regressions, complete action oracle suite, replay, paired-state privacy and agreed performance/context budgets.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
