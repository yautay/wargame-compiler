# STATUS

- **Data aktualizacji:** 2026-10-09
- **Bieżący milestone:** M-POC2
- **Bieżąca karta:** M-POC2A
- **Wynik M-POC0:** done
- **Blokady:** brak dla M-POC2A; lokalny pakiet ekstrakcji jeszcze nieprzygotowany
- **Wynik M-POC1A:** done — przegląd struktury źródła zakończony w zapisanym zakresie
- **Wynik M-POC1B:** done — przygotowanie i przegląd oczekiwań oraz sytuacji zakończone
- **Wynik M-POC1C:** done — decyzje 06 o zakresie i 07 o freeze zapisane; eval-v1 zamrożone

Zamrożono eval-v1 z zatwierdzonego kandydata 03. Zakres i politykę pomiaru
zatwierdzono decyzją 06; osobna decyzja 07 zatwierdziła zamrożenie.
Nie powtarzać zakończonych przeglądów ani pytań o ten sam zakres/freeze.
Źródła, kandydaci, odpowiedzi, decyzje i historyczne handoffy pozostają zachowane.

Zamrożony zakres: 66 lokalnych grup treści, 8 wymagań kontekstu, 20 sytuacji
(17 wyników lokalnych / 3 blokady), 5 relacji jawnych i 3 niejawne.
105 pozostałych propozycji nie jest gold; 7 wzmianek i 7 kontynuacji osobno.
Progi i limity bez zmian; zero krytycznych błędów jest nadrzędne wobec 95%.
Dotychczasowy aktywny czas i dostępny budżet pozostają unknown.

Artefakty pod private/poc/spqr-chapter9/: evaluation/eval-v1/,
evaluation/freeze-public-v1.json i evaluation/M-POC1C-review-008/.
Prywatny manifest i completion prowadzą pełne SHA-256, decyzje i kontrole.
Metadane freeze nie zawierają treści oczekiwań ani odpowiedzi.

Kontrole przed zamrożeniem: scripts/check.ps1 — 94 passed, diff check poprawny.
Końcowe kontrole zapisuje completion sesji. Utworzono lokalną .venv w głównym
repo na zgodnym interpreterze z pytest; środowisko i narzędzia pozostają lokalne.
Praca jest w osobnej kopii feature/tests od ae8f6f0 wskazanej w locatorze;
główny HEAD/indeks pozostają zachowane. Właściciel zlecił commit i push
checkpointu na origin/feature/tests. Zakres i dowody publikacji prowadzi
evaluation/M-POC1C-publication-20261009-01/; środowisko pozostaje lokalne.

Dokładny następny krok: M-POC2A — wejścia, minimalny format, prompt i transfer-list.
M-POC2A/B i pierwsza ekstrakcja niewykonane; wyniki jakości n/a.
Ekstraktor w M-POC2B dostaje wyłącznie odseparowany pakiet bez klucza oceny.
M-POC2 jest jedynym next. Docelowa architektura czeka na wynik M-POC7.

## Historia wcześniejszego przygotowania i przekazania

Poniżej zachowano przekazanie B i historyczne wyniki przygotowania.

Przegląd M-POC1B 2026-10-07–08 zakończono po 24 rzeczywistych decyzjach
właściciela. Ostatnia decyzja RQ-15e/closing potwierdza krytyczność wskazanych
wcześniejszych zakresów i zamknięcie B z zachowaniem ograniczeń.
Wszystkie 20 sytuacji oceniono w pokazanych zakresach: 17 wyników lokalnych
 i 3 uzasadnione blokady. Objaśnienia nie dodały próbek ani pokrycia.

74 propozycje mają dowody i granice kontekstu. Katalog prowadzi do zakresów
decyzji; nie nadaje 74 pełnych potwierdzeń. Rozliczenie 96 kandydatur zawiera
127 propozycji/facetów: 113 wykonawczych (99 jawnych/14 niejawnych),
7 wzmianek i 7 kontynuacji. Siedem wzmianek i trzy niejawne relacje wewnętrzne
zaakceptowano w opisanych zakresach. Nieprzejrzane pola/aliasy/cele pozostają
niepotwierdzone; brak certyfikatu grafu, gold i pomiaru jakości ekstrakcji.

