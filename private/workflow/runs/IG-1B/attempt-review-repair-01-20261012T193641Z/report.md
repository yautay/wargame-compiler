# IG-1B first bounded F1 repair delivery

**Executor outcome: F1 repair implemented and checks pass; independent closure remains pending.** All four source-input task criteria are covered from the executor perspective. No accepted/done or source-meaning/executable readiness decision is made here.

The operator instructed “Kontynuuj” after the stated next action, bounded F1 repair and independent re-review. Only this repair was claimed through `review -> changes_requested -> in_progress`. The existing reviewer session is authorized; no new session or agent is created. IG-1A remains done and its 82 frozen artifacts are unchanged.

## Finding and exact repair scope

Independent finding F1 (P2) demonstrated that extra KB bytes, a blob for a missing entry, or an unlisted junction could remain in a sealed directory while verification/reuse returned its unchanged ID. The original reviewer report/evidence are preserved: `private/workflow/runs/IG-1B/review-confirmed-20261012T185333Z/review.json`, SHA-256 `d5cc08accd4da84660ef3b451022758312e14b0f5c1e4d543de79458b9f22af4`.

Only `src/wgc/inputs/snapshot.py`, its local README, and `tests/inputs/test_snapshot.py` changed. The schema, canonical identity rules, native opened-handle controls, input plans, copied private bytes, source pin and availability report are unchanged. Original 33-test source bytes remain an exact prefix of the augmented file; 18 new tests were appended, with no original assertion edits.

`verify_tree_names` derives permitted files from available manifest blobs plus root manifest.json and the source-only source-pin.json. Permitted directories are exactly the required parents. It inventories names with no-follow metadata and rejects unknown files, metadata, empty directories, nonregular entries, symlinks and Windows reparse points before opening copied content or the pin. A manifest-declared missing entry contributes no allowed blob. The check gates staging verification, published verification and existing-target reuse. A corrupt existing snapshot is rejected and left unchanged.

This addresses ordinary static tampering; the documented need to isolate destinations from hostile concurrent writers remains. No new importer, interpreter, compiler, game mechanism or source semantics is introduced. F1 repair-cycle count is **1**; there has been no second cycle or unchanged-failure retry in this repair.

## Criterion coverage

| Queue criterion | Executor assessment |
|---|---|
| 1. Every input file has path, bytes, hash, role and availability; detect change during copy. | Covered. Exact file/parent-directory closure now complements size/hash/availability accounting and all original mutation/copy integrity controls. |
| 2. Missing 36 historically configured source paths are rechecked and reported, not silently substituted. | Covered and unchanged. The private audit rechecks the exact current WGU configured path set, all 36 missing paths, null evidence and no substitution. |
| 3. Pin the promoted PDF as a new selected source with identity_to_wgu_original unknown. | Covered and unchanged. Exact promoted PDF/provenance/source pin retain new_ig_source and identity_to_wgu_original unknown; no meaning acceptance. |
| 4. Reject path escapes, linked paths and unintended source reads; no neighbour writes. | Covered. New static sealed-tree link/addition rejection is exercised in both snapshot kinds and verify/reuse modes; original path/handle/alias/disjoint-output controls remain strict. |

Unmet implementation criteria from the executor perspective: none. Unmet lifecycle gate: separate independent technical closure on these new hashes. The previous independent P2 remains formally open until that reviewer disposition. Source-meaning defect counts are null; source meaning was not reviewed.

## Actual controls and preservation

| Control | Exit/result |
|---|---|
| Final explicit input suite, fresh basetemp, reviewed native execution | 0; 51 passed in 5.56 s |
| Byte-identical reviewer review_controls.py replay in a fresh evidence directory | 0; all 14 expectations conform, including all three saved F1 reproductions |
| Byte-identical native_handle_probe.py replay | 0; redirected junction handle rejects before yielding content; normal read handle denies writes |
| Byte-identical private_audit.py replay | 0; 25 copies, 5,199,801 bytes; exact tree sets; two repeats preserve all IDs/bytes |
| scripts/check.ps1 -Task IG-1B | 0; 102 passed in 57.38 s; plan/dry-run/tests/diff all zero |
| git diff --check and workflow.py validate | 0, 0 |
| Preserved original product/delivery/reviewer/IG-1A hashes | 0; all comparisons match |

Checks and durations are recorded in checks.json/replayed-checks.json; logs are retained. Native tests/probes require normally reviewed local escalation on this host because the sandbox denies final-handle inspection and actual links. No safeguard or expected result was weakened. Replayed reviewer scripts are executor validation, not a new independent review; all generated evidence is in a fresh directory and the original reviewer files remain immutable.

All 34 original product files were copied byte-for-byte into baseline/ before the claim. The entire original 59-artifact delivery is reverified through that explicit mapping for old product revisions. Original reports/manifests and all 30 reviewer artifacts remain unchanged. Only the three stated live product paths now have new hashes. Snapshot IDs are unchanged: inputs `sha256:0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df`; sources `sha256:86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008`. The private set contains 23 WGU files, two registry files and 36 individually missing configured sources.

## Configuration, measurements and open decisions

Executor identity: `executor-ig-1b-repair01-20261012T193641Z`. Current configuration: gpt-6.1-sol/high from the operator UI confirmation for this same ongoing chat, retained with explicit continuity in configuration.json. Runtime metadata are unavailable; reviewer-session settings are not used to confirm executor settings.

UTC claim-to-freeze interval `2026-10-12T19:39:20.220424+00:00` to `2026-10-12T19:49:04.930250+00:00`; wall `584.709826` seconds. Tokens, operator seconds, cost, peak memory and game performance remain null. Test durations do not measure gameplay.

Open decision: independently close F1 and assess all four criteria on the new complete frozen list. At most two repair cycles are allowed for F1; if a later unchanged failure exhausts that limit, escalate rather than silently repair again. No semantic or executable acceptance follows from technical controls. Archives/Git history, neighbouring writes, additional chats/agents, automation, external services, commits and pushes were not used.

## Complete current product SHA-256

| File | SHA-256 |
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
| `src/wgc/inputs/README.md` | `13cc4125230d6d7e92b89853b95c8bb00c88fdf7efcf1fa0fc9a1b998597e642` |
| `src/wgc/inputs/snapshot.py` | `6f701f14fb23a377af11ea73eba24e088c90db74acef8587d0838ed4e4eb01ed` |
| `tests/inputs/test_snapshot.py` | `5de3af682b07821c1c6c07ba1fc3e46e3b782a3aa848b263147c04be1ce6f358` |

Next exact action: transition this delivery to review and pass the pinned rereview-prompt.md to the already authorized independent reviewer. Preserve the old report and write a new reviewer result. Do not start IG-1C.
