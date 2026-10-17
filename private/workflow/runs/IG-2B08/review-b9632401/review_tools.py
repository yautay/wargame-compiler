"""Independent, bounded reviewer checks. No writes to the frozen delivery."""
import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pdfplumber
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.relative_to(Path.cwd())
SESSION = Path('private/workflow/orchestrator/20261017T071640Z-9e122b0d/002-IG-2B08-reviewer-b9632401')
DELIVERY = Path('private/workflow/runs/IG-2B08/inventory-p33-scope02')
CONTRACT = Path('private/workflow/runs/IG-2B08/context-recovery-20261017-p33-01/input-pins.json')


def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pin(p):
    p = Path(p)
    return dict(path=p.as_posix(), bytes=p.stat().st_size, sha256=sha(p))


def meta():
    return dict(role='reviewer', actor='ig2:002-IG-2B08-reviewer-b9632401:reviewer',
                model='gpt-6.1-sol', reasoning='high',
                configuration_evidence=(SESSION/'runtime-configuration.json').as_posix(),
                configuration_sha256=sha(SESSION/'runtime-configuration.json'))


def write(name, data):
    p=ROOT/name
    assert not p.exists(), p
    p.write_text(json.dumps({**meta(), **data}, indent=2)+'\n', encoding='utf-8')


def pins_in(obj):
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj:
            yield obj
        for val in obj.values():
            yield from pins_in(val)
    elif isinstance(obj, list):
        for val in obj:
            yield from pins_in(val)


def verify_pin(item):
    assert sha(item['path']) == item['sha256'], item['path']
    if 'bytes' in item:
        assert Path(item['path']).stat().st_size == item['bytes'], item['path']


def preflight():
    delivery=load(DELIVERY/'delivery.json')
    for item in delivery['artifacts']:
        verify_pin(item)
    scope=load(load(SESSION/'task.json')['context_recovery_authorization']['scope']['path'])
    verify_pin(scope['preserve_manifest'])
    old=list(pins_in(load(scope['preserve_manifest']['path'])))
    for item in old:
        verify_pin(item)
    contract=load(CONTRACT)
    # Validate exact input pins internally; do not emit unassigned source records.
    for item in pins_in(contract):
        verify_pin(item)
    write('checkpoint.json', dict(task='IG-2B08', started_utc=datetime.now(timezone.utc).isoformat(),
          input_packet=pin(SESSION/'packet.json'), delivery=pin(DELIVERY/'delivery.json'),
          frozen_artifact_count=len(delivery['artifacts']), preserved_old_artifact_count=len(old),
          completed_criteria=[], blocker=None, next_operation='Fresh bounded original renders and full ledger inspection.'))


