"""Synthetic mutation oracles for the persisted identity contract."""
import copy
import hashlib
import json

import pytest

from wgc.contracts.source import canonical_bytes
from wgc.wgu_adapter.identity import empty_registry, locator, reconcile, validate_registry
from wgc.wgu_adapter.importer import finish, import_bytes


def corpus(data,path='kb/terms.yaml'):
    raw=json.dumps(data,ensure_ascii=False).encode('utf-8')
    f=import_bytes(raw,path);f.update(availability='available',role='kb',blob_path='files/'+path,edition_label=None)
    result=finish([f]);result['input_snapshot_id']='sha256:'+hashlib.sha256(raw).hexdigest()
    result['source_snapshot_id']='sha256:'+'0'*64
    return result


def ids(result,kind='term',key='en'):
    return {o['value'][key]:e['id'] for e in result['registry']['entries'] if e['active'] and e['kind']==kind
            for o in e['observations'] if isinstance(o['value'],dict)}


def test_reorder_insert_rename_delete_file_move():
    first=reconcile(corpus({'terms':[{'en':'Alpha','definition':'A uniquely identifies this concept'},
                                    {'en':'Beta','definition':'B uniquely identifies this concept'}]}),namespace='synthetic')
    original=ids(first)
    second=reconcile(corpus({'terms':[{'en':'Gamma','definition':'C uniquely identifies this concept'},
                                     {'en':'Beta','definition':'B uniquely identifies this concept'},
                                     {'en':'Alpha','definition':'A uniquely identifies this concept'}]},'kb/renamed.yaml'),
                     first['registry'],namespace='synthetic')
    assert ids(second)['Alpha']==original['Alpha'] and ids(second)['Beta']==original['Beta']
    assert ids(second)['Gamma'] not in set(original.values())
    third=reconcile(corpus({'terms':[{'en':'Bravo','definition':'B uniquely identifies this concept'},
                                    {'en':'Gamma','definition':'C uniquely identifies this concept'}]}),second['registry'],namespace='synthetic')
    assert ids(third)['Bravo']==original['Beta']
    retired=next(e for e in third['registry']['entries'] if e['id']==original['Alpha'])
    assert retired['active'] is False and retired['origin_history']
    assert all(e['origin_key'].startswith('allocation:') for e in third['registry']['entries'])
    assert all(e['id'].rsplit(':',1)[1].startswith('e') for e in third['registry']['entries'])


def test_identical_input_reuses_exact_registry():
    imported=corpus({'terms':[{'en':'Alpha','definition':'distinct A'},{'en':'Beta','definition':'distinct B'}]})
    one=reconcile(imported,namespace='synthetic')
    two=reconcile(imported,one['registry'],namespace='synthetic')
    assert canonical_bytes(one['registry'])==canonical_bytes(two['registry'])
    assert one['assignments']==two['assignments'] or all(a['ids']==b['ids'] for a,b in zip(one['assignments'],two['assignments']))
    independent=reconcile(imported,namespace='synthetic')
    assert canonical_bytes(one['registry'])==canonical_bytes(independent['registry'])


def test_duplicate_anonymous_and_ambiguous_rename_are_gaps():
    duplicate=corpus({'terms':[{'en':'Alpha'},{'en':'Alpha'}]})
    one=reconcile(duplicate,namespace='synthetic')
    assert not one['registry']['entries']
    assert len([g for g in one['registry']['gaps'] if g['active']])==1
    assert all(a['ids']==[] and a['gap_id'] for a in one['assignments'])
    two=reconcile(duplicate,one['registry'],namespace='synthetic')
    assert canonical_bytes(one['registry'])==canonical_bytes(two['registry'])
    original=reconcile(corpus({'terms':[{'en':'Alpha','definition':'same'},
                                       {'en':'Beta','definition':'same'}]}),namespace='synthetic')
    changed=reconcile(corpus({'terms':[{'en':'X','definition':'same'},{'en':'Y','definition':'same'}]}),
                      original['registry'],namespace='synthetic')
    gap=next(g for g in changed['registry']['gaps'] if g['active'])
    assert set(gap['candidate_ids'])==set(ids(original).values())
    assert not ids(changed)


def test_no_guess_for_label_only_rename():
    first=reconcile(corpus({'terms':[{'en':'Alpha'}]}),namespace='synthetic')
    changed=reconcile(corpus({'terms':[{'en':'Renamed'}]}),first['registry'],namespace='synthetic')
    assert changed['assignments'][0]['ids']==[]
    assert changed['registry']['gaps'][0]['candidate_ids']==[ids(first)['Alpha']]


def test_numbered_steps_follow_unique_body_after_insertion():
    old=corpus({'procedures':[{'id':'P-A','title':'Synthetic procedure','steps':[
        {'n':1,'text':'Alpha distinct body'},{'n':2,'text':'Beta distinct body'}]}]},'kb/procedures.yaml')
    one=reconcile(old,namespace='synthetic');prior=ids(one,'step','text')
    new=corpus({'procedures':[{'id':'P-A','title':'Synthetic procedure','steps':[
        {'n':1,'text':'New distinct body'},{'n':2,'text':'Alpha distinct body'},
        {'n':'3.a','text':'Beta distinct body'}]}]},'kb/procedures.yaml')
    two=reconcile(new,one['registry'],namespace='synthetic')
    assert ids(two,'step','text')['Alpha distinct body']==prior['Alpha distinct body']
    assert ids(two,'step','text')['Beta distinct body']==prior['Beta distinct body']


