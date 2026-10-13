"""Materialize this evaluated first-result baseline once, without rewriting it."""
import collections
import datetime
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT=Path.cwd(); P=ROOT/'private/poc/spqr-chapter9'; M=P/'measurement/M-POC3-first-001'
A=json.loads((M/'analysis.json').read_bytes()); B=json.loads((M/'bbox-analysis.json').read_bytes())
raw=(P/'runs/first-001/first-001.json').read_bytes(); D=json.loads(raw)
E=json.loads((P/'evaluation/eval-v1/expectations.json').read_bytes())
G=json.loads((P/'evaluation/eval-v1/dependencies.json').read_bytes())
POL=json.loads((P/'evaluation/eval-v1/measurement-policy.json').read_bytes())
RUN=json.loads((P/'runs/first-001/run.json').read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(path):
    b=path.read_bytes();return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)}
def save(path,obj):
    if path.exists():
        assert json.loads(path.read_bytes())==obj, 'Refusing to overwrite baseline: '+str(path)
        return
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert sha(raw)==A['response']['sha256']
assert not A['issues'] and not A['duplicate_json_keys']
assert all(x['matches'] for x in A['input_integrity']+A['evaluation_integrity'])
for f in json.loads((M/'protected-before.json').read_bytes()):
    assert desc(ROOT/f['path'])==f, 'Protected artifact changed: '+f['path']
transfer=[]
for f in RUN['inputs']['known_prepared_package_files']:
    canonical=(ROOT/f['canonical_path']).read_bytes(); transferred=(ROOT/f['transfer_path']).read_bytes()
    assert canonical==transferred and sha(canonical)==f['sha256'] and len(canonical)==f['bytes']
    transfer.append({'package_path':f['package_path'],'sha256':sha(canonical),'bytes':len(canonical),'byte_identical':True})
assert (ROOT/RUN['response']['original_path']).read_bytes()==raw
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
PR=P/'proposals/first-001'; R=P/'reports/first-001'
assert not (R/'closure.json').exists(), 'Baseline already closed'
assert not R.exists() or not list(R.iterdir()), 'Report destination must be new/empty'
if (PR/'provenance.json').exists():stamp=json.loads((PR/'provenance.json').read_bytes())['recorded_at_utc']
PR.mkdir(parents=True,exist_ok=True);R.mkdir(parents=True,exist_ok=True)
if (PR/'proposal.json').exists():assert (PR/'proposal.json').read_bytes()==raw
else:(PR/'proposal.json').write_bytes(raw)
provenance={'run_id':'first-001','card':'M-POC3','recorded_at_utc':stamp,
 'raw_response':A['response'],'representation':desc(PR/'proposal.json'),
 'derivation':'Byte-identical standalone JSON representation. No wrapper removed; no value, number, punctuation, state or metadata edited.',
 'parse':'strict UTF-8, one JSON object, no trailing non-whitespace, no duplicate JSON keys or non-finite constants',
 'pointer_policy':'RFC6901 pointers; UTF-8 byte offsets are zero-based half-open ranges into raw_response, including JSON lexical quoting/escaping; span hash is over exactly those original bytes',
 'json_value_spans':A['json_value_spans'],'record_pointers':A['record_pointers'],
 'input_manifest':A['input_manifest'],'evaluation_manifest':A['evaluation_manifest'],
 'receipt_run':desc(P/'runs/first-001/run.json'),'receipt_evidence':desc(P/'runs/first-001/session-evidence.txt'),
 'extraction_configuration':RUN['extraction_configuration'],'extraction_timing':RUN['timing'],
 'historical_transferred_files':'unknown','historical_prompt':'unknown','clean_context':'unknown','independent_assessment_exposure':'unknown',
 'self_report_policy':'Retained in proposal bytes and receipt metadata; not an independent attestation. No proven blind trial and no proven contamination.',
 'semantic_acceptance':'not_performed','new_inference_responses':0,'corrections_in_this_session':0}
save(PR/'provenance.json',provenance)

errors=[]
def error(class_,criticality,detail,pointers=None,eval_refs=None,status='observed',impact=None):
    id_=f'ERR-first-001-{len(errors)+1:03}'
    errors.append({'id':id_,'class':class_,'criticality':criticality,'detail':detail,
      'response_pointers':pointers or [],'raw_spans':[A['json_value_spans'][x] for x in (pointers or [])],
      'evaluation_refs':eval_refs or [],'status':status,'impact':impact or 'Requires scoped review; no automatic semantic acceptance.',
      'raw_response_sha256':A['response']['sha256']})
    return id_
