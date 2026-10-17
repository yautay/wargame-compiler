"""Synthetic full snapshot/import/export integration, with independently known inputs."""
import base64
import copy
import hashlib
import json
from pathlib import Path

import pytest

from wgc.contracts.source import canonical_bytes, seal_record
from wgc.export.source import build, historical, validate_export
from wgc.export.storage import publish
from wgc.inputs.snapshot import freeze_inputs, verify_snapshot
from wgc.wgu_adapter.importer import import_snapshot


def fixture(tmp_path, broken=False):
    game, registry = tmp_path/'game', tmp_path/'registry'
    (game/'kb').mkdir(parents=True); registry.mkdir()
    raw = {
        'wgu.yaml': b'name: synthetic\neditions: [invented-4, invented-5]\n',
        'kb/extensions.yaml': json.dumps({'meta': {'unrecognized': [1, {'a/b': 'kept'}]},
            'rules': [{'id': 'R-A', 'title': 'Synthetic rule', 'refs': ['R-Missing.x'],
                       'version': {'introduced': 'invented-4', 'changed_in': 'invented-5'},
                       'x-extra': {'nested': [0, {'a/b': 'future'}]}}],
            'terms': [{'en': 'Same', 'definition': 'identical'}, {'en': 'Same', 'definition': 'identical'}],
            'procedures': [{'id': 'P-A', 'title': 'Synthetic procedure', 'steps': [{'n': 1, 'text': 'Opaque step'}]}]}).encode(),
        'kb/notes.bin': b'\x00\xff\r\nopaque\x80'
    }
    if broken: raw['kb/broken.yaml'] = b'rules: [\n'
    for name, data in raw.items(): (game/name).write_bytes(data)
    (registry/'rulebook.pdf').write_bytes(b'%PDF-invented-source')
    (registry/'provenance.json').write_bytes(b'{"identity":"unknown"}')
    def entry(root, name, role):
        data = (root/name).read_bytes()
        return {'relative_path': name, 'role': role, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    request = {'game_root': str(game), 'registry_root': str(registry),
        'game_files': [entry(game, n, 'game_config' if n=='wgu.yaml' else 'kb') for n in sorted(raw)],
        'registry_files': [entry(registry,'rulebook.pdf','selected_rulebook'), entry(registry,'provenance.json','provenance')],
        'historical_configured_sources': [{'relative_path':'docs/missing.pdf','role':'configured_source','availability':'missing'}],
        'selection': {'source_id':'synthetic-source','role':'rulebook','edition_label':'invented-5',
            'edition_basis':'Synthetic operator-selected fixture','selected_path':'rulebook.pdf',
            'sha256':hashlib.sha256((registry/'rulebook.pdf').read_bytes()).hexdigest(),
            'identity_to_wgu_original':'unknown','semantic_acceptance':'not_granted'}}
    frozen = freeze_inputs(request, tmp_path/'inputs', tmp_path/'sources')
    imported = import_snapshot(frozen['input_snapshot'])
    source = verify_snapshot(frozen['source_snapshot'])
    kwargs = {'namespace':'synthetic','source_manifest':source,
        'input_manifest_sha256':hashlib.sha256((Path(frozen['input_snapshot'])/'manifest.json').read_bytes()).hexdigest(),
        'source_manifest_sha256':hashlib.sha256((Path(frozen['source_snapshot'])/'manifest.json').read_bytes()).hexdigest()}
    return raw, frozen, imported, build(imported, **kwargs), kwargs


def test_complete_bytes_records_unknown_fields_and_missing_file_accounting(tmp_path):
    raw, frozen, imported, result, _ = fixture(tmp_path)
    files = {f['path']:f for f in imported['files']}
    assert set(files) == set(raw) | {'docs/missing.pdf'}
    for name, data in raw.items():
        assert base64.b64decode(files[name]['raw_base64']) == data
        assert files[name]['sha256'] == hashlib.sha256(data).hexdigest()
    assert files['docs/missing.pdf']['raw_base64'] is None and files['docs/missing.pdf']['records'] == []
    # Known invented input: five entities; four whole metadata/binary observations.
    assert imported['record_counts'] == {'processed':5, 'raw':4, 'error':0}
    rule = next(r for r in files['kb/extensions.yaml']['records'] if r['kind']=='rule')
    assert '/rules/0/x-extra' in rule['unknown_field_paths']
    node = next(e for e in result['registry']['entries'] if e['active'] and e['kind']=='rule')
    assert node['observations'][0]['value']['x-extra'] == {'nested':[0,{'a/b':'future'}]}
    assert any(f['field']=='/rules/0/x-extra/nested/1/a~1b' for f in files['kb/extensions.yaml']['fields'])
    assert len([g for g in result['registry']['gaps'] if g['active']]) == 1


def test_repeat_import_and_actual_publication_are_byte_identical(tmp_path):
    _, frozen, imported, first, kwargs = fixture(tmp_path)
    repeated_import = import_snapshot(frozen['input_snapshot'])
    assert canonical_bytes(imported) == canonical_bytes(repeated_import)
    second = build(repeated_import, first['registry'], previous_bundle=first['bundle'], **kwargs)
    for key in ['bundle','registry','references']: assert canonical_bytes(first[key]) == canonical_bytes(second[key])
    one = publish(first, tmp_path/'exports', operation_evidence={'task':'synthetic-import-acceptance'})
    two = publish(second, tmp_path/'exports', operation_evidence={'task':'synthetic-import-acceptance','repeat':True})
    assert one['package']==two['package'] and one['manifest']==two['manifest']
    assert one['operation']!=two['operation']
    assert json.loads(Path(one['operation']).read_bytes())['started_utc'] is not None


def test_structurally_sealed_snapshot_retains_gaps_history_and_all_readiness_boundaries(tmp_path):
    _, _, _, result, _ = fixture(tmp_path)
    original = copy.deepcopy(result['bundle'])
    draft = next(r for r in original['records'] if r['id']==original['snapshot_id'])
    record = copy.deepcopy(draft); record['data']['state']='sealed'
    record['id']='wgc-snapshot:'+hashlib.sha256(canonical_bytes(record['data'])).hexdigest()
    record['lineage_refs']=[historical(draft)]
    sealed = seal_record(record)
    bundle = {**original,'snapshot_id':sealed['id'],'records':original['records']+[sealed]}
    validation = validate_export(bundle)
    assert result['bundle']==original and draft in bundle['records']
    assert sealed['data']['selected']==draft['data']['selected']
    assert sealed['data']['conflict_refs']==draft['data']['conflict_refs'] and sealed['data']['conflict_refs']
    assert sealed['data']['assessments']==draft['data']['assessments']
    assert validation['structural_validation']=='passed'
    assert validation['semantic_acceptance_granted'] is False and validation['executable']['status']=='blocked'
    assert sealed['data']['assessments']['coverage_refs']==sealed['data']['assessments']['semantic_review_refs']==[]
    assert any(r['record_type']=='gap' and r['data']['kind']=='missing_source' for r in bundle['records'])


def test_mixed_edition_claims_and_unresolved_references_never_become_approval(tmp_path):
    _, _, imported, result, _ = fixture(tmp_path)
    assert imported['semantic_acceptance']=='not_granted'
    rule = next(r for f in imported['files'] for r in f['records'] if r['kind']=='rule')
    assert rule['value']['version']=={'introduced':'invented-4','changed_in':'invented-5'}
    assert any(d['target_status']=='unresolved' for d in result['references']['diagnostics'])
    assert result['registry']['input_context']['source_manifest']['selection']['identity_to_wgu_original']=='unknown'
    profile=next(r for r in result['bundle']['records'] if r['record_type']=='profile')
    assert all(c['knowledge']=='unknown' for c in profile['data']['compatibility_decisions'])
    assert all(r['record_type'] not in {'review','coverage','evidence','region'} for r in result['bundle']['records'])


def test_malformed_file_stays_an_error_with_exact_raw_bytes_and_export_gap(tmp_path):
    raw, _, imported, result, _ = fixture(tmp_path, broken=True)
    broken=next(f for f in imported['files'] if f['path']=='kb/broken.yaml')
    assert base64.b64decode(broken['raw_base64'])==raw['kb/broken.yaml']
    assert broken['status']=='error' and broken['records'][0]['status']=='error'
    assert imported['record_counts']=={'processed':5,'raw':4,'error':1}
    assert any(g['active'] and 'Malformed import' in g['reason'] for g in result['registry']['gaps'])
