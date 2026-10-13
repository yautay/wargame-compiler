# Deterministic legal action contract

The source IG provides evidence; typed semantics describe rules; the immutable compiled
package supports fast local execution. See [architecture](IG-WGU-ARCHITECTURE.md).
This is a logical library interface, not an HTTP service or implemented runtime.

| Operation | Input | Output |
|---|---|---|
| decision_view | State, profile, viewer | Permitted observations and current decision owner/window |
| legal_actions | State, package, entitled actor | Legal actions or exact parameter domains with dependent constraints |
| validate_action | Package ID, state revision, actor, complete action parameters | legal / illegal / blocked and stable permitted reason codes |
| apply_action | Action revalidated against the same package and current revision | Atomic state/event delta up to the next decision or chance window |
| chance_options | Chance node, rule/pool state | Permitted outcomes, probabilities and requirements |
| resolve_chance | Allowed result from authoritative randomness | Deterministic continuation and recorded draw |
| explain | Validation result or event trace, viewer | Visibility-safe reason and evidence references |

Queries do not mutate state or draw randomness. The same package, state, history and
action give identical results and stable ordering. Record random outcomes for replay;
the player model does not control the random source. Validate package ID, state revision,
decision window, actor and parameters again at application. A previously offered action
ID is not lasting authorization. Stale proposals have no effects or paid costs.

Execution preserves invocation-local bindings, reaction ownership, continuation stack,
cause, timing, attempt/success costs and committed event history. Apply each cost once.
Define transaction boundaries at decisions/chance nodes and the profile's cancellation
policy. Reactions do not automatically resume a parent; cancellation is not global rollback.
Replay checks all event/state hashes with the pinned package and recorded random outcomes.

## Soundness, completeness and unknowns

Every fully specified action labelled legal must pass validation (soundness). Every
legal action in the declared scope must be represented (completeness). A strategic
shortlist is a separate AI layer and cannot redefine either property. Generator-validator
agreement alone is insufficient: they can share the same omission. Compare against
source-justified expected cases and exhaustive small-state oracles using an independently
written enumeration, then compare reference and compiled execution.

Avoid materializing a giant Cartesian product of actors, targets, paths and orderings.
Expose exact domains and constraints, bind parameters stepwise, and enumerate lazily.
Cursors pin package/state/window/viewer/query; pagination must not skip or duplicate
choices. Time limits explicitly mark incomplete output. First-page absence does not mean
illegality. Broad candidates are not legal until checked. Missing history, source rules,
profile or data yields blocked, not illegal or an empty complete menu.

Opaque or unresolved meaning affecting legal choices, timing, visibility, cost or effect
blocks executable readiness. The runtime never asks an LLM to fill that gap. A profile
release needs closed dependencies, including external tables, maps and counters.
Complete import, full source representation, semantic acceptance, successful compilation
and gameplay readiness are separate claims.

## Information boundaries and AI context

Define legal attempts under player knowledge separately from privileged outcome resolution.
Two states indistinguishable to a player must not leak forbidden information through
menus, reason codes, explanations, counts, cursors, identifiers, caches or deltas. Test
the whole response, not just visible fields. Cache keys include package, profile,
revision/dependencies, decision window and visibility context. Audit observable timing
where secret-dependent work could expose information.

AI receives compact observations, stable visible object IDs, exact choices/domains and
strategic features the player may know. It can request permitted details. Default context
excludes the full rulebook, IG, proofs and irrelevant history. Revisioned deltas must detect
gaps and trigger resynchronization. Compression must preserve player-available information
and action completeness. Failed/malformed AI selections are rejected locally with no mutation.

## Performance and regression evidence

Establish a simple reference executor before optimization. Compile type checks and static
dependencies ahead of play. Index by window, action type and object type; invalidate
caches through affected state dependencies. Compare every optimization with the reference.

Measure zero LLM calls on legal paths; p50/p95/p99 latency and memory; cold/warm/invalidated
cache; candidate/domain counts; large states, nested reactions and combinatorial paths;
player-view bytes and token estimates with named tokenizer; details requested per decision;
replay agreement, privacy and exact action coverage. Operator approves concrete thresholds
on named hardware and a fixed state corpus before performance acceptance. No latency or
token claim is accepted without measurement. Lower context cost alone does not prove
better strategy. Source changes trigger revision impact review, rebuilt packages and regressions.
