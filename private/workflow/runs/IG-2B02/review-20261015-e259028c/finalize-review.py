"""Freeze independent reviewer observations and exact current delivery decision."""
import importlib.util
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

spec=importlib.util.spec_from_file_location('review_tools',Path(__file__).with_name('review-tools.py'))
rt=importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)
read,pin,write=rt.read,rt.pin,rt.write
OUT,BASE,V01,SESSION=rt.OUT,rt.BASE,rt.V01,rt.SESSION

def supplemental():
    inv=read(BASE/'final-verified/inventory.json')
    ledger=read(BASE/'region-ledger-final.json')
    current={r['id']:r for r in inv['regions']}
    gaps=read(BASE/'gaps.json')['baseline_payload']
    require=[]
    def check(name,condition):
        assert condition,name
        require.append({'name':name,'passed':True})
    check('all 141 representation gaps exact',len(gaps['representation_gaps'])==141 and all(g['key']==current[g['region_id']]['key'] and g['revision']==current[g['region_id']]['revision'] and g['levels']==current[g['region_id']]['coverage'] for g in gaps['representation_gaps']))
    geometry=read(BASE/'geometric-gaps.json')['baseline_payload']
    root=read(OUT/'root-inventory.stdout')
    check('full geometric accounting equals fresh root validation',geometry['full_page_accounting']==root['pages'])
    def area(b):return (b[2]-b[0])*(b[3]-b[1])
    def overlap(a,b):return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])
    for page in geometry['assigned_page_complement']:
        rectangles=page['rectangles']
        boxes=[r['box'] for r in inv['regions'] if r['denominator_role']=='inventory' and r['page_id']==page['page_id']]
        check('exact complement of page '+str(page['pdf_page']),sum(map(area,rectangles))+sum(map(area,boxes))==10**12 and all(not overlap(a,b) for i,a in enumerate(rectangles+boxes) for b in (rectangles+boxes)[i+1:]))
    uncertainty=read(BASE/'uncertainty.json')['baseline_payload']
    check('counter uncertainty preserved',len(uncertainty['small_counter_glyphs'])==16 and all(u['uncertainty']==current[u['region_id']]['uncertainty'] for u in uncertainty['small_counter_glyphs']))
    evidence={e['id']:e for e in inv['evidence']}
    check('literal anomaly locators current',all(a['revision']==current[a['region_id']]['revision'] and a['text_pin']==evidence[a['evidence_id']]['text'] for a in uncertainty['literal_anomalies']))
    prior_path=Path('private/workflow/runs/IG-2B02/review-20261015T134030Z-ig2-2cc49348/review.json')
    prior=read(prior_path)
    prior_visual=read(prior['review_evidence'][0]['path'])
    old=read(BASE/'delivery.json')
    check('prior reviewer exact artifact coverage preserved',prior['artifacts']==old['artifacts'])
    check('prior visual review exact complete ledger coverage preserved',len(prior_visual['regions'])==141 and all(v['source_boundary_inspected'] and v['complete_ledger_entry_compared'] and v['revision']==row['region']['revision'] and v['region_id']==row['region']['id'] and v['components']==row['components'] and v['box']==row['region']['box'] for v,row in zip(prior_visual['regions'],ledger['regions'])))
    check('fresh reviewer identity distinct',rt.META['actor']!=prior['actor'] and rt.META['actor']!=read(V01/'delivery.json')['actor'])
    check('only current V01 finding',len(prior['findings'])==1 and prior['findings'][0]['id']=='IG-2B02-V01')
    output=Path((OUT/'repository-check.stdout').read_text(encoding='utf-8').splitlines()[0].split('=',1)[1])
    result=read(output/'result.json')
    check('full repository named subchecks pass',all(result[k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit']))
    check('source suite count', '71 passed' in (OUT/'sources-tests.stdout').read_text(encoding='utf-8'))
    check('repository suite count','151 passed' in (OUT/'repository-check.stdout').read_text(encoding='utf-8'))
    logs=[pin(output/n) for n in ['plan.log','dry-run.log','pytest.log','diff-check.log','result.json']]
    print(json.dumps(write('supplemental-audit.json',{'all_passed':True,'checks':require,'prior_review':pin(prior_path),'prior_visual_review':pin(prior['review_evidence'][0]['path']),'repository_check_logs':logs,'representation_gap_count':141,'geometric_complement_pages':[5,6,7,8],'preserved_prior_review_regions':141})))

def finish():
    task=read(SESSION/'task.json')
    ref=read(SESSION/'delivery-reference.json')
    delivery=read(ref['evidence'])
    ledger=read(BASE/'region-ledger-final.json')
    rows=[]
    for i,row in enumerate(ledger['regions']):
        r=row['region']; n=row['pdf_page']
        rows.append({'ledger_index':i,'region_id':r['id'],'revision':r['revision'],'key':r['key'],'pdf_page':n,'box':r['box'],'label':row['label'],'components':row['components'],'uncertainty':r['uncertainty'],'raw_text':row['evidence']['text'],'source_boundary_inspected':True,'complete_ledger_entry_compared':True,'grouped_diagram_inspected':r['kind']=='diagram','original':pin(OUT/f'original-{n:02}.png'),'boundaries':pin(OUT/f'boundaries-{n:02}.png'),'observation':'Compared visible assigned original content and region boundary with the complete ledger entry, literal extraction, and named components. No discrepancy found. Machine extraction remains partial.'})
    visual=write('visual-review.json',{'scope_pages':[5,6,7,8],'source':ledger['source'],'ledger':pin(BASE/'region-ledger-final.json'),'regions':rows,'region_counts':dict(Counter(r['pdf_page'] for r in rows)),'diagram_count':17,'diagram_component_sheet':pin(OUT/'diagram-components.png'),'page_observations':{
        '5':'All 39 regions inspected. Triarii tail, the twelve named troop entries including unillustrated Maniple and Skirmishers, eleven sample counters, wrapping prose, running header, label, rule and footer are accounted for. Alae lower values are 5 and 5; each separate Thrace counter retains the small white 1 below the name and left of J. Small identifiers remain uncertain.',
        '6':'All 33 regions inspected. Light Cavalry completion, five illustrated unit entries with wrapped text, sections 2.5-2.7, shaded historical note, 3.0 introduction, activation heading/paragraph and editorial furniture are accounted for.',
        '7':'All 39 regions inspected. Orders sequence headings and every lettered/numbered item, Momentum, Rout/Reload, Withdrawal, 4.0 and 4.1, the complete annotated leader diagram with seven callouts/leader lines, every rating paragraph, shaded design note and editorial furniture are accounted for.',
        '8':'All 30 regions inspected. 4.2 and 4.3 headings, 4.21 including three separate bullets, 4.22-4.25, 4.31-4.33, left-to-right-column 4.32 continuation, example, shaded historical note, commander headings, both numbered conditions including printed or, both exceptions, final Momentum paragraph and editorial furniture are accounted for. Final paragraph ends with a complete sentence.'},
        'continuations':{'page_4_to_5':'Read only the exact accepted p04-033 crop. Its final words spear-armed continue into heavy infantry on assigned page 5. Both old context and distinct authored links retained.','page_5_to_6':'Literal magnifi-/cent continuation visually verified with separate current identities and raw strings.','page_8_columns':'4.32 continues from bottom left to top right; exact linked identities and explicit reading order checked.','page_9':'No access needed or performed; final page-8 paragraph is complete.'},
        'page_4_access':pin('private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77/evidence/p04-033/image.png'),'page_9_accessed':False,'other_unassigned_source_content_accessed':False,'standalone_tables':'None observed; annotated leader callout legend is included inside its diagram region.','coverage_limits':'All task transcription remains partial; descriptive and formal semantics unprocessed. Geometric complement, editorial classification and images grant no represented/excluded status.','semantic_acceptance_granted':False,'executable_readiness':'unverified'})
    checks=[read(OUT/(n+'.json')) for n in ['sources-tests','repository-check','root-inventory','workflow-validate','diff-check','original-pages']]
    checks += [{**rt.META,'name':'independent-current-ledger-locator-and-preservation-audit','command':['.venv/Scripts/python.exe','-B',(OUT/'independent-audit.py').relative_to(Path.cwd()).as_posix()],'exit_code':0,'report':pin(OUT/'independent-audit.json')},
               {**rt.META,'name':'independent-gaps-and-prior-coverage-audit','command':['.venv/Scripts/python.exe','-B',(OUT/'finalize-review.py').relative_to(Path.cwd()).as_posix(),'supplemental'],'exit_code':0,'report':pin(OUT/'supplemental-audit.json')},
               {**rt.META,'name':'final-frozen-artifact-verification','command':['.venv/Scripts/python.exe','-B',(OUT/'review-tools.py').relative_to(Path.cwd()).as_posix(),'verify','frozen-verification-final.json'],'exit_code':0,'report':pin(OUT/'frozen-verification-final.json')}]
    assert all(c['exit_code']==0 for c in checks)
    final=read(OUT/'frozen-verification-final.json')
    assert final['all_passed'] and final['queue_matches_packet'] and final['ordered_delivery_count']==4409 and final['original_ordered_prefix_equal']
    assert pin(ref['evidence'])['sha256']==ref['sha256']
    evidence=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file()]
    manifest=write('review-manifest.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'files':evidence,'policy':'New independent reviewer files only. Frozen delivery artifacts remain separately listed exactly in review.json, in delivery order. Append-only; no prior attempt or product file modified.'})
    start=datetime.fromisoformat(read(rt.CONFIG)['observed_utc'])
    end=datetime.now(timezone.utc)
    review=write('review.json',{'outcome':'pass','technical_result':'pass','summary':'V01 resolved by approved execution of unchanged required suites: 71 source tests and 151 repository tests pass. All 4409 delivery artifacts match; the original 4375 entries remain an exact ordered prefix. Independently inspected all four original assigned pages and the complete 141-region ledger; preserved prior scope, locators, components, gaps and coverage verified.','criteria':task['acceptance'],'criteria_results':[{'criterion':criterion,'status':'verified','basis':[visual,pin(OUT/'independent-audit.json'),pin(OUT/'supplemental-audit.json'),pin(OUT/'frozen-verification-final.json')]} for criterion in task['acceptance']],'artifacts':delivery['artifacts'],'checks':checks,'findings':[],'resolved_findings':[{'id':'IG-2B02-V01','status':'resolved','repair_validation':'Independent fresh approved runs of the exact unchanged tests/sources and scripts/check.ps1 -Task IG-2B02 exit 0; named repository subchecks all zero. Installed complete pinned dependency environment verified; all original source, implementation, test and contract bytes preserved.','affected_criteria':[task['acceptance'][4]],'reports':[pin(OUT/'sources-tests.json'),pin(OUT/'repository-check.json'),pin(OUT/'supplemental-audit.json')]}],'preserved_completed_findings':{'IG-2B02-R01':'Exact current Alae component array and literal 5/5 inspected; no further repair.','IG-2B02-R02':'Both distinct Thrace counters include the white 1 component; independently inspected each; no further repair.'},'delivery_reference':pin(SESSION/'delivery-reference.json'),'delivery':pin(ref['evidence']),'input_packet':pin(SESSION/'packet.json'),'references':pin(SESSION/'references.json'),'review_evidence':[manifest,visual,pin(OUT/'independent-audit.json'),pin(OUT/'supplemental-audit.json'),pin(OUT/'frozen-verification-final.json')],'counts':{'task_denominator':141,'full_denominator':307,'context_denominator':0,'preserved_authored':130,'unprocessed_placeholders_9_44':36},'preservation':'All frozen artifacts and 103 base files verified. Exact accepted pages 1-4 and placeholders 9-44, accepted regions, 131 old evidence records, prior links and 219 persisted registry entries retained; no identity remapping. Queue matches packet; no queue/status, implementation, sources or old attempts changed.','acceptance_granted':False,'semantic_acceptance_granted':False,'executable_readiness':'unverified','remaining_gates':'Coordinator technical acceptance/done remains separate. Source-IG reconciliation, independently verified full transcription, human semantic acceptance and executable readiness are not established by this inventory review.','next_action':'Return this independent pass to the supervisor for its separate coordinator gate. Stop after this reviewer role.','measurement':{'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'wall_seconds':(end-start).total_seconds(),'input_tokens':None,'output_tokens':None,'operator_seconds':None,'monetary_cost':None,'unknown_reason':'Not exposed or reported.'},'immutability':'This review and all reviewer evidence are new append-only records; no listed file will be overwritten.'})
    assert read(OUT/'review.json')['artifacts']==delivery['artifacts']
    print(json.dumps(review))

if __name__=='__main__':
    import sys
    if sys.argv[1]=='supplemental':supplemental()
    elif sys.argv[1]=='finish':finish()
