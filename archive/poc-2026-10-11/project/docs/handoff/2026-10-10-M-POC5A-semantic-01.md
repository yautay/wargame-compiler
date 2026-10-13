# M-POC5A — część .1, rejestr i pierwsze porównania

- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Data: 2026-10-10, Europe/Warsaw. Codex, C:/repo/wargame-compiler,
feature/tests. Bieżąca część M-POC5A.1, waiting_review. Przed oceną znaczenia
podzielono pełny zakres na cztery części do 90 minut; opis i karty podrzędne
w [M-POC5A](../work/tasks/M-POC5A.md). Nie wykonano części .2–.4.

## Wejścia i integralność

first-001: 617941 bajtów, SHA-256
3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
context-01: 712014 bajtów, SHA-256
95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
eval-v1: SHA-256
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.

Zweryfikowano kopię PDF, manifesty obu wejść, freeze, zamknięte raporty
i 35 095 zakresów provenance (16 768/18 327). Szczegóły, wejścia i hashe
w nowym measurement/M-POC5A-semantic-01/input-audit.json pod prywatnym
korzeniem private/poc/spqr-chapter9/. Zachowanie chronionych plików i logi
kontroli prowadzi nowy completion.json, bez zmian historycznych raportów.

## Faktyczny zakres

reviews/semantic-01/checklist.json, review.md, issues.json, focus-01.md
prowadzą dwa osobne zestawy pending na tym samym eval-v1. Przygotowano
porównania dla wszystkich 74 oczekiwań, 207 pozycji, 277 diagnostycznych
par rubryka/oczekiwanie oraz 126/131 proponowanych krawędzi. Każdy zakres
ma źródło, mapowanie i ślad do surowych bajtów; mapowanie nie daje akceptacji.
277 par nie jest nowym mianownikiem reguł. 66/8 oraz rubryki zachowane.

Pokazano właścicielowi trzy dokładne lokalne porównania z propozycjami
oceniającego; decyzje pozostają pending, dopóki nie wpłynie rzeczywista
odpowiedź. Nie zapisano akceptacji znaczenia, ocen poprawnych grup, TP/FP/FN
ani certyfikatu pełnego grafu. Pozostałe zakresy jawnie pending w częściach
.2–.4; nie pominięto ich i nie uznano przygotowania za wykonany przegląd.

## Ograniczenia i przegląd człowieka

Oryginały, źródła, wejścia, manifesty, freeze, eval-v1 i zamknięte raporty
zachowano. Krytyczny brak źródła blokuje zależny pełny wynik; lokalne
syntetyczne fakty nie wymagają automatycznie całego rzeczywistego setupu.
Nie pozyskano nowych źródeł ani trzeciego kroku; stop na granicy 2 zachowany.
1 dodatkowa strona/1 reguła/0 tabel, 1 runda kontekstu, 0 korekt; w tej
części 0 ekstrakcji, 0 kontekstu i 0 korekt. 20 sytuacji pozostaje w M-POC5B.

Naruszenie listing/path discovery w sesji kontekstu nadal potwierdzone;
ekspozycja na treść oceny i czysty kontekst unknown, bez dowodu skażenia
lub pełnej izolacji. Historyczne first-001, selektory, tokeny/cena, aktywny
czas i budżet unknown. Pierwszy zarejestrowany zegar tej sesji był po
bootstrapie; kalendarzowe metadane nie są aktywnym pomiarem czasu.

## Dokładne wznowienie

Od SEM-001/002/003 w focus-01.md: odnotować rzeczywiste decyzje właściciela
z dokładnym zakresem i hashami, w nowych plikach decyzji, bez poprawiania
odpowiedzi. Akceptacja części nie akceptuje całych EXP-ID lub pozostałych pól.
Potem pełny przegląd części .2–.4 od pierwszego pending; kolejny podział
przed wykonaniem, jeśli część nie mieści się w 90 minutach.
STATUS nadal M-POC5/M-POC5A; M-POC5B, M-POC6/7 i architektura niewykonane.

Kontrole: scripts/check.ps1 oraz git diff --check; rzeczywisty wynik,
logi i końcowe hashe w completion.json i append-only sessions.jsonl.
scripts/check.ps1: **120 passed**; git diff --check bez błędów.
Audyt dowodów zachował 189 chronionych plików i pierwotny prefiks pomiarów.
Historyczne CRLF w trzech edytowanych dokumentach wywołało ostrzeżenia Git
o przyszłej normalizacji do LF; nie były błędami kontroli.
Publikacja Git nie była polecona w tej sesji; zapis lokalny do przeglądu.
