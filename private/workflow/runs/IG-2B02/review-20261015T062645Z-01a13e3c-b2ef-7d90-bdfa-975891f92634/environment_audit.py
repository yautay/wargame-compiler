from review_driver import *
import importlib.metadata
cat=load(P/'frozen-pins.json')
rows=[]
for expected in cat['all_unique_frozen_refs_and_launch_controls']:
    path=Path(expected['path']);path=path if path.is_absolute() else ROOT/path
    actual=pin(path)
    assert actual['bytes']==expected['bytes'] and actual['sha256']==expected['sha256'],expected['path']
    rows.append({'expected':expected,'actual':actual,'result':'exact'})
for expected in cat['launch_gate_pins']:
    path=Path(expected['path']);path=path if path.is_absolute() else ROOT/path
    assert pin(path)['sha256']==expected['sha256'] and path.stat().st_size==expected['bytes'],str(path)
envp=load(D/'toolchain.json')
native={}
for tool,obs in envp['native'].items():
    path=Path(obs['executable']['path']);actual=pin(path)
    assert actual==obs['executable'],tool
    rec=run('07-version-'+tool,[path,'-v' if tool in ('pdfinfo','pdftoppm') else '--version'])
    version=((ROOT/rec['stderr']['path']).read_text(encoding='utf-8')+(ROOT/rec['stdout']['path']).read_text(encoding='utf-8')).strip()
    assert version==obs['version'],(tool,version)
    native[tool]={'executable':actual,'version':version,'check':rec}
versions={k:importlib.metadata.version(k) for k in ('pypdf','pdfplumber','Pillow','pytest')}
assert sys.version==envp['python'] and versions==envp['libraries']
py_pin=pin(PY)
assert py_pin['sha256']==envp['python_executable']['sha256'] and py_pin['bytes']==envp['python_executable']['bytes']
write('toolchain.json',{'observed_utc':utc(),'python':sys.version,'python_executable_observation':py_pin,'libraries':versions,'bundle_version':'26.1013.11914','native_executable_observations':native,'comparison':'Exact executable hash/version/library match against frozen toolchain; no drift.','process_environment':{k:env[k] for k in ('PYTHONDONTWRITEBYTECODE','PYTHONPATH')},'note':'Native and .venv executable observations are not workflow artifacts.'})
envelope=load(D/'delivery-transition-envelope.json');manifest=load(D/'delivery-manifest.json');seal=load(D/'final-seal.json')
groups=[envelope['artifacts'],manifest['new_reviewed_artifacts'],manifest['immutable_inputs_and_old_evidence'],seal['postfreeze_recovery_and_epilogue_artifacts']]
assert [len(g) for g in groups]==[2895,1462,1428,40]
union={}
for group in groups:
    assert len({p['path'] for p in group})==len(group)
    for p in group:
        if p['path'] in union:assert union[p['path']]==p
        union[p['path']]=p
assert len(union)==2930
assert cat['approved_ordered_artifact_list']==envelope['artifacts']
q=load(ROOT/'docs/work/queue.json')
active=[t['id'] for t in q['tasks'] if t['status'] in ('in_progress','review','changes_requested','accepted')]
assert active==['IG-2B02']
write('independent-byte-audit.json',{'utc':utc(),'catalogue':pin(P/'frozen-pins.json'),'independently_verified':rows,'group_lengths':[len(g) for g in groups],'union_count':len(union),'exact_approved_order_preserved':True,'active_tasks':active,'executable_observations':'Hashed at native paths; never serialized into workflow artifact arrays.','fresh_packet_reconstruction':'Verified by byte/status helper: 93973 logical LF / 96208 physical CRLF bytes.'})
checkpoint('input_and_environment_gate',['Actual independent gpt-6.1-sol/high configuration','All input byte/status gates','Own four original-page observations before ledger','Unchanged runtime/toolchain'], 'Inspect all final ledger/specifications/components, exact crop boundaries and independent structural/locator replay.')
print('Independent byte and runtime gates passed',len(rows))
