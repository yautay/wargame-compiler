"""Finalize and seal this review only; no queue transition or delivery repair."""
from pathlib import Path
import datetime,hashlib,json,re
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
BASE=ROOT/'private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77'
SESSION='01a13b6c-f981-7192-a5ff-1126c809cd63'; ACTOR='codex-'+SESSION
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 p=Path(p); raw=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
if (OUT/'review-seal.json').exists(): raise RuntimeError('Review already frozen')

# Select only current-session tool command metadata and the current-turn usage snapshot.
# No other sessions, reasoning messages, user/account IDs or conversation prose are exported.
session=Path('C:/Users/yauta/.codex/sessions/2026/10/14')/f'rollout-2026-10-14T19-19-20-{SESSION}.jsonl'
tool_calls={}; batches=[]; usage=None
for line in session.open(encoding='utf-8'):
 x=json.loads(line); p=x.get('payload',{})
 if x['type']=='token_usage_record' and p.get('session_id')==SESSION:
  usage={'timestamp':x['timestamp'],'turn_id':p['turn_id'],'turn_token_usage':p['turn_token_usage'],'thread_token_usage':p['thread_token_usage'],'scope':'Observed current metadata cumulative snapshot before sealing; final response/seal overhead is outside this snapshot. Repeated model context counts as input, not unique source tokens.'}
 if x['type']!='response_item': continue
 if p.get('type')=='custom_tool_call' and p.get('name')=='exec':
  if 'tools.exec_command(' in p.get('input','') or 'tools.write_stdin(' in p.get('input',''):
   tool_calls[p['call_id']]={'call_id':p['call_id'],'started_utc':x['timestamp'],'tool_input':p['input'],'outcomes':[]}
 elif p.get('type')=='custom_tool_call_output' and p['call_id'] in tool_calls:
  rec=tool_calls.pop(p['call_id']); rec['ended_utc']=x['timestamp']
  for block in p.get('output',[]):
   if block.get('type')!='input_text': continue
   try: result=json.loads(block['text'])
   except (ValueError,TypeError): continue
   if isinstance(result,dict) and 'value' in result and isinstance(result['value'],dict): result=result['value']
   if not isinstance(result,dict): continue
   entry={k:result[k] for k in ['exit_code','session_id','chunk_id','wall_time_seconds','original_token_count'] if k in result}
   if result.get('exit_code') not in [None,0]: entry['error_excerpt']=result.get('output','')[:5000]
   if entry: rec['outcomes'].append(entry)
  batches.append(rec)
save('tool-command-audit.json',{'scope':'Own current session shell/tool commands through this snapshot; exact inputs and observed exit/timing metadata. Subprocess logs retain full required check outputs. Truncated read outputs are not reconstructed.','batches':batches})
save('token-usage-snapshot.json',usage)

errors=[
 {'id':'RE01','command':'Get-Content docs/work/cards/IG-2B01.md','exit_code':0,'error':'Incorrect card path; PowerShell nonterminating missing-path error within an enclosing read batch.','correction':'Used scripts/search.ps1 and read docs/work/tasks/IG-2B01.md. No file was created.'},
 {'id':'RE02','command':'Inline Python strict pin verification of input/final packet current-file references','exit_code':1,'error':'Asserted live STATUS projection must equal earlier packet snapshot.','correction':'Kept frozen packet pins intact, separately recorded four live projection differences and their exact diffs.'},
 {'id':'RE03','command':'.venv/Scripts/python.exe -B '+(OUT/'independent_review.py').relative_to(ROOT).as_posix()+' reproduce (initial attempt)','exit_code':1,'error':'Existing bundle has no pdftotext.exe at the assumed path; WinError 2 before content extraction.','correction':'No install. Used existing pdfminer for independent whole-page text extraction on pages 1-4, alongside pdfplumber and Poppler rendering.'},
 {'id':'RE04','command':read(OUT/'root-inventory-validate.json')['command'],'exit_code':2,'error':'CLI requires private-relative POSIX path; absolute path rejected before validation.','correction':'Corrected invocation in root-inventory-validate-corrected.json passed with exit 0.'},
 {'id':'RE05','command':'.venv/Scripts/python.exe -B '+(OUT/'assess_and_freeze.py').relative_to(ROOT).as_posix()+' (initial attempt)','exit_code':1,'error':'Deep dependency-reference assertion incorrectly required the historical closure queue pin to equal the live queue.','correction':'Named immutable dependency artifacts verified separately; old queue/context-policy comparisons explicitly recorded and scoped to mutable operational snapshots.'}
]
save('reviewer-errors.json',{'errors':errors,'failed_required_final_checks':0,'retry_policy':'Each error received one changed-hypothesis correction; no product/validator weakening or unchanged retries.'})

