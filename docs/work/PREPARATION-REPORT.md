# Preparation report — 2026-10-11

This records the planning session's result, not live task status. Use queue.json for
the current queue. No product implementation, model execution, new chat, subagent,
automation, external API call, commit or push was started.

## Delivered

- English active architecture, data and mechanical contracts, implementation plan,
  legal-action requirements and short AGENTS/CLAUDE instructions.
- One canonical JSON queue with 39 tasks: 5 import/contract tasks, 14 inventory and
  reconciliation tasks, 8 semantic tasks, 9 runtime/compiler/update/performance tasks,
  and 3 player/strategy/release tasks. Cards and status views are generated and checked.
- Sequential workflow with independent review, separate human semantic acceptance,
  scoped writes, checkpoints, interruption recovery, bounded retries and honest metrics.
- Four operator prompts and three repository-local staged skills. Explicit skill paths
  work without auto-discovery; no global installation was performed.
- Local queue/context/search/check tools and an explicitly invoked archive relocation,
  verification and restore tool. These tools do not implement IG or game mechanics.
- A verified active copy of the SPQR 5E PDF with provenance, so source work does not
  require historical access. Identity with WGU's missing original remains unknown.

## Verification evidence

| Check | Observed result |
|---|---|
| scripts/check.ps1 | Exit 0; 23 tests passed in 39.53 seconds |
| Queue and projections | 39 task cards, acyclic dependencies, required criteria, scoped context and matching derived views |
| Dry run | IG-1A packet; 11 files; 46,723 text bytes; no measured token count; real queue unchanged |
| Synthetic orchestration | Claim, delivery, separate reviewer, acceptance and done; self-review, skipped review, altered delivery, missing human decision and invalid resume rejected |
| Default search and context | Default rg excludes history; packet test works in a workspace with no archives |
| Archive tool on synthetic data | Copy/hash/restore/removal passed; changed source, existing batch, corrupted copy and existing restore destination rejected |
| Explicit real source integrity | All 56,150 files match relocation inventory sizes and SHA-256; source set complete |
| Prior manifest audit | POC 3,117 entries, pre-POC payload and two restore copies of 392 entries, and 22 preserved planning files match; eight pre-existing public legacy variants recorded separately |
| PDF promotion | Copied bytes match e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e |
| git diff --check | Exit 0; line-ending notices do not indicate a whitespace failure |
| Skill checks | Local frontmatter/routing checks passed; bundled quick_validate.py blocked by missing PyYAML |

Routine logs: `private/workflow/checks/active-c7637f4098c24e1a9b2286f1de9a7052/`.
Archive audit: `private/workflow/archive-audit.json`.
Relocation manifest SHA-256:
`42f9d921257f0313acefbb090bd018927be1f837740c52d2f99c20649b87c515`.
Final packet prepared at
`private/workflow/packets/IG-1A-4bc3623cf8f343498c5fdd2b1ebedb25/`.
Regenerate packets after context or queue changes; never reuse stale file hashes.

## Outstanding conditions

**External archive migration is not complete.** The requested destination is outside
this session's writable roots and its approval policy is never. No bypass was attempted
and no archive originals were removed. The eight legacy variants were preserved together
with verified original bytes; no historical result was repaired or normalized. The full
external copy and restore rehearsal must still be run in a permitted session.

**Automatic skill installation/discovery is not complete.** `.agents` is protected
read-only here. The skill-creator checker also needs PyYAML, which neither available
Python runtime provides. Use the explicit staged paths now; install and verify discovery
when permissions allow. See [skills](SKILLS.md) and [environment evidence](ENVIRONMENT.md).

**Isolation is partial while history remains physically present.** The packet builder
enforces its own allowlist; ripgrep and pytest have verified defaults. These do not deny
arbitrary file reads, other indexers or Git history. No model-wide read prohibition was
configured. See [archive access](../ARCHIVES.md) for the operator's remaining migration.

The exact architect model/reasoning is unknown, not inferred from the recommended
Astra/high prompt. The future executor target is Sol/high and must be confirmed on claim.
Later tasks must pin the playable scenario/options, missing compatible materials,
human reviewer authority, and measured hardware/performance/context thresholds.
They do not prevent the first source-contract increment, IG-1A.

Start via [operator prompts](PROMPTS.md) and [the workflow](WORKFLOW.md). This preparation
does not authorize starting implementation in the current session.
