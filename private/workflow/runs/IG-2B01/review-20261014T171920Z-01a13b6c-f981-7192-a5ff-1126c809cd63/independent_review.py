"""Independent, bounded IG-2B01 reproduction; writes only this review directory."""
from pathlib import Path
import copy, hashlib, json, math, os, subprocess, sys, time
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'private/workflow/runs/IG-2B01/inventory-20261014T165724Z-01a13b57-40e6-78d2-9d17-0b3e91afba77'
BUNDLE = Path('C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/dependencies')
sys.path.insert(0, str(BUNDLE / 'python/Lib/site-packages'))
sys.path.insert(0, str(ROOT / 'src'))
os.environ['PYTHONPATH'] = os.pathsep.join([str(ROOT/'src'),str(BUNDLE/'python/Lib/site-packages')])
os.environ['PATH'] = str(BUNDLE/'native/poppler/Library/bin') + os.pathsep + os.environ['PATH']
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.dont_write_bytecode = True
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def save(name, data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now(): return datetime.now(timezone.utc).isoformat()
def run(name, args):
    start=now(); t=time.monotonic()
    p=subprocess.run([str(a) for a in args],cwd=ROOT,capture_output=True,env=os.environ)
    (OUT/(name+'.stdout')).write_text(p.stdout.decode('utf-8',errors='replace'),encoding='utf-8')
    (OUT/(name+'.stderr')).write_text(p.stderr.decode('utf-8',errors='replace'),encoding='utf-8')
    rec={'command':[str(a) for a in args],'exit_code':p.returncode,'started_utc':start,'ended_utc':now(),'wall_seconds':time.monotonic()-t}
    save(name+'.json',rec)
    print(name,p.returncode,flush=True)
    return p

def checks():
    run('check',['pwsh','-NoProfile','-File','scripts/check.ps1','-Task','IG-2B01'])
    run('workflow-validate',[sys.executable,'scripts/workflow.py','validate'])
    run('diff-check',['git','diff','--check'])
    run('root-inventory-validate',[sys.executable,'-B','-m','wgc.sources','validate',BASE/'final-verified/inventory.json'])

def reproduce():
    import pypdf, pdfplumber, PIL
    from pypdf import PdfReader,PdfWriter
    from pypdf.generic import RectangleObject
    from PIL import Image,ImageDraw
    inv=read(BASE/'final-verified/inventory.json'); ledger=read(BASE/'region-ledger-final.json')
    source=ROOT/inv['source']['pdf']['path']; assert sha(source)==inv['source']['sha256']
    reader=PdfReader(source,strict=True); assert len(reader.pages)==44
    toolchain={'python':sys.version,'executable':sys.executable,'python_sha256':sha(sys.executable),'libraries':{'pypdf':pypdf.__version__,'pdfplumber':pdfplumber.__version__,'Pillow':PIL.__version__},'native':{}}
    for exe in ['pdfinfo','pdftoppm']:
        path=BUNDLE/'native/poppler/Library/bin'/f'{exe}.exe'; p=run('version-'+exe,[path,'-v']); toolchain['native'][exe]={'path':str(path),'sha256':sha(path),'exit_code':p.returncode,'version':(p.stdout+p.stderr).decode()}
    save('toolchain.json',toolchain)
    run('pdfinfo',[BUNDLE/'native/poppler/Library/bin/pdfinfo.exe',source])
    # Full content access only physical pages 1-4.
    run('render-pages-1-4',[BUNDLE/'native/poppler/Library/bin/pdftoppm.exe','-f','1','-l','4','-r','144','-png',source,OUT/'page'])
    from pdfminer.high_level import extract_text
    (OUT/'pages-1-4-pdfminer.txt').write_text(extract_text(source,page_numbers=[0,1,2,3]),encoding='utf-8')
    pages={p['id']:p for p in inv['pages']}; regions={r['id']:r for r in inv['regions']}
    ledger_map={r['region_id']:r for r in ledger}
    counts={n:sum(r['denominator_role']=='inventory' and pages[r['page_id']]['pdf_page']==n for r in inv['regions']) for n in range(1,45)}
    assert [counts[n] for n in range(1,5)]==[26,31,38,35]
    assert len(ledger)==130 and len(inv['evidence'])==131
    assert all(s['status'] not in ['represented','excluded'] for r in inv['regions'] for s in r['coverage'].values())
    baseline_path=ROOT/'private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/inventory-one/inventory.json'
    baseline=read(baseline_path); baseline_regions={r['id']:r for r in baseline['regions']}
    assert all(p==baseline['pages'][p['pdf_page']-1] for p in inv['pages'] if p['pdf_page']>=5)
    assert all(r==baseline_regions[r['id']] for r in inv['regions'] if r['denominator_role']=='inventory' and pages[r['page_id']]['pdf_page']>=5)
    reg={ (r['kind'],r['key']):r for r in inv['registry']['entries'] }
    assert all(reg[(e['kind'],e['key'])]==e for e in baseline['registry']['entries'])
    assert len(set(inv['reading_order']))==len(inv['regions'])==len(inv['reading_order'])
    char_reports=[]
    with pdfplumber.open(source) as pdf:
        for n in range(1,5):
            p=pdf.pages[n-1]; rs=[r for r in inv['regions'] if pages[r['page_id']]['pdf_page']==n and r['denominator_role']=='inventory']
            boxes={r['id']:[r['box'][0]*612/1e6,r['box'][1]*792/1e6,r['box'][2]*612/1e6,r['box'][3]*792/1e6] for r in rs}
            uncovered=[]; clipped=[]; words=[]
            for c in p.chars:
                if not c['text'].strip(): continue
                cx=(c['x0']+c['x1'])/2; cy=(c['top']+c['bottom'])/2
                hits=[rid for rid,b in boxes.items() if b[0]<=cx<b[2] and b[1]<=cy<b[3]]
                if not hits: uncovered.append({k:c[k] for k in ['text','x0','x1','top','bottom']})
                elif not any(b[0]-0.001<=c['x0'] and c['x1']<=b[2]+0.001 and b[1]-0.001<=c['top'] and c['bottom']<=b[3]+0.001 for rid,b in boxes.items() if rid in hits): clipped.append({'char':{k:c[k] for k in ['text','x0','x1','top','bottom']},'region_ids':hits})
            for w in p.extract_words():
                cx=(w['x0']+w['x1'])/2; cy=(w['top']+w['bottom'])/2
                if not any(b[0]<=cx<b[2] and b[1]<=cy<b[3] for b in boxes.values()): words.append(w)
            char_reports.append({'page':n,'nonspace_chars':sum(bool(c['text'].strip()) for c in p.chars),'uncovered_chars':uncovered,'bbox_clipped_chars':clipped,'uncovered_words':words})
            (OUT/f'page-{n:02}-pdfplumber.txt').write_text(p.extract_text(layout=False) or '',encoding='utf-8')
            image=Image.open(OUT/f'page-{n:02}.png').convert('RGB'); draw=ImageDraw.Draw(image)
            for i,r in enumerate(rs):
                b=boxes[r['id']]; xy=tuple(round(v*2) for v in b); draw.rectangle(xy,outline='red',width=1); draw.text((xy[0],xy[1]),str(ledger_map[r['id']]['reading_order_index']),fill='blue')
            image.save(OUT/f'overlay-{n:02}.png')
    save('character-word-audit.json',char_reports)
    print('CHAR AUDIT',[(r['page'],len(r['uncovered_chars']),len(r['bbox_clipped_chars']),len(r['uncovered_words'])) for r in char_reports],flush=True)
    # Recreate each exact region from source independently of executor scripts.
    crop_results=[]
    crop_root=OUT/'reproduced'; crop_root.mkdir(exist_ok=False)
    for e in inv['evidence']:
        n=e['pdf_page']; r=regions[e['region_id']]; p=pages[r['page_id']]
        if n>4: assert n==5 and r['denominator_role']=='context' and r['key']=='ig2b01:context:triarii-tail' and r['box']==[71895,63131,495099,98485]
        assert n<=5
        box=r['box']; native=[box[0]*612/1e6,792-box[3]*792/1e6,box[2]*612/1e6,792-box[1]*792/1e6]
        writer=PdfWriter(); cropped=writer.add_page(reader.pages[n-1]); cropped.mediabox=RectangleObject(native); cropped.cropbox=RectangleObject(native)
        stem=crop_root/f'{n:02}-{e["region_id"].split(":")[1]}'; crop=stem.with_suffix('.pdf')
        with crop.open('xb') as f: writer.write(f)
        with pdfplumber.open(crop) as pdf:
            text=pdf.pages[0].crop(pdf.pages[0].bbox).extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
        stem.with_suffix('.txt').write_text(text,encoding='utf-8',newline='\n')
        args=[str(BUNDLE/'native/poppler/Library/bin/pdftoppm.exe'),'-f','1','-l','1','-singlefile','-cropbox','-r',str(e['render_parameters']['dpi']),'-png',str(crop),str(stem)]
        t=time.monotonic(); started=now(); result=subprocess.run(args,capture_output=True)
        assert result.returncode==0,result.stderr
        original_text=(ROOT/e['text']['path']).read_text(encoding='utf-8')
        original_image=Image.open(ROOT/e['image']['path']); new_image=Image.open(stem.with_suffix('.png'))
        expected_size=(math.ceil((native[2]-native[0])*2),math.ceil((native[3]-native[1])*2))
        row={'region_id':r['id'],'key':r['key'],'pdf_page':n,'box':box,'native_bounds':native,'text_equal':text==original_text,'png_bytes_equal':sha(stem.with_suffix('.png'))==e['image']['sha256'],'pixels_equal':original_image.mode==new_image.mode and original_image.tobytes()==new_image.tobytes(),'size':list(new_image.size),'expected_size':list(expected_size),'offsets_equal':e['text_offsets']=={'unit':'unicode_codepoints','bounds':'half_open','start':0,'end':len(original_text)},'codepoints_equal':e['text_codepoints']==len(original_text),'command':args,'exit_code':result.returncode,'started_utc':started,'ended_utc':now(),'wall_seconds':time.monotonic()-t}
        assert new_image.size==expected_size
        assert row['text_equal'] and row['pixels_equal'] and row['offsets_equal'] and row['codepoints_equal'],row
        if n<=4:
            l=ledger_map[r['id']]; assert l['box']==box and l['region_revision']==r['revision'] and l['coverage']==r['coverage'] and l['evidence']==e and l['reading_order_index']==inv['reading_order'].index(r['id'])
        crop_results.append(row)
    save('crop-reproduction.json',crop_results)
    save('structural-independent.json',{'page_count':len(reader.pages),'counts':counts,'task_denominator':sum(counts[n] for n in range(1,5)),'inventory_denominator':sum(counts.values()),'context_regions':sum(r['denominator_role']=='context' for r in inv['regions']),'all_40_placeholders_exactly_unchanged':True,'all_40_pages_exactly_unchanged':True,'baseline_registry_entries_preserved':True,'reading_order_complete':True,'all_131_crop_text_and_pixels_reproduced':True,'all_130_ledger_bindings_exact':True,'no_represented_or_excluded':True,'source_unchanged':sha(source)==inv['source']['sha256']})
    print('REPRODUCTION COMPLETE',len(crop_results),flush=True)

def secondary():
    from fractions import Fraction
    import uuid
    from wgc.sources.inventory import assign,assemble
    inv=read(BASE/'final-verified/inventory.json'); ledger=read(BASE/'region-ledger-final.json')
    canonical=lambda x: json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    revision=lambda x: hashlib.sha256(canonical({k:v for k,v in x.items() if k!='revision'})).hexdigest()
    records=[inv,*inv['pages'],*inv['regions']]
    assert all(revision(r)==r['revision'] for r in records)
    for r in inv['registry']['entries']: uuid.UUID(r['id'].split(':')[1])
    reg=copy.deepcopy(inv['registry'])
    ids=[assign(reg,e['kind'],e['key']) for e in reversed(inv['registry']['entries'])]
    assert reg==inv['registry'] and ids==[e['id'] for e in reversed(inv['registry']['entries'])]
    reconstructed=assemble(inv['source'],inv['pages'],inv['regions'],reg,reading_order=inv['reading_order'],links=inv['links'],evidence=inv['evidence'],toolchain=inv['toolchain'])
    assert canonical(reconstructed)==canonical(inv)
    (OUT/'replayed-inventory.json').write_bytes(canonical(reconstructed)+b'\n')
    gap_report=read(BASE/'geometric-gaps.json'); gap_results=[]
    for n in range(1,5):
        rs=[r for r in ledger if r['page']==n]; boxes=[r['box'] for r in rs]
        for j,a in enumerate(boxes):
            assert all(not (max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])) for b in boxes[j+1:])
        complement=next(g for g in gap_report if g['pdf_page']==n)
        rects=complement['complement_rectangles']; area=lambda b:(b[2]-b[0])*(b[3]-b[1])
        assert sum(area(b) for b in boxes)+sum(area(b) for b in rects)==10**12
        assert sum(area(b) for b in rects)==complement['unaccounted_area_trillionths']
        for j,a in enumerate(rects):
            assert all(not (max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])) for b in boxes+rects[j+1:])
        for r in rs:
            b=r['box']; rational=[Fraction(612*b[0],10**6),Fraction(792*(10**6-b[3]),10**6),Fraction(612*b[2],10**6),Fraction(792*(10**6-b[1]),10**6)]
            assert r['exact_native_bottom_left_bounds_rational']==[{'numerator':v.numerator,'denominator':v.denominator} for v in rational]
        gap_results.append({'page':n,'complement_rectangles':len(rects),'gap_area_trillionths':sum(area(b) for b in rects),'disjoint_complete_partition':True})
    uncertainty=read(BASE/'uncertainty.json'); um={u['region_id']:u for u in uncertainty}; gaps=read(BASE/'gaps.json'); gm={g['region_id']:g for g in gaps['regions']}; uresults=[]
    for e in inv['evidence']:
        text=(ROOT/e['text']['path']).read_text(encoding='utf-8'); u=um[e['region_id']]
        assert u['evidence_id']==e['id'] and u['text_pin']==e['text'] and u['replacement_character_count']==text.count('\ufffd') and u['empty_extraction']==(text=='')
        assert u['known_replacement_offsets']==[i for i,c in enumerate(text) if c=='\ufffd']
        uresults.append({'region_id':e['region_id'],'empty_text':text=='','replacement_count':text.count('\ufffd'),'uncertainty_bound_to_final_evidence':True})
    for r in ledger:
        g=gm[r['region_id']]; assert g['region_revision']==r['region_revision'] and g['levels']==r['coverage']
    assert read(BASE/'continuations.json')['links']==inv['links']
    baseline=read(ROOT/'private/workflow/runs/IG-2A/repair-20261014T093001Z-01a139bc-256f-7da0-b4a7-8940ca16fc81/inventory-one/inventory.json')
    stripped=copy.deepcopy(inv); stripped['evidence']=[]
    for p in stripped['pages']: p.update(copy.deepcopy(baseline['pages'][p['pdf_page']-1]))
    stripped['revision']=revision(stripped)
    replay=read(BASE/'final-verified/replay-without-evidence.json')
    assert canonical(stripped)==canonical(replay)
    save('secondary-independent.json',{'all_216_enclosing_revisions_recomputed':len(records),'registry_reverse_lookup_replay_identical':True,'assembled_inventory_exact_canonical_replay':True,'executor_author_replay_verified_independently':True,'geometric_partitions':gap_results,'all_130_rational_bbox_values_exact':True,'all_131_uncertainty_records_current':True,'all_130_gap_records_current':True,'all_15_links_equal_report_and_inventory':True,'uncertainty_records':uresults})
    print('SECONDARY COMPLETE',len(records),flush=True)

if __name__=='__main__':
    if sys.argv[1]=='checks': checks()
    elif sys.argv[1]=='reproduce': reproduce()
    elif sys.argv[1]=='validate-corrected': run('root-inventory-validate-corrected',[sys.executable,'-B','-m','wgc.sources','validate',(BASE/'final-verified/inventory.json').relative_to(ROOT).as_posix()])
    elif sys.argv[1]=='secondary': secondary()
