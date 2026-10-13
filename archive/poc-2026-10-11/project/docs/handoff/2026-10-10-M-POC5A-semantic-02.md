# M-POC5A — część .2, porównanie EXP-001–025

- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Data: 2026-10-10, Europe/Warsaw. Codex, C:/repo/wargame-compiler,
feature/tests. Polecenie „ok kontynuuj” upoważniło dalsze porównania, lecz
nie zawierało akceptacji poprzednich dokładnych propozycji znaczenia.
Część .1 i jej pytania nadal waiting_review; w tej kontynuacji wykonano
tylko zakres części .2, bez .3/.4, sytuacji, korekt lub architektury.

## Wejścia i integralność

first-001: 617941 bajtów, SHA-256
3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
context-01: 712014 bajtów, SHA-256
95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
eval-v1: SHA-256
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.
Ponownie zgodne. Źródło, wejścia, odpowiedzi, ocena i zamknięte raporty
zachowane; wcześniejsze review i pomiar części .1 również niezmienione.

## Faktyczny zakres i propozycje

Prywatny korzeń: private/poc/spqr-chapter9/.
Nowy pakiet reviews/semantic-01/part-02/: comparisons.json, review.md,
issues.json, owner-focus.md, manifest.json i zapis prezentacji.
current-state-02.json jest osobnym wskaźnikiem dodatku do starego checklist,
bez przepisywania dawnych artefaktów i pomiarów.

Oceniający porównał EXP-001–025, 42 różne powiązane pozycje źródłowe i 88
diagnostycznych par rubryka/oczekiwanie. To 23 zakresy treści i 2 kontekstu:
21 propozycji zgodności lokalnej, 1 zgodności treści z osobnym błędem dowodu,
1 niepełna interpretacja; jedno poparte blokowanie źródła i jedna kwestia
deklaracji blokowania wymagająca rozstrzygnięcia. Przejrzano obrazy PDF31–33
w potrzebnych zakresach; nie certyfikowano wszystkich glifów lub małych cyfr.

W obu wynikach 18 mapowanych reguł/węzłów ma te same wartości, ze śladami
do osobnych bajtów. Nie twierdzimy, że leksykalne bajty rekordów są identyczne.
Odpowiedź po kontekście nadal ma odrębne luki i relacje, które nie zostały
automatycznie zaliczone przez zgodność miejscowej treści.

## Przegląd właściciela i ograniczenia

Pokazano pakiet 22 lokalnych propozycji i nową kwestię blokowania;
brak decyzji pozostaje pending/waiting_review. Zero zaakceptowanych grup
i brak semantycznych TP/FP/FN. 49 pozostałych oczekiwań oraz szersze zakresy
inwentarza, wszystkie relacje i dokładne lokatory nadal pending.
42 pozycje nie oznaczają 42 pełnych akceptacji, a 88 par nie zwiększa
mianownika 66 reguł. Nie przeniesiono akceptacji źródła z M-POC4 na znaczenie.

Bez nowego źródła/pass-02 lub trzeciego kroku. 1 strona/1 reguła/0 tabel,
1 runda kontekstu/0 korekt; w tej części 0 ekstrakcji, 0 kontekstu, 0 korekt,
0 ocen sytuacji. Brak rzeczywistego setupu nie blokuje domyślnie zadanych
lokalnych operatorów. Krytyczny brak blokuje pełny zależny wynik.
Izolacja nazw/ścieżek była naruszona; ekspozycja i czysty kontekst unknown,
bez dowodu pełnego skażenia lub izolacji. Selektory/czasy/tokeny/cena oraz
aktywny budżet unknown; czas kalendarzowy nie jest aktywnym pomiarem.

## Dokładne wznowienie

Właściciel rozstrzyga pokazane zakresy z focus-01.md i part-02/owner-focus.md.
Zapisz jego decyzje osobno z hashami i dokładnym zakresem; nie nadaj
akceptacji za niego ani nie zmieniaj odpowiedzi. Następnie pending części .2
i pełny zakres .3/.4 zgodnie z podziałem do 90 minut. M-POC5 jedyny next,
M-POC5A nadal partial; M-POC5B i M-POC6/7 niewykonane.

## Kontrole i pomiar

scripts/check.ps1 oraz git diff --check, logi, końcowy audyt niezmienności
i append-only sessions.jsonl prowadzi nowy pomiar
measurement/M-POC5A-semantic-02/completion.json. Nie wykonano publikacji Git.
Wynik: **121 passed**, git diff --check bez błędów. Audyt porównań sprawdził
24 różne ślady do oryginalnych rekordów w każdym wyniku i zachował 207
chronionych plików. Ostrzeżenia CRLF→LF w trzech zmienionych dokumentach
publicznych nie są błędami diff. Wszystkie decyzje człowieka nadal pending.
