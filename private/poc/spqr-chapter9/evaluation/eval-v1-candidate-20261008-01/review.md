# M-POC1C — kandydat eval-v1 przed decyzją właściciela

Status: **candidate / waiting_review**. Ten katalog nie jest zamrożonym `eval-v1`,
nie jest certyfikatem całego grafu i nie autoryzuje M-POC2A/B. Nie utworzono
`freeze-public-v1.json`.

## Podstawa i zakres

Źródło: SPQR, 5th Edition, rozdział 9.0. Core biegnie od nagłówka 9.0 w prawej
kolumnie PDF31 do miejsca przed 10.0 w lewej kolumnie PDF37. Pełny SHA-256 PDF:
`e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`. Treść graniczna poza tym zakresem jest kontekstem.

Kandydat materializuje wyłącznie zakresy rzeczywiście zatwierdzone w decyzjach
M-POC1A i M-POC1B. Oryginalne drafty pozostają rodzicami i nie zostały zmienione.
Każdy rekord prowadzi do rodzica, decyzji i osobnego overlay/mapy zmian.

## Liczebności kandydata

- inwentarz referencyjny: 207 rekordów (190 bazowych + 17 zatwierdzonych strukturalnych spanów); tylko 29 rekordów bazowych ma indywidualnie wskazany zakres przeglądu strukturalnego, bez akceptacji znaczenia;
- oczekiwania: 74 ID, ale mianownikiem semantycznym jest 86 zakresowo zatwierdzonych jednostek twierdzeń, nie 74 całe rekordy draftu;
- sytuacje: 20, w tym 17 lokalnych wyników i 3 uzasadnione blokady; wszystkie pozostają w mianowniku;
- relacje-kandydatury: 127 facetów, w tym 113 wykonawczych (99 jawnych, 14 niejawnych), 7 wzmianek i 7 kontynuacji;
- zakresowo zatwierdzone relacje wykonawcze: 3 niejawne (`DEP-NEW-001/002/003`) i **0 jawnych**;
- potwierdzone wzmianki: 7/7, zawsze poza mianownikiem wykonawczym;
- kontynuacje: 7, raportowane oddzielnie i niewłączane do wykonawczego gold.

## Ograniczenia zachowane w kandydacie

Nie rozstrzygnięto EXP-002 (bazowe 0 Hits i dolna granica redukcji), EXP-031
(AS/LC printed result wobec halve), DEP-031 (niepotwierdzona hipoteza MRRC/row),
rzeczywistego kontekstu EXP-010/019/033/050/064/066/074 ani pozostałego zakresu
EXP-040 (geometria, 6.69/10.22, kolejność i wspólny jedyny cel). Nie rozstrzygnięto
relacji rzutu 4.84 do pierwszego kierunkowego DR 9.14, pełnych procedur Shock/OW/
casualty/supply/eligibility, nieprzejrzanych aliasów i metadanych relacji, pełnej
atomowości ani wszystkich drobnych wartości grafiki. Niczego z tego nie uznano za gold.

## Progi i limity z POC-PLAN.md

Limity bez zmiany: siedem stron core; kontekst maksymalnie 8 dodatkowych różnych
stron, 20 dodatkowych reguł, 4 tabele, głębokość 2 kroków i 2 rundy (pierwszy
osiągnięty limit); łącznie najwyżej 3 odpowiedzi korekcyjne, w tym najwyżej jedna
wczesna korekta formatu; czas użytkownika do 8 godzin, najwyżej 4 po pierwszej
ekstrakcji; jedna kompletna pierwsza odpowiedź, a każde ponowienie z nowym ID.

Próg „kontynuować”: wszystkie krytyczne twierdzenia poprawne; zero krytycznych
błędów znaczenia, nieoznaczonych luk i niepopartych faktów; wszystkie 20 sytuacji
ocenione, co najmniej 80% z poprawnym merytorycznym wynikiem; kompletność reguł
oraz precyzja i kompletność relacji co najmniej 95%, osobno jawne/niejawne;
krytyczne zależności mają źródło albo jawnie blokują; budżet zachowany i koszt
zaakceptowany przez właściciela. Pusty mianownik ma `n/a` i nie potwierdza jakości.

Próg „poprawić metodę”: brak niekontrolowanego zgadywania, co najmniej 80% dla
reguł/relacji i 70% sytuacji po ostatniej dozwolonej iteracji. Poniżej tych progów
przy wiarygodnym zestawie lub przy dominującym ręcznym koszcie metoda jest odrzucana.

## Czy kandydat pozwala uczciwie mierzyć plan

Tak — dla 20 sytuacji, 86 jawnie wydzielonych lokalnych twierdzeń,
siedmiu wzmianek i trzech wąskich niejawnych relacji. Nie — dla kompletności całego
inwentarza/atomowości oraz dla jawnych relacji wykonawczych: licznik zatwierdzonych
relacji jawnych wynosi 0, więc ich precision/recall to `n/a`. Z tego powodu ten
kandydat nie może uczciwie dowieść progu „kontynuować do architektury”, nawet przy
idealnej odpowiedzi ekstraktora. Może służyć jako ograniczona ocena diagnostyczna,
jeżeli właściciel świadomie zaakceptuje ten zakres i konsekwencję.

## Decyzja wymagana przed freeze

Potrzebna jest odrębna decyzja właściciela, czy zamrozić dokładnie ten ograniczony
pakiet z jawnym `n/a` dla relacji jawnych i brakiem dowodu progu „kontynuować”.
Akceptacja zamknięcia M-POC1B nie jest zgodą na freeze.
