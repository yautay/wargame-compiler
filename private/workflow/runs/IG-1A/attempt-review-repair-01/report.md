# IG-1A repair cycle 1: frozen re-review delivery

Three independently reproduced P2 findings F1-F3 have bounded source-contract repairs. All current project tests and the original independent counterexamples pass when run by the executor. The corrected delivery is ready for independent re-review; the executor has not closed the findings, accepted the task, or marked done.

## Findings and repair evidence

| Finding | Repair | Contract-based verification |
|---|---|---|
| F1: gap counted as represented content | coverage target_refs admits only node/evidence/relation; both reference modes obey type constraints | Static gap-only/mixed cases in both modes reject; original node and new evidence/relation positives pass |
| F2: unrelated approval reused for exclusion | Current complete accepted human source_composition review must have exact coverage_boundary inventory/region/level, region full-record target and inventory full-record basis | Exact authorized boundary passes; unrelated/other-region/other-level/other-inventory/partial/stale/model/missing-basis cases reject |
| F3: required historical dependency outside selection | Selected required/conditional relation endpoints must match selected exact revisions; historical pins may not consume omitted/superseded revisions | Both requirements and both endpoints exercised; exact selected pins, informational history and unresolved links remain valid |

The new exclusion boundary targets a region and inventory rather than its own coverage record, avoiding circular hashes. It is typed metadata for human scope decisions, not authenticated human approval or a gameplay interpreter. Unknown and opaque source content still blocks execution; no source record can claim executable ready.

## Criteria met and unmet

- Implemented and covered from the executor perspective: Schema represents sources/regions, clauses with stable aspects and semantic groups, relations, gaps, origin bindings, coverage, profiles, runs, reviews and snapshots.
- Implemented and covered from the executor perspective: ID and revision hash rules are explicit and deterministic; anonymous identities do not depend on array position.
- Implemented and covered from the executor perspective: Source representation distinguishes review, coverage and executable readiness; source-level opaque is accepted without granting execution.
- Implemented and covered from the executor perspective: State, causal history, parameters, persistent choices, reactions, continuations, costs, geometry, tables, chance and visibility have addressable source representations; no generic payload-only claim.
- Implemented and covered from the executor perspective: No importer, formal interpreter, compiler or game logic is implemented; record open formal-language decisions for IG-3A.

The original required cases remain present, with 50 static synthetic fixture oracles total (26 original plus 24 added). All stated expectations are based on the source proposal and independent findings, not the validator output. The five edited existing product files are contracts/ig/README.md, contracts/ig/source.schema.json, src/wgc/contracts/source.py, tests/contracts/fixtures/catalog.json and tests/contracts/test_source.py. Twenty-four new static fixtures are added under tests/contracts/fixtures/. No other pre-existing product file changed in this repair.

Unmet gate: independent re-review of the new hashes. The earlier independent review failed three P2 findings; its report remains immutable. Passing its test suite in the executor session is evidence of repair, not independent approval. Findings remain pending independent disposition. No SPQR human semantic acceptance or executable readiness is granted; that acceptance is not required for the technical IG-1A task.

## Checks

| Command | Exit | Outcome |
|---|---:|---|
| `.venv/Scripts/python.exe -m pytest tests/contracts -q -p no:cacheprovider --tb=short --basetemp private/workflow/runs/IG-1A/attempt-review-repair-01/test-temp-01` | 0 | 70 passed; 13.52 seconds |
| `PYTHONPATH=src .venv/Scripts/python.exe -m pytest private/workflow/runs/IG-1A/review-independent-20261012T164949Z-163b3167/test_review.py -q -p no:cacheprovider --basetemp private/workflow/runs/IG-1A/attempt-review-repair-01/reviewer-oracle-temp-01 --tb=short` | 0 | 16 passed; 2.86 seconds |
| `pwsh -NoProfile -File scripts/check.ps1` | 0 | 96 passed; 49.74 seconds |
| `git diff --check` | 0 | Passed |
| `.venv/Scripts/python.exe scripts/workflow.py validate` | 0 | Passed |
| `Python SHA-256 comparison of every baseline copy and independent review artifact; expected five-file change set` | 0 | Passed |

Project controls: plan=0, dry-run=0, tests=0, diff=0. Ordinary suite: 96 passed (70 source-contract tests and 26 pre-existing controls), 49.74 seconds. The unchanged independent 16-bundle suite: 16 passed, 2.86 seconds. No assertions or tests were weakened, removed or skipped. Reviewer-owned fixtures, reports, checks and hashes were not modified. Only its read-only pytest suite was executed, with a new executor-owned temp directory.

## Configuration and measurements

Executor: `ig-1a-executor-20261012-0540`; confirmed gpt-6.1-sol / high from the existing operator UI confirmation for this unchanged session, preserved in configuration.json. The new repair claim cites that confirmed source rather than treating requested settings as evidence.

The independent review was launched with requested Sol/high. Its original report truthfully recorded runtime unknowns. A later strictly scoped metadata extraction from the exact created session now confirms model gpt-6.1-sol and effort high for turn 01a13104-561d-7581-9b15-2852f085d0f3. reviewer-runtime-metadata.json preserves the source path, timestamp, turn/session ID and exact metadata-record hash. Only session identity and configuration fields were extracted, not message/tool/reasoning content or other sessions. This supplementary evidence does not overwrite the reviewer report or certify the next turn in advance.

Repair start UTC `2026-10-12T17:03:12.024313+00:00`; freeze UTC `2026-10-12T17:17:59.863629+00:00`; elapsed wall seconds `887.839`. Input/output tokens, operator seconds and monetary cost are null because not exposed/reported. Independent review's own measured interval and unavailable counters remain in its review.json. Test runtimes are check measurements, not game performance.

