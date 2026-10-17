"""Deterministic structural source-IG projection with lossless identity payloads.

Raw WGU observations remain in the canonical identity registry and frozen input.
The graph exposes addressable aspects and dedicated mechanism descriptions with
explicit source-reconciliation gaps. It does not fabricate publisher evidence,
PDF pages, atomization, units, table axes or accepted expected outcomes.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from wgc.contracts.source import canonical_bytes, seal_record, validate_bundle
from wgc.wgu_adapter.identity import empty_registry, locator, reconcile, validate_registry
from wgc.wgu_adapter.references import diagnose

PROFILE_VERSION='wgc-source-export-1'
PROFILE_PATH=Path(__file__).with_name('source-export.schema.json')
PROFILE_SHA256='2a1f619eb4773d1432470cf0a340ac55c2f74451661c92002a6c89a7864bd768'
FACETS={'when':'condition','effect':'effect','exceptions':'exception','definition':'definition',
        'section':'scope','timing':'timing'}


def digest(value):return hashlib.sha256(canonical_bytes(value)).hexdigest()


def active(identity,kind,aspect=None):
    result={'mode':'active','id':identity,'record_type':kind}
    if aspect is not None:result['aspect_id']=aspect
    return result


def historical(record):
    return {'mode':'historical','id':record['id'],'record_type':record['record_type'],
            'revision_id':record['revision_id']}


def unknown(gap,reason='Publisher-source meaning is not reconciled; raw WGU value remains in the identity registry/input'):
    return {'knowledge':'unknown','representation':'literal','value':None,'reason':reason,
            'gap_refs':[active(gap,'gap')],'evidence_refs':[],'scope_refs':[]}


def aspect_id(key):return 'field-'+key.encode('utf-8').hex()


def source_records(imported, source_manifest=None, input_manifest_sha256=None, source_manifest_sha256=None):
    """Source file entries are declared external origins, not anonymous KB entities."""
    result=[]
    groups=[(imported['input_snapshot_id'],imported['files'],input_manifest_sha256)]
    if source_manifest is not None:
        groups.append((source_manifest['snapshot_id'],source_manifest['files'],source_manifest_sha256))
    for snapshot,files,manifest_hash in groups:
        metadata_rows=[{k:f.get(k) for k in ['path','blob_path','role','availability','bytes','sha256','edition_label']} for f in files]
        origin_snapshot=snapshot if manifest_hash is not None else 'wgc-metadata:'+digest({'files':metadata_rows})
        origin_hash=manifest_hash or digest({'files':metadata_rows})
        for index,f in enumerate(files):
            available=f.get('availability')=='available'
            path=f['path'];role=f.get('role','other')
            value=metadata_rows[index]
            origin={'input_snapshot_id':origin_snapshot,'input_sha256':origin_hash,
                    'relative_path':'manifest.json','field_locator':'/files/'+str(index)}
            # Scope ID distinguishes two declared registries with the same file name.
            external='source-file:'+('selected/' if snapshot!=imported['input_snapshot_id'] else 'input/')+path
            result.append({'locator':locator('@source/'+snapshot+'/'+path,''),'kind':'source',
                           'value':value,'external_id':external,'status':'raw','origin':origin,
                           'parent_locator':None})
    return result


def validate_export(bundle):
    if hashlib.sha256(PROFILE_PATH.read_bytes()).hexdigest()!=PROFILE_SHA256:
        raise ValueError('approved export profile changed')
    return validate_bundle(bundle,schema_path=PROFILE_PATH)


def build(imported, previous_registry=None, *, namespace='wgu.spqr', previous_bundle=None,
          source_manifest=None, input_manifest_sha256=None, source_manifest_sha256=None,
          hints=None, lineage=None, scope_resolutions=None):
    extras=source_records(imported,source_manifest,input_manifest_sha256,source_manifest_sha256)
    reconciled=reconcile(imported,previous_registry,namespace=namespace,hints=hints,
                         lineage=lineage,extra_records=extras)
    registry=reconciled['registry'];references=diagnose(reconciled,scope_resolutions=scope_resolutions)
    registry['input_context']={'input_snapshot_id':imported['input_snapshot_id'],
        'input_manifest_sha256':input_manifest_sha256,'source_manifest_sha256':source_manifest_sha256,
        'source_manifest':copy.deepcopy(source_manifest),'import_sha256':digest(imported),
        'schema_profile_sha256':PROFILE_SHA256}
    if input_manifest_sha256 is None:
        registry['input_context']['generated_input_metadata']={'files':[
            {k:f.get(k) for k in ['path','blob_path','role','availability','bytes','sha256','edition_label']} for f in imported['files']]}
    if source_manifest is not None and source_manifest_sha256 is None:
        registry['input_context']['generated_source_metadata']={'files':copy.deepcopy(source_manifest['files'])}
    assignments={a['locator']:a for a in reconciled['assignments']}
    entries={e['id']:e for e in registry['entries']}
    run_id=namespace+':run';meaning_gap=namespace+':source-reconciliation';profile_id=namespace+':profile'
    prior_records=copy.deepcopy(previous_bundle['records']) if previous_bundle else []
    prior_selected={}
    if previous_bundle:
        validate_export(previous_bundle)
        prior_snapshot=next(r for r in prior_records if r['id']==previous_bundle['snapshot_id'])
        prior_store={(r['id'],r['revision_id']):r for r in prior_records}
        prior_selected={e['id']:prior_store[(e['id'],e['revision_id'])] for e in prior_snapshot['data']['selected']}
    current={}
    def record(identity,kind,data,lineage_ids=()):
        old=prior_selected.get(identity)
        lineage_refs=[]
        if old and sorted(r['id'] for r in old['lineage_refs'])==sorted(lineage_ids):
            lineage_refs=copy.deepcopy(old['lineage_refs'])
        else:
            for parent in lineage_ids:
                if parent not in prior_selected:
                    raise ValueError('exact previous selected revision required for split/merge lineage: '+parent)
                lineage_refs.append(historical(prior_selected[parent]))
        envelope={'id':identity,'record_type':kind,'schema_version':PROFILE_VERSION,'run_id':run_id,
                  'supersedes_refs':copy.deepcopy(old['supersedes_refs']) if old else [],
                  'lineage_refs':lineage_refs or copy.deepcopy(old['lineage_refs']) if old else lineage_refs,
                  'data':data}
        candidate=seal_record(envelope)
        if old and candidate['content_hash']!=old['content_hash']:
            envelope['supersedes_refs']=[historical(old)];candidate=seal_record(envelope)
        current[identity]=candidate
        return candidate
    record(run_id,'run',{'context_manifest_sha256':digest(registry['input_context']),'raw_proposal_sha256':None,
        'model':None,'reasoning':None,'configuration_evidence':'Deterministic local transformation; actual executor/session evidence is in operational reports outside canonical hashes',
        'started_utc':None,'ended_utc':None,'measurements':{'wall_milliseconds':None,
        'input_tokens':None,'output_tokens':None,'unknown_reason':'Operational measurements are excluded from canonical product content'},
        'expectation_basis':'Structural input accounting and declared identity/reference contracts; no gameplay expected answers'})
    record(meaning_gap,'gap',{'kind':'unprocessed','reason':'Publisher sources, mixed editions, KB assertions and semantic composition require independent subsequent reconciliation',
        'affected_refs':[],'candidate_refs':[],'blocked_operations':['source_verification','semantic_acceptance','formalization','execution']})
    for gap in registry['gaps']:
        if gap['active']:
            record(gap['id'],'gap',{'kind':'ambiguity','reason':gap['reason'],'affected_refs':[],
                'candidate_refs':[],'blocked_operations':['source_verification','semantic_acceptance','formalization','execution']})
    source_ids=[]
    for e in registry['entries']:
        if not e['active'] or e['kind']!='source':continue
        value=e['observations'][0]['value'];missing=value['availability']!='available'
        gap_id=e['id']+'/availability'
        if missing:
            record(gap_id,'gap',{'kind':'missing_source','reason':'Configured source remains unavailable: '+value['path'],
                'affected_refs':[],'candidate_refs':[],'blocked_operations':['source_verification','semantic_acceptance','formalization','execution']})
        role='rulebook' if value['role']=='selected_rulebook' else 'other'
        record(e['id'],'source',{'role':role,'publisher':'unknown','system':namespace,
            'edition':value['edition_label'] or 'unknown/mixed-unverified','language':'unknown',
            'part':value['path'],'media_type':'application/pdf' if value['path'].endswith('.pdf') else 'application/octet-stream',
            'byte_count':value['bytes'],'sha256':value['sha256'],'availability':value['availability'],
            'compatibility':unknown(meaning_gap,'Edition compatibility and identity to missing WGU originals are unknown'),
            'gap_refs':[active(gap_id,'gap')] if missing else [active(meaning_gap,'gap')]})
        source_ids.append(e['id'])
    for e in registry['entries']:
        if not e['active'] or e['kind'] in ('source','derived_relation','binding'):continue
        observations=e['observations'];values=[o['value'] for o in observations]
        keys=sorted({key for value in values if isinstance(value,dict) for key in value})
        if not keys:keys=['raw']
        aspects=[{'aspect_id':aspect_id(key),'facet':FACETS.get(key,'transcription'),
            'statement':unknown(meaning_gap),'normative':True,'execution_impact':'blocking',
            'informational_review_ref':None} for key in keys]
        kind={'term':'concept','terminology':'concept','procedure':'procedure','step':'step','table':'table'}.get(e['kind'],'clause')
        if kind=='procedure':description={'kind':kind,**{k:unknown(meaning_gap) for k in
            ('actor','guard','inputs','outputs','branches','loops','termination','failure','reaction_windows')}}
        elif kind=='step':description={'kind':kind,**{k:unknown(meaning_gap) for k in
            ('actor','guard','ordered_writes','completion','failure')}}
        elif kind=='table':
            # No invented source axes/cells: the table facet retains the unresolved
            # axis inventory as an explicit placeholder with unknown declarations.
            description={'kind':'table','axes':[{'axis_id':'unreconciled','order':0,
                'unit':unknown(meaning_gap),'boundaries':unknown(meaning_gap)}],
                'cells':[],'notes':[],**{k:unknown(meaning_gap) for k in
                ('out_of_range','missing_cell','decorations','legend','participant_bindings')}}
        else:description={'kind':kind,'description':unknown(meaning_gap)}
        title=next((v[key] for v in values if isinstance(v,dict) for key in ('title','en','source_term')
                    if isinstance(v.get(key),str) and v[key]),None) or 'Imported '+e['kind']+' candidate'
        parents=e['scope']
        record(e['id'],'node',{'title':title,'editorial_parent_ref':active(parents[0],'node') if len(parents)==1 else None,
            'aspects':aspects,'semantic_groups':[],'description':description},e['lineage_ids'])
    derived_index={}
    for entry in registry['entries']:
        if entry['kind'] in ('binding','derived_relation'):
            for alias in entry['external_ids']:
                derived_index.setdefault((entry['kind'],alias),[]).append(entry)
    def derived(kind,key,observations):
        external='derived:'+canonical_bytes(key).decode('utf-8')
        matches=derived_index.get((kind,external),[])
        if len(matches)>1:raise ValueError('colliding persisted derived binding')
        if matches:e=matches[0]
        else:
            number=registry['next_identity'];registry['next_identity']+=1
            e={'id':namespace+':e'+str(number).zfill(7),'origin_key':'allocation:e'+str(number).zfill(7),
               'kind':kind,'scope':[],'external_ids':[external],'last_values':[],
               'observations':[],'origin_history':[],'lineage_ids':[],'lineage_basis':None,'active':True}
            registry['entries'].append(e);entries[e['id']]=e
            derived_index[(kind,external)]=[e]
        e['active']=True;e['observations']=sorted(observations,key=canonical_bytes)
        e['last_values']=[o['value'] for o in e['observations']]
        origins={canonical_bytes(o):o for o in e['origin_history']}
        for o in observations:origins[canonical_bytes(o['origin'])]=o['origin']
        e['origin_history']=[origins[k] for k in sorted(origins)]
        return e['id']
    diagnostic_by_origin={}
    for d in references['diagnostics']:
        key=locator(d['origin']['relative_path'],d['origin']['field_locator'])
        diagnostic_by_origin.setdefault(key,{})[d['field']]=d
    type_map={'see':'mention','exception-to':'exception','modifies':'modifies','precedes':'precedes','requires':'condition'}
    for r in reconciled['records']:
        if r['kind']!='relation':continue
        owner_ids=assignments[r['locator']]['ids'];value=r['value']
        if not owner_ids or not isinstance(value,dict):continue
        diag=diagnostic_by_origin.get(r['locator'],{})
        starts=diag.get('from',{}).get('target_ids',[]) or owner_ids
        targets=diag.get('to',{}).get('target_ids',[]) or [None]
        supported=value.get('type') in type_map
        for owner in owner_ids:
            for start in sorted(starts):
                for target in sorted(targets,key=lambda x:x or ''):
                    identity=derived('derived_relation',[owner,start,target,value.get('to')],
                        [{'origin':r['origin'],'value':value,'external_id':None,'status':r['status']}])
                    resolved=supported and target is not None and bool(diag.get('from',{}).get('target_ids'))
                    record(identity,'relation',{'relation_type':type_map.get(value.get('type'),'mention'),
                        'from_ref':active(start,current[start]['record_type']),
                        'target_status':'resolved' if resolved else 'unsupported' if not supported else 'unresolved',
                        'target_ref':active(target,current[target]['record_type']) if resolved else None,
                        'raw_locator':value.get('to') or '<empty target>','edition':'unknown/mixed-unverified',
                        'candidate_refs':[],'gap_refs':[active(meaning_gap,'gap')],
                        'applicability':unknown(meaning_gap),'evidence_refs':[],'requirement':'informational',
                        'requirement_group':{'group_id':'unaccepted-candidate','operator':'all'}})
    # Exact record and top-field bindings preserve arbitrary nested payloads in the
    # canonical registry; each subtree locator is a full input field binding.
    for r in reconciled['records']:
        assignment=assignments[r['locator']];ids=assignment['ids']
        targets=[active(i,current[i]['record_type']) for i in ids]
        if not targets:targets=[active(assignment['gap_id'],'gap')]
        fields=[('',targets,r['value'])]
        if isinstance(r['value'],dict):
            for key in sorted(r['value']):
                refs=[active(i,'node',aspect_id(key)) for i in ids if current[i]['record_type']=='node'] or targets
                fields.append(('/'+key.replace('~','~0').replace('/','~1'),refs,r['value'][key]))
        for suffix,refs,bound_value in fields:
            origin={**r['origin'],'field_locator':r['origin']['field_locator']+suffix}
            identity=derived('binding',[origin,refs],[{'origin':origin,'value':bound_value,
                'external_id':r['external_id'],'status':r['status']}])
            record(identity,'origin_binding',{**origin,'field_locator':'json-pointer:'+origin['field_locator'],
                'ig_refs':refs,'external_namespace':namespace,'external_id':r['external_id'],
                'mapping_status':'conflict' if assignment['gap_id'] else 'exact'})
    # Whole-file bindings cover collection/root containers. Their values are the
    # actual parsed document (or null for opaque bytes), never file metadata mislabeled
    # as a YAML field. File metadata above binds to the exact manifest entry.
    for f in imported['files']:
        if f['availability']!='available':continue
        source_locator=locator('@source/'+imported['input_snapshot_id']+'/'+f['path'],'')
        a=assignments[source_locator];targets=[active(i,'source') for i in a['ids']] or [active(a['gap_id'],'gap')]
        origin={'input_snapshot_id':imported['input_snapshot_id'],'input_sha256':f['sha256'],
                'relative_path':f['path'],'field_locator':''}
        identity=derived('binding',[origin,targets],[{'origin':origin,'value':f['document'],'external_id':None,'status':f['status']}])
        record(identity,'origin_binding',{**origin,'field_locator':'json-pointer:','ig_refs':targets,
            'external_namespace':namespace,'external_id':None,'mapping_status':'exact' if a['ids'] else 'conflict'})
    registry['entries'].sort(key=lambda e:e['id']);validate_registry(registry)
    identity_data=[]
    for e in registry['entries']:
        if e['active']:identity_data.append({'origin_key':e['origin_key'],'id':e['id'],'status':'assigned','candidate_ids':[],'gap_refs':[]})
    for g in registry['gaps']:
        if g['active']:identity_data.append({'origin_key':g['origin_key'],'id':g['id'],'status':'ambiguous',
            'candidate_ids':g['candidate_ids'],'gap_refs':[active(g['id'],'gap')]})
    record(namespace+':registry','identity_registry',{'entries':sorted(identity_data,key=lambda e:e['origin_key'])})
    record(profile_id,'profile',{'system':namespace,'edition':'mixed-unverified','rules_mode':'structural-unreconciled',
        'options':[],'scenario':unknown(meaning_gap,'Imported questions are evaluation candidates; battle scenario selection is unknown'),
        'map_refs':[],'counter_refs':[],'material_refs':[historical(current[i]) for i in sorted(source_ids)],
        'compatibility_decisions':[unknown(meaning_gap)]})
    selected=[{k:r[k] for k in ('id','record_type','revision_id','content_hash')} for r in sorted(current.values(),key=lambda r:r['id'])]
    snapshot_data={'state':'draft','selected':selected,'profile_ref':active(profile_id,'profile'),
        'conflict_refs':[active(g['id'],'gap') for g in registry['gaps'] if g['active']],
        'assessments':{'import':{'status':'complete','basis_refs':[active(run_id,'run')]},'coverage_refs':[],
        'semantic_review_refs':[],'executable':{'status':'blocked','scope_refs':[],
        'blocker_refs':[active(meaning_gap,'gap')],'reason':'Structural import only; source reconciliation, human acceptance and executable semantics remain outstanding'}}}
    snapshot_id='wgc-snapshot:'+digest(snapshot_data)
    record(snapshot_id,'snapshot',snapshot_data)
    store={(r['id'],r['revision_id']):r for r in prior_records}
    for r in current.values():store[(r['id'],r['revision_id'])]=r
    bundle={'schema_version':PROFILE_VERSION,'snapshot_id':snapshot_id,
            'records':sorted(store.values(),key=lambda r:(r['id'],r['revision_id']))}
    validation=validate_export(bundle)
    return {'bundle':bundle,'registry':registry,'references':references,'validation':validation,
            'assignments':reconciled['assignments']}
