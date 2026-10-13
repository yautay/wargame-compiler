import json, hashlib, pathlib, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
M = P / 'measurement/M-POC5A-semantic-04d4'
R = P / 'reviews/semantic-01'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def ref(path):
    b = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def write(name, value):
    (M/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def pointer(obj, ptr):
    for part in ptr.strip('/').split('/'):
        part = part.replace('~1','/').replace('~0','~')
        obj = obj[int(part)] if isinstance(obj,list) else obj[part]
    return obj

def init():
    assert ROOT.as_posix() == 'C:/repo/wargame-compiler', ROOT
    expected = {
        'runs/first-001/first-001.json': (617941,'3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307'),
        'runs/context-01/response.raw.txt': (712014,'95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b'),
        'evaluation/eval-v1/manifest.json': (4116,'7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce'),
        'source/original-pdf-20261008-01.pdf': (3965827,'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'),
        'measurement/M-POC5A-semantic-04d1/scope-plan.json': (9721,'928dc497c018a6e9cdae75681a523f4d8d62e071ff657edfd876d20af7c16fe5')}
    verified=[]
    for name,(size,sha) in expected.items():
        entry=ref(P/name); assert (entry['bytes'],entry['sha256']) == (size,sha)
        verified.append(entry)
    write('preflight.json',dict(recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), verified=verified, all_match=True))
    old=[ref(f) for f in P.rglob('*') if f.is_file() and M not in f.parents and '_checks' not in f.parts]
    write('immutability-before.json',dict(files=old, sessions_prefix_only=True))
    part=read(P/'measurement/M-POC5A-semantic-04d1/scope-plan.json')['parts'][3]
    write('estimate.json',dict(card='M-POC5A.4d4', recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
          recorded_before_semantic_review=True, minutes_range=[75,90], limit_minutes=90,
          scope_plan=ref(P/'measurement/M-POC5A-semantic-04d1/scope-plan.json'), assignment_pointer='/parts/3',
          inventory_ids=part['inventory_ids'], positions=41, occurrences=82, per_answer={'first-001':41,'context-01':41},
          rationale='41 exact labels/clauses, three supplied graphics, two physical continuations; shared source passages with separate child and answer judgments. Full source/field review and verification fit one part.',
          active_time='unknown', model_configuration='unknown', token_cost_budget='unknown', further_split_required=False))
    print('Verified five anchors; pre-review estimate and immutable baseline saved.',len(old),'prior files.')

def inputs():
    paths={f['path'] for f in read(P/'measurement/M-POC5A-semantic-04d3/read-inputs.json')['files']}
    paths.update(['docs/work/tasks/semantic/M-POC5A.4d4.md','docs/handoff/2026-10-11-M-POC5A-owner13-handoff-01.md'])
    for name in ['current-state-27.json','owner-decision-03.json','owner-decision-07.json','owner-decision-10.json','owner-decision-13.json','owner-review-overlay-03.json','owner-review-overlay-13.json','owner-review-summary-03.md','owner-review-summary-07.md','owner-review-summary-10.md','owner-review-summary-13.md','review.md','issues.json']:
        paths.add((R/name).relative_to(ROOT).as_posix())
    for part in ['part-02','part-03','part-04a','part-04b1','part-04b2','part-04b3','part-04c1','part-04c2','part-04c3','part-04d1','part-04d2','part-04d3']:
        paths.update(f.relative_to(ROOT).as_posix() for f in (R/part).iterdir() if f.is_file())
    for name in ['reports/context-01/context-comparison.json','measurement/M-POC4B-context-01/report-reference-supplement.json',
                 'reviews/context-source-01/decision-01.json','reviews/context-source-01/review-closure-01.json']:
        paths.add((P/name).relative_to(ROOT).as_posix())
    records=[]
    for name in sorted(paths):
        f=ROOT/name; entry=ref(f)
        if f.suffix=='.json':
            data=read(f); entry['parsed_full_json']=True
            entry['top_level_keys']=list(data) if isinstance(data,dict) else ['list']
        else: f.read_text(encoding='utf-8-sig'); entry['read_full_text']=True
        records.append(entry)
    write('read-inputs.json',dict(files=records, method='Full bytes and full JSON parse; relevant source/output contents exposed separately for manual semantic review. This mechanical log is not semantic proof.'))
    print('Read and parsed',len(records),'required/history files.')

