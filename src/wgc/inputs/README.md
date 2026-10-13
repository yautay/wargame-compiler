# Input byte snapshots, wgc-input-1

`snapshot.py` freezes exactly an operator-enumerated WGU `wgu.yaml` and `kb/`
file set, individually listed configured sources, and explicitly listed source
registry files. It does not parse YAML, infer auxiliary paths, import the KB,
interpret publisher content or evaluate game rules. Directory enumeration is
limited to KB names; source registry directories are never recursively scanned.

The request supplies absolute `game_root` and `registry_root`, `game_files`,
`historical_configured_sources`, `registry_files` and an explicit `selection`.
Required entries have relative POSIX paths, role, byte count and SHA-256 pins.
Optional configured sources declare their observed availability. All 36 historical
SPQR source paths are individually rechecked; missing bytes have null size/hash/
copy path and cannot silently become the promoted PDF. Additional auxiliary input
requires another explicit enumeration. Planning timestamps are not snapshot identity.

`contracts/ig/input.schema.json` specifies both manifest shapes. The bounded offline
schema evaluator and WGC-C14N-1 canonicalization from the IG-1A source contract are
reused without changing that frozen product. A snapshot ID is `sha256:` followed by
SHA-256 of its canonical manifest body excluding only `snapshot_id`. File order is
sorted by exact relative path. Files preserve original bytes, including line endings,
encoding, combining characters and binary data. Schema-only checks cannot establish
copy integrity, selected source identity or path safety; `verify_snapshot` is required.

Verification inventories the complete sealed tree by names and no-follow metadata
before opening copied blobs or the source pin. The only allowed files are the exact
available manifest blobs, root `manifest.json`, and root `source-pin.json` for source
snapshots. Allowed directories are precisely their required parents. Extra bytes,
metadata, empty directories, symlinks, junctions and blobs for missing entries reject.
This check applies to staging, published verification and existing-snapshot reuse;
corrupt existing directories are never overwritten or silently repaired.

Published directories are named `sha256-<digest>` and contain canonical `manifest.json`
and `files/<relative-path>`. A source snapshot also contains `source-pin.json`, which
pins the new IG source and explicitly retains `identity_to_wgu_original: unknown`
and `semantic_acceptance: not_granted`. Edition labels are declared provenance,
not newly verified source meaning. Input manifests link the exact source snapshot ID.

Paths reject traversal, ADS, Windows device/trailing-character aliases, duplicate/case
aliases, symlinks and junctions in any existing ancestor. Physical hardlink aliases
also reject. Before reading any source bytes, the complete plan and KB name set are
checked. Windows read handles refuse reparse points, check their actual final path
and share only reads; POSIX uses directory descriptors and `O_NOFOLLOW`. If the host
cannot perform these checks, the operation fails closed. No sandbox bypass is built
into the library. Required inputs must match their pinned size/hash.

Copies are independently reopened and hashed. The KB name set is checked again and
every available origin is rehashed before publication; missing sources are rechecked
for appearance. Handle/path identity, size and modification metadata also detect changes.
Windows ctime is compared within the handle API because pathname `stat` and `fstat`
have differing creation/change-time semantics. Full byte hashing remains authoritative.

Each destination is disjoint from input roots and the other destination. Staging is
new `.pending-<UUID>` content. Manifests and bytes are verified before publication by
rename. Existing snapshots are verified and reused, never overwritten; newly created
successful duplicate staging is removed only after checking its resolved parent boundary.
Failed staging is retained as incomplete evidence and has no published snapshot status.
Source and input publication are separate: an input publication failure can leave a
valid unreferenced source snapshot, not an accepted input set. There is no global filesystem
transaction across all origins, and later origin mutations do not change frozen bytes.
Application append-only storage detects operator tampering; it is not OS-level immutability.
Untrusted concurrent writers to destination directories require filesystem isolation.

Run locally with explicit destination directories:

```powershell
$env:PYTHONPATH = 'src'
$env:PYTHONDONTWRITEBYTECODE = '1'
.\.venv\Scripts\python.exe -m wgc.inputs.snapshot request.json --inputs private/ig/projects/spqr/inputs --sources private/ig/projects/spqr/sources
.\.venv\Scripts\python.exe -m pytest tests/inputs -q -p no:cacheprovider --basetemp private/workflow/checks/input-check-new
```

Use a fresh test directory. CLI exit 0 confirms the recorded byte snapshot, not source
coverage or semantics. Failure exits 1 and publishes no falsely valid changed input.
The existing project test paths are preserved; `tests/inputs` is run explicitly in this
increment rather than modifying integration paths outside the IG-1B write scope.
On this Windows host, native final-path checks and real junction/hardlink tests need a
local execution context that permits those operations; restricted execution rejects them.