e916ptr=A['record_pointers']['E916']
format_error=error('format','unknown',
 'E916 quotes "This rule does not apply to Leader Elephants." but bbox ends at y=1000 px = 360 PDF pt; source final line extends below this box. Exact quote is supported on full page and in helper, not entirely in the asserted image area.',
 [e916ptr+'/quote/value',e916ptr+'/image'],['inventory:C-9.16-01','expectation:EXP-016'],
 status='confirmed_locator_failure',impact='Evidence trace is incomplete for the quoted exception; bbox validity alone cannot pass quote-in-area. Source exception criticality is frozen, semantic error criticality remains unknown.')

tuple_map={'DEP-008':'D924911','DEP-002':'D911914','DEP-017':'D953941','DEP-024':'D982985','DEP-041':'D914table'}
endpoint_map={'C-9.24-03':'R924','C-9.11-10':'R911','C-9.11-09':'R911','R-9.14':'R914',
 'C-9.53-05':'R953','R-9.41':'R941','C-9.82-01':'R982','C-9.85-01':'R985','R-9.85':'R985','C-9.14-01':'R914','T-01':'N914table',
 'C-9.72-01':'R972','R-9.71':'R971','TR-03':'N914table','C-9.14-11':'R914','C-9.86-01':'R986'}
outdep={d['id']:d for d in D['dependencies']}
relations=[]
for n,g in enumerate(G['confirmed_execution_relations']):
    expected=(endpoint_map[g['from']],endpoint_map[g['to']],g['kind'],g['explicitness'])
    matches=[d['id'] for d in D['dependencies'] if (d['from'],d['to'],d['kind'],d['explicitness'])==expected]
    expected_id=tuple_map.get(g['id'])
    assert matches==([expected_id] if expected_id else [])
    ids=matches; eptrs=[A['record_pointers'][x] for x in ids]
    err=None
    if not matches:
        err=error('pominięcie',g['criticality'],
          'No output dependency has frozen source/target/direction/kind/explicitness tuple '+str(expected)+'. Prose presence does not supply a dependency record.',
          ['/dependencies'],['dependency:'+g['id']],status='confirmed_structural_omission',impact='Critical scoped graph link absent; no full executable-graph or semantic verdict.')
    relations.append({'evaluation_id':g['id'],'evaluation_pointer':f'/confirmed_execution_relations/{n}',
      'frozen_from':g['from'],'frozen_to':g['to'],'kind':g['kind'],'explicitness':g['explicitness'],
      'mapped_output_endpoints':list(expected[:2]),'mapping_policy':'Exact printed-rule/object identity; source and target child scope retained in the frozen record, whole output rule mapping is a candidate only.',
      'candidate_output_ids':ids,'tuple_status':'candidate_tuple_match' if matches else 'missing_tuple',
      'scope_necessity_semantic_status':'not_assessable','reason':'Retained constraints and exact necessity scope require human semantic review in M-POC5; tuple presence earns no semantic TP.',
      'output_pointers':eptrs,'raw_spans':[A['json_value_spans'][x] for x in eptrs],
      'criticality':g['criticality'],'error_id':err})

mention_map={'DEP-044':'D966diag','DEP-063':'D953scenario'}
mentions=[]
for n,g in enumerate(G['mentions']):
    match=mention_map.get(g['id']); err=None
    if g['id']=='DEP-037':
        err=error('błędna interpretacja',g['criticality'],
         'Frozen mention occurrence of Stacking Charts is output as D961stack table_use execution; same source/reference, different kind. Candidate classification discrepancy, not an owner verdict.',
         [A['record_pointers']['D961stack']],['mention:'+g['id']],status='pending_human_classification')
        status='different_kind_candidate'; candidates=['D961stack']
    elif not match:
        err=error('pominięcie',g['criticality'],
          'No separate mention relation for frozen occurrence '+g['id']+' from '+g['from']+' to '+g['target_candidate']['name']+'. Other source/kind facets do not replace this occurrence.',
          ['/dependencies'],['mention:'+g['id']],status='confirmed_structural_omission',impact='Missing separate non-execution occurrence; external target alias identity remains unconfirmed.')
        status='missing_tuple';candidates=[]
    else:status='candidate_occurrence_match';candidates=[match]
    mentions.append({'evaluation_id':g['id'],'evaluation_pointer':f'/mentions/{n}',
        'from':g['from'],'target_candidate':g['target_candidate'],'output_ids':candidates,'tuple_status':status,
        'external_target_alias_identity':'not_assessable','semantic_status':'not_assessable','error_id':err,
        'raw_spans':[A['json_value_spans'][A['record_pointers'][x]] for x in candidates]})
