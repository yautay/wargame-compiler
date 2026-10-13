from session import ROOT,P,R,M,read,ref as file_ref,save,md,pointer,now
import collections,json

ref_cache={}
def ref(f):
    key=f.as_posix()
    if key not in ref_cache:ref_cache[key]=file_ref(f)
    return ref_cache[key]

OUT=R/'part-04d5';OUT.mkdir(exist_ok=True)
state=read(R/'current-state-29.json');overlay=read(R/'owner-review-overlay-14.json')
expectations=read(P/'evaluation/eval-v1/expectations.json')['expectations']
inventory=read(P/'evaluation/eval-v1/inventory.json')['items']
policy=read(P/'evaluation/eval-v1/measurement-policy.json')
scopeplan=read(P/'measurement/M-POC5A-semantic-04d1/scope-plan.json')
assert len(expectations)==74 and len(inventory)==207
prior={}
for part in ['part-02','part-03','part-04a']:
    f=R/part/'comparisons.json'
    for idx,x in enumerate(read(f)['expectations']):
        assert x['id'] not in prior;prior[x['id']]=(x,ref(f),f'/expectations/{idx}')
props={run:read(P/f'proposals/{run}/proposal.json') for run in overlay['runs']}
provs={run:read(P/f'proposals/{run}/provenance.json') for run in props}
raw={run:(ROOT/state['responses'][run]['path']).read_bytes() for run in props}
verified_traces=[]
def trace(run,ptr):
    span=provs[run]['json_value_spans'][ptr];chunk=raw[run][span['start_byte']:span['end_byte_exclusive']]
    import hashlib
    assert hashlib.sha256(chunk).hexdigest()==span['sha256']
    value=pointer(props[run],ptr);assert json.loads(chunk)==value
    verified_traces.append((run,ptr))
    return dict(response=state['responses'][run],pointer=ptr,raw_span=span,original_value=value)

# Manual boundary conclusions, retaining pending cases instead of choosing old variants.
pending_notes={
 'EXP-010': 'Wiersz1–6 wymaga kompasu wybranej bitwy. Oba modele odróżniają diagram przykładowy od rzeczywistej mapy i deklarują blocking=true; brakujące realne źródło nadal pozostaje otwarte. Nie zamieniam przykładu roll1 w uniwersalny kierunek ani blokady realnej mapy w blokadę zadanej syntetycznej trasy.',
 'EXP-017': 'Warunek DR>TQ i minimum1 są zapisane, lecz interpretation unknown i G916 blocking pozostawiają gałąź DR<=TQ bez ustalonego wyniku. Przyjęty numer/wyjątek Leader Elephant/literalna klauzula ani decyzja o lokatorze nie rozstrzygają SEM-001. Wariant pozostaje do dawnej decyzji właściciela, bez nowego zawsze1CH.',
 'EXP-019': 'Dosłowny unless rules specifically otherwise zachowany; exceptions unknown. Streszczenie Any leader may command i false blocking wymagają osobnej oceny realnego użycia. Ograniczone przyjęcie lokalnego odsyłacza/wymagania nie certyfikuje uprawnienia konkretnego leadera ani nie domyka SEM-009.',
 'EXP-040': 'Oba R953 zachowują both rout/separate hexes i literalne the unit, ale interpretation/G953 pozostawia liczbę eliminowanych jednostek otwartą. .4d3 przyjęła literalną treść, nie pełną gałąź per-unit eliminacji. Zachowuję SEM-002, w tym dostępność podparcia dla ekstraktora i realną geometrię/kolejność; nie pozyskuję nowej strony.',
 'EXP-050': 'R97intro ma datę/OC jako predykat, nie fakty wybranej bitwy; osobnej date/OC gap brak, AWL/RP/LOS/ZOC mają blocking gaps. Przyjęta proza nie jest przyjęciem kompletnej deklaracji źródeł lub konkretnej kwalifikacji bitwy. SEM-010 pozostaje otwarte; pominięcie historycznej końcówki SEM-021 już rozstrzygnięte osobno.',
 'EXP-052': 'R971 iR972 zachowują dwie bramki i stationary Shock exception, lecz nie podają jawnego połączenia we wskazanym reviewed_scope. .4d3 przyjęła dokładne klauzule osobno; nie wybrała koniunkcji za model. Brak DEP-NEW-001 zachowany strukturalnie; SEM-011/EXP-052 i sześć powiązanych rubryk pending.',
 'EXP-066': 'Lokalne ignore Chariots reference on Combat Tables zachowane. Do identyfikacji rzeczywistych wyłączanych entries potrzeba tabel; flags false pozostają oryginalne. .4d1 przyjęła literalny nakaz, nie wystarczalność blokady pełnego lookupu. SEM-012 pending, bez zgadywania tabel, nowego źródła lub twierdzenia o dokonanym złym lookupie.',
 'EXP-074': 'Modele zachowują visible glyphs i jawnie wykluczają game-wide/rating-position meanings. .4d4 potwierdziła Scorpio/markery w tym zakresie. Nie dostarcza to zidentyfikowanego rzeczywistego TQ/MA ani osobnej conditional blocking deklaracji; SEM-013 nadal pending. Syntetyczne TQ6 nie staje się realnym ratingiem jednostki.'}

