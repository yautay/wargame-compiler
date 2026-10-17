"""Coordinator closure only: verify frozen decisions; no delivery/content repair."""
import copy, hashlib, importlib.util, json, os, subprocess, sys, time, uuid
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path.cwd().resolve(); RUN=Path(__file__).resolve().parent; REL=RUN.relative_to(ROOT).as_posix()
ACTOR='codex-01a13b57-40e6-78d2-9d17-0b3e91afba77'
BASE='private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77'
REV='private/workflow/runs/IG-2B01/review-20261014T171920Z-01a13b6c-f981-7192-a5ff-1126c809cd63'
sys.dont_write_bytecode=True
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(name,d): (RUN/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=Path(p);p=p if p.is_absolute() else ROOT/p
 assert p.resolve().is_relative_to(ROOT)
 raw=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def verify(a):
 got=pin(a['path']);assert got['sha256']==a['sha256'],a['path']
 if 'bytes' in a: assert got['bytes']==a['bytes'],a['path']
 return got
def command(name,args):
 start=datetime.now(timezone.utc);t=time.monotonic()
 result=subprocess.run(args,capture_output=True,encoding='utf-8',errors='replace')
 (RUN/(name+'.stdout')).write_text(result.stdout,encoding='utf-8');(RUN/(name+'.stderr')).write_text(result.stderr,encoding='utf-8')
 record={'command':subprocess.list2cmdline(args),'argv':args,'exit_code':result.returncode,'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'stdout':pin(RUN/(name+'.stdout')),'stderr':pin(RUN/(name+'.stderr'))}
 save(name+'.json',record);print(name,result.returncode,result.stdout[:300],result.stderr[:200],flush=True)
 return result
def checked(name,args):
 result=command(name,args);assert result.returncode==0,name;return result
def reverify():
 d=read(f'{REL}/verification.json')
 for a in d['immutable_pins']: verify(a)
 return d
def transition(state,evidence):
 q=read('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-2B01');old=t['status'];prior=copy.deepcopy(t['events'])
 result=command(state+'-transition',[sys.executable,'-B','scripts/workflow.py','transition','--task','IG-2B01','--to',state,'--evidence',f'{REL}/{evidence}'])
 current=read('docs/work/queue.json');task=next(t for t in current['tasks'] if t['id']=='IG-2B01')
 committed=task['status']==state and task['events'][:-1]==prior and task['events'][-1]['from']==old and task['events'][-1]['evidence']==f'{REL}/{evidence}' and task['events'][-1]['sha256']==pin(f'{REL}/{evidence}')['sha256']
 save(state+'-event-verification.json',{'command_exit':result.returncode,'committed_event_verified':committed,'actual_status':task['status'],'event':task['events'][-1],'evidence':pin(f'{REL}/{evidence}'),'transition_retried':False})
 assert committed,'Stop: transition not committed as expected. Do not retry automatically.'
 if result.returncode:
  # Projection-only recovery: use the unchanged workflow generator, never replay an event.
  module_spec=importlib.util.spec_from_file_location('closure_workflow',ROOT/'scripts/workflow.py'); module=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(module)
  module.validate(current,ROOT,check_views=False);recovered=[]
  for rel,body in module.views(current).items():
   target=ROOT/rel
   if target.is_file() and target.read_text(encoding='utf-8')==body: continue
   before=target.read_bytes() if target.exists() else None
   name='projection-before-'+rel.replace('/','_')
   if before is not None: (RUN/name).write_bytes(before)
   tmp=target.with_name(target.name+'.closure-'+uuid.uuid4().hex+'.tmp')
   tmp.write_text(body,encoding='utf-8',newline='\n');os.replace(tmp,target)
   recovered.append({'path':rel,'before':pin(RUN/name) if before is not None else None,'after':pin(rel)})
  save(state+'-projection-recovery.json',{'reason':'Transition event committed before failed CLI projection; regenerate only exact workflow.views bytes by atomic replacement.','command_exit':result.returncode,'event_repeated':False,'recovered':recovered})
  checked(state+'-recovery-validate',[sys.executable,'-B','scripts/workflow.py','validate'])
def process_environment():
 tool=read(f'{BASE}/toolchain.json');os.environ['PYTHONPATH']=tool['process_pythonpath'];os.environ['PATH']=tool['process_path_prefix']+';'+os.environ['PATH'];os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['PYTHONIOENCODING']='utf-8'

mode=sys.argv[1]
if mode=='prepare':
 start=datetime.now(timezone.utc).isoformat()
 save('configuration.json',{'role':'coordinator','actor':ACTOR,'session_id':os.environ.get('CODEX_THREAD_ID'),'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':'Direct operator confirmation earlier in this same session: Potwierdzam: GPT-6.1 Sol / high. No new executor/reviewer identity is claimed.','closure_started_utc':start,'input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None})
 save('operator-authorization.json',{'role':'human_operator','statement':'Zweryfikuj hashe review i delivery, rozlicz P2 i P3, a jeśli nie ma blokad, zamknij IG-2B01 przez acceptance → done. Nie rozpoczynaj IG-2B02.','source':'Current operator message in this chat','scope':'Verify frozen hashes, record coordinator dispositions, technical review -> accepted -> done for IG-2B01 only. No semantic acceptance or IG-2B02.'})
 q=read('docs/work/queue.json');save('queue-before.json',q)
 task=next(t for t in q['tasks'] if t['id']=='IG-2B01');assert task['status']=='review' and not task['semantic_acceptance_required']
 expected={f'{REV}/review-seal.json':'25fdb8b32e93470d9ceee699dbb2e369a2ad4c3dc6ab454579c8a34fe58aa2c5',f'{BASE}/final-seal.json':'92d0497dcdd19876127217917bb30240ff17e8893d7cc2b195d342fb53d69e13',f'{BASE}/delivery.json':'9fd4b11bdfd04e75edafca96daa29add39151612291b2fefbd7a68e534325ef7',f'{BASE}/delivery-manifest.json':'1d8ad7eaa494f14a95c762de3197ae7b9c4be057a1e4470e11987d56761fd5fc'}
 pins={};groups={}
 def take(items,name):
  groups[name]=len(items)
  for a in items: pins[a['path']]=verify(a)
 take([{'path':p,'sha256':h} for p,h in expected.items()],'operator_anchor_pins')
 rs=read(f'{REV}/review-seal.json'); ds=read(f'{BASE}/final-seal.json')
 take([v for v in rs.values() if isinstance(v,dict) and 'path' in v and 'sha256' in v],'review_seal_direct')
 take(rs['original_delivery_pins'],'review_seal_original_delivery')
 take([v for v in ds.values() if isinstance(v,dict) and 'path' in v and 'sha256' in v],'delivery_seal_direct')
 take(ds['governance_artifacts'],'delivery_seal_governance')
 review=read(rs['review']['path']);rm=read(rs['manifest']['path']);delivery=read(ds['delivery']['path']);dm=read(ds['manifest']['path']);handoff=read(rs['handoff']['path'])
 for name,items in [('review_manifest',rm['artifacts']),('review_external_logs',rm['external_check_logs']),('review_artifacts',review['artifacts']),('delivery_artifacts',delivery['artifacts']),('delivery_manifest',dm['artifacts']),('handoff_check_logs',handoff['check_scratch_logs']),('base_products',read(f'{BASE}/base-products.json')['files'])]: take(items,name)
 take([review['configuration_evidence']],'review_configuration')
 assert review['actor']!=delivery['actor'] and review['role']=='reviewer' and review['outcome']=='PASS'
 assert rs['outcome']==handoff['outcome']=='PASS' and review['blocking_findings']==0
 assert review['artifacts']==delivery['artifacts']
 assert review['criteria']==task['acceptance'] and all(c['outcome']=='PASS' for c in review['criterion_results'])
 assert all(c['exit_code']==0 for c in review['checks'])
 verify({'path':task['events'][-1]['evidence'],'sha256':task['events'][-1]['sha256']})
 assert task['events'][-1]['evidence']==f'{BASE}/delivery.json'
 doc=read(f'{BASE}/final-verified/inventory.json');take([doc['source']['pdf'],doc['source']['provenance']],'source_pins')
 context=[r for r in doc['regions'] if r['denominator_role']=='context'];assert len(context)==1 and context[0]['box']==[71895,63131,495099,98485]
 c=context[0];ce=next(e for e in doc['evidence'] if e['region_id']==c['id']);take([ce['image'],ce['text'],ce['crop_pdf']],'final_context')
 scope=read(f'{BASE}/scope-report-final.json');assert scope['task_denominator']==130 and scope['context_denominator']==0 and scope['represented_at_any_level']==scope['excluded_at_any_level']==0
 edition=next(r for r in doc['regions'] if r['key']=='ig2b01:cover:edition');ee=next(e for e in doc['evidence'] if e['region_id']==edition['id']);take([ee['text'],ee['image']],'edition_evidence')
 text=(ROOT/ee['text']['path']).read_text(encoding='utf-8');assert text=='E5th EdBition' and text[0]=='E' and text[7]=='B'
 assert edition['coverage']['transcription']['status']=='partial'
 save('verification.json',{'task':'IG-2B01','outcome':'PASS','verified_utc':datetime.now(timezone.utc).isoformat(),'groups':groups,'unique_immutable_pins':len(pins),'immutable_pins':sorted(pins.values(),key=lambda p:p['path']),'reviewer':review['actor'],'executor':delivery['actor'],'exact_review_delivery_artifact_list_equal':True,'exact_criteria_pass':True,'blocking_findings':0,'context':{'region':c,'evidence':ce,'task_denominator':130,'context_denominator':0},'edition':{'region':edition,'evidence':ee,'literal_text':text,'extra_offsets':[0,7]},'initial_broad_probe_content_reopened':False})
 save('checkpoint.json',{'task':'IG-2B01','actor':ACTOR,'role':'coordinator','configuration':pin(RUN/'configuration.json'),'verification':pin(RUN/'verification.json'),'original_queue':pin(RUN/'queue-before.json'),'completed':['Frozen review/delivery and every manifest member verified; exact criteria and independent attribution checked.'],'next_operation':'Inspect only final context and edition PNG, record P2/P3 dispositions, then technical acceptance.','blocker':None})
 checked('initial-workflow',[sys.executable,'-B','scripts/workflow.py','validate']);checked('initial-next',[sys.executable,'-B','scripts/workflow.py','next'])
 print('VERIFIED',groups,'unique',len(pins),'context_image',ce['image']['path'],'edition_image',ee['image']['path'],flush=True)
elif mode=='accept':
 reverify();v=read(f'{REL}/verification.json');review=read(f'{REV}/review.json');delivery=read(f'{BASE}/delivery.json')
 save('finding-dispositions.json',{'role':'coordinator','actor':ACTOR,'operator_authorization':pin(RUN/'operator-authorization.json'),'review':pin(f'{REV}/review.json'),'utc':datetime.now(timezone.utc).isoformat(),'decisions':[
 {'finding':'IG2B01-R01','severity':'P2','decision':'Contained disclosed process deviation acknowledged; nonblocking for technical acceptance of the exact final inventory.','facts':'The initial page-5 probe y=50..105 exposed neighboring entry material, as preserved in immutable disclosure metadata. This was outside the minimal continuation need. Final context is the exact two-line Triarii tail at [71895,63131,495099,98485], contributes zero denominator, and independent review found no resulting inventory omission/corruption.','basis':[pin(f'{BASE}/context-overread.json'),pin(f'{BASE}/context-access-authorization.json'),pin(f'{REV}/review-report.md')],'verification':'All exact context pins checked; final narrow PNG observed. Initial broad source/probe was not reopened.','limits':'Prior exposure is not undone, retroactively authorized or declared compliant. No neighboring-entry review is claimed.','preventive_action':'Future continuation probes should start with narrow predetermined boundaries; expansion needs a recorded concrete continuation necessity. Retain all disclosure bytes.','artifact_repair_required':False},
 {'finding':'IG2B01-R02','severity':'P3','decision':'Resolved for this inventory closure by explicitly retaining a revision-bound transcription advisory; future exact-transcription work must address it before promoting coverage.','facts':{'region_id':v['edition']['region']['id'],'region_revision':v['edition']['region']['revision'],'evidence':v['edition']['evidence'],'literal':'E5th EdBition','extra_unicode_offsets':[0,7],'visible_png':'5th Edition','transcription_status':'partial'},'verification':'Literal UTF-8 text/codepoints and exact PNG checked; reviewer independently reproduced both.','limits':'Raw evidence and publisher bytes remain unchanged. Visible text is an observation, not an accepted normalized transcription, human semantic decision or represented coverage.','future_action':'Carry this precise anomaly, offsets and PNG basis into any later exact-transcription/reconciliation work. No downstream task is started or modified.','artifact_repair_required':False}],
 'blocking_findings_remaining':0,'semantic_acceptance_granted':False,'source_ig_whole_record_review_granted':False})
 save('criteria.json',{'criteria':review['criterion_results'],'coordinator_assessment':'All exact queue criteria are met in the bounded inventory scope based on the separate reviewer PASS and verified frozen evidence. P2/P3 disposition is recorded separately; no semantic approval is inferred.','basis':[pin(f'{REV}/review.json'),pin(RUN/'verification.json'),pin(RUN/'finding-dispositions.json')]})
 checked('before-accepted-workflow',[sys.executable,'-B','scripts/workflow.py','validate']);checked('before-accepted-diff',['git','diff','--check'])
 accepted=copy.deepcopy(review)
 # Preserve independent reviewer attribution. The coordinator only records that verified decision after resolving its stated condition.
 accepted.update(recorded_by=ACTOR,recording_role='coordinator',decision_attribution={'reviewer':review['actor'],'source_review':pin(f'{REV}/review.json'),'source_seal':pin(f'{REV}/review-seal.json'),'coordinator_recording':'Same frozen reviewer PASS and mandatory artifact list copied without changing reviewer identity or claiming new independent review. Coordinator separately disposes the acknowledged P2/P3 findings under explicit operator instruction.'},coordinator_disposition=pin(RUN/'finding-dispositions.json'),coordinator_verification=pin(RUN/'verification.json'),coordinator_criteria=pin(RUN/'criteria.json'),operator_authorization=pin(RUN/'operator-authorization.json'))
 accepted['summary']='Coordinator-recorded independent technical PASS for exact IG-2B01 delivery after verified hashes and explicit nonblocking P2/P3 dispositions.'
 assert accepted['actor']!=delivery['actor'] and accepted['artifacts']==delivery['artifacts']
 save('accepted.json',accepted);transition('accepted','accepted.json')
elif mode=='check':
 process_environment();checked('project-check',['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-2B01'])
elif mode=='done':
 reverify();q=read('docs/work/queue.json');task=next(t for t in q['tasks'] if t['id']=='IG-2B01');assert task['status']=='accepted'
 accepted=read(f'{REL}/accepted.json');project=read(f'{REL}/project-check.json');assert project['exit_code']==0
 checked('before-done-workflow',[sys.executable,'-B','scripts/workflow.py','validate']);checked('before-done-diff',['git','diff','--check'])
 checks=[project,read(f'{REL}/before-done-workflow.json'),read(f'{REL}/before-done-diff.json')]
 done={'role':'coordinator','actor':ACTOR,'task':'IG-2B01','summary':'Technical closure only: verified exact independent PASS/delivery, all criteria and explicit P2/P3 dispositions; unchanged mandatory artifact list. No downstream task started or promoted.','model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':pin(RUN/'configuration.json'),'criteria':accepted['criteria'],'artifacts':accepted['artifacts'],'checks':checks,'independent_review':pin(f'{REV}/review.json'),'accepted_evidence':pin(RUN/'accepted.json'),'finding_dispositions':pin(RUN/'finding-dispositions.json'),'operator_authorization':pin(RUN/'operator-authorization.json'),'semantic_acceptance_granted':False,'source_ig_whole_record_review_granted':False,'next_action':'No IG-2B02 action; await separate operator instruction.'}
 save('done.json',done);transition('done','done.json')
 checked('final-workflow',[sys.executable,'-B','scripts/workflow.py','validate']);checked('final-diff',['git','diff','--check'])
 v=reverify();now=read('docs/work/queue.json');before=read(f'{REL}/queue-before.json')
 assert [t for t in now['tasks'] if t['id']!='IG-2B01']==[t for t in before['tasks'] if t['id']!='IG-2B01']
 task=next(t for t in now['tasks'] if t['id']=='IG-2B01');assert task['status']=='done';assert next(t for t in now['tasks'] if t['id']=='IG-2B02')['status']=='planned'
 start=datetime.fromisoformat(read(f'{REL}/configuration.json')['closure_started_utc']);end=datetime.now(timezone.utc)
 measurement={'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'wall_seconds':(end-start).total_seconds(),'scope':'Coordinator closure verification through done and final checks; preliminary reads before captured start are unmeasured.','model':'gpt-6.1-sol','reasoning':'high','input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None};save('measurement.json',measurement)
 save('preservation-final.json',{'unique_immutable_pins_reverified':v['unique_immutable_pins'],'all_review_delivery_source_product_bytes_unchanged':True,'all_other_38_task_records_unchanged':True,'IG2B02_status':'planned','accepted_event':task['events'][-2],'done_event':task['events'][-1],'no_semantic_acceptance':True,'queue':pin('docs/work/queue.json')})
 report=f'''# IG-2B01 technical closure

IG-2B01 is done through review -> accepted -> done under the current operator's explicit instruction. Coordinator {ACTOR} verified every member of the independent review and original delivery manifests, all exact acceptance criteria and the independent reviewer identity. There were {v['groups']['review_manifest']} reviewer-manifest members, {v['groups']['delivery_manifest']} executor-manifest members and {v['groups']['delivery_artifacts']} mandatory delivery artifacts; {v['unique_immutable_pins']} distinct immutable paths were verified and rechecked after closure.

The independent PASS is attributed to {accepted['actor']}; accepted.json records that existing decision with the exact original delivery artifact list, while coordinator dispositions/verification remain separately pinned. This is not a new self-review. The reviewer configuration and current-session operator-confirmed coordinator configuration remain distinct evidence.

P2 / IG2B01-R01: the real initial overread of neighboring page-5 content is acknowledged as a contained process deviation. It is not undone, retroactively authorized or declared compliant. Final context is the exact two-line Triarii continuation with zero denominator, the 130-region inventory remains intact, and the independent reviewer found no blocking artifact defect. The narrow final evidence was checked without reopening initial broad content. Future continuation access should begin with narrow predetermined bounds and expand only for documented necessity. No artifact repair is required for this technical closure; immutable disclosure remains preserved.

P3 / IG2B01-R02: the raw edition text E5th EdBition, extra E/B at Unicode offsets 0/7 and visible PNG reading 5th Edition are explicitly pinned to the unchanged region/evidence revision in finding-dispositions.json. This advisory remains for future exact transcription. Raw text is preserved, transcription remains partial, and no semantic or represented-coverage promotion occurs.

The unchanged scripts/check.ps1 -Task IG-2B01 ran while accepted and passed; its complete command/exit/UTC/logs are retained. Workflow validation and git diff --check passed before and after done. No product/content/schema change required rerunning the reviewer's 131 independent reproductions. Full final source, tool, delivery and review hash rechecks passed. Any transition CLI failure is separately recorded with actual event verification and projection-only recovery; no transition is repeated automatically.

All other 38 task records are unchanged. IG-2B02 remains planned and was not executed or made ready. No reset/clean/stash/commit/push, external API, new chat/agent/automation, neighboring-repository write or Git-history/archive access occurred. Only the two authorized IG-2B01 queue events, generated projections and new coordinator/check evidence changed.

This closes bounded source inventory only. Partial transcription, explicit geometric/representation gaps, unprocessed semantics and the unchanged 40 other-page placeholders remain. No human semantic acceptance, exact source-IG whole-record review, approved exclusion, compilation or executable readiness is granted.

UTC {measurement['started_utc']} to {measurement['ended_utc']}; elapsed {measurement['wall_seconds']:.3f} seconds for the measured closure. Tokens, cost and operator time are null. Stop here; any IG-2B02 work requires separate operator instruction.
'''
 (RUN/'closure-handoff.md').write_text(report,encoding='utf-8',newline='\n')
 members=[pin(p) for p in sorted(RUN.rglob('*')) if p.is_file() and p.name not in ['manifest.json','final-seal.json']]
 # Also pin the fresh standard check's top-level logs, without synthetic scratch trees.
 stdout=(RUN/'project-check.stdout').read_text(encoding='utf-8')
 logline=next(l for l in stdout.splitlines() if l.startswith('LOG_ROOT='));logs=Path(logline[len('LOG_ROOT='):])
 members += [pin(p) for p in sorted(logs.iterdir()) if p.is_file()]
 save('manifest.json',{'task':'IG-2B01','actor':ACTOR,'artifacts':members,'immutable_basis':pin(RUN/'verification.json'),'self_reference_policy':'Manifest excludes itself and final seal; seal pins manifest and closure targets. Existing frozen evidence is referenced by unchanged pins, never rewritten.'})
 save('final-seal.json',{'task':'IG-2B01','status':'done','actor':ACTOR,'manifest':pin(RUN/'manifest.json'),'handoff':pin(RUN/'closure-handoff.md'),'accepted':pin(RUN/'accepted.json'),'done':pin(RUN/'done.json'),'dispositions':pin(RUN/'finding-dispositions.json'),'independent_review_seal':pin(f'{REV}/review-seal.json'),'original_delivery_seal':pin(f'{BASE}/final-seal.json'),'queue':pin('docs/work/queue.json'),'all_immutable_pins_reverified':True,'all_other_38_tasks_unchanged':True,'IG2B02_status':'planned','semantic_acceptance_granted':False,'measurement':measurement})
 print('CLOSED',pin(RUN/'final-seal.json'),flush=True)
else: raise ValueError(mode)
