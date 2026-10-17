"""Fresh independent controls of receipt persistence, atomic export and replay."""
import copy

import pytest

from wgc.contracts.source import canonical_bytes
from wgc.export.source import build
from wgc.wgu_adapter.identity import locator, reconcile
from probes import corpus, ids, selected


def term_merge(key=None):
    first = build(corpus({'terms': [{'en': 'Copper', 'definition': 'Copper body'}, {'en': 'Silver', 'definition': 'Silver body'}]}), namespace='review')
    child = locator('kb/extensions.yaml', '/terms/0')
    decision = {'operation': 'merge', 'parents': sorted(ids(first).values()), 'children': [child],
        'basis': 'Independent final receipt contract control', 'decision_id': 'final-merge'}
    if key is not None: decision['child_keys'] = {child: key}
    current = corpus({'terms': [{'en': 'Alloy', 'definition': 'Combined body'}]})
    merged = build(current, first['registry'], namespace='review', previous_bundle=first['bundle'], lineage=[decision])
    return merged, decision


@pytest.mark.parametrize('retire_first', [False, True])
def test_persisted_receipt_kind_guard_includes_retired_child(retire_first):
    merged, decision = term_merge()
    registry = merged['registry']
    if retire_first:
        registry = reconcile(corpus({'terms': []}), registry, namespace='review')['registry']
        assert not next(e for e in registry['entries'] if e['id'] == ids(merged)['Alloy'])['active']
    previous = copy.deepcopy(registry)
    with pytest.raises(ValueError, match='changed child contract'):
        reconcile(corpus({'rules': [{'id': 'R-Alloy', 'title': 'New typed output'}]}), registry,
            namespace='review', lineage=[{**decision, 'children': [locator('kb/extensions.yaml', '/rules/0')]}])
    assert registry == previous


@pytest.mark.parametrize('changed_key', [None, 'different'])
def test_changed_child_key_rejects_whole_export_without_mutating_registry_or_bundle(changed_key):
    merged, decision = term_merge('stable')
    previous = copy.deepcopy(merged)
    replay = {k: v for k, v in decision.items() if k != 'child_keys'}
    if changed_key is not None: replay['child_keys'] = {decision['children'][0]: changed_key}
    with pytest.raises(ValueError, match='changed child contract'):
        build(corpus({'terms': [{'en': 'Alloy renamed', 'definition': 'Corrected body'}]}),
            merged['registry'], namespace='review', previous_bundle=merged['bundle'], lineage=[replay])
    assert merged == previous


def test_new_named_output_after_rejection_keeps_old_receipt_history_and_replays():
    merged, decision = term_merge()
    previous = copy.deepcopy(merged)
    new_input = corpus({'rules': [{'id': 'R-Alloy', 'title': 'Deliberately new output kind'}]})
    old_replay = {**decision, 'children': [locator('kb/extensions.yaml', '/rules/0')]}
    with pytest.raises(ValueError):
        reconcile(new_input, merged['registry'], namespace='review', lineage=[old_replay])
    assert merged == previous
    new_decision = {**old_replay, 'decision_id': 'deliberately-new-final-contract'}
    changed = reconcile(new_input, merged['registry'], namespace='review', lineage=[new_decision])
    old_child = ids(merged)['Alloy']
    new_child = ids(changed, 'rule', 'id')['R-Alloy']
    assert new_child != old_child
    old_entry = next(e for e in changed['registry']['entries'] if e['id'] == old_child)
    new_entry = next(e for e in changed['registry']['entries'] if e['id'] == new_child)
    assert not old_entry['active'] and old_entry['origin_history'] == next(e for e in previous['registry']['entries'] if e['id'] == old_child)['origin_history']
    assert new_entry['lineage_key'] != old_entry['lineage_key']
    assert new_entry['lineage_ids'] == sorted(decision['parents'])
    replay = reconcile(new_input, changed['registry'], namespace='review', lineage=[new_decision])
    assert canonical_bytes(changed['registry']) == canonical_bytes(replay['registry'])


def test_keyed_merge_moved_locator_correction_keeps_exact_export_history():
    merged, decision = term_merge('stable')
    previous = copy.deepcopy(merged)
    child_id = ids(merged)['Alloy']
    old_child = selected(merged)[child_id]
    moved_child = locator('kb/new-location.yaml', '/terms/0')
    moved_decision = {**decision, 'children': [moved_child], 'child_keys': {moved_child: 'stable'}, 'parents': list(reversed(decision['parents']))}
    current = corpus({'terms': [{'en': 'Alloy renamed', 'definition': 'Corrected moved body'}]}, 'kb/new-location.yaml')
    moved = build(current, merged['registry'], namespace='review', previous_bundle=merged['bundle'], lineage=[moved_decision])
    assert merged == previous
    assert ids(moved) == {'Alloy renamed': child_id}
    record = selected(moved)[child_id]
    assert record['lineage_refs'] == old_child['lineage_refs']
    assert record['supersedes_refs'] == [{'mode': 'historical', 'id': child_id, 'record_type': 'node', 'revision_id': old_child['revision_id']}]
    assert old_child in moved['bundle']['records']
    old_e = next(e for e in merged['registry']['entries'] if e['id'] == child_id)
    new_e = next(e for e in moved['registry']['entries'] if e['id'] == child_id)
    assert new_e['origin_key'] == old_e['origin_key']
    assert all(o in new_e['origin_history'] for o in old_e['origin_history'])
    repeated = build(current, moved['registry'], namespace='review', previous_bundle=moved['bundle'], lineage=[moved_decision])
    assert all(canonical_bytes(moved[k]) == canonical_bytes(repeated[k]) for k in ['bundle', 'registry', 'references'])
    assert moved['validation']['semantic_acceptance_granted'] is False
