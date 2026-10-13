"""Bind manual locator assessments to independently verified source/raw spans."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c1'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=load(R/'checklist.json');A=load(M/'annotations.json');diag=load(M/'locator-diagnostics.json');plan=load(M/'scope-plan.json');prior=load(R/'current-state-15.json')
ids=plan['parts'][0]['evidence_ids'];assert [x[0] for x in A['rows']]==ids==[x['evidence_id'] for x in diag['rows']]
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
    issue='SEM-005' if eid=='E916' else 'SEM-007'
    loss=sum(c['dark_pixels_outside_original_crop'] for c in d['quote_glyphs_outside_box'])
    assert not d['quote_whole_glyph_envelopes_contained']
    assert (loss>0)==(assessment!='readable_raster_envelope_not_contained')
    row=dict(id=eid,pdf_page=e['pdf_page'],source_scope='Original short quote and its asserted image rectangle, not entire evidence/node/rule.',
        source_quote_original=e['quote']['value'],independent_source_helper=source_helper,source_image=d['source_image'],
        diagnostic_artifact=ref(M/'locator-diagnostics.json'),diagnostic_pointer=f'/rows/{len(rows)}',diagnostic=d,
        manual_assessment=assessment,manual_comparison=note,reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',
        inherited_issue=issue,strict_full_quote_glyph_envelope='fails_exact_envelope_containment',
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
                strict_full_glyph_containment=False,claimed_crop=t['original_record']['image'],missing_ink_pixels_diagnostic=loss),
            whole_glyph_boundary_review='All outside quote glyphs recorded individually in diagnostics; no tolerance expansion.',raster_review=row['raster_short_quote'],
            comparison=note,meaning_result='not_assessable_for_whole_record',proposed_assessment=assessment,exclusions=A['exclusions'],owner_decision=None)
    rows.append(row)
summary=dict(distinct_ids=22,assigned_occurrences=44,per_answer={'first-001':22,'context-01':22},evaluator_compared_occurrences=44,owner_available_occurrences=44,new_owner_reviewed_occurrences=0,owner_pending_occurrences=44,
    geometry_valid_occurrences=44,short_quotes_supported_in_full_supplied_source=44,strict_quote_glyph_envelope_passes=0,strict_quote_glyph_envelope_failures=44,
    readable_raster_no_observed_quote_ink_loss=38,readable_raster_with_descenders_clipped=4,missing_final_quote_line=2,
    remaining_uncompared_locator_occurrences=80,all_locator_scope_occurrences=124,owner_actual_file_open_or_read='unknown',
    previous_owner_relation_scopes=257,pending_expectation_ids=prior['pending_expectation_ids'],semantic_error_counts='not_assessable',TP_FP_FN_precision_recall='not_assessable')
packet=dict(id='M-POC5A.4c1-comparisons-01',card='M-POC5A.4c1',status='partial_waiting_review',evaluation=C['evaluation'],source=C['source'],responses=C['responses'],
    previous_state=ref(R/'current-state-15.json'),owner_decision=ref(R/'owner-decision-07.json'),owner_overlay=ref(R/'owner-review-overlay-07.json'),scope_plan=ref(M/'scope-plan.json'),estimate=ref(M/'start.json'),
    method=A['method'],authoring=ref(M/'annotations.json'),summary=summary,locators=rows,visual_evidence_policy='Original exact crops unchanged; red-reference/magnification/contact sheets are diagnostic views of already supplied raster, never replacement/corrected locators.',
    full_pages_manually_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in [31,32,33]],quote_sheets_manually_inspected=[ref(M/f'visual-02/page-{n}-quote-sheet.png') for n in [31,32,33]],
    exact_crops_manually_inspected=[ref(M/f'visual-02/{n}-exact.png') for n in ['E916','E914cont','E873']],
    magnified_boundary_patches_manually_inspected=[ref(M/f'visual-02/{eid}-boundary-{idx}.png') for eid,idx in [('E911a',0),('E914priority',0),('E915',0),('E92',0),('E914cont',7),('E873',18)]],
    inherited_issues=prior['unresolved_issue_ids'],prior_dispositions=prior['issue_dispositions'],new_owner_decisions=[],new_sources=0,new_extractions=0,new_corrections=0,other_parts_executed=False,
    limits=C['limits'],limitations=C['limitations'])
save(OUT/'comparisons.json',packet)
save(OUT/'issues.json',dict(inherited_pending=prior['unresolved_issue_ids'],previous_dispositions_preserved=prior['issue_dispositions'],
    observations=[
        dict(id='SEM-005',scope=['E916'],occurrences=2,proposal='Confirm inherited locator failure: final exception line outside unchanged rectangle; keep separate from semantic omission/wrong read and SEM-001/EXP-017.',status='waiting_review',human_reviewer=None),
        dict(id='SEM-007',scope=[x for x in ids if x!='E916'],occurrences=42,proposal='All42 fail exact whole-glyph envelopes.38 have readable short raster quote without observed ink loss;4 (E914cont/E873) visibly clip descenders. Partial source/locator judgment only;80 assigned locator occurrences not reviewed here.',status='waiting_review',human_reviewer=None)],
    new_semantic_issue_ids=[],wrong_read='not_assessable',no_automatic_semantic_FP_or_FN=True))
save(OUT/'presentation.json',dict(card='M-POC5A.4c1',summary=summary,decisions=[
    dict(number=1,ids=ids,occurrences=44,proposal='Accept source quote location and valid geometry separately from full quote containment. All44 fail strict whole-glyph-envelope criterion.'),
    dict(number=2,ids=[r['id'] for r in rows if r['manual_assessment']=='readable_raster_envelope_not_contained'],occurrences=38,proposal='Accept only readable short raster quote without observed ink loss, retaining strict envelope limitation; no whole crop/record acceptance.'),
    dict(number=3,ids=['E914cont','E873','E916'],occurrences=6,proposal='Accept observed incomplete raster evidence:4 descender clipping and2 missing final exception line. Correct source quote does not cure locator; no automatic wrong-read/full semantic error.')],
    excludes=A['exclusions'],actual_owner_file_open_or_read='unknown',proposal_only=True,next_after_owner_decision='Separate .4c2,21IDs/42occurrences after estimate; .4c3 and old pending preserved.'))
lines=['# M-POC5A.4c1 — rzeczywiste porównania22 lokatorów /44 wystąpień','',A['method'],'',
    '44 geometrie poprawne i cytaty znalezione w pełnym dostarczonym źródle. Ścisłe pełne obwiednie glifów:0 pass/44 fail. Raster:38 krótkich czytelnych cytatów bez zaobserwowanej utraty tuszu,4 z przyciętymi descenderami,2 z brakującą ostatnią linią. To różne miary, nie liczba poprawnych reguł.',
    '',*[f"{run}: `{a['sha256']}`, {a['bytes']} bajtów." for run,a in C['responses'].items()],
    '',f"eval-v1 `{C['evaluation']['sha256']}`; source `{C['source']['sha256']}`.",
    '', '[Pełne ślady JSON](comparisons.json), [decyzje po ludzku](owner-focus.md). Wszystkie nowe propozycje waiting_review.','']
for row in rows:
    d=row['diagnostic'];helper=row['independent_source_helper'];lines += [f"## {row['id']}",'','Dokładny zakres: oryginalny krótki cytat i jego prostokąt.','',
        '> '+row['source_quote_original'],'','Niezależny dosłowny helper:','', '> '+helper['literal_text'].replace('\n','\n> '),'',
        f"Helper `{helper['pointer']}`, znaki {helper['character_range']}, SHA-256 `{helper['utf8_excerpt_sha256']}`.",'',
        f"Strona{row['pdf_page']}; bbox piksele {d['original_bbox_pixels']}, PDFpt {d['bbox_pdf_points']}; wymiary {d['actual_dimensions']}.",'',
        f"Rzeczywisty krótki cytat PDFpt {d['source_quote_match']['bbox_pdf_points']}; całe obwiednie NIE mieszczą się. Raster: {row['raster_short_quote']}.",'',
        'Ręczne porównanie: '+row['manual_comparison'],'',f"[Dokładny nieposzerzony crop](../../../measurement/M-POC5A-semantic-04c1/visual-02/{row['id']}-exact.png) · [Referencja do porównania granicy](../../../measurement/M-POC5A-semantic-04c1/visual-02/{row['id']}-quote-reference.png). Referencja nie naprawia lokatora.",'']
    for run,x in row['runs'].items():
        t=x['output_trace'];sp=t['raw_span'];lines += [f"**{run}:** `{t['pointer']}`, bajty [{sp['start_byte']},{sp['end_byte_exclusive']}), SHA-256 `{sp['sha256']}`. RecenzentCodex, humanwaiting_review.",'']
        for field in ['quote/value','image/bbox','image/path','image/sha256']:
            f=t['locator_fields'][field];sp=f['raw_span'];lines += [f"Pole `{f['pointer']}`; bajty [{sp['start_byte']},{sp['end_byte_exclusive']}), hash `{sp['sha256']}`; wartość {json.dumps(f['original_value'],ensure_ascii=False)}.",'']
    lines += ['Każdy naruszony glif:', '',*[json.dumps(c,ensure_ascii=False) for c in d['quote_glyphs_outside_box']],'',
        'Wyłączenia: pełny rekord/klauzula/pozostały crop, artwork/ratingi, wcześniejsze pending, brakujące procedury, automatyczne semantyczneFP/FN/gold.','']
lines += ['## Granice i wznowienie','',
    'Przypisano22ID/44wystąpienia i każde realnie porównano. Udostępniono44, porównano44, nowych decyzji właściciela0, pending44. Kolejne80wystąpień ma jawny przydział w .4c2/.4c3, tutaj nie wykonane.',
    'Owner-decision07 przyjmuje poprzednie68+2+2 zakresów .4b3; razem257 komponentowych ocen relacji. Nie daje całych poprawnych rekordów/grafu. Osiem wcześniejszych oczekiwań/SEM-001–013 w pozostałych zakresach otwarte; SEM-005/007 mają teraz ograniczone propozycje lokatorowe, bez automatycznego zamknięcia.',
    'Brak nowych źródeł/korekt/ekstrakcji/sytuacji; eval-v1/gold i limity bez zmiany. Pełne metryki/TP/FP/FN, aktywne czasy i budżet nieocenione. Izolacja dawnego context-01 bez zmiany: listing/path pozaallowlistą potwierdzony, odczyt treści oceny niezaobserwowany; exposure/cleancontextunknown.',
    'Po decyzji obecnego pakietu osobna .4c2,21ID/42wystąpienia po oszacowaniu. Nadrzędne M-POC5A/.4/.4b/.4c partial; M-POC5 jedyny next.','']
(OUT/'comparisons.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'review.md').write_text('# M-POC5A.4c1 — przegląd wykonany\n\n'+A['method']+'\n\n'+
    '[Każde porównanie](comparisons.md) · [ślad JSON](comparisons.json) · [decyzje](owner-focus.md) · [obserwacje SEM-005/007](issues.json).\n\n'+'\n\n'.join(lines[-5:]),encoding='utf-8')
save(M/'packet-summary.json',summary);print(json.dumps(summary,ensure_ascii=False))
