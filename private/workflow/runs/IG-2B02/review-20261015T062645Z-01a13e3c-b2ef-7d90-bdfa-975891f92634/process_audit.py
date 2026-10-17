from review_driver import *
import ast,re
manifest=load(D/'delivery-manifest.json');seal=load(D/'final-seal.json');envelope=load(D/'delivery-transition-envelope.json');original=load(D/'delivery.json')
refs={p['path']:p for p in manifest['new_reviewed_artifacts']+seal['postfreeze_recovery_and_epilogue_artifacts']}
scripts=[];commands=[];failures=[]
for name,p in sorted(refs.items()):
    path=ROOT/name
    if name.endswith('.py'):
        code=path.read_text(encoding='utf-8-sig');ast.parse(code)
        scripts.append({'pin':p,'syntax':'valid','executed_by_reviewer':path.name=='author.py','inspection':'Read in full as submitted generation/audit/recovery code; fixed-path executor scripts were not run. Author replay destinations were absolute fresh reviewer subdirectories.'})
    if name.endswith('.command.json'):
        command=load(path);commands.append({'pin':p,'command':command['command'],'exit_code':command['exit_code'],'stdout':command['stdout'],'stderr':command['stderr']})
        if command['exit_code']:
            failures.append({'pin':p,'command':command['command'],'exit_code':command['exit_code'],'stderr':(ROOT/command['stderr']['path']).read_text(encoding='utf-8-sig')})
bad=load(D/'review-transition-diagnosis.json')['invalid_artifacts'];bad_paths={p['pin']['path'] for p in bad}
kept=[p for p in original['artifacts'] if p['path'] not in bad_paths]
assert len(bad)==5 and envelope['artifacts'][:len(kept)]==kept and len(envelope['artifacts'])==2895
assert envelope['artifacts'][len(kept):]==[pin(D/f) for f in ('delivery.json','review-transition.command.json','review-transition.stdout','review-transition.stderr','review-transition-diagnosis.json','transition-recovery-proposal.json','transition-recovery-handoff.md','checkpoint-review-transition-failed.json','prepare-transition-recovery.py')]
authorization=load(D/'operator-retry-authorization.json');assert authorization['approved_envelope']==pin(D/'delivery-transition-envelope.json') and authorization['authorized_retry_count']==1
queue=load(ROOT/'docs/work/queue.json');task=next(t for t in queue['tasks'] if t['id']=='IG-2B02');event=task['events'][-1]
assert event==seal['review_event'] and event['evidence'].endswith('/delivery-transition-envelope.json') and event['sha256']==digest(D/'delivery-transition-envelope.json')
assert task['status']=='review' and len(task['events'])==3
assert load(D/'review-transition.command.json')['exit_code']==1 and load(D/'review-transition-authorized.command.json')['exit_code']==0
mutable=manifest['mutable_input_snapshot_observations']
assert all('policy' in p and 'original_observed_pin' in p for p in mutable)
for observation in mutable:
    path=observation['original_observed_pin']['path']
    assert path in ('docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md','docs/work/queue.json') or path.startswith('docs/work/tasks/')
check=load(R/'commands/12-repository-check.json');text=(ROOT/check['stdout']['path']).read_text(encoding='utf-8-sig')
match=re.search(r'^LOG_ROOT=(.+)$',text,re.M);assert match
check_root=Path(match[1].strip()).resolve();assert check_root.is_relative_to(ROOT/'private/workflow/checks')
result=load(check_root/'result.json');assert all(result[k]==0 for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
assert '102 passed' in text
check_logs=[pin(p) for p in sorted(check_root.iterdir()) if p.is_file()]
write('required-check-results.json',{'source_tests':load(R/'commands/11-source-tests.json'),'source_count':71,'repository_check':check,'full_suite_count':102,'check_root':check_root.relative_to(ROOT).as_posix(),'result':result,'outputs':check_logs,'workflow_validate':load(R/'commands/13-final-workflow-validate.json'),'git_diff_check':load(R/'commands/14-final-diff-check.json'),'warnings':'pypdf original Xref warnings and Git CRLF-to-LF warnings retained in exact command stderr/stdout; no suppression or source normalization.'})
write('process-review.json',{'outcome':'reviewed','reviewed_utc':utc(),'scripts':scripts,'executor_command_records':commands,'executor_nonzero_commands':failures,'executor_additional_error_records':[{'pin':pin(D/f),'record':load(D/f)} for f in ('preflight-initial-error.json','preflight-environment-error.json','process-defects.json')],'recovery_chain':{'original_delivery':pin(D/'delivery.json'),'corrected_envelope':pin(D/'delivery-transition-envelope.json'),'event':event,'manifest':pin(D/'delivery-manifest.json'),'final_seal':pin(D/'final-seal.json'),'authorization':pin(D/'operator-retry-authorization.json'),'exact_removal_only':list(bad_paths),'all_admissible_originals_retained_in_order':True,'appended_recovery_entries':envelope['artifacts'][len(kept):],'successful_retry_count':1,'authority_limit':'Pinned operator authorization observation and actual queue event corroborate operational retry; no semantic approval inferred. Other conversations were not inspected.'},'mutable_snapshot_policy':mutable,'historical_claims':'Old pending-status reports and draft inventories are preserved process history. Current product targets are authored/final-verified outputs, final ledger with later component observations, and event-selected envelope.','boundary_overlap_recovery':'Initial author run failed unchanged disjointness validator; final normalized rectangles independently disjoint with exact complement. Source inspection confirms moved boundaries remain in whitespace.','triarii_correction':'Final link supported by exact accepted page-4 crop; original erroneous reason preserved only in superseded process artifacts.','component_correction_review':'Six later correction groups source-checked; two remaining grouped-component defects found in three other regions, recorded as R01/R02. Executor all-viewed booleans do not establish completeness.','reviewer_process_observations':[{'operation':'Initial own metadata OpenText','exit_code':1,'error':'Active journal sharing violation; cleanup also encountered null reader.','retry_hypothesis':'Shared FileStream ReadWrite access; read only own session_meta/turn_context fields.','retry_exit_code':0},{'operation':'Direct visual_prepare.py invocation','exit_code':1,'error':'ModuleNotFoundError: PIL because new shell omitted bundled PYTHONPATH.','retry_hypothesis':'Run through owned driver with explicit authorized process environment.','retry_exit_code':0,'evidence':pin(R/'commands/09-visual-preparation.json')}],'uncaptured_setup_measurements':{'started_utc':None,'ended_utc':None,'stdout_stderr_files':None,'reason':'These setup/read-only invocations preceded the persistent command logger; actual error/exits were observed in tool responses. No timestamps/raw logs fabricated. Required validation/replay command logs are fully retained.'},'no_executor_tool_test_contract_changes':True,'no_real_queue_mutation_by_reviewer':True})
checkpoint('process_and_checks_reviewed',['All 141 visual regions and two findings','38 source-supported added links; exact retained context','Both persisted-registry replays identical','71 source / 102 full-suite tests passed; required checks exit zero','Generation/recovery code and original failure chain reviewed'], 'Complete ongoing full locator replay, final hashes/scope check, criteria matrix and frozen handoff.')
print('PROCESS REVIEW',len(scripts),'scripts',len(commands),'recorded commands;',len(failures),'historical nonzero commands; 71/102 tests passed')
