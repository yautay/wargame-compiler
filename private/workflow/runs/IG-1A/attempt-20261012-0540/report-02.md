# IG-1A frozen candidate report

The source-contract product increment is implemented, but delivery is blocked before independent review because the required full project check is not green. No acceptance or done transition has been made. No other task was started.

## Criteria

- Implemented and covered by the focused contract suite: Schema represents sources/regions, clauses with stable aspects and semantic groups, relations, gaps, origin bindings, coverage, profiles, runs, reviews and snapshots.
- Implemented and covered by the focused contract suite: ID and revision hash rules are explicit and deterministic; anonymous identities do not depend on array position.
- Implemented and covered by the focused contract suite: Source representation distinguishes review, coverage and executable readiness; source-level opaque is accepted without granting execution.
- Implemented and covered by the focused contract suite: State, causal history, parameters, persistent choices, reactions, continuations, costs, geometry, tables, chance and visibility have addressable source representations; no generic payload-only claim.
- Implemented and covered by the focused contract suite: No importer, formal interpreter, compiler or game logic is implemented; record open formal-language decisions for IG-3A.

Required contract validation cases pass: unknown without gap, changed aspect hash/freshness, model approval, active versus historical references, duplicate identity and opaque execution blocker. Additional cases cover page-spanning evidence, cross-section exceptions, table notes, missing units, cycles, edition conflict, partial review, dependency regression and coverage overlap.

Unmet gates: `scripts/check.ps1` still has seven failing pre-existing workflow tests; independent technical review has not occurred. This task does not require human SPQR semantic acceptance, and none was granted. Import/source coverage/gameplay readiness of actual SPQR are not claimed.

## Configuration and measurements

Observed model/reasoning: `gpt-6.1-sol` / `high`. Source: operator observation of the current session UI, recorded verbatim as `GPT-6.1 Sol / reasoning high - TAK` in configuration.json. Exact runtime model/reasoning metadata were not exposed; the original request was not treated as evidence.

Executor: `ig-1a-executor-20261012-0540`. Start UTC: `2026-10-12T14:51:29.775886+00:00`; candidate freeze UTC: `2026-10-12T15:20:21.934166+00:00`; elapsed wall seconds: `1732.158`. The elapsed interval includes waiting for the scope decision. Session input/output tokens, operator seconds and monetary cost: null (not exposed/reported).

Latest focused suite: 46 passed in 5.36 seconds. Full suite before the requested fixture repair: 65 passed, 7 failed in 50.90 seconds. These are check runtimes, not gameplay performance measurements.

Executor-observed issues: one minor test-vector defect corrected; one environment temp-path issue resolved; one major check-script ready-task assumption corrected; one major workflow sandbox defect remains outside authorized write scope. A checkpoint was briefly updated in place, then its original exact claimed bytes were reconstructed and SHA-256 verified; the implementation increment was preserved in checkpoint-implementation-01.json. Independent reviewer defect counts are null because review has not occurred.

## Checks

| Command | Exit | Result |
|---|---:|---|
| `.\.venv\Scripts\python.exe -m pytest tests/contracts -q -p no:cacheprovider --tb=short --basetemp private/workflow/runs/IG-1A/attempt-20261012-0540/test-temp-04` | 0 | 46 |
| `.\.venv\Scripts\python.exe scripts/workflow.py validate` | 0 | Passed |
| `.\.venv\Scripts\python.exe scripts/workflow.py dry-run --task IG-1A` | 0 | Passed |
| `PYTHONPATH=src .\.venv\Scripts\python.exe -m wgc.contracts.source tests/contracts/fixtures/valid-source.json` | 0 | Passed |
| `git diff --check` | 0 | Passed |
| `pwsh -NoProfile -File scripts/check.ps1` | 1 | The pre-existing workflow sandbox copied live in_progress status/events; minimal out-of-card repair awaits operator authorization. The dry-run ready-only failure has been repaired inside the allowed check script, then verified through explicit dry-run. |

