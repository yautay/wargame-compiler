# IG-3E: Formalize geometry and component contracts

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-3D](IG-3D.md)
- Human semantic acceptance required: true.

## Goal

Formalize spatial policies and required maps/counters separately from the textual rulebook.

## Concrete deliverables

- Spatial semantics and component input requirements
- Private spatial acceptance cases

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Exact spatial clause IDs, pinned map/counter material where available

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- private/ig/projects/spqr/semantics/geometry/
- private/ig/projects/spqr/evaluation/geometry/
- contracts/components/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Bounded source batches cover facing, multihex occupancy, movement, ZOC, LOS, paths and stacking.
- Specify metrics, edge/hex terrain, endpoint rules and existence/optimality/choice distinctions.
- Unavailable map/topology data is an explicit profile blocker.

## Required validation

- Source-justified multihex, sheet-label collision, tied path, facing/pivot, LOS boundary and stacking timing cases.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
