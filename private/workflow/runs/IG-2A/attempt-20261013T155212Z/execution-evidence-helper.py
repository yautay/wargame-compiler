from pathlib import Path
import json, hashlib, sys, subprocess, os, datetime, urllib.request, urllib.parse
from html.parser import HTMLParser

ROOT = Path('C:/repo/wargame-compiler')
RUN = 'private/workflow/runs/IG-2A/attempt-20261013T155212Z'
SOURCE = 'private/ig/sources/spqr-5e-official/revision-20261013T155212Z'
INVENTORY = 'private/ig/projects/spqr/sources/inventory/ig2a-20261013T155212Z'
ACTOR = 'codex-01a135f6-cdab-7723-bd6a-9e0044d12323'
PAGE = 'https://www.gmtgames.com/p-1118-spqr-deluxe-5th-edition.aspx'
OLD_HASH = 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
BUNDLE = 'C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/Lib/site-packages'
sys.path.insert(0,str(ROOT/'scripts'))
import workflow
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8-sig'))
def write(rel,data):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f: f.write(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def pin(rel): return {'path':rel,'sha256':sha(ROOT/rel)}
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def evidence(role, summary, artifacts):
    return dict(role=role,actor=ACTOR,summary=summary,criteria=read('docs/work/queue.json')['tasks'][5]['acceptance'],artifacts=[pin(x) for x in artifacts],model='gpt-6.1-sol',reasoning='high',configuration_evidence=RUN+'/configuration.json')
def command(args,name):
    start=utc(); t=__import__('time').monotonic(); p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
    write(RUN+'/'+name+'.json',dict(command=subprocess.list2cmdline(args),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,started_utc=start,ended_utc=utc(),wall_seconds=__import__('time').monotonic()-t))
    print(p.stdout[-3000:]); print(p.stderr[-3000:]); assert p.returncode==0
    return p
def scope():
    q=read('docs/work/queue.json'); task=next(t for t in q['tasks'] if t['id']=='IG-2A'); assert task['status']=='planned'
    write(RUN+'/queue-before.json',q)
    write(RUN+'/configuration.json',dict(thread_id=ACTOR.removeprefix('codex-'),model='gpt-6.1-sol',reasoning='high',observed_current_turn_context_utc='2026-10-13T15:52:12.187Z',session_metadata_file='C:/Users/yauta/.codex/sessions/2026/10/13/rollout-2026-10-13T17-52-09-01a135f6-cdab-7723-bd6a-9e0044d12323.jsonl',fields={'payload.model':'gpt-6.1-sol','payload.effort':'high','payload.collaboration_mode.settings.reasoning_effort':'high'},operator_message='potwierdzam',started_utc='2026-10-13T15:52:12.187Z',tokens=None,cost=None,operator_seconds=None))
    checks=[]; protected={}
    h=read('private/workflow/runs/IG-1E/completion-20261013/final-stage-handoff.json')
    for item in h['completed_tasks']:
        t=next(t for t in q['tasks'] if t['id']==item['task']); assert t['status']=='done'
        for k in ['delivery','independent_review','acceptance','coordinator_done']:
            a=item[k]; assert sha(ROOT/a['path'])==a['sha256']; protected[a['path']]=a['sha256']
        for a in read(item['delivery']['path'])['artifacts']:
            assert sha(ROOT/a['path'])==a['sha256'], a['path']; protected[a['path']]=a['sha256']
        checks.append(dict(task=t['id'],status=t['status'],evidence=item,delivery_artifacts_verified=len(read(item['delivery']['path'])['artifacts'])))
    write(RUN+'/dependency-verification.json',dict(tasks=checks,protected_hashes=protected,regenerated=False))
    git=subprocess.run(['git','status','--porcelain=v1','-z'],cwd=ROOT,capture_output=True,check=True)
    (ROOT/RUN/'git-status-before.bin').write_bytes(git.stdout)
    task['write_scope'] += [SOURCE+'/',INVENTORY+'/',RUN+'/']
    write(RUN+'/acquisition-scope.json',dict(task='IG-2A',role='coordinator',actor=ACTOR,source_directory=SOURCE,inventory_directory=INVENTORY,run_directory=RUN,network_allowlist=[PAGE,'https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/gbsp/SPQR%2BDeluxe_Rule%2Bbook_WEB.pdf'],real_verification_pages=[1,2,3,4],structural_scope='All physical pages; geometry and embedded labels only. No substantive inventory outside 1-4.',decision='Acquisition paths pinned before acquisition. Final input hashes and measured count required before readiness.',coordinate_contract='Unrotated effective CropBox top-left; PDF points and integer page millionths; clockwise rotation to displayed frame; UserUnit explicitly handled.'))
    policy=read('docs/work/context-policy.json')
    for rel in [RUN+'/acquisition-scope.json',RUN+'/configuration.json',RUN+'/dependency-verification.json',RUN+'/refinement.json',SOURCE+'/provenance.json',SOURCE+'/rulebook.pdf']:
        if rel not in policy['allow']: policy['allow'].append(rel)
    (ROOT/'docs/work/context-policy.json').write_text(json.dumps(policy,indent=2)+'\n',encoding='utf-8')
    (ROOT/'docs/work/queue.json').write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    workflow.render(q,ROOT); workflow.validate(q,ROOT)
    print('Scope pinned. Dependency frozen evidence verified:',len(protected))
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.href=None; self.text=''; self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a': self.href=dict(attrs).get('href'); self.text=''
    def handle_data(self,d):
        if self.href: self.text+=d
    def handle_endtag(self,tag):
        if tag=='a' and self.href: self.links.append((self.text.strip(),self.href)); self.href=None
class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self): self.records=[]
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if urllib.parse.urlsplit(newurl).hostname not in {'www.gmtgames.com','gmtgames.com','gmtwebsiteassets.s3.us-west-2.amazonaws.com'}: raise ValueError('Redirect outside authorization')
        self.records.append(dict(from_url=req.full_url,status=code,to_url=newurl)); return super().redirect_request(req,fp,code,msg,headers,newurl)
