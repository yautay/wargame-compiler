"""Independent structural/determinism oracles using invented records only."""
import copy
import hashlib
import json

import pytest

from wgc.contracts.source import ContractError, canonical_bytes, content_hash, seal_record, validate_bundle
from wgc.export.source import build, validate_export, PROFILE_VERSION
from wgc.export.storage import publish
from wgc.wgu_adapter.identity import locator
from tests.wgu_adapter.test_identity import corpus


def term_ids(result):
    return {o['value']['en']:e['id'] for e in result['registry']['entries'] if e['active'] and e['kind']=='term'
            for o in e['observations']}


def selected(result):
    b=result['bundle'];snapshot=next(r for r in b['records'] if r['id']==b['snapshot_id'])
    store={(r['id'],r['revision_id']):r for r in b['records']}
    return {s['id']:store[(s['id'],s['revision_id'])] for s in snapshot['data']['selected']}


def test_exact_repeated_and_independent_exports():
    imported=corpus({'terms':[{'en':'Alpha','definition':'Distinct alpha','extension':{'nested':[1,2]}}]})
    one=build(imported,namespace='synthetic')
    independent=build(imported,namespace='synthetic')
    again=build(imported,one['registry'],namespace='synthetic',previous_bundle=one['bundle'])
    for key in ('bundle','registry','references'):
        assert canonical_bytes(one[key])==canonical_bytes(independent[key])==canonical_bytes(again[key])
    assert one['bundle']['schema_version']==PROFILE_VERSION
    run=next(r for r in one['bundle']['records'] if r['record_type']=='run')
    assert run['data']['started_utc'] is None and run['data']['ended_utc'] is None
    assert one['validation']['semantic_acceptance_granted'] is False
    assert one['validation']['executable']['status']=='blocked'
    assert next(e for e in one['registry']['entries'] if e['kind']=='term')['observations'][0]['value']['extension']=={'nested':[1,2]}


def test_revision_supersession_and_reorder_identity():
    first=build(corpus({'terms':[{'en':'Alpha','definition':'Distinct alpha'},{'en':'Beta','definition':'Distinct beta'}]}),namespace='synthetic')
    original=term_ids(first)
    second=build(corpus({'terms':[{'en':'Bravo','definition':'Distinct beta'},{'en':'Alpha','definition':'Distinct alpha'}]},'kb/renamed.yaml'),
                 first['registry'],namespace='synthetic',previous_bundle=first['bundle'])
    assert term_ids(second)=={'Bravo':original['Beta'],'Alpha':original['Alpha']}
    current=selected(second)[original['Beta']];prior=selected(first)[original['Beta']]
    assert current['supersedes_refs']==[{'mode':'historical','id':prior['id'],'record_type':'node','revision_id':prior['revision_id']}]
    assert any(r['id']==prior['id'] and r['revision_id']==prior['revision_id'] for r in second['bundle']['records'])
    third=build(corpus({'terms':[{'en':'Bravo','definition':'Distinct beta'},{'en':'Alpha','definition':'Distinct alpha'}]},'kb/renamed.yaml'),
                second['registry'],namespace='synthetic',previous_bundle=second['bundle'])
    assert canonical_bytes(second['bundle'])==canonical_bytes(third['bundle'])


def test_exact_lineage_and_repeat_after_parent_retirement():
    first=build(corpus({'terms':[{'en':'Whole','definition':'whole'}]}),namespace='synthetic')
    parent=term_ids(first)['Whole']
    split_input=corpus({'terms':[{'en':'Left','definition':'left'},{'en':'Right','definition':'right'}]})
    lineage=[{'operation':'split','parents':[parent],
              'children':[locator('kb/terms.yaml','/terms/0'),locator('kb/terms.yaml','/terms/1')],
              'basis':'Explicit synthetic partition'}]
    split=build(split_input,first['registry'],namespace='synthetic',previous_bundle=first['bundle'],lineage=lineage)
    prior=selected(first)[parent]
    for identity in term_ids(split).values():
        assert selected(split)[identity]['lineage_refs']==[{'mode':'historical','id':parent,'record_type':'node','revision_id':prior['revision_id']}]
    repeated=build(split_input,split['registry'],namespace='synthetic',previous_bundle=split['bundle'])
    assert canonical_bytes(split['bundle'])==canonical_bytes(repeated['bundle'])


def test_cycles_navigation_and_unresolved_scopes_do_not_accept_semantics():
    imported=corpus({'rules':[{'id':'R-A','title':'Alpha','refs':['R-B.x'],'see':'R-B1a'},
                            {'id':'R-B','title':'Beta'}],
        'relations':[{'from':'R-A','to':'R-B','type':'requires','status':'verified'},
                     {'from':'R-B','to':'R-A','type':'requires','status':'verified'}]},'kb/extensions.yaml')
    result=build(imported,namespace='synthetic')
    assert len(result['references']['cycles'])==1
    assert {'unresolved_scope','unresolved_subpoint'}<=set(d['scope_status'] for d in result['references']['diagnostics'])
    assert all(r['data']['requirement']=='informational' for r in selected(result).values() if r['record_type']=='relation')
    assert all(r['record_type']!='review' for r in result['bundle']['records'])
    assert validate_export(result['bundle'])['semantic_acceptance_granted'] is False


