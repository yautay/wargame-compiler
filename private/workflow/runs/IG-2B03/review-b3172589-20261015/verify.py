import hashlib, json, pathlib, datetime

ROOT = pathlib.Path.cwd()
OUT = ROOT / 'private/workflow/runs/IG-2B03/review-b3172589-20261015'
SESSION = pathlib.Path('private/workflow/orchestrator/20261015T164901Z-046553b7/002-IG-2B03-reviewer-b3172589')
BASE = pathlib.Path('private/workflow/runs/IG-2B03/continuation-search-20261015-01')
def load(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with (ROOT/p).open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
CONFIG = SESSION / 'runtime-configuration.json'
META = dict(role='reviewer',actor='ig2:002-IG-2B03-reviewer-b3172589:reviewer',task='IG-2B03',model='gpt-6.1-sol',reasoning='high',configuration_evidence=CONFIG.as_posix(),configuration_sha256=sha(CONFIG))
def save(name, data):
    p=OUT/name
    with p.open('x',encoding='utf-8',newline='\n') as f: json.dump({**META,**data},f,ensure_ascii=True,indent=2); f.write('\n')
def verify(records):
    errors=[]
    for r in records:
        p=pathlib.Path(r['path'])
        try:
            if sha(p)!=r['sha256'] or ('bytes' in r and (ROOT/p).stat().st_size != r['bytes']): errors.append(str(p))
        except OSError as e: errors.append(f'{p}: {e}')
    return dict(verified=len(records)-len(errors),total=len(records),errors=errors)

if __name__=='__main__':
    cfg=load(CONFIG)
    assert cfg['status']=='confirmed' and cfg['model']=='gpt-6.1-sol' and cfg['reasoning']=='high'
    packet=load(SESSION/'packet.json'); task=load(SESSION/'task.json')
    save('checkpoint.json',dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input_packet=dict(path=(SESSION/'packet.json').as_posix(),sha256=sha(SESSION/'packet.json')),completed_criteria=[],next_operation='Hash all exact frozen artifacts and compare accepted structural scope; independently inspect original pages 9-12 and complete ledgers.',product_writes=[]))
    scope=load(task['continuation_authorization']['scope']['path'])
    pins=load(scope['input_pins']['path'])
    ref=load(SESSION/'delivery-reference.json'); delivery=load(ref['evidence']); manifest=load(BASE/'delivery-manifest.json')
    dependency=load(SESSION/'references.json')['dependencies']['IG-2B02']; done=load(dependency['evidence'])
    preserve=load(scope['preserve_manifest']['path'])
    groups={
        'packet':packet['files']+packet['control_files'],
        'queue_pin':[dict(path='docs/work/queue.json',sha256=packet['queue_sha256'])],
        'continuation_pins':[task['continuation_authorization']['scope'],task['continuation_authorization']['evidence'],scope['assessment'],scope['preserve_manifest'],dict(path=scope['blocked_evidence'],sha256=scope['blocked_sha256'])],
        'original_input_pins':pins['files'],
        'delivery_reference':[dict(path=ref['evidence'],sha256=ref['sha256'])],
        'accepted_dependency_reference':[dict(path=dependency['evidence'],sha256=dependency['sha256'])],
        'accepted_dependency_artifacts':done['artifacts'],
        'blocked_preserved_artifacts':preserve['artifacts'],
        'delivery_artifacts':delivery['artifacts'],
        'manifest_artifacts':manifest['artifacts'],
    }
    results={k:verify(v) for k,v in groups.items()}
    assert delivery['artifacts'][:-1]==manifest['artifacts'], 'Manifest list must be exact delivery prefix'
    inventory=load(BASE/'final-verified/inventory.json'); baseline=load(scope['preservation']['baseline_inventory']['path'])
    registry=load(BASE/'final-verified/identity-registry.json'); old_registry=load(scope['preservation']['registry']['path'])
    pages={p['id']:p for p in inventory['pages']}; assigned={p['id'] for p in inventory['pages'] if p['pdf_page'] in [9,10,11,12]}
    regions={r['id']:r for r in inventory['regions']}
    evidence={e['id']:e for e in inventory['evidence']}
    old_regions={r['id']:r for r in baseline['regions']}
    comparisons={
        'unchanged_unassigned_pages':all(p==pages[p['id']] for p in baseline['pages'] if p['id'] not in assigned),
        'unchanged_unassigned_regions':all(r==regions[r['id']] for r in baseline['regions'] if r['page_id'] not in assigned),
        'prior_region_array_order': [r for r in baseline['regions'] if r['page_id'] not in assigned]==[r for r in inventory['regions'] if r['page_id'] not in assigned],
        'prior_evidence_records':all(e==evidence[e['id']] for e in baseline['evidence']),
        'prior_link_records':all(l in inventory['links'] for l in baseline['links']),
        'prior_nonassigned_reading_order':[i for i in baseline['reading_order'] if old_regions[i]['page_id'] not in assigned]==[i for i in inventory['reading_order'] if regions[i]['page_id'] not in assigned],
        'prior_registry_bindings':all(e in registry['entries'] for e in old_registry['entries']),
        'full_page_count':len(inventory['pages'])==44,
        'retired_placeholders_retained':all(any(e['id']==p['id'] for e in registry['entries']) for p in pins['replace_only_placeholders']),
    }
    authored=[BASE/x/'inventory.json' for x in ['authored','replay-a-authored','replay-b-authored']]
    regs=[BASE/x/'identity-registry.json' for x in ['authored','replay-a-authored','replay-b-authored']]
    comparisons['authored_replay_bytes_equal']=len({sha(x) for x in authored})==1
    comparisons['registry_replay_bytes_equal']=len({sha(x) for x in regs})==1
    ledger=load(BASE/'region-ledger.json')
    comparisons['complete_ledger_ids']=set(x['region']['id'] for x in ledger['regions'])=={r['id'] for r in inventory['regions'] if r['page_id'] in assigned}
    comparisons['complete_ledger_records']=all(x['region']==regions[x['region']['id']] and x['evidence']==evidence[x['evidence']['id']] for x in ledger['regions'])
    comparisons['ledger_order']=ledger['reading_order']==[i for i in inventory['reading_order'] if regions[i]['page_id'] in assigned]
    comparisons['criteria_exact']=delivery['criteria']==task['acceptance']
    save('hash-preservation-report.json',dict(groups=results,comparisons=comparisons,counts=dict(delivery_artifacts=len(delivery['artifacts']),assigned_regions=len(ledger['regions']),prior_pages=40,prior_regions=sum(r['page_id'] not in assigned for r in baseline['regions']),prior_evidence=len(baseline['evidence']),prior_links=len(baseline['links']),prior_registry=len(old_registry['entries'])),semantic_acceptance_granted=False))
    print(json.dumps(dict(hash_groups={k:dict(total=v['total'],errors=v['errors']) for k,v in results.items()},comparisons=comparisons),indent=2))
