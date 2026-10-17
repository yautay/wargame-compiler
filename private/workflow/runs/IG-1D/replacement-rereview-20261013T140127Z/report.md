# IG-1D repair iteration 1 replacement technical review

Result: **changes_requested**. R01, R02 and R03 are closed. R04's correction/rename behavior is fixed, but its exact named child-contract boundary remains incomplete. No new finding ID was introduced. One P2 finding remains, with one bounded repair iteration available (iteration 1 of maximum 2 already used).

Reviewer: `ig1d-replacement-reviewer-20261013T140127Z`, distinct from executor `ig1-stage-executor-20261013` and the unavailable previous reviewer. Actual configuration: GPT-6.1 Sol / high, freshly confirmed by the operator in this replacement chat (`potwierdzam`), recorded in configuration-confirmed.json. Previous reviewer/executor confirmation was not used as proof. This review uses the operator-authorized replacement exception; the previous re-review has no final review.json and was never treated as accepted.

Reviewed delivery: private/workflow/runs/IG-1D/repair-01-20261013/delivery.json, SHA256 `3ebef08719717c41043cb4df8bb98874d214e38d0e8fdbf21de6e35a9adfaa73`, exactly 50 artifacts, enumerated in reviewed-artifact-manifest.json and review.json. Every exact byte matched before and after review. The 119 checkpoint entries were verified through each verified_path; 69 parent versions, 182 foundation artifacts, 42 prior review artifacts, 43 prior review-manifest artifacts and all 36 previous re-review files also matched. Queue SHA256 remained `07cb9707259e91d1f779360ba4eb8606a3d2ae51502aaba53c4961a7e264e1e3`: IG-1A/B/C done, IG-1D review, IG-1E planned.

R04: identity.py:139-147 guards decision ID/operation/parents/basis, while identity.py:230-239 filters receipt children by kind/scope before deciding to allocate. Replaying a term merge receipt as a rule child filters out the old term; the empty candidate set allocates another child under the same named receipt. The unchanged receipt_edge_probes.py::test_named_merge_receipt_changed_child_kind_is_not_silently_reallocated fails once. This violates original R04's exact child-contract and changed/colliding-decision boundary. Require an atomic rejection or explicit retained conflict before allocation, with independent logical kind/scope/persistent-key checking and controls for deliberately new decision IDs. Preserve valid text correction/rename and keyed/multiple-child behavior. Detailed bounded requirements are in findings.json and dispositions.json.

R01 closure: contradictory term and step evidence retains candidates/origins as gaps; local and three-way controls pass, explicit hints resolve without extra allocation, and ordinary edit/reorder/rename/move controls pass. The public step-renumber fixture adds explicit authoring hints while retaining exact prior-ID assertions; strict negative gap controls remain. R02 closure: overlap is rejected before assignment with unchanged prior state; disjoint/many-to-many/lineage replay pass. R03 closure: exact active IDs and aliases use a singleton union, retaining ambiguity and excluding retired IDs; endpoint/navigation/scope/cycle/no-approval controls and full independently reconstructed diagnostics pass.

Validation:

- Public adapter/export suites: 93 passed, native execution exit 0.
- All 15 original reviewer probes: 15 passed, native execution exit 0, original bytes unchanged.
- Existing risk/receipt-edge probes: 9 passed, 1 failed (R04), exit 1; no unchanged defect retry.
- Existing export-history probes: 2 passed, exit 0.
- Required scripts/check.ps1 -Task IG-1D: 102 passed, exit 0; queue validation and dry-run passed.
- git diff --check: exit 0.
- Full independent accounting/two complete canonical transforms and publications: exit 0.
- Supplemental raw YAML unknown-location/reference/cycle oracle: exit 0.

Initial sandbox runs are retained: adapter/export 91 passed and 2 WinError 5 failures; original probes 14 passed and 1 WinError 5 failure; full accounting stopped with WinError 5 before inventory. Narrow local native runs with fresh directories passed all those unchanged assertions. No no-follow bypass, reinstall, or global configuration change was made. Exact argv, process-local PYTHONPATH, UTC, wall time and all exit codes/failures are in checks.json and individual logs. Cache disabled; fresh short basetemp per run.

Independent accounting measured 1,692 records and 38,206 YAML field/container locations across 59 manifest entries (23 available, 36 configured sources missing). It verified exact raw bytes, every entity value/parent/origin observation, 16,276 binding subtrees, aspect/record hashes and selected/historical reference closure. The frozen package has 18,303 source graph records and 18,262 identities. Supplemental inspection independently found 705 unknown roots encompassing 1,521 field/container locations, reconstructed 2,930 diagnostics (2,889 resolved, 41 unresolved) and independently matched cycle components. Counts follow enumerated raw inputs; importer counters were only cross-checked afterwards.

The selected current canonical package is `sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc`, taken from repair-01-20261013/full-export-accounting-final.json. Fresh seeded transform equals those exact canonical files; repeated transform and two real publications are byte-identical. Publications use separate actual operational sidecars under this review run. The operator-approved wgc-source-export-1 profile retains null canonical timestamps; original source-v1 schema/validator bytes remain frozen.

Measured evidence run: 2026-10-13T14:03:19.308477+00:00 to 2026-10-13T14:13:05.654345+00:00; 586.346 seconds. Earlier read-only instruction inspection was unmeasured and excluded. Full accounting wall time: 449.654 seconds. Tokens, cost and operator time are null. Configuration initially null was replaced only by a fresh operator-confirmation artifact, without overwriting the checkpoint.

Remaining gates: bounded R04 iteration-2 claim/repair, exact new delivery, independent re-review, then coordinator technical acceptance/done. IG-1E remains planned and was not run. Publisher coverage, source meaning/human semantic acceptance and executable readiness are separate and not granted; mixed-edition uncertainty and missing originals remain. The product, public tests, queue, generated documents and prior evidence were not modified. No commit, push, new chat, agent, worktree, automation, neighbouring repository access, Git/archive history inspection or external API was used.

All final review evidence is frozen by review-manifest.json; final-seal.json separately pins review.json and review-manifest.json to avoid circular hashes. The reviewer did not change queue state; the coordinator owns any later transition.
