# Independent source inventory (wgc-inventory-1)

This lasting tooling implements physical source accounting and evidence locators.
The schema is `contracts/ig/regions.schema.json`; `inventory.validate` checks shapes,
canonical hashes, identity references, complete pages, geometry, coverage partitions,
reading order and evidence bytes. It reuses the frozen IG-1A integer-only canonical
JSON and offline schema evaluator without changing their bytes. This sidecar does
not create or approve source-IG semantic records. IG-2 reconciliation must bind these
exact locators to source-IG regions and preserve the frozen IG-1A review rules.

## Identity and revisions

A source has a logical source ID and exact PDF SHA256. A persisted registry assigns
UUIDs to explicit page and region keys. Page keys are physical page addresses within
one exact PDF revision; region keys are author-assigned and never derived from text,
coordinates, content hashes or array positions. Replaying the registry retains IDs;
reordering or editing a region changes its revision, not identity. Retired registry
entries remain available. Splits/merges require new explicit keys and a later lineage
decision. A new PDF SHA256 refuses automatic registry reuse: page correspondence must
be resolved explicitly, so inserting a page cannot silently transfer identity.

Revisions are SHA256 of WGC-C14N-1 bytes excluding only the enclosing `revision` field.
Nested records carry their own revisions. Inventory hashes include the persisted
registry and exact evidence references; timestamps/cost/runtime measurements are
operational sidecars. New output directories are mandatory; no overwrite or promotion.

## Page geometry and labels

`pdf_page` is 1-based physical order. Printed labels are independent: unknown has
null plus reason; embedded PageLabels is unverified metadata; verified requires a
separate exact evidence ID. Absence of PageLabels never implies the printed number.

MediaBox and CropBox serialize native bottom-left PDF coordinates in integer
micro-points. One native unit is UserUnit/72 inch. Effective CropBox is their positive
intersection. Reject nonpositive boxes/units and unsupported rotations. Canonical
region boxes are unrotated effective-CropBox top-left **integer page millionths**,
with x right, y down, and half-open bounds. Regions must fit this frame; no silent
clipping. `pdf_to_box` converts native PDF bounds with outward rounding; `box_to_pdf`
returns exact rational native bounds. UserUnit cancels in normalization and scales
physical dimensions. `display_box` applies clockwise /Rotate (0/90/180/270); displayed
dimensions swap at 90/270. No mixed text/box denominator conventions are inferred.

Evidence derives a separate PDF with MediaBox/CropBox set to the exact region and
UserUnit scaled into its content and geometry. It preserves page rotation. Poppler
renders that cropped page; pdfplumber clips extraction to the same displayed frame.
Text, PNG and cropped PDF each have repo-relative safe path, byte count and SHA256.
Text offsets use Unicode codepoints and half-open bounds in the exact UTF-8 file.
Text extraction order is not reading order. Empty text can be valid for a diagram;
its presence or absence never grants coverage. Evidence includes original source,
region revision, page, box, engines/versions, DPI and pixel dimensions. Uncertainty is
separate. Revisions, source or artifact changes invalidate the evidence locator.

## Order, links and coverage

An explicit global reading-order list names each region once. It can describe columns
and cross-page order; no top-to-bottom extraction heuristic approves it. Typed
`continuation`, `note_for` and `illustrates` links retain exact region IDs and a reason.
Links describe structure, not executable dependencies or accepted interpretations.

Inventory boxes on each page must be disjoint. Duplicate IDs/keys and overlaps fail.
Context boxes may overlap or duplicate geometry; they contribute zero denominator
units. Every page is present even when it has no regions, and uncovered geometric
area is reported in integer trillionths as an explicit gap. Complete geometric area
does not prove substantive inventory: an unprocessed full-page placeholder remains
unprocessed. IG-2B must replace these placeholders with its independently authored
regions. The denominator counts regions independently of KB headings; it is not a
percentage of rule meaning. All 44 official pages are structurally accounted for;
IG-2A checks extraction/rendering only on pinned pages 1-4.

Transcription, descriptive semantics and formal semantics have separate statuses.
`represented` forbids gap/reason. `partial`/`unprocessed` require a gap and reason.
`excluded` requires a reason and an exact source/region/box/level/partition boundary,
human-role authorization claim and decision artifact. `partition_hash` pins sorted
inventory identities and boxes without coverage, avoiding a circular hash. A changed
partition invalidates exclusions. Structural validation of those claims does not
authenticate a human or grant semantic acceptance; the coordinator must verify them.
Excluded regions remain visible and never count as represented.

## Local usage and dependencies

Use existing bundled pypdf, pdfplumber, Pillow and Poppler (pdfinfo, pdftoppm). No
network calls, installs or global configuration changes occur in these tools. Supply
the bundle's site-packages to the local interpreter using a process-only PYTHONPATH;
exact paths, library versions, executable hashes and rendering settings belong in
the operational report. Synthetic fixtures do not contain publisher text. The CLI
requires `private/` for publisher inputs and derived outputs.

```text
python -m wgc.sources inventory --pdf private/.../rulebook.pdf --provenance private/.../provenance.json --source-id source:spqr:5e:core --sha256 HASH --output private/.../new-run
python -m wgc.sources inventory ... --registry private/.../new-run/identity-registry.json --output private/.../replay
python -m wgc.sources evidence --inventory private/.../new-run/inventory.json --pages 1 2 3 4 --output private/.../evidence
python -m wgc.sources validate private/.../evidence/inventory.json
```

Run explicit `tests/sources` with a fresh short basetemp and `-p no:cacheprovider`.
Tests cover two columns, tables/notes, cross-page structure, missing pages, duplicates,
overlap/context, unknown labels, all rotations/nonzero box origins/UserUnit, artifact
tampering, partial/exclusion handling and registry replay. Full source meaning,
independent technical review and human semantic acceptance remain separate gates.