def acquire():
    assert SOURCE+'/' in next(t for t in read('docs/work/queue.json')['tasks'] if t['id']=='IG-2A')['write_scope']
    handler=Redirects(); opener=urllib.request.build_opener(handler)
    def fetch(url):
        started=utc()
        with opener.open(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'*/*'}),timeout=60) as r:
            body=r.read(); meta=dict(requested_url=url,final_url=r.url,status=r.status,headers=dict(r.headers),redirects=list(handler.records),started_utc=started,acquired_utc=utc(),bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
        handler.records.clear(); return body,meta
    body,page_meta=fetch(PAGE); parser=Links(); parser.feed(body.decode('utf-8',errors='replace'))
    links=[href for label,href in parser.links if label=='5th Edition Rulebook']; assert len(links)==1,links
    url=urllib.parse.urljoin(PAGE,links[0]); assert urllib.parse.unquote(url)==urllib.parse.unquote(read(RUN+'/acquisition-scope.json')['network_allowlist'][1]),url
    (ROOT/SOURCE).mkdir(parents=True,exist_ok=False)
    (ROOT/SOURCE/'referring-page.html').write_bytes(body); write(SOURCE+'/referring-page-http.json',page_meta)
    pdf,meta=fetch(url); assert pdf.startswith(b'%PDF-')
    (ROOT/SOURCE/'rulebook.pdf').write_bytes(pdf); write(SOURCE+'/rulebook-http.json',meta)
    sys.path.insert(0,BUNDLE); from pypdf import PdfReader
    reader=PdfReader(ROOT/SOURCE/'rulebook.pdf'); count=len(reader.pages)
    p=subprocess.run(['pdfinfo',str(ROOT/SOURCE/'rulebook.pdf')],capture_output=True,text=True,check=True)
    (ROOT/SOURCE/'pdfinfo.txt').write_text(p.stdout,encoding='utf-8')
    import re
    independent=int(re.search(r'^Pages:\s+(\d+)',p.stdout,re.M)[1]); assert independent==count
    text=reader.pages[0].extract_text()
    assert '5th Edition' in text or 'Fifth Edition' in text
    (ROOT/SOURCE/'edition-page-001.txt').write_text(text,encoding='utf-8')
    write(SOURCE+'/provenance.json',dict(format='wgc-official-source-acquisition-1',source_id='source:spqr:5e:core',source_revision=meta['sha256'],pdf=pin(SOURCE+'/rulebook.pdf'),referring_page=PAGE,link_label='LIVING RULES / 5th Edition / 5th Edition Rulebook',http=meta,referring_page_evidence=pin(SOURCE+'/referring-page.html'),bytes=len(pdf),sha256=meta['sha256'],edition='5th Edition',edition_evidence=pin(SOURCE+'/edition-page-001.txt'),publication_date=None,publication_date_reason='No verified publication date; HTTP Last-Modified and PDF metadata are not publication dates.',page_count=count,independent_page_counts={'pypdf':count,'poppler_pdfinfo':independent},previous_frozen_sha256=OLD_HASH,byte_identity_to_previous=meta['sha256']==OLD_HASH,identity_to_wgu_original='unknown',identity_note='Fresh official acquisition provenance is separate from verified byte identity.',metadata={k:str(v) for k,v in (reader.metadata or {}).items()}))
    print('Fresh official PDF acquired:',len(pdf),meta['sha256'],'pages:',count,'same old bytes:',meta['sha256']==OLD_HASH)
def finish_acquisition():
    sys.path.insert(0,BUNDLE); from pypdf import PdfReader
    reader=PdfReader(ROOT/SOURCE/'rulebook.pdf'); meta=read(SOURCE+'/rulebook-http.json'); pdf=(ROOT/SOURCE/'rulebook.pdf').read_bytes()
    text=reader.pages[0].extract_text(); print(text[:600]); assert '5th Edition' in text or 'Fifth Edition' in text
    (ROOT/SOURCE/'edition-page-001.txt').write_text(text,encoding='utf-8')
    import re
    count=len(reader.pages); independent=int(re.search(r'^Pages:\s+(\d+)',(ROOT/SOURCE/'pdfinfo.txt').read_text(),re.M)[1]); assert count==independent
    write(SOURCE+'/provenance.json',dict(format='wgc-official-source-acquisition-1',source_id='source:spqr:5e:core',source_revision=meta['sha256'],pdf=pin(SOURCE+'/rulebook.pdf'),referring_page=PAGE,link_label='LIVING RULES / 5th Edition / 5th Edition Rulebook',http=meta,referring_page_evidence=pin(SOURCE+'/referring-page.html'),bytes=len(pdf),sha256=meta['sha256'],edition='5th Edition',edition_evidence=pin(SOURCE+'/edition-page-001.txt'),publication_date=None,publication_date_reason='No verified publication date; HTTP Last-Modified and PDF metadata are not publication dates.',page_count=count,independent_page_counts={'pypdf':count,'poppler_pdfinfo':independent},previous_frozen_sha256=OLD_HASH,byte_identity_to_previous=meta['sha256']==OLD_HASH,identity_to_wgu_original='unknown',identity_note='Fresh official acquisition provenance is separate from verified byte identity.',metadata={k:str(v) for k,v in (reader.metadata or {}).items()}))
    write(RUN+'/preparation-corrections.json',dict(commands=[{'operation':'workflow context','exit_code':2,'resolution':'Use supported packet command after readiness.'},{'operation':'sandbox git status','exit_code':128,'resolution':'Read current worktree with authorized escalation.'},{'operation':'acquire URL equality','exit_code':1,'resolution':'Compare percent-decoded exact linked asset URLs; + and %2B encode identical object path.'},{'operation':'acquire edition text helper','exit_code':1,'resolution':'Downloaded PDF and HTTP evidence preserved. Use bundled pypdf instead of unavailable PATH pdftotext; no repeat download.'}]))
    print('Verified acquisition:',len(pdf),meta['sha256'],'pages',count,'same previous',meta['sha256']==OLD_HASH)
def ready_claim():
    q=read('docs/work/queue.json'); t=next(t for t in q['tasks'] if t['id']=='IG-2A'); assert t['status']=='planned'
    src=read(SOURCE+'/provenance.json')
    refinement=dict(role='coordinator',actor=ACTOR,task='IG-2A',input_pins=[pin(SOURCE+'/rulebook.pdf'),pin(SOURCE+'/provenance.json'),pin(RUN+'/dependency-verification.json')],source_revision=src['sha256'],physical_page_count=src['page_count'],real_pages=[1,2,3,4],allowed_write_scope=t['write_scope'],contracts={'version':'wgc-inventory-1','identity':'Persisted UUID registry keyed by explicit author page/region keys, bound to exact source revision; no geometry/content-derived region identity or auto-rematch on source change.','geometry':'PDF native bottom-left points and UserUnit to unrotated effective CropBox top-left integer millionths; MediaBox intersection; explicit clockwise display rotation. Serialized native box coordinates are integer micro-points; UserUnit is a rational.','reading_order':'Explicit region IDs and continuation/note links, never inferred from extraction ordering.','evidence':'Separate UTF-8 text and crop PNG files with paths, bytes, SHA256, extraction/render settings and exact region revision/bbox/source pins.','coverage':'Disjoint inventory boxes; context excluded from denominator; duplicate IDs/keys and overlapping inventory rejected. Three representation levels; partial/unprocessed never represented; approved exclusion boundary required. Per-page uncovered area remains an explicit gap.','structural_seed':'All physical pages receive an unprocessed full-page placeholder; no substantive classification or source-meaning coverage granted. IG-2B replaces placeholders in its bounded outputs.','validation':'Missing page; multi-column explicit ordering; table notes; cross-page links; duplicate/overlap; CropBox/MediaBox/UserUnit/rotations; revision and artifact tamper; path escapes; source mutation; replay; independent page count.'},dependencies='All IG-1A through IG-1E done evidence and delivery files rehashed; no regeneration.',downstream_implications='Measured 44 pages supports existing 11 four-page partitions numerically. Each future IG-2B packet must pin this fresh acquisition and IG-2A contract; no downstream state or content changed.',measurement=dict(started_utc='2026-10-13T15:52:12.187Z',tokens=None,cost=None,operator_seconds=None),unresolved='Independent technical review and all substantive page inventory remain pending; WGU-original identity unknown.')
    write(RUN+'/refinement.json',refinement)
    t['kind']='implementation'
    t['inputs']=[f"Official PDF {SOURCE}/rulebook.pdf SHA256 {src['sha256']}; independent physical page count {src['page_count']}",f"Fresh official provenance {SOURCE}/provenance.json SHA256 {sha(ROOT/SOURCE/'provenance.json')}",'Synthetic public layout/geometry/coverage cases; real evidence verification physical pages 1-4 only; all-page geometry and embedded-label accounting.',f'Final coordinator refinement {RUN}/refinement.json; stable persisted identity and evidence/coverage contracts.']
    t['context'] += ['contracts/ig/README.md','src/wgc/contracts/source.py',RUN+'/configuration.json',RUN+'/refinement.json',SOURCE+'/provenance.json',SOURCE+'/rulebook.pdf']
    t['outputs']=['contracts/ig/regions.schema.json and documented wgc-inventory-1 contract','Local source page/region inventory, coordinate/evidence/coverage tools and synthetic tests',INVENTORY+'/ with 44-page structural accounting, registry, verification evidence for pages 1-4 and repeatability report',RUN+'/ frozen delivery manifest and independent-review handoff']
    t['exclusions']=[x.replace('online services,','online services except the explicitly authorized official GMT referring page and its linked 5E PDF,') for x in t['exclusions']]
    t['tests'] += ['Explicit tests/sources with fresh short basetemp and -p no:cacheprovider; check.ps1 -Task IG-2A while active; workflow validate; git diff --check.', 'Two fresh structural inventories with reused persisted registry; compare identical canonical bytes and region identities; independent Poppler and pypdf count; inspect real rendered pages 1-4.']
    (ROOT/'docs/work/queue.json').write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); workflow.render(q,ROOT); workflow.validate(q,ROOT)
    write(RUN+'/ready.json',evidence('coordinator','Refinement resolved, exact acquisition and output scope pinned; dependencies verified.',[RUN+'/refinement.json',RUN+'/configuration.json',SOURCE+'/provenance.json',RUN+'/dependency-verification.json']))
    command([str(ROOT/'.venv/Scripts/python.exe'),'scripts/workflow.py','transition','--task','IG-2A','--to','ready','--evidence',RUN+'/ready.json'],'ready-transition')
    result=command([str(ROOT/'.venv/Scripts/python.exe'),'scripts/workflow.py','packet','--task','IG-2A'],'packet-command')
    packet=result.stdout.strip(); manifest=read(packet+'/manifest.json'); assert sha(ROOT/packet/'context.txt')==manifest['context_sha256']; assert manifest['queue_sha256']==sha(ROOT/'docs/work/queue.json')
    for a in manifest['files']: assert workflow.permitted(ROOT,a['path']) and sha(ROOT/a['path'])==a['sha256']
    write(RUN+'/packet-verification.json',dict(packet=packet,manifest=pin(packet+'/manifest.json'),context=pin(packet+'/context.txt'),files_verified=len(manifest['files']),queue_sha256=manifest['queue_sha256'],source_binary_hashed_not_dumped=True))
    write(RUN+'/checkpoint-claim.json',dict(task='IG-2A',actor=ACTOR,attempt=RUN,model='gpt-6.1-sol',reasoning='high',configuration=pin(RUN+'/configuration.json'),packet=pin(packet+'/manifest.json'),input_hashes=refinement['input_pins'],base_file_hashes={p:sha(ROOT/p) if (ROOT/p).is_file() else None for p in ['contracts/ig/regions.schema.json','src/wgc/sources/inventory.py','tests/sources/test_inventory.py']},completed_criteria=['Refinement','Official acquisition','Dependency verification','Fresh allowlisted packet verification'],checks=[],blocker=None,next_operation='Implement refined inventory contracts/tools/tests; preserve all prior changes.'))
    write(RUN+'/claim.json',evidence('executor','Claim only IG-2A after verified Sol/high, readiness and packet verification.',[RUN+'/checkpoint-claim.json',RUN+'/packet-verification.json',RUN+'/configuration.json']))
    command([str(ROOT/'.venv/Scripts/python.exe'),'scripts/workflow.py','transition','--task','IG-2A','--to','in_progress','--evidence',RUN+'/claim.json'],'claim-transition')
    print('PACKET='+packet)
