# STATUS

- **Data aktualizacji:** 2026-10-10
- **Bieżący milestone:** M-POC5
- **Bieżąca karta:** M-POC5A
- **Wynik M-POC0:** done
- **Wynik M-POC1A:** done — przegląd struktury w zapisanym zakresie
- **Wynik M-POC1B:** done — przegląd oczekiwań i sytuacji
- **Wynik M-POC1C:** done — zakres zatwierdzony, eval-v1 zamrożone
- **Wynik M-POC2A:** done — pakiet przygotowany
- **Wynik M-POC2B:** done — odbiór istniejącej first-001 z brakami unknown
- **Wynik M-POC3:** done — baseline zamknięty przed korektami, bez semantycznej akceptacji
- **Wynik M-POC4A:** done — właściciel zatwierdził wybór źródła i zakres; pass-01 zamrożony osobnym zapisem
- **Wynik M-POC4B:** done — właściciel przyjął ograniczony efekt źródła, 0 pełnych domknięć i jawne blokady; bez akceptacji znaczenia
- **Wynik M-POC5A:** planned — wspólny przegląd znaczenia obu wyników jeszcze niewykonany
- **Blokady:** znaczenie obu wyników waiting_review; brak dokładnych tabel oraz rzeczywistych źródeł mapy/scenariusza/żetonu; ścieżka do trzeciego nierozstrzygniętego kroku, bez jego pozyskania; izolacja dostępu naruszona, ekspozycja na ocenę unknown; konfiguracja i aktywny budżet unknown

2026-10-10 właściciel potwierdził „zatwierdzam” i „akceptuje wyniki” po
wyjaśnieniu ograniczonego rezultatu M-POC4B. Zapisano
reviews/context-source-01/decision-01.json i review-closure-01.json.
Akceptacja obejmuje częściowe źródło/procedurę, 0 pełnych domknięć, 4 częściowe
aktualizacje, 4 nowe deklaracje oraz jawne ograniczenia głębokości/izolacji.
Nie obejmuje znaczenia reguł/relacji, kolejności obliczeń, sytuacji ani budżetu.
Nie poświadczono otwarcia całego raportu lub obrazu przez właściciela.

M-POC4 done w zakresie wyboru źródła, odbioru, raportu i ograniczonego przeglądu
efektu. Zamknięte raporty/requesty/pomiary z historycznym partial pozostają
niezmienione; nowa decyzja i closure prowadzą aktualny workflow.
Dokładny następny krok: osobna M-POC5A w C:/repo/wargame-compiler,
odczyt obu run/proposal/report i eval-v1, dwa zestawy ocen z hashami,
pokazywanie dowodów właścicielowi. Bez modelowej autoakceptacji, nowej
ekstrakcji/korekty, pass-02 ani M-POC5B w tej samej karcie.
M-POC5 jedyny next. Prompt: prompts/semantic-review-start-v1.txt pod
private/poc/spqr-chapter9/. Nowy pomiar zamknięcia przeglądu:
measurement/M-POC4B-owner-review-001/completion.json i nowy wpis sessions.jsonl.
Kontrole zamknięcia: scripts/check.ps1 **115 passed**, git diff --check bez błędów.

## Historia raportu M-POC4B przed przyjęciem ograniczonego wyniku

M-POC4B odebrało istniejący plik transfer/context-v1/context-01.json
i zachowało 712014 bajtów w runs/context-01/response.raw.txt. SHA-256:
95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
Manifest nowego pakietu zgodny; 41 artefaktów/42 wejścia oraz 7 artefaktów
eval-v1 zweryfikowane. Rodzic first-001 i zamknięty baseline zachowane.
Nowe run.json/session-evidence, proposal/provenance oraz reports/context-01/
mają osobne hashe i dokładne ślady do surowych bajtów.

