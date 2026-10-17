# IG-5B: Integrate strategic action selection

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-5A](IG-5A.md)
- Human semantic acceptance required: false.

## Goal

Connect an explicitly selected strategy client to the local player protocol without delegating legality.

## Concrete deliverables

- Strategy adapter boundary and offline reference policy
- Malformed/stale selection recovery

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Player protocol; operator-selected model/provider/budget only when later authorized

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- src/wgc/strategy/
- tests/strategy/
- docs/player/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Strategy sees only player-safe compact context and submits an exact action for runtime revalidation.
- Offline reference policy works without external API; live provider requires separate explicit authorization.
- Compare strategy quality separately from token cost; no hallucinated action applies state.

## Required validation

- Malformed/forbidden/stale action and context-limit cases; zero provider calls on legal-runtime paths.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