Wskazane interpretacje EXP-009 i EXP-040 rozstrzygnięto lokalnie, ograniczenie
EXP-074 i warunkową krytyczność potwierdzono. Korekty i decyzje osobno;
oryginalne źródła/drafty/odpowiedzi/manifesty/pomiary i wcześniejsze handoffy
zachowano bajtowo. Nie przeniesiono akceptacji struktury M-POC1A na znaczenie.
Finalne artefakty prywatnie w `evaluation/owner-review-002/` pod korzeniem
`private/poc/spqr-chapter9/`: `decision-24-RQ-15e-closing.json`,
`review-summary-final-20261008.md`, `review-catalog-final-24.json`,
`review-criteria-final-24.json`, `review-manifest-final-20261008.json`,
`closure-seal-24.json`, `completion-after-decision-24.json`.
Nowy pomiar zamknięcia: `measurement/M-POC1B-owner-review-002/completion.json`.

Dokładny przyszły krok: M-POC1C od decyzji 24 (RQ-15e/closing), finalnego
podsumowania/manifestu/katalogu oraz listy ograniczeń. EXP-002/031, DEP-031,
realny kontekst EXP-010/019/033/050/064/066/074, pozostały zakres EXP-040,
nieprzejrzane metadane/aliasy i procedury zewnętrzne pozostają jawne.
Nie traktować niepotwierdzonych pól lub source_supported jako pewnego gold.
M-POC1C i M-POC2B nie wykonano; eval-v1 niezamrożone. M-POC1 jedyny next.

Kontrole zamknięcia: scripts/check.ps1, lokalne TMP/TEMP, nowy basetemp
 i końcowy git diff --check; faktyczne wyniki/logi/hashe w prywatnym rejestrze.
Źródło ma identyczny SHA-256; stabilna kopia i mapa w prywatnym
`source/source-location-supplement-20261008-01.json`. Source-v1 zachowano.
Dodatkowy kontekst poza core nie rozszerza zakresu ekstrakcji.
Znany wyjątek początkowych bajtów `.git/index` odnotowano; staging/HEAD zgodne,
przyczyna nieustalona, indeksu nie nadpisywano. Pozostałe chronione pliki
zachowane; historycznego audytu całego archiwum nie powtarzano.

## Historyczne przygotowanie i wcześniejsze kontrole

Snapshot 392 plików (81 319 086 bajtów) i odtworzenie mają zgodne SHA-256.
237 publicznych plików jest w archiwum, 155 prywatnych zachowano według mapy.
Legacy uruchamia się z własnego katalogu: 807 passed, 1 skipped, oba CLI help poprawne.
Nowa aktywna struktura zawiera plan, 15 kart, ADR-0039 i minimalne kontrole.
Kontrole aktywne: **51 passed**; `git diff --check` bez błędów.
Skrypt odtwarzania: 392/392 zgodne; istniejący cel odrzucany bez nadpisania.

