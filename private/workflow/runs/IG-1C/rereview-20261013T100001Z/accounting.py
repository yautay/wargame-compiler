"""Inventory exact manifest bytes independently of adapter record/field counters."""
import base64
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import yaml
from yaml.nodes import MappingNode, SequenceNode

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'src'))
from wgc.wgu_adapter.importer import import_snapshot, canonical
from wgc.inputs.snapshot import verify_snapshot

RUN = Path(__file__).resolve().parent
INPUT = ROOT / 'private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df'
SOURCE = ROOT / 'private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008'
FROZEN_IMPORT = ROOT / 'private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json'
FROZEN_ACCOUNT = ROOT / 'private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/independent-accounting.json'
start = datetime.now(timezone.utc)
clock = time.perf_counter()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def escape(key):
    return str(key).replace('~', '~0').replace('/', '~1')

def locate(document, path):
    v = document
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        v = v[int(part)] if isinstance(v, list) else v[part]
    return v

def fields(node, path='', key_mark=None):
    mark, end = node.start_mark, node.end_mark
    yield {'field': path, 'tag': node.tag, 'line': mark.line + 1, 'column': mark.column + 1,
           'end_line': end.line + 1, 'end_column': end.column + 1,
           'character_start': mark.index, 'character_end': end.index,
           'key_line': key_mark.line + 1 if key_mark else None,
           'key_column': key_mark.column + 1 if key_mark else None}
    if isinstance(node, MappingNode):
        for key, child in node.value:
            yield from fields(child, path + '/' + escape(key.value), key.start_mark)
    elif isinstance(node, SequenceNode):
        for index, child in enumerate(node.value):
            yield from fields(child, path + '/' + str(index))

# Collection meaning comes from the pinned store/schema and explicit task
# terminology scope. It is deliberately independent of importer.COLLECTIONS.
COLLECTION_KINDS = dict(rules='rule', terms='term', procedures='procedure', tables='table',
                        relations='relation', ambiguities='ambiguity', changes='change',
                        scenarios='question', questions='question', concepts='terminology',
                        confusables='confusable')

def entities(document):
    result = []
    def visit(kind, value, path, parent=None):
        result.append((path, kind, parent, value))
        if kind in {'procedure', 'step'} and isinstance(value, dict):
            for name in ('steps', 'substeps', 'subprocedures'):
                if name in value:
                    assert isinstance(value[name], list)
                    for i, child in enumerate(value[name]):
                        visit('procedure' if name == 'subprocedures' else 'step', child, path + '/' + name + '/' + str(i), path)
    for key, value in document.items():
        path = '/' + escape(key)
        if key in COLLECTION_KINDS:
            assert isinstance(value, list)
            for index, item in enumerate(value):
                visit(COLLECTION_KINDS[key], item, path + '/' + str(index))
        else:
            result.append((path, 'auxiliary', None, value))
    return result

schema = json.loads((Path('C:/repo/wargame-utils/wgu/schemas/kb.schema.json')).read_text(encoding='utf-8'))
defs = schema['$defs']
unknown_locations = []

def unknowns(value, contract, path):
    if '$ref' in contract:
        contract = defs[contract['$ref'].split('/')[-1]]
    if isinstance(value, dict):
        properties = contract.get('properties', {})
        for key, item in value.items():
            p = path + '/' + escape(key)
            if key not in properties:
                yield p
                yield from unknowns(item, {}, p)
            else:
                yield from unknowns(item, properties[key], p)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from unknowns(item, contract.get('items', {}), path + '/' + str(index))

def safe_json(value):
    # Fail if this actual corpus contains any non-JSON scalar. Do not silently
    # normalize special YAML types to the product's representation.
    if isinstance(value, dict):
        assert all(isinstance(k, str) for k in value)
        for child in value.values():
            safe_json(child)
    elif isinstance(value, list):
        for child in value:
            safe_json(child)
    else:
        assert value is None or type(value) in (str, int, bool)