exp_rows=[]
for idx,e in enumerate(expectations):
    original,prior_ref,prior_ptr=prior[e['id']]
    assert original['source_scope']==e['reviewed_scope'],e['id']
    row=dict(id=e['id'],classification=e['classification'],frozen_expectation_ref=ref(P/'evaluation/eval-v1/expectations.json'),
       expectation_pointer=f'/expectations/{idx}',reviewed_scope=e['reviewed_scope'],source_evidence=e['evidence'],
       prior_comparison_ref=prior_ref,prior_comparison_pointer=prior_ptr,
       unreviewed_fields=e['unreviewed_fields'],limits=e['limits'],runs={},whole_parent_record_accepted=False,
       reconciliation_reviewer='Codex',new_scoring_units=0,
       reconciliation=pending_notes.get(e['id'],'Dokładny zakres wcześniejszej decyzji zachowany. Porównano jego przypisanie do tego samego frozen reviewed_scope i obu oryginalnych hashów oraz sprawdzono wyłączenia. Nie przeniesiono akceptacji na cały parent, zewnętrzną procedurę lub realne parametry.'))
    for run,data in overlay['runs'].items():
        owned=[(family,i,x) for family in ['scopes','context_requirements'] for i,x in enumerate(data[family]) if x['id']==e['id']]
        assert len(owned)==(0 if e['id'] in pending_notes else 1),e['id']
        traces={oid:trace(run,t['pointer']) for oid,t in original['runs'][run]['output_trace'].items()}
        owner=owned[0][2] if owned else None
        if owner:
            assert owner['reviewed_scope']==e['reviewed_scope']
            assert owner['response']==state['responses'][run]
        row['runs'][run]=dict(response=state['responses'][run],prior_scoped_owner_status='reviewed' if owner else 'pending',
          prior_owner_decision=owner['decision'] if owner else None,
          owner_overlay_pointer=f'/runs/{run}/{owned[0][0]}/{owned[0][1]}' if owner else None,
          original_comparison=original['runs'][run]['comparison'],original_proposed_assessment=original['runs'][run].get('proposed_assessment',original['proposed_assessment']),
          reconciliation_result='preserve_accepted_local_scope' if owner and e['classification']=='confirmed_local_content_scope' else
            'preserve_accepted_source_requirement_full_result_blocked' if owner else 'preserve_old_pending_no_variant_chosen',
          exact_original_output_traces=traces,gap_claims=original['runs'][run].get('gap_claims',[]),
          full_dependent_result='not_assessable' if e['classification']=='requires_context' else 'excluded_beyond_exact_reviewed_scope',
          reviewer='Codex',new_owner_decision=None,whole_record_accepted=False)
    exp_rows.append(row)

