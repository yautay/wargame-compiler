# Source Instruction Graph contract, version 1

`source.schema.json` is the JSON Schema Draft 2020-12 shape for `wgc-source-1`.
The accompanying validator checks the additional invariants below. Both are required;
schema-only validation cannot check content hashes, selected references or freshness.
This is the lasting source layer of WGC's complete SPQR product. All public examples
are invented copper-token material, with no publisher text or SPQR rules.

## Bundle and records

A bundle contains `schema_version`, `snapshot_id` and an immutable `records` store.
Every record carries `id`, `record_type`, `schema_version`, `revision_id`,
`content_hash`, `run_id`, `supersedes_refs`, `lineage_refs` and typed `data`.
The store may contain several revisions of one identity. Duplicate `(id, revision_id)`
pairs and changes to an identity's record type are invalid. The named snapshot has
exactly one revision in the bundle. Its selected manifest pins one revision, type and
hash per identity. Snapshots cannot select other snapshots, including themselves.
`draft` and `sealed` describe structural selection; neither certifies source meaning.

| Record type | Addressable source content |
|---|---|
| `source` | Role, publisher, system, edition, language, part, media type, bytes, SHA-256, availability, compatibility and gaps |
| `region` | Exact source revision, 1-based PDF page, separate printed label, reading order and a precise box or text interval |
| `evidence` | Exact region revisions, direct/context/counterevidence role, literal text, separate normalization and uncertain symbols |
| `node` | Typed descriptions, stable aspects and explicit semantic groups; editorial parentage is separate |
| `relation` | Typed directed links, applicability, target status, raw locator, edition, candidates, evidence, gaps and all/any requirement groups |
| `gap` | Missing/unreadable/unprocessed/ambiguous/conflicting/unsupported content, affected targets, candidates and blocked operations |
| `origin_binding` | Many-to-many input snapshot/hash/path/field locators to IG identities/aspects, namespaced external IDs and mapping status |
| `coverage` | Inventory revision, exact region, representation level, status, targets/gaps and explicit denominator membership |
| `profile` | System, edition, rules mode, options, scenario, maps/counters, pinned materials and compatibility decisions |
| `run` | Proposal/context hashes, observed configuration and evidence, UTC timestamps, measured values or explicit unknowns, expectation basis |
| `review` | Exact target/aspect and basis revisions, scope, kind, actor/role, decision artifact, authorization, rationale and explicit supersession |
| `snapshot` | Selected revision manifest, profile, conflicts and independent import/coverage/review/execution assessments |
| `identity_registry` | Persisted origin keys and assigned IDs; ambiguous rematches retain candidates and a gap |

`run_id` names a run in the supplied store. The record hash includes this provenance.
The bundle is a closed structural validation unit: unavailable external records must
be represented by source availability/gaps and unresolved raw locators, not fabricated
resolved references. Origins name input snapshots by ID/hash without reading them.
No validator opens an origin path, source file, URL or decision artifact.

## Identity and revision rules

IDs are ASCII namespaced strings, at most 100 characters, matching the schema's ID
pattern; they are not paths. External IDs must be namespaced by their input KB.
An anonymous identity is allocated once, assigned a persisted `origin_key` in an
`identity_registry`, and reused after reorder or correction. Neither an array index,
content hash, title nor filename is an identity generator. Ambiguous rematches require
an `ambiguous` entry and a gap, not an automatic best match. Several origin keys may
bind to the same IG ID. Duplicate origin keys within a registry revision are invalid.

Within a node, `aspect_id` and `group_id` are stable local identifiers. Their full
address is `(node ID, aspect ID)` or `(node ID, group ID)`; record array order is irrelevant
to identity. Aspect IDs may remain stable when meaning changes, but hashes and review
freshness then change. Preserve unchanged aspect IDs across container revisions.
Tables similarly name axes, cells and notes; source coordinates name the participating
axis and its descriptive position. Note scopes and merged cells resolve
inside that table revision. Axes have distinct explicit orders. Cells identify their
participating axes; detailed formal coordinate/value-domain typing belongs to IG-3A.

