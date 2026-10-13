# Independent IG-1A re-review: repair cycle 1

**Technical result: FAIL — F1 and F3 fixed; F2 partially repaired with one remaining P2 defect.** The original independent 16-case suite passes. Further bounded counterexamples show that an aspect-scoped inventory basis can authorize an exclusion and remain `current` after the inventory's full revision changes. No SPQR semantic acceptance, executable readiness, accepted/done transition, or downstream task start is granted.

Reviewer identity remains `review-independent-20261012T164949Z-163b3167`, distinct from executor `ig-1a-executor-20261012-0540`. This is the same operator-authorized reviewer session and a new append-only review directory. The scope is F1-F3 and their affected invariants. Product, queue/status, old review, baseline, and frozen delivery artifacts were preserved.

## Frozen input and configuration

New delivery SHA-256 `d83e6d04d9b047e03dfdbf3d0849d6d755e16a29f2287cd63495a01cd8bcdf3c` matches the latest IG-1A `in_progress -> review` queue event of `2026-10-12T17:18:02.124788+00:00`. All **76/76** artifact hashes matched before assessment. The complete list is pinned in `hash-verification.json` and `review.json`, and rechecked in `preservation-final.json`.

Repair packet manifest SHA-256 `fc7be33bd8393780043500be3623a947a9a6981030851b60a9e9e69e2c89ad0e`; context SHA-256 `ead069c075669379104ce3bf20918384d0cbf45423a98e7beb6ae4c3f454e00a`. These match checkpoint-frozen.json. The packet's card records changes_requested; the live queue now records review. Only workflow-generated views differ from their packet versions. The four assigned design documents and task criteria remain unchanged from the first review. Read the prepared re-review prompt, local wgc-review skill, WORKFLOW, queue criterion/event context, new packet/card, frozen report, changed code/schema/documentation/test expectations, and preserved baseline comparison.

All 36 preserved baseline copies match the old delivery's original product hashes. All original 50 delivery artifacts are preserved when old product paths are mapped to those copies, and all artifacts pinned by the prior review remain unchanged. The prior review JSON SHA-256 `5dab7b6d6b2851e451ce9124d7a6aa17a44624f7b6c0f6cd5b6739d519e35a39` matches the repair checkpoint. Its honest unknown-configuration record is retained.

**Actual current model/reasoning: `gpt-6.1-sol` / `high`.** Independently extracted from the exact own-session `turn_context` configuration record for turn `01a13122-8cdc-77f3-b992-181624ea3507`, timestamp `2026-10-12T17:21:50.465Z`, session `01a13104-4cba-7610-b690-dc463e8c4e32`, cwd `C:\repo\wargame-compiler`. Raw JSONL line SHA-256 including its newline is `e5035048369ecb361c83f30180f26b27c1e5256d09c4cb73174118e94d94dc04`. The source path and exact extracted fields are in `configuration-final.json`.

The first review turn's own metadata independently confirms the same model/effort; its raw line hash including newline is `73691b65a221a2723c8cb8375749db3517e3d1a8c8d21e8ddd4db7d328da91f6`, matching the supplied supplementary runtime evidence. This new evidence supplements the immutable prior report rather than rewriting its original knowledge state. The runtime field `effort` supplies `high`; the separately absent `reasoning_effort` field remains null. Only session identity/configuration fields were extracted; no message, tool, reasoning content, other sessions, archives or Git history were used as review context. Initial diagnostic records used an overly strict header filter and then a hash omitting newline; `configuration-final.json` resolves both without overwriting them.

## F1 disposition: fixed

The new `content_ref` shape combines the existing typed active/historical reference with the allowed record families node/evidence/relation. Coverage target_refs now uses that shape. It rejects gap-only and mixed gap/content lists in either mode, and it rejects metadata records as content. Actual record-family resolution remains checked by the source validator, so merely declaring a different family does not bypass the restriction.

Independent evidence: original F1 counterexample now rejects; the four new frozen gap cases pass their negative expectations. Eighteen further tests reject mixed node/metadata or node/gap targets across both reference modes (source, region, profile, run, review, registry, origin binding, coverage, gap). Six positive tests validate node/evidence/relation targets in both modes. Two further tests retain valid partial/unprocessed accounting with explicit gap_refs and no represented target. Positive structural coverage still makes no source-meaning claim.

