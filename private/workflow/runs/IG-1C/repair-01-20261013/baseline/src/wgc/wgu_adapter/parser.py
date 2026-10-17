"""Bounded safe YAML loading with duplicate-key rejection and field locations.

Raw bytes remain authoritative. Offsets below are Unicode character offsets,
not byte offsets. Aliases are expanded only within the node budget; recursive
aliases, merge keys, complex/non-string keys and unsupported safe types are
explicit errors rather than silently lossy conversions.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import date, datetime
import math

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode

MAX_BYTES = 16 * 1024 * 1024
MAX_NODES = 200_000
MAX_DEPTH = 100


class ParseError(ValueError):
    def __init__(self, message, path, mark=None, pointer=''):
        self.diagnostic = {'code': 'yaml_error', 'message': message, 'file': path,
                           'field': pointer, 'line': mark.line + 1 if mark else None,
                           'column': mark.column + 1 if mark else None}
        super().__init__(f'{path}:{self.diagnostic["line"]}:{self.diagnostic["column"]}: {message}')


class StrictSafeLoader(yaml.SafeLoader):
    """No unsafe constructors; never accept last-key-wins behavior."""

    def construct_mapping(self, node, deep=False):
        seen = set()
        for key, _ in node.value:
            if key.tag != 'tag:yaml.org,2002:str':
                raise yaml.constructor.ConstructorError(None, None,
                    'mapping keys must be strings; merge keys are unsupported', key.start_mark)
            value = self.construct_object(key, deep=True)
            if value in seen:
                raise yaml.constructor.ConstructorError(None, None,
                    f'duplicate key {value!r}', key.start_mark)
            seen.add(value)
        return super().construct_mapping(node, deep=deep)


def pointer_part(value):
    return str(value).replace('~', '~0').replace('/', '~1')


def json_value(value):
    """Encode safe scalar types explicitly instead of changing their meaning."""
    if isinstance(value, (datetime, date)):
        return {'yaml_type': 'timestamp', 'value': value.isoformat()}
    if isinstance(value, bytes):
        return {'yaml_type': 'binary', 'base64': base64.b64encode(value).decode('ascii')}
    if isinstance(value, float):
        return {'yaml_type': 'float', 'value': repr(value) if math.isfinite(value) else str(value)}
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, list):
        return [json_value(x) for x in value]
    if isinstance(value, dict):
        return {k: json_value(v) for k, v in value.items()}
    raise ValueError('unsupported safe YAML type: ' + type(value).__name__)


@dataclass
class Document:
    value: object
    fields: list[dict]


def parse(raw: bytes, path='<memory>') -> Document:
    if len(raw) > MAX_BYTES:
        raise ParseError('document exceeds byte budget', path)
    loader = None
    try:
        text = raw.decode('utf-8-sig')
        loader = StrictSafeLoader(text)
        root = loader.get_single_node()
        if root is None:
            raise ParseError('empty YAML document', path)
        fields = []
        def walk(node, pointer, ancestors, depth, key_mark=None):
            if depth > MAX_DEPTH or len(fields) >= MAX_NODES:
                raise ParseError('document exceeds expansion/depth budget', path, node.start_mark, pointer)
            if id(node) in ancestors:
                raise ParseError('recursive YAML alias', path, node.start_mark, pointer)
            mark, end = node.start_mark, node.end_mark
            fields.append({'field': pointer, 'tag': node.tag, 'line': mark.line+1,
                           'column': mark.column+1, 'end_line': end.line+1,
                           'end_column': end.column+1, 'character_start': mark.index,
                           'character_end': end.index,
                           'key_line': key_mark.line+1 if key_mark else None,
                           'key_column': key_mark.column+1 if key_mark else None})
            trail = ancestors | {id(node)}
            if isinstance(node, MappingNode):
                # Validate duplicate and non-string keys before traversing paths.
                loader.construct_mapping(node)
                for key, child in node.value:
                    walk(child, pointer+'/'+pointer_part(key.value), trail, depth+1, key.start_mark)
            elif isinstance(node, SequenceNode):
                for i, child in enumerate(node.value):
                    walk(child, pointer+'/'+str(i), trail, depth+1)
            elif not isinstance(node, ScalarNode):
                raise ParseError('unsupported YAML node', path, mark, pointer)
        walk(root, '', set(), 0)
        value = json_value(loader.construct_document(root))
        return Document(value, fields)
    except ParseError:
        raise
    except (yaml.YAMLError, UnicodeError, ValueError, RecursionError) as error:
        raise ParseError(str(error), path, getattr(error, 'problem_mark', None)) from error
    finally:
        if loader is not None:
            loader.dispose()
