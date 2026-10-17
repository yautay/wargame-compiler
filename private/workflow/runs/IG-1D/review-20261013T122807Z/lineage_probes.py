"""Independent merge receipts, unique-child edit and exact historical lineage."""
from wgc.contracts.source import canonical_bytes
from wgc.export.source import build
from wgc.wgu_adapter.identity import locator, reconcile
from probes import corpus, ids, selected


def merge_case():
    prior_input = corpus({'terms': [{'en': 'North', 'definition': 'North body'}, {'en': 'South', 'definition': 'South body'}]})
    first = reconcile(prior_input, namespace='review')
    current_input = corpus({'terms': [{'en': 'Together', 'definition': 'Both merged contributions'}]})
    decision = {'operation': 'merge', 'parents': sorted(ids(first).values()), 'children': [locator('kb/extensions.yaml', '/terms/0')], 'basis': 'One explicit merged child', 'decision_id': 'merge-1'}
    merged = reconcile(current_input, first['registry'], namespace='review', lineage=[decision])
    return first, current_input, decision, merged


def test_merge_receipt_unchanged_replay_is_exact():
    first, current, decision, merged = merge_case()
    again = reconcile(current, merged['registry'], namespace='review', lineage=[decision])
    assert canonical_bytes(merged['registry']) == canonical_bytes(again['registry'])
    assert next(e for e in merged['registry']['entries'] if e['active'])['lineage_ids'] == decision['parents']
    assert set(ids(merged).values()).isdisjoint(ids(first).values())


def test_unique_merge_child_correction_retains_persisted_receipt_identity():
    first, current, decision, merged = merge_case()
    # The decision has exactly one child. Its persistent receipt, operation,
    # parents, child kind and scope identify that one child independently of text.
    corrected_input = corpus({'terms': [{'en': 'Together', 'definition': 'Corrected combined contributions'}]})
    corrected = reconcile(corrected_input, merged['registry'], namespace='review', lineage=[decision])
    assert ids(corrected) == {'Together': ids(merged)['Together']}
    assert not [g for g in corrected['registry']['gaps'] if g['active']]


def test_export_merge_keeps_exact_prior_revisions_and_does_not_transfer_approval():
    prior = build(corpus({'terms': [{'en': 'North', 'definition': 'North body'}, {'en': 'South', 'definition': 'South body'}]}), namespace='review')
    parents = sorted(ids(prior).values())
    decision = {'operation': 'merge', 'parents': parents, 'children': [locator('kb/extensions.yaml', '/terms/0')], 'basis': 'One explicit merged child', 'decision_id': 'merge-1'}
    current_input = corpus({'terms': [{'en': 'Together', 'definition': 'Both merged contributions'}]})
    merged = build(current_input, prior['registry'], namespace='review', previous_bundle=prior['bundle'], lineage=[decision])
    node = selected(merged)[ids(merged)['Together']]
    assert node['lineage_refs'] == [{'mode': 'historical', 'id': p, 'record_type': 'node', 'revision_id': selected(prior)[p]['revision_id']} for p in parents]
    repeated = build(current_input, merged['registry'], namespace='review', previous_bundle=merged['bundle'], lineage=[decision])
    assert canonical_bytes(merged['bundle']) == canonical_bytes(repeated['bundle'])
    assert merged['validation']['semantic_acceptance_granted'] is False
