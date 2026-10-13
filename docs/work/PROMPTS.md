# Operator prompts

Run local checks, choose a task, and generate its packet before pasting one prompt.
Replace bracketed IDs/paths with the command output. These prompts never start sessions.
Repository outputs are English. The operator may converse in Polish.

## Next implementation task

```text
Work locally in C:\repo\wargame-compiler. Use GPT-6.1 Sol, reasoning high.
Verify the actual session configuration; record unknown if not observable and do not
claim it matches merely because this prompt requests it.
Read AGENTS.md and docs/skills/wgc-execute/SKILL.md, then the exact packet [packet path].
Implement only [task ID] from docs/work/queue.json. Check readiness and input hashes,
record the claim/checkpoint, then produce its lasting deliverables and required tests.
Use English in the repo. Preserve unrelated changes. Do not read archives or Git history,
create agents/chats/automations, call external APIs, commit or push unless separately asked.
Do not implement downstream tasks. Stop at a frozen delivery ready for independent review.
Report criteria, tests, hashes, actual configuration, measurements and next action.
```

## Independent review

```text
Review [task ID] independently in C:\repo\wargame-compiler using GPT-6.1 Sol/high.
Read AGENTS.md, docs/skills/wgc-review/SKILL.md, its packet and frozen delivery [path].
Verify delivered hashes and report your actual configuration and separate reviewer identity.
Check the contract, owned diff, failure cases and evidence behind expected test outcomes.
Distinguish code review, source-meaning observations, and human semantic acceptance.
For rule work inspect exactly the assigned source pages/IDs; no historical gold by default.
Report actionable findings with location, consequence, evidence and required validation.
Do not edit implementation, invent human approval, or mark the task done. Save a review
artifact for the coordinator. No agents, APIs, commits or pushes.
```

## Resume after interruption

```text
Resume [task ID], attempt [attempt], from [checkpoint path] in C:\repo\wargame-compiler.
Read AGENTS.md, docs/skills/wgc-execute/SKILL.md, current task packet and checkpoint.
Confirm actual configuration, dependencies, ownership, source and work-file hashes.
Preserve all existing work. Reconcile differences before continuing; do not reset/clean/stash.
Reuse verified completed work. Run only checks justified by changes or unresolved failures.
If the same blocker remains, preserve it and report the smallest resolution needed.
Continue only the remaining criteria of this task, then freeze delivery for separate review.
```

## Handle a blocker

```text
Triage blocker [blocker/evidence path] for [task ID]. Use docs/skills/wgc-queue/SKILL.md.
Read only the card, checkpoint and evidence necessary for this blocker.
State the missing fact, affected criteria, attempted remedies and remaining retry allowance.
Prepare the smallest concrete options/decision for the owner if needed; do not guess rule
meaning, lower acceptance criteria or expand filesystem permissions.
If new evidence resolves it, record why, transition blocked -> planned, recheck dependencies
and context, then prepare the next packet. Do not launch an executor or perform product work.
```
