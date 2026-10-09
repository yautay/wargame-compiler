# proposal-format-v1

Small experimental JSON format, not a final rule language or a legacy contract.
Produce one UTF-8 JSON object. All extracted content is an unreviewed proposal.
Use strings for prose in the source language; JSON keys use the names below.
The separate `synthetic-example-v1.json` is fictional and has no SPQR content.

## Envelope

Required keys: `format_version` = `proposal-format-v1`, `run_id` = `first-001`,
`input_manifest_sha256` (SHA-256 of the actual manifest bytes), `evaluation_id`
(metadata ID only), `scope`, `provenance`, `sources`, `evidence`, `nodes`, `rules`,
`dependencies`, `gaps`, and `coverage`.

`scope` identifies source ID/hash, one-based physical PDF pages, core boundaries,
and supplied boundary context. `provenance` records actual application/model/
reasoning when available, their source, and whether assessment content was seen.
Unknown metadata is the literal string `unknown`, never a guessed selector.
`sources` lists source IDs and full SHA-256 hashes from the input manifest;
the synthetic example may embed its fictional source text instead.

## Values and absence

For every semantic field below use a Field object:
`{"state":"known|established_absent|unknown|not_applicable", "value":..., "evidence_ids":[], "reason":..., "gap_ids":[]}`.

- `known`: value is supported by cited evidence (lists can contain structured items).
- `established_absent`: evidence positively supports absence within the identified
  clause, e.g. no exception stated in that clause. `value` is an empty list or null.
  This does not establish absence from the whole game or an external procedure.
- `unknown`: `value` is null, with reason and at least one explicit gap ID.
- `not_applicable`: `value` is null and reason explains why the field does not apply.

No bare empty arrays may stand for unknown semantic information. A top-level
record collection may be empty only if `coverage` explains that no supported
records were found, or gaps declare the part unread/unrepresented.
Parameter items have `name`, `value`, `unit` (a Field), and `evidence_ids`.
Preserve numbers, operators, units, negations, exceptions, and time exactly;
an interpretation must not silently change the transcription.

## Evidence and source objects

Each evidence record has unique `id`, `source_id`, `source_sha256`, `pdf_page`
(one-based), `printed_page` (string or `unknown`), `region_id`, `kind`
(`text`, `table`, `diagram`, or `mixed`), `quote` (Field), and `image`.
Text quote is a short exact source transcription; uncertain text uses an
unknown Field and a gap. Typographic normalization must be stated separately.
`image` is null for purely textual synthetic evidence; real graphic evidence
requires `path`, `sha256`, `bbox`, and `coordinate_system`. Use full-page image
coordinates: top-left origin, x right, y down, pixels, [x0,y0,x1,y1]; state
image width and height. PDF coordinates in scope.json use top-left PDF points.
Do not mix crop-local pixels, page pixels, or PDF points. A graphic-only value
can be known from its image even if the helper text does not contain it.

`nodes` are local targets with unique `id`, `kind` (`table`, `diagram`,
`definition`, `procedure`, `fragment`, `external_candidate`, or `other`),
`original_label` (Field), `scope_role` (`core` or `boundary_context`),
`content` (Field), `evidence_ids`, and `review_status` = `unreviewed`.
Use nodes to preserve table headers, rows, footnotes, diagram labels/captions
and distinctions between transcription and interpretation. A target mentioned
but unavailable must have unknown content and a gap, never invented steps.
Boundary-context nodes are evidence targets, not core rule coverage.

## Rule records

Each rule has unique local `id`, `original_label` (Field), `scope_role` = `core`,
`clause_map`, `transcription` (Field), `interpretation` (Field), `conditions`
(Field), `action_effect` (Field), `exceptions` (Field), `parameters` (Field),
`unit_types` (Field), `scope_limits` (Field), `time_limits` (Field),
`evidence_ids`, `gap_ids`, and `review_status` = `unreviewed`.

`clause_map` is a nonempty list of {`local_clause_id`, `region_id`,
`evidence_ids`, `original_label_text`}. Local clause IDs are unique across the
output. Preserve the original printed labels; do not repair numbering from
memory. One label may have several rule/clause records; continuations may use
several regions for one rule. Explain splits/overlaps, never count duplicate
representations as extra completeness. Notes and introductions with rule
content retain their source kind in coverage, without invented rule numbers.
Prose interpretation and literal transcription remain separate fields.

## Dependency records and direction

Each dependency has `id`, `from` (rule/node ID), `to` (existing rule/node ID
or null), `target_candidate` (null or {`original_reference`, `description`,
`needed_context`}), `kind`, `explicitness` (`explicit` or `implicit`),
`rationale`, `evidence_ids`, `target_status`, `impact_if_missing`, `gap_ids`,
and `review_status` = `unreviewed`.

Kinds: `procedure_use`, `table_use`, `definition`, `condition`, `modification`,
`exception`, `continuation`, `mention`.
`from` uses/refers to the target; `to` is the used procedure/table/definition
or modified/general rule. Continuation points from earlier fragment to later
fragment. Explain the direction. Implicit relations need source evidence of
necessity; similar words alone do not support an edge. A `mention` is not an
execution dependency. Keep mentions and physical continuations distinguishable.
`target_status`: `internal`, `external_with_source`, `unresolved`, `unsupported`.
`external_with_source` requires evidence from actually supplied context;
a bare numerical reference is `unresolved`, not a verified external target.
For null `to`, a candidate and a gap are required. Do not duplicate the same
source/target/kind relation to increase counts. Multiple facets need explanations.
`impact_if_missing` states affected IDs, what cannot be resolved, and whether
the missing information blocks a full result; do not invent evaluation situations.

## Gaps and coverage

Each gap has unique `id`, `class` (`unreadable`, `missing_context`,
`ambiguous_source`, `unsupported_interpretation`, `unprocessed`, or `other`),
`affected_ids`, `source_regions`, `reason`, `needed_context`, `blocking`, and
`evidence_ids`. Unsupported interpretations remain gaps, not source facts.

`coverage` has an entry per core region in source reading order:
{`region_id`, `status` (`represented`, `partial`, `unprocessed`), `rule_ids`,
`node_ids`, `dependency_ids`, `gap_ids`, `notes`}.
Also list source labels/notes/tables/diagrams observed and their mappings; a
source object's kind is not inferred from an evaluation key. Context-only
regions are listed separately and excluded from core representation counts.
Represented means mapped by this proposal, not semantically accepted.
If output size or readability prevents completion, report partial coverage and
unprocessed regions explicitly. Do not claim a perfect extraction or calculate
quality against unseen answers.

## Mechanical checks before returning

JSON parses; IDs are unique; references resolve or have explicit candidates;
source/image hashes match supplied files; all core regions have coverage;
uncertain values are unknown with gaps; text and graphic evidence is locatable.
These checks do not accept the meaning of the rules or the graph.