manifest_raw = (INPUT / 'manifest.json').read_bytes()
assert sha(manifest_raw) == '67ac53869ea80ea4d84018e253a9033e48fe89823d0a9a397ab8fe41b91d33d5'
manifest = json.loads(manifest_raw)
source_raw = (SOURCE / 'manifest.json').read_bytes()
assert sha(source_raw) == '615b1ae1cbeebf894c7f8dbbb7c3f2bcb0819427a342b3fa05bc690c33b9eed8'
source = json.loads(source_raw)
assert source['selection']['identity_to_wgu_original'] == 'unknown'
assert source['selection']['semantic_acceptance'] == 'not_granted'
source_ledger = []
for entry in source['files']:
    raw = (SOURCE / entry['blob_path']).read_bytes()
    assert len(raw) == entry['bytes'] and sha(raw) == entry['sha256']
    source_ledger.append(entry)
pin = json.loads((SOURCE / 'source-pin.json').read_bytes())
assert pin == {**source['selection'], 'source_snapshot_id': source['snapshot_id'], 'selection_purpose': 'new_ig_source'}

frozen = json.loads(FROZEN_IMPORT.read_bytes())
by_path = {f['path']: f for f in frozen['files']}
assert len(by_path) == len(frozen['files']) == len(manifest['files'])
assert set(by_path) == {f['path'] for f in manifest['files']}
ledger = []
all_kinds = Counter()
all_statuses = Counter()
total_fields = 0
samples = {}
for entry in manifest['files']:
    f = by_path[entry['path']]
    if entry['availability'] == 'missing':
        assert f['availability'] == 'missing' and f['raw_base64'] is None
        assert f['records'] == [] and f['fields'] == [] and f['document'] is None
        assert f['diagnostics'] == [{'code': 'missing_source', 'file': entry['path']}]
        ledger.append({'path': entry['path'], 'availability': 'missing', 'records': [], 'fields': [], 'unknown_locations': []})
        continue
    assert entry['blob_path'] == 'files/' + entry['path']
    raw = (INPUT / entry['blob_path']).read_bytes()
    assert len(raw) == entry['bytes'] == f['bytes']
    assert sha(raw) == entry['sha256'] == f['sha256']
    assert base64.b64decode(f['raw_base64'], validate=True) == raw
    if Path(entry['path']).suffix.lower() in ('.yml', '.yaml'):
        text = raw.decode('utf-8-sig')
        independent = yaml.safe_load(text)
        safe_json(independent)
        assert isinstance(independent, dict)
        assert independent == f['document']
        expected_fields = list(fields(yaml.compose(text, Loader=yaml.SafeLoader)))
        assert len({x['field'] for x in expected_fields}) == len(expected_fields)
        assert expected_fields == f['fields']
        expected_records = entities(independent)
        field_by_path = {x['field']: x for x in expected_fields}
        file_unknown = []
        for p, kind, parent, value in expected_records:
            definition = {'question': 'scenario'}.get(kind, kind)
            for unknown in unknowns(value, defs.get(definition, {}), p):
                assert unknown in field_by_path
                assert locate(f['document'], unknown) == locate(independent, unknown)
                file_unknown.append(unknown)
        total_fields += len(expected_fields)
    else:
        expected_records = [('', 'auxiliary', None, None)]
        expected_fields, file_unknown, field_by_path = [], [], {}
        assert f['document'] is None and f['fields'] == []
    actual_records = {(r['field'], r['kind']): r for r in f['records']}
    assert len(expected_records) == len(actual_records) == len(f['records'])
    record_ledger = []
    for p, kind, parent, value in expected_records:
        r = actual_records[(p, kind)]
        assert r['value'] == value and r['parent_field'] == parent
        assert r['location'] == field_by_path.get(p)
        assert r['external_id'] == (value.get('id') if kind != 'auxiliary' and isinstance(value, dict) else None)
        assert r['semantic_acceptance'] == 'not_granted' and r['executable_readiness'] == 'not_granted'
        if kind == 'question':
            assert r['mapping_status'] == 'evaluation_candidate'
        for key in ('refs', 'see'):
            if isinstance(value, dict) and key in value:
                assert {'field': p + '/' + key, 'value': value[key], 'role': 'navigation'} in r['navigation']
        for unknown in r['unknown_field_paths']:
            assert unknown in field_by_path
        record_ledger.append({'field': p, 'kind': kind, 'parent_field': parent, 'status': r['status'], 'external_id': r['external_id'], 'unknown_field_paths': r['unknown_field_paths'], 'value_sha256': sha(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode())})
        all_kinds[kind] += 1
        all_statuses[r['status']] += 1
        samples.setdefault(kind, {'file': entry['path'], 'field': p, 'raw_sha256': sha(raw), 'value': value, 'location': r['location'], 'mapping_status': r['mapping_status']})
    ledger.append({'path': entry['path'], 'availability': 'available', 'bytes': len(raw), 'sha256': sha(raw), 'records': record_ledger, 'fields': expected_fields, 'unknown_locations': file_unknown})
    unknown_locations.extend({'file': entry['path'], 'field': p} for p in file_unknown)