inv_rows=[]
assigned=[id for part in scopeplan['parts'][:4] for id in part['inventory_ids']]
assert len(assigned)==207 and len(set(assigned))==207 and set(assigned)=={x['id'] for x in inventory}
for idx,i in enumerate(inventory):
    row=dict(id=i['id'],type=i['type'],frozen_inventory_pointer=f'/items/{idx}',runs={},reconciliation_reviewer='Codex',new_scoring_units=0)
    for run,data in overlay['runs'].items():
        oi,owner=next((n,x) for n,x in enumerate(data['inventory_scopes']) if x['id']==i['id'])
        assert owner['status']=='reviewed' and owner['whole_record_accepted'] is False
        row['runs'][run]=dict(response=state['responses'][run],owner_overlay=ref(R/'owner-review-overlay-14.json'),owner_overlay_pointer=f'/runs/{run}/inventory_scopes/{oi}',
           decision=owner['decision'],manual_assessment=owner['manual_assessment'],compared=True,available=True,owner_decided=True,
           reconciliation='Retain this exact previously accepted feature and its exclusions; label/parent/child/image does not certify entire containing record.',
           whole_record_accepted=False)
    inv_rows.append(row)

category_rows=[];accepted={x['id']:x for x in overlay['category_units']}
for ci,c in enumerate(policy['categories']):
    assert len(c['units'])==c['denominator_proposed']
    for ui,u in enumerate(c['units']):
        prev=accepted.get(u['id'])
        if prev:assert prev['scoped_content']==u['scoped_content']
        else:assert u['expectation_id'] in ['EXP-017','EXP-040','EXP-052']
        category_rows.append(dict(id=u['id'],category=c['id'],expectation_id=u['expectation_id'],policy_pointer=f'/categories/{ci}/units/{ui}',
          scoped_content=u['scoped_content'],per_answer_prior_status={r:'accepted_exact_scope' if prev else 'old_pending' for r in props},
          prior_owner_decision=prev['decision'] if prev else None,do_not_score=u['do_not_score'],
          reconciliation='Category tag only for exact accepted EXP components; no new rule point, no transfer from literal inventory judgments.' if prev else pending_notes[u['expectation_id']],
          reviewer='Codex',new_scoring_units=0))
assert len(category_rows)==277 and len(accepted)==264
category_counts={c['id']:dict(frozen_pairs=len(c['units']),prior_accepted_pairs=sum(u['id'] in accepted for u in c['units']),old_pending_pairs=sum(u['id'] not in accepted for u in c['units'])) for c in policy['categories']}

relation_rows=[];locator_rows=[];record_rows=[]
for run,data in overlay['runs'].items():
    rel={x['id']:x for x in data['relationship_scopes']}
    assert set(rel)=={x['id'] for x in props[run]['dependencies']},run
    for idx,edge in enumerate(props[run]['dependencies']):
        o=rel[edge['id']]
        relation_rows.append(dict(run=run,id=edge['id'],prior_owner_decision=o['decision'],prior_accepted_components=o['accepted_components'],
          excluded_components=o['excluded_components'],source_scope=o.get('source_scope'),target_scope=o.get('target_scope'),
          rejected_original_facets=o.get('rejected_original_facets'),expected_kind=o.get('expected_kind'),
          evaluator_comparison=o.get('evaluator_comparison',o.get('comparison',o.get('proposal',o['result']))),
          trace=trace(run,f'/dependencies/{idx}'),new_points=0,whole_record_accepted=False,full_dependent_result_accepted=False))
    for idx,o in enumerate(data['locator_scopes']):
        locator_rows.append(dict(run=run,id=o['id'],prior_owner_decision=o['decision'],prior_manual_assessment=o['manual_assessment'],
          prior_accepted_facets=o['accepted_facets'],evaluator_comparison=o['evaluator_comparison'],
          overlay_pointer=f'/runs/{run}/locator_scopes/{idx}',original_locator_repaired=False,whole_evidence_record_accepted=False,
          reconciliation='Keep source/geometry/readability and envelope failure as separate facets; earlier geometric acceptance does not accept meaning or repair source rectangle.'))
    for family in ['rules','nodes']:
        for idx,record in enumerate(props[run][family]):
            record_rows.append(dict(run=run,id=record['id'],trace=trace(run,f'/{family}/{idx}'),original_fields=list(record),
              whole_record_accepted=False,unreviewed_scope_policy='Every field remains limited to explicitly accepted feature/source/child scope; no full-field certificate from matching pointer. Unshown aliases/interpretation, real parameters and external procedures remain excluded.'))
