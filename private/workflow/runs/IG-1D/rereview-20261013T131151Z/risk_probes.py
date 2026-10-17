"""First-repair risk controls derived from the four frozen reviewer findings."""
import copy

import pytest

from wgc.contracts.source import canonical_bytes
from wgc.export.source import build
from wgc.wgu_adapter.identity import locator, reconcile
from wgc.wgu_adapter.references import diagnose
from probes import corpus, ids, selected


def terms(*items):
    return corpus({'terms': [{'en': label, 'definition': body} for label, body in items]})


def test_conflict_is_local_and_explicit_hints_resolve_without_new_allocations():
    one = reconcile(terms(('Copper', 'Copper body'), ('Silver', 'Silver body'), ('Gold', 'Gold body')), namespace='review')
    original = ids(one)
    current = terms(('Copper', 'Silver body'), ('Silver', 'Copper body'), ('Gold', 'Gold body'))
    conflicted = reconcile(current, one['registry'], namespace='review')
    assert ids(conflicted) == {'Gold': original['Gold']}
    assert {i for g in conflicted['registry']['gaps'] if g['active'] for i in g['candidate_ids']} == {original['Copper'], original['Silver']}
    assert {o['origin']['field_locator'] for g in conflicted['registry']['gaps'] if g['active'] for o in g['observations']} == {'/terms/0', '/terms/1'}
    hints = {locator('kb/extensions.yaml', '/terms/0'): {'ids': [original['Copper']], 'basis': 'Explicit correction under unchanged names'}, locator('kb/extensions.yaml', '/terms/1'): {'ids': [original['Silver']], 'basis': 'Explicit correction under unchanged names'}}
    resolved = reconcile(current, conflicted['registry'], namespace='review', hints=hints)
    assert ids(resolved) == original
    assert resolved['registry']['next_identity'] == one['registry']['next_identity']
    assert not [g for g in resolved['registry']['gaps'] if g['active']]
    assert all(e['origin_history'] for e in resolved['registry']['entries'])


def test_three_way_contradictory_term_evidence_preserves_candidates():
    one = reconcile(terms(('Copper', 'Copper body'), ('Silver', 'Silver body'), ('Gold', 'Gold body')), namespace='review')
    conflicted = reconcile(terms(('Copper', 'Silver body'), ('Silver', 'Gold body'), ('Gold', 'Copper body')), one['registry'], namespace='review')
    assert not ids(conflicted)
    assert all(a['gap_id'] and not a['ids'] for a in conflicted['assignments'])
    assert {i for g in conflicted['registry']['gaps'] if g['active'] for i in g['candidate_ids']} == set(ids(one).values())


def test_merge_hint_overlap_rejects_or_preserves_both_decisions_as_conflict():
    one = reconcile(terms(('North', 'North body'), ('South', 'South body'), ('Other', 'Other body')), namespace='review')
    original = ids(one)
    before = copy.deepcopy(one['registry'])
    child = locator('kb/extensions.yaml', '/terms/0')
    decision = {'operation': 'merge', 'parents': [original['North'], original['South']], 'children': [child], 'basis': 'Allocate new merge child', 'decision_id': 'merge-overlap'}
    hint = {child: {'ids': [original['Other']], 'basis': 'Retain existing unrelated Other instead'}}
    try:
        result = reconcile(terms(('Together', 'Combined body')), one['registry'], namespace='review', lineage=[decision], hints=hint)
    except ValueError:
        assert one['registry'] == before
        return
    assert result['assignments'][0]['ids'] == [] and result['assignments'][0]['gap_id']
    assert one['registry'] == before


