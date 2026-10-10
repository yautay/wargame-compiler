# context-01 - oddzielny raport M-POC4B

Data: 2026-10-10, Europe/Warsaw. Raport zamknięty; karta partial/waiting_review.
Odbiór istniejącej ręcznej odpowiedzi, bez powtórzenia inferencji/korekt.
Oryginał transfer/context-v1/context-01.json i runs/context-01/response.raw.txt
mają identyczne 712014 bajtów, SHA-256 95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
Rodzic first-001, SHA-256 3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307, pozostaje baseline.
Manifest nowego pakietu: 1140a43519ae60646ea783bb24ec4dacc2f608e88d80efd83a206427aa45eff4; eval-v1 niezmienione.

## Pierwszy wynik / po kontekście / po korektach

| Obserwacja | first-001 | context-01 | po korektach |
|---|---:|---:|---|
| Reguły / węzły / relacje / dowody / deklaracje luk | 50 / 58 / 126 / 105 / 81 | 50 / 60 / 131 / 111 / 85 | not_assessable |
| Pełne usunięte deklaracje luk | baseline | 0 | not_assessable |
| Częściowo zaktualizowane wcześniejsze luki | baseline | 4, nadal blocking | not_assessable |
| Zamrożone jawne pary-kandydaci | 5/5 | 5/5 | not_assessable |
| Zamrożone niejawne pary-kandydaci | 0/3 | 0/3 | not_assessable |
| Semantyczne TP/FP/FN i 20 sytuacji | not_assessable | not_assessable | not_assessable |

Nie utożsamiać liczby rekordów/źródłowych operatorów z poprawą znaczenia.
Zmieniły się R932, N932ex, dwa stare rekordy zależności i cztery stare luki.
Dodano dwa węzły, pięć relacji, sześć dowodów i cztery luki. Żaden stary rekord
nie został usunięty. Wszystkie 81 deklaracji luk pozostało; changed_gaps nadal
blocking. D962shock ma teraz cel w dostarczonym fragmencie, lecz jego pełny
wynik pozostaje zablokowany. Interpretacja wyjątku R932 oraz nowa niejawna
relacja ze R923 wymagają review; nie uznano ich za naprawę lub semantyczne TP.

## Kontrole struktury, źródeł i mianowników

480 ID rekordów i 154 ID klauzul unikalnych; 3660 referencji rozwiązanych.
10108 wymaganych kluczy, 832 Field objects, 759 wartości enum, bez błędów
tych kontroli. 41/41 artefaktów nowego manifestu i 42/42 pliki wejściowe,
43/43 wiązania sources, 7/7 artefakty zamrożonej oceny zgodne.
105 odziedziczonych dowodów jest identycznych z baseline; raportuje się
osobno odziedziczone oględziny i obecne helper/hash/geometry checks.

111 krótkich cytatów ma podparcie: 109 matches helper, 2 dawne ograniczone
oględziny potwierdzone śladem identyczności. Wszystkie 6 nowych cytatów pasuje
do pomocniczego tekstu i źródłowego wycinka. 111/111 geometrii/hashów/wymiarów
poprawnych. Dziedziczony błąd E916 nie naprawiony; 58 dawnych granic glifów
pending. Nowe 6 obszarów: 0 ścisłych matches całych glifów, 6 matches glifów
przecinających granice; w oględzinach rasteru wszystkie sześć cytatów czytelne.
Nie nadaje to ścisłego certyfikatu granic: 64 pending łącznie, 41 dawnych
ścisłych matches, 5 dawnych napisów graficznych, 1 błąd obszaru. Nie zmieniono
samego źródła ani bbox w odpowiedzi, nie sprawdzono wszystkich treści/liczb.

207 ID inwentarza rozliczone: 205 kandydatów, 2 lokatory nieocenione; 41/41
różnych oznaczeń. Mapowanie nie dowodzi kompletności każdej klauzuli.
66 grup treści, 8 wymagań kontekstu i rubryki 41/38/43/66/52/29/7/1
zachowują mianowniki i not_assessable. 20 sytuacji (17 lokalnych/3 blokady)
nie rozstrzygnięto na nowo; syntetyczne dane nie stały się rzeczywistym setupem.

