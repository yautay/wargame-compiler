"""Pin IG-1D inputs/ownership and operator-approved deterministic export profile."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
R=Path(__file__).parent
ROOT=Path.cwd()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def art(p):return {'path':p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix(),'sha256':sha(p)}
def write(n,d):
 with (R/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,indent=2);f.write('\n')
q=read('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-1D')
if len(sys.argv)==1:
 assert t['status']=='planned'
 c=next(t for t in q['tasks'] if t['id']=='IG-1C');assert c['status']=='done'
 delivery=Path('private/workflow/runs/IG-1C/repair-01-20261013/delivery.json')
 for a in read(delivery)['artifacts']:assert sha(a['path'])==a['sha256']
 assert not Path('private/ig/projects/spqr/records').exists(),'Existing registry must be triaged, not replaced'
 write('queue-before.json',q)
 write('operator-profile-approval.json',{'role':'operator','recorded_utc':datetime.now(timezone.utc).isoformat(),'direct_current_conversation_response':'zgodnie z zaleceniem','response_to':'Explicit choice of separate recommended wgc-source-export-1 profile in the immediately preceding question','approved_proposal':art(R/'source-export.schema.proposed.json'),'approved_patch':art(R/'profile-proposal.patch'),'scope':'Only versioned export profile within src/wgc/export; canonical run timestamps null and real measurements sidecar; original source-v1 foundation remains byte-preserved','human_semantic_acceptance_granted':False})
 write('initial-registry.json',{'format':'wgc-wgu-identity-1','namespace':'wgu.spqr','next_identity':1,'next_gap':1,'entries':[],'gaps':[]})
 pin=[Path('private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json'),Path('contracts/ig/source.schema.json'),Path('contracts/ig/README.md'),Path('src/wgc/contracts/source.py'),Path('private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json'),Path('private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json'),R/'initial-registry.json',R/'source-export.schema.proposed.json',R/'operator-profile-approval.json']
 t['inputs']=[p.as_posix()+' SHA-256 '+sha(p) for p in pin]
 t['inputs']+=['Approved deterministic source-export profile: wgc-source-export-1, mechanical/hash/reference rules unchanged; actual operational timestamps/configuration/measurements sidecar outside canonical artifact hashes. No frozen foundation edits.','No previous identity registry exists; explicitly pinned empty namespace wgu.spqr seed. Persist allocations/aliases/lineage; array positions/content hashes/titles/filenames are never ID generators.','Only NEW assigned test files; preserve IG-1C parser.py/importer.py and its accepted tests unchanged.']
 t['outputs']+=['Operator-approved versioned source-export schema/profile with null canonical run timestamps and separate operational evidence']
 t['context']+=['contracts/ig/README.md','src/wgc/contracts/source.py']
 t['export_profile_decision']=art(R/'operator-profile-approval.json')
 with Path('docs/work/queue.json').open('w',encoding='utf-8',newline='\n') as f:json.dump(q,f,ensure_ascii=False,indent=2);f.write('\n')
 write('ready.json',{'role':'coordinator','actor':'ig1-stage-executor-20261013','summary':'IG-1C independently reviewed, accepted and done; exact complete import/source/schema/empty identity inputs pinned; operator explicitly approved minimal deterministic export profile without modifying frozen foundation. Only IG-1D becomes ready; one executor writer retains ownership.','criteria':t['start_conditions'],'artifacts':[art(p) for p in [R/'operator-profile-approval.json',R/'initial-registry.json',R/'source-export.schema.proposed.json',delivery]],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Earlier direct operator UI confirmation in this same ongoing executor conversation: sol 6.1 high; no settings change requested or observed.'})
 print('IG-1D exact inputs/profile approval/readiness prepared')
else:
 assert sys.argv[1]=='claim' and t['status']=='ready'
 packet=Path(sys.argv[2]);m=read(packet/'manifest.json')
 for a in m['files']:assert sha(a['path'])==a['sha256']
 assert sha(packet/'context.txt')==m['context_sha256']
 scope=['src/wgc/wgu_adapter/identity.py','src/wgc/wgu_adapter/references.py','src/wgc/export']
 assert not any(Path(p).exists() for p in scope)
 write('checkpoint.json',{'task':'IG-1D','actor':'ig1-stage-executor-20261013','started_utc':datetime.now(timezone.utc).isoformat(),'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct current-conversation operator UI observation retained with same-session continuity: sol 6.1 high; no setting change requested/observed.','input_packet':art(packet/'manifest.json'),'base_product_files':[],'protected_IG_1C_delivery':art(Path('private/workflow/runs/IG-1C/repair-01-20261013/delivery.json')),'profile_approval':art(R/'operator-profile-approval.json'),'write_scope':t['write_scope'],'next_operation':'Implement persisted identities/lineage, exact reference diagnostics and deterministic structural export; new synthetic tests and private full export; independent reviewer gate before acceptance.','tokens':None,'cost':None})
 write('claim.json',{'role':'executor','actor':'ig1-stage-executor-20261013','summary':'Claim only ready IG-1D after done IG-1C and explicit export-profile contract decision; fresh packet hashes, empty previous registry and protected parent delivery pinned.','criteria':t['start_conditions'],'artifacts':[art(R/n) for n in ['checkpoint.json','operator-profile-approval.json','initial-registry.json']],'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct earlier operator UI confirmation in this same ongoing executor conversation; no observed/requested configuration change.'})
 print('IG-1D claim prepared')
