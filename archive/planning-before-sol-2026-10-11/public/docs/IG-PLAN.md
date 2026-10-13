# Plan WGC: pełna instrukcja i KB WGU do IG

- **Data:** 2026-10-11.
- **Kierunek:** digitalizacja do IG; plan wykorzystania KB i pełnej instrukcji zlecony przez właściciela.
- **Status:** architektura i plan zapisane; implementacja nie rozpoczęta.
- **Pierwszy wynik:** IG całej instrukcji podstawowej SPQR 5E, z reużyciem KB WGU.
- **Kryterium docelowe:** deterministyczne, szybkie legalne akcje i zmiany
  stanu dla przyszłego AI, bez wydawania tokenów na interpretację legalności.
- **Zakres tej pracy:** wyłącznie plan; bez implementacji.

[Architektura integracji](IG-WGU-ARCHITECTURE.md) określa wejścia, mapowanie,
moduły, review i kryteria wyniku. [Model](IG-DATA-MODEL.md) pozostaje draftem,
a [profile mechanik](IG-MECHANICS-PROFILES.md) opisują również późniejsze
możliwości wykonawcze. [Kontrakt legalnych akcji](IG-LEGAL-ACTIONS.md)
określa wymagania stanu, decyzji, kompilacji, szybkości i oszczędzania kontekstu.
[ADR-0040](adr/ADR-0040-ig-i-archiwum-poc.md)
pozostaje decyzją kierunkową; [POC](../archive/poc-2026-10-11/README.md)
jest nieukończonym archiwum, bez aktywnej kolejki.

## Zmiana planu po doprecyzowaniu celu

Właściciel wskazał pełną instrukcję i wykorzystanie KB sąsiedniego WGU.
Zastępuje to wcześniejszą rekomendację małego pilota oraz prób pięciu rodzin
przed pracą nad pełnym SPQR. Nie trzeba ponownie podejmować decyzji, czy
chcemy pełnej instrukcji. Etapy są częściami budowy jednego narzędzia
i jednego pełnego wyniku. Rozdziały porządkują pracę, nie ograniczają celu.

WGC importuje istniejącą atomizację, sprawdza powiązania ze źródłem i uzupełnia
luki. Nie zakładamy, że rekord KB jest zawsze poprawną jednostką IG.
Instrukcja i jej pełny spis fragmentów są niezależną podstawą kontroli pokrycia.

## Etapy i kryteria odbioru

| Etap | Zakres pracy | Wymagany wynik |
|---|---|---|
| IG-0 | Recenzja oraz architektura WGU + źródła → IG → legalne akcje | Raport, architektura i plan zapisane; kierunek doprecyzowany przez właściciela |
| IG-1 | Kontrakt IG z warstwą semantyczną, snapshot wejść, adapter WGU, walidator | Cała KB zaimportowana bez utraty pól; kontrakty stanu i akcji przygotowane, źródła i braki rozliczone |
| IG-2 | Pełny inwentarz instrukcji i uzgodnienie KB ze źródłem | Wszystkie 44 strony i ich regiony rozliczone; mapowanie wiele-do-wielu; pominięcia, duplikaty i sprzeczności w kolejce |
| IG-3 | Formalizacja i review pełnej instrukcji | Stan, akcje, warunki, wybory, reakcje, skutki, tabele i widoczność mają sprawdzoną semantykę; blokady wykonania jawne |
| IG-4 | Kompilacja i deterministyczny mechanizm reguł | Pakiet dla profilu SPQR, legalne akcje i walidator, zmiany stanu, replay, aktualizacje i pomiary kosztu; brak LLM w legalności |
| IG-5 | Integracja przeciwnika AI i kolejne profile | AI wybiera spośród legalnych decyzji przez zwięzły interfejs; dalsze scenariusze i OSG/GCACW jako osobne rozszerzenia |

IG-2 daje pełny snapshot roboczy, nawet jeśli wymaga korekt. IG-3 formalizuje
jego znaczenie, a IG-4 dostarcza mechanizm dla AI. Żaden etap nie może
nazywać luk pokryciem treści ani oczekującego review akceptacją.

## Kolejność realizacji

1. W IG-1 wprowadzić minimalny kontrakt klauzul z aspektami, źródeł,
   origin bindings, relacji, luk, coverage i review oraz kontrakty stanu,
   akcji i procedur potrzebne kompilacji. Dodać bezpieczny parser
   oraz adapter katalogu WGU; cała KB jest wejściem integracyjnym.
2. Zamrozić dostępny PDF jako jawnie wybrane źródło nowego IG. Nie przypisywać
   mu tożsamości bajtowej brakującego wejścia WGU. Brakujące karty i księgę
   scenariuszy zapisać w rejestrze, wraz z konsekwencjami dla profilu.
