# IG-1A frozen delivery for independent review

IG-1A: Establish the source IG contract is implemented and passes the required project checks. This is the executor delivery, ready for independent technical review. It is not acceptance and must not be marked done by the executor.

## Criteria met and unmet

- Implemented: Schema represents sources/regions, clauses with stable aspects and semantic groups, relations, gaps, origin bindings, coverage, profiles, runs, reviews and snapshots.
  Evidence: Thirteen typed record families cover the requested collections; nodes embed stable aspects and explicit semantic groups. Static fixtures cover sources/regions/evidence, origin mapping, profile, run, review and selected snapshot.
- Implemented: ID and revision hash rules are explicit and deterministic; anonymous identities do not depend on array position.
  Evidence: WGC-C14N-1 defines exact integer-only canonical bytes, derived revision/aspect hashes, stable namespaced identity and persisted anonymous mapping. Fixed byte/hash vectors, integrity cases and reorder tests exercise these rules.
- Implemented: Source representation distinguishes review, coverage and executable readiness; source-level opaque is accepted without granting execution.
  Evidence: Import, coverage, review metadata/freshness and executable assessment are independent. Opaque source content passes structural validation, but normative opacity/unknowns require blockers; source executable status cannot be ready. Validation always grants no semantic acceptance.
- Implemented: State, causal history, parameters, persistent choices, reactions, continuations, costs, geometry, tables, chance and visibility have addressable source representations; no generic payload-only claim.
  Evidence: Dedicated node kinds and named descriptor fields preserve state, causes/history, parameters, bindings/choices, reactions/continuations, costs, geometry/spatial policies, calculations/tables, chance/visibility and victory. Explicit tests assert required fields independently of schema enumeration.
- Implemented: No importer, formal interpreter, compiler or game logic is implemented; record open formal-language decisions for IG-3A.
  Evidence: Only source description/schema validation and hash/reference checks are implemented. No importer, formal rule interpreter, compiler, game logic or AI opponent exists in this increment. Formal-language choices remain open in the contract README for IG-3A.

All required valid/invalid cases are present: unknown value without gap, changed aspect integrity and stale acceptance, model approval, dangling active versus historical reference, duplicate identity and opaque execution blocker. The 26 static fixture cases have explicit expected results and architectural bases in tests/contracts/fixtures/catalog.json. Additional coverage includes page-spanning clauses, cross-section exceptions, table notes, missing unit, procedure cycle, edition conflict, partial acceptance, dependency regression and coverage denominator overlap.

Unmet lifecycle gate: independent technical review is pending. All implementation criteria and required checks are covered from the executor perspective; the reviewer must independently confirm or reject them. Human semantic acceptance is not required for this task and none was granted. No complete SPQR import, source coverage, accepted meaning or gameplay readiness is claimed by these synthetic tests.

## Configuration and measured evidence

Executor identity: `ig-1a-executor-20261012-0540`. Confirmed configuration: `gpt-6.1-sol` / `high`. Source: operator UI observation in this ongoing conversation, stated `GPT-6.1 Sol / reasoning high - TAK` and recorded in configuration.json. Exact model/reasoning runtime metadata are unavailable; the requested configuration was never used as confirmation. The scope repair resumed the same ongoing session; no configuration change was observed.

Repair attempt start UTC: `2026-10-12T15:30:17.258744+00:00`; freeze UTC: `2026-10-12T15:33:43.441465+00:00`; measured elapsed wall seconds: `206.183`. The previous implementation attempt has its separate measured interval in checks.json. No active-work total across operator waits is inferred.

Full project suite: 72 passed, 0 failed, pytest-reported 30.33 seconds. This includes 46 source-contract tests and the 26 existing workflow/archive-tool tests. Token counts, operator time and monetary cost are null because unavailable; they are not zero. These are check runtimes, not game-performance measurements.

Executor-observed defects: two major infrastructure assumptions fixed (ready-only check dry-run and live-queue state in synthetic fixture); one minor fixed canonical test-vector error. One temp-path environment issue was resolved with fresh private basetemp directories. A briefly overwritten claim checkpoint was restored to its exact original SHA-256 and its implementation increment retained separately. No known failing check remains. Independent reviewer defect counts and source-meaning defect counts are null because those reviews have not occurred.

## Checks

| Command | Exit | Evidence |
|---|---:|---|
| `pwsh -NoProfile -File scripts/check.ps1` | 0 | private/workflow/checks/active-04ffe945d7c343e4871e6602878a2e62 |
| `git diff --check` | 0 | private/workflow/runs/IG-1A/attempt-20261012-scope-repair/diff-check-final.log |
| `.\.venv\Scripts\python.exe scripts/workflow.py validate` | 0 | Verified |
| `Python SHA-256 comparison: removing exactly the three approved fixture lines recreates its original base bytes; all prior delivery hashes remain unchanged` | 0 | Verified |

