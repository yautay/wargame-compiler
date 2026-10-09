"""One-session offline baseline audit and bounded source-location work; no inference."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path.cwd()
P = ROOT / 'private/poc/spqr-chapter9'
M = P / 'measurement/M-POC4A-pass-01'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(path): return json.loads(path.read_bytes())
def desc(path):
    b = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(b), sha256=sha(b))
def save(path, obj):
    assert not path.exists(), path
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def verify(a, base=ROOT):
    path=base/a['path']; b=path.read_bytes()
    assert sha(b)==a['sha256'] and len(b)==a['bytes'], path
    return desc(path)

if __name__ == '__main__':
    protected=[]
    for folder in ['runs/first-001','proposals/first-001','reports/first-001','inputs/v1',
                   'transfer/first-v1','evaluation/eval-v1','source','prompts','formats',
                   'measurement/M-POC3-first-001']:
        protected += [desc(f) for f in sorted((P/folder).rglob('*')) if f.is_file()]
    protected.append(desc(P/'measurement/sessions.jsonl'))
    save(M/'protected-before.json', protected)
    run=load(P/'runs/first-001/run.json')
    raw=(P/'runs/first-001/first-001.json').read_bytes()
    assert sha(raw)==run['response']['sha256'] and len(raw)==run['response']['bytes']
    assert (ROOT/run['response']['original_path']).read_bytes()==raw
    assert (P/'proposals/first-001/proposal.json').read_bytes()==raw
    closure=load(P/'reports/first-001/closure.json')
    verify(closure['report_manifest'])
    report=load(P/'reports/first-001/manifest.json')
    for a in report['artifacts']+[report['response'],report['input_manifest'],report['evaluation_manifest']]: verify(a)
    inputs=load(P/'inputs/v1/manifest.json')
    for a in inputs['artifacts']: verify(a,P)
    evaluation=load(P/'evaluation/eval-v1/manifest.json')
    for a in evaluation['artifacts']: verify(a)
    for a in run['inputs']['known_prepared_package_files']:
        assert (ROOT/a['canonical_path']).read_bytes()==(ROOT/a['transfer_path']).read_bytes()
        assert desc(ROOT/a['canonical_path'])['sha256']==a['sha256']
    prov=load(P/'proposals/first-001/provenance.json'); proposal=json.loads(raw)
    for ptr, span in prov['json_value_spans'].items():
        frag=raw[span['start_byte']:span['end_byte_exclusive']]
        value=proposal
        if ptr:
            for part in ptr[1:].split('/'):
                key=part.replace('~1','/').replace('~0','~')
                value=value[int(key)] if isinstance(value,list) else value[key]
        assert sha(frag)==span['sha256'] and json.loads(frag)==value, ptr
    source=load(P/'source/source-v1.json')['source']
    copy=P/'source/original-pdf-20261008-01.pdf'
    assert desc(copy)['sha256']==source['sha256'] and desc(copy)['bytes']==source['bytes']
    result=dict(id='M-POC4A-baseline-integrity', checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        response=desc(P/'runs/first-001/first-001.json'), report_manifest=desc(P/'reports/first-001/manifest.json'),
        closure=desc(P/'reports/first-001/closure.json'), report_artifacts=len(report['artifacts']),
        input_artifacts=len(inputs['artifacts']), transfer_files=len(run['inputs']['known_prepared_package_files']),
        evaluation_artifacts=len(evaluation['artifacts']), raw_pointer_spans=len(prov['json_value_spans']),
        all_match=True, source_copy=desc(copy), historical_source_path_exists=Path(source['path']).exists(),
        limitation='Byte integrity only; no new semantic acceptance or provenance attestation. Historical configuration/timing/transfer/clean context remain unknown.')
    save(M/'baseline-integrity.json',result)
    print(json.dumps(result,indent=2))
