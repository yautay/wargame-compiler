---
name: wgc-queue
description: Coordinate the WGC task queue, context packets, handoffs, refinement and blockers; use when managing work rather than implementing a task.
---

# wgc-queue

Read docs/work/WORKFLOW.md and the selected record in docs/work/queue.json.
Run scripts/workflow.py validate and next; refine tasks before making them ready.
Use packet to prepare only allowlisted context. Keep statuses and task content in the
queue, then render derived views. Record transition evidence, checkpoint ownership and
independent review; do not invent semantic acceptance or launch sessions automatically.
For blockers prepare the smallest decision using docs/work/PROMPTS.md. Historical
access requires explicit scope and purpose under docs/ARCHIVES.md. Preserve prior attempts.
