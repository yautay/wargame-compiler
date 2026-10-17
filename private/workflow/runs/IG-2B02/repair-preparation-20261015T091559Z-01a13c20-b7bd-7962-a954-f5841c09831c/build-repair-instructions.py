"""Create complete future repair/coordinator/rereview instructions, not a repair."""
import json,hashlib,copy
from pathlib import Path
R=Path('C:/repo/wargame-compiler');P=Path(__file__).resolve().parent;PR=P.relative_to(R).as_posix()
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def pin(p):
 raw=(R/p).read_bytes();return {'path':p,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def write(name,obj):
 with (P/name).open('x',encoding='utf-8',newline='\n') as stream:json.dump(obj,stream,ensure_ascii=False,indent=2);stream.write('\n')
def textfile(name,text):
 with (P/name).open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)
state=load(PR+'/preparation.json');D=state['original_delivery_directory'];V=state['independent_review_directory'];A=state['reserved_absent_repair_attempt'];scope=load(PR+'/repair-scope.json');proposal=load(PR+'/coordinator-queue-patch-v2.json')
BODY=r'''IG-2B02-R01/R02 — NEW LOCAL REPAIR EXECUTOR INSTRUCTION

Work only in C:\repo\wargame-compiler in a NEW local session requested as GPT-6.1 Sol
(gpt-6.1-sol), reasoning high. Communicate in Polish; repository and private reports
in English, explicit UTF-8 without BOM. Preserve source/historical bytes. This file
is a prepared instruction, not evidence of authorization, a claim or a running session.
The current preparation did not change queue/status, perform a repair, launch a session
or grant acceptance. The operator must separately authorize coordinator setup and
execution. Read the pin/path table at the end before using named artifacts.

1. PRE-EXECUTION GATES AND OWNERSHIP

Read AGENTS.md, README.md, docs/STATUS.md, docs/HANDOFF.md, docs/work/WORKFLOW.md,
then docs/skills/wgc-execute/SKILL.md explicitly, the selected IG-2B02 record/card,
the exact coordinator-issued repair packet, repair-scope.json, findings.json and
the frozen delivery/review manifests and seals named below. Review only bounded inputs.
Use queue.json as sole status/scope authority. Default context/search uses workflow.py
and search.ps1; do not broaden to archives, history or adjacent source content.

This task currently remains review with its old frozen-executor write_scope. YOU MUST
NOT claim directly from review, write the old scope, or casually change role/queue to
bypass that gate. A separately authorized coordinator must first follow coordinator-
setup.txt, apply ONLY coordinator-queue-patch-v2.json, record exact review ->
changes_requested evidence, render/validate, and issue a fresh repair packet plus
coordinator-handoff.json containing actual resulting paths/hashes. The private-index
v1 proposal is superseded; the selected v2 uses one metadata-only docs/work/ index
already permitted by current policy, with no policy or validator changes.

If that completed coordinator setup/handoff is absent or current status is still
review, stop before any repair/claim and request setup. Pasting this executor prompt
does not impersonate a coordinator or make a stale packet current. The pre-preparation
review-state packet below is input evidence only, never claim readiness. If queue,
packet, scope or inputs drift except exact documented coordinator changes, checkpoint
and request coordinator refresh. Do not edit queue structure or any validation.

Confirm YOUR actual new session ID, actor, model gpt-6.1-sol and reasoning high from
YOUR own current runtime session_meta/turn_context or direct operator observation of
this NEW session. Requested settings, creation flags, this prompt, config.toml and
old actors' configuration records are not proof. If unavailable, record null values
with reasons and request the missing observation; do not claim/author until confirmed.
Own session metadata access is limited to configuration/identity records, not other
conversations/history. Actor must identify your real new session and differ from
original executor 01a13c20-b7bd-7962-a954-f5841c09831c and independent reviewer
01a13e3c-b2ef-7d90-bdfa-975891f92634. Their records remain immutable prior evidence.

Only after actual configuration confirmation and coordinator readiness, create the
exact RESERVED ABSENT repair directory in the pin/path section. Do not create/reuse
the original executor or reviewer directory. If the reserved repair directory exists,
or an owned input is changed by another writer, checkpoint/escalate; never overwrite
or steal ownership. Write configuration.json and preclaim checkpoint.json; freeze a
separate preclaim-checkpoint.json so a queue artifact pin never points to a mutable
checkpoint. Include actor/session/attempt, packet/context hashes, actual coordinator
event/authorization and queue snapshots, source/provenance/contract/tool/base/review
pins, completed/unmet criteria, owned base/current hashes, commands/exits/logs, UTC/wall
time, blocker and next operation. Unknown tokens/cost/operator time are null with reasons.

Prepare claim.json with role executor, YOUR confirmed actual configuration/evidence,
all unchanged task acceptance criteria, exact bounded write scope and immutable
checkpoint/configuration artifact pins. Use workflow changes_requested -> in_progress
once, then inspect actual status/event/evidence hash. No queue structural edits.
After ANY transition failure inspect actual persisted state/event FIRST. Never repeat
automatically; if the event persisted correctly, coordinate projection-only recovery;
otherwise checkpoint/escalate before a new attempt. At most two unchanged retries or
two repair cycles per finding, with a changed hypothesis recorded before another try.

No agents/chats/automations, external APIs/downloads/installs, Git history/archives,
neighboring repositories, global settings, reset/clean/stash/commit/push or downstream
work. Never resolve gameplay legality with an LLM. Preserve unrelated work. An ignore
file is not a read barrier. Writes are only your exact new repair directory, fresh
packet/check outputs and necessary workflow status projections via authorized tools.
All original delivery/review/preparation, source, src, tests and contracts are read-only.

2. EXACT REPAIR — THREE METADATA TARGETS ONLY

R01/P2: ig2b02:p5:alae:counter,
region:cbf6f8d6-889b-4fcb-bc54-a41a8d9052d0,
revision 9bb2b17d8602bc61d60944b00befd342c27b0e8403ef0f11508e4e4db335eaa7,
physical page 5, box [71895,107954,134804,155935].
The old component array has 6 at index 5 and 5 at index 6. Independent review observes
both bottom values as 5. Reconfirm the exact original/crop and replace ONLY index 5
with literal string 5. Keep all other descriptions and ordering, including the small
uncertain AS XIVa-like identifier, unchanged. Do not infer new gameplay meaning.

R02/P2: TWO distinct regions, each must remain its own existing identity:
ig2b02:p5:light-infantry:counter,
region:c3d45e49-7d30-4572-92f7-7ffcb468e840,
revision e94036005f19209a8517d9f9c784b3b03141fdcf1134929cef084abfe0770893,
box [513071,296717,575981,345329];
ig2b02:p5:javelinists:counter,
region:66a11202-3a57-4637-a1ac-308cb62e2662,
revision 7dfc5ab19034511a810e095475e9374972ce017123097dbc598a768c0acd0705,
box [513071,537878,575981,586490]. Both physical page 5.
The small white 1 beneath Thrace, immediately left of circular J, is omitted from
both descriptions. Reconfirm BOTH exact counters separately, then insert literal
string 1 after Thrace and before J missile glyph in each array. Preserve all other
entries and order. The two identical-looking images do not authorize deduplication,
merging IDs or altering denominator. Literal glyph inventory is not rule interpretation.

repair-scope.json gives the complete exact before/required-after arrays, regions,
revisions/boxes and original/triple/reviewer enlargement pins. If source observation
contradicts either finding or needs wider scope, retain evidence and escalate; do not
expand, guess, reinterpret or silently repair another entry.

Content access for this repair: ONLY the three exact page-5 counter crops/visible
frames above and their pinned reviewer original-derived enlargements. Original full
page-5/reviewer original file may be byte-hashed, but do not open/render/analyze full
pages for this metadata repair. If a fresh observation aid is needed, derive only the
exact bounded counter crop in your directory and label it derived, with pins/operation.
Do not dump off-crop PDF streams/resources or unrestricted text. No page-4/page-9 or
other page content access is needed/authorized. Existing continuation evidence may be
byte-checked only. All 44-page count/geometry checks remain structural. A later fresh
independent reviewer will separately have the original full pages-5-8 review scope.

3. IMMUTABLE PRODUCT AND REPAIR OUTPUT DESIGN

This repair changes component metadata sidecars, NOT wgc-inventory-1 canonical records.
Do not allocate/remap IDs, reseed/rebuild inventory, change keys/revisions/boxes/page
geometry/source/labels/evidence/order/links/coverage/uncertainty or retire memberships.
Do not bump a canonical region/top revision when its data did not change. Preserve:
141 task regions (39/33/39/30), full 130+36+141=307, context denominator zero, all
accepted 1-4 records/evidence, 9-44 placeholders, old registry entries and old context.
The prior page-5 context remains exact context with old evidence/link/order; no promotion.
All new transcription stays partial; descriptive/formal semantics unprocessed, with
unchanged reasons/gaps. No represented/excluded promotion or human semantic decision.

Build complete new-attempt snapshot files authored/inventory.json, authored/identity-
registry.json, final-verified/inventory.json, final-verified/identity-registry.json and
final-verified/coverage.json by BYTE-IDENTICAL copy of the corresponding reviewed IG-2B02
files. Compare exact SHA256/bytes, canonical revisions and object equality. This is an
explicit unaccepted repair snapshot, not a new inventory seed or evidence promotion.
Retain all original immutable evidence paths in those snapshots. Never copy/regenerate
the 423 primary evidence files or old evidence; all raw artifacts/locators remain exact.

Create new full author-specifications-final.json with only the three component-array
deltas. Preserve every other specification, box, key, grouping, link and order. Preserve
the existing component-observations corrections for OTHER counters; explicitly extend
the new effective correction map for these three targets with the same after arrays.
Use one documented effective-components rule consistently. No legacy generator may
reintroduce 6 or omit 1. Original author-specifications.py and drafts remain immutable
historical inputs. If creating a replacement/replay generator, it belongs only in the
new repair directory and must reproduce the new full metadata deterministically.

Create a complete new 141-entry region-ledger-final.json, not only three replacement
entries. Change exactly the three component arrays plus necessary current snapshot/
report pin references. Preserve all canonical nested regions, original evidence pins,
groups, ordering, native bounds, raw text pins and unrelated component lists exactly.
Make a new visual-inspection.json consistent with the same arrays, but do NOT claim
the old actor's all-page inspection as your new viewing. Attribute unchanged source
observations to pinned original executor/independent-review inputs; record your actual
new three-counter observations separately. Reuse current original evidence references.

Regenerate current dependent claims/reports/pins under the new attempt with explicit
provenance: affected-component-audit, finding-dispositions, delta-audit, preservation,
report-consistency, scope/coverage/gaps/uncertainty/continuation/correspondence/locator,
replay and criteria reports. An unchanged report may be referenced as immutable input
or included with explicitly original attribution; never silently relabel old work as
new independent verification. Every current product/report reference must resolve to
the intended new snapshot or clearly marked immutable original. Separate historical
defective component arrays from the new current targets; do not search-and-replace
source/raw text or rewrite old findings/history. New operational timestamps/actors/pins
are legitimate report metadata, never extra source/semantic changes.
'''
BODY+=r'''
4. MEANINGFUL VALIDATION, CHECKPOINTS AND COMMANDS

Reobserve/hash local/bundled toolchain 26.1013.11914 and compare exact pins below and
frozen toolchain.json. Expected Python 3.12.14 (MSC v.1944 AMD64), pypdf 6.10.0,
pdfplumber 0.11.9, Pillow 12.3.0, pytest 9.1.1; Poppler 26.07.0, PowerShell 7.6.5,
git 2.56.0.windows.2. Install nothing. Do not weaken validators/tests/contracts or
suppress Xref warnings. Tool/bundle observations do not confirm model configuration.

Process-only PowerShell setup:
Set-Location -LiteralPath 'C:\repo\wargame-compiler'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'C:\repo\wargame-compiler\src;C:\Users\yauta\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Lib\site-packages'
$env:PATH = 'C:\Users\yauta\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin;' + $env:PATH

Use repo-relative FORWARD-SLASH private artifact/CLI paths. Absolute native executable
arguments are not workflow artifact references. Record exact commands, exits, separate
stdout/stderr pins, UTC/wall times and actual errors after every usable increment.
Never assume tool calls share process environment. Unknown measurements are null.

Mandatory checks:
- Verify all frozen base/review file pins before AND after repair, including current
  original event chain, three exact source triples, source/provenance, tools/contracts.
- Source-observed expected results for R01/R02, both repeated Thrace counters separately;
  log exact viewed crops and observations, no guessed timestamps or inherited viewing.
- Full metadata delta audit: exactly the three authorized component arrays changed in
  specifications/effective corrections/ledger/current component claims; every unrelated
  region/component/override unchanged. Operational actor/timestamp/current-report pins
  must be separately classified and justified; forbid accidental text normalization.
- Assert byte-identical canonical snapshot files, original IDs/revisions/geometry/source,
  all 423 raw files and their original paths, all old registry entries/order/links/context,
  all coverage statuses/gaps and 141/307/zero-context counts. Validate full 44-page source
  count/geometry using unchanged root validator without unassigned content extraction.
- Complete current report-consistency audit (all 141 ledger entries, component authority
  precedence, visual report references and every finding disposition), not a three-row
  patch pretending to be a complete ledger. Link new current reports and original baseline
  clearly. Criterion 1 is executor-repaired_pending_independent_review, never self-accepted;
  criterion 5 for this new delivery remains pending a fresh independent session.
- Persist replayable repair code and independently rerun it into TWO fresh child output
  directories in the new repair attempt, using exact pinned bases/persisted registry.
  Reproduce exact new metadata bytes and unchanged canonical snapshot/registry bytes.
  No generic inventory generation, new UUID assignment or old fixed-path scripts.
- Recompute/verify new SHA256/bytes of every submitted artifact and every old reference;
  failure must remain visible and be reproduced only in bounded scope, never hidden.

After coordinator handoff, set $A to the exact reserved repo-relative repair directory
below, and $ClaimPacket to the ACTUAL new packet from that handoff (not a placeholder).
Run workflow validate and check latest changes_requested event before claim. After
claim, only your documented in_progress event/projection changes may differ.

.\.venv\Scripts\python.exe -B scripts/workflow.py validate
.\.venv\Scripts\python.exe -B -m wgc.sources validate "$A/final-verified/inventory.json"
$repairBaseTemp = 'C:/repo/wargame-compiler/private/workflow/checks/fix-b02-' + [guid]::NewGuid().ToString('N').Substring(0,12)
if (Test-Path -LiteralPath $repairBaseTemp) { throw 'Basetemp must be fresh.' }
.\.venv\Scripts\python.exe -B -m pytest -q tests/sources --basetemp $repairBaseTemp -p no:cacheprovider --tb=short
& 'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.EXE' -NoProfile -File scripts/check.ps1 -Task IG-2B02
.\.venv\Scripts\python.exe -B scripts/workflow.py validate
git diff --check

Run each command sequentially and record/check each exit before dependent work. The
prior 71 source/102 full-suite passes are baseline facts, not your new results. Do not
claim repaired content from synthetic tests alone. No new public source-derived tests.
Checkpoint before interruption, input conflict, tooling escalation or every completed
repair/verification increment. Keep original failures and changed-hypothesis records.

5. NEW FROZEN DELIVERY -> REVIEW, THEN STOP

Write finding-dispositions.json with both exact finding IDs, all three target IDs and
before/after arrays, original/review evidence pins, own observations, change paths,
validation results and resolution 'implemented_pending_independent_review'. Do not
write accepted/resolved-by-independent-review before that separate review occurs.

Prepare full current delivery-manifest.json, delivery.json, delivery-handoff.md, criteria
and checkpoint. List every new current reviewed file/report/script/log and immutable
base/input/evidence references. Clearly classify superseded original metadata as historic
baseline, not new current targets. Use explicit cycle/self-exclusion policy. Do not
include forbidden .venv/absolute executables as DIRECT workflow artifact paths; preserve
their pins inside toolchain metadata. Do not reference mutable checkpoint paths with
hashes that will later change; freeze immutable stage copies. Delivery role executor,
actual new actor/configuration proof, all exact task criteria, real required checks with
exit zero, manifest pin and complete ordered reviewed artifact list are mandatory.

Before first delivery transition, preflight EVERY artifact through unchanged workflow
safe_path/denied/file/digest rules without mutating queue. Do not merely hash files and
miss path policy. Include only admissible repo-relative reviewed file pins in artifacts;
native/bundle observations remain metadata. Keep the original failed envelope/recovery
history frozen; do not repeat that mistake or overwrite an already sealed new envelope.

Freeze artifacts and run once:
.\.venv\Scripts\python.exe -B scripts/workflow.py transition --task IG-2B02 --to review --evidence "$A/delivery.json"

Inspect actual queue/event/evidence hash regardless of exit. If failure, do not repeat
automatically or modify a sealed file; checkpoint/escalate. If correct event persisted
but projection failed, coordinate projection-only recovery. No acceptance/done.

After successful review event, create a FRESH review packet using unchanged workflow.py
packet --task IG-2B02. Construct independent-rereview-launch.txt and rereview-input-pins.json
with ACTUAL NEW delivery/manifest/handoff/specifications/component/ledger/inspection/report
hashes, exact original baseline/review references, latest review event, new packet path/
manifest/context hashes and current queue snapshot. Use independent-rereview-template.txt
below as a requirement template, not a false already-completed review. No invented future
hashes, actor/session IDs or reviewer decisions; missing actual pins block the handoff.

Avoid circular hashes: post-review packet, final rereview launch/pin index and transition
logs are explicitly post-freeze outputs excluded from the product manifest, then pinned
by final-seal.json along with sealed delivery/manifest/handoff/criteria/current snapshots.
The rereview prompt can then cite the real manifest/envelope hashes without modifying
them; final seal excludes itself and its actual hash is returned separately to operator.
Do not rewrite any sealed artifact. Record end UTC/elapsed wall, actual actor/model/
reasoning/proof, defects/checks and null unavailable tokens/cost/operator time.

Return exact new frozen paths/hashes and complete R01/R02 disposition/delta/preservation
reports. STOP in review. Do not create or message a reviewer session, grant acceptance,
semantic approval or done, repair a different finding, reopen IG-2B01 or start IG-2B03.
The operator will authorize a fresh independent reviewer separately. That reviewer must
not be your repair session; old review does not automatically approve new metadata.

6. EXACT PATHS, BYTE PINS AND COORDINATOR HANDOFF
'''