assert len(relation_rows)==257 and len(locator_rows)==124 and len(record_rows)==218

issue_rows=[]
for name in ['issues.json','part-02/issues.json','part-03/issues.json','part-04a/issues.json']:
    f=R/name
    for idx,o in enumerate(read(f)['issues']):
        issue_rows.append(dict(id=o['id'],original_issue_ref=ref(f),original_issue_pointer=f'/issues/{idx}',original_proposal=o['proposal'],
           latest_limited_disposition=state['issue_dispositions'].get(o['id']),remaining_original_scope='retained_open_by_owner_instruction',
           reconciliation='Use latest additive decisions for accepted facets; do not repeat stale earlier pending as if unchanged. Remaining meaning/full-record/source scope stays open.',reviewer='Codex'))
assert len(issue_rows)==13 and {x['id'] for x in issue_rows}==set(state['unresolved_issue_ids'])
for o in issue_rows:
    if o['id']=='SEM-004':o['reconciliation']='DCTX923-S4 operator correspondence already accepted; earlier mixed-defense/Size/CRT and broader semantics remain open. No new gold edge.'
    if o['id']=='SEM-005':o['reconciliation']='E916 locator defect confirmed by owner; original unchanged. Do not reopen accepted defect, or infer semantic minimum resolution from it.'
    if o['id']=='SEM-006':o['reconciliation']='Three frozen implicit execution pairs and four mentions remain absent as records; prosaic content separate. D961stack kind is already owner-decided mention; no stale pending of that accepted component and no automatic semantic FN.'
    if o['id']=='SEM-007':o['reconciliation']='All124 assigned locator facets decided; not64stillunreviewed bounds. Preserve122 measurable envelope failures and2numeric-precision unresolved;116readable/6clipped-readable/2missingline. Wider graphical meaning/full-record facets not certified.'

summary=dict(inventory_positions_reconciled=207,inventory_occurrences_previously_compared_and_owner_decided=414,new_inventory_occurrences=0,
  expectation_ids_reconciled=74,expectation_variant_occurrences_reconciled=148,
  prior_local_scopes_accepted_per_answer=63,local_scope_denominator=66,old_local_pending_ids=['EXP-017','EXP-040','EXP-052'],
  prior_context_requirements_accepted_per_answer=3,context_denominator=8,old_context_pending_ids=['EXP-010','EXP-019','EXP-050','EXP-066','EXP-074'],
  old_pending_expectation_ids=state['pending_expectation_ids'],category_pairs_reconciled=277,prior_accepted_category_pairs=264,old_pending_category_pairs=13,
  category_counts=category_counts,prior_relation_scope_occurrences_reconciled=257,prior_locator_scope_occurrences_reconciled=124,
  wider_original_records_scope_accounted=218,old_issue_ids_reconciled=13,new_issues=0,new_rule_points=0,
  evaluator_reconciliation_complete=True,owner_reconciliation_status='waiting_review',new_reconciliation_package_available=True,
  inventory_owner_pending_occurrences=0,prior_decisions_not_reopened=True,
  full_semantic_metrics='not_assessable',whole_M_POC5A_closed=False,M_POC5B_executed=False,
  count_policy='Separate axes only.148EXP variants/414inventory scopes/277category pairs/257relations/124locators are not additive rule points. No new inventory or rule score in reconciliation.')
