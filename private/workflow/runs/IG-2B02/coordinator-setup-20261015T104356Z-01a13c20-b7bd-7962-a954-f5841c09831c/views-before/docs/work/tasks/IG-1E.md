# IG-1E: Accept full KB input accounting

<!-- Generated from docs/work/queue.json; edit the queue, then render. -->

- Status: `done`; kind: `implementation`.
- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.
- Dependencies: [IG-1D](IG-1D.md)
- Human semantic acceptance required: false.

## Goal

Deliver a reproducible complete private KB import and a technical acceptance report.

## Concrete deliverables

- Private full-input import report and sealed structural snapshot
- Public synthetic integration regression suite

## Start conditions

- All dependencies are done; input revisions and assigned file scope are pinned.
- Actual executor configuration and ownership are recorded; unresolved refinement prevents start.

## Input contracts

- private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json SHA-256 67ac53869ea80ea4d84018e253a9033e48fe89823d0a9a397ab8fe41b91d33d5
- private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json SHA-256 615b1ae1cbeebf894c7f8dbbb7c3f2bcb0819427a342b3fa05bc690c33b9eed8
- private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json SHA-256 2999d63c680b4c52a095e0edb18952c70eefdf4baf7c2e01481840cda18ca61a
- private/workflow/runs/IG-1D/repair-02-20261013/delivery.json SHA-256 ea2d2cacf42939e516dfc8b65f6c0cffc2d2267478819233fb1f573fddd4275c
- private/workflow/runs/IG-1D/repair-02-20261013/preservation.json SHA-256 11e73e3ef527b90c03f386eb98471b2f500447b2907b4f59a15f3fdfc530d051
- private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z/review.json SHA-256 0cf77240f11260ce513484a07d79ef3919f48d63dd61433ed9f274effbdb424c
- private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z/review-manifest.json SHA-256 ada8130957d2b336225acfa386878b6f327a27be37a47556b58ce28cfed55a60
- private/workflow/runs/IG-1D/repair-02-20261013/accounting.py SHA-256 5a9b9e7d97b2afd2470890f16e426e89b7eb51cf54e9e80c260b7a4b34c4d00b
- private/workflow/runs/IG-1D/preflight-20261013/initial-registry.json SHA-256 37d6ae2aef4a5ba533b390e331ce748c6b84a3f13c857e799533195f1f903934
- private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc/manifest.json SHA-256 e34a0f71198358c602c5a04aa5d0ff1b357506b32f2a9f75acd35c69ac98a48e
- private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc/source-ig.json SHA-256 ac9370c5535a5d49b513deba7f6136d9eebe538f71599cc1dd468fb0921d5ebb
- private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc/identity-registry.json SHA-256 05eaf2ef84dc457fcbdac04e92abff19620831086fda12eddd26a154b37e7539
- private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc/references.json SHA-256 ce1e9259b75408a634c00bccadd29b5c45333151e5a9fd75ffd71883b780669f
- src/wgc/wgu_adapter/importer.py SHA-256 b8c67438690b3f68d66e2b6b85b25cd5e43b81673c7f8aaf969b659b9980f359
- src/wgc/wgu_adapter/parser.py SHA-256 1a696cc1e36e143c7118b122a868de799134c84ae2f7615e9eacf3bcafca108f
- src/wgc/wgu_adapter/identity.py SHA-256 784ab223591db89b8b09ca5e7c3c835b8f393828f46790f983fab6c4146c28a6
- src/wgc/wgu_adapter/references.py SHA-256 2052794a3ce213fa3951607c7f0c9f3fdab9f4f882dd2cb2117b4c9db23f9f96
- src/wgc/export/source.py SHA-256 bf58eb6ac141ede3a9d3f2fa9ffc858be61c73252a596480d0edc4e62f6b407b
- src/wgc/export/storage.py SHA-256 eef41dcf6c752dbd5c48621fb3c2c052bbccc3a393ba656703fef1c0d5f21b52
- src/wgc/export/source-export.schema.json SHA-256 2a1f619eb4773d1432470cf0a340ac55c2f74451661c92002a6c89a7864bd768
- src/wgc/inputs/snapshot.py SHA-256 6f701f14fb23a377af11ea73eba24e088c90db74acef8587d0838ed4e4eb01ed
- src/wgc/contracts/source.py SHA-256 14aa5fd5129ed5f6ae65937a3f646407c3f1433483aa2145b53f942ed43509b1
- Use only exact files enumerated by the frozen input/source manifests; no publisher text/page interpretation.
- Independent complete inventory, two fresh imports/transforms/publications and reproducible sealed structural snapshot; no semantic, source-coverage or executable acceptance.
- New sealed snapshot identity retains original draft snapshot by exact historical lineage and preserves every selected revision/readiness assessment; immutable dedicated structural manifest, no existing profile/schema changes.

## Required context

- docs/IG-WGU-ARCHITECTURE.md
- docs/IG-DATA-MODEL.md
- contracts/ig/README.md
- src/wgc/contracts/source.py
- src/wgc/export/README.md

## Allowed write scope

- tests/integration/
- private/ig/projects/spqr/runs/import-acceptance/
- private/ig/projects/spqr/snapshots/

## Exclusions

- Archives and Git history; neighbouring repositories; global configuration.
- Downstream tasks, unrelated changes, online services, commits and pushes.
- Publisher content in public fixtures; automatic semantic acceptance.

## Acceptance criteria

- No file/record/unknown field silently disappears; report processed/raw/error counts separately.
- Structural snapshot can be sealed with gaps; no claim of source coverage or semantic correctness.
- Document missing sources and required subsequent reconciliation; preserve mixed editions.

## Required validation

- Full private accounting and reproducibility run; independent reviewer samples mappings and checks entire file/record ledger.
- No archived fixtures, answers or gold required.

## Blockers and escalation

- A required contract is ambiguous, input changed, or owned files have another writer: checkpoint and escalate to coordinator.
- After two unchanged retries or two repair cycles, record blocked with the smallest resolution needed.

## Final report and handoff

- Freeze deliverable paths/SHA-256, input packet hash, exact criteria met/unmet, test commands/exits and independent review request.
- Record actual model/reasoning evidence, UTC/wall time, observed tokens or null, defects, unresolved decisions and next operation.

Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.
Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.
