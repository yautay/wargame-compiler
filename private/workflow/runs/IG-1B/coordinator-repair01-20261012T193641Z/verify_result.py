"""Verify completed independent evidence before any coordinator disposition."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
HERE = Path(__file__).parent
DELIVERY = ROOT / 'private/workflow/runs/IG-1B/attempt-review-repair-01-20261012T193641Z/delivery.json'
EXPECTED = 'cf1c928b34aa70ae5b7cf59928baa273c45b02fc26331f8f534f6d1d8056c236'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    path = path.absolute()
    assert path.is_relative_to(ROOT) and not path.is_symlink()
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(items):
    rows = []
    for item in items:
        path = ROOT / item['path']
        actual = digest(path)
        assert actual == item['sha256'], item['path']
        rows.append({'path': item['path'], 'sha256': actual, 'match': True})
    return rows


def main():
    review_path = Path(sys.argv[1]).absolute()
    review = read(review_path)
    assert digest(review_path) == 'a437521ea9feec705ac01039b28e133a0deceaa47b1cd49bead955af34989f10'
    delivery = read(DELIVERY)
    queue = read(ROOT / 'docs/work/queue.json')
    task = next(t for t in queue['tasks'] if t['id'] == 'IG-1B')
    assert task['status'] == 'review'
    assert task['semantic_acceptance_required'] is False
    assert digest(DELIVERY) == EXPECTED
    assert review['role'] == 'reviewer' and review['actor'] != delivery['actor']
    assert review['criteria'] == delivery['criteria'] == task['acceptance']
    frozen = review['frozen_delivery']
    assert frozen['path'] == DELIVERY.relative_to(ROOT).as_posix() and frozen['sha256'] == EXPECTED
    if 'complete_frozen_hashes' in frozen:
        recorded = [{'path': a['path'], 'sha256': a['expected_sha256']} for a in frozen['complete_frozen_hashes']]
    else:
        recorded = review['frozen_delivery_artifacts']
    assert recorded == delivery['artifacts']
    report_rows = verify(review['artifacts'])
    delivery_rows = verify(delivery['artifacts'])
    config_pin = review['configuration_evidence']
    assert digest(ROOT / config_pin['path']) == config_pin['sha256']
    assert review['model'] == 'gpt-6.1-sol' and review['reasoning'] == 'high'
    assert review['semantic_acceptance_granted'] is False
    assert review['executable_readiness_granted'] is False
    result = str(review.get('pass_fail', review.get('technical_result'))).lower()
    assert result in {'pass', 'fail'}
    finding_rows = review.get('findings', [])
    if result == 'pass':
        assert not finding_rows
        assert review['technical_pass'] is True and not review['criteria_unmet']
        assert any(f['id'] == 'F1' and f['status'] == 'closed' and f['repair_cycles_used'] == 1
                   for f in review['finding_dispositions'])
    ig1a = read(ROOT / 'private/workflow/runs/IG-1A/attempt-review-repair-02/delivery.json')
    ig1a_rows = verify(ig1a['artifacts'])
    output = {'task': 'IG-1B', 'independent_result': result, 'reviewer': review['actor'],
              'delivery': {'path': DELIVERY.relative_to(ROOT).as_posix(), 'sha256': EXPECTED},
              'review': {'path': review_path.relative_to(ROOT).as_posix(), 'sha256': digest(review_path)},
              'delivery_artifacts': delivery_rows, 'review_artifacts': report_rows,
              'ig_1a_artifacts': ig1a_rows, 'complete_frozen_list_matches': True,
              'model': review['model'], 'reasoning': review['reasoning'],
              'configuration_evidence': config_pin, 'findings': finding_rows,
              'queue_sha256_before': digest(ROOT / 'docs/work/queue.json'), 'queue_transition_performed': False,
              'semantic_acceptance_granted': False, 'executable_readiness_granted': False}
    (HERE / 'verification.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: output[k] for k in ['independent_result', 'review', 'complete_frozen_list_matches', 'findings']}, indent=2))


if __name__ == '__main__':
    main()
