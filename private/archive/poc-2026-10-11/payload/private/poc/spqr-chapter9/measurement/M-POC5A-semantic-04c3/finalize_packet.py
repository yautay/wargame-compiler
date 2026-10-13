"""Freeze new review/state and update aggregate public continuation."""
from pathlib import Path
import copy, hashlib, json
ROOT=Path(__file__).resolve().parents[5]; P=ROOT/'private/poc/spqr-chapter9'; M=Path(__file__).resolve().parent; R=P/'reviews/semantic-01'; OUT=R/'part-04c3'; D=ROOT/'docs'
def load(p): return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes(); return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=load(OUT/'comparisons.json'); old=load(R/'current-state-19.json')
save(OUT/'manifest.json',dict(id='M-POC5A.4c3-manifest-01',card='M-POC5A.4c3',status='partial_waiting_review',evaluation=c['evaluation'],source=c['source'],responses=c['responses'],
    artifacts=[ref(OUT/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],scope_plan=c['scope_plan'],estimate=ref(M/'start.json'),
    manual_annotations=ref(M/'annotations.json'),locator_diagnostics=ref(M/'locator-diagnostics.json'),owner_decisions=[]))
s=copy.deepcopy(old);s.update(id='M-POC5A-current-state-20',part='M-POC5A.4c3',previous_state=ref(R/'current-state-19.json'),proposal_overlay=ref(OUT/'manifest.json'),
    prior_part_summary=old['summary'],summary=c['summary'],new_owner_decisions=[],newly_decided_assigned_occurrences=0,part_4c3_evaluator_review_complete=True,part_4c3_owner_review_complete=False,
    locator_evaluator_compared_occurrences=124,locator_owner_reviewed_occurrences=86,locator_owner_pending_compared_occurrences=38,remaining_uncompared_locator_occurrences=0,
    locator_remaining_parts={},locator_inherited_issue_observations=['SEM-007'],all_assigned_locator_evaluator_review_complete=True,all_locator_review_pending=False,
    next_part='M-POC5A.4d',parts_4c3_4d_not_executed=False,part_4d_not_executed=True,
    next_action='Owner decisions on .4c3:38 valid geometry/source and envelope failures;36 readable short rasters,2E1011 clipped but readable. Then estimate/split.4d before execution; separateM-POC5B20situations/40assessments. Old unresolved remain open.',
    resume='124/124 assigned locator occurrences compared;86 previous owner scopes,38 new pending. Parent cards partial, no full-content certificate. Two remainingstage5 blocks.4d andM-POC5B; further sessions/hours unknown until estimates.')
assert s['decision']==ref(R/'owner-decision-09.json') and s['relationship_owner_decision']==ref(R/'owner-decision-07.json')
assert s['unresolved_issue_ids']==old['unresolved_issue_ids'] and s['issue_dispositions']==old['issue_dispositions']
save(R/'current-state-20.json',s)
save(M/'stage-5-remaining.json',dict(request_verbatim=load(M/'approval-evidence.json')['owner_reply_verbatim'],current_part='M-POC5A.4c3',current_occurrences_compared=38,
    after_current_packet_owner_decision=[dict(card='M-POC5A.4d',scope='207 inventory positions,66+8 expectations, wider components and previous unresolved; no residual count equated with whole207',sessions='unknown_pending_estimate_and_possible_split'),
    dict(card='M-POC5B',frozen_situations=20,answer_variants=2,assessments=40,sessions='unknown_pending_estimate_and_possible_split')],
    remaining_work_blocks_after_this_part=2,remaining_hours='unknown',no_percentage_completion_claim=True,performed_in_this_session=False,previous_unresolved_remain_open=True))
aggregate='''Właściciel zatwierdził oceny .4c2 i polecił kontynuację oraz wskazanie
pozostałego etapu 5. Owner-decision-09/overlay-09 zapisują 42 ograniczone
oceny: czytelne krótkie rastry/poprawne źródła i geometrie; 40 mierzalnych
ograniczeń pełnych obwiedni oraz 2 przypadki nieocenialne z powodu precyzji.
Łącznie 86 wcześniejszych wystąpień lokatorów ma decyzje właściciela.
To komponenty oceny, nie 86 dobrych lokatorów lub całych poprawnych reguł.

Wykonano ostatnią przypisaną partię .4c3: 22 ID / 38 wystąpień, osobno
16/22. Sześć rekordów tylko po kontekście oceniono w już dostarczonym
wycinku, bez odczytu pozostałej strony. Geometria/źródło zgodne 38;
pełne obwiednie 38 mierzalnych naruszeń. Raster: 36 krótkich cytatów
czytelnych bez zaobserwowanej utraty tuszu, 2 czytelne, ale z uciętymi
dolnymi częściami liter. Oryginalne ramki/odpowiedzi bez naprawy.

Porównano 38 /udostępniono 38 /nowych decyzji właściciela 0 /pending 38.
Faktyczny odczyt plików unknown. Wszystkie 124/124 przypisane wystąpienia
lokatorów rzeczywiście porównano. To nie pełna certyfikacja dowodów,
grafu, ratingów lub znaczenia całych rekordów. current-state-20 prowadzi
nowy prywatny part-04c3: porównania, nieposzerzone wycinki, diagnostyka
granic, dokładne pola/pointers/hash/bajty i owner-focus po ludzku.

257 decyzji komponentów relacji, 264 pary rubryka/EXP, po 63 lokalne
zakresy/3 wymagania źródła na wynik oraz 8 dawnych oczekiwań zachowane.
Starsze nierozstrzygnięcia pozostają otwarte; pełne metryki nieocenialne.
Gold i limity bez zmiany. Nadrzędne karty partial, M-POC5 jedyny next.

Po decyzjach .4c3 pozostają dwa bloki etapu 5: osobna .4d rozliczy
inwentarz/szersze komponenty/pending; potem M-POC5B oceni 20 zamrożonych
sytuacji w dwóch odpowiedziach (40 ocen). Liczba sesji i godzin unknown
do oszacowania zakresu i ewentualnego podziału przed pracą. Nie wykonano
.4d/B, nowych źródeł/ekstrakcji/korekt/czatów/commit/push w tej sesji.
Pomiar: measurement/M-POC5A-semantic-04c3/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4c','.4c2','.4c3']]]
p=D/'STATUS.md'; text=p.read_text(encoding='utf-8'); lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'): lines[i]='- **Wynik M-POC5A:** partial — .4c2 zatwierdzona 42 oceny; .4c3 porównana 22ID/38, nowe pending; wszystkie124/124 przypisane lokatory porównane,86 z decyzjami; dalej .4d iM-POC5B20sytuacji, starsze pending zachowane'
marker='## M-POC5A — przegląd lokatorów .4c2, 2026-10-11'; text='\n'.join(lines)+'\n';assert marker in text
p.write_text(text.replace(marker,'## M-POC5A — ostatnia partia lokatorów .4c3, 2026-10-11\n\n'+aggregate+'\n'+marker,1),encoding='utf-8')
p=D/'ROADMAP.md'; text=p.read_text(encoding='utf-8'); needle='.4c1 zatwierdzona44 oceny komponentów; .4c2 porównana21ID/42, nowe pending; łącznie86/124 porównano; po decyzjach osobna .4c3, pozostałe38 przypisane';assert needle in text
p.write_text(text.replace(needle,'.4c1/.4c2 zatwierdzone86 ocen komponentów; .4c3 porównana22ID/38 nowe pending;124/124 przypisane lokatory porównano; po decyzjach .4d rozliczenie iM-POC5B20sytuacji, oszacować/podzielić przed pracą',1),encoding='utf-8')
for p in files[3:]: p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Zatwierdzenie .4c2 i wykonanie .4c3 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
handoff=D/'handoff/2026-10-11-M-POC5A-semantic-04c3.md';assert not handoff.exists()
handoff.write_text('''# M-POC5A.4c3 — ostatnia przypisana partia lokatorów

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca Codex; właściciel akceptuje znaczenie. Oryginały/źródła/eval-v1
prowadzą hashe w prywatnym manifeście. Artefakty mają prefixpart-04c3
(karta początkowo wymieniała part-4c3). Nowe propozycje waiting_review;
poprzednie42 tylko w pokazanych cechach przyjęte, dawne decyzje zachowane.

Szacunek60–85 minut zapisano przed review; dalszy podział niepotrzebny.
Rzeczywiste logi scripts/check.ps1 offline, lokalneTMP/TEMP i nowybasetemp,
git diff --check oraz audyt niezmienności: nowy pomiar/completion.json.
Czas kalendarzowy osobno; selektory, aktywne czasy, tokeny/cena/budżet unknown.
Kontrole techniczne nie przyjmują znaczenia. Następna czynność: decyzje
obecnego owner-focus, potem oszacowanie pełnej .4d przed wykonaniem.

Limity:1 dodatkowa strona/1reguła/0tabel,1runda/0korekt,0pełnych domknięć,
4częściowe uzupełnienia/4nowe deklaracje, stop rozszerzania na2.
Historyczne naruszenie izolacji nazw/ścieżek potwierdzone; odczyt treści
oceny niezaobserwowany; exposure/cleancontextunknown. Bez certyfikacji
pełnego grafu/rekordów/setupu/sytuacji/budżetu.
''',encoding='utf-8')
p=D/'HANDOFF.md'; history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n')
history=history.replace('[2026-10-11-M-POC5A-semantic-04c2](handoff/2026-10-11-M-POC5A-semantic-04c2.md)','2026-10-11-M-POC5A-semantic-04c2 (`handoff/2026-10-11-M-POC5A-semantic-04c2.md`)',1)
p.write_text('# HANDOFF\n\n- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04c3](handoff/2026-10-11-M-POC5A-semantic-04c3.md)\n- **Wynik:** partial\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'+aggregate+'\n## Historia przed .4c3\n'+history,encoding='utf-8')
save(M/'public-document-artifacts.json',[ref(p) for p in [*files,handoff]])
save(M/'packet-artifacts.json',dict(manifest=ref(OUT/'manifest.json'),current_state=ref(R/'current-state-20.json')))
save(M/'operational-events.json',dict(events=[dict(event='Initial file lookups',detail='Root AGENTS.md absent; two task lookups lacked semantic/ subdirectory; correct existing cards then read. No semantic/source diagnostic failure.')],semantic_revisions=0,extraction_corrections=0,original_responses_modified=False,
    method='Bundled PDF/Pillow read-only diagnostics. Fullpage27 render hash/dimensions metadata only; no pixels/text outside supplied Step4crop read.'))
print('Frozen part04c3/current-state20; owner09 bounded assent, aggregate docs and remainingstage5 recorded.')
