"""Synthetic strict controls for independent IG1D-R01 through IG1D-R04."""
import copy
import pytest

from wgc.contracts.source import canonical_bytes
from wgc.wgu_adapter.identity import reconcile,locator
from wgc.wgu_adapter.references import diagnose
from tests.wgu_adapter.test_identity import corpus,ids


def test_conflicting_term_evidence_retained_and_explicitly_resolvable():
    first=reconcile(corpus({'terms':[{'en':'Copper','definition':'Copper body'},
                                     {'en':'Silver','definition':'Silver body'}]}),namespace='synthetic')
    old=ids(first);current=corpus({'terms':[{'en':'Copper','definition':'Silver body'},
                                         {'en':'Silver','definition':'Copper body'}]})
    result=reconcile(current,first['registry'],namespace='synthetic')
    assert all(not a['ids'] and a['gap_id'] for a in result['assignments'])
    for gap in result['registry']['gaps']:
        if gap['active']:assert set(gap['candidate_ids'])==set(old.values())
    assert sum(len(g['observations']) for g in result['registry']['gaps'] if g['active'])==2
    hints={locator('kb/terms.yaml','/terms/'+str(i)):{'ids':[old[name]],'basis':'Synthetic explicit correction preserves the named identity'}
           for i,name in enumerate(['Copper','Silver'])}
    resolved=reconcile(current,first['registry'],namespace='synthetic',hints=hints)
    assert ids(resolved)==old
    assert all(e['observations'][0]['value']['definition']==('Silver body' if e['observations'][0]['value']['en']=='Copper' else 'Copper body')
               for e in resolved['registry']['entries'] if e['active'])


def test_conflicting_step_number_and_body_is_gap():
    first=reconcile(corpus({'procedures':[{'id':'P-A','title':'Procedure','steps':[
        {'n':1,'text':'Copper body'},{'n':2,'text':'Silver body'}]}]},'kb/procedures.yaml'),namespace='synthetic')
    current=corpus({'procedures':[{'id':'P-A','title':'Procedure','steps':[
        {'n':1,'text':'Silver body'},{'n':2,'text':'Copper body'}]}]},'kb/procedures.yaml')
    result=reconcile(current,first['registry'],namespace='synthetic')
    steps=[a for a in result['assignments'] if '/steps/' in a['locator']]
    assert len(steps)==2 and all(a['gap_id'] and not a['ids'] for a in steps)


@pytest.mark.parametrize('operation',['split','merge'])
def test_overlap_rejects_atomically(operation):
    first=reconcile(corpus({'terms':[{'en':'A','definition':'a'},{'en':'B','definition':'b'},
                                     {'en':'Other','definition':'other'}]}),namespace='synthetic');old=ids(first)
    if operation=='split':
        current=corpus({'terms':[{'en':'Left'},{'en':'Right'}]});parents=[old['A']]
        children=[locator('kb/terms.yaml','/terms/0'),locator('kb/terms.yaml','/terms/1')]
    else:
        current=corpus({'terms':[{'en':'Merged'}]});parents=[old['A'],old['B']]
        children=[locator('kb/terms.yaml','/terms/0')]
    previous=copy.deepcopy(first['registry'])
    with pytest.raises(ValueError,match='overlapping'):
        reconcile(current,previous,namespace='synthetic',lineage=[{'operation':operation,'parents':parents,
            'children':children,'basis':'Synthetic lineage decision'}],hints={children[0]:{
                'ids':[old['Other']],'basis':'Contradictory explicit existing identity'}})
    assert previous==first['registry']


def test_direct_ids_cycles_and_retired_targets():
    base=corpus({'rules':[{'id':'R-A','title':'A'},{'id':'R-B','title':'B'}]},'kb/extensions.yaml')
    first=reconcile(base,namespace='synthetic');old=ids(first,'rule','id')
    current=corpus({'rules':[{'id':'R-A','title':'A','refs':[old['R-B']]},
                            {'id':'R-B','title':'B','refs':[old['R-A']]}],
                    'relations':[{'from':old['R-A'],'to':old['R-B'],'type':'requires'}]},'kb/extensions.yaml')
    r=reconcile(current,first['registry'],namespace='synthetic');report=diagnose(r)
    assert all(d['target_status']=='resolved' for d in report['diagnostics'])
    assert len(report['cycles'])==1
    retired=reconcile(corpus({'rules':[{'id':'R-A','title':'A','refs':[old['R-B']]}]},'kb/extensions.yaml'),r['registry'],namespace='synthetic')
    assert diagnose(retired)['diagnostics'][0]['target_status']=='unresolved'


def test_active_id_alias_collision_is_not_guessed():
    first=reconcile(corpus({'terms':[{'en':'A','definition':'a'},{'en':'B','definition':'b'}]}),namespace='synthetic')
    a,b=sorted(e['id'] for e in first['registry']['entries'])
    second=copy.deepcopy(first);entry=next(e for e in second['registry']['entries'] if e['id']==b)
    entry['external_ids'].append(a)
    second['records'][0]['value']['refs']=[a]
    report=diagnose(second);d=next(d for d in report['diagnostics'] if d['raw_locator']==a)
    assert d['target_status']=='ambiguous' and set(d['candidate_ids'])=={a,b}


def test_unique_merge_receipt_retains_identity_through_correction_and_rename():
    first=reconcile(corpus({'terms':[{'en':'North','definition':'n'},{'en':'South','definition':'s'}]}),namespace='synthetic')
    parents=sorted(ids(first).values());child=locator('kb/terms.yaml','/terms/0')
    op={'operation':'merge','parents':parents,'children':[child],'basis':'Synthetic explicit merge','decision_id':'merge-1'}
    merged=reconcile(corpus({'terms':[{'en':'Together','definition':'original'}]}),first['registry'],namespace='synthetic',lineage=[op])
    identity=ids(merged)['Together'];origin_key=next(e['origin_key'] for e in merged['registry']['entries'] if e['id']==identity)
    corrected=reconcile(corpus({'terms':[{'en':'Renamed','definition':'corrected'}]}),merged['registry'],namespace='synthetic',lineage=[op])
    assert ids(corrected)=={'Renamed':identity}
    e=next(e for e in corrected['registry']['entries'] if e['id']==identity)
    assert e['origin_key']==origin_key and e['lineage_ids']==parents and len(e['origin_history'])==2
    repeated=reconcile(corpus({'terms':[{'en':'Renamed','definition':'corrected'}]}),corrected['registry'],namespace='synthetic',lineage=[op])
    assert canonical_bytes(corrected['registry'])==canonical_bytes(repeated['registry'])
    with pytest.raises(ValueError,match='collides'):
        reconcile(corpus({'terms':[{'en':'Renamed','definition':'corrected'}]}),corrected['registry'],namespace='synthetic',
                  lineage=[{**op,'basis':'A changed decision contract with the same receipt ID'}])
