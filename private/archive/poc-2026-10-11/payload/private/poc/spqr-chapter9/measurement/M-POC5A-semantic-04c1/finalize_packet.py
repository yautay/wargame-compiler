"""Freeze locator review and update public aggregate state."""
from pathlib import Path
import copy,json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c1';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=load(OUT/'comparisons.json');summary=c['summary'];old=load(R/'current-state-15.json')
save(OUT/'manifest.json',dict(id='M-POC5A.4c1-manifest-01',card='M-POC5A.4c1',status='partial_waiting_review',evaluation=c['evaluation'],source=c['source'],responses=c['responses'],
    artifacts=[ref(OUT/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],scope_plan=ref(M/'scope-plan.json'),estimate=ref(M/'start.json'),
    manual_annotations=ref(M/'annotations.json'),locator_diagnostics=ref(M/'locator-diagnostics.json'),owner_decisions=[]))
state=copy.deepcopy(old);state.update(id='M-POC5A-current-state-16',part='M-POC5A.4c1',previous_state=ref(R/'current-state-15.json'),proposal_overlay=ref(OUT/'manifest.json'),
    prior_part_summary=old['summary'],summary=summary,new_owner_decisions=[],newly_decided_assigned_occurrences=0,part_4c1_evaluator_review_complete=True,part_4c1_owner_review_complete=False,
    locator_scope_plan=ref(M/'scope-plan.json'),locator_evaluator_compared_occurrences=44,locator_owner_pending_compared_occurrences=44,locator_owner_reviewed_occurrences=0,
    remaining_uncompared_locator_occurrences=80,all_locator_scope_occurrences=124,locator_remaining_parts={'M-POC5A.4c2':42,'M-POC5A.4c3':38},
    locator_new_issue_ids=[],locator_inherited_issue_observations=['SEM-005','SEM-007'],next_part='M-POC5A.4c2',
    next_action='Owner decision on .4c1 source/geometry, strict44 envelope failures,38 readable raster quotes and6 incomplete raster occurrences. Afterwards separate .4c2,21IDs/42occurrences after estimate.',
    resume='Assigned first locator part22IDs/44occurrences actually compared, all new scopes await owner. Owner-decision07/overlay07 retain257 relation component decisions; old8expectations/SEM-001–013 preserved.80 remaining locator occurrences assigned to.4c2/.4c3; no whole card closure.',
    parts_4c_4d_not_executed=False,parts_4c2_4c3_4d_not_executed=True,M_POC5A_4c_closed=False)
assert state['decision']==ref(R/'owner-decision-07.json') and state['overlay']==ref(R/'owner-review-overlay-07.json')
assert state['unresolved_issue_ids']==old['unresolved_issue_ids'] and state['owner_accepted_relationship_occurrences']==257
save(R/'current-state-16.json',state)
aggregate='''Właściciel zatwierdził trzy rekomendacje .4b3 odpowiedzią „ok kontynuuj”:
68 ograniczonych ocen i4 wystąpienia dwóch osobnych kwestii.
Owner-decision-07/overlay-07 zachowują185 poprzednich zakresów; łącznie257
przypisanych wystąpień relacji ma decyzje o komponentach, nie całych rekordach.
SEM-018/019 rozstrzygnięte tylko w przedstawionych zakresach. Osiem starych
oczekiwań, SEM-001–013 w pozostałych zakresach i wyłączone pola otwarte.

Przed oceną .4c podzielono124 wystąpienia (59/65) na części44/42/38.
Wykonano rzeczywisty przegląd .4c1:22ID/44 wystąpienia, osobno22/22.
Geometria/hash/wymiary i lokalizacja krótkiego cytatu na pełnym źródle
potwierdzone przez oceniającego44. Pełne obwiednie glifów:0/44 mieszczą się.
Raster:38 krótkich cytatów czytelnych bez zaobserwowanej utraty tuszu,
4 z przyciętymi dolnymi częściami liter,2 z brakującą linią cytatu.
Nie utożsamiono wad lokatora z błędami odczytu/znaczenia lub metrykami.

Prywatny part-04c1 zawiera porównania, źródła, dokładne nieposzerzone
wycinki, diagnostyczne widoki granic, ślady pól do bajtów i owner-focus.
Porównano44 /udostępniono44 /nowych decyzji właściciela0 /pending44.
Faktyczny odczyt plików unknown. SEM-005/007 otrzymały ograniczone
propozycje, bez automatycznego zamknięcia. current-state-16 prowadzi
przegląd. Kolejne80 wystąpień niewykonane, jawnie przypisane.

Najbliższa czynność: decyzje według owner-focus .4c1, potem osobna .4c2
21ID/42 wystąpienia, oszacować przed pracą. .4c3 ma22ID/38, .4d iM-POC5B
osobno. M-POC5A/.4/.4b/.4c partial, M-POC5 jedyny next. Bez nowych
źródeł, ekstrakcji, korekt, czatów, commit/push; gold i limity bez zmiany.
Pomiar/logi/audyt: measurement/M-POC5A-semantic-04c1/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4c','.4c1']]]
p=D/'STATUS.md';text=p.read_text(encoding='utf-8');lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'):lines[i]='- **Wynik M-POC5A:** partial — .4b3 zatwierdzona w zakresie68+2+2; łącznie257 komponentowych decyzji relacji; .4c1 faktycznie porównana22ID/44 wystąpienia, nowe oceny pending; następnie osobna .4c2'
text='\n'.join(lines)+'\n';marker='## M-POC5A — decyzja .4b3 i podział .4c, 2026-10-11';assert marker in text
p.write_text(text.replace(marker,'## M-POC5A — przegląd lokatorów .4c1, 2026-10-11\n\n'+aggregate+'\n'+marker,1),encoding='utf-8')
p=D/'ROADMAP.md';text=p.read_text(encoding='utf-8');needle='bieżąca .4c1; reszta i M-POC5B osobno';assert needle in text
p.write_text(text.replace(needle,'.4c1 rzeczywiście porównana22ID/44, nowe decyzje pending; po decyzjach osobna .4c2, pozostałe80 przypisane, reszta i M-POC5B osobno',1),encoding='utf-8')
for p in files[3:]:p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Wykonanie .4c1 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
handoff=D/'handoff/2026-10-11-M-POC5A-semantic-04c1.md';assert not handoff.exists()
handoff.write_text('''# M-POC5A.4c1 — przegląd pierwszej części lokatorów

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca przeglądu: Codex. Właściciel zaakceptował poprzedni dokładny
pakiet relacji; nowe oceny lokatorów nadal czekają na decyzję. Oryginalne
hashe odpowiedzi/eval-v1/źródła oraz zakresy prowadzi prywatny manifest.
Poprzednie pakiety/decyzje/raporty/pomiary pozostają niezmiennymi dowodami.

Szacunek .4c160–220min i podział44/42/38 zapisano przed review; pierwsza
część70–85min. Czas kalendarzowy, rzeczywiste logi scripts/check.ps1 offline
z lokalnymiTMP/TEMP i nowymbasetemp, git diff --check i końcowy audyt
w measurement/M-POC5A-semantic-04c1/completion.json. Niewiadome aktywnego
czasu, selektorów, tokenów/ceny/budżetu bez zmiany. Dwie nieudane czynności
diagnostyczne i sposób naprawy prowadzi operational-events.json, bez
zmiany odpowiedzi lub źródła. Kontrole nie akceptują znaczenia.

Limity bez zmiany:1strona/1reguła/0tabel,1runda/0korekt,0pełnych domknięć,
4częściowe aktualizacje/4nowe deklaracje, stop ekspansji na2. Naruszenie
izolacji nazw/ścieżek context-01 potwierdzone; odczyt treści oceny
niezaobserwowany, exposure/cleancontextunknown. Brak certyfikacji grafu,
ratingów, setupu, sytuacji lub zgodności aktywnego budżetu.
''',encoding='utf-8')
p=D/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n')
history=history.replace('[2026-10-11-M-POC5A-semantic-04b3](handoff/2026-10-11-M-POC5A-semantic-04b3.md)',
    '2026-10-11-M-POC5A-semantic-04b3 (`handoff/2026-10-11-M-POC5A-semantic-04b3.md`)',1)
p.write_text('''# HANDOFF

- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04c1](handoff/2026-10-11-M-POC5A-semantic-04c1.md)
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'\n## Historia przed .4c1\n'+history,encoding='utf-8')
allpublic=[*files,D/'work/tasks/semantic/M-POC5A.4b.md',D/'work/tasks/semantic/M-POC5A.4b3.md',D/'work/tasks/semantic/M-POC5A.4c2.md',D/'work/tasks/semantic/M-POC5A.4c3.md',D/'work/tasks/README.md',handoff]
save(M/'public-document-artifacts.json',[ref(p) for p in allpublic]);save(M/'packet-artifacts.json',dict(manifest=ref(OUT/'manifest.json'),current_state=ref(R/'current-state-16.json')))
print('New frozen packet/current-state16 and aggregate handoff written. Old issues/owner scopes retained.')
