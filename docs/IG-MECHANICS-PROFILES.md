# Mechanical semantics and profiles

The shared IG represents mechanical concepts; each profile supplies the actual rules.
SPQR is first. OSG and GCACW remain future independent profile work, not prerequisites
or evidence that SPQR semantics generalize. Bibliographic and research history is outside
default context. This consolidation preserves its useful design constraints below.

## State, history and causes

State variables specify type, units, owner, bounds and reset rules. Boolean, enum,
integer, rational, set, reference and multiset/physical-instance pools are distinct.
Organization, activation, fatigue, losses, ammunition and command status can coexist;
do not collapse them into a universal status enum.

Events record cause, attempt/commit/invalidation state, read moment, ordered writes,
limits and reset window. Writes include set, increment, decrement, flip, move, remove,
schedule and invoke, with explicit targets. Equal final values can have different
consequences when caused by an action cost versus combat. Preserve rule-relevant history:
prior positions, first occurrence, attempted actions, counters, used participants and
already-paid costs. Missing history is unknown, not zero. Permission, obligation and
prohibition differ; attempt and success costs may differ.

## Time, reactions and continuation

Time is a hierarchy of instances: turn, phase, segment, activation, step and event as
needed by the profile. A phase name is not an occurrence. Counters scope to object,
side, activation, turn or game. Procedures specify actor, guard, inputs/outputs,
branches, loops, completion, failure and reaction windows.

Windows specify trigger, eligible player, opening/closing conditions, attempt limit and
resume/replace/cancel/restart policy. Continuations bind a particular invocation frame,
local environment and return point. Cancellation does not imply global rollback;
specify which effects, costs and history survive. Priorities and simultaneous resolution
must come from sources, including who breaks a tie. No universal reaction queue is assumed.
Temporary effects define start, expiry, checkpoint, snapshot reads and refresh rules.

## Choices and calculations

Choice contracts specify owner, selector, cardinality, constraints, binding ID, lifetime
and reselection policy. Player choice, automatic selection and randomness are different.
Bindings belong to invocation instances. Eligible, selected, committed, participating
and affected sets can differ. A participant used across several steps cannot silently
be replaced by a more advantageous one in each calculation.

Aggregation specifies set/filter/measure/operator and modifier order. Size, combat
strength and other measures use distinct units. Loss allocation specifies deciding
player, targets, proportions, overflow and elimination timing. Calculations are ordered
add/subtract/multiply/divide/compare/round/clamp/column_shift/lookup/decode/invoke steps.
Changing input strength, a die roll, a table column or the decoded outcome are distinct.
Use rationals where needed; rounding includes stage, method and beneficiary.
Modifier stacking explicitly defines addition, exclusion, replacement, cap or choice.

Tables preserve ordered axes, inclusive/exclusive boundaries, out-of-range and missing-cell
policy, units, merged cells, note scopes, meaningful decorations and legends. Lookup pins
the table revision and participant bindings. Outcomes retain original symbols plus ordered,
conditional effects and triggered procedures. A symbol without its legend is incomplete.

## Geometry

Locations qualify map, sheet and hex label. Geometry includes occupied hexes, anchor,
orientation, relative zones and pivot policy. Track hex/edge terrain, elevation and
infrastructure state. Movement, retreat, command, supply, ZOC and LOS are distinct
spatial policies even on the same hex grid. Specify metric, endpoints, rounding,
admissible nodes/edges, cost and exceptions. Multihex units count once as entities.

Distinguish path existence, all-path conditions, optimality and player selection of tied
paths. Reachability is not shortest path or retreat priority. Stack constraints specify
order/composition/limit/checkpoint. Off-map locations are named zones with ownership,
capacity and transfer rules. Unread topology can remain a source gap but blocks execution.

## Randomness, visibility and victory

Randomizers specify physical symbols, meaning, draw count, combination, independence,
replacement and pool composition. A d10 is not automatically 1–10. Store raw/modified
result, draw identity, reroll policy and sharing across targets. Pools with duplicate
symbols require multiplicity or physical identities; set semantics lose probability.
Unknown composition means unknown distribution.

Visibility applies to the entire observable response: state, domains, rejected choices,
reason codes, proof paths, gaps, identifiers, cursor metadata and caches. A privileged
tool's full state is not player knowledge. Define legal attempts under hidden information
and when outcomes reveal facts. Never filter only the final JSON field after computing
a secret-dependent action menu.

Victory specifies metric, counted set, checkpoint, comparison, termination and tie rule.
Scenario thresholds, immediate endings and end-of-turn assessment are distinct.
Territorial control may require history as well as occupancy.

## Mechanical dependency directions

| Relation | Direction |
|---|---|
| reads / writes | Assertion or step → state/resource definition |
| triggers | Event type with cause filter → procedure/step |
| schedules | Assertion or step → future window |
| resumes | Reaction procedure → parent continuation point |
| constrains | Constraint → choice/action/path/outcome |
| uses_binding | Step/assertion → participant/value choice definition |

Change impact follows all these links as well as tables, profiles and ordinary references.
An incomplete dependency graph cannot certify absence of regressions. Each capability
needs evidenced examples; merely adding a payload field is not support. Representation,
semantic review and resolvability of a particular query remain independent assessments.
