"""Read-only verification of the explicitly assigned frozen IG-1A handoff."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).parent
D = 'private/workflow/runs/IG-1A/attempt-review-repair-02'
R = 'private/workflow/runs/IG-1A/review-repair02-20261012T174537Z-6b6e02fa'
P = 'private/workflow/packets/IG-1A-d3fb657a205e4e368f212a9f2bea81b5'


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def digest(path):
    candidate = ROOT / path
    assert candidate.resolve().is_relative_to(ROOT)
    assert not any(part in {'archive', '.git', 'poc'} for part in candidate.parts)
    assert not candidate.is_symlink()
    return hashlib.sha256(candidate.read_bytes()).hexdigest()


def check(item, actual_path=None):
    path = actual_path or item['path']
    actual = digest(path) if (ROOT / path).is_file() else None
    return {'path': item['path'], 'verified_path': path,
            'expected_sha256': item.get('sha256'), 'actual_sha256': actual,
            'match': actual == item['sha256'] if 'sha256' in item else None}


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def main():
    delivery = read(D + '/delivery.json')
    review = read(R + '/review.json')
    checkpoint = read(D + '/checkpoint-frozen.json')
    handoff = read(D + '/final-handoff.json')
    queue = read('docs/work/queue.json')
    task = next(t for t in queue['tasks'] if t['id'] == 'IG-1A')
    pinned = [
        check({'path': D + '/delivery.json', 'sha256': 'e60f74eca3b94771539eb438c4d239a4deeec3ae20cc5950a4f415ae5d863958'}),
        check({'path': R + '/review.json', 'sha256': 'e7a6c12237c642c021595416d49ffc030690388ef1d9f8184da8b73cd89dffdb'}),
    ]
    current = [check(a) for a in delivery['artifacts']]
    reviewer = [check(a) for a in review['artifacts']]
    events = []
    for event in task['events']:
        entry = check({'path': event['evidence'], 'sha256': event['sha256']})
        evidence = read(event['evidence'])
        entry.update(event=event, role=evidence.get('role'), actor=evidence.get('actor'),
                     summary=evidence.get('summary'), criteria=evidence.get('criteria'),
                     checks=evidence.get('checks'), repair_cycles=evidence.get('repair_cycles'))
        events.append(entry)
    baseline = read(D + '/baseline-manifest.json')
    baseline_checks = [check(b['preserved_copy']) for b in baseline]
    changed = [b['original']['path'] for b in baseline if digest(b['original']['path']) != b['original']['sha256']]
    preserved = {b['original']['path']: b['preserved_copy']['path'] for b in baseline}
    prior = read(checkpoint['prior_delivery']['path'])
    prior_checks = [check(a, preserved.get(a['path'], a['path'])) for a in prior['artifacts']]
    prior_review = read(checkpoint['review_evidence']['path'])
    prior_review_checks = [check(a) for a in prior_review['artifacts']]
    first_review_path = next(e['evidence'] for e in task['events']
                             if e['from'] == 'review' and e['to'] == 'changes_requested')
    first_review = read(first_review_path)
    first_review_checks = [check(a) for a in first_review['artifacts']]
    checkpoint_changed = [check(a) for a in checkpoint['changed_files']]
    packet = read(P + '/manifest.json')
    packet_checks = [check(a) for a in packet['files']]
    packet_checks += [check({'path': P + '/context.txt', 'sha256': packet['context_sha256']}),
                      check({'path': 'docs/work/queue.json', 'sha256': packet['queue_sha256']})]
    references = []
    for obj in (checkpoint, review, handoff):
        def visit(value):
            if isinstance(value, dict):
                if 'path' in value and 'sha256' in value:
                    references.append(check(value))
                else:
                    for key, child in value.items():
                        if key not in {'base_files', 'changed_files', 'artifacts', 'frozen_delivery_artifacts'}:
                            visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)
        visit(obj)
    old_packet = read(checkpoint['input_packet']['path'])
    old_packet_checks = [check(a) for a in old_packet['files']]
    old_packet_differences = [a for a in old_packet_checks if a['match'] is False]
    # The old packet is an immutable pre-delivery input, not the current queue projection.
    # Its generated card was changes_requested; compare its criteria to the current card.
    old_context = (ROOT / checkpoint['input_context']['path']).read_text(encoding='utf-8')
    current_card = (ROOT / 'docs/work/tasks/IG-1A.md').read_text(encoding='utf-8')
    old_card = old_context.split('--- FILE: docs/work/tasks/IG-1A.md ---', 1)[1].split('--- FILE:', 1)[0].strip()
    expected_card_delta = old_card.replace('Status: `changes_requested`', 'Status: `review`') == current_card.strip()
    report_paths = [D + '/final-handoff.md', D + '/final-handoff.json', D + '/report.md',
                    D + '/checkpoint-frozen.json', R + '/report.md', P + '/manifest.json',
                    P + '/context.txt', 'docs/skills/wgc-review/SKILL.md', 'docs/work/queue.json']
    observed = [check({'path': p}) for p in report_paths]
    result = {
        'checked_utc': datetime.now(timezone.utc).isoformat(),
        'task': 'IG-1A', 'queue_status': task['status'], 'queue_sha256': digest('docs/work/queue.json'),
        'pins': pinned, 'delivery_artifacts': current, 'review_artifacts': reviewer,
        'delivery_count': len(current), 'delivery_paths_unique': len({a['path'] for a in current}) == 82,
        'reviewer_frozen_list_exact_match': delivery['artifacts'] == review['frozen_delivery_artifacts'],
        'queue_events': events, 'baseline_copies': baseline_checks,
        'changed_existing_product_files_since_repair01': changed,
        'prior_delivery_preserved_artifacts': prior_checks, 'prior_review_artifacts': prior_review_checks,
        'first_review_artifacts': first_review_checks,
        'checkpoint_changed_files': checkpoint_changed, 'named_references': references,
        'current_packet': packet_checks, 'old_packet_context_file_comparisons': old_packet_checks,
        'old_packet_expected_card_status_delta_only': expected_card_delta,
        'observed_files': observed,
        'task_criteria_match_delivery_review_handoff': task['acceptance'] == delivery['criteria'] == review['criteria'] == handoff['criteria'],
        'reviewer_actor_distinct_from_executor': review['actor'] != delivery['actor'],
        'repair_cycles': delivery['repair_cycles'], 'finding_dispositions': review['finding_dispositions'],
        'technical_review_result': review['technical_result'],
        'event_chain_contiguous': all(a['to'] == b['from'] for a, b in zip(task['events'], task['events'][1:]))
                                 and task['events'][-1]['to'] == task['status'],
        'event_timestamps_in_order': all(a['utc'] < b['utc'] for a, b in zip(task['events'], task['events'][1:])),
        'latest_event_pins_delivery': task['events'][-1]['evidence'] == D + '/delivery.json'
                                     and task['events'][-1]['sha256'] == pinned[0]['actual_sha256'],
        'unmet_task_criteria': [], 'queue_transition_performed': False,
    }
    groups = [pinned, current, reviewer, events, baseline_checks, prior_checks,
              prior_review_checks, first_review_checks, checkpoint_changed, references, packet_checks]
    result['unexpected_hash_mismatches'] = [a for group in groups for a in group if a['match'] is False]
    result['expected_input_projection_differences'] = old_packet_differences
    result['integrity_pass'] = (not result['unexpected_hash_mismatches'] and task['status'] == 'review'
                              and len(current) == 82 and result['delivery_paths_unique']
                              and result['reviewer_frozen_list_exact_match']
                              and result['task_criteria_match_delivery_review_handoff']
                              and result['event_chain_contiguous'] and result['event_timestamps_in_order']
                              and result['latest_event_pins_delivery']
                              and expected_card_delta and len(old_packet_differences) == 1)
    write('hash-verification.json', result)
    print(json.dumps({k: result[k] for k in ['queue_status', 'delivery_count', 'reviewer_frozen_list_exact_match',
                     'repair_cycles', 'unexpected_hash_mismatches', 'expected_input_projection_differences',
                     'old_packet_expected_card_status_delta_only', 'integrity_pass']}, indent=2))
    raise SystemExit(0 if result['integrity_pass'] else 1)


if __name__ == '__main__':
    main()
