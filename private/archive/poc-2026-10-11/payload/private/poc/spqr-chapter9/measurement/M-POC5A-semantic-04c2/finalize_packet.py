"""Freeze new locator proposal/state and aggregate documentation."""
from pathlib import Path
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';OUT=R/'part-04c2';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
c=load(OUT/'comparisons.json');summary=c['summary'];old=load(R/'current-state-17.json')
save(OUT/'manifest.json',dict(id='M-POC5A.4c2-manifest-01',card='M-POC5A.4c2',status='partial_waiting_review',evaluation=c['evaluation'],source=c['source'],responses=c['responses'],
    artifacts=[ref(OUT/f) for f in ['comparisons.json','comparisons.md','review.md','issues.json','owner-focus.md','presentation.json']],scope_plan=c['scope_plan'],estimate=ref(M/'start.json'),
    manual_annotations=ref(M/'annotations.json'),locator_diagnostics=ref(M/'locator-diagnostics.json'),owner_decisions=[]))
state=copy.deepcopy(old);state.update(id='M-POC5A-current-state-18',part='M-POC5A.4c2',previous_state=ref(R/'current-state-17.json'),proposal_overlay=ref(OUT/'manifest.json'),
    prior_part_summary=old['summary'],summary=summary,new_owner_decisions=[],newly_decided_assigned_occurrences=0,part_4c2_evaluator_review_complete=True,part_4c2_owner_review_complete=False,
    locator_evaluator_compared_occurrences=86,locator_owner_pending_compared_occurrences=42,locator_owner_reviewed_occurrences=44,
    remaining_uncompared_locator_occurrences=38,locator_remaining_parts={'M-POC5A.4c3':38},locator_inherited_issue_observations=['SEM-007'],next_part='M-POC5A.4c3',
    next_action='Owner decisions on.4c2:42 readable short rasters/source/geometry,40 measurable envelope failures,2E962 numericprecision unresolved. Then separate.4c3,22IDs/38occurrences after estimate.',
    resume='Owner-decision08 accepted previous44 mixed locator assessments;42 new.4c2 occurrences actually compared awaiting owner.86/124 compared; remaining38 assigned.4c3. Older pending, defects and257 relation component decisions preserved; no full card closure.',
    parts_4c2_4c3_4d_not_executed=False,parts_4c3_4d_not_executed=True)
