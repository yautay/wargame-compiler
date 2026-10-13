"""One-run offline M-POC4B audit adapted from the active baseline audit. No inference, repairs or writes to inputs/eval/run.

Run from repository root. analysis.json is a working evaluation artifact; final
reports are materialized separately after reading and reviewing these results.
"""
import collections
import hashlib
import json
import re
import struct
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path.cwd()
P = ROOT / 'private/poc/spqr-chapter9'
OUT = P / 'measurement/M-POC4B-context-01'
T = P / 'transfer/context-v1'
RAW = P / 'runs/context-01/response.raw.txt'
raw = RAW.read_bytes()
text = raw.decode('utf-8')
def sha(b): return hashlib.sha256(b).hexdigest()
def read(rel): return json.loads((P / rel).read_bytes())
def descriptor(path):
    b = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(b), 'sha256': sha(b)}

# Recursive byte scanner, independent of pretty-printing or assumed line format.
# Each JSON value has an RFC6901 pointer and exact UTF-8 half-open byte range.
offsets = [0]
for c in text: offsets.append(offsets[-1] + len(c.encode('utf-8')))
spans = {}
duplicate_keys = []
decoder = json.JSONDecoder()
def token(s): return s.replace('~','~0').replace('/','~1')
def scan(i, ptr):
    while text[i].isspace(): i += 1
    start = i
    if text[i] == '{':
        i += 1; keys = set()
        while True:
            while text[i].isspace(): i += 1
            if text[i] == '}': i += 1; break
            key, end = decoder.raw_decode(text, i); i = end
            if key in keys: duplicate_keys.append({'pointer':ptr,'key':key})
            keys.add(key)
            while text[i].isspace(): i += 1
            assert text[i] == ':'; i = scan(i + 1, ptr + '/' + token(key))
            while text[i].isspace(): i += 1
            if text[i] == ',': i += 1
            else: assert text[i] == '}'
    elif text[i] == '[':
        i += 1; n = 0
        while True:
            while text[i].isspace(): i += 1
            if text[i] == ']': i += 1; break
            i = scan(i,ptr+'/'+str(n)); n += 1
            while text[i].isspace(): i += 1
            if text[i] == ',': i += 1
            else: assert text[i] == ']'
    else:
        _, i = decoder.raw_decode(text,i)
    b0,b1 = offsets[start], offsets[i]
    spans[ptr] = {'start_byte':b0,'end_byte_exclusive':b1,'sha256':sha(raw[b0:b1])}
    return i