The full check reports plan=0, dry-run=0, tests=0 and diff=0. Its dry-run leaves the queue unchanged, launches zero models and writes zero product files. The exact passing logs and result.json are pinned in delivery.json. The existing test assertions remain unchanged; no tests were skipped, removed or weakened.

## Authorized scope and preservation

The declared IG-1A write paths were honored, with one explicit operator exception: tests/test_workflow.py. scope-exception.json records the operator reply `pozwalam` to the precise proposed patch. Only the copied synthetic task is initialized to ready and empty events, plus an explanatory comment. Removing exactly that insertion reconstructs the original test file bytes and base SHA-256. The live queue, real transition evidence and assertions are untouched by the fixture.

scripts/check.ps1 now selects a ready task, otherwise the active task, otherwise the first task for a harmless context dry-run; optional -Task pins it explicitly. pyproject.toml includes tests/contracts and the src import path in normal project controls. Original staged content of both files was preserved. The source product was not modified during the scope repair, and all previous frozen candidate artifacts still match their original hashes.

The previous blocked candidate and its failing evidence remain immutable in attempt-20261012-0540. Workflow transitions used the explicit blocked -> planned -> ready -> in_progress sequence with fresh claim/checkpoint and authorization evidence. The next state is review, not accepted/done. Queue and generated views are managed only through workflow transition/render.

No archive/Git-history contents, neighbouring repositories, external APIs, agents/new chats/schedulers, global configuration, resets/clean/stash, commits or pushes were used. No real game evidence was imported into public fixtures.

## Frozen input context

Resume packet manifest: `private/workflow/packets/IG-1A-34c168acdc5349429ebe64436ef952a4/manifest.json`, SHA-256 `d2e6e8d92bfc62609956bff873e1785b7d4805b3a529b40c541d4c6133f391e5`. Context: `private/workflow/packets/IG-1A-34c168acdc5349429ebe64436ef952a4/context.txt`, SHA-256 `e2196f03fecabb5d6f2afa1161b6778cbefcb27693bc2a7a35e1c4eec0eb9c12`. All 11 file hashes, queue hash and context hash were verified before the new claim. The context bundle hash matches the original IG-1A input context; control-plane task events are recorded separately.

## Limitations and open IG-3A decisions

The offline validator supports only the explicitly documented keyword subset used by the bundled Draft 2020-12 schema and fails on unsupported keywords. There is no third-party dependency or schema/network fetching. It checks shapes, hashes, typed references, selected closure, groups, table scopes and review metadata/freshness; it cannot authenticate humans, read decision artifacts, prove source meanings or prove semantic dependency completeness. Coverage counts are region claims, not rulebook-completeness certification. Mixed box/text denominator equivalence still requires inventory author judgment. Informational normative treatment still requires actual human authority and meaning review beyond metadata checks.

Open IG-3A decisions in contracts/ig/README.md include formal types/operators/unit conversions; causal event writes and transaction/history semantics; binding lifetime, loops and reaction/cancellation/continuation policies; table coordinates/lookup/decoding/calculation/modifier order; geometry/paths/stacks; chance distributions and authoritative draws; visibility-safe complete observations and legal attempts; and formal attachment, dependency closure, acceptance invalidation and readiness queries. No universal precedence, reaction queue, rollback or random distribution is selected here.

## Product files and SHA-256

| Path | SHA-256 |
|---|---|
| `contracts/ig/README.md` | `71163c1b98e50ac767ca10fb0b174fdd113bc4d13097eec3495065b0c09dfb88` |
| `contracts/ig/source.schema.json` | `749405ff52615a77bf46543e47a68504f4482f38c2c394979147c80dd01bed74` |
| `pyproject.toml` | `e7d4993802db43bca3446ca0c6bc684c04a62ecf53bb7cbb0fa2019709a1571d` |
| `scripts/check.ps1` | `587b06670b7c42c567e95e67afe1d738681f2ad95e9fe1464b4f60cfb6425f73` |
| `src/wgc/contracts/__init__.py` | `e41623d285e0a5c24494cb81a161d63ae1816c1ef9fb3f810a657a6cf5cfdf81` |
| `src/wgc/contracts/source.py` | `8e045b7c96076051632ecaab6c6bbb24d8394308383a9b4d9910302b18619e10` |
| `tests/contracts/fixtures/README.md` | `82a5f403d0ce3df1fdb75d955173a09a9cb79c84680dce77663c16f914e0ad2b` |
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
| `tests/test_workflow.py` | `c29111c6bb8703615199d7d189ae42dc115a33a445a33d4c37fade9be7826eea` |

## Review handoff

Use review-prompt.md in a separately started independent review session. It requires a distinct reviewer identity, actual configuration evidence, exact delivery hash verification and criterion-by-criterion findings. It does not authorize silent repairs or SPQR meaning acceptance. The prepared prompt has not been dispatched; no reviewer session was created.

Next exact action: independently review the entire delivery.json artifact list and report findings on these exact hashes. The executor stops at review and does not accept its work, mark done or start any downstream task.
