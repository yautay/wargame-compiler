# IG-1A final handoff verification

**Technical result: PASS. Recommend technical acceptance of the exact frozen delivery.**

All five queue criteria are satisfied within the source-contract scope. No actionable technical finding remains. This is a recommendation only: queue stays `review`, with no accepted/done transition. No SPQR semantic acceptance or executable readiness is granted.

Reviewer identity: `review-handoff-20261012T180728Z`, distinct from executor `ig-1a-executor-20261012-0540` and the earlier independent reviewer. Only IG-1A final handoff verification was performed. The local `docs/skills/wgc-review/SKILL.md` was explicitly read and applied.

## Configuration and measurements

Current session: **GPT-6.1 Sol / reasoning high**. Exact runtime metadata were unavailable; before substantive verification, the operator answered “potwierdzam” to the explicit question confirming both settings from this current chat UI. `configuration.json` preserves that evidence. No earlier-session confirmation was used to confirm this session.

Measured UTC interval: `2026-10-12T18:07:28+00:00` to `2026-10-12T18:16:31.161148+00:00`; elapsed `543.161148` seconds. The interval begins with the first explicit UTC clock read after confirmation; prior reads, initial commands and the operator wait have no invented duration. Tokens, operator seconds, cost, peak memory and gameplay latency are `null`. Check runtimes are not game performance measurements.

## Integrity, queue and provenance

| Pinned evidence | Actual SHA-256 |
|---|---|
| `private/workflow/runs/IG-1A/attempt-review-repair-02/delivery.json` | `e60f74eca3b94771539eb438c4d239a4deeec3ae20cc5950a4f415ae5d863958` |
| `private/workflow/runs/IG-1A/review-repair02-20261012T174537Z-6b6e02fa/review.json` | `e7a6c12237c642c021595416d49ffc030690388ef1d9f8184da8b73cd89dffdb` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/final-handoff.md` | `b04e30b9e32305eda10e0ca2ad8526a1af0ba5f8337afd07f757b1d480ff7fe6` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/final-handoff.json` | `c5123248d5926e5716a215c63b222563187b46fd2e1b3e8ce62035d0a6b666c8` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/report.md` | `669cd6c90666c719a453315de363fdae4ebf8dda34e1e8efe30b86a397b46fba` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/checkpoint-frozen.json` | `876958f3ce7139308319e6a7c2f40d027cbb3af98adc3bf6f031fe745582f897` |
| `private/workflow/runs/IG-1A/review-repair02-20261012T174537Z-6b6e02fa/report.md` | `d88016b8f6ffd7fa123d06332849008e7d36d4e11a5754cded7b60ce6fa39d3a` |
| `private/workflow/packets/IG-1A-d3fb657a205e4e368f212a9f2bea81b5/manifest.json` | `a4d12f4f16cba54854b079a411fa478c3bf7b9a30d7130bf48088fbe905e659b` |
| `private/workflow/packets/IG-1A-d3fb657a205e4e368f212a9f2bea81b5/context.txt` | `bd3ea219e8bccf4c1a2b5b06cc94b7a0cb5139cc11487e93c82869ea8f3bc66d` |
| `docs/skills/wgc-review/SKILL.md` | `03b6c9adc814037c85bb3111692f231c4140ed55d4c3c94e1518b0a77b9d773e` |
| `docs/work/queue.json` | `85b06d2fdc49c4e83e928ffb1642c6b14b36146d75c80ec15e5982155c0b1821` |

Both operator-specified main hashes match exactly. All **82/82 delivery artifacts** match; all paths are unique and the complete reviewer-frozen list matches the delivery list exactly, including order and hashes. All **60/60 final-review artifacts**, **56/56 prior-review artifacts** and **35/35 original-review artifacts** match. All 60 preserved baseline copies, 76 prior-delivery artifacts via explicit baseline mapping, 66 checkpoint changed files and current packet pins also match.

