# IG-1C first bounded repair delivery

Independent findings IG1C-R01, IG1C-R02 and IG1C-R03 are each at repair iteration 1
of maximum 2. The parent review and delivery remain byte-preserved. Re-review must
verify these new hashes; passing executor probes does not close the findings.

R01: normalize malformed built-in bool/timestamp/int/float/binary scalar constructor
failures into located ParseError. Normalization is restricted to those scalar tags,
so unrelated implementation defects propagate. Inventory node pointers before scalar
construction; retain exact file/field/line/column. Multi-file sealed-snapshot testing
proves a malformed scalar is an accounted error while subsequent valid/raw files
still survive. Existing unsafe-tag, duplicate-key and alias/depth controls stay strict.

R02: embed the exact operator-pinned WGU structural schema in the owned importer
with its source hash; no neighboring runtime reads or new dependencies. Validate
known optional scalar types, enums, identifiers and nested shapes and canonical file
metadata. Unknown extensions remain preserved. The deliberate existing integer
step.n extension is documented, preserves original values and excludes bool; the
embedded original schema remains unchanged. These are structural checks, not game
semantics. Empty title/en strings allowed by the pinned schema are not falsely rejected.

R03: confusables item values follow the schema's unconstrained item contract;
strings, sequences, null, numbers and mapping extensions survive without false
errors. Their incidental id fields are not entity identities. Genuine malformed
entity records and duplicate recognized IDs remain errors.

Controls: 59 public synthetic adapter regressions plus 35 unchanged independent
reviewer probes pass (94 total). Project check passes with 102 existing tests;
diff check passes. Full independent frozen-file/record/field audit and two complete
imports pass: 23 available WGU files / 36 missing source entries; 1692 records,
1655 processed / 37 raw / zero errors; 38206 locations. The final repair import is
also byte-identical to the earlier successful repair audit after metadata-validation
completion. Earlier outputs and every frozen report are preserved. No historical
count is a test oracle; original full-accounting assertions were not weakened.

One synthetic shared-game-ID fixture was missing mandatory manifest.schema under
the newly added metadata validation. It now includes schema: wgu/kb@1; zero-error
and duplicate-ID assertions stay strict, with stronger exact accounting for the
added raw field and two retained game fields. Separate invalid-metadata tests still
reject missing/wrong schema. This was a changed input condition, not assertion relaxation.

All 53 parent artifact versions are verified against current or explicitly preserved
baseline copies. All 40 reviewer evidence artifacts and 148 accepted foundation
artifacts are unchanged. Only parser.py/importer.py and assigned synthetic tests
were changed; private outputs use new directories. No foundation, neighboring,
archive/history, global settings, new chat/agent/worktree or API changes occurred.

Actual executor Sol/high is based on the earlier direct operator observation in
this same ongoing conversation, with no observed/requested setting change. The
independent reviewer has its own separate operator-confirmed configuration. Native
handle tests/full import used normally reviewed narrow local escalation because
sandbox WinError 5 was previously measured. Native symlink measurements remain null.
Tokens, cost and operator time remain unavailable/null.

Independent re-review and coordinator technical acceptance/done remain outstanding.
Missing sources, mixed editions, source identity unknown, publisher coverage,
human semantic acceptance and executable readiness remain separate. IG-1D/E planned.
