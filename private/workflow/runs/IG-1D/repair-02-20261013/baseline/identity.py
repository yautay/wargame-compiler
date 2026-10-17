"""Persisted allocation identities, transparent rematches and explicit lineage.

IDs and origin keys come only from persisted counters. Content descriptors are
match evidence, never ID generators. File/array locators are provenance coordinates.
Indistinguishable observations and ambiguous rematches remain gaps until an explicit
binding/lineage decision supplies the missing identity information.
"""
from __future__ import annotations

from collections import defaultdict
import copy
import json
import re

from wgc.contracts.source import canonical_bytes

FORMAT = 'wgc-wgu-identity-1'


def locator(path, field):
    return canonical_bytes([path,field]).decode('utf-8')


def empty_registry(namespace):
    if not re.fullmatch(r'[a-z][a-z0-9_.-]*',namespace) or len(namespace)>50:
        raise ValueError('invalid identity namespace')
    return {'format':FORMAT,'namespace':namespace,'next_identity':1,'next_gap':1,
            'entries':[],'gaps':[]}


def validate_registry(registry):
    canonical_bytes(registry)
    if registry.get('format')!=FORMAT:
        raise ValueError('unsupported identity registry')
    empty_registry(registry['namespace'])
    identities=set();keys=set()
    for entry in registry['entries']:
        if entry['id'] in identities or entry['origin_key'] in keys:
            raise ValueError('duplicate persisted identity/origin key')
        identities.add(entry['id']);keys.add(entry['origin_key'])
        if not entry['id'].startswith(registry['namespace']+':e'):
            raise ValueError('identity outside registry namespace')
    gaps=set()
    for gap in registry['gaps']:
        if gap['id'] in identities|gaps:
            raise ValueError('duplicate registry gap identity')
        gaps.add(gap['id'])
    if (type(registry['next_identity']) is not int or registry['next_identity']<1
            or type(registry['next_gap']) is not int or registry['next_gap']<1):
        raise ValueError('invalid allocation counters')
    if any(int(i.rsplit(':e',1)[1])>=registry['next_identity'] for i in identities):
        raise ValueError('identity counter would reuse a prior identity')
    if any(int(i.rsplit(':g',1)[1])>=registry['next_gap'] for i in gaps):
        raise ValueError('gap counter would reuse a prior identity')


def input_records(imported):
    result=[]
    for f in imported['files']:
        for r in f.get('records',[]):
            origin={'input_snapshot_id':imported['input_snapshot_id'],
                    'input_sha256':f['sha256'],'relative_path':f['path'],
                    'field_locator':r['field']}
            result.append({'locator':locator(f['path'],r['field']),'kind':r['kind'],
                           'value':copy.deepcopy(r['value']),'external_id':r['external_id'],
                           'status':r['status'],'origin':origin,
                           'raw_file_sha256':f['sha256'] if r['kind']=='auxiliary' and r['value'] is None and r['field']=='' and r['status']=='raw' else None,
                           'parent_locator':locator(f['path'],r['parent_field']) if r['parent_field'] is not None else None})
    return result


def _value(record):
    value=record['value']
    if value is None and record.get('raw_file_sha256') is not None:
        return {'unparsed_file_sha256':record['raw_file_sha256']}
    if isinstance(value,dict):
        # A declared external-ID rename does not itself create a new logical entity.
        ignored={'id'}
        if record.get('kind')=='source':ignored.update({'path','blob_path'})
        return {k:v for k,v in value.items() if k not in ignored}
    return value


def _primary(kind,value):
    if not isinstance(value,dict):return None
    if kind=='term' and isinstance(value.get('en'),str):
        return [value['en'],value.get('kind')]
    if kind=='relation' and all(isinstance(value.get(k),str) for k in ('from','to','type')):
        return [value['from'],value['to'],value['type']]
    if kind=='step' and type(value.get('n')) in (str,int):return [value['n']]
    return None


def _rename_evidence(kind,value):
    if not isinstance(value,dict):return None
    ignored={'id','en','pl','pl_forms','title','source_term'}
    if kind=='step':ignored.add('n')
    result={k:v for k,v in value.items() if k not in ignored}
    # Bare category/numbering labels do not justify a guessed rename.
    substantive=set(result)-{'kind','n','refs','status'}
    if not substantive or not any(result[k] not in (None,'',[],{}) for k in substantive):return None
    return result


