"""Save evidence-backed model proposals for EXP-026–050, without owner acceptance."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01'
OUT=REV/'part-03'
OUT.mkdir(exist_ok=True)
assert not (OUT/'comparisons.json').exists()
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(path,obj):
    assert not path.exists(),path
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

protected=[]
for tree in ['source','runs','proposals','reports','inputs','context','transfer','evaluation/eval-v1','reviews',
             'measurement/M-POC5A-semantic-01','measurement/M-POC5A-semantic-02','measurement/M-POC5A-owner-review-001']:
    protected += [ref(f) for f in sorted((P/tree).rglob('*')) if f.is_file() and OUT not in f.parents]
save(M/'start.json',dict(card='M-POC5A',part='M-POC5A.3',first_recorded_clock_utc='2026-10-10T19:09:56+00:00',
    bootstrap_start='unknown',recorded_at_utc=datetime.now(timezone.utc).isoformat(),protected=protected,
    sessions_before=ref(P/'measurement/sessions.jsonl'),owner_instruction='kontynuuj',
    instruction_scope='Continue independent comparisons; no choice or acceptance of prior pending alternatives.'))
C=load(REV/'checklist.json');previous=load(REV/'current-state-03.json')
for r in list(C['responses'].values())+[C['evaluation'],C['source']]:assert ref(ROOT/r['path'])==r
for key in ['decision','overlay']:assert ref(ROOT/previous[key]['path'])==previous[key]

notes={
26:('supported_local_scope','R923: PH/HI/LG broniące przez Front przed LI nie robią Pre-Shock nawet z markerem atakującego; LI nadal sprawdza. Reverse wyraźnie nie zachodzi. Nie rozszerzono na Flank/Rear lub inne typy.'),
27:('supported_local_scope','R924: SK Rout oznacza eliminację, facing kosztuje 0 MP, ponowne ruchy w Game Turn bez Cohesion cost. Nie ma ogólnego zwolnienia z kosztów terenu i stacking.'),
28:('supported_local_scope','R924 i N924ex pokazują pojedynczą przerwę na gap, z możliwością oddzielnych powtórzeń. Dwa kolejne Velites w przykładzie nie tworzą line. Literalne układy 2808/2809/2810/2811/2812 zachowane; nie przyznano pełnej legalności 4.32.'),
29:('supported_local_scope','R931: missile-armed LC, target strictly lower MA (<, nie <=), wyjątek SK; LC Archers fire podczas OW według 6.55. G-D931HD/OW zatrzymują pełne procedury, nie znany warunek lokalny.'),
30:('supported_local_scope','Lokalne R932.action_effect/parameters w obu wynikach zachowują pół/floor Hits zadanych przez atakujące LC PH/HI/MI/LG/BI. context-01 zmienia interpretation/exceptions, lecz nie literalną lokalną transkrypcję ani parametr. Ta propozycja nie akceptuje nowych operatorów/wyjątku Routed, całej R932, relacji ani kolejności AS/LC; SEM-003 nadal pending.'),
31:('source_block_supported','first-001 zachowuje literalny printed-result przykład i unknown interpretację; G932/G-D932CRT blocking. context-01 dodaje źródłowe kwalifikacje AS/LC/Routed, ale N932ex nadal unknown i GCTX-order/CRT/applicability/845 blocking. Propozycja: właściwe zachowanie nierozstrzygnięcia pełnego przykładu i potrzeby kontekstu; źródłowa poprawność samych nowych operatorów pozostaje osobnym SEM-003, bez założenia automatycznego znoszenia 2x i pół.'),
32:('supported_local_scope','R941.conditions: moves adjacent i Shock przez Front; po 2L na flank zajęty przez friendly PH lub w friendly PH ZOC, HI any Class 1L zamiast 2L. Wyłączenia: rozpoczęcie adjacent i pozostanie tam, Flank/Rear oraz jakikolwiek PH wśród atakujących. Brak CRT nie blokuje podanego lokalnego shiftu.'),
33:('source_block_supported','R95note/N95design zachowują operatywny wymóg scenario-specific eligible units, R951 warunek eligible. G-D95scenario blocking=true, brak listy nie zastąpiony zgodą dla wszystkich PH. N953ex to jedynie odesłanie do przykładu; jego nonblocking nie zamyka krytycznej listy eligibility. Nie oceniono SIT-11.'),
34:('supported_local_scope','R951: IO albo LC bezpośrednio od OC, back PH startuje bezpośrednio za front, płaci terrain+1 MP, trafia pod front; kończy ruch obu w tej Orders Phase. Nie ustalono realnej eligibility, OC ani kosztu terenu.'),
35:('supported_local_scope','R952: rozkazy tylko OC; 2 IO przy ruchu w trybie IO, PAW 6.8, no Wheel/Reverse/Column. Unstack IO lub LC as above, top rusza za normalny koszt, bottom zostaje. R951 i pierwszy warunek OC zachowują zakres as above; nie domknięto pełnej procedury LC lub PAW.'),
36:('supported_local_scope','R952 dla units in DD: zawsze MA4, nigdy MA5; movement CH do każdej, zakaz wejścia/przejścia jakiegokolwiek unit przez gotowy DD. R951 osobno reprezentuje etap formowania, zanim gotowy stack istnieje. Nie odczytano zakazu jako anulowania formowania.'),
37:('supported_local_scope','R953: combine Sizes, TQ top, przy Rear bottom; jeśli wybrana do check jednostka dostaje jakiekolwiek Hits, druga również sprawdza. Unknown interpretacja końcowej eliminacji G953 nie uchyla jawnych wcześniejszych efektów; prawdziwe ratingi i pełny check nieustalone.'),
38:('supported_local_scope','R953: przeciwnik broniący się przed DD +1 Pre-Shock; DD jako defender -1. R941 w mapowanym zakresie zachowuje warunki i wyłączenia Phalanx Defense, więc nie przyznano shiftu bezwarunkowo. Nie nadaje to formalnego TP krawędzi R953→R941.'),
39:('supported_local_scope','R953: Hits DD defender w Shock przez Flank/Rear 3x zamiast 2x; Shock rozdzielony równo, nieparzysty Hit do top. Missile do top z wyjątkiem Rear do bottom. Selekcja TQ przez Rear nie zmienia odd-Hit allocation Shock; baza i inne mnożniki pozostają poza zakresem.'),
40:('incomplete_local_interpretation_pending_source_availability','Oba R953 zachowują both rout i separate hexes, ale końcowe the unit pozostaje literalne; interpretation unknown/G953 blocking. Eval-v1 ma per-unit eliminację z możliwością legalnego Rout drugiej PH. Propozycja niepełnej reprezentacji tej lokalnej gałęzi pozostaje SEM-002 pending; osobno dostępność podparcia 10.24/25/23 dla ekstraktora i rzeczywista geometria/kolejność.'),
41:('supported_local_scope','R961: rule of thumb dwóch Roman infantry tego samego border color, z wyjątkami jak Velites. Nie pełne eligibility. Joint move 2 IO; 1 IO tylko z OC w stack dającym rozkazy; 1 LC tylko jeśli obie eligible. Odesłania do charts/line nie zamykają pełnych procedur.'),
42:('supported_local_scope','R962: combine Size, inne ratingi w tym TQ top; własny check każdej z top TQ; tylko top Missile Fire, obie Shock tego samego hex; Automatic Hits do każdej. Shock alokacja delegated 8.46 Step4/10.13. R962 jest niezmieniona; context D962shock dostało endpoint, lecz G-D962shock nadal blocking, dalej brak 6.68 #6. Lokalna reprezentacja nie zamyka alokacji ani nie nadaje TP.'),
43:('supported_local_scope','R963 zachowuje OR: różne border colors lub ten sam color i różne classes. +1 DRM do wszystkich TQ checks, bez zastąpienia OR przez AND. Faktyczne kolory i klasy wymagają danych.'),
44:('supported_local_scope','R964: zamiana kolejności stack tylko IO, nie część movement ani LC; facing może LC. Przy ruchu jednej jednostki z stacku rusza tylko top. Nie rozszerzono zwykłego unstack na szczególne MLE.'),
45:('supported_local_scope','R965: Roman infantry 1 MP za facing dowolnej liczby vertices, nie koszt za każdy vertex. Nie przeniesiono tej operacji na MLE, które zachowuje facing.'),
46:('supported_local_scope','R966: top units w stackach tej samej Line, sideways do vacant flank; Clear i poza enemy ZOC, facing bez zmiany; wyłącznie unstack, nie stacking together. N966diagram zachowuje Original Deployment u góry, After MLE u dołu jako ilustrację. Nie akceptujemy małych ratingów, identyfikacji front/back konkretnych counterów ani ogólnego prawa do dowolnej strony z samej grafiki.'),
47:('supported_local_scope','R967: reakcja w instant approach enemy combat within 2 hexes of stacked Roman line; wolno odroczyć pierwszą okazję do następnego kwalifikowanego triggeru. OW/MLE razem tylko przez różne jednostki z właściwymi triggerami, nie te same. N967ex zachowuje przykład Velites OW i Hastati MLE.'),
48:('supported_local_scope','R968 wyraźnie kwalifikuje post-MLE move przez When by LC: obie jednostki mogą ruszyć z MA-2. LC-only dla aktywnego MLE, 0 CH za samo MLE i zakaz Column. Nie przeniesiono uprawnienia dalszego ruchu na tryb reakcyjny R967.'),
49:('supported_local_scope','R97intro: obowiązek dla Romans przed 200 BCE i bez Scipio Africanus jako OC; Cannae jawnie objęte instrukcją gry, nie historycznym wnioskowaniem. Parametr jest prior to 200, nie <=200. Explanatory C9.7-S2 nie stanowi dodatkowego obowiązku.'),
50:('partial_context_declaration_pending','Obie odpowiedzi podają predykaty daty/OC i warunki Triarii, nie rzeczywiste dane wybranej bitwy. AWL/RP/LOS/ZOC mają jawne blocking gaps; brak osobnych deklaracji źródła rzeczywistej daty i OC w R97intro.gap_ids (pusta lista). SEM-010: wystarczalność tego opisu needs-context wymaga właściciela. Nie jest to dowód fikcyjnego wybrania dowódcy/daty; known na conditions oznacza znany warunek, nie spełniony fakt. Nie oceniono SIT.')
}
extras={31:['G932'],33:['G-D95scenario'],40:['G953'],42:['D962shock','G-D962shock'],50:['G-D972AWL','G-D972RP']}
rows=[]
for e in C['expectations'][25:50]:
    n=int(e['id'].split('-')[1]);proposal,note=notes[n]
    row=dict(id=e['id'],classification=e['classification'],criticality=e['criticality'],source_scope=e['source_scope'],
        source_evidence=e['source_evidence'],inventory_refs=e['inventory_refs'],limits=e['limits'],
        unreviewed_fields=e['exclusions'],authorizing_decisions=e['authorizing_decisions'],
        proposed_assessment=proposal,comparison=note,proposed_by='Codex',human_reviewer=None,
        human_status='pending',result='not_assessable',whole_record_accepted=False,runs={})
    for run in C['responses']:
        ids=e['runs'][run]['output_record_ids']
        row['runs'][run]=dict(response=C['responses'][run],evaluation=C['evaluation'],
            proposed_assessment=proposal,comparison=note,reviewer='Codex; proposed comparison only',human_reviewer=None,
            status='pending',meaning_result='not_assessable',
            output_trace={rid:C['output_records'][run][rid] for rid in ids+extras.get(n,[])},
            dimension_trace=e['dimensions'][run],gap_claims=e['runs'][run]['extractor_gap_claims'],
            uncertainties=e['limits']+e['exclusions'])
    row['changed_mapped_record_ids']=[rid for rid in e['runs']['first-001']['output_record_ids']
        if C['output_records']['first-001'][rid]['original_record']!=C['output_records']['context-01'][rid]['original_record']]
    rows.append(row)
ids={rid for e in rows for rid in e['inventory_refs']}
inventory=[dict(base_item=r,status='pending',meaning_result='not_assessable',human_reviewer=None,
    scope='Only spans owned by associated EXPs, not whole parents or fields.',
    associated_proposals=[dict(id=e['id'],proposal=e['proposed_assessment'],comparison=e['comparison'])
        for e in rows if r['id'] in e['inventory_refs']]) for r in C['inventory'] if r['id'] in ids]
categories=[dict(base_unit=r,status='pending',result='not_assessable',human_reviewer=None,
    proposed_group_assessment=next(e['proposed_assessment'] for e in rows if e['id']==r['frozen_unit']['expectation_id']),
    limitation='Diagnostic category/EXP unit, not an additional rule point or accepted score.')
    for r in C['category_units'] if 26<=int(r['frozen_unit']['expectation_id'].split('-')[1])<=50]
mapped={rid for e in C['expectations'][25:50] for rid in e['runs']['first-001']['output_record_ids']}
changed=sorted(rid for rid in mapped if C['output_records']['first-001'][rid]['original_record']!=C['output_records']['context-01'][rid]['original_record'])
assert changed==['N932ex','R932'] and len(mapped)==26
summary=dict(expectations=25,local_content_groups=22,context_requirements=3,
    distinct_source_inventory_items=len(inventory),diagnostic_category_units=len(categories),
    model_proposals=dict(Counter(e['proposed_assessment'] for e in rows)),mapped_record_count=26,
    mapped_value_identical_count=24,changed_mapped_record_ids=changed,
    new_owner_decisions=0,previous_owner_accepted_groups_per_answer=22,
    still_pending_expectations=52,remaining_uncompared_expectations=24,semantic_metrics='not_assessable')
payload=dict(id='M-POC5A.3-comparisons-01',card='M-POC5A',part='M-POC5A.3',status='partial_waiting_review',
    evaluation=C['evaluation'],responses=C['responses'],source=C['source'],base_checklist=ref(REV/'checklist.json'),
    prior_state=ref(REV/'current-state-03.json'),prior_owner_decision=ref(REV/'owner-decision-01.json'),
    owner_decisions=[],summary=summary,expectations=rows,inventory=inventory,categories=categories,
    limitations=C['limitations'],limits=C['limits'],
    tooling_diagnostic='An earlier diagnostic print assumed transcription on graphic evidence and raised KeyError. Corrected to optional text; graphic source viewed. No source or answer change.',
    acceptance_policy='Proposals only. Prior 22 accepted scopes do not approve these 25. Full inventory/relations/locators/situations and unknown fields excluded.')
save(OUT/'comparisons.json',payload)
issue=dict(id='SEM-010',expectation='EXP-050',classes=['brak kontekstu','niejednoznaczność'],
    criticality='critical_in_reviewed_scope',status='pending',proposed_by='Codex',human_reviewer=None,
    source_scope=rows[-1]['source_scope'],source_evidence=rows[-1]['source_evidence'],
    responses=C['responses'],evaluation=C['evaluation'],
    evidence={run:rows[-1]['runs'][run]['output_trace'] for run in C['responses']},
    proposal=notes[50][1],impact='Whether exact real-battle date/OC source needs and their applicability block are sufficiently explicit.',
    uncertainty='Predicates are known, real facts not asserted. AWL/RP/LOS/ZOC block exists. No actual case was resolved; absence of separate date/OC gap is not automatically a confirmed critical error.',
    exclusions='No new gold; do not invent date/OC or judge all real setup or any situation.')
save(OUT/'issues.json',dict(issues=[issue],inherited_pending=['SEM-001','SEM-002','SEM-003','SEM-004','SEM-005','SEM-006','SEM-007','SEM-008','SEM-009'],
    previous_acceptance=ref(REV/'owner-decision-01.json'),confirmed_semantic_errors='not_assessable',owner_decisions=[]))

lines=['# M-POC5A.3 — EXP-026–050','',
    'Propozycje Codex po porównaniu source spans i pól obu wyników; wszystkie nowe decyzje właściciela pending. Wcześniejsze 22 zaakceptowane lokalne zakresy pozostają osobną decyzją i nie akceptują nowych części tych samych reguł.', '',
    f"eval-v1 `{C['evaluation']['sha256']}`.", '',
    *[f"{run}: `{r['sha256']}`, {r['bytes']} bajtów." for run,r in C['responses'].items()], '',
    'Pełne ślady: [comparisons.json](comparisons.json). Nowa kwestia: [issues.json](issues.json). Czytelny pakiet: [owner-focus.md](owner-focus.md).', '',
    '21 propozycji zgodności lokalnej, 2 właściwe potrzeby/blokady źródła, 1 niepełna lokalna interpretacja (SEM-002) i 1 niepełna jawność potrzeb setupu (SEM-010) do decyzji. Nie jest to zaakceptowany wynik jakości.', '',
    f"Powiązano {len(inventory)} różnych pozycji inwentarza i {len(categories)} par rubryka/EXP. 24 z 26 mapowanych reguł/węzłów ma identyczne wartości; R932/N932ex różnią się. Nie poświadczono identyczności leksykalnych bajtów ani całego grafu.", '',
    '## Pełne porównania w dokładnym zakresie','']
for e in rows:
    lines += [f"### {e['id']}",'', 'Dokładny zatwierdzony zakres: '+e['source_scope'],'',
        'Porównanie: '+e['comparison'],'', 'Propozycja: `'+e['proposed_assessment']+'`; decyzja właściciela pending dla obu hashów.','']
    for v in e['source_evidence']:
        text=v.get('source_span') or v.get('transcription') or '[graphic evidence; no literal text field]'
        if not isinstance(text,str):text=json.dumps(text,ensure_ascii=False)
        lines += [f"Źródło PDF {v['pdf_page']} {v.get('column','')}, {v.get('inventory_ref','')}, bbox {v.get('bbox_pdf_points')}.",'',
            '> '+text.replace('\n','\n> '),'']
    for run,r in e['runs'].items():
        lines += [f"**{run}** — osobna propozycja/pending:",'']
        for rid,t in r['output_trace'].items():
            lines += [f"{rid}, `{t['pointer']}`, bajty [{t['raw_span']['start_byte']},{t['raw_span']['end_byte_exclusive']}), hash `{t['raw_span']['sha256']}`.",'']
            for field in ['transcription','interpretation','conditions','action_effect','exceptions','parameters','time_limits','content','gap_ids','blocking','impact_if_missing']:
                obj=t['original_record']
                if field in obj:
                    value=obj[field]
                    if isinstance(value,dict) and 'state' in value:value={k:value[k] for k in ['state','value','reason','gap_ids'] if k in value}
                    lines += [field+': '+json.dumps(value,ensure_ascii=False),'']
    lines += ['Wyłączenia i niepewności: '+'; '.join(e['limits']+e['unreviewed_fields']),'']
lines += ['## Zachowane granice','',
    'SEM-002 i SEM-003 nadal pending. Akceptacja lokalnego pół/floor w EXP-030 nie akceptuje całej R932, nowego Routed/AS wyjątku, kolejności lub relacji; akceptacja wymagania źródła w EXP-031 nie rozstrzyga operators/result.', '',
    'R962 lokalna delegacja nie domyka pełnej alokacji. Nowa ścieżka trzech krawędzi kończy się na brakującym 6.68 #6; stop rozszerzania na granicy 2 zachowany, brak certyfikatu całego grafu.', '',
    'Krytyczny brak źródła blokuje odpowiedni pełny wynik. Znane operatory/warunki z zadanymi faktami nie są automatycznie blokowane brakiem całego setupu. 20 sytuacji nie oceniono.', '',
    'R966diagram: sprawdzono tekst warunków oraz orientację Original/After panels. Nie certyfikowano tiny ratings, tożsamości counterów w obu panelach lub wszystkich granic glifów. E916 i 64 granice nadal otwarte.', '',
    'Źródła, odpowiedzi, eval-v1 i wcześniejsze pakiety/raporty zachowane. 0 nowych ekstrakcji, kontekstu i korekt. Historyczne izolacja/ekspozycja i selektory/czasy/tokeny/cena/aktywny budżet nadal unknown. M-POC5A partial.', '']
(OUT/'review.md').write_text('\n'.join(lines),encoding='utf-8')

focus=['# Przegląd właściciela — EXP-026–050','',
    'Tylko nowe, dokładne zakresy poniżej. Poprzednie 22 akceptacje nie przenoszą się na inne klauzule tych samych reguł. Pełna transkrypcja, pola i ślady bajtów: [review.md](review.md) i [comparisons.json](comparisons.json).','',
    f"first-001 `{C['responses']['first-001']['sha256']}`; context-01 `{C['responses']['context-01']['sha256']}`; eval-v1 `{C['evaluation']['sha256']}`.",'',
    '## Propozycja akceptacji 21 zakresów lokalnych i 2 wymagań źródła','',
    'Lokalne: EXP-026–030, EXP-032, EXP-034–039, EXP-041–049. Wymagania/blokady źródła: EXP-031 i EXP-033. Wyłączone: EXP-040 i EXP-050 oraz rozstrzygnięcia SEM-002/003/009/010. Akceptacja nie obejmuje całych rekordów, aliasów, ratingów grafik, relacji, sytuacji ani finalnych wyników zależnych od brakującego źródła.','']
for e in rows:
    focus += [f"### {e['id']}",'', 'Zatwierdzony zakres: '+e['source_scope'],'',
        'Oba wyniki / różnice: '+e['comparison'],'',
        'Propozycja: `'+e['proposed_assessment']+'`, właściciel pending.','',
        'Źródła: '+', '.join(f"PDF {v['pdf_page']} {v.get('column','')}, {v.get('inventory_ref','')}" for v in e['source_evidence'])+'.','',
        'Niepewności/wyłączenia: '+'; '.join(e['limits']),'']
focus += ['## SEM-010 — potrzeba rzeczywistej daty i OC','',
    'R97intro.conditions zachowuje znane predykaty daty/OC. R97intro.gap_ids jest puste; R972/AWL/RP i R971/LOS są jawnie blocking. Nie ma konkretnego przypadku z nieprawdziwą datą/dowódcą ani pełnym wynikiem. Właściciel rozstrzyga, czy jawność AWL/RP i warunków wystarcza, czy potrzeba osobnej deklaracji braku źródła rzeczywistej daty/OC. Nie traktować known-predicate jako spełnionego real-faktu.','',
    '## Obrazy źródła','',
    '- [PDF33 right](../../../inputs/v1/regions/pdf-33-core-right.png): klauzule SK/LI.',
    '- [PDF34 left](../../../inputs/v1/regions/pdf-34-core-left.png): przykład Line, LC i Phalanx Defense.',
    '- [PDF34 right](../../../inputs/v1/regions/pdf-34-core-right.png): Double Depth.',
    '- [PDF35 left](../../../inputs/v1/regions/pdf-35-core-left.png): Roman stack i diagram.',
    '- [PDF35 right](../../../inputs/v1/regions/pdf-35-core-right.png): MLE i Triarii.',
    '- [Step 4](../../../context/pass-01/evidence/8.46-step-4-pdf-27.png): ograniczony kontekst AS/LC i odesłanie alokacji.',
    '', 'E916, 64 granice glifów, wszystkie krawędzie, rzeczywisty setup i 20 sytuacji pozostają wyłączone. Żadnych nowych źródeł lub korekt; następna część .4 ma EXP-051–074 i pozostały inwentarz/relacje/lokatory.','']
(OUT/'owner-focus.md').write_text('\n'.join(focus),encoding='utf-8')
save(OUT/'presentation.json',dict(part='M-POC5A.3',owner_instruction='kontynuuj',instruction_is_acceptance=False,
    packet='owner-focus.md',open_result='not_recorded_yet; no owner open proof',
    questions=[dict(id='SEM-P03-POSITIVE',scope='21 exact local reviewed_scopes and 2 context-needs scopes, in both hashes; no full outcomes/records or SEM-002/003/010 choices',status='waiting_review'),
        dict(id='SEM-010',scope='Whether real date/OC need is sufficiently explicit; no actual case or situation outcome',status='waiting_review')],
    owner_decisions=[],reviewer=None))
save(OUT/'manifest.json',dict(id='M-POC5A.3-packet-manifest',evaluation=C['evaluation'],responses=C['responses'],
    prior_acceptance=ref(REV/'owner-decision-01.json'),artifacts=[ref(OUT/f) for f in ['comparisons.json','issues.json','review.md','owner-focus.md','presentation.json']],
    semantic_acceptance='not_performed_for_new_scopes',owner_decisions=[]))
save(REV/'current-state-04.json',dict(id='M-POC5A-current-state-04',card='M-POC5A',part='M-POC5A.3',
    status='partial_waiting_review',previous_state=ref(REV/'current-state-03.json'),
    previous_owner_decision=ref(REV/'owner-decision-01.json'),overlay=ref(OUT/'manifest.json'),
    evaluation=C['evaluation'],responses=C['responses'],summary=summary,owner_accepted_local_groups_per_answer=22,
    no_new_owner_decisions=True,remaining_uncompared_expectations=24,
    pending_previous_parts_preserved=True,resume='Owner exact-scope decisions for part-03 positive set/SEM-010 and prior pending alternatives. Next separate part .4 remains unperformed.'))
print(json.dumps(summary,ensure_ascii=False))