configuration=read(OUT/'configuration.json'); configuration['reasoning']='high'; configuration['configuration_evidence']='Own current turn_context at 2026-10-14T17:19:23.369Z; payload model and effort plus collaboration_mode model/reasoning agree.'
save('configuration.json',configuration)
end=utc(); start=configuration['started_utc']; elapsed=(datetime.datetime.fromisoformat(end)-datetime.datetime.fromisoformat(start.replace('Z','+00:00'))).total_seconds()
save('measurement.json',{'actor':ACTOR,'started_utc':start,'ended_utc':end,'wall_seconds':elapsed,'start_basis':'Own session_meta timestamp, not a conservative estimate.','measurement_scope':'Current session creation through final report/evidence preparation; manifest/seal hashing and final user response follow.','model':'gpt-6.1-sol','reasoning':'high','input_tokens':usage['turn_token_usage']['input_tokens'] if usage else None,'output_tokens':usage['turn_token_usage']['output_tokens'] if usage else None,'token_usage_basis':'token-usage-snapshot.json; bounded cumulative snapshot, not final billing','cost':None,'cost_unknown_reason':'No monetary billing measurement exposed; no guessed price calculation.','operator_seconds':None,'operator_time_unknown_reason':'Not reported by operator.'})

criteria=next(t['acceptance'] for t in read(ROOT/'docs/work/queue.json')['tasks'] if t['id']=='IG-2B01')
criterion_results=[{'criterion':criteria[0],'outcome':'PASS','basis':['independent-expectations.json','content-observations.json','character-word-audit.json','secondary-independent.json'],'limit':'No approved editorial exclusion or semantic acceptance.'},{'criterion':criteria[1],'outcome':'PASS','basis':['crop-reproduction.json','secondary-independent.json','content-observations.json'],'limit':'Literal extraction remains partial; explicit R02 advisory is not normalized into source bytes.'},{'criterion':criteria[2],'outcome':'PASS','basis':['configuration.json','content-observations.json','review-report.md'],'limit':'Distinct current session inspected originals and complete final ledger; not executor self-review.'}]
save('criteria.json',criterion_results)
findings=[{'id':'IG2B01-R01','severity':'P2','category':'process_scope','blocking':False,'status':'contained_disclosed_coordinator_disposition_required','title':'Initial page-5 probe exposed adjacent content','locator':{'reports':[pin(BASE/'context-access-authorization.json'),pin(BASE/'context-overread.json')],'physical_page':5,'initial_top_left_points':[44,50,303,105],'final_region_id':'region:e8d77349-41ce-47d0-b678-eab1d0c8e8ed','final_box':[71895,63131,495099,98485]},'reproduction':'Compare already-pinned disclosure/access metadata and final narrow evidence; do not open initial probe or adjacent source content.','impact':'Real bounded access deviation. No demonstrated damage to final inventory or denominator; final narrowing cannot undo prior exposure.','minimum_correction':'Coordinator records explicit disposition before technical acceptance; preserve immutable disclosure, use narrowly predetermined continuation probes in future. No artifact repair requested.','verification':'Recheck narrow final context and zero denominator. No neighboring-entry access.','basis_limit':'Disclosure/metadata evidence only; prohibited neighboring content was not independently inspected.'},{'id':'IG2B01-R02','severity':'P3','category':'transcription_advisory','blocking':False,'status':'future_transcription_refinement','title':'Edition raw text contains font-overlap E/B','locator':{'physical_page':1,'region_id':'region:74a8c133-e1a5-4ec4-8ebc-517987e6b24f','key':'ig2b01:cover:edition','box':[441176,715909,562091,741161],'extra_codepoint_offsets':[0,7]},'reproduction':'Exact literal extraction E5th EdBition reproduces; PNG visibly reads 5th Edition.','impact':'Potential downstream confusion if partial machine evidence is treated as transcription; current coverage/generic uncertainty prevent that claim.','minimum_correction':'Future transcription work should explicitly record this anomaly/offsets and PNG comparison. Preserve raw text and source bytes.','verification':'Compare codepoints and PNG at the exact unchanged region revision.'}]
save('findings.json',{'outcome':'PASS','blocking_product_findings':0,'observations':findings,'severity_counts':{'P0':0,'P1':0,'P2':1,'P3':1}})
checks=[]
for name in ['check','workflow-validate','diff-check','root-inventory-validate-corrected']:
 c=read(OUT/(name+'.json')); assert c['exit_code']==0; checks.append(c)
for mode in ['reproduce','secondary']:
 checks.append({'command':[str(ROOT/'.venv/Scripts/python.exe'),'-B',str(OUT/'independent_review.py'),mode],'exit_code':0,'log_basis':'Own tool-command-audit.json and '+('crop-reproduction.json' if mode=='reproduce' else 'secondary-independent.json'),'expectation':'Source pixels/text/bounds and offsets reproduce at all 131 regions; source-observed completeness separately assessed.' if mode=='reproduce' else 'Exact canonical revisions, registry replay, all rational bounds, geometry partitions and final uncertainty/gap bindings.'})
