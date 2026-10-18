# Wargame Compiler

WGC turns a WGU knowledge base and complete source materials into an evidence-backed
Instruction Graph, formal rule semantics, a compiled rules package, and deterministic
legal actions and state transitions. A future AI opponent spends its context on
strategy and chooses through a compact player interface. Gameplay legality never
requires an LLM call.

The product target includes the **entire SPQR 5E core rulebook from the start**.
Incremental tasks build lasting parts of that product. No further POC is planned.
There is currently no new importer, compiler, game runtime, or AI opponent.

Start with [status](docs/STATUS.md), [handoff](docs/HANDOFF.md), and the
[workflow](docs/work/WORKFLOW.md). The only task/status source of truth is
[queue.json](docs/work/queue.json); [roadmap](docs/ROADMAP.md) and task cards are generated.

- [Architecture](docs/IG-WGU-ARCHITECTURE.md), [data contracts](docs/IG-DATA-MODEL.md),
  [mechanics and profiles](docs/IG-MECHANICS-PROFILES.md), [legal action contract](docs/IG-LEGAL-ACTIONS.md).
- [Implementation plan](docs/IG-PLAN.md), [operator prompts](docs/work/PROMPTS.md),
  [local skills](docs/work/SKILLS.md), [environment evidence](docs/work/ENVIRONMENT.md).
- [Archive locations and explicit access](docs/ARCHIVES.md).

Repository prose and tooling use English. Publisher text, imported KB data, and
immutable historical records retain their original language and bytes. Game content,
source documents, positions, and source-derived examples belong in `private/`.

```powershell
pwsh -NoProfile -File scripts/check.ps1
.\.venv\Scripts\python.exe scripts/workflow.py next
.\.venv\Scripts\python.exe scripts/workflow.py packet --task IG-1A
```

The packet command prepares local context; it does not start a model or change task
state. Checks validate planning and workflow, not the unimplemented game's correctness.
Archive integrity is an explicit separate command, never part of routine checks.

To restore the IG-2 checkpoint on another Windows computer, follow
[IG-2 environment restore and resume](docs/work/IG2-RESTORE.md). Run its input audit
and model-free preflight before starting the supervisor with a local host binding.
