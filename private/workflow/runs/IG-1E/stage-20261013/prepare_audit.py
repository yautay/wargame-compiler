"""Extend the preserved raw-input oracle with IG-1E independent set/count controls."""
from pathlib import Path
import hashlib,json
ROOT=Path.cwd();SCRIPT=Path(__file__).resolve().parent
source=Path('private/workflow/runs/IG-1D/repair-02-20261013/accounting.py')
target=SCRIPT/'accounting.py'
output=ROOT/'private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013'
output.mkdir(parents=True,exist_ok=False)
text=source.read_text(encoding='utf-8')
text=text.replace('RUN = Path(__file__).resolve().parent', "RUN = ROOT / 'private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013'")
imports='''from wgc.wgu_adapter.importer import import_snapshot
fresh_imports = [import_snapshot(INPUT), import_snapshot(INPUT)]
for index, fresh in enumerate(fresh_imports, 1):
    assert canonical(fresh) + b'\\n' == IMPORTED.read_bytes()
    with (RUN / ('import-' + str(index) + '.json')).open('xb') as stream:
        stream.write(canonical(fresh) + b'\\n')
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
'''
needle="assert sha(IMPORTED.read_bytes()) == '2999d63c680b4c52a095e0edb18952c70eefdf4baf7c2e01481840cda18ca61a'"
assert text.count(needle)==1
text=text.replace(needle,needle+'\n'+imports)
needle="        assert r['value'] == value and r['parent_field'] == parent"
extra='''
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
'''
assert text.count(needle)==1;text=text.replace(needle,needle+extra)
needle="assert sum(kind_counts.values()) == imported['record_total']"
text=text.replace(needle,"assert {k: independent_status_counts[k] for k in ['processed','raw','error']} == imported['record_counts']\n"+needle)
needle="report = {'result': 'pass'"
assert text.count(needle)==1
text=text.replace(needle,"report = {'independent_record_status_counts': {k: independent_status_counts[k] for k in ['processed','raw','error']}, 'independent_unknown_root_count': len(independent_unknown_roots), 'independent_unknown_location_count': len(independent_unknown_locations), 'independent_unknown_roots': independent_unknown_roots, 'independent_unknown_field_locations': [{'file': f, 'field': p} for f,p in sorted(independent_unknown_locations)], 'two_fresh_imports_match_accepted_bytes': True, 'result': 'pass'")
with target.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
with (SCRIPT/'oracle-extension.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump({'source':source.as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'target':target.relative_to(ROOT).as_posix(),'target_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
 'retained_assertions':'All original full-input field/binding/hash/revision/canonical transformation/publication assertions retained.',
 'added_controls':['Complete manifest/import path-set and uniqueness equality','Two actual complete fresh imports equal accepted raw bytes','Independent processed/raw/error status classification','Independent known-field contract and de-duplicated unknown root/subtree location counts'],
 'assertions_removed':False},f,indent=2);f.write('\n')
print('Fresh IG-1E full-input oracle prepared; prior oracle and accepted outputs unchanged.')
