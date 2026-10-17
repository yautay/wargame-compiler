from pathlib import Path
import hashlib, importlib.metadata, json
from run_checks import OUT, ROOT, ATTEMPT, save, run
from wgc.sources.inventory import safe_artifact

tc=json.loads((ATTEMPT/'toolchain.json').read_text())
exe=[]
for name,pin in tc['executables'].items():
    h=hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
    exe.append({'name':name,'path':pin['path'],'expected_sha256':pin['sha256'],'actual_sha256':h,'matches':h==pin['sha256']})
assert all(e['matches'] for e in exe)
versions={n:importlib.metadata.version(n) for n in tc['libraries']}
assert versions==tc['libraries']
deps=json.loads((ATTEMPT/'dependency-verification.json').read_text())
protected=deps['protected_hashes']
contract=[]
if isinstance(protected,dict):
    for rel,h in protected.items():
        if rel in ['src/wgc/contracts/source.py','contracts/ig/source.schema.json','contracts/ig/README.md']:
            actual=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
            contract.append({'path':rel,'expected':h,'actual':actual,'matches':h==actual})
assert all(p['matches'] for p in contract)
paths=[]
for rel in ['private/a//b','private/a/./b','private/aux.txt','private/file:ads','private/COM1','private/LPT9.txt','private/a. /b','private/a/../b']:
    try:safe_artifact(ROOT,rel);reject=False
    except ValueError:reject=True
    paths.append({'path':rel,'rejected':reject})
assert all(p['rejected'] for p in paths)
save('toolchain-and-contract-verification.json',{'executables':exe,'actual_libraries':versions,'frozen_IG1_contract_hashes':contract,'extra_path_probes':paths,'no_install':True,'environment_scope':'Child processes only; values supplied from frozen toolchain.json.'})
save('visual-inspection.json',{'actor':'codex-01a1363e-1de5-7073-8185-d9a1f2e89c35','method':'Reviewer inspected four independent original-PDF 144-DPI PNGs via view_image after pixel equality against frozen evidence.','pages':[{'pdf_page':1,'label':'unknown','edition_visible':'5th Edition','observations':'Cover image, heading and contents panel visible without clipping.'},{'pdf_page':2,'label':'2','position':'top-left','observations':'Two text columns and header/footer visible.'},{'pdf_page':3,'label':'3','position':'top-right','observations':'Two columns and illustrated unit panel visible without missing graphics.'},{'pdf_page':4,'label':'4','position':'top-left','observations':'Text columns and inline unit illustrations visible.'}],'content_scope':[1,2,3,4],'pages_5_to_44':'Structural geometry only; no text extraction or image inspection.','semantic_acceptance_granted':False,'xref_assessment':'Observed warning reproduced in strict pypdf; it corrects object IDs in memory. Frozen bytes remain pinned. Independent Poppler count and original/derived pixel equality on pages 1-4 provide structural corroboration. No PDF repair or warning suppression; uninspected source content remains outside review.'})
run('final-workflow',[tc['python_executable'],'scripts/workflow.py','validate'])
run('final-diff',['git','diff','--check'])
print('Supplemental toolchain hashes, IG-1 contract preservation, paths and visual record saved.')
