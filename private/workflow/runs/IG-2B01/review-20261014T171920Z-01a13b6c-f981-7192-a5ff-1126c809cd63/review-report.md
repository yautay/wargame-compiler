# Independent review of frozen IG-2B01 delivery

Outcome: **PASS for the bounded inventory artifact and technical review gate**. No blocking product/content finding was established. One contained process deviation and one transcription advisory are recorded below. PASS does not erase the earlier overread, authenticate a human, approve transcription/semantics, close the queue, or establish executable readiness. The coordinator must explicitly record the disposition of the access deviation before technical acceptance.

Reviewer: `codex-01a13b6c-f981-7192-a5ff-1126c809cd63`, independent of executor `codex-01a13b57-40e6-78d2-9d17-0b3e91afba77`. Actual `gpt-6.1-sol` / `high` was verified from this session's current `turn_context` before substantive review. The session metadata, not launch settings or executor confirmation, is the configuration basis. Exact evidence and measurements accompany this report.

## Frozen targets and scope

The executor directory is `private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77/`. These supplied pins matched before assessment and were checked again during final preservation:

| Artifact | SHA256 |
| --- | --- |
| final-seal.json | 92d0497dcdd19876127217917bb30240ff17e8893d7cc2b195d342fb53d69e13 |
| delivery.json | 9fd4b11bdfd04e75edafca96daa29add39151612291b2fefbd7a68e534325ef7 |
| delivery-manifest.json | 1d8ad7eaa494f14a95c762de3197ae7b9c4be057a1e4470e11987d56761fd5fc |
| delivery-handoff.md | cc1db56c976a7b3742944b1f6b4cc5891aaff1961344b3d4864cabf756235f3b |
| final-verified/inventory.json | 42adf9a1598bd682917eb087e295fe899212e59dd81aed5c293e2187b9c587bb |

The assessment uses `final-verified/inventory.json` and `region-ledger-final.json`; earlier author/replay records were used only for repeatability/preservation. All 557 executor delivery-manifest members match their byte and size pins. The review JSON preserves the original delivery artifact list exactly.

The original official PDF SHA256 is `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`; provenance SHA256 is `90ca669ff57bd499975fbf29353175caff5ee583cb0f4be588f37cf21d57959b`. Neither was downloaded or modified. Full text/image inspection was restricted to physical pages 1–4. The only page-5 content access was the final context region `[71895,63131,495099,98485]`, the quantized rational inverse of the specified x=44..303, y=50..78 point crop. No initial broad probe image/text was opened. Pages 6–44 received structural count/geometry access only.

The queue remained `review`. Existing packets were read and their frozen manifest/context bytes verified; no new packet or allowlist edit was needed under the operator's explicit review scope. Four current projection comparisons differ from packet snapshots: initial STATUS/HANDOFF/task card and final task card. The exact differences are retained in `packet-assessment.json`; the final card differs only by `in_progress` → `review`. These are live queue projections rather than changed frozen packet bytes.

Named current IG-2A dependency records, baseline and registry match the dependency-verification pins. Their selected delivery/review/acceptance/done chain is consistent, and the current queue records IG-2A as done with the pinned accepted/done artifacts. Deep reference checks additionally expose the expected old queue pin and old context-policy pin. The latter matches the retained `context-policy-before.json`; current policy adds six named context paths and preserves all previous entries. No immutable dependency artifact drift was found. This dependency verification does not transfer semantic acceptance.

## Independent inspection and expectations

The reviewer rendered original physical pages 1–4 directly with Poppler at 144 DPI, extracted those pages with pdfplumber and pdfminer, read their complete region texts, and compared all four full-page originals and independently drawn overlays with all 130 final ledger records. The 14 non-cover diagrams were additionally inspected together in the independent detail contact image. `independent-expectations.json` states source-observed features separately from executor outputs; `content-observations.json` records every region/revision and component checklist assessed.

| Physical page | Inventory regions | Source accounting observed |
| --- | ---: | --- |
| 1 | 26 | Visible series/title/edition/credit, full SPQR outlines, framed artwork, TOC heading and twelve rows with dot leaders/destinations, four panel rules, publisher address; hidden header/folio and hidden copyright remain explicit raw-layer artifacts. |
| 2 | 31 | Header/folio/rule/footer, introduction heading and all paragraphs, edition/player/new-player notes, split-column note completion, components heading/introduction and ten bullets, map/piece headings and descriptions, clauses 2.21/2.22 and opening 2.23 fragment. |
| 3 | 38 | Complete 2.23 continuation, four skill bullets, markings/borders, complete 2.24 historical paragraph, leader/marker descriptions, 2.25 heading, five annotated groups and five sample counters/captions, four panel rules, chart/die and terminology headings/text, five definitions and editorial furniture. |
| 4 | 35 | Sixteen left-column definitions, Type/ZOC and combat-types introduction, Consular Army/Legion, Velites/Hastati/Principes/Triarii text and four counters, wrapped text fragments, header/folio/rule/footer. |

