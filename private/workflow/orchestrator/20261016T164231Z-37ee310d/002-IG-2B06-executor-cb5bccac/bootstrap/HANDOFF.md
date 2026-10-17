# WGC handoff

<!-- Generated from docs/work/queue.json. -->

Next ready task: **IG-2B06**. Choose one task; do not execute a whole stage.
Read [workflow](work/WORKFLOW.md), then use [operator prompts](work/PROMPTS.md).

```powershell
pwsh -NoProfile -File scripts/check.ps1
.\.venv\Scripts\python.exe scripts/workflow.py next
.\.venv\Scripts\python.exe scripts/workflow.py packet --task IG-2B06
```

The packet lists exact context and hashes. It does not launch a model or claim the task.
Use the staged [execution skill](skills/wgc-execute/SKILL.md) explicitly; automatic
installation is pending. Operator selects GPT-6.1 Sol/high, records actual settings,
and follows claim → implementation → independent review → repair → acceptance → done.
Checkpoints and evidence live in private/workflow/runs; preserve prior attempts.

The active SPQR PDF is in private/ig/sources/spqr-5e with verified provenance.
The WGU inspection is input evidence, not a semantic acceptance or an exact current count.
Neighbouring KB/WGU repositories are read-only. Required scenarios/options, missing
materials, authorized semantic reviewer and performance hardware/thresholds must be
pinned in the tasks that need them; they do not prevent the first source-contract task.

External history relocation remains governed by [the archive register](ARCHIVES.md)
and the queue infrastructure blockers. No archive content is needed for this packet.
Do not use old prompts, archived operational approvals or Git history as default context.