assert dict(all_kinds) == frozen['kind_counts']
assert sum(all_kinds.values()) == frozen['record_total']
assert {k: all_statuses[k] for k in ('processed', 'raw', 'error')} == frozen['record_counts']
executor = json.loads(FROZEN_ACCOUNT.read_bytes())
assert executor['independent_record_count'] == sum(all_kinds.values())
assert executor['independent_field_count'] == total_fields
assert executor['available_bytes'] == sum(x.get('bytes', 0) for x in ledger)
# Exercise native safe no-follow verification and independent production repeat.
assert verify_snapshot(INPUT) == manifest
assert verify_snapshot(SOURCE) == source
first = import_snapshot(INPUT)
second = import_snapshot(INPUT)
assert canonical(first) + b'\n' == FROZEN_IMPORT.read_bytes()
assert canonical(first) == canonical(second)
report = {'result': 'pass', 'start_utc': start.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter() - clock,
          'input_manifest_sha256': sha(manifest_raw), 'source_manifest_sha256': sha(source_raw),
          'manifest_entries': len(ledger), 'available_files': sum(x['availability'] == 'available' for x in ledger),
          'missing_files': sum(x['availability'] == 'missing' for x in ledger), 'available_bytes': sum(x.get('bytes', 0) for x in ledger),
          'record_count': sum(all_kinds.values()), 'kind_counts': dict(all_kinds), 'status_counts': dict(all_statuses),
          'field_count': total_fields, 'unknown_location_count': len(unknown_locations),
          'unknown_definition': 'Every mapping field without a definition in the pinned WGU schema, recursively including untyped payload/auxiliary/terminology mappings; more conservative than adapter KNOWN list.',
          'unknown_locations': unknown_locations, 'ledger': ledger, 'sample_mappings': samples,
          'source_ledger': source_ledger, 'identity_to_wgu_original': 'unknown', 'two_imports_byte_identical': True, 'matches_frozen_import': True,
          'expected_result_provenance': 'Exact snapshot manifest hashes/raw blobs; independent yaml.safe_load and yaml.compose; collection definitions pinned schema/store plus task terminology scope; no adapter counters used to enumerate expected records or fields.',
          'semantic_acceptance': 'not_granted', 'publisher_source_coverage': 'not_verified', 'executable_readiness': 'not_granted'}
with (RUN / 'independent-accounting.json').open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2, ensure_ascii=False)
    stream.write('\n')
print(json.dumps({k: v for k, v in report.items() if k not in {'ledger', 'sample_mappings', 'source_ledger', 'unknown_locations'}}))
