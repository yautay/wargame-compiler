# POC reguł i zależności SPQR

Plan eksperymentu, 2026-10-07. Decyzja: [ADR-0039](adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
Stan wykonania prowadzi [ROADMAP](ROADMAP.md), zakres sesji [karty](work/tasks/README.md).
M-POC0 nie wykonuje ekstrakcji ani inwentaryzacji M-POC1.

## Cel i zakres

Sprawdzić jakość ekstrakcji reguł i zależności oraz koszt dojścia do użytecznego
wyniku. Wynik ma dostarczyć podstawy do decyzji architektonicznej, nie dowieść
gotowości pełnego silnika gry.

Źródło: `C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf`, SPQR, 5th Edition.
Historyczny hash zapisany w propozycji zakresu:
`e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.
M-POC1 musi go sprawdzić wobec rzeczywistego pliku; M-POC0 nie zatwierdza nowego odczytu PDF.
Źródło jest czytane, repo `C:\dev\spqr` nie jest modyfikowane.

Rozdział 9.0 „Special Combat Units”: **PDF 31–37**, od nagłówka 9.0 w prawej
kolumnie PDF 31 do miejsca przed nagłówkiem 10.0 w lewej kolumnie PDF 37.
Pozostała treść stron granicznych jest kontekstem. Numer strony PDF liczymy od 1,
drukowaną etykietę zapisujemy osobno. Nie zakładamy ciągłości numeracji reguł.

Propozycja `private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json`
wskazuje **19 różnych liczbowych odwołań zewnętrznych**. To kandydaci, nie zweryfikowany
graf ani mianownik pomiaru. Trzeba uwzględnić nazwane tabele i zależności bez numerów.
Starszy zakres kończący się na PDF 36 był niepełny; kontynuacja sięga PDF 37.

## Minimalna propozycja do pomiaru

M-POC2A zapisze niewielki format roboczy `proposal-format-v1.md` i przykład syntetyczny
bez SPQR. Nie przyjmujemy teraz docelowego języka, schematów legacy ani kontraktu KB.
Minimum:

- koperta: ID przebiegu, wersja formatu, hash manifestu wejść i zakres;
- reguła: lokalne ID, oryginalne oznaczenie, warunki, działanie/skutek, wyjątki,
  parametry, wartości/jednostki, typy jednostek gry, zakres i ograniczenia czasowe;
- dowody: ID źródła/hash, strona PDF, cytat; jeśli istotna grafika — plik/hash obrazu
  i obszar z jawnym układem współrzędnych. Oddzielić transkrypcję od interpretacji;
- zależności jako osobne rekordy: ID, `from`, `to` lub jawny kandydat celu,
  rodzaj, jawna/niejawna, uzasadnienie, dowód, status i wpływ braku na reguły/sytuacje;
- osobne braki i nierozstrzygnięcia z przyczyną, zakresem i potrzebnym kontekstem.

Brak wartości to jawne `unknown`/luka, a brak wyjątków ustalony z tekstu to odrębny
stan. Nie wypełniać obu pustą listą bez wyjaśnienia. Jedno oznaczenie może obejmować
kilka klauzul; inwentarz i mapowanie klauzul zapobiegają sztucznemu pompowaniu kompletności.

## Relacje i kierunek

`from` oznacza regułę korzystającą z celu lub odnoszącą się do niego, `to` — używaną
procedurę/tabelę/definicję albo modyfikowaną regułę ogólną. Dla kontynuacji:
fragment rozpoczynający → dalszy fragment. Uzasadnienie wyjaśnia semantykę kierunku.

| Rodzaj | Co sprawdzić |
|---|---|
| Użycie procedury | Czy rozstrzygnięcie wymaga wykonania wskazanych kroków |
| Użycie tabeli | Czy wynik zależy od odczytu tabeli, jej nagłówków i not |
| Definicja | Czy cel definiuje pojęcie/parametr potrzebny w regule |
| Warunek | Czy cel dostarcza warunek stosowalności |
| Modyfikacja | Czy reguła zmienia działanie/wartość reguły ogólnej |
| Wyjątek | Czy zawęża/uchyla regułę ogólną w określonym zakresie |
| Kontynuacja | Czy treść jednej reguły przechodzi między fragmentami |
| Wzmianka | Odwołanie informacyjne; samo w sobie nie jest zależnością wykonania |

Status celu: wewnętrzny, zewnętrzny ze źródłem, nierozstrzygnięty albo niepoparty.
Stan przeglądu jest osobny. Niejawna krawędź wymaga źródłowego uzasadnienia potrzeby,
nie tylko podobieństwa słów. Każdy krytyczny cel ma dostępne źródło i dowód albo
blokuje odpowiednie rozstrzygnięcie. Nie utożsamiamy wzmianki z zależnością wykonania.

## Etapy i warunki przejścia

| Milestone | Praca i wynik | Warunek przekazania |
|---|---|---|
| M-POC0 | Snapshot, odtworzenie, oddzielne archiwum, wnioski, ADR, bootstrap, plan i karty | Hashy zgodne; osobna kontrola legacy i aktywnej struktury; dopiero wtedy M-POC1 jako next |
| M-POC1 | Inwentarz oznaczeń, tabel, diagramów, not, kontynuacji i kandydatów; ręczne oczekiwania oraz 15–20 sytuacji | Przegląd właściciela, osobno oczekiwania potwierdzone i wymagające kontekstu, zamrożony `eval-v1` przed pierwszą ekstrakcją |
| M-POC2 | Rendery, pomocniczy tekst, manifest/hash, prompt, minimalny format; ręczna ekstrakcja w Codex | Zachowane oryginalne wejścia, prompt, surowa odpowiedź, model, rozumowanie, sposób zapisu i dostępny czas; brak klucza oceny w kontekście ekstraktora |
| M-POC3 | Kontrola formatu, ID, referencji, dowodów i porównanie z inwentarzem | Raport pierwszego wyniku zapisany przed korektą; jawna lista błędów i blokad; parser nie uzasadnia akceptacji znaczenia |
| M-POC4 | Ograniczone domknięcie potrzebnych zależności | Każdy dodany kontekst ma przyczynę, dowód i koszt zakresu; brak źródła pozostaje luką; osobny wynik po kontekście |
| M-POC5 | Przegląd warunków, skutków, wyjątków, liczb, negacji, czasu; zwykłe/graniczne/konfliktowe sytuacje | Oczekiwane rozstrzygnięcia mają źródło; człowiek ocenia znaczenie; blokowane sytuacje nie są zgadywane |
| M-POC6 | Pakiety korekt, ręczne odpowiedzi, ponowne kontrole i koszt | Każda odpowiedź zachowana; poprawione błędy i regresje policzone; osiągnięcie kryteriów lub limitu, bez nieskończonej pętli |
| M-POC7 | Porównanie pierwszego wyniku, kontekstu i korekt; decyzja | Właściciel wybiera kontynuację, poprawę metody lub odrzucenie na podstawie raportów; dopiero wtedy propozycja kontraktu, magazynu, orkiestracji i ponownego użycia legacy |

W M-POC1A powstaje inwentarz; M-POC1B układa oczekiwania i sytuacje; M-POC1C zamraża
je po przeglądzie. M-POC2A przygotowuje pakiet, M-POC2B wykonuje ręczną ekstrakcję.
M-POC4A wybiera kontekst, M-POC4B uzyskuje i ocenia odpowiedź z kontekstem.
M-POC5A przegląda reguły, M-POC5B sytuacje. M-POC6A wykonuje jedną korektę,
M-POC6B porównuje jej wynik i koszt. M-POC7A przygotowuje porównanie,
M-POC7B zapisuje decyzję człowieka. Karta M-POC3 obejmuje raport pierwszego wyniku.
Każda karta mieści się w jednej sesji; przed przekroczeniem 90 minut podzielić zakres.

M-POC5A/B oceniają oddzielnie **oryginalny pierwszy wynik i wynik po kontekście**.
Wyniki tych późniejszych przeglądów są nowymi artefaktami w `reviews/`, powiązanymi
z hashami odpowiedzi; nie zmieniają zamkniętego raportu M-POC3. Jeżeli pierwszego
wyniku nie da się odczytać, jego znaczenie/sytuacje pozostają `not_assessable`,
a naprawa formatu ma osobną ocenę. Każda korekta ponownie przechodzi te same miary.

## Zamrożony zestaw oceny i niezależność

`eval-v1` zawiera ręczny inwentarz, oczekiwania z dowodem i oznaczeniem krytyczności,
sprawdzony zestaw relacji oraz **15–20 sytuacji**: zwykłe, wyjątki, granice i konflikty.
Każda sytuacja ma źródłowo uzasadniony oczekiwany wynik lub oczekiwaną blokadę.
Krytyczny błąd zmienia legalność, skutek, liczbę, wyjątek, czas albo możliwość
rozstrzygnięcia. Krytyczność ustalamy przed oglądaniem odpowiedzi.

Przegląd właściciela zapisuje recenzenta, datę, zakres, dowody, niepewności oraz hashe.
Zbiór potwierdzony i zbiór wymagający kontekstu mają odrębne liczniki. Nieudowodnionego
oczekiwania nie używamy jako pewnej poprawnej odpowiedzi. Wersję i hash zamrażamy
przed ekstrakcją; kompletność relacji dotyczy tego sprawdzonego zestawu, nie całej gry.

Ekstraktor dostaje wyłącznie `inputs/v1/`, `prompts/first-v1.txt`, format propozycji
i `freeze-public-v1.json` z ID/hashami bez treści oczekiwań. Właściciel uruchamia
ręcznie czystą sesję Codex bez historii pracy nad oceną. Nie przekazywać jej
prywatnych handoffów oceniających, `evaluation/`, raportów lub odpowiedzi wzorcowych.
Jeśli wykonawca widział oczekiwania, oznaczyć próbę `contaminated`; nie jest ślepą
pierwszą ekstrakcją. Nowa próba wymaga jawnego ID i uczciwego raportu kosztu.

Odkryty błąd zestawu oceny zapisujemy w erracie z dowodem i decyzją właściciela.
`eval-v1` pozostaje niezmieniony. Ewentualne `eval-v2` ma mapę różnic; wszystkie
porównywane wyniki oceniamy na tej samej wersji oraz pokazujemy wpływ zmiany.
Nie zmieniamy oczekiwań, by dopasować je do odpowiedzi modelu.

## Artefakty i niezmienność

Korzeń nowych prywatnych danych: `private/poc/spqr-chapter9/` (dalej `P/`). Poniższe
lokalizacje są planem; M-POC0 tworzy tylko informacyjny README katalogu.

| Lokalizacja | Zawartość / reguła |
|---|---|
| `P/source/source-v1.json` | Ścieżka i zweryfikowany hash PDF, wydanie, granice i odrębny kontekst |
| `P/evaluation/draft/` | Roboczy inwentarz i oczekiwania M-POC1; bez surowych odpowiedzi |
| `P/evaluation/eval-v1/` | `inventory.json`, `expectations.json`, `dependencies.json`, `situations.json`, `review.md`, `manifest.json`; zamrożone razem |
| `P/evaluation/freeze-public-v1.json` | ID, hashe, data i potwierdzenie zamrożenia bez treści oczekiwań; może wejść do pakietu, zostaje prywatny |
| `P/inputs/v1/` | Oryginał/kopia źródła prywatnie, rendery stron, pomocniczy tekst, manifest pełnych SHA-256 i wersji narzędzi; niezmienne po wysłaniu |
| `P/prompts/first-v1.txt` | Dokładny prompt; bez odpowiedzi zestawu oceny; niezmienny po próbie |
| `P/formats/proposal-format-v1.md` | Roboczy minimalny format i syntetyczny przykład, zamrożone dla pierwszej próby |
| `P/runs/first-001/` | `response.raw.txt` lub oryginalny pobrany plik, `run.json`, dowód sesji; surowe bajty bez usuwania otoczek |
| `P/proposals/first-001/` | Oddzielny odczyt danych i mapa do surowej odpowiedzi/hash; nigdy uzupełnianie brakującej treści |
| `P/reports/first-001/` | `format.json`, `inventory.json`, `report.md`, metryki i hashe; raport pierwszego wyniku zamknięty przed korektami |
| `P/context/pass-01/` | Lista celów, przyczyn, dowodów, głębokości i limitów; nowe źródła/rendery, prompt, manifest |
| `P/runs/context-01/`, `P/reports/context-01/` | Oddzielna odpowiedź po kontekście i jej ocena; także przy porażce |
| `P/reviews/semantic-01/`, `P/reviews/situations-01/` | Lista porównań, dowodów, recenzenta i decyzji; jawne blokady |
| `P/corrections/correction-01/` | Pakiet błędów, rodzic odpowiedzi, prompt, nowa odpowiedź, metadane i dowody; każda iteracja osobno |
| `P/reports/correction-01/` | Ponowne kontrole, różnice, poprawione błędy i regresje |
| `P/measurement/` | `sessions.jsonl`, raporty czasu i kosztu; dopisywanie, poprawka wpisu przez nowy rekord |
| `P/decision/` | `comparison.md`, `human-decision.md`, hashe podstawy decyzji; ewentualny publiczny raport zawiera tylko agregaty |

Nazwy `pass-02`, `context-02`, `correction-02/03` oznaczają nowe katalogi, nigdy
nadpisanie poprzednika. Dotychczasowe `private/source-artifacts/` to źródła historyczne;
nie są aktywnym katalogiem odpowiedzi POC. Stare `.glu/` jest w prywatnym archiwum.

Zapis każdego przebiegu obejmuje aplikację, widoczną nazwę modelu i rozumowanie,
źródło tych informacji, moment rozpoczęcia/końca jeśli dostępny, czas użytkownika,
prompt, listę faktycznie przekazanych plików, hashe, sposób odbioru oraz ograniczenia.
Nieznany czas modelu/tokeny/cena pozostają `unknown`, nie zero. Hashe nie dowodzą
autorstwa ani znaczenia; oryginalne odpowiedzi i dowody sesji pozostają potrzebne.

<a id="korekty"></a>
## Pętla korekt i problemy przed M-POC6

Każdy błąd M-POC3–M-POC5 ma ID, klasę, krytyczność, dowód, wpływ i status.
Klasy: **format**, **pominięcie**, **błędny odczyt**, **błędna interpretacja**,
**brak kontekstu**, **niejednoznaczność**. Problemy operacyjne raportować osobno.

1. Zamknij raport bieżącej odpowiedzi przed zmianą. Zapisz nieocenialne metryki
   jako `not_assessable` i powód; nie zakładaj zera błędów.
2. Jeśli format blokuje dalszą ocenę, uruchom kartę M-POC6A w trybie wczesnym:
   najwyżej jedna korekta formatu, liczona do całego budżetu trzech korekt.
   Zachowaj pierwszy wynik jako osobny baseline, ocenę czytelnej korekty jako `format-repair-01`.
3. Dla braku kontekstu użyj M-POC4A/B; dla błędów odczytu/znaczenia przygotuj
   ograniczony pakiet M-POC6A. Niejednoznaczność źródła pozostaje do przeglądu
   właściciela, nie jest naprawiana samą deklaracją modelu.
4. Nową kompletną odpowiedź uzyskaj ręcznie. Nie poprawiaj lokalnie historii ani
   nie zastępuj jej fixture'em. Przepisanie technicznego JSON do osobnego pliku
   jest dopuszczalne tylko bez zmiany treści i ze śladem do surowych bajtów.
5. M-POC6B ponawia format/ID/referencje/dowody oraz kontrole dotkniętych i krytycznych
   elementów. Porównaj także wcześniej poprawne sytuacje, żeby wykryć regresje.
   Wracaj do przerwanego M-POC3/4/5, bez pozornego zaliczania późniejszych etapów.

Po wykorzystaniu budżetu przejdź z raportem ograniczeń do decyzji, nie wykonuj
kolejnych wywołań. Brak odpowiedzi zatrzymuje zależną pracę; można przygotować
raport dostępności. Brak źródła zapisuje cel i blokowane sytuacje. Brak przeglądu
pozostawia `waiting_review`; model nie podpisuje się za człowieka.

## Limity eksperymentu

Domyślne limity planu do zamrożenia wraz z `eval-v1` w M-POC1C:

- podstawowy zakres: siedem stron granicznych/core, z rozdzieleniem kolumn;
- kontekst: maksymalnie **8 dodatkowych różnych stron, 20 dodatkowych reguł,
  4 dodatkowe tabele, 2 kroki zależności i 2 rundy**; obowiązuje pierwszy osiągnięty limit;
- korekty: maksymalnie **3 odpowiedzi korekcyjne łącznie**, w tym najwyżej jedna
  wczesna korekta formatu; odpowiedzi z samym nowym kontekstem mają osobny licznik dwóch rund;
- czas użytkownika: do **8 godzin łącznie**, w tym najwyżej **4 godziny po pierwszej
  ekstrakcji**. M-POC0 raportujemy osobno jako koszt reorganizacji, nie koszt ekstrakcji;
- próba pierwsza: jedna kompletna odpowiedź. Brak odpowiedzi zapisujemy jako awarię,
  a ponowienie wymaga jawnego nowego ID i mieści się w łącznym czasie, bez cichego wyboru najlepszego wyniku.

Przed dodaniem kontekstu policz przyrost, współdzielone strony licz raz, zapisuj
także liczbę unikalnych reguł/tabel i najdłuższą ścieżkę. Cel bez numeru ma lokalne ID.
Limit nie daje prawa do całej instrukcji. Jego zwiększenie wymaga nowej wersji planu
i decyzji właściciela przed następną próbą; nie poprawia retrospektywnie wyniku tego eksperymentu.

## Pomiar

Każda metryka ma licznik, sprawdzony mianownik, wersję oceny, metodę dopasowania,
listę nierozstrzygniętych przypadków i pokrycie przeglądu. Przy mianowniku zero lub
niesprawdzonym podaj `n/a`, bez procentu. Rozlicz każdy element inwentarza jako
poprawny, błędny, pominięty, zablokowany lub jeszcze nieoceniony.

| Obszar | Metoda i ograniczenie |
|---|---|
| Reguły | Poprawnie reprezentowane oznaczenia i klauzule / ręcznie potwierdzone oczekiwane; osobno liczba znalezionych oznaczeń i poprawność znaczenia |
| Relacje jawne i niejawne | Osobne TP/FP/FN: dopasowanie celu, źródła, kierunku i rodzaju do sprawdzonego zestawu; precyzja TP/(TP+FP), kompletność TP/(TP+FN) |
| Relacje nowe | Dodatkowa krawędź poza gold wymaga osobnego review; pending nie jest TP ani pewnym FP. Do finalnej precyzji ocenić wszystkie proponowane krawędzie; wcześniej raportować zakres oceny |
| Kierunki i rodzaje | Liczba poprawnych i błędnych par; zły kierunek/rodzaj nie jest pełnym TP. Wzmianki oceniane osobno od wykonawczych zależności |
| Braki i dopowiedzenia | Cele nierozstrzygnięte, niepoparte krawędzie, krytyczne i niekrytyczne luki, poprawnie zgłoszone blokady i nieoznaczone braki |
| Treść | Liczby, jednostki, negacje, warunki, wyjątki, czas, tabele, diagramy: osobne liczniki oczekiwań i błędów, z krytycznością |
| Kontekst | Dodatkowe strony/reguły/tabele, kroki i rundy; także nieskuteczne rozszerzenia i uzasadnienie każdego |
| Sytuacje | Wszystkie 15–20: poprawny wynik, błędny wynik, właściwa blokada, nieuzasadniona blokada, nieocenione; brak kontekstu nie znika z mianownika |
| Koszt | Iteracje, odpowiedzi bez wyniku, poprawione błędy, regresje, czas użytkownika według etapu, dostępny czas modelu i całkowity; tokeny/cena tylko gdy udokumentowane |

Dla pełnej precyzji TP obejmuje wszystkie ręcznie potwierdzone propozycje, także
poprawne nowe krawędzie spoza zamrożonego zestawu; FP obejmuje ocenione błędne lub
niepoparte propozycje. Dla kompletności TP i FN dotyczą wyłącznie zamrożonego zbioru.
Raport rozróżnia `TP_output` i `TP_gold`; nowe krawędzie nie powiększają potajemnie
mianownika gold. Duplikaty tej samej relacji nie zwiększają TP, są błędem formatu.

Raportuj trzy osobne kolumny: **pierwszy wynik**, **po dodaniu kontekstu**,
**po korektach**. Wczesna naprawa formatu jest czwartą jawnie oznaczoną obserwacją,
nie zamiennikiem pierwszego wyniku. W porównaniu podaj chronologię i hashe rodziców,
aby nie przypisywać poprawy korekt samemu dodaniu kontekstu.
Nie jest to kontrolowany pomiar przewagi modelu ani generalizacja na inne gry.

## Decyzja i akceptacja

Progi są operacyjną definicją użyteczności tej próby. M-POC1C utrwala je przed wynikiem.
Podstawą jest końcowy przegląd właściciela; walidator ani zgodna opinia modelu go nie zastępują.

**Kontynuować do projektu architektury**, jeśli w limitach:

- wszystkie krytyczne oczekiwania są poprawne; zero krytycznych błędów znaczenia,
  nieoznaczonych luk i niepopartych twierdzeń uznanych za fakt;
- wszystkie 15–20 sytuacji oceniono: prawidłowy wynik lub źródłowo uzasadniona
  oczekiwana blokada; co najmniej 80% całego zestawu ma poprawny merytoryczny wynik,
  a żadna sytuacja oznaczona przed próbą jako rozstrzygalna nie pozostaje bezpodstawnie zablokowana;
- kompletność poprawnych reguł oraz precyzja i kompletność zależności wynoszą
  co najmniej 95% na sprawdzonych mianownikach, **osobno dla jawnych i niejawnych**;
  pusty zbiór ma `n/a` i nie potwierdza jakości tej kategorii;
- każda krytyczna zależność ma źródło i dowód albo jawnie blokuje rozstrzygnięcie;
  wszystkie pozostałe błędy są opisane i świadomie wyłączone z przyjętego zakresu;
- czas i liczba prób mieszczą się w budżecie, a właściciel uznaje koszt za użyteczny.

**Poprawić metodę i zaplanować nowy ograniczony eksperyment**, jeśli progi kontynuacji
nie są spełnione, ale po ostatniej dozwolonej iteracji nie ma niekontrolowanego zgadywania,
kompletność reguł i metryki relacji mają co najmniej 80%, a poprawne rozstrzygnięcia
obejmują co najmniej 70% wszystkich sytuacji. Raport musi wskazać konkretną przyczynę,
proponowaną zmianę i nowy limit. Brak źródła, nierzetelny gold, skażenie oceną lub
niedostępny pomiar oznaczają potrzebę poprawy projektu eksperymentu, nie dowód jakości modelu.

**Odrzucić obecną metodę jako podstawę architektury**, jeśli przy wiarygodnym zestawie
oceny po wyczerpaniu limitu wynik spada poniżej powyższych progów naprawy, pozostaje
krytyczne zgadywanie mimo raportu/korekty lub ręczne odtworzenie wyniku dominuje koszt.
Przekroczenie budżetu uniemożliwia „kontynuować”; właściciel wybiera udokumentowaną
poprawę metody albo odrzucenie. Przy braku mierzalnego wyniku nie deklarujemy przewagi
ani porażki konkretnego modelu. M-POC7 zachowuje również negatywne wyniki.

## Poza zakresem

Pełny język reguł, silnik gry, importer, magazyn rewizji, akceptacja KB, integracja
GLU, API inferencji, automatyzacja GUI, porównanie modeli bez eksperymentu,
automatyczne użycie starego kodu i rozszerzenie na całą instrukcję.
M-POC7 może zaproponować architekturę i zakres ponownego użycia archiwum,
ale jej implementacja wymaga osobnego kolejnego planu.
