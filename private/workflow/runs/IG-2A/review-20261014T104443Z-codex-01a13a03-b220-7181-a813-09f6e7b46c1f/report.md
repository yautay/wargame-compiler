# IG-2A independent technical review of bounded repair

Outcome: **PASS** for the repaired IG-2A tooling increment. All five prior findings are closed against the exact repaired delivery; no new actionable product finding was established. This report is an independent technical handoff, not acceptance/done or human semantic approval.

Reviewer `codex-01a13a03-b220-7181-a813-09f6e7b46c1f` is distinct from executor `codex-01a139bc-256f-7da0-b4a7-8940ca16fc81` and prior reviewer `codex-01a1363e-1de5-7073-8185-d9a1f2e89c35`. Current-session turn metadata records `gpt-6.1-sol`, effort `high`; the operator also stated “potwierdzam 6.1 sol high”. Configuration evidence is filtered current-session metadata, not the executor's confirmation. No product, queue/status, allowlist, previous-run or source writes were made.

## Frozen scope and integrity

The four operator repair pins match: delivery `c69df3b2867f440c6b330159a2d335dff6bf959192ebb9d3ac5d0ea59977195e`, manifest `3652874c7a029100efe81b93914934e469ba5b519bf1b66b0ff2b209645a7d49`, handoff `0ad1c51043eaef5859f6e99484889ae9e2aa0eda4c837dd9f75c754165b0e758`, final seal `64f96bc690396ceeb3ed37722c0c29546fa4a76448710ad8b8731043f0ce312d`. All 273 delivery artifacts, sealed post-freeze/governance artifacts and 159 prior-review manifest artifacts were verified. Prior final seal and manifest match their operator pins; the old report was assessed through its retained candidates, not assumed correct.

`input-verification.json` records 674 matching checks, including every one of 87 original delivery copies, 81 intentionally unchanged original live artifacts, and all eight product-before copies. Product comparison diffs are generated solely from those verified copies. `preservation-final.json` rechecks those pins, the unchanged workflow/check/search scripts and IG-1A validator/schema/README, the original delivery JSON, current runtime binaries and worktree status. The other 38 queue task records still match repair-start records. Queue SHA256 stays `18621ef45410770936da05949da3c434a9aedf262e50f18db3fc5d90ad809386`, status `review`.

The fresh review-preparation packet's files and queue pin equal `workflow.packet(..., output=False)`; regeneration was unnecessary. `packet-verification.json` pins its manifest/context. The recorded interrupted review transition is consistent with a queue event already written and a successful projection-only recovery; current workflow validation passes. No unexplained coordinator changes were found.

## Finding dispositions

### IG2A-R01

CLOSED. Resealed CropBox, effective-crop intersection, MediaBox, rotation and UserUnit changes reject stale evidence without root; root validation rejects the changed actual-source geometry. Address swap rejects identity remapping. Replacing the evidence page-basis hash does not bypass source geometry checks. Fresh evidence and legacy reproduction baseline pass. No closure is inferred from a missing schema field.

### IG2A-R02

CLOSED. False 72-DPI metadata on actual 144-DPI evidence fails the DPI/geometry prediction; one-pixel forged rounding metadata fails. Eight fractional nonzero-origin partial-crop 72/144-DPI cases at all rotations pass exact rational dimension expectations and eight independently redrawn full-image pixel oracles at zero tolerance. Eight additional exact-integer pixel-boundary renders at UserUnit 1.1 pass. Poppler ceiling is explicit; PNG dimensions agree.

### IG2A-R03

CLOSED. Valid other-page evidence rejects a verified label on this page; correct same-page current evidence passes. Actual delivery labels 2/3/4 match current reviewer image observations and exact page/source/region evidence basis. Unknown cover and pages 5-44 remain unknown; embedded_unverified metadata remains unverified. Glyph and human authority claims are not authenticated by association checks.

### IG2A-R04

CLOSED within the sidecar author-scope contract. Changed author key, kind, uncertainty, registry, source identity/revision, page mapping, geometry partition, denominator role, reading order or link rejects the old boundary. Direct coverage report marks its author scope stale, source-IG freshness unknown and human authority unverified. The unchanged synthetic basis passes only those limited structural checks. Coverage-only rationale changes deliberately do not imply a current approved IG-1A whole-record exclusion. Frozen IG-1A tools/schema/README hashes remain unchanged.

### IG2A-R05

CLOSED. A two-page pinned source with consistently forged one-page claims rejects actual source-count mismatch. Swapped physical addresses under persisted identities reject remapping. Reordered page array passes; two official fresh inventories using persisted registry have identical canonical and serialized bytes and identities. Changed-PDF registry reuse refuses explicit remapping. Geometry/revision changes remain separate from UUID identity.

`dispositions.json` preserves each exact prior closure condition and links independent candidates. `retained-reproduction-results.json` has two passing migrated baselines and ten rejecting original adverse mutations; freshness diagnostics are not schema-only failures. Fresh derivations were written separately; original candidates/evidence were not modified.

## Exact acceptance criteria

**MET — Every PDF page and region is addressable with coordinate conventions and printed-label mapping.**

