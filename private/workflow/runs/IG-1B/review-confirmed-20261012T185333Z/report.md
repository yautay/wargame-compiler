# IG-1B independent technical review

**Result: FAIL. One P2 finding requires repair before technical acceptance.**

Reviewer: `reviewer-ig-1b-confirmed-20261012T185333Z`, distinct from executor `executor-ig-1b-20261012T182300Z`. The operator confirmed the current reviewer session's GPT-6.1 Sol/high configuration with “potwierdzam” in response to the explicit current-session UI question. `configuration.json` records that source; requested creation settings and executor confirmation were not used as evidence. The earlier configuration-pending preflight directory remains preserved.

The reviewed frozen manifest is `private/workflow/runs/IG-1B/attempt-20261012T182300Z/delivery.json`, SHA-256 `c76162309a0cdd3c9be6d0d1e0c57496c005cf31e61cf77ed9e5751d772487b8`. All 59 unique artifact paths and hashes match. The 34 product artifacts also match the frozen checkpoint's exact changed-file list. Hashes were verified before substantive assessment and again after tests and real private repeats. All 82 accepted IG-1A artifacts remain unchanged. The queue remains `review` for IG-1B and retains SHA-256 `1ff2113c596116a2c3c194e9081546697e44adb089f90925665b4ef6fc01de8a`.

## F1 — P2: Reject unmanifested files and links when verifying a sealed snapshot

Location: `src/wgc/inputs/snapshot.py:266-280`, especially the missing-entry `continue` at lines 271-274; existing-target reuse at lines 301-304.

`_verify_snapshot` checks only paths listed in the manifest. It does not inventory the sealed directory's actual names or inspect unlisted descendants for reparse points. Therefore an existing snapshot can acquire additional data or a junction, still pass `verify_snapshot`, and be reused under the same content-addressed ID. The existing-target branch discards its freshly built staging directory after that incomplete verification and preserves the unexpected entries.

Independent, native Windows reproductions in `review_controls.py` create a valid synthetic snapshot and then, before verification/reuse, separately add:

- `files/kb/unlisted.yaml`, absent from the manifest;
- `files/docs/original.pdf`, whose manifest entry still states `missing` with null byte/hash/blob evidence;
- an actual junction at `files/kb/unlisted` pointing to a synthetic directory outside that sealed tree.

All three cases should reject under the immutable-byte-manifest, link-rejection and append-only-integrity contracts. All three instead pass verification and `freeze_inputs` reuse, return the identical previous result/ID, and retain the added entry. `review-controls.json` records expected rejection and actual acceptance. The command exits 1 because these three expectations fail; the other 11 independent expectations conform. This is one defect with three reproductions, not three independent defects.

Consequence: a consumer trusting successful verification and subsequently enumerating `files/kb` can see data that is absent from the hashed manifest, or traverse a junction outside the frozen tree. Extra bytes can also coexist with a recorded missing-source entry. No such extra entries were found in the actual frozen SPQR delivery, and the reproductions do not show source-byte consumption through the extra junction by this snapshot module. The integrity guarantee nevertheless fails for ordinary static tampering performed before reuse; no concurrent destination writer is needed. The documented exclusion for hostile concurrent destination writes does not cover this case.

Required verification after repair: derive and enforce the allowed sealed-tree file set from manifest blobs plus the documented metadata files, inventory names without following links, reject unexpected files and reparse points, and reject a blob for a missing entry. Apply the check to published verification and reuse; do not overwrite a corrupt existing snapshot. Add input/source snapshot controls for extra bytes, missing-entry blobs and real junctions/symlinks. Preserve the original positive byte oracles, repeatability, tampered-byte/pin rejection, cleanup boundaries and native handle assertions. Rerun the explicit input suite, these three controls, the project check, private repeat/copy audit and preservation checks against a new frozen repair delivery. No repair was made in this reviewer session.

## Criteria

| Card criterion | Result | Evidence and remaining gap |
|---|---|---|
| 1. Every input file has path, bytes, hash, role and availability; detect change during copy. | Partially met; overall unmet due to F1. | Delivered manifests account for all 25 copied inputs and 36 missing configured paths. Pins, native write sharing, same-handle signature checks, global rehash, name-set mutation and independent copy corruption controls work. Sealed-tree completeness on verification/reuse is not enforced. |
| 2. Missing 36 historically configured source paths are rechecked and reported, not silently substituted. | Met. | Independently extracted the exact path set from the current pinned `wgu.yaml` source block and compared it with the request, advisory inventory, input manifest and availability report. All 36 paths were individually rechecked and remain missing; null evidence is preserved. |
| 3. Pin the promoted PDF as a new selected source with identity_to_wgu_original unknown. | Met. | Exact promoted PDF/provenance bytes match the request and both copied registry files. The canonical pin retains `new_ig_source`, `unknown`, `not_granted`, and the exact source snapshot ID. Edition is declared provenance, not publisher-meaning verification. |
| 4. Reject path escapes, linked paths and unintended source reads; no neighbour writes. | Partially met; overall unmet due to F1. | Initial traversal/case/physical-alias controls, actual Windows junction checks, safe final-handle checks, unlisted-registry no-read control and disjoint-output controls pass. A static unlisted junction inside an already published snapshot is accepted on verification/reuse. |

