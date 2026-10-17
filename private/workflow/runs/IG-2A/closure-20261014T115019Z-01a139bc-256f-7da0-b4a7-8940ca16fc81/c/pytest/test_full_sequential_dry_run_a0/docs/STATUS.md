# WGC status

<!-- Generated from docs/work/queue.json. -->

Queue updated: 2026-10-14. Next ready task: **none**.
Done tasks: 1/1.
The planning tools do not certify game behavior. Source import, source coverage,
human semantic acceptance, compilation and gameplay readiness are separate gates.

Requested planning configuration: GPT-6 Astra/high. Recorded actual model/reasoning:
unknown/unknown.
Future executor target: GPT-6.1 Sol/high; verify its actual configuration at claim time.

## Infrastructure blockers

- ARCHIVE-WRITE: blocked. Destination outside writable roots; approval_policy=never. No originals removed. Operator runs the prepared verified migration in a session with write permission to C:/repo/wargame-compiler-archive.
- SKILL-INSTALL: blocked. .agents is read-only in this session; skills are staged in docs/skills. Use explicit skill paths in prompts now; install and verify discovery in a permitted session.

See [handoff](HANDOFF.md), [workflow](work/WORKFLOW.md), [archive register](ARCHIVES.md)
and [environment evidence](work/ENVIRONMENT.md). No inherited commit/push approval exists.
