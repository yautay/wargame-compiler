"""Lossless structural WGU import; imported metadata grants no source meaning."""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from wgc.inputs.snapshot import open_read, verify_snapshot
from wgc.wgu_adapter.parser import ParseError, parse, pointer_part

COLLECTIONS = {'rules': 'rule', 'terms': 'term', 'procedures': 'procedure',
               'tables': 'table', 'relations': 'relation', 'ambiguities': 'ambiguity',
               'changes': 'change', 'scenarios': 'question', 'questions': 'question',
               'concepts': 'terminology', 'confusables': 'confusable'}
REQUIRED = {'rule': ('id','title'), 'term': ('en',), 'procedure': ('id','title'),
            'step': ('n','text'), 'table': ('id','title'),
            'relation': ('from','to','type'), 'ambiguity': ('id','title'),
            'change': ('id',), 'question': ('id','question'), 'terminology': ('id',)}
KNOWN = {
    'rule': 'id title section source when effect exceptions see keywords notes flags version digital refs extra body',
    'term': 'id en pl kind definition defined_at used_in refs',
    'procedure': 'id title steps subprocedures notes refs',
    'step': 'n text markers refs steps substeps',
    'table': 'id title tables notes refs data complete',
    'relation': 'id from to type when note status',
    'ambiguity': 'id title group scope quotes description readings recommendation strength resolution_source impact status resolution refs extra body',
    'change': 'id group from_version to_version kind place change effect rules refs source extra',
    'question': 'id question answer chain refs group given when then',
    'terminology': 'id source_term variants sense rules pl pl_forms rejected related status decided_by rationale evidence',
    'confusable': 'text', 'auxiliary': ''}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def import_bytes(raw, path):
    """Account one file including malformed input; raw bytes always survive."""
    f = {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
         'raw_base64': base64.b64encode(raw).decode('ascii'), 'document': None,
         'fields': [], 'records': [], 'diagnostics': []}
    locations = {}
    def diagnostic(code, message, field):
        loc = locations.get(field, {})
        d = {'code': code, 'message': message, 'file': path, 'field': field,
             'line': loc.get('line'), 'column': loc.get('column')}
        f['diagnostics'].append(d)
        return d
    def record(kind, value, field, parent=None, raw_only=False):
        errors = []
        if not raw_only:
            if not isinstance(value, dict):
                errors.append(diagnostic('malformed_record', 'record must be a mapping', field))
            else:
                for name in REQUIRED.get(kind, ()):
                    v = value.get(name)
                    if name == 'n':
                        valid = type(v) in (str, int) and str(v) != ''
                    else:
                        valid = isinstance(v, str) and bool(v)
                    if not valid:
                        errors.append(diagnostic('malformed_field', 'required field has invalid type/value: '+name, field+'/'+name))
                if 'id' in value and (not isinstance(value['id'], str) or not value['id']):
                    errors.append(diagnostic('malformed_id', 'id must be a nonempty string', field+'/id'))
                if 'refs' in value and (not isinstance(value['refs'], list) or any(not isinstance(x,str) for x in value['refs'])):
                    errors.append(diagnostic('malformed_refs', 'refs must be a string list', field+'/refs'))
        r = {'kind': kind, 'field': field, 'parent_field': parent, 'value': value,
             'status': 'error' if errors else 'raw' if raw_only else 'processed',
             'external_id': value.get('id') if not raw_only and isinstance(value,dict) and isinstance(value.get('id'),str) else None,
             'location': locations.get(field),
             'unknown_field_paths': [field+'/'+pointer_part(k) for k in value if k not in KNOWN.get(kind,'').split()] if isinstance(value,dict) else [],
             'mapping_status': 'unprocessed' if raw_only else 'evaluation_candidate' if kind=='question' else 'structural_candidate',
             'navigation': [{'field':field+'/'+k,'value':value[k],'role':'navigation'} for k in ('refs','see') if isinstance(value,dict) and k in value],
             'semantic_acceptance': 'not_granted', 'executable_readiness': 'not_granted'}
        f['records'].append(r)
        if isinstance(value,dict) and kind in ('procedure','step'):
            for key, child_kind in [('subprocedures','procedure'),('steps','step'),('substeps','step')]:
                if key not in value:
                    continue
                children = value[key]
                if not isinstance(children,list):
                    diagnostic('malformed_collection', key+' must be a list', field+'/'+key)
                    record('auxiliary',children,field+'/'+key,field,raw_only=True)
                    r['status']='error'
                else:
                    for i, child in enumerate(children):
                        record(child_kind,child,field+'/'+key+'/'+str(i),field)
        return r
    if Path(path).suffix.lower() not in ('.yaml','.yml'):
        record('auxiliary', None, '', raw_only=True)
        diagnostic('raw_auxiliary_file','Non-YAML file preserved byte for byte','')
    else:
        try:
            doc = parse(raw,path)
            f['document'], f['fields'] = doc.value, doc.fields
            locations.update({x['field']: x for x in doc.fields})
            if not isinstance(doc.value,dict):
                diagnostic('malformed_document','WGU document must be a mapping','')
                record('auxiliary',doc.value,'',raw_only=True)['status']='error'
            else:
                # Preserve file metadata and unrecognized extensions as raw records.
                expected = 'rules' if path.startswith('kb/rules/') else Path(path).stem
                recognized = False
                for key,value in doc.value.items():
                    field='/'+pointer_part(key)
                    if key in COLLECTIONS:
                        recognized=True
                        if not isinstance(value,list):
                            diagnostic('malformed_collection',key+' must be a list',field)
                            record('auxiliary',value,field,raw_only=True)['status']='error'
                        else:
                            for i,item in enumerate(value):
                                record(COLLECTIONS[key],item,field+'/'+str(i))
                    else:
                        record('auxiliary',value,field,raw_only=True)
                if expected in COLLECTIONS and expected not in doc.value:
                    # scenarios is the historical question collection; keep exact key contract.
                    diagnostic('missing_collection','Expected collection key is missing: '+expected,'')
                    record('auxiliary',None,'',raw_only=True)['status']='error'
                if not recognized and expected not in ('manifest','wgu','terminology'):
                    diagnostic('raw_unknown_file','Unknown YAML file retained with full field ledger','')
        except ParseError as error:
            f['diagnostics'].append(error.diagnostic)
            record('auxiliary',None,'',raw_only=True)['status']='error'
    return f


