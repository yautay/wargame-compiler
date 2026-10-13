# Run evidence examples

These are shapes for operator/executor records, not evidence of a completed task.
Save each attempt under `private/workflow/runs/<task>/<attempt>/`. Never overwrite a
previous attempt or fabricate model settings, checks, reviewer identity or owner decisions.

A checkpoint records task/attempt, input packet path/hash, source revisions, base and
current hashes of owned files, completed criteria, commands/exits, current blocker,
and the next exact operation. Keep actual model/reasoning and observed token counts
null with a reason until verified. Do not include secrets or unrelated session history.

An executor claim may reference the checkpoint as its first artifact. A delivery manifest
lists every changed product/test/contract file submitted for review plus relevant reports;
it must not be limited to a prose summary. Hash the bytes actually reviewed. Independent
review and coordinator acceptance reference that same frozen artifact list.

```json
{
  "role": "executor",
  "actor": "operator-assigned-session-identity",
  "summary": "Describe the concrete claim or delivery",
  "model": null,
  "reasoning": null,
  "configuration_evidence": "Unknown until confirmed by runtime metadata or operator UI observation",
  "criteria": ["Copy the exact acceptance criteria covered by this evidence"],
  "artifacts": [
    {"path": "private/workflow/runs/IG-1A/attempt-1/checkpoint.json", "sha256": "replace-with-computed-hash"}
  ],
  "checks": [
    {"command": "replace-with-actually-run-command", "exit_code": null}
  ],
  "measurement": {
    "started_utc": null,
    "ended_utc": null,
    "wall_seconds": null,
    "operator_seconds": null,
    "input_tokens": null,
    "output_tokens": null,
    "unknown_reason": "Not observed in this example"
  }
}
```

This example intentionally cannot claim a task or pass a delivery gate. Fill measured
values and hashes first. For an in-progress claim, confirmed model must be `gpt-6.1-sol`
and reasoning `high`. For accepted, role is reviewer with a distinct identity, all exact
task criteria, matching delivery artifacts and passing checks. For done, role is coordinator.

A task requiring semantic acceptance additionally references `semantic_decision`, the
path of an immutable JSON record with role human_owner or human_reviewer, actor,
authorization evidence, exact targets/revisions/aspects, basis, decision accepted, and
decision_artifact pointing to the actual human statement. The tool checks structure and
hashes; it does not authenticate people. The coordinator must verify the recorded
authority and scope against the real statement. Model-authored approval is invalid.

```powershell
.\.venv\Scripts\python.exe scripts/workflow.py transition --task IG-1A --to in_progress --evidence private/workflow/runs/IG-1A/attempt-1/claim.json
```

The example command is for a future executor session. No transition was made to the
real implementation queue during plan preparation. Synthetic transition tests use
temporary copies and leave the real queue unchanged.
