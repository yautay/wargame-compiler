"""Lossless structural WGU import; imported metadata grants no source meaning."""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

from wgc.inputs.snapshot import open_read, verify_snapshot
from wgc.wgu_adapter.parser import ParseError, parse, pointer_part

COLLECTIONS = {'rules': 'rule', 'terms': 'term', 'procedures': 'procedure',
               'tables': 'table', 'relations': 'relation', 'ambiguities': 'ambiguity',
               'changes': 'change', 'scenarios': 'question', 'questions': 'question',
               'concepts': 'terminology', 'confusables': 'confusable'}
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

# Embedded structural contract from the operator-pinned read-only WGU schema.
# No neighboring repository or remote resource is read at import runtime.
WGU_SCHEMA_SHA256 = '0a93858ed3e0d99382ea962350e3b2994fab90b872a8b86584519b5a9e33a551'
WGU_SCHEMA = json.loads('{"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"https://github.com/yautay/wargame-utils/schemas/kb.schema.json","title":"wargame_utils knowledge base (wgu/kb@1)","description":"Contract between the analysis tool (wargame_utils) and digitization projects. Each $defs/*File entry describes one YAML file of kb/. Free text is Markdown in the KB language; field names are English.","$defs":{"id":{"type":"string","pattern":"^[A-Z][A-Za-z0-9]*(-[A-Za-z0-9.]+)*$"},"ids":{"type":"array","items":{"type":"string"}},"md":{"type":"string","description":"Markdown text"},"strength":{"enum":["certain","probable","speculative"]},"source":{"type":"object","properties":{"text":{"$ref":"#/$defs/md","description":"human-readable citation"},"pages":{"type":"string","description":"page(s) of the original rulebook"},"section":{"type":"string"},"document":{"type":"string","description":"path of the source document if not the current rules"},"translation":{"type":"array","items":{"type":"object","properties":{"file":{"type":"string"},"lines":{"type":"string"}},"required":["file"]}}}},"rule":{"type":"object","required":["id","title"],"properties":{"id":{"$ref":"#/$defs/id"},"title":{"type":"string"},"section":{"type":"string","description":"rule number in the rulebook"},"source":{"$ref":"#/$defs/source"},"when":{"$ref":"#/$defs/md","description":"conditions / trigger"},"effect":{"$ref":"#/$defs/md","description":"what happens (the FACT)"},"exceptions":{"$ref":"#/$defs/md"},"see":{"$ref":"#/$defs/md","description":"cross references"},"keywords":{"type":"array","items":{"type":"string"}},"notes":{"$ref":"#/$defs/md","description":"analyst notes; inferences marked [wniosek]/[inference]"},"flags":{"type":"array","items":{"enum":["changed","optional","title-specific","summary","inference","errata","removed"]}},"version":{"type":"object","properties":{"introduced":{"type":"string"},"changed_in":{"type":"string"}}},"digital":{"type":"object","description":"hints for digitization (filled by /wgu:digitalizacja)","properties":{"kind":{"enum":["definition","procedure-step","constraint","modifier","table-lookup","state-change","decision","reaction","random","hidden-info","victory","setup","presentation"]},"decision_by":{"type":"string"},"randomness":{"type":"string"},"state":{"type":"array","items":{"type":"string"}}}},"refs":{"$ref":"#/$defs/ids"},"extra":{"type":"object"},"body":{"$ref":"#/$defs/md"}}},"rulesFile":{"type":"object","required":["chapter","rules"],"properties":{"chapter":{"type":"object","required":["title"],"properties":{"id":{"type":"string"},"title":{"type":"string"}}},"rules":{"type":"array","items":{"$ref":"#/$defs/rule"}}}},"term":{"type":"object","required":["en"],"properties":{"id":{"$ref":"#/$defs/id"},"en":{"type":"string"},"pl":{"type":"string"},"kind":{"type":"string","description":"technical | descriptive"},"definition":{"$ref":"#/$defs/md"},"defined_at":{"type":"string"},"used_in":{"type":"string"},"refs":{"$ref":"#/$defs/ids"}}},"termsFile":{"type":"object","properties":{"terms":{"type":"array","items":{"$ref":"#/$defs/term"}},"confusables":{"type":"array"},"notes":{"$ref":"#/$defs/md"}}},"table":{"type":"object","required":["id","title"],"properties":{"id":{"$ref":"#/$defs/id"},"title":{"type":"string"},"tables":{"type":"array","items":{"type":"object","properties":{"columns":{"type":"array"},"rows":{"type":"array","items":{"type":"array"}}}}},"notes":{"$ref":"#/$defs/md"},"refs":{"$ref":"#/$defs/ids"},"data":{"description":"machine-readable form for engines (filled by /wgu:digitalizacja)"},"complete":{"type":"boolean","description":"false when values live outside the KB (e.g. a missing charts sheet)"}}},"tablesFile":{"type":"object","properties":{"tables":{"type":"array","items":{"$ref":"#/$defs/table"}}}},"step":{"type":"object","required":["n","text"],"properties":{"n":{"type":"string"},"text":{"$ref":"#/$defs/md"},"markers":{"type":"array","items":{"enum":["decision","reaction","roll","pitfall"]}},"refs":{"$ref":"#/$defs/ids"}}},"procedure":{"type":"object","required":["id","title"],"properties":{"id":{"$ref":"#/$defs/id"},"title":{"type":"string"},"steps":{"type":"array","items":{"$ref":"#/$defs/step"}},"subprocedures":{"type":"array","items":{"$ref":"#/$defs/procedure"}},"notes":{"$ref":"#/$defs/md"},"refs":{"$ref":"#/$defs/ids"}}},"proceduresFile":{"type":"object","properties":{"legend":{"$ref":"#/$defs/md"},"procedures":{"type":"array","items":{"$ref":"#/$defs/procedure"}}}},"relation":{"type":"object","required":["from","to","type"],"properties":{"from":{"type":"string"},"to":{"type":"string"},"type":{"enum":["overrides","exception-to","requires","modifies","precedes","replaces","see"]},"when":{"$ref":"#/$defs/md"},"note":{"$ref":"#/$defs/md"},"status":{"enum":["imported","verified","inferred"],"description":"imported = parsed automatically, needs analyst check"}}},"relationsFile":{"type":"object","properties":{"relations":{"type":"array","items":{"$ref":"#/$defs/relation"}}}},"ambiguity":{"type":"object","required":["id","title"],"properties":{"id":{"$ref":"#/$defs/id"},"title":{"type":"string"},"group":{"type":"string"},"scope":{"enum":["original","translation","errata","digital"]},"quotes":{"$ref":"#/$defs/md"},"description":{"$ref":"#/$defs/md"},"readings":{"$ref":"#/$defs/md"},"recommendation":{"$ref":"#/$defs/md"},"strength":{"$ref":"#/$defs/strength"},"resolution_source":{"$ref":"#/$defs/md"},"impact":{"$ref":"#/$defs/md"},"status":{"enum":["open","resolved","house-rule","wont-fix"]},"resolution":{"$ref":"#/$defs/md","description":"how/when resolved (errata, FAQ, owner decision)"},"refs":{"$ref":"#/$defs/ids"},"extra":{"type":"object"},"body":{"$ref":"#/$defs/md"}}},"ambiguitiesFile":{"type":"object","properties":{"ambiguities":{"type":"array","items":{"$ref":"#/$defs/ambiguity"}}}},"change":{"type":"object","required":["id"],"properties":{"id":{"$ref":"#/$defs/id"},"group":{"type":"string"},"from_version":{"type":"string"},"to_version":{"type":"string"},"kind":{"enum":["version","errata","faq","clarification","translation-fix","readability"]},"place":{"type":"string"},"change":{"$ref":"#/$defs/md"},"effect":{"$ref":"#/$defs/md"},"rules":{"type":"string"},"refs":{"$ref":"#/$defs/ids"},"source":{"$ref":"#/$defs/source"},"extra":{"type":"object"}}},"changesFile":{"type":"object","properties":{"changes":{"type":"array","items":{"$ref":"#/$defs/change"}},"notes":{"$ref":"#/$defs/md"}}},"scenario":{"type":"object","required":["id","question"],"properties":{"id":{"$ref":"#/$defs/id"},"question":{"$ref":"#/$defs/md"},"answer":{"$ref":"#/$defs/md"},"chain":{"$ref":"#/$defs/md"},"refs":{"$ref":"#/$defs/ids"},"group":{"type":"string"},"given":{"description":"structured initial state (digitization golden test)"},"when":{"description":"action/decisions/dice"},"then":{"description":"expected state/result"}}},"scenariosFile":{"type":"object","properties":{"scenarios":{"type":"array","items":{"$ref":"#/$defs/scenario"}}}},"node":{"type":"object","required":["id","shape","text"],"properties":{"id":{"type":"string"},"shape":{"type":"string","description":"start | end/koniec | decision/decyzja | action/akcja | note/notatka | data | table | exception"},"text":{"$ref":"#/$defs/md"},"rules":{"type":"string"},"refs":{"$ref":"#/$defs/ids"}}},"edge":{"type":"object","required":["from","to"],"properties":{"from":{"type":"string"},"to":{"type":"string"},"label":{"type":"string"}}},"aid":{"type":"object","required":["id","title"],"properties":{"id":{"type":"string","pattern":"^P\\\\d+"},"title":{"type":"string"},"header":{"type":"string"},"kind":{"type":"string"},"type":{"type":"string"},"format":{"type":"string"},"priority":{"type":"integer"},"complexity":{"type":"string"},"use_moment":{"$ref":"#/$defs/md"},"sources":{"$ref":"#/$defs/md"},"nodes":{"type":"array","items":{"$ref":"#/$defs/node"}},"edges":{"type":"array","items":{"$ref":"#/$defs/edge"}},"sections":{"type":"object","additionalProperties":{"type":"string"}},"acceptance":{"type":"array","items":{"type":"string"}},"status":{"enum":["spec","in-progress","done","issues"]},"refs":{"$ref":"#/$defs/ids"}}},"manifest":{"type":"object","required":["schema","game"],"properties":{"schema":{"const":"wgu/kb@1"},"game":{"type":"object"},"sources":{"type":"array"},"language":{"type":"object"},"interpretation_protocol":{"$ref":"#/$defs/md"},"warnings":{"$ref":"#/$defs/md"},"analysis":{"$ref":"#/$defs/md"},"legacy_conventions":{"type":"object"},"history":{"type":"array"}}}}}')
DEFINITIONS = {'question': 'scenario', **{k: k for k in
    ('rule','term','procedure','step','table','relation','ambiguity','change')}}
