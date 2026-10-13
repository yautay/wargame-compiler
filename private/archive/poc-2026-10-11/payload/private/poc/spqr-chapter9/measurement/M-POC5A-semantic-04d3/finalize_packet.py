"""Freeze additive review/state; public documents contain aggregates only."""
from pathlib import Path
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';O=R/'part-04d3';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=load(O/'comparisons.json');old=load(R/'current-state-25.json')
save(M/'source-views.json',dict(manually_inspected_supplied_pages=c['visual_source_pages_manually_inspected'],manually_inspected_graphic_zooms=c['graphic_views_manually_inspected'],graphic_crop_derivation=c['graphic_source_crops'],supplementary_already_supplied_step4_crop=ref(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png'),new_sources=0,no_whole_page27_read=True,graphic_review='Layout/captions/selected glyphs supported; rating meanings and exact upper/lower counter identity tracking between panels excluded.'))
save(O/'manifest.json',dict(id='M-POC5A.4d3-manifest-01',card='M-POC5A.4d3',status='partial_waiting_review',source=c['source'],evaluation=c['evaluation'],responses=c['responses'],artifacts=[ref(O/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],scope_plan=c['scope_plan'],scope_assignment=c['scope_assignment'],estimate=c['estimate'],manual_annotations=c['manual_annotations'],source_views=ref(M/'source-views.json'),owner_decisions=[]))
s=copy.deepcopy(old);s.update(id='M-POC5A-current-state-26',part='M-POC5A.4d3',previous_state=ref(R/'current-state-25.json'),proposal_overlay=ref(O/'manifest.json'),prior_part_summary=old['summary'],summary=c['summary'],new_owner_decisions=[],newly_decided_assigned_occurrences=0,part_4d3_evaluator_review_complete=True,part_4d3_owner_review_complete=False,
    inventory_evaluator_compared_assigned_occurrences=332,inventory_owner_reviewed_new_occurrences=0,inventory_owner_reviewed_assigned_occurrences=214,inventory_owner_pending_compared_occurrences=118,inventory_remaining_assigned_occurrences=82,inventory_remaining_assigned_ids=41,inventory_remaining_parts={'M-POC5A.4d4':41},part_4d5_reconciliation_pending=True,new_issue_ids=['SEM-021'],unresolved_issue_ids=old['unresolved_issue_ids']+['SEM-021'],next_part='M-POC5A.4d4',
    next_action='Owner review.4d3:114 exact bounded facets and2mixedparent+2omittedexplanatorychild judgments for one historical explanation per answer. Old unresolved unchanged. Then estimate separate.4d4 41IDs82occurrences.',resume='166/207 IDs332/414 inventory occurrences compared;214 prior owner scopes and118 new proposals. Remaining41IDs then.4d5 reconciliation; separateM-POC5B20situations40assessments. Parent cards partial.')
assert s['decision']==ref(R/'owner-decision-12.json') and s['issue_dispositions']==old['issue_dispositions'];save(R/'current-state-26.json',s)
aggregate='''Właściciel zatwierdził .4d2:136 ograniczonych ocen. Owner-decision-12
i overlay-12 prowadzą razem214 przyjętych zakresów inwentarza; nie całe
rekordy ani dodatkowe punkty. Starsze nierozstrzygnięcia zachowano.

Wykonano całą .4d3:59 pozycji/118 wystąpień, osobno59/59. Rzeczywiste
porównania obejmują oznaczenia, klauzule i osiem dokładnych child spans,
diagram, dwa podpisy oraz fizyczną kontynuację. Prywatny part-04d3
ma exactsource/pole/hash/pointer/bajty i opis decyzji po ludzku.

Proponowane114 ocen ograniczonego wsparcia oraz2 mieszane oceny całego
akapitu i2 oceny pominiętego fragmentu wyjaśnienia. To jedna pominięta
klauzula na odpowiedź, nie cztery niezależne błędy; operatywna część
zachowana, źródłowy obraz pozostaje dostępny. Nie wykazano przez to
błędnego wyniku gry. Porównano118/udostępniono118/nowych decyzji0/pending118.
Faktyczny odczyt plików unknown. Starsze8 oczekiwań/13 kwestii pozostają
otwarte; nowa obserwacja osobno waiting_review. Nie wybrano starych wariantów.

Łącznie .4d:166/207 pozycji i332/414 wystąpień porównano;214 zakresów
wcześniej przyjętych i118 nowych pending. Pozostała .4d4(41pozycji),
następnie .4d5 końcowe uzgodnienie. Potem osobneM-POC5B20 zamrożonych
sytuacji w obu odpowiedziach(40ocen). Tych kart nie wykonano w tej sesji.
Szacunek.4d3 75–90minut zapisano przed review; następna część wymaga
szacunku przed pracą. Aktywne czasy/selektory/tokeny/cena/budżet unknown.

257 zakresów relacji,124 zakresy lokatorów,264 pary rubryka/oczekiwanie
oraz po63 lokalne zakresy/3 wymagania źródła na wynik zachowano bez
ponownego punktowania. Gold i limity bez zmiany, pełne metryki nieocenialne.
current-state-26 prowadzi wynik, karty nadrzędne partial, M-POC5 jedyny next.
Bez nowych źródeł/ekstrakcji/korekt/czatów/commit/push.
Pomiar: measurement/M-POC5A-semantic-04d3/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4d','.4d2','.4d3']]]
p=D/'STATUS.md';t=p.read_text(encoding='utf-8');lines=t.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'):lines[i]='- **Wynik M-POC5A:** partial — .4d2 zatwierdzona136 zakresów; .4d3 porównana59 pozycji/118 ocen,114 ograniczone i4 mieszane zakresy pending; razem166/207 pozycji332/414 wystąpień; pozostałe41 pozycji iuzgodnienie, potemM-POC5B20sytuacji; starsze pending otwarte'
t='\n'.join(lines)+'\n';marker='## M-POC5A — przegląd inwentarza .4d2, 2026-10-11';assert marker in t;p.write_text(t.replace(marker,'## M-POC5A — przegląd inwentarza .4d3, 2026-10-11\n\n'+aggregate+'\n'+marker,1),encoding='utf-8')
p=D/'ROADMAP.md';t=p.read_text(encoding='utf-8');needle='.4d1 zatwierdzona78 zakresów; .4d2 porównana68 pozycji/136 ograniczonych ocen pending;107/207 pozycji214/414 wystąpień porównano; pozostałe100 pozycji59/41 iuzgodnienie, potemM-POC5B20sytuacji';assert needle in t
p.write_text(t.replace(needle,'.4d1/.4d2 zatwierdzone214 zakresów; .4d3 porównana59 pozycji/118 ocen(114+2mieszaneparent+2child), nowe pending;166/207 pozycji332/414 wystąpień porównano; pozostałe41 pozycji iuzgodnienie, potemM-POC5B20sytuacji',1),encoding='utf-8')
for p in files[3:]:p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Zatwierdzenie .4d2 i wykonanie .4d3 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
h=D/'handoff/2026-10-11-M-POC5A-semantic-04d3.md';assert not h.exists();h.write_text('''# M-POC5A.4d3 — trzecia partia inwentarza

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca Codex; znaczenie akceptuje właściciel. Nowe118 propozycji
waiting_review. 20 mapped rekordów na wariant; parent/child nie zwiększają
punktów reguł i nie podwajają obserwacji pominięcia. Dokładne zakresy
źródłowe prowadzą przed containing parent, także przy przecięciu kolumn.

Kontrole: scripts/check.ps1 offline, lokalneTMP/TEMP i nowybasetemp,
git diff --check, walidacja helpers/pointers/bajty/crops i audyt
niezmienności. Rzeczywiste wyniki i jedenappend sessions.jsonl w nowym
completion.json. Czas kalendarzowy osobno od nieznanego aktywnego czasu.

Historyczne naruszenie izolacji nazw/ścieżek zachowane; odczyt treści
oceny niezaobserwowany, exposure/cleancontext unknown. Limity zachowane:
1 dodatkowa strona/1reguła/0tabel,1runda/0korekt,0pełnych domknięć,
4częściowe uzupełnienia/4nowe deklaracje,stoprozszerzania2.
''',encoding='utf-8')
p=D/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n');history=history.replace('[2026-10-11-M-POC5A-semantic-04d2](handoff/2026-10-11-M-POC5A-semantic-04d2.md)','2026-10-11-M-POC5A-semantic-04d2 (`handoff/2026-10-11-M-POC5A-semantic-04d2.md`)',1)
p.write_text('# HANDOFF\n\n- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04d3](handoff/2026-10-11-M-POC5A-semantic-04d3.md)\n- **Wynik:** partial\n- **Następny milestone:** M-POC5\n- **Następna karta:** M-POC5A\n\n'+aggregate+'\n## Historia przed .4d3\n'+history,encoding='utf-8')
save(M/'public-document-artifacts.json',[ref(p) for p in [*files,h]]);save(M/'packet-artifacts.json',dict(manifest=ref(O/'manifest.json'),current_state=ref(R/'current-state-26.json')))
save(M/'operational-events.json',dict(events=[],method='New evaluator helpers bind manual annotations to original records without extraction or repair; read-only source crop for diagram legibility.',semantic_revisions=0,extraction_corrections=0,original_responses_modified=False,source_views=ref(M/'source-views.json')))
print('Frozen part04d3/state26;114 bounded+2mixedparent+2child pending; earlier214 scoped accepted,remaining41+reconciliation.')