report=dict(id='M-POC5A.4d5-reconciliation-01',card='M-POC5A.4d5',status='partial_waiting_review',reviewer='Codex',human_reviewer=None,
  previous_state=ref(R/'current-state-29.json'),owner_decision=ref(R/'owner-decision-14.json'),owner_overlay=ref(R/'owner-review-overlay-14.json'),
  evaluation=state['evaluation'],responses=state['responses'],estimate=ref(M/'estimate.json'),scope_plan=state['inventory_scope_plan'],scope_pointer='/parts/4',
  method='Actual reconciliation of frozen ownership, prior exact decisions, original response fields and exclusions; old pending source/fields inspected manually. Hash validation only establishes lineage. Original accepted scopes preserved without re-scoring; no broader parent inference.',
  summary=summary,expectations=exp_rows,inventory=inv_rows,categories=category_rows,relations=relation_rows,locators=locator_rows,
  original_record_scope_boundaries=record_rows,issues=issue_rows,latest_limited_issue_dispositions=state['issue_dispositions'],
  missing_frozen_execution_pairs=['DEP-NEW-001','DEP-NEW-002','DEP-NEW-003'],missing_frozen_mentions=['DEP-034','DEP-035','DEP-043','DEP-067-1'],
  source_views_reinspected_in_this_reconciliation=[ref(P/f'source/review-evidence/pdf-{p}.png') for p in [32,33,34,35]],
  source_policy='Only supplied PDF31–37/previously supplied Step4. No fullPDF27 or new source acquisition; no new table/procedure or situation execution.',
  new_sources=0,new_extractions=0,new_corrections=0,new_gold=0,other_parts_executed=[],
  limitations=['Older8pending/13issues retained in remaining scopes. Exact source requirements do not provide actual map/scenario/rating/table.',
    'Listing/path discovery outside extractor allowlist confirmed; evaluation-content read not observed; assessment exposure/clean context unknown.',
    'Model/reasoning selectors, active time, tokens/cost/overall budget unknown; calendar time not active time.'])
save(OUT/'comparisons.json',report)
save(M/'validation.json',dict(exact_inventory_partition=True,all74expectations_joined_to_prior_comparison=True,all_accepted_owner_scopes_match_frozen_reviewed_scope=True,
  category_pairs=277,accepted_pairs=264,pending_pairs=13,all257proposed_edges_accounted=True,all124locator_scopes_accounted=True,
  raw_record_spans_verified=len(verified_traces),unique_raw_record_spans_verified=len(set(verified_traces)),summary=summary))

lines=['# M-POC5A.4d5 — końcowe uzgodnienie zakresów','',
 'Uzgodniono207 pozycji/414 wcześniejszych ocen inwentarza,74 oczekiwania w obu odpowiedziach,277 par rubryki,257 zakresów relacji,124 lokatorów i13 starych kwestii. To oddzielne osie, nie sumowane punkty reguł. Każdy wcześniejszy zakres zachowuje swoją decyzję; nowa akceptacja dotyczy tylko raportu uzgodnienia.',
 '', 'Pełne źródła, oryginalne pola i bajty: [comparisons.json](comparisons.json).','', '## Wszystkie74 oczekiwania','']
for x in exp_rows:
    lines += [f"### {x['id']} — {x['classification']}",'',x['reviewed_scope'],'',x['reconciliation'],'',
      'Wyłączenia: '+'; '.join(x['unreviewed_fields']+x['limits']), '']
    for run,d in x['runs'].items():
        lines += [f"**{run}: {d['reconciliation_result']}**. Wcześniejszy owner status: {d['prior_scoped_owner_status']}.",'',d['original_comparison'],'']
        for oid,t in d['exact_original_output_traces'].items():
            span=t['raw_span'];lines += [f"{oid}: `{t['pointer']}`, bajty[{span['start_byte']},{span['end_byte_exclusive']}); SHA `{span['sha256']}`."]
        lines += ['']
lines+=['## Wszystkie207 pozycje inwentarza','','| ID | First — dokładna wcześniejsza ocena | Context — dokładna wcześniejsza ocena |','|---|---|---|']
for x in inv_rows:lines.append(f"| {x['id']} | {x['runs']['first-001']['manual_assessment']} | {x['runs']['context-01']['manual_assessment']} |")
lines+=['','Wszystkie414 zakresów ma decyzje; nie całe poprawne rekordy. Pochodzenie, właściciel i dokładne wyłączenia prowadzą wskazane owner-overlay pointers w JSON.','', '## Wszystkie277 par rubryki','','| Para | Wcześniejsza decyzja | Ograniczenie |','|---|---|---|']
for x in category_rows:lines.append(f"| {x['id']} | {x['per_answer_prior_status']['first-001']} — oba wyniki | Tylko {x['expectation_id']} reviewed_scope; bez nowego punktu |")
lines+=['','264 wcześniejsze pary przyjęte;13 nadal pending dla EXP-017/040/052. To te same pary w każdej odpowiedzi, nie554 reguły.','', '## Stare kwestie i późniejsze decyzje','']
for x in issue_rows:lines += [f"### {x['id']}",'',x['original_proposal'],'',x['reconciliation'],'', 'Późniejsza dyspozycja: '+str(x['latest_limited_disposition']),'']
lines += ['## Pozostałe granice','','W JSON rozliczono wszystkie257 oryginalnych krawędzi z wcześniejszymi accepted/excluded components,124 lokatory i218 oryginalnych rekordów reguł/węzłów. Nie nadano im pełnej akceptacji z powodu pokrycia inwentarza. Brakujące3 pary wykonawcze/4wzmianki zachowane, bez autoFN;105 niepotwierdzonych kandydatów nie staje się gold.','',
 'Nowe punkty reguł/inwentarza:0. Nowe błędy:0 w raporcie uzgodnienia — nie jest to globalne zero błędów odpowiedzi. Uzgodnienie czeka na właściciela; po nim osobne M-POC5B20 sytuacji/40 ocen.']
