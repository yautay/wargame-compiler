"""Verify the closed artifacts, preserve measurement prefix, append once."""
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path.cwd();P=ROOT/'private/poc/spqr-chapter9';M=P/'measurement/M-POC3-first-001';R=P/'reports/first-001';PR=P/'proposals/first-001'
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(path):
    b=path.read_bytes();return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def save(path,obj):
    assert not path.exists(), 'Refusing to overwrite '+str(path)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
before=json.loads((M/'protected-before.json').read_bytes())
protected=[]
for a in before:
    now=desc(ROOT/a['path']);assert now==a,'Protected bytes changed: '+a['path'];protected.append(now)
save(M/'protected-after.json',{'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_match_before':True,'files':protected})
manifest=json.loads((R/'manifest.json').read_bytes());closure=json.loads((R/'closure.json').read_bytes())
for a in manifest['artifacts']:assert desc(ROOT/a['path'])==a
assert desc(R/'manifest.json')==closure['report_manifest']
raw=(P/'runs/first-001/first-001.json').read_bytes();d=json.loads(raw)
assert (PR/'proposal.json').read_bytes()==raw
prov=json.loads((PR/'provenance.json').read_bytes())
def deref(pointer):
    o=d
    if not pointer:return o
    for part in pointer[1:].split('/'):
        k=part.replace('~1','/').replace('~0','~')
        o=o[int(k)] if isinstance(o,list) else o[k]
    return o
for ptr,s in prov['json_value_spans'].items():
    fragment=raw[s['start_byte']:s['end_byte_exclusive']]
    assert sha(fragment)==s['sha256'] and json.loads(fragment)==deref(ptr),ptr
metrics=json.loads((R/'metrics.json').read_bytes());inv=json.loads((R/'inventory.json').read_bytes())
assert len(inv['items'])==len({x['inventory_id'] for x in inv['items']})==207
assert len(inv['expectations'])==74 and not inv['unmapped_reference_ids']
assert sum(c['unassessed'] for c in metrics['content_categories'])==sum(c['checked_denominator'] for c in metrics['content_categories'])
assert metrics['image_locators']['strict_contained_quote_matches']+metrics['image_locators']['graphic_label_visual_matches']+metrics['image_locators']['quote_area_failure']+metrics['image_locators']['boundary_clipping_pending_review']==105
cmp=json.loads((R/'dependency-comparison.json').read_bytes())
assert len(cmp['all_output_edges'])==126 and len({x['id'] for x in cmp['all_output_edges']})==126
assert len(cmp['execution_relations'])==8 and len(cmp['mentions'])==len(cmp['continuations'])==7
run=json.loads((P/'runs/first-001/run.json').read_bytes())
for f in run['inputs']['known_prepared_package_files']:
    a=(ROOT/f['canonical_path']).read_bytes();b=(ROOT/f['transfer_path']).read_bytes()
    assert a==b and sha(a)==f['sha256'] and len(a)==f['bytes']
assert (ROOT/run['response']['original_path']).read_bytes()==raw
checkroot=ROOT/'private/poc/_checks/active-6c5bcb2f017c4e378b4262461799028f'
check_result=json.loads((checkroot/'result.json').read_text(encoding='utf-8-sig'))
log=(checkroot/'pytest.log').read_text(encoding='utf-8-sig')
assert check_result['tests_exit']==check_result['diff_exit']==0
assert re.search(r'104 passed',log)
checks={'script':'scripts/check.ps1','result':desc(checkroot/'result.json'),
 'pytest_log':desc(checkroot/'pytest.log'),'diff_check_log':desc(checkroot/'diff-check.log'),
 'passed':104,'tests_exit':0,'diff_exit':0,'basetemp':check_result['basetemp'],
 'tmp_temp_policy':'scripts/check.ps1 creates local runRoot/temp and a previously nonexistent GUID basetemp',
 'final_standalone_diff_check':{'exit':0,'log':desc(M/'diff-check.log'),'warning':'Git line-ending notices for public documents; no whitespace errors'}}
