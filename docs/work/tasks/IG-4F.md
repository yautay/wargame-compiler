# IG-4F: Enforce player observation and explanation boundaries

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4E](IG-4E.md)
- Human semantic acceptance required: false.

## Goal

Implement visibility-safe views, legal attempts and diagnostics before AI integration.

## Concrete deliverables

- decision_view/explain and whole-response visibility policy

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Accepted visibility semantics and paired states with equal player observations

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/player/visibility.py
- src/wgc/player/explain.py
- tests/player/privacy/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- No secret-dependent leak through menus, reasons, counts, IDs, cursors, proofs or caches.
- Privileged outcome resolution is separated from permitted player attempts.
- Full response observational equivalence holds for indistinguishable states unless an authorized reveal occurs.

## Required validation

- Paired-state property tests over all response fields and error paths; deliberate leak mutations must fail.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