def originals():
    contract=load(CONTRACT)
    pdf=contract['source']['pdf']['path']
    out=ROOT/'originals'
    out.mkdir(exist_ok=False)
    observations=load(DELIVERY/'region-ledger.json')['new_observations']
    comparisons=[]
    with pdfplumber.open(pdf) as original:
        for page in (29,30,31,32,33):
            prefix=out/f'page-{page}'
            cmd=['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','144']
            if page==33:
                cmd+=['-x','90','-y','100','-W','522','-H','60']
                clipped=original.pages[page-1].crop((45,50,306,80),strict=True)
            else:
                clipped=original.pages[page-1]
            subprocess.run(cmd+['-png',pdf,str(prefix)],check=True,capture_output=True)
            text=clipped.extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
            prefix.with_suffix('.txt').write_text(text,encoding='utf-8')
            comparisons.append(dict(page=page, fresh_image=pin(prefix.with_suffix('.png')),
                fresh_text=pin(prefix.with_suffix('.txt')),
                frozen_image_equal=sha(prefix.with_suffix('.png'))==sha(DELIVERY/'originals'/f'page-{page}.png')))
            if page==33:
                assert Image.open(prefix.with_suffix('.png')).size==(522,60)
                continue
            rows=[o for o in observations if o['page']==page]
            im=Image.open(prefix.with_suffix('.png')).convert('RGB')
            draw=ImageDraw.Draw(im)
            for idx,o in enumerate(rows):
                box=tuple(round(v*2) for v in o['points'])
                draw.rectangle(box,outline='red' if o['role']=='inventory' else 'blue',width=1)
                draw.text((box[0]+1,box[1]+1),str(idx+1),fill='red')
            im.save(out/f'page-{page}-boundaries.png')
            # Every region and detail shown from freshly rendered original pixels.
            for start in range(0,len(rows),12):
                sheet=Image.new('RGB',(1500,1200),'white')
                d=ImageDraw.Draw(sheet)
                for index,o in enumerate(rows[start:start+12]):
                    source=Image.open(prefix.with_suffix('.png')).convert('RGB')
                    crop=source.crop(tuple(round(v*2) for v in o['points']))
                    crop.thumbnail((490,255))
                    x=(index%3)*500; y=(index//3)*300
                    sheet.paste(crop,(x,y+42))
                    label=f'{start+index+1}: '+o['key'].split(':',2)[2]
                    d.text((x+2,y+2),label,fill='black')
                    d.text((x+2,y+18),o['kind']+' / '+o['role'],fill='black')
                sheet.save(out/f'page-{page}-sheet-{start//12+1}.png')
    write('original-generation.json',dict(summary='Fresh serial original renders; native page-33 output clipped before pixels, original page clipped before text.',
        source=contract['source']['pdf'], comparisons=comparisons, source_scope=[29,30,31,32],
        page33_box=[45,50,306,80], page28_access='Reference-only prepared projection; no render or extraction.'))


def audit():
    from collections import Counter
    from wgc.sources.inventory import validate, digest, page_basis_hash, coverage
    from wgc.sources.geometry import overlaps

    task=load(SESSION/'task.json')
    contract=load(CONTRACT)
    base=load(contract['baseline_inventory']['path'])
    baseline_registry=load(contract['identity_registry']['path'])
    assert base['registry']==baseline_registry
    docs=[load(DELIVERY/name/'inventory.json') for name in ('final-verified','replay-1','replay-2')]
    retired=set(task['inventory_contract']['placeholder_target_ids'])
    old={r['id']:r for r in base['regions']}
    expected_new={o['region_id'] for o in load(DELIVERY/'region-ledger.json')['new_observations']}
    ledger=load(DELIVERY/'region-ledger.json')
    delivery=load(DELIVERY/'delivery.json')
    delivery_index={p['path']:p for p in delivery['artifacts']}
    assert len(delivery_index)==len(delivery['artifacts'])
    source_pins=load(DELIVERY/'source-pins.json')
    indexed={p['path']:p for p in source_pins['artifacts']}
    assert len(indexed)==len(source_pins['artifacts'])
    for p in source_pins['artifacts']+source_pins['current_reports']:
        verify_pin(p)
        assert delivery_index[p['path']]==p
    checks=[]
    for name,doc in zip(('final-verified','replay-1','replay-2'),docs):
        # validate with actual root: structural PDF checks never emit page content.
        result=validate(doc,Path.cwd())
        now={r['id']:r for r in doc['regions']}
        assert set(old)-set(now)==retired
        assert set(now)-set(old)==expected_new
        for identity,region in old.items():
            if identity not in retired:
                assert now[identity]==region
        assert doc['source']==base['source']
        assert doc['pages']==base['pages']
        assert {p['pdf_page'] for p in doc['pages']}==set(range(1,45))
        assert doc['links'][:len(base['links'])]==base['links']
        assert doc['evidence'][:len(base['evidence'])]==base['evidence']
        old_order=[x for x in base['reading_order'] if x not in retired]
        assert [x for x in doc['reading_order'] if x in set(old_order)]==old_order
        assert all(entry in doc['registry']['entries'] for entry in baseline_registry['entries'])
        assert doc['registry']==load(DELIVERY/name/'identity-registry.json')
        assigned=[r for r in doc['regions'] if r['id'] in expected_new]
        pages={p['id']:p for p in doc['pages']}
        evs={e['region_id']:e for e in doc['evidence']}
        for r in assigned:
            e=evs[r['id']]
            assert e['page_basis_hash']==page_basis_hash(pages[r['page_id']])
            assert e['region_revision']==r['revision']
            assert e['box']==r['box'] and e['source_sha256']==doc['source']['sha256']
            assert pages[r['page_id']]['pdf_page'] in (29,30,31,32,33)
            for field in ('crop_pdf','text','image'):
                assert indexed.get(e[field]['path'])==e[field]
                assert delivery_index.get(e[field]['path'])==e[field]
        for p in pins_in(doc):
            verify_pin(p)
            assert indexed.get(p['path'])==p
            assert delivery_index.get(p['path'])==p
        checks.append(dict(name=name,inventory=pin(DELIVERY/name/'inventory.json'),
            new_regions=len(assigned), root_source_validation=True,
            preserved_regions=len(old)-len(retired), preserved_links=len(base['links']),
            preserved_evidence=len(base['evidence']), retained_registry_entries=len(baseline_registry['entries'])))
    final=docs[0]
    for replay in docs[1:]:
        for field in ('source','pages','regions','registry','reading_order','links','toolchain'):
            assert replay[field]==final[field]
        def normalized(doc):
            rows=copy.deepcopy(doc['evidence'])
            for e in rows:
                if e['region_id'] in expected_new:
                    for key in ('crop_pdf','text','image'):
                        e[key]['path']=e[key]['path'].split('/evidence/',1)[1]
            return rows
        assert normalized(final)==normalized(replay)
    page_map={p['id']:p['pdf_page'] for p in final['pages']}
    ledger_fields=('id','key','revision','box','kind','denominator_role','coverage')
    assert len(ledger['regions'])==len(final['regions'])
    for row,region in zip(ledger['regions'],final['regions']):
        assert all(row[f]==region[f] for f in ledger_fields)
        assert row['pdf_page']==page_map[region['page_id']]
    assert ledger['reading_order']==final['reading_order'] and ledger['links']==final['links']
    components=load(DELIVERY/'component-ledger.json')['components']
    expected_components={o['region_id'] for o in ledger['new_observations'] if o['kind'] in ('diagram','table','legend','example')}
    assert {o['region_id'] for o in components}==expected_components
    originals=load(DELIVERY/'original-page-inspection.json')
    for p in originals['original_artifacts']:
        assert indexed.get(p['path'])==p and delivery_index.get(p['path'])==p
    cov=load(DELIVERY/'coverage-report.json')
    fresh_cov=coverage(final)
    for field in fresh_cov:
        assert fresh_cov[field]==cov[field],field
    assigned=[r for r in final['regions'] if r['id'] in expected_new and r['denominator_role']=='inventory']
    assert cov['assigned_four_page']['denominator_regions']==len(assigned)==183
    assert cov['inherited_nonassigned']['denominator_regions']==845
    assert cov['denominator_regions']==1028
    assert cov['context_only']['denominator_contribution']==0
    for lvl in ('transcription','descriptive_semantics','formal_semantics'):
        assert dict(Counter(r['coverage'][lvl]['status'] for r in assigned))==cov['assigned_four_page']['levels'][lvl]
    for p in delivery['artifacts']:
        verify_pin(p)
    write('independent-audit.json',dict(summary='Independent entire-delivery hash, 44-page preservation, complete ledger, freshness and source-index checks; both separately frozen full replays compared.',
          checks=checks, frozen_artifact_count=len(delivery['artifacts']), source_index_count=len(indexed),
          ledger_region_count=len(ledger['regions']), new_region_count=len(expected_new), component_count=len(components),
          full_denominator=1028, assigned_denominator=183, inherited_denominator=845, context_contribution=0,
          normalized_replays_equal=True, exit_code=0))
    print(json.dumps(dict(verified=True,artifacts=len(delivery['artifacts']),regions=len(expected_new),components=len(components))))


def cli_validation():
    commands=[]
    for name in ('final-verified','replay-1','replay-2'):
        cmd=['.venv/Scripts/python.exe','-m','wgc.sources','validate',(DELIVERY/name/'inventory.json').as_posix()]
        started=datetime.now(timezone.utc)
        log=ROOT/f'{name}-cli-validation-posix.log'
        with log.open('xb') as stream:
            result=subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT)
        commands.append(dict(command=' '.join(cmd), exit_code=result.returncode,
            started_utc=started.isoformat(), ended_utc=datetime.now(timezone.utc).isoformat(),log=pin(log),root_source_access=True))
        print(name,result.returncode,flush=True)
    write('cli-validation-posix.json',dict(summary='Independent unchanged final and both replay CLI validation commands with actual repository/source access; corrected reviewer wrapper path separators after CLI rejected backslashes.',checks=commands))
    assert all(c['exit_code']==0 for c in commands)


