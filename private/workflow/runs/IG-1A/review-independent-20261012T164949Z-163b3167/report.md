# Independent technical review of IG-1A

Result: **FAIL — changes required**, with three P2 findings. The standard repository checks pass, but independent synthetic counterexamples violate coverage and selected-reference invariants. This report grants no SPQR semantic acceptance and no executable readiness. Queue state remains `review`; only the coordinator may arrange repair and a new frozen delivery.

Reviewer identity: `review-independent-20261012T164949Z-163b3167`, distinct from executor `ig-1a-executor-20261012-0540`. Scope: IG-1A only. No implementation, frozen delivery, fixture, queue, or status files were edited. New review artifacts live in this directory; the standard check script created its own fresh output directory.

## Configuration and provenance

Requested configuration: `gpt-6.1-sol` / `high`, from the separate-session review request. Exact executing model and reasoning are **null**: runtime metadata available to this reviewer do not expose them. The operator was asked to confirm the UI settings of this separate session; no confirmation had arrived when this report was finalized. Creation parameters and the executor's UI confirmation were not treated as runtime evidence. The technical findings can be reproduced locally; this report does not certify the requested reviewer configuration.

Read AGENTS.md, README.md, STATUS.md, HANDOFF.md, WORKFLOW.md, the local wgc-review skill, the prepared review prompt, queue IG-1A, the original packet and its four assigned design documents. All evidence is synthetic. No game PDF, archives, Git history, neighbouring repositories, external APIs, agents, additional chats, automation, commits, or pushes were accessed or created.

Frozen delivery SHA-256: `115b22ab83d71ed1cb176fee045200d14a96ad2ab54865a09d0daec2293fc0ac`. All **50/50** artifact hashes matched before review. `hash-verification.json` pins the entire exact artifact list, including the two explicitly listed construction scripts in the older attempt directory; no older operational candidate was substituted for this delivery.

Original packet manifest SHA-256: `d2e6e8d92bfc62609956bff873e1785b7d4805b3a529b40c541d4c6133f391e5`. Context SHA-256: `e2196f03fecabb5d6f2afa1161b6778cbefcb27693bc2a7a35e1c4eec0eb9c12`. Both match the frozen report. Current STATUS/HANDOFF/task-card differences are workflow projections of the transition to review. The packet's WORKFLOW text has transport-normalized line endings (nine LF-only lines became CRLF); normalized text matches, and the current original WORKFLOW bytes match its manifest hash. This is recorded explicitly rather than claiming byte-identical embedded text. `packet-verification-final.json` records both comparisons.

## Findings

### F1 — P2: gaps can be counted as represented coverage

Location: `src/wgc/contracts/source.py:367-368` and `:415`; schema `contracts/ig/source.schema.json:2415` (`coverage_data.target_refs`). Counterexample: `gap-as-represented-target.json`, record `synthetic:coverage0`, `/data/target_refs/0`.

Replace the only represented target with an active reference to `synthetic:gap`, leave `gap_refs` empty, and recompute the coverage and selected-snapshot hashes. Validation succeeds and reports two represented transcription inventory regions, although the first is represented solely by a gap. The existing negative fixture puts a gap in `gap_refs`; it does not test the same gap in `target_refs`.

Consequence: source coverage can be overstated using structurally valid, properly hashed records. This contradicts the architecture's explicit rule that gaps never count as represented content and criterion 3's separation of coverage from other claims.

Smallest repair: constrain or explicitly validate the record types allowed in represented `target_refs`, rejecting gap records as represented content. Document the allowed source-content target families rather than permitting every record type by default. Verify a gap-only target is rejected, a mixed node/gap target is rejected, the existing valid node targets remain valid, and both reference modes obey the same rule. Add an independently authored static regression fixture.

### F2 — P2: an unrelated scoped approval authorizes a coverage exclusion

Location: `src/wgc/contracts/source.py:369-372`; schema `contracts/ig/source.schema.json:2446` (`coverage_data.scope_decision_ref`). Counterexample: `unrelated-exclusion-approval.json`, record `synthetic:coverage0`, `/data/scope_decision_ref`.

Mark region 1 coverage `excluded`, give it an exclusion reason, and point `scope_decision_ref` to the existing human-accepted review. That review explicitly targets only `synthetic:clause/lit-condition` and says its scope excludes the effect. It does not approve excluding region 1 or establish an inventory boundary. Validation nevertheless succeeds and reports one represented and one excluded transcription inventory region.

Consequence: any unrelated current acceptance can be reused to exclude source material. Scope text, exact targets, and acceptance boundaries are present in the records but are not connected to the exclusion decision. This fails the approved-scope-boundary requirement and criterion 3. It is a structural mismatch, independent of the separate limitation that human identity/artifacts are unauthenticated.

Smallest repair: define a machine-checkable exclusion decision target (for example, the exact region and relevant inventory/level boundary), and require the referenced accepted, current, complete decision to target that boundary. Avoid a circular hash by targeting the region/boundary rather than the coverage record containing the decision reference. Do not use a substring test against prose. Verify unrelated, other-region, stale, partial, and model decisions fail; an exact authorized boundary decision passes. Preserve historical rejected/accepted records without transferring their scope.

