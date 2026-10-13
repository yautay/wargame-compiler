# IG-1B frozen executor delivery

**Outcome: four task criteria implemented and checked; ready for separate independent technical review.** This executor does not grant acceptance, done, source meaning or executable readiness. No next task is started.

The operator explicitly accepted IG-1A and authorized starting the next ready task in this same conversation. IG-1A completed through hashed accepted/done events; all 82 frozen delivery artifacts remain unchanged. IG-1B was made ready only after scoped input/hash enumeration, then claimed with pinned packet and ownership evidence. The local wgc-queue and wgc-execute skills were explicitly read and applied.

## Delivery and measured inputs

`src/wgc/inputs/snapshot.py` provides an offline, read-only byte snapshot facility and CLI. `contracts/ig/input.schema.json` specifies versioned input/source manifests; the source contract canonical profile and bounded evaluator are reused unchanged. Only the IG-1B owned paths were added. Existing pyproject/check integration paths remain unchanged; new tests are run explicitly.

- Measured WGU inputs: **23 files**, exactly `wgu.yaml` and `kb/`, rehashed from current bytes. They match the advisory 23 game-file entries. The prior inspection also cited four utility code-basis files, which are not this task input and were not read.
- Source registry: **2 copied files**, exactly promoted `rulebook.pdf` and `provenance.json`.
- Independent copied-byte verification: **25 files, 5199801 bytes**; every copy matches current original bytes and request pins.
- Configured sources: **36 individually rechecked missing paths**, each with explicit role/availability and null bytes/hash/copy path. No promoted-source substitution.
- Input snapshot ID: `sha256:0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df`.
- Source snapshot ID: `sha256:86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008`.
- Second real freeze produced identical IDs, manifests and results; existing snapshots were verified, not rewritten. No unsealed staging remains in the actual SPQR snapshot roots.

The selected pin is a **new IG source** from the assigned promoted SPQR 5E registry, with `identity_to_wgu_original: unknown` and `semantic_acceptance: not_granted`. Its PDF SHA-256 is `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`. Edition is declared registry provenance; this task did not read publisher meaning. A stored archive locator was preserved as metadata without archive access.

The content-addressed availability report is `private/ig/projects/spqr/sources/availability-d7d7370248aafe9fe4393c5e767264768d908a220f3ef7899de58078f57d1923.json`; SHA-256 `d7d7370248aafe9fe4393c5e767264768d908a220f3ef7899de58078f57d1923`.

## Criteria and required controls

| Queue criterion | Executor coverage |
|---|---|
| 1. Every input file has path, bytes, hash, role and availability; detect change during copy. | Implemented and checked: Every listed file has a relative path, role, availability and exact byte/hash evidence or explicit nulls. Required pins, same-handle stability, independent copy hashes, global origin rehash and KB name-set checks detect mutations. |
| 2. Missing 36 historically configured source paths are rechecked and reported, not silently substituted. | Implemented and checked: All 36 historical configured paths were individually rechecked during preflight, snapshot and independent verification. Missing originals remain missing, never substituted with selected promoted bytes. |
| 3. Pin the promoted PDF as a new selected source with identity_to_wgu_original unknown. | Implemented and checked: The source snapshot retains the exact promoted PDF/provenance and explicit new-source pin. The input manifest references its exact snapshot ID; original WGU identity remains unknown. |
| 4. Reject path escapes, linked paths and unintended source reads; no neighbour writes. | Implemented and checked: Unsafe spellings, duplicate/case aliases, linked ancestors and physical aliases reject. All plan paths are checked before source bytes. Windows checks actual opened final paths/reparse attributes and shares only reads; POSIX uses descriptor-relative O_NOFOLLOW. Destinations are disjoint from origin roots. |

Unmet implementation criteria from the executor perspective: **none**. Unmet lifecycle gate: **separate independent technical review of these exact hashes**. No self-review or human source-meaning acceptance is fabricated.

Synthetic tests derive expectations from the task byte/scope contract and architecture snapshot invariants: copy mutation and same-size/restored-mtime mutation reject; missing sources remain explicit; new KB names and newly appearing sources reject; duplicate/case/hardlink aliases and traversal/ADS/device names reject; actual directory junction/symlink escapes and opened-handle redirection reject before consuming content; read-only neighbour roots cannot become output destinations; independent byte/hash/manifest-ID oracles and repeatability pass. On Windows, attempted writes while a read handle is open are denied. Publisher content appears only in private copies.

## Actual passing checks

