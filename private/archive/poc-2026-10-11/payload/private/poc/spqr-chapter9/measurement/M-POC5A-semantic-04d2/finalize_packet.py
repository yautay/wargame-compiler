"""Freeze the new proposal and aggregate public continuation."""
from pathlib import Path
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';O=R/'part-04d2';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=load(O/'comparisons.json');old=load(R/'current-state-23.json')
save(M/'source-views.json',dict(manually_inspected_supplied_pages=c['visual_source_pages_manually_inspected'],page34_reason='Only assigned C-9.24-05/K-04 continuation assessed; other .4d3 content not reviewed',manually_inspected_graphic_zooms=c['graphic_views_manually_inspected'],graphic_crop_derivation=c['graphic_source_crops'],new_sources=0,graphic_review='Visible glyphs and orientation compared; no rating-position meaning or universal battle compass accepted',source27_read_this_session=False))
save(O/'manifest.json',dict(id='M-POC5A.4d2-manifest-01',card='M-POC5A.4d2',status='partial_waiting_review',source=c['source'],evaluation=c['evaluation'],responses=c['responses'],artifacts=[ref(O/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],scope_plan=c['scope_plan'],scope_assignment=c['scope_assignment'],estimate=c['estimate'],manual_annotations=c['manual_annotations'],source_views=ref(M/'source-views.json'),owner_decisions=[]))
s=copy.deepcopy(old);s.update(id='M-POC5A-current-state-24',part='M-POC5A.4d2',previous_state=ref(R/'current-state-23.json'),proposal_overlay=ref(O/'manifest.json'),prior_part_summary=old['summary'],summary=c['summary'],new_owner_decisions=[],newly_decided_assigned_occurrences=0,
    part_4d2_evaluator_review_complete=True,part_4d2_owner_review_complete=False,inventory_evaluator_compared_assigned_occurrences=214,inventory_owner_reviewed_new_occurrences=0,inventory_owner_reviewed_assigned_occurrences=78,inventory_owner_pending_compared_occurrences=136,inventory_remaining_assigned_occurrences=200,inventory_remaining_assigned_ids=100,
    inventory_remaining_parts={'M-POC5A.4d3':59,'M-POC5A.4d4':41},part_4d5_reconciliation_pending=True,new_issue_ids=[],next_part='M-POC5A.4d3',next_action='Owner review .4d2:136 stated bounded label/clause/row/glyph/orientation/physical-continuation assessments; older pending and missing full results excluded. Then refreshed estimate for separate.4d3 59IDs118occurrences.',
    resume='107/207 IDs214/414 occurrences compared in this separate inventory scope;78 previous owner-scoped judgments and136 new proposals pending. Remaining100IDs59/41 plus.4d5 reconciliation. M-POC5B20situations40assessments follows separately; parent cards partial.')
assert s['decision']==ref(R/'owner-decision-11.json') and s['issue_dispositions']==old['issue_dispositions'] and s['unresolved_issue_ids']==old['unresolved_issue_ids']
save(R/'current-state-24.json',s)
aggregate='''Właściciel zatwierdził .4d1: 76 ograniczonych ocen treści/roli oraz
2 ograniczone pominięcia w treści przy poprawnym cytacie dowodowym.
Owner-decision-11/overlay-11 prowadzą 78 przyjętych zakresów inwentarza;
starsze nierozstrzygnięcia i oryginalne odpowiedzi zachowano.

Wykonano całą przypisaną .4d2: 68 pozycji /136 wystąpień, osobno68/68.
Rzeczywiście porównano oznaczenia, dokładne klauzule, tabelę/wiersze,
grafikę i fizyczne kontynuacje z dostarczonym źródłem i obiema odpowiedziami.
Nowy prywatny part-04d2 zawiera dokładne źródła, pola/hash/pointer/bajty,
oceny i wyłączenia oraz czytelny owner-focus. Przyjęcie parent nie
zastępuje oceny child. Treść, widoczne napisy i znaczenie ratingów osobno.

Proponowane136 ograniczonych ocen; nie wykazano nowego błędu znaczenia
w tych wskazanych cechach. Porównano136 /udostępniono136 /nowych decyzji
właściciela0 /pending136. Faktyczny odczyt plików unknown. Starsze8
oczekiwań/13kwestii pozostają otwarte; nie wybrano ich wariantów przez
nową ocenę literalną. Pełne zależne wyniki nadal wymagają brakujących źródeł.

Łącznie .4d:107/207 pozycji,214/414 wystąpień porównano;78 wcześniej
przyjętych zakresów i136 nowych pending. Pozostałe100 pozycji w osobnych
.4d3(59) i.4d4(41), potem.4d5 końcowe uzgodnienie. Następnie oddzielne
M-POC5B20 zamrożonych sytuacji w obu odpowiedziach, czyli40 ocen.
Nie wykonano tych kart w tej sesji. Odświeżony szacunek .4d2 75–90minut
zapisano przed review; następna część wymaga szacunku przed pracą.

257 zakresów relacji,124 zakresy lokatorów,264 pary rubryka/oczekiwanie,
po63 lokalne zakresy/3 wymagania źródła na wynik zachowane bez ponownego
punktowania. Gold i limity bez zmiany, pełne metryki not_assessable.
current-state-24 prowadzi nowy wynik; karty nadrzędne partial,
M-POC5 jedyny next. Aktywne czasy/selektory/tokeny/cena/budżet unknown.
Bez nowych źródeł/ekstrakcji/korekt/czatów/commit/push.
Pomiar: measurement/M-POC5A-semantic-04d2/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4d','.4d1','.4d2']]]
p=D/'STATUS.md';t=p.read_text(encoding='utf-8');lines=t.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'):lines[i]='- **Wynik M-POC5A:** partial — .4d1 zatwierdzona78 zakresów; .4d2 porównana68 pozycji/136 ograniczonych ocen pending; razem107/207 pozycji,214/414 wystąpień; pozostałe100 pozycji iuzgodnienie, potemM-POC5B20sytuacji; starsze pending otwarte'
t='\n'.join(lines)+'\n';marker='## M-POC5A — przegląd inwentarza .4d1, 2026-10-11';assert marker in t
p.write_text(t.replace(marker,'## M-POC5A — przegląd inwentarza .4d2, 2026-10-11\n\n'+aggregate+'\n'+marker,1),encoding='utf-8')
p=D/'ROADMAP.md';t=p.read_text(encoding='utf-8');needle='.4d1 porównana39 pozycji/78 ocen z propozycjami76+2 pending; pozostałe168 pozycji68/59/41 iuzgodnienie, potemM-POC5B20sytuacji';assert needle in t
p.write_text(t.replace(needle,'.4d1 zatwierdzona78 zakresów; .4d2 porównana68 pozycji/136 ograniczonych ocen pending;107/207 pozycji214/414 wystąpień porównano; pozostałe100 pozycji59/41 iuzgodnienie, potemM-POC5B20sytuacji',1),encoding='utf-8')
for p in files[3:]:p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Zatwierdzenie .4d1 i wykonanie .4d2 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
h=D/'handoff/2026-10-11-M-POC5A-semantic-04d2.md';assert not h.exists()
h.write_text('''# M-POC5A.4d2 — druga partia inwentarza

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca Codex; znaczenie akceptuje właściciel. Nowe136 propozycji
waiting_review. Każda ocena ma niepewności i wyłączenia; nie rozszerzać
jej na dawne pending lub cały parent. 25 różnych mapped rekordów na
wariant; dzieci i wiersze nie zwiększają liczby punktów reguł.

Kontrole: scripts/check.ps1 offline, lokalneTMP/TEMP i nowybasetemp,
git diff --check, walidacja source/helpers/pointers/rawbytes i audyt
niezmienności. Rzeczywiste wyniki i jedenappend sessions.jsonl w nowym
completion.json. Czas kalendarzowy osobno od nieznanego aktywnego czasu.

Historyczne naruszenie izolacji nazw/ścieżek zachowane; odczyt treści
oceny niezaobserwowany, exposure/cleancontext unknown. Limity bez zmian:
1 dodatkowa strona/1reguła/0tabel,1runda/0korekt,0pełnych domknięć,
4częściowe uzupełnienia/4nowe deklaracje,stoprozszerzania2.
''',encoding='utf-8')
p=D/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n');history=history.replace('[2026-10-11-M-POC5A-semantic-04d1](handoff/2026-10-11-M-POC5A-semantic-04d1.md)','2026-10-11-M-POC5A-semantic-04d1 (`handoff/2026-10-11-M-POC5A-semantic-04d1.md`)',1)
p.write_text('# HANDOFF\n\n- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04d2](handoff/2026-10-11-M-POC5A-semantic-04d2.md)\n- **Wynik:** partial\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'+aggregate+'\n## Historia przed .4d2\n'+history,encoding='utf-8')
save(M/'public-document-artifacts.json',[ref(p) for p in [*files,h]])
save(M/'packet-artifacts.json',dict(manifest=ref(O/'manifest.json'),current_state=ref(R/'current-state-24.json')))
save(M/'operational-events.json',dict(events=[dict(event='Initial source-display helper lacked graphic case',detail='read_slice.py attempted transcription key for D-01 evidence, which is a graphic envelope with no text transcription. KeyError retained in tool history. Display helper changed to show original graphic inventory and supplied image instead; remaining graphic/continuation rows then actually read.'),dict(event='Generated diagnostic image link corrected',detail='Three new comparison links initially used crop filenames relative to review folder; changed to exact absolute workspace image paths before freezing packet. No response/source changes.')],semantic_revisions=0,extraction_corrections=0,original_responses_modified=False,source_views=ref(M/'source-views.json')))
print('Frozen part04d2/current-state24; previous78 owner-scoped, new136 pending; remaining100+reconciliation.')
