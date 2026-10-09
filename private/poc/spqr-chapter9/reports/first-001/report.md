# first-001 — zamknięty baseline M-POC3

Data: 2026-10-09, Europe/Warsaw. Zapis UTC: 2026-10-09T19:00:39.677705+00:00.
Wykonawca: Codex, C:/repo/wargame-compiler, feature/tests. Wynik karty: done
w zakresie raportu pierwszego wyniku. Ocena znaczenia: waiting_review.

Odpowiedź ma 617941 bajtów, SHA-256 3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
Manifest wejść: 39e0a65e2f7d0d991c1bd031c6a99e6c40b80fe34e5429640e150fbfbedf340a; manifest eval-v1:
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce. Oryginał to runs/first-001/first-001.json,
zgodnie z run.json, zamiast response.raw.txt. Proposal jest jego bajtowo identyczną
kopią. provenance.json prowadzi każdy JSON pointer do dokładnych zakresów bajtów
i hashy surowej odpowiedzi. Nie zmieniono wejść, manifestów, promptu ani eval-v1.

## Kontrole struktury i dowodów

JSON poprawnie parsuje się jako jeden obiekt UTF-8; brak duplikatów kluczy.
454 ID rekordów i 154 ID klauzul są unikalne. Rozwiązano 3401 referencji;
sprawdzono 9731 wymaganych kluczy, 797 Field objects, 730 wartości enum
i 4 tożsamości koperty, bez błędów tych kontroli. To kontrola roboczego formatu,
bez przyjęcia kontraktu docelowego ani semantycznej akceptacji.

32/32 artefakty manifestu mają zgodne bajty/hashe; 33/33 pliki pakietu kanonicznego
i transferu są identyczne. 34/34 deklaracje źródeł wiążą się z manifestem;
105/105 dowodów ma zgodne źródło, hash, stronę i region. 7/7 artefaktów eval-v1
zgodnych z zamrożonym manifestem. 12/12 regionów core ma mapę w kolejności;
4 regiony kontekstu nie są liczone jako core.

103/105 krótkich cytatów pasuje do pomocniczego tekstu po łączeniu wierszy
i dzielonych słów. Dwa dalsze cytaty zweryfikowano wizualnie: zachowany łącznik
w E911design oraz napis w grafice E911counter. Wszystkie 105 krótkich cytatów
ma źródłowe podparcie w tym ograniczonym zakresie; nie certyfikuje to całych
transkrypcji, liczb, pól reguł ani interpretacji.

105/105 obrazów ma zgodny plik/hash, wymiary PNG, stronę, jawny układ współrzędnych
i poprawne geometrycznie bbox. Kontrola położenia cytatu: 41/105 obejmuje pełne
glify tekstu; 5/105 krótkich napisów graficznych zlokalizowano wizualnie;
58/105 pasuje jedynie do glifów przecinających granice bbox i pozostaje do
przeglądu przycięć. Jeden obszar, E916, nie obejmuje całego cytatu: dolna granica
360 PDF pt urywa końcową linię. To potwierdzony błąd lokatora, mimo poprawnego
cytatu na pełnej stronie. Szczegóły, tekst w bbox i ślad bajtowy: quotes.json,
image-areas.json oraz errors.json. Odpowiedzi nie poprawiono.

## Inwentarz i sprawdzone mianowniki

Rozliczono każde z 207 ID inwentarza. 205 ma kandydata z przecięciem źródłowego
obszaru; dwa nagłówki C-9.94-01/C-9.96-01 mają reprezentację nadrzędną, lecz bez
przecięcia wskazanych dowodów z nagłówkiem. Oba pozostają unassessed_locator,
nie uznane automatycznie za pominiętą treść. Wszystkie 207 ocen znaczenia są
unassessed/not_assessable. Mapowanie przez rodzica nie dowodzi reprezentacji
każdej klauzuli. Znaleziono 41/41 różnych oznaczeń; podział 9.96 nie zwiększa
tego licznika. 50 reguł i 154 klauzule modelu nie są mianownikiem kompletności.

Inwentarz obejmuje 98 grup klauzul, 14 not, 1 tabelę, 3 wiersze tabeli,
2 diagramy, 7 kontynuacji oraz pozostałe rekordy i 17 uzupełniających spanów;
wszystkie ID i typy rozliczono w inventory.json. To inwentarz referencyjny,
bez pełnego gold rozdziału ani sprawdzonego atomowego mianownika.

Przeliczono 66 potwierdzonych grup treści i 8 grup wymagających kontekstu;
wynik semantyczny wszystkich: not_assessable do M-POC5. Mianowniki rubryk:
liczby 41, jednostki 38, negacje 43, warunki 66, wyjątki 52, czas 29,
tabele 7, diagramy 1. Każda para rubryka/EXP-ID ma zapis nieocenialności;
kategorii nie sumuje się jako dodatkowych punktów reguł. Wszystkie 20 sytuacji
(17 oczekiwanych wyników lokalnych, 3 blokady) nieocenione w M-POC3.