Full-check evidence is retained at private/workflow/checks/active-f430d107590d4118bcc85544a59ef6fd. Initial baseline checks before the claim passed 26 tests. Initial focused failures and their corrections remain in checkpoint-implementation-01.json and checks-interim.json. No test was removed, skipped or weakened to hide a failure.

## Blocker and smallest resolution

The sandbox fixture in tests/test_workflow.py copies the current queue task, including its status and real transition events, into a synthetic temporary repository. Its state-machine tests require the pre-claim ready state and cannot resolve real evidence in the temporary workspace. The proposed patch sets only that copied task to ready and clears only its copied events. Production queue state, event evidence and every assertion remain unchanged. The exact patch is workflow-fixture-scope-request.patch. An asynchronous operator question requested this single write-scope exception; no authorization has been received at candidate freeze. This file has not been modified.

scripts/check.ps1 was changed within the card scope to select ready, otherwise active, otherwise the first task for a harmless packet dry-run; an explicit -Task also works. This launches no model and changes no task status. pyproject.toml now includes the source-contract test directory and src import path in the ordinary suite.

## Inputs and preservation

Input packet manifest SHA-256: `b646eee15539050aca43532e5f6d5a7ffb8dea1acf73326cd42b12460bbade37`; context SHA-256: `e2196f03fecabb5d6f2afa1161b6778cbefcb27693bc2a7a35e1c4eec0eb9c12`. All 11 context hashes and initial queue/base hashes were verified before claim; the base files were reverified after UI confirmation. The original immutable claim and its artifacts were verified again after implementation.

The only product/test writes are the declared IG-1A directories, pyproject.toml and scripts/check.ps1. Workflow run/check files and queue/generated views follow the authorized workflow. Existing staged changes in both integration files were used as the baseline and preserved. No reset, clean, stash, stage, commit, push, archive/history read, neighbouring-repository write, new agent/chat, scheduled automation, external API or game-content import occurred.

## Limits and open decisions

The validator supports only the documented bundled JSON Schema keyword subset, without third-party dependencies or network access. Shape validation does not authenticate humans or prove evidence meanings. Review-basis completeness remains a claim; current freshness is conditional on the recorded complete basis. Coverage counts are structural region counts; overlap across box and extracted-text conventions requires inventory author judgment. Descriptions preserve mechanical fields but do not execute them. No universal precedence, reaction queue, rollback or random distribution is assumed.

Open IG-3A decisions are listed in contracts/ig/README.md: formal types/operators/units, causal events and transactional history, invocation bindings/reactions/continuations, cancellation survival, tables/calculations/geometry/chance, complete visibility-safe responses, dependency closure/readiness and formal-contract attachment. No importer, formal rule interpreter, compiler, runtime or AI opponent is implemented.

## Frozen product paths and SHA-256

