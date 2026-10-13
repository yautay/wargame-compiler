"""Before semantic review: preserve history, bounded assent, exhaustive allocation."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';D=ROOT/'docs';PACK=R/'part-04c3'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();C=load(R/'checklist.json');prior=load(R/'current-state-20.json');packet=load(PACK/'comparisons.json');pres=load(PACK/'presentation.json')
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
save(M/'start.json',dict(card='M-POC5A.4d1',recorded_at_utc=now,protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),prior_state=ref(R/'current-state-20.json'),
    estimate_before_semantic_review=dict(whole_4d_minutes_range=[300,420],whole_4d_fits_single90min_session=False,first_part_minutes_range=[70,85],assigned_inventory_ids=39,assigned_occurrences=78,further_split_before_execution=True,includes_previous_locator_assent=True),
    active_time='unknown',model_selector='unknown',reasoning_selector='unknown'))
for x in [C['source'],C['evaluation'],*C['responses'].values(),*load(PACK/'manifest.json')['artifacts']]:assert ref(ROOT/x['path'])==x
reply='Zatwierdzam i kontynuuj'
save(M/'approval-evidence.json',dict(owner_reply_verbatim=reply,recorded_at_utc=now,owner_message_sent_at_utc='unknown',actual_owner_file_open_or_read='unknown',
    interpretation='Explicit approval of immediately presented .4c3:38 source/geometry and retained envelope failures,36 readable rasters,2E1011 clipped but readable. No old unresolved meaning chosen. Continue next.4d after estimate/split.',presented_decisions=pres['decisions'],basis=[ref(PACK/'owner-focus.md'),ref(PACK/'presentation.json')]))
reviewer='owner in this chat; personal identity unknown';scopes=[]
for i,row in enumerate(packet['locators']):
    j=dict(id=row['id'],source_scope=row['source_scope'],source_quote_original=row['source_quote_original'],independent_source_helper=row['independent_source_helper'],source_image=row['source_image'],diagnostic_artifact=row['diagnostic_artifact'],diagnostic_pointer=row['diagnostic_pointer'],
        manual_assessment=row['manual_assessment'],evaluator_comparison=row['manual_comparison'],status='reviewed',reviewer=reviewer,recorded_at_utc=now,
        accepted_facets=dict(valid_geometry=True,quote_supported_in_supplied_source=True,strict_whole_glyph_containment=row['strict_full_quote_glyph_envelope'],raster_result=row['raster_short_quote']),
        whole_evidence_record_accepted=False,original_locator_repaired=False,exclusions=row['exclusions'],uncertainties=row['uncertainties'],runs={})
    for run,x in row['runs'].items():
        j['runs'][run]=dict(response=C['responses'][run],reviewer=reviewer,status='reviewed',result='owner_accepted_bounded_locator_assessment',comparison_artifact=ref(PACK/'comparisons.json'),comparison_pointer=f'/locators/{i}/runs/{run}',
            output_trace=copy.deepcopy(x['output_trace']),geometry=x['geometry'],quote_location=x['quote_location'],raster_review=x['raster_review'],comparison=x['comparison'],inherited_report_observations=x['inherited_report_observations'],exclusions=x['exclusions'],original_locator_repaired=False,whole_record_accepted=False)
    scopes.append(j)
disposition={'SEM-007':'Owner accepted all124 assigned short-quote locator assessments in bounded facets:122 measurable envelope failures,2E962 numericprecision unresolved;116 readable without observed ink loss,6clipped but readable,2E916 missingline. Source/geometry124. Original defects retained; wider evidence/glyph/whole-content review not certified.'}
decision=dict(id='M-POC5A-owner-decision-10',card='M-POC5A',part='M-POC5A.4c3',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,reviewer=reviewer,owner_reply_verbatim=reply,
    decision='accepted_presented38_bounded_locator_assessments',approval_evidence=ref(M/'approval-evidence.json'),prior_decision=ref(R/'owner-decision-09.json'),prior_state=ref(R/'current-state-20.json'),comparison_manifest=ref(PACK/'manifest.json'),focused_packet=ref(PACK/'owner-focus.md'),
    evaluation=C['evaluation'],responses=C['responses'],source=C['source'],recommendations=pres['decisions'],scopes=scopes,newly_reviewed_locator_occurrences=38,per_answer={'first-001':16,'context-01':22},valid_geometry=38,
    strict_quote_glyph_envelope_passes=0,strict_quote_glyph_envelope_failures=38,readable_raster_without_observed_ink_loss=36,readable_with_descenders_clipped=2,missing_final_quote_line=0,issue_disposition=disposition,
    unresolved_prior_issue_ids=prior['unresolved_issue_ids'],pending_expectation_ids=prior['pending_expectation_ids'],count_policy='38 distinct occurrence judgments with overlapping facets; not38 good whole records or semanticTP.',
    owner_file_open_or_read='unknown',metrics='not_assessable',excluded=pres['excludes'],no_response_changes=True,no_gold_change=True,no_new_sources=True,whole_card_closed=False)
save(R/'owner-decision-10.json',decision);dr=ref(R/'owner-decision-10.json');oldo=load(R/'owner-review-overlay-09.json');o=copy.deepcopy(oldo)
o.update(id='M-POC5A-owner-review-overlay-10',decision=dr,prior_overlay=ref(R/'owner-review-overlay-09.json'),locator_owner_decision=dr,owner_reviewed_locator_scoped_occurrences=124,
    all_locator_review='All124 assigned short-quote occurrences owner-reviewed in exact bounded facets; no whole-evidence/content certificate.',locator_count_policy=decision['count_policy'])
o['issue_dispositions'].update(disposition)
for run,v in o['runs'].items():
    v['locator_scopes'] += [dict({k:z for k,z in j.items() if k!='runs'},response=C['responses'][run],decision=dr,trace=j['runs'][run]) for j in scopes if run in j['runs']]
    v['owner_reviewed_locator_scoped_occurrences']=59 if run=='first-001' else 65;v['assigned_remaining_unreviewed_locator_occurrences']=0
save(R/'owner-review-overlay-10.json',o)
(R/'owner-review-summary-10.md').write_text('# Zatwierdzenie .4c3\n\nWłaściciel: „'+reply+'”. Przyjęto38 ocen: źródło/geometria oraz38 naruszeń obwiedni;36 krótkich rastrów czytelnych bez utraty tuszu,2E1011 czytelne z przyciętym p/Q. Łącznie124 przypisane oceny, osobno59/65. To nie124 dobre lokatory lub pełne poprawne rekordy. Dawne wady pozostają w oryginałach,2E962 nadal nieocenialne z powodu precyzji. Starsze nierozstrzygnięcia/8oczekiwań bez zmiany. Następna.4d podzielona przed wykonaniem; pierwsza.4d1 39pozycji/78wystąpień.\n',encoding='utf-8')
types={'chapter_heading','section_heading','note','note_text_span','example'};first=[x['id'] for x in C['inventory'] if x['type'] in types];assert len(first)==39
parts=[dict(card='M-POC5A.4d1',inventory_ids=first,description='Headings/notes/exact note spans/examples; literal content and interpretation separately',minutes_range=[70,85])]
for n,pages in [(2,[31,32,33]),(3,[34,35]),(4,[36,37])]:
    ids=[x['id'] for x in C['inventory'] if x['id'] not in first and x['frozen_item']['evidence'][0]['pdf_page'] in pages]
    parts.append(dict(card=f'M-POC5A.4d{n}',inventory_ids=ids,pdf_pages=pages,description='Rule labels,clauses,exact child spans and supplied graphics/continuations in assigned area; old reviewed facets retained',minutes_range=[70,90]))
parts.append(dict(card='M-POC5A.4d5',inventory_ids=[],description='Reconciliation of all207 positions,66local/8context expectations,277rubric units,old issues and excluded field scopes; no forced closure or autoacceptance',expectation_ids=[x['id'] for x in C['expectations']],issue_ids=prior['unresolved_issue_ids'],rubric_unit_count=len(C['category_units']),minutes_range=[50,75]))
allids=[i for x in parts for i in x['inventory_ids']];assert len(allids)==len(set(allids))==207 and set(allids)=={x['id'] for x in C['inventory']}
for x in parts:x.update(inventory_positions=len(x['inventory_ids']),inventory_occurrences=len(x['inventory_ids'])*2,semantic_review_executed=False)
save(M/'scope-plan.json',dict(id='M-POC5A.4d-scope-plan-01',recorded_at_utc=now,before_semantic_review=True,evaluation=C['evaluation'],responses=C['responses'],inventory=ref(P/'evaluation/eval-v1/inventory.json'),
    whole_scope_estimate_minutes_range=[300,420],basis='207 precise inventory occurrences per variant include child scopes, broader fields and graph/graphic material; earlier scoped acceptance is not whole-node approval.',parts=parts,
    exhaustive_disjoint_inventory_ids=True,reconciliation_part_revisits_prior_facets_without_new_points=True,only_part_executed_this_session='M-POC5A.4d1',further_split_before_execution_if_estimate_exceeds90=True,no_new_gold=True))
s=copy.deepcopy(prior);s.update(id='M-POC5A-current-state-21',part='M-POC5A.4c3-owner-review_and4d-split',previous_state=ref(R/'current-state-20.json'),decision=dr,overlay=ref(R/'owner-review-overlay-10.json'),locator_owner_decision=dr,new_owner_decisions=[dr],
    part_4c3_owner_review_complete=True,locator_owner_pending_compared_occurrences=0,locator_owner_reviewed_occurrences=124,all_assigned_locator_owner_scoped_review_complete=True,
    next_part='M-POC5A.4d1',inventory_scope_plan=ref(M/'scope-plan.json'),inventory_evaluator_compared_assigned_occurrences=0,inventory_remaining_assigned_occurrences=414,
    next_action='Execute only.4d1 assigned39inventory positions/78occurrences after70–85min estimate. Remainingparts168positions plusreconciliation preserved; old meaning unresolved. M-POC5B separate.',
    resume='Owner10 accepted38 last locator facets. All124 assigned scoped reviewed, no full-record certificate.4d split before review into39 plus three pagegroups and reconciliation; first.4d1.')
s['issue_dispositions'].update(disposition);s['summary'].update(new_owner_reviewed_occurrences=38,owner_pending_occurrences=0,owner_accepted_scoped_occurrences=38)
save(R/'current-state-21.json',s)
save(M/'owner-decision-artifacts.json',dict(artifacts=[ref(R/f) for f in ['owner-decision-10.json','owner-review-overlay-10.json','current-state-21.json','owner-review-summary-10.md']]))
paths=[ROOT/x['path'] for x in load(P/'measurement/M-POC5A-semantic-04c3/read-inputs.json')['files']]+[R/'current-state-20.json',R/'current-state-21.json',R/'owner-decision-10.json',R/'owner-review-overlay-10.json',PACK/'comparisons.json',PACK/'manifest.json',D/'handoff/2026-10-11-M-POC5A-semantic-04c3.md',D/'work/tasks/semantic/M-POC5A.4d.md']
paths=list(dict.fromkeys(paths))
for path in paths:
    b=path.read_bytes();json.loads(b) if path.suffix=='.json' else b.decode('utf-8-sig')
save(M/'read-inputs.json',dict(files=[ref(p) for p in paths],method='Full bytes read/JSON parsed for required inputs. Semantic reading/manual comparison recorded separately.'))
public=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/README.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4c','.4c3','.4d']]]
save(M/'public-documents-before.json',[ref(p) for p in public])
for part in parts:
    path=D/f"work/tasks/semantic/{part['card']}.md";assert not path.exists()
    path.write_text(f"# {part['card']}: Przegląd inwentarza — część{part['card'][-1]}\n\n- **ID:** {part['card']}\n- **Milestone:** M-POC5\n- **Rola:** Przegląd wspólny; akceptuje właściciel\n- **Zależności:** [M-POC5A.4d](M-POC5A.4d.md), najnowszy current-state\n\n## Zakres i wejścia\n\nDokładny rozłączny przydział PRZED oceną: private/poc/spqr-chapter9/measurement/M-POC5A-semantic-04d1/scope-plan.json. {part['inventory_positions']}pozycji/{part['inventory_occurrences']}wystąpień inwentarza; część5 rozlicza całość bez dodatkowych punktów. Bootstrap/playbook/STATUS/HANDOFF/ROADMAP/POC-PLAN/ADR-0039, kartyM-POC5A/.4/.4d, oryginalny checklist i oba run/proposal/provenance/report, niezmienny eval-v1 oraz latest state/decision/overlay.\n\n## Wykonanie i granice\n\nOsobne rzeczywiste porównania źródła i każdego właściwego child span oraz odpowiedzi obu hashów. Literalna treść/interpretacja, wcześniej przyjęty zakres/szersze nieprzejrzane pola osobno. Nie nadawać akceptacji przez mapped-parent. Zachować8starych oczekiwań/kwestie i braki źródeł. Szacunek{part['minutes_range'][0]}–{part['minutes_range'][1]}minut; limit90, dalszy podział przed wykonaniem jeśli potrzebny. Wykonać jedną część w sesji, nie sam rejestr pending.\n\n## Artefakty i kontrole\n\nNowy prywatny part-04d{part['card'][-1]}/:comparisons/review/issues/owner-focus/presentation/manifest. Additive current-state, nowy pomiar, sessions.jsonl append-only. Właściciel przyjmuje pokazany zakres; brak decyzji waiting_review. scripts/check.ps1 offline, lokalneTMP/TEMP i nowybasetemp, git diff --check, logi i audyt niezmienności.\n\n## Wyłączenia i przekazanie\n\nInne części/M-POC5B20sytuacji, nowe źródła/ekstrakcja/korekty/API inferencji, commit/push i architektura. Pełne metryki bez sprawdzonych mianowników not_assessable, gold bez zmiany. Nadrzędne karty partial, M-POC5 jedyny next; następna osobna część po decyzjach obecnej.\n",encoding='utf-8')
planning='\n\n## Podział .4d przed wykonaniem — 2026-10-11\n\nWłaściciel zatwierdził38 ograniczonych ocen .4c3; razem124 przypisane oceny lokatorów. Nie zaakceptowano całych rekordów lub dawnych nierozstrzygnięć. Pełną .4d oszacowano300–420minut i podzielono przed review: '+', '.join(f"[{x['card']}]({x['card']}.md):{x['inventory_positions']}pozycji" for x in parts)+'. Dokładne listy207ID i przydział rozliczenia w nowym prywatnym scope-plan. W tej sesji tylko.4d1:39pozycji/78wystąpień,70–85minut; następne części osobno, dalszy podział przed wykonaniem jeśli potrzebny.8dawnych oczekiwań/kwestie zachowane.\n'
for path in [D/'work/tasks/semantic/M-POC5A.4d.md',D/'work/tasks/semantic/M-POC5A.4.md'] :path.write_text(path.read_text(encoding='utf-8').rstrip()+planning,encoding='utf-8')
# Parent .4 links live alongside new subcards; links from .4d planning are correct.
for name in ['STATUS.md','ROADMAP.md']:
    path=D/name;text=path.read_text(encoding='utf-8');text+='\n## Plan .4d przed przeglądem — 2026-10-11\n\nPięć osobnych części: '+', '.join(f"[{x['card']}](work/tasks/semantic/{x['card']}.md) {x['inventory_positions']}pozycji" for x in parts)+'. Całość300–420minut; pierwsza39pozycji/78wystąpień70–85minut. ExactIDs prywatnie, dalszy podział przed wykonaniem jeśli potrzebny; nadrzędne karty partial, M-POC5 jedyny next.\n';path.write_text(text,encoding='utf-8')
path=D/'work/tasks/README.md';path.write_text(path.read_text(encoding='utf-8').rstrip()+'\n\nPodział inwentarza M-POC5A.4d: '+', '.join(f"[{x['card']}](semantic/{x['card']}.md)" for x in parts)+'. Dokładne przydziały przygotowane przed oceną, jedna część na sesję.\n',encoding='utf-8')
save(M/'planning-public-documents.json',[ref(D/name) for name in ['STATUS.md','ROADMAP.md','work/tasks/README.md','work/tasks/semantic/M-POC5A.4.md','work/tasks/semantic/M-POC5A.4d.md']]+[ref(D/f"work/tasks/semantic/{x['card']}.md") for x in parts])
print(json.dumps(dict(owner_locator_total=124,inventory_parts=[(x['card'],x['inventory_positions']) for x in parts],protected=len(protected))))
