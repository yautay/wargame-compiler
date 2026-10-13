"""Advance public aggregate pointers; keep all private rule details private."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[5]
M=Path(__file__).resolve().parent
docs=ROOT/'docs'
files=[docs/'STATUS.md',docs/'ROADMAP.md',docs/'HANDOFF.md',docs/'work/tasks/M-POC5A.md',
       *[docs/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4b','.4b1']]]
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
before=[ref(p) for p in files]
assert not (M/'public-documents-before.json').exists()
(M/'public-documents-before.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
aggregate='''Właściciel przyjął sześć przedstawionych rekomendacji odpowiedzią
„zgodnie z rekomendacją”. Nowa owner-decision-05, overlay-05 i current-state-11
pod prywatnym reviews/semantic-01/ zapisują 9 wydzielonych wystąpień (4/5)
z ocenami mieszanymi oraz 2 dodatkowe wystąpienia zamrożonej wzmianki.
116 wcześniejszych pozytywnych zakresów zachowano. Wszystkie 125 przypisanych
wystąpień .4b1 ma decyzje o dokładnych zakresach; nie oznacza to 125 całych
poprawnych relacji. Rozstrzygnięcia odnotowują błędne klasyfikacje i
niewystarczającą deklarację blokady, bez poprawiania odpowiedzi.

SEM-014–016 rozstrzygnięto w przedstawionych zakresach, SEM-004 częściowo;
reszta SEM-001–013 i osiem wcześniejszych oczekiwań pozostają otwarte.
Po 63 lokalne zakresy / 3 wymagania źródła na wynik i 264 pary rubryka/EXP
bez zmiany. Wyłączone pola, pełne wyniki, lokatory i metryki nie otrzymują
akceptacji. Pozostałe .4b2/.4b3 mają 132 wystąpienia do pełnego przeglądu;
dodatkowa decyzja o wzmiance nie wykonuje całej następnej partii.

Następna osobna .4b2: 30 ID / 60 wystąpień według istniejącego scope-plan,
z oszacowaniem przed wykonaniem. .4b3/.4c/.4d i M-POC5B osobno.
M-POC5A/.4/.4b partial, M-POC5 jedyny next. Oryginały, źródła, eval-v1,
poprzednie decyzje i pomiary zachowano; bez nowych źródeł, ekstrakcji,
korekt, czatów i commit/push. Pomiar: measurement/M-POC5A-owner-review-005/.
'''
p=docs/'STATUS.md';text=p.read_text(encoding='utf-8')
lines=text.splitlines()
for i,line in enumerate(lines):
    if line.startswith('- **Wynik M-POC5A:**'):
        lines[i]='- **Wynik M-POC5A:** partial — .4b1: decyzje o dokładnych zakresach wszystkich 125 przypisanych wystąpień (116 wcześniejszych pozytywnych + 9 nowych mieszanych), dodatkowo 2 wystąpienia wzmianki; rekomendacje 1–6 przyjęte; wcześniejsze nierozstrzygnięcia zachowane; następna osobna .4b2'
text='\n'.join(lines)+'\n'
marker='## M-POC5A — akceptacja pozytywnego zakresu .4b1, 2026-10-11'
assert marker in text
text=text.replace(marker,'## M-POC5A — rozstrzygnięcie rekomendacji 1–6, 2026-10-11\n\n'+aggregate+'\n'+marker,1)
p.write_text(text,encoding='utf-8')
p=docs/'ROADMAP.md';text=p.read_text(encoding='utf-8')
old='właściciel przyjął 116 dokładnych zakresów relacji (56/60), 9 wydzielonych wystąpień pending'
assert old in text
text=text.replace(old,'właściciel przyjął 116 pozytywnych zakresów (56/60) i rozstrzygnął 9 wydzielonych wystąpień z ocenami mieszanymi oraz 2 dodatkowe wystąpienia wzmianki; wcześniejsze pending i wyłączone pola zachowane',1)
p.write_text(text,encoding='utf-8')
append='\n## Rozstrzygnięcie rekomendacji 1–6 — 2026-10-11\n\n'+aggregate
for p in files[3:]:
    p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n'+append,encoding='utf-8')
new=docs/'handoff/2026-10-11-M-POC5A-owner-review-05.md'
assert not new.exists()
new.write_text('''# M-POC5A — rozstrzygnięcie sześciu rekomendacji .4b1

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'''
Wykonawca zapisu: Codex; decyzja znaczenia: właściciel w tym czacie.
Wejścia i hashe: nowy prywatny owner-decision-05 odsyła do niezmienionych
obu oryginałów, eval-v1, pakietu part-04b1 oraz poprzedniej decyzji i stanu.
Pełny zakres zatwierdzenia i wyłączenia zapisano w owner-review-summary-05.md.
Faktyczne otwarcie plików unknown; zgodę udzielono po wyjaśnieniu w czacie.

Kontrole, audyt niezmienności i append-only pomiar sesji: prywatny katalog
measurement/M-POC5A-owner-review-005/, completion.json i logi. Kontrole
potwierdzają spójność zapisu, nie poszerzają semantycznej akceptacji.
Szacunek zapisu i weryfikacji 10–20 minut; rzeczywisty przedział kalendarzowy
w completion.json, czas aktywny/tokeny/cena i zgodność budżetu unknown.
Ta sesja nie wykonuje .4b2, .4b3 lub innych kart.

Limity kontekstu i korekt bez zmian: 1 strona / 1 reguła / 0 tabel,
1 runda / 0 korekt, 0 pełnych domknięć, 4 częściowe aktualizacje i 4 nowe
deklaracje. Trzeciego źródła nie pozyskano. Stan izolacji i wcześniejsze
niewiadome zachowane, bez certyfikacji pełnego grafu lub budżetu.
''',encoding='utf-8')
p=docs/'HANDOFF.md';history=p.read_text(encoding='utf-8').removeprefix('# HANDOFF\n')
history=history.replace('[2026-10-11-M-POC5A-owner-review-04](handoff/2026-10-11-M-POC5A-owner-review-04.md)',
    '2026-10-11-M-POC5A-owner-review-04 (`handoff/2026-10-11-M-POC5A-owner-review-04.md`)',1)
p.write_text('''# HANDOFF

- **Ostatnia sesja:** [2026-10-11-M-POC5A-owner-review-05](handoff/2026-10-11-M-POC5A-owner-review-05.md)
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

'''+aggregate+'\n## Historia przed rozstrzygnięciem rekomendacji 1–6\n'+history,encoding='utf-8')
assert not (M/'public-document-artifacts.json').exists()
(M/'public-document-artifacts.json').write_text(json.dumps([ref(p) for p in [*files,new]],indent=2)+'\n',encoding='utf-8')
print('Updated aggregate state and new handoff; preserved previous handoff file.')