def component_probe():
    observations=load(DELIVERY/'region-ledger.json')['new_observations']
    rows=[o for o in observations if o['key'].startswith('ig2b08:p30:advance-component-')]
    original=Image.open(ROOT/'originals/page-30.png').convert('RGB')
    missed=[]
    for y in range(730,756):
        for x in range(184,208):
            red,green,blue=original.getpixel((x,y))
            if blue>180 and green>140 and red<100:
                if not any(o['points'][0]<=x/2<o['points'][2] and
                           o['points'][1]<=y/2<o['points'][3] for o in rows):
                    missed.append([x,y])
    target=next(o for o in rows if o['key']=='ig2b08:p30:advance-component-arrows')
    sample=[94,367]
    assert original.getpixel((188,734))==(42,197,244)
    assert len(missed)==77
    primary=[o for o in observations if o['key'].startswith('ig2b08:p30:advance-tile-')]
    assert any(o['points'][0]<=94<o['points'][2] and o['points'][1]<=367<o['points'][3] for o in primary)
    per_run=[]
    for name in ('final-verified','replay-1','replay-2'):
        doc=load(DELIVERY/name/'inventory.json')
        r=next(r for r in doc['regions'] if r['key']==target['key'])
        e=next(e for e in doc['evidence'] if e['region_id']==r['id'])
        per_run.append(dict(name=name,region_id=r['id'],revision=r['revision'],box=r['box'],image=e['image']))
    write('component-boundary-probe.json',dict(summary='F01: left cyan arrowhead lies outside every Advance detail component crop; primary field tiles retain the source pixels.',
        physical_page=30, source=load(CONTRACT)['source']['pdf'],
        current_arrow_key=target['key'], current_arrow_points=target['points'],
        sample_original_pixel_144dpi=[188,734],sample_rgb=[42,197,244],sample_pdf_points=sample,
        subwindow_pdf_points=[92,365,104,378],cyan_pixels_outside_all_advance_detail_crops=77,
        component_keys_checked=[o['key'] for o in rows],frozen_runs=per_run,
        fresh_original=pin(ROOT/'originals/page-30.png'),
        annotated_panel=pin(ROOT/'page30-advance-arrow-boundary.png'),
        fresh_component_sheet=pin(ROOT/'originals/page-30-sheet-5.png'),
        primary_inventory_tiles_retain_sample=True, complete_component_boundary=False,exit_code=1))
    print('F01 reproduced: 77 cyan arrowhead pixels in the selected source window are outside all Advance detail component crops; primary tiles retain them.')
    return 1


