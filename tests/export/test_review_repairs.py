"""Synthetic export closure after direct-reference/merge correction repairs."""
from wgc.export.source import build,validate_export
from wgc.wgu_adapter.identity import locator
from tests.wgu_adapter.test_identity import corpus
from tests.export.test_source import term_ids,selected


def test_merge_correction_keeps_history_and_parent_revisions():
    first=build(corpus({'terms':[{'en':'North','definition':'n'},{'en':'South','definition':'s'}]}),namespace='synthetic')
    parents=sorted(term_ids(first).values());op={'operation':'merge','parents':parents,
        'children':[locator('kb/terms.yaml','/terms/0')],'basis':'Synthetic explicit merge','decision_id':'merge-1'}
    merged=build(corpus({'terms':[{'en':'Together','definition':'original'}]}),first['registry'],namespace='synthetic',previous_bundle=first['bundle'],lineage=[op])
    identity=term_ids(merged)['Together'];old=selected(merged)[identity]
    corrected=build(corpus({'terms':[{'en':'Renamed','definition':'corrected'}]}),merged['registry'],namespace='synthetic',previous_bundle=merged['bundle'],lineage=[op])
    current=selected(corrected)[identity]
    assert current['lineage_refs']==old['lineage_refs']
    assert current['supersedes_refs'][0]['revision_id']==old['revision_id']
    assert validate_export(corrected['bundle'])['semantic_acceptance_granted'] is False


def test_direct_candidate_endpoints_resolve_without_semantic_approval():
    first=build(corpus({'rules':[{'id':'R-A','title':'A'},{'id':'R-B','title':'B'}]},'kb/extensions.yaml'),namespace='synthetic')
    aliases={alias:e['id'] for e in first['registry']['entries'] if e['active'] and e['kind']=='rule' for alias in e['external_ids']}
    updated=build(corpus({'rules':[{'id':'R-A','title':'A'},{'id':'R-B','title':'B'}],
        'relations':[{'from':aliases['R-A'],'to':aliases['R-B'],'type':'requires'}]},'kb/extensions.yaml'),first['registry'],namespace='synthetic',previous_bundle=first['bundle'])
    relation=next(r for r in selected(updated).values() if r['record_type']=='relation')
    assert relation['data']['target_status']=='resolved'
    assert relation['data']['from_ref']['id']==aliases['R-A'] and relation['data']['target_ref']['id']==aliases['R-B']
    assert relation['data']['requirement']=='informational'
