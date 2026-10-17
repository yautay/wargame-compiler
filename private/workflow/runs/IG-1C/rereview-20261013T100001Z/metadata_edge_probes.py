"""Check mandatory manifest metadata after the fixture contract correction."""
import base64

import pytest

from wgc.wgu_adapter.importer import finish, import_bytes


@pytest.mark.parametrize('raw,missing', [
    (b'game: {id: synthetic}\n', ['/schema']),
    (b'schema: wgu/kb@1\n', ['/game']),
    (b'novel: {retained: true}\n', ['/schema', '/game']),
])
def test_missing_mandatory_manifest_metadata_is_located_and_raw_retained(raw, missing):
    f = import_bytes(raw, 'kb/manifest.yaml')
    result = finish([f])
    assert result['record_counts'] == {'processed': 0, 'raw': 1, 'error': len(missing)}
    assert base64.b64decode(f['raw_base64']) == raw
    for pointer in missing:
        d = next(d for d in f['diagnostics'] if d['field'] == pointer)
        assert d['code'] == 'missing_field'
        assert (d['line'], d['column']) == (1, 1)
        r = next(r for r in f['records'] if r['field'] == pointer)
        assert r['value'] is None and r['status'] == 'error'
