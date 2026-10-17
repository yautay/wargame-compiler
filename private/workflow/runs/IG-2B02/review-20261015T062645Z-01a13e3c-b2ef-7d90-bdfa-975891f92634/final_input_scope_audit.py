from review_driver import *
cat=load(P/'frozen-pins.json');verified=[]
for expected in cat['all_unique_frozen_refs_and_launch_controls']:
    path=Path(expected['path']);path=path if path.is_absolute() else ROOT/path
    actual=pin(path)
    assert actual['bytes']==expected['bytes'] and actual['sha256']==expected['sha256'],expected['path']
    verified.append(expected)
envelope=load(D/'delivery-transition-envelope.json');manifest=load(D/'delivery-manifest.json');seal=load(D/'final-seal.json')
groups=[envelope['artifacts'],manifest['new_reviewed_artifacts'],manifest['immutable_inputs_and_old_evidence'],seal['postfreeze_recovery_and_epilogue_artifacts']]
union={}
for group in groups:
    for p in group:
        path=Path(p['path']);path=path if path.is_absolute() else ROOT/path
        assert pin(path)['sha256']==p['sha256'] and path.stat().st_size==p['bytes']
        if p['path'] in union:assert p==union[p['path']]
        union[p['path']]=p
assert [len(g) for g in groups]==[2895,1462,1428,40] and len(union)==2930
q=load(ROOT/'docs/work/queue.json');task=next(t for t in q['tasks'] if t['id']=='IG-2B02')
assert task['status']=='review' and task['events'][-1]==seal['review_event']
assert [t['id'] for t in q['tasks'] if t['status'] in ('in_progress','review','changes_requested','accepted')]==['IG-2B02']
assert all(next(t for t in q['tasks'] if t['id']==dep)['status']=='done' for dep in ('IG-2A','IG-2B01'))
preserved=[];projection=[]
for p in load(D/'existing-changes.json')['tracked_modified_files']:
    path=p['path'];is_projection=path in ('docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md','docs/work/queue.json') or path.startswith('docs/work/tasks/')
    if is_projection:projection.append({'original_executor_observation':p,'current':pin(ROOT/path),'policy':'Current exact review-state bytes independently pinned by fresh packet/catalogue; historical ready-state observations intentionally differ.'})
    else:
        assert pin(ROOT/path)==p,path
        preserved.append(p)
rec=run('17-final-working-tree-status',['git','status','--porcelain=v1','--untracked-files=normal'])
baseline=(R/'commands/04-working-tree-baseline.stdout').read_bytes();current=(ROOT/rec['stdout']['path']).read_bytes()
assert baseline==current,'Unexpected working-tree status change; coordinator triage required.'
known={p['path'] for p in manifest['new_reviewed_artifacts']+seal['postfreeze_recovery_and_epilogue_artifacts']}|{(D/'final-seal.json').relative_to(ROOT).as_posix()}
actual_files={p.relative_to(ROOT).as_posix() for p in D.rglob('*') if p.is_file()}
unexpected=sorted(actual_files-known)
assert not unexpected,unexpected
owned_files=[pin(p) for p in R.rglob('*') if p.is_file()]
write('final-input-scope-audit.json',{'outcome':'passed','observed_utc':utc(),'catalogue':pin(P/'frozen-pins.json'),'catalogue_refs_verified':len(verified),'all_2930_delivery_union_refs_verified_again':True,'group_lengths':[len(g) for g in groups],'queue':pin(ROOT/'docs/work/queue.json'),'review_event':task['events'][-1],'active_task':'IG-2B02','dependencies_done':['IG-2A','IG-2B01'],'unrelated_existing_modified_files_exact_against_executor_preclaim_pins':preserved,'historical_mutable_projection_observations':projection,'working_tree_status_baseline':pin(R/'commands/04-working-tree-baseline.stdout'),'working_tree_status_current':rec,'status_bytes_identical':True,'unexpected_executor_paths':unexpected,'frozen_executor_file_namespace_verified':len(actual_files),'reviewer_mutation_scope':'All reviewer-authored files and replays confined to this single new review directory. Required pytest/check outputs confined to their freshly generated private/workflow/checks directories. No queue/projection/executor/input/source/tool/test/contract repair writes; no commit/push/global settings/sessions/agents/automations/external APIs.','reviewer_files_before_final_reports':owned_files,'scope_verification_limit':'Git history was not read. Baseline working-tree status plus exact named frozen/unrelated modification pins were compared; no claim of an independently captured byte snapshot of every unrelated untracked file.'})
print('FINAL INPUT/SCOPE GATE PASSED',len(union),'frozen refs;',len(actual_files),'executor files unchanged namespace')
