# IG-3H: Close full semantic coverage and acceptance

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-3G](IG-3G.md)
- Human semantic acceptance required: true.

## Goal

Reconcile all formalization batches with the complete source ledger and obtain exact human acceptance.

## Concrete deliverables

- Full semantic coverage/closure report
- Human decision ledger and executable-scope manifest

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- All source regions/clauses, semantic batches, technical reviews and human decisions

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- private/ig/projects/spqr/reviews/semantic-release/
- private/ig/projects/spqr/reports/semantic-closure/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Every clause is formalized, reviewed informational, or explicitly blocking; optional rules are accounted for.
- Source/meaning review covers the entire declared scope; unresolved contradictions/opaque dependencies prohibit executable release.
- Human acceptance pins revisions and profile, separately from code tests and model agreement.

## Required validation

- Independent coverage join, dependency-closure audit and cross-chapter source-derived regression review.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
