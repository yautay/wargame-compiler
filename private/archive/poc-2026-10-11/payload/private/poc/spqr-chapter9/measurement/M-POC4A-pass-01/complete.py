"""Final bounded metadata audit, byte preservation, and append-only measurement."""
import datetime
import json
import collections
import subprocess
from prepare import ROOT,P,M,load,desc,save,sha,verify
C=P/'context/pass-01'
targets=load(C/'targets.json');audit=load(C/'critical-source-audit.json');decl=load(C/'declaration-review.json')
old_manifest=desc(C/'manifest.json')
def update(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def identity(row):
    lookup=row['source_lookup'];label=lookup.get('scope','')
    original=row.get('extractor_declaration',{}).get('needed_context','')
    tc=row.get('target_candidate',{})
    label+=' '+original+' '+str(tc.get('name',''))+' '+str(tc.get('facet',''))
    low=label.lower()
    tableid=None
    for needles,tid in [(['mrrc','missile range'],'CTX-TBL-MRRC'),
        (['shock crt','shock combat results','shock combat crt'],'CTX-TBL-SHOCK-CRT'),
        (['clash of spears'],'CTX-TBL-CLASH'),(['shock superiority chart'],'CTX-TBL-SHOCK-SUPERIORITY'),
        (['movement cost chart'],'CTX-TBL-MOVEMENT-COST'),(['stacking chart'],'CTX-TBL-STACKING'),
        (['cohesion hit and tq check chart'],'CTX-TBL-COHESION-TQ'),(['combat table'],'CTX-TBL-COMBAT-UNRESOLVED')]:
        if any(n in low for n in needles):tableid=tid;break
    lookup['target_id']=tableid or 'CTX-LOOKUP-'+row['id']
    lookup['target_id_policy']='Local lookup-request identity only; exact rows, aliases and equivalence remain unconfirmed. References supply zero tables.'
for row in decl['rows']+audit['unconfirmed_candidates']+audit['frozen_context_requirements']:identity(row)
update(C/'declaration-review.json',decl);update(C/'critical-source-audit.json',audit)
paths=dict(selected=['9.32','8.46/Step-4'],selected_depth=1,considered=[
    dict(nodes=['9.32','8.46/Step-4','CTX-TBL-SHOCK-CRT'],depth=2,status='blocked_source'),
    dict(nodes=['9.32','8.46/Step-4','8.45'],depth=2,status='source_locator_candidate_deferred',reason='Not supplied; applicability/selection procedure outside chosen Step 4. Stop here.'),
    dict(nodes=['9.32','8.46/Step-4','10.13'],depth=2,status='source_already_in_baseline',reason='Existing boundary context reference only; do not follow to 6.68 as a third step.')],
    longest=2,delta_unchanged=dict(pages=1,rules=1,tables=0),
    reason='Final accounting of explicit cross-references in the selected fragment; no additional source materialization or changed pre-expansion cost.',
    stop='All depth-2 nodes terminal for this pass; no further branch or automatic round')
save(M/'final-path-audit.json',paths)
targets['final_path_audit']=desc(M/'final-path-audit.json')
targets['named_target_registry']=[dict(id=tid,status='blocked_source',
    reason='Exact chart rows/headers/notes unavailable in the bounded verified source set; lookup-request label is not an accepted alias.',
    scope='Exact named table/row requested; no additional table supplied') for tid in sorted(set(
    row['source_lookup']['target_id'] for row in decl['rows']+audit['unconfirmed_candidates']+audit['frozen_context_requirements']
    if row['source_lookup']['target_id'].startswith('CTX-TBL-')))]
targets['source_audit']=desc(C/'critical-source-audit.json');targets['declarations_audit']=desc(C/'declaration-review.json')
update(C/'targets.json',targets)
manifest=load(C/'manifest.json')
for a in manifest['files']:
    a.update(desc(ROOT/a['path']))
manifest['final_path_audit']=desc(M/'final-path-audit.json')
update(C/'manifest.json',manifest)
save(M/'package-seal-final.json',dict(previous_draft_manifest=old_manifest,
    manifest=dict(**desc(C/'manifest.json'),reason='Final integrity/allowlist of reviewable draft',scope='One pass; no approval or freeze'),
    files=manifest['files'],human_source_acceptance='waiting_review',frozen=False,
    metadata_amendment='Added distinct lookup IDs for named tables and unnamed targets; explicit terminal path audit. Source payload/cost/prompt unchanged.'))

# Verify protected files, not merely reports that once said they matched.
before=load(M/'protected-before.json');sessions=P/'measurement/sessions.jsonl'
prefix=sessions.read_bytes();prefixdesc=next(x for x in before if x['path']==desc(sessions)['path'])
assert desc(sessions)==prefixdesc
protected=[]
for a in before:
    assert desc(ROOT/a['path'])==a,a['path']
    protected.append(desc(ROOT/a['path']))
save(M/'protected-after.json',dict(all_match=True,count=len(protected),files=protected,
    reason='End-of-session byte verification of original responses, baseline reports/measurement, original inputs/transfer, source and eval-v1.'))
for a in manifest['files']:verify(a)
verify(targets['source_audit']);verify(targets['declarations_audit'])
assert len(decl['rows'])==len({x['id'] for x in decl['rows']})==79
raw=(P/'runs/first-001/first-001.json').read_bytes();proposal=json.loads(raw)
for row in decl['rows']:
    n=int(row['response_pointer'].split('/')[-1]);assert proposal['gaps'][n]==row['extractor_declaration']
    span=row['raw_span'];assert sha(raw[span['start_byte']:span['end_byte_exclusive']])==span['sha256']
    assert row['independent_necessity']=='pending' and row['criticality']=='unknown'
    assert row['source_lookup']['reason'] and row['situation_impacts'] and row['source_lookup']['target_id']
for row in audit['confirmed_execution']:
    assert row['target_source_evidence'] and row['status']=='source_already_in_baseline'
assert len(audit['confirmed_execution'])==8 and len(audit['frozen_context_requirements'])==8
assert len(audit['unconfirmed_candidates'])==105
for row in audit['unconfirmed_candidates']+audit['frozen_context_requirements']:
    assert row['source_lookup']['reason'] and row['situation_impacts']
assert not manifest['frozen'] and manifest['human_source_acceptance']=='waiting_review'
assert len(manifest['extractor_additional_allowlist'])==3
assert all('evidence/' in x for x in manifest['extractor_additional_allowlist'])
assert paths['longest']==2 and targets['budget']['time_budget_compliance']=='unknown'
checkroot=ROOT/'private/poc/_checks/active-2cb00ce4f11947b5b8253217a24547a9'
check=load(checkroot/'result.json');log=(checkroot/'pytest.log').read_text('utf-8-sig')
assert check['tests_exit']==check['diff_exit']==0 and '105 passed' in log
diff=subprocess.run(['git','diff','--check'],capture_output=True)
(M/'diff-check.log').write_bytes(diff.stdout+diff.stderr)
assert diff.returncode==0
end=datetime.datetime.now(datetime.timezone.utc)
clock=datetime.datetime(2026,10,9,19,20,21,tzinfo=datetime.timezone.utc)
record=dict(id='M-POC4A-pass-01-selection',card='M-POC4A',milestone='M-POC4',outcome='partial',
    workflow_status='prepared_waiting_review',date='2026-10-09',timezone='Europe/Warsaw',
    workspace='C:/repo/wargame-compiler',branch='feature/tests',
    first_recorded_clock_utc=clock.isoformat(),completed_at_utc=end.isoformat(),
    recorded_calendar_elapsed_seconds=(end-clock).total_seconds(),
    time_limitation='First recorded clock was after bootstrap/source reads. Calendar time does not measure active human/model time or historical extraction; active budget unknown.',
    actual_model_visible_name='unknown',reasoning_level='unknown',extraction_configuration='unknown',
    user_active_time='unknown',model_active_time='unknown',tokens='unknown',price='unknown',
    remaining_active_budget='unknown',time_budget_compliance='unknown',
    historical_handoff='unknown',actual_prompt_sent='unknown',clean_context='unknown',blind_session='unknown',
    source=desc(P/'source/original-pdf-20261008-01.pdf'),source_v1=desc(P/'source/source-v1.json'),
    baseline_integrity=desc(M/'baseline-integrity.json'),parent_response=desc(P/'runs/first-001/first-001.json'),
    evaluation_id='eval-v1',evaluation_manifest=desc(P/'evaluation/eval-v1/manifest.json'),
    baseline_closed=True,semantic_acceptance='not_performed',semantic_result='not_assessable',
    human_review=dict(critical_sources='waiting_review',meaning='waiting_review',new_decisions=0),
    limits_unchanged=True,source_scope_limit_compliance=True,
    counters=dict(added_unique_pages=1,added_unique_rules=1,added_unique_tables=0,selected_depth=1,
        longest_considered_path=2,prepared_passes=1,reserved_round=1,context_response_rounds=0,new_inference_responses=0,corrective_responses=0),
    first_reached_limit='dependency_depth boundary; further expansion stopped; missing table terminal blocked_source',
    declaration_counts=dict(collections.Counter(x['source_lookup']['status'] for x in decl['rows'])),
    declaration_necessity='79 pending candidates, no new criticality or gold',
    critical_source_scope=dict(confirmed_relations=8,frozen_context_requirements=8,unconfirmed_candidates=105),
    outputs=[dict(**desc(x),reason='Bounded context selection/review artifact',scope='One draft pass; roles in manifest') for x in sorted(C.rglob('*')) if x.is_file()],
    package_seal=desc(M/'package-seal-final.json'),protected_file_count=len(protected),protected_all_unchanged=True,
    sessions_append_baseline=prefixdesc,
    checks=dict(script='scripts/check.ps1',passed=105,tests_exit=0,diff_exit=0,result=desc(checkroot/'result.json'),
        pytest_log=desc(checkroot/'pytest.log'),script_diff_log=desc(checkroot/'diff-check.log'),standalone_diff_log=desc(M/'diff-check.log'),
        basetemp=check['basetemp'],tmp_temp_policy='Local GUID run root, previously nonexistent basetemp; offline'),
    operational_events=[
        'Read-only console inspection retries: cp1252 encoding/default decoding and venv without pdfplumber; switched to UTF-8/bundled runtime. No original mutated.',
        'Initial source lookup script name shadowed select module; renamed before lookup outputs or context materialization.',
        'Draft named-procedure locator candidates corrected against actual headings before manifest; not semantic acceptance.',
        'One document patch rejected before mutation due to duplicate HANDOFF delete/add; reissued as valid updates.'],
    next_card='M-POC4A',next_action='Human reviews concrete source evidence/limits/blockers and writes a scoped decision with hashes. Freeze only after source review; future separate M-POC4B not executed.',
    audit_evidence=[desc(x) for x in sorted(M.iterdir()) if x.is_file()])
save(M/'completion.json',record)
assert prefix.endswith(b'\n') and not any(json.loads(x)['id']==record['id'] for x in prefix.splitlines())
line=dict(record,completion=desc(M/'completion.json'))
with sessions.open('ab') as stream:stream.write((json.dumps(line,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
after=sessions.read_bytes();assert after[:len(prefix)]==prefix
save(M/'append-verification.json',dict(record_id=record['id'],prefix_preserved=True,previous_prefix=prefixdesc,
    after=desc(sessions),completion=desc(M/'completion.json')))
print(json.dumps(dict(protected=len(protected),all_unchanged=True,prefix_preserved=True,checks_passed=105,
    manifest=desc(C/'manifest.json'),completion=desc(M/'completion.json')),indent=2))