md(OUT/'comparisons.md','\n'.join(lines))
save(OUT/'issues.json',dict(id='M-POC5A.4d5-issues-01',new_issues=[],inherited_open_issues=issue_rows,
  prior_limited_issue_dispositions=state['issue_dispositions'],old_pending_expectations=state['pending_expectation_ids'],
  reconciliation_status='waiting_review',new_semantic_errors_confirmed=0,global_zero_errors_claimed=False))
save(OUT/'presentation.json',dict(id='M-POC5A.4d5-presentation-01',status='waiting_review',summary=summary,
  recommendations=[dict(id='REC-4D5-01',proposal='Accept completed exact reconciliation and transfer to separately estimated M-POC5B with8oldpending/13oldissues and explicit source blocks retained.',
    scope='No new inventory/rule scores, no full record or full precision/recall, no old variant choice.')],
  comparison_files=[ref(OUT/'comparisons.json'),ref(OUT/'comparisons.md')],owner_file_open_or_read='unknown',
  prior_inventory_compared_available_decided_pending={'compared':414,'available':414,'decided':414,'pending':0},
  new_reconciliation_package={'compared':1,'available':1,'owner_decided':0,'pending':1}))
md(OUT/'review.md','''# M-POC5A.4d5 — uzgodnienie wykonane

Wykonano cały przydział części5:207 pozycji i414 wcześniejszych ocen inwentarza,74 oczekiwania w obu hashach,277 par rubryki,13 starych kwestii i granice pozostałych pól. Dodatkowo rozliczono257 wcześniej ocenionych krawędzi,124 lokatory oraz218 oryginalnych rekordów reguł/węzłów. Odczytano źródła/pola ośmiu starych pending i rozdzielono aktualne przyjęte aspekty od otwartych reszt. Nie jest to sam rejestr oczekiwania: każda pozycja ma konkretny wniosek, dokładną podstawę i wyłączenia.

Owner-decision14 zapisuje zatwierdzenie82 ocen .4d4 (80wsparcia/2mieszane SEM-022), razem414 wcześniejszych zakresów inwentarza z decyzjami. Uzgodnienie nie tworzy nowych punktów. Po63/66 zakresy lokalne i3/8 wymagania źródła przyjęte;8 oczekiwań nadal otwartych.264/277 par rubryki zachowane,13pending dla3lokalnych kwestii. Pełne metryki nadal not_assessable.

[Porównania](comparisons.md) · [Pełne ślady](comparisons.json) · [Opis po ludzku](owner-focus.md).

Propozycja: przyjąć dokładne rozliczenie i przekazać podstawę do osobnego M-POC5B, z jawnymi ograniczeniami. Raport uzgodnienia waiting_review, wcześniejszych414 decyzji nie cofnięto. M-POC5A/.4/.4d partial; nie ogłoszono pełnej poprawności lub końca etapu5. M-POC5B40 ocen nie wykonano. Bez nowych źródeł, ekstrakcji, korekt lub gold. Szacunek65–85min zapisano przed pracą; aktywne czasy/budżet unknown.
''')
print('Reconciled207inventory/74expectations/277rubricpairs/13issues; retained414inventory decisions and8oldpending. Verified',len(verified_traces),'raw record spans.')