def manifests():
    inputs=read(M/'read-inputs.json')['files'];results=[];unavailable=[]
    cache={}
    def walk(obj,ptr=''):
        if isinstance(obj,dict):
            if 'path' in obj and 'sha256' in obj and isinstance(obj['path'],str):yield ptr,obj
            for k,v in obj.items():yield from walk(v,ptr+'/'+k)
        elif isinstance(obj,list):
            for i,v in enumerate(obj):yield from walk(v,ptr+'/'+str(i))
    for entry in inputs:
        f=ROOT/entry['path']
        if f.name not in ['manifest.json','closure.json','freeze-v1.json']:continue
        data=read(f)
        for ptr,item in walk(data):
            name=item['path'];target=ROOT/name
            if not name.startswith('private/'):
                base=P/'transfer/context-v1' if 'transfer/context-v1' in f.as_posix() else P
                target=base/name
            if not target.is_file():
                unavailable.append(dict(manifest=entry['path'],pointer=ptr,reference=item,reason='Historical/external path does not resolve locally; not asserted verified.'));continue
            key=target.as_posix()
            if key not in cache:cache[key]=ref(target)
            actual=cache[key];match=actual['sha256']==item['sha256'] and ('bytes' not in item or actual['bytes']==item['bytes'])
            results.append(dict(manifest=entry['path'],pointer=ptr,expected=item,actual=actual,match=match))
    write('manifest-verification.json',dict(verified_references=results,matched=sum(r['match'] for r in results),mismatches=[r for r in results if not r['match']],unavailable_historical_references=unavailable,hash_check_is_not_semantic_proof=True))
    print('Manifest refs',len(results),'matches',sum(r['match'] for r in results),'unavailable',len(unavailable))
    assert all(r['match'] for r in results)

def show(start,end):
    ids=read(M/'estimate.json')['inventory_ids']
    inv=read(P/'evaluation/eval-v1/inventory.json')['items']
    for num,id in enumerate(ids[start:end], start):
        item=next(i for i in inv if i['id']==id)
        print('\n',num,id,item['type'],'parent',item['parent_id'])
        if 'source_transcription' in item: print('CHILD',item['source_transcription'])
        for e in item['evidence']: print('SOURCE',json.dumps(e,ensure_ascii=False))
        extra={k:v for k,v in item.items() if k not in ['evidence','parent_record','candidate_review','observation_status','human_review','semantic_acceptance','review_issue_ids']}
        print('ITEM',json.dumps(extra,ensure_ascii=False))
        for run in ['first-001','context-01']:
            mapping=next(i for i in read(P/f'reports/{run}/inventory.json')['items'] if i['inventory_id']==id)
            prop=read(P/f'proposals/{run}/proposal.json')
            print('ANSWER',run,'MAP',mapping['output_pointers'],mapping['evidence_ids'])
            for ptr in mapping['output_pointers']:
                subset={'C-9.96-02':['/rules/46'],'C-9.96-03':['/rules/47'],'C-9.96-04':['/rules/48','/rules/49'],'C-9.96-05':['/rules/48'],'C-9.96-06':['/rules/48'],'C-9.96-07':['/rules/49']}
                if id in subset and ptr not in subset[id]:continue
                obj=pointer(prop,ptr)
                fields={k:({'state':v['state'],'value':v.get('value')} if isinstance(v,dict) and 'state' in v else v) for k,v in obj.items() if k not in ['clause_map','review_status','scope_role','evidence_ids']}
                if item['type']=='rule_label': fields={'id':obj['id'],'original_label':obj['original_label']}
                if fields.get('interpretation')==fields.get('action_effect'): fields['interpretation']='identical value/state to action_effect (read from original)'
                print(ptr,json.dumps(fields,ensure_ascii=False))

def visuals():
    from PIL import Image
    out=M/'visuals';out.mkdir(exist_ok=False)
    records=[]
    for run in ['first-001','context-01']:
        prop=read(P/f'proposals/{run}/proposal.json')
        for eid in ['E981counter','E985markers','E986marker','E995']:
            idx,e=next((i,e) for i,e in enumerate(prop['evidence']) if e['id']==eid)
            src=P/e['image']['path']; assert ref(src)['sha256']==e['image']['sha256']
            im=Image.open(src); assert im.size==(e['image']['width'],e['image']['height'])
            crop=im.crop(e['image']['bbox']);f=out/f'{run}-{eid}-exact.png';crop.save(f)
            if eid!='E995':
                fbig=out/f'{run}-{eid}-view.png';crop.resize((crop.width*4,crop.height*4)).save(fbig)
            else: fbig=f
            records.append(dict(run=run,evidence_id=eid,evidence_pointer=f'/evidence/{idx}',image=ref(src),bbox=e['image']['bbox'],exact_crop=ref(f),view=ref(fbig), enlargement_only=eid!='E995'))
    write('visuals.json',dict(crops=records,no_new_source=True,original_bbox_not_expanded=True))
    print('Eight exact supplied-image crops saved; six enlarged views, no extra source.')

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='init':init()
    elif mode=='inputs':inputs()
    elif mode=='show':show(int(sys.argv[2]),int(sys.argv[3]))
    elif mode=='visuals':visuals()
    elif mode=='manifests':manifests()
