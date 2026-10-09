# STATUS

- **Data aktualizacji:** 2026-10-09
- **Bieżący milestone:** M-POC3
- **Bieżąca karta:** M-POC3
- **Wynik M-POC0:** done
- **Blokady:** brak technicznych odbioru; braki dowodów pochodzenia/konfiguracji/czasu zapisane jako unknown, niezależność próby niepotwierdzona
- **Wynik M-POC1A:** done — przegląd struktury źródła zakończony w zapisanym zakresie
- **Wynik M-POC1B:** done — przegląd oczekiwań i sytuacji zakończony
- **Wynik M-POC1C:** done — decyzje 06/07 zapisane, eval-v1 zamrożone
- **Wynik M-POC2A:** done — pakiet przygotowany, oględziny właściciela potwierdzone
- **Wynik M-POC2B:** done — odbiór i rejestracja już wykonanej first-001, bez powtarzania ekstrakcji; z jawnymi brakami dokumentacji
- **Wynik M-POC3:** planned — nie rozpoczęto raportu pierwszego wyniku

Właściciel potwierdził wykonanie ekstrakcji i wskazał oryginał
private/poc/spqr-chapter9/transfer/first-v1/first-001.json. Zweryfikowany SHA-256:
3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
Bajtowo identyczna kopia (617941 bajtów) zachowana w runs/first-001/first-001.json
pod private/poc/spqr-chapter9/, obok run.json i session-evidence.txt.
Nowy wpis odbioru: measurement/sessions.jsonl, ID M-POC2B-first-001-receipt.

Manifest wejść SHA-256:
39e0a65e2f7d0d991c1bd031c6a99e6c40b80fe34e5429640e150fbfbedf340a.
Obie kopie manifestu zgodne. Wszystkie 33 pliki transfer-list istnieją i są
bajtowo identyczne z kanonicznym pakietem; 32 artefakty manifestu mają zgodne
hashe i rozmiary. Kontrola dotyczy chwili odbioru. Oryginał odpowiedzi,
wejścia, formaty, prompt i manifesty zachowane bez zmian, także historyczne
pole prepared_not_sent. Fakt późniejszego odbioru zapisany wyłącznie osobno.

Brakuje historycznego transkryptu/ID sesji, faktycznej listy przekazanych/odczytanych
plików i użytego promptu, niezależnego potwierdzenia czystego kontekstu,
widocznej konfiguracji, czasów ekstrakcji i aktywnych czasów człowieka/modelu,
sposobu pierwotnego eksportu, tokenów i ceny: unknown. Samoopis odpowiedzi
(Codex desktop, model/rozumowanie unknown, not_exposed) zachowano jako deklarację,
bez niezależnego potwierdzenia. Nie poświadczono ślepej próby ani skażenia.
Znany pakiet i jego obecne hashe nie dowodzą historycznego użycia plików.
Zapisany czas odbioru nie jest czasem ekstrakcji; zużycie aktywnego budżetu unknown.

Nie powtórzono ekstrakcji, nie poprawiono odpowiedzi, nie otwarto klucza
oceny evaluation/eval-v1 i nie rozpoczęto M-POC3. Znaczenie i jakość nieocenione.
Kontrole scripts/check.ps1, git diff --check i integralność odbioru prowadzi
nowy wpis pomiarowy z rzeczywistymi logami i hashami; nie jest to raport jakości.

Dokładny następny krok: osobna sesja M-POC3 najpierw sprawdza
runs/first-001/run.json, session-evidence.txt oraz SHA-256 kopii first-001.json,
zachowuje braki pochodzenia/unknown, a następnie oceniający otwiera eval-v1
zgodnie z kartą i zapisuje raport pierwszego wyniku przed jakąkolwiek korektą.
M-POC2 done w zakresie przygotowania i rejestracji; M-POC3 jedyny next.
M-POC3–M-POC7 niewykonane. Progi i limity eksperymentu bez zmian.

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

## Historyczny stan otwartych kwestii przed freeze (zastąpiony powyżej)

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
