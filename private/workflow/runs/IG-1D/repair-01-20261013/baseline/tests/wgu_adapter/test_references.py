"""Synthetic exact scopes and cyclic graph oracles; no gameplay expected results."""
import pytest

from wgc.wgu_adapter.identity import reconcile
from wgc.wgu_adapter.references import diagnose, _cycles
from tests.wgu_adapter.test_identity import corpus, ids


def test_navigation_scope_subpoints_and_exact_explicit_resolution():
    data={'rules':[{'id':'R-A','title':'Alpha','refs':['R-B','R-B.x','R-B1a','R-Missing'],
                    'see':'R-B and R-Missing'},{'id':'R-B','title':'Beta'}]}
    r=reconcile(corpus(data,'kb/extensions.yaml'),namespace='synthetic')
    report=diagnose(r);by_raw={d['raw_locator']:d for d in report['diagnostics']}
    assert by_raw['R-B']['target_status']=='resolved'
    assert by_raw['R-B.x']['scope_status']=='unresolved_scope'
    assert by_raw['R-B1a']['scope_status']=='unresolved_subpoint'
    assert by_raw['R-B and R-Missing']['target_status']=='unresolved'
    assert all(d['role']=='navigation' and d['semantic_acceptance']=='not_granted' for d in report['diagnostics'])
    explicit=diagnose(r,scope_resolutions={'R-B.x':{'targets':['R-B'],'basis':'Synthetic exact scope declaration'}})
    assert next(d for d in explicit['diagnostics'] if d['raw_locator']=='R-B.x')['scope_status']=='explicit_exact_set'
    with pytest.raises(ValueError):diagnose(r,scope_resolutions={'R-B.x':{'targets':['R-Missing'],'basis':'invalid'}})
    with pytest.raises(ValueError):diagnose(r,scope_resolutions={'R-B.x':{'targets':['R-B'],'basis':''}})


def test_rule_cycles_are_diagnostics():
    r=reconcile(corpus({'rules':[{'id':'R-A','title':'Alpha'},{'id':'R-B','title':'Beta'}],
        'relations':[{'from':'R-A','to':'R-B','type':'requires'},
                     {'from':'R-B','to':'R-A','type':'requires'}]},'kb/extensions.yaml'),namespace='synthetic')
    report=diagnose(r)
    assert len(report['cycles'])==1 and len(report['cycles'][0])==2
    assert report['cycles_are_allowed'] is True


def test_large_cycle_has_no_recursive_dag_limit():
    edges=[(str(i),str(i+1)) for i in range(2000)]+[('2000','0')]
    assert len(_cycles(edges)[0])==2001