All 12 IG-1A queue-event JSON hashes match. Event states form a contiguous chain with ordered timestamps ending in `review`; the latest event pins the current delivery hash. The independent final PASS is retained in its pinned review artifact, and has not been converted into acceptance. `validate` confirms all 39 tasks and generated views; `next` reports no ready task. The newly generated packet was read with its card and four named design documents. No new claim was made.

One expected input projection difference exists: the old frozen input packet pins `docs/work/tasks/IG-1A.md` at `788df9bd2d5ee6650975b2d8c5ada45391835b23bfb6155aad05c165362bed34`; current bytes hash to `c3f7ef9dc8a9c8251e6ffcae3f2ce19962a28e61b5361daa23ade8205bf5d7c6`. Comparison against the embedded original card proves the only content change is `changes_requested` → `review`. Criteria and all design input hashes are unchanged. This expected workflow projection update does not alter the frozen delivery or PASS. Unexpected hash discrepancies: **none**.

The executor frozen report correctly says independent closure was pending at its earlier freeze. The later independently pinned report/review and final handoff record that closure. Their chronology is consistent; earlier reports were preserved rather than rewritten.

## Criteria and required cases

| Criterion | Assessment and evidence |
|---|---|
| 1. Schema represents sources/regions, clauses with stable aspects and semantic groups, relations, gaps, origin bindings, coverage, profiles, runs, reviews and snapshots. | **PASS.** All required record families have explicit shapes and source-layer examples. Origins, coverage, reviews and snapshot assessments are distinct. |
| 2. ID and revision hash rules are explicit and deterministic; anonymous identities do not depend on array position. | **PASS.** Integer/scalar canonicalization is explicit and deterministic; fixed independent byte/hash expectations and duplicate/reorder controls pass. F3 exact selected endpoints pass. |
| 3. Source representation distinguishes review, coverage and executable readiness; source-level opaque is accepted without granting execution. | **PASS.** Source-level opacity can be structurally valid while execution is blocked. Review/coverage/import do not grant semantic acceptance. F1 and F2/F2-R1 are closed within structural scope. |
| 4. State, causal history, parameters, persistent choices, reactions, continuations, costs, geometry, tables, chance and visibility have addressable source representations; no generic payload-only claim. | **PASS.** Dedicated named source fields cover all requested mechanisms. They are addressable descriptions and uncertainty records; no executable SPQR interpretation is inferred. |
| 5. No importer, formal interpreter, compiler or game logic is implemented; record open formal-language decisions for IG-3A. | **PASS.** Delivered code parses, hashes and validates source structures locally. It does not evaluate game rules. Future formal operators, execution algorithms and readiness decisions remain explicitly open. |

Unmet task criteria: **none**. Pending lifecycle decision: operator/coordinator disposition. Exact evidence locations and the required-case mapping are recorded in `review.json`.

Required cases were checked against their contract-derived expectations: unknown values without gaps reject; stale aspect hashes reject; changed target/dependency revisions make old reviews stale; model approval rejects; active resolution cannot borrow retained history; missing exact historical pins and duplicate identities reject; opaque source content remains valid only with execution blocked. The independent suite and the 56-case frozen catalogue cover positive and negative cases. Expectations come from the task card and the architecture/data/mechanics/legal-action contracts, plus the independently documented findings; validator agreement is not treated as source truth.

## Finding closure

- **F1: fixed, one repair cycle.** Gap/metadata targets cannot represent source content, including active/historical and mixed target lists. Node/evidence/relation positives and partial/unprocessed gap accounting pass.
- **F2/F2-R1: fixed, two repair cycles.** Coverage exclusions require the exact inventory/region/level boundary, full-record region target and full-record inventory basis. `whole_historical_ref` forbids `aspect_id` on both inventory pin locations, including retained records. Both unchanged original F2-R1 counterexamples reject at schema validation. Full inventory-with-aspects positives pass; a whole inventory change invalidates the prior exclusion even with unchanged aspect hash; ordinary aspect-scoped freshness retains its valid behavior. No third repair was initiated.
- **F3: fixed, one repair cycle.** Required/conditional endpoints must resolve to the exact selected revision in both directions. Unselected/superseded same-aspect revisions reject; informational historical mentions and unresolved candidates remain preserved.

