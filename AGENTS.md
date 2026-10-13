# WGC repository instructions

Write repository content in English; preserve source and historical bytes.
Read README.md, docs/STATUS.md, docs/HANDOFF.md, then the selected task packet.
Use docs/work/queue.json as the only queue/status authority. Follow
docs/work/WORKFLOW.md and only the relevant local skill in docs/skills/.

Build the full SPQR product incrementally; no new POC. Import, coverage, semantic
acceptance, and executable readiness are separate. Never resolve gameplay legality
with an LLM. Human semantic acceptance is separate from model/code review.

Default context and search use scripts/workflow.py and scripts/search.ps1.
History (including Git history) needs an explicit operator scope and purpose;
see docs/ARCHIVES.md. An ignore file is not a read permission barrier.

Preserve existing changes; no reset, clean, stash, commit, push, global configuration,
new chats, agents, automation, or external APIs unless the current operator requests them.
Keep game evidence under private/. Do not modify neighbouring repositories.
Run scripts/check.ps1 and git diff --check. Record actual model/reasoning evidence;
unknown is not the requested GPT-6.1 Sol/high configuration.