def install():
    import shutil
    assert next(t for t in read('docs/work/queue.json')['tasks'] if t['id']=='IG-2A')['status']=='in_progress'
    staging=Path(__file__).parent/'product'; files=[]
    for p in staging.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(staging).as_posix(); assert rel.startswith(('src/wgc/sources/','tests/sources/')) or rel=='contracts/ig/regions.schema.json'
        target=ROOT/rel; assert not target.exists(),f'Preserve preexisting file: {rel}'
        target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,target); files.append(pin(rel))
    write(RUN+'/checkpoint-implementation.json',dict(task='IG-2A',actor=ACTOR,model='gpt-6.1-sol',reasoning='high',configuration=pin(RUN+'/configuration.json'),changed_files=files,completed=['Inventory contracts and local tools','Synthetic validation cases implemented'],checks=[],blocker=None,next_operation='Run source tests, full-PDF structural inventory replay, and real pages 1-4 evidence verification.'))
    print('Installed new scoped files:',len(files))
def tests():
    env=os.environ.copy(); env['PYTHONPATH']=os.pathsep.join([str(ROOT/'src'),str(ROOT/'.venv/Lib/site-packages'),BUNDLE]); env['PYTHONDONTWRITEBYTECODE']='1'
    import tempfile,uuid
    basetemp=str(Path(tempfile.gettempdir())/('wg2a-'+uuid.uuid4().hex[:8])); assert not Path(basetemp).exists()
    args=[str(ROOT/'.venv/Scripts/python.exe'),'-m','pytest','tests/sources','-q','--basetemp',basetemp,'-p','no:cacheprovider','--tb=short']
    start=utc(); time=__import__('time'); clock=time.monotonic(); p=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True)
    number=len(list((ROOT/RUN).glob('sources-tests-*.json')))+1
    write(RUN+f'/sources-tests-{number:02d}.json',dict(command=subprocess.list2cmdline(args),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,started_utc=start,ended_utc=utc(),wall_seconds=time.monotonic()-clock))
    print(p.stdout); print(p.stderr); print('EXIT',p.returncode)
