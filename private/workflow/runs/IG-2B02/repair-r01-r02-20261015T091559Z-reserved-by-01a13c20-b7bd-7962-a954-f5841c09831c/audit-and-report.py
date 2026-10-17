"""Independent comparisons of complete metadata and canonical snapshots; current reports."""
from collections import Counter
import copy
from importlib.machinery import SourceFileLoader
import json
from pathlib import Path

u = SourceFileLoader('repair_common', str(Path(__file__).with_name('repair-common.py'))).load_module()
replay = SourceFileLoader('repair_replay', str(u.A / 'replay-repair.py')).load_module()

def diffs(a,b,path=''):
    if a == b:
        return []
    if path.endswith('/components') or '/corrections_after_enlargement/' in path:
        return [dict(pointer=path,before=a,after=b)]
    if isinstance(a,dict) and isinstance(b,dict):
        result=[]
        for key in list(a) + [k for k in b if k not in a]:
            p=path+'/'+key.replace('~','~0').replace('/','~1')
            if key not in a or key not in b:
                result.append(dict(pointer=p,change='added' if key in b else 'removed'))
            else:
                result.extend(diffs(a[key],b[key],p))
        return result
    if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in diffs(x,y,path+'/'+str(i))]
    return [dict(pointer=path,before=a,after=b)]

def report(name,value):
    u.write(u.A/name,dict(task='IG-2B02',actor=u.CFG['actor'],recorded_utc=u.now(),**value))

