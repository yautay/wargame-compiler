"""Coordinator preparation only; never claims or authors source inventory."""
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path.cwd()
RUN = Path(__file__).parent.relative_to(ROOT)
B = Path('private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77')
C = Path('private/workflow/runs/IG-2B01/closure-20261014T183702Z-01a13b57-40e6-78d2-9d17-0b3e91afba77')
R = Path('private/workflow/runs/IG-2B01/review-20261014T171920Z-01a13b6c-f981-7192-a5ff-1126c809cd63')
A = Path('private/workflow/runs/IG-2A/closure-20261014T115019Z-01a139bc-256f-7da0-b4a7-8940ca16fc81')
ACTOR = 'codex-' + os.environ['CODEX_THREAD_ID']
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    with Path(p).open('rb') as s: return hashlib.file_digest(s, 'sha256').hexdigest()
def pin(p): return {'path':Path(p).as_posix(),'bytes':Path(p).stat().st_size,'sha256':sha(p)}
def write(name,d):
    body=json.dumps(d,ensure_ascii=False,indent=2)+'\n'
    p=RUN/name
    if p.exists():
        assert p.read_text(encoding='utf-8')==body, 'Refuse overwrite: '+str(p)
    else: p.write_text(body,encoding='utf-8')
def command(name, argv, env=None):
    start=dt.datetime.now(dt.timezone.utc)
    r=subprocess.run(argv,capture_output=True,env=env)
    end=dt.datetime.now(dt.timezone.utc)
    (RUN/(name+'.stdout')).write_bytes(r.stdout); (RUN/(name+'.stderr')).write_bytes(r.stderr)
    d={'command':argv,'exit_code':r.returncode,'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'wall_seconds':(end-start).total_seconds(),'stdout':pin(RUN/(name+'.stdout')),'stderr':pin(RUN/(name+'.stderr'))}
    write(name+'.json',d); print(name,r.returncode, r.stdout.decode('utf-8',errors='replace')[:500]); return d

def prepare():
    q=read('docs/work/queue.json'); write('queue-before.json',q)
    write('preliminary-command-notes.json',{'initial_workflow_validate_exit':0,'initial_next_exit':0,'initial_next_result':'No ready task.','search_invocation_error':{'command':'pwsh -NoProfile -File scripts/search.ps1 -Pattern "def |allow|manifest" -Paths scripts/workflow.py','exit_code':1,'error':'A parameter cannot be found that matches parameter name Paths.','resolution':'Read actual parameter definition; reran with supported Pattern-only invocation, exit 0.'},'preparation_only':True})
    assert {t['id']:t['status'] for t in q['tasks'] if t['id'] in ['IG-2A','IG-2B01','IG-2B02']}=={'IG-2A':'done','IG-2B01':'done','IG-2B02':'planned'}
    by={t['id']:t for t in q['tasks']}
    delivery=read(B/'delivery.json'); accepted=read(C/'accepted.json'); done=read(C/'done.json'); review=read(R/'review.json')
    assert delivery['artifacts']==accepted['artifacts']==done['artifacts']==review['artifacts']
    assert accepted['actor']==review['actor']!=delivery['actor']
    assert accepted['criteria']==done['criteria']==by['IG-2B01']['acceptance']
    assert review['outcome']=='PASS' and review['blocking_findings']==0
    verified={}; mutable=[]
    def visit(d):
        if isinstance(d,dict):
            if isinstance(d.get('path'),str) and 'sha256' in d:
                rel=d['path']; p=Path(rel)
                assert not p.is_absolute() and '..' not in p.parts and not rel.startswith(('.git','archive','private/archive'))
                actual=pin(p)
                if rel in ['docs/work/queue.json','docs/work/context-policy.json','docs/ROADMAP.md','docs/STATUS.md','docs/HANDOFF.md'] or rel.startswith('docs/work/tasks/'):
                    mutable.append({'expected':d,'current':actual,'note':'Historical projection/queue snapshot pin; current events verified directly, no historical bytes reopened.'})
                else:
                    assert actual['sha256']==d['sha256'], (rel,d['sha256'],actual)
                    if 'bytes' in d: assert actual['bytes']==d['bytes'],rel
                    verified[rel]=actual
            for v in d.values(): visit(v)
        elif isinstance(d,list):
            for v in d: visit(v)
    seeds=[C/'final-seal.json',C/'manifest.json',B/'final-seal.json',B/'delivery-manifest.json',B/'delivery.json',C/'accepted.json',C/'done.json',R/'review-seal.json',R/'review-manifest.json',R/'review.json',A/'final-seal.json',A/'accepted.json',A/'done.json']
    for p in seeds: verified[p.as_posix()]=pin(p); visit(read(p))
    for task_id in ['IG-2A','IG-2B01']:
        for e in by[task_id]['events']:
            assert sha(e['evidence'])==e['sha256']; verified[e['evidence']]=pin(e['evidence'])
    inv=read(B/'final-verified/inventory.json'); registry=read(B/'final-verified/identity-registry.json')
    assert inv['registry']==registry and len(inv['pages'])==44
    pages={p['id']:p['pdf_page'] for p in inv['pages']}
    authored=[r for r in inv['regions'] if pages[r['page_id']]<=4 and r['denominator_role']=='inventory']
    placeholders=[r for r in inv['regions'] if pages[r['page_id']]>=5 and r['denominator_role']=='inventory']
    contexts=[r for r in inv['regions'] if r['denominator_role']=='context']
    assert len(authored)==130 and len(placeholders)==40 and len(contexts)==1
    context=contexts[0]; assert context['id']=='region:e8d77349-41ce-47d0-b678-eab1d0c8e8ed' and pages[context['page_id']]==5
    assert all(r['coverage'][level]['status']=='unprocessed' for r in placeholders for level in r['coverage'])
    ai=Path('private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/inventory-one/inventory.json')
    baseline=read(ai)
    assert [p for p in baseline['pages'] if p['pdf_page']>=5]==[p for p in inv['pages'] if p['pdf_page']>=5]
    assert [r for r in baseline['regions'] if pages[r['page_id']]>=5]==placeholders
    assert all(e in registry['entries'] for e in baseline['registry']['entries'])
    write('dependency-hash-audit.json',{'immutable_files':list(verified.values()),'mutable_snapshot_pins':mutable,'events':{i:by[i]['events'] for i in ['IG-2A','IG-2B01']},'no_source_content_extraction':True})
    summary={'role':'coordinator','actor':ACTOR,'IG2A_status':'done','IG2B01_status':'done','outcome':'verified','immutable_files_verified':len(verified),'audit':pin(RUN/'dependency-hash-audit.json'),'delivery_artifact_count':len(delivery['artifacts']),'reviewer':review['actor'],'executor':delivery['actor'],'artifact_lists_equal':True,'criteria_equal':True,'current_event_hashes_verified':True,'closure_seal':pin(C/'final-seal.json'),'review_seal':pin(R/'review-seal.json'),'delivery_seal':pin(B/'final-seal.json'),'accepted':pin(C/'accepted.json'),'done':pin(C/'done.json'),'closure_handoff':pin(C/'closure-handoff.md'),'finding_dispositions':pin(C/'finding-dispositions.json'),'limits':'Technical inventory closure only. Nonblocking R01 process overread acknowledged; R02 exact transcription advisory retained. No new independent review, human semantic acceptance, whole-record source-IG review, approved exclusion or executable readiness.','baseline':pin(B/'final-verified/inventory.json'),'registry':pin(B/'final-verified/identity-registry.json'),'pages':44,'accepted_authored_pages':[1,2,3,4],'accepted_authored_regions':130,'unprocessed_placeholders':40,'context_denominator':0}
    write('dependency-verification.json',summary)
    env=os.environ.copy(); bundle=Path('C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies')
    env['PYTHONPATH']=str(ROOT/'src')+';'+str(bundle/'python/Lib/site-packages'); env['PYTHONDONTWRITEBYTECODE']='1'
    native=bundle/'native/poppler/Library/bin'; env['PATH']=str(native)+';'+env['PATH']
    lib=command('library-versions',[sys.executable,'-B','-c','import sys,importlib.metadata,json; print(json.dumps({"python":sys.version,"libraries":{n:importlib.metadata.version(n) for n in ["pypdf","pdfplumber","Pillow","pytest"]}}))'],env)
    assert lib['exit_code']==0
    toolchain=json.loads((RUN/'library-versions.stdout').read_text(encoding='utf-8'))
    toolchain.update({'bundle_version':'26.1013.11914','python_executable':pin(sys.executable),'process_pythonpath':env['PYTHONPATH'],'process_path_prefix':str(native),'native':{}})
    for name in ['pdfinfo','pdftoppm','pwsh','git']:
        executable=shutil.which(name); version=command(name+'-version',[executable, '-v' if name in ['pdfinfo','pdftoppm'] else ('-Version' if name=='pwsh' else '--version')],env)
        assert version['exit_code']==0
        toolchain['native'][name]={'executable':pin(executable),'version':((RUN/(name+'-version.stdout')).read_text(encoding='utf-8')+(RUN/(name+'-version.stderr')).read_text(encoding='utf-8')).strip()}
    frozen_paths=[p for p in verified if p.startswith('src/wgc/sources/') or p=='contracts/ig/regions.schema.json' or p.startswith('src/wgc/contracts/') or p.startswith('contracts/ig/')]
    toolchain['frozen_contract_and_tool_pins']=[verified[p] for p in sorted(frozen_paths)]
    toolchain['workflow_and_checks']=[pin(p) for p in ['scripts/workflow.py','scripts/check.ps1','scripts/search.ps1']]
    write('toolchain.json',toolchain)
    source_pins={'source':inv['source'],'baseline':pin(B/'final-verified/inventory.json'),'persisted_registry':pin(B/'final-verified/identity-registry.json'),'accepted_contract_pins':toolchain['frozen_contract_and_tool_pins'],'read_policy':'Large baseline is a pinned structural input, not packet prose. Read only named JSON structure needed to preserve records and compare scope; no source extraction on unassigned pages.'}
    write('source-pins.json',source_pins)
    future=Path('private/workflow/runs/IG-2B02')/('inventory-20261014T201344Z-reserved-by-'+os.environ['CODEX_THREAD_ID'])
    assert not future.exists()
    context_evidence=[e for e in inv['evidence'] if e['region_id']==context['id']]
    parent=next(r for r in inv['regions'] if r['id']=='region:ba4a5094-22f5-4a67-8a19-6cc598a17b1b')
    parent_evidence=[e for e in inv['evidence'] if e['region_id']==parent['id']]
    scope={'task':'IG-2B02','role':'coordinator','actor':ACTOR,'authoring_pages':[5,6,7,8],'full_structural_page_count':44,'preparation_run':RUN.as_posix(),'reserved_executor_attempt':future.as_posix(),'attempt_policy':'Executor creates this absent directory only after new-session configuration evidence; never reuse a prior run. If it exists or another writer appears, checkpoint and escalate before claim.','baseline':source_pins['baseline'],'registry':source_pins['persisted_registry'],'preservation':{'pages_1_4':'Preserve all accepted page/region/evidence records and their revisions, registry bindings, links, and relative reading order; references remain at old immutable paths. Do not regenerate or copy/promote old evidence.','pages_9_44':'Preserve all page records and original 36 inventory placeholders exactly, including unprocessed coverage, uncertainty, membership and relative reading order.','pages_5_8':'Retire only four placeholder memberships, retain their registry entries. Independently author regions with explicit ig2b02 keys and newly assigned UUIDs; preserve page IDs, keys, physical addresses and geometry. Any label update needs exact same-page current evidence.','registry':'Extend accepted IG-2B01 persisted registry; retain every existing kind/key/ID entry. Never reuse the earlier IG-2A registry instead or reseed UUIDs.','revisions':'Recompute changed author-region/page/top inventory revisions using unchanged WGC-C14N-1 and wgc-inventory-1. Keep unchanged nested records and evidence byte pins. New author scope changes partition_hash; no inherited exclusion authorization.'},'existing_context':{'record':context,'evidence':context_evidence,'policy':'Preserve exact context key/ID/revision/box/coverage/evidence, membership, prior link and reading-order occurrence. It stays context with zero denominator; never promote it to inventory. Allocate a distinct authored region for the page-5 material with a new explicit ig2b02 key/ID. Persist context-authored-correspondence.json with both exact IDs/revisions/boxes, source pin and source-observed correspondence; do not remap IDs or transfer review/acceptance. Retain old continuation; a separately evidenced new continuation to the authored region may be added without editing old regions/links. Splits/merges need explicit lineage decision and escalation, not inferred identity.'},'continuation_context':{'page_4':{'region':parent,'evidence':parent_evidence,'access':'Only this accepted exact final region and its existing crop/text/PNG for the 4-to-5 continuation; no whole page-4 rendering or other page-1-4 content analysis.'},'page_9':{'access':'Conditional only if an observed unfinished page-8 fragment needs completion. Before any content access, record exact need, originating page-8 region, proposed physical-page-9 normalized box and maximum two-line top-of-corresponding-column probe in checkpoint/context-access.json. Open only that predetermined crop; never dump/render the entire page or neighboring entry. If the narrow crop cannot resolve the continuation, record unresolved boundary/gap and request bounded coordinator refinement before expanding.','denominator':'Any new context ID has role context and zero task/full inventory denominator.'},'pages_10_44':'No text/image content access; structural source count/geometry validation only.'},'outputs':[str(future/p).replace('\\','/') for p in ['authored/inventory.json','authored/identity-registry.json','final-verified/inventory.json','final-verified/identity-registry.json','final-verified/coverage.json','region-ledger-final.json','scope-report-final.json','context-authored-correspondence.json','continuations.json','uncertainty.json','gaps.json','geometric-gaps.json','visual-inspection.json','locator-audit.json','replay-report.json','preservation-report.json','criteria.json','checkpoint.json','configuration.json','toolchain.json','delivery-manifest.json','delivery.json','delivery-handoff.md','final-seal.json']],'evidence_output':(future/'evidence').as_posix()+'/ (new author/context triples only; 144 DPI Poppler PNG, exact crop PDF and raw UTF-8 pdfplumber text, page_basis_hash and region revisions)','denominator':'Task: only new independently authored inventory regions on pages 5-8. Full sidecar: 130 preserved authored + 36 unchanged placeholders + new page-5-8 inventory regions; all context counts zero. Geometric completeness, region count and semantic coverage are separate.','coverage':'BBox, PNG, extraction or editorial classification never means represented or approved exclusion. Keep partial/unprocessed with explicit gaps until actual source-justified representation exists. No gameplay legality via LLM. Human semantic acceptance and IG-1A whole-record review remain separate future gates.','stop':'Delivery -> review only; new delivery requires a fresh independent reviewer of exact frozen hashes. Do not self-accept, close, execute a downstream task or create a session.'}
    write('scope.json',scope)
    t=by['IG-2B02']; t['title']='Inventory SPQR PDF pages 05-08'; t['outputs']=scope['outputs']+[scope['evidence_output']]
    t['write_scope']=[future.as_posix()+'/','private/workflow/packets/','private/workflow/checks/']
    t['inputs']=[f"Official PDF {inv['source']['pdf']['path']} SHA256 {inv['source']['sha256']}; 44 physical pages; substantive authoring only 5-8",f"Official provenance {inv['source']['provenance']['path']} SHA256 {inv['source']['provenance']['sha256']}",f"Accepted IG-2B01 baseline {source_pins['baseline']['path']} SHA256 {source_pins['baseline']['sha256']}",f"Persisted IG-2B01 registry {source_pins['persisted_registry']['path']} SHA256 {source_pins['persisted_registry']['sha256']}; extend without changing existing key/ID bindings",'Full 44-page sidecar; preserve accepted 1-4 and placeholders 9-44. Retire only placeholder memberships 5-8, preserving registry entries.','Existing page-5 context region remains exact context/zero denominator; new authored identity plus exact correspondence sidecar.','Boundary context: only pinned page-4 region; conditional predetermined maximum-two-line page-9 crop after recorded need, otherwise unresolved gap. No other content access.']
    t['context']=['docs/work/EVIDENCE.md','src/wgc/sources/README.md','contracts/ig/README.md','contracts/ig/regions.schema.json',inv['source']['provenance']['path'],inv['source']['pdf']['path']]+[(RUN/p).as_posix() for p in ['configuration.json','dependency-verification.json','source-pins.json','scope.json','toolchain.json']]
    t['start_conditions']=['Dependencies IG-2A and IG-2B01 are done with exact closure/delivery/review pins; this readiness is preparation only.','Before claim, a NEW executor session must verify actual GPT-6.1 Sol/high from its own metadata or direct operator observation and record identity/configuration/checkpoint. Requested settings and other sessions do not prove actual settings.','Verify packet, source, contract/tool and baseline/registry hashes; exclusive ownership of the reserved absent executor run; all unrelated changes preserved.']
    t['acceptance']=['Independently account for all source regions on physical pages 5-8, including headings, clauses, notes, examples, tables/legends, diagrams/components and editorial furniture, with explicit ledger and gaps.','Retain full 44-page wgc-inventory-1 accounting; preserve exact accepted pages/regions/evidence 1-4 and placeholders 9-44; extend the accepted persisted registry without identity remapping.','Keep exact current source/page/region/bbox and text/PNG/crop-PDF evidence pins, reading order, uncertainty and continuations. Preserve the existing page-5 context identity/revision/evidence/link and map it to a distinct authored identity without denominator duplication.','Report task/full/context denominators separately; context is zero, partial/unprocessed stays a gap, bbox/PNG does not grant representation, editorial classification does not grant exclusion or semantic acceptance.','A separate independent reviewer compares all four assigned original pages against the complete frozen ledger and verifies unchanged prior scope, continuation bounds, correspondence, tool/source hashes and every submitted artifact.']
    t['tests']=['Root inventory.validate/CLI validates byte-pinned PDF, strict pypdf and Poppler 44-page counts, actual all-page geometry, schema/canonical revisions, registry, partitions and reading order.','Visual inspection of every original assigned page 5-8 and all proposed region boundaries/components; exact current evidence artifact SHA256/bytes, rational crop bounds, Unicode offsets, page_basis_hash and predicted/actual PNG dimensions.','Compare accepted nested records 1-4, 9-44 placeholders, registry entries, old evidence and old links with baseline; repeat persisted-registry authoring in fresh output directories and compare identical canonical bytes/IDs.','Check zero context denominator, page-5 context-to-new-author correspondence and recorded bounded continuation access; explicit content/representation/geometric gaps at all levels.','Run explicit unchanged tests/sources with fresh short basetemp and -p no:cacheprovider; scripts/check.ps1 -Task IG-2B02 while active; workflow validate; git diff --check. Reproduce/escalate tool failures without editing tools/tests/contracts or weakening checks.']
    t['exclusions'] += ['No changes to src/wgc/sources, tests, contracts or frozen IG-2A/IG-2B01 artifacts; no source download. Queue structural edits are coordinator-owned; executor status updates only through workflow transitions.','No analysis of pages outside 5-8 except exact scoped continuation context. No broad adjacent-page probes, represented/excluded promotions by assertion or source-IG whole-record review by inheritance.']
    policy=read('docs/work/context-policy.json')
    additions=t['context']+[source_pins['baseline']['path'],source_pins['persisted_registry']['path']]+[e[k]['path'] for e in context_evidence+parent_evidence for k in ['text','image','crop_pdf']]
    for rel in additions:
        if rel not in policy['allow'] and not any(p.endswith('/') and rel.startswith(p) for p in policy['allow']): policy['allow'].append(rel)
    Path('docs/work/context-policy.json').write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    Path('docs/work/queue.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    write('refinement.json',{'role':'coordinator','actor':ACTOR,'summary':'Only IG-2B02 contract refined; no claim or source authoring. Exact read allowlist additions, full-page structural accounting, immutable inheritance and bounded continuation policy.','allowlist_additions':[x for x in additions if x in policy['allow']],'scope':pin(RUN/'scope.json'),'source_pins':pin(RUN/'source-pins.json'),'dependencies':pin(RUN/'dependency-verification.json'),'model':None,'reasoning':None,'configuration_evidence':pin(RUN/'configuration.json')})
    print('Prepared coordinator scope:',RUN)

if __name__=='__main__': prepare()
