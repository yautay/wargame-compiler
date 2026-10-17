"""Immutable canonical packages; measured operations live beside the packages."""
from __future__ import annotations

from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import time
import uuid

from wgc.contracts.source import canonical_bytes
from wgc.inputs.snapshot import no_links, open_read, verify_tree_names
from wgc.export.source import PROFILE_SHA256, validate_export
from wgc.wgu_adapter.identity import validate_registry


def _read(path):
    with open_read(path) as stream:return stream.read()


def publish(result, directory, *, operation_evidence=None):
    start=datetime.now(timezone.utc);clock=time.monotonic()
    validate_export(result['bundle']);validate_registry(result['registry'])
    directory=Path(directory).absolute();no_links(directory);directory.mkdir(parents=True,exist_ok=True)
    files={'source-ig.json':canonical_bytes(result['bundle'])+b'\n',
           'identity-registry.json':canonical_bytes(result['registry'])+b'\n',
           'references.json':canonical_bytes(result['references'])+b'\n'}
    body={'format':'wgc-source-export-package-1','schema_profile_sha256':PROFILE_SHA256,
          'state':'structural-draft','files':[{'path':p,'bytes':len(raw),
              'sha256':hashlib.sha256(raw).hexdigest()} for p,raw in sorted(files.items())]}
    identifier=hashlib.sha256(canonical_bytes(body)).hexdigest()
    manifest={**body,'package_id':'sha256:'+identifier}
    files['manifest.json']=canonical_bytes(manifest)+b'\n'
    target=directory/('sha256-'+identifier);no_links(target)
    if not target.exists():
        target.mkdir(exist_ok=False)
        for name,raw in files.items():
            path=target/name;no_links(path)
            with path.open('xb') as stream:stream.write(raw)
    verify_tree_names(target,set(files))
    for name,raw in files.items():
        if _read(target/name)!=raw:raise ValueError('existing canonical package changed; preserve for diagnosis')
    operations=directory/'operations';no_links(operations);operations.mkdir(exist_ok=True)
    operation={'format':'wgc-export-operation-1','package_id':manifest['package_id'],
        'started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat(),
        'wall_seconds':time.monotonic()-clock,'evidence':operation_evidence,
        'input_tokens':None,'output_tokens':None,'cost':None,'semantic_acceptance':'not_granted',
        'source_coverage':'not_verified','executable_readiness':'not_granted'}
    operation_path=operations/('operation-'+uuid.uuid4().hex+'.json')
    with operation_path.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(operation,stream,ensure_ascii=False,indent=2);stream.write('\n')
    return {'package':str(target),'manifest':manifest,'operation':str(operation_path)}