continuation_ids=['Dcont-R911','Dcont-table914','Dcont-R914','Dcont-R924','Dcont-R966','Dcont-R991','Dcont-R996b']
continuations=[]
for n,(g,id_) in enumerate(zip(G['continuations'],continuation_ids)):
    d=outdep[id_]; assert d['kind']=='continuation' and d['explicitness']=='explicit'
    f=next(x for x in D['nodes'] if x['id']==d['from']); t=next(x for x in D['nodes'] if x['id']==d['to'])
    assert f['kind']==t['kind']=='fragment'
    # Require physical source reading order, then y position within same region.
    ev={e['id']:e for e in D['evidence']}
    fe=ev[f['evidence_ids'][0]];te=ev[t['evidence_ids'][0]]
    order=lambda e:(A['core_regions'].index(e['region_id']),e['image']['bbox'][1])
    assert order(fe)<order(te)
    continuations.append({'evaluation_id':g['id'],'evaluation_pointer':f'/continuations/{n}',
       'output_id':id_,'from':d['from'],'to':d['to'],'tuple_status':'candidate_physical_order_match',
       'semantic_status':'not_assessable','raw_span':A['json_value_spans'][A['record_pointers'][id_]]})

# Every proposed edge remains individually accounted for. Outside-set proposals
# are not silently FP, and broad candidate matches are not silently semantic TP.
candidate_ids=set(tuple_map.values())|set(mention_map.values())|set(continuation_ids)
output_edges=[]
for d in D['dependencies']:
    output_edges.append({'id':d['id'],'explicitness':d['explicitness'],'kind':d['kind'],
      'target_status':d['target_status'],'classification':'frozen_tuple_candidate' if d['id'] in candidate_ids else ('different_kind_candidate' if d['id']=='D961stack' else 'outside_confirmed_tuple_set_pending_review'),
      'semantic_result':'not_assessable','review_status':'waiting_review',
      'pointer':A['record_pointers'][d['id']],'raw_span':A['json_value_spans'][A['record_pointers'][d['id']]]})
for g in D['gaps']:
    is_context=g['class']=='missing_context'
    error('brak kontekstu' if is_context else 'niejednoznaczność','unknown',
       'Extractor-declared gap '+g['id']+': '+g['reason'],[A['record_pointers'][g['id']]],
       status='reported_claim_requires_review',impact={'affected_ids':g['affected_ids'],'blocking_claim':g['blocking'],'needed_context':g['needed_context'],'independent_semantic_confirmation':'not_assessable'})

quotes=A['quotes']; graphics={'E911counter','E921counter','E981counter','E985markers','E986marker'}
bbox={x['evidence_id']:x for x in B['results']}
for q in quotes:
    eid=q['evidence_id']; b=bbox[eid]
    if q['status']=='needs_visual_review':
        assert eid in {'E911design','E911counter'}
        q['status']='visual_source_match';q['visual_status']='matched_by_Codex'
        q['visual_note']='PDF32 design note retains the compound hyphen across line break.' if eid=='E911design' else 'PDF31 embedded counter graphic visibly reads Africa; helper omits graphic text.'
    if eid in graphics:
        q['area_status']='graphic_label_visually_located';q['area_note']='Named short label visually observed within corresponding counter/marker on full-page render; no numeric ratings or semantic use accepted.'
    elif eid=='E916':
        q['area_status']='failed';q['error_id']=format_error
    elif b['quote_status']=='contained_glyph_match':q['area_status']='contained_glyph_match'
    else:
        assert b['overlap_quote_status']=='overlapping_glyph_match'
        q['area_status']='boundary_clipping_pending_review'
        q['error_id']=error('niejednoznaczność','unknown',
          'Quote '+eid+' matches overlapping glyph extraction but not whole contained glyph extraction; bbox clips some quote-edge glyphs. Exact crop legibility/full quote containment remains unconfirmed.',
          [A['record_pointers'][eid]+'/image'],status='pending_locator_review',impact='Do not count this locator as a strict full-quote-area pass.')
    q['bbox_audit']=b
