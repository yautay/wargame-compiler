from prepare import *
mode=sys.argv[1]
def checked(name,args):
 r=run(name,args)
 if r.returncode: raise RuntimeError(f'{name}: inspect queue/event before retry')
 return r
if mode=='prepare':
 scope=read(f'{REL}/scope-report-final.json'); doc=read(f'{REL}/final-verified/inventory.json'); ledger=read(f'{REL}/region-ledger-final.json')
 # The corrected locator is the final version. Old evidence and all development artifacts remain intact.
 q=read('docs/work/queue.json'); task=next(t for t in q['tasks'] if t['id']=='IG-2B01')
 write(f'{REL}/final-output-selection.json',{'actor':ACTOR,'role':'coordinator','utc':datetime.now(timezone.utc).isoformat(),'final_inventory':pin(f'{REL}/final-verified/inventory.json'),'final_ledger':pin(f'{REL}/region-ledger-final.json'),'reason':'One visual locator correction; retain all earlier derivations. Final-verified supersedes final only as the review target, without deleting or overwriting either.'})
 task['outputs']=[x.replace('/final/inventory.json','/final-verified/inventory.json').replace('/final/identity-registry.json','/final-verified/identity-registry.json').replace('/region-ledger.json','/region-ledger-final.json').replace('scope-report.json','scope-report-final.json') for x in task['outputs']]
 write('docs/work/queue.json',q)
 checked('final-output-render',[sys.executable,'scripts/workflow.py','render'])
 checked('before-freeze-workflow',[sys.executable,'scripts/workflow.py','validate'])
 checked('before-freeze-dry-run',[sys.executable,'scripts/workflow.py','dry-run','--task','IG-2B01'])
 # A fresh final packet supplements the retained preclaim packet; both are verified independently.
 r=checked('final-packet-command',[sys.executable,'scripts/workflow.py','packet','--task','IG-2B01']); p=r.stdout.strip();m=read(p+'/manifest.json')
 for a in m['files']: assert pin(a['path'])['sha256']==a['sha256']
 assert pin(p+'/context.txt')['sha256']==m['context_sha256']
 write(f'{REL}/final-input-packet.json',{'manifest':pin(p+'/manifest.json'),'context':pin(p+'/context.txt'),'queue_sha256':m['queue_sha256'],'all_files_verified':True,'original_packet':pin(f'{REL}/input-packet.json'),'supplement':pin(f'{REL}/final-output-selection.json')})
 checked('before-freeze-diff',['git','diff','--check'])
 visual={'actor':ACTOR,'role':'executor','independent_review':False,'original_pages_viewed':[pin(f'{REL}/pages/original-{p:02}.png') for p in range(1,5)],'overlay_pages_viewed':[pin(f'{REL}/overlays-verified/page-{p:02}.png') for p in range(1,5)],'observations':[
 {'page':1,'observation':'Cover series line, vector SPQR logo, subtitle, battle artwork/frame, designer/title/edition lines, two-column contents with 12 entries/dot leaders/destinations, panel frame and publisher address inventoried. Hidden template header/folio/copyright remain explicit extraction artifacts, not visible cover labels. Logo locator widened after image inspection.'},
 {'page':2,'observation':'Left introduction, edition/player notes and split new-player note; right continuation, ten component bullets, map/piece headings and clauses 2.21/2.22/2.23 inventoried. 2.23 continues at page 3. No separate source footnote or mechanical outcome table observed.'},
 {'page':3,'observation':'Continuation, four legion skill bullets, markings/border and historical descriptions, leader/marker paragraphs; boxed 2.25 panel with annotated phalanx/infantry/cavalry/scorpion/elephant diagrams, captions/leader lines/legends and five additional samples; die and terminology entries inventoried. Raster counter symbols retain transcription uncertainty.'},
 {'page':4,'observation':'Sixteen left-column terminology entries; right type/ZOC/army/legion descriptions and four counter illustrations with wrapped description fragments inventoried. Triarii sentence continues into exact two-line page 5 context crop.'}],
 'context':'Only final narrow Triarii crop inspected for continuation; initial wider probe deviation disclosed in context-overread.json. Context contributes zero denominator.','limits':'Visual executor observations and word-center accounting do not certify source meaning, human acceptance or independent review.'}
 write(f'{REL}/visual-inspection.json',visual)
 criteria=[]
 for i,c in enumerate(task['acceptance']):
  criteria.append({'criterion':c,'status':'pending_independent_review' if i==2 else 'executor_delivery_met_pending_independent_review','evidence':[f'{REL}/region-ledger-final.json',f'{REL}/locator-audit.json',f'{REL}/visual-inspection.json',f'{REL}/continuations.json',f'{REL}/gaps.json'],'limitations':'Separate reviewer must compare all assigned original pages and the exact complete region ledger. This session cannot supply independent review.' if i==2 else 'Complete authored inventory proposal with explicit extraction/representation/geometric gaps; no semantic acceptance or approved exclusion.'})
 write(f'{REL}/criteria.json',criteria)
 started=datetime.fromtimestamp(RUN.stat().st_birthtime,timezone.utc);end=datetime.now(timezone.utc)
 measurement={'actor':ACTOR,'model':'gpt-6.1-sol','reasoning':'high','started_utc':started.isoformat(),'ended_utc':end.isoformat(),'wall_seconds':(end-started).total_seconds(),'measurement_scope':'Observed attempt-directory creation through delivery preparation; preliminary reads and operator-confirmation conversation preceded this measured window. Configuration file approximate session-start estimate is not used as an exact measurement.','session_start_utc':None,'session_start_unknown_reason':'Session-start timestamp is not exposed; initial approximate estimate is explicitly not measured.','input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None}
 write(f'{REL}/measurement.json',measurement)
 report=f'''# IG-2B01 inventory delivery

Outcome: authored inventory of official SPQR 5E physical pages 1-4, ready for separate independent review. Executor {ACTOR}, GPT-6.1 Sol/high confirmed directly by the current-session operator before claim. No semantic acceptance, approved exclusion, gameplay decision, acceptance/done or IG-2B02 execution.

The final review target is `{REL}/final-verified/inventory.json`, with persisted `identity-registry.json`, complete `region-ledger-final.json`, `scope-report-final.json`, `continuations.json`, `uncertainty.json`, `gaps.json` and `geometric-gaps.json`. The final inventory retains all 44 physical page records, unchanged page and placeholder records 5-44, and all original registry entries. Four old placeholder memberships are replaced by 130 independently authored regions: page 1: 26; page 2: 31; page 3: 38; page 4: 35. The task denominator is 130; full-inventory denominator 170 includes 40 unprocessed out-of-task placeholders; one page 5 context region contributes zero. No KB headings/data were used.

All headings, paragraphs, list items, notes, diagrams/legends/captions, sample counters, navigation table rows and editorial furniture observed on the four rendered pages are addressed. Grouped diagrams retain a component checklist naming embedded captions, legends, arrows and counter content; no additional denominator units are invented for their embedded components. Reading order explicitly traverses left then right columns with recorded fragment links. The cover's hidden running text/folio is distinguished from visible ink. Printed labels 2/3/4 have exact current same-page folio evidence; cover and 5-44 stay unknown.

Each authored region and context has separate original-source/revision/page/bbox pins, UTF-8 extracted text, PNG and cropped PDF. The ledger records exact integer-millionth locators and rational native bounds; root validation checks source bytes/count/geometry, page-basis freshness, region revisions, artifact hashes, Unicode offsets and exact predicted/actual PNG dimensions. Persisted-registry replay reproduces canonical author bytes and UUIDs. Old page-1 logo evidence is retained; a visual inspection found a tight right edge and the final locator/evidence were corrected in a fresh directory without changing identity or tools.

Transcription remains partial for authored content; all descriptive/formal semantics remain unprocessed. Machine extraction may contain replacement glyphs, line-wrap artifacts and absent raster/vector text, and cover extraction includes hidden template text. These issues, all region-level representation gaps and exact geometric complements are retained. A bbox or PNG never grants represented status. Editorial classification never grants an exclusion. Sidecar structure does not authenticate a human or replace frozen IG-1A exact whole-record review. No gameplay legality was resolved.

Page 4's Triarii entry finishes in two lines at page 5 top left. The final context crop is x=44..303, y=50..78 PDF top-left points. The initial y=50..105 probe inadvertently exposed two lines and part of a counter from the next entry; this bounded access deviation is disclosed and retained, with no analysis or denominator use of neighboring material. Pages 6-44 received structural count/geometry access only. No PDF download or external API occurred.

Validation includes unchanged `scripts/check.ps1 -Task IG-2B01` while active (102 tests passed), root inventory validation, 131 exact evidence-locator audits, all four original-page and overlay visual inspections, text word-center accounting, explicit geometric-gap accounting, unchanged-placeholder checks, canonical registry replay, workflow validation/dry-run and `git diff --check`. Full logs, command argv/UTC/exit codes and timings are preserved. The first author draft failed overlap validation; locator/edge authoring was corrected without changing the validator. The existing pypdf nonzero-index Xref warning is retained. Source/tool/schema/product hashes and all other 38 task records are unchanged. Full project tests ran before the final private locator correction; their code inputs did not change, and final private content checks ran afterward.

Every criterion is assessed in `criteria.json`. The independent-review criterion remains pending: this executor's inspection is not independent review. The next reviewer must compare all four original pages with the exact final ledger, inspect grouped legends/counter boundaries, the logo correction, word/geometric gaps, narrow continuation and access-deviation disclosure, and verify all delivery hashes. No acceptance/done should be inferred from green structural checks.

Measured attempt UTC {measurement['started_utc']} to {measurement['ended_utc']}, {measurement['wall_seconds']:.3f} seconds at delivery preparation. Exact process timings are separately recorded; preliminary/session-start elapsed time is unknown. Tokens, cost and operator time are null. Final transition/seal measurements follow separately. Stop after in_progress -> review.
'''
 (RUN/'delivery-handoff.md').write_text(report,encoding='utf-8',newline='\n')
 cp=read(f'{REL}/checkpoint-preclaim.json');cp.update(completed_criteria=criteria,changed_files=[pin(f'{REL}/final-verified/inventory.json'),pin(f'{REL}/region-ledger-final.json')],final_packet=pin(f'{REL}/final-input-packet.json'),next_operation='Freeze exact delivery, transition to review, stop.',blocker=None)
 write(f'{REL}/checkpoint.json',cp)
 print('Delivery preparation complete; inspect visual observations before freeze.')
elif mode=='seal':
 q=read('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-2B01');assert t['status']=='in_progress'
 checks=[read(f'{REL}/{n}.json') for n in ['project-check','author-final','derive-command','logo-correction-command','assess-command','before-freeze-workflow','before-freeze-dry-run','before-freeze-diff']]
 assert all(c['exit_code']==0 for c in checks)
 excludes={'delivery-manifest.json','delivery.json','final-seal.json'}
 artifacts=[pin(p) for p in sorted(RUN.rglob('*')) if p.is_file() and p.name not in excludes]
 # Hand over check logs, not unnecessary synthetic scratch trees.
 checkroot=Path('private/workflow/checks/active-6bd5604a2b824da8a0eb4a1b5aad0961')
 artifacts += [pin(p) for p in sorted(checkroot.glob('*')) if p.is_file()]
 for key in ['input-packet.json','final-input-packet.json']:
  packet=read(f'{REL}/{key}');artifacts.extend([packet['manifest'],packet['context']])
 unique={a['path']:a for a in artifacts};artifacts=sorted(unique.values(),key=lambda a:a['path'])
 manifest={'format':'wgc-delivery-manifest-1','task':'IG-2B01','actor':ACTOR,'artifacts':artifacts,'final_inventory':pin(f'{REL}/final-verified/inventory.json'),'criteria':read(f'{REL}/criteria.json'),'checks':checks,'measurement':read(f'{REL}/measurement.json'),'exclusions':'This manifest cannot hash itself. delivery.json pins it; final-seal.json pins subsequent governance logs and the exact delivery. All retained intermediate artifacts remain clearly distinct from final review targets.','independent_review':None,'semantic_acceptance_granted':False}
 write(f'{REL}/delivery-manifest.json',manifest)
 delivery={'role':'executor','actor':ACTOR,'summary':'IG-2B01 authored 130-region physical-pages-1-4 inventory with full 44-page accounting, exact evidence and explicit gaps; independent review requested.','model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Current-session direct operator confirmation recorded in configuration.json; actual CODEX_THREAD_ID matches actor.','criteria':t['acceptance'],'artifacts':artifacts+[pin(f'{REL}/delivery-manifest.json')],'checks':checks,'measurement':read(f'{REL}/measurement.json'),'independent_review':None,'semantic_acceptance_granted':False}
 write(f'{REL}/delivery.json',delivery)
 for a in delivery['artifacts']: assert pin(a['path'])==a,a['path']
 r=run('review-transition',[sys.executable,'scripts/workflow.py','transition','--task','IG-2B01','--to','review','--evidence',f'{REL}/delivery.json'])
 if r.returncode: raise RuntimeError('Inspect actual queue status and evidence/event hash before any retry')
 checked('post-review-workflow',[sys.executable,'scripts/workflow.py','validate']);checked('post-review-diff',['git','diff','--check'])
 q=read('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-2B01');assert t['status']=='review'
 for a in delivery['artifacts']: assert pin(a['path'])==a,a['path']
 for a in read(f'{REL}/base-products.json')['files']: assert pin(a['path'])==a
 before=read(f'{REL}/queue-before.json');assert [x for x in q['tasks'] if x['id']!='IG-2B01']==[x for x in before['tasks'] if x['id']!='IG-2B01']
 end=datetime.now(timezone.utc);start=datetime.fromtimestamp(RUN.stat().st_birthtime,timezone.utc)
 write(f'{REL}/final-seal.json',{'task':'IG-2B01','status':'review','actor':ACTOR,'model':'gpt-6.1-sol','reasoning':'high','delivery':pin(f'{REL}/delivery.json'),'manifest':pin(f'{REL}/delivery-manifest.json'),'handoff':pin(f'{REL}/delivery-handoff.md'),'final_inventory':pin(f'{REL}/final-verified/inventory.json'),'queue_event':t['events'][-1],'governance_artifacts':[pin(p) for p in sorted(RUN.glob('*')) if p.is_file() and (p.name.startswith('review-transition') or p.name.startswith('post-review'))],'all_delivery_pins_reverified':True,'other_38_tasks_unchanged':True,'base_products_unchanged':True,'independent_review':None,'semantic_acceptance_granted':False,'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'wall_seconds':(end-start).total_seconds(),'input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None,'next_action':'Separate independent review of exact final inventory/ledger and all assigned pages. No acceptance/done or IG-2B02.'})
 print('FROZEN REVIEW',pin(f'{REL}/final-seal.json'))
else: raise ValueError(mode)