COORD=r'''IG-2B02-R01/R02 — COORDINATOR SETUP PLAN (PREPARED, NOT EXECUTED)

This is preparation only. Do NOT apply it until the operator separately authorizes
coordinator setup/execution. No acceptance/done or new session is authorized by this
plan. Current queue is review; old frozen task write_scope must not be reused for repair.

Use docs/skills/wgc-queue/SKILL.md explicitly. Confirm actual actor/configuration evidence,
read AGENTS/README/STATUS/HANDOFF/WORKFLOW and the exact prepared scope/proposal plus
independent review R01/R02. Verify all pins. Write a NEW coordinator-setup run (actual
UTC/session ID) under private/workflow/runs/IG-2B02/, not this sealed preparation and
not the reserved executor directory. Record the operator authorization and own role;
unknown configuration/usage fields are null with reasons, not borrowed from old sessions.

Apply ONLY selected coordinator-queue-patch-v2.json after checking its expected real queue
hash/status/event. Save exact before/after snapshots in the new coordinator directory.
Preserve every other queue/task field and every existing event byte/object. The proposed
fields update only this task's repair write scope, current output paths, bounded context/
inputs/start conditions/exclusions. Acceptance criteria, required tests, dependencies,
goal, executor configuration, semantic gate and other tasks stay exact. No context-policy
or validator edit: metadata-only docs/work/ index is already allowed. The private-index
v1 patch is retained failed preparation history and MUST NOT be applied.

Validate the candidate queue with unchanged workflow validation before publishing it,
then write queue atomically (checked current hash, no lock stealing), render derived
views using workflow.py render, run workflow validate/dry-run --task IG-2B02, required
scripts/check.ps1 -Task IG-2B02 and git diff --check with recorded commands/logs/exits.
Draft structural validation and packet-size estimate are preparation facts only;
recheck actual resulting packet, including Windows logical LF/physical CRLF bytes.

Write immutable coordinator-decision.json in that NEW setup directory with role
coordinator, actual actor/config evidence, summary adopting ONLY independent findings
R01/R02 for bounded repair (not accepting/dismissing them), all exact task criteria,
pins of review/findings/seal/scope/selected queue patch and completed setup checks.
Its artifacts use admissible repo-relative paths; do not put binary observation paths
directly into a workflow artifact array. Do not pin mutable queue/projection/checkpoint
paths as immutable transition artifacts; pin saved immutable snapshots/stage evidence.

Only after explicit operator setup authorization and passing checks, run:
.\.venv\Scripts\python.exe -B scripts/workflow.py transition --task IG-2B02 --to changes_requested --evidence <ACTUAL_COORDINATOR_RUN>/coordinator-decision.json

Use the ACTUAL new decision path, never a template/null placeholder. Inspect actual
state/event/hash first after any exit; never automatically repeat a transition. Correct
event with failed projection needs coordinator projection-only recovery; otherwise
checkpoint/escalate. No acceptance/done and no changes to frozen original delivery/review.

Generate workflow.py packet --task IG-2B02 AFTER successful changes_requested. Verify
all allowlisted inputs and reconstruct exact payload; keep <100000 logical UTF-8 bytes,
no truncation. Draft was 97079 bytes in review state, leaving room for longer status.
If actual changes make it stale/oversized, refine exact context safely and issue a new
handoff; never weaken limits or run the executor with a stale packet.

Write coordinator-handoff.json containing actual new status/event/evidence hash, current
queue hash, selected scope/patch/index pins, actual packet directory/manifest/context
paths+SHA256+bytes/logical byte count, reserved repair attempt absence/ownership policy,
actual source/tool/baseline/review checks and exact allowed write scope. Freeze a setup
manifest/seal, preserving original files. Then stop coordinator setup. Operator separately
launches the new repair executor using repair-launch.txt and THIS actual handoff.

The new executor may claim changes_requested -> in_progress only after confirming
its own actual Sol/high, exact handoff/packet/input/scope pins and absent new attempt.
It must return new frozen delivery -> review and prepare a fresh independent-review
handoff; no current session or coordinator grants accepted/done. Do not auto-create
either repair or reviewer sessions, send other chats messages or start later tasks.
'''

