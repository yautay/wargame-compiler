import copy
import hashlib
import json
import sys
import os
import importlib.metadata
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SESSION = Path('private/workflow/orchestrator/20261015T175019Z-9761be5b/002-IG-2B03-reviewer-cabf2418')
OLD = Path('private/workflow/runs/IG-2B03/continuation-search-20261015-01')
NEW = Path('private/workflow/runs/IG-2B03/repair-r01-f684f3e2-01')
ACTOR = 'ig2:002-IG-2B03-reviewer-cabf2418:reviewer'

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def pin(path):
    p = Path(path)
    b = p.read_bytes()
    return {'path': p.as_posix(), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def verify(record):
    actual = pin(record.get('path', record.get('evidence')))
    assert actual['sha256'] == record['sha256'], actual['path']
    if 'bytes' in record:
        assert actual['bytes'] == record['bytes'], actual['path']

def common():
    config = SESSION / 'runtime-configuration.json'
    c = read(config)
    assert (c['status'], c['model'], c['reasoning']) == ('confirmed', 'gpt-6.1-sol', 'high')
    assert pin(config)['sha256'] == '72bc31860295263a903b02314ae959ac3eef0e2cba18d1edcab14a6c4ec866ad'
    return dict(role='reviewer', actor=ACTOR, task='IG-2B03', model=c['model'], reasoning=c['reasoning'], configuration_evidence=config.as_posix(), configuration_sha256=pin(config)['sha256'])

def write(name, data):
    with (ROOT / name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump({**common(), **data}, f, ensure_ascii=False, indent=2)
        f.write('\n')

def main():
    packet = read(SESSION / 'packet.json')
    assert pin('docs/work/queue.json')['sha256'] == packet['queue_sha256']
    for r in packet['files'] + packet['control_files']:
        verify(r)
    inputs = read('private/workflow/runs/IG-2B03/preparation-003-e285fb76/input-pins.json')
    for r in inputs['files'] + inputs['context_only_evidence'] + [inputs['dependency_reference']]:
        verify(r)
    verify({'path':(SESSION/'search-manifest.json').as_posix(), 'sha256':'86baa1381b15f6727368caf34dd713c907c8840769f44e282bd366897289436b'})
    toolchain = read('private/workflow/runs/IG-2B03/preparation-003-e285fb76/toolchain.json')
    assert os.environ['PYTHONPATH'] == toolchain['process_pythonpath']
    assert toolchain['process_path_prefix'].lower() in [p.lower() for p in os.environ['PATH'].split(';')]
    verify(toolchain['python_executable'])
    for name, data in toolchain['native'].items():
        verify(data['executable'])
        assert pin(shutil.which(name))['sha256'] == data['executable']['sha256']
    for library, version in toolchain['libraries'].items():
        assert importlib.metadata.version(library) == version
    refs = read(SESSION / 'references.json')
    for r in list(refs['dependencies'].values()) + [refs['findings'], refs['prior_delivery'], refs['repair_claim'], read(SESSION / 'delivery-reference.json')]:
        verify(r)
    task = read(SESSION / 'task.json')
    queue = read('docs/work/queue.json')
    tasks = queue['tasks']
    selected = {t['id']: t for t in tasks if t['id'] in ['IG-2B03', 'IG-2B02']}
    assert {k:v for k,v in selected['IG-2B03'].items() if k != 'events'} == task
    assert selected['IG-2B02']['status'] == 'done'
    for key in ['scope', 'evidence']:
        verify(task['repair_authorization'][key])
    old_delivery = read(OLD / 'delivery.json')
    delivery = read(NEW / 'delivery.json')
    manifest = read(NEW / 'delivery-manifest.json')
    assert delivery['criteria'] == task['acceptance']
    assert delivery['artifacts'][:len(old_delivery['artifacts'])] == old_delivery['artifacts']
    assert delivery['artifacts'][:-1] == manifest['artifacts']
    assert delivery['artifacts'][-1] == pin(NEW / 'delivery-manifest.json')
    blocked_path = 'private/workflow/runs/IG-2B03/recovery-20261015-search-01/preserve-manifest.json'
    verify(read(NEW / 'preservation-report.json')['blocked_manifest'])
    groups = {
        'current_delivery': delivery['artifacts'],
        'blocked_attempt': read(blocked_path)['artifacts'],
        'accepted_dependency': read(refs['dependencies']['IG-2B02']['evidence'])['artifacts'],
        'prior_review': read(refs['findings']['evidence'])['review_artifacts'],
    }
    for records in groups.values():
        for r in records:
            verify(r)
    verify({'path':task['continuation_authorization']['blocked_evidence'], 'sha256':task['continuation_authorization']['blocked_sha256']})
    old = read(OLD / 'region-ledger.json')
    new = read(NEW / 'region-ledger.json')
    provenance = ['actor', 'configuration_evidence', 'configuration_sha256', 'repair_provenance']
    differences = []
    for a, b in zip(old['regions'], new['regions'], strict=True):
        x, y = copy.deepcopy(a), copy.deepcopy(b)
        ar, br = x.pop('raw_cross_references'), y.pop('raw_cross_references')
        assert x == y, a['region']['id']
        assert br[:len(ar)] == ar
        if ar != br:
            additions = br[len(ar):]
            assert additions and all(s in ' '.join(a['raw_extracted_text'].split()) for s in additions)
            differences.append({'region_id':a['region']['id'], 'key':a['region']['key'], 'pdf_page':a['pdf_page'], 'additions':additions, 'text':pin(a['evidence']['text']['path'])})
    for obj in [old, new]:
        for k in provenance:
            obj.pop(k, None)
        for r in obj['regions']:
            r.pop('raw_cross_references')
    assert old == new
    a, b = read(OLD / 'continuations.json'), read(NEW / 'continuations.json')
    ar, br = a.pop('unfollowed_references'), b.pop('unfollowed_references')
    assert br[:len(ar)] == ar
    assert br[len(ar):] == [{'region_id':d['region_id'], 'raw':d['additions']} for d in differences]
    assert len(a['literal_continuations']) == 4
    for obj in [a,b]:
        for k in provenance:
            obj.pop(k, None)
    assert a == b
    audit = read(NEW / 'reference-audit.json')
    assert len(differences) == 7 and sum(len(d['additions']) for d in differences) == 8
    assert len(audit['region_audit']) == 135
    for change in audit['changes']:
        text = Path(change['text_artifact']['path']).read_text(encoding='utf-8')
        verify(change['text_artifact'])
        for offset in change['text_offsets']:
            assert text[offset['start']:offset['end']] == offset['exact_text_slice']
            assert ' '.join(offset['exact_text_slice'].split()) == offset['literal']
    report = dict(format='wgc-independent-r01-verification-1', utc=datetime.now(timezone.utc).isoformat(), outcome='pass', verified_groups={k:len(v) for k,v in groups.items()}, packet=pin(SESSION/'packet.json'), queue_sha256=packet['queue_sha256'], original_artifact_prefix_count=len(old_delivery['artifacts']), changed_regions=differences, ledger_rows=135, components=22, literal_continuations=4, full_structures_unchanged_except_reference_additions_and_provenance=True, semantic_acceptance_granted=False)
    write('end-integrity.json' if '--final' in sys.argv else 'hash-structure-verification.json', report)
    print(json.dumps({k:report[k] for k in ['outcome','verified_groups','original_artifact_prefix_count','ledger_rows']}))

if __name__ == '__main__':
    main()
