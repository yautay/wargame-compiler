# IG-1A: final bounded F2 re-review

Continue in the same operator-authorized independent reviewer session, using the same
identity distinct from the executor. Re-review only F2-R1 and affected F1/F3 regressions.
Explicitly read docs/skills/wgc-review/SKILL.md and the local workflow. Verify the latest
IG-1A review-event SHA-256 for this run's delivery.json and every listed artifact.
Read report.md, checkpoint-frozen.json, the packet/context named there, and the prior
review-repair01-20261012T172231Z-9f8db531 report/evidence. Preserve every previous report.

The second repair adds whole_historical_ref to source.schema.json. Coverage inventory_ref
and review coverage_boundary.inventory_ref now disallow aspect_id. The existing exact
basis membership and whole-revision freshness logic is unchanged; generic historical_ref
continues to support aspect-scoped ordinary reviews. Only schema, README and catalogue
changed among existing product files; six static synthetic cases were added. Preserved
repair-01 product bytes are under baseline/, mapped by baseline-manifest.json.

Verify independently:

- Both saved F2-R1 counterexamples reject, including the changed full inventory with an
  unchanged aspect. Test coverage and boundary pin shapes separately, in current and
  retained records. Do not silently relax the documented full-record invariant.
- Exact full-record inventory boundaries still pass, even when the inventory has aspects.
  A changed full inventory makes the old full-record decision stale/rejected. Aspect-only
  review bases cannot authorize a full boundary. Generic aspect-scoped freshness remains
  unchanged outside exclusion and does not lose legitimate unrelated-aspect behavior.
- Re-run F1/F3 rejection/positive controls, original 16 independent bundles, your augmented
  bounded suite and all ordinary checks. Current executor outcomes are 102 project tests,
  95 augmented independent tests and 16 original tests passing; these are not your approval.

Confirm current turn model/effort from the exact own-session turn_context configuration
fields, retaining prior configuration evidence and reading no conversation/tool/reasoning
contents or other session histories. Record actual gpt-6.1-sol/high or an honest mismatch.
Write only a new review directory and fresh check outputs. Do not edit implementation,
schema/fixtures/tests, queue/status, prior reports/deliveries or baseline copies. Do not
create another session/agent/automation, use external APIs, read archives/Git history or
neighbouring repositories, commit/push, accept/done or grant SPQR semantic acceptance.

This is repair cycle 2 for F2; F1/F3 had one repair and were independently fixed. If F2
still fails, record the remaining counterexample and smallest operator/coordinator action;
workflow prohibits another silent repair cycle. Pin the complete current delivery list,
account for all IG-1A criteria, record findings/configuration/check exits/UTC measurements
and unknown counters as null, and leave queue review. Return the independent technical
result and review/evidence paths. Do not message other tasks; the parent reads the result.
