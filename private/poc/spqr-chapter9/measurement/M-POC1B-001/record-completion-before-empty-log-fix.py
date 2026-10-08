"""Final delivery/provenance record for this manual drafting session."""
from pathlib import Path
import json,hashlib,subprocess
from datetime import datetime,timezone

R=Path('C:/dev/wargame-compiler')
P=R/'private/poc/spqr-chapter9'
S=P/'measurement/M-POC1B-001'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def entry(p): return {'path':str(p.relative_to(R)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)}
def write_new(p,v):
    assert not p.exists()
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

baseline=read(S/'baseline.json')
for row in baseline['protected_files']:
    p=Path(row['path'])
    assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
for row in read(P/'source/review-evidence/historical-baseline.json'):
    p=R/row['path']
    assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
assert sha(Path(read(P/'source/source-v1.json')['source']['path']))==read(P/'source/source-v1.json')['source']['sha256']
outputs=[P/'evaluation/draft'/n for n in ('expectations.json','dependencies.json','situations.json','review-questions.md')]
public=[R/n for n in ('docs/STATUS.md','docs/ROADMAP.md','docs/HANDOFF.md','docs/handoff/2026-10-07-M-POC1B.md')]
checks=[]
for token in ('286e90f6bdb7428eb870cfb43557b7b6','268cb3105d27423fb47d195e11fc148d'):
    folder=R/'private/poc/_checks'/('active-'+token)
    result=read(folder/'result.json')
    assert result['tests_exit']==0 and result['diff_exit']==0
    assert '62 passed' in (folder/'pytest.log').read_text(encoding='utf-8-sig')
    checks.append({'log_root':str(folder.relative_to(R)).replace('\\','/'),
      'result':result,'pytest':'62 passed','local_TMP_TEMP':str(folder/'temp'),
      'new_basetemp_created_by_check_script':True,
      'log_hashes':[entry(folder/name) for name in ('pytest.log','diff-check.log','result.json')]})
