# IG-2A independent technical review

**Outcome: CHANGES_REQUESTED.** Five findings: three P1 and two P2. The frozen bytes are intact and ordinary tests pass, but edited inventories can retain invalid source/evidence/exclusion associations. No repair, technical acceptance, semantic acceptance or queue transition was performed.

Reviewer: `codex-01a1363e-1de5-7073-8185-d9a1f2e89c35`. Executor: `codex-01a135f6-cdab-7723-bd6a-9e0044d12323`. Actual current-session GPT-6.1 Sol / high was confirmed directly by the operator replying "potwierdzam" to the current-session configuration question. Thread identity comes from process CODEX_THREAD_ID; no previous-session configuration was reused.

## Frozen scope and integrity

All 87 delivery artifacts were independently rehashed before review and again before freeze: zero mismatches. The specified delivery JSON, manifest and handoff hashes match. The authoritative queue remains review with identical bytes. The fresh packet was generated through the unchanged workflow.packet(output=False), verified against the current queue/allowlist and serialized here. The old executor packet context was read and its hash verified; its older queue hash is expected. See reviewed-artifact-manifest.json, packet-verification.json and preservation-final.json.

Review examined all files under the explicitly delivered src/wgc/sources and tests/sources, regions.schema.json, refinement, acquisition and the exact inventory/evidence artifacts. The frozen IG-1A source schema, validator and README remain byte-identical to recorded dependency pins. The new sidecar reuses WGC-C14N-1 and does not emit accepted source-IG semantics. Its exclusion freshness must still preserve the frozen full-region/inventory review boundary; structural actor-role claims cannot authenticate a human.

## Independent positive evidence

The original official PDF is 3,965,827 bytes with SHA256 e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e. Strict pypdf and independent Poppler each counted 44 pages. Saved referring HTML/link, acquisition times, HTTP lengths/hash, redirects, edition evidence and original bytes are internally consistent; no network request or source rewrite occurred. Saved HTTP evidence is provenance, not an independent authentication of a live network origin. Publication date and identity to the unavailable WGU original remain unknown.

Two newly built complete structural inventories reused the persisted registry and produced identical canonical inventory bytes, also identical to the frozen seed. Region identity remains separate from content revision; changed source SHA/registry mismatches are refused. Structural metadata for all 44 pages matches the actual PDF. All frozen placeholders count as unprocessed (44) and represented (0) at every level. Geometrically complete placeholders never establish substantive coverage.

Reviewer inspected independently rendered physical pages 1-4. Original-PDF PNGs are pixel-identical to the frozen derived evidence. Cover visibly says 5th Edition and has no verified printed page label; labels 2, 3 and 4 are visible at top-left, top-right and top-left respectively. Two columns and graphics are present without observed clipping. Original/derived crop geometry matches. Four additional synthetic asymmetric red-region crops with nonzero MediaBox/CropBox origins, fractional UserUnit 3/2 and rotations 0/90/180/270 match independently calculated pixel sizes and rotated red bounding boxes; outside text is absent. Pages 5-44 had geometry-only access; no content analysis or substantive inventory was performed.

The non-zero-indexed Xref warning was reproduced and retained in pypdf-warnings.log. pypdf corrects object IDs in memory. Original bytes were not repaired. Independent Poppler structure/count and four pixel comparisons corroborate the inspected scope; they do not establish uninspected source meaning.

## Validation results

- Explicit tests/sources: 39 passed; exit 0, fresh reviewer t basetemp, -p no:cacheprovider.
- Unchanged scripts/check.ps1 -Task IG-2A, through the documented process-local output adapter: 102 passed; exit 0. The adapter redirects only operational log/temp destination into reviewer c; check source and validation logic were not edited.
- workflow validate and git diff --check: exit 0, including final checks.
- Independent boundary probes: 28 records; 10 expected rejection boundaries failed, grouped into five findings below. Child probe exit 1 intentionally reports detected defects; runner exit 0 is orchestration completion, not a passing probe result.
- Exact commands, exits, output streams and measured subprocess clocks are in checks.json and individual check JSON files. Extra unsafe Windows path aliases were rejected. Frozen bundled library versions and executable hashes match toolchain.json. No installs or global environment changes occurred.

Ordinary tests exercise malformed hashes/paths/count disagreement, region edits, geometry conversions, context overlaps, typed links and output immutability. The independent probes additionally reseal edited metadata correctly; these are valid candidate revisions with stale derivation/decision bases, not malformed JSON/hash fixtures. Review does not use an LLM to decide gameplay legality.

## Findings

### IG2A-R01 [P1] Evidence stays current after the page coordinate basis changes

Location: src/wgc/sources/inventory.py:182-187, contracts/ig/regions.schema.json /$defs/evidence, src/wgc/sources/pdf.py:74-85.

Reproduction: Reseal page 1 after changing /Rotate to 90, UserUnit from 1 to 2, or CropBox/effective CropBox x0 to 10 native points. Leave the region revision, evidence locators and artifact bytes unchanged. validate(document, root) accepts all three.