REREVIEW=r'''IG-2B02-R01/R02 — INDEPENDENT REREVIEW REQUIREMENT TEMPLATE

This is a template, NOT an issued review launch or evidence of future hashes/config.
The repair executor must produce a complete new independent-rereview-launch.txt and
rereview-input-pins.json AFTER freezing its actual output and successful review event.
It must substitute actual new paths/SHA256/bytes, queue/event, repair/claim/review packets
and required report pins. Leave no unresolved placeholders in the final issued prompt.
The operator later starts a NEW local independent GPT-6.1 Sol/high session; nobody
creates that session automatically from the repair task or this preparation.

Use docs/skills/wgc-review/SKILL.md, read AGENTS/README/STATUS/HANDOFF/WORKFLOW, exact
NEW review packet, new repair delivery/manifest/final seal, all three old target pins,
old frozen delivery/review, finding-dispositions/delta/preservation/report-consistency
and every current updated metadata artifact. Confirm YOUR actual new session identity
and gpt-6.1-sol/high from own runtime metadata or direct operator observation of this
session. Requested flags/old configuration are not proof. If unavailable, null/reason,
request observation, stop substantive review. Reviewer must differ from the repair
executor and original executor; use a fresh independent session/context, not self-review.

Write only a fresh reviewer directory and new check outputs. Do not modify original
or repair delivery/review/source/tool/test/contract/queue/projections. Preserve all old
sealed bytes and ordered new delivery.artifacts list. No acceptance/done or transition.

Independently inspect all four original assigned physical pages 5-8 against the complete
updated 141-region ledger and all grouped components; no sample substitution. Freshly
observe the three affected page-5 counters against exact source crops: Alae bottom 5/5,
both Thrace small white 1 recorded separately, all other components and literal uncertainty
retained. Verify every new report/specification/observation/ledger uses consistent current
component authority and no stale original generator/draft reintroduces the errors.
Trace and disposition BOTH finding IDs, not only one duplicated-counter occurrence.

Independently check exact declared component delta and operational attribution/pin delta.
Compare all unchanged 138 new-region component lists, all unrelated prior component
overrides, every nested canonical region/evidence/group/order/link/coverage record,
canonical inventory/registry/coverage bytes and all 423 primary raw artifacts. Keep
141 task/307 full/zero-context counts, 130 preserved authored and 36 placeholders,
old context identity/revision/evidence/link and accepted prior scope exact. No IDs,
canonical revisions/geometry/source/text/evidence/coverage or meaning may change.
Verify new complete metadata replay in two fresh reviewer-owned outputs without
executing fixed-path old executor scripts. Explicitly validate every current report pin.

Reopen original pinned PDF with unchanged root validator for 44-page actual count/
geometry/schema/canonical/identity/order/partition checks. Verify all current target
artifact hashes/source/page/basis/region boxes/offsets/PNG dimensions. Old independent
locator/render audits may support precisely documented UNCHANGED baseline risks only
after byte/source/geometry equality is independently confirmed; never transfer their
technical result as review of changed metadata. Freshly compare the three changed
component groups. Re-extract/render more only if drift/new risk/failure justifies it;
do not alter or regenerate primary immutable evidence. Tests/validator success alone
does not prove literal component completeness or source meaning.

Source scope for rereview is original task pages 5-8, exact old page-4 Triarii crop only
for necessary continuation verification; no other 1-4 content. Page 9 is conditional
only on a new observed unfinished page-8 fragment, with before-access need/origin ID/
revision/box and predetermined maximum-two-line top-of-corresponding-column crop.
Never whole-page/neighbor probes; insufficient crop -> gap/coordinator refinement.
Pages 10-44 geometry/count only. No archive/history/neighbor/API/download/agent/chat/
automation/global changes, commits/pushes or gameplay legality via an LLM.

Reobserve local toolchain and run unchanged source tests with fresh short basetemp,
-p no:cacheprovider, scripts/check.ps1 -Task IG-2B02, root inventory CLI validate,
workflow validate and git diff --check. Record actual commands/exits/stdout/stderr,
UTC/wall time/errors, two-retry limits and null unavailable usage. Retain Xref warnings.

Produce complete new region-review ledger, R01/R02 recheck records, criteria matrix,
findings, byte/delta/preservation/report-consistency/replay audits, review.json,
manifest/handoff/seal with actual hashes and new independent configuration proof.
review.json.artifacts must equal the NEW event's full ordered delivery.artifacts list,
not the old original envelope. New reviewer outputs go in separate fields/manifest.
Assess all five unchanged task criteria explicitly; criterion 5 is established only by
this real complete separate rereview, never executor self-inspection or old R01/R02 review.
Possible result no_blocking_findings / changes_recommended / review_incomplete; do not
grant accepted/done or invent human semantic/whole-record source-IG approval. Freeze
all new findings/reports/evidence with explicit self-exclusion policy, leave real task
in review and hand decision to operator/coordinator. Do not start IG-2B03 or create
another session. Source authenticity, coverage, human semantic acceptance and executable
readiness remain separate; none follows automatically from a green technical rereview.
'''

