# IG-1B independent re-review — F1 repair cycle 1

**Technical result: PASS. F1 is closed on this exact repaired delivery.** No new actionable technical finding was found. Native Windows symlink creation was unavailable, as recorded below; actual junction rejection and no-follow traversal controls were independently exercised.

Reviewer: `reviewer-ig-1b-rereview01-20261012T194946Z`, in the same existing independent reviewer session, distinct from executor `executor-ig-1b-repair01-20261012T193641Z`. Actual reviewer configuration is GPT-6.1 Sol/high from the earlier direct operator UI confirmation in this conversation, preserved with explicit same-session continuity in `configuration.json`. No model/settings change is reported in the current conversation. Runtime configuration metadata remain unavailable; executor and requested creation settings were not used as reviewer evidence.

Reviewed delivery: `private/workflow/runs/IG-1B/attempt-review-repair-01-20261012T193641Z/delivery.json`, SHA-256 `cf1c928b34aa70ae5b7cf59928baa273c45b02fc26331f8f534f6d1d8056c236`. All **66 unique artifact paths/hashes** match before assessment and after execution. All 34 previous product byte copies match their old hashes; the prior 59-artifact delivery matches through the explicit baseline mapping. Earlier reviewer evidence and the 82 accepted IG-1A hashes remain preserved. The current queue stays at `review` for IG-1B with SHA-256 `b885ed281d0a374f259515635cdbe8f53a48393860a238cabe8b5c60a59a5b51`.

## F1 disposition and affected risk assessment

F1 previously allowed an extra KB file, a blob for a manifest-declared missing source, and an unlisted junction to remain in a verified/reused snapshot without changing its ID. The saved reviewer scripts were copied byte-for-byte into this new directory and independently executed here. All **14 original expectations now conform**, including those three counterexamples. Each now rejects at verification, before the old probe can reach its subsequent reuse step. The separate input/source verify/reuse matrix independently exercises corrupt-target reuse and preservation.

The repair adds `verify_tree_names` and changes only `_verify_snapshot` among existing source functions/classes. The permitted files are derived from available manifest blobs, root `manifest.json`, and root `source-pin.json` only for source snapshots. Permitted directories are exactly the parents of those files. The verifier scans no-follow entry metadata, rejects symlinks/reparse points, unknown files or directories and nonregular types, and compares the complete actual and permitted sets. Missing entries add no allowed blob. This happens before copied-byte or source-pin reads. The same check gates first publication's staging verification, published verification, and existing-target verification before staging cleanup/reuse. Existing corrupt snapshots are not overwritten.

Independent affected-risk probes additionally confirm, for both snapshot kinds:

- Declared blobs replaced by directories reject under direct verification and reuse, while manifest/pin bytes and the replacement entry are retained.
- Deleted available blobs reject because the exact allowed set is incomplete.
- An actual junction replacing the required `files` parent rejects without scanning or opening its destination, even when that destination contains the formerly valid copied files.
- Simulated nonregular declared-entry metadata (`S_IFIFO`) rejects before copied content is opened. The probe also asserts that entry metadata are requested with `follow_symlinks=False`. A real Windows FIFO is not claimed.
- Extra staging metadata rejects before publication and before any copied blob/pin read. Rejected staging remains evidence. For a failed input-stage publication, a previously valid source snapshot can remain, consistent with the documented separate publication operations.

Those **12 additional available probes pass**, with tracked target reads limited to `manifest.json` and no unexpected content reads/link traversal. The original 18 appended tests cover extra bytes, metadata, empty directories and actual junctions in both input/source snapshots and both verification/reuse modes, plus missing-entry blobs in verification/reuse. Their expectations follow the immutable byte-accounting and link-rejection contract, not mere agreement with the verifier.

F1 used **one repair cycle**. The original finding and FAIL report remain immutable; this is a new independent disposition for the new hash set. No reviewer repairs were made.

## Every card criterion

| Criterion | Result | Independent evidence |
|---|---|---|
| 1. Every input file has path, bytes, hash, role and availability; detect change during copy. | Met. | Exact sealed file/parent sets now complement the existing pins, same-handle metadata checks, independent copy hashes, global origin rehash and mutation/name-set controls. The native suite and saved copy/ctime/mutation probes pass. |
| 2. Missing 36 historically configured source paths are rechecked and reported, not silently substituted. | Met. | The byte-identical private audit independently compares the exact current WGU configured path set, request, advisory inventory, input manifest and availability report. All 36 named paths remain missing with null byte/hash/blob evidence. |
| 3. Pin the promoted PDF as a new selected source with identity_to_wgu_original unknown. | Met. | Exact PDF/provenance copies and canonical source pin remain unchanged, preserve `new_ig_source`, `unknown` and `not_granted`, and link the exact source snapshot ID. |
| 4. Reject path escapes, linked paths and unintended source reads; no neighbour writes. | Met within the recorded Windows validation scope. | Original path/case/physical-alias/handle/disjoint-output controls pass. Unknown sealed entries and actual junctions reject without content reads or traversal, including a linked required parent. Actual symlink creation is unavailable on this host; no successful native symlink assertion is claimed. |

