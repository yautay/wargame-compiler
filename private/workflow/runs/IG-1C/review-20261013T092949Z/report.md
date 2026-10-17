# IG-1C independent technical review: changes requested

The full frozen input accounting and byte preservation pass. Independent adversarial review finds three P2 structural defects, so this delivery does not receive technical PASS. No semantic acceptance, publisher coverage or executable readiness is granted. The reviewer changed no product, queue, frozen delivery, dependency or neighboring repository bytes.

## Exact reviewed delivery and configuration

Current delivery: `private/workflow/runs/IG-1C/resume-20261013/delivery.json`, SHA-256 `aefeac57292fcb742e8f7263d2ed30af56af01fd1da8282bc7e4baa3c78742b8`. All **53 artifacts** match before and after review; the complete exact list is embedded in `review.json` and `verification-before.json` / `verification-after.json`. The original 34 artifacts are an unchanged subset. Parent delivery: `private/workflow/runs/IG-1C/stage-20261013/delivery.json`, SHA-256 `8e3fc23cf3d64783b10c2f48287196b807272c2f5b356bcaabf35e695dbd9017`.

Reviewer actor: `ig1c-reviewer-20261013T071955Z`; executor actor: `ig1-stage-executor-20261013`. Actual reviewer configuration is `gpt-6.1-sol` / `high`, confirmed directly by the operator in this reviewer chat after the explicit request to inspect this chat UI. The original pending-null observation and confirmation remain preserved. This is independent of requested creation parameters and executor evidence. Configuration source/hash is recorded in `configuration.json` and `review.json`.

The fresh reviewer packet is `private/workflow/packets/IG-1C-1092608e68ff4dfeb1400b841a891d2d/manifest.json`; every named file size/hash, packet context hash and queue hash was verified. The full packet, selected card and named context were read. The active local skill is `docs/skills/wgc-review/SKILL.md`. IG-1C remains review; IG-1D/E remain planned. Earlier queue recovery is a workflow correction and consumed no product-finding repair cycles.

## Findings

1. **IG1C-R01 (P2), parser.py:114–115.** `!!bool invalid` raises uncaught KeyError; `!!timestamp invalid` raises uncaught AttributeError. The importer catches only ParseError at importer.py:126, so malformed supported scalar contents abort the complete import instead of producing raw/error accounting. Required verification includes both strict probes, located diagnostics and a multi-file import retaining valid files beside malformed files.
2. **IG1C-R02 (P2), importer.py:59–70.** Known optional field types, enums and nested table shapes are not validated/diagnosed. Numeric term definition, unsupported rule flag, mapping instead of a table array and unsupported relation type all count as processed with zero errors. The independent oracle is the exact pinned WGU schema. Preserve extensions and deliberately supported integer/string numbering while adding explicit structural diagnostics. Re-inventory the actual corpus after changes without weakening assertions.
3. **IG1C-R03 (P2), importer.py:55–57.** Scalar confusables entries are falsely required to be mappings. The pinned termsFile schema permits arbitrary array items. `confusables: [Alpha, Beta]` incorrectly produces two errors. Preserve valid heterogeneous entries as supported or explicit raw/unprocessed records without fabricated malformed-record errors.

`findings.json` contains exact code locations, consequences, reproducers, evidence, independent expectation justification and required verification for each stable ID. `probes.py` and its complete log preserve all seven failing assertions unchanged. No repair was performed.

## Full input and provenance evidence

Independent accounting covers **59 manifest entries**, **23 available files** totaling **1,233,389 bytes**, **36 missing configured sources**, **1,692 records** (1,655 processed, 37 raw, zero errors in this actual corpus), **38,206 field/container locations**, and **8,904 conservatively defined unknown-field locations**. All raw bytes, complete document values, every record value, parent binding, external identity, field YAML tag/marks/character ranges and unknown values were checked. Every record has a private value hash; representative mappings for every kind are retained in `independent-accounting.json`. That report explains the unknown-location definition; its count is not the adapter's immediate unknown-field count.

Measured kinds are 523 rules, 134 terms, 15 procedures, 80 nested steps, 48 tables, 233 relations, 79 ambiguities, 3 changes, 59 questions, 465 terminology concepts, 16 confusables and 37 auxiliary records. These counts were derived from raw current bytes rather than historical constants or adapter counters. Two native-verified complete imports are byte-identical and exactly match the frozen import.json. The executor's accounting counts are independently corroborated; its passing tests alone did not establish review acceptance.