Root validation checks the byte-pinned PDF count/geometry and each physical identity, all pages remain addressable, current evidence pins exact normalized/native/displayed bases. Correct same-page label association passes, cross-page/stale association fails. Official repeatability and 12 exact image comparisons pass (eight synthetic and four official).

**MET — Text, images, uncertainty and reading order remain separate; duplicate context does not increase coverage.**

Separate UTF-8 text, PNG, uncertainty, Unicode offsets, explicit reading-order IDs and note/continuation links survive. The 71-test source suite includes multicolumn/table-note/cross-page cases and duplicate-context accounting. Independent overlapping-context passes without increasing denominator; inventory overlap, duplicates and missing order fail. Evidence DPI and geometry are cross-checked.

**MET — Unknown or excluded areas are visible; partial/gap is never represented.**

All 44 official placeholders are unprocessed with zero represented regions at every level. Missing actual PDF page cannot be concealed; uncovered area is explicit; partial retains gaps and cannot count as represented. Exclusions remain visible structural claims, stale author scopes reject, and source-IG review freshness/human authority remain unknown/unverified.

## Validation and expectation provenance

The explicit source suite passed **71 tests**, fresh short basetemp `t`, `-p no:cacheprovider`. The unchanged `scripts/check.ps1 -Task IG-2A` passed **102 project tests**, workflow validation, task dry-run and Git diff checks. Its output-only PowerShell adapter redirects just the generated operational directory into `c`; it executes the original script, preserves every validation, and records equal before/after script hashes. Required checks, exact commands, exits, stdout/stderr and elapsed times are retained in `required-checks.json`, `real-required-checks.json`, `final-checks.json` and individual command records.

There are **55** fresh independent boundary probes, **12** migrated retained cases, **8** fractional/nonzero-origin/all-rotation/72-or-144-DPI dimension probes, **8** full-image zero-tolerance pixel comparisons against an independently drawn physical oracle, and **8** exact-integer pixel-boundary renders at UserUnit 1.1. The eight dimension probes are included in the fresh probe count. The oracle builds its own zero-origin PDF from authored native coordinates; no WGC conversion/size/scaling helper supplies expected results. Dimensions use exact physical rationals and per-axis ceiling; interior color landmarks provide a separate rotation check. No one-pixel allowance was used for full-image agreement.

Independent pypdf and Poppler counts are both **44**. Two newly generated structural inventories using the persisted registry have identical canonical and serialized bytes and UUID mappings. Structural geometry for all 44 pages matches independent pypdf inspection; substantive content access was limited to physical pages 1–4. Four full-page derived PNGs agree pixel-for-pixel with direct original-PDF Poppler renders. The current reviewer viewed the fresh contact sheet and full page 3; labels 2/3/4 and visible layouts agree with the repaired verified inventory. Cover has no verified page label; pages 5–44 remain unknown. `visual-inspection.json` records observations only, without interpreting any game rules.

Actual dependencies: Python 3.12.14, pypdf 6.10.0, pdfplumber 0.11.9, Pillow 12.3.0, reportlab 4.4.9, pytest 9.1.1, Poppler 26.07.0. Reviewer captured Python and Poppler executable hashes before probes and confirmed them unchanged at the end. Poppler hashes independently match the repair's current bundle 26.1013.11914 and differ from the earlier bundle claims; matching version strings are not treated as binary identity. No installs or global changes occurred.

All substantive validation commands passed. `preflight-errors.json` retains the initial helper API-name error and absent unused jsonschema metadata query; both concerned reviewer setup, not product tests. Their actual failed command output remains available. One boundary-results filename collided with its wrapper command record: exact printed rows survived in captured stdout, were recovered into `independent-integer-pixel-boundaries.json`, and the producer output name was corrected without rerunning probes or changing expectations. Source pypdf Xref warnings and synthetic Poppler display-font configuration warnings remain in raw logs. The latter did not affect the rectangle-only pixel oracle, which compares exactly.

## Limits and coordinator action

`validate(document)` without a root only establishes internal consistency and reports source structure unverified. Root validation establishes the actual pinned source's count and geometry; self-consistent registry/evidence claims do not authenticate authors or derivation authority. A sidecar exclusion scope is coverage-independent to avoid circular hashes; it deliberately excludes coverage fields and page labels/evidence. A changed coverage rationale can therefore retain author-scope freshness while source-IG review freshness remains unknown. This never constitutes a current approved IG-1A whole-record exclusion. Later reconciliation must apply the unchanged full-record IG-1A target/inventory review contract and verify the real human statement independently.

All 44 pages remain substantive unprocessed placeholders. Full-profile source completeness, source meaning, semantic acceptance, compilation and executable readiness were not assessed. No IG-2B task was performed. Tokens, cost and operator time remain null.

Session UTC start `2026-10-14T10:44:43.646Z`; evidence-review end `2026-10-14T11:00:28.252594+00:00`; elapsed 944.607 seconds. `measurement.json` records these boundaries; the final seal separately records the later freeze end and total wall time. The initial helper failure's command-level UTC boundaries were not captured and remain null; its tool-reported elapsed time is retained.

Coordinator next action: verify this review's final seal/manifest and pinned delivery, then make the coordinator-owned technical acceptance decision through the repository workflow if justified. This reviewer performed no transition and grants no semantic decision. Stop here; IG-2B needs a separate operator/coordinator instruction.
