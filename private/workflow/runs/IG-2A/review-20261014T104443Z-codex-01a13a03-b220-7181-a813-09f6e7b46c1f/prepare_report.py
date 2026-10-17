from support import *
from collections import Counter
from wgc.sources.inventory import validate

ACTOR='codex-01a13a03-b220-7181-a813-09f6e7b46c1f'
TASK=read(RUN/'queue-record.json')
old_findings=read(REPAIR/'dispositions-before.json')
probes=read(RUN/'probe-results.json')['results']
retained=read(RUN/'retained-reproduction-results.json')['results']
assert all(p['expectation_met'] for p in probes+retained)
assert all(p['expectation_met'] for p in read(RUN/'independent-pixel-oracles.json')['results'])
criteria_strings=TASK['acceptance'] if 'acceptance' in TASK else None
if criteria_strings is None:
    # Queue content is the authority; inspect its exact key rather than reconstructing.
    print('task keys',list(TASK));raise ValueError('Locate exact acceptance key before report')
checks=read(RUN/'required-checks.json')+read(RUN/'real-required-checks.json')+read(RUN/'final-checks.json')
for name in ['verify-inputs-02','independent-probes','retained-reproductions','pixel-oracles','integer-pixel-boundaries','real-source-checks','final-verification']:
    checks.append(read(RUN/(name+'.json')))
assert all(c['exit_code']==0 for c in checks)
visual={'actor':ACTOR,'method':'Reviewer viewed fresh contact sheet of physical pages 1-4 and full-resolution original-source physical page 3 via view_image. Original and independently derived page PNGs are pixel-identical.','contact_sheet':pin(RUN/'real-pages-contact.png'),'pages':[{'physical_page':n,'image':pin(RUN/f'direct/page-{n:02}.png'),'observed_printed_label':None if n==1 else str(n),'label_location':None if n==1 else ('top-right' if n==3 else 'top-left'),'visible_clipping':False} for n in [1,2,3,4]],'cover_label_status':'unknown','edition_observation':'5th Edition visible on physical page 1','pages_5_44_content_access':False,'scope':'Visual rendition/printed-label observations only; no interpretation or game legality decisions.','semantic_acceptance_granted':False}
write('visual-inspection.json',visual)
closure_text={
 'IG2A-R01':'CLOSED. Resealed CropBox, effective-crop intersection, MediaBox, rotation and UserUnit changes reject stale evidence without root; root validation rejects the changed actual-source geometry. Address swap rejects identity remapping. Replacing the evidence page-basis hash does not bypass source geometry checks. Fresh evidence and legacy reproduction baseline pass. No closure is inferred from a missing schema field.',
 'IG2A-R02':'CLOSED. False 72-DPI metadata on actual 144-DPI evidence fails the DPI/geometry prediction; one-pixel forged rounding metadata fails. Eight fractional nonzero-origin partial-crop 72/144-DPI cases at all rotations pass exact rational dimension expectations and eight independently redrawn full-image pixel oracles at zero tolerance. Eight additional exact-integer pixel-boundary renders at UserUnit 1.1 pass. Poppler ceiling is explicit; PNG dimensions agree.',
 'IG2A-R03':'CLOSED. Valid other-page evidence rejects a verified label on this page; correct same-page current evidence passes. Actual delivery labels 2/3/4 match current reviewer image observations and exact page/source/region evidence basis. Unknown cover and pages 5-44 remain unknown; embedded_unverified metadata remains unverified. Glyph and human authority claims are not authenticated by association checks.',
 'IG2A-R04':'CLOSED within the sidecar author-scope contract. Changed author key, kind, uncertainty, registry, source identity/revision, page mapping, geometry partition, denominator role, reading order or link rejects the old boundary. Direct coverage report marks its author scope stale, source-IG freshness unknown and human authority unverified. The unchanged synthetic basis passes only those limited structural checks. Coverage-only rationale changes deliberately do not imply a current approved IG-1A whole-record exclusion. Frozen IG-1A tools/schema/README hashes remain unchanged.',
 'IG2A-R05':'CLOSED. A two-page pinned source with consistently forged one-page claims rejects actual source-count mismatch. Swapped physical addresses under persisted identities reject remapping. Reordered page array passes; two official fresh inventories using persisted registry have identical canonical and serialized bytes and identities. Changed-PDF registry reuse refuses explicit remapping. Geometry/revision changes remain separate from UUID identity.'}
