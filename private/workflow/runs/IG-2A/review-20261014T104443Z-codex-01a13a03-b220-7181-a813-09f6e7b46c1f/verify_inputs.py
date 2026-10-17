from support import *
import importlib.util, difflib, platform, importlib.metadata

expected = {
    REPAIR/'delivery.json':'c69df3b2867f440c6b330159a2d335dff6bf959192ebb9d3ac5d0ea59977195e',
    REPAIR/'delivery-manifest.json':'3652874c7a029100efe81b93914934e469ba5b519bf1b66b0ff2b209645a7d49',
    REPAIR/'delivery-handoff.md':'0ad1c51043eaef5859f6e99484889ae9e2aa0eda4c837dd9f75c754165b0e758',
    REPAIR/'final-seal.json':'64f96bc690396ceeb3ed37722c0c29546fa4a76448710ad8b8731043f0ce312d',
    PRIOR/'final-seal.json':'d45b128f0e3be2cb0f3a97c4e7b91c955fe2760474ca78e6dbeca379089d864a',
    PRIOR/'review-manifest.json':'5bef17ff2526b5f423704625d8eb31c5e49229b3f4c010140be9833f48d02c73',
    ROOT/'private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf':'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'}
results=[]
def verify(entry,group):
    path=ROOT/entry['path']
    result={'group':group, **entry, 'actual_sha256':digest(path), 'actual_bytes':path.stat().st_size}
    result['matches']=result['sha256']==result['actual_sha256'] and ('bytes' not in entry or entry['bytes']==result['actual_bytes'])
    results.append(result)
for path,sha in expected.items(): verify({'path':path.relative_to(ROOT).as_posix(),'sha256':sha},'operator-pin')
for entry in read(REPAIR/'delivery-manifest.json')['artifacts']: verify(entry,'repair-delivery')
seal=read(REPAIR/'final-seal.json')
for key in ['delivery','manifest','handoff','transition_recovery']: verify(seal[key],'repair-seal')
for key in ['post_freeze_operational_artifacts','governance_artifacts']:
    for entry in seal[key]: verify(entry,key)
for entry in read(PRIOR/'review-manifest.json')['artifacts']: verify(entry,'prior-review')
for key in ['manifest','handoff','report','review']: verify(read(PRIOR/'final-seal.json')[key],'prior-seal')
packet=read(PREP/'packet-manifest.json')
for entry in packet['files']: verify(entry,'packet')
verify({'path':'docs/work/queue.json','sha256':packet['queue_sha256']},'packet-queue')
write('input-verification.json',{'verified_utc':utc(),'records':results,'failures':[x for x in results if not x['matches']]})
assert all(x['matches'] for x in results), 'Input pin divergence; stop and inform coordinator'
spec=importlib.util.spec_from_file_location('workflow',ROOT/'scripts/workflow.py')
workflow=importlib.util.module_from_spec(spec);spec.loader.exec_module(workflow)
queue=workflow.read_json(ROOT/workflow.QUEUE)
current_packet=workflow.packet(queue,ROOT,'IG-2A',output=False)
assert current_packet==packet, 'Current packet differs; coordinator explanation required'
write('packet-verification.json',{'queue_unchanged':True,'current_packet_matches_preparation':True,'preparation_manifest':pin(PREP/'packet-manifest.json'),'preparation_context':pin(PREP/'packet-context.txt'),'regeneration_required':False})
task=next(t for t in queue['tasks'] if t['id']=='IG-2A')
write('queue-record.json',task)
print('verified',len(results),'records; delivery',len(read(REPAIR/'delivery-manifest.json')['artifacts']), 'queue',task['status'])
session=Path(r'C:\Users\yauta\.codex\sessions\2026\10\14\rollout-2026-10-14T12-44-43-01a13a03-b220-7181-a813-09f6e7b46c1f.jsonl')
turns=[json.loads(line) for line in session.read_text(encoding='utf-8').splitlines() if json.loads(line).get('type')=='turn_context']
write('configuration.json',{'actor':'codex-01a13a03-b220-7181-a813-09f6e7b46c1f','session_id':'01a13a03-b220-7181-a813-09f6e7b46c1f','requested_model':'gpt-6.1-sol','requested_reasoning':'high','model':turns[-1]['payload']['model'],'reasoning':turns[-1]['payload']['effort'],'metadata_path':str(session),'metadata_timestamp':turns[-1]['timestamp'],'operator_confirmation':'potwierdzam 6.1 sol high','started_utc':'2026-10-14T10:44:43.646Z','tokens':None,'cost':None,'operator_seconds':None,'unknown_reason':'Usage/cost/operator time are not exposed or reported.'})
assert turns[-1]['payload']['model']=='gpt-6.1-sol' and turns[-1]['payload']['effort']=='high'
command('initial-git-status',['git','status','--porcelain=v1'])
versions={name:importlib.metadata.version(name) for name in ['pypdf','pdfplumber','Pillow','reportlab','pytest']}
binaries={name: {'path':str(path),'sha256':digest(path)} for name,path in {'python':PYTHON,'base-python':Path(sys._base_executable),'pdfinfo':POPPLER/'pdfinfo.exe','pdftoppm':POPPLER/'pdftoppm.exe'}.items()}
for name in ['pdfinfo','pdftoppm']: command(name+'-version',[POPPLER/(name+'.exe'),'-v'])
write('toolchain.json',{'python':sys.version,'libraries':versions,'executables':binaries,'bundle_version':'26.1013.11914','captured_before_probes_utc':utc(),'executor_binary_comparison':{name:binaries[name]['sha256']==read(REPAIR/'toolchain.json')['executables'][name]['sha256'] for name in ['pdfinfo','pdftoppm']},'process_pythonpath':os.environ['PYTHONPATH'],'process_path_prefix':str(POPPLER),'installs':0,'global_config_changes':0})
print('versions',versions)
preservation=read(REPAIR/'preservation-final.json')
original_path=ROOT/preservation['original_delivery_json_copy']['path']
original=read(original_path)
snapshot_results=[]
for entry in original['artifacts']:
    verify({**entry,'path':(REPAIR/'original-delivery'/entry['path']).relative_to(ROOT).as_posix()},'original-preserved-copy')
    if entry['path'] not in preservation['intentional_superseded_live_paths']: verify(entry,'unchanged-original-live')
for entry in read(REPAIR/'base-products.json'):
    before=REPAIR/'product-before'/entry['path']
    verify({**entry,'path':before.relative_to(ROOT).as_posix()},'product-before')
    now=ROOT/entry['path']
    diff=''.join(difflib.unified_diff(before.read_text(encoding='utf-8-sig').splitlines(True),now.read_text(encoding='utf-8-sig').splitlines(True),fromfile='verified-product-before/'+entry['path'],tofile=entry['path']))
    (RUN/('diff-'+entry['path'].replace('/','_')+'.txt')).write_text(diff,encoding='utf-8')
write('input-verification.json',{'verified_utc':utc(),'records':results,'failures':[x for x in results if not x['matches']]})
assert all(x['matches'] for x in results), 'Preservation divergence'
print('including preservation:',len(results),'pins pass')