`supersedes_refs` names earlier immutable revisions of the same identity/type.
`lineage_refs` preserves exact origins when splitting or merging records with other IDs;
new IDs, aspects and groups receive their own decisions. Lineage never transfers
acceptance. Do not rewrite old revisions to make a new decision appear current.

The optional storage helper uses `id-<lowercase hex of UTF-8 ID>.json`. This is injective,
Windows-safe, case-sensitive in its encoded identity, and under the filename length
limit for allowed IDs. Literal colon-bearing IDs must never be used as Windows paths.

## WGC-C14N-1 canonical bytes

This is a specified WGC profile, not a claim to implement RFC 8785. Input is UTF-8 JSON
without BOM, duplicate object keys, floating-point/nonfinite numbers or Unicode
surrogates. Booleans are distinct from integers. Quantities use integer amounts and
explicit units; fractional quantities use a signed integer numerator and positive
integer denominator, with an explicit unit. Fractions are not automatically reduced:
different source spellings remain different content.

Canonicalization recursively sorts object keys by Unicode scalar value, keeps arrays
in their supplied order, emits Unicode directly as UTF-8 and uses only `,` and `:`
separators with no insignificant spaces or trailing newline. Strings retain their
original scalar sequence: no NFC conversion, trimming, line-ending normalization or
source transcription repair. Quote, backslash and control escaping follows Python
`json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(',', ':'))` under this
integer/scalar-only profile. The fixed byte/hash vectors in `tests/contracts/test_source.py`
provide a portable oracle. Original source bytes are separately pinned by SHA-256;
canonicalization never rewrites those bytes.

`content_hash = SHA-256(canonical(record minus revision_id and content_hash))`, lowercase
hex. All other fields, including schema version, ID, run, lineage, references, review
metadata and data, participate. `revision_id = 'sha256:' + content_hash`. An aspect hash
uses the same canonicalization over the aspect minus only `aspect_hash`. Changing a
statement, facet, scope, evidence or execution annotation changes its hash. Whitespace
outside JSON strings does not change a content hash; reordering an ordered array does.
Reordering the bundle's record store does not change any record identity or revision.

The library's `seal_record` returns a copy with these hashes. It performs no acceptance,
validation, storage write, snapshot promotion or inference.

## Reference resolution

Each reference has `mode`, `id`, declared `record_type` and optionally `aspect_id`.
`active` references have no revision field and resolve only through the selected
snapshot. `historical` references require an exact `revision_id` and resolve only in
the immutable store. Reference types and aspect membership must match. Old records in
the store never satisfy a missing active reference. Conversely a historical review,
supersession or mention may legitimately target an unselected revision.

All historical references, including those in unselected revisions, must resolve.
Active references inside an unselected revision belonged to its original snapshot:
they are not activated or resolved against the current selection. Local shape/hash,
aspect/group/table, field-reference type and path invariants still apply to old records.
To validate their old active dependency closure, supply their original snapshot as a
separate bundle. This permits historical retention without silently substituting new
targets into old rules. Exact historical pins provide acyclic hashing; active ID edges
allow procedure graph cycles without recursive revision hashes.

`mention` is navigation. `procedure_use`, `table_use`, `definition` and `condition` are
dependencies. `exception` and `modifies` point from modifying rule to base rule;
`applies_to` from clause to scope; `illustrates` from example to rule; `precedes` from
earlier to later step. Mechanical links retain reads/writes, event triggers, scheduled
windows, reaction resumes, constraints and persistent bindings. Neither a link name nor
an editorial parent implements its behavior. Unresolved/ambiguous/unsupported targets
have null `target_ref`, raw locator, edition and gaps; candidate references identify
known stored candidates. Required and conditional links never treat unknown applicability
as false. Cycles are valid source descriptions and cannot certify termination.

## Knowledge, aspects and source mechanics

