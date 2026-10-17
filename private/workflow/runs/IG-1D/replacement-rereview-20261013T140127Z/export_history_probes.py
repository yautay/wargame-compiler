"""Independent corrected-child historical revision and decision atomicity checks."""
import copy

import pytest

from wgc.contracts.source import canonical_bytes
from wgc.export.source import build
from wgc.wgu_adapter.identity import locator
from probes import corpus, ids, selected


def test_corrected_and_renamed_merge_child_keeps_exact_parent_and_child_history():
    first = build(corpus({'terms': [{'en': 'North', 'definition': 'North body'}, {'en': 'South', 'definition': 'South body'}]}), namespace='review')
    parents = sorted(ids(first).values())
    decision = {'operation': 'merge', 'parents': parents, 'children': [locator('kb/extensions.yaml', '/terms/0')], 'basis': 'Exactly one explicit merged child', 'decision_id': 'history-merge'}
    merged = build(corpus({'terms': [{'en': 'Together', 'definition': 'Combined body'}]}), first['registry'], namespace='review', previous_bundle=first['bundle'], lineage=[decision])
    child_id = ids(merged)['Together']
    old_child = selected(merged)[child_id]
    corrected_input = corpus({'terms': [{'en': 'Combined renamed', 'definition': 'Corrected combined body'}]})
    corrected = build(corrected_input, merged['registry'], namespace='review', previous_bundle=merged['bundle'], lineage=[decision])
    assert ids(corrected) == {'Combined renamed': child_id}
    child = selected(corrected)[child_id]
    assert child['lineage_refs'] == [{'mode': 'historical', 'id': p, 'record_type': 'node', 'revision_id': selected(first)[p]['revision_id']} for p in parents]
    assert child['supersedes_refs'] == [{'mode': 'historical', 'id': child_id, 'record_type': 'node', 'revision_id': old_child['revision_id']}]
    assert any(r == old_child for r in corrected['bundle']['records'])
    repeated = build(corrected_input, corrected['registry'], namespace='review', previous_bundle=corrected['bundle'], lineage=[decision])
    assert all(canonical_bytes(corrected[k]) == canonical_bytes(repeated[k]) for k in ['bundle', 'registry', 'references'])
    assert corrected['validation']['semantic_acceptance_granted'] is False
    assert corrected['validation']['executable']['status'] == 'blocked'


def test_named_receipt_changed_basis_rejects_without_mutating_prior_outputs():
    first = build(corpus({'terms': [{'en': 'North', 'definition': 'North body'}, {'en': 'South', 'definition': 'South body'}]}), namespace='review')
    decision = {'operation': 'merge', 'parents': sorted(ids(first).values()), 'children': [locator('kb/extensions.yaml', '/terms/0')], 'basis': 'Exactly one explicit merged child', 'decision_id': 'history-merge'}
    current = corpus({'terms': [{'en': 'Together', 'definition': 'Combined body'}]})
    merged = build(current, first['registry'], namespace='review', previous_bundle=first['bundle'], lineage=[decision])
    previous = copy.deepcopy(merged)
    with pytest.raises(ValueError):
        build(current, merged['registry'], namespace='review', previous_bundle=merged['bundle'], lineage=[{**decision, 'basis': 'A different decision contract'}])
    assert merged == previous
