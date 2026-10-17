# IG-4E: Generate complete dependent action domains

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4D](IG-4D.md)
- Human semantic acceptance required: false.

## Goal

Expose sound and complete legal choices without materializing every combination.

## Concrete deliverables

- legal_actions with exact dependent domains, lazy enumeration and revisioned pagination

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Validated actions and explicit semantic selectors/constraints

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/runtime/actions.py
- src/wgc/runtime/domains.py
- tests/runtime/actions/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Every legal result validates; independent exhaustive small-state oracle finds no omitted legal choice.
- Stable cursor binds package/state/window/actor/viewer/query; no omissions/duplicates across pages.
- Budget exhaustion is incomplete; blocked semantics is not an empty complete menu; no mutation or RNG in queries.

## Required validation

- Independent brute-force domains, mutual parameter constraints, pagination unions, changed cursor inputs and timeout behavior.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