dispositions=[]
for f in old_findings:
    group=[p for p in probes if (f['id']=='IG2A-R01' and ('stale_' in p['name'] and 'exclusion' not in p['name'] or p['name'].startswith('forged_basis'))) or (f['id']=='IG2A-R02' and any(s in p['name'] for s in ['dpi','pixel','fractional'])) or (f['id']=='IG2A-R03' and 'label' in p['name']) or (f['id']=='IG2A-R04' and ('exclusion' in p['name'] or 'ig1a' in p['name'])) or (f['id']=='IG2A-R05' and any(s in p['name'] for s in ['reordered','missing_actual','registry_reuse','address']))]
    dispositions.append({'id':f['id'],'prior_severity':f['severity'],'disposition':'CLOSED','closure_condition':f['closure_condition'],'reviewer_assessment':closure_text[f['id']],'independent_candidates':[p.get('candidate') for p in group if p.get('candidate')],'evidence':[pin(RUN/'probe-results.json'),pin(RUN/'retained-reproduction-results.json'),pin(RUN/'independent-pixel-oracles.json'),pin(RUN/'preservation-final.json')]})
write('dispositions.json',dispositions)
write('findings.json',{'outcome':'PASS','actionable_findings':[],'new_defect_counts':{'P0':0,'P1':0,'P2':0,'P3':0},'prior_finding_dispositions':dispositions,'semantic_acceptance_granted':False})
criteria=[]
bases=[
 'Root validation checks the byte-pinned PDF count/geometry and each physical identity, all pages remain addressable, current evidence pins exact normalized/native/displayed bases. Correct same-page label association passes, cross-page/stale association fails. Official repeatability and 12 exact image comparisons pass (eight synthetic and four official).',
 'Separate UTF-8 text, PNG, uncertainty, Unicode offsets, explicit reading-order IDs and note/continuation links survive. The 71-test source suite includes multicolumn/table-note/cross-page cases and duplicate-context accounting. Independent overlapping-context passes without increasing denominator; inventory overlap, duplicates and missing order fail. Evidence DPI and geometry are cross-checked.',
 'All 44 official placeholders are unprocessed with zero represented regions at every level. Missing actual PDF page cannot be concealed; uncovered area is explicit; partial retains gaps and cannot count as represented. Exclusions remain visible structural claims, stale author scopes reject, and source-IG review freshness/human authority remain unknown/unverified.'
]
assert len(criteria_strings)==3
for criterion,basis in zip(criteria_strings,bases):criteria.append({'criterion':criterion,'status':'MET_FOR_IG2A_TECHNICAL_TOOLING_SCOPE','assessment':basis,'evidence':[pin(RUN/'probe-results.json'),pin(RUN/'repeatability.json'),pin(RUN/'real-render-comparison.json'),pin(RUN/'delivery-inventory-validation.json'),pin(RUN/'required-checks.json')],'limitations':'No substantive IG-2B inventory, semantic acceptance, source-IG exclusion approval, compilation or executable readiness.'})
write('criteria.json',criteria)
started=read(RUN/'configuration.json')['started_utc'];ended=utc()
measurement={'started_utc':started,'ended_utc':ended,'wall_seconds':(datetime.fromisoformat(ended)-datetime.fromisoformat(started.replace('Z','+00:00'))).total_seconds(),'start_basis':'Current-session session_meta timestamp, read directly before substantive review.','end_basis':'Independent review evidence/report preparation boundary; final freeze boundary is separately measured in final-seal.json.','input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None,'unknown_reason':'Not exposed/reported; no estimates substituted.'}
write('measurement.json',measurement)
report=f'''# IG-2A independent technical review of bounded repair

Outcome: **PASS** for the repaired IG-2A tooling increment. All five prior findings are closed against the exact repaired delivery; no new actionable product finding was established. This report is an independent technical handoff, not acceptance/done or human semantic approval.

Reviewer `{ACTOR}` is distinct from executor `codex-01a139bc-256f-7da0-b4a7-8940ca16fc81` and prior reviewer `codex-01a1363e-1de5-7073-8185-d9a1f2e89c35`. Current-session turn metadata records `gpt-6.1-sol`, effort `high`; the operator also stated “potwierdzam 6.1 sol high”. Configuration evidence is filtered current-session metadata, not the executor's confirmation. No product, queue/status, allowlist, previous-run or source writes were made.

## Frozen scope and integrity

The four operator repair pins match: delivery `c69df3b2867f440c6b330159a2d335dff6bf959192ebb9d3ac5d0ea59977195e`, manifest `3652874c7a029100efe81b93914934e469ba5b519bf1b66b0ff2b209645a7d49`, handoff `0ad1c51043eaef5859f6e99484889ae9e2aa0eda4c837dd9f75c754165b0e758`, final seal `64f96bc690396ceeb3ed37722c0c29546fa4a76448710ad8b8731043f0ce312d`. All 273 delivery artifacts, sealed post-freeze/governance artifacts and 159 prior-review manifest artifacts were verified. Prior final seal and manifest match their operator pins; the old report was assessed through its retained candidates, not assumed correct.

`input-verification.json` records 674 matching checks, including every one of 87 original delivery copies, 81 intentionally unchanged original live artifacts, and all eight product-before copies. Product comparison diffs are generated solely from those verified copies. `preservation-final.json` rechecks those pins, the unchanged workflow/check/search scripts and IG-1A validator/schema/README, the original delivery JSON, current runtime binaries and worktree status. The other 38 queue task records still match repair-start records. Queue SHA256 stays `18621ef45410770936da05949da3c434a9aedf262e50f18db3fc5d90ad809386`, status `review`.

The fresh review-preparation packet's files and queue pin equal `workflow.packet(..., output=False)`; regeneration was unnecessary. `packet-verification.json` pins its manifest/context. The recorded interrupted review transition is consistent with a queue event already written and a successful projection-only recovery; current workflow validation passes. No unexplained coordinator changes were found.

## Finding dispositions

'''+ '\n\n'.join('### '+f['id']+'\n\n'+closure_text[f['id']] for f in old_findings)+f'''

`dispositions.json` preserves each exact prior closure condition and links independent candidates. `retained-reproduction-results.json` has two passing migrated baselines and ten rejecting original adverse mutations; freshness diagnostics are not schema-only failures. Fresh derivations were written separately; original candidates/evidence were not modified.

## Exact acceptance criteria

'''+ '\n\n'.join('**MET — '+c['criterion']+'**\n\n'+c['assessment'] for c in criteria)+f'''

## Validation and expectation provenance

The explicit source suite passed **71 tests**, fresh short basetemp `t`, `-p no:cacheprovider`. The unchanged `scripts/check.ps1 -Task IG-2A` passed **102 project tests**, workflow validation, task dry-run and Git diff checks. Its output-only PowerShell adapter redirects just the generated operational directory into `c`; it executes the original script, preserves every validation, and records equal before/after script hashes. Required checks, exact commands, exits, stdout/stderr and elapsed times are retained in `required-checks.json`, `real-required-checks.json`, `final-checks.json` and individual command records.

There are **{len(probes)}** fresh independent boundary probes, **12** migrated retained cases, **8** fractional/nonzero-origin/all-rotation/72-or-144-DPI dimension probes, **8** full-image zero-tolerance pixel comparisons against an independently drawn physical oracle, and **8** exact-integer pixel-boundary renders at UserUnit 1.1. The eight dimension probes are included in the fresh probe count. The oracle builds its own zero-origin PDF from authored native coordinates; no WGC conversion/size/scaling helper supplies expected results. Dimensions use exact physical rationals and per-axis ceiling; interior color landmarks provide a separate rotation check. No one-pixel allowance was used for full-image agreement.

Independent pypdf and Poppler counts are both **44**. Two newly generated structural inventories using the persisted registry have identical canonical and serialized bytes and UUID mappings. Structural geometry for all 44 pages matches independent pypdf inspection; substantive content access was limited to physical pages 1–4. Four full-page derived PNGs agree pixel-for-pixel with direct original-PDF Poppler renders. The current reviewer viewed the fresh contact sheet and full page 3; labels 2/3/4 and visible layouts agree with the repaired verified inventory. Cover has no verified page label; pages 5–44 remain unknown. `visual-inspection.json` records observations only, without interpreting any game rules.

Actual dependencies: Python 3.12.14, pypdf 6.10.0, pdfplumber 0.11.9, Pillow 12.3.0, reportlab 4.4.9, pytest 9.1.1, Poppler 26.07.0. Reviewer captured Python and Poppler executable hashes before probes and confirmed them unchanged at the end. Poppler hashes independently match the repair's current bundle 26.1013.11914 and differ from the earlier bundle claims; matching version strings are not treated as binary identity. No installs or global changes occurred.

All substantive validation commands passed. `preflight-errors.json` retains the initial helper API-name error and absent unused jsonschema metadata query; both concerned reviewer setup, not product tests. Their actual failed command output remains available. One boundary-results filename collided with its wrapper command record: exact printed rows survived in captured stdout, were recovered into `independent-integer-pixel-boundaries.json`, and the producer output name was corrected without rerunning probes or changing expectations. Source pypdf Xref warnings and synthetic Poppler display-font configuration warnings remain in raw logs. The latter did not affect the rectangle-only pixel oracle, which compares exactly.

## Limits and coordinator action

`validate(document)` without a root only establishes internal consistency and reports source structure unverified. Root validation establishes the actual pinned source's count and geometry; self-consistent registry/evidence claims do not authenticate authors or derivation authority. A sidecar exclusion scope is coverage-independent to avoid circular hashes; it deliberately excludes coverage fields and page labels/evidence. A changed coverage rationale can therefore retain author-scope freshness while source-IG review freshness remains unknown. This never constitutes a current approved IG-1A whole-record exclusion. Later reconciliation must apply the unchanged full-record IG-1A target/inventory review contract and verify the real human statement independently.

All 44 pages remain substantive unprocessed placeholders. Full-profile source completeness, source meaning, semantic acceptance, compilation and executable readiness were not assessed. No IG-2B task was performed. Tokens, cost and operator time remain null.

Session UTC start `{started}`; evidence-review end `{ended}`; elapsed {measurement['wall_seconds']:.3f} seconds. `measurement.json` records these boundaries; the final seal separately records the later freeze end and total wall time. The initial helper failure's command-level UTC boundaries were not captured and remain null; its tool-reported elapsed time is retained.

Coordinator next action: verify this review's final seal/manifest and pinned delivery, then make the coordinator-owned technical acceptance decision through the repository workflow if justified. This reviewer performed no transition and grants no semantic decision. Stop here; IG-2B needs a separate operator/coordinator instruction.
'''
    
(RUN/'report.md').write_text(report,encoding='utf-8')
review={'role':'reviewer','actor':ACTOR,'task':'IG-2A','summary':'PASS: five repaired prior findings independently closed; no new actionable findings. Technical handoff only.','outcome':'PASS','criteria':criteria_strings,'artifacts':read(REPAIR/'delivery.json')['artifacts']+[pin(RUN/p) for p in ['configuration.json','report.md','findings.json','dispositions.json','criteria.json','measurement.json','input-verification.json','preservation-final.json','probe-results.json','retained-reproduction-results.json','independent-pixel-oracles.json','independent-integer-pixel-boundaries.json','visual-inspection.json','repeatability.json','delivery-inventory-validation.json']],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':pin(RUN/'configuration.json')['path'],'checks':checks,'measurement':measurement,'semantic_acceptance_granted':False,'executable_readiness':'unassessed','new_actionable_findings':0}
write('review.json',review)
handoff={'role':'reviewer','actor':ACTOR,'task':'IG-2A','outcome':'PASS','review':pin(RUN/'review.json'),'report':pin(RUN/'report.md'),'delivery':pin(REPAIR/'delivery.json'),'delivery_manifest':pin(REPAIR/'delivery-manifest.json'),'delivery_final_seal':pin(REPAIR/'final-seal.json'),'closed_findings':[f['id'] for f in old_findings],'new_actionable_findings':0,'criteria':criteria_strings,'queue_unchanged':True,'queue_status':'review','semantic_acceptance_granted':False,'next_action':'Coordinator verifies this independent review seal/manifest and exact delivery before any coordinator-owned technical acceptance transition. No IG-2B from this review; no human semantic decision supplied.'}
write('coordinator-handoff.json',handoff)
print('Report and coordinator handoff prepared; freeze remains')