Each descriptive statement explicitly specifies knowledge, representation, value,
reason, gap references, evidence references and scope references. `known` is an
evidenced proposal with a non-null typed value, not acceptance. `established_absent`
has null value and requires evidence, reason and explicit scope. `unknown` has null
value, reason and at least one gap. `not_applicable` has null value and a reason for
the scope exclusion. Missing fields, empty lists and zero measurements prove no absence.
Literal, normalized and interpreted statements remain distinct.

Values distinguish text, symbol with legend references, integer quantity, rational,
reference and opaque text with an execution limitation. Facets distinguish condition,
effect, exception, timing, parameter, permission, obligation, prohibition, trigger,
cost, choice, calculation, transition, duration, aggregation, visibility and victory,
as well as transcription, scope and definition. Groups explicitly bind correctly typed
condition/effect/exception/timing aspect IDs with all/any/sequence composition. A common
subject does not implicitly combine its aspects. Group effects cannot be empty.

Every normative aspect declares `formal`, `informational` or `blocking` execution impact.
`formal` is a source-side classification to be formalized later, not compiled behavior.
Opaque or unknown normative aspects require `blocking`. An informational normative aspect needs
a current, complete human accepted review of that exact stable aspect and a recorded rationale. The
validator checks the metadata, but does not authenticate the human statement or establish
that information cannot affect gameplay. Such authority and source interpretation remain
separate human review obligations.

Node descriptions have explicit fields, each addressable by node ID and field name:

| Concepts | Dedicated source fields include |
|---|---|
| State/resources | Value type, unit, owner, bounds, reset, pool composition |
| Causal events/history | Cause filter, attempt/commit/invalidation, read moment, ordered writes, limits/reset window, positions, first occurrence, attempts, counters, participants, paid costs |
| Parameters/actions/procedures | Value type, domain, units/comparisons/bounds, actor, guard, inputs/outputs, branches, loops, termination, failure, windows |
| Persistent choices | Owner, selection mode, selector, cardinality, constraints, binding ID, lifetime, reselection and eligible/selected/committed/participating/affected sets |
| Timing/reactions/continuations | Instance hierarchy, opening/closing, priorities/ties, eligible player, attempt limit, resume/replace/cancel/restart, surviving effects/costs/history, invocation frame, environment, return point |
| Costs/durations | Attempt versus success, payer/resource/amount, checkpoint, pay-once key, cancellation survival, start/expiry/refresh and snapshot reads |
| Geometry/spatial policies | Map/sheet/hex, occupied hexes, anchor/orientation, zones/pivot, terrain/elevation/infrastructure, off-map/stack constraints, metric, endpoints, admissible nodes/edges, cost, path quantifier, optimality/tied selection |
| Calculations/aggregation/loss | Ordered operations, units/comparisons, rounding stage/method/beneficiary, modifiers/stacking, set/filter/measure/operator, allocation owner/proportions/overflow/elimination timing |
| Tables/outcomes | Ordered axes, boundaries/units, addressed cells, merged cells, scoped notes, missing/out-of-range policy, decorations/legend, participant bindings, original symbols and ordered conditional effects |
| Chance | Physical symbols/meaning, draw count, combination, independence, replacement, multiplicities/instances, raw/modified results, draw identity, rerolls and sharing |
| Visibility/victory | State and domains, rejected choices, reasons/proofs/gaps/IDs/cursors/caches, legal attempts/reveal checkpoint, metric/set/checkpoint/comparison/termination/ties/control history |

These fields preserve source descriptions and their uncertainties. They are not a
generic payload escape hatch or a universal game expression language. No rule legality,
state transition, arithmetic, randomness or player observation is evaluated here.

## Coverage, reviews and readiness