def test_disjoint_hint_and_lineage_remain_valid():
    one = reconcile(terms(('Whole', 'Whole body'), ('Other', 'Other body')), namespace='review')
    original = ids(one)
    children = [locator('kb/extensions.yaml', '/terms/0'), locator('kb/extensions.yaml', '/terms/1')]
    other = locator('kb/extensions.yaml', '/terms/2')
    decision = {'operation': 'split', 'parents': [original['Whole']], 'children': children, 'basis': 'Two explicit split children', 'decision_id': 'split-disjoint'}
    result = reconcile(terms(('North', 'North part'), ('South', 'South part'), ('Other renamed', 'Other corrected')), one['registry'], namespace='review', lineage=[decision], hints={other: {'ids': [original['Other']], 'basis': 'Explicit disjoint correction'}})
    assert ids(result)['Other renamed'] == original['Other']
    assert len({a['ids'][0] for a in result['assignments']}) == 3
    assert not [g for g in result['registry']['gaps'] if g['active']]


def test_direct_active_ids_resolve_relation_endpoints_and_navigation_cycles():
    initial = corpus({'rules': [{'id': 'R-A', 'title': 'A'}, {'id': 'R-B', 'title': 'B'}]})
    first = build(initial, namespace='review')
    rule_ids = ids(first, 'rule', 'id')
    data = {'rules': [{'id': 'R-A', 'title': 'A', 'refs': [rule_ids['R-B']]}, {'id': 'R-B', 'title': 'B', 'see': rule_ids['R-A']}], 'relations': [{'from': rule_ids['R-A'], 'to': rule_ids['R-B'], 'type': 'requires'}]}
    result = build(corpus(data), first['registry'], namespace='review', previous_bundle=first['bundle'])
    report = result['references']
    assert all(d['target_status'] == 'resolved' for d in report['diagnostics'])
    assert sorted(rule_ids.values()) in report['cycles']
    relation = next(r for r in selected(result).values() if r['record_type'] == 'relation')
    assert relation['data']['from_ref']['id'] == rule_ids['R-A']
    assert relation['data']['target_ref']['id'] == rule_ids['R-B']
    assert relation['data']['target_status'] == 'resolved'
    assert relation['data']['requirement'] == 'informational'
    assert result['validation']['semantic_acceptance_granted'] is False


def test_retired_or_nonexistent_allocated_ids_remain_unresolved():
    first = reconcile(corpus({'rules': [{'id': 'R-A', 'title': 'A'}, {'id': 'R-B', 'title': 'B'}]}), namespace='review')
    rule_ids = ids(first, 'rule', 'id')
    current = reconcile(corpus({'rules': [{'id': 'R-A', 'title': 'A', 'refs': [rule_ids['R-B'], 'review:e9999999']}]}), first['registry'], namespace='review')
    report = diagnose(current)
    assert len(report['diagnostics']) == 2
    assert all(d['target_status'] == 'unresolved' and d['target_ids'] == [] for d in report['diagnostics'])


def test_single_merge_child_rename_and_multiple_corrections_keep_receipt():
    first = reconcile(terms(('North', 'North body'), ('South', 'South body')), namespace='review')
    decision = {'operation': 'merge', 'parents': sorted(ids(first).values()), 'children': [locator('kb/extensions.yaml', '/terms/0')], 'basis': 'Exactly one merged child', 'decision_id': 'single-merge'}
    merged = reconcile(terms(('Together', 'Combined body')), first['registry'], namespace='review', lineage=[decision])
    original_id = ids(merged)['Together']
    renamed = reconcile(terms(('Combined', 'Corrected combined body')), merged['registry'], namespace='review', lineage=[decision])
    assert ids(renamed) == {'Combined': original_id}
    corrected = reconcile(terms(('Combined', 'Second corrected body')), renamed['registry'], namespace='review', lineage=[decision])
    assert ids(corrected) == {'Combined': original_id}
    assert corrected['registry']['next_identity'] == merged['registry']['next_identity']
    assert len(next(e for e in corrected['registry']['entries'] if e['id'] == original_id)['origin_history']) == 3
    repeated = reconcile(terms(('Combined', 'Second corrected body')), corrected['registry'], namespace='review', lineage=[decision])
    assert canonical_bytes(corrected['registry']) == canonical_bytes(repeated['registry'])