The selected registry manifest, source pin and its two enumerated blobs are rehashed; identity to WGU's unavailable original remains **unknown**. PDF bytes were hashed as source evidence; publisher meaning was not reviewed. No neighboring scans, source-history reads, old gold or expected gameplay answers were used. The four exact external WGU schema/store/export/lint files match their pinned hashes. They were read for contract/provenance analysis; none was executed or edited. Hash-only preservation verifies all **148 accepted foundation artifact references** from current frozen foundation-audit.json; prior completed-task text, packets and dry-runs were not reopened.

Saved official PyPI metadata pins PyYAML 6.0.3 wheel hash `5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b`. All 23 installed non-RECORD wheel files match its bytes. Installation-mutated RECORD is explicitly excluded. No network/dependency operation was required.

## Every exact acceptance criterion

| Criterion | Assessment |
|---|---|
| Import rules, terms, nested procedures, tables, relations, ambiguities, changes, questions, terminology and auxiliary files. | Partial: full actual corpus passes; schema-valid scalar confusables fail (R03) and malformed supported YAML can abort complete accounting (R01). |
| Unsafe YAML tags and duplicate keys fail with locations; errors do not become empty collections. | Partial: unsafe Python tags and duplicate keys are explicitly located errors and never empty success; malformed safe scalars escape the error contract (R01). |
| Every unknown field/file is preserved or explicitly diagnosed; WGU verified/complete/resolved remains imported metadata. | Pass on complete frozen corpus and independent extension/unknown-file probes. Raw preservation and no inherited approval are corroborated; complete error recovery still needs R01. |
| Refs/see remain navigation; questions are evaluation candidates, not battle scenarios or accepted expected results. | Pass: every applicable actual record and independent controls preserve these distinctions. |

The required malformed-record validation also remains incomplete for known optional types/containers/enums (R02). Anonymous terms, nested numbering, duplicate IDs, real recursion/alias expansion/depth budgets and unknown fields/files pass their independent controls. There is no newly implemented game logic and no LLM legality claim.

## Actual checks and limitations

| Control | Actual result |
|---|---|
| Workflow validate / fresh packet / packet and delivery hashes | Exit 0; all pinned bytes match. |
| Explicit tests/wgu_adapter | Exit 0; 31 pass. |
| Independent adversarial probes | Exit 1; 28 pass, 7 fail, grouped into three P2 findings. |
| Separate tests/inputs in initial sandbox | Exit 1; 15 pass, 36 fail due native Windows/filesystem sandbox restrictions. Original log retained. |
| tests/inputs after reviewed narrow local escalation and fresh basetemp | Exit 0; 51 pass. No no-follow check bypassed. |
| Independent complete accounting, native verification and two imports | Initial sandbox exit 1 (WinError 5); changed-condition narrow local escalation exit 0. |
| scripts/check.ps1 -Task IG-1C | Exit 0; plan/dry-run/pytest/diff all 0; 102 tests pass. |
| Final git diff --check | Exit 0. |
| Final frozen delivery/external/dependency/foundation preservation | Exit 0; all 53 delivery and 148 foundation entries preserved. |

All commands/exits and measured wall intervals are in review.json and individual check records. No unchanged failed probe was retried; no product assertion was weakened. The reviewed native escalation changes environmental conditions, not product behavior. Real Windows junction tests passed. Native file/directory symlink behavior remains unmeasured/null; passing junction tests are not evidence for symlinks. Tokens, cost and operator time are unavailable/null. Full source coverage, human semantic acceptance and executable readiness remain separate, ungranted gates.

## Next exact action

Coordinator requests bounded repairs for IG1C-R01/R02/R03, preserves this delivery/review, freezes changed hashes, and returns the changes to this independent reviewer. Maximum two repair cycles per finding and two unchanged-failure retries apply; this review used zero repair cycles. Re-run strict reviewer probes, affected adapter controls, complete private accounting and required project/diff checks. Acceptance/done and any next-task readiness remain the coordinator's responsibility. The reviewer sent no messages to other chats and changed no queue state.