def finish(files):
    """Detect every duplicate ID without last-record-wins indexing."""
    ids = defaultdict(list)
    for f in files:
        for r in f.get('records',[]):
            if r['external_id'] is not None:
                ids[r['external_id']].append((f,r))
    duplicates=[]
    for identity,occurrences in sorted(ids.items()):
        if len(occurrences)<2:
            continue
        locations=[{'file':f['path'],'field':r['field'],'location':r['location']} for f,r in occurrences]
        duplicates.append({'external_id':identity,'occurrences':locations})
        for f,r in occurrences:
            r['status']='error'
            f['diagnostics'].append({'code':'duplicate_id','external_id':identity,'file':f['path'],
                                     'field':r['field'],'occurrences':locations})
    totals=Counter()
    kinds=Counter()
    for f in files:
        counts=Counter(r['status'] for r in f.get('records',[]))
        f['accounting']={k:counts[k] for k in ('processed','raw','error')}
        f['accounting']['total']=sum(counts.values())
        f['status']='missing' if f.get('availability')=='missing' else 'error' if counts['error'] else 'processed' if counts['processed'] else 'raw'
        totals.update(counts)
        kinds.update(r['kind'] for r in f.get('records',[]))
    return {'format':'wgc-wgu-import-1','adapter_version':'1','files':files,
            'record_counts':{k:totals[k] for k in ('processed','raw','error')},
            'record_total':sum(totals.values()), 'kind_counts':dict(sorted(kinds.items())),
            'file_counts':dict(sorted(Counter(f['status'] for f in files).items())),
            'duplicate_ids':duplicates,'semantic_acceptance':'not_granted',
            'publisher_source_coverage':'not_verified','executable_readiness':'not_granted'}


def import_snapshot(directory):
    directory=Path(directory)
    manifest=verify_snapshot(directory)
    if manifest['kind']!='input_snapshot':
        raise ValueError('expected complete WGU input snapshot')
    files=[]
    for item in manifest['files']:
        if item['availability']=='missing':
            files.append({**item,'records':[],'fields':[],'document':None,'raw_base64':None,
                          'diagnostics':[{'code':'missing_source','file':item['path']}]})
            continue
        with open_read(directory/item['blob_path']) as stream:
            raw=stream.read()
        if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
            raise ValueError('input changed after verification: '+item['path'])
        f=import_bytes(raw,item['path'])
        f.update(availability='available',role=item['role'],blob_path=item['blob_path'])
        files.append(f)
    # Reverify after complete import to detect mutation and tree additions.
    if verify_snapshot(directory)!=manifest:
        raise ValueError('snapshot changed during import')
    result=finish(files)
    result['input_snapshot_id']=manifest['snapshot_id']
    result['source_snapshot_id']=manifest['source_snapshot_id']
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('snapshot',type=Path);p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    result=import_snapshot(args.snapshot)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('xb') as stream:
        stream.write(canonical(result)+b'\n')
    print(json.dumps({k:result[k] for k in ['record_counts','record_total','kind_counts','file_counts']}))
    return 1 if result['record_counts']['error'] else 0


if __name__=='__main__':
    raise SystemExit(main())