end=datetime.datetime.now(datetime.timezone.utc)
started=datetime.datetime(2026,10,9,18,47,33,tzinfo=datetime.timezone.utc)
record={'id':'M-POC3-first-001-baseline','date':'2026-10-09','timezone':'Europe/Warsaw',
 'card':'M-POC3','milestone':'M-POC3','outcome':'done','run_id':'first-001',
 'phase':'first_result_format_evidence_inventory_report','workflow_status':'closed_baseline_waiting_semantic_review',
 'milestone_status':'done','next_card':'M-POC4A',
 'next_action':'Separate M-POC4A: read run.json and closed report/dependency comparison/errors; select necessary blocking targets, verify source availability, count unique added pages/rules/tables/depth and limits before context/pass-01. Do not infer external context need from missing internal graph tuples.',
 'first_recorded_clock_utc':started.isoformat(),'completed_at_utc':end.isoformat(),
 'recorded_calendar_elapsed_seconds':(end-started).total_seconds(),
 'time_limitation':'First recorded clock is after bootstrap. Calendar evaluation time is neither extraction time nor active user/model time and does not prove total budget compliance.',
 'app':'Codex desktop','app_metadata_source':'Current developer desktop context; current evaluator only, not extractor configuration proof',
 'actual_model_visible_name':'unknown','reasoning_level':'unknown','extraction_configuration':'unknown',
 'user_active_time':'unknown','model_active_time':'unknown','extraction_started_at_utc':'unknown','extraction_completed_at_utc':'unknown',
 'tokens':'unknown','price':'unknown','budget_compliance':'unknown',
 'blind_session':'unknown','assessment_exposure':'unknown','actual_historical_transfer_list':'unknown','actual_prompt_sent':'unknown',
 'assessment_version':'eval-v1','assessment_manifest_sha256':metrics['evaluation_manifest_sha256'],
 'assessment_key_opened':True,'assessment_access_scope':'M-POC3 evaluator explicitly authorized by owner instruction and task card; frozen assessment unchanged',
 'quality':'structural_and_locational_baseline_only; semantic not_assessable','semantic_acceptance':'not_performed',
 'human_review':{'semantic_acceptance':'not_performed','scope_decisions_for_frozen_evaluation':'Existing owner decisions retained; no new semantic approval in M-POC3'},
 'response':desc(P/'runs/first-001/first-001.json'),'input_manifest_sha256':metrics['input_manifest_sha256'] if 'input_manifest_sha256' in metrics else run['inputs']['manifest_sha256'],
 'counters':{'new_extraction_responses':0,'new_context_rounds':0,'new_corrective_responses':0,'accepted_semantic_errors':'not_assessable'},
 'summary_metrics':{'inventory':metrics['reference_inventory'],'image_locators':metrics['image_locators'],
  'source_quotes':metrics['source_quotes'],'relations':metrics['relations'],'six_error_classes':metrics['six_error_classes']},
 'baseline_closed_at_utc':closure['closed_at_utc'],'closure':desc(R/'closure.json'),
 'outputs':[desc(x) for folder in [PR,R] for x in sorted(folder.iterdir()) if x.is_file()],
 'audit_evidence':[desc(x) for x in sorted(M.iterdir()) if x.is_file()],
 'protected_byte_verification':{'checked_file_count':len(before),'all_unchanged':True,'report_lineage_spans_verified':len(prov['json_value_spans']),'all_span_values_and_hashes_match_raw':True,'transfer_files':33,'eval_manifest_artifacts':7},
 'checks':checks,
 'operational_events':[
  {'operation':'Initial baseline materialization','exit':1,'reason':'KeyError for R-9.85 crosswalk key; stopped before reports; proposal bytes/provenance staged and subsequently preserved unchanged. Crosswalk corrected.'},
  {'operation':'Baseline materialization after crosswalk correction','exit':1,'reason':'All reports and closure written successfully; final console print failed with cp1252 UnicodeEncodeError. UTF-8 console setting fixed in script; closed reports not rerun/overwritten. All manifest, span and closure hashes independently verified.'},
  {'operation':'Public document patch preparation','result':'invalid patch rejected before mutation','reason':'Multiple patch operations targeted HANDOFF.md. Reissued as separate valid operations; no partial document mutation from rejected patch.'}],
 'documentation_gaps':run['documentation_gaps']}
sessions=P/'measurement/sessions.jsonl';prefix=sessions.read_bytes()
prefixdesc=next(x for x in before if x['path']==sessions.relative_to(ROOT).as_posix())
assert len(prefix)==prefixdesc['bytes'] and sha(prefix)==prefixdesc['sha256']
assert prefix.endswith(b'\n') and not any(json.loads(line)['id']==record['id'] for line in prefix.splitlines())
record['sessions_append_baseline']=prefixdesc
save(M/'completion.json',record)
completion_desc=desc(M/'completion.json')
line=dict(record);line['completion']=completion_desc
with sessions.open('ab') as stream:stream.write((json.dumps(line,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8'))
after=sessions.read_bytes();assert after[:len(prefix)]==prefix
save(M/'append-verification.json',{'record_id':record['id'],'previous_prefix':prefixdesc,
 'prefix_preserved_byte_identical':True,'sessions_after':desc(sessions),'completion':completion_desc,
 'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps({'completion':completion_desc,'protected_files':len(before),'verified_raw_spans':len(prov['json_value_spans']),
 'tests_passed':104,'diff_check_exit':0,'previous_measurement_prefix_preserved':True},ensure_ascii=False,indent=2))
