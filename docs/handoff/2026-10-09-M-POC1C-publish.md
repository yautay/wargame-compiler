# M-POC1C — checkpoint publikacyjny

- **Milestone:** M-POC1
- **Karta:** M-POC1C
- **Wynik:** done
- **Następny milestone:** M-POC2
- **Następna karta:** M-POC2A

Data: 2026-10-09, Europe/Warsaw. Właściciel jawnie polecił „commit + push”.
Zgoda obejmuje zapis ukończonego M-POC1C na origin/feature/tests i potrzebnych
prywatnych artefaktów; nie zmienia zakresu oceny, limitów ani zamrożonych bajtów.

## Stan i konkretne artefakty

eval-v1 jest zamrożone po decyzjach 06 o zakresie i 07 o freeze.
Manifest SHA-256:
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.
Zakres: 66 grup lokalnej treści, 8 wymagań kontekstu, 20 sytuacji (17/3),
5 jawnych i 3 niejawne relacje. 105 niepotwierdzonych propozycji pozostaje
poza gold; 7 wzmianek i 7 kontynuacji osobno. Progi i limity niezmienione.

Pod private/poc/spqr-chapter9/ publikowany checkpoint obejmuje:
evaluation/M-POC1C-review-007/, evaluation/M-POC1C-review-008/,
evaluation/eval-v1/, evaluation/freeze-public-v1.json, oba odpowiadające
measurement/M-POC1C-review-007/ i 008/, oraz nowy
evaluation/M-POC1C-publication-20261009-01/. W nim są zgoda, zakres publikacji,
hashe, kontrole i kopie poprzednich wskaźników dokumentacji.
Publikowane logi obejmują wyłącznie wskazane pliki, nie całe basetemp.

Faktyczny zakres i hashe prowadzi publication-inventory.json. Nie zmieniono
ignorowania /private/; staging jest jawną listą plików. Atrybuty -text
zachowują surowe bajty prywatnych danych. Zamrożonych danych, oryginalnych
odpowiedzi, manifestów i wcześniejszych handoffów nie nadpisywano.
Dokładny SHA nowego commita ustala Git; nie wpisujemy go do niego samego.

## Kontrole i środowisko

Zamknięcie freeze miało 95 passed oraz poprawne hashe i git diff --check.
Checkpoint publikacji dodaje handoff; faktyczny nowy wynik scripts/check.ps1
jest w osobnym completion wraz z hashem manifestu i audytem staged blobów.
Testów i runtime legacy nie zmieniono ani nie importowano.

.venv i pobrane narzędzia są lokalne, poza publikacją. Do kontroli wskazać
istniejący Python z pytest przez -Python; TMP/TEMP lokalne i nowy basetemp.
Historyczne ścieżki, HEAD/indeksy i locator sprzed publikacji są snapshotami;
nie używać ich do przywracania Git ani uruchamiać historycznych record/close.

## Wznowienie nowej sesji

Na bieżącym laptopie odczytać private/poc/active-feature-workspace.json
głównego repo i użyć wskazanej kopii roboczej feature/tests.
W świeżym klonie użyć feature/tests bezpośrednio i sprawdzić aktualny remote.

Przeczytać CLAUDE, SESSION-PLAYBOOK, STATUS, HANDOFF i ten handoff, ROADMAP,
POC-PLAN oraz kartę M-POC2A. Zweryfikować hashe eval-v1 i freeze-public-v1
bez nadpisania. Nie powtarzać pytań o zakres/freeze — zgody już zapisane.

Wykonać wyłącznie M-POC2A: wejścia, minimalny format, prompt i transfer-list.
Stabilny PDF jest prywatnie w tym repo; oddzielić core i kontekst zgodnie
ze source-v1 i supplementem lokalizacji. Zamrożonych odpowiedzi nie włączać
do pakietu. Zakończyć kartę kontrolami i aktualizacją stanu/handoffu.

M-POC2B jest kolejną osobną czystą sesją, ręcznie otwieraną przez właściciela,
z wyłącznie odseparowanym pakietem. Nie przekazywać jej evaluation/,
odpowiedzi wzorcowych, decyzji ani prywatnych handoffów oceny.
M-POC2A/B i ekstrakcja jeszcze niewykonane; M-POC2 jedyny next.