def update_owned():
    import shutil
    staging=Path(__file__).parent/'product'
    files=[]
    for p in staging.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(staging).as_posix(); assert rel.startswith(('src/wgc/sources/','tests/sources/')) or rel=='contracts/ig/regions.schema.json'
        shutil.copyfile(p,ROOT/rel); files.append(pin(rel))
    number=len(list((ROOT/RUN).glob('checkpoint-update-*.json')))+1
    write(RUN+f'/checkpoint-update-{number:02d}.json',dict(task='IG-2A',actor=ACTOR,changed_files=files,corrections=['Fresh short existing temp root','Fix test stale reference after resealing copied regions','Attach pypdf pages to derived writer before scaling; preserve original','Add CLI, metadata-label and duplicate-context probes'],next_operation='Rerun changed source tests and complete real source verification.'))
def verify_real():
    import shutil,time,importlib.metadata
    env=os.environ.copy(); env['PYTHONPATH']=os.pathsep.join([str(ROOT/'src'),str(ROOT/'.venv/Lib/site-packages'),BUNDLE]); env['PYTHONDONTWRITEBYTECODE']='1'
    sys.path[:0]=[str(ROOT/'src'),BUNDLE]
    from wgc.sources.inventory import validate
    from wgc.contracts.source import load_json
    base=[str(ROOT/'.venv/Scripts/python.exe'),'-m','wgc.sources']
    args=['inventory','--pdf',SOURCE+'/rulebook.pdf','--provenance',SOURCE+'/provenance.json','--source-id','source:spqr:5e:core','--sha256',OLD_HASH]
    def run(arguments,name):
        start=utc(); clock=time.monotonic(); p=subprocess.run(base+arguments,cwd=ROOT,env=env,capture_output=True,text=True)
        write(RUN+'/'+name+'.json',dict(command=subprocess.list2cmdline(base+arguments),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,started_utc=start,ended_utc=utc(),wall_seconds=time.monotonic()-clock))
        print(name,p.returncode,p.stdout[-200:]); print(p.stderr[-1500:]); assert p.returncode==0
    run(args+['--output',INVENTORY+'/seed'],'full-inventory-command')
    run(args+['--registry',INVENTORY+'/seed/identity-registry.json','--output',INVENTORY+'/replay'],'full-replay-command')
    for name in ['inventory.json','identity-registry.json','coverage.json']:
        assert (ROOT/INVENTORY/'seed'/name).read_bytes()==(ROOT/INVENTORY/'replay'/name).read_bytes()
    run(['evidence','--inventory',INVENTORY+'/seed/inventory.json','--pages','1','2','3','4','--output',INVENTORY+'/evidence'],'real-evidence-command')
    doc=load_json(ROOT/INVENTORY/'evidence/inventory.json'); report=validate(doc,ROOT)
    assert len(doc['pages'])==44 and len(doc['evidence'])==4
    assert all(report['levels'][level]['unprocessed']==44 and report['levels'][level]['represented']==0 for level in report['levels'])
    write(INVENTORY+'/verification.json',dict(source_revision=OLD_HASH,measured_pages=44,independent_page_counts=doc['source']['independent_counts'],replay_comparison='All inventory/registry/coverage bytes identical using persisted registry.',compared_hashes={name:sha(ROOT/INVENTORY/'seed'/name) for name in ['inventory.json','identity-registry.json','coverage.json']},verified_real_pages=[1,2,3,4],evidence_inventory=pin(INVENTORY+'/evidence/inventory.json'),coverage=report,substantive_inventory_completed=False,downstream='Existing 11 four-page partitions match measured count numerically; future packets must pin new acquisition/contract. No IG-2B task executed or made ready.'))
    versions={n:importlib.metadata.version(n) for n in ['pypdf','pdfplumber','Pillow','reportlab']}
    tools={n:dict(path=shutil.which(n),sha256=sha(shutil.which(n))) for n in ['pdfinfo','pdftoppm']}
    write(RUN+'/toolchain.json',dict(python_executable=str(ROOT/'.venv/Scripts/python.exe'),python_version=sys.version,bundled_site_packages=BUNDLE,bundle_version='26.1011.11113',libraries=versions,executables=tools,render_dpi=144,render_flags=['-singlefile','-cropbox','-png'],no_install_or_global_config_changes=True,process_pythonpath=env['PYTHONPATH']))
    write(RUN+'/checkpoint-verification.json',dict(task='IG-2A',actor=ACTOR,model='gpt-6.1-sol',reasoning='high',completed=['39 public synthetic source tests passed','44-page structural accounting','Byte-identical registry replay','Exact text/render evidence pages 1-4'],outputs=[pin(INVENTORY+'/evidence/inventory.json'),pin(INVENTORY+'/verification.json')],next_operation='Inspect all four real PNG pages, run check.ps1 and workflow/diff validation, verify preservation, freeze delivery for independent review.'))