## Relacje

Odpowiedź: 126 unikalnych relacji — 72 jawne wykonawcze, 26 niejawnych
wykonawczych, 21 wzmianek i 7 kontynuacji. Każda ma osobny wpis oceny.
Mianowniki zamrożone przeliczono: 5 jawnych i 3 niejawne wykonawcze,
7 wzmianek, 7 kontynuacji. Porównano źródło, cel, kierunek, rodzaj i jawność;
mapowanie całej reguły do zakresu child jest wyłącznie kandydatem.

Jawne: 5/5 kandydatów par. Niejawne: 0/3; brak osobnych relacji
DEP-NEW-001/002/003 w wymaganych zakresach. Krytyczność pochodzi z eval-v1,
nie z nowej oceny za człowieka. Wzmianki: 2/7 kandydatów wystąpienia,
1/7 kandydat o innym rodzaju (D961stack), 4/7 brakujących osobnych par.
Kontynuacje: 7/7 kandydatów z prawidłową fizyczną kolejnością fragmentów.

TP_gold, TP_output, FP, FN oraz semantyczna precyzja/kompletność są
not_assessable; nie nadano pięciu kandydatom semantycznego TP. Pozostałe
67 jawnych i 26 niejawnych propozycji spoza potwierdzonych par czekają na review,
nie są pewnymi FP. Wzmianki i kontynuacje pozostają osobnymi kategoriami.
105 niepotwierdzonych kandydatur eval-v1 nie jest gold.

## Sześć klas

| Klasa | Potwierdzone obserwacje strukturalne | Inne zapisane obserwacje / twierdzenia |
|---|---:|---|
| format | 1 błąd obszaru E916 | format czytelny; bez potrzeby naprawy parsowania |
| pominięcie | 7 brakujących par (3 krytyczne niejawne, 4 wzmianki) | kompletność semantyczna klauzul not_assessable |
| błędny odczyt | not_assessable | 0 wpisów tej klasy, brak pełnego przeglądu transkrypcji |
| błędna interpretacja | not_assessable | 1 kandydat różnicy rodzaju, oczekuje człowieka |
| brak kontekstu | not_assessable | 79 jawnych deklaracji luk ekstraktora, ocena potrzeby/blokad pending |
| niejednoznaczność | not_assessable | 2 deklaracje ekstraktora i 58 przypadków granic glifów, pending |

Deklaracje G916/G953 nie ustanawiają nowej niejednoznaczności gold:
porównanie z wcześniej zatwierdzonymi zakresami EXP-017/040 wymaga M-POC5.
Każda obserwacja ma ID, klasę, krytyczność/unknown, dowód, wpływ i status.
Brak ocenionych błędów znaczenia nie jest zerem błędów. Problemy operacyjne
i niepotwierdzone pochodzenie są oddzielne od sześciu klas.

## Ograniczenia, zamknięcie i wznowienie

Konfiguracja, czas ekstrakcji, faktyczny historyczny prompt/lista przekazanych
plików, czysty kontekst, ekspozycja na ocenę, sposób eksportu, tokeny i cena
pozostają unknown. Samoopis nie jest niezależnym dowodem. Dostępność pakietu
teraz nie dowodzi jego historycznego użycia; nie potwierdzono ślepej próby ani
skażenia. Czas kalendarzowy tej oceny nie jest aktywnym czasem człowieka/modelu
ani czasem ekstrakcji. Nie potwierdzono zgodności z łącznym budżetem.

Baseline zamknięto przed jakąkolwiek korektą, nowym kontekstem lub inferencją;
closure.json wiąże hashe wszystkich artefaktów. Kontrole scripts/check.ps1
oraz git diff --check po aktualizacji dokumentów zapisuje wyłącznie nowy pomiar
measurement/M-POC3-first-001/completion.json i dopisany rekord sessions.jsonl;
nie zmieniają tego zamkniętego raportu. Nowe odpowiedzi i oceny muszą dostać
odrębne ID/katalogi. W tej sesji 0 ekstrakcji, 0 rund kontekstu, 0 korekt.

Dokładny następny krok: osobna karta M-POC4A od run.json, tego report.md,
dependency-comparison.json i listy 79 zadeklarowanych braków w errors.json:
wybrać wyłącznie potrzebne blokujące cele, sprawdzić dostępność źródeł i policzyć
przyrost stron/reguł/tabel oraz głębokość przed tworzeniem context/pass-01.
Nie zamieniać trzech brakujących relacji wewnętrznych w domyślny wniosek,
że potrzebny jest nowy zewnętrzny kontekst. M-POC5 otrzymuje jawny baseline,
nieocenione zakresy i G916/G953 do porównania z zamrożonymi decyzjami.
M-POC4A ani dalszych kart nie rozpoczęto. Semantyczna akceptacja: not_performed.
