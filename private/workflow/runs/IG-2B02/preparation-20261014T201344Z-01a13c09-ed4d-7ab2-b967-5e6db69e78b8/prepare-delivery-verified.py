"""Verify fresh packet and write a launch prompt; does not create executor session."""
import runpy, sys, json
from pathlib import Path
r=Path(__file__).resolve().parent
m=runpy.run_path(str(r/'prepare-refined.py')); read=m['read']; pin=m['pin']; write=m['write']; sha=m['sha']; run=m['RUN']
sys.path.insert(0,'scripts'); import workflow
q=read('docs/work/queue.json'); task=next(t for t in q['tasks'] if t['id']=='IG-2B02')
p=Path((r/'fresh-packet.stdout').read_text(encoding='utf-8').strip()); manifest=read(p/'manifest.json')
assert task['status']=='ready' and len(task['events'])==1 and task['events'][0]['to']=='ready'
assert manifest['queue_sha256']==sha('docs/work/queue.json')
expected=list(dict.fromkeys(workflow.BASE_CONTEXT+['docs/work/tasks/IG-2B02.md']+task['context']))
assert [f['path'] for f in manifest['files']]==expected
sections=[]
for f in manifest['files']:
    assert workflow.permitted(Path.cwd(),f['path']) and pin(f['path'])==f
    x=Path(f['path'])
    if x.suffix.lower() in {'.md','.json','.py','.ps1','.toml'}: sections.append('\n--- FILE: '+f['path']+' ---\n'+x.read_text(encoding='utf-8-sig'))