| Command/control | Exit | Result |
|---|---:|---|
| Explicit final tests/inputs suite, fresh test-temp-04, local require_escalated | 0 | 33 passed in 4.69 s; real Windows junction/hardlink tests included |
| pwsh -NoProfile -File scripts/check.ps1 -Task IG-1B | 0 | 102 passed in 46.11 s; plan/dry-run/tests/diff all 0 |
| Actual pinned snapshot CLI, two executions | 0, 0 | Identical snapshot IDs/results; existing bytes reused |
| Independent private copy/origin/hash/availability/manifest-ID verification | 0 | 25 files, 5,199,801 bytes; 36 missing sources; no actual staging remains |
| git diff --check | 0 | Existing line-ending warnings only; no whitespace errors |
| workflow.py validate and next | 0, 0 | 39 tasks valid; No ready task |
| IG-1A frozen delivery SHA-256 preservation | 0 | All 82 accepted delivery artifacts unchanged |

Exact passing command records, logs and result JSON are in checks.json. Tests/inputs is outside the inherited explicit default testpaths, so it was run separately without an out-of-scope integration edit. The two suites are reported separately.

## Development failures and resolution

All earlier logs are preserved in development-check-history.json. First default-sandbox test run: 14 passed/13 failed, 8.30 s; the environment denied final-handle path inspection (WinError 5), actual junction creation and hardlink creation. The library failed closed. The explicitly scoped require_escalated command was approved by automatic review; no rejection or workaround occurred.

The first permitted native run: 16 passed/11 failed, 4.65 s. A newly created-file diagnostic established different ctime semantics between Windows fstat and pathname stat. Implementation was corrected to compare ctime within the same handle API, path identity/size/mtime separately and retain full copy/global origin SHA-256. This is a recorded changed hypothesis, not an unchanged-failure retry. Assertions were not weakened. The corrected suite passed 27 tests in 3.70 s; after additional publication/metadata/cleanup-boundary controls, the final 33 tests passed. No independent review repair cycle has occurred for IG-1B. IG-1A F2 has not been reopened or repaired again.

## Configuration, measurements and limits

Executor `executor-ig-1b-20261012T182300Z`; current model/reasoning **gpt-6.1-sol/high**. The same current chat was confirmed by the operator from its UI before substantive work; configuration.json records continuity and distinguishes direct current-session testimony from unavailable runtime metadata. No prior-session settings substitute for it.

UTC claim-to-freeze interval: `2026-10-12T18:24:46.107634+00:00` to `2026-10-12T18:42:30.821515+00:00`; elapsed `1064.713881` seconds. Token counts, operator seconds, monetary cost, peak memory and game performance are null. Test seconds are measured controls, not gameplay latency. Independent technical defect counts and source-meaning defect counts remain null until the appropriate separate review; no known unresolved executor defect is claimed fixed by self-acceptance.

Snapshot immutability is append-only application behavior with revalidation, not OS-level protection against operator tampering. Source and input publication are separate; a failed input publication may leave a valid unreferenced source snapshot. Origins are not a global filesystem transaction; later origin changes do not rewrite frozen bytes. Destination directories require isolation from hostile concurrent writers. Failed staging is retained under its fresh run/test location as incomplete evidence. On this host, required Windows handle/link controls need a permitted local context; restricted execution rejects them rather than weakening them.

Open decisions: obtain independent technical review; later tasks reconcile unavailable materials and source meaning. Missing configured material blocks only dependent source verification, not the available KB byte snapshot. No importer, interpreter, compiler or game mechanism was created. No archives/Git history, neighbour writes, new agents/chats, automation, external services, commits or pushes were used.

## Frozen product files and SHA-256

