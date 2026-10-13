"""Record bounded owner assent and partition locator scope BEFORE review."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';D=ROOT/'docs';PACK=R/'part-04b3'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();C=load(R/'checklist.json');prior=load(R/'current-state-14.json');pres=load(PACK/'presentation.json');packet=load(PACK/'comparisons.json');reply='ok kontynuuj'
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
save(M/'start.json',dict(card='M-POC5A.4c1',recorded_at_utc=now,protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),prior_state=ref(R/'current-state-14.json'),
    estimate_before_locator_review=dict(full_part_minutes=[160,220],first_part_minutes=[70,85],first_part_ids=22,first_part_occurrences=44,split_required=True,includes_bounded_prior_owner_decision_record=True),
    active_time='unknown',model_selector='unknown',reasoning_selector='unknown'))
for a in [C['source'],C['evaluation'],*C['responses'].values(),*load(PACK/'manifest.json')['artifacts']]:assert ref(ROOT/a['path'])==a
recommendations=[
 dict(number=1,ids=pres['positive_scope']['ids'],occurrences=68,decision='Accept68 individually bounded relation roles/source requirements; missing target content, whole records and old pending excluded.',includes=pres['positive_scope']['includes'],excludes=pres['positive_scope']['excludes']),
 dict(number=2,ids=['D951terrain'],occurrences=2,issue='SEM-018',decision='Normal terrain cost requirement explicit; specific chart/table-use target inferred, not literal explicit chart reference. Actual cost/chart/alias not accepted.'),
 dict(number=3,ids=['D961stack'],occurrences=2,issue='SEM-019',decision='Summary lookup not execution prerequisite. Local statements readable without summary; full actual stacking legality with unsupplied exceptions still conditionally blocked. Prior mention-kind SEM-015 unchanged, not reaccepted.')]
save(M/'approval-evidence.json',dict(owner_reply_verbatim=reply,recorded_at_utc=now,owner_message_sent_at_utc='unknown',actual_owner_file_open_or_read='unknown',
    interpretation='ok assents to the three immediately presented bounded recommendations; kontynuuj authorizes next review. No approval of earlier unresolved choices/whole records.',recommendations=recommendations,
    basis=[ref(PACK/'owner-focus.md'),ref(PACK/'presentation.json'),ref(PACK/'issues.json')]))
reviewer='owner in this chat; personal identity unknown';scopes=[]
for index,row in enumerate(packet['relationships']):
    num=2 if row['id']=='D951terrain' else 3 if row['id']=='D961stack' else 1
    j=copy.deepcopy({k:v for k,v in row.items() if k not in ['runs','human_status','human_reviewer']})
    j.update(status='reviewed',reviewer=reviewer,recorded_at_utc=now,owner_recommendation_number=num,
        result={1:'correct_in_individually_bounded_requirement_scope',2:'cost_requirement_supported_explicit_chart_kind_not_supported',3:'summary_necessity_and_block_scope_qualified_prior_kind_preserved'}[num],
        accepted_components=recommendations[num-1],excluded_components=pres['positive_scope']['excludes'],whole_record_accepted=False,full_dependent_result_accepted=False,runs={})
    for run,x in row['runs'].items():
        j['runs'][run]=dict(response=C['responses'][run],reviewer=reviewer,status='reviewed',result=j['result'],comparison_artifact=ref(PACK/'comparisons.json'),comparison_pointer=f'/relationships/{index}/runs/{run}',
            edge_trace=copy.deepcopy(x['output_trace'][row['id']]),endpoint_traces={rid:dict(response=q['response'],pointer=q['pointer'],raw_span=q['raw_span']) for rid,q in x['output_trace'].items()},
            target_identity=x['target_identity'],direction=x['direction'],kind=x['kind'],explicitness=x['explicitness'],missing_target_impact=x['missing_target_impact'],exclusions=x['exclusions'],uncertainties=x['uncertainties'],whole_record_accepted=False,full_result_accepted=False)
    scopes.append(j)
dispositions={
 'SEM-018':'Resolved only for explicit normal-cost requirement versus inferred chart/table-use target; no actual chart/cost or full result accepted.',
 'SEM-019':'Resolved only for summary necessity/impact; local summary not execution prerequisite, actual stacking exceptions still missing. Prior SEM-015 kind retained.'}
decision=dict(id='M-POC5A-owner-decision-07',card='M-POC5A',part='M-POC5A.4b3',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,reviewer=reviewer,owner_reply_verbatim=reply,
    decision='accepted_three_presented_bounded_recommendations_68_plus2_plus2',approval_evidence=ref(M/'approval-evidence.json'),prior_decision=ref(R/'owner-decision-06.json'),prior_state=ref(R/'current-state-14.json'),
    comparison_manifest=ref(PACK/'manifest.json'),presentation=ref(PACK/'presentation.json'),focused_packet=ref(PACK/'owner-focus.md'),evaluation=C['evaluation'],responses=C['responses'],source=C['source'],recommendations=recommendations,scopes=scopes,
    newly_decided_assigned_occurrences=72,per_answer={'first-001':36,'context-01':36},positive_bounded_occurrences=68,qualified_occurrences=4,prior_owner_decided_assigned_scopes_preserved=185,owner_decided_assigned_scopes_total=257,
    remaining_assigned_scopes_without_owner_decision=0,prior_kind_D961stack_preserved=True,issue_disposition=dispositions,unresolved_prior_issue_ids=prior['inherited_issue_ids'],pending_expectation_ids=prior['pending_expectation_ids'],
    excluded=pres['positive_scope']['excludes'],owner_file_open_or_read='unknown',metrics='not_assessable',no_response_changes=True,no_gold_change=True,whole_card_closed=False)
save(R/'owner-decision-07.json',decision);dr=ref(R/'owner-decision-07.json');old=load(R/'owner-review-overlay-06.json');overlay=copy.deepcopy(old)
overlay.update(id='M-POC5A-owner-review-overlay-07',decision=dr,prior_overlay=ref(R/'owner-review-overlay-06.json'),relationship_owner_decision=dr,prior_relationship_owner_decision=old['relationship_owner_decision'],
    accepted_relation_scoped_occurrences=257,newly_decided_scoped_occurrences_4b3=72,positive_bounded_occurrences_4b3=68,qualified_occurrences_4b3=4,pending_prior_issue_ids=decision['unresolved_prior_issue_ids'],pending_relation_ids_4b3=[],
    all_output_edges_review='257 assigned occurrences have individually bounded component decisions; not257 whole correct edges. Original flags and earlier missing frozen pairs/excluded fields preserved.',
    relation_scope_policy=dict(previous_policy=old['relation_scope_policy'],part_4b3_presentation=pres,decision=dr,count_policy='257 scoped judgments, no whole-record acceptance/final metrics.'))
overlay['issue_dispositions'].update(dispositions)
for j in scopes:
    if j['owner_recommendation_number']>1:overlay['relation_facet_decisions'].append(dict(id='SEM-018' if j['owner_recommendation_number']==2 else 'SEM-019',edge=j['id'],decision=dr,assessment=j['accepted_components'],source_scope=j['source_scope'],target_scope=j['target_scope'],runs=j['runs']))
for run,v in overlay['runs'].items():
    for j in scopes:v['relationship_scopes'].append(dict({k:x for k,x in j.items() if k!='runs'},response=C['responses'][run],decision=dr,trace=j['runs'][run]))
    v.update(accepted_relation_scoped_occurrences=len(v['relationship_scopes']),assigned_relation_occurrences_4b3=36,pending_relation_occurrences_4b3=0,remaining_without_owner_relation_scope=0)
assert len(overlay['runs']['first-001']['relationship_scopes'])==126 and len(overlay['runs']['context-01']['relationship_scopes'])==131
save(R/'owner-review-overlay-07.json',overlay)
state=copy.deepcopy(prior);state.update(id='M-POC5A-current-state-15',part='M-POC5A.4b3-owner-review',previous_state=ref(R/'current-state-14.json'),decision=dr,overlay=ref(R/'owner-review-overlay-07.json'),
    owner_accepted_relationship_occurrences=257,owner_decided_assigned_relationship_occurrences=257,owner_pending_relationship_occurrences=0,owner_pending_relationship_occurrences_4b3=0,new_owner_decisions=[dr],newly_decided_assigned_occurrences=72,
    part_4b3_owner_review_complete=True,unresolved_issue_ids=decision['unresolved_prior_issue_ids'],next_part='M-POC5A.4c1',next_action='Execute first pre-partitioned locator part .4c1 after estimate; keep earlier pending/excluded fields.',
    owner_accepted_relationship_occurrences_policy='257 assigned scoped decisions:185 prior plus68 bounded requirements+2cost/chart classification+2summary impact; notwholecorrectedges.',
    owner_pending_relationship_occurrences_policy='No pending newly presented assigned .4b scopes; excluded fields, old missing frozen pairs and older pending not closed.',
    resume='Owner accepted three .4b3 recommendations68+2+2. Next .4c1 first partition; earlier8expectations/SEM-001–013 and full relation/locator review still incomplete.')
state['issue_dispositions'].update(dispositions);state['summary'].update(new_owner_reviewed_occurrences=72,owner_pending_occurrences=0,owner_accepted_scoped_occurrences=72,owner_decided_assigned_scopes_total=257)
save(R/'current-state-15.json',state)
(R/'owner-review-summary-07.md').write_text('''# Zatwierdzenie trzech rekomendacji .4b3

Właściciel odpowiedział „ok kontynuuj” po trzech konkretnych rekomendacjach.
Zapisano zgodę na68 ograniczonych ocen relacji/wymagań,2 oceny rozróżnienia
jawnego kosztu od wnioskowanego celu tabeli oraz2 oceny konieczności/blokady
podsumowania stosów. D961stack pozostaje mention według poprzedniej decyzji;
nie jest ponownie oceniany jako nowy komponent rodzaju.

Nowe owner-decision-07, overlay-07 i current-state-15 zachowują oryginalne
odpowiedzi, flagi i wcześniejsze decyzje. SEM-018/019 rozstrzygnięto tylko
w przedstawionych zakresach. Wcześniejsze185 zakresów zachowano; razem257
przypisanych wystąpień ma decyzje o komponentach, nie257 poprawnych całych
relacji. Osiem wcześniejszych oczekiwań iSEM-001–013 w pozostałych zakresach,
wyłączone pola, brakujące pary, pełne wyniki i lokatory pozostają otwarte.
Gold i pełne metryki bez zmiany. Faktyczny odczyt plików unknown.

„Kontynuuj” zezwala na następny przegląd .4c po podziale i oszacowaniu.
''',encoding='utf-8')
first=[x['evidence_id'] for x in C['locator_review']['first-001'] if x['original_evidence']['original_record']['pdf_page']<=33]
second=[x['evidence_id'] for x in C['locator_review']['first-001'] if x['original_evidence']['original_record']['pdf_page'] in [34,35]]
third=[x['evidence_id'] for x in C['locator_review']['context-01'] if x['original_evidence']['original_record']['pdf_page'] in [36,37,27]]
assert len(first)==22 and len(second)==21 and len(third)==22
parts=[]
for n,ids,counts,minutes in [(1,first,{'first-001':22,'context-01':22},[70,85]),(2,second,{'first-001':21,'context-01':21},[60,80]),(3,third,{'first-001':16,'context-01':22},[60,85])]:
    parts.append(dict(card=f'M-POC5A.4c{n}',evidence_ids=ids,per_answer=counts,occurrences=sum(counts.values()),estimate_minutes=minutes,status='assigned_before_review'))
for run,items in C['locator_review'].items():
    actual=[i for part in parts for i in part['evidence_ids'] if any(x['evidence_id']==i for x in items)]
    assert len(actual)==len(set(actual))==len(items) and set(actual)=={x['evidence_id'] for x in items}
plan=dict(id='M-POC5A.4c-scope-plan-01',created_at_utc=datetime.now(timezone.utc).isoformat(),before_locator_review=True,basis=ref(R/'checklist.json'),responses=C['responses'],source=C['source'],evaluation=C['evaluation'],
    count_policy='65 distinct evidence IDs:58 shared boundary cases+E916 shared+6new context-only =124 occurrences59/65. Assignment from metadata is not locator assessment.',full_estimate_minutes=[160,220],parts=parts,actual_locator_review_executed=False)
save(M/'scope-plan.json',plan)
required=[ROOT/'CLAUDE.md',D/'SESSION-PLAYBOOK.md',D/'STATUS.md',D/'HANDOFF.md',D/'handoff/2026-10-11-M-POC5A-semantic-04b3.md',D/'ROADMAP.md',D/'POC-PLAN.md',D/'adr/ADR-0039-archiwum-i-poc-przed-architektura.md',D/'work/tasks/M-POC5A.md',D/'work/tasks/semantic/M-POC5A.4.md',D/'work/tasks/semantic/M-POC5A.4c.md',R/'checklist.json',R/'current-state-15.json',R/'owner-decision-07.json',R/'owner-review-overlay-07.json']
for run in C['responses']:
    required += [P/f'runs/{run}/{f}' for f in ['run.json','session-evidence.txt']]+[P/f'proposals/{run}/{f}' for f in ['proposal.json','provenance.json']]+[P/f'reports/{run}/{f}' for f in ['report.md','errors.json','inventory.json','metrics.json','dependency-comparison.json','manifest.json','closure.json']]
required += [P/'evaluation/eval-v1'/f for f in ['expectations.json','inventory.json','dependencies.json','measurement-policy.json','manifest.json']]
required += [P/f for f in ['source/source-v1.json','inputs/v1/manifest.json','context/pass-01/manifest.json','context/pass-01/freeze-v1.json','transfer/context-v1/context/pass-01/manifest.json','measurement/M-POC3-first-001/bbox-analysis.json']]
for p in required:
    b=p.read_bytes();json.loads(b) if p.suffix=='.json' else b.decode('utf-8-sig')
save(M/'read-inputs.json',dict(files=[ref(p) for p in required],method='Full bytes read/JSON parsed; individual locator source/visual review separately recorded. Reading is not acceptance.'))
save(M/'owner-decision-artifacts.json',dict(artifacts=[ref(R/f) for f in ['owner-decision-07.json','owner-review-overlay-07.json','current-state-15.json','owner-review-summary-07.md']]))
public=[D/'STATUS.md',D/'ROADMAP.md',D/'work/tasks/M-POC5A.md',D/'work/tasks/semantic/M-POC5A.4.md',D/'work/tasks/semantic/M-POC5A.4b.md',D/'work/tasks/semantic/M-POC5A.4b3.md',D/'work/tasks/semantic/M-POC5A.4c.md',D/'work/tasks/README.md',D/'HANDOFF.md']
save(M/'public-documents-before.json',[ref(p) for p in public])
aggregate='''Właściciel zatwierdził trzy dokładne rekomendacje .4b3:68 ograniczonych
ocen i4 wystąpienia dwóch osobnych kwestii. Owner-decision-07/overlay-07
oraz current-state-15 zachowują poprzednie185 zakresów; razem257
przypisanych wystąpień ma decyzje o komponentach, nie całych rekordach.
SEM-018/019 rozstrzygnięte tylko w przedstawionych zakresach. Osiem
wcześniejszych oczekiwań, SEM-001–013 i wyłączone pola nadal otwarte.

Przed review .4c podzielono124 wystąpienia lokatorów (59/65) na trzy
rozłączne części: .4c1 22ID/44 wystąpienia, .4c2 21ID/42, .4c3 22ID/38.
Szacunek całości160–220 minut; pierwsza część70–85. W tej sesji wykonywana
wyłącznie .4c1. Pozostałe przypisane, bez oceny z samych metadanych.
M-POC5A/.4/.4b/.4c partial, M-POC5 jedyny next. Bez ekstrakcji/korekt,
nowych źródeł, czatów, commit/push. Prywatny pomiar i scope-plan:
measurement/M-POC5A-semantic-04c1/.
'''
for p in public[2:7]:p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Decyzja .4b3 i podział .4c przed wykonaniem — 2026-10-11\n\n'+aggregate,encoding='utf-8')
for part in parts:
    p=D/f"work/tasks/semantic/{part['card']}.md";assert not p.exists()
    p.write_text(f'''# {part['card']}: Lokatory — część{part['card'][-1]}

- **ID:** {part['card']}
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; znaczenie akceptuje właściciel
- **Zależności:** [M-POC5A.4c](M-POC5A.4c.md), najnowszy current-state.

## Cel i wejścia

Rzeczywisty przegląd {len(part['evidence_ids'])} przypisanych lokatorów /
{part['occurrences']} wystąpień ({part['per_answer']['first-001']}/{part['per_answer']['context-01']}). Pełna lista ID w prywatnym
measurement/M-POC5A-semantic-04c1/scope-plan.json, przygotowanym przed oceną.
Bootstrap, playbook, STATUS/HANDOFF i latest handoff, ROADMAP/POC-PLAN,
ADR-0039, karty M-POC5A/.4/.4c; oba oryginały, proposal/provenance/report,
checklist, latest current-state/owner-decision/overlay i niezmieniony eval-v1.

## Wymagane działania i granice

Sprawdzić osobno geometrię/hash obrazu, lokalizację całego krótkiego cytatu,
granice pełnych glifów, widoczne pocięcie znaków, czytelność i treść. Użyć
istniejących dostarczonych obrazów; dla PDF27 wyłącznie suppliedStep4crop.
Literalny cytat oddzielić od interpretacji; ślad do bajtów obu odpowiedzi.
Nie poprawiać bbox/cytatu/odpowiedzi. Nie dziedziczyć akceptacji lokalnych
znaczeń do lokatora. Szacunek {part['estimate_minutes'][0]}–{part['estimate_minutes'][1]} minut,
jedna karta do90min; ewentualny dalszy podział przed oceną.

## Artefakty i zakończenie

Nowy prywatny part-{part['card'].split('.')[-1]}/: comparisons/review/issues/owner-focus/
presentation/manifest. Additive current-state, nowy pomiar, append-only
sessions.jsonl. Wszystkie przypisane ID źródłowo ocenione lub jawnie blokowane;
same pending/metadane nie wykonują przeglądu. scripts/check.ps1 offline,
lokalneTMP/TEMP/nowybasetemp, git diff --check i audyt niezmienności.
Oceny modelu są propozycjami; decyzja właściciela tylko w pokazanym zakresie.

## Wyłączenia i wznowienie

Inne części, .4d/M-POC5B i20sytuacji, nowe źródła/ekstrakcja/korekty,
API inferencji, architektura i commit/push. Dawne nierozstrzygnięcia i
decyzje zachować. Nadrzędne karty partial do rozliczenia i decyzji całości;
M-POC5 jedyny next. Następna osobna część po decyzjach obecnej.
''',encoding='utf-8')
p=D/'work/tasks/README.md';text=p.read_text(encoding='utf-8');text+='\n\n## Podział przeglądu lokatorów przed wykonaniem — 2026-10-11\n\n'
text+='\n'.join(f"- [{x['card']}](semantic/{x['card']}.md): {len(x['evidence_ids'])} ID /{x['occurrences']} wystąpień." for x in parts)+'\n';p.write_text(text,encoding='utf-8')
p=D/'STATUS.md';text=p.read_text(encoding='utf-8');text=text.replace('## M-POC5A — rzeczywisty przegląd .4b3, 2026-10-11','## M-POC5A — decyzja .4b3 i podział .4c, 2026-10-11\n\n'+aggregate+'\n## M-POC5A — rzeczywisty przegląd .4b3, 2026-10-11',1);p.write_text(text,encoding='utf-8')
p=D/'ROADMAP.md';text=p.read_text(encoding='utf-8');needle='po decyzjach osobna .4c, reszta i M-POC5B osobno';assert needle in text
p.write_text(text.replace(needle,'właściciel przyjął68+2+2 zakresów .4b3; łącznie257 scoped decyzji; .4c podzielona przed review na44/42/38 wystąpień, bieżąca .4c1; reszta i M-POC5B osobno',1),encoding='utf-8')
print(json.dumps(dict(owner_decided=72,total_scoped=257,protected=len(protected),parts=parts),ensure_ascii=False))