Consequence: Normalized box coordinates depend on page geometry and units. Old text/PNG/derived-PDF files are accepted as current evidence for a different native/displayed crop. Page hashes are checked only against themselves, and evidence has no pinned page-geometry revision.

Required change: Bind the evidence derivation to a non-circular exact page geometry/physical-page basis and verify it against the pinned PDF when claiming source-grounded validity. Reject stale geometry even when page/document hashes were correctly recomputed. Preserve explicit author region identity across legitimate revisions.

Repair verification: On a clean valid migrated baseline, change CropBox, effective crop, rotation and UserUnit independently, reseal the page/container and retain old evidence. Each must fail with a freshness/source-basis error; fresh evidence for an unchanged actual source basis must pass. Keep all four independent asymmetric pixel/rotation/UserUnit oracles passing.

Exact candidate JSONs and hashes: see this finding in findings.json and p2/probe-results.json. CLI reproduction from the repository root is `.venv/Scripts/python.exe -m wgc.sources validate private/workflow/runs/IG-2A/review-20261013T171051Z-codex-01a1363e-1de5-7073-8185-d9a1f2e89c35/p2/stale_page_rotation.input.json` with the frozen process PYTHONPATH from toolchain.json; current code accepts (exit 0). Running probes.py again requires a new subdirectory argument to preserve existing outputs.

### IG2A-R02 [P2] DPI metadata is not checked against crop geometry and image dimensions

Location: src/wgc/sources/inventory.py:198-200.

Reproduction: Change the first evidence render_parameters.dpi from 144 to 72, preserving its 400 by 600 PNG, source geometry, file pins and all other settings; reseal the container. validate(document, root) accepts it.

Consequence: The documented render settings can describe an impossible render. Width/height are compared only to the PNG header, so the recorded DPI does not substantiate accurate coordinate/pixel evidence.

Required change: Cross-check DPI, normalized crop physical dimensions, UserUnit, rotation and render dimensions with an explicit Poppler rounding convention. Do not authenticate arbitrary settings solely from their presence in the schema.

Repair verification: The retained false_render_dpi input must fail for inconsistent rendering metadata, while actual 72/144-DPI evidence for nonzero origins, fractional UserUnit and all rotations passes with independently calculated pixel dimensions.

Exact candidate JSONs and hashes: see this finding in findings.json and p2/probe-results.json. CLI reproduction from the repository root is `.venv/Scripts/python.exe -m wgc.sources validate private/workflow/runs/IG-2A/review-20261013T171051Z-codex-01a1363e-1de5-7073-8185-d9a1f2e89c35/p2/false_render_dpi.input.json` with the frozen process PYTHONPATH from toolchain.json; current code accepts (exit 0). Running probes.py again requires a new subdirectory argument to preserve existing outputs.

### IG2A-R03 [P2] A verified printed label can cite evidence from another page

Location: src/wgc/sources/inventory.py:203-204.

Reproduction: Set page 1 label to verified value 2 and cite the exact evidence ID for page 2. Reseal the page and document. The referenced evidence exists, so validation accepts the wrong-page association.

Consequence: The printed-label mapping is not technically bound to its physical page. A downstream locator can appear visually verified using an unrelated page image; ID existence alone is insufficient.

Required change: Require the label evidence to resolve to the same physical page/source and a current geometry/region basis. Verifying the visible glyph remains a reviewer observation, separate from structural association.

Repair verification: Cross-page evidence must be rejected even if the evidence itself is valid. Same-page current evidence must pass. Preserve unknown cover labels and embedded_unverified PageLabels without promoting metadata to visual verification.

Exact candidate JSONs and hashes: see this finding in findings.json and p2/probe-results.json. CLI reproduction from the repository root is `.venv/Scripts/python.exe -m wgc.sources validate private/workflow/runs/IG-2A/review-20261013T171051Z-codex-01a1363e-1de5-7073-8185-d9a1f2e89c35/p2/wrong_page_printed_label.input.json` with the frozen process PYTHONPATH from toolchain.json; current code accepts (exit 0). Running probes.py again requires a new subdirectory argument to preserve existing outputs.

### IG2A-R04 [P1] Exclusion freshness omits the author region and registry basis

Location: src/wgc/sources/inventory.py:105-110, src/wgc/sources/inventory.py:166-170, contracts/ig/README.md:193-205.

Reproduction: Start with the passing synthetic exact exclusion. Keep its decision bytes, box and boundary unchanged; change the region kind/uncertainty and reseal it, or change its author key and corresponding registry entry while retaining the UUID. The same exclusion remains valid. Physical-page remapping is also absent from the partition basis (see R05).

Consequence: partition_hash covers only source SHA and inventory region IDs/page IDs/boxes. It cannot invalidate a decision after author/registry scope revisions. The frozen IG-1A exclusion contract requires an exact current whole-region and inventory basis; this sidecar must not transfer a prior scope decision into a changed basis merely because its rectangles are unchanged.

