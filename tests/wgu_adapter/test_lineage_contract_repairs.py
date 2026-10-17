"""Synthetic R04 receipt-contract boundaries, independent of corrected content."""
import copy

import pytest

from wgc.wgu_adapter.identity import locator, reconcile
from tests.wgu_adapter.test_identity import corpus, ids


def merged_term(child_key=None):
    first = reconcile(corpus({'terms': [{'en': 'North', 'definition': 'north'},
                                       {'en': 'South', 'definition': 'south'}]}), namespace='synthetic')
    loc = locator('kb/terms.yaml', '/terms/0')
    decision = {'operation': 'merge', 'parents': sorted(ids(first).values()),
                'children': [loc], 'basis': 'Explicit synthetic merge', 'decision_id': 'merge-contract'}
    if child_key is not None: decision['child_keys'] = {loc: child_key}
    merged = reconcile(corpus({'terms': [{'en': 'Together', 'definition': 'combined'}]}),
                       first['registry'], namespace='synthetic', lineage=[decision])
    return merged, decision


def rejects_atomically(imported, previous, decision):
    before = copy.deepcopy(previous)
    with pytest.raises(ValueError, match='changed child contract'):
        reconcile(imported, previous, namespace='synthetic', lineage=[decision])
    assert previous == before


def test_named_merge_changed_kind_rejects_atomically():
    merged, decision = merged_term()
    rejects_atomically(corpus({'rules': [{'id': 'R-Together', 'title': 'Different kind'}]}),
                      merged['registry'], {**decision, 'children': [locator('kb/terms.yaml', '/rules/0')]})


@pytest.mark.parametrize(('prior_key', 'next_key'), [(None, 'new'), ('kept', None), ('kept', 'changed')])
def test_named_merge_changed_persistent_child_key_rejects(prior_key, next_key):
    merged, decision = merged_term(prior_key)
    decision.pop('child_keys', None)
    if next_key is not None: decision['child_keys'] = {decision['children'][0]: next_key}
    rejects_atomically(corpus({'terms': [{'en': 'Corrected', 'definition': 'new text'}]}),
                      merged['registry'], decision)


def test_new_named_decision_allows_deliberately_different_kind():
    merged, decision = merged_term()
    old_id = ids(merged)['Together']
    new = reconcile(corpus({'rules': [{'id': 'R-Together', 'title': 'Deliberate new output'}]}),
                    merged['registry'], namespace='synthetic', lineage=[
                        {**decision, 'decision_id': 'merge-rule-contract',
                         'children': [locator('kb/terms.yaml', '/rules/0')]}])
    new_id = ids(new, 'rule', 'id')['R-Together']
    assert new_id != old_id
    old_entry = next(e for e in new['registry']['entries'] if e['id'] == old_id)
    new_entry = next(e for e in new['registry']['entries'] if e['id'] == new_id)
    assert not old_entry['active'] and old_entry['origin_history']
    assert new_entry['lineage_ids'] == decision['parents']


def merged_step():
    data = {'procedures': [{'id': 'P-A', 'title': 'A', 'steps': [{'n': 1, 'text': 'north'}, {'n': 2, 'text': 'south'}]},
                           {'id': 'P-B', 'title': 'B', 'steps': []}]}
    first = reconcile(corpus(data), namespace='synthetic')
    decision = {'operation': 'merge', 'parents': sorted(ids(first, 'step', 'text').values()),
                'children': [locator('kb/terms.yaml', '/procedures/0/steps/0')],
                'basis': 'Synthetic merge of two local steps', 'decision_id': 'merge-step'}
    current = {'procedures': [{'id': 'P-A', 'title': 'A', 'steps': [{'n': 1, 'text': 'together'}]},
                              {'id': 'P-B', 'title': 'B', 'steps': []}]}
    merged = reconcile(corpus(current), first['registry'], namespace='synthetic', lineage=[decision])
    return merged, decision


def test_named_merge_changed_logical_parent_scope_rejects():
    merged, decision = merged_step()
    changed = {'procedures': [{'id': 'P-A', 'title': 'A', 'steps': []},
                              {'id': 'P-B', 'title': 'B', 'steps': [{'n': 1, 'text': 'together'}]}]}
    rejects_atomically(corpus(changed), merged['registry'],
                      {**decision, 'children': [locator('kb/terms.yaml', '/procedures/1/steps/0')]})


def test_named_merge_reordered_parent_and_file_move_keep_scope_and_allocation():
    merged, decision = merged_step()
    before = copy.deepcopy(merged['registry'])
    identity = ids(merged, 'step', 'text')['together']
    changed = {'procedures': [{'id': 'P-B', 'title': 'B', 'steps': []},
                              {'id': 'P-A', 'title': 'A', 'steps': [{'n': 7, 'text': 'corrected'}]}]}
    result = reconcile(corpus(changed, 'kb/moved.yaml'), merged['registry'], namespace='synthetic',
                       lineage=[{**decision, 'children': [locator('kb/moved.yaml', '/procedures/1/steps/0')]}])
    assert ids(result, 'step', 'text') == {'corrected': identity}
    assert merged['registry'] == before
    entry = next(e for e in result['registry']['entries'] if e['id'] == identity)
    prior = next(e for e in before['entries'] if e['id'] == identity)
    assert entry['scope'] == prior['scope'] and entry['origin_key'] == prior['origin_key']
    assert all(origin in entry['origin_history'] for origin in prior['origin_history'])


def test_named_keyed_split_changed_key_rejects_and_reorder_replays():
    first = reconcile(corpus({'terms': [{'en': 'Whole', 'definition': 'whole'}]}), namespace='synthetic')
    locations = [locator('kb/terms.yaml', '/terms/0'), locator('kb/terms.yaml', '/terms/1')]
    decision = {'operation': 'split', 'parents': list(ids(first).values()), 'children': locations,
                'basis': 'Synthetic keyed split', 'decision_id': 'split-contract',
                'child_keys': dict(zip(locations, ['left', 'right']))}
    data = {'terms': [{'en': 'Left', 'definition': 'left body'}, {'en': 'Right', 'definition': 'right body'}]}
    split = reconcile(corpus(data), first['registry'], namespace='synthetic', lineage=[decision])
    rejects_atomically(corpus(data), split['registry'],
                      {**decision, 'child_keys': dict(zip(locations, ['changed', 'right']))})
    reordered = reconcile(corpus({'terms': list(reversed(data['terms']))}), split['registry'],
                          namespace='synthetic', lineage=[{**decision, 'child_keys': dict(zip(locations, ['right', 'left']))}])
    assert ids(reordered) == ids(split)