delivery=read(BASE/'delivery.json'); original_pins=[pin(BASE/n) for n in ['final-seal.json','delivery.json','delivery-manifest.json','delivery-handoff.md','final-verified/inventory.json','region-ledger-final.json','final-verified/identity-registry.json']]
assert next(t['status'] for t in read(ROOT/'docs/work/queue.json')['tasks'] if t['id']=='IG-2B01')=='review'
review={'format':'wgc-independent-review-1','task':'IG-2B01','role':'reviewer','actor':ACTOR,'executor':delivery['actor'],'outcome':'PASS','summary':'Independent full four-page final-ledger/source comparison and 131-region reproduction passed; no blocking artifact defect. Contained page-5 scope deviation needs explicit coordinator disposition; transcription advisory retained.','model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':pin(OUT/'configuration.json'),'criteria':criteria,'criterion_results':criterion_results,'checks':checks,'artifacts':delivery['artifacts'],'original_delivery_pins':original_pins,'findings':findings,'blocking_findings':0,'semantic_decision':None,'semantic_acceptance_granted':False,'source_ig_whole_record_review_granted':False,'human_authority':'unverified','executable_readiness':'unassessed','measurement':read(OUT/'measurement.json'),'next_action':'Coordinator verifies review seal/exact original delivery pins and records R01 disposition before preparing technical acceptance of IG-2B01. Reviewer leaves queue at review; no repairs or IG-2B02.'}
save('review.json',review)
check_stdout=(OUT/'check.stdout').read_text(encoding='utf-8'); check_root=Path(re.search(r'LOG_ROOT=([^\r\n]+)',check_stdout).group(1))
check_pins=[pin(check_root/n) for n in ['result.json','plan.log','dry-run.log','pytest.log','diff-check.log']]
handoff={'task':'IG-2B01','role':'reviewer','actor':ACTOR,'outcome':'PASS','review':pin(OUT/'review.json'),'report':pin(OUT/'review-report.md'),'original_delivery_pins':original_pins,'configuration':pin(OUT/'configuration.json'),'criteria':criterion_results,'checks':checks,'check_scratch_logs':check_pins,'finding_disposition':'Zero blocking artifact findings. R01 bounded process deviation needs explicit coordinator acknowledgement/disposition; R02 is future transcription refinement. Neither licenses silent repair or semantic promotion.','queue_status':'review','queue_transition_performed':False,'semantic_acceptance_granted':False,'next_action':review['next_action']}
save('coordinator-handoff.json',handoff)
save('closure-evidence-disposition.json',{'old_queue_pin':'IG-2A closure queue pin describes an earlier accepted/done snapshot; current queue legitimately contains subsequent IG-2B01 lifecycle. Named immutable accepted/done bytes and current event references match.','old_context_policy_pin':pin(BASE/'context-policy-before.json'),'current_context_policy':pin(ROOT/'docs/work/context-policy.json'),'policy_delta':'Six additive exact paths (three IG-2B01 preflight records and three accepted baseline/registry artifacts); all old entries/settings retained.','no_history_expansion':True})

# Verify preservation again immediately before hashing this new output tree.
original_manifest=read(BASE/'delivery-manifest.json')
for p in original_manifest['artifacts']: assert pin(ROOT/p['path'])==p
for p in original_pins: assert pin(ROOT/p['path'])==p
assert pin(ROOT/'docs/work/queue.json')==read(OUT/'preservation-independent.json')['queue_pin_at_review_snapshot']
manifest={'format':'wgc-review-manifest-1','task':'IG-2B01','actor':ACTOR,'artifacts':[pin(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in ['review-manifest.json','review-seal.json']],'external_check_logs':check_pins,'original_delivery_pins':original_pins,'self_reference_policy':'Manifest excludes itself and the final seal; final seal pins this manifest, review and handoff. No bytes are changed after sealing.'}
save('review-manifest.json',manifest)
save('review-seal.json',{'format':'wgc-review-seal-1','task':'IG-2B01','actor':ACTOR,'outcome':'PASS','model':'gpt-6.1-sol','reasoning':'high','review':pin(OUT/'review.json'),'manifest':pin(OUT/'review-manifest.json'),'handoff':pin(OUT/'coordinator-handoff.json'),'report':pin(OUT/'review-report.md'),'original_delivery_pins':original_pins,'sealed_utc':utc(),'semantic_acceptance_granted':False,'queue_status':'review','next_action':review['next_action']})
seal=read(OUT/'review-seal.json')
for p in manifest['artifacts']+manifest['external_check_logs']+seal['original_delivery_pins']+[seal['review'],seal['manifest'],seal['handoff'],seal['report']]: assert pin(ROOT/p['path'])==p
print(json.dumps({'outcome':'PASS','own_artifacts':len(manifest['artifacts']),'review_seal':pin(OUT/'review-seal.json'),'review':seal['review'],'manifest':seal['manifest'],'handoff':seal['handoff'],'measurement':read(OUT/'measurement.json')},indent=2))
