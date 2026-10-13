# M-POC5A.4b1 — rzeczywiste porównania relacji

Recenzent propozycji: Codex. Znaczenie akceptuje właściciel; wszystkie nowe decyzje waiting_review.

65 ID /125 wystąpień: first60, context65. Dodatkowo22 zamrożone pary osobno dla obu odpowiedzi. 60 ID/116 wystąpień ma pozytywną propozycję w dokładnym ograniczonym zakresie;5 ID/9 wystąpień wydzielono do decyzji. To nie liczby poprawnych całych rekordów/TP.

first-001: SHA-256 `3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307`, 617941 bajtów.
context-01: SHA-256 `95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b`, 712014 bajtów.

eval-v1 `7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce`; źródło PDF `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.

[Pełne porównania JSON](comparisons.json): osobne oba hashe, source/targetscope, dosłowne źródła i zapisy modelu, pointers, bajty [start,end), SHA-256 rekordów/pól, gapy, dowody i wyłączenia.

Wykonano ręczne porównanie wszystkich65przypisanychID i22zamrożonychpar w obu hashach, z dostarczonym tekstem/rendrami; skrypty wiążą ślady.

[Czytelne porównania](comparisons.md), [pakiet decyzji właściciela](owner-focus.md), [kwestie](issues.json).

Nie wykonywano .4b2/.4b3 jako partii. D961stack występuje wyłącznie jako wymagany dodatkowy frozenmention comparison; pozostały zakres .4b3 pozostaje przypisany.

##Granice wyniku

105 candidates nie staje się gold. Nowe edges osobno, bez punktów za nowość. PełneTP_gold/TP_output/FP/FN/precision/recall not_assessable. 132 wystąpienia .4b2/.4b3 czekają na osobne sesje.

Właścicielowi udostępniono pakiet125 wystąpień; faktyczny odczyt/otwarcie unknown, nowe humanreview0, pending125. Dodatkowe22pary/hash także waiting_review. Dawne63lokalne/3wymagania source na hash bez zmiany; EXP-010/017/019/040/050/052/066/074 i SEM-001–013 pozostają otwarte.

1 dodatkowa strona/1reguła/0tabel,1runda context/0korekt;0pełnych domknięć,4częściowe uzupełnienia i4nowe deklaracje. Trzeciego źródła nie pozyskano, stop rozszerzania na2. Czysty kontekst/ekspozycja unknown, listing/path discovery poza allowlistą potwierdzony, treści oceny nie zaobserwowano. Nie dowodzi skażenia ani izolacji. Aktywny czas/budżet/config/tokeny/cena unknown.

Następny krok: decyzje dla owner-focus i wcześniejszych pending; potem osobna .4b2, oszacowana przed wykonaniem; .4b3/.4c/.4d później. M-POC5A/.4/.4b partial; M-POC5 jedyny next.
