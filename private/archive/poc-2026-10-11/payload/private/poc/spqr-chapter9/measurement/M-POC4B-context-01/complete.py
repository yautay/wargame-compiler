"""Final report/span/byte integrity, real checks and append-only measurement."""
from pathlib import Path
import json,hashlib,datetime,subprocess
ROOT=Path.cwd();P=ROOT/'private/poc/spqr-chapter9';M=P/'measurement/M-POC4B-context-01'
R=P/'reports/context-01';PR=P/'proposals/context-01';RUN=P/'runs/context-01'
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(x):
    b=x.read_bytes();return dict(path=x.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def load(x):return json.loads(x.read_bytes())
def save(x,obj):
    assert not x.exists(),x
    x.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
before=load(M/'protected-before.json')
for a in before:assert desc(ROOT/a['path'])==a,a['path']
save(M/'protected-after.json',dict(all_match_before=True,count=len(before),files=before))
raw=(RUN/'response.raw.txt').read_bytes();D=json.loads(raw)
assert raw==(PR/'proposal.json').read_bytes()==(P/'transfer/context-v1/context-01.json').read_bytes()
manifest=load(R/'manifest.json');closure=load(R/'closure.json')
assert desc(R/'manifest.json')==closure['report_manifest']
for a in manifest['artifacts']:assert desc(ROOT/a['path'])==a,a['path']
prov=load(PR/'provenance.json')
for ptr,span in prov['json_value_spans'].items():
    frag=raw[span['start_byte']:span['end_byte_exclusive']];assert sha(frag)==span['sha256'],ptr
    value=D
    if ptr:
        for part in ptr[1:].split('/'):
            key=part.replace('~1','/').replace('~0','~')
            value=value[int(key)] if isinstance(value,list) else value[key]
    assert json.loads(frag)==value,ptr
cmp=load(R/'context-comparison.json');dep=load(R/'dependency-comparison.json')
assert len(dep['all_output_edges'])==131 and len({x['id'] for x in dep['all_output_edges']})==131
assert cmp['inherited_gap_ids_retained']==81 and cmp['full_declared_gap_closures']==0
assert all(x['after']['blocking'] for x in cmp['partial_source_updates'])
assert len(load(R/'inventory.json')['items'])==207 and len(load(R/'inventory.json')['expectations'])==74
assert len(load(R/'quotes.json')['quotes'])==111 and len(load(R/'image-areas.json')['images'])==111
errors=load(R/'errors.json')['errors']
lineage={x['inherited_baseline_error_id']:x['id'] for x in errors if 'inherited_baseline_error_id' in x}
referenced=sorted({x.get('error_id') for x in dep['execution_relations'] if x.get('error_id')})
assert all(x in lineage for x in referenced)
save(M/'report-reference-supplement.json',dict(id='M-POC4B-context-01-reference-lineage',
    context_dependency_comparison=desc(R/'dependency-comparison.json'),context_errors=desc(R/'errors.json'),
    parent_dependency_comparison=desc(P/'reports/first-001/dependency-comparison.json'),
    parent_errors=desc(P/'reports/first-001/errors.json'),
    reason='Inherited tuple observations retain their explicit ERR-first-001 lineage IDs; this supplement maps them to the current observation IDs without rewriting the sealed report.',
    referenced_parent_ids=referenced,baseline_to_context_error_id=lineage,
    payload_or_semantic_change=False,scope='Report-reference lineage only'))
run=load(RUN/'run.json');assert desc(M/'extractor-thread-snapshot.json')==run['session_evidence']['snapshot']
checkroot=ROOT/'private/poc/_checks/active-c61ce4720db54e64aef8c54336b81116'
check=json.loads((checkroot/'result.json').read_text('utf-8-sig'))
assert check['tests_exit']==check['diff_exit']==0 and '114 passed' in (checkroot/'pytest.log').read_text('utf-8-sig')
diff=subprocess.run(['git','diff','--check'],capture_output=True)
(M/'diff-check.log').write_bytes(diff.stdout+diff.stderr);assert diff.returncode==0
metrics=load(R/'metrics.json')
sessions=P/'measurement/sessions.jsonl';prefix=sessions.read_bytes()
prefixdesc=next(x for x in before if x['path']==desc(sessions)['path']);assert desc(sessions)==prefixdesc
end=datetime.datetime.now(datetime.timezone.utc)
clock=datetime.datetime(2026,10,10,16,32,4,tzinfo=datetime.timezone.utc)
record=dict(id='M-POC4B-context-01-report',date='2026-10-10',timezone='Europe/Warsaw',card='M-POC4B',milestone='M-POC4',
    outcome='partial',phase='receipt_and_independent_context_report',workflow_status='closed_report_waiting_source_effect_review',
    first_recorded_clock_utc=clock.isoformat(),completed_at_utc=end.isoformat(),recorded_calendar_elapsed_seconds=(end-clock).total_seconds(),
    time_limitation='Evaluator calendar interval is not active user/model time; extractor app turn clocks recorded separately, neither establishes remaining total/after-first budget.',
    application='Codex desktop evaluator; separate extractor app task transcript available',
    actual_model_visible_name='unknown',reasoning_level='unknown',user_active_time='unknown',model_active_time='unknown',
    tokens='unknown',price='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',
    parent_response=desc(P/'runs/first-001/first-001.json'),response=desc(RUN/'response.raw.txt'),
    input_manifest=run['input_manifest'],original_input_manifest=run['original_input_manifest'],freeze=run['freeze'],
    evaluation_id='eval-v1',evaluation_manifest=run['evaluation_manifest'],
    extraction_turn_timing=run['timing'],extraction_configuration=run['extraction_configuration'],
    session_scope_violation='Confirmed repository-root names/path discovery outside allowlist',
    clean_context_verified=False,assessment_exposure='unknown',contamination_proven=False,
    human_review=dict(source_selection='Previously approved in M-POC4A exact scope',source_effect='waiting_review',
        meaning='waiting_review',new_semantic_decisions=0),semantic_acceptance='not_performed',semantic_result='not_assessable',
    counters=dict(manual_context_response_rounds_total=1,new_inference_responses_by_evaluator=0,new_corrections=0,
        additional_pages=1,additional_rules=1,additional_tables=0,supplied_depth=1,selected_considered_depth=2,
        new_linked_path_to_unresolved_target=3,no_third_step_source_acquired=True,no_pass_02=True),
    size_and_round_limits_unchanged=True,full_graph_depth_compliance='not_assessable',
    context_result=dict(full_declared_gap_closures=0,old_declarations_retained=81,partial_updates=4,new_declarations=4,
        semantic_improvement='not_assessable',semantic_regressions='not_assessable'),
    summary_metrics=metrics,report_manifest=desc(R/'manifest.json'),report_closure=desc(R/'closure.json'),
    outputs=[desc(x) for folder in [RUN,PR,R] for x in sorted(folder.iterdir()) if x.is_file()],
    pending_review_request=desc(P/'reviews/context-source-01/request.json'),
    audit_evidence=[desc(x) for x in sorted(M.iterdir()) if x.is_file()],
    protected_files=len(before),protected_all_unchanged=True,raw_pointer_spans_verified=len(prov['json_value_spans']),
    original_and_preserved_and_proposal_byte_identical=True,sessions_append_baseline=prefixdesc,
    checks=dict(script='scripts/check.ps1',passed=114,tests_exit=0,diff_exit=0,result=desc(checkroot/'result.json'),
        pytest_log=desc(checkroot/'pytest.log'),script_diff_log=desc(checkroot/'diff-check.log'),standalone_diff_log=desc(M/'diff-check.log'),
        basetemp=check['basetemp'],tmp_temp_policy='Local GUID run root and previously nonexistent basetemp; offline'),
    next_card='M-POC4B',next_action='Owner reviews closed report, context comparison and source-effect request. Confirm only bounded partial procedure/source target with zero full gap closure and explicit residual/depth/isolation limitations. Then M-POC5A/B evaluates both answers separately on eval-v1.',
    not_performed=['new extraction','response correction','source expansion/pass-02','semantic acceptance','M-POC5','M-POC6','M-POC7'],
    preserved_existing_changes='M-POC4A review/freeze/transfer preparation changes retained; baseline artifacts/expectations never overwritten.')
save(M/'completion.json',record)
assert prefix.endswith(b'\n') and not any(json.loads(line)['id']==record['id'] for line in prefix.splitlines())
line=dict(record,completion=desc(M/'completion.json'))
with sessions.open('ab') as f:f.write((json.dumps(line,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
assert sessions.read_bytes()[:len(prefix)]==prefix
save(M/'append-verification.json',dict(record_id=record['id'],previous_prefix=prefixdesc,prefix_preserved=True,
    completion=desc(M/'completion.json'),after=desc(sessions)))
print(json.dumps(dict(completion=desc(M/'completion.json'),tests_passed=114,protected=len(before),
    raw_pointer_spans=len(prov['json_value_spans']),prefix_preserved=True,report_closed=True,card='partial/waiting_review'),indent=2))
