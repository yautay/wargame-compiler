# Frozen IG-1A boundaries for IG-2B02

Full contract reference: contracts/ig/README.md; SHA256 c2d05b9cb20da646de21dc8b3f715799fae2006f06f322c7be800f0cb7e8db57. This exact excerpt and summary constrain the inventory sidecar; they do not alter the contract. Full README remains an explicitly named read-only reference.

Use integer-only WGC-C14N-1, UTF-8 without BOM, duplicate keys, floating-point/nonfinite values or surrogates. Canonical JSON sorts keys and retains array order and source string bytes. Persist explicit keys and UUIDs; reordering, content hashes, coordinates and filenames never allocate identity. Splits/merges require explicit lineage, new keys and decisions; no review transfer. The inventory contract reuses frozen tooling; edit no source contract or tool.

## Coverage, reviews and readiness

Snapshot assessments report four independent dimensions. Import complete is only an
input-accounting claim. Coverage is measured by transcription, descriptive semantics
and formal semantics; it does not imply either human acceptance or execution. Coverage
entries distinguish represented/partial/unprocessed/excluded. Partial and unprocessed
entries require gaps; represented entries require targets and cannot count a gap as
represented content. Coverage `target_refs` allow only `node`, `evidence` or `relation`
source-content records, in either reference mode. Gaps belong in `gap_refs`; sources,
regions and workflow/profile/review metadata are not content targets. A mixed list with
a gap is invalid too. This type check does not prove the representation's source meaning.

Exclusion requires a reason and a current complete human accepted `source_composition`
review. Its optional `coverage_boundary` object must specify `purpose: coverage_exclusion`
and exactly match the coverage entry's historical `inventory_ref`, historical `region_ref`
and representation `level`. Inventory pins in both coverage and boundary metadata use
`whole_historical_ref`: they cannot carry `aspect_id`. The matching inventory basis is
therefore a whole-record pin, and a different selected inventory revision makes the
exclusion decision stale even if every particular aspect is unchanged. This restriction
does not alter aspect-scoped targets or bases in ordinary reviews. That exact region
must be a full-record review target and
the exact inventory a full-record review basis. Other-region, other-level, unrelated,
stale or partial decisions cannot transfer approval. The decision targets the region
and inventory boundary rather than the coverage record containing its own reference,
so revision hashing remains acyclic. Authorization and decision artifacts still require
independent human verification; matching metadata does not authenticate them.
`inventory` regions define the denominator; `context` regions are excluded from it.
Duplicate or overlapping inventory regions within a level/source revision/page/locator
convention are rejected. Boxes use integer millionths of a page, top-left origin;
text intervals use Unicode codepoints, half-open bounds, and a pinned extracted-text
hash. Across box and text conventions no overlap equivalence is inferred; the inventory
author must use one convention per partition or independently justify a mixed partition.
Counts are region counts, not percentages or proof of complete rulebook representation.


No source-IG review or human approval is granted by this coordinator refinement. Import, coverage, human semantic acceptance and executable readiness remain separate. New inventory delivery needs fresh independent technical review and later exact whole-record reconciliation. No gameplay legality is resolved by an LLM.