def finalize():
    task=load(SESSION/'task.json')
    delivery=load(DELIVERY/'delivery.json')
    observations=load(DELIVERY/'region-ledger.json')['new_observations']
    all_ids=[o['region_id'] for o in observations]
    component_ids=[o['region_id'] for o in load(DELIVERY/'component-ledger.json')['components']]
    details={29:[4,5,8,9,10],30:[3,4,5,6]}
    page_notes={
        29:'Compared all 120 proposed rectangles against the original and overlay: two combat snapshots, A-D/T-Z locators, counters, hit/routed markers, origin/destination layers and arrows; incoming example, five example paragraphs, heading, two design notes and clause. Editorial header/footer retained. Detail sheets disambiguate overlapping layers.',
        30:'Compared all 67 proposed rectangles: four panel fields and captions, markers/counters/origins/arrows, clauses and bullets, history/play notes and both continuation boundaries. F01: Advance left cyan arrowhead is absent from all seven detail component crops, although retained by primary field tiles.',
        31:'Compared all 42 proposed rectangles: incoming pursuit paragraph, wrapped 8.63 plus Pursuit/Finished marker, Zama example and notes, pursuit rating key/value cells and modifier rows, five chart descriptions, two section headings, elephant history, elephant counter and wrapped Pass-Thru introduction, restrictions and procedure steps. Actual charts are not claimed present on this page.',
        32:'Compared all 39 proposed rectangles: continuation steps, notes, clause paragraphs and bullets; all eight split-table header/key/result cells; two elephant example field tiles, two counter/hex details and six compass labels; caption and exit paragraph. Fresh exact page-33 crop contains only the two complete continuation lines.'}
    write('visual-review.json',dict(summary='Independent full assigned original-page, boundary/component and complete-ledger comparison against frozen hashes; physical/descriptive review only.',
        source=load(CONTRACT)['source']['pdf'], original_generation=pin(ROOT/'original-generation.json'),
        frozen_region_ledger=pin(DELIVERY/'region-ledger.json'), frozen_component_ledger=pin(DELIVERY/'component-ledger.json'),
        pages=[dict(physical_page=p,reviewed_new_ids=[o['region_id'] for o in observations if o['page']==p],
                    fresh_original=pin(ROOT/'originals'/f'page-{p}.png'),
                    fresh_boundary_overlay=pin(ROOT/'originals'/f'page-{p}-boundaries.png'),observation=page_notes[p]) for p in (29,30,31,32)],
        reviewed_new_region_ids=all_ids,reviewed_component_ids=component_ids,
        inspected_detail_sheets=[pin(ROOT/'originals'/f'page-{p}-sheet-{i}.png') for p,indices in details.items() for i in indices],
        incoming_boundary=dict(physical_page=28,mode='Prepared direct dependency boundary projection only; retained reference compared with newly inspected page 29.'),
        exit_boundary=dict(physical_page=33,box_points=[45,50,306,80],image=pin(ROOT/'originals/page-33.png'),
                           observation='Exactly two complete lines; no following note, heading or right column. Context contribution zero.'),
        complete_ledger_audit=pin(ROOT/'independent-audit.json'),finding_evidence=pin(ROOT/'component-boundary-probe.json'),
        semantic_acceptance_granted=False,gameplay_readiness=False))
    scope=load(task['context_recovery_authorization']['scope']['path'])
    preserved=list(pins_in(load(scope['preserve_manifest']['path'])))
    for p in preserved:
        verify_pin(p)
    for p in delivery['artifacts']:
        verify_pin(p)
    assert delivery['criteria']==task['acceptance']
    runtime=load(SESSION/'runtime-configuration.json')
    assert (runtime['status'],runtime['model'],runtime['reasoning'])==('confirmed','gpt-6.1-sol','high')
    write('final-integrity.json',dict(summary='All frozen delivery and preserved blocked-attempt bytes reverified after reviewer checks; no implementation, queue, source or old-attempt writes.',
        delivery=pin(DELIVERY/'delivery.json'),frozen_artifact_count=len(delivery['artifacts']),
        preserved_old_artifact_count=len(preserved),mismatches=[],configuration=pin(SESSION/'runtime-configuration.json'),exit_code=0))
    checks=[
        dict(command=f'.venv/Scripts/python.exe {ROOT.as_posix()}/review_tools.py preflight',exit_code=0,evidence=pin(ROOT/'checkpoint.json')),
        dict(command=f'.venv/Scripts/python.exe {ROOT.as_posix()}/review_tools.py originals',exit_code=0,evidence=pin(ROOT/'original-generation.json')),
        dict(command=f'.venv/Scripts/python.exe {ROOT.as_posix()}/review_tools.py audit',exit_code=0,evidence=pin(ROOT/'independent-audit.json')),
        *load(ROOT/'cli-validation-posix.json')['checks'],
        dict(command=f'.venv/Scripts/python.exe -m pytest tests/sources -q --basetemp {ROOT.as_posix()}/source-pytest -p no:cacheprovider --tb=short',
             exit_code=0,tests_passed=71,execution='Approved exact unchanged suite after observed restricted-token pytest temporary-directory denial; fresh reviewer basetemp preserves frozen delivery.',log=pin(ROOT/'source-suite-approved.log')),
        dict(command='pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08',exit_code=0,tests_passed=288,
             execution='Approved exact unchanged check after recorded restricted-token WinError 5 accessing pytest basetemp.',log=pin(ROOT/'full-check-approved.log')),
        dict(command='git diff --check',exit_code=0,log=pin(ROOT/'diff-check.log')),
        dict(command=f'.venv/Scripts/python.exe {ROOT.as_posix()}/review_tools.py component-probe',exit_code=1,
             result='F01 reproduced; complete-component boundary check fails.',evidence=pin(ROOT/'component-boundary-probe.json')),
        dict(command='Independent entire assigned original-page/region/component/complete-ledger visual review',exit_code=1,
             result='F01 prevents technical pass.',evidence=pin(ROOT/'visual-review.json')),
        dict(command='Final exhaustive frozen-delivery and old-attempt hash verification',exit_code=0,evidence=pin(ROOT/'final-integrity.json'))]
    finding=dict(id='F01',severity='medium',title='Page-30 Advance component evidence clips the left cyan arrowhead',
        locations=[dict(path=(DELIVERY/'component-ledger.json').as_posix(),pointer='/components/149/points'),
                   dict(path=(DELIVERY/'region-ledger.json').as_posix(),pointer='/new_observations/229/points'),
                   dict(path=(DELIVERY/'original-page-inspection.json').as_posix(),pointer='/observations/229/points')],
        region_key='ig2b08:p30:advance-component-arrows',region_id='region:798e9f78-b8b9-45d5-a546-fb914abe4f9c',
        region_revision='50be08a1fc9d97a3be7d28ffe938676af499d4450bbb9bb6f1b71755e6c1bcdd',
        description='The Advance panel has two cyan curved arrows. The arrows detail uses [104,345,141,476] points, cutting off the head and upper curve of the left arrow. Fresh original pixel [188,734] at 144 DPI is cyan [42,197,244] (PDF point [94,367]); it lies outside every one of the seven Advance detail-component boxes. A bounded 12x13-point source window contains 77 such cyan pixels. The same incomplete boundary is frozen in final-verified and both replays. Primary field tiles retain these pixels, so this is incomplete component accounting/evidence, not lost whole-page pixels or denominator inflation.',
        consequence='The complete-component/fresh exact evidence and complete-replay claims are stronger than the authored component set. The verifier compares keys to SPECS and cannot catch this truncated source component.',
        affected_criteria=[task['acceptance'][i] for i in (0,5,6,8)],
        evidence=[pin(ROOT/'component-boundary-probe.json'),pin(ROOT/'page30-advance-arrow-boundary.png'),pin(ROOT/'originals/page-30-sheet-5.png')],
        required_repair='In a fresh authorized repair attempt, correct or split the zero-denominator Advance arrow detail selections so both cyan curves, their arrowheads and the black forward arrow are fully accounted for with exact component locators. Preserve the disjoint primary field tiles and all accepted baseline objects/registry history. Regenerate affected evidence and reports, complete final/replay sets and exhaustive source/delivery indexes at fresh paths; keep this frozen delivery and blocked attempt immutable.',
        repair_validation=['Compare the complete left cyan arrow against the original page and corrected final/replay detail evidence; the intended arrow component must contain source point [94,367] and its full visible curve/head, not merely a field tile or neighboring counter crop.',
            'Add a source-bound component-completeness check that rejects the current truncated selection; key-set equality alone is insufficient.',
            'Recheck all assigned components and both complete separately generated serial replays, stable identities, evidence freshness and exhaustive current indexes; preserve 44-page baseline objects, retained order and zero context contribution.',
            'Rerun the unchanged source suite, final and both replay CLI validation, owned batch verifier, scripts/check.ps1 -Task IG-2B08 and git diff --check using authorized execution where required.'])
    unmet={0,5,6,8}
    reasons={0:'Component-level accounting incomplete for the left cyan arrowhead; primary tiles retain it.',
        5:'The arrow detail omits part of a visible component; broad field tiling does not supply its exact component evidence.',
        6:'The declared complete region/component index has no complete locator for this arrowhead.',
        8:'Both replays reproduce the same incomplete source component selection, despite matching authored sets.'}
    now=datetime.now(timezone.utc)
    started=datetime.fromisoformat(load(ROOT/'checkpoint.json')['started_utc'])
    files=[ROOT/'review_tools.py',ROOT/'checkpoint.json',ROOT/'original-generation.json',ROOT/'independent-audit.json',
        ROOT/'cli-validation.json',ROOT/'cli-validation-posix.json',ROOT/'component-boundary-probe.json',ROOT/'visual-review.json',
        ROOT/'final-integrity.json',ROOT/'page30-advance-arrow-boundary.png',ROOT/'source-suite-approved.log',
        ROOT/'full-check-restricted.log',ROOT/'full-check-approved.log',ROOT/'diff-check.log']
    for name in ('final-verified','replay-1','replay-2'):
        files += [ROOT/f'{name}-cli-validation.log',ROOT/f'{name}-cli-validation-posix.log']
    for p in (29,30,31,32,33):
        files += [ROOT/'originals'/f'page-{p}.png',ROOT/'originals'/f'page-{p}.txt']
        if p!=33:
            files += [ROOT/'originals'/f'page-{p}-boundaries.png']
            count=sum(o['page']==p for o in observations)
            files += [ROOT/'originals'/f'page-{p}-sheet-{i+1}.png' for i in range((count+11)//12)]
    write('review.json',dict(task='IG-2B08',outcome='changes_requested',
        summary='Changes requested for F01: the page-30 Advance arrow detail clips the left cyan arrowhead in final and both replays. All frozen hashes, 44-page preservation, normalized replay/ledger/index checks and required suites pass. No semantic acceptance or gameplay readiness granted.',
        criteria=task['acceptance'],artifacts=delivery['artifacts'],checks=checks,
        delivery_reference=pin(DELIVERY/'delivery.json'),input_packet=pin(SESSION/'packet.json'),
        criteria_assessment=[dict(criterion=c,status='unmet' if i in unmet else 'met',finding_ids=['F01'] if i in unmet else [],
            assessment=reasons.get(i,'Verified by fresh original/complete-ledger review, independent entire-artifact/preservation/index/replay audit and unchanged named checks within physical inventory scope.')) for i,c in enumerate(task['acceptance'])],
        findings=[finding],review_artifacts=[pin(p) for p in files],
        validation_history=[dict(command='pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08',exit_code=1,
            reason='Windows restricted-token WinError 5 accessing pytest mode-0700 basetemp; approved unchanged execution subsequently passed.',log=pin(ROOT/'full-check-restricted.log')),
            dict(command=f'.venv/Scripts/python.exe {ROOT.as_posix()}/review_tools.py cli-validation',exit_code=1,
            reason='Reviewer wrapper supplied Windows backslashes; CLI rejected paths before source access. Corrected wrapper to POSIX private/ operands; all three unchanged validations subsequently passed.',evidence=pin(ROOT/'cli-validation.json'))],
        measurement=dict(started_utc=started.isoformat(),ended_utc=now.isoformat(),elapsed_wall_seconds=(now-started).total_seconds(),
            operator_seconds=None,input_tokens=None,output_tokens=None,unknown_reason='Token counts and operator time were not exposed.',
            requested_model='gpt-6.1-sol',requested_reasoning='high',observed_model='gpt-6.1-sol',observed_reasoning='high'),
        defect_counts=dict(medium=1),human_semantic_acceptance_granted=False,semantic_acceptance_granted=False,
        executable_readiness='unverified',queue_mutated=False,implementation_mutated=False,
        next_operation='Coordinator prepares one bounded F01 repair and fresh supervisor-launched executor session; this reviewer role stops.'))
    print(json.dumps(dict(outcome='changes_requested',evidence=(ROOT/'review.json').as_posix(),findings=1,artifacts=len(delivery['artifacts']))))


if __name__=='__main__':
    import sys
    sys.exit({'preflight':preflight,'originals':originals,'audit':audit,
              'cli-validation':cli_validation,'component-probe':component_probe,'finalize':finalize}[sys.argv[1]]() or 0)