Snapshot assessments report four independent dimensions. Import complete is only an
input-accounting claim. Coverage is measured by transcription, descriptive semantics
and formal semantics; it does not imply either human acceptance or execution. Coverage
entries distinguish represented/partial/unprocessed/excluded. Partial and unprocessed
entries require gaps; represented entries require targets and cannot count a gap as
represented content. Exclusion requires a reason and a human accepted scope decision.
`inventory` regions define the denominator; `context` regions are excluded from it.
Duplicate or overlapping inventory regions within a level/source revision/page/locator
convention are rejected. Boxes use integer millionths of a page, top-left origin;
text intervals use Unicode codepoints, half-open bounds, and a pinned extracted-text
hash. Across box and text conventions no overlap equivalence is inferred; the inventory
author must use one convention per partition or independently justify a mixed partition.
Counts are region counts, not percentages or proof of complete rulebook representation.

Reviews distinguish transcription, interpretation, source composition, situation outcomes
and technical observations. Only a declared human_owner or human_reviewer with authorization
and a decision artifact may record `accepted`. A model or validator may record observations
or rejection. Structural checks do not authenticate identities, authority, artifacts or
source meanings. Dates do not override contradictory decisions; preserve both and use
explicit review supersession plus rationale. There is no automatic effective acceptance
aggregation in this increment.

For selected reviews, freshness is independently computed from exact targets and bases.
Changed/missing selected bases or changed target aspect hashes yield `stale`. Aspect-scoped
targets compare that aspect, so a change to an unrelated aspect need not invalidate them;
whole-record bases compare exact revisions. An unchanged but partial/unknown basis yields
`unknown`; only a declared complete, nonempty, unchanged basis yields `current`. Completeness
itself is a review claim; the validator cannot prove that all semantic dependencies were listed.
Partial acceptance remains bounded by explicit targets and scope; it does not accept siblings.

The source schema allows executable `unassessed` or `blocked`, never `ready`. The validator
reports selected opaque/unknown/blocking nodes, unresolved required/conditional links
and execution gaps as blockers and always returns
`semantic_acceptance_granted: false`. It neither grants a gameplay release nor asks an LLM
to resolve opacity. Executable readiness belongs to later formalization, authorized meaning
review, dependency closure, state/history requirements, compilation and independent runtime
evidence. An opaque source record can pass this contract while its dependent scope remains
blocked for execution.

## Local validation and tests

No dependency installation or network is required. From the repository root:

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m wgc.contracts.source tests/contracts/fixtures/valid-source.json
.\.venv\Scripts\python.exe -m pytest tests/contracts -q -p no:cacheprovider --basetemp private/workflow/checks/contract-review-new
pwsh -NoProfile -File scripts/check.ps1
git diff --check
```

Choose a fresh `--basetemp` path for each check. CLI exit 0 means structural validity,
including hash/reference invariants; invalid input or unreadable files exit 1 with an
error. The standard project suite includes `tests/contracts`. The offline evaluator is
explicitly limited to the bundled schema's keyword subset and rejects unknown keywords;
it is not a general-purpose JSON Schema implementation. It opens no schema URLs.

`tests/contracts/fixtures/catalog.json` records each independently specified oracle and
its architectural basis. Static cases cover unknown units, changed aspect integrity and
freshness, dependency regression, model approval, active/historical dangling references,
duplicate identities, opaque blockers, group composition, table notes, edition conflicts,
procedure cycles and scoped review. Additional tests use fixed canonical bytes/hashes,
strict JSON, reordered records, mechanism field expectations and CLI status. The synthetic
accepted metadata in fixtures grants no real semantic acceptance.

## Open formal-language decisions for IG-3A

IG-3A must choose the actual value/domain/expression type system, exact operators and
unit conversions; ordered event writes, transactional boundaries and causal history;
invocation bindings, loops/termination, reaction scheduling and cancellation survival;
table coordinates/lookups/decoding/modifier order; geometry/path/stack algorithms;
chance distributions, multiplicities and authoritative draws; visibility-safe complete
observations and legal attempts; and profile/dependency closure/readiness queries.
It must also pin how external formal contracts and reports attach to these source IDs,
and how changed dependencies invalidate acceptance and compiled packages. Nothing in
this source contract selects universal precedence, a reaction queue, a rollback policy,
a randomizer distribution or an execution algorithm.