Current technical defects in this bounded verification: P0=0, P1=0, P2=0, P3=0. Source-meaning defect counts: `null`, outside this assignment.

## Actual controls

| Control | Exit | Measured result |
|---|---:|---|
| workflow.py validate | 0 | 39 tasks, DAG, scope, context and generated views valid |
| workflow.py next | 0 | No ready task |
| workflow.py packet --task IG-1A | 0 | Fresh read-only context packet generated |
| `pwsh -NoProfile -File scripts/check.ps1 -Task IG-1A` | 0 | 102 passed in 42.48 s; wall 52.826728 s |
| `Existing independent suites (95 augmented + 16 original + 9 final boundaries)` | 0 | 120 passed in 23.99 s; wall 24.843230 s |
| `git diff --check` | 0 | PASS; wall 2.662993 s |
| `C:\repo\wargame-compiler\.venv\Scripts\python.exe C:\repo\wargame-compiler\private\workflow\runs\IG-1A\review-handoff-20261012T180728Z\verify_handoff.py` | 0 | PASS; wall 2.746508 s |

Project plan/dry-run/tests/diff exits are all zero. The 102 project tests include 76 contract controls; the 120 independent tests include catalogue replay and overlap with product checks, so they are not summed into a unique total. Frozen reviewer test files were copied byte-for-byte into this new review directory because their helpers emit evidence beside themselves. Original assertions were not changed. The original 16-case suite was executed read-only with fresh temporary paths. Copy provenance, exact argv, exits, durations and logs are in `suite-copy-provenance.json` and `checks.json`.

Standalone `git diff --check` passes. Its 43 existing line-ending warning lines do not report whitespace errors; no normalization or configuration change was made. The project dry-run reports unchanged queue, zero models launched and zero product files written.

## Preservation and open decisions

Post-check integrity passes for the complete frozen lists, reports, named evidence and queue. Queue SHA-256 remains `85b06d2fdc49c4e83e928ffb1642c6b14b36146d75c80ec15e5982155c0b1821`. The observed handoff/report/input bytes and porcelain Git status remain unchanged; new review evidence is under the already untracked run directory. All writes in this session are fresh review evidence, the required generated packet, or fresh check outputs. No implementation/product test was edited, and no frozen report was overwritten.

The only three changed existing product files relative to the prior repair baseline are the already-delivered schema, README and catalogue; the six added fixtures are already part of the frozen delivery. These changes predate this verification.

- Operator/coordinator technical acceptance and any later accepted/done transition remain a separate explicitly authorized action. This session records only a recommendation.
- No third F2 repair is authorized. Any recurrence requires an operator decision and new documented hypothesis/scope before repair.
- The formal-language choices recorded for IG-3A remain future work; this session starts no downstream task.
- Real source coverage, authorized human source-meaning decisions, compilation and gameplay readiness remain separate future gates. IG-1A itself requires no SPQR semantic acceptance.

Known source-layer limits remain explicit: human authority/artifacts are not authenticated by structural metadata; basis completeness is declared; contradictory review decisions need explicit handling; synthetic counts do not certify full source coverage; mixed coordinate partitions need author justification. These do not create an unmet IG-1A source-contract criterion. Technical PASS does not certify actual SPQR meaning, legality, full-profile readiness or all possible defects.

No archives or Git history were read; no neighbouring repository was modified; no agent, new chat, automation, external API, commit or push was used. No importer, interpreter, compiler or game mechanism was created. Next task was not started.

## Verified delivery files