Format czytelny: 480 ID rekordów, 154 ID klauzul, 3660 rozwiązanych referencji.
Zmieniła się 1 reguła, 1 istniejący węzeł, 2 stare relacje i 4 stare luki.
Dodano 2 węzły, 5 relacji, 6 dowodów i 4 luki. Wszystkie 81 dawnych deklaracji
luk zachowane, 4 częściowo uzupełnione nadal blokują; 0 pełnych domknięć.
Nowe cytaty poparte źródłem i czytelne w rasterze; 6 nowych granic glifów
pending. Dziedziczony błąd obszaru i 7 brakujących par nie naprawione.
207 ID, 66 grup treści, 8 kontekstu i 20 sytuacji zachowują mianowniki;
znaczenie, TP/FP/FN i regresje semantyczne not_assessable.

Przyrost źródła nadal 1 strona/1 reguła/0 tabel. Wykonano 1 ręczną rundę
odpowiedzi po kontekście, 0 korekt i 0 nowych inferencji oceniającego.
Nowe połączenie w propozycji ujawnia ścieżkę 3 kroków do brakującego celu;
nie pozyskano trzeciego źródła, dalsze rozszerzanie zatrzymano na granicy 2.
Nie zadeklarowano zgodności głębokości całego grafu ani aktywnego budżetu czasu.

Niezależny transkrypt aplikacji potwierdza wylistowanie nazw/wyszukiwanie ścieżek
poza allowlistą w korzeniu repo. Pełna izolacja niepoświadczona; nie dowodzi
to odczytu klucza oceny. Ekspozycja i czysty kontekst unknown, bez dowodu skażenia.
Zapisano kalendarzowe metadane turnu; nie utożsamiono ich z czasem aktywnym.
Samoopis ekstraktora pozostaje deklaracją.

Dokładne wznowienie: reviews/context-source-01/request.json i zamknięty
reports/context-01/report.md prowadzą przegląd człowieka zakresu efektu.
Po nim można zamknąć M-POC4B i przejść do M-POC5A/B z oboma hashami odpowiedzi.
Nie powtarzać ekstrakcji ani dokładać pass-02. M-POC4 pozostaje jedynym next.
Pomiary/kontrole: measurement/M-POC4B-context-01/completion.json i nowy wpis
measurement/sessions.jsonl. M-POC5–M-POC7 niewykonane.
Kontrole M-POC4B: scripts/check.ps1 **114 passed**, git diff --check bez błędów.

## Historia zamknięcia M-POC4A przed odpowiedzią context-01

2026-10-10 właściciel odpowiedział „Zatwierdzam” po prezentacji ograniczonego
źródła i pomocniczego tekstu. Zapisano decyzję z zakresem/hashami w
evaluation/M-POC4A-review-001/decision-01.json; nie poświadczono otwarcia
obrazu przez właściciela ani akceptacji znaczenia, wyników i budżetu czasu.
M-POC4A done dotyczy wyboru źródła i przygotowania, bez sukcesu ekstrakcji.

context/pass-01/freeze-v1.json zamraża niezmieniony draft i wybrany payload;
wcześniejszy manifest/targets/prompt/review zachowują historyczne bajty/flagę draft.
Aktualny stan prowadzi nowy freeze i decyzja, bez nadpisania manifestów.
Oryginały first-001, pierwsze wejścia, eval-v1 i raporty M-POC3 zachowane.

Przyrost nadal 1 strona, 1 reguła, 0 tabel; dostarczona ścieżka 1 krok,
rozważana 2; dalsze rozszerzanie zatrzymane. Limity 8/20/4/2/2 bez zmian,
0 rund odpowiedzi, 0 nowych inferencji i 0 korekt. Aktywny budżet czasu
i jego zgodność unknown. Pozostałe blocked_source/pending/not_assessable zachowane.