def visual_and_checks():
    import time
    env=os.environ.copy(); env['PYTHONPATH']=os.pathsep.join([str(ROOT/'src'),str(ROOT/'.venv/Lib/site-packages'),BUNDLE]); env['PYTHONDONTWRITEBYTECODE']='1'
    sys.path[:0]=[str(ROOT/'src'),BUNDLE]
    from PIL import Image,ImageChops
    from wgc.sources.inventory import seal,validate
    from wgc.contracts.source import canonical_bytes,load_json
    direct=ROOT/INVENTORY/'direct-original-render'; direct.mkdir(exist_ok=False)
    p=subprocess.run(['pdftoppm','-f','1','-l','4','-cropbox','-r','144','-png',str(ROOT/SOURCE/'rulebook.pdf'),str(direct/'page')],cwd=ROOT,capture_output=True,text=True)
    write(RUN+'/direct-render-command.json',dict(command='pdftoppm -f 1 -l 4 -cropbox -r 144 -png '+SOURCE+'/rulebook.pdf '+INVENTORY+'/direct-original-render/page',exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)); assert p.returncode==0
    comparisons=[]
    for number in [1,2,3,4]:
        image=ROOT/INVENTORY/f'evidence/page-{number:03d}-region-000/image.png'
        ref=next(direct.glob(f'page-{number:02d}.png'))
        with Image.open(image) as a,Image.open(ref) as b:
            assert a.size==b.size and ImageChops.difference(a.convert('RGB'),b.convert('RGB')).getbbox() is None
        comparisons.append(dict(pdf_page=number,derived_png_sha256=sha(image),direct_original_png_sha256=sha(ref),pixels_identical=True))
    doc=load_json(ROOT/INVENTORY/'evidence/inventory.json')
    for p in doc['pages']:
        if p['pdf_page'] in [2,3,4]:
            ev=next(e for e in doc['evidence'] if e['pdf_page']==p['pdf_page'])
            p['label']=dict(status='verified',value=str(p['pdf_page']),reason='Executor visual observation of printed header marker in exact PNG; technical locator only, no source meaning approval.',evidence=ev['id'])
        elif p['pdf_page']==1:
            p['label']=dict(status='unknown',value=None,reason='Cover has no visually observed printed page marker. Text-layer number is not used as printed-label proof.',evidence=None)
    doc['pages']=[seal(p) for p in doc['pages']]; doc=seal(doc); report=validate(doc,ROOT)
    (ROOT/INVENTORY/'verified-inventory.json').write_bytes(canonical_bytes(doc)+b'\n')
    (ROOT/INVENTORY/'verified-coverage.json').write_bytes(canonical_bytes(report)+b'\n')
    write(RUN+'/visual-verification.json',dict(actor=ACTOR,pages=[1,2,3,4],method='All four 144-DPI PNGs inspected through view_image; derived crops compared pixel-for-pixel with direct rendering of original PDF.',comparisons=comparisons,observations='No clipping or missing graphics observed. Physical 2,3,4 printed labels observed; cover label remains unknown; 5-44 not visually reviewed.',parser_warning='pypdf reports non-zero-indexed Xref and corrects object IDs in memory. Original downloaded SHA256 remains unchanged; independent Poppler count and direct renders pass.',semantic_acceptance=False))
    checks=[([str(ROOT/'.venv/Scripts/python.exe'),'scripts/workflow.py','validate'],'workflow-check'),(['git','diff','--check'],'diff-check'),(['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-2A'],'project-check')]
    for args,name in checks:
        start=utc(); clock=time.monotonic(); result=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True)
        write(RUN+'/'+name+'.json',dict(command=subprocess.list2cmdline(args),exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr,started_utc=start,ended_utc=utc(),wall_seconds=time.monotonic()-clock))
        print(name,result.returncode,result.stdout[-2000:],result.stderr[-1500:]); assert result.returncode==0
