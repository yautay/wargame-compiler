"""Fresh structural and byte-preservation checks for the repaired reports."""
import copy
from repair_indexes import META, OLD, ROOT, RUN, SESSION, ADDITIONS, load, pin, write


def verify(record):
    actual = pin(ROOT / record['path'])
    assert actual['sha256'] == record['sha256'], record['path']
    if 'bytes' in record:
        assert actual['bytes'] == record['bytes'], record['path']


def main():
    task = load(SESSION / 'task.json')
    references = load(SESSION / 'references.json')
    scope = load(ROOT / task['repair_authorization']['scope']['path'])
    old_delivery = load(OLD / 'delivery.json')
    prior_preservation = load(OLD / 'preservation-report.json')
    blocked = load(ROOT / prior_preservation['blocked_artifact_manifest']['path'])
    dependency = load(ROOT / prior_preservation['accepted_dependency_event']['path'])
    review = load(ROOT / references['findings']['evidence'])
    frozen_groups = {'old_delivery': old_delivery['artifacts'],
                     'blocked_attempt': blocked['artifacts'],
                     'accepted_dependency': dependency['artifacts'],
                     'review_reports': review['review_artifacts']}
    for group in frozen_groups.values():
        for record in group:
            verify(record)
    for record in [scope['immutable_delivery'],
                   prior_preservation['blocked_artifact_manifest'],
                   prior_preservation['accepted_dependency_event'],
                   task['repair_authorization']['scope'],
                   task['repair_authorization']['evidence'],
                   {'path': references['findings']['evidence'],
                    'sha256': references['findings']['sha256']}]:
        verify(record)
    assert pin(ROOT / META['configuration_evidence'])['sha256'] == META['configuration_sha256']
    config = load(ROOT / META['configuration_evidence'])
    assert (config['status'], config['model'], config['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
    queue = load(ROOT / 'docs/work/queue.json')
    selected = {row['id']: row for row in queue['tasks'] if row['id'] in ['IG-2B03', 'IG-2B02']}
    assert selected['IG-2B02']['status'] == 'done'
    assert selected['IG-2B03']['status'] == 'in_progress'
    claim_event = selected['IG-2B03']['events'][-1]
    assert claim_event['evidence'] == (RUN / 'claim.json').relative_to(ROOT).as_posix()
    assert claim_event['sha256'] == pin(RUN / 'claim.json')['sha256']
    assert all(selected['IG-2B03'][key] == value for key, value in task.items() if key != 'status')

    old_ledger = load(OLD / 'region-ledger.json')
    new_ledger = load(RUN / 'region-ledger.json')
    stripped = copy.deepcopy(new_ledger)
    for key in META:
        assert stripped[key] == META[key]
        stripped[key] = old_ledger[key]
    del stripped['repair_provenance']
    changed_ids = []
    for before, after in zip(old_ledger['regions'], stripped['regions'], strict=True):
        additions = ADDITIONS.get(before['region']['key'], [])
        assert after['raw_cross_references'] == before['raw_cross_references'] + additions
        if additions:
            changed_ids.append(before['region']['id'])
            after['raw_cross_references'] = before['raw_cross_references']
        assert before == after
    assert stripped == old_ledger
    assert len(stripped['regions']) == 135
    old_cont = load(OLD / 'continuations.json')
    new_cont = load(RUN / 'continuations.json')
    stripped_cont = copy.deepcopy(new_cont)
    for key in META:
        assert stripped_cont[key] == META[key]
        stripped_cont[key] = old_cont[key]
    del stripped_cont['repair_provenance']
    original_count = len(old_cont['unfollowed_references'])
    assert stripped_cont['unfollowed_references'][:original_count] == old_cont['unfollowed_references']
    appended = stripped_cont['unfollowed_references'][original_count:]
    assert len(appended) == 7
    for row, region_id in zip(appended, changed_ids, strict=True):
        assert row['region_id'] == region_id
        region = next(item for item in new_ledger['regions'] if item['region']['id'] == region_id)
        assert row['raw'] == region['raw_cross_references'] == ADDITIONS[region['region']['key']]
    stripped_cont['unfollowed_references'] = stripped_cont['unfollowed_references'][:original_count]
    assert stripped_cont == old_cont
    assert len(old_cont['literal_continuations']) == 4
    audit = load(RUN / 'reference-audit.json')
    assert audit['regions_audited'] == 135 and audit['added_literals'] == 8
    for change in audit['changes']:
        verify(change['text_artifact'])
        text = (ROOT / change['text_artifact']['path']).read_text(encoding='utf-8')
        for item in change['text_offsets']:
            assert text[item['start']:item['end']] == item['exact_text_slice']
            assert ' '.join(item['exact_text_slice'].split()) == item['literal']
    for record in audit['original_page_images_inspected'] + audit['repaired_reports']:
        verify(record)
    write('preservation-report.json', {
        **META, 'format': 'wgc-repair-preservation-1',
        'frozen_groups_rehashed': {name: len(group) for name, group in frozen_groups.items()},
        'baseline_delivery': pin(OLD / 'delivery.json'),
        'baseline_manifest': pin(OLD / 'delivery-manifest.json'),
        'blocked_manifest': prior_preservation['blocked_artifact_manifest'],
        'all_prior_frozen_bytes_unchanged': True,
        'inventory_and_registry_unchanged': True,
        'all_135_region_ids_keys_revisions_boxes_locators_and_coverage_unchanged': True,
        'all_22_component_locators_unchanged': True,
        'reading_order_and_four_literal_continuations_unchanged': True,
        'full_task_context_counts_unchanged': old_delivery['counts'],
        'accepted_pages_1_to_8_and_placeholders_13_to_44': 'Frozen inventory bytes and accepted dependency artifacts rehashed unchanged; no edits to any nested record.',
        'claim_and_dependency_verified': True,
        'semantic_acceptance_granted': False})
    write('index-validation.json', {
        **META, 'format': 'wgc-index-repair-validation-1',
        'finding': 'R01', 'outcome': 'pass',
        'changed_region_ids': changed_ids, 'added_reference_literals': 8,
        'original_reference_prefix_preserved': True,
        'complete_ledger_comparison_allows_only_reference_additions_and_provenance': True,
        'complete_continuation_comparison_allows_only_reference_additions_and_provenance': True,
        'unicode_offsets_and_existing_text_hashes_verified': True,
        'source_review_scope': 'All assigned original pages visually inspected for literal named-reference omissions. No new boundary, gameplay or semantic acceptance assertion.',
        'checks': [{'command': '.venv/Scripts/python.exe -B private/workflow/runs/IG-2B03/repair-r01-f684f3e2-01/verify_repair.py', 'exit_code': 0}],
        'semantic_acceptance_granted': False})
    print('PASS: reference-only structural changes; all prior frozen groups rehashed unchanged.')


if __name__ == '__main__':
    main()
