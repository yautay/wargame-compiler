import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from verify import ROOT, OLD, NEW, SESSION, read, pin, write, verify, common

ledger = read(NEW/'region-ledger.json')
components = read(OLD/'component-ledger.json')
coverage = read(OLD/'coverage-report.json')
pages = []
descriptions = {
    9: 'Both columns read: 4.34-4.35, design note, 4.4 heading/counter/introduction and six separate list items, historical note, 4.5 introduction, 4.51-4.56 opening, exception and play note. Both explicit Line Command Eligibility Chart citations are indexed. Header, label, separator, copyright and blank page area inspected.',
    10: 'Both columns read: 4.56 continuation and two bullets; 4.6 body, exception and historical digression; 4.7 and 4.71-4.75 with design note; 4.8 introduction and 4.81-4.84 with design note. Leader Casualty Table and all visible numeric citations are retained. Other Leader Casualty occurrences describe an operation rather than citing a named source; humor rule is an editorial expression. Header/footer and blank page area inspected.',
    11: 'Both columns read: 4.85, 4.9 heading/counter, 4.91 introduction and two bullets, 4.92 introduction/three bullets/closing, 4.93-4.94, 5.0 heading/introduction/important box, 5.1 and 5.11-5.15 with both exception blocks and activation example, 5.2/5.21/example and 5.22 introduction. Stacking rules, Momentum rule and Trump Option are visibly explicit references and now indexed. Ordinary phase/term occurrences are not inferred citations. Header/footer and both continuation boundaries inspected.',
    12: 'Both columns read: 5.22 seven items/closing; 5.23 introduction/two items/closing; 5.24/example; 5.25; both 5.26 paragraphs and column continuation/example; 5.27-5.28 with two items/closing; 5.3 heading/note; 5.31 introduction/three bullets; 5.32/example; 5.33 introduction/three bullets; 5.34. Explicit Phase A, Phase B, both phase-D destinations and Trumping, below are now indexed. Header/footer and blank page area inspected.',
}
for page in [9,10,11,12]:
    rows = [r for r in ledger['regions'] if r['pdf_page']==page]
    gap = next(g for g in coverage['task']['geometric_gaps'] if g['pdf_page']==page)
    boxes = [r['region']['box'] for r in rows]
    gaps = gap['geometric_gap_rectangles']
    all_boxes = boxes + gaps
    xs = sorted({v for b in all_boxes for v in [b[0],b[2]]})
    assert xs[0]==0 and xs[-1]==1000000
    for x1,x2 in zip(xs,xs[1:]):
        intervals = sorted((b[1],b[3]) for b in all_boxes if b[0]<=x1 and b[2]>=x2)
        y=0
        for y1,y2 in intervals:
            assert y1==y and y2>y1
            y=y2
        assert y==1000000
    gap_area=sum((b[2]-b[0])*(b[3]-b[1]) for b in gaps)
    assert gap_area==gap['unaccounted_area_trillionths']
    pages.append(dict(pdf_page=page, observation=descriptions[page], region_count=len(rows), original_image=pin(OLD/f'original-pages/page-{page:02d}.png'), column_images=[pin(OLD/f'original-pages/page-{page:02d}-{side}.png') for side in ['left','right']], boundary_overlay=pin(OLD/f'original-pages/boundaries-{page:02d}.png'), gap_rectangles=len(gaps), geometric_gap_area_trillionths=gap_area, exact_geometry_partition='pass', further_explicit_reference_omissions_observed=0))

prior = read('private/workflow/runs/IG-2B03/review-b3172589-20261015/source-comparison.json')
assert {r['region_id'] for r in prior['region_comparisons']} == {r['region']['id'] for r in ledger['regions']}
for r in ledger['regions']:
    p=next(x for x in prior['region_comparisons'] if x['region_id']==r['region']['id'])
    assert all(p[k]==r['region'][k] for k in ['key','revision','box'])
