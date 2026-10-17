# IG-2B02 transition-envelope recovery handoff

The original frozen delivery and manifest remain immutable. All implementation and
required validations passed (71 source tests, 102 full-suite tests). The attempted
in_progress -> review transition exited 1 with Invalid artifact hash/path. Inspection
confirmed queue still in_progress and no review event persisted.

The executor wrongly included five executable observations as direct workflow artifact
paths: .venv/Scripts/python.exe is denied, and four installed native executable paths
are absolute/outside the repository. All bytes matched. These pins remain preserved
inside toolchain.json, preflight.json and delivery-manifest.json. The append-only
delivery-transition-envelope.json removes only those five direct paths, retaining all
admissible frozen product/report/source/evidence references and adding recovery evidence.
No original frozen artifact, source, tool, test, contract or validation was changed.

This is a concrete recovery proposal, not a successful transition or authorization to
retry. The launch instruction requires checkpoint/escalation and forbids automatic
repeat after transition failure. The operator/coordinator must explicitly authorize
the proposed new envelope/retry. If authorized, execute exactly the recorded command,
inspect actual event/hash/status, seal original delivery plus this new envelope and
all recovery evidence without overwriting originals, and stop at review.

The independent reviewer must use the exact envelope selected by the eventual review
event. That envelope will include the original frozen manifest, all admissible original
review targets and this recovery record. Original assigned-page/ledger/old-scope/hash
verification requirements remain unchanged. The current task is not yet in review.
