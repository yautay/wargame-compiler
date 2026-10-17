# IG-4H: Establish performance and context budgets

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `planned`; kind: `refine`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-4G](IG-4G.md)
- Human semantic acceptance required: false.

## Goal

Measure a fixed representative corpus and obtain concrete acceptance thresholds before optimization.

## Concrete deliverables

- Benchmark harness, hardware/corpus manifest, baseline and agreed thresholds

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- Correct runtime and profile, representative large positions and reaction/choice cases

## Required context

- docs/IG-MECHANICS-PROFILES.md
- docs/IG-LEGAL-ACTIONS.md

## Allowed write scope

- bench/runtime/
- tests/bench/
- private/ig/projects/spqr/bench/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- Report p50/p95/p99, memory, cold/warm/invalidated cache, domain size and candidates.
- Measure view bytes/tokens with named tokenizer; unknown token values remain unknown.
- Owner agrees measurable thresholds on named hardware; zero LLM calls in legal paths is mandatory.

## Required validation

- Reproducible benchmark run; workload includes combinatorial choices and nested reactions, not only trivial positions.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
