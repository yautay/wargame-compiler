"""Independent byte/prefix and preserved-review coverage audit, no source analysis."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).parent
ROOT = Path('private/workflow/runs/IG-2B04')
SESSION = Path('private/workflow/orchestrator/20261016T142331Z-0d4dc364/002-IG-2B04-reviewer-4fab98d5')

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def pin(path):
    p = Path(path)
    return {'path': p.as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}

def base(summary):
    cpath = SESSION / 'runtime-configuration.json'
    c = load(cpath)
    assert (c['status'], c['model'], c['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
    return dict(role='reviewer', actor='ig2:002-IG-2B04-reviewer-4fab98d5:reviewer',
                task='IG-2B04', model=c['model'], reasoning=c['reasoning'],
                configuration_evidence=cpath.as_posix(), configuration_sha256=sha(cpath),
                utc=datetime.now(timezone.utc).isoformat(), summary=summary)

def write(name, value):
    p = OUT / name
    assert not p.exists(), p
    p.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

def audit(name):
    mismatches = []
    counts = {}
    verified = []
    def verify(items, label):
        counts[label] = len(items)
        for item in items:
            actual = pin(item['path'])
            ok = actual['sha256'] == item['sha256'] and ('bytes' not in item or actual['bytes'] == item['bytes'])
            verified.append(dict(group=label, **actual, passed=ok))
            if not ok:
                mismatches.append({'expected': item, 'actual': actual})

    ref = load(SESSION / 'delivery-reference.json')
    verify([{'path': ref['evidence'], 'sha256': ref['sha256']}], 'current_delivery_envelope')
    delivery = load(ref['evidence'])
    assert load(SESSION / 'delivery.json') == delivery
    original_path = ROOT / 'continuation-13-16-rg04/delivery-manifest.json'
    verify([{'path': original_path.as_posix(), 'sha256': 'ba026675123a5e9f3b397ebc41b8840dcdc349d04391037a4d74ec5abd6463fc'}], 'original_envelope')
    original = load(original_path)
    assert len(original['artifacts']) == 2325
    assert delivery['artifacts'][:2325] == original['artifacts']
    verify(delivery['artifacts'], 'current_delivery_artifacts')
    protect_path = ROOT / 'rg-recovery-20261016-01/preserve.json'
    verify([{'path': protect_path.as_posix(), 'sha256': 'ffd957d8e26ed8c4b0b782d46e3c1db2170094ea55286481c7fe9d1237dffe13', 'bytes': 204341}], 'protected_manifest')
    verify(load(protect_path)['artifacts'], 'protected_artifacts')
    review_path = ROOT / 'review-ce506337-01/review.json'
    verify([{'path': review_path.as_posix(), 'sha256': 'f6946697d279730c5fada8bd8dc3fabd7e1dc1c4a594ed875ab8a2680e1e6c2e'}], 'prior_review')
    review = load(review_path)
    assert review['artifacts'] == original['artifacts']
    verify(review['review_artifacts'], 'prior_review_artifacts')
    packet = load(SESSION / 'packet.json')
    packet_items = []
    for item in packet['files'] + packet['control_files']:
        item = dict(item)
        if item['path'] in ('docs/STATUS.md', 'docs/HANDOFF.md'):
            item['path'] = (SESSION / 'bootstrap' / Path(item['path']).name).as_posix()
        packet_items.append(item)
    verify(packet_items, 'packet_files_and_controls')
    task = load(SESSION / 'task.json')
    verify([task['context_recovery_authorization'][k] for k in ('scope', 'assessment')]
           + [task['inventory_contract'], task['repair_authorization']['scope'], task['repair_authorization']['evidence']],
           'current_contract_pins')
    refs = load(SESSION / 'references.json')
    verify([{'path': refs[k]['evidence'], 'sha256': refs[k]['sha256']} for k in ('findings', 'prior_delivery', 'repair_claim')], 'current_reference_pins')
    # Dependency content remains behind the prepared projection helper. Byte hashing
    # frozen artifacts above does not interpret or print dependency contents.
    ledger = load(ROOT / 'continuation-13-16-rg04/region-ledger.json')
    inspection_path = ROOT / 'review-ce506337-01/source-inspection.json'
    inspection = load(inspection_path)
    components = inspection['component_reviews']
    regions = ledger['regions']
    assert len(regions) == len(components) == 113
    reviewed = {c['key']: c for c in components}
    assert len(reviewed) == 113
    coverage = []
    for region in regions:
        spec = region['specification']
        c = reviewed[spec['key']]
        ok = (c['passed'] is True and c['original_comparison']
              and c['region_id'] == region['record']['id']
              and c['pdf_page'] == spec['pdf_page'] and c['kind'] == spec['kind']
              and c['normalized_box'] == spec['box'])
        assert ok, spec['key']
        coverage.append({'key': spec['key'], 'region_id': c['region_id'], 'pdf_page': c['pdf_page'], 'passed': bool(ok)})
    assert inspection['scope'] == [13, 14, 15, 16]
    assert inspection['passed'] is True
    assert len(inspection['continuations_reviewed']) == 5
    assert review['source_review_findings'] == []
    assert [f['id'] for f in review['findings']] == ['V01']
    assert all(p['all_components_and_boundaries_visually_compared'] for p in inspection['pages'])
    for page in inspection['pages']:
        assert page['component_count'] == sum(c['pdf_page'] == page['pdf_page'] for c in components)
    assert delivery['criteria'] == task['acceptance'] == review['criteria']
    assert not mismatches, mismatches
    report = base('Every current delivery artifact, protected pin and prior review artifact verified; complete prior 113-component source-review coverage retained for validation-only V01 rereview.')
    report.update(counts=counts, mismatches=mismatches, exact_ordered_prefix_count=2325,
                  delivery=pin(ref['evidence']), protected_manifest=pin(protect_path),
                  prior_review=pin(review_path), preserved_source_inspection=pin(inspection_path),
                  preserved_component_coverage=coverage, preserved_page_counts={str(p['pdf_page']):p['component_count'] for p in inspection['pages']},
                  preserved_continuations=inspection['continuations_reviewed'],
                  source_inspection_or_regeneration_performed=False, semantic_acceptance_granted=False,
                  verified=verified, passed=True)
    write(name, report)
    print(json.dumps({'passed': True, 'counts': counts, 'ordered_prefix': 2325, 'preserved_components': 113, 'configuration_sha256': report['configuration_sha256']}))

if __name__ == '__main__':
    audit(sys.argv[1])