def test_relation_endpoint_alias_rename_keeps_identity():
    def data(a):return {'rules':[{'id':a,'title':'Alpha'},{'id':'R-B','title':'Beta'}],
        'relations':[{'from':a,'to':'R-B','type':'requires','note':'An unchanged candidate'}]}
    one=reconcile(corpus(data('R-A'),'kb/extensions.yaml'),namespace='synthetic')
    prior=next(e['id'] for e in one['registry']['entries'] if e['kind']=='relation')
    two=reconcile(corpus(data('R-AA'),'kb/extensions.yaml'),one['registry'],namespace='synthetic')
    assert next(e['id'] for e in two['registry']['entries'] if e['kind']=='relation' and e['active'])==prior


def test_explicit_split_merge_and_many_to_many_bindings():
    first=reconcile(corpus({'terms':[{'en':'Whole','definition':'one whole'}]}),namespace='synthetic')
    parent=ids(first)['Whole']
    split_input=corpus({'terms':[{'en':'Left','definition':'left part'},{'en':'Right','definition':'right part'}]})
    children=[locator('kb/terms.yaml','/terms/0'),locator('kb/terms.yaml','/terms/1')]
    split=reconcile(split_input,first['registry'],namespace='synthetic',lineage=[{
        'operation':'split','parents':[parent],'children':children,'basis':'Synthetic explicit partition decision'}])
    child_ids=set(ids(split).values());assert parent not in child_ids and len(child_ids)==2
    assert all(e['lineage_ids']==[parent] for e in split['registry']['entries'] if e['active'])
    merged_input=corpus({'terms':[{'en':'Merged','definition':'two combined parts'}]})
    merge=reconcile(merged_input,split['registry'],namespace='synthetic',lineage=[{
        'operation':'merge','parents':sorted(child_ids),'children':[locator('kb/terms.yaml','/terms/0')],
        'basis':'Synthetic explicit merge decision'}])
    merged=ids(merge)['Merged'];assert merged not in child_ids|{parent}
    mapped=reconcile(split_input,merge['registry'],namespace='synthetic',hints={
        loc:{'ids':[merged],'basis':'Synthetic many-to-one origin binding'} for loc in children})
    entry=next(e for e in mapped['registry']['entries'] if e['id']==merged)
    assert len(entry['observations'])==2
    both=reconcile(merged_input,split['registry'],namespace='synthetic',hints={
        locator('kb/terms.yaml','/terms/0'):{'ids':sorted(child_ids),'basis':'Synthetic one-to-many origin binding'}})
    assert set(both['assignments'][0]['ids'])==child_ids


def test_registry_and_binding_corruption_fail_without_mutating_previous():
    one=reconcile(corpus({'terms':[{'en':'Alpha'}]}),namespace='synthetic')
    baseline=copy.deepcopy(one['registry'])
    with pytest.raises(ValueError):reconcile(corpus({'terms':[{'en':'Alpha'}]}),baseline,namespace='synthetic',
        hints={locator('kb/terms.yaml','/terms/0'):{'ids':[ids(one)['Alpha']],'basis':''}})
    assert baseline==one['registry']
    bad=copy.deepcopy(baseline);bad['next_identity']=1
    with pytest.raises(ValueError):validate_registry(bad)


def test_split_decision_replay_is_idempotent_and_independent_of_input_order():
    first=reconcile(corpus({'terms':[{'en':'Whole','definition':'whole'}]}),namespace='synthetic')
    parent=ids(first)['Whole']
    data={'terms':[{'en':'Left','definition':'left'},{'en':'Right','definition':'right'}]}
    imported=corpus(data)
    op={'operation':'split','parents':[parent],
        'children':[locator('kb/terms.yaml','/terms/0'),locator('kb/terms.yaml','/terms/1')],
        'basis':'Synthetic replayable partition','decision_id':'synthetic-partition-1'}
    one=reconcile(imported,first['registry'],namespace='synthetic',lineage=[op])
    again=reconcile(imported,one['registry'],namespace='synthetic',lineage=[op])
    assert canonical_bytes(one['registry'])==canonical_bytes(again['registry'])
    reverse=corpus({'terms':list(reversed(data['terms']))})
    independently=reconcile(reverse,first['registry'],namespace='synthetic',lineage=[op])
    assert ids(one)==ids(independently)


def test_identical_split_children_need_explicit_persistent_keys():
    first=reconcile(corpus({'terms':[{'en':'Whole','definition':'whole'}]}),namespace='synthetic')
    parent=ids(first)['Whole'];imported=corpus({'terms':[{'en':'Same'},{'en':'Same'}]})
    children=[locator('kb/terms.yaml','/terms/0'),locator('kb/terms.yaml','/terms/1')]
    op={'operation':'split','parents':[parent],'children':children,'basis':'Explicit synthetic partition','decision_id':'partition'}
    pending=reconcile(imported,first['registry'],namespace='synthetic',lineage=[op])
    assert all(a['ids']==[] for a in pending['assignments'])
    assert sum(len(g['observations']) for g in pending['registry']['gaps'] if g['active'])==2
    keyed={**op,'child_keys':{children[0]:'left-branch',children[1]:'right-branch'}}
    assigned=reconcile(imported,first['registry'],namespace='synthetic',lineage=[keyed])
    assert len({a['ids'][0] for a in assigned['assignments']})==2
    again=reconcile(imported,assigned['registry'],namespace='synthetic',lineage=[keyed])
    assert canonical_bytes(assigned['registry'])==canonical_bytes(again['registry'])


def test_identical_error_gaps_preserve_every_origin():
    imported=corpus({'terms':[{'en':42},{'en':42}]})
    result=reconcile(imported,namespace='synthetic')
    assert all(a['ids']==[] for a in result['assignments'])
    assert sum(len(g['observations']) for g in result['registry']['gaps'] if g['active'])==2
    assert {o['origin']['field_locator'] for g in result['registry']['gaps'] for o in g['observations']}=={'/terms/0','/terms/1'}
