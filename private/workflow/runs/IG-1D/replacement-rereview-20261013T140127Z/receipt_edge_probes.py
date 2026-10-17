"""Additional boundary checks for named child contracts and non-term conflicts."""
import copy

import pytest

from wgc.wgu_adapter.identity import locator, reconcile
from wgc.wgu_adapter.references import diagnose
from probes import corpus, ids


def test_conflicting_step_number_and_body_retains_all_candidates():
    one = reconcile(corpus({'procedures': [{'id': 'P-A', 'title': 'Procedure', 'steps': [{'n': 1, 'text': 'North body'}, {'n': 2, 'text': 'South body'}]}]}), namespace='review')
    prior_ids = ids(one, 'step', 'text')
    two = reconcile(corpus({'procedures': [{'id': 'P-A', 'title': 'Procedure', 'steps': [{'n': 1, 'text': 'South body'}, {'n': 2, 'text': 'North body'}]}]}), one['registry'], namespace='review')
    steps = [a for a in two['assignments'] if '/steps/' in a['locator']]
    assert len(steps) == 2 and all(not a['ids'] and a['gap_id'] for a in steps)
    assert {i for g in two['registry']['gaps'] if g['active'] for i in g['candidate_ids']} == set(prior_ids.values())


def test_direct_identity_alias_collision_is_ambiguous():
    first = reconcile(corpus({'rules': [{'id': 'R-A', 'title': 'A'}, {'id': 'R-B', 'title': 'B'}]}), namespace='review')
    a, b = sorted(e['id'] for e in first['registry']['entries'])
    other = next(e for e in first['registry']['entries'] if e['id'] == b)
    other['external_ids'].append(a)
    first['records'][0]['value']['refs'] = [a]
    diagnostic = next(d for d in diagnose(first)['diagnostics'] if d['raw_locator'] == a)
    assert diagnostic['target_status'] == 'ambiguous'
    assert diagnostic['target_ids'] == [] and set(diagnostic['candidate_ids']) == {a, b}


def test_named_merge_receipt_changed_child_kind_is_not_silently_reallocated():
    first = reconcile(corpus({'terms': [{'en': 'North', 'definition': 'North body'}, {'en': 'South', 'definition': 'South body'}]}), namespace='review')
    decision = {'operation': 'merge', 'parents': sorted(ids(first).values()), 'children': [locator('kb/extensions.yaml', '/terms/0')], 'basis': 'One explicit merged child', 'decision_id': 'merge-child-contract'}
    merged = reconcile(corpus({'terms': [{'en': 'Together', 'definition': 'Combined body'}]}), first['registry'], namespace='review', lineage=[decision])
    before = copy.deepcopy(merged['registry'])
    changed = corpus({'rules': [{'id': 'R-Together', 'title': 'A different logical child kind'}]})
    changed_decision = {**decision, 'children': [locator('kb/extensions.yaml', '/rules/0')]}
    try:
        result = reconcile(changed, merged['registry'], namespace='review', lineage=[changed_decision])
    except ValueError:
        assert merged['registry'] == before
        return
    assert all(not a['ids'] and a['gap_id'] for a in result['assignments']), 'A named one-child receipt cannot silently acquire a different child-kind contract'
    assert merged['registry'] == before