### F3 — P2: selected required dependencies can bypass snapshot selection

Location: `src/wgc/contracts/source.py:238-242`, `:303-304`, and `:433-435`; schema `contracts/ig/source.schema.json:2132` (`relation_data.target_ref`). Counterexample: `historical-required-dependency.json`, record `synthetic:history-link`, `/data/target_ref`; omitted selection `synthetic:procedure`.

Turn the selected navigation relation into a required `procedure_use`, make applicability known, pin its target historically to `synthetic:procedure`, and remove that procedure from the selected manifest while retaining its immutable revision in the store. Validation succeeds. The required relation is reported as resolved and is absent from `source_blocker_ids`; the unselected procedure's unknown termination is also absent from that list. Other baseline blockers remain, so this does not create executable readiness.

Consequence: a selected semantic dependency can silently consume an unselected revision. A historical navigation reference legitimately resolves retained evidence, but changing its role to a required procedure does not trigger the selected-rule invariant. This undermines snapshot closure and contradicts the data model's rule that references used as active rules resolve only in the selected snapshot. Relevant to criterion 2 and the source dependency boundary.

Smallest repair: enforce selection for selected semantic dependency endpoints. Either require active references for those rule links, or require any exact historical pin to match the selected revision and reject an unselected/different revision. Keep historical reviews, provenance, supersession and informational navigation valid. Add static tests for required and conditional dependencies to unselected and superseded revisions, alongside the existing historical mention and active-dangling controls. This needs no gameplay interpreter.

## Acceptance criteria accounting

| Criterion (queue order) | Assessment | Evidence and limit |
|---|---|---|
| 1. Schema represents sources/regions, stable aspects/groups, relations, gaps, origins, coverage, profiles, runs, reviews, snapshots | Representation present | Thirteen typed record families; explicit envelopes, aspects and semantic groups. Positive baseline and empty/duplicate/wrong-facet group tests support representation. Coverage enforcement still needs F1/F2. |
| 2. Explicit deterministic identity/revision hashes; anonymous identities independent of position | Hash/identity portion passes; selected-reference invariant fails | Integer/scalar canonical profile, fixed independent byte/hash vectors, stored identity registry, injective Windows filename encoding, reorder and duplicate tests. F3 permits a required link outside selection. This is not an identity-hash failure. |
| 3. Review, coverage and execution separate; opaque source allowed without execution | Separation present; coverage correctness fails | Source status cannot be `ready`; validation grants no semantic acceptance; opaque/unknown normative impact fails unless blocking. Freshness follows exact targets/bases. F1/F2 invalidate approval of this criterion as delivered. |
| 4. Required mechanics addressable without generic payload-only claims | Pass for source descriptions | Dedicated kinds/fields for state, resources, history/causes, parameters, choices/bindings, reactions, continuations, costs, geometry/spatial policies, tables/calculation, chance and visibility. Additional fields cover duration, allocation and victory. Addressability is by node and named descriptor field, with aspect-scoped reviews where supplied. Several fixture fields are explicit not-applicable descriptions; these are not evidence of real SPQR meaning. |
| 5. No importer/formal interpreter/compiler/game logic; open IG-3A decisions | Pass | Product code performs JSON shape/hash/reference checks and structural reporting. README keeps formal operators, units, transactional history, bindings/termination, reaction/cancellation, lookup/geometry/chance/visibility and closure choices open. Construction scripts were read, not executed. |

Overall technical pass is withheld for F1-F3. No task completion or SPQR semantic acceptance is inferred from schema representation or passing project tests.

## Required validation and additional adversarial accounting

All 26 catalogue fixture outcomes were reproduced; each catalogue row records an architectural basis and expected outcome. The independent probe summary contains 51 checks: 26 catalogue cases, 16 complete synthetic mutations and nine schema keyword cases. **48 expectations met; three failed**. The final focused pytest run confirms **13 passed / 3 failed** on the 16 independent bundles.

