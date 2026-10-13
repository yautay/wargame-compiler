# Independent IG-1A review prompt

Work locally in `C:\repo\wargame-compiler`. Discuss findings with the operator in Polish;
write repository reports in English. Review only IG-1A: Establish the source IG contract.
Do not implement another task, repair the delivery silently, run agents/new chats,
access archives/Git history/neighbouring repositories/external APIs, or commit/push.

Read `AGENTS.md`, `README.md`, `docs/STATUS.md`, `docs/HANDOFF.md`,
`docs/work/WORKFLOW.md` and explicitly `docs/skills/wgc-review/SKILL.md`.
Use `docs/work/queue.json` as the sole task/status authority. Establish a reviewer
identity distinct from `ig-1a-executor-20261012-0540`. Confirm actual model/reasoning
from runtime metadata or operator UI observation; requested GPT-6.1 Sol/high is not
evidence by itself. Do not claim to be an authorized source-meaning reviewer.

Read the frozen run `private/workflow/runs/IG-1A/attempt-20261012-scope-repair/`, specifically
`delivery.json`, `report.md`, `checks.json`, `configuration.json` and the paths in the
delivery artifact list. Verify every SHA-256 before review. Verify the original input
packet `private/workflow/packets/IG-1A-34c168acdc5349429ebe64436ef952a4/manifest.json`
and `context.txt`; differences in current generated status/task views caused by workflow
transitions are control-plane updates, not unrecorded product changes. Read only the
architecture/data/mechanics/legal-action documents named in that packet. No game PDF
or real source-derived fixture is required for this technical source-contract task.
The previous blocked candidate remains preserved in attempt-20261012-0540; do not confuse
its failing checks with the current passing delivery. The exception authorizes only
tests/test_workflow.py synthetic baseline initialization.

Account for every IG-1A acceptance criterion and required validation case independently.
Inspect the schema, source validator, identity/hash/reference rules, and synthetic oracle
catalogue. Try to falsify the implementation, including unknown without gap, changed
aspect with old acceptance, changed dependency, model approval, active versus historical
resolution, duplicate identity, opaque/unknown execution claims, group composition,
tables/notes/coordinates, source-profile compatibility, cycle representation, coverage
denominator overlap, scoped/partial review and false freshness. Evaluate whether all
required mechanical concepts are addressable source descriptions without a generic
payload-only claim or prematurely implemented formal/game language. Check the supported
JSON Schema subset against the bundled schema; schema validity alone does not prove
cross-record invariants or meaning. Identify any unsupported or overclaimed behavior.

Confirm separation of import, coverage, source-meaning decisions and executable
readiness. Green validation must not grant semantic acceptance or execution. Review
the proposed IG-3A open decisions and the source-layer limitations, including authority
authentication and dependency-basis completeness. Check that the test expectations are
grounded in architectural contract requirements rather than mirrored implementation.

Inspect any operator-authorized exception recorded in `scope-exception.json` for the
minimal workflow sandbox fixture repair; it must affect only synthetic test state and
must not change the live queue or weaken any assertion. The check-script change must
keep all tests enabled and make its dry-run select a current task without starting one.

Run `pwsh -NoProfile -File scripts/check.ps1` and `git diff --check`. Additional focused
tests should use a fresh `--basetemp` under `private/workflow/` and no external APIs.
Preserve all existing changes. Do not reread histories or older operational evidence.

Write a new immutable review record/report under this task's run area, with severity,
exact file/record/aspect, counterexample, criterion and smallest repair needed. Pin the
entire exact frozen delivery artifact list. Record measured configuration, UTC/wall time,
actual checks/exits, and unavailable token/operator-time data as null. Report independent
technical pass/fail and any remaining risks; this is not SPQR semantic acceptance.
Use workflow transitions only if the operator's review instructions and local review
skill authorize them. Never approve your own changes or mark another task started.