| Path | SHA-256 |
|---|---|
| `contracts/ig/input.schema.json` | `cc79d4824170a39105598b7ba267771b7516ae8b6fc2c1b67e6b019445bd2504` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/ambiguities.yaml` | `d11e59ee4858421ed7f25091641964f45c41625003ba9d03ef9f51cec28adb9a` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/changes.yaml` | `fabf4b17ce452fa6bf1c634dca430956054f47e392b2d773e3a562b978c53053` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/manifest.yaml` | `3031a4c7ea87552d5074dc4f9bd43947dfdb4189d060ded4bbd3eb66ef2cd7f6` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/notes/overview.md` | `32886018fc9523502a50f46523a49e8e70e92d223d360c69a64eb5644d28f80b` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/procedures.yaml` | `651614ce6a49c436ec23a6b8bd5b64f8c77d786edd4323b2ae91c4cb6ff3eff3` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/relations.yaml` | `1737abb4a2f8877af8964e303d325d24ee7ae17ab2a9e3edeec4f91974fecb2a` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/01-wprowadzenie.yaml` | `77709eeec903a5a8b6f80a3bdada4994254dbdf41844c947d6edd8ddf81e549c` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/02-komponenty-terminologia.yaml` | `94810dd6362e28d5fde8633c6788082e8705849d58c01abc0f660f6c4cb78aae` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/03-sekwencja-gry.yaml` | `d926613871f4bd99757e07b0b5f3df59800757afbb68576a0382a64538702688` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/04-dowodcy.yaml` | `8b0abe24168605ee682449ce75f24408075a1c50c22abfd3f50c9d3704ad77cc` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/05-aktywacja-rozkazy.yaml` | `d7db614e3b1007b24228460be4bbd1197262b20046f82e1e205564e04f0a911b` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/06-ruch.yaml` | `5f365777d87030b96e3ede3ab8b1d1c97fddfd6fc17b91c59b8daff8b2038844` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/07-ukierunkowanie-zoc.yaml` | `11a8a7c2e2ef6d5bfff2fdee92e0e374418617574b5bd463619d936e1317f8e0` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/08-walka.yaml` | `7ff997bce127f0b08b9754a1739ade67fd9ae36771e5ede40bcb5832e43797a4` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/09-jednostki-specjalne.yaml` | `9e28d5df8720dc1dce71f687146f25fcea313df46e98f670f52cc55b579d221c` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/10-skutki-walki.yaml` | `dceb1c9ad26a8f52e7dcfdf8d0bdb39443a16520a1d02f657fdedbd403976090` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/11-wycofanie-armii.yaml` | `4882c57a9010a010496d610bf2b7030b31c8087c7cd621d3b0f19ace072d44ea` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/rules/12-scenariusze-ksiega-2018.yaml` | `869fcf8be6266607a018b8b617da030cbc03aed44c84e4ca4773e551ddbddf5a` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/scenarios.yaml` | `0287171c71593defc5675c9db3d412ae4dda0635402f459a2e5764514b4ff90c` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/tables.yaml` | `e0d061947276e38723e6c304887650213c8a646dac41ff8cb7bb608c023f5b49` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/terminology.yaml` | `9e86ec5abf30436afd3de805a50972cf3953fd749dcaeac7d52c3d87a4c27ffb` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/kb/terms.yaml` | `44d8f2b6882f549160082a2f200b74901f2099ff54cd5c12a33036296baecc85` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/files/wgu.yaml` | `3f022a178835733ec0b085148c7fdf689430265e1b99bdeff2a4103c566de205` |
| `private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json` | `67ac53869ea80ea4d84018e253a9033e48fe89823d0a9a397ab8fe41b91d33d5` |
| `private/ig/projects/spqr/sources/availability-d7d7370248aafe9fe4393c5e767264768d908a220f3ef7899de58078f57d1923.json` | `d7d7370248aafe9fe4393c5e767264768d908a220f3ef7899de58078f57d1923` |
| `private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/files/provenance.json` | `185ef47f755fa710273ea48fbf4ad544e9ac20a3be708d18ee548349869ec3a8` |
| `private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/files/rulebook.pdf` | `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e` |
| `private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json` | `615b1ae1cbeebf894c7f8dbbb7c3f2bcb0819427a342b3fa05bc690c33b9eed8` |
| `private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/source-pin.json` | `3e722f7b3a30e81b40443d080c09bc28d276b23ba10568ec4dea5549af09871a` |
| `src/wgc/inputs/__init__.py` | `5c4a97d2a37a1c082f97c9d53249ac5190b08055d36196200d52fd73fbb4628a` |
| `src/wgc/inputs/README.md` | `ddda59507927e8bb2c29f5255d34591f7a2f661ca5fd9133452dd7d54e11804f` |
| `src/wgc/inputs/snapshot.py` | `14663b10b27e1bfb09d8da47b1c5c3826784399a8c0da6e81d13dd2461a08640` |
| `tests/inputs/test_snapshot.py` | `1a515d131c8c7e254dc48f9d9790045ba60af1e9cea1f3ee3cbbb419aa2b6fa6` |

## Next exact action

Transition only IG-1B to review with delivery.json. Supply review-prompt.md to a separately authorized independent reviewer. Confirm that reviewer current-session configuration, verify the complete frozen list first, rerun required native/synthetic and project controls, and report findings without implementation edits or self-acceptance. Do not start IG-1C.
