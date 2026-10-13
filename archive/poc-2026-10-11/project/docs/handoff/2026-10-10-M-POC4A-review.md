# M-POC4A - decyzja właściciela i zamrożenie ograniczonego kontekstu

- **Milestone:** M-POC4
- **Karta:** M-POC4A
- **Wynik:** done
- **Następny milestone:** M-POC4
- **Następna karta:** M-POC4B

Data: 2026-10-10, Europe/Warsaw. Wykonawca: Codex, C:/repo/wargame-compiler,
feature/tests. Done oznacza wybór źródła, decyzję człowieka i przygotowanie
zamrożonego przekazania. Znaczenie i wyniki nie otrzymały nowej akceptacji.

## Przegląd i zakres decyzji

Właściciel zgłosił brak wyświetlania obrazu. Przygotowano osobny podgląd
z niezmienionym obrazem i pomocniczym tekstem; dokładny tekst pokazano w czacie.
Następnie otrzymano „Zatwierdzam” i zapisano decyzję wyboru źródła oraz zakresu.
Nie zadeklarowano, że właściciel rzeczywiście otworzył określony viewer albo
osobiście sprawdził glify. Decyzja nie rozstrzyga znaczenia, kolejności obliczeń,
wyników sytuacji, krytyczności niepotwierdzonych kandydatur ani budżetu czasu.

Prywatne ścieżki liczone od private/poc/spqr-chapter9/:
evaluation/M-POC4A-review-001/request.json, source-preview.html,
source-preview-manifest.json, decision-01.json i review-closure-01.json.
Decyzja SHA-256: c0439827e267cb15148fa4f24f0c0543ad839428fa65de4461a137106cb2583f.

## Zamrożenie i przygotowane przekazanie

context/pass-01/freeze-v1.json wiąże niezmieniony wcześniejszy manifest,
pliki, decyzję, źródła i nowy manifest przekazania. Draftów i wcześniejszych
requestów/manifestów nie nadpisano; historyczne waiting_review pozostaje
w pierwotnych bajtach, aktualny ograniczony stan prowadzi osobny freeze.
Freeze SHA-256: 7609c1c41455094e2fc59af11400c551bf32f4c8ccca3a707c9418f6dba25fad.

transfer/context-v1/ ma 42 pliki allowlisty, bez klucza oceny, raportów,
oceniających handoffów, całego PDF i rejestrów błędów. Włączono niezmienione
wejścia pierwszej próby oraz jej surową odpowiedź jako rodzica, ograniczony
zatwierdzony fragment, metadane freeze i nowy prompt. Wąski dodatek techniczny
formatu ustala ID/hash przebiegu i jawne współrzędne wycinka; nie naprawia
first-001 ani nie zmienia kryteriów eval-v1.
Manifest przekazania SHA-256:
1140a43519ae60646ea783bb24ec4dacc2f608e88d80efd83a206427aa45eff4.

Baseline first-001, oryginalne wejścia, zamrożony eval-v1 i raporty M-POC3
zachowane. Przyrost nadal 1 strona, 1 reguła, 0 tabel; ścieżka dostarczona
1 krok, rozważana 2. Zatrzymanie dalszego rozszerzania i limity 8/20/4/2/2
bez zmian. 0 rund odpowiedzi, 0 nowych inferencji, 0 korekt.
Pakiet prepared_not_sent; faktyczne przekazanie/czas nowej sesji niepoświadczone.
Aktualny budżet czasu unknown; zgodność czasu unknown.

Pozostałe brakujące tabele oraz rzeczywiste źródła mapy/scenariusza/żetonu
pozostają blocked_source. 79 deklaracji i 105 kandydatur zachowują rozróżnienia;
akceptacja jednego źródła nie nadaje im akceptacji znaczenia, konieczności lub gold.

## Kontrole i dokładny następny krok

Kontrole i logi scripts/check.ps1 oraz git diff --check, niezmienność źródeł,
prefiks sessions.jsonl i pełna allowlista: measurement/M-POC4A-review-001/completion.json.
scripts/check.ps1: **113 passed**, git diff --check bez błędów; lokalne TMP/TEMP
i wcześniej nieistniejący GUID basetemp. Dodatkowy pakiet/metryki nie wykonują inferencji.
Aktywny test ciągłości obejmuje teraz poprawne przejście M-POC4A -> M-POC4B
oraz odrzuca przejście przed zakończeniem A, powtórzenie, pominięcie i złą kartę.
Testów legacy i progów jakości nie zmieniono.

Właściciel ręcznie otwiera osobną izolowaną sesję w:
C:/repo/wargame-compiler/private/poc/spqr-chapter9/transfer/context-v1.
Start: transfer-list.txt, context/pass-01/manifest.json, prompts/context-v1.txt.
Ekstraktor otrzymuje wyłącznie allowlistę i zapisuje jedną context-01.json;
nie otwiera nadrzędnego repo ani tego handoffu. Nową sesję otwiera właściciel,
nie model ani automatyzacja. Nie wykonywać ekstrakcji w czacie oceniającym.

Po odbiorze M-POC4B zapisuje osobne bajty i run/proposal/report/metrics,
porównuje wynik z baseline na niezmienionym eval-v1 i zachowuje nieznane
metadane jako unknown. Brak odpowiedzi pozostaje waiting_response;
nie ponawiać automatycznie. Nie wykonano M-POC4B ani dalszych kart.