| Path | SHA-256 |
|---|---|
| `contracts/ig/README.md` | `71163c1b98e50ac767ca10fb0b174fdd113bc4d13097eec3495065b0c09dfb88` |
| `contracts/ig/source.schema.json` | `749405ff52615a77bf46543e47a68504f4482f38c2c394979147c80dd01bed74` |
| `pyproject.toml` | `e7d4993802db43bca3446ca0c6bc684c04a62ecf53bb7cbb0fa2019709a1571d` |
| `scripts/check.ps1` | `587b06670b7c42c567e95e67afe1d738681f2ad95e9fe1464b4f60cfb6425f73` |
| `src/wgc/contracts/__init__.py` | `e41623d285e0a5c24494cb81a161d63ae1816c1ef9fb3f810a657a6cf5cfdf81` |
| `src/wgc/contracts/source.py` | `8e045b7c96076051632ecaab6c6bbb24d8394308383a9b4d9910302b18619e10` |
| `tests/contracts/fixtures/catalog.json` | `1c28ca6fcaa72748853d9528ac8334295ecf7bf03515335f620316757646a9b8` |
| `tests/contracts/fixtures/invalid-anonymous-identity-conflict.json` | `656c89379b355fc478d5a9faf217116f8ff994eb2e523e2bea3704f6f5061060` |
| `tests/contracts/fixtures/invalid-changed-aspect-hash.json` | `2c04c31919aeb450cc48ae80e1c2f82b3713dd14c0ecfa3ff6c07e43b594c2be` |
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
| `tests/contracts/fixtures/invalid-table-note.json` | `3e59a7c9cc3d6ba213c5adaeaaa8869eee84b97f3c73c6b7e503fc5b30ed80a9` |
| `tests/contracts/fixtures/invalid-unknown-without-gap.json` | `ee5e80d4b000bd48a518c81136bc254349e19561112987aca112db520517975b` |
| `tests/contracts/fixtures/README.md` | `82a5f403d0ce3df1fdb75d955173a09a9cb79c84680dce77663c16f914e0ad2b` |
| `tests/contracts/fixtures/valid-changed-aspect.json` | `92ee3df90d0501e2af40528f4505d43d6ab3c88af00d4d23e3a0f176faa2a723` |
| `tests/contracts/fixtures/valid-changed-dependency.json` | `9fa45d5b015851ad321a936c578c5e09122fd716b86af96ef9c12db67d3c46a7` |
| `tests/contracts/fixtures/valid-cross-section-exception.json` | `6dc73a731e0e36f5dd1b8629e712cee81e2f7e9b5508d27735997a419caf19f7` |
| `tests/contracts/fixtures/valid-edition-conflict.json` | `044556aac43817f78d6356e6974412c06c9b12834282353108a3833734f658a0` |
| `tests/contracts/fixtures/valid-historical-reference.json` | `9f6d03b2372847cb4e678d5537cb51f030e2370a005ba5ffa2eb55876db9d1b2` |
| `tests/contracts/fixtures/valid-overlapping-context.json` | `ee16f98d763e528896d3a4e063e4d1239149aed29c705ee5cba401688a5be77a` |
| `tests/contracts/fixtures/valid-partial-review.json` | `d12c2bf2bb7654217e57c9b77da67d1d74e0b388192dd64fc4b365190eb8939d` |
| `tests/contracts/fixtures/valid-procedure-cycle.json` | `fabc738c5423550d2a061095151a3b8a60d1e168f81a2a85f75258b011517f2b` |
| `tests/contracts/fixtures/valid-source.json` | `9f6d03b2372847cb4e678d5537cb51f030e2370a005ba5ffa2eb55876db9d1b2` |
| `tests/contracts/test_source.py` | `8d97d98c076f65bba12f8546145fac66b68bcd477c524b4c550a19b684cd6747` |

## Independent review handoff

review-prompt.md contains the separate-session prompt. Do not start review until the operator resolves the scope exception, all required checks pass, a new delivery.json pins the repaired hashes, and workflow transitions IG-1A to review. The current delivery-candidate.json is frozen evidence of a blocked candidate, not a passing review delivery. The next operation is exactly the bounded fixture repair after operator authorization; no downstream work is authorized.

## Final check and blocked handoff

The final check-script version was run again: plan=0, dry-run=0, pytest=1, diff=0. 7 failed, 65 passed in 28.10s. Logs: private/workflow/checks/active-58245dbebedc4865bd3cde4a7d4200b0. The dry-run integration repair works; the seven unchanged workflow fixture failures remain. No further unchanged retry was made.

IG-1A is handed off as blocked, not review/done. The operator must authorize the single test-fixture write-scope exception; then replan blocked -> planned -> ready with workflow evidence and resume using a new claim/checkpoint before applying the approved patch. Retain this frozen candidate. After all checks pass, freeze a new delivery and enter review. The independent review prompt is prepared but must not be dispatched against this failing candidate.

Final measurement UTC: 2026-10-12T15:22:49.264628+00:00; elapsed wall seconds: 1879.489. Latest checks are checks-02.json and checkpoint-frozen-candidate-02.json.