3. W IG-2 zbudować pełny indeks źródła, a następnie uzgodnić wszystkie rozdziały
   i obiekty towarzyszące z KB. Powstaje cały graf roboczy.
4. W IG-3 obsługiwać kolejkę różnic według wpływu i zależności. Formalizować
   wszystkie reguły wpływające na legalność i skutki w wybranym profilu.
   Każda klauzula ma formalizację, uzasadniony status informacyjny lub blokadę.
   Struktura
   review powstaje już w IG-1; tu dochodzą wygodne pakiety z dowodem i diffem
   oraz przegląd treści całego deklarowanego zakresu.
5. W IG-4 skompilować sprawdzoną semantykę do pakietu reguł i zbudować
   deterministyczną bibliotekę legalności i zmian stanu. Sprawdzić zgodność
   generatora z walidatorem, pełność domen, reakcje, replay i wycieki informacji.
   Mierzyć czas odpowiedzi i rozmiar widoku decyzji; zastosować indeksy
   i cache z kontrolą poprawności. Wykonać aktualizację wejść z zachowaniem review.

Pierwsza karta implementacyjna: [IG-1](work/tasks/IG-1.md).
Minimalny format będzie doprecyzowany na podstawie rzeczywistego importu
i potrzeb legalnych akcji. Nie projektować pełnego uniwersalnego języka
wszystkich gier przed wdrożeniem SPQR.

## Zakres odbioru pełnego IG

- Każdy plik i rekord wejściowy ma rozliczenie: mapowanie, zachowany payload
  lub jawny błąd. Nieobsługiwane pole nie znika.
- Każda strona i region niezależnego inwentarza źródła ma pokrycie,
  lukę albo uzasadnione wyłączenie. Raport osobno liczy te kategorie.
- Klauzule i relacje prowadzą do dowodów lub konkretnej luki; zakres źródła,
  wydania, opcji i scenariusza jest jawny.
- Można znaleźć regułę po ID WGU, numerze źródła i tekście; odczytać jej
  źródło, wyjątki, zależności, niejasności i aktualny status review.
- Żaden status verified, complete ani gotowa odpowiedź WGU nie nadają same
  z siebie statusu zweryfikowanego IG.
- Aktualizacja wejścia zachowuje ID, historię i rozstrzygnięcia; konflikty
  i nieaktualne podstawy review są raportowane.
- Wydanie gotowe dla AI ma domkniętą semantykę legalności, skutków i kolejności
  w deklarowanym profilu. Opaque wpływające na decyzję jest blokadą wydania.
- Legalność nie wymaga LLM. AI dostaje widok gracza i dokładne legalne wybory,
  a wybrana akcja jest walidowana względem aktualnego stanu.

Pełna instrukcja nie oznacza automatycznie pełnej digitalizacji wszystkich
komponentów gry. Wydanie wymienia brakujące materiały. Brak map lub danych
żetonów nie blokuje opisania instrukcji, ale blokuje twierdzenie o gotowości
do rozstrzygania zależnych od nich sytuacji.

## Walidacja i koszt

Kontrole importera używają syntetycznych fixture oraz prywatnego pełnego
wejścia SPQR. Sprawdzają utratę danych, referencje, wersje, rewizje,
pokrycie i aktualność review. Mechanizm ma dodatkowo testy legalności,
kompletności wyborów, skutków, losowości, powrotów i prywatności.
Przypadki semantyczne są sprawdzane ze źródłem;
pytania kontrolne KB są materiałem regresji, nie niezależnym gold.
36 wcześniejszych przypadków badawczych nadal ma status proposed_not_run.

Mierzyć czas podczas realizacji pełnego celu, osobno dla dopasowania,
review, korekt i konfliktów. Pierwsze ukończone pakiety aktualizują prognozę
pozostałej pracy; nie są nową bramką pilota. Budżety POC i wcześniejszy
proponowany limit dwóch godzin nie są przyjętym ograniczeniem.

## Stan decyzji

[Recenzja IG-0](reviews/IG-0-critical-review.md) pozostaje zapisem wykonanej
analizy. Jej propozycja D3 o małej próbie została zastąpiona kierunkiem
właściciela. Pozostałe wybory skonsolidowano w
[architekturze](IG-WGU-ARCHITECTURE.md): przypięcie źródeł, scenariusz/opcje
pierwszego profilu wykonawczego, organizacja review i warunki pomiarów.
IG-0 jest zakończone jako recenzja i planowanie, nie jako akceptacja semantyki
gry. IG-1 to następna praca implementacyjna, niewykonana w tej sesji.
Dokładny schemat danych pozostaje draftem do dopracowania podczas budowy.

Ta sesja przygotowuje plan. Implementacja, silnik, UI produktu, API inferencji,
nowe czaty/agenci oraz zmiany w WGU lub archiwach nie są jej zadaniami.