All four task criteria are technically met; no implementation criterion remains unmet. This review grants neither human semantic acceptance, source coverage nor executable/gameplay readiness. The promoted PDF remains a selected new IG source whose identity with the missing WGU original is unknown.

## Commands, results and limitations

`workflow.py validate`, `next`, and `packet --task IG-1B` each exited 0. Queue authority reports IG-1B as `review` and no ready task. The new packet is `private/workflow/packets/IG-1B-f92be3fad15e43f7aeb9b6dd555f2a1d`. The pinned repair packet/context and prior delivery/review references match their recorded hashes. The selected card remains byte-identical to the prior review-state card.

The first explicit native input run exited 1 with 47 passed and four fixture errors in 6.29 seconds. Its long reviewer-directory basetemp caused `WinError 206` when the empty-directory cases attempted to create paths over the Windows path limit. The assertions under test were not reached for those four cases. This was resolved by a new shorter basetemp, `private/workflow/checks/r1-1954`, without any implementation, test, assertion or global configuration change. The unchanged full suite then exited **0: 51 passed in 5.33 seconds**. Both attempts and exact logs remain preserved.

The saved `review_controls.py`, `native_handle_probe.py` and `private_audit.py` each independently exited **0** in this new reviewer directory under normally reviewed local native execution. The handle proof records the exact native rejection `opened source escaped its exact enumerated path` before yielding a readable stream, and separately confirms a normal read handle denies writes. The private audit independently measures **25 matching copies / 5,199,801 bytes**, comprising 23 WGU files and two registry files, checks all 36 missing sources, canonical IDs/metadata/pin/availability and exact published tree names, and performs two real repeats. Both repeats preserve identical IDs and bytes and leave no pending staging in the assigned real roots.

The initial `closure_probes.py` invocation exited 1 because Windows refused file-symlink creation with **WinError 1314: a required privilege is not held by the client**. The local command had been approved; this is an OS privilege limitation, not an automatic approval rejection or observed verifier failure. No privilege/configuration change or bypass was attempted. Actual file- and directory-symlink rejection values are **null**. The remaining unchanged assertions were continued from byte-identical script copies in another fresh synthetic subdirectory: `run_closure_available.py` exited **0**, with all 12 available probes passing. Real junctions exercise Windows reparse-point rejection and traversal prevention; source inspection independently confirms the explicit `S_ISLNK` check and no-follow stat call. That evidence supports F1 closure on this host, while a real symlink-capable host remains useful additional portability verification. No unavailable symlink assertion was converted into a passing result.

`pwsh -NoProfile -File scripts/check.ps1 -Task IG-1B` exited **0: 102 inherited tests passed in 33.82 seconds**, with plan/dry-run/pytest/diff exits all 0. Its new evidence root is `private/workflow/checks/active-ecae2f1886a748fe80758f6b96da283f`. The 51 input tests remain explicit and separate from the inherited default project testpaths. Explicit `git diff --check` exited **0**; only the existing line-ending warnings appear.

Exact commands/argv, exits, UTC timestamps and measured command wall times are recorded in `native-checks.json`, the other command JSON files and `review.json`. Failed environment/setup attempts are separately retained as check history; they do not conceal product failures or claim unavailable measurements.

## Scope, preservation and handoff

Independent baseline/current comparison confirms that only the three authorized product paths changed: `src/wgc/inputs/snapshot.py`, its local README, and `tests/inputs/test_snapshot.py`. Every previous input-test source byte is an unchanged prefix; two parametrized functions add 18 cases. Other existing source functions/classes, including native handle checks, same-handle ctime/path signatures, origin rehash, disjoint destinations, publication and cleanup controls, are unchanged by AST comparison. `repair-scope-verification.json` and the independent source diff record this.

After all tests and private repeats, preservation reverified all 66 current delivery artifacts, 34 baseline copies, the mapped prior 59-artifact delivery, prior reviewer artifacts/reports and all 82 accepted IG-1A hashes, along with both delivery manifests and queue. They remain unchanged. Reviewer writes are restricted to fresh review/check evidence and synthetic fixtures; real repeats use only the pinned origins and assigned snapshot roots. No implementation/tests, frozen reports or queue were edited by the reviewer. No archive/Git-history access, neighbouring writes, external services, other-chat messages, additional chats/agents, automation, commits, pushes or next task were used.

The measured re-review interval starts at the current-session UTC marker `2026-10-12T19:49:46+00:00`; the final end and wall seconds are in `review.json`. Complete-session start, token counts, operator seconds, cost, peak memory and gameplay performance are unavailable and null. Technical open defect counts are zero; one prior P2 is closed. Source-meaning defect counts remain null because meaning review was not performed.

Next action belongs to the coordinator/operator: assess this independent technical PASS and record the appropriate disposition for the exact frozen delivery. Queue status is deliberately unchanged at `review`; this reviewer does not claim accepted/done or start IG-1C.