STRUCTURAL_EXTENSIONS = {'step.n': 'Integer or string local numbering is preserved; bool is invalid.'}
FILE_DEFINITIONS = {'rules': 'rulesFile', 'terms': 'termsFile', 'tables': 'tablesFile',
                    'procedures': 'proceduresFile', 'relations': 'relationsFile',
                    'ambiguities': 'ambiguitiesFile', 'changes': 'changesFile',
                    'scenarios': 'scenariosFile', 'manifest': 'manifest'}


def schema_errors(value, shape, pointer):
    """Check the pinned schema's structural vocabulary; unknown fields survive."""
    if '$ref' in shape:
        name = shape['$ref'].removeprefix('#/$defs/')
        return schema_errors(value, WGU_SCHEMA['$defs'][name], pointer)
    errors = []
    kinds = {'object': isinstance(value, dict), 'array': isinstance(value, list),
             'string': isinstance(value, str), 'integer': type(value) is int,
             'boolean': type(value) is bool, 'null': value is None}
    expected = shape.get('type')
    integer_numbering = (shape is WGU_SCHEMA['$defs']['step']['properties']['n']
                         and type(value) is int)
    if expected and not kinds.get(expected, False) and not integer_numbering:
        return [(pointer, 'expected '+expected)]
    if 'enum' in shape and value not in shape['enum']:
        errors.append((pointer, 'value is outside the declared enum'))
    if 'const' in shape and value != shape['const']:
        errors.append((pointer, 'value differs from the declared constant'))
    if isinstance(value, str) and 'pattern' in shape and not re.search(shape['pattern'], value):
        errors.append((pointer, 'value does not match the declared identifier pattern'))
    if isinstance(value, dict):
        for key in shape.get('required', []):
            if key not in value:
                errors.append((pointer+'/'+pointer_part(key), 'required field is missing'))
        for key, child in value.items():
            if key in shape.get('properties', {}):
                errors.extend(schema_errors(child,shape['properties'][key],pointer+'/'+pointer_part(key)))
            elif isinstance(shape.get('additionalProperties'), dict):
                errors.extend(schema_errors(child,shape['additionalProperties'],pointer+'/'+pointer_part(key)))
    elif isinstance(value, list) and 'items' in shape:
        for i, child in enumerate(value):
            errors.extend(schema_errors(child,shape['items'],pointer+'/'+str(i)))
    return errors


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
        parent = field
        while parent not in locations and parent:
            parent = parent.rsplit('/',1)[0]
        loc = locations.get(parent, {})
        d = {'code': code, 'message': message, 'file': path, 'field': field,
             'line': loc.get('line'), 'column': loc.get('column')}
        f['diagnostics'].append(d)
        return d
    def record(kind, value, field, parent=None, raw_only=False):
        errors = []
        if not raw_only and kind != 'confusable':
            if not isinstance(value, dict):
                errors.append(diagnostic('malformed_record', 'record must be a mapping', field))
            else:
                definition = DEFINITIONS.get(kind)
                if definition:
                    for pointer, message in schema_errors(value,WGU_SCHEMA['$defs'][definition],field):
                        errors.append(diagnostic('malformed_field', message, pointer))
                elif kind == 'terminology' and (not isinstance(value.get('id'),str) or not value['id']):
                    errors.append(diagnostic('malformed_id','terminology extension requires a nonempty string id',field+'/id'))
                if not definition and 'id' in value and (not isinstance(value['id'], str) or not value['id']):
                    errors.append(diagnostic('malformed_id', 'id must be a nonempty string', field+'/id'))
        r = {'kind': kind, 'field': field, 'parent_field': parent, 'value': value,
             'status': 'error' if errors else 'raw' if raw_only else 'processed',
             'external_id': value.get('id') if not raw_only and kind != 'confusable' and isinstance(value,dict) and isinstance(value.get('id'),str) else None,
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
                file_shape = WGU_SCHEMA['$defs'].get(FILE_DEFINITIONS.get(expected,''),{})
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
                        metadata = record('auxiliary',value,field,raw_only=True)
                        if key in file_shape.get('properties', {}):
                            structural = schema_errors(value,file_shape['properties'][key],field)
                            for pointer,message in structural:
                                diagnostic('malformed_field',message,pointer)
                            if structural:
                                metadata['status']='error'
                for key in file_shape.get('required', []):
                    if key not in doc.value and key not in COLLECTIONS:
                        field='/'+pointer_part(key)
                        diagnostic('missing_field','Required file metadata is missing: '+key,field)
                        record('auxiliary',None,field,raw_only=True)['status']='error'
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
            'structural_schema_sha256':WGU_SCHEMA_SHA256,'structural_extensions':STRUCTURAL_EXTENSIONS,
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
