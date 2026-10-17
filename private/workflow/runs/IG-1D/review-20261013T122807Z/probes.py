"""Independent identity/reference/source-export oracles using invented data."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

from wgc.contracts.source import ContractError, canonical_bytes, seal_record
from wgc.export.source import build, validate_export
from wgc.export.storage import publish
from wgc.wgu_adapter.identity import locator, reconcile
from wgc.wgu_adapter.importer import finish, import_bytes
from wgc.wgu_adapter.references import diagnose


def corpus(data, path='kb/extensions.yaml'):
    raw = json.dumps(data, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    file = import_bytes(raw, path)
    file.update(availability='available', role='kb', blob_path='files/' + path, edition_label=None)
    result = finish([file])
    result['input_snapshot_id'] = 'sha256:' + hashlib.sha256(raw).hexdigest()
    result['source_snapshot_id'] = 'sha256:' + '0' * 64
    return result


def ids(result, kind='term', label='en'):
    return {o['value'][label]: e['id'] for e in result['registry']['entries'] if e['active'] and e['kind'] == kind for o in e['observations']}


def selected(result):
    bundle = result['bundle']
    snapshot = next(r for r in bundle['records'] if r['id'] == bundle['snapshot_id'])
    store = {(r['id'], r['revision_id']): r for r in bundle['records']}
    return {e['id']: store[(e['id'], e['revision_id'])] for e in snapshot['data']['selected']}


def test_independently_justified_edit_reorder_insert_rename_delete_move():
    one = reconcile(corpus({'terms': [{'en': 'Copper', 'definition': 'Copper distinct body'}, {'en': 'Silver', 'definition': 'Silver distinct body'}]}), namespace='review')
    original = ids(one)
    two = reconcile(corpus({'terms': [{'en': 'Silver', 'definition': 'Silver revised body'}, {'en': 'Copper', 'definition': 'Copper distinct body'}, {'en': 'Gold', 'definition': 'Gold distinct body'}]}, 'kb/moved.yaml'), one['registry'], namespace='review')
    assert ids(two)['Silver'] == original['Silver'] and ids(two)['Copper'] == original['Copper']
    assert ids(two)['Gold'] not in set(original.values())
    three = reconcile(corpus({'terms': [{'en': 'Argent', 'definition': 'Silver revised body'}, {'en': 'Gold', 'definition': 'Gold distinct body'}]}), two['registry'], namespace='review')
    assert ids(three)['Argent'] == original['Silver']
    assert next(e for e in three['registry']['entries'] if e['id'] == original['Copper'])['active'] is False
    assert all(e['origin_key'].startswith('allocation:') for e in three['registry']['entries'])


def test_conflicting_label_and_body_evidence_is_not_silently_prioritized():
    # The same resulting bytes have two compatible histories: keep names and
    # exchange/edit definitions, or keep definitions and exchange/rename names.
    # No external IDs or explicit decision disambiguate these identity histories.
    one = reconcile(corpus({'terms': [{'en': 'Copper', 'definition': 'Copper distinct body'}, {'en': 'Silver', 'definition': 'Silver distinct body'}]}), namespace='review')
    two = reconcile(corpus({'terms': [{'en': 'Copper', 'definition': 'Silver distinct body'}, {'en': 'Silver', 'definition': 'Copper distinct body'}]}), one['registry'], namespace='review')
    assert all(a['ids'] == [] and a['gap_id'] for a in two['assignments'])
    candidates = {i for g in two['registry']['gaps'] if g['active'] for i in g['candidate_ids']}
    assert candidates == set(ids(one).values())


def test_identical_lineage_child_keys_survive_reorder_edit_and_replay():
    first = reconcile(corpus({'terms': [{'en': 'Whole', 'definition': 'Whole body'}]}), namespace='review')
    parent = ids(first)['Whole']
    children = [locator('kb/extensions.yaml', '/terms/0'), locator('kb/extensions.yaml', '/terms/1')]
    op = {'operation': 'split', 'parents': [parent], 'children': children, 'basis': 'Explicit reviewer synthetic partition', 'decision_id': 'partition-1', 'child_keys': {children[0]: 'north', children[1]: 'south'}}
    split = reconcile(corpus({'terms': [{'en': 'Same'}, {'en': 'Same'}]}), first['registry'], namespace='review', lineage=[op])
    by_key = {e['lineage_child_key']: e['id'] for e in split['registry']['entries'] if e['active']}
    moved_op = {**op, 'child_keys': {children[0]: 'south', children[1]: 'north'}}
    moved = reconcile(corpus({'terms': [{'en': 'South changed'}, {'en': 'North changed'}]}), split['registry'], namespace='review', lineage=[moved_op])
    assert ids(moved) == {'South changed': by_key['south'], 'North changed': by_key['north']}
    repeated = reconcile(corpus({'terms': [{'en': 'South changed'}, {'en': 'North changed'}]}), moved['registry'], namespace='review', lineage=[moved_op])
    assert canonical_bytes(moved['registry']) == canonical_bytes(repeated['registry'])


def test_conflicting_hint_and_lineage_on_same_child_requires_explicit_conflict():
    first = reconcile(corpus({'terms': [{'en': 'Whole', 'definition': 'Whole body'}, {'en': 'Other', 'definition': 'Other body'}]}), namespace='review')
    prior = ids(first)
    children = [locator('kb/extensions.yaml', '/terms/0'), locator('kb/extensions.yaml', '/terms/1')]
    op = {'operation': 'split', 'parents': [prior['Whole']], 'children': children, 'basis': 'Allocate new split identities', 'decision_id': 'partition'}
    hints = {children[0]: {'ids': [prior['Other']], 'basis': 'Explicitly preserve Other identity instead'}}
    try:
        result = reconcile(corpus({'terms': [{'en': 'North', 'definition': 'North body'}, {'en': 'South', 'definition': 'South body'}]}), first['registry'], namespace='review', lineage=[op], hints=hints)
    except ValueError:
        return
    child = next(a for a in result['assignments'] if a['locator'] == children[0])
    assert child['ids'] == [] and child['gap_id'], 'Contradictory explicit bindings may not be silently ignored'


def test_exact_current_allocated_ids_resolve_in_navigation():
    first = reconcile(corpus({'rules': [{'id': 'R-A', 'title': 'A'}, {'id': 'R-B', 'title': 'B'}]}), namespace='review')
    rule_ids = ids(first, 'rule', 'id')
    second = reconcile(corpus({'rules': [{'id': 'R-A', 'title': 'A', 'refs': [rule_ids['R-B']]}, {'id': 'R-B', 'title': 'B'}]}), first['registry'], namespace='review')
    diagnostic = next(d for d in diagnose(second)['diagnostics'] if d['raw_locator'] == rule_ids['R-B'])
    assert diagnostic['target_status'] == 'resolved'
    assert diagnostic['target_ids'] == [rule_ids['R-B']]
    assert diagnostic['role'] == 'navigation'


def test_alias_collision_and_explicit_scope_stay_honest():
    data = {'rules': [{'id': 'R-A', 'title': 'A', 'refs': ['R-Collision', 'R-B.x', 'R-B1a']}, {'id': 'R-B', 'title': 'B'}]}
    r = reconcile(corpus(data), namespace='review')
    rules = [e for e in r['registry']['entries'] if e['active'] and e['kind'] == 'rule']
    for e in rules:
        e['external_ids'].append('R-Collision')
    report = diagnose(r)
    by_raw = {d['raw_locator']: d for d in report['diagnostics']}
    assert by_raw['R-Collision']['target_status'] == 'ambiguous' and by_raw['R-Collision']['target_ids'] == []
    assert by_raw['R-B.x']['target_status'] == by_raw['R-B1a']['target_status'] == 'unresolved'
    with pytest.raises(ValueError):
        diagnose(r, scope_resolutions={'R-B.x': {'targets': ['R-Collision'], 'basis': 'Cannot resolve a colliding target'}})
    target = next(e['id'] for e in rules if 'R-B' in e['external_ids'])
    explicit = diagnose(r, scope_resolutions={'R-B.x': {'targets': [target], 'basis': 'Explicit exact singleton scope'}})
    d = next(d for d in explicit['diagnostics'] if d['raw_locator'] == 'R-B.x')
    assert d['target_ids'] == [target] and d['scope_status'] == 'explicit_exact_set'


@pytest.mark.parametrize('missing', ['from', 'to', 'both'])
def test_relationship_resolution_requires_both_endpoints(missing):
    from_id = 'R-Missing' if missing in {'from', 'both'} else 'R-A'
    to_id = 'R-Missing' if missing in {'to', 'both'} else 'R-B'
    result = build(corpus({'rules': [{'id': 'R-A', 'title': 'A'}, {'id': 'R-B', 'title': 'B'}], 'relations': [{'from': from_id, 'to': to_id, 'type': 'requires', 'status': 'verified'}]}), namespace='review')
    relation = next(r for r in selected(result).values() if r['record_type'] == 'relation')
    assert relation['data']['target_status'] == 'unresolved'
    assert relation['data']['target_ref'] is None
    assert relation['data']['requirement'] == 'informational'
    assert result['validation']['semantic_acceptance_granted'] is False


def test_export_lineage_revision_closure_and_many_to_many_raw_values():
    first = build(corpus({'terms': [{'en': 'Whole', 'definition': 'Whole body'}]}), namespace='review')
    parent = ids(first)['Whole']
    children = [locator('kb/extensions.yaml', '/terms/0'), locator('kb/extensions.yaml', '/terms/1')]
    op = {'operation': 'split', 'parents': [parent], 'children': children, 'basis': 'Synthetic explicit split', 'decision_id': 'split'}
    imported = corpus({'terms': [{'en': 'Left', 'definition': 'Left body', 'novel': {'deep': [None, 4]}}, {'en': 'Right', 'definition': 'Right body'}]})
    second = build(imported, first['registry'], namespace='review', previous_bundle=first['bundle'], lineage=[op])
    prior = selected(first)[parent]
    for identity in ids(second).values():
        assert selected(second)[identity]['lineage_refs'] == [{'mode': 'historical', 'id': parent, 'record_type': 'node', 'revision_id': prior['revision_id']}]
    merged_input = corpus({'terms': [{'en': 'Together', 'definition': 'Both contributions', 'novel': {'deep': [False, 9]}}]})
    hints = {locator('kb/extensions.yaml', '/terms/0'): {'ids': list(ids(second).values()), 'basis': 'Exact explicit one-to-many contribution'}}
    third = build(merged_input, second['registry'], namespace='review', previous_bundle=second['bundle'], hints=hints)
    binding = next(r for r in selected(third).values() if r['record_type'] == 'origin_binding' and r['data']['field_locator'] == 'json-pointer:/terms/0/novel')
    assert {r['id'] for r in binding['data']['ig_refs']} == set(ids(second).values())
    assert all('aspect_id' in r for r in binding['data']['ig_refs'])
    validate_export(third['bundle'])
    assert all(r['record_type'] != 'review' for r in third['bundle']['records'])


def test_profile_timestamps_hash_and_reference_closure_are_strict():
    result = build(corpus({'terms': [{'en': 'Copper', 'definition': 'Body'}]}), namespace='review')
    bad = copy.deepcopy(result['bundle'])
    run = next(r for r in bad['records'] if r['record_type'] == 'run')
    run['data']['started_utc'] = '2026-10-13T00:00:00Z'
    with pytest.raises(ContractError):
        validate_export(bad)
    bad = copy.deepcopy(result['bundle'])
    bad['records'][0]['content_hash'] = '0' * 64
    with pytest.raises(ContractError):
        validate_export(bad)
    bad = copy.deepcopy(result['bundle'])
    snapshot = next(r for r in bad['records'] if r['id'] == bad['snapshot_id'])
    snapshot['data']['selected'][0]['revision_id'] = 'sha256:' + '0' * 64
    snapshot.update(seal_record(snapshot))
    with pytest.raises(ContractError):
        validate_export(bad)


def test_packages_preserve_partial_or_corrupt_tree_and_allow_cycles(tmp_path):
    data = {'rules': [{'id': 'R-A', 'title': 'A', 'refs': ['R-B']}, {'id': 'R-B', 'title': 'B', 'refs': ['R-A']}], 'procedures': [{'id': 'P-A', 'title': 'P', 'refs': ['P-A']}]}
    result = build(corpus(data), namespace='review')
    assert len(result['references']['cycles']) == 2 and result['references']['cycles_are_allowed']
    one = publish(result, tmp_path / 'packages', operation_evidence={'review': 'synthetic'})
    two = publish(result, tmp_path / 'packages', operation_evidence={'review': 'repeat'})
    assert one['package'] == two['package'] and one['operation'] != two['operation']
    package = Path(one['package'])
    target = package / 'references.json'
    target.write_bytes(b'corrupt retained bytes')
    with pytest.raises(ValueError):
        publish(result, tmp_path / 'packages')
    assert target.read_bytes() == b'corrupt retained bytes'