assert state['decision']==ref(R/'owner-decision-08.json') and state['overlay']==ref(R/'owner-review-overlay-08.json') and state['unresolved_issue_ids']==old['unresolved_issue_ids']
save(R/'current-state-18.json',state)
aggregate='''Właściciel zatwierdził oceny .4c1 odpowiedzią „zatwierdzam i kontynuuj”.
Owner-decision-08/overlay-08 zapisują44 rozłączne oceny komponentów:
poprawną geometrię,38 czytelnych krótkich rastrów i6 niepełnych;
wszystkie44 ścisłe naruszenia obwiedni zachowane. To nie44 dobre lokatory
lub poprawne całe reguły. Wady oryginalnych lokatorów nie zostały naprawione.
SEM-005 potwierdzony tylko jako wada dowodu, SEM-007 częściowo oceniony;
inne wcześniejsze nierozstrzygnięcia i8 oczekiwań pozostają otwarte.

Wykonano rzeczywisty przegląd .4c2:21ID/42 wystąpienia, osobno21/21.
Każdy krótki cytat odnaleziono w źródle; hash/wymiary/geometria zgodne42.
Wszystkie42 krótkie rastry czytelne bez zaobserwowanej utraty tuszu.
Pełne obwiednie:40 mierzalnych naruszeń;2 wystąpienia mają wyłącznie
różnicę na poziomie reprezentacji zmiennoprzecinkowej i ścisła ocena
pozostaje nieocenialna z powodu precyzji. Raw porównania bez tolerancji
zachowano, bez poszerzania ramki lub automatycznego ścisłego pass.
Wady/niepewności lokatora nie są automatycznie błędami znaczenia.

Prywatny part-04c2 ma każde porównanie, źródła, obrazy granic i dokładne
nieposzerzone wycinki, pola/pointers/hash/bajty oraz owner-focus.
Porównano42 /udostępniono42 /nowych decyzji właściciela0 /pending42.
Faktyczne otwarcie/odczyt plików unknown. current-state-18 prowadzi
przegląd. Łącznie86/124 przypisanych wystąpień lokatorów porównano,
44 poprzednie ma decyzje właściciela.38 w .4c3 nadal niewykonane.

257 komponentowych decyzji relacji,264 pary rubryka/EXP, po63 lokalne
zakresy/3 wymagania źródła na wynik zachowane. Pełne wyniki/pola/aliasy,
ratingi, setup, sytuacje i metryki wyłączone. Gold i limity bez zmiany.
Najbliższy krok: decyzje według owner-focus .4c2, potem osobna .4c3:
22ID/38 wystąpień po oszacowaniu. .4d iM-POC5B osobno; nadrzędne karty
partial, M-POC5 jedyny next. Bez nowych źródeł/ekstrakcji/korekt/czatów/
commit/push. Pomiar: measurement/M-POC5A-semantic-04c2/.
'''
files=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4c','.4c1','.4c2']]]
p=D/'STATUS.md';text=p.read_text(encoding='utf-8');lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'):lines[i]='- **Wynik M-POC5A:** partial — .4c1 zatwierdzona44 oceny komponentów; .4c2 porównana21ID/42, nowe decyzje pending; łącznie86/124 lokatorów porównano; po decyzjach osobna .4c3, starsze pending zachowane'
text='\n'.join(lines)+'\n';marker='## M-POC5A — przegląd lokatorów .4c1, 2026-10-11';assert marker in text
p.write_text(text.replace(marker,'## M-POC5A — przegląd lokatorów .4c2, 2026-10-11\n\n'+aggregate+'\n'+marker,1),encoding='utf-8')
p=D/'ROADMAP.md';text=p.read_text(encoding='utf-8');needle='.4c1 rzeczywiście porównana22ID/44, nowe decyzje pending; po decyzjach osobna .4c2, pozostałe80 przypisane';assert needle in text
p.write_text(text.replace(needle,'.4c1 zatwierdzona44 oceny komponentów; .4c2 porównana21ID/42, nowe pending; łącznie86/124 porównano; po decyzjach osobna .4c3, pozostałe38 przypisane',1),encoding='utf-8')
for p in files[3:]:p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n\n## Zatwierdzenie .4c1 i wykonanie .4c2 — 2026-10-11\n\n'+aggregate,encoding='utf-8')
handoff=D/'handoff/2026-10-11-M-POC5A-semantic-04c2.md';assert not handoff.exists()
handoff.write_text('''# M-POC5A.4c2 — druga część przeglądu lokatorów

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca: Codex; znaczenie przyjmuje właściciel. Zgoda dotyczy poprzedniej
części; nowe oceny .4c2 waiting_review. Oryginalne hashe odpowiedzi,
eval-v1, źródła i przydziału prowadzi prywatny manifest. Dawne dowody,
decyzje/raporty/pomiary niezmienione. Artefakty mają spójny prefixpart-04c2.

Szacunek60–80 minut zapisano przed review; dalszy podział nie był potrzebny.
Rzeczywiste logi scripts/check.ps1 offline, lokalneTMP/TEMP/nowybasetemp,
git diff --check, czas kalendarzowy i końcowy audyt w nowym pomiarze
measurement/M-POC5A-semantic-04c2/completion.json. Kontrole nie akceptują
znaczenia. Aktywne czasy/selektory/tokens/cena/budżet unknown.

Limity bez zmiany:1strona/1reguła/0tabel,1runda/0korekt,0pełnych domknięć,
4częściowe aktualizacje/4nowe deklaracje, stop ekspansji na2.
Naruszenie izolacji nazw/ścieżek dawnego context-01 potwierdzone; odczyt
treści oceny niezaobserwowany; exposure/cleancontextunknown. Bez
certyfikacji całego grafu, ratingów, setupu, sytuacji lub aktywnego budżetu.
''',encoding='utf-8')
p=D/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n')
history=history.replace('[2026-10-11-M-POC5A-semantic-04c1](handoff/2026-10-11-M-POC5A-semantic-04c1.md)',
    '2026-10-11-M-POC5A-semantic-04c1 (`handoff/2026-10-11-M-POC5A-semantic-04c1.md`)',1)
p.write_text('''# HANDOFF

- **Ostatnia sesja:** [2026-10-11-M-POC5A-semantic-04c2](handoff/2026-10-11-M-POC5A-semantic-04c2.md)
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'\n## Historia przed .4c2\n'+history,encoding='utf-8')
save(M/'public-document-artifacts.json',[ref(p) for p in [*files,handoff]]);save(M/'packet-artifacts.json',dict(manifest=ref(OUT/'manifest.json'),current_state=ref(R/'current-state-18.json')))
print('New frozen part04c2 packet/current-state18 and aggregate handoff saved; owner08/prior assessments unchanged.')