Stan przygotowania przed rzeczywistym przeglądem (oryginalny draft):
jedyny next to M-POC1, bieżąca karta M-POC1B. Przygotowano cztery wymagane
artefakty draft: 74 oczekiwania z dowodami/krytycznością, rozliczenie 96/96
kandydatur w 127 propozycjach/facetach relacji i 20 sytuacji oraz 15 pytań przeglądu.
To nie zweryfikowany graf ani gold. Osobno: 113 propozycji wykonawczych
(99 jawnych, 14 niejawnych), 7 wzmianek, 7 kontynuacji. Nie nadano akceptacji.
64 oczekiwania są lokalnie poparte źródłem, 8 wymaga kontekstu, 2 pozostają
interpretacyjnie nierozstrzygnięte; właściciel potwierdził w M-POC1B zero rekordów.
20 sytuacji zawiera 16 proponowanych wyników lokalnych i 4 uzasadnione blokady;
nie są to wyniki ekstrakcji ani pełne rozstrzygnięcia gry.
Pytania i szczegóły tylko w `private/poc/spqr-chapter9/evaluation/draft/`.
Audyt nowych artefaktów passed; 80 zastanych plików źródła/przeglądu i indeks Git
bez zmian, ponowny audyt 9298 plików historycznych zgodny bajtowo/SHA-256.
Kontrole M-POC1B: **62 passed**, `git diff --check` bez błędów;
lokalne TMP/TEMP i nowy basetemp. Logi i końcowe hashe w rejestrze sesji.
M-POC1A zakończono po dziesięciu rzeczywistych decyzjach właściciela.
Przegląd dotyczył granic, struktury, wskazanych podziałów i sposobu raportowania
niepewności. Znaczenie, cały graf i oczekiwania nie zostały zaakceptowane ani zamrożone.
Źródło: SPQR 5th Edition, rozdział 9.0, PDF 31–37 z granicami opisanymi w planie.
Istnienie, pełny SHA-256 zgodny z historycznym manifestem i wydanie sprawdzone.
Wszystkie rendery core obejrzano, granice i kontekst rozdzielono.
Roboczo: 41 oznaczeń reguł, 98 grup klauzul, 14 not, 1 tabela, 2 diagramy,
7 kontynuacji; 96 rekordów kandydatur zależności, bez zatwierdzonego grafu.
Wcześniejsze drafty zachowano bajtowo. Decyzje, źródłowe wycinki, cztery osobne
uzupełnienia oraz mapy zmian są w
`private/poc/spqr-chapter9/evaluation/owner-review-001/`.
Wznowienie prowadzi `review-summary.md`, a hashe `review-manifest.json`.
Kontrole M-POC1A: **52 passed**, `git diff --check` bez błędów;
9298 historycznych plików zachowało bajty i pełne SHA-256, indeks Git bez zmian.
Po przeglądzie właściciela: **61 passed**, w tym kontrole postępu kart;
audyt integralności uzupełnień i ponowny audyt 9298 historycznych plików passed.
Propozycja ekstrakcji: ręczna sesja Codex, GPT 6.1 Sol / wysoki.

## Niewykonane i otwarte

- M-POC1: M-POC1A/B done w zapisanych zakresach; M-POC1C partial/waiting_review.
  M-POC2–M-POC7 niewykonane. Brak eval-v1, nowej odpowiedzi ekstrakcji
  i pomiarów jej jakości. Nie rozpoczęto zamrożenia ani implementacji.
- Nieprzejrzane zakresy relacji/aliasów/parametrów i zewnętrzne źródła
  pozostają niepotwierdzone. Pełny podział atomowy i wszystkie drobne
  wartości ilustracji niepotwierdzone; stosować katalog zakresów decyzji.
- Historyczny punkt wznowienia po decyzji 05 (zastąpiony decyzją 06): odczytać review-state-after-decision-05.json,
  dependency-overlay-05.json i pending-question-06-scope.json z rejestru
  evaluation/M-POC1C-review-006/ oraz eval-v1-candidate-20261009-03/ (manifest,
  review.md, measurement-policy.json). Akceptacja zakresu i polityki oceny,
  dopiero potem osobna zgoda freeze; wcześniejsze relacje nie wymagają ponownego review.
- Hipoteza jednostki rozdziału i użyteczność formatu czekają na pomiar.
- M-DESK2 historycznie partial; jego dawny backlog pozostaje poza kolejką.
- Snapshot i odtworzenie lokalne; brak kopii na odrębny nośnik.
- `.venv` zachowano bez instalacji; brak runtime WGC/GLU w aktywnym projekcie.

[Plan](POC-PLAN.md), [roadmapa](ROADMAP.md), [handoff](HANDOFF.md),
[karty](work/tasks/README.md), [archiwum](../archive/legacy-2026-10-07/README.md).