for im in A['images']:
    q=next(q for q in quotes if q['evidence_id']==im['evidence_id'])
    im['quote_in_area_status']=q['area_status']; im['content_within_bbox']='not_assessable'
    im['limitation']='Hash/dimensions/coordinates and short quote audited; complete node/rule transcription and small graphic values not accepted.'

mapped={x['inventory_id']:x for x in A['inventory_results']}
expectation_results=[]
for n,e in enumerate(E['expectations']):
    output_ids=sorted({id_ for ref in e['inventory_refs'] if ref in mapped for id_ in mapped[ref]['output_ids']})
    output_gap_ids=sorted({g['id'] for g in D['gaps'] if set(g['affected_ids'])&set(output_ids)})
    expectation_results.append({'id':e['id'],'evaluation_pointer':f'/expectations/{n}',
       'classification':e['classification'],'inventory_refs':e['inventory_refs'],'mapped_output_ids':output_ids,
       'unmapped_inventory_refs':[x for x in e['inventory_refs'] if x not in mapped],
       'candidate_gap_ids':output_gap_ids,'criticality':e['criticality'],
       'result':'not_assessable','reason':'M-POC3 locates candidates; all owned reviewed components, contradictions and concrete blocking behavior await human semantic review in M-POC5.',
       'raw_spans':[A['json_value_spans'][A['record_pointers'][x]] for x in output_ids]})
categories=[]
for c in POL['categories']:
    units=[{'id':u['id'],'expectation_id':u['expectation_id'],'result':'not_assessable',
            'reason':'All relevant confirmed components in this category/EXP pair have not undergone human semantic review.'} for u in c['units']]
    assert len(units)==c['denominator_proposed']
    categories.append({'id':c['id'],'checked_denominator':len(units),'correct':'not_assessable','errors':'not_assessable','omitted':'not_assessable','blocked':'not_assessable','unassessed':len(units),'percentage':'n/a','units':units})
class_counts=collections.Counter(x['class'] for x in errors)
confirmed=collections.Counter(x['class'] for x in errors if x['status'] in {'confirmed_locator_failure','confirmed_structural_omission'})
six=[{'class':c,'confirmed_observations':confirmed[c] if c in {'format','pominięcie'} else 'not_assessable',
      'logged_observations_or_claims':class_counts[c],'scope':'Locator/tuple audit and separately labeled output claims; counts are not accepted semantic errors.'}
     for c in ['format','pominięcie','błędny odczyt','błędna interpretacja','brak kontekstu','niejednoznaczność']]
