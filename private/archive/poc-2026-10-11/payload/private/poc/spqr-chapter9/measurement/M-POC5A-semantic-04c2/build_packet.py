"""Bind manual locator assessments to independently verified source/raw spans."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c2'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=load(R/'checklist.json');A=load(M/'annotations.json');diag=load(M/'locator-diagnostics.json');plan=load(P/'measurement/M-POC5A-semantic-04c1/scope-plan.json');prior=load(R/'current-state-17.json')
ids=plan['parts'][1]['evidence_ids'];assert [x[0] for x in A['rows']]==ids==[x['evidence_id'] for x in diag['rows']]
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
    e=C['output_records']['first-001'][eid]['original_record'];idx,region=next((i,x) for i,x in enumerate(helpers) if x['region_id']==e['region_id'])
    match=re.search(pattern(e['quote']['value']),region['text']);assert match,eid
    source_helper=dict(artifact=ref(P/'inputs/v1/helper-regions.json'),pointer=f'/regions/{idx}/text',region_id=region['region_id'],character_range=list(match.span()),literal_text=match.group(),utf8_excerpt_sha256=hashlib.sha256(match.group().encode()).hexdigest(),
        source=C['source'],pdf_page=e['pdf_page'],image=ref(P/e['image']['path']),scope='Exact short quoted occurrence only; not whole source rule or wider parent mapping.')
    issue='SEM-007'
    loss=sum(c['dark_pixels_outside_original_crop'] for c in d['quote_glyphs_outside_box'])
    assert not d['quote_whole_glyph_envelopes_contained']
    assert loss==0
    assert assessment in ['readable_raster_envelope_not_contained','readable_raster_numeric_precision_unresolved']
    row=dict(id=eid,pdf_page=e['pdf_page'],source_scope='Original short quote and its asserted image rectangle, not entire evidence/node/rule.',
        source_quote_original=e['quote']['value'],independent_source_helper=source_helper,source_image=d['source_image'],
        diagnostic_artifact=ref(M/'locator-diagnostics.json'),diagnostic_pointer=f'/rows/{len(rows)}',diagnostic=d,
        manual_assessment=assessment,manual_comparison=note,reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',
        inherited_issue=issue,strict_full_quote_glyph_envelope='not_assessable_numeric_precision' if eid=='E962' else 'fails_exact_envelope_containment',
        raster_short_quote='readable_no_observed_ink_loss' if loss==0 else 'missing_final_quote_line' if eid=='E916' else 'readable_but_descender_ink_clipped',
        literal_reading='Quote supported on full supplied page and exact helper; this does not certify the claimed crop contains complete quote.',
        interpretation='This locator review does not choose prior semantic variants or accept complete rule outcomes.',
        original_quote_and_image_equal_between_runs=True,exclusions=A['exclusions'],uncertainties=['PDF advance/character envelope is not font ink outline','Threshold diagnostic does not alone certify all ink/background','No full-record/whole-crop or unreviewed content acceptance'],runs={})
    for run in C['responses']:
        t=trace(run,eid);ptr=t['pointer'];b=e['image']['bbox']
        er=[dict(artifact=ref(P/f'reports/{run}/errors.json'),pointer=f'/errors/{i}',original_observation=x) for i,x in enumerate(errors[run]) if any(z.startswith(ptr+'/') for z in x['response_pointers'])]
        assert er,eid
        row['runs'][run]=dict(response=C['responses'][run],reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',evaluator_compared=True,output_trace=t,
            inherited_report_observations=er,geometry=dict(result='valid_coordinates_hash_dimensions_in_asserted_page',box=b,actual_dimensions=d['actual_dimensions'],does_not_establish_quote_coverage=True),
            quote_location=dict(source_helper=source_helper,actual_quote_bbox_pdf_points=d['source_quote_match']['bbox_pdf_points'],actual_quote_bbox_pixels=d['source_quote_match']['bbox_pixels'],
                strict_full_glyph_containment=False,strict_containment_policy='Raw no-tolerance predicate retained; numeric-only E962 is not proven clipping/pass.',claimed_crop=t['original_record']['image'],missing_ink_pixels_diagnostic=loss),
            whole_glyph_boundary_review='All outside quote glyphs recorded individually in diagnostics; no tolerance expansion.',raster_review=row['raster_short_quote'],
            comparison=note,meaning_result='not_assessable_for_whole_record',proposed_assessment=assessment,exclusions=A['exclusions'],owner_decision=None)
    rows.append(row)
summary=dict(distinct_ids=21,assigned_occurrences=42,per_answer={'first-001':21,'context-01':21},evaluator_compared_occurrences=42,owner_available_occurrences=42,new_owner_reviewed_occurrences=0,owner_pending_occurrences=42,
    geometry_valid_occurrences=42,short_quotes_supported_in_full_supplied_source=42,raw_no_tolerance_envelope_false_occurrences=42,
    strict_quote_glyph_envelope_passes=0,strict_quote_glyph_envelope_failures_geometrically_distinguishable=40,strict_quote_glyph_envelope_numeric_precision_unresolved=2,
    readable_raster_no_observed_quote_ink_loss=42,readable_raster_with_descenders_clipped=0,missing_final_quote_line=0,
    previous_owner_locator_scopes=44,total_evaluator_compared_locator_occurrences=86,remaining_uncompared_locator_occurrences=38,all_locator_scope_occurrences=124,
    owner_actual_file_open_or_read='unknown',previous_owner_relation_scopes=257,pending_expectation_ids=prior['pending_expectation_ids'],semantic_error_counts='not_assessable',TP_FP_FN_precision_recall='not_assessable')
assert all(x['raster_short_quote']=='readable_no_observed_ink_loss' for x in rows)
packet=dict(id='M-POC5A.4c2-comparisons-01',card='M-POC5A.4c2',status='partial_waiting_review',evaluation=C['evaluation'],source=C['source'],responses=C['responses'],
    previous_state=ref(R/'current-state-17.json'),owner_decision=ref(R/'owner-decision-08.json'),owner_overlay=ref(R/'owner-review-overlay-08.json'),
    scope_plan=ref(P/'measurement/M-POC5A-semantic-04c1/scope-plan.json'),estimate=ref(M/'start.json'),method=A['method'],authoring=ref(M/'annotations.json'),summary=summary,locators=rows,
    numerical_precision_policy=A['numerical_precision_policy'],visual_evidence_policy='Exact original crops retained; references/magnification/sheets are diagnostics from previously supplied rasters, never repaired locators.',
    full_pages_manually_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in [34,35]],quote_sheets_manually_inspected=[ref(M/f'visual/page-{n}-quote-sheet.png') for n in [34,35]],
    exact_crops_manually_inspected=[ref(M/f'visual/{n}-exact.png') for n in ['E924cont','E952','E962','E965','E972','E95','E97']],
    magnified_boundary_patches_manually_inspected=[ref(M/f'visual/{n}-boundary-0.png') for n in ['E952','E962','E963','E966b','E95']],
    inherited_issues=prior['unresolved_issue_ids'],prior_dispositions=prior['issue_dispositions'],new_owner_decisions=[],new_sources=0,new_extractions=0,new_corrections=0,other_parts_executed=False,limits=C['limits'],limitations=C['limitations'])
save(OUT/'comparisons.json',packet)
save(OUT/'issues.json',dict(inherited_pending=prior['unresolved_issue_ids'],previous_dispositions_preserved=prior['issue_dispositions'],observations=[
    dict(id='SEM-007',scope=ids,occurrences=42,proposal='All42 short rasters readable without observed ink loss.40 measurable whole-envelope differences,2 E962 numericalprecision unresolved. No asserted definite physical clipping from2.84e-14pt; no tolerance expansion/certain strict pass.',status='waiting_review',human_reviewer=None)],
    new_semantic_issue_ids=[],wrong_read='not_assessable',no_automatic_semantic_FP_or_FN=True,remaining_uncompared_locator_occurrences=38))
save(OUT/'presentation.json',dict(card='M-POC5A.4c2',summary=summary,decisions=[
    dict(number=1,ids=ids,occurrences=42,proposal='Accept valid geometry/source quote location and readable short raster without observed ink loss only. No whole record/whole-crop/glyph certificate.'),
    dict(number=2,ids=[i for i in ids if i!='E962'],occurrences=40,proposal='Retain measurable full-glyph-envelope containment failures; they do not automatically establish visible ink loss or semantic error.'),
    dict(number=3,ids=['E962'],occurrences=2,proposal='Accept numericprecision limitation:2.84e-14pt alone not demonstrated geometric clipping. Keep strict containment not_assessable_numeric_precision; no repair/tolerance/certain pass.')],
    count_policy='42 distinct occurrence assessments; three decisions cover overlapping facets, not84 or126 new points.',excludes=A['exclusions'],actual_owner_file_open_or_read='unknown',proposal_only=True,
    next_after_owner_decision='Separate.4c3,22IDs/38occurrences after estimate; old pending and.4d preserved.'))
lines=['# M-POC5A.4c2 — rzeczywiste porównania21 lokatorów /42 wystąpień','',A['method'],'',
    '42 poprawne geometrie i krótkie cytaty odnalezione w źródle; wszystkie42 rastry czytelne bez zaobserwowanej utraty tuszu. Obwiednie:40 mierzalnych naruszeń,2 E962 z samą niepewnością zmiennoprzecinkową. Raw exact predicate false42 zachowano, bez automatycznego strict pass. To osobne miary, nie liczba poprawnych całych reguł.',
    '',*[f"{run}: `{x['sha256']}`, {x['bytes']} bajtów." for run,x in C['responses'].items()],
    '',f"eval-v1 `{C['evaluation']['sha256']}`; source `{C['source']['sha256']}`.",
    '', '[Pełne ślady JSON](comparisons.json), [decyzje po ludzku](owner-focus.md). Wszystkie nowe propozycje waiting_review.','']
for row in rows:
    d=row['diagnostic'];helper=row['independent_source_helper'];lines += [f"## {row['id']}",'','Zakres: oryginalny krótki cytat i wskazany prostokąt.','',
        '> '+row['source_quote_original'],'','Niezależny dosłowny helper:','', '> '+helper['literal_text'].replace('\n','\n> '),'',
        f"Helper `{helper['pointer']}`, znaki {helper['character_range']}, hash `{helper['utf8_excerpt_sha256']}`.",'',
        f"Strona{row['pdf_page']}; bbox piksele {d['original_bbox_pixels']}, PDFpt {d['bbox_pdf_points']}; wymiary {d['actual_dimensions']}.",'',
        f"Rzeczywisty cytat PDFpt {d['source_quote_match']['bbox_pdf_points']}; obwiednie: {row['strict_full_quote_glyph_envelope']}; raster: {row['raster_short_quote']}.",'',
        'Ręczne porównanie: '+row['manual_comparison'],'',
        f"[Dokładny crop](../../../measurement/M-POC5A-semantic-04c2/visual/{row['id']}-exact.png) · [Referencja granic](../../../measurement/M-POC5A-semantic-04c2/visual/{row['id']}-quote-reference.png). Referencja nie naprawia oryginalnego lokatora.",'']
    for run,x in row['runs'].items():
        t=x['output_trace'];sp=t['raw_span'];lines += [f"**{run}:** `{t['pointer']}`, bajty [{sp['start_byte']},{sp['end_byte_exclusive']}), hash `{sp['sha256']}`. RecenzentCodex; nowa ocena właściciela waiting_review.",'']
        for field in ['quote/value','image/bbox','image/path','image/sha256']:
            f=t['locator_fields'][field];sp=f['raw_span'];lines += [f"Pole `{f['pointer']}`; bajty [{sp['start_byte']},{sp['end_byte_exclusive']}), hash `{sp['sha256']}`, wartość {json.dumps(f['original_value'],ensure_ascii=False)}.",'']
    lines += ['Każdy glif outside według niezmienionego raw predicate:','',*[json.dumps(x,ensure_ascii=False) for x in d['quote_glyphs_outside_box']],'',
        'Wyłączenia: całe rekordy/klauzule/crop, ratingi/diagram/setup, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.','']
lines += ['## Granice i wznowienie','',
    'Każde21ID/42wystąpienia faktycznie porównano. Udostępniono42, porównano42, nowych decyzji właściciela0, pending42. Poprzednie44 oceny .4c1 mają decyzjęowner08; łącznie86przypisanych wystąpień lokatorów porównano. Kolejne38ma jawny przydział .4c3, tutaj niewykonane.',
    A['numerical_precision_policy'],
    'Owner08 nie naprawił E916 lub innych cropów, przyjął mieszane oceny lokatorowe. SEM-005 potwierdzony tylko jako wada dowodu; SEM-007 częściowo oceniony, reszta otwarta. Osiem wcześniejszych oczekiwań i inne zakresySEM-001–013 zachowane;257 komponentowych decyzji relacji/264 pary rubryka/EXP bez zmiany.',
    'Brak nowych źródeł/ekstrakcji/korekt/sytuacji. Gold/limity i niewiadome izolacji/czasów/selektorów/tokens/ceny/budżetu bez zmiany. Pełne TP/FP/FN/precision/recall nieocenialne; ani raw predicate, ani raster nie poświadcza całego grafu/rekordu.',
    'Po decyzjach obecnego pakietu osobna .4c3:22ID/38wystąpienia po oszacowaniu. Nadrzędne M-POC5A/.4/.4b/.4c partial, M-POC5 jedyny next.','']
(OUT/'comparisons.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'review.md').write_text('# M-POC5A.4c2 — przegląd wykonany\n\n'+A['method']+'\n\n'+
    '[Każde porównanie](comparisons.md) · [surowe ślady](comparisons.json) · [decyzje](owner-focus.md) · [obserwacje SEM-007](issues.json).\n\n'+'\n\n'.join(lines[-6:]),encoding='utf-8')
save(M/'packet-summary.json',summary);print(json.dumps(summary,ensure_ascii=False))
