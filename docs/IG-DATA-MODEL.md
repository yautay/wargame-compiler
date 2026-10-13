# IG data contract proposal

This document consolidates the earlier `ig-draft-0.2` design. It is not a machine schema
or accepted game semantics. IG-1A establishes the source contract; IG-3A establishes
the executable language after source reconciliation. See [architecture](IG-WGU-ARCHITECTURE.md).

## Identity and record envelope

Each record has stable `id`, `record_type`, `schema_version`, `revision_id`, `run_id`,
`supersedes_refs`, and canonical content hash. Stable identity is separate from revision,
file path, array position and content hash. External WGU IDs are namespaced by KB.
`origin_bindings` link many-to-many IG IDs to input snapshot/file/field locators.
Anonymous terms and relations use a persisted identity registry; ambiguous rematches
become conflicts. Split/merge lineage does not transfer acceptance automatically.

References used as active rules resolve only in the selected snapshot. Historical
review and supersession references resolve in an immutable revision store. A snapshot
selects at most one revision per ID, but may retain conflicting assertions with different
IDs. The presence of an old revision does not activate it. Namespaced IDs must be safely
encoded as Windows file names rather than used literally with colons.

## Collections and invariants

| Collection | Minimum content and constraints |
|---|---|
| sources / artifacts | Role, publisher/system/edition/language, part, media type, bytes, SHA-256, availability and compatibility |
| regions / evidence | Source revision, PDF page (1-based), printed label, reading order, coordinate/offset convention, precise region links |
| nodes | Sections, clauses, concepts, procedures/steps, tables/axes/cells, diagrams, components and mechanical definitions |
| assertions | Subject, stable aspect, knowledge state, literal/normalized/interpreted representation, value, scope, evidence and gaps |
| semantic_groups | Stable aspect IDs and explicit condition/effect/exception/timing composition |
| relations | Typed directed link, applicability, target status, candidates, evidence, requirement grouping |
| gaps | Missing source, unreadable, unprocessed, ambiguity, conflict or unsupported interpretation; affected targets and blocked operations |
| profiles | System, edition, rules mode, options, scenario, maps/counters, pinned materials and compatibility decisions |
| reviews | Exact targets and basis revisions, kind, actor role, decision/observation, scope and supersession |
| coverage | Inventory revision, region, representation level, status and exclusion reason |
| snapshots | Selected revisions and hashes, profile, conflicts, manifest and independent readiness reports |
| runs / evaluation | Raw proposals, context manifest, actual configuration evidence, measurements and independently justified expectations |

`sources.role`: rulebook, errata, faq, scenario, map, counter_sheet, player_aid, other.
Edition labels do not establish compatibility. Exact transcription, normalization,
uncertain symbols and interpretation remain distinguishable. Evidence roles are direct,
context and counterevidence. Attaching a whole page does not prove every assertion.

Nodes include action, event_type, state_variable, resource, timing_window, choice,
selector, spatial_policy, randomizer, calculation and outcome. Their source representation
may precede formal execution. A generic payload field alone is not demonstrated support.
Editorial parentage is not an execution dependency. Clause boundaries preserve complete
conditions and effects; aspects can be separately reviewed inside a container revision.

## Knowledge and representation

Knowledge states: `known` (evidenced proposal, review separate), `established_absent`
(source proves absence in an explicit scope), `unknown` (null plus gap/reason), and
`not_applicable` (null plus reason). Missing fields and empty lists never prove absence.
Representations: literal, normalized, interpreted. A normative assertion has an explicit
execution impact: formal, informational with reviewed rationale, or blocking.

Facets include transcription, condition, effect, parameter, exception, timing, scope,
definition, permission, obligation, prohibition, trigger, cost, choice, calculation,
transition, duration, aggregation, visibility and victory. A shared subject ID does
not bind several conditions to the right effects; semantic groups do that explicitly.
Units, comparison operators, rounding stage, temporal bounds and causal filters are typed.
Opaque is preserved text with an execution limitation, never a runtime LLM callback.

## Relations

Navigation (`mention`) is distinct from dependency (`procedure_use`, `table_use`,
`definition`, `condition`). Exception/modification points from modifying rule to base.
`applies_to` points from clause to scope object; `illustrates` from example to rule;
`precedes` from earlier to later step with its condition. `continuation` alone is not
an executable stack frame. Mechanical relations are specified in the mechanics contract.

`target_status`: resolved, unresolved, ambiguous, unsupported. Non-resolved references
retain raw locator, edition, candidate IDs and a gap. Targets can select exact aspects.
`requirement`: required, conditional, informational; groups explicitly specify all/any.
Unknown applicability cannot be treated as false. Rule graphs may contain cycles;
the task dependency graph may not. Procedure cycles need termination/continuation rules.

## Reviews and readiness

Review kinds distinguish transcription, interpretation, source composition and situation
outcomes. Roles distinguish human_owner, authorized human_reviewer, model, validator.
Only an authorized human grants semantic acceptance. Store the decision artifact,
actor, exact target/aspect revisions, scope and basis (sources, definitions, bindings,
profile and dependencies). Basis completeness is complete, partial or unknown.
Freshness is independently computed as current, stale or unknown. A newer date does
not resolve contradictory decisions; explicit supersession and rationale are required.

Coverage statuses are represented, partial, unprocessed, excluded, measured separately
for transcription, descriptive semantics and formal semantics. Exclusions need a reason
and approved scope boundary. Do not add overlapping context regions to the denominator.
Executable readiness is a query over snapshot/profile/dependency closure and available
state/history, not a global `rule_ready` flag.

## Storage and validation

Use `private/ig/projects/spqr/{inputs,sources,records,runs,reviews,snapshots,reports,evaluation}/`.
The promoted source registry at `private/ig/sources/` is a read-only input to later project
snapshots. Source-derived material stays private; public schema fixtures are synthetic.
One record per file is optional. Containers retain stable aspect IDs and raw input mapping.
Indexes are derived. Snapshot states draft/sealed describe structural integrity, not quality.

Validate identity/revision uniqueness, hashes, typed references, evidence scope, unknown
values with gaps, table notes/axes, group composition, review authority and freshness,
coverage denominators, conflicts, and historical versus active reference resolution.
The first schema must represent all required mechanical concepts without implementing
a universal game language. Later formal contracts must make those concepts executable.

Tests need a clause spanning pages, cross-chapter exception, table note, missing unit,
procedure cycle, edition conflict, partial acceptance and regression after dependency
change. Expected meanings are justified against sources, independently of implementation.