All 82 rows below are independently hashed from current disk bytes and match both frozen lists. `hash-verification.json` additionally records every verified review artifact, baseline copy, prior-delivery mapping, event and input with its expected and actual SHA-256.

| File | Verified SHA-256 |
|---|---|
| `contracts/ig/README.md` | `c2d05b9cb20da646de21dc8b3f715799fae2006f06f322c7be800f0cb7e8db57` |
| `contracts/ig/source.schema.json` | `8593fb5f3929f72a97657593272c9089a34faeac74ce10a2f7a925a00fddab13` |
| `pyproject.toml` | `e7d4993802db43bca3446ca0c6bc684c04a62ecf53bb7cbb0fa2019709a1571d` |
| `scripts/check.ps1` | `587b06670b7c42c567e95e67afe1d738681f2ad95e9fe1464b4f60cfb6425f73` |
| `src/wgc/contracts/__init__.py` | `e41623d285e0a5c24494cb81a161d63ae1816c1ef9fb3f810a657a6cf5cfdf81` |
| `src/wgc/contracts/source.py` | `14aa5fd5129ed5f6ae65937a3f646407c3f1433483aa2145b53f942ed43509b1` |
| `tests/contracts/fixtures/catalog.json` | `bdb3bdc0b03eff47570085f07712596548660a45f948ce5bc0873f7396909312` |
| `tests/contracts/fixtures/invalid-anonymous-identity-conflict.json` | `656c89379b355fc478d5a9faf217116f8ff994eb2e523e2bea3704f6f5061060` |
| `tests/contracts/fixtures/invalid-changed-aspect-hash.json` | `2c04c31919aeb450cc48ae80e1c2f82b3713dd14c0ecfa3ff6c07e43b594c2be` |
| `tests/contracts/fixtures/invalid-conditional-historical-superseded.json` | `cbee7ea45acdde7cb26132e4fb610c29431038681aa4c8468d76a818eb06727f` |
| `tests/contracts/fixtures/invalid-conditional-historical-unselected-source.json` | `b6f4d90d007d6080de98bd117581fce656b752f64daed44794d133a2a9b99e0a` |
| `tests/contracts/fixtures/invalid-conditional-historical-unselected.json` | `d266e21e556b79a5675eca4c677b32c88042520a8bb9492bea825f58a9b05a68` |
| `tests/contracts/fixtures/invalid-coverage-exclusion-missing-inventory-basis.json` | `d103636e387e277699c13e592399421e2386c1deab8f1ad0b56456acd15da79d` |
| `tests/contracts/fixtures/invalid-coverage-exclusion-model.json` | `2f16616fb1bdc3d46e9f4de53224c6b7b81915921d6a7f2c85332ec0c6de6c7d` |
| `tests/contracts/fixtures/invalid-coverage-exclusion-other-inventory.json` | `948141960d8aec907c31f8b9d2be0c264d66b4ac29b6613cd8a10d77daf53baa` |
| `tests/contracts/fixtures/invalid-coverage-exclusion-other-level.json` | `9ed60dd9f2ed3f0aa7a4f331aad3405f0f76c32c29899adaf5ebf149da33fbf1` |
| `tests/contracts/fixtures/invalid-coverage-exclusion-other-region.json` | `8a32ea5c9930c1e8b060c04fa809d51cdc4e9a93755a0c34e305399ad15edab8` |
| `tests/contracts/fixtures/invalid-coverage-exclusion-partial.json` | `61a72de214b3bdf33a5d2288e46e789f8d63989dedd5bc0e7e53c3e60dc16c65` |
| `tests/contracts/fixtures/invalid-coverage-exclusion-stale.json` | `19ea8d14a87cddbd059b2660aaa2c2fd0c39e328ef7c041039556d1442f8f9a5` |
| `tests/contracts/fixtures/invalid-coverage-exclusion-unrelated.json` | `6e2605d8482881447d5945afe81e88d67e5d085817c40be3f9950e98ce43a0e2` |
| `tests/contracts/fixtures/invalid-coverage-gap-target-active-mixed.json` | `5a63927ae5fedce48a271407eddf75b8c075fb6f10863e37026b536f8ab0a494` |
| `tests/contracts/fixtures/invalid-coverage-gap-target-active.json` | `0a9f71499d7fb9098c76b9302ad37d46406353cdcde915c86002a20ac4c83f89` |
| `tests/contracts/fixtures/invalid-coverage-gap-target-historical-mixed.json` | `6f6c1499914d1d2a81d2f3f538b344ff2c1dea522cd141334fe2b52254483414` |
| `tests/contracts/fixtures/invalid-coverage-gap-target-historical.json` | `a2906a1a32b34382bb5e161048a177dc0043b6bd0d5d551f0ae04811bbbe6024` |
| `tests/contracts/fixtures/invalid-dangling-active.json` | `e23234a19764662c6bd28a6570ad4c3856955a8c7f56c31199f86497a5edd90e` |
| `tests/contracts/fixtures/invalid-dangling-historical.json` | `1875fb915556e8ef2ffbdc9bb054ee3924ca0f5a33fae8b1579d4220db0a8ef5` |
| `tests/contracts/fixtures/invalid-duplicate-selection.json` | `fcefa6d2aa1af2e6e4d5c49f6cd33a3188ba46c50ebc4057b9c19d233ca418f2` |
| `tests/contracts/fixtures/invalid-duplicate-store.json` | `932c39e4e7c47f97a64c4a9cb34e67193f6291700d385037e7bc1b3d7f0708eb` |
| `tests/contracts/fixtures/invalid-exclusion-aspect-only-boundary-pin.json` | `2ffa0ba34d920e31e32caa467da2e2e94aea582a144398128165653484441811` |
| `tests/contracts/fixtures/invalid-exclusion-aspect-only-review-basis.json` | `c6e3aeadc6053985b3975982c7fc050ba73b701e86b3d38e9cd17a08437d7627` |
| `tests/contracts/fixtures/invalid-exclusion-full-inventory-changed.json` | `d86e8ca5752bc879bfc91c30e2449fe1abc71676660b18e128e4b6b37600170b` |
| `tests/contracts/fixtures/invalid-exclusion-inventory-aspect-stale.json` | `f320b1f2b7b7b7542f72dcb8b43f66c37930a66c3175e77083234a9ec00e20fb` |
| `tests/contracts/fixtures/invalid-exclusion-inventory-aspect.json` | `c4f9e95146ccaa161700cc75ce294925786159dbaaabc01e821e4760cebbf12c` |
| `tests/contracts/fixtures/invalid-gap-counted-as-coverage.json` | `c105f5a777639036b3e3f0e2eeeabb5699c5d6827a10265140bde5013ca856ad` |
| `tests/contracts/fixtures/invalid-group-binding.json` | `af5aa206a2a31926d11d31503c15aa7012d102dce2aa2627f82896689a63619a` |
| `tests/contracts/fixtures/invalid-known-without-evidence.json` | `bc1f5773b30fd956388dda57fa2984e5c3118a478d5faefec11be81b7f54c19f` |
| `tests/contracts/fixtures/invalid-model-approval.json` | `c12bbe40d372dd408456f88846be7c7617ac187824b5972f5078e98e4110a05f` |
| `tests/contracts/fixtures/invalid-opaque-formal.json` | `81588bb151374ff44141cb85964b2d4bfd9c0d3002c71dc6b043ec0f5badcda7` |
| `tests/contracts/fixtures/invalid-opaque-ready.json` | `eaadb38dea99363e629505e4a8cc5041a031be75ad43b70794cf6a76443ec419` |
| `tests/contracts/fixtures/invalid-origin-path.json` | `e27165a475ca06951f3c7720e08424cd143013fcc3061916777f1e009eeefd82` |
| `tests/contracts/fixtures/invalid-overlapping-coverage.json` | `69b12e8c3ed06cf80f46f7fa18125dad1761bdace54cbeef72b6b144a9456b7e` |
| `tests/contracts/fixtures/invalid-reference-type.json` | `ce20da383d4f7b1074103300b5a2a3940de06b020ee6eba4a408383fb4d1b543` |
| `tests/contracts/fixtures/invalid-required-historical-superseded.json` | `5e293974a670b6c9950eb013565840e065a5f1a002ed66b40c7aafbf63df7121` |
| `tests/contracts/fixtures/invalid-required-historical-unselected-source.json` | `f76fb1e5e95485d5dd22f397cd520247814fdaa0791c72ca5c017166e9a82225` |
| `tests/contracts/fixtures/invalid-required-historical-unselected.json` | `cc1845c0b13f9bcd6d2d9c7c5c0ef45f55173ed5af37626d4eee8048037b8f44` |
| `tests/contracts/fixtures/invalid-table-note.json` | `3e59a7c9cc3d6ba213c5adaeaaa8869eee84b97f3c73c6b7e503fc5b30ed80a9` |
| `tests/contracts/fixtures/invalid-unknown-without-gap.json` | `ee5e80d4b000bd48a518c81136bc254349e19561112987aca112db520517975b` |
| `tests/contracts/fixtures/README.md` | `82a5f403d0ce3df1fdb75d955173a09a9cb79c84680dce77663c16f914e0ad2b` |
| `tests/contracts/fixtures/valid-changed-aspect.json` | `92ee3df90d0501e2af40528f4505d43d6ab3c88af00d4d23e3a0f176faa2a723` |
| `tests/contracts/fixtures/valid-changed-dependency.json` | `9fa45d5b015851ad321a936c578c5e09122fd716b86af96ef9c12db67d3c46a7` |
| `tests/contracts/fixtures/valid-conditional-historical-selected.json` | `7dec696c435998a36b63da2b0b6dec9ffec0bf723d7b68c67d133b1a0d376f9e` |
| `tests/contracts/fixtures/valid-coverage-content-evidence.json` | `7e495eb2e8accc703d533a71730a107f817ad378815288ac040d5bf3f232d705` |
| `tests/contracts/fixtures/valid-coverage-content-history-link.json` | `06163cb572d7a953f98f7ed4dc47c274bc9b7a368a65684e75e02aecdbc0926d` |
| `tests/contracts/fixtures/valid-cross-section-exception.json` | `6dc73a731e0e36f5dd1b8629e712cee81e2f7e9b5508d27735997a419caf19f7` |
| `tests/contracts/fixtures/valid-edition-conflict.json` | `044556aac43817f78d6356e6974412c06c9b12834282353108a3833734f658a0` |
| `tests/contracts/fixtures/valid-exact-coverage-exclusion.json` | `d49ba267de3f78122fc4a50ae02d17ed8daf12bdb03062c9a6579d5e4018dc0e` |
| `tests/contracts/fixtures/valid-exclusion-full-inventory-with-aspect.json` | `bb105e0695600f8d814e97d394f73b8912cb27ecd57bf0652362e3d37752ee9e` |
| `tests/contracts/fixtures/valid-historical-reference.json` | `9f6d03b2372847cb4e678d5537cb51f030e2370a005ba5ffa2eb55876db9d1b2` |
| `tests/contracts/fixtures/valid-overlapping-context.json` | `ee16f98d763e528896d3a4e063e4d1239149aed29c705ee5cba401688a5be77a` |
| `tests/contracts/fixtures/valid-partial-review.json` | `d12c2bf2bb7654217e57c9b77da67d1d74e0b388192dd64fc4b365190eb8939d` |
| `tests/contracts/fixtures/valid-procedure-cycle.json` | `fabc738c5423550d2a061095151a3b8a60d1e168f81a2a85f75258b011517f2b` |
| `tests/contracts/fixtures/valid-required-historical-selected.json` | `56d84227f49740843d9959ed3857e68487de16312da32630f8a555bb9a0e6b3d` |
| `tests/contracts/fixtures/valid-source.json` | `9f6d03b2372847cb4e678d5537cb51f030e2370a005ba5ffa2eb55876db9d1b2` |
| `tests/contracts/fixtures/valid-unresolved-conditional-dependency.json` | `cc8d199b4b3bb97fe4192961e85dad5a1699d206539dfba84bbef05edf5b39c8` |
| `tests/contracts/test_source.py` | `83f980a41bf7f7cf6277ba67a93e1ea9d5ab03733ea078f5f2af4c5072ff0159` |
| `tests/test_workflow.py` | `c29111c6bb8703615199d7d189ae42dc115a33a445a33d4c37fade9be7826eea` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/report.md` | `669cd6c90666c719a453315de363fdae4ebf8dda34e1e8efe30b86a397b46fba` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/checks.json` | `6f9c727374e455bb3decb46e14848ac1131dc40c8df363934c43529c33807629` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/configuration.json` | `20810ac1d01121a37cbadded861f81ad6c814b721cc6572245c72b320cae33b2` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/checkpoint-frozen.json` | `876958f3ce7139308319e6a7c2f40d027cbb3af98adc3bf6f031fe745582f897` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/rereview-prompt.md` | `2b49f5abd395e32806c4a7065528699f0639e6ac2687e1afb00f49f1500fbca5` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/baseline-manifest.json` | `0e2a54a9f94be6f499300d5d8893574c114daa1b743972d61efe29bdb0c7d996` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/build_schema.py` | `b277a8bd86dbddcd8b37b1bcc0207328afa6e9a22275a77e985700cfd4861a33` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/build_fixtures.py` | `44b94ea3f8b0589ece92b04fc1963e6013043e583bfed5a7a35020f6b098dd0a` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/build_regressions.py` | `dd3dcc8a989e26436692d66909d1ab2b36e6f33100d61c220d89ddb7b9ea7ac1` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/build_inventory_regressions.py` | `2ee0d13c3c8260d0051e7635708715fedee871d0bda3a4db939aa5b02872caa9` |
| `private/workflow/runs/IG-1A/attempt-review-repair-02/diff-check-final.log` | `755591b02c7df0a0d4ae2653c9205a8bb5edd308b6934d230b7f9dbf08efe97c` |
| `private/workflow/checks/active-83d5c8323e4847cbb847e31843154a05/result.json` | `8e565bc646988e08970b8e8600aea663412687a56ed6f8b339f39ff98b6c00e2` |
| `private/workflow/checks/active-83d5c8323e4847cbb847e31843154a05/pytest.log` | `79cb578224d9afeb0f884f0105fcc80bde221a15f066c276f3b098f6575b9c1c` |
| `private/workflow/checks/active-83d5c8323e4847cbb847e31843154a05/plan.log` | `19ea16b93167c3e5a49bd4ff78879840839ad84d1b20ae7914cbd570f9505d41` |
| `private/workflow/checks/active-83d5c8323e4847cbb847e31843154a05/dry-run.log` | `260c7da81a969341c9b3eb71cdcaae0026ff79325c256a7e0b2ca9be6078ec00` |
| `private/workflow/checks/active-83d5c8323e4847cbb847e31843154a05/diff-check.log` | `755591b02c7df0a0d4ae2653c9205a8bb5edd308b6934d230b7f9dbf08efe97c` |

## Evidence index

- `review.json`: structured result, criterion/case mapping, checks, measurements, current configuration and artifact hashes.
- `hash-verification.json`: complete byte-integrity and workflow-event verification, including the expected generated-card delta.
- `preservation.json`: post-test queue, report and Git-status preservation.
- `checks.json`, `preflight.json` and logs: current-session actual commands/results.
- `configuration.json`: current operator UI confirmation, explicitly distinguished from unavailable runtime metadata.