if __name__=='__main__':
 q=load('docs/work/queue.json');task=next(t for t in q['tasks'] if t['id']=='IG-2B02');assert task['status']=='review' and pin('docs/work/queue.json')==state['queue_snapshot'] and not (R/A).exists()
 DM=load(D+'/delivery-manifest.json');DS=load(D+'/final-seal.json');DE=load(D+'/delivery-transition-envelope.json');VM=load(V+'/review-manifest.json');VS=load(V+'/review-seal.json')
 allpins={}
 groups=[DE['artifacts'],DM['new_reviewed_artifacts'],DM['immutable_inputs_and_old_evidence'],DS['postfreeze_recovery_and_epilogue_artifacts'],VM['new_review_outputs'],VM['fresh_required_check_log_outputs'],VM['reviewed_delivery_artifacts_exact_event_order'],VM['reviewed_delivery_metadata'],VS['final_report_hashes'],[VS['review'],VS['manifest'],VS['handoff'],pin(V+'/review-seal.json')]]
 for group in groups:
  for p in group:
   if p['path'] in allpins:assert allpins[p['path']]==p,p['path']
   allpins[p['path']]=p
 write('frozen-base-pins.json',{'task':'IG-2B02','original_delivery':state['original_delivery'],'review':state['review'],'review_seal':state['review_seal'],'original_review_event':state['review_event'],'frozen_pins':list(allpins.values()),'unique_frozen_refs':len(allpins),'policy':'Byte-hash exact frozen references only; current queue/projections after later authorized setup are not immutable baseline files. Native executable observations are hash metadata, never direct workflow artifact refs. No source content review or repair performed by this preparation.'})
 PK='private/workflow/packets/IG-2B02-85b52f747fdb4b6eb91adad01fbd83ee';packet=load(PK+'/manifest.json');assert packet['queue_sha256']==state['queue_snapshot']['sha256']
 sections=[]
 for p in packet['files']:
  assert pin(p['path'])==p
  if Path(p['path']).suffix.lower() in ('.md','.json','.py','.ps1','.toml'):sections.append('\n--- FILE: '+p['path']+' ---\n'+(R/p['path']).read_text(encoding='utf-8-sig'))
 payload='\n'.join(sections);assert len(payload.encode('utf-8'))==packet['text_bytes'] and payload.replace('\n','\r\n').encode('utf-8')==(R/PK/'context.txt').read_bytes()
 controls=[PR+'/preparation.json',PR+'/repair-scope.json',PR+'/coordinator-queue-patch-v2.json',PR+'/proposal-validation.json',proposal['context_index']['path'],PR+'/verify-frozen-bases.py',PK+'/manifest.json',PK+'/context.txt','docs/work/queue.json','docs/work/context-policy.json','docs/work/WORKFLOW.md','docs/skills/wgc-execute/SKILL.md','docs/skills/wgc-review/SKILL.md']
 core=['delivery-transition-envelope.json','delivery-manifest.json','final-seal.json','review-handoff-final.md','authored/inventory.json','authored/identity-registry.json','final-verified/inventory.json','final-verified/identity-registry.json','final-verified/coverage.json','author-specifications-final.json','author-specifications.py','component-observations.json','region-ledger-final.json','visual-inspection.json','scope-report-final.json','locator-audit.json','preservation-report.json','replay-report.json','context-authored-correspondence.json','continuations.json','uncertainty.json','gaps.json','geometric-gaps.json','criteria.json','toolchain.json']
 controls += [D+'/'+n for n in core]+[V+'/'+n for n in ('review.json','review-manifest.json','review-seal.json','review-handoff.md','findings.json','criteria-review.json','configuration-proof.json')]
 controls += ['private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf','private/ig/sources/spqr-5e-official/revision-20261013T155212Z/provenance.json','src/wgc/contracts/source.py','contracts/ig/source.schema.json','contracts/ig/regions.schema.json','contracts/ig/README.md','src/wgc/sources/inventory.py','src/wgc/sources/pdf.py','src/wgc/sources/geometry.py','scripts/workflow.py','scripts/check.ps1','scripts/search.ps1']
 for target in scope['targets']:
  controls += [target['original_source_evidence'][k]['path'] for k in ('text','image','crop_pdf')]+[target['independent_review_enlargement']['path']]
 rows=[pin(p) for p in dict.fromkeys(controls)];write('launch-gate-pins.json',{'task':'IG-2B02','pins':rows,'reserved_repair_attempt':A,'repair_attempt_exists':False,'future_claim_packet':None,'future_claim_packet_null_reason':'Coordinator has not yet authorized/applied setup or changes_requested; actual new claim packet must be issued after that event.','future_repaired_delivery_hashes':None,'future_repaired_hashes_null_reason':'Repair not executed; future executor computes actual new frozen hashes and complete rereview launch after successful review event.'})
 paths='\nEXACT DIRECTORY ALIASES (repo-relative, forward slashes)\nD — immutable original delivery: '+D+'\nV — immutable independent review: '+V+'\nP — immutable preparation: '+PR+'\nA — exact RESERVED ABSENT repair output directory: '+A+'\n\n'
 table='PATH | BYTES | SHA256\n'+'\n'.join(p['path']+' | '+str(p['bytes'])+' | '+p['sha256'] for p in rows)+'\n'
 catalog=pin(PR+'/frozen-base-pins.json');scopepin=pin(PR+'/repair-scope.json')
 footer='\nComplete frozen base/review catalogue: '+catalog['path']+'\nSHA256 '+catalog['sha256']+'; '+str(catalog['bytes'])+' bytes; '+str(len(allpins))+' unique frozen refs.\n'
 footer+='\nExact original acceptance criteria (UNCHANGED; same order in claim/delivery/review):\n'+'\n'.join(str(i)+'. '+c for i,c in enumerate(task['acceptance'],1))+'\n'
 footer+='\nPreparation packet is current REVIEW-state input evidence: '+PK+'; '+str(packet['text_bytes'])+' logical LF bytes, '+str(pin(PK+'/context.txt')['bytes'])+' physical CRLF bytes. It is NOT the future changes_requested claim packet.\n'
 footer+='\nFrozen-byte helper (verify its pinned bytes first; explicit fresh report under your own repair run):\n.\\.venv\\Scripts\\python.exe -B '+PR+'/verify-frozen-bases.py --report ($A + "/preclaim-frozen-bases.json")\n'
 footer+='\nDo not create the repair directory before confirmed actual configuration and coordinator setup. If not yet authorized, helper reports for coordinator preparation belong to that coordinator run, not A. Do not use preparation helper success as permission to claim.\n'
 textfile('repair-launch.txt',BODY+paths+table+footer+'\nCompanion mandatory coordinator plan: '+PR+'/coordinator-setup.txt\nCompanion rereview requirement template: '+PR+'/independent-rereview-template.txt\n')
 textfile('coordinator-setup.txt',COORD+paths+table+footer)
 textfile('independent-rereview-template.txt',REREVIEW+paths+'\nFrozen base/review pin catalogue: '+catalog['path']+'\nSHA256 '+catalog['sha256']+'\n\nRepair output hashes/event/packet: null until ACTUAL future repair. Issuing a final prompt with this null is forbidden; repair executor fills actual values and final seal pins the generated launch.\n')
 write('instruction-delivery.json',{'role':'repair_instruction_preparer','task':'IG-2B02','preparer_actor':state['preparer_actor'],'repair_instruction':pin(PR+'/repair-launch.txt'),'coordinator_plan':pin(PR+'/coordinator-setup.txt'),'rereview_template':pin(PR+'/independent-rereview-template.txt'),'scope':scopepin,'selected_queue_patch':pin(PR+'/coordinator-queue-patch-v2.json'),'metadata_context_index':proposal['context_index'],'frozen_base_catalogue':catalog,'launch_gate_pins':pin(PR+'/launch-gate-pins.json'),'current_queue':state['queue_snapshot'],'reserved_repair_attempt':A,'created_session':False,'repair_executed':False,'queue_changed':False,'acceptance_granted':False,'next_operation':'Operator may separately authorize bounded coordinator setup, then NEW actual-config-verified repair executor; executor returns review and actual fresh independent-rereview handoff, without creating sessions or acceptance.'})
 print(json.dumps({'repair_instruction':pin(PR+'/repair-launch.txt'),'coordinator_plan':pin(PR+'/coordinator-setup.txt'),'rereview_template':pin(PR+'/independent-rereview-template.txt'),'scope':scopepin,'frozen_refs':len(allpins),'queue_unchanged':pin('docs/work/queue.json')==state['queue_snapshot'],'repair_attempt_still_absent':not (R/A).exists()},indent=2))
