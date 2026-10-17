# IG-1D bounded second R04 repair

The named lineage replay now examines all persisted receipt children before the
kind/scope filter. A reused decision with incompatible logical child kind, resolved
parent scope or persistent child key raises ValueError on a private registry copy.
The caller registry is unchanged, and no replacement allocation is returned. A new
decision identifier permits a deliberately different output contract.

New synthetic controls cover term-to-rule reuse, child-key addition/removal/change,
logical procedure scope changes, deliberately new typed decisions, keyed splits,
parent reordering and file movement with corrected content. Unique merge corrections,
rename, stable IDs/origin keys and historical origins remain covered. No original
reviewer assertion or existing test was changed. R01-R03 remain closed by the
independent repair-1 report; only R04 used its second and final repair cycle.

The full public adapter/export suite and all original, risk, receipt-edge and export
history probes passed. The required project and diff checks passed. The independent
full-input oracle was copied without assertion changes; only its operational actor
was adapted. It checks every frozen file, record, YAML field/container location,
binding, raw byte/hash and selected/historical revision closure, and performs two
canonical transformations/publications. Its fresh output matches the frozen draft.

All current parent, prior checkpoint, independent reviewer and accepted foundation
versions are preserved by exact SHA256 mappings in preservation.json. The previous
identity.py bytes have an explicit baseline copy. Original source schema/validator,
approved export profile, input snapshots and accepted imports are unchanged.

The product remains structural-draft. Missing sources, unresolved references,
mixed-edition uncertainty and blocking opaque aspects remain. Technical delivery
does not grant source coverage, human semantic acceptance or executable readiness.
Independent re-review of these exact new bytes and coordinator acceptance/done are
pending. IG-1E is planned and cannot begin before those gates pass.
