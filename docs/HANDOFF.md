# HANDOFF

- **Ostatnia sesja:** [2026-10-09-M-POC1C-publish](handoff/2026-10-09-M-POC1C-publish.md)
- **Wynik:** done
- **Następny milestone:** M-POC2
- **Następna karta:** M-POC2A

M-POC1C zakończono po rzeczywistych decyzjach 06 (zakres) i 07 (freeze).
eval-v1 jest zamrożone; freeze-public-v1 zawiera wyłącznie metadane.
Nie powtarzać pytań o akceptację tego samego pakietu.

Właściciel zlecił commit i push checkpointu na origin/feature/tests.
Zakres publikacji i zgoda są w evaluation/M-POC1C-publication-20261009-01/
pod private/poc/spqr-chapter9/. Obejmuje zamrożone dane, decyzje 06/07,
raporty, hashe i potrzebne logi; .venv, instalatory i basetemp są lokalne.
Dokładne SHA nowego commita i wynik remote są wynikiem operacji Git,
nie polem wpisywanym do tego samego commita.

Prywatne dane: evaluation/eval-v1/, evaluation/freeze-public-v1.json,
evaluation/M-POC1C-review-007/ i 008/ oraz oba rejestry measurement.
Źródła i wcześniejsze artefakty zachowano; pełne hashe prowadzą manifesty.

Następny krok to M-POC2A: pakiet wejść, format, prompt i transfer-list.
M-POC2A/B i ekstrakcja niewykonane; wyniki jakości n/a. M-POC2 jedyny next.
Ekstraktor później dostaje odseparowany pakiet bez klucza oceny.

Na tym laptopie kopię roboczą prowadzi prywatny locator głównego repo.
W nowym klonie pracować bezpośrednio na feature/tests; historyczne lokalne
ścieżki i informacje o master/shared objects są snapshotami poprzedniej maszyny.
Nie kopiować środowiska. Istniejący lokalny Python z pytest jest wystarczający.

[STATUS](STATUS.md), [ROADMAP](ROADMAP.md), [plan](POC-PLAN.md).
