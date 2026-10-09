"""Immutable completion record after the actual final checks."""
from prepare import ROOT, P, M, I, now, load, record, write, verify
from datetime import datetime
import os
import subprocess

baseline = load(M / 'baseline.json')
verify(baseline['files'])
seal = load(M / 'package-seal.json')
verify(seal['files'], P)
verify(seal['files'], ROOT / seal['export_root'])
owner_review = load(M / 'owner-visual-review.json')
assert owner_review['readability_and_boundaries_confirmed']
verify([owner_review['review_html'], owner_review['reviewed_package_manifest']])
assert record(ROOT / '.git/index') in baseline['files']

check_paths = [
    ROOT / 'private/poc/_checks/active-77111fd3b8a34627b33c498a19d88c4a',
    ROOT / 'private/poc/_checks/active-7c7433d8e9d749058db04d904c468cf0',
]
checks = []
for path in check_paths:
    result = load(path / 'result.json')
    assert result['tests_exit'] == result['diff_exit'] == 0
    log = (path / 'pytest.log').read_text(encoding='utf-8-sig')
    checks.append({'result':result,'log_root':path.relative_to(ROOT).as_posix(),
                   'pytest_summary':log.strip().splitlines()[-1],
                   'hashes':[record(path / name) for name in ('pytest.log','result.json')],
                   'local_tmp_temp':True,'new_basetemp':True})
assert '102 passed' in checks[-1]['pytest_summary']
git_env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
diff = subprocess.run(['git','diff','--check'],cwd=ROOT,env=git_env,capture_output=True,text=True)
assert diff.returncode == 0, diff.stderr
status = subprocess.check_output(['git','status','--short','--branch'],cwd=ROOT,env=git_env,text=True)
write(M / 'git-status-final.txt', status)
write(M / 'git-diff-check-final.json', {'exit_code':diff.returncode,'stdout':diff.stdout,'stderr':diff.stderr})
finished = now()
elapsed = (datetime.fromisoformat(finished) - datetime.fromisoformat(baseline['recorded_at_utc'])).total_seconds()
output_paths = [ROOT / 'docs' / name for name in ('STATUS.md','HANDOFF.md','ROADMAP.md','work/tasks/M-POC2B.md','handoff/2026-10-09-M-POC2A.md')]
output_paths += [ROOT / 'tests/test_poc_continuity.py']
output_paths += sorted(path for path in M.rglob('*') if path.is_file() and path.name not in {'completion.json'} and '__pycache__' not in path.parts)
completion = {
    'id':'M-POC2A-20261009-001','card':'M-POC2A','milestone':'M-POC2','outcome':'done',
    'completed_at_utc':finished,'first_recorded_clock_utc':'2026-10-09T16:41:55Z',
    'baseline_recorded_at_utc':baseline['recorded_at_utc'],'calendar_seconds_since_baseline':elapsed,
    'clock_limitations':'Initial bootstrap and environment discovery precede the first clock. Calendar duration includes owner review and waits; active time is unknown.',
    'timezone':'Europe/Warsaw','application':'Codex desktop','actual_model_visible_name':'unknown',
    'reasoning_level':'unknown','model_metadata_source':'UI selector not inspected; repository proposal is not actual session configuration',
    'user_active_time':'unknown','model_active_time':'unknown','tokens':'unknown','price':'unknown',
    'cumulative_available_budget':'unknown; no retroactive assertion of unused 8-hour budget',
    'source_sha256':load(I / 'scope.json')['source_sha256'],
    'manifest':record(I / 'manifest.json'),'package_seal':record(M / 'package-seal.json'),
    'package_file_count':seal['file_count'],'package_bytes':seal['total_bytes'],
    'core_regions':12,'context_regions':4,'full_renders':7,'dpi':200,'additional_pages':0,
    'visual_review':{'codex_full_pages':[31,32,33,34,35,36,37],'codex_selected_crops':['pdf-31-core-right','pdf-37-core-left','pdf-32-core-left','pdf-32-core-right','pdf-35-core-left'],'owner_confirmation':record(M / 'owner-visual-review.json'),'semantic_acceptance':False},
    'artifact_audit':record(M / 'artifact-audit.json'),'source_validation':record(M / 'source-validation.json'),
    'protected_files_unchanged':len(baseline['files']),'git_index_unchanged':True,
    'checks':checks,'final_diff_check':record(M / 'git-diff-check-final.json'),
    'output_and_evidence_hashes':[record(path) for path in output_paths],
    'environment_issues_preserved':['Bundled venv ensurepip failed; bundled pip --python installed into local .venv.','PyPI DNS failed in sandbox; authorized escalated retry installed pytest 9.1.1 into local .venv.'],
    'transfer_state':'prepared_not_sent','files_sent_to_other_chats':[],
    'inference_api':False,'gui_automation':False,'semantic_extraction_run':False,
    'new_chats_created':False,'legacy_runtime_used':False,'commit_or_push':False,
    'quality_results':'n/a: first extraction not performed','next_card':'M-POC2B',
    'next_action':'Owner opens a clean manual session in private/poc/spqr-chapter9/transfer/first-v1, provides only the transfer-list files and executes prompts/first-v1.txt; preserve raw response and actual session metadata separately.',
    'limitations':['Helper text is automatic and may omit/misorder graphics and glyphs; full renders are authoritative.','No context beyond PDF 31-37 added.','Prepared session has review history and is not the blind extractor.','Files are local and ignored by Git; no new remote publication performed.'],
}
write(M / 'completion.json', completion)
write(M / 'sessions-M-POC2A-001.jsonl', __import__('json').dumps({'id':completion['id'],'card':'M-POC2A','outcome':'done','completed_at_utc':finished,'completion':record(M / 'completion.json'),'next_card':'M-POC2B','sent_to_extractor':False},ensure_ascii=False)+'\n')
print('Completed M-POC2A: 102 passed; 722 protected files and package hashes unchanged; owner review recorded')
