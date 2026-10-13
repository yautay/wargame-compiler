# M-POC5A.1: Integralność, pełny rejestr i pierwsze rozbieżności

- **ID:** M-POC5A.1
- **Milestone:** M-POC5
- **Rola:** Przegląd wspólny; akceptuje właściciel
- **Zależności:** M-POC4 done w ograniczonym zakresie; wcześniejsze części M-POC5A dla późniejszych części.

## Cel i pytanie eksperymentalne

Weryfikacja wszystkich wejść, obu odpowiedzi i provenance; kompletne 74 oczekiwania, 207 pozycji, rubryki i relacje w rejestrze. Pierwszy konkretny przegląd rozbieżności wskazanych w promptcie. Pozostałe oceny pending.

## Dokładne pliki do przeczytania

Wszystkie wejścia i zasady [karty nadrzędnej](../M-POC5A.md), prompt semantic-review-start-v1.txt oraz pełny prywatny rejestr reviews/semantic-01/ pod private/poc/spqr-chapter9/.

## Wejścia i wersja oceny

Niezmienione eval-v1 i obie oryginalne odpowiedzi first-001/context-01, z osobnymi hashami i dokładnymi zakresami źródeł oraz surowych bajtów.

## Wymagane działania

Weryfikacja wszystkich wejść, obu odpowiedzi i provenance; kompletne 74 oczekiwania, 207 pozycji, rubryki i relacje w rejestrze. Pierwszy konkretny przegląd rozbieżności wskazanych w promptcie. Pozostałe oceny pending. Oddzielić transkrypcję od interpretacji, lokalny wynik od realnego setupu, brak kontekstu od niejednoznaczności. Nie zmieniać ekstrakcji ani historycznych raportów. Jedna część do 90 minut; podział dalszy przed wykonaniem.

## Artefakty wyjściowe i lokalizacje

Prywatne reviews/semantic-01/checklist.json, review.md, issues.json oraz osobne zapisy decyzji człowieka z hashami; append-only measurement/sessions.jsonl i nowy katalog pomiaru części.

## Kryteria zakończenia i kontrole

Jawny spis zakresów pokazanych, ocenionych i pending, recenzent, dowód i niepewność. scripts/check.ps1, git diff --check, rzeczywiste logi i kontrola niezmienności.

## Zakres wyłączony

M-POC5B i 20 sytuacji, nowe źródła/pass-02, ekstrakcje i korekty, M-POC6/7 oraz architektura.

## Przegląd człowieka

Model przygotowuje propozycje i porównania. Tylko faktyczna decyzja właściciela akceptuje pokazany dokładny zakres; brak decyzji pozostaje waiting_review.

## Wznowienie

Od pierwszego pending w zakresie tej części; nie nadawać akceptacji przez przeniesienie statusów z innych zakresów lub wcześniejszego przeglądu źródła.

## Przekazanie

Następna część otrzymuje wszystkie pozostałe pending. Karta M-POC5A pozostaje partial do rozliczenia całego zakresu; dopiero później osobna M-POC5B.
