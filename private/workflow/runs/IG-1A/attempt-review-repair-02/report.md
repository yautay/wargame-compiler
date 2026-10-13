# IG-1A: frozen delivery after final bounded F2 repair

The second F2 repair rejects aspect inventory pins through an explicit whole-record historical-reference shape. Current ordinary controls and independent counterexamples pass when run by the executor. F1/F3 were independently fixed in the previous re-review; independent closure of F2-R1 and overall technical pass are pending. No accepted/done transition or SPQR semantic acceptance is granted.

## Repair scope and independent findings

F2-R1 was reproduced independently in two correctly hashed bundles: an aspect pin can stand for an inventory boundary, and it remains current after the rest of that inventory changes. This is the outstanding part of F2, so repair counts are F1=1, F2=2, F3=1; F2 is not reset as a new finding. No third F2 repair cycle is authorized by workflow.

source.schema.json now defines whole_historical_ref without aspect_id and uses it for coverage.inventory_ref and review.coverage_boundary.inventory_ref. Existing exact full basis membership and whole-revision freshness remain unchanged. Generic historical_ref still supports normal aspect-scoped reviews; source.py and its generic freshness logic are unchanged in this repair.

Only contracts/ig/source.schema.json, contracts/ig/README.md and tests/contracts/fixtures/catalog.json changed among existing product files. Six static synthetic oracles add the two independent reproductions, valid full-record inventory with an aspect, stale full-record boundary after a description change with unchanged aspect, aspect-only review basis rejection and boundary-only aspect rejection. The previous 50 fixtures and all code/integration/test assertions remain byte-identical.

## Criteria met and unmet

- Implemented and covered from the executor perspective: Schema represents sources/regions, clauses with stable aspects and semantic groups, relations, gaps, origin bindings, coverage, profiles, runs, reviews and snapshots.
- Implemented and covered from the executor perspective: ID and revision hash rules are explicit and deterministic; anonymous identities do not depend on array position.
- Implemented and covered from the executor perspective: Source representation distinguishes review, coverage and executable readiness; source-level opaque is accepted without granting execution.
- Implemented and covered from the executor perspective: State, causal history, parameters, persistent choices, reactions, continuations, costs, geometry, tables, chance and visibility have addressable source representations; no generic payload-only claim.
- Implemented and covered from the executor perspective: No importer, formal interpreter, compiler or game logic is implemented; record open formal-language decisions for IG-3A.

All original required cases remain present. There are 56 static fixture oracles and 76 contract tests. Import, coverage, semantic review and executable readiness remain separate; opaque/unknown source content never grants execution. No importer, formal rule interpreter, compiler, game logic or AI opponent was introduced.

Unmet lifecycle gate: independent review of the latest hashes. The prior independent re-review fixed F1/F3 and retained one P2 F2-R1. Its two failing cases now reject, but executor tests do not close the reviewer finding or approve the delivery. Technical task criteria require the reviewer disposition; human SPQR semantic acceptance is not required for IG-1A and is not fabricated.

## Actual checks

| Command | Exit | Result |
|---|---:|---|
| `.venv/Scripts/python.exe -m pytest tests/contracts -q -p no:cacheprovider --tb=short --basetemp private/workflow/runs/IG-1A/attempt-review-repair-02/test-temp-01` | 0 | 76 passed in 10.2 s |
| `PYTHONPATH=src .venv/Scripts/python.exe -m pytest private/workflow/runs/IG-1A/review-repair01-20261012T172231Z-9f8db531/test_rereview.py -q -p no:cacheprovider --basetemp private/workflow/runs/IG-1A/attempt-review-repair-02/independent-temp-01 --tb=short` | 0 | 95 passed in 14.84 s |
| `PYTHONPATH=src .venv/Scripts/python.exe -m pytest private/workflow/runs/IG-1A/review-independent-20261012T164949Z-163b3167/test_review.py -q -p no:cacheprovider --basetemp private/workflow/runs/IG-1A/attempt-review-repair-02/original-independent-temp-01 --tb=short` | 0 | 16 passed in 3.07 s |
| `pwsh -NoProfile -File scripts/check.ps1` | 0 | 102 passed in 33.02 s |
| `git diff --check` | 0 | Passed |
| `.venv/Scripts/python.exe scripts/workflow.py validate` | 0 | Passed |
| `Python SHA-256 comparison: all 60 preserved product copies and prior independent review artifacts match; only three expected existing product files changed` | 0 | Passed |

