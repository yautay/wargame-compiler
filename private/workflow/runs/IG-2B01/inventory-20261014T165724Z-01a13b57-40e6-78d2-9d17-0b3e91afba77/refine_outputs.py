from prepare import *
q=read('docs/work/queue.json'); t=next(x for x in q['tasks'] if x['id']=='IG-2B01')
old=copy.deepcopy(t)
t['outputs']=[f'{REL}/final/inventory.json (full 44-page wgc-inventory-1; pages 1-4 authored; original placeholder records 5-44 retained)',f'{REL}/final/identity-registry.json',f'{REL}/authored/ (replayable pre-evidence inventory and extended persisted registry)',f'{REL}/evidence/ (131 exact region text/PNG/crop-PDF triples, including 1 context-only region)',f'{REL}/region-ledger.json, scope-report.json, continuations.json, uncertainty.json, gaps.json, geometric-gaps.json',f'{REL}/delivery-manifest.json, delivery.json, delivery-handoff.md']
t['write_scope']=[REL+'/', 'private/workflow/packets/', 'private/workflow/checks/']
write(f'{REL}/output-refinement.json',{'role':'coordinator','actor':ACTOR,'utc':datetime.now(timezone.utc).isoformat(),'reason':'Name the final evidence-bearing inventory separately from its retained pre-evidence replay input. Clarify workflow-owned packet/check directories; executor content remains confined to this attempt. No source pages, contract, criteria, task state or other task scope changed.','prior_outputs':old['outputs'],'outputs':t['outputs'],'prior_write_scope':old['write_scope'],'write_scope':t['write_scope'],'packet_directory_constraint':'Only newly generated IG-2B01 packets; no edits to prior packets or other tasks.'})
write('docs/work/queue.json',q)
r=run('output-refinement-render',[sys.executable,'scripts/workflow.py','render']); assert r.returncode==0
r=run('output-refinement-validate',[sys.executable,'scripts/workflow.py','validate']); assert r.returncode==0