metrics={'run_id':'first-001','evaluation_id':'eval-v1','recorded_at_utc':stamp,
 'response_sha256':A['response']['sha256'],'evaluation_manifest_sha256':A['evaluation_manifest']['sha256'],
 'method':'Independent offline format/reference/input checks, exact source-object crosswalk, bounded tuple candidates, strict and intersecting glyph locator checks plus seven full-page visual inspections. No correction or new model inference.',
 'counts':A['counts'],'clauses':{'output_local_clause_ids':154,'frozen_reference_clause_groups':98,'atomic_norm_denominator':'unknown','semantic_completeness':'not_assessable','percentage':'n/a'},
 'structural_checks':{k:{'passed':v,'checked_denominator':v} for k,v in A['checks'].items()},
 'input_files':{'matched':32,'checked_denominator':32},'transfer_files':{'byte_identical':33,'checked_denominator':33,'historical_use':'unknown'},
 'evaluation_files':{'unchanged_manifest_matches':7,'checked_denominator':7},
 'source_bindings':{'matched':34,'checked_denominator':34},'core_regions':{'in_order':12,'checked_denominator':12},
 'source_quotes':{'checked_denominator':105,'normalized_helper_matches':103,'additional_visual_matches':2,'supported_short_quotes':105,'transcription_error_count':'not_assessable','limitation':'Quote verification does not certify all output transcription or meaning.'},
 'image_locators':{'checked_denominator':105,'hash_dimensions_valid_coordinates':105,'strict_contained_quote_matches':41,'graphic_label_visual_matches':5,'quote_area_failure':1,'boundary_clipping_pending_review':58,'fully_valid_content_areas':'not_assessable'},
 'reference_inventory':{'checked_denominator':207,'located_candidates':205,'unassessed_locators':2,'semantic_unassessed':207,'correct':'not_assessable','incorrect':'not_assessable','omitted':'not_assessable','blocked':'not_assessable','percentage':'n/a','by_type':A['inventory_type_counts'],
   'distinct_printed_rule_labels':{'located':41,'checked_denominator':41,'semantic_correct':'not_assessable','method':'Exact label string and mapped rule evidence overlap; 9.96 splits counted once, no invented 9.92.'}},
 'content_groups':{'checked_denominator':66,'unassessed':66,'correct':'not_assessable','incorrect':'not_assessable','percentage':'n/a'},
 'context_groups':{'checked_denominator':8,'unassessed':8,'correctly_blocked':'not_assessable','unmarked_missing_context':'not_assessable'},
 'content_categories':categories,
 'relations':{'output_counts':A['output_edge_counts'],
   'explicit':{'checked_frozen_denominator':5,'tuple_candidates':5,'missing_tuples':0,'output_execution_denominator':72,'output_pending_review':72,'TP_gold':'not_assessable','TP_output':'not_assessable','FP':'not_assessable','FN':'not_assessable','precision':'not_assessable','recall':'not_assessable'},
   'implicit':{'checked_frozen_denominator':3,'tuple_candidates':0,'missing_tuples':3,'output_execution_denominator':26,'output_pending_review':26,'TP_gold':'not_assessable','TP_output':'not_assessable','FP':'not_assessable','FN':'not_assessable','precision':'not_assessable','recall':'not_assessable'},
   'direction_and_kind':{'exact_tuple_candidates':5,'checked_execution_denominator':8,'missing_exact_tuples':3,'confirmed_semantic_direction_or_kind_errors':'not_assessable'},
   'mentions':{'checked_frozen_denominator':7,'occurrence_candidates':2,'different_kind_candidate':1,'missing_tuples':4,'output_pending_review':21,'semantic_quality':'not_assessable'},
   'continuations':{'checked_frozen_denominator':7,'physical_order_candidates':7,'output_pending_review':7,'semantic_quality':'not_assessable'},
   'outside_confirmed_execution_set':{'explicit_pending':67,'implicit_pending':26,'not_certain_FP':True,'unconfirmed_eval_candidates':105},
   'complete_graph_certified':False},
 'situations':{'checked_denominator':20,'frozen_expected_local_results':17,'frozen_expected_blocks':3,'unassessed':20,'results':'not_assessable','reason':'M-POC5B not performed; no new situation inference in M-POC3.'},
 'six_error_classes':six,'accepted_critical_semantic_error_count':'not_assessable',
 'human_semantic_review':{'coverage':0,'checked_content_denominator':66,'status':'waiting_review','acceptance':'not_performed'},
 'cost':{'new_extractions_in_this_session':0,'new_context_rounds_in_this_session':0,'new_corrections_in_this_session':0,'extraction_configuration':'unknown','extraction_time':'unknown','user_active_seconds':'unknown','model_active_seconds':'unknown','tokens':'unknown','price':'unknown','budget_compliance':'unknown'},
 'blind_trial_verified':'unknown','historical_handoff_verified':'unknown',
 'context_result':'not_assessable','corrected_result':'not_assessable','semantic_acceptance':'not_performed'}
format_report={'run_id':'first-001','evaluation_id':'eval-v1','recorded_at_utc':stamp,
 'raw_response':A['response'],'json_parse':'passed','duplicate_json_keys':A['duplicate_json_keys'],
 'format_contract':desc(P/'formats/proposal-format-v1.md'),'schema_acceptance_is_semantic_acceptance':False,
 'required_key_field_id_reference_enum_checks':dict(A['checks']),
 'mechanical_schema_issues':A['issues'],'references':A['references'],
 'input_manifest':A['input_manifest'],'input_integrity':A['input_integrity'],'transfer_integrity':transfer,
 'evaluation_manifest':A['evaluation_manifest'],'evaluation_integrity':A['evaluation_integrity'],
 'source_bindings':A['source_bindings'],'quote_summary':metrics['source_quotes'],'image_summary':metrics['image_locators'],
 'confirmed_locator_failure_ids':[format_error],'quote_details':'quotes.json','image_details':'image-areas.json',
 'outcome':'readable_format_with_locator_failure_and_pending_clipping','blocks_reading':False,
 'early_format_repair_required_to_read':False,'human_semantic_acceptance':'not_performed'}