end = scan(0,'')
assert not text[end:].strip()
proposal = json.loads(raw, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
for ptr,s in spans.items():
    assert json.loads(raw[s['start_byte']:s['end_byte_exclusive']]) is not None or raw[s['start_byte']:s['end_byte_exclusive']] == b'null'
assert sha(raw) == '95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b'
assert sha((P/'inputs/v1/manifest.json').read_bytes()) == '39e0a65e2f7d0d991c1bd031c6a99e6c40b80fe34e5429640e150fbfbedf340a'
manifest = read('inputs/v1/manifest.json')
scope = read('inputs/v1/scope.json')
helpers = read('inputs/v1/helper-regions.json')
eval_manifest = read('evaluation/eval-v1/manifest.json')
inventory = read('evaluation/eval-v1/inventory.json')
expectations = read('evaluation/eval-v1/expectations.json')
dependencies = read('evaluation/eval-v1/dependencies.json')
policy = read('evaluation/eval-v1/measurement-policy.json')

# Receipt owns the broader protected snapshot; this audit never rewrites it.

issues = []
checks = collections.Counter()
def issue(ptr, code, detail):
    issues.append({'pointer':ptr,'code':code,'detail':detail,'raw_span':spans.get(ptr)})
def require(obj, keys, ptr):
    for k in keys.split():
        checks['required_keys'] += 1
        if k not in obj: issue(ptr,'missing_key',k)
required = {
 'sources':'id sha256',
 'evidence':'id source_id source_sha256 pdf_page printed_page region_id kind quote image',
 'nodes':'id kind original_label scope_role content evidence_ids review_status',
 'rules':'id original_label scope_role clause_map transcription interpretation conditions action_effect exceptions parameters unit_types scope_limits time_limits evidence_ids gap_ids review_status',
 'dependencies':'id from to target_candidate kind explicitness rationale evidence_ids target_status impact_if_missing gap_ids review_status',
 'gaps':'id class affected_ids source_regions reason needed_context blocking evidence_ids',
}
require(proposal,'format_version run_id input_manifest_sha256 evaluation_id scope provenance sources evidence nodes rules dependencies gaps coverage','')
for k,expected in [('format_version','proposal-format-v1'),('run_id','context-01'),('input_manifest_sha256',sha((T/'context/pass-01/manifest.json').read_bytes())),('evaluation_id','eval-v1')]:
    checks['envelope_identity'] += 1
    if proposal[k] != expected: issue('/'+k,'wrong_envelope_identity',expected)
ids = {}; namespaces = {}; record_pointer = {}
for group in required:
    namespaces[group] = set()
    for n,obj in enumerate(proposal[group]):
        ptr = '/'+group+'/'+str(n); require(obj,required[group],ptr)
        id_ = obj['id']; namespaces[group].add(id_); record_pointer[id_] = ptr
        checks['record_ids'] += 1
        if id_ in ids: issue(ptr,'duplicate_id',id_)
        ids[id_] = (group,obj)
        if 'review_status' in obj and obj['review_status'] != 'unreviewed': issue(ptr,'review_status',obj['review_status'])
clause_ids = set()
for n,r in enumerate(proposal['rules']):
    if not r['clause_map']: issue('/rules/'+str(n),'empty_clause_map',r['id'])
    for m,c in enumerate(r['clause_map']):
        ptr = f'/rules/{n}/clause_map/{m}'
        require(c,'local_clause_id region_id evidence_ids original_label_text',ptr)
        checks['clause_ids'] += 1
        if c['local_clause_id'] in clause_ids or c['local_clause_id'] in ids: issue(ptr,'duplicate_clause_id',c['local_clause_id'])
        clause_ids.add(c['local_clause_id']); record_pointer[c['local_clause_id']] = ptr
regions = {r['region_id']:r for r in scope['regions']}
regions['pdf-27-context-8.46-step-4']={'region_id':'pdf-27-context-8.46-step-4','pdf_page':27,'printed_page':'unknown','scope_role':'boundary_context'}
references = []
ref_keys = {'evidence_ids':namespaces['evidence'],'gap_ids':namespaces['gaps'],
 'rule_ids':namespaces['rules'],'node_ids':namespaces['nodes'],
 'dependency_ids':namespaces['dependencies'],'clause_ids':clause_ids,
 'affected_ids':set(ids)|clause_ids, 'region_ids':set(regions),'source_regions':set(regions)}
def walk(o,ptr=''):
    if isinstance(o,dict):
        if 'state' in o:
            checks['field_objects'] += 1
            require(o,'state value evidence_ids reason gap_ids',ptr)
            state = o['state']
            if state not in {'known','established_absent','unknown','not_applicable'}: issue(ptr,'field_state',state)
            if state == 'unknown' and (o['value'] is not None or not o['reason'] or not o['gap_ids']): issue(ptr,'unknown_without_gap',o)
            if state == 'not_applicable' and (o['value'] is not None or not o['reason']): issue(ptr,'not_applicable_value_or_reason',o)
            if state == 'established_absent' and (o['value'] not in (None,[]) or not o['evidence_ids']): issue(ptr,'absence_without_evidence',o)
            # A quote's evidence is the containing source/image locator, not itself.
            if state == 'known' and not o['evidence_ids'] and not ptr.endswith('/quote'): issue(ptr,'known_without_evidence',o)
        for k,v in o.items():
            kp = ptr+'/'+token(k)
            if k in ref_keys:
                for j,ref in enumerate(v):
                    rp=kp+'/'+str(j); references.append({'pointer':rp,'target':ref,'namespace':k,'resolved':ref in ref_keys[k]})
                    checks['references'] += 1
                    if ref not in ref_keys[k]: issue(rp,'unresolved_reference',ref)
            if k in {'region_id','source_id'} and isinstance(v,str):
                allowed=set(regions) if k=='region_id' else namespaces['sources']
                checks['references'] += 1
                references.append({'pointer':kp,'target':v,'namespace':k,'resolved':v in allowed})
                if v not in allowed: issue(kp,'unresolved_reference',v)
            walk(v,kp)
    elif isinstance(o,list):
        for n,v in enumerate(o):walk(v,ptr+'/'+str(n))
walk(proposal)
enums = {'evidence':{'kind':{'text','table','diagram','mixed'}},
 'nodes':{'kind':{'table','diagram','definition','procedure','fragment','external_candidate','other'},'scope_role':{'core','boundary_context'}},
 'rules':{'scope_role':{'core'}},
 'dependencies':{'kind':{'procedure_use','table_use','definition','condition','modification','exception','continuation','mention'},'explicitness':{'explicit','implicit'},'target_status':{'internal','external_with_source','unresolved','unsupported'}},
 'gaps':{'class':{'unreadable','missing_context','ambiguous_source','unsupported_interpretation','unprocessed','other'}}}
for group,fields in enums.items():
    for n,obj in enumerate(proposal[group]):
        for key,values in fields.items():
            checks['enum_values'] += 1
            if obj[key] not in values: issue(f'/{group}/{n}/{key}','enum_value',obj[key])
edge_keys = collections.defaultdict(list)
for n,d in enumerate(proposal['dependencies']):
    ptr=f'/dependencies/{n}'
    for key in ['from','to']:
        ref=d[key]
        if ref is not None:
            checks['references']+=1
            valid=ref in namespaces['rules']|namespaces['nodes']
            references.append({'pointer':ptr+'/'+key,'target':ref,'namespace':'rule_or_node','resolved':valid})
            if not valid: issue(ptr+'/'+key,'unresolved_endpoint',ref)
    if d['to'] is None and (not d['target_candidate'] or not d['gap_ids']):issue(ptr,'null_target_without_candidate_gap',d['id'])
    if d['target_candidate'] is not None:require(d['target_candidate'],'original_reference description needed_context',ptr+'/target_candidate')
    if d['target_status'] in {'internal','external_with_source'} and d['to'] is None:issue(ptr,'resolved_status_null_target',d['id'])
    candidate=json.dumps(d['target_candidate'],sort_keys=True) if d['to'] is None else d['to']
    edge_keys[(d['from'],candidate,d['kind'])].append(d['id'])
for key,values in edge_keys.items():
    if len(values)>1: issue(record_pointer[values[0]],'duplicate_edge',values)

integrity=[]
transfer_manifest=json.loads((T/'context/pass-01/manifest.json').read_bytes())
for a in transfer_manifest['artifacts']:
    b=(T/a['path']).read_bytes()
    integrity.append({'path':a['path'],'bytes':len(b),'sha256':sha(b),'matches':len(b)==a['bytes'] and sha(b)==a['sha256']})
eval_integrity=[]
for a in eval_manifest['artifacts']:
    b=(ROOT/a['path']).read_bytes()
    eval_integrity.append({'path':a['path'],'bytes':len(b),'sha256':sha(b),'matches':len(b)==a['bytes'] and sha(b)==a['sha256']})
source_bindings=[]
artifacts={a['path']:a for a in transfer_manifest['artifacts']}
artifacts['inputs/v1/manifest.json']=descriptor(T/'inputs/v1/manifest.json')
artifacts['context/pass-01/manifest.json']=descriptor(T/'context/pass-01/manifest.json')
for n,s in enumerate(proposal['sources']):
    expected=artifacts.get(s.get('path',''))
    if s['id']==manifest['source_id']: expected={'sha256':manifest['source_sha256']}
    ok=expected is not None and s['sha256']==expected['sha256'] and ('bytes' not in s or s['bytes']==expected['bytes'])
    source_bindings.append({'id':s['id'],'matches':ok,'original_pdf_supplied_to_extractor':False if s['id']==manifest['source_id'] else 'not_applicable'})
    if not ok:issue(f'/sources/{n}','source_binding',s['id'])

def normalize(s):
    s=re.sub(r'[-\u00ad]\s*\n\s*(?=[A-Za-z])','',s)
    return re.sub(r'\s+',' ',s).strip()
helpermap={r['region_id']:r['text'] for r in helpers['regions']}
helpermap['pdf-27-context-8.46-step-4']=(T/'context/pass-01/evidence/8.46-step-4-helper.txt').read_text('utf-8')
quotes=[]; images=[]
for n,e in enumerate(proposal['evidence']):
    ptr=f'/evidence/{n}'; region=regions.get(e['region_id'])
    binding=e['source_id']==manifest['source_id'] and e['source_sha256']==manifest['source_sha256'] and region and e['pdf_page']==region['pdf_page'] and e['printed_page']==region['printed_page']
    checks['evidence_source_bindings']+=1
    if not binding:issue(ptr,'evidence_source_binding',e['id'])
    im=e['image']; imissues=[]
    if im is None:
        if e['kind'] in {'diagram','mixed','table'}:imissues.append('missing image')
    else:
        require(im,'path sha256 bbox coordinate_system',ptr+'/image')
        path=T/im['path']; b=path.read_bytes()
        assert b[:8]==b'\x89PNG\r\n\x1a\n'
        width,height=struct.unpack('>II',b[16:24])
        if sha(b)!=im['sha256'] or im['path'] not in artifacts or artifacts[im['path']]['sha256']!=im['sha256']:imissues.append('hash/path mismatch')
        is_context_crop=im['path']=='context/pass-01/evidence/8.46-step-4-pdf-27.png'
        if not is_context_crop and not im['path'].startswith('inputs/v1/pages/'):imissues.append('not full-page image')
        if not is_context_crop and im['path']!=f"inputs/v1/pages/pdf-{e['pdf_page']}.png":imissues.append('image page mismatch')
        if is_context_crop and (e['pdf_page']!=27 or im.get('pdf_bbox_points')!=[40,413,300,650]):imissues.append('crop source mapping')
        if im.get('width')!=width or im.get('height')!=height:imissues.append('dimensions mismatch')
        bbox=im['bbox']
        if len(bbox)!=4 or not all(isinstance(x,(int,float)) for x in bbox) or not (0<=bbox[0]<bbox[2]<=width and 0<=bbox[1]<bbox[3]<=height):imissues.append('invalid bbox')
        coord=im['coordinate_system'].lower()
        frame='crop-local' if is_context_crop else 'full-page'
        if not all(x in coord for x in [frame,'pixel','top-left','x right','y down']):imissues.append('coordinate system')
        images.append({'evidence_id':e['id'],'pointer':ptr+'/image','image_path':im['path'],'bbox':bbox,'actual_dimensions':[width,height],'status':'passed' if not imissues else 'failed','issues':imissues,'content_within_bbox':'not_assessable','raw_span':spans[ptr+'/image']})
    for detail in imissues:issue(ptr+'/image','image_locator',detail)
    q=e['quote']; val=q['value']
    if q['state']=='known' and isinstance(val,str):
        qn=normalize(val); hn=normalize(helpermap[e['region_id']]); matched=qn in hn
        quotes.append({'evidence_id':e['id'],'pointer':ptr+'/quote/value','quote':val,'helper_region':e['region_id'],'status':'normalized_helper_match' if matched else 'needs_visual_review','method':'case-sensitive whitespace joining and end-line word-split removal only; no punctuation/numeric repair','match_offset_in_normalized_helper':hn.find(qn) if matched else None,'raw_span':spans[ptr+'/quote/value'],'visual_status':'not_assessable'})
    else:quotes.append({'evidence_id':e['id'],'pointer':ptr+'/quote','status':'not_assessable','reason':'quote is not a known text string','raw_span':spans[ptr+'/quote']})
core=proposal['coverage']['core_regions']; core_order=[x['region_id'] for x in core]
if core_order!=scope['reading_order']:issue('/coverage/core_regions','coverage_order',core_order)
for n,c in enumerate(core):
    require(c,'region_id status rule_ids node_ids dependency_ids gap_ids notes',f'/coverage/core_regions/{n}')
    if c['status'] not in {'represented','partial','unprocessed'}:issue(f'/coverage/core_regions/{n}','coverage_status',c['status'])

# Reference inventory mapping is locational only, never semantic scoring.
manual={
 'H-9.0':['N90'],**{'H-9.'+str(i):['N9'+str(i)] for i in range(1,10)},
 'N-01':['N91hist'],'N-02':['N911design'],'N-03':['R913note'],'N-04':['N914design'],
 'N-05':['N917hist'],'N-06':['N919hist'],'N-07':['R92note','N92design'],'N-08':['N941design'],
 'N-09':['R95note','N95design'],'N-10':['N96hist'],'N-11':['R982note'],'N-12':['N99design'],
 'N-13':['N994design'],'N-14':['R996note','N996design'],
 'X-01':['N914diagram'],'X-02':['N923ex'],'X-03':['N924ex'],'X-04':['N932ex'],
 'X-05':['N941ex'],'X-06':['N953ex'],'X-07':['N967ex'],
 'T-01':['N914table'],'TR-01':['N914table'],'TR-02':['N914table'],'TR-03':['N914table'],
 'D-01':['N914diagram'],'D-02':['N966diagram'],'CAP-01':['N966diagram'],'CAP-02':['N966diagram'],
 'G-01':['N911counter'],'G-02':['N921counter'],'G-03':['N981counter'],'G-04':['N985markers'],'G-05':['N986marker'],
 'K-01':['N911first','N911next'],'K-02':['N914tablefirst','N914tablenext'],
 'K-03':['N914first','N914next'],'K-04':['N924first','N924next'],
 'K-05':['N966first','N966next'],'K-06':['N991first','N991next'],'K-07':['N996first','N996next']}
manual['C-9.7-01']=['R97intro']
inventory_by_id={i['id']:i for i in inventory['items']}
def mapped(i):
    id_=i['id']
    if id_ in manual:return manual[id_],'explicit source-object crosswalk'
    if i['type']=='rule_label':return [r['id'] for r in proposal['rules'] if r['original_label']['value']==i['original_label']],'exact printed label; split 9.96 counted once'
    if i['parent_id'] in inventory_by_id:
        parent,method=mapped(inventory_by_id[i['parent_id']])
        return parent,'parent source-object candidate; child content unassessed'
    return [],'no parent mapping'
inventory_results=[]
for n,i in enumerate(inventory['items']):
    mapped_ids,method=mapped(i)
    evidence_ids=sorted({e for id_ in mapped_ids for e in ids[id_][1].get('evidence_ids',[])})
    # Spatial check reports containing image overlap, not exact child transcription.
    intersections=[]
    for ev in i.get('evidence',[]):
        ib=ev.get('bbox_pdf_points')
        if not ib:continue
        pixel=[ib[0]*1700/612,ib[1]*2200/792,ib[2]*1700/612,ib[3]*2200/792]
        for eid in evidence_ids:
            e=ids[eid][1];im=e['image']
            if im and not im['path'].startswith('inputs/v1/pages/'):continue
            if im and e['pdf_page']==ev['pdf_page']:
                b=im['bbox']
                if min(b[2],pixel[2])>max(b[0],pixel[0]) and min(b[3],pixel[3])>max(b[1],pixel[1]):intersections.append(eid)
    inventory_results.append({'inventory_id':i['id'],'inventory_pointer':f'/items/{n}','type':i['type'],'parent_id':i['parent_id'],'output_ids':mapped_ids,'output_pointers':[record_pointer[x] for x in mapped_ids],'evidence_ids':evidence_ids,'spatial_overlap_evidence_ids':sorted(set(intersections)),'mapping_method':method,'structural_status':'located_candidate' if mapped_ids and intersections else 'unassessed_locator','assessment_status':'unassessed','semantic_status':'not_assessable','reason':'M-POC4B reference mapping only; exact child content and all scoped semantic components require M-POC5 human review','raw_spans':[spans[record_pointer[x]] for x in mapped_ids]})
assert len(inventory_results)==207

analysis={'run_id':'context-01','evaluation_id':'eval-v1','response':descriptor(RAW),
 'input_manifest':descriptor(T/'context/pass-01/manifest.json'),'evaluation_manifest':descriptor(P/'evaluation/eval-v1/manifest.json'),
 'counts':{k:len(proposal[k]) for k in required},'checks':dict(checks),
 'json_value_spans':spans,'record_pointers':record_pointer,'duplicate_json_keys':duplicate_keys,
 'issues':issues,'references':references,'input_integrity':integrity,'evaluation_integrity':eval_integrity,
 'source_bindings':source_bindings,'quotes':quotes,'images':images,'core_regions':core_order,
 'inventory_results':inventory_results,'inventory_type_counts':dict(collections.Counter(i['type'] for i in inventory_results)),
 'output_edge_counts':dict(collections.Counter(d['explicitness']+':'+('execution' if d['kind'] not in {'mention','continuation'} else d['kind']) for d in proposal['dependencies'])),
 'output_gap_counts':dict(collections.Counter(g['class'] for g in proposal['gaps'])),
 'frozen_denominators':{'content_groups':len([x for x in expectations['expectations'] if x['classification']=='confirmed_local_content_scope']),'context_groups':len([x for x in expectations['expectations'] if x['classification']=='requires_context']),'explicit_execution':len([x for x in dependencies['confirmed_execution_relations'] if x['explicitness']=='explicit']),'implicit_execution':len([x for x in dependencies['confirmed_execution_relations'] if x['explicitness']=='implicit']),'mentions':len(dependencies['mentions']),'continuations':len(dependencies['continuations']),'situations':policy['situations']['denominator'],'content_categories':{c['id']:len(c['units']) for c in policy['categories']}}}
(OUT/'analysis.json').write_text(json.dumps(analysis,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:analysis[k] for k in ['counts','checks','issues','output_edge_counts','output_gap_counts','frozen_denominators']},ensure_ascii=False,indent=2))
print('Quotes pending:',[(q['evidence_id'],q.get('quote')) for q in quotes if q['status']=='needs_visual_review'])
print('Inventory locators pending:',[(i['inventory_id'],i['output_ids']) for i in inventory_results if i['structural_status']!='located_candidate'])
