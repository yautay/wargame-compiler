---
name: wgc-execute
description: Implement one ready WGC task within its declared file scope and produce a tested, frozen delivery for independent review.
---

# wgc-execute

Read the supplied packet and only its named context, plus docs/work/WORKFLOW.md.
Confirm task readiness, input hashes, write ownership and actual model/reasoning evidence.
Claim the task with a checkpoint under private/workflow/runs/<task>/<attempt>/.
Build only the listed deliverables; task exclusions and dependency gates remain binding.
Use synthetic public tests and private source-derived fixtures. Meaningful tests need
source-justified expectations, not merely mirrored implementation assumptions.
Run relevant tests and scripts/check.ps1, freeze file hashes and report unmet criteria.
Hand off for a separate review; never grant yourself semantic acceptance or start the
next task. Resume via checkpoint/hash comparison. Do not load historical gold by default.