payload='\n'.join(sections).encode('utf-8')
physical_payload=payload.replace(b'\n',b'\r\n') if sys.platform=='win32' else payload
assert (p/'context.txt').read_bytes()==physical_payload
assert sha(p/'context.txt')==manifest['context_sha256'] and len(payload)==manifest['text_bytes']<=100000
write('packet-verification.json',{'task':'IG-2B02','status':'ready','queue':pin('docs/work/queue.json'),'manifest':pin(p/'manifest.json'),'context':pin(p/'context.txt'),'all_exact_context_hashes_verified':True,'allowlisted_paths':expected,'payload_reconstructed_byte_identically':True,'platform_newline_policy':'Windows Path.write_text newline=None expands LF to CRLF; manifest text_bytes measures the logical LF payload, context SHA256 pins actual disk bytes. Both recomputed separately.','physical_context_bytes':len(physical_payload),'text_bytes':len(payload),'no_models_launched':True,'no_claim_or_authoring':True})
scope=read(r/'scope.json'); tools=read(r/'toolchain.json'); refs=read(r/'source-pins.json'); attempt=scope['reserved_executor_attempt']
assert not Path(attempt).exists()
def item(label,d): return f"- {label}: `{d['path']}`; SHA256 `{d['sha256']}`; {d['bytes']} bytes."
pins='\n'.join([item('Packet manifest',pin(p/'manifest.json')),item('Packet context',pin(p/'context.txt')),item('Ready evidence',pin(run/'ready.json')),item('Scope',pin(run/'scope.json')),item('Source PDF',refs['source']['pdf']),item('Official provenance',refs['source']['provenance']),item('Accepted IG-2B01 baseline',refs['baseline']),item('Persisted IG-2B01 registry',refs['persisted_registry']),item('Dependency closure verification',pin(run/'dependency-verification.json')),item('Toolchain evidence',pin(run/'toolchain.json'))])
toolpins='\n'.join([item('Python executable',tools['python_executable'])]+[item(n+' executable',d['executable']) for n,d in tools['native'].items()]+[item('Frozen tool/contract',x) for x in tools['frozen_contract_and_tool_pins']]+[item('Workflow/check/search',x) for x in tools['workflow_and_checks']])
text=f'''# IG-2B02 executor launch command

Paste this complete instruction into a separate NEW local executor session in C:\\repo\\wargame-compiler. This preparation did not create, configure, claim or launch that session. Communicate with the operator in Polish; repository content, private reports and evidence must be English and explicit UTF-8. Execute only IG-2B02 through frozen delivery -> review, then stop.

Use docs/skills/wgc-execute/SKILL.md explicitly. Read AGENTS.md, README.md, docs/STATUS.md, docs/HANDOFF.md, docs/work/WORKFLOW.md, then the exact supplied packet and its named context. Queue.json is the sole status authority; default context/search uses scripts/workflow.py and scripts/search.ps1. No archives, Git history, external APIs/downloads, global settings, neighboring repositories, reset/clean/stash/commit/push, other tasks, agents, chats or automations.

Before claim, confirm the actual configuration of YOUR NEW session is GPT-6.1 Sol (`gpt-6.1-sol`) / `high` from your own runtime/session metadata or direct operator observation of this new session. Record actual session ID, actor, configuration evidence and UTC. Requesting these settings, this prompt, prior configuration files and this coordinator's null configuration are not proof. If confirmation is unavailable, do not claim or author; record missing evidence and request the operator's observation. Unknown values are null with reasons.

Run workflow validate and next. Verify IG-2B02 is ready, IG-2B01/IG-2A done, the one ready event matches its evidence, no task is active and queue/packet/exact input hashes below match. Reconstruct packet payload from its exact allowlisted paths and verify context/manifest hashes. If queue/context/input changes, stop for coordinator refresh; do not use a stale packet. Do not reopen IG-2B01.

{pins}

Coordinator evidence directory: `{run.as_posix()}`. It is read-only to you. The exact reserved executor attempt is `{attempt}/`; it must still be absent. Create it only for your new session after confirmed configuration, write configuration.json and a preclaim checkpoint.json, and record exclusive ownership. Checkpoint includes exact task/actor/attempt, packet path/hash, source/provenance/contract/tool/baseline/registry hashes, base/current owned hashes, completed/unmet criteria, actual commands/exits, blocker and next operation. Keep all other existing working changes. Do not overwrite old attempts; if this directory exists or another writer changes an owned input, checkpoint and escalate. Record your new session's actor even though the coordinator reserved the directory name.

Prepare claim.json with role executor, your actor, confirmed actual model/reasoning and evidence, task criteria, checkpoint artifact pin and exact write scope. Then run:

```powershell
.\\.venv\\Scripts\\python.exe -B scripts/workflow.py transition --task IG-2B02 --to in_progress --evidence {attempt}/claim.json
```

No queue structural edits: only authorized workflow status transitions and generated views. Owned writes are this exact executor directory, newly generated packet/check directories, and necessary workflow projections. Do not write this preparation, frozen IG-2A/IG-2B01, src/wgc/sources, tests or contracts. Do not change validations. After any transition failure inspect actual status/event/evidence hash FIRST; workflow may have persisted before projection failure. Never automatically repeat a transition. If an event is correct, coordinate projection-only render recovery; otherwise checkpoint/escalate.

Author only physical pages 5, 6, 7, 8. Use the accepted final IG-2B01 full 44-page inventory as the structural base and its persisted registry as the identity base; never rebuild from an IG-2A seed or generic full-page inventory. Preserve accepted pages/regions/evidence 1-4, unchanged page records/placeholders 9-44, all existing registry entries, old links and relative reading order. Retire only the four page-5-8 placeholder memberships, retaining their registry entries. Give independently observed new regions explicit stable `ig2b02:` keys and persisted new UUIDs; no text/array/coordinate/hash-based identity remap. Keep physical page IDs/keys/geometry and source revision unchanged; independently observed printed labels require current same-page evidence. Recompute only changed nested/top revisions with frozen integer-only WGC-C14N-1. Preserve every unchanged nested record and evidence reference exactly.

Existing context identity `region:e8d77349-41ce-47d0-b678-eab1d0c8e8ed`, key `ig2b01:context:triarii-tail`, revision `af2a41ef3c500858f945d9a813c185f8ca3bc6fbc142e61348e6da5964d011c1`, page 5 box `[71895,63131,495099,98485]` remains unchanged context with zero denominator, old evidence and the prior page-4 link. Never promote/remap it to inventory. Independently allocate a distinct authored page-5 region; record source-observed exact context/authored IDs, revisions, boxes and correspondence in context-authored-correspondence.json. Retain the prior link; a separately source-evidenced new continuation to the authored identity can be added without changing old records/links. Splits/merges need explicit lineage decisions, not automatic acceptance transfer.

Content context outside 5-8 is tightly bounded in scope.json: page 4 only the exact accepted Triarii region `region:ba4a5094-22f5-4a67-8a19-6cc598a17b1b` and its already-pinned final text/PNG/crop-PDF; no whole-page render or other 1-4 analysis. Page 9 only if an observed unfinished page-8 fragment requires it. BEFORE access record originating ID/box, exact need and predetermined normalized top-of-corresponding-column crop with maximum two lines in checkpoint/context-access.json. Never render/dump whole page 9 or a neighboring entry. If it is insufficient, retain an unresolved boundary/gap and seek bounded coordinator refinement before expansion. New context identity stays zero denominator. Pages 10-44 receive structural count/geometry validation only. Do not open prior broad-probe content. No preparation content analysis of 5-8 has already been done for you.

Inventory all assigned visible clauses/headings/notes/examples/diagrams/counters/tables/legends/editorial furniture independently of KB headings. Document grouped components, explicit reading order, continuation/note/illustration links, uncertain readings and literal extraction anomalies. Task denominator counts only newly authored inventory regions on 5-8; full denominator is 130 preserved authored + 36 unprocessed placeholders + new assigned inventory regions; every context counts zero. Keep geometric complement, transcription, descriptive and formal semantics as separate measures. A bbox, PNG or extraction is not represented coverage; editorial classification is not approved exclusion. Partial/unprocessed requires explicit gaps. Sidecar partition hashes never substitute for frozen IG-1A exact whole-record region targets and inventory bases; human authenticity/semantic acceptance is a separate gate. Never resolve gameplay legality using an LLM.

Use only existing local/bundled dependencies, version 26.1013.11914. Current observed Python: {tools['python']}. Libraries: {json.dumps(tools['libraries'],sort_keys=True)}. Native versions: {json.dumps({k:v['version'].splitlines()[0] for k,v in tools['native'].items()},sort_keys=True)}. Reobserve/hash YOUR actual toolchain and compare with these pins before execution; record drift and escalate. These observations do not prove your model configuration.

{toolpins}

Process-only setup (use repo-relative forward-slash private paths for the source CLI; never serialize Windows backslashes as a private path):

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = '{tools['process_pythonpath']}'
$env:PATH = '{tools['process_path_prefix']};' + $env:PATH
.\\.venv\\Scripts\\python.exe -B -m wgc.sources validate {refs['baseline']['path']}
```

Build replayable authored/inventory.json and authored/identity-registry.json from the accepted structure, then new evidence and final-verified outputs; do not invoke generic inventory generation to replace accepted content. The existing CLI evidence command extracts ALL regions on requested pages, including the old page-5 context. Therefore use unchanged library extract_evidence for the exact new authored IDs and any authorized new context only, keeping all old evidence unchanged, with fresh output directories. Record the actual command/script and hash in your attempt. Derive exact cropped PDF, 144-DPI Poppler PNG and raw UTF-8 pdfplumber text with page_basis_hash/current region revision/source pin, rational native bounds, Unicode codepoint half-open offsets, engine versions and exact pixel dimensions. Never fabricate evidence pins. Do not silently normalize original text or publisher bytes.

Every exact deliverable path is listed in `{run.as_posix()}/scope.json` outputs. Include full final inventory/registry/coverage; complete region-ledger-final; scope denominators; context-authored-correspondence; continuations, uncertainties and content/representation/geometric gaps; full assigned-page original/overlay visual inspection; exact locator audit; deterministic persisted-registry replay; preservation comparison against unchanged accepted scope; criterion results; configuration/toolchain/checkpoints; delivery-manifest, delivery and handoff. Keep independent review criterion pending until a separate reviewer actually reviews.

Required validation: root validate reopens the byte-pinned original PDF and compares strict pypdf and Poppler 44-page counts/all-page geometry without extracting unassigned content; all schema/canonical/identity/order/partition checks; every assigned page and region/component visually against original; exact evidence SHA256/bytes/source/page/region/frame/page_basis_hash, rational crop bounds, offsets and predicted/actual PNG dimensions; unchanged 1-4 records/evidence, placeholders 9-44, registry entries/links; new task/full/zero-context counts; bounded boundary access; replay in fresh output directories produces identical canonical author bytes/IDs. Run unchanged tests/sources with a fresh short basetemp and `-p no:cacheprovider`, then:

```powershell
.\\.venv\\Scripts\\python.exe -B -m wgc.sources validate {attempt}/final-verified/inventory.json
pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B02
.\\.venv\\Scripts\\python.exe -B scripts/workflow.py validate
git diff --check
```

Record exact commands, exit codes, stdout/stderr, UTC/wall times and actual errors. Tooling failures: reproduce with bounded scope and escalate; edit no tool/test/contract, weaken no check. At most two unchanged retries/repair cycles under workflow; record changed hypothesis before another attempt. Existing pypdf Xref warnings must remain visible, not suppressed. Checkpoint after every usable increment and before interruption.

Freeze a complete delivery-manifest.json of all new reviewed files/reports and exact immutable old input/evidence references (exclude self with explicit policy), delivery.json pins the manifest and full artifact list with role executor/passing checks, and delivery-handoff.md reports every criterion met/unmet, inputs/packet hashes, gaps, scope limits, defects and independent-review request. Record UTC start/end, elapsed wall time, actual actor/model/reasoning/evidence; unexposed tokens/cost/operator time null with reasons. Seal final delivery/manifest/handoff/criteria/check outputs and exact reviewed inventory/registry. Run in_progress -> review with delivery.json, inspect actual event/hash/status and freeze final-seal.json without overwriting sealed artifacts.

STOP at review. This NEW delivery requires a fresh separate independent reviewer identity/session comparing original assigned pages to the complete exact ledger and all delivery hashes; executor self-inspection and IG-2B01 review do not satisfy it. Do not grant acceptance/done, human semantic acceptance or whole-record review; do not start IG-2B03 or create any session. Return exact frozen paths/hashes, checks, material blockers and the independent-review handoff to the operator.
'''
(r/'executor-command.md').write_text(text,encoding='utf-8')
write('executor-command-verification.json',{'prompt':pin(run/'executor-command.md'),'packet':pin(p/'manifest.json'),'scope':pin(run/'scope.json'),'reserved_attempt_still_absent':not Path(attempt).exists(),'new_session_configuration_gate':True,'stop_at_independent_review':True,'no_executor_created':True})
print('Verified packet bytes:',len(payload),'Prompt:',(run/'executor-command.md').as_posix())
