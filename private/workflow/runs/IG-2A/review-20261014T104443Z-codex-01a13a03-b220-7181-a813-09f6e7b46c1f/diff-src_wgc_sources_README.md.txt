--- verified-product-before/src/wgc/sources/README.md
+++ src/wgc/sources/README.md
@@ -12,7 +12,8 @@
 
 A source has a logical source ID and exact PDF SHA256. A persisted registry assigns
 UUIDs to explicit page and region keys. Page keys are physical page addresses within
-one exact PDF revision; region keys are author-assigned and never derived from text,
+one exact PDF revision, spelled `physical-page:<1-based number>`. Validation refuses
+another physical address under that key/UUID. Region keys are author-assigned and never derived from text,
 coordinates, content hashes or array positions. Replaying the registry retains IDs;
 reordering or editing a region changes its revision, not identity. Retired registry
 entries remain available. Splits/merges require new explicit keys and a later lineage
@@ -29,6 +30,8 @@
 `pdf_page` is 1-based physical order. Printed labels are independent: unknown has
 null plus reason; embedded PageLabels is unverified metadata; verified requires a
 separate exact evidence ID. Absence of PageLabels never implies the printed number.
+Verified label evidence must belong to that same physical page and remain current;
+checking that association does not verify the visible glyph or a human's identity.
 
 MediaBox and CropBox serialize native bottom-left PDF coordinates in integer
 micro-points. One native unit is UserUnit/72 inch. Effective CropBox is their positive
@@ -47,8 +50,25 @@
 Text offsets use Unicode codepoints and half-open bounds in the exact UTF-8 file.
 Text extraction order is not reading order. Empty text can be valid for a diagram;
 its presence or absence never grants coverage. Evidence includes original source,
-region revision, page, box, engines/versions, DPI and pixel dimensions. Uncertainty is
-separate. Revisions, source or artifact changes invalidate the evidence locator.
+region revision, page, box, engines/versions, DPI and pixel dimensions. Its required
+`page_basis_hash` pins page ID/key, physical address, source revision, both PDF boxes,
+effective crop, rotation and UserUnit, excluding mutable labels and evidence. This
+coverage-independent basis prevents circular hashes and invalidates stale geometry.
+The evidence identity includes that basis. Uncertainty is separate. Revisions, source
+or artifact changes invalidate the evidence locator. Existing evidence without the
+basis requires new derivation in a new output directory; do not invent a freshness pin.
+
+Poppler pixel dimensions use the ceiling of each displayed physical crop axis in
+points times DPI/72, evaluated at double precision. UserUnit scales both axes, and
+90/270 rotation swaps them. Validation checks this prediction against metadata and
+the actual PNG header, with no one-pixel tolerance. It never rounds to nearest.
+
+`validate(document, root)` reopens the byte-pinned PDF, compares strict pypdf and
+Poppler page counts, and verifies every physical page's actual geometry. Both counters
+inside edited JSON cannot conceal an omitted PDF page. It rechecks the PDF pin after
+validation. This is structural access only, with no text/image extraction. Validation
+without `root` checks internal consistency and reports source structure as unverified;
+it cannot substantiate a claim about actual source bytes.
 
 ## Order, links and coverage
 
@@ -70,11 +90,21 @@
 Transcription, descriptive semantics and formal semantics have separate statuses.
 `represented` forbids gap/reason. `partial`/`unprocessed` require a gap and reason.
 `excluded` requires a reason and an exact source/region/box/level/partition boundary,
-human-role authorization claim and decision artifact. `partition_hash` pins sorted
-inventory identities and boxes without coverage, avoiding a circular hash. A changed
-partition invalidates exclusions. Structural validation of those claims does not
+human-role authorization claim and decision artifact. `partition_hash` pins the exact
+source metadata, full registry, sorted page address/geometry bases, all regions' author
+fields (including classification, uncertainty, keys and denominator role), reading order
+and links. Region revisions/coverage and page labels/evidence are excluded to avoid
+circular decision/evidence hashes. A changed author or registry scope invalidates the
+old claim, even with unchanged rectangles. Structural validation of those claims does not
 authenticate a human or grant semantic acceptance; the coordinator must verify them.
 Excluded regions remain visible and never count as represented.
+
+This scope hash is a sidecar author basis, not the frozen IG-1A whole-record region and
+inventory review basis. Each reported exclusion keeps source-IG review freshness
+`unknown` and human authority `unverified`, even when its author scope matches. Later
+reconciliation must establish the exact whole-record targets/bases and independently
+authenticate the scoped human decision; this tool never reports a current approved
+source-IG exclusion or transfers semantic acceptance.
 
 ## Local usage and dependencies
 
