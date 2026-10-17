# IG-1C technical delivery

Complete lossless import of the frozen WGU input preserves raw bytes, YAML field
locations, extensions, file metadata, unknown files and nested records. Safe YAML
loading rejects unsafe tags, duplicate keys, recursive aliases, unsupported complex
keys/merge keys and over-budget input explicitly. Malformed records remain in the
ledger with errors. Anonymous terms and nested step numbers retain their original
values. Duplicate recognized entity IDs retain every occurrence and diagnostic.
Auxiliary game identifiers are metadata, not entity identities.

The independent full-input oracle reads the manifest and files directly, inventories
every record and every field separately from adapter counters, compares all values
and raw bytes and verifies two complete imports are byte-identical. It measures 59
manifest entries: 23 available WGU files (1,233,389 bytes), 36 unavailable configured
sources; 1,692 accounted records: 1,655 processed, 37 raw, zero errors; 38,206 YAML
field/container locations. The separately pinned registry contains two available
files, bringing foundation available bytes to 5,199,801. The PDF is not KB data.

Recognized records: 523 rules, 134 terms, 15 procedures, 80 steps, 48 tables, 233
relations, 79 ambiguities, 3 changes, 59 evaluation questions, 465 terminology
concepts, 16 confusables. Auxiliary records account for all remaining file metadata.
Counts are measured and independently derived, not historical test constants.

Refs/see are navigation only. Relation verified, table complete, ambiguity resolved,
terminology decisions and question answers retain imported values without approval.
No publisher-source coverage, human semantic acceptance, executable readiness or
game interpreter is claimed. Missing/mixed-edition materials remain for later
reconciliation. Source identity to WGU's missing original remains unknown.

Dependency: project-local PyYAML 6.0.3; wheel SHA-256 matches saved official PyPI
metadata; installed wheel source/extension files match literally. Product scope is
parser.py/importer.py/tests and private import runs; dependency installation is the
operator-authorized separate .venv exception. No foundation product edits.

Controls: 31 synthetic adapter tests and 102 existing project tests pass; full
private file/record/field accounting and repeatability pass; diff check passes.
Native no-follow handle verification required narrowly approved local escalation
because sandbox denied GetFinalPathNameByHandle (WinError 5). Symlink behavior is
unmeasured here; prior unavailable native symlink measurements remain null.
Initial harness assertions used differing IG-1A review field/case conventions and
were corrected against actual evidence. First full audit exposed the shared game-ID
bug; a regression closes it. Initial project check failed solely on coordinator
CRLF diff whitespace. Baseline line endings are preserved and added lines use LF.
All prior reports/accepted foundation files remain unchanged.

Independent technical review is pending. IG-1D and IG-1E remain planned. Operator
confirmed this executor conversation's UI as "sol 6.1 high"; requested reviewer
settings do not establish actual reviewer configuration. Usage/cost/operator time
are unavailable and null.
