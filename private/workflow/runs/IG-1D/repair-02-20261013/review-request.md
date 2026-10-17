# Independent re-review request: IG-1D bounded R04 repair two

Review the new delivery.json in this directory and its exact artifact manifest.
The operational chat message will provide its SHA256 after freezing. The prior
finalized replacement review is replacement-rereview-20261013T140127Z/review.json
(bd053c6d858dfbb2656a5e10b9ea395d14aee6f2e04f56f4f1d0176746accfba).
R01-R03 remain closed; R04 has now used iteration two of maximum two.

The product change is only the named receipt guard in identity.py. It compares
all persisted children before kind/scope filtering can hide an incompatible
output. Incompatible kind, resolved parent scope or persistent child key rejects
atomically. Existing unique-child correction and rename retain identity; a new
named decision permits an intentionally different output contract. The only new
public test file is test_lineage_contract_repairs.py. No existing assertion changed.

Independently verify the boundary, strict negative/positive controls, receipt replay,
keys, logical scopes, parent/file reorder and historical origins. Preserve all 15
original probes and all existing risk/receipt-edge/export-history assertions. The
executor passed 128 combined public/independent controls and 102 project tests.
Re-review affects exact new product bytes; these counts alone are not acceptance.

Verify preservation.json and the old/foundation versions at their verified_path.
The full-input accounting oracle in this directory retains every prior assertion;
only the operational publication actor changed, as oracle-preservation.json checks.
Independently re-enumerate files, records, unknown fields, bindings, reference and
hash/revision closure, then verify two real canonical transformations/publications.

Use a fresh private review directory and short basetemp with no cacheprovider.
Never run helpers that write into frozen old directories without copying and
adapting only their output destinations. Native no-follow probes need the same
reviewed local execution; do not weaken assertions or bypass checks. Configuration
continuity is only valid for the same replacement reviewer chat already confirmed
by the operator. Record actual UTC/wall time and null unavailable usage/cost.

Finish and freeze review.json, report.md, findings/dispositions and a hash manifest.
If technical checks pass, explicitly close every original finding and account for
every task criterion. Include workflow-compatible passing acceptance evidence
with role reviewer, your distinct actor, exact delivery.artifacts and exact task
criteria. Preserve failed setup attempts separately if any; never relabel them.
Do not edit product/tests/queue or grant human semantic acceptance. Report exact
final paths and hashes. If R04 still fails, report the exhausted repair budget.
