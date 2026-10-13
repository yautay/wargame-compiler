"""Freeze this new packet; retain historical packets and scoped decisions."""
from pathlib import Path
import json, hashlib, copy
ROOT=Path(__file__).resolve().parents[5]; P=ROOT/'private/poc/spqr-chapter9'; M=Path(__file__).resolve().parent; R=P/'reviews/semantic-01'; O=R/'part-04d1'; D=ROOT/'docs'
def load(p): return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes(); return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=load(O/'comparisons.json'); old=load(R/'current-state-21.json')
save(M/'source-views.json',dict(full_supplied_pages=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in range(31,37)],
    supplementary_supplied_step4_crop=ref(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png'),
    method='Manual visual inspection of these already supplied source images. Supplementary Step4 crop checked for AS/LC operator support in X-04; no other part of page27 read.',
    new_sources=0,no_whole_page27_read=True))
save(O/'manifest.json',dict(id='M-POC5A.4d1-manifest-01',card='M-POC5A.4d1',status='partial_waiting_review',source=c['source'],evaluation=c['evaluation'],responses=c['responses'],
    artifacts=[ref(O/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],scope_plan=c['scope_plan'],estimate=c['estimate'],manual_annotations=c['manual_annotations'],
    source_views=ref(M/'source-views.json'),estimate_arithmetic_note=ref(M/'estimate-arithmetic-note.json'),owner_decisions=[]))
s=copy.deepcopy(old); s.update(id='M-POC5A-current-state-22',part='M-POC5A.4d1',previous_state=ref(R/'current-state-21.json'),proposal_overlay=ref(O/'manifest.json'),
    prior_part_summary=old['summary'],summary=c['summary'],new_owner_decisions=[],newly_decided_assigned_occurrences=0,
    part_4d_not_executed=False,part_4d1_evaluator_review_complete=True,part_4d1_owner_review_complete=False,M_POC5A_4d_closed=False,
    inventory_evaluator_compared_assigned_occurrences=78,inventory_owner_reviewed_new_occurrences=0,inventory_owner_pending_compared_occurrences=78,
    inventory_remaining_assigned_occurrences=336,inventory_remaining_assigned_ids=168,inventory_remaining_parts={'M-POC5A.4d2':68,'M-POC5A.4d3':59,'M-POC5A.4d4':41},
    part_4d5_reconciliation_pending=True,new_issue_ids=['SEM-020'],unresolved_issue_ids=old['unresolved_issue_ids']+['SEM-020'],
    next_part='M-POC5A.4d2',next_action='Owner review .4d1:76 bounded supported facets and2 limited main-content omissions with faithful evidence. Then refresh .4d2 estimate before reviewing68 assigned inventory IDs/136occurrences. Older unresolved unchanged.',
    resume='39/207 assigned inventory IDs and78/414 occurrences compared in this separate scope; no duplicate rubric points. Remaining168 IDs split68/59/41, then separate .4d5 reconciliation. M-POC5B20situations/40assessments follows separately; parent cards partial.')
assert s['decision']==ref(R/'owner-decision-10.json') and s['issue_dispositions']==old['issue_dispositions']
save(R/'current-state-22.json',s)
aggregate='''Właściciel zatwierdził .4c3: 38 ograniczonych ocen komponentów.
Wszystkie 124 przypisane wystąpienia lokatorów mają teraz decyzje
właściciela; nie jest to akceptacja całych rekordów ani dobrych ramek.
Oryginalne wady zachowano. Owner-decision-10/overlay-10 prowadzą stan.

Przed review podzielono .4d na pięć osobnych kart, z rozłącznym przydziałem
39/68/59/41 pozycji i osobnym końcowym uzgodnieniem. Wykonano wyłącznie
.4d1: 39 pozycji / 78 wystąpień, osobno 39/39 w obu odpowiedziach.
Rzeczywiście porównano nagłówki, noty i przykłady w dostarczonych źródłach
z oryginalnymi rekordami. Prywatny pakiet part-04d1 zawiera dokładne
zakresy źródłowe, pola, hash/pointer/bajty, niepewności i owner-focus.

Proponowane 76 ocen ograniczonego wsparcia treści oraz 2 oceny częściowego
pominięcia w treści noty, z poprawnym cytatem dowodowym. Struktury danych
nie otrzymują certyfikatu dosłownej transkrypcji. Udostępniono 78,
porównano 78, nowych decyzji właściciela 0, pending 78. Faktyczny odczyt
plików przez właściciela unknown. Starsze nierozstrzygnięcia i wyłączone
pola pozostają otwarte. Pełne metryki not_assessable, gold bez zmiany.

257 wcześniejszych zakresów relacji, 124 zakresy lokatorów, 264 pary
rubryka/oczekiwanie, po 63 lokalne zakresy/3 wymagania źródła i 8 dawnych
oczekiwań pending zachowano. Nie dodaje się punktów za parent/child.
current-state-22 prowadzi nowy wynik. Nadrzędne karty partial;
M-POC5 pozostaje jedynym next.

Po decyzjach .4d1 pozostały cztery karty .4d: 168 pozycji w trzech
partiach 68/59/41, następnie końcowe uzgodnienie. Potem osobne M-POC5B:
20 zamrożonych sytuacji w dwóch odpowiedziach, czyli 40 ocen.
Pierwotny ogólny szacunek .4d 300–420 minut zachowano; suma zapisanych
przed review zakresów pięciu części wynosi 330–430 minut. Szacunek
obecnej części 70–85 minut. Przed kolejną częścią odświeżyć jej szacunek;
nie wykonano jej w tej sesji. Czas aktywny i zgodność budżetu unknown.
Nie wykonano nowych źródeł, ekstrakcji, korekt, czatów, commit/push.
Pomiar: measurement/M-POC5A-semantic-04d1/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4c','.4c3','.4d','.4d1']]]
p=D/'STATUS.md'; t=p.read_text(encoding='utf-8'); lines=t.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'): lines[i]='- **Wynik M-POC5A:** partial — .4c3 zatwierdzona,124 zakresy lokatorów z decyzjami; .4d1 porównana39 pozycji/78 ocen,76 ograniczonych i2 mieszane propozycje pending; pozostałe168 pozycji iuzgodnienie, potemM-POC5B20sytuacji; starsze pending otwarte'
t='\n'.join(lines)+'\n'; marker='## M-POC5A — ostatnia partia lokatorów .4c3, 2026-10-11'; assert marker in t
p.write_text(t.replace(marker,'## M-POC5A — przegląd inwentarza .4d1, 2026-10-11\n\n'+aggregate+'\n'+marker,1),encoding='utf-8')
p=D/'ROADMAP.md';t=p.read_text(encoding='utf-8'); needle='.4c1/.4c2 zatwierdzone86 ocen komponentów; .4c3 porównana22ID/38 nowe pending;124/124 przypisane lokatory porównano; po decyzjach .4d rozliczenie iM-POC5B20sytuacji, oszacować/podzielić przed pracą';assert needle in t
p.write_text(t.replace(needle,'124 zakresy lokatorów z decyzjami; .4d podzielona przed review na pięć kart; .4d1 porównana39 pozycji/78 ocen z propozycjami76+2 pending; pozostałe168 pozycji68/59/41 iuzgodnienie, potemM-POC5B20sytuacji',1),encoding='utf-8')
for p in files[3:]: p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Zatwierdzenie .4c3 i wykonanie .4d1 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
h=D/'handoff/2026-10-11-M-POC5A-semantic-04d1.md';assert not h.exists()
h.write_text('''# M-POC5A.4d1 — przegląd pierwszej partii inwentarza

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca Codex; właściciel akceptuje znaczenie. Nowe propozycje
waiting_review, oryginalne odpowiedzi i wszystkie dawne prywatne artefakty
bez zmian. Hashe prowadzi nowy manifest i audyt niezmienności pomiaru.
Nie przenosić nowej pozytywnej oceny na starsze pending lub szersze pola.

Kontrole: scripts/check.ps1 offline, lokalne TMP/TEMP i nowy basetemp,
git diff --check, walidacja dokładnych bajtów/pointers i końcowy audyt.
Rzeczywiste wyniki i jeden append sessions.jsonl: nowy completion.json.
Selektory modelu/rozumowania, czasy aktywne, tokeny/cena/budżet unknown.
Historyczne naruszenie izolacji nazw/ścieżek zachowane; odczyt treści
oceny niezaobserwowany; exposure/clean context unknown.
Limity zachowano:1 dodatkowa strona/1 reguła/0 tabel,1 runda/0 korekt,
0 pełnych domknięć luk,4 częściowe uzupełnienia/4 nowe deklaracje,stop2.
''',encoding='utf-8')
p=D/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n');history=history.replace('[2026-10-11-M-POC5A-semantic-04c3](handoff/2026-10-11-M-POC5A-semantic-04c3.md)','2026-10-11-M-POC5A-semantic-04c3 (`handoff/2026-10-11-M-POC5A-semantic-04c3.md`)',1)
p.write_text('# HANDOFF\n\n- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04d1](handoff/2026-10-11-M-POC5A-semantic-04d1.md)\n- **Wynik:** partial\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'+aggregate+'\n## Historia przed .4d1\n'+history,encoding='utf-8')
save(M/'public-document-artifacts.json',[ref(p) for p in [*files,h]])
save(M/'packet-artifacts.json',dict(manifest=ref(O/'manifest.json'),current_state=ref(R/'current-state-22.json')))
save(M/'operational-events.json',dict(events=[dict(event='Initial packet-build syntax failure',detail='SyntaxError at reserved keyword class= in dict constructor. Corrected evaluator helper to issue_class before successful packet creation; no source/model edits or extraction.')],semantic_revisions=0,extraction_corrections=0,original_responses_modified=False,source_views=ref(M/'source-views.json')))
print('Frozen part04d1/current-state22. New proposed78, earlier locator scopes124 accepted; remaining168+reconciliation.')