def normalize_views():
    q=read('docs/work/queue.json'); files=['docs/work/queue.json','docs/work/context-policy.json']
    for rel in files:
        body=(ROOT/rel).read_text(encoding='utf-8')
        with (ROOT/rel).open('w',encoding='utf-8',newline='\n') as f: f.write(body)
    for rel,body in workflow.views(q).items():
        if (ROOT/rel).read_bytes()!=body.encode('utf-8'):
            with (ROOT/rel).open('w',encoding='utf-8',newline='\n') as f: f.write(body)
    workflow.validate(q,ROOT)
    number=len(list((ROOT/RUN).glob('line-ending-correction-*.json')))+1
    write(RUN+f'/line-ending-correction-{number:02d}.json',dict(reason='Existing Windows workflow renderer writes CRLF; repository eol=lf. Serialize coordinator queue/policy and generated views with explicit LF after transitions. No workflow script, task content outside IG-2A, staged files, frozen artifacts or assertions changed.',queue_sha256=sha(ROOT/'docs/work/queue.json')))
def final_checks():
    import time
    normalize_views()
    env=os.environ.copy(); env['PYTHONPATH']=os.pathsep.join([str(ROOT/'src'),str(ROOT/'.venv/Lib/site-packages'),BUNDLE]); env['PYTHONDONTWRITEBYTECODE']='1'
    for args,name in [(['git','diff','--check'],'diff-check-final'),(['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-2A'],'project-check'),([str(ROOT/'.venv/Scripts/python.exe'),'scripts/workflow.py','validate'],'workflow-check-final')]:
        start=utc(); clock=time.monotonic(); result=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True)
        write(RUN+'/'+name+'.json',dict(command=subprocess.list2cmdline(args),exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr,started_utc=start,ended_utc=utc(),wall_seconds=time.monotonic()-clock))
        print(name,result.returncode,result.stdout[-2000:],result.stderr[-1000:]); assert result.returncode==0
