# IG-3G: Formalize visibility profiles and victory

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-3F](IG-3F.md)
- Human semantic acceptance required: true.

## Goal

Close profile applicability, hidden-information observation policy and victory semantics.

## Concrete deliverables

- Pinned runnable-profile proposal and compatibility decisions
- Visibility and victory IR/cases

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Full core rulebook, all optional-rule applicability, scenario/options choice and required materials

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- private/ig/projects/spqr/semantics/profile/
- private/ig/projects/spqr/evaluation/profile/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Exact clause batches cover visibility of state/actions/diagnostics and permitted hidden-information attempts.
- Profile pins edition, scenario, options, compatible tables/maps/counters and rule precedence with evidence.
- Immediate versus checkpoint victory and tie rules are explicit; unsupported material blocks profile readiness.

## Required validation

- Paired indistinguishable states, scenario override conflict, end-of-turn versus immediate victory and optional-rule applicability.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