def reconcile(imported, previous=None, *, namespace='wgu.spqr', hints=None,
              lineage=None, extra_records=()):
    """Return new canonical registry and exact current observation assignments.

    hints[locator] = {ids: [...], basis: nonempty explanation} is an explicit
    many-to-many identity binding. Lineage operations declare parents and child
    locators plus a basis; children receive new allocations, never inherited approval.
    """
    registry=copy.deepcopy(previous) if previous is not None else empty_registry(namespace)
    validate_registry(registry)
    if registry['namespace']!=namespace:raise ValueError('registry namespace changed')
    records=input_records(imported)+copy.deepcopy(list(extra_records))
    by_loc={r['locator']:r for r in records}
    if len(by_loc)!=len(records):raise ValueError('duplicate current origin locator')
    old={e['id']:e for e in registry['entries']}
    old_values={i:copy.deepcopy(e['last_values']) for i,e in old.items()}
    old_raw_hashes={i:copy.deepcopy(e.get('raw_file_hashes',[])) for i,e in old.items()}
    old_scopes={i:copy.deepcopy(e['scope']) for i,e in old.items()}
    assignments={};used=set();reserved=set();forced={};ambiguous_candidates=set()
    hints=hints or {};lineage=lineage or []
    for op in lineage:
        parents,children=op['parents'],op['children']
        if (op.get('operation') not in ('split','merge') or not op.get('basis')
                or len(parents)!=len(set(parents)) or len(children)!=len(set(children))
                or not parents or not children or any(p not in old for p in parents)
                or any(c not in by_loc or c in forced for c in children)):
            raise ValueError('invalid or colliding explicit lineage decision')
        if op['operation']=='split' and (len(parents)!=1 or len(children)<2):
            raise ValueError('split needs one parent and multiple children')
        if op['operation']=='merge' and (len(parents)<2 or len(children)!=1):
            raise ValueError('merge needs multiple parents and one child')
        if reserved.intersection(parents):raise ValueError('parent used by multiple lineage decisions')
        reserved.update(parents)
        enriched=copy.deepcopy(op)
        enriched['key']=canonical_bytes([op.get('decision_id'),op['operation'],sorted(parents),op['basis']]).decode('utf-8')
        if op.get('decision_id') is not None:
            if not isinstance(op['decision_id'],str) or not op['decision_id']:
                raise ValueError('decision_id must be a nonempty persistent identifier')
            for entry in old.values():
                if entry.get('lineage_key'):
                    prior_receipt=json.loads(entry['lineage_key'])
                    if prior_receipt[0]==op['decision_id'] and entry['lineage_key']!=enriched['key']:
                        raise ValueError('persistent lineage decision_id collides with a changed contract')
        child_keys=op.get('child_keys',{})
        if child_keys and (set(child_keys)!=set(children) or len(set(child_keys.values()))!=len(children)
                           or any(not isinstance(v,str) or not v for v in child_keys.values())):
            raise ValueError('explicit persistent child keys must be distinct and cover every child')
        fingerprints=[canonical_bytes([by_loc[c]['kind'],_value(by_loc[c])]) for c in children]
        enriched['indistinguishable']=len(fingerprints)!=len(set(fingerprints)) and not child_keys
        for c in children:forced[c]=enriched
    for loc,hint in hints.items():
        ids=hint.get('ids',[])
        if loc in forced:
            raise ValueError('overlapping explicit lineage and binding decisions require a single resolved decision')
        if (loc not in by_loc or not hint.get('basis') or not ids or len(ids)!=len(set(ids))
                or any(i not in old or i in reserved for i in ids)
                or any(old[i]['kind']!=by_loc[loc]['kind'] for i in ids)):
            raise ValueError('invalid explicit identity binding')
    for e in registry['entries']:
        e['active']=False;e['observations']=[]
    for g in registry['gaps']:g['active']=False

    def observation(r):
        return {'origin':copy.deepcopy(r['origin']),'value':copy.deepcopy(r['value']),
                'external_id':r['external_id'],'status':r['status']}

    def assign(r,ids,basis):
        assignments[r['locator']]={'locator':r['locator'],'ids':sorted(ids),'gap_id':None,
                                   'basis':basis,'parent_locator':r['parent_locator']}
        for i in ids:
            e=old[i]
            e['scope']=sorted(set(e['scope']+r.get('scope',[]))) if e['observations'] else copy.deepcopy(r.get('scope',[]))
            e['active']=True;e['observations'].append(observation(r));used.add(i)
            if r['external_id'] is not None:e['external_ids']=sorted(set(e['external_ids']+[r['external_id']]))

    def allocate(r,scope,basis,parents=(),lineage_key=None,child_key=None):
        number=registry['next_identity'];registry['next_identity']+=1
        identity=namespace+':e'+str(number).zfill(7)
        e={'id':identity,'origin_key':'allocation:e'+str(number).zfill(7),
           'kind':r['kind'],'scope':scope,'external_ids':[],
           'last_values':[],'observations':[],'origin_history':[],
           'lineage_ids':sorted(parents),'lineage_basis':basis if parents else None,'active':False}
        if lineage_key is not None:e['lineage_key']=lineage_key;e['lineage_child_key']=child_key
        registry['entries'].append(e);old[identity]=e
        assign(r,[identity],basis)

    def gap(group,scope,candidates,reason):
        ambiguous_candidates.update(candidates)
        signature=canonical_bytes({'kind':group[0]['kind'],'scope':scope,
            'values':sorted([_value(r) for r in group],key=canonical_bytes),
            'candidates':sorted(candidates),'reason':reason}).decode('utf-8')
        existing=next((g for g in registry['gaps'] if g['match_evidence']==signature),None)
        if existing is None:
            number=registry['next_gap'];registry['next_gap']+=1
            existing={'id':namespace+':g'+str(number).zfill(7),
                      'origin_key':'allocation:g'+str(number).zfill(7),
                      'match_evidence':signature,'candidate_ids':sorted(candidates),
                      'reason':reason,'kind':group[0]['kind'],'observations':[],'active':True}
            registry['gaps'].append(existing)
        observations=existing['observations'] if existing['active'] else []
        observed={canonical_bytes(o):o for o in observations+[observation(r) for r in group]}
        existing['active']=True;existing['observations']=[observed[k] for k in sorted(observed)]
        for r in group:assignments[r['locator']]={'locator':r['locator'],'ids':[],
            'gap_id':existing['id'],'basis':reason,'parent_locator':r['parent_locator']}

    pending=list(records)
    while pending:
        ready=[r for r in pending if r['parent_locator'] is None or r['parent_locator'] in assignments]
        if not ready:
            for r in pending:gap([r],[],[],'Unresolved or cyclic editorial origin scope')
            break
        ready_ids={r['locator'] for r in ready};pending=[r for r in pending if r['locator'] not in ready_ids]
        ready.sort(key=lambda r:canonical_bytes([r['kind'],r['external_id'],_value(r),
            forced.get(r['locator'],{}).get('child_keys',{}).get(r['locator'])]))
        buckets=defaultdict(list)
        for r in ready:
            parent=assignments.get(r['parent_locator'])
            scope=parent['ids'] if parent else []
            r['scope']=scope
            if parent and not scope:
                gap([r],scope,[],'Parent identity unresolved; no child identity guessed');continue
            if r['locator'] in forced:
                op=forced[r['locator']];child_key=op.get('child_keys',{}).get(r['locator'])
                if op['indistinguishable']:
                    gap([r],scope,[],'Explicit lineage children need persistent keys to distinguish identical observations');continue
                children=[i for i,e in old.items() if e.get('lineage_key')==op['key'] and e['kind']==r['kind']
                          and old_scopes.get(i,e['scope'])==scope and i in old_values]
                matches=[i for i in children if (child_key is not None and old[i].get('lineage_child_key')==child_key)
                         or (child_key is None and any(_value({'value':v,'kind':r['kind']})==_value(r) for v in old_values.get(i,[])))]
                if (op['operation']=='merge' and len(op['children'])==1 and len(children)==1
                        and old[children[0]].get('lineage_child_key')==child_key):
                    matches=children
                if len(matches)==1:assign(r,matches,'Replay of persisted explicit lineage decision')
                elif children:gap([r],scope,children,'Explicit lineage replay needs an unambiguous child binding')
                else:allocate(r,scope,'Explicit '+op['operation']+': '+op['basis'],op['parents'],op['key'],child_key)
                continue
            if r['locator'] in hints:
                hint=hints[r['locator']];assign(r,hint['ids'],'Explicit binding: '+hint['basis']);continue
            if r['status']=='error':
                gap([r],scope,[],'Malformed import record retained without assigning an identity');continue
            buckets[(r['kind'],canonical_bytes(scope))].append(r)
        for (kind,scope_bytes),group in sorted(buckets.items(),key=lambda item:(item[0][0]=='relation',item[0])):
            scope=group[0]['scope']
            # Declared IDs first; a reused ID changing logical kind is a conflict.
            external=defaultdict(list)
            for r in group:
                if r['external_id'] is not None:external[r['external_id']].append(r)
            for ext,items in sorted(external.items()):
                matches=[i for i,e in old.items() if ext in e['external_ids'] and i not in reserved]
                if len(items)>1 or len(matches)>1 or any(old[i]['kind']!=kind for i in matches):
                    gap(items,scope,matches,'External-ID collision or changed logical kind');continue
                if len(matches)==1:assign(items[0],matches,'Persisted declared external identifier')
            available={i for i,e in old.items() if e['kind']==kind and old_scopes.get(i,e['scope'])==scope
                       and i not in used|reserved|ambiguous_candidates and i in old_values}
            def primary(r):
                value=r['value']
                if kind=='relation' and isinstance(value,dict):
                    value=copy.deepcopy(value)
                    for name in ('from','to'):
                        matches=[i for i,e in old.items() if value.get(name) in e['external_ids']]
                        if len(matches)==1:value[name]=matches[0]
                return _primary(kind,value)
            for evidence_fn,label in [(lambda r:_value({**r,'kind':kind}),'Unique unchanged value'),
                    (lambda r:_rename_evidence(kind,r['value']),'Unique unchanged substantive rename evidence'),
                    (primary,'Unique declared label/endpoint/number')]:
                if label=='Unique unchanged substantive rename evidence':
                    # Inspect every competing descriptor against the same remaining
                    # previous-state set before committing any heuristic rematch.
                    evidence_maps=[]
                    for fn in (primary,lambda r:_rename_evidence(kind,r['value'])):
                        mapping=defaultdict(set)
                        for i in available:
                            for value in old_values[i]:
                                ev=fn({'value':value})
                                if ev is not None:mapping[canonical_bytes(ev)].add(i)
                        evidence_maps.append(mapping)
                    conflicts=[]
                    for r in group:
                        if r['locator'] in assignments:continue
                        p=primary(r);b=_rename_evidence(kind,r['value'])
                        labels=evidence_maps[0].get(canonical_bytes(p),set()) if p is not None else set()
                        bodies=evidence_maps[1].get(canonical_bytes(b),set()) if b is not None else set()
                        if labels and bodies and labels!=bodies:
                            conflicts.append((r,labels|bodies))
                    for r,candidates in conflicts:
                        gap([r],scope,candidates,'Contradictory anonymous label/endpoint/number and substantive evidence')
                    available.difference_update(ambiguous_candidates)
                incoming=defaultdict(list);previous_values=defaultdict(set)
                for r in group:
                    if r['locator'] in assignments:continue
                    value=evidence_fn(r)
                    if value is not None or label=='Unique unchanged value':incoming[canonical_bytes(value)].append(r)
                for i in available:
                    for value in old_values[i]:
                        hashes=old_raw_hashes.get(i,[]) if value is None else []
                        evidence=[{'value':value,'raw_file_sha256':h} for h in hashes] or [{'value':value}]
                        for old_record in evidence:
                            v=evidence_fn(old_record)
                            if v is not None or label=='Unique unchanged value':previous_values[canonical_bytes(v)].add(i)
                for key,items in sorted(incoming.items()):
                    candidates=previous_values[key]&available
                    if len(items)==1 and len(candidates)==1:
                        identity=next(iter(candidates));assign(items[0],[identity],label);available.remove(identity)
                    elif candidates and (len(items)>1 or len(candidates)>1):
                        gap(items,scope,candidates,'Ambiguous '+label.lower())
                        available.difference_update(candidates)
            remaining=defaultdict(list)
            for r in group:
                if r['locator'] not in assignments:
                    remaining[canonical_bytes([r['external_id'],_value(r)])].append(r)
            for _,items in sorted(remaining.items()):
                if len(items)>1:
                    gap(items,scope,[],'Indistinguishable anonymous observations');continue
                r=items[0]
                if r['external_id'] is None and _rename_evidence(kind,r['value']) is None and available:
                    gap(items,scope,available,'Insufficient evidence to distinguish insertion from anonymous rename');continue
                allocate(r,scope,'New persisted allocation; no previous match')
    for e in registry['entries']:
        e['observations']=sorted(e['observations'],key=canonical_bytes)
        if e['observations']:
            unique={canonical_bytes(o['value']):o['value'] for o in e['observations']}
            e['last_values']=[unique[k] for k in sorted(unique)]
            if e['kind']=='auxiliary' and all(o['value'] is None and o['origin']['field_locator']=='' and o['status']=='raw' for o in e['observations']):
                e['raw_file_hashes']=sorted({o['origin']['input_sha256'] for o in e['observations']})
            origins={canonical_bytes(o):o for o in e['origin_history']}
            for o in e['observations']:origins[canonical_bytes(o['origin'])]=o['origin']
            e['origin_history']=[origins[k] for k in sorted(origins)]
    registry['entries'].sort(key=lambda e:e['id']);registry['gaps'].sort(key=lambda g:g['id'])
    validate_registry(registry)
    return {'registry':registry,'assignments':[assignments[k] for k in sorted(assignments)],
            'records':sorted(records,key=lambda r:r['locator'])}
