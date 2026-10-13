# IG-1A independent re-review after repair cycle 1

Re-review only F1-F3 and their affected invariants in the same independently created
review session. Preserve your reviewer identity, distinct from the executor. Discuss
findings in Polish and write repository evidence in English. Do not create agents,
sessions, automation, commits/pushes or external API calls. Do not access archives,
Git history or neighbouring repositories. Do not repair the implementation or change
queue/status files, accept/done, or grant SPQR semantic acceptance.

Explicitly read docs/skills/wgc-review/SKILL.md and docs/work/WORKFLOW.md. Queue status
and task criteria remain authoritative in docs/work/queue.json. Read the new frozen
delivery private/workflow/runs/IG-1A/attempt-review-repair-01/delivery.json and report.md.
Anchor its expected SHA-256 to the latest IG-1A review transition, then verify every
artifact before assessment. Read the packet and context named in checkpoint-frozen.json;
workflow-generated status/card differences are expected control-plane changes.

Your previous report remains immutable at
private/workflow/runs/IG-1A/review-independent-20261012T164949Z-163b3167/review.json.
The original product bytes have been preserved under attempt-review-repair-01/baseline/
with baseline-manifest.json, since the working product paths now contain repaired bytes.
Do not attempt to validate old product hashes against current repaired paths and call
that an unexpected divergence. Compare the preserved bytes against the old frozen hashes.

Runtime configuration evidence is now available in reviewer-runtime-metadata.json in
the repair run. It extracts only model/effort/cwd/turn identity from the exact review
session's turn_context record, with recorded model gpt-6.1-sol and effort high. Verify
your current turn's configuration independently from metadata in the exact own-session
file named there. Read only session identity and turn_context configuration fields;
do not extract message, tool, reasoning contents or other session histories. Record
actual values and source, not merely creation parameters or the executor's UI evidence.

Bounded implementation changes:

- F1: coverage target_refs admit only node/evidence/relation source-content families.
  Gaps in either reference mode, alone or mixed with content, must reject. Metadata
  records are not content targets. Test positives for each allowed family and existing
  represented/partial cases; retain the distinction between structural claim and meaning.
- F2: exclusion needs a current complete accepted human source_composition review.
  coverage_boundary must exactly match purpose coverage_exclusion, inventory_ref,
  region_ref and representation level; the region is an exact full-record target and
  inventory is an exact full-record basis. Test unrelated/other-region/other-level/
  other-inventory/partial/stale/model decisions and missing target/basis metadata,
  plus a valid exact boundary. Try to falsify scope transfer or false freshness.
- F3: selected required/conditional relation endpoints must resolve to the selected
  exact revision. Historical pins are allowed only if they match selection. Test both
  endpoints, unselected and superseded revisions, both requirements, valid exact pins,
  valid historical informational mentions and unresolved source links retaining gaps.

The executor added 24 static fixture cases to the original 26. There are 70 contract
tests and 96 ordinary project tests. The original independent 16-case pytest suite
now passes when run by the executor, but that is not independent re-review acceptance.
Run it yourself and try further bounded counterexamples. Read the expectation catalogue
and check its independent contract basis, not just agreement with implementation.

Run scripts/check.ps1 and git diff --check, using new private check directories.
Write only a new review directory under private/workflow/runs/IG-1A/, and ordinary
check outputs. Preserve old reviews and all delivery artifacts. Pin the complete new
artifact list. Report F1-F3 fixed/unfixed with evidence, any new findings by severity,
each IG-1A criterion, actual configuration, command exits and measurements (unknowns
null). Leave queue state review; return the review evidence/report paths. Do not send
messages to other tasks. The operator/coordinator will read your result.