Observed independent defect counts on the prior delivery: P0=0, P1=0, P2=3, P3=0. All three stop reproducing against current code, but independent closure is pending. Source-meaning defect counts remain null. This is the first repair cycle for each finding; no further unchanged retries or silent scope expansion occurred.

## Inputs, snapshots and preservation

Repair packet `private/workflow/packets/IG-1A-06ffa55757af452f8200e1cc6a58856a/manifest.json`, SHA-256 `fc7be33bd8393780043500be3623a947a9a6981030851b60a9e9e69e2c89ad0e`. Context `private/workflow/packets/IG-1A-06ffa55757af452f8200e1cc6a58856a/context.txt`, SHA-256 `ead069c075669379104ce3bf20918384d0cbf45423a98e7beb6ae4c3f454e00a`. All 11 context files, context bundle, initial queue and prior 50 delivery hashes were verified before claim.

Original product bytes were copied and verified under baseline/, with baseline-manifest.json mapping original paths/hashes to preserved copies. Prior delivery and review JSON/reports remain immutable. Current product paths intentionally carry the repaired bytes, so old manifest hashes should be verified against those preserved copies when comparing versions. This is current-task recovery evidence, not an archive/history context expansion.

The only task executed remains IG-1A. Queue changes used workflow transition (review -> changes_requested -> in_progress) and render. No acceptance/done transition is made. Prior operator-approved tests/test_workflow.py sandbox repair remains unchanged. No neighbouring repository, Git history/archive, external API, agent, extra chat, automation, commit or push was used during repairs. The one separate reviewer session was explicitly authorized by the operator.

## Limits and open decisions

The schema remains a pre-acceptance refinement of source version wgc-source-1. The offline evaluator supports its documented bundled keyword subset, not general JSON Schema certification. Coverage target-family and approval-boundary checks do not prove source meaning or authenticate people. Review dependency completeness remains a declared basis claim; actual source/game readiness belongs to later stages. No importer, formal interpreter, game compiler/runtime or AI opponent is implemented.

IG-3A decisions remain open in contracts/ig/README.md: executable value/operator/unit types, ordered causal writes/history/transactions, binding and invocation lifetime, loops/termination, reactions and cancellation survival, calculations/tables/geometry/chance, full visibility-safe responses, formal attachment/dependency closure and acceptance/readiness invalidation. These structural repairs choose none of those game policies.

## Frozen product files and SHA-256

| Path | SHA-256 |
|---|---|
| `contracts/ig/README.md` | `fc4ba2ddf9874b8d4c0d6ea3e6d51d3b5285923f327faf6296a17817de06fc9e` |
| `contracts/ig/source.schema.json` | `0c424d0fb627ddbc11437a24d5d35b15e80ad9448fc162798641f84a38f95cd7` |
| `pyproject.toml` | `e7d4993802db43bca3446ca0c6bc684c04a62ecf53bb7cbb0fa2019709a1571d` |
| `scripts/check.ps1` | `587b06670b7c42c567e95e67afe1d738681f2ad95e9fe1464b4f60cfb6425f73` |
| `src/wgc/contracts/__init__.py` | `e41623d285e0a5c24494cb81a161d63ae1816c1ef9fb3f810a657a6cf5cfdf81` |
| `src/wgc/contracts/source.py` | `14aa5fd5129ed5f6ae65937a3f646407c3f1433483aa2145b53f942ed43509b1` |
| `tests/contracts/fixtures/catalog.json` | `69831e498c859c5113de5dccb53f43d7ccf18f172be4fe49f1e789cea7e7433e` |
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
| `tests/contracts/fixtures/valid-historical-reference.json` | `9f6d03b2372847cb4e678d5537cb51f030e2370a005ba5ffa2eb55876db9d1b2` |
| `tests/contracts/fixtures/valid-overlapping-context.json` | `ee16f98d763e528896d3a4e063e4d1239149aed29c705ee5cba401688a5be77a` |
| `tests/contracts/fixtures/valid-partial-review.json` | `d12c2bf2bb7654217e57c9b77da67d1d74e0b388192dd64fc4b365190eb8939d` |
| `tests/contracts/fixtures/valid-procedure-cycle.json` | `fabc738c5423550d2a061095151a3b8a60d1e168f81a2a85f75258b011517f2b` |
| `tests/contracts/fixtures/valid-required-historical-selected.json` | `56d84227f49740843d9959ed3857e68487de16312da32630f8a555bb9a0e6b3d` |
| `tests/contracts/fixtures/valid-source.json` | `9f6d03b2372847cb4e678d5537cb51f030e2370a005ba5ffa2eb55876db9d1b2` |
| `tests/contracts/fixtures/valid-unresolved-conditional-dependency.json` | `cc8d199b4b3bb97fe4192961e85dad5a1699d206539dfba84bbef05edf5b39c8` |
| `tests/contracts/test_source.py` | `83f980a41bf7f7cf6277ba67a93e1ea9d5ab03733ea078f5f2af4c5072ff0159` |
| `tests/test_workflow.py` | `c29111c6bb8703615199d7d189ae42dc115a33a445a33d4c37fade9be7826eea` |

## Handoff

rereview-prompt.md is a concrete follow-up for the existing reviewer session 01a13104-4cba-7610-b690-dc463e8c4e32. No new session is needed. A pending operator question requested authorization to send metadata confirmation and corrected hashes to that session; none had arrived at freeze, so no follow-up message has been sent. UI configuration confirmation is no longer necessary for the first review turn because its actual metadata have been extracted. The remaining dispatch requirement is explicit permission to message the existing task.

Next action: authorize that follow-up, have the independent reviewer verify the current delivery.json hash and entire artifact list, re-run F1-F3 and affected risks, and report a new independent decision. Leave queue review and do not start a downstream task.