env=__import__('os').environ.copy()
env['GIT_OPTIONAL_LOCKS']='0'
git=['git','-c','safe.directory=C:/dev/wargame-compiler']
diff=subprocess.run(git+['diff','--check'],cwd=R,env=env,capture_output=True,text=True)
assert diff.returncode==0,diff.stderr
status=subprocess.run(git+['status','--short'],cwd=R,env=env,capture_output=True,text=True)
assert status.returncode==0,status.stderr
(S/'git-status-final.txt').write_text(status.stdout+'\nSTDERR:\n'+status.stderr,encoding='utf-8')
name_status=subprocess.run(git+['diff','--name-status'],cwd=R,env=env,capture_output=True,text=True)
assert name_status.returncode==0
(S/'git-diff-name-status-final.txt').write_text(name_status.stdout+'\nSTDERR:\n'+name_status.stderr,encoding='utf-8')
now=datetime.now(timezone.utc)
first=datetime(2026,10,7,11,59,50,tzinfo=timezone.utc)
e=read(outputs[0]);d=read(outputs[1]);s=read(outputs[2])
record={
 'id':'M-POC1B-20261007-draft-001','date':'2026-10-07','timezone':'Europe/Warsaw',
 'card':'M-POC1B','outcome':'partial','technical_preparation':'complete','workflow_status':'waiting_review',
 'milestone':'M-POC1','milestone_status':'next','next_card':'M-POC1B',
 'next_action':'Start owner review at evaluation/draft/review-questions.md RQ-01 with its complete source and SIT-07; record actual scoped decisions separately. Do not freeze or run M-POC1C/M-POC2B.',
 'app':'Codex desktop','actual_model_visible_name':'unknown','reasoning_level':'unknown',
 'model_metadata_source':'System describes Codex based on GPT-6; selector not inspected; proposed extraction configuration not attributed.',
 'user_active_time':'unknown','model_active_time':'unknown','tokens':'unknown','price':'unknown',
 'first_recorded_clock_utc':first.isoformat(),'completed_at_utc':now.isoformat(),
 'recorded_calendar_elapsed_seconds':(now-first).total_seconds(),
 'budget_limitation':'First clock follows bootstrap and initial source reads; exact full session start and active work not measured. Recorded interval is not entire active time. No long owner wait or additional card performed.',
 'assessment_version':'draft_unfrozen','frozen':False,'semantic_extraction_run':False,'blind_session':False,
 'human_review':{'status':'waiting_review','reviewer':None,'date':None,'approved_expectations':0,'approved_dependencies':0,'approved_situations':0},
 'historical_owner_review':'Ten scoped M-POC1A decisions retained; no semantic approval transferred.',
 'source':{'path':read(P/'source/source-v1.json')['source']['path'],
           'sha256':e['source_sha256'],'pages_read':'PDF31–37 full renders plus direct scoped PDF crops; boundary context separate',
           'added_external_pages':0,'map_or_scenario_added':False},
 'private_inputs':[entry(Path(row['path'])) for row in baseline['protected_files'] if '/.git/' not in row['path'].replace('\\','/')],
 'public_bootstrap_inputs':['CLAUDE.md','docs/SESSION-PLAYBOOK.md','docs/STATUS.md','docs/HANDOFF.md',
   'docs/handoff/2026-10-07-M-POC1A-review.md','docs/ROADMAP.md','docs/POC-PLAN.md',
   'docs/adr/ADR-0039-archiwum-i-poc-przed-architektura.md','docs/work/tasks/README.md','docs/work/tasks/M-POC1B.md'],
 'public_input_hash_limitation':'Pre-edit public bootstrap hashes not captured; current hashes below identify delivery only.',
 'output_method':'Manually authored propositions/candidate dispositions/situations; private session formatter attaches unchanged inventory evidence and checks IDs/hashes. No model-generated extraction response claimed.',
 'outputs':[entry(p) for p in outputs],'public_handoff_files':[entry(p) for p in public],
 'supporting_audit':[entry(S/n) for n in ('baseline.json','assembly-summary.json','refinement-map.json','artifact-audit.json','direct-pdf-read.json')],
 'counts':{'expectations':e['counts'],'dependencies':d['counts'],'relations':d['denominators'],
           'situations':s['counts'],'expected_kinds':s['expected_kind_counts'],'review_questions':15},
 'checks':checks,'final_direct_git_diff_check':{'exit_code':diff.returncode,'stdout':diff.stdout,'stderr':diff.stderr},
 'protected_preexisting_files_unchanged':len(baseline['protected_files']),
 'historical_files_hashes_unchanged':9298,'Git_index_unchanged':True,
 'limitations':['Local outcome tests do not resolve complete combat/routes',
  'No verified atomic/full graph denominator','External/scenario/map targets and aliases unresolved',
  'Graphic glyph transcription not exhaustive','Source-supported proposals are not owner-confirmed',
  'Actual model/reasoning/active time/token/price unknown','Global Git ignore file inaccessible warning retained'],
 'no_inference_API':True,'no_GUI_automation':True,'no_other_chats_or_messages':True,
 'no_other_repository_changes':True,'no_legacy_code_or_schema_import':True,
 'no_reset_clean_stash_commit_push_global_git_config':True,
 'later_cards_executed':False,'M_DESK2':'historical partial outside active queue'
}
write_new(S/'completion.json',record)
with (P/'measurement/sessions.jsonl').open('a',encoding='utf-8') as f:
    f.write(json.dumps(record,ensure_ascii=False)+'\n')
print(json.dumps({'status':record['outcome'],'technical_preparation':record['technical_preparation'],
 'checks':record['checks'][-1]['pytest'],'diff_check_exit':diff.returncode,
 'recorded_calendar_minutes':record['recorded_calendar_elapsed_seconds']/60,
 'outputs':record['outputs'],'protected_files':record['protected_preexisting_files_unchanged'],
 'historical_files':9298,'next_card':'M-POC1B'},ensure_ascii=False))
