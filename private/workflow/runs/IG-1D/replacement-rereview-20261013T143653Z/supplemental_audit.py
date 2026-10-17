"""Independent unknown-location denominator and reference diagnostics oracle."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
import yaml

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
started = datetime.now(timezone.utc)
clock = time.perf_counter()
INPUT = ROOT / 'private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df'
IMPORTED = ROOT / 'private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json'
CURRENT = ROOT / 'private/workflow/runs/IG-1D/repair-01-20261013/full-export-accounting-final.json'

def read(p): return json.loads(p.read_bytes())
def canon(v): return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
def sha(raw): return hashlib.sha256(raw).hexdigest()
def esc(k): return str(k).replace('~', '~0').replace('/', '~1')
def at(v, p):
    for k in p.split('/')[1:]:
        k = k.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v

# Declare the accepted record vocabulary locally; do not import implementation counters,
# importer KNOWN, diagnose, reconcile, or any transformation result as expected output.
known = {
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
collections = dict(rules='rule', terms='term', procedures='procedure', tables='table',
    relations='relation', ambiguities='ambiguity', changes='change', scenarios='question',
    questions='question', concepts='terminology', confusables='confusable')

assert sha(IMPORTED.read_bytes()) == '2999d63c680b4c52a095e0edb18952c70eefdf4baf7c2e01481840cda18ca61a'
assert sha(CURRENT.read_bytes()) == 'b1cc378954c8fc930e2bd7dc5638a23805177820a083a5966b3f99f512f07ba1'
package = Path(read(CURRENT)['package']['package'])
manifest = read(package / 'manifest.json')
for a in manifest['files']:
    assert sha((package / a['path']).read_bytes()) == a['sha256']
registry, references = read(package / 'identity-registry.json'), read(package / 'references.json')
im, imported = read(INPUT / 'manifest.json'), read(IMPORTED)
assert len(im['files']) == len(imported['files'])
active = {e['id']: e for e in registry['entries'] if e['active']}
aliases = defaultdict(set)
origins = defaultdict(set)
for identity, e in active.items():
    for alias in e['external_ids']: aliases[alias].add(identity)
    if e['kind'] in known:
        for o in e['observations']:
            origins[(o['origin']['relative_path'], o['origin']['field_locator'], e['kind'])].add(identity)

records = []
unknown = []
for entry, f in zip(im['files'], imported['files']):
    assert entry['path'] == f['path']
    if entry['availability'] == 'missing': continue
    raw = (INPUT / entry['blob_path']).read_bytes()
    assert sha(raw) == entry['sha256']
    if Path(entry['path']).suffix.lower() not in {'.yaml', '.yml'}: continue
    doc = yaml.safe_load(raw.decode('utf-8-sig'))
    actual = {(r['field'], r['kind']): r for r in f['records']}
    def visit(kind, value, pointer):
        r = actual[(pointer, kind)]
        assert r['value'] == value
        expected_unknown = [pointer + '/' + esc(k) for k in value if k not in known[kind].split()] if isinstance(value, dict) else []
        assert set(expected_unknown) == set(r['unknown_field_paths'])
        for p in expected_unknown:
            deeper = [field for field in f['fields'] if field['field'] == p or field['field'].startswith(p + '/')]
            assert deeper
            unknown.append({'file': entry['path'], 'record_field': pointer, 'kind': kind,
                'unknown_root': p, 'value_sha256': sha(canon(at(doc, p))),
                'locations': [{**field, 'value_sha256': sha(canon(at(doc, field['field'])))} for field in deeper]})
        origin = dict(input_snapshot_id=im['snapshot_id'], input_sha256=entry['sha256'], relative_path=entry['path'], field_locator=pointer)
        records.append((kind, value, origin, sorted(origins[(entry['path'], pointer, kind)])))
        if kind in {'procedure', 'step'} and isinstance(value, dict):
            for key in ['steps', 'substeps', 'subprocedures']:
                for i, child in enumerate(value.get(key, [])):
                    visit('procedure' if key == 'subprocedures' else 'step', child, pointer + '/' + key + '/' + str(i))
    for key, value in doc.items():
        if key in collections:
            for i, child in enumerate(value): visit(collections[key], child, '/' + esc(key) + '/' + str(i))
        else: visit('auxiliary', value, '/' + esc(key))

expected = []
edges = set()
for kind, value, origin, owners in records:
    if not isinstance(value, dict): continue
    declarations = []
    for key in ['refs', 'see']:
        raw = value.get(key)
        if key == 'refs' and isinstance(raw, list):
            declarations += [(key + '/' + str(i), s, 'navigation') for i, s in enumerate(raw) if isinstance(s, str)]
        elif isinstance(raw, str): declarations.append((key, raw, 'navigation'))
    if kind == 'relation': declarations += [(key, value[key], 'relation_candidate') for key in ['from', 'to'] if isinstance(value.get(key), str)]
    targets = {}
    for field, raw, role in declarations:
        candidates = aliases.get(raw, set()) | ({raw} if raw in active else set())
        status = 'resolved' if len(candidates) == 1 else 'ambiguous' if candidates else 'unresolved'
        item = {'owner_ids': owners, 'origin': origin, 'field': field, 'raw_locator': raw, 'role': role,
            'semantic_acceptance': 'not_granted', 'target_status': status,
            'target_ids': sorted(candidates) if status == 'resolved' else [],
            'candidate_ids': sorted(candidates) if status == 'ambiguous' else []}
        expected.append(item)
        targets[field] = item['target_ids']
        if role == 'navigation': edges.update((owner, target) for owner in owners for target in item['target_ids'])
    if kind == 'relation': edges.update((a, b) for a in targets.get('from', []) for b in targets.get('to', []))
comparison_keys = set(expected[0])
assert sorted(map(canon, expected)) == sorted(canon({k: d[k] for k in comparison_keys}) for d in references['diagnostics'])
graph = defaultdict(set)
for a, b in edges: graph[a].add(b); graph.setdefault(b, set())
def reachable(n):
    found, todo = set(), [n]
    while todo:
        v = todo.pop()
        if v in found: continue
        found.add(v); todo.extend(graph[v] - found)
    return found
# Mutual reachability supplies a separate SCC oracle, unlike production DFS passes.
reach = {n: reachable(n) for n in graph}
remaining = set(graph)
cycles = []
while remaining:
    n = min(remaining)
    group = {m for m in reach[n] if n in reach[m]}
    remaining -= group
    if len(group) > 1 or n in graph[n]: cycles.append(sorted(group))
assert sorted(cycles) == references['cycles']
report = {'result': 'pass', 'started_utc': started.isoformat(), 'ended_utc': datetime.now(timezone.utc).isoformat(),
    'wall_seconds': time.perf_counter() - clock, 'unknown_root_count': len(unknown),
    'unknown_field_container_location_count': sum(len(r['locations']) for r in unknown),
    'unknown_roots': unknown, 'independent_reference_diagnostic_count': len(expected),
    'reference_status_counts': dict(Counter(r['target_status'] for r in expected)),
    'diagnostics': expected, 'cycles': sorted(cycles), 'identity_count': len(registry['entries']),
    'active_identity_count': len(active), 'package_id': manifest['package_id'],
    'oracle': 'Raw manifest YAML, locally declared structural vocabulary, exact unknown subtrees and YAML coordinates; current identities and aliases, independently enumerated declarations and targets, independent mutual-reachability SCCs. No importer counters or reference implementation used as oracle.',
    'semantic_acceptance_granted': False, 'publisher_source_coverage_granted': False, 'executable_readiness_granted': False}
with (RUN / 'supplemental-accounting.json').open('x', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2); f.write('\n')
print(json.dumps({k: v for k, v in report.items() if k not in ['unknown_roots', 'diagnostics', 'cycles']}))