save(R/'format.json',format_report)
save(R/'inventory.json',{'run_id':'first-001','evaluation_id':'eval-v1','response_sha256':A['response']['sha256'],
 'evaluation_manifest_sha256':A['evaluation_manifest']['sha256'],'mapping_is_semantic_score':False,
 'summary':metrics['reference_inventory'],'items':A['inventory_results'],'expectations':expectation_results,
 'unmapped_reference_ids':sorted({r for e in expectation_results for r in e['unmapped_inventory_refs']}),
 'unassessed_locator_ids':[x['inventory_id'] for x in A['inventory_results'] if x['structural_status']=='unassessed_locator']})
save(R/'dependency-comparison.json',{'run_id':'first-001','evaluation_id':'eval-v1',
 'response_sha256':A['response']['sha256'],'evaluation_manifest_sha256':A['evaluation_manifest']['sha256'],
 'execution_relations':relations,'mentions':mentions,'continuations':continuations,'all_output_edges':output_edges,
 'review_rule':'Tuple candidate presence and physical order do not prove exact necessity scope or accept meaning. Every unique edge requires review before final precision.'})
save(R/'quotes.json',{'run_id':'first-001','response_sha256':A['response']['sha256'],'summary':metrics['source_quotes'],'quotes':quotes})
save(R/'image-areas.json',{'run_id':'first-001','response_sha256':A['response']['sha256'],'summary':metrics['image_locators'],
 'visual_review':{'reviewer':'Codex in current M-POC3 session','pages':[31,32,33,34,35,36,37],'scope':'Complete relevant supplied page renders viewed; five embedded graphic short labels and two helper-mismatch quotes located. No human acceptance or small-value/glyph certificate.'},'images':A['images']})
save(R/'errors.json',{'run_id':'first-001','response_sha256':A['response']['sha256'],
 'six_classes':six,'count_policy':'Observations, self-reported claims and pending classification are distinguished; absence of assessed semantic errors is not zero semantic errors.',
 'errors':errors,'operational_limitations':RUN['documentation_gaps']})
