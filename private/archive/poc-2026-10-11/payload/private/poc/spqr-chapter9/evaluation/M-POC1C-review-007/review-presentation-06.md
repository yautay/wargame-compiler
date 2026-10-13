**Kandydat `03` jest gotowy do przeglądu zakresu.** Sprawdziłem zgodność SHA-256 i rozmiarów wszystkich 22 plików wskazanych przez manifest: danych, źródła i dokumentów pochodzenia.

Proponowany zakres oceny:

| Element | Zakres |
|---|---|
| Treść | 66 grup sprawdzonych lokalnych treści |
| Brakujący kontekst | 8 wymagań ocenianych osobno |
| Sytuacje testowe | 20: 17 wyników lokalnych i 3 uzasadnione blokady |
| Zależności wykonawcze | 5 relacji jawnych i 3 niejawne |
| Kontrole dodatkowe | 7 wzmianek i 7 fizycznych kontynuacji tekstu |

Pozostałe **105 propozycji zależności pozostaje niepotwierdzonych**. Zestaw pozwala ocenić wskazane zakresy; nie potwierdza kompletności całego rozdziału ani grafu.

Sposób oceniania:

- Grupa treści otrzymuje punkt, gdy wszystkie jej potwierdzone składniki są poprawne, poparte dowodem i bez krytycznej sprzeczności. Częściowe wykonanie raportujemy osobno.
- Osobno sprawdzamy liczby, jednostki, negacje, warunki, wyjątki, czas, tabele i diagramy. Kategorie mogą się nakładać; ich punktów nie sumujemy do kompletności treści.
- Relacje oceniamy według źródła, celu, kierunku i rodzaju. Końcowa precyzja wymaga przeglądu **wszystkich relacji zaproponowanych przez ekstraktor**, również nowych.
- Każda sytuacja pozostaje jednym przypadkiem. Uzasadniona blokada jest poprawnym zachowaniem, ale nie liczy się jako wynik merytoryczny do progu 80%.

**Progi pozostają zgodne z planem:** zero krytycznych błędów, nieoznaczonych luk i niepopartych faktów; wszystkie 20 sytuacji ocenione, minimum 16 z poprawnym wynikiem merytorycznym; co najmniej 95% kompletności treści oraz precyzji i kompletności relacji, osobno jawnych i niejawnych.

Przy tej małej próbce próg kompletności relacji oznacza **5/5 i 3/3**. Choć 63/66 grup osiąga liczbowo 95%, każda grupa zawiera krytyczny zakres — wymóg poprawności wszystkich krytycznych składników nadal obowiązuje.

Limity eksperymentu:

- 7 stron podstawowych; dodatkowy kontekst: maksymalnie 8 stron, 20 reguł, 4 tabele, głębokość 2 zależności i 2 rundy.
- Maksymalnie 3 odpowiedzi korekcyjne, w tym najwyżej jedna wczesna naprawa formatu.
- Maksymalnie 8 godzin aktywnego czasu użytkownika łącznie, w tym 4 po pierwszej ekstrakcji.

Dotychczasowy aktywny czas pozostaje nieznany, więc dostępnego budżetu czasu nie mamy potwierdzonego. Zakres tabel i diagramów jest ograniczony do wcześniej sprawdzonych fragmentów; nie obejmuje pełnego odczytu wszystkich wartości i procedur zewnętrznych.

**Czy zatwierdzasz ten zakres, sposób oceniania, ograniczenia oraz progi i limity?** Możesz odpowiedzieć „zatwierdzam zakres” albo wskazać zmianę. Zamrożenie pakietu będzie następną, osobną decyzją.

Twoja akceptacja jest wymagana przez [kartę M-POC1C](https://github.com/yautay/wargame-compiler/blob/ae8f6f0433500933af4978b8f9ed50d828e6b5d0/docs/work/tasks/M-POC1C.md), która przypisuje właścicielowi zatwierdzenie podstawy oceny i limitów.