Required change: Pin an exact, coverage-independent author/registry/page/partition decision basis that avoids circular coverage hashing, or explicitly report the decision freshness as unknown/stale until reconciliation establishes the required IG-1A basis. Keep technical claim validation separate from human authority/decision authentication; do not invent acceptance.

Repair verification: Change region key, classification, uncertainty, registry scope, source and physical-page mapping separately after a valid exclusion. Old decision basis must become stale/unknown or fail and must not be reported as a current approved exclusion. Unchanged exact basis and separately authentic human evidence can retain their limited scope. The current partition-change rejection must continue to pass.

Exact candidate JSONs and hashes: see this finding in findings.json and p2/probe-results.json. CLI reproduction from the repository root is `.venv/Scripts/python.exe -m wgc.sources validate private/workflow/runs/IG-2A/review-20261013T171051Z-codex-01a1363e-1de5-7073-8185-d9a1f2e89c35/p2/exclusion_after_region_revision.input.json` with the frozen process PYTHONPATH from toolchain.json; current code accepts (exit 0). Running probes.py again requires a new subdirectory argument to preserve existing outputs.

### IG2A-R05 [P1] Root validation can accept omitted PDF pages and physical identity remapping

Location: src/wgc/sources/inventory.py:127-148.

Reproduction: For the unchanged pinned two-page synthetic PDF, set page_count and both named independent count records to 1, retain only page/region/order entry 1, and remove evidence; reseal. Root validation accepts a one-page inventory. Independently, swap pdf_page numbers 1 and 2 while retaining physical-page author keys, IDs and registry and removing evidence; validation also accepts.

Consequence: The counter claims are compared to each other, not the byte-pinned source, and physical identity keys are not bound to immutable physical addresses. A missing real page becomes invisible and persisted IDs silently move to another page without any explicit mapping decision. The frozen 44-page delivery is correct, but the validator is insufficient for downstream edited inventories.

Required change: Use an exact independently verified source-structure basis for page count and page addresses. Validate author-key/registry physical-page bindings against that basis and reject silent remapping. Keep changed-PDF SHA registry reuse refusal intact.

Repair verification: With a two-page byte-pinned PDF, consistent forged one-page counters must fail with actual missing-page/source-basis diagnostics. Swapping physical addresses under the same persisted IDs must fail. Reordering the pages array without changing physical addresses and two fresh registry replays must pass.

Exact candidate JSONs and hashes: see this finding in findings.json and p2/probe-results.json. CLI reproduction from the repository root is `.venv/Scripts/python.exe -m wgc.sources validate private/workflow/runs/IG-2A/review-20261013T171051Z-codex-01a1363e-1de5-7073-8185-d9a1f2e89c35/p2/false_consistent_page_count.input.json` with the frozen process PYTHONPATH from toolchain.json; current code accepts (exit 0). Running probes.py again requires a new subdirectory argument to preserve existing outputs.

## Criterion decisions

- **NOT_MET** — Every PDF page and region is addressable with coordinate conventions and printed-label mapping. Frozen delivery independently has 44 physical pages, distinct labels and correct geometry; genuine conversion/render oracles pass. General source-address and label freshness validation remains bypassable.
- **NOT_MET** — Text, images, uncertainty and reading order remain separate; duplicate context does not increase coverage. Text/image/uncertainty/order fields are separate; notes/continuation/order checks and duplicate/context denominator probes pass. Source/evidence rendering metadata can nevertheless become inconsistent without rejection.
- **NOT_MET** — Unknown or excluded areas are visible; partial/gap is never represented. All frozen placeholders remain unprocessed, represented counts are zero at all three levels, partial retains gaps, missing-region area is visible and changed rectangle partitions reject old exclusions. Omitted actual pages and stale author/registry exclusion bases remain accepted.

## Measurement, limitations and coordinator handoff

Measured UTC interval: 2026-10-13T17:10:51.773356+00:00 to 2026-10-13T17:21:17.129954+00:00; 625.356598 seconds. This begins at the first captured UTC timestamp; earlier preliminary reads are unmeasured and are explicitly null. checkpoint.json had an unverified earlier start literal, superseded by configuration.json, preflight-observations.json and measurement.json. Token totals, cost and operator time are null. No monetary or token estimates are substituted.

This is a technical rejection of the tooling increment. It does not execute substantive IG-2B inventory or grant human semantic acceptance. No human exclusion authority was authenticated: synthetic decision claims are deliberate fixtures. Source meaning, source-IG reconciliation, compilation and executable readiness remain separate gates.

Coordinator next action: assess the five findings and record changes_requested with the frozen review evidence if accepted as a technical decision; prepare bounded executor repair scope, preserving the original delivery. Repair only in a separately authorized executor attempt, rerun the changed risks and obtain fresh independent review of new hashes. Do not accept/done IG-2A or execute IG-2B from this review.

All reviewer evidence is inside this new directory. Existing changes and all 87 frozen executor artifacts remain intact. No reset, clean, stash, commit, push, archive/Git-history access, adjacent repository writes, new chat, agent, automation or external API occurred.