## F2 disposition: partial — remaining P2 F2-R1

The repair correctly rejects the original unrelated approval and requires a current complete accepted human source_composition review, an exact boundary object, a region target and an inventory basis. The frozen other-region/level/inventory, partial, stale, model and missing-basis negatives pass. Additional independent tests reject missing region targets, wrong review kind, unknown basis completeness, rejected decisions, missing authorization and missing decision artifact. Exact full-record boundary metadata remains a valid positive.

**F2-R1: inventory aspect pins bypass the required full-record basis.**

- Exact location: `src/wgc/contracts/source.py:378-383`, particularly membership of `data['inventory_ref']` in the review basis; `review_freshness` at lines 252-263 compares only an aspect when aspect_id is present. Schema locations: `/$defs/coverage_data/properties/inventory_ref` and `/$defs/review_data/properties/coverage_boundary/properties/inventory_ref` both use historical_ref, whose optional aspect_id remains allowed.
- Contract violated: the prepared repair scope and contracts/ig/README.md explicitly require the exact inventory as a **full-record** review basis. This is the outstanding part of F2, not a new gameplay-language requirement.
- Counterexample A: `f2-aspect-inventory-basis.json`. Give `synthetic:inventory` a valid stable aspect, set the coverage inventory_ref to that historical aspect address, and copy that same address into the accepted boundary review's inventory_ref and basis. The exact region remains a full-record target and the decision retains complete human source_composition metadata. All hashes and selected revisions are correct. Validation passes, counts one transcription region as excluded, and reports the boundary review current. It should reject the aspect-scoped inventory basis.
- Counterexample B: `f2-aspect-inventory-stale-boundary.json`. Starting from A, change the inventory's descriptive partition statement, preserve the old revision and select the new revision, while leaving its aspect unchanged. The coverage and decision still pin the older inventory revision via the aspect. Validation again passes and reports the exclusion review current although its pinned inventory revision differs from selection. The independent tests intentionally fail because no ContractError is raised.
- Consequence: approval of one aspect can transfer to a changed whole-inventory boundary. Full-record inventory changes need not invalidate exclusion, allowing false freshness and unjustified scope exclusion. The two reproductions are one defect, severity P2.
- Evidence: `test_rereview.py::test_f2_inventory_basis_must_be_a_full_record`, both parameter values; complete correctly hashed bundles; `f2-actual-reports.json` records current freshness, excluded count 1 and the mismatched selected revision in B; `bounded-suite.log` records both failing tests.
- Smallest repair: require a historical inventory pin without aspect_id for coverage exclusion and its boundary metadata. With that full-record pin, require the exact full-record inventory basis and use whole-revision freshness. A dedicated full-record historical-ref shape or an explicit rejection guard is sufficient; preserve aspect-scoped reviews elsewhere. Do not weaken generic review freshness or remove aspect support from unrelated contracts.
- Required verification: both counterexamples reject; a valid full-record exclusion still passes; changing that inventory's full revision makes the old exclusion stale/rejected; unrelated-aspect reviews unrelated to exclusion retain their original current behavior. Re-run the affected frozen cases, the original independent suite, these new cases and normal project checks under a new frozen delivery.

## F3 disposition: fixed

`require_selected` compares each selected required/conditional relation's resolved endpoint with the exact selected revision. Both from_ref and a resolved target_ref are checked, irrespective of reference mode. Unresolved targets remain null with locator/gap/candidates and do not activate retained history. Unselected old relation revisions retain their prior snapshot semantics.

Independent evidence: the original required historical procedure counterexample now rejects. The frozen required/conditional unselected/superseded/from-endpoint negative cases and exact-selected positives meet their stated expectations. Four additional tests reject superseded endpoint revisions even when the selected newer container has the same aspect hash; both endpoints and requirements are exercised. An unresolved conditional link with a retained historical candidate passes structural validation, appears as an execution blocker and grants no acceptance. Informational historical mention fixtures remain valid.

## Criteria and required validation accounting