| Required case or risk | Observed result |
|---|---|
| Unknown value without gap | Static negative rejects; known without evidence also rejects. Unknown normative aspect labelled formal rejects independently. |
| Changed aspect integrity and old acceptance | Stale aspect hash rejects; properly resealed changed aspect makes old scoped review stale. Changing an unrelated effect leaves the condition-scoped review current. |
| Changed dependency / false freshness | Source basis change is stale; missing selected source basis is stale; whole-record target description change is stale. Complete empty basis rejects; partial/unknown unchanged basis reports unknown. Dependency completeness remains a declared claim. |
| Model/validator approval | Both accepted model and validator roles reject. Model observation passes and grants no acceptance. Human metadata in fixtures are fictional and unauthenticated. |
| Active versus historical resolution | Active dangling fails; historical missing revision fails; retained historical mention passes. Required historical dependency outside selection exposes F3. |
| Duplicate identity and anonymous mapping | Duplicate store/selection/origin key rejects; reordering store preserves result. Stable record type/aspect checks inspected. Registry persistence is a contract, not an implemented rematcher. |
| Opaque/unknown execution claims | Opaque formal and source `ready` reject; positive opaque source remains structurally valid and executable blocked. Unknown normative formal independently rejects. |
| Clause spans pages / printed labels | Baseline evidence pins two regions with distinct 1-based PDF pages and printed labels. Source bytes remain separate from canonical record bytes. |
| Group composition | Wrong facet, empty effect and duplicate condition reject; positive explicit grouping retained. No composition semantics are executed. |
| Tables/notes/coordinates | Dangling note target, empty note scope and wrong participating coordinate reject. Axis/cell/note identity and order, merged references inspected. Formal coordinate domains/lookups remain IG-3A. |
| Cross-section exception | Static positive preserves modifier-to-base direction across separate editorial sections; editorial parent is not treated as execution. |
| Edition/profile compatibility | Explicit unknown profile compatibility with a gap is preserved, without a newer-wins policy. Positive fixture remains blocked. No edition compatibility is authenticated or inferred from labels. |
| Procedure cycle | Active-ID cycle is stored without recursive hashing; missing termination is unknown/blocking. The source contract claims no loop execution or termination proof. |
| Coverage denominator overlap | Overlapping inventory rejects; overlapping context preserves count. Box/offset code inspected. Mixed locator and differing extraction hashes cannot prove nonoverlap; inventory authors must justify partition conventions. F1/F2 are separate defects. |
| Scoped/partial review | Exact aspect targets remain bounded; partial/unknown basis gives unknown; changed relevant target/basis gives stale. Unrelated scope reuse exposes F2. |

The fixed byte/hash tests and catalogue expectations have a stated design basis rather than using validator output as an oracle. Mechanical fixture construction iterates schema fields, so fixture presence alone is weaker evidence; the fixed mechanism expectations in test_source.py and direct comparison against IG-MECHANICS-PROFILES independently establish the required named fields. None of these synthetic oracles justify publisher meaning.

## Schema subset, scope exception and limitations

The bundled schema uses only the evaluator's supported keywords; local refs and sibling restrictions, exact oneOf matching, if/then, required/properties/additionalProperties, arrays, string constraints, numeric bounds and boolean/integer separation were inspected and exercised. Unsupported keyword rejection is covered by the product tests. This is a bounded offline implementation for this schema, not certification as a general Draft 2020-12 validator. Cross-record checks remain necessary; F1-F3 pass shape validation with correct hashes.

The operator-authorized workflow fixture exception is verified by removing exactly the comment and two synthetic initialization assignments. The reconstructed file SHA-256 equals `dc2abee8f50737f18ee0ef7c23404a857ebe10c913a7d1aa65c6fe75363f9b22`, the exception's recorded base. No assertion was changed. The fixture deep-copies the task before setting ready/empty events. The check script still invokes the full configured pytest suite, selects current IG-1A for dry-run, starts zero models and leaves queue bytes unchanged. See `scope-exception-verification.json` and the fresh dry-run log.

Remaining acknowledged source-layer limitations: authority and decision artifacts are metadata rather than authenticated facts; complete review basis is not a dependency completeness proof; contradictory reviews have no effective-decision aggregation; field-level descriptions are not executable values/domains; coverage counts are claims over inventory regions rather than complete-rulebook certification; mixed coordinates require inventory judgment. Source/profile closure, hidden-information safety, runtime algorithms and game performance require later tasks. These limits do not excuse the three concrete structural failures above.

## Checks and handoff

| Command | Actual exit/result | Evidence |
|---|---|---|
| `pwsh -NoProfile -File scripts/check.ps1` | 0; 72 passed in 48.00 s; plan/dry-run/tests/diff all 0 | `private/workflow/checks/active-21aba6918dd34d5ead87c82bd5db7626/` |
| Reviewer `probe.py` (final strengthened historical procedure case) | 1; 51 expectations, three unmet | `probe.log`, `probe-results.json` |
| Reviewer focused pytest, first run | 1; 13 passed, 3 failed in 5.85 s | `focused-pytest.log`, fresh `pytest-fresh/` |
| Reviewer focused pytest after strengthening F3 | 1; 13 passed, 3 failed in 3.44 s | `focused-pytest-final.log`, fresh `pytest-final/` |
| Standalone `git diff --check` | See `checks.json`; actual exit recorded | `diff-check.log` |
| Final frozen delivery/packet/preservation checks | See `preservation-final.json`; every original delivery artifact rehashed | Immutable manifest and exact current hashes |

`review.json` records actual configuration unknowns, measured UTC interval, null unavailable token/operator/cost data, findings, checks and evidence hashes. Initial context reading preceded the first clock measurement and is excluded from the measured interval; no invented total active-work duration is reported. An initial ad hoc evidence extraction assumed CRLF and failed for an LF test file; it was corrected by byte-preserving splitlines reconstruction. The final packet evidence also explains transport normalization instead of treating it as an input mutation.

Next exact action: coordinator authorizes bounded repairs for F1-F3, obtains a new frozen delivery and requests independent review of changed hashes plus affected cases. Confirm the reviewer session's actual UI configuration separately if this review is to satisfy the requested model/reasoning gate. No accepted/done transition is authorized by this report.