Przygotowano transfer/context-v1/ z 42 plikami allowlisty: niezmienione wejścia
pierwszej próby, rodzic odpowiedzi, wybrany fragment, metadane zamrożenia,
nowy prompt i wąski dodatek techniczny formatu dla ID przebiegu/hashu manifestu
oraz jawnych współrzędnych wycinka. Bez klucza oceny, raportów, całego PDF
i materiałów oceniających. Pakiet prepared_not_sent; nie wykonano M-POC4B.

Dokładny następny krok: właściciel ręcznie otwiera osobną izolowaną sesję
w transfer/context-v1/, czyta transfer-list.txt i prompts/context-v1.txt;
uzyskuje jedną odpowiedź context-01.json. Oceniający po odbiorze wykonuje
M-POC4B na eval-v1, osobno od baseline. Nie generować odpowiedzi w tym czacie,
który zna klucz oceny. M-POC4 pozostaje jedynym next.
Zamknięcie i kontrole: measurement/M-POC4A-review-001/completion.json
oraz dopisany rekord measurement/sessions.jsonl.
Kontrole zamknięcia review: scripts/check.ps1 **113 passed**, git diff --check bez błędów.

## Historia przygotowania M-POC4A przed decyzją właściciela

M-POC4A zweryfikowało integralność baseline: 32/32 artefakty wejść,
33/33 pliki transferu, 7/7 artefakty eval-v1, 10/10 artefakty raportu
i 16 768 zakresów provenance zgodne. Zweryfikowana stabilna kopia PDF
w repo ma hash source-v1; historyczna ścieżka nie istnieje i nie jest wymagana.
Oryginały, pierwsze wejścia, eval-v1 i raporty M-POC3 zachowano.

context/pass-01 zawiera targets.json, manifest.json, prompt.txt, dowody
i review.md. Pakiet draft, niezamrożony i nieprzekazany. Przyrost policzony
przed rozszerzeniem: 1 strona, 1 reguła, 0 tabel; dostarczona ścieżka 1 krok,
rozważana 2 kroki do blocked_source. Na granicy głębokości zatrzymano
dalszy wybór, zgodnie z pierwszym osiągniętym limitem. Limity 8/20/4/2/2
bez zmian; 1 pass przygotowany, 0 rund odpowiedzi, 0 inferencji i 0 korekt.
Zgodność aktywnego budżetu czasu unknown, bez deklaracji zaliczenia.

Rozliczono 8 potwierdzonych relacji wewnętrznych (źródła już w baseline),
8 wymagań kontekstu oraz 105 niepotwierdzonych kandydatur. 79 deklaracji:
3 z częściowym źródłem, 56 z kandydatami lokalizacji, 20 blocked_source.
Nie są to potwierdzone błędy ani zaakceptowane źródła. Brakujące wewnętrzne
pary nie spowodowały automatycznej ekspansji. Znaczenie i sytuacje pozostają
pending/not_assessable; syntetyczne fakty nie ustalają rzeczywistego setupu.

Dokładne wznowienie: M-POC4A, review pakietu i jawny nowy zapis decyzji
człowieka z zakresem/hashami; dopiero potem freeze i osobna M-POC4B.
M-POC4 pozostaje jedynym next. Nowe pomiary i dowody integralności:
measurement/M-POC4A-pass-01/ oraz dopisany rekord measurement/sessions.jsonl.
Kontrole M-POC4A: scripts/check.ps1 **105 passed**, git diff --check bez błędów.

Zapis Git, aktualizacja 2026-10-10: po bezpośrednim potwierdzeniu właściciela
wypchnięto `0e016e4` (pakiet) i `8ec04d7` (zapis stanu) do origin/feature/tests,
wraz z prywatnymi artefaktami. Zdalny HEAD `8ec04d7` potwierdzono przez
git ls-remote. Wcześniejsza blokada publikacji zniesiona; historyczne odrzucenia
zachowane w measurement/M-POC4A-publication-01/state.json, wynik publikacji
w osobnym completion.json. M-POC4A nadal partial/waiting_review;
zgoda na push nie oznacza akceptacji źródła krytycznego ani znaczenia.

