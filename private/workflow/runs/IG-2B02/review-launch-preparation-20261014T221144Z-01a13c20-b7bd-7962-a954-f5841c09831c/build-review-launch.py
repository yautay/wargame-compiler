"""Prepare instruction/pin catalogue only; never execute an independent review."""
import json,hashlib,os
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('C:/repo/wargame-compiler');OUT=Path(__file__).resolve().parent
D='private/workflow/runs/IG-2B02/inventory-20261014T201344Z-reserved-by-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'
P='private/workflow/runs/IG-2B02/preparation-20261014T201344Z-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'
PK='private/workflow/packets/IG-2B02-0851cf2e8efe4e0b818505d7727cb94f'
OLDPK='private/workflow/packets/IG-2B02-46811ecf99cf4834b010368daddf5f08'
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def pin(p):
 raw=(ROOT/p).read_bytes();return {'path':p,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def write(name,obj):
 with (OUT/name).open('x',encoding='utf-8',newline='\n') as stream:json.dump(obj,stream,ensure_ascii=False,indent=2);stream.write('\n')
BODY=r'''IG-2B02 — NEW INDEPENDENT REVIEW SESSION LAUNCH INSTRUCTION

Paste this entire instruction into a manually opened NEW local Codex session in
C:\repo\wargame-compiler, configured for GPT-6.1 Sol (gpt-6.1-sol), reasoning high.
This instruction preparation has not created, configured or launched that session.
Communicate with the operator in Polish. All authored repository/review reports must
be English, explicit UTF-8 without BOM; retain original source/historical bytes.

1. AUTHORITY, INDEPENDENCE AND STOP CONDITION

Use docs/skills/wgc-review/SKILL.md explicitly. Act only as independent technical
inventory reviewer for IG-2B02. The operator authorizes this bounded review and its
new review evidence directory by pasting this instruction. Do not execute a claim,
acceptance, done, changes_requested, blocked or other queue transition. Leave queue
and generated projections unchanged. Stop after frozen review findings and handoff.
The coordinator/operator separately decides repairs, acceptance and subsequent work.

Your session/actor must differ from executor session
01a13c20-b7bd-7962-a954-f5841c09831c and actor
codex-01a13c20-b7bd-7962-a954-f5841c09831c. That executor cannot independently review
its own output. Do not use an executor fork/history as the independent evidence basis.
Record YOUR actual new session ID/actor, own current model/reasoning evidence and UTC.
Confirm gpt-6.1-sol/high from YOUR current session runtime turn_context or direct
operator observation identifying this NEW session. Requested settings, this prompt,
create_thread flags, executor configuration and old configuration files are not proof.
If actual confirmation is unavailable, record model/reasoning as null with reasons,
request the operator's observation and stop substantive review until confirmed.
Own-session metadata access is limited to session_meta/turn_context for identity and
configuration; do not inspect conversations or other sessions. No invented usage/cost.

No archives, Git history, broad probes, neighboring repositories, external APIs or
downloads, agents, chats, automations, global settings, installs, reset/clean/stash,
commit/push, downstream work or gameplay legality decisions using an LLM. Preserve all
existing changes. An ignore file is not a permission barrier. Use scripts/workflow.py
and scripts/search.ps1 for default scoped context/search; do not broaden the named
context to search publisher content. Source/review evidence remains under private/.

2. READ ORDER, CURRENT QUEUE AND FROZEN DELIVERY

Read AGENTS.md, README.md, docs/STATUS.md, docs/HANDOFF.md, docs/work/WORKFLOW.md,
docs/skills/wgc-review/SKILL.md, then the exact FRESH review packet below and its named
context. Also read docs/work/EVIDENCE.md and the selected IG-2B02 record/card. Packet
executor claim/write instructions describe the original implementation; they do not
authorize a reviewer claim or writes to frozen executor scope. This instruction owns
the reviewer-specific scope and stop condition. Read only named delivery metadata and
frozen tooling needed for verification; raw source content stays bounded in section 5.

Use queue.json as sole status authority. Run workflow validate and next. Expected:
IG-2B02 is review; IG-2A and IG-2B01 are done; no other task is active; next reports no
ready task. Do not claim or start another task. Current queue/event pins are below.

The authoritative review event is in_progress -> review at
2026-10-14T21:57:09.490446+00:00 and points to delivery-transition-envelope.json,
SHA256 c02077ee51ff4dc773385942de23fe0f1428ddf7cc038b45a8464e78056c5a19.
It does NOT point to the original delivery.json. That original envelope failed before
any review event because five executable observations were invalid direct artifact
paths. An explicit operator decision authorized one append-only corrected envelope
and retry. The retry succeeded. Old envelope, failure logs, pending checkpoint,
proposal and original manifest remain immutable. Their historical pending statements
are superseded operationally by operator-retry-authorization.json, the actual event,
review-handoff-final.md and final-seal.json. Do not replay any transition or sealing
script. Verify this chain rather than treating authorization text as semantic approval.

Verify before assessment: fresh packet manifest/context and current allowlist payload,
queue/event, approved envelope, original manifest, final seal, final handoff, original
PDF/provenance, accepted baseline/registry, contract/tool pins and every submitted
artifact. Reconstruct fresh packet logical LF payload with the unchanged writer's
physical Windows CRLF behavior; both byte counts/hashes are pinned below. The original
executor packet is an immutable historical input reference, not the current queue
snapshot. Hash its exact saved bytes; do not rebuild it against today's projections.

Verify all arrays independently: approved envelope.artifacts (2895 ordered entries),
original manifest.new_reviewed_artifacts (1462), immutable_inputs_and_old_evidence
(1428), and final seal.postfreeze_recovery_and_epilogue_artifacts (40). Their union has
2930 unique frozen references. Matching byte pins is a gate, not independent review.
Treat arrays/status/counts as assertions to verify, not proof of source completeness.
Retain the exact approved envelope.artifacts list and order in your review record for
future coordinator comparison; do not silently filter, reorder, rebuild or remap it.

Five executable pins remain observations INSIDE frozen toolchain/preflight/manifest
metadata. Hash them at their explicitly pinned local paths; never copy absolute/native
or .venv paths into a workflow artifact array. Mutable_input_snapshot_observations
describe original queue/projection snapshots. Check their declared change policy and
frozen packet basis; do not demand old ready-state views equal current review views.

If any queue/context/input/frozen artifact changed, source/tool drift is found, a
dependency is no longer done or another writer appears, save a new review checkpoint
and request coordinator refresh/triage. Do not use a stale packet or repair inputs.

3. OWNERSHIP AND REVIEW OUTPUTS

After your identity/configuration gate, create exactly one NEW absent review directory:
private/workflow/runs/IG-2B02/review-<ACTUAL_UTC_STAMP>-<YOUR_NEW_SESSION_ID>/
Use the actual UTC format YYYYMMDDTHHMMSSZ; not local time or the executor ID. Record
exclusive ownership. If the directory exists, do not reuse/overwrite it; checkpoint
the conflict and escalate. No writes inside the frozen executor or preparation runs.

Authorized reviewer writes: your exact new review directory, fresh private/workflow/
checks directories generated by required checks, and no other paths. Queue, projections,
source PDF/provenance, all executor inputs/outputs, IG-2A/IG-2B01, src, tests and contracts
are read-only. Do not invoke scripts/workflow.py render or transition. Do not run any
executor script that writes fixed paths, derives new evidence into executor directories,
updates checkpoints or reseals the delivery. Inspect their code as review material.

Write configuration.json and checkpoint.json before review, then checkpoint after every
usable increment/before interruption. Include exact task/actor/session/attempt, current
queue/event and packet path/hash, source/provenance/contract/tool/baseline/registry pins,
base/current owned hashes, completed/unmet criteria, actual commands/exits/stdout/stderr,
UTC/wall time, blocker, retry hypothesis and next operation. Null unknown measurements
with explicit reasons. Preserve every prior attempt and frozen artifact.

Required review outputs within your new directory:
configuration.json; toolchain.json; checkpoint.json; input-hash-audit.json;
page-observations.json; region-review-ledger.json; locator-audit.json;
preservation-audit.json; continuation-audit.json; denominator-audit.json;
replay-report.json; criteria-review.json; findings.json; review.json;
review-manifest.json; review-handoff.md; review-seal.json; exact check logs and your
new original-page/crop/overlay observation evidence. Reports may reference existing
immutable evidence instead of copying it. Every assessed region must be explicit;
do not substitute a sampled inspection or a prose-only “all passed” statement.

4. LOCAL ENVIRONMENT AND PROCESS-ONLY SETUP

Use only existing local/bundled dependencies, bundle 26.1013.11914. Reobserve actual
executable hashes/versions and libraries, compare against frozen toolchain.json, and
record drift before review. Expected Python 3.12.14 (main, Aug 25 2026, 14:01:42)
[MSC v.1944 64 bit (AMD64)]; pypdf 6.10.0, pdfplumber 0.11.9, Pillow 12.3.0,
pytest 9.1.1; pdfinfo/pdftoppm 26.07.0; PowerShell 7.6.5; git 2.56.0.windows.2.
Exact binaries/contracts/tool hashes are in the pin tables/catalogue below. Install
nothing. Reuse unchanged tooling and validators; do not weaken checks or suppress
pypdf Xref warnings. This environment evidence does not confirm your model settings.

PowerShell process setup (do not change global/user configuration):

Set-Location -LiteralPath 'C:\repo\wargame-compiler'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'C:\repo\wargame-compiler\src;C:\Users\yauta\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages'
$env:PATH = 'C:\Users\yauta\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin;' + $env:PATH
$D = 'private/workflow/runs/IG-2B02/inventory-20261014T201344Z-reserved-by-01a13c09-ed4d-7ab2-b967-5e6db69e78b8'

Use repo-relative forward-slash private paths for wgc.sources CLI and persisted artifact
pins. Absolute executable/working-directory command arguments are distinct from safe
private artifact paths. Never serialize Windows backslashes as a private artifact path.
Check and record each command's actual exit separately; stop dependent work on failure.
At most two unchanged retries/repair cycles; record a changed hypothesis before another
attempt. Reproduce bounded tooling failures and escalate without editing tools/tests/
contracts or changing validations. No automatic transition retry is authorized here.
'''
BODY+=r'''
5. SOURCE ACCESS BOUNDARIES — NO SCOPE EXPANSION

Only source authorized: the exact official revision PDF/provenance pinned below under
private/ig/sources/spqr-5e-official/revision-20261013T155212Z/. The generic HANDOFF
source label private/ig/sources/spqr-5e is an older renderer template; do not use/open it.
Review content on physical pages 5, 6, 7, 8 only. Printed labels are separate observations.
Render those original pages afresh in YOUR directory before relying on executor overlays
or ledger classifications. Never render/extract whole unassigned neighboring pages.

Physical page 4: only accepted exact Triarii region
region:ba4a5094-22f5-4a67-8a19-6cc598a17b1b;
key ig2b01:p4:triarii-text-a;
revision 49cc860a420db660e06df00c2d903b80ce40b66e2ee3296732f93df7a68927a0;
normalized box [586601,878787,929738,928030].
Use only its existing text/PNG/crop-PDF, each pinned below, to test the 4->5 continuation.
Do not render whole page 4 or analyze other page-1-4 content. Structural equality/hash
checks of old accepted JSON/evidence are permitted; that is not new content analysis.

Physical page 9: executor reports no access and no unfinished page-8 fragment. Verify
that claim against original page 8. Do not probe page 9 by default. If you independently
observe an unfinished page-8 fragment requiring completion, BEFORE any page-9 content
access record exact originating region ID/revision/box, need, proposed normalized
top-of-corresponding-column crop and maximum TWO lines in your checkpoint/context-access
report. Only that predetermined narrow crop may be inspected as review-only evidence,
with zero denominator and no alteration/allocation in the frozen inventory/registry.
Never render/dump whole page 9 or a neighboring entry. If insufficient or ambiguous,
report the unresolved boundary and seek bounded coordinator refinement before expansion.

Physical pages 10-44: count/geometry validation only; no source text/image content access.
Do not open broad-probe content from prior attempts. Do not recursively load a corpus,
baseline evidence tree or review archive. Byte-hash named references without reading
their source meaning. Cropped PDFs can retain off-crop underlying resources: inspect
only the visible clipped frame, never dump unrestricted page streams/text/images.

6. COMPLETE INDEPENDENT REVIEW, NOT EXECUTOR REPORT CONFIRMATION

A. Original-first physical inventory review
Render every original assigned page independently; inspect both columns, furniture,
notes, examples, bullets, counter illustrations/text/numbers/symbols, callout lines and
legends. Record your observations before comparing ledger proposals. Then examine all
141 new region boundaries and all grouped components against originals and exact crop
evidence. Cover every original page and ledger entry, not a sample or only KB headings.
Detect visible omissions, undescribed grouped components, mislabeled glyphs, clipped
text, neighboring-entry inclusion, unjustified grouping/splits and source-order errors.
Read region-ledger-final.json, author-specifications-final.json and the later component-
observations.json together; verify corrections from source rather than inheriting them.
Superseded drafts/pre-link-correction artifacts are process history, not product targets.

For each assessed region record exact ID/key/revision/page/box, original/crop evidence
pins, group/components, observed result, any uncertainty, and finding references. Record
original-page and component visual evidence in your review directory. Distinguish raw
publisher-derived extraction from independently verified reading. Do not silently repair
hyphens, spaces, typography, Greek/symbol glyphs or counter identifiers. Report literal
anomalies with half-open Unicode codepoint offsets and exact text hash. Source text must
remain unchanged. Empty extraction can be valid for graphics; neither emptiness nor a
PNG grants representation. Assess full-page extraction's column interleaving separately
from the explicit global reading order. Original-first observations are review notes,
not an alternate inventory seed, new accepted IDs or semantic acceptance.

B. Frozen schema, identity, canonicalization and all-page structure
Use the unchanged root validator to reopen the byte-pinned PDF. Independently compare
strict pypdf and Poppler 44-page counts and actual all-page MediaBox/CropBox/effective
crop/rotation/UserUnit without unassigned content extraction. Check source pin before
and after. Check schema, integer-only WGC-C14N-1 revisions, page_basis_hash, key/UUID
bindings, page address, nonoverlapping inventory rectangles, denominator roles, exact
global reading-order membership and links. Reject floats/normalization/remapped identity
in canonical inventory data; operational measurement reports are separate sidecars.

Compare against the exact accepted IG-2B01 full 44-page baseline and persisted registry.
Never reconstruct from IG-2A or a generic full-page inventory. Pages/regions/evidence
1-4 and page records/placeholders 9-44 must remain exact. Preserve all old registry
entries, old links and relative old reading order. Only four page-5-8 placeholder
MEMBERSHIPS retire; their registry entries remain. All new inventory regions must have
explicit author-chosen ig2b02 keys and persisted UUIDs, not text/array/coordinate/hash-
based identity. Page IDs/keys/physical addresses/source revision/geometry remain exact.
Changed nested/top revisions are recomputed; unchanged records retain their revisions.
Current printed label evidence must come from that same physical page. No split/merge
may silently transfer review/acceptance; record any lineage issue as a finding.

C. Exact locator and derivation audit for every new region
Audit every new text/PNG/crop-PDF triple: source hash, PDF page, region ID/revision/box,
frame, page_basis_hash, artifact SHA256/bytes, exact rational native crop bounds,
crop MediaBox/CropBox, rotation and UserUnit normalization, 144-DPI Poppler rendering,
engine/version parameters, predicted AND actual PNG dimensions with no one-pixel
tolerance, raw UTF-8 bytes and half-open Unicode codepoint offsets. Expected 141 new
locators and 423 primary evidence files; check these independently. Reproduce rendering
and raw clipped extraction in fresh reviewer directories and compare exact bytes. Do
not forge freshness pins, normalize raw text or modify old evidence references.
Do not run the generic CLI evidence command for pages 5-8: it also selects the retained
old page-5 context. If using extract_evidence, inspect/use the unchanged library only
for exact new assigned IDs into YOUR fresh outputs, and never create old-ID evidence.
Its returned output pins differ in directory path; compare artifact bytes/derivation
basis, not a forced equality of path strings. Re-rendering an existing exact crop and
reextracting its clipped frame is an allowed independent locator test.

D. Preservation, continuations and old-context/new-authored correspondence
The retained page-5 context is exactly:
region:e8d77349-41ce-47d0-b678-eab1d0c8e8ed;
key ig2b01:context:triarii-tail;
revision af2a41ef3c500858f945d9a813c185f8ca3bc6fbc142e61348e6da5964d011c1;
page ID page:9df6cbac-0930-49e6-9b41-a936a9b55f73;
box [71895,63131,495099,98485].
It remains unchanged context, zero denominator, with old evidence, membership, reading-
order occurrence and prior page-4 link. Independently verify the distinct authored
page-5 tail ID/revision/box and exact source-observed correspondence from correspondence
report and original page 5. Never promote/remap context or inherit its review/coverage.
Verify the newly added continuation, preserved old link, page-5->6 Light Cavalry join,
same-page rule-4.32 column continuation, wrapped prose links and note/illustration links.
Check source-observed exact text rather than the initially erroneous superseded Triarii
link description. No neighboring content may be imported to resolve a review finding.

E. Counts, gaps and distinct readiness gates
Verify task counts 39/33/39/30 on physical pages 5/6/7/8: 141 new inventory regions.
Full denominator: 130 preserved authored + 36 unchanged unprocessed placeholders +
141 new = 307. One retained context region contributes ZERO task/full inventory units.
Grouped counter/diagram components are documented inside a region, not duplicate units.
These arithmetic assertions do not prove grouping or source completeness; report source
omissions or invalid groupings even when counts match. Compare 16 unit-counter diagram
regions and one annotated leader-counter region against originals; verify rather than
assume “no standalone table” or any classification claim. Inspect exact geometric
complement independently, sum integer trillionths and separate it from content and
transcription/descriptive/formal representation gaps.

All 141 new transcription statuses are partial; new descriptive/formal semantics are
unprocessed. Check explicit reasons/gaps and absence of unsupported represented/excluded
promotions. A bbox, PNG, extraction or editorial classification is not represented
coverage or approved exclusion. Sidecar partition hashes cannot substitute for frozen
IG-1A exact whole-record region targets and whole-inventory review bases. Technical
inventory review, source authenticity, human semantic acceptance, semantic reconciliation
and executable readiness remain separate. Never resolve gameplay legality using an LLM.

F. Replay, generation code and process/recovery evidence
Inspect generation/extraction/audit/report scripts and failed attempts within the exact
submitted scope. Check expectations against independent source observations; passing
validator/tests or executor “all viewed” booleans alone do not prove completeness.
Review evidence for the recorded environment/newline errors, repaired boundary overlaps,
Triarii link correction and small-counter component corrections. Check that frozen
tools/tests/contracts were not changed and unrelated changes stayed intact. Reproduce
only source-justified checks; do not perform broad Git/archival comparisons.

Independently replay authoring with the persisted EXTENDED authored registry and explicit
final specifications into two fresh directories owned by you. Compare exact canonical
authored inventory/registry bytes and IDs with pinned authored outputs. Do not reseed
UUIDs, allocate replacements, promote outputs or rebuild source structure. The frozen
author.py joins its destination to executor A: if you use it, inspect it first and pass
an ABSOLUTE destination under your review directory named replay-author-1/replay-author-2
(never basename authored). A relative review destination would wrongly write inside
executor scope. Never invoke other executor main scripts with fixed output paths.
If replay cannot be made safely within authorized scope, report the precise blocker.
'''
BODY+=r'''
7. REQUIRED COMMANDS AND INDEPENDENT OUTPUTS

Run these only AFTER actual new-session configuration/identity confirmation. Capture
each real command, exit, stdout/stderr, start/end UTC and wall time in your own reports.
The supplied byte/status helper is optional to implement yourself but its complete
checks are mandatory; its exact path/hash appears in the table below. It reads named
pins only, writes the supplied fresh report and performs no source-content inspection.
It does not count as your independent review. Inspect its code before using it.

Create fresh ownership (after your actual configuration is confirmed):

$reviewSessionId = $env:CODEX_SESSION_ID
if (-not $reviewSessionId -or $reviewSessionId -eq '01a13c20-b7bd-7962-a954-f5841c09831c') { throw 'A verified NEW independent session identity is required.' }
$reviewStamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
$reviewRelative = 'private/workflow/runs/IG-2B02/review-' + $reviewStamp + '-' + $reviewSessionId
$reviewRoot = [IO.Path]::GetFullPath((Join-Path 'C:/repo/wargame-compiler' $reviewRelative))
if (Test-Path -LiteralPath $reviewRoot) { throw 'Review attempt must be new; never overwrite an existing attempt.' }
New-Item -ItemType Directory -Path $reviewRoot | Out-Null

Record configuration.json, exclusive ownership and your initial checkpoint before
substantive work. Define $reviewActor from YOUR observed identity. The metadata/actor
fact must be true; these variable assignments do not independently establish it.
Run the explicitly pinned byte/status helper below with --report set to
($reviewRelative + '/input-hash-audit.json'). Verify both the helper and preparation
metadata hashes before execution. If writing your own verifier, persist/hash its code.

Required structural validation:

.\.venv\Scripts\python.exe -B scripts/workflow.py validate
.\.venv\Scripts\python.exe -B scripts/workflow.py next
.\.venv\Scripts\python.exe -B -m wgc.sources validate "$D/final-verified/inventory.json"

Original source renders (new reviewer output only; no page-4/9 whole-page render):

$reviewOriginals = Join-Path $reviewRoot 'originals'
New-Item -ItemType Directory -Path $reviewOriginals | Out-Null
$reviewSourcePdf = 'private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'
& 'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.EXE' -f 5 -l 8 -cropbox -r 144 -png $reviewSourcePdf (Join-Path $reviewOriginals 'original')

Independently inspect all four originals and every ledger region/component; then derive
your own exact overlays/crop comparisons under your review directory and audit locators.
Record each region/page outcome with actual viewed evidence, not fabricated viewing
timestamps, a blanket assertion or executor self-inspection copied as your own.

After inspecting author.py and confirming destination behavior, safe persisted-registry
replays (destinations must be ABSOLUTE and new, basename must not be authored):

$reviewReplayOne = Join-Path $reviewRoot 'replay-author-1'
$reviewReplayTwo = Join-Path $reviewRoot 'replay-author-2'
.\.venv\Scripts\python.exe -B "$D/author.py" $reviewReplayOne "$D/authored/identity-registry.json"
.\.venv\Scripts\python.exe -B "$D/author.py" $reviewReplayTwo "$D/authored/identity-registry.json"

Compare each replay inventory/registry file's exact bytes/SHA256 with the pinned authored
counterpart and record all identity bindings. Do not run any fixed-path derivation,
finalize, audit, freeze, recovery or sealing main script from the executor attempt.

Unchanged source tests with fresh SHORT basetemp and no cacheprovider:

$reviewBaseTemp = 'C:/repo/wargame-compiler/private/workflow/checks/rv-b02-' + [guid]::NewGuid().ToString('N').Substring(0,12)
if (Test-Path -LiteralPath $reviewBaseTemp) { throw 'Test basetemp must be new.' }
.\.venv\Scripts\python.exe -B -m pytest -q tests/sources --basetemp $reviewBaseTemp -p no:cacheprovider --tb=short
& 'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.EXE' -NoProfile -File scripts/check.ps1 -Task IG-2B02
.\.venv\Scripts\python.exe -B scripts/workflow.py validate
git diff --check

Original executor observations were 71 source tests and 102 full-suite tests passing;
verify your own current results, do not copy exits/counts. Check resulting logs and the
fresh check result.json. Synthetic temporary test fixtures are permitted within fresh
private check directories; tests may simulate transitions there, never the real queue.
Retain visible Xref/line-ending warnings and record real failures. Existing whole-repo
working changes are not this review's implementation diff; check delivered byte targets
against their exact accepted baseline and script/contract pins, without Git history.

8. FINDINGS, FREEZE, HANDOFF AND FINAL STOP

For every finding record stable finding ID, severity, precise artifact/path and
region ID/revision/page/box or raw text offset, observed source/evidence pins,
expected contract/source behavior, consequence, smallest repair scope and required
verification. Distinguish blocking inventory/source/identity/evidence defects from
advisory transcription or process observations; never call a material omission
nonblocking solely because extraction/tests pass. Explicitly record uncertain readings
and unavailable checks. Report all criteria, including unreviewed/unmet ones.

Your review.json must have role reviewer, YOUR independent actor/model/reasoning and
configuration evidence, summary, exact current task acceptance criteria in original
order, per-criterion results, findings references, actual checks, review scope/limits,
UTC/wall measurements and explicit null reasons for unavailable tokens/cost/operator
time. artifacts must equal the approved event envelope.artifacts EXACTLY, same list/
order/pins; attach YOUR new reports via separate review_outputs/review_manifest fields.
Possible technical result: no_blocking_findings, changes_recommended or review_incomplete.
Do not use a queue acceptance/done decision or fabricate human/source-meaning authority.
If a required check failed, retain its nonzero exit and mark affected review incomplete;
do not present a passing gate by omitting the failure. Owner semantic decision is absent.

Freeze review-manifest.json with every new reviewed report, observation/script, check
command/stdout/stderr and original/crop/overlay proof, plus exact reviewed delivery/input
references. Define self-exclusion/cycle policy explicitly. review.json pins the manifest
and reviewed target list; review-handoff.md explains every met/unmet criterion, all
findings/defects, continuation limits, literal uncertainties and scope/readiness gaps.
Keep authored/delivery artifacts immutable; do not edit executor criteria.json to clear
its historical pending criterion. Your separate complete independent review can assess
criterion 5 in your own report only; coordinator then evaluates that fresh evidence.

Before review-seal.json, reverify input hashes, real queue status/event and all delivered
artifacts again, and confirm your writes were confined to the new review/check scope.
Record the final exact review.json/manifest/handoff/report hashes and command exits.
Do not overwrite sealed files or old attempts. If repair is recommended, do not repair
it; hand scoped findings to the coordinator. If blocked, checkpoint evidence and the
smallest missing fact/scope refinement; do not change real task status yourself.

STOP. Leave IG-2B02 in review. Do not grant accepted/done, semantic acceptance,
whole-record source-IG review or executable readiness. Do not start IG-2B03, send other
chats messages, create a session/agent/automation or call an external API. Return the
fresh independent identity/configuration proof, exact reviewed delivery and review
paths/hashes, complete criterion/findings matrix, actual checks and coordinator handoff.

9. EXACT PINNED INPUTS — FULL REPO-RELATIVE PATHS

Every row below is SHA256 of the exact file bytes plus actual byte count. These are
the launch gates, not a substitute for verifying the complete frozen artifact arrays.
The separate frozen-pins.json catalogue contains their complete unique union. Executable
observation paths are local hash inputs only, not workflow artifact references.
'''

if __name__=='__main__':
 prep=load(OUT.relative_to(ROOT).as_posix()+'/preparation.json');queue=load('docs/work/queue.json');task=next(t for t in queue['tasks'] if t['id']=='IG-2B02');assert task['status']=='review' and pin('docs/work/queue.json')==prep['queue']
 envelope=load(D+'/delivery-transition-envelope.json');manifest=load(D+'/delivery-manifest.json');seal=load(D+'/final-seal.json');scope=load(P+'/scope.json')
 controls=[PK+'/manifest.json',PK+'/context.txt','docs/work/queue.json','docs/skills/wgc-review/SKILL.md',OUT.relative_to(ROOT).as_posix()+'/preparation.json',OUT.relative_to(ROOT).as_posix()+'/verify-frozen-review-inputs.py']
 core=['delivery-transition-envelope.json','delivery-manifest.json','final-seal.json','review-handoff-final.md','delivery.json','delivery-handoff.md','operator-retry-authorization.json','authored/inventory.json','authored/identity-registry.json','final-verified/inventory.json','final-verified/identity-registry.json','final-verified/coverage.json','region-ledger-final.json','scope-report-final.json','context-authored-correspondence.json','continuations.json','uncertainty.json','gaps.json','geometric-gaps.json','visual-inspection.json','locator-audit.json','replay-report.json','preservation-report.json','criteria.json','configuration.json','toolchain.json','required-checks.json']
 controls += [D+'/'+name for name in core]
 controls += [P+'/scope.json',P+'/contract-boundaries.md',P+'/source-pins.json',P+'/dependency-verification.json',P+'/toolchain.json',OLDPK+'/manifest.json',OLDPK+'/context.txt',scope['baseline']['path'],scope['registry']['path'],'private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf','private/ig/sources/spqr-5e-official/revision-20261013T155212Z/provenance.json']
 controls += [scope['continuation_context']['page_4']['evidence'][0][key]['path'] for key in ('text','image','crop_pdf')]
 controls += ['contracts/ig/regions.schema.json','contracts/ig/source.schema.json','contracts/ig/README.md','src/wgc/contracts/source.py','src/wgc/sources/README.md','src/wgc/sources/__init__.py','src/wgc/sources/__main__.py','src/wgc/sources/geometry.py','src/wgc/sources/inventory.py','src/wgc/sources/pdf.py','scripts/workflow.py','scripts/check.ps1','scripts/search.ps1']
 controls=list(dict.fromkeys(controls));rows=[pin(p) for p in controls];allpins={p['path']:p for p in rows}
 for group in (envelope['artifacts'],manifest['new_reviewed_artifacts'],manifest['immutable_inputs_and_old_evidence'],seal['postfreeze_recovery_and_epilogue_artifacts']):
  for p in group:
   if p['path'] in allpins:assert allpins[p['path']]==p
   allpins[p['path']]=p
 write('frozen-pins.json',{'format':'wgc-review-launch-pins-1','task':'IG-2B02','authoritative_review_event':task['events'][-1],'launch_gate_pins':rows,'all_unique_frozen_refs_and_launch_controls':list(allpins.values()),'approved_ordered_artifact_list':envelope['artifacts'],'source_content_scope':'Physical pages 5-8; exact page-4 Triarii crop only; page 9 conditional maximum-two-line predeclared crop; pages 10-44 geometry/count only. Byte hashing other exact named references is not content inspection.','policy':'This catalogue is preparation only, not independent review or acceptance. Binary observations are not direct workflow artifact paths.'})
 text=BODY+'\nPATH | BYTES | SHA256\n'+'\n'.join(p['path']+' | '+str(p['bytes'])+' | '+p['sha256'] for p in rows)+'\n'
 catalogue=pin(OUT.relative_to(ROOT).as_posix()+'/frozen-pins.json')
 text+='\nComplete frozen/input catalogue: '+catalogue['path']+'\nSHA256 '+catalogue['sha256']+'; '+str(catalogue['bytes'])+' bytes.\n'
 helper=OUT.relative_to(ROOT).as_posix()+'/verify-frozen-review-inputs.py'
 text+='\nPinned byte/status helper command (reviewer output only):\n.\\.venv\\Scripts\\python.exe -B '+helper+' --report ($reviewRelative + "/input-hash-audit.json")\n'
 text+='\nFresh packet: '+str(prep['packet_context']['bytes'])+' physical CRLF bytes; '+str(prep['packet_logical_text_bytes'])+' logical LF bytes. Queue SHA256 '+prep['queue']['sha256']+'.\n'
 text+='\nExact task acceptance criteria, preserve order in review.json:\n'+'\n'.join(str(i)+'. '+c for i,c in enumerate(task['acceptance'],1))+'\n'
 text+='\nPreparation observed status/event and hashes only. Independent review not performed. No session created, queue transition or acceptance granted.\n'
 with (OUT/'independent-review-launch.txt').open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)
 current_sid=os.environ.get('CODEX_SESSION_ID');configuration={'session_id':current_sid,'actor':'codex-'+current_sid if current_sid else None,'model':None,'reasoning':None,'reason':'Own current runtime metadata not yet observed in this preparation command.'}
 if current_sid=='01a13c20-b7bd-7962-a954-f5841c09831c':
  meta=Path('C:/Users/yauta/.codex/sessions/2026/10/14/rollout-2026-10-14T22-35-39-'+current_sid+'.jsonl');last=None
  for raw in meta.read_bytes().splitlines():
   record=json.loads(raw)
   if record['type']=='turn_context':last=(record,hashlib.sha256(raw).hexdigest())
  if last:
   record,sha=last;configuration.update(model=record['payload'].get('model'),reasoning=record['payload'].get('effort'),reason=None,evidence={'kind':'Own current session turn_context','timestamp':record['timestamp'],'sha256':sha,'metadata_path':meta.as_posix()})
 configuration['role']='Review launch preparer, not independent reviewer; same actor as executor';write('preparer-configuration.json',configuration)
 write('launch-delivery.json',{'role':'instruction_preparer','actor':configuration['actor'],'task':'IG-2B02','created_utc':datetime.now(timezone.utc).isoformat(),'actual_preparer_configuration':configuration,'instruction':pin(OUT.relative_to(ROOT).as_posix()+'/independent-review-launch.txt'),'catalogue':catalogue,'helper':pin(helper),'verification':pin(OUT.relative_to(ROOT).as_posix()+'/frozen-delivery-verification.json'),'queue_pin':prep['queue'],'review_event':task['events'][-1],'new_independent_session_created':False,'independent_review_performed':False,'task_status_changed':False,'acceptance_granted':False,'next_operation':'Operator manually opens a NEW local GPT-6.1 Sol/high session and pastes the complete instruction; that reviewer verifies actual configuration and saves a bounded independent review only.'})
 print(json.dumps({'instruction':pin(OUT.relative_to(ROOT).as_posix()+'/independent-review-launch.txt'),'catalogue':catalogue,'helper':pin(helper),'queue_unchanged':pin('docs/work/queue.json')==prep['queue']},indent=2))
