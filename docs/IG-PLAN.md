# Incremental product implementation

The owner has chosen the full SPQR 5E rulebook plus WGU KB as the first product scope.
This decision replaces the earlier small-pilot recommendation. The queue is
[queue.json](work/queue.json); stages below describe outcomes, not duplicate statuses.

| Stage | Lasting outcome | Main boundary |
|---|---|---|
| IG-1 | Versioned source contract, frozen inputs, complete WGU import | No semantic approval inherited from WGU |
| IG-2 | Independent whole-source inventory and reconciled source IG | Missing regions remain gaps, not coverage |
| IG-3 | Typed semantics, bounded formalization batches, separate source review | Human acceptance pins exact revisions and scope |
| IG-4 | Reference execution, compiler, legal runtime, updates and measured performance | No LLM in legality or state transitions |
| IG-5 | Compact player interface, strategy integration, full-profile release | Strategy filtering never defines legality |

Detailed tasks split IG-1 into contracts, input snapshots, parsing/import, identities,
and full-KB integration. IG-2 separates tooling from source work. Each four-page source
batch is independently reviewed; cross-page clauses carry explicit continuation links.
Reconciliation and formalization use exact ID lists produced from the inventory,
with at most 20 clauses per batch initially. A large clause is split into addressable
aspects without separating a condition from its effect. The coordinator can lower
the batch size when context or review cost grows.

Later task cards are bounded capability increments, not permission to implement an
entire stage. Cards marked `refine` cannot start until their exact inputs, outputs,
write scope, acceptance cases, and unresolved contract decisions are recorded in the
queue. Corpus coordinators expand into child tasks, one at a time or as an explicit
finite partition; they do not silently perform the entire corpus themselves.
All source inventory IDs must be assigned exactly once as work targets. Context overlap
is allowed and does not increase coverage. Parent completion requires accepted children
and a full coverage ledger with explicit residual blockers.

The full rulebook includes optional rules with applicability conditions. A runnable
profile additionally pins scenario, options, maps, counters, tables, and compatible
editions. A missing external card does not prevent importing the KB or representing
the rulebook, but blocks affected gameplay readiness.

Four distinct measures are mandatory: input accounting, source representation,
current human semantic acceptance, and executable closure for a profile. Report gaps,
exclusions, and represented content separately. Neither 100% import nor passing tests
is a semantic acceptance decision.

Quality evidence combines synthetic contract tests, private full-input integration,
source-justified expected cases, bounded exhaustive action oracles, differential
reference/compiled execution, replay and privacy tests. Imported WGU answers and the
36 earlier research cases are candidates, not independently accepted gold.

Measure wall time, model usage where observable, operator time where reported,
review/correction effort, and defects. Unknown measurements remain null. First
completed product increments improve estimates; they do not introduce another pilot gate.