Zapisano wszystkie wymagane artefakty proposals/first-001/ i reports/first-001/
pod private/poc/spqr-chapter9/, mapę do surowych bajtów oraz manifest i closure.
Odpowiedź runs/first-001/first-001.json zachowana (617941 bajtów).
SHA-256: 3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
Manifest wejść: 39e0a65e2f7d0d991c1bd031c6a99e6c40b80fe34e5429640e150fbfbedf340a.
Oba zgodne, 32/32 artefakty i 33/33 pliki pakietu zgodne. Eval-v1 otwarto
zgodnie z kartą M-POC3; 7/7 artefaktów zgodnych z zamrożonym manifestem.
Oryginałów, wejść, promptu i zamrożonej oceny nie zmieniono.

Format czytelny; 454 ID rekordów i 154 ID klauzul unikalnych, 3401 referencji
rozwiązanych. Rozliczono wszystkie 207 ID inwentarza: 205 kandydatów lokalizacji,
2 lokatory nieocenione; znaleziono 41/41 różnych oznaczeń. 105 krótkich cytatów
podpartych, lecz 1 wskazany obszar nie obejmuje cytatu i 58 granic glifów czeka
na review. Geometria/hash/wymiary wszystkich 105 obszarów poprawne.

Relacje: 5/5 jawnych kandydatów, 0/3 niejawnych i 3 brakujące krytyczne pary.
Wzmianki 2/7 kandydatów, 1 różnica rodzaju pending, 4 brakujące pary;
kontynuacje 7/7 kandydatów kolejności. Wszystkie 126 propozycji rozliczone.
Sześć klas: format 1 potwierdzony błąd; pominięcie 7 brakujących par;
błędny odczyt not_assessable; błędna interpretacja 1 kandydat; brak kontekstu
79 deklaracji; niejednoznaczność 2 deklaracje i 58 granic do review.
Twierdzenia ekstraktora i pending nie są potwierdzonymi błędami semantycznymi.

66 grup treści, 8 wymagań kontekstu, 20 sytuacji i rubryki mają sprawdzone
mianowniki i not_assessable dla znaczenia. TP/FP/FN, semantyczna precyzja
oraz kompletność nieocenione; nowe relacje nie są pewnymi FP. Brak pełnego gold,
certyfikatu całego grafu i semantycznej akceptacji. Ocena człowieka waiting_review.

Nieznane konfiguracja/czasy ekstrakcji, historyczna lista przekazania/prompt,
czysty kontekst, ekspozycja na ocenę, eksport, tokeny i cena nadal unknown.
Samoopis nie jest niezależnym dowodem. Nie potwierdzono ślepej próby ani skażenia.
Czas kalendarzowy oceny nie ustala aktywnego budżetu; zgodność z limitami unknown.
Nie wykonano ekstrakcji, korekt, nowych inferencji ani dalszych kart.

Kontrole zamknięcia: scripts/check.ps1 **104 passed**, git diff --check bez błędów.
Pomiary i rzeczywiste logi scripts/check.ps1 oraz git diff --check:
measurement/M-POC3-first-001/completion.json i nowy rekord
M-POC3-first-001-baseline w measurement/sessions.jsonl. Baseline pozostaje zamknięty.
Historyczny punkt wznowienia po M-POC3 (zastąpiony powyższym): od run.json, report.md,
dependency-comparison.json i zadeklarowanych braków w errors.json wybiera
potrzebne blokujące cele, sprawdza źródła i liczy przyrost stron/reguł/tabel,
głębokość oraz limity przed context/pass-01. Brakujące pary wewnętrzne
nie uzasadniają automatycznie nowego kontekstu. M-POC4 jedyny next;
M-POC4B–M-POC7 nierozpoczęte. Progi i limity bez zmian.

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
