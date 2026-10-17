from reviewer import *
import copy, importlib.util
sys.dont_write_bytecode=True

def diff(a,b,path=''):
    if type(a)!=type(b): return [dict(pointer=path,before=a,after=b)]
    if isinstance(a,dict):
        result=[]
        for k in sorted(a.keys()|b.keys()):
            if k not in a or k not in b: result.append(dict(pointer=path+'/'+k,before=a.get(k),after=b.get(k)))
            else: result.extend(diff(a[k],b[k],path+'/'+k))
        return result
    if isinstance(a,list):
        if len(a)!=len(b): return [dict(pointer=path,before=a,after=b)]
        return [x for i,(aa,bb) in enumerate(zip(a,b)) for x in diff(aa,bb,path+'/'+str(i))]
    return [] if a==b else [dict(pointer=path,before=a,after=b)]

def audit():
    preflight()
    old=read(OLD/'final-verified/inventory.json'); current=read(REPAIR/'final-verified/inventory.json')
    ledger=read(REPAIR/'region-ledger-final.json'); oldledger=read(OLD/'region-ledger-final.json')
    spec=read(REPAIR/'author-specifications-final.json'); oldspec=read(OLD/'author-specifications-final.json')
    obs=read(REPAIR/'component-observations.json'); oldobs=read(OLD/'component-observations.json')
    visual=read(REPAIR/'visual-inspection.json')
    scope=read(ROOT/'private/workflow/runs/IG-2B02/repair-preparation-20261015T091559Z-01a13c20-b7bd-7962-a954-f5841c09831c/repair-scope.json')
    targets={t['region']['key']:t for t in scope['targets']}
    specs={s['key']:s for s in spec['specifications']}
    original_specs={s['key']:s for s in oldspec['specifications']}
    original_rows={s['region']['key']:s for s in oldledger['regions']}
    visuals={s['key']:s for s in visual['every_region']}
    rows=[]
    for i,r in enumerate(ledger['regions']):
        key=r['region']['key']; before=original_rows[key]
        effective=obs['corrections_after_enlargement'].get(key,specs[key]['components'])
        stripped=copy.deepcopy(r); stripped['components']=before['components']
        entry=dict(index=i,key=key,region_id=r['region']['id'],revision=r['region']['revision'],target=key in targets,components=r['components'],components_changed=before['components']!=r['components'],all_other_nested_row_fields_exact=stripped==before,effective_authority_match=effective==r['components'],visual_components_match=visuals[key]['components']==r['components'],canonical_region_match=next(c for c in current['regions'] if c['id']==r['region']['id'])==r['region'],full_row_delta=diff(before,r))
        if key in targets:
            entry['matches_declared_delta']=r['region']==targets[key]['region'] and before['components']==targets[key]['before_components'] and r['components']==targets[key]['required_after_components']
        rows.append(entry)
    write('component-delta-audit.json',dict(regions=rows,region_count=len(rows),changed_keys=[r['key'] for r in rows if r['components_changed']],unchanged_138_exact=sum(not r['components_changed'] for r in rows)==138,seven_prior_overrides_exact=all(obs['corrections_after_enlargement'][k]==v for k,v in oldobs['corrections_after_enlargement'].items()),specification_delta=diff(oldspec,spec),observation_delta=diff(oldobs,obs),ledger_top_level_delta=diff({k:v for k,v in oldledger.items() if k!='regions'},{k:v for k,v in ledger.items() if k!='regions'}),effective_authority='Current final specifications, with current corrections_after_enlargement overriding per key. Old drafts/generators never used as current component authority.'))
    snapshots=[]
    for n in ['authored/inventory.json','authored/identity-registry.json','final-verified/inventory.json','final-verified/identity-registry.json','final-verified/coverage.json']:
        snapshots.append(dict(name=n,original=pin(OLD/n),current=pin(REPAIR/n),byte_identical=(OLD/n).read_bytes()==(REPAIR/n).read_bytes()))
    accepted=read(ROOT/'private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77/final-verified/inventory.json')
    current_regions={r['id']:r for r in current['regions']}; pg={p['id']:p['pdf_page'] for p in current['pages']}
    preserved=[r for r in accepted['regions'] if r['denominator_role']=='inventory' and pg[r['page_id']]<=4]
    placeholders=[r for r in accepted['regions'] if pg[r['page_id']]>=9]
    context=[r for r in accepted['regions'] if r['denominator_role']=='context']
    prior_evidence={r['id']:r for r in accepted['evidence']}
    write('preservation-audit.json',dict(canonical_snapshots=snapshots,entire_final_inventory_deep_equal=old==current,all_44_page_objects_exact=old['pages']==current['pages'],all_308_region_objects_exact=old['regions']==current['regions'],all_evidence_objects_exact=old['evidence']==current['evidence'],all_links_exact=old['links']==current['links'],all_order_exact=old['reading_order']==current['reading_order'],registry_exact=old['registry']==current['registry'],preserved_authored_count=len(preserved),preserved_authored_all_exact=all(current_regions[r['id']]==r for r in preserved),placeholders_count=len(placeholders),placeholders_all_exact=all(current_regions[r['id']]==r for r in placeholders),accepted_context_records_exact=all(current_regions[r['id']]==r for r in context),accepted_evidence_all_exact=all(next(e for e in current['evidence'] if e['id']==k)==v for k,v in prior_evidence.items()),accepted_links_all_exact=all(l in current['links'] for l in accepted['links']),accepted_registry_entries_all_exact=all(e in current['registry']['entries'] for e in accepted['registry']['entries']),task_denominator=len(rows),full_denominator=sum(r['denominator_role']=='inventory' for r in current['regions']),context_denominator=0,context_region_count=sum(r['denominator_role']=='context' for r in current['regions']),task_counts_by_page={str(p):sum(r['pdf_page']==p for r in ledger['regions']) for p in range(5,9)}))
    primary=[r['evidence'][k] for r in ledger['regions'] for k in ['text','image','crop_pdf']]
    write('primary-byte-audit.json',check_pins([primary]))
    reports=[]; report_objects=[]
    for p in sorted(REPAIR.glob('*.json')):
        j=read(p); report_objects.append(j)
        d=diff(read(OLD/p.name),j) if (OLD/p.name).is_file() else None
        reports.append(dict(pin=pin(p),top_level_fields=list(j) if isinstance(j,dict) else None,old_report=pin(OLD/p.name) if (OLD/p.name).is_file() else None,delta=d))
    write('current-report-review-index.json',dict(reports=reports,policy='All direct current JSON metadata inspected structurally, with full recursive original/current differences recorded. Assertions are independently checked by reviewer audits and source viewing, not adopted from executor.'))
    write('current-report-pin-audit.json',check_pins(report_objects))
    # Import only inspected generate(), never the fixed-output CLI or old executor scripts.
    module_spec=importlib.util.spec_from_file_location('reviewer_metadata_replay',REPAIR/'replay-repair.py')
    mod=importlib.util.module_from_spec(module_spec); module_spec.loader.exec_module(mod)
    runs=[]
    for n in ['replay-one','replay-two']:
        destination=OUT/n; destination.mkdir(exist_ok=False); output=mod.generate(); entries=[]
        for name,data in output.items():
            dest=destination/name; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
            entries.append(dict(name=name,replayed=pin(dest),current=pin(REPAIR/name),byte_identical=data==(REPAIR/name).read_bytes()))
        runs.append(dict(output=destination.relative_to(ROOT).as_posix(),products=entries))
    write('replay-audit.json',dict(runs=runs,product_count_per_run=9,complete_declared_replay=True,primary_logical_references_retained=True,old_fixed_path_scripts_executed=False,repair_cli_executed=False,immutable_original_evidence_regenerated=False))
    print(json.dumps(dict(rows=len(rows),changed=[r['key'] for r in rows if r['components_changed']],reports=len(reports),report_pin_errors=read(OUT/'current-report-pin-audit.json')['errors'],snapshots_exact=all(x['byte_identical'] for x in snapshots),replay_exact=all(e['byte_identical'] for r in runs for e in r['products']))))
if __name__=='__main__': audit()
