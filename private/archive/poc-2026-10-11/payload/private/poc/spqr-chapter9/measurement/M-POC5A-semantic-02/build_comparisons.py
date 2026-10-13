"""Save manually prepared comparison proposals; never update extraction or human decisions."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
M = Path(__file__).resolve().parent
OUT = P / 'reviews/semantic-01/part-02'
OUT.mkdir(exist_ok=True)
assert not (OUT / 'comparisons.json').exists()

def ref(path):
    data=path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())

def load(path):
    return json.loads(path.read_bytes())

def save(path,obj):
    assert not path.exists(),path
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

C=load(P/'reviews/semantic-01/checklist.json')
protected=[]
for tree in ['source','runs','proposals','reports','inputs','context','transfer','evaluation/eval-v1',
             'reviews/context-source-01','measurement/M-POC5A-semantic-01','reviews/semantic-01']:
    protected.extend(ref(f) for f in sorted((P/tree).rglob('*')) if f.is_file() and OUT not in f.parents)
sessions=P/'measurement/sessions.jsonl'
save(M/'start.json',dict(card='M-POC5A',part='M-POC5A.2',first_recorded_clock_utc='2026-10-10T18:49:47+00:00',
    bootstrap_start='unknown',recorded_at_utc=datetime.now(timezone.utc).isoformat(),protected=protected,
    sessions_before=ref(sessions),user_instruction='ok kontynuuj',
    instruction_scope='Continue work; does not explicitly decide pending SEM-001/002/003.',
    previous_owner_decisions_still_pending=True,source_expansion=0))
for r in list(C['responses'].values())+[C['evaluation'],C['source']]:
    assert ref(ROOT/r['path']) == r

# These are explicit model proposals after source and field comparison, not computed scores.
notes={
1:('supported_local_scope','R911.conditions: Front, marker, wolny Rear; exceptions: Flank/Rear, współatak i ZOC na początku Orders Phase. time_limits zachowuje decyzję przed DR i początkowy ZOC. Obie jednostki muszą spełniać warunki. Nie wyliczamy geometrii ZOC.'),
2:('supported_local_scope','R911 action_effect/parameters zachowują Pre-Shock +1 DRM, pół/floor Hits obrońcy i -1 Hits EL. Są to operatory zgodne z zatwierdzonym zakresem 5→2 oraz 3→2; nie dopisano dolnej granicy dla bazowego 0 ani kolejności innych modyfikatorów. Nie oceniono SIT.'),
3:('supported_local_scope','R911 action_effect krok 3: po Shock, tylko gdy piechota nie Rout i EL nie Rampage; wolny Rear wybiera gracz EL, facing zachowane. Nie zastępuje to pełnego wyniku Shock.'),
4:('supported_local_scope','R911 rozdziela końcowy Pass-Thru TQ od Pre-Shock, wyłącza SK z kroku 4 i nalicza tylko positive excess DR-TQ. R924 powtarza wyłączenie SK. Parametr positive excess nie importuje minimum 1 z 9.16; brak konkretnej liczby nie jest pominięciem operatora.'),
5:('supported_local_scope','R912: Reaction Fire only, nazwany Elephant Screen MRRC row, własne supply markers i brak screen u Leader Elephant. Nie ma podstaw do wartości pełnego lookupu lub domknięcia supply.'),
6:('supported_local_scope','R913: Mounted Javelinists dla Missile Fire; javeliny/screen mają osobne DR. R913note: historyczny brak wież nie zmienia reguły. Nie utożsamiono niepotwierdzonych aliasów wiersza MRRC.'),
7:('supported_local_scope','R914 i N914table zachowują immediate Rout→Rampage; zwykły EL: 0 do najbliższej friendly, remis wybiera przeciwnik; pierwsze 7–9 od przyczyny, późniejsze 7–9 eliminacja. first/subsequent jest jawne w wierszu tabeli. Rzeczywisty kierunek nie został ustalony.'),
8:('supported_local_scope','N914table: Leader 0 eliminuje; późniejsze 7–9 rally z Hits=TQ−2 zamiast eliminacji. R914.exceptions utrzymuje ten wyjątek wobec ogólnego zakazu rally. Pierwsze 7–9 nie daje drugiego punktu w EXP-008.'),
9:('supported_local_scope','N914table rozdziela first Rampage DR od any subsequent: pierwsze Leader 7–9 prowadzi od przyczyny, nie do natychmiastowego rally. R914.exceptions ogranicza rally do subsequent. Nie określono zaliczania rzutu wyzwalającego 4.84.'),
10:('source_block_supported','N914diagram podaje illustrative example, użycie kompasu konkretnej bitwy i brak uniwersalnego kierunku geograficznego. D914compass/G-D914compass mają brak źródła i blocking=true. To blokada rzeczywistego kierunku, nie lokalnie podanej syntetycznej trasy.'),
11:('supported_local_scope','R914: immediate i serial resolution, wyjątek OW; brak ZOC i Reaction Fire każdego rodzaju; no rally z osobnym wyjątkiem Leader w exceptions. C-9.14-11 przechodzi na PDF33 i kontynuacja źródła jest zachowana. Wyjątek jest referencją do EXP-008, bez drugiego punktu.'),
12:('supported_local_scope','R914 parametry/action: próba 3 hexów na directional DR; stop adjacent przed occupied hex; occupant 1 CH przez Front, 2 Flank/Rear, cavalry zawsze 2; oba elementy stacku Hits. Leader unable to withdraw według 4.72 ginie bez DR. Realnego warunku unable nie domknięto.'),
13:('supported_local_scope','R914: ponawianie do offmap/elimination, >=8 hexów od nearest unit i eliminacja po 4. consecutive DR, jeśli wcześniej nie zakończono. Wiersz tabeli i wyjątki nadal kwalifikują późniejsze 7–9 oraz Leader. Nie dodano realnego pomiaru mapy.'),
14:('supported_local_scope','R914: leader podróżuje z EL; na końcu casualty 4.73, survivor zostaje na końcowym heksie. Offmap eliminuje obu, odrębnie od survival placement. Nie podano wyniku casualty DR z nieobecnego źródła.'),
15:('supported_local_scope','R915: zakaz voluntary enemy EL ZOC, 2 CH za każdy Flank/Rear hex i przy forced ZOC entry; Front attack zakazany, Flank/Rear nie daje zwykłego AS. Pozwolenie lokalne nie potwierdza pełnej legalności ataku bez bazowego kontekstu.'),
16:('supported_local_scope_with_locator_issue','R916: wejście z nonadjacent do adjacent, obligatory OW attempt; jeśli można odejść brak Reaction Fire, jeśli nie można immediate TQ, routed cavalry eliminuje bez DR. Leader EL wyłączony w exceptions. Zakres minimum należy do EXP-017. E916 urywa cytat wyjątku; semantyczne podparcie pochodzi z pełnego regionu PDF33, a lokator nadal błędny.'),
17:('incomplete_local_interpretation','R916 zachowuje DR>TQ/difference/minimum 1, ale interpretation=unknown i G916.blocking pozostawiają DR<=TQ nierozstrzygnięte. Zatwierdzona lokalna gałąź 0 CH nie jest jednoznacznie reprezentowana jako ustalona. SEM-001 nadal czeka na decyzję właściciela; nie stwierdzono błędnej transkrypcji ani zawsze 1 CH.'),
18:('supported_local_scope','R917 zawiera zakaz Position Superiority dla EL vs EL oraz pozycyjnego AS z Flank/Rear. Nie zawiera zakazu wszystkich rodzajów superiority. Pole o AS należy czytać wraz z zakresem Position Superiority; pełne ogólne procedury pozostają poza oceną.'),
19:('blocking_flag_conflict_pending','R918.transcription zachowuje unless rules specifically otherwise, a exceptions=unknown wskazuje nieznane wyjątki. Jednak action_effect/interpretation brzmi Any leader may command i D918specific/G-D918specific mają blocks_full_result=false/blocking=false. Oznaczono brak źródła, lecz nie zadeklarowano blokady realnej autoryzacji. Kandydat SEM-009: właściwość deklaracji blokady w rzeczywistym użyciu wymaga decyzji; nie ma konkretnego niepoprawnie wybranego dowódcy.'),
20:('supported_local_scope','R919.conditions: Indian vs African; +1 Pre-Shock wyłącznie African, dodatkowo do not Clash/SS. Nie przeniesiono DRM na Indian lub wszystkie EL; nie pominięto not przez ogólne zwolnienie.'),
21:('supported_local_scope','R92note: Velites to LI, nie SK. R921: OW Hits dla SK tylko Rear, Velites Flank/Rear. Nie przeniesiono wszystkich wyjątków SK na Velites. Historyczna nota ma operatywny fragment N-07-S2; pozostała historia poza gold.'),
22:('supported_local_scope','R921.conditions i parameters zachowują approaching MA<=SK MA oraz maksimum 2 hexów. action_effect powtarza źródłowe regardless of MA differential; trzeba je czytać w tym warunku, nie jako zniesienie <=. Pełna trasa i kąt OW są osobne. Sama fraza regardless nie jest błędem odczytu.'),
23:('supported_local_scope','R922: target SK +2 Missile DRM; SK/LI Archers Class A nie H&D; LC każdego missile class nie H&D przeciw SK. Te zakazy nie ustalają pełnego lookupu MRRC lub reszty procedury.'),
24:('supported_local_scope','R923: SK nie Shock attack; atakujący SK alone nie Pre-Shock nawet z markerem; mixed defense wybiera other type i pomija SK Size. Wyjątek końcowego Pass-Thru należy do EXP-004, nie do tego zwolnienia. Nowa DCTX923-S4 ma osobny pending.'),
25:('supported_local_scope','R923.action/parameters: Hits zadane przez SK pół, floor, maksimum 1 CH. W context-01 Step 4 dostarcza stronę atakującego przy obrońcy SK, lecz nie zmienia lokalnej treści R923. Nowa relacja i pełne applicability/base/CRT/order pozostają poza tą oceną.')
}

rows=[]
for e in C['expectations'][:25]:
    n=int(e['id'].split('-')[1]);proposal,note=notes[n]
    row=dict(id=e['id'],source_scope=e['source_scope'],source_evidence=e['source_evidence'],
        inventory_refs=e['inventory_refs'],criticality=e['criticality'],classification=e['classification'],
        limits=e['limits'],unreviewed_fields=e['exclusions'],authorizing_decisions=e['authorizing_decisions'],
        proposed_assessment=proposal,comparison=note,proposed_by='Codex',human_reviewer=None,
        human_status='pending',result='not_assessable',scope_only=True,runs={})
    for run in C['responses']:
        ids=e['runs'][run]['output_record_ids']
        extra=['D918specific','G-D918specific'] if n==19 else ['D914compass','G-D914compass'] if n==10 else ['G916'] if n==17 else ['E916'] if n==16 else []
        row['runs'][run]=dict(response=C['responses'][run],proposal=proposal,reviewer='Codex; proposed comparison only',
            human_reviewer=None,status='pending',meaning_result='not_assessable',
            comparison=note,output_trace={rid:C['output_records'][run][rid] for rid in ids+extra},
            gap_claims=e['runs'][run]['extractor_gap_claims'],uncertainties=e['limits']+e['exclusions'])
        row['runs'][run]['dimension_trace']=e['dimensions'][run]
    row['mapped_content_identical_between_runs']=all(C['output_records']['first-001'][rid]['original_record']==
        C['output_records']['context-01'][rid]['original_record'] for rid in e['runs']['first-001']['output_record_ids'])
    assert row['mapped_content_identical_between_runs']
    rows.append(row)

inventory_ids={rid for e in rows for rid in e['inventory_refs']}
inventory=[dict(base_item=r,comparison_scope='Only source spans owned by associated EXP rows; not full parent or unreviewed fields.',
    proposed_by='Codex',human_reviewer=None,status='pending',meaning_result='not_assessable',
    associated_proposals=[dict(expectation=e['id'],proposal=e['proposed_assessment'],comparison=e['comparison'])
        for e in rows if r['id'] in e['inventory_refs']]) for r in C['inventory'] if r['id'] in inventory_ids]
categories=[dict(base_unit=r,proposed_group_assessment=next(e['proposed_assessment'] for e in rows if e['id']==r['frozen_unit']['expectation_id']),
    human_reviewer=None,status='pending',result='not_assessable',
    limitation='Category membership is diagnostic. Complete group comparison is not a separate accepted category score.')
    for r in C['category_units'] if r['frozen_unit']['expectation_id'] in {e['id'] for e in rows}]
summary=dict(expectations=25,local_content_groups=23,context_requirements=2,
    distinct_source_inventory_items=len(inventory),diagnostic_category_units=len(categories),
    model_proposals=dict(Counter(e['proposed_assessment'] for e in rows)),
    owner_decisions=0,accepted_content_groups=dict(first_001=0,context_01=0),
    remaining_expectations_not_compared_in_this_part=49,semantic_metrics='not_assessable')
payload=dict(id='M-POC5A.2-comparisons-01',card='M-POC5A',part='M-POC5A.2',status='partial_waiting_review',
    evaluation=C['evaluation'],responses=C['responses'],source=C['source'],base_checklist=ref(P/'reviews/semantic-01/checklist.json'),
    prepared_at_utc=datetime.now(timezone.utc).isoformat(),owner_decisions=[],summary=summary,
    expectations=rows,inventory=inventory,categories=categories,
    limitations=C['limitations'],limits=C['limits'],
    acceptance_policy='All classifications are model proposals. Owner acceptance applies only to exact shown frozen scope/hash, not metadata, whole inventory records, relations, locators or situations.',
    history_policy='Additive overlay; original checklist, reports, first preparation and their seals unchanged.')
save(OUT/'comparisons.json',payload)

issue=dict(id='SEM-009',expectation='EXP-019',classification=['brak kontekstu','błędna interpretacja'],
    criticality='critical_in_reviewed_scope',status='pending',proposed_by='Codex',human_reviewer=None,
    source_scope=C['expectations'][18]['source_scope'],source_evidence=C['expectations'][18]['source_evidence'],
    evidence={r:rows[18]['runs'][r]['output_trace'] for r in C['responses']},response_hashes=C['responses'],evaluation=C['evaluation'],
    proposal=notes[19][1],impact='Potential missing explicit block on actual commander eligibility when exceptions are unknown.',
    uncertainty='Unknown exceptions and false blocking flags are observed. No concrete real-state eligibility answer exists; whether this is an unmarked critical block remains an owner decision.',
    excluded='No new exact relation gold, no judgment of all command rules, no invented commander/scenario, no situation outcome.')
save(OUT/'issues.json',dict(issues=[issue],inherited_pending=['SEM-001','SEM-002','SEM-003','SEM-004','SEM-005','SEM-006','SEM-007','SEM-008'],
    wrong_read_confirmed='not_assessable',confirmed_semantic_errors='not_assessable',owner_decisions=[]))

lines=['# M-POC5A.2 — EXP-001–025: konkretne porównania', '',
    'Stan partial/waiting_review. Poniżej propozycje oceniającego Codex po porównaniu źródeł z polami obu odpowiedzi. Żadna nie została zaakceptowana za właściciela. „ok kontynuuj” autoryzuje dalszą pracę, nie rozstrzyga wcześniejszych SEM-001/002/003.', '',
    'Pełne transkrypcje, pola i ślady bajtowe: [comparisons.json](comparisons.json). Nowa kwestia: [issues.json](issues.json). Pierwszy pakiet nadal [pending](../focus-01.md).', '',
    f"eval-v1 `{C['evaluation']['sha256']}`.", '',
    *[f"{r}: `{v['sha256']}`, {v['bytes']} bajtów." for r,v in C['responses'].items()], '',
    '## Wynik porównania oceniającego', '',
    '23 zakresy lokalne: 21 propozycji zgodności, 1 propozycja zgodności treści z osobnym błędem lokatora E916, 1 niepełna interpretacja (EXP-017). Dwa wymagania kontekstu: właściwa blokada mapy (EXP-010) i nierozstrzygnięta deklaracja blokowania dowodzenia (EXP-019). Te liczby opisują propozycje, nie metrykę poprawności ani akceptację.', '',
    f"Powiązano {len(inventory)} różnych pozycji źródłowego inwentarza i {len(categories)} par rubryka/EXP. Nie nadano pełnej akceptacji pozycji o szerszym zakresie; tabele, nota operatywna i przykład kompasu są czytane tylko w zatwierdzonym zakresie.", '',
    '## Nowa kwestia SEM-009 — 9.18', '',
    '> Unless the rules specifically state otherwise, Elephant units may be commanded by any leader.', '',
    'W obu wynikach literalny cytat zachowuje zastrzeżenie, a wyjątki mają unknown. Jednocześnie R918.action_effect mówi „Any leader may command Elephant units”, D918specific.blocks_full_result=false, G-D918specific.blocking=false. Brak wyjątków zgłoszono, lecz brak jawnej blokady realnej autoryzacji. To kandydat do oceny; nie wskazano rzeczywistego dowódcy i nie potwierdzono błędnego wyniku.', '',
    'Proponowana decyzja: znana reguła lokalna pozostaje; rzeczywiste uprawnienie konkretnego leadera wymaga sprawdzenia wyjątków. Właściciel rozstrzyga, czy false w dwóch deklaracjach jest nieoznaczoną blokadą krytyczną. Nie ocenia to kierunku/rodzaju D918specific jako nowego gold.', '',
    '## Zakresy do rzeczywistego review', '']
for e in rows:
    lines += [f"### {e['id']}", '', 'Dokładny zatwierdzony zakres: '+e['source_scope'], '',
        'Porównanie: '+e['comparison'], '',
        'Propozycja: `'+e['proposed_assessment']+'`; właściciel **pending** dla obu hashów.', '',
        'Źródło: '+', '.join(f"PDF {v['pdf_page']} {v.get('column','')}, {v.get('inventory_ref','')}, bbox {v.get('bbox_pdf_points')}" for v in e['source_evidence']), '',
        'Transkrypcja źródła (source_span ma pierwszeństwo nad kopertą):', '']
    for v in e['source_evidence']:
        exact=v.get('source_span')
        if not isinstance(exact,str):exact=v.get('transcription','')
        lines += ['> '+exact.replace('\n','\n> '), '']
    for run,d in e['runs'].items():
        lines += [f"**{run}** — osobny wynik pending; porównane pola:", '']
        for rid,t in d['output_trace'].items():
            obj=t['original_record'];lines += [f"{rid}, `{t['pointer']}`, bajty [{t['raw_span']['start_byte']},{t['raw_span']['end_byte_exclusive']}), hash `{t['raw_span']['sha256']}`.", '']
            for field in ['transcription','interpretation','conditions','action_effect','exceptions','parameters','time_limits','content','blocking','impact_if_missing']:
                if field in obj:
                    value=obj[field]
                    if isinstance(value,dict) and 'state' in value:value={k:value[k] for k in ['state','value','reason','gap_ids'] if k in value}
                    lines += [field+': '+json.dumps(value,ensure_ascii=False), '']
    lines += ['Wyłączenia/niepewności: '+'; '.join(e['limits']+e['unreviewed_fields']), '']
lines += ['## Granice tego pakietu', '',
    'R921 „regardless of MA differential” jest frazą źródłową; warunek approaching MA<=SK MA nadal obowiązuje w conditions/parameters. Nie nazwano tego błędem odczytu. R917 dotyczy Position Superiority, nie wszystkich form superiority.', '',
    'Znane operatory przy zadanych faktach nie wymagają automatycznie pełnego rzeczywistego setupu. Wszystkie gap.blocking do zakresów pełnego Shock/OW/CRT trzeba czytać oddzielnie od lokalnych operatorów. 20 sytuacji nie oceniono.', '',
    'Potwierdzono równość wartości 18 mapowanych reguł/węzłów i wskazano osobne zakresy bajtów obu wyników; nie oznacza to identyczności leksykalnych bajtów ani poświadczenia znaczenia. Nowa DCTX923-S4, trzy dawne brakujące krytyczne pary i wszystkie pozostałe krawędzie nadal pending. 64 granice glifów i E916 nie zostały zamknięte.', '',
    'Nie pozyskano źródeł ani pass-02, ekstrakcji lub korekt. Historyczne niewiadome izolacji/ekspozycji/selektorów/czasów/tokenów/ceny i aktywny budżet unknown. 49 dalszych oczekiwań w częściach .3/.4 pozostaje pending.', '']
(OUT/'review.md').write_text('\n'.join(lines),encoding='utf-8')
save(OUT/'manifest.json',dict(id='M-POC5A.2-packet-manifest',evaluation=C['evaluation'],responses=C['responses'],
    source=C['source'],artifacts=[ref(OUT/f) for f in ['comparisons.json','issues.json','review.md']],
    semantic_acceptance='not_performed',owner_decisions=[]))
save(P/'reviews/semantic-01/current-state-02.json',dict(id='M-POC5A-current-state-02',card='M-POC5A',part='M-POC5A.2',
    status='partial_waiting_review',base=ref(P/'reviews/semantic-01/checklist.json'),overlay=ref(OUT/'manifest.json'),
    previous_presentation=ref(P/'reviews/semantic-01/presentation-01.json'),summary=summary,
    owner_decisions=[],acceptance='not_performed',resume='Pending SEM-001/002/003 and new part-02 local scopes/SEM-009; subsequent parts after their exact review scopes.'))
print(json.dumps(summary,ensure_ascii=False))