| IG-1A criterion | Current assessment |
|---|---|
| 1. Represent all source/region/aspect/group/relation/gap/origin/coverage/profile/run/review/snapshot families | Representation remains present; optional typed coverage boundary extends review metadata. Full-record exclusion enforcement still needs F2-R1. |
| 2. Explicit deterministic identities/revisions, anonymous identities independent of position | Pass within the source contract. Existing hash/canonicalization/identity tests remain enabled; F3 selection defect is fixed. No identity rematcher is claimed. |
| 3. Separate review, coverage and execution; opaque source allowed without execution | **Not fully satisfied**: F1 is fixed, but F2-R1 leaves a false-freshness/exclusion path. Source ready remains disallowed, opacity remains blocking and no semantic acceptance is granted by validation. |
| 4. Required mechanics addressable through source descriptions | Previous source-representation pass retained. Named fields/aspects and their tests are unchanged; repairs add no generic payload mechanism or executable interpretation. |
| 5. No importer/formal interpreter/compiler/game logic; open IG-3A decisions | Pass. Five changed existing files plus 24 synthetic fixtures are bounded structural-contract changes. Formal types/operators, history/transactions, bindings/reactions/termination, tables/geometry/chance/visibility and readiness decisions remain open. |

All original required cases remain reproduced: unknown without gap, changed aspect hash, old aspect acceptance, model approval, dangling active/historical references, duplicate identity, opaque execution blocker. Existing cross-page clause/printed labels, cross-section exception, table note, missing unit, cycle, edition compatibility, scoped/partial review, dependency changes and coverage overlap cases still meet their expectations. The original independent 16-case suite was run by this reviewer, independently of executor results.

The 50-case frozen catalogue is independently replayed in test_rereview.py with its explicit validity, freshness, execution and coverage-count expectations. The 24 added fixtures have architectural/F1-F3 bases, and the small test_source.py change only adds checking the expected excluded count. The test oracle does not assume implementation rejection; the two failing cases demonstrate that disagreement is retained. Structural metadata do not authenticate source meaning or human authority.

## Actual checks and scope preservation

| Check | Actual result | Evidence |
|---|---|---|
| `pwsh -NoProfile -File scripts/check.ps1` | Exit 0; 96 passed in 40.40 s; plan/dry-run/tests/diff 0 | `private/workflow/checks/active-66b816ee50fa4de596a256ba3d34f7f7/` |
| Original reviewer test_review.py with fresh basetemp | Exit 0; 16 passed in 7.08 s | `original-suite.log`, `original-suite-temp/` |
| Further bounded suite including 50 frozen catalogue cases | Exit 1; 85 passed, 2 failed in 16.99 s | `bounded-suite.log`, `bounded-temp/` |
| Added partial/unprocessed positive checks only | Exit 0; 2 passed, 87 deselected in 0.41 s | `partial-suite.log`, `partial-temp/` |
| Inspect actual F2 counterexample reports | Exit 0; both structurally passed/current, one excluded region each | `f2-actual-reports.json` |
| Standalone `git diff --check` | Actual exit in checks.json | `diff-check.log` |
| Final frozen/queue/prior preservation hashes | Actual results in preservation-final.json | Complete lists with actual SHA-256 |

The augmented independent suite covers 89 tests across the bounded and two focused runs: 87 passed, 2 failed. Those failures remain unsilenced. All basetemp locations are fresh and under this new review directory. Standard tests remain fully enabled. Dry-run reports queue_unchanged true, models_launched 0 and product_files_written 0. The earlier operator-authorized synthetic workflow fixture repair and check script are unchanged.

No game evidence, archive, Git history, neighbouring repository, external API, additional agent/session, automation, commit/push or queue transition was used. Tests generated only synthetic review evidence. New diagnostics and file diffs are stored here; old reports and configuration records were preserved. An initial diff read used the host's default text encoding and failed on a UTF-8 fixture test; subsequent explicit UTF-8 comparison succeeded without file changes.

Remaining source-layer limits from the first review are retained: human identity/decision artifacts are not authenticated, complete review basis is declared rather than proven, conflicting reviews lack effective-decision aggregation, coverage-region counts are not complete-rulebook certification, and source descriptions are not executable semantics. These limits do not excuse the explicit full-record inventory invariant.

`review.json` records model/effort metadata source, UTC/wall measurements and null unavailable token/operator/cost data. Queue remains `review`. Next exact action: coordinator scopes the second bounded F2 repair to reject aspect inventory pins for exclusion, obtains a new frozen delivery and asks this independent reviewer to verify its changed hashes and affected cases. F1/F3 need regression protection but no additional repair is requested here.