No omitted clause, heading, note, inline example, navigation row, diagram, external legend, caption, connector or visible editorial rule was found. The source contains no separate mechanical outcome table on these pages; the TOC navigation rows and annotated-example panels remain accounted for. External navigation/reference strings remain raw and unresolved.

Grouped diagram granularity is sufficient for this inventory task. The phalanx group contains its caption, counter values, six annotation labels and connectors; infantry and cavalry each preserve both counters and every shared/separate label/connector. Scorpion and elephant preserve their captions and complete local legends. Five additional samples retain full raster art and captions; four page-4 counters preserve their entire printed contents. Generic checklist references to all counter values do not substitute for future exact transcription, but current PNG evidence and explicit partial/unprocessed statuses keep those details present and unapproved. There is no requirement here to invent separate denominator units for each raster glyph.

Reading order is an explicit complete permutation of all 171 regions, including context and placeholders. Inspection confirmed the left-to-right column traversal and special crossings: page-2 new-player note across columns; 2.23 across pages 2/3; terminology list across pages 3/4 (not an incomplete DR sentence); Hastati and Principes wraps; Triarii into the exact page-5 tail. The 15 declared continuation/illustration links have appropriate endpoints/reasons and match the continuation report exactly. Folio evidence correctly binds visible labels 2/3/4; the invisible cover folio does not become a visible printed label.

## Independent reproduction and integrity

The reviewer recreated each of the 131 exact cropped PDFs from the original source using independently written orchestration, the final normalized bounds and explicit point arithmetic. All 131 extracted texts and PNG pixels agree with final evidence. Unicode codepoint counts and half-open offsets agree. Actual PNG dimensions equal separately computed double-precision ceiling predictions, with no tolerance. The report preserves each render command, exit code and timing. This reproduction proves locator/render/text consistency; content completeness was assessed separately from originals and the ledger.

The independent character/word-center audit found zero unassigned nonspace character centers and zero unassigned words on all four pages (749, 4885, 3116 and 4811 nonspace characters). Eight nominal cover-title font boxes extend below that title region; inspection of the full original, overlay and reproduced title showed complete visible contours. This metric anomaly is not a clipped-letter defect. Character-center accounting alone was not treated as a raster/vector completeness oracle.

All 216 enclosing revisions (inventory, 44 pages, 171 regions) were independently recomputed with the published integer-only canonical JSON profile. Reverse-order persisted-key lookup preserved every UUID and registry byte. Reassembly reproduces exact canonical inventory bytes. Independently stripping evidence/restoring baseline labels reproduces the executor's author replay. All original registry entries, including the four retired placeholder keys, remain present. The final logo correction changes revision/evidence, retains identity/registry, and its complete R/Q contours are preserved. No product/schema/validator weakening was found; frozen product pins match.

All 130 ledger bindings, rational native bounds, coverage and reading indexes equal their final inventory counterparts. All 131 uncertainty records bind current final evidence and exact text pins; replacement-character counts/offsets are accurate (zero U+FFFD in these files). All 130 representation-gap records match final revisions/statuses. Special source glyphs, raw hyphenation, raster-only text and extraction contamination remain unverified. No normalization or semantic promotion was performed.

The independent disjoint rectangle calculation reproduces every geometric complement and accounts for exactly 10^12 page-area units per page:

| Page | Geometric gap area, trillionths |
| --- | ---: |
| 1 | 540608359683 |
| 2 | 295556916526 |
| 3 | 408882759548 |
| 4 | 312879453869 |

The inspected complements are margins, gutters, spacing, cover/panel background. They remain explicit unapproved gaps; blank appearance grants no exclusion. The full 44-page inventory denominator is 170: 130 authored task regions plus 40 exact unchanged unprocessed placeholders on pages 5–44. One context region contributes zero. All page/placeholder records 5–44 match the accepted baseline exactly. Represented/excluded counts remain zero at every level. Transcription is partial for the 130 authored regions; descriptive/formal semantics remain unprocessed.

## Findings and disposition