Met criteria: 2 and 3. Unmet criteria: 1 and 4, limited to F1; their passing subcontrols are retained above. No source meaning, coverage, human semantic acceptance, gameplay legality or executable readiness was assessed or granted.

## Independent checks and exact accounting

- `workflow.py validate`, `next`, and `packet --task IG-1B` exited 0. The fresh packet is `private/workflow/packets/IG-1B-92d157a2197d4d95b70373af84a50223`. The original packet/context hashes match the delivery. `packet-card-diff.txt` proves the selected card changed only from `ready` to `review`.
- Explicit `tests/inputs` with new restricted basetemp exited 1: 15 passed, 18 failed in 3.83 seconds. Failures are the independently reproduced sandbox denial of final-handle-path inspection (WinError 5) and actual link creation; there was no protection removal or assertion weakening.
- The same frozen explicit `tests/inputs` suite with a distinct fresh native basetemp and reviewed local escalation exited 0: 33 passed in 2.35 seconds. It exercises original-byte oracles, repeatability, mutations between files, appearing/missing inputs, traversal/ADS/device/case aliases, physical hardlink aliases, actual junctions, opened-handle redirection, canonical metadata and corrupt reuse.
- `review_controls.py` under reviewed local escalation exited 1: 11 conforming expectations and three failing expectations demonstrating F1. Additional passing controls cover same-handle ctime change with stable size/mtime, independent copy corruption, disappearing configured/KB files, four destination-overlap cases, canonical-but-altered pin rejection, cross-root physical aliases and no unlisted registry content reads.
- `native_handle_probe.py` under reviewed local escalation exited 0. With only ancestry prechecks disabled to simulate a lost race, an actual junction produces the precise native error `opened source escaped its exact enumerated path` before a readable stream is yielded. A normal opened read handle separately denies writes and retains original bytes.
- `private_audit.py` under reviewed local escalation exited 0. It independently verifies all 25 copies against the explicitly pinned originals, measures 5,199,801 bytes, confirms 23 WGU files and two registry files, checks canonical metadata/content-addressed IDs, compares exact sealed file sets, verifies the availability report and source pin, and performs two real `freeze_inputs` calls writing only the assigned input/source snapshot roots. Both repeats preserve identical IDs, manifests and bytes and leave no pending staging.
- `pwsh -NoProfile -File scripts/check.ps1 -Task IG-1B` exited 0: 102 inherited tests passed in 36.54 seconds; plan, dry-run, tests and diff exits were all 0. The default project testpaths do not include `tests/inputs`, so the 33 input tests are reported separately. Its fresh evidence root is `private/workflow/checks/active-f438822376be466a9d312afe9c1a39e9`.
- Explicit `git diff --check` exited 0. The log contains the existing line-ending warnings, without whitespace errors.
- Post-test preservation independently reverified all 59 IG-1B artifacts, all 82 IG-1A artifacts, the complete delivery manifest and queue. All match their frozen/baseline hashes. The actual private published snapshots contain no unexpected files or links.

Complete frozen hashes, command exits and UTC/wall records are in `review.json`; raw logs, command JSON, scripts and exact probes remain in this directory. The source audit read only the explicit game/registry file lists and checked the individually named missing paths. KB enumeration was limited to authorized names; no source registry directory contents were recursively loaded.

## Development-history assessment and limits

The preserved `development-check-history.json` and tests-01/02/03/04 evidence distinguish two events. Restricted execution denied native APIs/link creation. The first permitted earlier run then hit false `input changed during copy` errors from comparing Windows pathname and handle ctime semantics. The current implementation preserves the full same-handle ctime signature comparison, separately compares pathname device/inode/size/mtime, and retains independent and global SHA-256 checks. Fresh-created-file tests and the independent ctime/copy-corruption probes confirm the current fix without weakening those protections.

The current frozen tests retain strict expected mutation/pin/alias errors shown in earlier logs and contain no skip/xfail or conditional relaxation of those expectations. Earlier logs retain their failures. A byte-for-byte pre-fix test-source version is not supplied by this delivery, so a complete historical assertion diff is unavailable; no Git history or archives were accessed to fabricate that proof. No current assertion or implementation file was edited by the reviewer.

The byte facility has no global transaction over all origins: finite rechecks cannot certify later source changes. The copied immutable bytes and explicit revision pins are the reviewed evidence; later origin mutations do not grant new identity/meaning. Application validation is not OS-level write protection. Publication of source and input snapshots remains separate as documented. These limits do not explain or waive F1.

Measured review interval starts at the recorded current-session UTC marker `2026-10-12T18:53:33+00:00`; the end and elapsed wall seconds are recorded in `review.json`. This is a checkpoint-to-handoff interval, not a claim about the complete session or active work. Full session start, tokens, operator seconds, cost, peak memory and gameplay performance are unavailable and null. Independent technical defect count is one P2; source-meaning defect counts are null because meaning review was not performed.

The reviewer recommends coordinator disposition `changes_requested` for F1, while leaving queue/status unchanged at `review`. Only the coordinator/operator owns that action and a bounded repair attempt. No other task was started; no additional chats, agents, automations, external services, archive/Git-history reads, neighbouring writes, commits or pushes were used.
