# M-POC1C — kandydat 02 i bramka dalszego przeglądu

Wynik przygotowania: `partial/waiting_review`. Pakiet pozostaje niekompletny
według bieżącej karty i POC-PLAN. Zawartość zatwierdzonych wcześniej zakresów
przeniesiono z decyzji B; grupowanie pomiarowe i freeze wymagają odrębnej decyzji.

Źródło: SPQR, 5th Edition. SHA-256 stabilnej kopii PDF:
`e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.
Core: PDF31 prawa od 9.0 do PDF37 lewej przed 10.0. Pozostałe fragmenty
stron granicznych i wcześniejsze odczyty PDF10/15/20/39 są kontekstem przeglądu,
bez rozszerzenia zakresu pierwszej ekstrakcji.

## Zawartość i znaczenie liczników

| Zbiór | Liczba | Zakres pomiaru |
|---|---:|---|
| Inwentarz referencyjny | 207 = 190 + 17 spanów | 41 oznaczeń, 98 grup tekstu, 14 not, 1 tabela, 2 diagramy i 7 kontynuacji; przegląd A ograniczony strukturalnie, bez pełnego indywidualnego gold |
| Zgrupowane potwierdzone zakresy treści | 66 ID | Tylko opisane `reviewed_scope`, bez zbiorczej akceptacji całych rodziców; grupowanie jest propozycją C |
| Wymagania kontekstu | 8 ID | EXP-010/019/031/033/050/064/066/074; znane lokalne odczyty zachowane, brak konkretnych wartości/wyników |
| Sytuacje | 20 | 17 lokalnych wyników i 3 blokady; wszystkie w mianowniku, warianty nie dodają próbek |
| Potwierdzone wykonawcze relacje jawne | 0 | Obecnie `n/a`, brakuje pełnego przeglądu pól niezbędnych do dopasowania |
| Potwierdzone wykonawcze relacje niejawne | 3 | DEP-NEW-001/002/003, trzy różne krotki w zaakceptowanych lokalnych zakresach |
| Potwierdzone wzmianki | 7 | Wystąpienia informacyjne; oddzielny licznik, bez dopasowania niepotwierdzonych aliasów/zewnętrznych identyfikatorów |
| Kontynuacje fizyczne | 7 | Osobna kontrola źródła; poza wykonawczym TP/FN |
| Niepotwierdzone wykonawcze kandydatury | 110 | 99 jawnych i 11 niejawnych; obejmują 104 wymagające kontekstu, 5 lokalnych propozycji i 1 hipotezę |

127 facetów rozlicza historyczne 96 kandydatur i późniejsze propozycje;
nie jest mianownikiem 127 sprawdzonych relacji. Trzy zaakceptowane krotki mają
różne źródła/cel/rodzaj, więc nie dublują TP. Nowe krawędzie ekstraktora wymagają
osobnego przeglądu: pending nie jest TP ani pewnym FP. Pełna precyzja wymaga oceny
wszystkich krawędzi odpowiedzi, a recall korzysta tylko z ustalonego gold.

Licznik 86 z kandydata 01 wycofano jako mianownik. Powtarzał fragmenty decyzji,
m.in. wspólny zapis EXP-021/022, późniejszy rally Leader EL i MRRC mounted LI.
Kandydat 01 zachowano bajtowo. `change-map.json` mapuje wszystkie 74 ID do
nowych grup; wielokrotne akceptacje i cytaty stanowią dowody, nie nowe próbki.
Zasady kierunku, rodzaju i jawności pochodzą z planu oraz konkretnych decyzji.

## Granice zastosowania

- EXP-002: potwierdzono pokazane +1 DRM i rachunek 5→2/3→2. Bazowe 0 Hits,
  dolna granica redukcji i kolejność innych modyfikatorów pozostają nierozstrzygnięte.
- EXP-031: printed result/AS/halve wymaga tabel i kontekstu kolejności;
  nie wpisano rozwiązania ani nowego wyjątku. EXP-030/SIT-09 dotyczą wariantu bez AS.
- DEP-031: MRRC/row identity pozostaje niepotwierdzoną niejawną hipotezą,
  wyłączoną z relacyjnego gold; nie jest dowodem obliczenia strzału.
- EXP-010: konkretny kompas mapy; EXP-019: rzeczywiste wyjątki dowodzenia;
  EXP-033: lista jednostek eligible w scenariuszu; EXP-050: data/OC/AWL bitwy;
  EXP-064: commander/Initiative/command mapping; EXP-066: właściwe Combat Tables
  i entries; EXP-074: rzeczywisty zidentyfikowany żeton/parametr. Te źródła
  pozostają potrzebne; syntetyczne TQ/MA w sytuacjach ich nie zastępują.
- EXP-040: zaakceptowano indywidualną eliminację PH bez legalnego Rout.
  Geometria, retreat edge, 6.69/10.22, kolejność i wspólne jedyne miejsce nie mają
  rozstrzygnięcia; lokalny kontekst 10.24/25/23 nie dowodzi pełnego wyniku.
- Relacja rzutu 4.84 do pierwszego kierunkowego DR 9.14, depleted BI/Ferocity
  ordering, pełne Shock allocation, OW, casualty, supply i eligibility są otwarte.
- Pełny podział atomowy, wszystkie wartości/glify ilustracji, nieprzejrzane
  metadane relacji i aliasy nie mają akceptacji. Poprzednie Fire/Move i Once/Finished
  pozostają potwierdzone w ich konkretnych zakresach.

Każda z 20 sytuacji ma osobno zapisane syntetyczne wejścia, lokalny wynik/blokadę,
źródło, overlay i decyzję właściciela. SIT-06/11/18 pozostają blokowane wskazanym
brakiem. Po pozyskaniu odpowiedniego kontekstu trzeba ocenić możliwość rozwiązania;
blokady nie należy bezwarunkowo nagradzać przy dostępnym krytycznym źródle.

## Progi i budżet

POC-PLAN zachowano bez zmian. „Kontynuować”: zero krytycznych błędów, luk
nieoznaczonych i niepopartych twierdzeń uznanych za fakt; wszystkie krytyczne
oczekiwania poprawne; wszystkie 20 sytuacji ocenione, przynajmniej 80% całego
zestawu z poprawnym merytorycznym wynikiem (16/20, blokady nie są takim wynikiem);
co najmniej 95% kompletności reguł i co najmniej 95% precyzji/kompletności relacji
oddzielnie jawnych i niejawnych. Przy trzech niejawnych relacjach potrzeba 3/3
dla recall 95%; tego małego zbioru nie uogólnia się na całą kategorię.
Jeżeli grupowanie 66 treści zostałoby zaakceptowane, 95% odpowiadałoby 63/66,
ale nadrzędny wymóg poprawności wszystkich krytycznych zakresów nadal obowiązuje.

„Poprawić metodę”: po ostatniej dozwolonej iteracji bez niekontrolowanego
zgadywania, minimum 80% dla reguł i relacji oraz 70% wszystkich sytuacji (14/20),
z konkretną przyczyną i nowym ograniczonym planem. Brak wiarygodnej/mierzalnej
kategorii wymaga poprawy projektu eksperymentu, nie dowodzi jakości lub porażki modelu.
„Odrzucić”: poniżej progów naprawy przy wiarygodnej ocenie i wyczerpanych limitach,
utrzymujące się krytyczne zgadywanie lub dominujący ręczny koszt odtworzenia.

Limity: 7 stron core; kontekst maksymalnie 8 dodatkowych różnych stron,
20 dodatkowych reguł, 4 dodatkowe tabele, 2 kroki zależności i 2 rundy — pierwszy
osiągnięty limit. Do 3 odpowiedzi korekcyjnych łącznie, z najwyżej 1 wczesną
korektą formatu; same odpowiedzi kontekstowe mają osobny licznik 2 rund.
Do 8 godzin pracy użytkownika łącznie, w tym najwyżej 4 po pierwszej ekstrakcji.
Jedna kompletna pierwsza odpowiedź; ponowienie ma nowe ID i wchodzi do budżetu.
M-POC0 osobno. Dotychczasowy aktywny czas użytkownika/modelu, tokeny i koszty:
`unknown`. Znaczniki zapisu i czas rozmowy nie potwierdzają pozostałego budżetu.

## Bramka M-POC1C

Kandydat pozwala przygotować lokalne porównania treści i 20 sytuacji. Brakuje
sprawdzonego jawnego mianownika relacji oraz zaakceptowanej polityki grupowania
i szczegółowych rubryk kategorii. Nie spełnia jeszcze wymagań zamrożenia pełnej
podstawy według obecnego planu. Żaden próg nie został obniżony, a `n/a` nie zalicza
95%. W obecnym stanie nie wolno wyciągać wniosku „kontynuować do architektury”.

Najbliższy brak do odrębnej decyzji to pełna krotka DEP-008 (jawny lokalny wyjątek
SK → końcowy Pass-Thru Check). Jej odczyt semantyczny pochodzi z B; pytanie C
dotyczy potrzebnych pól relacji i ich dokładnego zakresu. Po tej decyzji należy
rozliczyć pozostałe potrzebne pola — nie otwierać ponownie całego B.
Gotowość pełnej podstawy i ostateczna zgoda na freeze są osobnymi bramkami.
Zmiana selektora zgłoszona słowami „Podbiłem model na sol” nie zatwierdza żadnej z nich.