Relacje wykonawcze: 75 jawnych, 28 niejawnych; poza nimi 21 wzmianek i 7
kontynuacji. Wszystkie 131 rozliczone. Brakujące trzy krytyczne pary niejawne
i cztery pary wzmianek nadal obecne jako pominięcia strukturalne; różnica
rodzaju jednej wzmianki pending. Wszystkie semantyczne precision/recall
not_assessable. Nowe propozycje spoza gold nie są pewnymi FP ani TP.

Sześć klas: format - 1 dziedziczony błąd lokatora; pominięcie - 7 brakujących
par; błędny odczyt - not_assessable; błędna interpretacja - kandydaci pending,
bez nowego werdyktu; brak kontekstu - 82 deklaracje; niejednoznaczność -
3 deklaracje oraz 64 granice glifów pending. Nie raportować zerowych błędów
znaczenia tylko dlatego, że nie wykonano review człowieka.

## Koszt, głębokość i izolacja

Faktycznie 1 ręczna odpowiedź po kontekście, 0 korekt, 0 nowych inferencji
w sesji oceniającej. Dodatkowe źródło: 1 strona / 1 reguła / 0 tabel.
Wybrana dostarczona ścieżka ma 1 krok, M-POC4A rozważało do 2. Nowy graf
łączy R932/R923/R962 -> NCTX846S4 -> istniejące N1013 -> brakujące 6.68
bullet #6: 3 krawędzie do nierozstrzygniętego celu. Nie pozyskano trzeciego
kroku źródła; na granicy 2 zatrzymano rozszerzanie. Nie deklarować zgodności
głębokości całego grafu. Brakujący cel i jego wpływ zachowano w raporcie;
pass-02 nie uruchomiono i nie wolno go traktować jako obejścia limitu.

Niezależny zapis aplikacji potwierdza start w korzeniu repo, próbę odczytu
nieistniejącej root transfer-list, listę nazw i wyszukiwanie ścieżek poza
allowlistą. Naruszona izolacja dostępu; nie jest to samo w sobie dowód
otwarcia klucza oceny. W dostępnym transkrypcie nie zaobserwowano odczytu
treści oceny; assessment exposure pozostaje unknown, bez certyfikatu czystego
kontekstu i bez dowodu skażenia. Samoopis not_exposed nie zastępuje dowodu.
Snapshot i konkretne komendy są w run.json i prywatnym pomiarze.

App turn: 2026-10-10T16:06:07+00:00 - 2026-10-10T16:18:37+00:00,
749.348 s kalendarzowych. To nie czas
aktywny człowieka/modelu ani ścisły czas inferencji. Model/rozumowanie,
aktywne czasy, tokeny, cena i budżet czasu unknown; żadnej zgodności nie
zadeklarowano. Historyczne konfiguracja/przekazanie/czysty kontekst first-001
pozostają unknown. Odpowiedzi, wejść, źródeł, draftów, freeze, eval-v1 ani
zamkniętego raportu baseline nie zmieniono.

## Wznowienie i bramka człowieka

Karta partial/waiting_review: przygotowano odbiór, niezależne kontrole i
zamknięty raport; człowiek ma potwierdzić zakres efektu dostarczonego fragmentu.
Proponowane rozliczenie: częściowe podparcie procedury i celu źródłowego,
0 pełnych domknięć luk, nierozstrzygnięte znaczenie i reszta blokad jawna.
Nie jest to automatyczne zaliczenie jakości ani 20 sytuacji.
reviews/context-source-01/request.json prowadzi konkretny przegląd tej bramki.
Po jego zamknięciu przejść do M-POC5A/B, oceniając oba wyniki osobno na eval-v1.
Nie powtarzać ekstrakcji, nie edytować odpowiedzi, nie dokładać nowego kontekstu.
Kontrole repo i pomiary zamknięcia są w nowym completion.json; ten raport
pozostaje niezmieniony, a późniejsze decyzje/review są osobnymi artefaktami.
