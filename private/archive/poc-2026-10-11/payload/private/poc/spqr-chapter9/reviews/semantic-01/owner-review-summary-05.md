# Decyzje właściciela 1–6 — 2026-10-11

Właściciel odpowiedział „zgodnie z rekomendacją” po sześciu konkretnych
rekomendacjach w czacie. Zapisano owner-decision-05.json, overlay-05 i stan11.

1. D9621013: poprawne odesłanie do 10.13; deklaracja blokady na relacji
   niewystarczająca. Brak 6.68 #6 nadal blokuje podział wewnątrz stosu.
   Nie stwierdzono konkretnego błędnego rozdziału strat.
2. DCTX923-S4: przyjęto niejawne powiązanie potwierdzające pół/floor/cap1
   dla Hits atakującego, gdy wybranym obrońcą jest SK. Dodatkowy fragment
   nie jest niezbędny do lokalnej operacji już zapisanej w 9.23. Samo SK
   w mieszanej obronie nie wystarcza. Reszta SEM-004 nadal otwarta.
3. D961stack / DEP-037: odesłanie do podsumowania jest wzmianką;
   table_use jest błędnym rodzajem w tym wystąpieniu. Nie oceniono całej .4b3.
4. D9161011: właściwy cel i kierunek; rodzaj procedure_use zamiast definition.
   EXP-017 oraz lokator E916 bez rozstrzygnięcia.
5. D967966: nazwana operacja MLE jest jawnym odwołaniem mimo braku numeru;
   implicit modelu nie jest poprawną klasyfikacją tego wystąpienia.
6. D968column: zakaz MLE w Column jest warunkiem dopuszczalności;
   mention modelu jest błędnym rodzajem w tym zakresie.

SEM-014/015/016 rozstrzygnięto tylko w opisanych zakresach; SEM-004 częściowo.
SEM-001–013 i osiem wcześniejszych oczekiwań pozostają otwarte w pozostałych
zakresach. Pozostałe wyłączone pola, w tym ogólne false na innych relacjach,
nie otrzymują akceptacji. Pełne wyniki i TP/FP/FN/precision/recall nieocenialne.

116 wcześniejszych pozytywnych zakresów bez zmiany. Nowa decyzja dotyczy
9 przypisanych wystąpień (4 first / 5 context) z ocenami mieszanymi oraz
2 dodatkowych wystąpień zamrożonej wzmianki. Łącznie 125 przypisanych
wystąpień .4b1 ma decyzje o dokładnych zakresach, a nie 125 poprawnych całych
relacji. Nowe decyzje odnotowują 8 wystąpień z błędem klasyfikacji lub
niewystarczającą deklaracją blokady w .4b1 oraz 2 z różnicą rodzaju wzmianki.
Nie są to automatyczne FP ani nowe punkty gold.

Następna osobna .4b2: 30 ID / 60 wystąpień po oszacowaniu. Pozostałe .4b2/3:
132 wystąpienia do pełnego scoped review, mimo wąskiej dodatkowej decyzji
o D961stack. M-POC5A/.4/.4b partial, M-POC5 jedyny next.
Oryginały, źródła, stare decyzje i pakiet porównań zachowano; bez nowych
źródeł, ekstrakcji, korekt, czatów, commit/push lub wykonania kolejnej partii.
