"""Bind manual locator assessments to independently verified source/raw spans."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c3'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=load(R/'checklist.json');A=load(M/'annotations.json');diag=load(M/'locator-diagnostics.json');plan=load(P/'measurement/M-POC5A-semantic-04c1/scope-plan.json');prior=load(R/'current-state-19.json')
ids=plan['parts'][2]['evidence_ids'];assert [x[0] for x in A['rows']]==ids==[x['evidence_id'] for x in diag['rows']]
prov={r:load(P/f'proposals/{r}/provenance.json') for r in C['responses']};errors={r:load(P/f'reports/{r}/errors.json')['errors'] for r in C['responses']}
helpers=load(P/'inputs/v1/helper-regions.json')['regions'];baseline=load(P/'measurement/M-POC3-first-001/bbox-analysis.json')
def pattern(q):
    return ''.join(r'\s+' if c.isspace() else re.escape(c)+r'(?:[-\u00ad]\s*)?' if c.isalpha() else re.escape(c) for c in q)
def trace(run,eid):
    x=C['output_records'][run][eid];ptr=x['pointer'];obj=x['original_record']
    fields={k:dict(pointer=ptr+'/'+k,raw_span=prov[run]['json_value_spans'][ptr+'/'+k],original_value=v) for k,v in obj.items()}
    precise={}
    for name in ['quote/value','image/bbox','image/path','image/sha256','image/width','image/height','image/coordinate_system']:
        val=obj
        for k in name.split('/'):val=val[k]
        precise[name]=dict(pointer=ptr+'/'+name,raw_span=prov[run]['json_value_spans'][ptr+'/'+name],original_value=val)
    return dict(response=C['responses'][run],pointer=ptr,raw_span=x['raw_span'],original_record=obj,fields=fields,locator_fields=precise)
OUT.mkdir(exist_ok=False);rows=[]
for (eid,assessment,note),d in zip(A['rows'],diag['rows']):
    e=C['output_records']['context-01'][eid]['original_record']
    if e['pdf_page']==27:
        helperpath=P/'context/pass-01/evidence/8.46-step-4-helper.txt';helpertext=helperpath.read_text(encoding='utf-8-sig');helperpointer=None
    else:
        idx,region=next((i,x) for i,x in enumerate(helpers) if x['region_id']==e['region_id']);helperpath=P/'inputs/v1/helper-regions.json';helpertext=region['text'];helperpointer=f'/regions/{idx}/text'
    match=re.search(pattern(e['quote']['value']),helpertext);assert match,eid
    source_helper=dict(artifact=ref(helperpath),pointer=helperpointer,region_id=e['region_id'],character_range=list(match.span()),literal_text=match.group(),utf8_excerpt_sha256=hashlib.sha256(match.group().encode()).hexdigest(),
        source=C['source'],pdf_page=e['pdf_page'],image=ref(P/e['image']['path']),scope='Exact short quoted occurrence in previously supplied source only; crop27 restricted to Step4.')
    issue='SEM-007'
    loss=sum(c['dark_pixels_outside_original_crop'] for c in d['quote_glyphs_outside_box'])
    assert not d['quote_whole_glyph_envelopes_contained']
    assert (loss==7)==(eid=='E1011')
    assert assessment in ['readable_raster_envelope_not_contained','readable_but_descender_ink_clipped']
    row=dict(id=eid,pdf_page=e['pdf_page'],source_scope='Original short quote and its asserted image rectangle, not entire evidence/node/rule.',
        source_quote_original=e['quote']['value'],independent_source_helper=source_helper,source_image=d['source_image'],
        diagnostic_artifact=ref(M/'locator-diagnostics.json'),diagnostic_pointer=f'/rows/{len(rows)}',diagnostic=d,
        manual_assessment=assessment,manual_comparison=note,reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',
        inherited_issue=issue,strict_full_quote_glyph_envelope='fails_exact_envelope_containment',
        raster_short_quote='readable_no_observed_ink_loss' if loss==0 else 'readable_but_descender_ink_clipped',
        literal_reading='Quote supported on full supplied page and exact helper; this does not certify the claimed crop contains complete quote.',
        interpretation='This locator review does not choose prior semantic variants or accept complete rule outcomes.',
        original_quote_and_image_equal_between_runs=d['both_runs_original_quote_and_image_equal'],exclusions=A['exclusions'],uncertainties=['PDF advance/character envelope is not font ink outline','Threshold diagnostic does not alone certify all ink/background','No full-record/whole-crop or unreviewed content acceptance'],runs={})
    for run in d['runs']:
        t=trace(run,eid);ptr=t['pointer'];b=e['image']['bbox']
        er=[dict(artifact=ref(P/f'reports/{run}/errors.json'),pointer=f'/errors/{i}',original_observation=x) for i,x in enumerate(errors[run]) if any(z.startswith(ptr+'/') for z in x['response_pointers'])]
        assert er,eid
        row['runs'][run]=dict(response=C['responses'][run],reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',evaluator_compared=True,output_trace=t,
            inherited_report_observations=er,geometry=dict(result='valid_coordinates_hash_dimensions_in_asserted_page',box=b,actual_dimensions=d['actual_dimensions'],does_not_establish_quote_coverage=True),
            quote_location=dict(source_helper=source_helper,actual_quote_bbox_pdf_points=d['source_quote_match']['bbox_pdf_points'],actual_quote_bbox_pixels=d['source_quote_match']['bbox_pixels'],
                strict_full_glyph_containment=False,strict_containment_policy='Raw no-tolerance predicate retained; envelope and ink independently assessed.',claimed_crop=t['original_record']['image'],missing_ink_pixels_diagnostic=loss),
            whole_glyph_boundary_review='All outside quote glyphs recorded individually in diagnostics; no tolerance expansion.',raster_review=row['raster_short_quote'],
            comparison=note,meaning_result='not_assessable_for_whole_record',proposed_assessment=assessment,exclusions=A['exclusions'],owner_decision=None)
    rows.append(row)
summary=dict(distinct_ids=22,assigned_occurrences=38,per_answer={'first-001':16,'context-01':22},context_only_ids=6,evaluator_compared_occurrences=38,owner_available_occurrences=38,new_owner_reviewed_occurrences=0,owner_pending_occurrences=38,
    geometry_valid_occurrences=38,short_quotes_supported_in_full_supplied_source=38,raw_no_tolerance_envelope_false_occurrences=38,
    strict_quote_glyph_envelope_passes=0,strict_quote_glyph_envelope_failures_geometrically_distinguishable=38,strict_quote_glyph_envelope_numeric_precision_unresolved=0,
    readable_raster_no_observed_quote_ink_loss=36,readable_raster_with_descenders_clipped=2,missing_final_quote_line=0,
    previous_owner_locator_scopes=86,total_evaluator_compared_locator_occurrences=124,remaining_uncompared_locator_occurrences=0,all_locator_scope_occurrences=124,
    owner_actual_file_open_or_read='unknown',previous_owner_relation_scopes=257,pending_expectation_ids=prior['pending_expectation_ids'],semantic_error_counts='not_assessable',TP_FP_FN_precision_recall='not_assessable')
packet=dict(id='M-POC5A.4c3-comparisons-01',card='M-POC5A.4c3',status='partial_waiting_review',evaluation=C['evaluation'],source=C['source'],responses=C['responses'],
    previous_state=ref(R/'current-state-19.json'),owner_decision=ref(R/'owner-decision-09.json'),owner_overlay=ref(R/'owner-review-overlay-09.json'),
    scope_plan=ref(P/'measurement/M-POC5A-semantic-04c1/scope-plan.json'),estimate=ref(M/'start.json'),method=A['method'],authoring=ref(M/'annotations.json'),summary=summary,locators=rows,
    numerical_precision_policy=A['numerical_precision_policy'],visual_evidence_policy='Exact original crops retained; references/magnification/sheets are diagnostics from previously supplied rasters, never repaired locators.',
    full_pages_manually_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in [36,37]],quote_sheets_manually_inspected=[ref(M/f'visual/page-{n}-quote-sheet.png') for n in [36,37,27]],supplied_context_crop_manually_inspected=ref(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png'),
    exact_crops_manually_inspected=[ref(M/f'visual/{n}-exact.png') for n in ['E1011','E981','ECTX846S4-header','ECTX846S4-SK','ECTX846S4-LC','ECTX846S4-DS','E98']],
    magnified_boundary_patches_manually_inspected=[ref(M/f'visual/E1011-boundary-{n}.png') for n in [6,14]],
    inherited_issues=prior['unresolved_issue_ids'],prior_dispositions=prior['issue_dispositions'],new_owner_decisions=[],new_sources=0,new_extractions=0,new_corrections=0,other_parts_executed=False,limits=C['limits'],limitations=C['limitations'])
save(OUT/'comparisons.json',packet)
save(OUT/'issues.json',dict(inherited_pending=prior['unresolved_issue_ids'],previous_dispositions_preserved=prior['issue_dispositions'],observations=[
    dict(id='SEM-007',scope=ids,occurrences=38,proposal='38 valid source/geometry locators;36 readable short rasters without observed ink loss,2E1011 readable but clipped p/Q. All38 measurable envelope failures, no automatic meaning error.',status='waiting_review',human_reviewer=None)],
    new_semantic_issue_ids=[],wrong_read='not_assessable',no_automatic_semantic_FP_or_FN=True,remaining_uncompared_locator_occurrences=0))
save(OUT/'presentation.json',dict(card='M-POC5A.4c3',summary=summary,decisions=[
    dict(number=1,ids=ids,occurrences=38,proposal='Accept valid geometry/source short-quote location and retain38 full-envelope failures, without whole record or automatic meaning error.'),
    dict(number=2,ids=[i for i in ids if i!='E1011'],occurrences=36,proposal='Accept readable short rasters without observed quote ink loss; source27 only suppliedcrop,6context-only records.'),
    dict(number=3,ids=['E1011'],occurrences=2,proposal='Accept evidence defect: text readable, but p in printed and Q tails clipped. Original crop unchanged; no demonstrated semantic misreading.')],
    count_policy='38 distinct occurrence assessments;38+36+2 overlapping facets, not76 new points.',excludes=A['exclusions'],actual_owner_file_open_or_read='unknown',proposal_only=True,
    next_after_owner_decision='Separate.4d inventory/pending reconciliation after full estimate/split if needed. Then separateM-POC5B20situations; old unresolved remain open.'))
lines=['# M-POC5A.4c3 — 22 lokatory /38 wystąpień','',A['method'],'',
    'Geometria/źródło38; pełne obwiednie38 naruszeń. Krótkie rastry36 czytelne bez obserwowanej utraty tuszu;2E1011 czytelne, ale dolne fragmenty p/Q ucięte.16 wspólnychID mają osobne ślady16/16;6 nowychID tylko context-01, bez pozornej oceny nieistniejących rekordów first.',
    '',*[f"{run}: `{x['sha256']}`, {x['bytes']} bajtów." for run,x in C['responses'].items()],
    '',f"eval-v1 `{C['evaluation']['sha256']}`; source `{C['source']['sha256']}`.",
    '', '[Ślady JSON](comparisons.json) · [Decyzje po ludzku](owner-focus.md). Nowe oceny waiting_review.','']
for row in rows:
    d=row['diagnostic'];helper=row['independent_source_helper'];lines += [f"## {row['id']}",'','Zakres: oryginalny krótki cytat i wskazany prostokąt.','',
        '> '+row['source_quote_original'],'','Dosłowny helper:','', '> '+helper['literal_text'].replace('\n','\n> '),'',
        f"Helper `{helper['artifact']['path']}` pointer{helper['pointer']}, znaki{helper['character_range']}, hash`{helper['utf8_excerpt_sha256']}`.",'',
        f"PDF{row['pdf_page']}; bbox piksele{d['original_bbox_pixels']}, PDFpt{d['bbox_pdf_points']}; rozmiar{d['actual_dimensions']}. Mapowanie{json.dumps(d['coordinate_mapping'],ensure_ascii=False)}.",'',
        f"Cytat PDFpt{d['source_quote_match']['bbox_pdf_points']}; obwiednie{row['strict_full_quote_glyph_envelope']}; raster{row['raster_short_quote']}.",'',
        'Ręczne porównanie: '+row['manual_comparison'],'',
        f"[Dokładny crop](../../../measurement/M-POC5A-semantic-04c3/visual/{row['id']}-exact.png) · [Referencja granic](../../../measurement/M-POC5A-semantic-04c3/visual/{row['id']}-quote-reference.png). Referencja nie naprawia oryginału.",'']
    for run,x in row['runs'].items():
        t=x['output_trace'];sp=t['raw_span'];lines += [f"**{run}:** `{t['pointer']}`, bajty[{sp['start_byte']},{sp['end_byte_exclusive']}), hash`{sp['sha256']}`; oceniającyCodex, właściciel waiting_review.",'']
        for field in ['quote/value','image/bbox','image/path','image/sha256']:
            f=t['locator_fields'][field];sp=f['raw_span'];lines += [f"`{f['pointer']}`; bajty[{sp['start_byte']},{sp['end_byte_exclusive']}), hash`{sp['sha256']}`, oryginał{json.dumps(f['original_value'],ensure_ascii=False)}.",'']
    if len(row['runs'])==1:lines += ['first-001: tenID nie występuje; nie nadano oceny lokatora nieistniejącego rekordu.','']
    lines += ['Poszczególne glify poza obwiednią według raw predicate:','',*[json.dumps(x,ensure_ascii=False) for x in d['quote_glyphs_outside_box']],'',
        'Wyłączenia: całe rekordy/klauzule/crop, żetony/ratingi/diagram/setup/sytuacje, dawne pending, pełne brakujące procedury i automatyczne semantyczneFP/FN.','']
lines += ['## Granice i dalsza praca','',
    'Porównano38 /udostępniono38 /nowych decyzji właściciela0 /pending38. Łącznie124/124 przypisane wystąpienia lokatorów rzeczywiście porównane;86 poprzednich z bounded decyzjami właściciela. To nie certyfikat wszystkich lokatorów/grafu lub poprawnych całych rekordów.',
    'Owner09 przyjął42 ocen .4c2:42 czytelne,40 mierzalnych ograniczeń obwiedni,2E962 nieocenialne z powodu precyzji. Dawne wady nie naprawione.257 komponentowych decyzji relacji,264 pary rubryka/EXP i8 oczekiwań oraz wcześniejsze nierozstrzygnięcia zachowane.',
    A['numerical_precision_policy'],
    'Pozostały etap5: po obecnych decyzjach osobna.4d rozliczy207 pozycji, szersze nieprzejrzane komponenty/66+8 oczekiwań/pending, po oszacowaniu i ewentualnym podziale. M-POC5B osobno20 sytuacji x2 odpowiedzi. Liczba dalszych sesji/godzin nieustalona, nie wykonano.4d/B w tej sesji.',
    'Pełne TP/FP/FN/precision/recall nieocenialne; gold/limity bez zmiany. Brak nowych źródeł/ekstrakcji/korekt; historyczna ekspozycja/cleancontext, czasy/selektory/tokeny/cena/budżet unknown. M-POC5A/.4/.4b/.4c partial, M-POC5 jedyny next.','']
(OUT/'comparisons.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'review.md').write_text('# M-POC5A.4c3 — przegląd wykonany\n\n'+A['method']+'\n\n[Porównania](comparisons.md) · [Surowe ślady](comparisons.json) · [Decyzje](owner-focus.md)\n\n'+'\n\n'.join(lines[-6:]),encoding='utf-8')
save(M/'packet-summary.json',summary);print(json.dumps(summary,ensure_ascii=False))