def test_many_to_many_origin_field_bindings():
    first=build(corpus({'terms':[{'en':'Alpha','definition':'a'},{'en':'Beta','definition':'b'}]}),namespace='synthetic')
    identities=sorted(term_ids(first).values())
    current=corpus({'terms':[{'en':'Shared','definition':'raw contribution','unknown':{'deep':['kept']}}]})
    result=build(current,first['registry'],namespace='synthetic',previous_bundle=first['bundle'],hints={
        locator('kb/terms.yaml','/terms/0'):{'ids':identities,'basis':'Explicit synthetic many-to-many mapping'}})
    bindings=[r for r in selected(result).values() if r['record_type']=='origin_binding'
              and r['data']['field_locator']=='json-pointer:/terms/0/unknown']
    assert len(bindings)==1
    assert {r['id'] for r in bindings[0]['data']['ig_refs']}==set(identities)
    assert all('aspect_id' in ref for ref in bindings[0]['data']['ig_refs'])
    observations=[o for e in result['registry']['entries'] if e['active'] and e['kind']=='binding'
                  for o in e['observations'] if o['origin']['field_locator']=='/terms/0/unknown']
    assert observations and all(o['value']=={'deep':['kept']} for o in observations)
    for e in result['registry']['entries']:
        if e['id'] in identities:assert e['observations'][0]['value']['unknown']=={'deep':['kept']}


def test_registry_collision_remains_gap_and_preserves_observations():
    result=build(corpus({'terms':[{'en':'Duplicate'},{'en':'Duplicate'}]}),namespace='synthetic')
    gap=next(g for g in result['registry']['gaps'] if g['active'])
    assert len(gap['observations'])==2
    assert any(r['id']==gap['id'] and r['record_type']=='gap' for r in selected(result).values())
    bindings=[r for r in selected(result).values() if r['record_type']=='origin_binding' and r['data']['mapping_status']=='conflict']
    assert len(bindings)>=2


def test_corrupt_hash_and_dangling_active_endpoint_are_rejected():
    result=build(corpus({'rules':[{'id':'R-A','title':'Alpha'},{'id':'R-B','title':'Beta'}],
        'relations':[{'from':'R-A','to':'R-B','type':'see'}]},'kb/extensions.yaml'),namespace='synthetic')
    bad=copy.deepcopy(result['bundle']);bad['records'][0]['content_hash']='0'*64
    with pytest.raises(ContractError):validate_export(bad)
    bad=copy.deepcopy(result['bundle']);relation=next(r for r in bad['records'] if r['record_type']=='relation')
    relation['data']['target_ref']['id']='synthetic:missing'
    resealed=seal_record(relation);relation.update(resealed)
    snapshot=next(r for r in bad['records'] if r['id']==bad['snapshot_id'])
    for s in snapshot['data']['selected']:
        if s['id']==relation['id']:s.update({k:relation[k] for k in ('revision_id','content_hash')})
    snapshot.update(seal_record(snapshot))
    with pytest.raises(ContractError,match='dangling active'):validate_export(bad)


def test_package_bytes_and_operational_timestamps_separated(tmp_path):
    result=build(corpus({'terms':[{'en':'Alpha','definition':'a'}]}),namespace='synthetic')
    first=publish(result,tmp_path/'exports',operation_evidence={'model':None})
    second=publish(result,tmp_path/'exports',operation_evidence={'model':'observed elsewhere'})
    assert first['package']==second['package']
    assert first['manifest']==second['manifest']
    assert first['operation']!=second['operation']
    root=__import__('pathlib').Path(first['package'])
    for f in first['manifest']['files']:
        raw=(root/f['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==f['sha256']
    (root/'extra.txt').write_text('unlisted')
    with pytest.raises(ValueError):publish(result,tmp_path/'exports')


def test_unconstrained_confusable_title_and_wide_namespace_remain_valid():
    result=build(corpus({'terms':[],'confusables':[{'title':42},None,False]}),namespace='n'*50)
    assert validate_export(result['bundle'])['structural_validation']=='passed'


def test_unresolved_from_endpoint_does_not_create_resolved_relationship():
    result=build(corpus({'rules':[{'id':'R-B','title':'Beta'}],
        'relations':[{'from':'R-Missing.x','to':'R-B','type':'requires'}]},'kb/extensions.yaml'),namespace='synthetic')
    relation=next(r for r in selected(result).values() if r['record_type']=='relation')
    assert relation['data']['target_status']=='unresolved'
    assert relation['data']['target_ref'] is None


def test_unparsed_auxiliary_file_repeats_without_identity_gap():
    imported=corpus({'synthetic':'opaque bytes'},'kb/notes/synthetic.bin')
    first=build(imported,namespace='synthetic')
    repeated=build(imported,first['registry'],namespace='synthetic',previous_bundle=first['bundle'])
    for key in ('bundle','registry','references'):
        assert canonical_bytes(first[key])==canonical_bytes(repeated[key])