Full project controls report plan=0, dry-run=0, tests=0, diff=0, with 102 passed (76 contract plus 26 existing controls), 33.02 seconds. The unchanged independent augmented suite passed 95 tests in 14.84 seconds; its catalogue expands to the current 56 cases. The original independent suite passed 16 in 3.07 seconds. These suites overlap and are reported separately, not summed into a fabricated unique-test count. Reviewer evidence files were not rewritten; tests used new executor-owned temp paths.

## Configuration and measurements

Executor identity `ig-1a-executor-20261012-0540`; confirmed gpt-6.1-sol/high from the existing operator UI statement for this unchanged ongoing session, copied without alteration in configuration.json. The independent repair-01 reviewer confirmed its actual turn_context model gpt-6.1-sol and effort high; its configuration-final.json and review.json retain timestamp, thread/turn ID, exact own-session source and line hash. First-review unknowns and later metadata confirmations remain append-only; a future review turn must check its own actual values.

Second F2 repair start UTC `2026-10-12T17:32:39.925511+00:00`; freeze UTC `2026-10-12T17:40:49.928825+00:00`; elapsed wall seconds `490.003`. Tokens, operator seconds and monetary cost are null because not exposed/reported. Test seconds are check measurements, not gameplay latency or performance. Prior reviewer measured interval remains in its immutable evidence.

Independent outstanding defect counts before this repair: P0=0, P1=0, P2=1, P3=0; source-meaning counts null. The remaining P2 stops reproducing in executor checks. Independent closure remains pending. No assertions were weakened, no failing case was skipped, and no unchanged failure was repeatedly retried.

## Inputs, byte preservation and authority

Packet `private/workflow/packets/IG-1A-620a0f57cd0840fcbc89118959a75f6b/manifest.json`, SHA-256 `1a4d30de911324fe561e23a20da2d5640d297ac4f865b5122542b48aad33692b`; context `private/workflow/packets/IG-1A-620a0f57cd0840fcbc89118959a75f6b/context.txt`, SHA-256 `ead069c075669379104ce3bf20918384d0cbf45423a98e7beb6ae4c3f454e00a`. All 11 context hashes, context/queue hashes and 76 prior delivery hashes matched before claim.

All 60 prior product files are preserved under baseline/ with exact original hashes in baseline-manifest.json. The previous first-delivery baseline is likewise retained in attempt-review-repair-01. Old delivery/review JSON, reports, all independent counterexamples and their logs are unchanged. New working product hashes intentionally differ from those old snapshots, so compare preserved bytes rather than demanding old hashes at updated paths.

This is still only IG-1A. Queue/status updates use workflow transition/render. The operator explicitly authorized the independent reviewer session and follow-up messages carrying corrected IG-1A deliveries to that same session; no additional permission is inferred from the reviewer itself. No new session/agent is needed for this re-review. No archives/Git history, neighbouring repositories, external APIs, automation, global configuration, commits or pushes were used during the repair.

## Limits and open decisions

The source contract remains a pre-acceptance refinement of wgc-source-1. Metadata checks do not authenticate human authority/artifacts or prove source meaning, full corpus coverage, or complete semantic dependency bases. The offline evaluator is limited to the bundled schema keyword subset. Whole inventory pins prevent the structural freshness bypass without changing valid aspect reviews elsewhere. Inventory partition justification across coordinate conventions remains an author obligation.

IG-3A decisions remain open in contracts/ig/README.md: executable types/operators/units, causal writes and transactions/history, invocation bindings, loops/termination/reactions/cancellation survival, tables/calculations/geometry/chance, visibility-safe complete responses, formal attachments and dependency/acceptance/readiness invalidation. This repair implements none of those game policies.

## Frozen product paths and SHA-256

| Path | SHA-256 |
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

## Independent handoff

rereview-prompt.md is ready for the existing reviewer session 01a13104-4cba-7610-b690-dc463e8c4e32. Verify the entire delivery.json list and original preserved snapshots. Re-run both F2-R1 reproductions, full inventory/aspect freshness controls, affected F1/F3 controls and all project checks. Leave queue review and report a new independent result. If F2 still fails, record blocked/escalation with the smallest operator/coordinator action; no third silent repair. The executor does not accept/done or start downstream tasks.
