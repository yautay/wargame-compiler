"""Generate the static wgc-input-1 byte-manifest shape, not game semantics."""
import json
from pathlib import Path


def obj(properties, required=None):
    return {'type': 'object', 'properties': properties,
            'required': list(properties) if required is None else required,
            'additionalProperties': False}


def nullable(shape):
    return {'oneOf': [shape, {'type': 'null'}]}


text = {'type': 'string', 'minLength': 1}
sha = {'type': 'string', 'pattern': '^[0-9a-f]{64}$(?![\\s\\S])'}
identifier = {'type': 'string', 'pattern': '^sha256:[0-9a-f]{64}$(?![\\s\\S])'}
size = {'type': 'integer', 'minimum': 0}
file = obj({'path': text, 'role': {'enum': ['game_config', 'kb', 'configured_source', 'provenance', 'selected_rulebook']},
            'availability': {'enum': ['available', 'missing']}, 'bytes': nullable(size),
            'sha256': nullable(sha), 'blob_path': nullable(text), 'edition_label': nullable(text)})
file['allOf'] = [
    {'if': {'properties': {'availability': {'const': 'available'}}},
     'then': {'properties': {'bytes': size, 'sha256': sha, 'blob_path': text}}},
    {'if': {'properties': {'availability': {'const': 'missing'}}},
     'then': {'properties': {'bytes': {'type': 'null'}, 'sha256': {'type': 'null'},
                             'blob_path': {'type': 'null'}, 'role': {'const': 'configured_source'}}}},
]
selection = obj({'source_id': text, 'role': {'const': 'rulebook'}, 'edition_label': text,
                 'edition_basis': text, 'selected_path': text, 'sha256': sha,
                 'identity_to_wgu_original': {'const': 'unknown'}, 'semantic_acceptance': {'const': 'not_granted'}})
common = {'schema_version': {'const': 'wgc-input-1'}, 'snapshot_id': identifier,
          'origin_root': text, 'files': {'type': 'array', 'minItems': 1, 'items': {'$ref': '#/$defs/file'}}}
source = obj({**common, 'kind': {'const': 'source_snapshot'}, 'selection': {'$ref': '#/$defs/selection'}})
inputs = obj({**common, 'kind': {'const': 'input_snapshot'}, 'source_snapshot_id': identifier})
schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema', '$id': 'urn:wgc:ig:input:1',
          'title': 'WGC immutable input and source byte manifests',
          'description': 'Application append-only snapshots; original bytes, availability and explicitly unknown WGU source identity. No import, source meaning or executable acceptance.',
          '$defs': {'file': file, 'selection': selection}, 'oneOf': [inputs, source]}
Path('contracts/ig/input.schema.json').write_text(json.dumps(schema, indent=2) + '\n', encoding='utf-8')