### IG2B01-R01 — medium / P2 process observation, contained, nonblocking for final artifact

Locator: executor `context-access-authorization.json` and `context-overread.json`; physical page 5 initial documented y=50..105 probe versus final region `[71895,63131,495099,98485]`. Reproduction/basis: compare these already-pinned metadata reports and the exact final context evidence. The initial image/text itself was not opened in this review, and neighboring content was not analyzed.

The executor explicitly reports that the initial 55-point-high probe exposed two lines and part of an adjacent counter. A written self-authorization for a crop does not make neighboring content necessary continuation context. This is a real bounded access deviation; narrowing the final crop contains final evidence and denominator use but cannot undo earlier exposure. The available basis is disclosure and metadata, not independent verification of the prohibited adjacent content. No claim is made that the overread did not occur.

Impact: scope discipline and access provenance, without a demonstrated omission/corruption of the final four-page inventory. Minimal corrective action: the coordinator records a separate disposition of this disclosed deviation before accepting the technical delivery; future continuation probes start with a narrow predetermined region and expand only with specific authorized necessity. Preserve the initial disclosure and all frozen bytes. No content repair, broad reinspection or retroactive authorization is requested. Required verification: acknowledge the metadata disclosure and recheck final narrow context/zero denominator pins; no neighboring-entry access.

### IG2B01-R02 — low / P3 transcription advisory, nonblocking

Locator: physical page 1, key `ig2b01:cover:edition`, region `region:74a8c133-e1a5-4ec4-8ebc-517987e6b24f`, bbox `[441176,715909,562091,741161]` (see authoritative inventory/ledger), text `evidence/p01-007/text.txt` and final corresponding PNG. The visible line reads “5th Edition”; literal extraction is `E5th EdBition`, with extraneous E/B at Unicode codepoints 0/7 from neighboring title font-box overlap. Independently recreated text/PNG reproduce this anomaly exactly.

Impact: an uncritical consumer could mistake machine evidence for transcription. Existing generic extraction uncertainty and partial coverage prevent that claim in this delivery, so this is not a blocking inventory defect. Minimal refinement: a future exact-transcription task records this specific anomaly/offsets and checks the visible PNG before proposing normalized text. Preserve literal evidence; do not silently edit publisher/source bytes or promote coverage. Required verification: compare exact literal text, codepoints and image at the same region revision. The advisory is also recorded per region in the independent observations.

## Criteria and checks

All three exact queue acceptance criteria pass within inventory/source-accounting scope:

1. “Account for every page region: clauses, headings, notes, examples, diagrams, tables/legends and editorial exclusions.” Source-bearing content and editorial furniture are inventoried; editorial classification is not approved exclusion. No omission was established.
2. “Keep exact evidence locators, uncertain readings and cross-page continuations; no silent omission.” Final bindings/bounds/text/PNG/offsets and continuation scopes reproduce; generic uncertainties/gaps remain explicit, with the additional edition advisory preserved here.
3. “Independent review compares the assigned pages against the complete region ledger.” This distinct reviewer inspected all four originals, complete texts, independent overlays and all 130 final ledger entries; executor self-inspection was not used as independent evidence.

Required `scripts/check.ps1 -Task IG-2B01` passed while status was review: 102 tests. `scripts/workflow.py validate`, `git diff --check`, and corrected root inventory validation passed. Required commands, stdout/stderr, exits and UTC/wall measurements are retained. Existing pypdf nonzero-index Xref and Git CRLF notices are preserved. The reviewer initially supplied an absolute CLI path, which exited 2 before validation; the corrected private-relative invocation exited 0. Other reviewer preflight/assessment errors and their corrected hypotheses are preserved in `tool-command-audit.json` and `reviewer-errors.json`, not hidden behind passing checks.

The review did not change the queue, public files, existing packets, product/delivery, baseline, source or provenance. No history/archives, neighboring repository, external API, installation/global setting, agent/chat/automation, reset/clean/stash/commit/push, repair, acceptance/done or IG-2B02 operation was performed. New evidence is restricted to this review directory and the permitted standard check scratch.

## Coordinator action

Verify `review-seal.json`, its review/manifest/handoff pins and the five original delivery pins above. Record the explicit R01 access-deviation disposition. If the coordinator accepts this bounded technical PASS and that disposition, prepare technical acceptance for these exact original delivery hashes and complete only IG-2B01 through the normal queue workflow. Do not convert this review into a human semantic decision or execute IG-2B02 as part of it. The reviewer has left the queue at review and made no transition.
