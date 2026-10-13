"""Independent contract expectations on complete synthetic probe bundles."""
from pathlib import Path

import pytest

from wgc.contracts.source import ContractError, load_json, validate_bundle

HERE = Path(__file__).parent
CASES = [r for r in load_json(HERE / 'probe-results.json') if (HERE / (r['name'] + '.json')).exists()]


@pytest.mark.parametrize('case', CASES, ids=lambda c: c['name'])
def test_independent_contract_expectation(case):
    bundle = load_json(HERE / (case['name'] + '.json'))
    if case['expected'] == 'invalid':
        with pytest.raises(ContractError):
            validate_bundle(bundle)
    else:
        report = validate_bundle(bundle)
        assert report['semantic_acceptance_granted'] is False
        name = case['name']
        if name in ('unknown-review-basis', 'unrelated-aspect-change', 'changed-target-description-whole-review', 'missing-selected-basis'):
            expected = {'unknown-review-basis': 'unknown', 'unrelated-aspect-change': 'current', 'changed-target-description-whole-review': 'stale', 'missing-selected-basis': 'stale'}[name]
            assert report['reviews'][0]['freshness'] == expected