save(R/'metrics.json',metrics)
report=f'''# first-001 — zamknięty baseline M-POC3

Data: 2026-10-09, Europe/Warsaw. Zapis UTC: {stamp}.
Wykonawca: Codex, C:/repo/wargame-compiler, feature/tests. Wynik karty: done
w zakresie raportu pierwszego wyniku. Ocena znaczenia: waiting_review.

Odpowiedź ma 617941 bajtów, SHA-256 {A['response']['sha256']}.
Manifest wejść: {A['input_manifest']['sha256']}; manifest eval-v1:
{A['evaluation_manifest']['sha256']}. Oryginał to runs/first-001/first-001.json,
zgodnie z run.json, zamiast response.raw.txt. Proposal jest jego bajtowo identyczną
kopią. provenance.json prowadzi każdy JSON pointer do dokładnych zakresów bajtów
i hashy surowej odpowiedzi. Nie zmieniono wejść, manifestów, promptu ani eval-v1.

## Kontrole struktury i dowodów

JSON poprawnie parsuje się jako jeden obiekt UTF-8; brak duplikatów kluczy.
454 ID rekordów i 154 ID klauzul są unikalne. Rozwiązano 3401 referencji;
sprawdzono 9731 wymaganych kluczy, 797 Field objects, 730 wartości enum
i 4 tożsamości koperty, bez błędów tych kontroli. To kontrola roboczego formatu,
bez przyjęcia kontraktu docelowego ani semantycznej akceptacji.

32/32 artefakty manifestu mają zgodne bajty/hashe; 33/33 pliki pakietu kanonicznego
i transferu są identyczne. 34/34 deklaracje źródeł wiążą się z manifestem;
105/105 dowodów ma zgodne źródło, hash, stronę i region. 7/7 artefaktów eval-v1
zgodnych z zamrożonym manifestem. 12/12 regionów core ma mapę w kolejności;
4 regiony kontekstu nie są liczone jako core.

103/105 krótkich cytatów pasuje do pomocniczego tekstu po łączeniu wierszy
i dzielonych słów. Dwa dalsze cytaty zweryfikowano wizualnie: zachowany łącznik
w E911design oraz napis w grafice E911counter. Wszystkie 105 krótkich cytatów
ma źródłowe podparcie w tym ograniczonym zakresie; nie certyfikuje to całych
transkrypcji, liczb, pól reguł ani interpretacji.

105/105 obrazów ma zgodny plik/hash, wymiary PNG, stronę, jawny układ współrzędnych
i poprawne geometrycznie bbox. Kontrola położenia cytatu: 41/105 obejmuje pełne
glify tekstu; 5/105 krótkich napisów graficznych zlokalizowano wizualnie;
58/105 pasuje jedynie do glifów przecinających granice bbox i pozostaje do
przeglądu przycięć. Jeden obszar, E916, nie obejmuje całego cytatu: dolna granica
360 PDF pt urywa końcową linię. To potwierdzony błąd lokatora, mimo poprawnego
cytatu na pełnej stronie. Szczegóły, tekst w bbox i ślad bajtowy: quotes.json,
image-areas.json oraz errors.json. Odpowiedzi nie poprawiono.

## Inwentarz i sprawdzone mianowniki

Rozliczono każde z 207 ID inwentarza. 205 ma kandydata z przecięciem źródłowego
obszaru; dwa nagłówki C-9.94-01/C-9.96-01 mają reprezentację nadrzędną, lecz bez
przecięcia wskazanych dowodów z nagłówkiem. Oba pozostają unassessed_locator,
nie uznane automatycznie za pominiętą treść. Wszystkie 207 ocen znaczenia są
unassessed/not_assessable. Mapowanie przez rodzica nie dowodzi reprezentacji
każdej klauzuli. Znaleziono 41/41 różnych oznaczeń; podział 9.96 nie zwiększa
tego licznika. 50 reguł i 154 klauzule modelu nie są mianownikiem kompletności.

Inwentarz obejmuje 98 grup klauzul, 14 not, 1 tabelę, 3 wiersze tabeli,
2 diagramy, 7 kontynuacji oraz pozostałe rekordy i 17 uzupełniających spanów;
wszystkie ID i typy rozliczono w inventory.json. To inwentarz referencyjny,
bez pełnego gold rozdziału ani sprawdzonego atomowego mianownika.

Przeliczono 66 potwierdzonych grup treści i 8 grup wymagających kontekstu;
wynik semantyczny wszystkich: not_assessable do M-POC5. Mianowniki rubryk:
liczby 41, jednostki 38, negacje 43, warunki 66, wyjątki 52, czas 29,
tabele 7, diagramy 1. Każda para rubryka/EXP-ID ma zapis nieocenialności;
kategorii nie sumuje się jako dodatkowych punktów reguł. Wszystkie 20 sytuacji
(17 oczekiwanych wyników lokalnych, 3 blokady) nieocenione w M-POC3.

## Relacje

Odpowiedź: 126 unikalnych relacji — 72 jawne wykonawcze, 26 niejawnych
wykonawczych, 21 wzmianek i 7 kontynuacji. Każda ma osobny wpis oceny.
Mianowniki zamrożone przeliczono: 5 jawnych i 3 niejawne wykonawcze,
7 wzmianek, 7 kontynuacji. Porównano źródło, cel, kierunek, rodzaj i jawność;
mapowanie całej reguły do zakresu child jest wyłącznie kandydatem.

Jawne: 5/5 kandydatów par. Niejawne: 0/3; brak osobnych relacji
DEP-NEW-001/002/003 w wymaganych zakresach. Krytyczność pochodzi z eval-v1,
nie z nowej oceny za człowieka. Wzmianki: 2/7 kandydatów wystąpienia,
1/7 kandydat o innym rodzaju (D961stack), 4/7 brakujących osobnych par.
Kontynuacje: 7/7 kandydatów z prawidłową fizyczną kolejnością fragmentów.

TP_gold, TP_output, FP, FN oraz semantyczna precyzja/kompletność są
not_assessable; nie nadano pięciu kandydatom semantycznego TP. Pozostałe
67 jawnych i 26 niejawnych propozycji spoza potwierdzonych par czekają na review,
nie są pewnymi FP. Wzmianki i kontynuacje pozostają osobnymi kategoriami.
105 niepotwierdzonych kandydatur eval-v1 nie jest gold.

## Sześć klas

| Klasa | Potwierdzone obserwacje strukturalne | Inne zapisane obserwacje / twierdzenia |
|---|---:|---|
| format | 1 błąd obszaru E916 | format czytelny; bez potrzeby naprawy parsowania |
| pominięcie | 7 brakujących par (3 krytyczne niejawne, 4 wzmianki) | kompletność semantyczna klauzul not_assessable |
| błędny odczyt | not_assessable | 0 wpisów tej klasy, brak pełnego przeglądu transkrypcji |
| błędna interpretacja | not_assessable | 1 kandydat różnicy rodzaju, oczekuje człowieka |
| brak kontekstu | not_assessable | 79 jawnych deklaracji luk ekstraktora, ocena potrzeby/blokad pending |
| niejednoznaczność | not_assessable | 2 deklaracje ekstraktora i 58 przypadków granic glifów, pending |

Deklaracje G916/G953 nie ustanawiają nowej niejednoznaczności gold:
porównanie z wcześniej zatwierdzonymi zakresami EXP-017/040 wymaga M-POC5.
Każda obserwacja ma ID, klasę, krytyczność/unknown, dowód, wpływ i status.
Brak ocenionych błędów znaczenia nie jest zerem błędów. Problemy operacyjne
i niepotwierdzone pochodzenie są oddzielne od sześciu klas.

## Ograniczenia, zamknięcie i wznowienie

Konfiguracja, czas ekstrakcji, faktyczny historyczny prompt/lista przekazanych
plików, czysty kontekst, ekspozycja na ocenę, sposób eksportu, tokeny i cena
pozostają unknown. Samoopis nie jest niezależnym dowodem. Dostępność pakietu
teraz nie dowodzi jego historycznego użycia; nie potwierdzono ślepej próby ani
skażenia. Czas kalendarzowy tej oceny nie jest aktywnym czasem człowieka/modelu
ani czasem ekstrakcji. Nie potwierdzono zgodności z łącznym budżetem.

Baseline zamknięto przed jakąkolwiek korektą, nowym kontekstem lub inferencją;
closure.json wiąże hashe wszystkich artefaktów. Kontrole scripts/check.ps1
oraz git diff --check po aktualizacji dokumentów zapisuje wyłącznie nowy pomiar
measurement/M-POC3-first-001/completion.json i dopisany rekord sessions.jsonl;
nie zmieniają tego zamkniętego raportu. Nowe odpowiedzi i oceny muszą dostać
odrębne ID/katalogi. W tej sesji 0 ekstrakcji, 0 rund kontekstu, 0 korekt.

Dokładny następny krok: osobna karta M-POC4A od run.json, tego report.md,
dependency-comparison.json i listy 79 zadeklarowanych braków w errors.json:
wybrać wyłącznie potrzebne blokujące cele, sprawdzić dostępność źródeł i policzyć
przyrost stron/reguł/tabel oraz głębokość przed tworzeniem context/pass-01.
Nie zamieniać trzech brakujących relacji wewnętrznych w domyślny wniosek,
że potrzebny jest nowy zewnętrzny kontekst. M-POC5 otrzymuje jawny baseline,
nieocenione zakresy i G916/G953 do porównania z zamrożonymi decyzjami.
M-POC4A ani dalszych kart nie rozpoczęto. Semantyczna akceptacja: not_performed.
'''
assert not (R/'report.md').exists();(R/'report.md').write_text(report,encoding='utf-8')
artifacts=[desc(x) for folder in [PR,R] for x in sorted(folder.iterdir()) if x.is_file()]
save(R/'manifest.json',{'run_id':'first-001','card':'M-POC3','recorded_at_utc':stamp,
  'response':A['response'],'input_manifest':A['input_manifest'],'evaluation_manifest':A['evaluation_manifest'],
  'artifacts':artifacts,'self_hash_policy':'manifest hash recorded in closure.json','semantic_acceptance':'not_performed'})
save(R/'closure.json',{'id':'M-POC3-first-001-baseline-closure','run_id':'first-001',
  'closed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closed_before_corrections':True,
  'response':A['response'],'report_manifest':desc(R/'manifest.json'),
  'new_inference_responses':0,'new_context_rounds':0,'new_corrections':0,
  'outcome':'done_report_only','human_semantic_acceptance':'not_performed',
  'immutability_policy':'Do not edit this baseline. Later context/corrections/reviews use new artifacts and parent response hashes.'})
print(json.dumps({'closed':desc(R/'closure.json'),'six_classes':six,'error_records':len(errors)},ensure_ascii=False,indent=2))
