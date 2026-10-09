# M-POC1C — konkretny kandydat 03 do przeglądu zakresu

Data klienta: 2026-10-09, Europe/Warsaw. Stan: partial/waiting_review.
Pakiet `eval-v1-candidate-20261009-03` nie jest zamrożony. Potrzebne są jeszcze
akceptacja proponowanego sposobu pomiaru i osobna rzeczywista decyzja freeze.
Akceptacja zakończenia B ani pięć decyzji C nie zastępują żadnej z tych bramek.

Źródło: SPQR, 5th Edition; SHA-256
`e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.
Core PDF31 prawa od 9.0 do PDF37 lewa przed 10.0; reszta kontekst.
Weryfikacja stabilnego PDF, rodzica 02, overlay i decyzji przed złożeniem.
Dokładne hashe plików oraz rodziców w manifest.json. Wszystkie stare bajty
pozostają niezmienione; dawny HEAD/indeks jest historycznym snapshotem.

## Gotowy zakres, nie cały rozdział ani pełny graf

- Inwentarz referencyjny: 207 rekordów (190 bazowych i 17 spanów A), w tym
  41 oznaczeń, 98 grup tekstu, 14 not, 1 tabela, 2 diagramy i 7 kontynuacji.
  A potwierdza ograniczoną strukturę, nie semantykę wszystkich rekordów.
- 74 ID oczekiwań: 66 grup zatwierdzonych lokalnych treści i 8 wymagań kontekstu.
  Tylko reviewed_scope jest treścią porównania; pole limitów ani nieprzejrzane
  metadane nie stają się odpowiedzią wzorcową. Grupowanie jest propozycją C.
- 20 sytuacji: 17 wyników lokalnych i 3 blokady (SIT-06/11/18); żadnej nowej próbki.
  Wszystkie warianty jednej sytuacji muszą być poprawne; nie pompują mianownika.
- Relacje wykonawcze: 5 jawnych i 3 niejawne, 8 różnych krotek w dokładnym zakresie.
  Jawne: DEP-008, DEP-002, DEP-017, DEP-024, DEP-041, z pięciu rzeczywistych zgód C.
  Niejawne: DEP-NEW-001/002/003, z zatwierdzonych zakresów B.
- 7 wzmianek: wystąpienia informacyjne, bez certyfikatu aliasów/identyfikacji celów.
  7 kontynuacji fizycznych: osobna kontrola, poza wykonawczym TP/FN.
- 105 innych wykonawczych propozycji: 94 jawne i 11 niejawnych, w tym DEP-031.
  Nie są gold ani pewnym FP; nie udajemy, że cały graf zweryfikowano.

Kontrola rozliczenia: 5+3+94+11+7+7 = 127 facetów. Te 127 nie stanowi
mianownika jakości relacji. W zamrożonym lokalnym zbiorze recall ma 5 i 3.
Pełna precyzja wymaga późniejszego przeglądu WSZYSTKICH krawędzi odpowiedzi.
Nowe poprawne krawędzie zwiększają TP_output, nie zmieniają TP_gold ani gold.
Pending spoza zbioru nie jest TP ani pewnym FP; duplikaty nie dodają punktów.

## Proponowane rubryki i kontrola mianowników

Jedna grupa treści dostaje punkt tylko za komplet poprawnych, należących do niej
potwierdzonych składników w zadanym zakresie, z dowodem i bez krytycznej sprzeczności.
Opisane braki, kontekst i odwołanie do składnika należącego do innego EXP-ID nie
dodają punktów. Nie nadajemy ułamkowego sukcesu za częściową grupę; błędy/fragmenty
raportujemy osobno. To porównanie 66 zakresów, nie 66 całych reguł ani norm atomowych.

Kategorie są nową, jawną propozycją pomiaru opartą o reviewed_scope, nie przejęciem
historycznych dimensions_reference_only. measurement-policy.json podaje każde ID
i zakres jednostki. Jedna para kategoria/EXP-ID jest jedną jednostką diagnostyczną.
W jednej kategorii punkt wymaga zachowania wszystkich jej potwierdzonych składników.
Nakładanie kategorii jest jawne; ich liczb NIE SUMOWAĆ do kompletności treści.

| Kategoria | Proponowany mianownik grup |
|---|---:|
| numbers | 41 |
| units | 38 |
| negations | 43 |
| conditions | 66 |
| exceptions | 52 |
| time | 29 |
| tables | 7 |
| diagrams | 1 |

Oddzielnie 2 stany ilustracji/markerów: EXP-054 Fire/Move i EXP-057 Once/Finished.
Nie są nowymi punktami reguł ani wszystkimi glifami. Jeden mianownik diagramów
dotyczy tylko EXP-046 i zaakceptowanej relacji Original/After oraz unstacking.
Nie dotyczy całości obu diagramów. Tabele: tylko lokalne wyniki 9.14 albo obowiązek
użycia wskazanej tabeli/zachowania jej not; brak rzeczywistych lookup MRRC/CRT/MCC.

Kategorie podają poprawne/błędne/pominięte/zablokowane/nieocenione. Plan nie ustanawia
osobnych progów procentowych każdej z tych kategorii; ich nie dodajemy. Obowiązuje
zero krytycznych błędów. Liczby oznaczeń/odwołań do reguł nie są liczbami gry.
Znane jednostki CH/MP/hex/DRM/rating/phase/turn zachować; nie wyliczać realnych żetonów.

## Utrzymane ograniczenia

- EXP-002: pokazane +1 DRM i 5→2/3→2 pozostają poprawne lokalnie; bazowe 0 Hits,
  dolna granica redukcji oraz kolejność pozostałych modyfikatorów nierozstrzygnięte.
- EXP-031: AS/printed result/halve oraz kolejność wymagają tabel/kontekstu.
  EXP-030/SIT-09 są wariantem bez AS, nie rozwiązaniem tego konfliktu.
- DEP-031: hipoteza tożsamości wierszy MRRC wyłączona z gold, nie dowodzi strzału.
- 8 wymagań kontekstu: EXP-010 kompas; EXP-019 rzeczywiste wyjątki dowodzenia;
  EXP-031 jak wyżej; EXP-033 scenario eligibility; EXP-050 data/OC/AWL bitwy;
  EXP-064 commander/Initiative/command; EXP-066 właściwe Combat Tables/entries;
  EXP-074 rzeczywisty zidentyfikowany żeton/parametr. Lokalny znany obowiązek jest
  osobny od nieznanych danych. Syntetyczne wartości sytuacji nie zastępują źródeł.
- EXP-040: tylko indywidualna eliminacja PH bez legalnego Rout. Retreat edge,
  geometria, 6.69/10.22, kolejność/wspólne jedyne miejsce i dalszy D1 są otwarte;
  odczyt 10.24/25/23 nie stanowi pełnego rozstrzygnięcia.
- Rzut wyzwalający 4.84 a pierwszy kierunkowy 9.14, depleted BI/Ferocity ordering,
  pełne Shock allocation, OW, casualty, supply i eligibility są otwarte.
- Pełne normy atomowe, drobne glify/wartości ilustracji, nieprzejrzane metadane/aliasy
  i parametry nie mają gold. Akceptacja tabeli jako celu relacji nie zamraża każdego pola.

Blokada ma zakres i konkretną przyczynę. Po dostarczeniu kontekstu trzeba ocenić,
czy nadal zachodzi; nie nagradzać automatycznej blokady przy dostępnym źródle.
Wynik lokalny sytuacji nie jest pełną legalnością ani wynikiem gry.

## Czy podstawa pozwala uczciwie mierzyć planowane kategorie?

Tak, dla jawnie ograniczonych lokalnych treści, 5 jawnych/3 niejawnych relacji,
20 sytuacji i wypisanych rubryk. To mała, nierównomierna próba, a nie certyfikat
kompletności całego rozdziału/grafu, jakości ogólnego odczytu tabel/diagramów
ani przewagi modelu. Pełna precyzja wymaga późniejszego review całej odpowiedzi.
Pomiary kosztu są możliwe tylko tam, gdzie dostępne są rzeczywiste dane; unknown
nie potwierdza przestrzegania budżetu. Wniosku do architektury nie uzasadnia samo
osiągnięcie lokalnego procentu bez pozostałych bramek i przeglądu właściciela.

## Niezmienione progi POC-PLAN

Kontynuować: wszystkie krytyczne zakresy poprawne; zero krytycznych błędów,
nieoznaczonych luk i niepopartych faktów; wszystkie 20 sytuacji ocenione;
minimum 16/20 poprawnych merytorycznych wyników (80%, blokady nie są wynikiem);
co najmniej 95% kompletności treści i P/R relacji osobno jawnych/niejawnych.
Arytmetycznie 63/66, 5/5 jawnych i 3/3 niejawnych spełniają próg recall.
Jednak wszystkie 66 grup mają potwierdzone krytyczne zakresy: zero błędów krytycznych
jest nadrzędne wobec 63/66. Podobnie wszystkie 20 sytuacji mają krytyczny lokalny zakres.
Każda krytyczna zależność ma źródło/dowód albo blokuje konkretne rozstrzygnięcie;
pozostałe wyłączenia jawne. Budżet zachowany i właściciel uznaje koszt za użyteczny.

Poprawić metodę: po ostatniej dozwolonej iteracji bez niekontrolowanego zgadywania,
minimum 80% reguł i relacji oraz 14/20 wyników sytuacji (70%), z konkretną przyczyną
i nowym ograniczonym planem. Recall arytmetycznie 53/66, 4/5 i 3/3.
Brak wiarygodnego gold/źródła/pomiaru wymaga poprawy projektu eksperymentu,
nie dowodzi jakości ani porażki konkretnego modelu.
Odrzucić: poniżej progów naprawy przy wiarygodnej ocenie po wyczerpaniu limitów,
utrzymujące się krytyczne zgadywanie albo dominujący ręczny koszt odtworzenia.
Przekroczenie budżetu wyklucza „kontynuować”.

## Niezmienione limity POC-PLAN

7 stron core. Kontekst: maksymalnie 8 nowych różnych stron, 20 reguł, 4 tabele,
2 kroki zależności i 2 rundy; obowiązuje pierwszy osiągnięty limit.
3 odpowiedzi korekcyjne łącznie, najwyżej 1 wczesna korekta formatu.
Odpowiedzi wyłącznie z kontekstem mają osobny licznik 2 rund.
8 godzin aktywnego czasu użytkownika łącznie, najwyżej 4 po pierwszej ekstrakcji.
Jedna kompletna pierwsza odpowiedź; retry wymaga jawnego nowego ID i budżetu.
Koszt M-POC0 osobno. Czas aktywny dotychczas, tokeny i cena unknown;
czas kalendarzowy rozmowy nie dowodzi dostępnego budżetu. Same hashe nie dowodzą znaczenia.

## Decyzja teraz i wznowienie

Pytanie 06 dotyczy konkretnego zakresu, grupowania, rubryk, wyłączeń i progów/limitów.
Po akceptacji zapis decyzji osobno. Następnie odrębne pytanie freeze o konkretny
pakiet i jego hash; dopiero rzeczywista zgoda pozwala utworzyć eval-v1 i
freeze-public-v1 zawierający wyłącznie metadane. Nie nadpisywać historii.
Brak którejkolwiek zgody: partial/waiting_review. Nie wykonano ekstrakcji/M-POC2A/B.
