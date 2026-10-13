# M-POC5A.4b1: Relacje — partia 1

- **ID:** M-POC5A.4b1
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** [M-POC5A.4b](M-POC5A.4b.md), stan current-state-07.json lub nowszy.

## Cel i pytanie eksperymentalne

Rzeczywisty przegląd przypisanych relacji obu odpowiedzi. Podział z
2026-10-11 PRZED wykonaniem: 65 różnych ID,
60 wystąpień first-001 i 65 context-01.
Typy/statusy ekstraktora służą wyłącznie przydzieleniu zakresu, nie ocenie.

## Dokładne pliki do przeczytania

Bootstrap, SESSION-PLAYBOOK, STATUS, HANDOFF i aktualny handoff, ROADMAP,
POC-PLAN, ADR-0039; karty M-POC5A/.4/.4b. Prywatnie stan, decyzje i overlay,
oba run/proposal/provenance/report, eval-v1 i źródła. Dokładny przydział:
private/poc/spqr-chapter9/measurement/M-POC5A-part04b-preparation-001/scope-plan.json.

## Wejścia i wersja oceny

Niezmienione first-001/context-01 i eval-v1; osobne hashe i bajty.
63 zakresy lokalne i 3 wymagania źródła przyjęte na wynik; żadna relacja
nie dziedziczy przez to akceptacji. 8 oczekiwań nadal pending.

## Wymagane działania

Sprawdzić dla każdego ID źródłowy zakres, tożsamość/zakres celu, kierunek,
rodzaj, jawność, konieczność i wpływ brakującego celu. Transkrypcję odróżnić
od interpretacji; brak źródła od pominięcia relacji. Dwa osobne wyniki na
eval-v1, z pointer/hash/bajtami, recenzentem, zakresem i niepewnościami.
W tej pierwszej partii dodatkowo porównać 5/3 zamrożonych par wykonawczych,
7 wzmianek i 7 kontynuacji oraz brakujące krytyczne pary, pięć nowych
krawędzi kontekstu i nierozstrzygniętą ścieżkę trzech kroków. Nie naprawiać
odpowiedzi i nie nadawać automatycznych TP/FP/FN.
Jedna część do 90 minut. Jeśli oszacowany zakres jest większy, podzielić
go z pełnymi listami ID PRZED przeglądem znaczenia i zaktualizować karty,
ROADMAP i STATUS. Nie zastępować realnego review samym rejestrem pending.

## Artefakty wyjściowe i lokalizacje

Nowy reviews/semantic-01/part-04b1/ (comparisons, review, issues,
owner-focus, presentation, manifest), additive current-state i nowy pomiar
M-POC5A-semantic-04b1/. Wpis sessions.jsonl append-only.

## Kryteria zakończenia i kontrole

Wszystkie przypisane ID rozliczone źródłowo, ocenione lub jawnie blokowane;
brak automatycznej akceptacji. scripts/check.ps1, git diff --check,
rzeczywiste logi i audyt niezmienności. Tylko decyzja człowieka akceptuje znaczenie.

## Zakres wyłączony

Inne partie, .4c/.4d, nowe źródła/pass-02, ekstrakcja i korekty,
API inferencji/automatyczne procesy modelowe, M-POC5B/20 sytuacji, M-POC6/7
i architektura. Nie rozszerzać eval-v1/gold ani wyborów właściciela.

## Przegląd człowieka

Pokazać decyzje po ludzku: co mówi źródło, co zapisał model, gdzie jest
różnica i co zmienia; potem proponowana decyzja i wyłączenia. Pełne ID,
hash/pointer/bajty zostają w prywatnym pakiecie. Brak decyzji waiting_review.

## Wznowienie

Od scope-plan i aktualnego current-state; wszystkie wcześniejsze pending
zachować. Nie utożsamiać poprawnego source requirement z zamkniętym wynikiem.

## Przekazanie

Następna osobna część z zachowaniem wszystkich pending. Nadrzędne .4b,
.4 i M-POC5A partial do pełnego rozliczenia i decyzji. M-POC5 jedyny next.

## Dokładne ID relacji tej partii

D1011descriptor, D911914, D911rout, D912MRRCdef, D913screen, D914diagram, D914rout, D914table, D9161011, D918specific, D919chartdef, D919clashdef, D922HD, D923ex, D924911, D924ex, D924rout, D931922, D932ex, D941ex, D951elig, D952951, D952column, D952reverse, D952wheel, D953941, D953elig, D953rout, D953scenario, D9621013, D962shock, D966diag, D967966, D967ex, D968966, D968column, D971app, D972app, D982985, D985982, D985markers, D986982, D986marker, D986react, D987rout, D991OW, D991PAW, D991column, D993rout, D994rout, D996def, D996fire, D996ratings, DCTX846S4-1013, DCTX846S4-845, DCTX846S4-CRT, DCTX923-S4, DCTX932-S4, Dcont-R911, Dcont-R914, Dcont-R924, Dcont-R966, Dcont-R991, Dcont-R996b, Dcont-table914.

## Wykonanie .4b1 — 2026-10-11

Rzeczywiste porównanie 65 przypisanych ID / 125 wystąpień (60/65) oraz
22 zamrożonych par na wynik ukończone przez oceniającego; akceptacja
właściciela waiting_review. Prywatny part-04b1 ma pełne porównania,
źródła/hashe/bajty, owner-focus i propozycje: 116 wystąpień w ograniczonym
pozytywnym zakresie, 9 do osobnej decyzji. Pokazany pakiet 125, oceniający
przejrzał 125, właściciel nowe 0, pending 125; faktyczny odczyt unknown.
3 krytyczne brakujące rekordy i 4 brakujące wzmianki zachowane oddzielnie
od obecnej prozy, bez automatycznego semantycznego FN. Wcześniejsze
nierozstrzygnięcia bez zmiany; current-state-09.json prowadzi nowy dodatek.
Nadrzędne M-POC5A/.4/.4b partial, nie done. Następna osobna .4b2 po pakiecie
decyzji; .4b3/.4c/.4d nadal niewykonane. M-POC5 jedyny next.

## Decyzja właściciela dla .4b1 — 2026-10-11

Po odpowiedzi „zatwierdzam” przyjęto dokładny pozytywny zakres 60 ID /
116 wystąpień (56 first / 60 context), bez całych rekordów lub wyłączonych pól.
Nowe owner-decision-04, overlay-04 i current-state-10 zachowują poprzednie
dowody i decyzje. 9 wydzielonych wystąpień, SEM-001–016 i wcześniejsze
8 oczekiwań pending. Pełne metryki nieocenialne; nadrzędne karty partial.
Następna osobna .4b2 (30 ID / 60 wystąpień), po oszacowaniu przed wykonaniem;
.4b3/.4c/.4d i M-POC5B osobno. M-POC5 jedyny next.

## Rozstrzygnięcie rekomendacji 1–6 — 2026-10-11

Właściciel przyjął sześć przedstawionych rekomendacji odpowiedzią
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