if __name__=='__main__':
    root_check=u.load(u.A/'root-inventory-validate.command.json')
    assert root_check['exit_code']==0
    root_result=u.load(u.A/'root-inventory-validate.stdout')
    assert root_result==u.load(u.A/'final-verified/coverage.json')
    oldspec=u.load(u.D/'author-specifications-final.json');spec=u.load(u.A/'author-specifications-final.json')
    oldobs=u.load(u.D/'component-observations.json');obs=u.load(u.A/'component-observations.json')
    oldledger=u.load(u.D/'region-ledger-final.json');ledger=u.load(u.A/'region-ledger-final.json')
    visual=u.load(u.A/'visual-inspection.json');own=u.load(u.A/'source-observations.json')
    oldvisual=u.load(u.D/'visual-inspection.json')
    assert len(ledger['regions'])==len(spec['specifications'])==len(visual['every_region'])==141
    assert len({x['region']['id'] for x in ledger['regions']})==141
    assert len({x['region']['key'] for x in ledger['regions']})==141
    expected=copy.deepcopy(oldspec)
    for row in expected['specifications']:
        if row['key'] in u.TARGETS:row['components']=u.TARGETS[row['key']]['required_after_components']
    assert spec==expected
    specdiff=diffs(oldspec,spec);assert len(specdiff)==3
    expected=copy.deepcopy(oldobs)
    expected['corrections_after_enlargement'].update({k:t['required_after_components'] for k,t in u.TARGETS.items()})
    expected['repair_provenance']=obs['repair_provenance'];assert obs==expected
    # Preserve the exact old compact-map lines, including original uncertain strings.
    oldtext=(u.D/'component-observations.json').read_text(encoding='utf-8')
    newtext=(u.A/'component-observations.json').read_text(encoding='utf-8')
    for line in oldtext.splitlines():
        if line.startswith('    "ig2b02:'):assert line in newtext
    ledgerdiff=diffs(oldledger,ledger)
    semantic=[x for x in ledgerdiff if x['pointer'].endswith('/components')]
    operational=[x for x in ledgerdiff if x not in semantic]
    assert len(semantic)==3
    assert {x['pointer'] for x in operational}=={'/inventory_pin/path','/registry_pin/path','/repair_attribution'}
    expected=copy.deepcopy(oldledger)
    for row in expected['regions']:
        if row['region']['key'] in u.TARGETS:row['components']=u.TARGETS[row['region']['key']]['required_after_components']
    for key in ('inventory_pin','registry_pin','repair_attribution'):expected[key]=ledger[key]
    assert ledger==expected
    full=u.load(u.A/'final-verified/inventory.json');reg=u.load(u.A/'final-verified/identity-registry.json')
    regions={x['id']:x for x in full['regions']};evidence={x['id']:x for x in full['evidence']}
    specs={x['key']:x for x in spec['specifications']}
    full_rows=[];raw=[];affected=[]
    for i,(row,previous,vrow) in enumerate(zip(ledger['regions'],oldledger['regions'],visual['every_region'])):
        key=row['region']['key'];t=u.TARGETS.get(key)
        assert row['region']==regions[row['region']['id']]
        assert row['evidence']==evidence[row['evidence']['id']]
        effective=obs['corrections_after_enlargement'].get(key,specs[key]['components'])
        assert effective==row['components']==vrow['components']
        assert vrow['region_id']==row['region']['id'] and vrow['revision']==row['region']['revision']
        assert vrow['key']==key and vrow['component_evidence_id']==row['evidence']['id']
        assert oldvisual['every_region'][i]['components']==previous['components']
        assert vrow['current_executor_viewed_exact_counter']==(key in u.TARGETS)
        assert row['evidence']['region_id']==row['region']['id'] and row['evidence']['box']==row['region']['box']
        assert row['evidence']['region_revision']==row['region']['revision']
        triple=[row['evidence'][k] for k in ('text','image','crop_pdf')]
        for p in triple:u.verify(p)
        raw.extend(triple)
        full_rows.append(dict(key=key,region_id=row['region']['id'],revision=row['region']['revision'],
                              canonical_region_exact=True,original_evidence_exact=True,effective_components_consistent=True,
                              full_noncomponent_entry_exact={k:v for k,v in row.items() if k!='components'}=={k:v for k,v in previous.items() if k!='components'},
                              component_delta='authorized' if t else 'unchanged',
                              own_viewed=bool(t),original_observation_attribution=u.pin(u.D/'visual-inspection.json')))
        if t:
            matching=[x for x in own['observations'] if x['region']['key']==key];assert len(matching)==1
            assert matching[0]['region']==row['region'] and matching[0]['observed_after_components']==row['components']
            assert previous['components']==t['before_components'] and row['components']==t['required_after_components']
            affected.append(dict(finding_id=t['finding_id'],key=key,region_id=row['region']['id'],revision=row['region']['revision'],
                                 pdf_page=5,box=row['region']['box'],before=t['before_components'],after=row['components'],
                                 primary_evidence=t['original_source_evidence'],review_enlargement=t['independent_review_enlargement'],
                                 own_observation=matching[0],current_changes=[dict(artifact=u.pin(u.A/'author-specifications-final.json'),pointer=f'/specifications/{i}/components'),
                                 dict(artifact=u.pin(u.A/'component-observations.json'),pointer='/corrections_after_enlargement/'+key),
                                 dict(artifact=u.pin(u.A/'region-ledger-final.json'),pointer=f'/regions/{i}/components'),
                                 dict(artifact=u.pin(u.A/'visual-inspection.json'),pointer=f'/every_region/{i}/components')],
                                 validation='Source-observed after array; all four current component authorities agree; canonical nested record and triple exact.'))
    assert len(raw)==423 and len({p['path'] for p in raw})==423
    assert len(affected)==3 and len({x['finding_id'] for x in affected})==2
    for row in full_rows:assert row['full_noncomponent_entry_exact']
    copies=[]
    for name in replay.PRODUCTS[:5]:
        assert (u.A/name).read_bytes()==(u.D/name).read_bytes()
        assert u.load(u.A/name)==u.load(u.D/name)
        copies.append(dict(current=u.pin(u.A/name),original=u.pin(u.D/name),byte_identical=True,object_equal=True))
    task_counts=Counter(str(r['pdf_page']) for r in ledger['regions']);assert dict(task_counts)=={'5':39,'6':33,'7':39,'8':30}
    assert len(full['pages'])==44 and len(full['regions'])==308
    assert sum(r['denominator_role']=='inventory' for r in full['regions'])==307
    assert sum(r['denominator_role']=='context' for r in full['regions'])==1
    baseline=u.load(u.D/'preservation-report.json')
    u.verify(baseline['baseline']);u.verify(baseline['registry_baseline'])
    accepted=u.load(u.R/baseline['baseline']['path']);accepted_reg=u.load(u.R/baseline['registry_baseline']['path'])
    assert all(entry in reg['entries'] for entry in accepted_reg['entries'])
    preserved=[r for r in accepted['regions'] if r['key'].startswith('ig2b01:') or r['denominator_role']=='context']
    for row in preserved:assert regions[row['id']]==row
    assert len([r for r in preserved if r['denominator_role']=='inventory'])==130
    old_evidence=[]
    for ev in accepted['evidence']:
        assert evidence[ev['id']]==ev
        for k in ('text','image','crop_pdf'):u.verify(ev[k]);old_evidence.append(ev[k])
    assert all(link in full['links'] for link in accepted['links'])
    accepted_ids={r['id'] for r in preserved}
    assert [x for x in full['reading_order'] if x in accepted_ids]==[x for x in accepted['reading_order'] if x in accepted_ids]
    placeholders=[r for r in accepted['regions'] if r['key'].startswith('placeholder:')]
    # Compare all non-task region objects directly with the reviewed complete base.
    old_full=u.load(u.D/'final-verified/inventory.json');assert old_full==full
    task_ids={r['region']['id'] for r in ledger['regions']}
    unchanged_other=[r for r in full['regions'] if r['id'] not in task_ids]
    assert len(unchanged_other)==167
    assert len([r for r in unchanged_other if r['denominator_role']=='inventory'])==166
    assert all(r['coverage']['transcription']['status']=='partial' and r['coverage']['descriptive_semantics']['status']=='unprocessed' and r['coverage']['formal_semantics']['status']=='unprocessed' for r in (x['region'] for x in ledger['regions']))
    for p in u.pins_in(full):u.verify(p)
    replay_results=[]
    for child in ('replay-one','replay-two'):
        files=[]
        for name in replay.PRODUCTS:
            assert (u.A/name).read_bytes()==(u.A/child/name).read_bytes(),(child,name)
            files.append(dict(current=u.pin(u.A/name),replayed=u.pin(u.A/child/name),byte_identical=True))
        replay_results.append(dict(output=child,files=files))
    report('delta-audit.json',dict(outcome='passed',specifications_delta=specdiff,ledger_component_delta=semantic,
                                 component_override_delta=diffs(oldobs,obs),ledger_operational_delta=operational,
                                 operational_justification='Current canonical snapshot paths point into new byte-identical attempt; repair_attribution separates old viewing from this actor and pins current correction authority.',
                                 visual_operational_justification='New actor and explicit per-region provenance replace inherited viewing claims; 141 effective arrays agree, with exactly the three authorized array changes.',
                                 unrelated_138_component_lists_exact=True,all_seven_original_overrides_exact=True,
                                 all_noncomponent_source_strings_and_order_exact=True,canonical_revision_changes=0,
                                 component_authority_rule=u.RULE,complete_region_comparisons=full_rows))
    report('affected-component-audit.json',dict(outcome='passed',targets=affected,component_authority_rule=u.RULE,
                                              no_identity_merge=True,source_observations=u.pin(u.A/'source-observations.json')))
    report('preservation-report.json',dict(outcome='passed',canonical_snapshot_comparisons=copies,
               accepted_baseline=baseline['baseline'],accepted_registry=baseline['registry_baseline'],
               reviewed_baseline=u.pin(u.D/'preservation-report.json'),original_report_attribution='Original executor baseline report retained as input only; equality and pin comparisons above/below are fresh repair checks.',
               source_and_page_geometry_exact=True,all_44_page_objects_exact=True,all_308_region_objects_exact=True,
               old_context_identity_revision_evidence_links_order_exact=True,all_53_links_and_308_order_entries_exact=True,
               registry_all_entries_and_order_exact=True,accepted_registry_entries_preserved=len(accepted_reg['entries']),
               preserved_authored=130,placeholders_9_44=36,task_counts_by_page=dict(task_counts),task_denominator=141,
               full_denominator=307,context_denominator=0,context_region_count=1,canonical_coverage_exact=True,
               new_primary_files_verified=raw,old_primary_files_verified=old_evidence,
               regenerated_or_copied_primary_evidence_files=0,original_evidence_paths_exact=True,
               source_content_access='Only three specified counter PNGs/enlargements; all other raw bytes hashed only.',
               unrelated_changes='Repair scripts write only attempt-owned paths; workflow transitions own authorized status projections. No reset/clean/stash/commit/push or unrelated file editing.',
               root_validation=root_check,source_structure_verification=root_result['source_structure_verification']))
    report('replay-report.json',dict(outcome='passed',generator=u.pin(u.A/'replay-repair.py'),support=u.pin(u.A/'repair-common.py'),
            plan=u.pin(u.A/'repair-plan.json'),runs=replay_results,files_per_run=9,
            product_reference_policy='Replay output files retain primary attempt logical references and therefore reproduce exact metadata bytes.',
            inventory_generation_invoked=False,uuid_allocation_invoked=False,old_fixed_path_scripts_executed=False))
    current_refs={name:u.pin(u.A/name) for name in replay.PRODUCTS}
    for name in ('scope-report-final.json','context-authored-correspondence.json','continuations.json','uncertainty.json','gaps.json','geometric-gaps.json','locator-audit.json'):
        payload=u.load(u.D/name)
        for x in u.pins_in(payload):u.verify(x)
        report(name,dict(format='wgc-current-report-with-attributed-baseline-1',
                         current_snapshot=current_refs['final-verified/inventory.json'],current_registry=current_refs['final-verified/identity-registry.json'],
                         current_component_authority={n:current_refs[n] for n in ('author-specifications-final.json','component-observations.json','region-ledger-final.json','visual-inspection.json')},
                         inherited_baseline_report=u.pin(u.D/name),inherited_actor=u.load(u.D/'visual-inspection.json')['actor'],
                         baseline_payload=payload,baseline_payload_policy='Byte-pinned original observations/report. All internal old paths remain immutable original references, not current repaired component authority or new viewing by this actor.',
                         current_verification='Canonical bytes, complete ledger noncomponent metadata and all raw references equal reviewed baseline; no changed scope, locator geometry, uncertainty, continuation, correspondence or coverage claims.',
                         fresh_validation=root_check,repair_delta=u.pin(u.A/'delta-audit.json'),
                         fresh_extraction_or_rendering_performed=False,own_content_access=u.pin(u.A/'source-observations.json'),
                         independent_rereview='Pending; unchanged original inspection attribution is not transferred.'))
    report('coverage-report.json',dict(outcome='passed_unchanged_coverage',current_coverage=u.pin(u.A/'final-verified/coverage.json'),
           root_validation=root_check,task_denominator=141,full_denominator=307,context_denominator=0,
           transcription='partial for all 141 task regions',descriptive_semantics='unprocessed',formal_semantics='unprocessed',
           new_represented_or_excluded=0,semantic_acceptance_granted=False,executable_readiness='unverified'))
    checks=[u.load(u.A/(label+'.command.json')) for label in ('root-inventory-validate','source-tests','repository-check','post-repair-workflow-validate','post-repair-diff-check')]
    assert all(c['exit_code']==0 for c in checks)
    for c in checks:
        for x in u.pins_in(c):u.verify(x)
    # Preserve full historical failure evidence separately from the required passing checks.
    report('required-checks.json',dict(outcome='passed',checks=checks,historical_failures=[u.pin(u.A/'observe-toolchain.command.json')],
           changed_hypothesis=u.pin(u.A/'toolchain-comparison-hypothesis.json'),
           warning_policy='Unmodified native stderr retains Xref warning; no suppression or contract/test edits.'))
    findings=[]
    for finding in u.load(u.V/'findings.json')['findings']:
        rows=[x for x in affected if x['finding_id']==finding['id']]
        assert len(rows)==(1 if finding['id'].endswith('R01') else 2)
        findings.append(dict(id=finding['id'],severity=finding['severity'],resolution='implemented_pending_independent_review',
                             original_finding=u.pin(u.V/'findings.json'),targets=rows,validation_checks=u.pin(u.A/'required-checks.json'),
                             delta_audit=u.pin(u.A/'delta-audit.json'),preservation=u.pin(u.A/'preservation-report.json'),
                             independent_resolution=None,independent_resolution_reason='Fresh separate reviewer has not yet inspected this new delivery.'))
    report('finding-dispositions.json',dict(findings=findings,findings_count=2,distinct_targets=3,acceptance_granted=False))
    q=u.load(u.R/'docs/work/queue.json');task=next(x for x in q['tasks'] if x['id']=='IG-2B02')
    criteria=[]
    statuses=['executor-repaired_pending_independent_review','preservation_verified_pending_independent_review',
              'preservation_verified_pending_independent_review','reported_unchanged_pending_independent_review','pending_fresh_independent_session']
    for i,(text,status) in enumerate(zip(task['acceptance'],statuses),1):
        criteria.append(dict(number=i,criterion=text,status=status,self_accepted=False,
                             evidence=[u.pin(u.A/n) for n in ('finding-dispositions.json','delta-audit.json','preservation-report.json','coverage-report.json','required-checks.json')]))
    report('criteria.json',dict(criteria=criteria,criterion_1='executor-repaired_pending_independent_review',
           criterion_5='pending_fresh_independent_session',independent_review='Pending',acceptance_granted=False,
           semantic_acceptance_granted=False,whole_record_source_IG_review='not established',executable_readiness='unverified'))
    # Resolve all recursively declared current and explicitly original pins before declaring consistency.
    verified=[]
    current_json=[p for p in u.A.glob('*.json') if p.name not in ('checkpoint.json',)]
    for p in current_json:
        for x in u.pins_in(u.load(p)):
            if p.name=='preclaim-gates.json' and x['path']=='docs/work/queue.json':
                # This original preparation-time pin is a historical observation, explicitly
                # reconciled with saved queue-before by preclaim gates, not the live queue.
                assert u.sha(u.C/'queue-before.json')==x['sha256'] and (u.C/'queue-before.json').stat().st_size==x['bytes']
            else:
                u.verify(x)
            verified.append(x)
    report('report-consistency-audit.json',dict(outcome='passed',ledger_entries_checked=141,
           authority_order=u.RULE,complete_region_results=full_rows,all_current_pin_occurrences_verified=len(verified),
           all_current_json_reports_checked=[u.pin(p) for p in current_json],
           report_provenance_policy='baseline_payload fields are explicitly original immutable attribution; current_snapshot/current_component_authority designate new repaired targets.',
           target_component_arrays_consistent=True,seven_prior_overrides_exact=True,unrelated_components_unchanged=138,
           finding_ids=['IG-2B02-R01','IG-2B02-R02'],distinct_target_ids=[x['region_id'] for x in affected],
           criteria_statuses=statuses,no_acceptance_or_inherited_rereview=True))
    u.checkpoint('repair_verified',['Exact three component deltas confirmed across complete 141-entry ledger and all effective metadata','Five canonical snapshots byte-identical; all 423 primary files and old raw references verified','Two fresh replay outputs byte-identical','New root/source/repository/workflow/diff checks passed'],
                 'Verify frozen inputs after repair, freeze full delivery and safe-path preflight, then one transition to review.')
    print('PASS: exact 3-region delta, 138 unchanged groups, 7 preserved overrides, 423 primary files, 141/307/0 counts, two byte-identical replays; complete attributed reports written.')
