# M-POC1C — zamrożenie eval-v1

- **Milestone:** M-POC1
- **Karta:** M-POC1C
- **Wynik:** done
- **Następny milestone:** M-POC2
- **Następna karta:** M-POC2A

Data: 2026-10-09, Europe/Warsaw. Właściciel odpowiedział „zatwierdzam”
na osobne pytanie freeze. Decyzja 07 jest zapisana; wcześniejsza decyzja 06
zatwierdziła zakres/rubryki/wyłączenia/progi/limity. Nie pytać ponownie.

## Wynik

Pod private/poc/spqr-chapter9/: evaluation/eval-v1/ zawiera cztery pliki danych,
measurement-policy.json, review.md, change-map.json i manifest.json.
evaluation/freeze-public-v1.json zawiera tylko ID/hash/data/potwierdzenie freeze,
bez treści oczekiwań. Manifest eval-v1 SHA-256:
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.

Zamrożenie: 2026-10-09T12:29:20.118357+00:00, przed pierwszą ekstrakcją.
Zakres: 66 lokalnych grup treści, 8 wymagań kontekstu, 20 sytuacji (17/3),
5 relacji jawnych i 3 niejawne. 105 niepotwierdzonych propozycji poza gold;
7 wzmianek i 7 kontynuacji osobno. Globalnego certyfikatu grafu/pól nie nadano.
Progi i limity niezmienione; nieznany aktywny czas nie potwierdza budżetu.

## Kontrole i zachowanie danych

Kontrole przed freeze: scripts/check.ps1 — 94 passed i git diff --check poprawny.
Końcowe kontrole, hashe, błędy środowiska i audyt zachowania poprzedników są
w evaluation/M-POC1C-review-008/ i measurement/M-POC1C-review-008/completion.json.
Źródłowy PDF i kandydaci zachowują bajty; zmieniono wyłącznie top-level metadane
cyklu życia w nowych kopiach, bez zmiany zagnieżdżonych rekordów.
M-POC1C done; M-POC2A/B i ekstrakcja niewykonane.

Właściciel zezwolił na lokalne .venv. Python i pytest są w głównym repo;
lokalne TMP/TEMP i nowy basetemp prowadzi scripts/check.ps1 uruchamiany z
-Python C:/dev/wargame-compiler/.venv/Scripts/python.exe.
Pierwsza próba na Pythonie 3.13 napotkała błąd dostępu do prywatnego basetemp;
zgodne lokalne środowisko 3.11.9 przechodzi niezmienione testy.
Poprzednie błędy/logi zachowano; nie dopisywano i nie osłabiano testów.

Kopia robocza jest od ae8f6f0 na feature/tests, jej ścieżka w
private/poc/active-feature-workspace.json głównego repo. Główny .git jest
chroniony; jego HEAD i indeks pozostają zachowane. Kopia wymaga obiektów
Git głównego repo. Nie ma commita/pusha tej sesji ani instalacji globalnej.

## Dokładne wznowienie

Odczytać bootstrap, bieżący STATUS/HANDOFF i kartę M-POC2A.
Sprawdzić hashe eval-v1 i freeze-public-v1; żadnego nadpisania.
Przygotować powtarzalny pakiet źródłowy, format, prompt i transfer-list.
Stabilny PDF jest już prywatnie w tym repo; historyczne ścieżki innego laptopa
nie są poleceniem modyfikowania drugiego repozytorium.
Czystą sesję M-POC2B otwiera ręcznie właściciel; nie przekazywać jej evaluation/,
oczekiwań, decyzji ani prywatnych handoffów oceny. Ta sesja zna klucz oceny.
