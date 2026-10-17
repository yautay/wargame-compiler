"""Independent full input/source binding inventory and reproducibility audit."""
import base64
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
import yaml
from yaml.nodes import MappingNode, SequenceNode

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from wgc.export.source import build
from wgc.export.storage import publish
from wgc.inputs.snapshot import verify_snapshot

INPUT = ROOT / 'private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df'
SOURCE = ROOT / 'private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008'
IMPORTED = ROOT / 'private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json'
PACKAGE = ROOT / 'private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc'
SEED = ROOT / 'private/workflow/runs/IG-1D/preflight-20261013/initial-registry.json'
started = datetime.now(timezone.utc)
clock = time.perf_counter()

def read(p):
    return json.loads(p.read_bytes())

def canonical(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def escape(key):
    return str(key).replace('~', '~0').replace('/', '~1')

def at(value, pointer):
    for part in pointer.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value

def field_ledger(node, pointer='', key_mark=None):
    a, b = node.start_mark, node.end_mark
    yield {'field': pointer, 'tag': node.tag, 'line': a.line + 1, 'column': a.column + 1,
        'end_line': b.line + 1, 'end_column': b.column + 1,
        'character_start': a.index, 'character_end': b.index,
        'key_line': key_mark.line + 1 if key_mark else None, 'key_column': key_mark.column + 1 if key_mark else None}
    if isinstance(node, MappingNode):
        for key, child in node.value:
            yield from field_ledger(child, pointer + '/' + escape(key.value), key.start_mark)
    elif isinstance(node, SequenceNode):
        for i, child in enumerate(node.value):
            yield from field_ledger(child, pointer + '/' + str(i))

KINDS = dict(rules='rule', terms='term', procedures='procedure', tables='table', relations='relation', ambiguities='ambiguity', changes='change', scenarios='question', questions='question', concepts='terminology', confusables='confusable')
def entity_ledger(document):
    output = []
    def visit(kind, value, pointer, parent=None):
        output.append((pointer, kind, parent, value))
        if kind in {'procedure', 'step'} and isinstance(value, dict):
            for name in ('steps', 'substeps', 'subprocedures'):
                if name in value:
                    assert isinstance(value[name], list)
                    for i, child in enumerate(value[name]):
                        visit('procedure' if name == 'subprocedures' else 'step', child, pointer + '/' + name + '/' + str(i), pointer)
    for key, value in document.items():
        pointer = '/' + escape(key)
        if key in KINDS:
            assert isinstance(value, list)
            for i, child in enumerate(value):
                visit(KINDS[key], child, pointer + '/' + str(i))
        else:
            output.append((pointer, 'auxiliary', None, value))
    return output

im, sm = read(INPUT / 'manifest.json'), read(SOURCE / 'manifest.json')
imh, smh = sha((INPUT / 'manifest.json').read_bytes()), sha((SOURCE / 'manifest.json').read_bytes())
assert imh == '67ac53869ea80ea4d84018e253a9033e48fe89823d0a9a397ab8fe41b91d33d5'
assert smh == '615b1ae1cbeebf894c7f8dbbb7c3f2bcb0819427a342b3fa05bc690c33b9eed8'
assert verify_snapshot(INPUT) == im and verify_snapshot(SOURCE) == sm
assert sm['selection']['identity_to_wgu_original'] == 'unknown'
imported = read(IMPORTED)
assert sha(IMPORTED.read_bytes()) == '2999d63c680b4c52a095e0edb18952c70eefdf4baf7c2e01481840cda18ca61a'
from wgc.wgu_adapter.importer import import_snapshot
fresh_imports = [import_snapshot(INPUT), import_snapshot(INPUT)]
for index, fresh in enumerate(fresh_imports, 1):
    assert canonical(fresh) + b'\n' == IMPORTED.read_bytes()
    with (RUN / ('import-' + str(index) + '.json')).open('xb') as stream:
        stream.write(canonical(fresh) + b'\n')
assert canonical(fresh_imports[0]) == canonical(fresh_imports[1])
assert len(im['files']) == len(imported['files'])
assert {f['path'] for f in im['files']} == {f['path'] for f in imported['files']}
assert len({f['path'] for f in imported['files']}) == len(imported['files'])
independent_status_counts = Counter()
independent_unknown_roots = []
independent_unknown_locations = set()
# An independent explicit field contract, not importer KNOWN/counters. Base WGU
# schema keys plus the pinned structural extensions observed during IG-1C.
field_contract = {
 'rule': 'id title section source when effect exceptions see keywords notes flags version digital refs extra body',
 'term': 'id en pl kind definition defined_at used_in refs',
 'procedure': 'id title steps subprocedures notes refs',
 'step': 'n text markers refs steps substeps',
 'table': 'id title tables notes refs data complete',
 'relation': 'id from to type when note status',
 'ambiguity': 'id title group scope quotes description readings recommendation strength resolution_source impact status resolution refs extra body',
 'change': 'id group from_version to_version kind place change effect rules refs source extra',
 'question': 'id question answer chain refs group given when then',
 'terminology': 'id source_term variants sense rules pl pl_forms rejected related status decided_by rationale evidence',
 'confusable': 'text', 'auxiliary': ''}

bundle = read(PACKAGE / 'source-ig.json')
registry = read(PACKAGE / 'identity-registry.json')
references = read(PACKAGE / 'references.json')
records = {(r['id'], r['revision_id']): r for r in bundle['records']}
snapshot = next(r for r in bundle['records'] if r['id'] == bundle['snapshot_id'])
selected = {s['id']: records[(s['id'], s['revision_id'])] for s in snapshot['data']['selected']}
# Independently compute every record/aspect hash and selected closure.
for r in bundle['records']:
    digest = sha(canonical({k: v for k, v in r.items() if k not in {'revision_id', 'content_hash'}}))
    assert r['content_hash'] == digest and r['revision_id'] == 'sha256:' + digest
    if r['record_type'] == 'node':
        for aspect in r['data']['aspects']:
            assert aspect['aspect_hash'] == sha(canonical({k: v for k, v in aspect.items() if k != 'aspect_hash'}))
for s in snapshot['data']['selected']:
    assert all(selected[s['id']][k] == s[k] for k in ['record_type', 'revision_id', 'content_hash'])
def check_refs(v):
    if isinstance(v, dict):
        if v.get('mode') in {'active', 'historical'}:
            target = selected[v['id']] if v['mode'] == 'active' else records[(v['id'], v['revision_id'])]
            assert target['record_type'] == v['record_type']
            if 'aspect_id' in v:
                assert any(a['aspect_id'] == v['aspect_id'] for a in target['data']['aspects'])
        for child in v.values():
            check_refs(child)
    elif isinstance(v, list):
        for child in v:
            check_refs(child)
check_refs(bundle)
assert all(r['record_type'] not in {'review', 'coverage', 'region', 'evidence'} for r in selected.values())
assert snapshot['data']['state'] == 'draft'
assert snapshot['data']['assessments']['executable']['status'] == 'blocked'
assert snapshot['data']['assessments']['semantic_review_refs'] == []
assert snapshot['data']['assessments']['coverage_refs'] == []
active_entries = {e['id']: e for e in registry['entries'] if e['active']}
observations = defaultdict(list)
binding_observations = defaultdict(list)
for e in active_entries.values():
    assert e['origin_key'].startswith('allocation:')
    for observation in e['observations']:
        o = observation['origin']
        if e['kind'] == 'binding':
            binding_observations[(o['input_snapshot_id'], o['relative_path'], o['field_locator'])].append((e, observation))
        elif e['kind'] not in {'source', 'derived_relation'}:
            observations[(o['relative_path'], o['field_locator'], e['kind'])].append((e, observation))
documents = {}
file_ledger = []
total_fields = 0
kind_counts = Counter()
all_unknown = []
for entry, f in zip(im['files'], imported['files']):
    assert entry['path'] == f['path']
    if entry['availability'] == 'missing':
        assert f['records'] == [] and f['fields'] == []
        file_ledger.append({'path': entry['path'], 'availability': 'missing', 'records': [], 'fields': []})
        continue
    raw = (INPUT / entry['blob_path']).read_bytes()
    assert sha(raw) == entry['sha256'] == f['sha256'] and len(raw) == entry['bytes'] == f['bytes']
    assert base64.b64decode(f['raw_base64'], validate=True) == raw
    if Path(entry['path']).suffix.lower() in {'.yaml', '.yml'}:
        text = raw.decode('utf-8-sig')
        document = yaml.safe_load(text)
        fields = list(field_ledger(yaml.compose(text, Loader=yaml.SafeLoader)))
        assert fields == f['fields'] and document == f['document']
        expected_entities = entity_ledger(document)
    else:
        document, fields = None, []
        expected_entities = [('', 'auxiliary', None, None)]
    documents[(im['snapshot_id'], entry['path'])] = document
    actual = {(r['field'], r['kind']): r for r in f['records']}
    assert len(actual) == len(f['records']) == len(expected_entities)
    full_fields = {x['field'] for x in fields}
    row_records = []
    for pointer, kind, parent, value in expected_entities:
        r = actual[(pointer, kind)]
        assert r['value'] == value and r['parent_field'] == parent
        expected_status = 'raw' if kind == 'auxiliary' else 'processed'
        assert r['status'] == expected_status
        independent_status_counts[expected_status] += 1
        unknown_roots = sorted(pointer + '/' + escape(k) for k in value
                               if k not in field_contract[kind].split()) if isinstance(value, dict) else []
        assert sorted(r['unknown_field_paths']) == unknown_roots
        for unknown in unknown_roots:
            assert unknown in full_fields
            independent_unknown_roots.append({'file': entry['path'], 'field': unknown,
                'value_sha256': sha(canonical(at(document, unknown)))})
            independent_unknown_locations.update((entry['path'], p) for p in full_fields
                                                if p == unknown or p.startswith(unknown + '/'))

        matches = observations[(entry['path'], pointer, kind)]
        assert len(matches) == 1
        e, observation = matches[0]
        assert observation['value'] == value and observation['external_id'] == r['external_id']
        assert observation['origin']['input_snapshot_id'] == im['snapshot_id']
        assert observation['origin']['input_sha256'] == entry['sha256']
        node = selected[e['id']]
        assert node['record_type'] == 'node'
        keys = sorted(value) if isinstance(value, dict) and value else ['raw']
        assert {a['aspect_id'] for a in node['data']['aspects']} == {'field-' + k.encode('utf-8').hex() for k in keys}
        assert all(a['statement']['knowledge'] == 'unknown' and a['statement']['evidence_refs'] == [] and a['execution_impact'] == 'blocking' for a in node['data']['aspects'])
        assert node['data']['semantic_groups'] == []
        coordinates = [pointer] + [pointer + '/' + escape(k) for k in sorted(value)] if isinstance(value, dict) else [pointer]
        for coordinate in coordinates:
            expected_value = at(document, coordinate) if document is not None else None
            bindings = binding_observations[(im['snapshot_id'], entry['path'], coordinate)]
            assert bindings
            assert any(o['value'] == expected_value and any(ref['id'] == e['id'] for ref in selected[b['id']]['data']['ig_refs']) for b, o in bindings)
        for unknown in r['unknown_field_paths']:
            assert unknown in full_fields
            all_unknown.append({'file': entry['path'], 'field': unknown, 'value_sha256': sha(canonical(at(document, unknown)))})
        row_records.append({'field': pointer, 'kind': kind, 'identity': e['id'], 'origin_key': e['origin_key'], 'parent_field': parent, 'value_sha256': sha(canonical(value))})
        kind_counts[kind] += 1
    # Every field is covered by at least a whole-file binding carrying exact
    # document values, with all deeper values/marks independently retained.
    whole = binding_observations[(im['snapshot_id'], entry['path'], '')]
    assert whole and any(o['value'] == document for e, o in whole)
    for field in fields:
        assert at(document, field['field']) == at(f['document'], field['field'])
    total_fields += len(fields)
    file_ledger.append({'path': entry['path'], 'availability': 'available', 'sha256': sha(raw), 'bytes': len(raw), 'records': row_records, 'fields': fields})
# Independently verify each binding against the exact manifest or document
# subtree; no registry counters can establish correctness of coordinates.
manifest_documents = {im['snapshot_id']: (im, imh), sm['snapshot_id']: (sm, smh)}
binding_ledger = []
for e in active_entries.values():
    if e['kind'] != 'binding':
        continue
    b = selected[e['id']]
    assert b['record_type'] == 'origin_binding'
    for observation in e['observations']:
        origin = observation['origin']
        assert b['data']['field_locator'] == 'json-pointer:' + origin['field_locator']
        assert all(b['data'][k] == origin[k] for k in ['input_snapshot_id', 'input_sha256', 'relative_path'])
        if origin['relative_path'] == 'manifest.json':
            manifest, digest = manifest_documents[origin['input_snapshot_id']]
            assert origin['input_sha256'] == digest
            expected = at(manifest, origin['field_locator'])
        else:
            entry = next(x for x in im['files'] if x['path'] == origin['relative_path'])
            assert origin['input_sha256'] == entry['sha256']
            doc = documents[(origin['input_snapshot_id'], origin['relative_path'])]
            expected = at(doc, origin['field_locator']) if doc is not None else None
        assert observation['value'] == expected
        assert b['data']['mapping_status'] == 'exact'
        binding_ledger.append({'identity': e['id'], 'origin': origin, 'target_refs': b['data']['ig_refs'], 'value_sha256': sha(canonical(expected))})
assert {k: independent_status_counts[k] for k in ['processed','raw','error']} == imported['record_counts']
assert sum(kind_counts.values()) == imported['record_total']
assert dict(kind_counts) == imported['kind_counts']
assert len(observations) == sum(kind_counts.values())
assert not [g for g in registry['gaps'] if g['active']]
assert registry['input_context']['input_manifest_sha256'] == imh and registry['input_context']['source_manifest_sha256'] == smh
assert references['semantic_acceptance'] == references['executable_readiness'] == 'not_granted'
assert all(d['semantic_acceptance'] == 'not_granted' for d in references['diagnostics'])
assert all(r['data']['started_utc'] is None and r['data']['ended_utc'] is None and r['data']['model'] is None for r in selected.values() if r['record_type'] == 'run')
print('Independent file/record/field/binding/hash inventory passed.', flush=True)
seed = read(SEED)
first = build(imported, seed, source_manifest=sm, input_manifest_sha256=imh, source_manifest_sha256=smh)
for name, key in [('source-ig.json', 'bundle'), ('identity-registry.json', 'registry'), ('references.json', 'references')]:
    assert canonical(first[key]) + b'\n' == (PACKAGE / name).read_bytes(), name
print('Fresh seeded complete transform equals frozen package.', flush=True)
second = build(imported, first['registry'], previous_bundle=first['bundle'], source_manifest=sm, input_manifest_sha256=imh, source_manifest_sha256=smh)
assert all(canonical(first[k]) == canonical(second[k]) for k in ['bundle', 'registry', 'references'])
print('Repeated complete transform equals first canonical result.', flush=True)
publication_one = publish(first, RUN / 'packages', operation_evidence={'review_actor': 'ig1e-independent-reviewer-20261013T150750Z'})
publication_two = publish(second, RUN / 'packages', operation_evidence={'review_actor': 'ig1e-independent-reviewer-20261013T150750Z', 'repeat': True})
assert publication_one['package'] == publication_two['package']
assert publication_one['manifest'] == publication_two['manifest'] == read(PACKAGE / 'manifest.json')
assert publication_one['operation'] != publication_two['operation']
for operation in [publication_one['operation'], publication_two['operation']]:
    assert read(Path(operation))['started_utc'] is not None
assert verify_snapshot(INPUT) == im and verify_snapshot(SOURCE) == sm
report = {'independent_record_status_counts': {k: independent_status_counts[k] for k in ['processed','raw','error']}, 'independent_unknown_root_count': len(independent_unknown_roots), 'independent_unknown_location_count': len(independent_unknown_locations), 'independent_unknown_roots': independent_unknown_roots, 'independent_unknown_field_locations': [{'file': f, 'field': p} for f,p in sorted(independent_unknown_locations)], 'two_fresh_imports_match_accepted_bytes': True, 'result': 'pass', 'start_utc': started.isoformat(), 'end_utc': datetime.now(timezone.utc).isoformat(), 'wall_seconds': time.perf_counter() - clock,
    'independent_record_count': sum(kind_counts.values()), 'independent_field_count': total_fields, 'kind_counts': dict(kind_counts), 'manifest_entries': len(file_ledger), 'available_files': sum(x['availability'] == 'available' for x in file_ledger), 'missing_sources': sum(x['availability'] == 'missing' for x in file_ledger),
    'source_graph_records': len(bundle['records']), 'binding_count': len(binding_ledger), 'unknown_locations': all_unknown,
    'ledger': file_ledger, 'binding_ledger': binding_ledger, 'publications': [publication_one, publication_two],
    'two_complete_outputs_and_packages_byte_identical': True, 'fresh_seeded_transform_matches_frozen': True,
    'identity_to_wgu_original': 'unknown', 'semantic_acceptance_granted': False, 'publisher_source_coverage_granted': False, 'executable_readiness_granted': False,
    'tokens': None, 'cost': None, 'operator_time_seconds': None,
    'oracle': 'Exact manifest/raw bytes; independent YAML load/compose; explicit collection/nesting inventory; every registry observation and binding subtree independently located; independently computed hashes and active/historical closure; two actual full transforms/publications.'}
with (RUN / 'independent-accounting.json').open('x', encoding='utf-8') as stream:
    json.dump(report, stream, indent=2, ensure_ascii=False)
    stream.write('\n')
print(json.dumps({k: v for k, v in report.items() if k not in {'ledger', 'binding_ledger', 'unknown_locations', 'publications', 'independent_unknown_roots', 'independent_unknown_field_locations'}}), flush=True)