assert len(prior['component_comparisons'])==22
write('source-comparison.json', dict(format='wgc-independent-r01-source-review-1', original_pdf=pin('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf'), method='Fresh visual inspection of all four frozen original-page PNGs, both original column crops for every page, all complete region overlays and the two counter/component overlays including expanded page-11 artwork. All 135 ledger rows were read in bounded per-page sections and compared to visible source; all 22 component observations and boundaries compared. Existing original images and prior reviewed coverage were hash-verified. No old derivation helper or transcript was read. Six fresh root structural validations supplement this source review; no old extraction/evidence/replays were regenerated.', pages=pages, region_comparisons=[dict(region_id=r['region']['id'],key=r['region']['key'],revision=r['region']['revision'],box=r['region']['box'],page_reading_order_index=r['page_reading_order_index'],result='Visible original page and boundary compared; raw reference index checked; no further actionable omission observed.', raw_cross_references=r['raw_cross_references']) for r in ledger['regions']], component_comparisons=[dict(key=r['key'],box=r['box'],page=r['page'],observation=r['observation'],result='Compared to visible counter and component overlay; inherited uncertainty preserved; context denominator remains zero.') for r in components['components']], preserved_prior_source_review=pin('private/workflow/runs/IG-2B03/review-b3172589-20261015/source-comparison.json'), prior_region_scope_exactly_preserved=True, changed_references=read(ROOT/'hash-structure-verification.json')['changed_regions'], literal_continuations=read(NEW/'continuations.json')['literal_continuations'], source_entry='Physical page 9 begins with complete 4.34; page 8 was not inspected.', source_exit='Physical page 12 ends with complete visible 5.34; page 13 was not inspected.', named_reference_policy='Explicit literal rule/option names, directional citations and labeled phase destinations retained; associated names with numeric citations remain in exact raw text; ordinary gameplay terms do not create inferred citations. No cited target was followed or assigned an inferred number.', missing_visible_source_regions_observed=0, standalone_tables_or_legends_observed=[], content_gaps='All 135 task regions remain unprocessed at transcription/descriptive/formal levels; all exact geometric gaps remain explicit; no editorial exclusion is authorized.', task_denominator=135, component_task_denominator=0, optional_page8_task_denominator=0, semantic_acceptance_granted=False, executable_readiness='unverified'))

checks = [dict(command='.venv/Scripts/python.exe -B -m pytest -q tests/sources --basetemp private/workflow/checks/b03-cabf2418 -p no:cacheprovider --tb=short',exit_code=0,result='71 passed in 26.63s',permissions='Approved require_escalated exact unchanged command after restricted-token mode0700 WinError 5'),dict(command='pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B03',exit_code=0,result='192 passed in 44.66s; plan/dry-run/tests/diff all zero',permissions='Approved require_escalated exact unchanged command after restricted-token mode0700 WinError 5', report=pin('private/workflow/checks/active-d6d08123c8ff44f286fe7b9d694afbd0/result.json')),dict(command='.venv/Scripts/python.exe -B scripts/workflow.py validate',exit_code=0,result='Validated 39 tasks, DAG, scope, context and derived views.'),dict(command='git diff --check',exit_code=0,result='Approved read-only execution passed; existing CRLF normalization warnings only.',permissions='Approved require_escalated exact unchanged command after initial restricted-token access warnings'),dict(command='.venv/Scripts/python.exe -B '+(ROOT/'verify.py').relative_to(Path.cwd()).as_posix(),exit_code=0,result='Every frozen artifact and exact control/dependency/source/configuration pin verified; full report structure comparison passed.'),dict(command='.venv/Scripts/python.exe -B '+(ROOT/'validate.py').relative_to(Path.cwd()).as_posix(),exit_code=0,result='157 locators verified; accepted nested scope/registry/evidence/links/order preserved; two authored replays byte-identical; six path-dependent inventories validated.')]
for c in read(ROOT/'validation.json')['checks']:
    data,_=json.JSONDecoder().raw_decode(Path(c['log']['path']).read_text(encoding='utf-8'))
    assert data['source_structure_verification']=='verified'
    checks.append({**c,'source_structure_verification':'verified'})
write('checks.json',dict(format='wgc-independent-review-checks-1',checks=checks,initial_failures='Source suite and repository check failed under the restricted Windows token with mode0700 WinError 5. Each exact unchanged command received one approved retry and passed. Initial diff output included access warnings despite exit zero; its approved exact retry had no access failures.',semantic_acceptance_granted=False))
print('Fresh complete source comparison and passing checks frozen.')