def freeze():
    import shutil,time
    q=read('docs/work/queue.json'); before=read(RUN+'/queue-before.json'); task=next(t for t in q['tasks'] if t['id']=='IG-2A'); assert task['status']=='in_progress'
    protected=read(RUN+'/dependency-verification.json')['protected_hashes']
    for rel,expected in protected.items(): assert sha(ROOT/rel)==expected,rel
    unchanged=[]
    for t in q['tasks']:
        if t['id']=='IG-2A': continue
        prior=next(x for x in before['tasks'] if x['id']==t['id']); assert t==prior,t['id']; unchanged.append(t['id'])
    current_status=subprocess.run(['git','status','--porcelain=v1','-z'],cwd=ROOT,capture_output=True,check=True).stdout
    (ROOT/RUN/'git-status-final.bin').write_bytes(current_status)
    def states(raw): return {s[3:]:s[:2] for s in raw.decode('utf-8').split('\x00') if s}
    a=states((ROOT/RUN/'git-status-before.bin').read_bytes()); b=states(current_status)
    for path,status in a.items(): assert path in b and status[0]==b[path][0],path
    write(RUN+'/preservation.json',dict(frozen_dependency_artifacts_verified=len(protected),changed_frozen_artifacts=[],other_task_records_byte_equivalent_as_json=unchanged,all_prior_staged_statuses_preserved=True,existing_status_entries=len(a),commit_reset_clean_stash_push_executed=False,new_chats_agents_automations=False))
    write(RUN+'/queue-at-freeze.json',q)
    shutil.copyfile(Path(__file__),ROOT/RUN/'execution-evidence-helper.py')
    shutil.copyfile(Path(__file__).parent/'build_schema.py',ROOT/RUN/'schema-authoring-helper.py')
    checks=[]
    for rel in ['sources-tests-03.json','full-inventory-command.json','full-replay-command.json','real-evidence-command.json','direct-render-command.json','project-check.json','workflow-check-final.json','diff-check-final.json']:
        record=read(RUN+'/'+rel); assert record['exit_code']==0
        checks.append(dict(command=record['command'],exit_code=record['exit_code'],evidence=pin(RUN+'/'+rel)))
    project=read(RUN+'/project-check.json'); import re
    checkroot=re.search(r'LOG_ROOT=([^\r\n]+)',project['stdout'])[1]
    components=json.loads((Path(checkroot)/'result.json').read_text(encoding='utf-8-sig')); assert all(components[k]==0 for k in ['plan_exit','dry_run_exit','tests_exit','diff_exit'])
    write(RUN+'/required-check-components.json',dict(check_directory=checkroot,result=components,result_sha256=sha(Path(checkroot)/'result.json'),project_tests='102 passed',source_tests='39 passed',final_required_checks=checks,failed_preparation_or_development_runs_preserved=['sources-tests-01.json','sources-tests-02.json','diff-check.json','preparation-corrections.json'],no_assertions_weakened=True))
    start=datetime.datetime.fromisoformat(read(RUN+'/configuration.json')['started_utc']); end=datetime.datetime.now(datetime.timezone.utc)
    measurement=dict(started_utc=start.isoformat(),ended_utc=end.isoformat(),wall_seconds=(end-start).total_seconds(),input_tokens=None,output_tokens=None,cost=None,operator_seconds=None,unknown_reason='No measured task token/cost totals or operator-time report are available. Per-command clocks recorded in command evidence.',requested_model='gpt-6.1-sol',requested_reasoning='high',actual_model='gpt-6.1-sol',actual_reasoning='high')
    write(RUN+'/measurement.json',measurement)
    files=[]
    for directory in ['src/wgc/sources','tests/sources',SOURCE,INVENTORY,RUN]:
        for p in (ROOT/directory).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                files.append(p.relative_to(ROOT).as_posix())
    files.append('contracts/ig/regions.schema.json')
    packet=read(RUN+'/packet-verification.json')['packet']
    files += [packet+'/manifest.json',packet+'/context.txt','docs/work/context-policy.json']
    artifacts=[dict(**pin(rel),bytes=(ROOT/rel).stat().st_size) for rel in sorted(set(files))]
    manifest=dict(format='wgc-delivery-manifest-1',task='IG-2A',actor=ACTOR,configuration=pin(RUN+'/configuration.json'),input_packet=pin(packet+'/manifest.json'),exact_inputs=read(RUN+'/refinement.json')['input_pins'],artifacts=artifacts,criteria=[dict(criterion=c,status='met_for_tooling_scope',evidence=['39 synthetic tests','44 measured pages; deterministic replay','4 real page evidence links; original/derived PNG equality']) for c in task['acceptance']],checks=checks,measurement=measurement,independent_review='pending',semantic_acceptance_granted=False,unresolved=['Substantive source inventory remains unprocessed on all 44 pages; IG-2B not executed.','Printed labels beyond pages 2-4 are unknown; cover has no visually observed marker.','pypdf corrected non-zero-indexed Xref IDs in memory; original PDF bytes remain unchanged and Poppler/direct rendering agree.','Source identity to WGU unavailable original remains unknown.','Human authorization claims on exclusion metadata must be separately verified; tools do not authenticate humans.','No independent technical review has occurred.'],defects={'independent_review_counts':None,'development_failures':{'test_fixture_reference':1,'environment_setup':2,'windows_line_endings':1},'all_observed_development_failures_resolved':True},scope_control='Only IG-2A product scope and coordinator queue/policy/views changed. Other task records and accepted frozen artifacts preserved.')
    write(RUN+'/delivery-manifest.json',manifest)
    handoff=f'''# IG-2A frozen delivery for independent technical review

Task status at handoff: review pending. Executor: {ACTOR}, actual GPT-6.1 Sol / high, confirmed by this session metadata and operator message. No self-approval or done transition. Work remains local and uncommitted.

## Frozen result

- Manifest: {RUN}/delivery-manifest.json
- Manifest SHA256: {sha(ROOT/RUN/'delivery-manifest.json')}
- Exact input packet: {packet}/manifest.json (SHA256 {sha(ROOT/packet/'manifest.json')})
- Product: src/wgc/sources/; tests/sources/; contracts/ig/regions.schema.json
- Final private inventory: {INVENTORY}/verified-inventory.json (SHA256 {sha(ROOT/INVENTORY/'verified-inventory.json')})
- Acquisition: {SOURCE}/provenance.json and rulebook.pdf
- Official PDF SHA256: {OLD_HASH}; 3,965,827 bytes; independently measured 44 pages.

The fresh official GMT acquisition is byte-identical to the previous frozen 5E source. It has its own referring-page/HTTP metadata, UTC acquisition, redirects, edition evidence and original bytes. No publication date was invented. All old source snapshots, registries and IG-1 deliveries remain unchanged. Identity to WGU's missing original remains unknown.

## Contracts and criteria

All three task criteria are met for the refined tooling scope: complete physical-page addressing and explicit printed-label status; persisted source-bound page/region identity and exact revisions; CropBox/MediaBox/UserUnit/rotation conversions; separate render/text/uncertainty/order; typed note/continuation links; disjoint denominator with context excluded; visible geometric gaps and represented/partial/unprocessed/excluded accounting. The schema and README define the exact conventions. Exclusion claims are not authenticated by code and cannot grant human semantic acceptance.

Every one of the 44 pages has an unprocessed structural placeholder. No substantive source region inventory or publisher meaning coverage is claimed. Printed labels 2, 3 and 4 were visually observed in exact images; cover and 5-44 remain unknown. Reading order of substantive regions is not inferred from machine extraction. Stable identity replay produced byte-identical inventory, registry and coverage files. Evidence verification used only physical pages 1-4, with four exact text/PNG/derived-PDF locators and 144-DPI parameters. All four derived PNGs are pixel-identical to direct renders of the original PDF.

## Validation and preservation

39 explicit synthetic source tests passed with a fresh short basetemp and -p no:cacheprovider. Active scripts/check.ps1 -Task IG-2A passed all components and 102 project tests. Workflow validation and git diff --check exited zero. The manifest records actual commands, exits, times and hashes. Earlier failed setup/test/diff attempts are retained with their corrections; no assertions were weakened. Windows workflow rendering produced CRLF; coordinator output serialization restored LF without changing task content or workflow code.

301 frozen dependency files were rehashed unchanged. All 38 other task records equal their starting records and every prior staged status is preserved. No commit, reset, clean, stash, push, archive/Git-history access, neighboring-repository write, new chat, agent or automation occurred. Existing bundled libraries and binaries were used with process-only Python paths; versions and executable hashes are in toolchain.json.

Start UTC: {measurement['started_utc']}. Freeze UTC: {measurement['ended_utc']}. Elapsed wall seconds to freeze: {measurement['wall_seconds']:.3f}. Tokens, cost and operator time are null because no measured totals were available.

## Remaining gaps and next exact action

pypdf reports non-zero-indexed Xref and corrects object IDs in memory. Original downloaded bytes are unchanged; independent Poppler count and original/derived PNG comparison pass. This parser warning is retained for review. Full source meaning, independent review, human acceptance and executable readiness remain separate gates. No gameplay/runtime/compiler/POC or LLM legality code was added.

Measured 44 pages supports the existing 11 four-page IG-2B partitions numerically. Each later packet must pin this fresh official acquisition and the accepted inventory contract. No IG-2B packet was executed or made ready.

The operator supplies a separate reviewer with this handoff, the delivery manifest and exact artifact hashes. Reviewer confirms their current configuration independently, verifies the frozen hashes, examines public contract/tool/test files and only real PDF pages 1-4, reruns meaningful checks, and records findings without repairing executor files. Do not accept or mark IG-2A done until separate technical review and coordinator verification. Stop here; do not execute IG-2B.
'''
    with (ROOT/RUN/'delivery-handoff.md').open('x',encoding='utf-8',newline='\n') as f: f.write(handoff)
    delivery=evidence('executor','Frozen IG-2A inventory tooling delivered for separate technical review; no acceptance granted.',[a['path'] for a in artifacts]+[RUN+'/delivery-manifest.json',RUN+'/delivery-handoff.md'])
    delivery.update(checks=[{'command':c['command'],'exit_code':c['exit_code']} for c in checks],measurement=measurement,input_packet=pin(packet+'/manifest.json'),unresolved=manifest['unresolved'])
    write(RUN+'/delivery.json',delivery)
    command([str(ROOT/'.venv/Scripts/python.exe'),'scripts/workflow.py','transition','--task','IG-2A','--to','review','--evidence',RUN+'/delivery.json'],'review-transition')
    normalize_views()
    for a in delivery['artifacts']: assert sha(ROOT/a['path'])==a['sha256'],a['path']
    for args in [[str(ROOT/'.venv/Scripts/python.exe'),'scripts/workflow.py','validate'],['git','diff','--check']]:
        p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True); assert p.returncode==0,p.stderr+p.stdout
    write(RUN+'/final-seal.json',dict(task='IG-2A',status='review',delivery=pin(RUN+'/delivery.json'),manifest=pin(RUN+'/delivery-manifest.json'),handoff=pin(RUN+'/delivery-handoff.md'),queue=pin('docs/work/queue.json'),review_transition=pin(RUN+'/review-transition.json'),all_delivery_artifacts_verified=len(delivery['artifacts']),checks=[{'command':'scripts/workflow.py validate','exit_code':0},{'command':'git diff --check','exit_code':0}],independent_review_started=False,ended_utc=utc()))
    out=Path(__file__).parent.parent/'outputs'; out.mkdir(exist_ok=True)
    shutil.copyfile(ROOT/RUN/'delivery-handoff.md',out/'IG-2A-handoff.md'); shutil.copyfile(ROOT/RUN/'delivery-manifest.json',out/'IG-2A-delivery-manifest.json'); shutil.copyfile(ROOT/RUN/'final-seal.json',out/'IG-2A-final-seal.json')
    print('Frozen delivery:',len(delivery['artifacts']),'artifacts. Queue IG-2A review. Other tasks unchanged.')
if __name__=='__main__': globals()[sys.argv[1]]()
