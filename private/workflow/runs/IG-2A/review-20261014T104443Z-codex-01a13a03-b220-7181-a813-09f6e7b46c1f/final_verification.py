from support import *
from wgc.sources.inventory import validate
from collections import Counter
import copy
# Recover independently printed boundary data from the captured stdout; command
# wrapper correctly owns the command-name JSON. No probe output is reinterpreted.
rows=json.loads((RUN/'integer-pixel-boundaries.stdout').read_text())
write('independent-integer-pixel-boundaries.json',{'basis':'CropBox native width 200, height 300; normalized span 0.3 by 0.7; UserUnit 1.1; exact physical dimensions 66 by 231 points. Eight actual boundary renders.','results':rows,'recovery':'Original boundary data JSON used the command-record filename and was replaced by its wrapper record. Exact results recovered from intact captured stdout; producer output name corrected. No probe rerun or expectation changes.'})
assert all(r['validator_error'] is None and r['actual_pixels']==r['exact_mathematical_pixels'] for r in rows)
records=read(RUN/'input-verification.json')['records']
final=[]
for old in records:
    path=ROOT/old['path'];current=pin(path)
    final.append({'path':old['path'],'expected_sha256':old['sha256'],'actual_sha256':current['sha256'],'matches':current['sha256']==old['sha256']})
for entry in read(REPAIR/'frozen-tools.json'):
    final.append({'path':entry['path'],'expected_sha256':entry['sha256'],'actual_sha256':digest(ROOT/entry['path']),'matches':digest(ROOT/entry['path'])==entry['sha256']})
preserved=read(REPAIR/'preservation-final.json')['original_delivery_json_copy']
for path in [ROOT/preserved['path'],ROOT/'private/workflow/runs/IG-2A/attempt-20261013T155212Z/delivery.json']:
    final.append({'path':path.relative_to(ROOT).as_posix(),'expected_sha256':preserved['sha256'],'actual_sha256':digest(path),'matches':digest(path)==preserved['sha256']})
assert all(r['matches'] for r in final)
queue=read(ROOT/'docs/work/queue.json');before=read(REPAIR/'queue-before.json')
unchanged=[t['id'] for t in before['tasks'] if t['id']!='IG-2A' and t==next(n for n in queue['tasks'] if n['id']==t['id'])]
assert len(unchanged)==38
initial=(RUN/'initial-git-status.stdout').read_bytes()
status=command('final-git-status',['git','status','--porcelain=v1'])
current=(RUN/'final-git-status.stdout').read_bytes()
assert initial==current,'Unexpected worktree status change'
for name,entry in read(RUN/'toolchain.json')['executables'].items():
    assert digest(entry['path'])==entry['sha256'], 'Runtime binary changed during review'
write('preservation-final.json',{'records':final,'verified_pin_counts_by_group':dict(Counter(r['group'] for r in records)),'queue_unchanged_from_review_packet':True,'queue_sha256':digest(ROOT/'docs/work/queue.json'),'queue_status':'review','other_38_task_records_unchanged_since_repair':True,'current_vs_initial_git_status_identical':True,'writes':'Only new review directory; all operational scratch retained here.','workflow_and_IG1A_contract_unchanged':True,'runtime_executable_hashes_unchanged_during_review':True,'source_pdf_unchanged':True,'git_history_access':False,'new_agents_or_chats':False,'external_APIs':False,'semantic_acceptance_granted':False})
verified=read(REPAIR/'verified-inventory.json');report=validate(verified,ROOT)
labels=[{'pdf_page':p['pdf_page'],**p['label']} for p in verified['pages']]
assert labels[0]['status']=='unknown'
assert all(p['status']=='unknown' for p in labels[4:])
assert [(p['pdf_page'],p['value']) for p in labels if p['status']=='verified']==[(2,'2'),(3,'3'),(4,'4')]
write('delivery-inventory-validation.json',{'candidate':pin(REPAIR/'verified-inventory.json'),'report':report,'labels':labels,'reviewer_visual_observations_match_verified_labels_2_3_4':True})
checks=[command('final-workflow-validate',[PYTHON,'scripts/workflow.py','validate']),command('final-git-diff-check',['git','diff','--check'])]
write('final-checks.json',checks);assert all(c['exit_code']==0 for c in checks)
print('All preservation, delivery labels, binaries and final workflow/diff checks passed')
