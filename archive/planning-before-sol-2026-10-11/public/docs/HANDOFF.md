# Przekazanie projektu IG

- **Data:** 2026-10-11.
- **Wynik:** recenzja i plan ukończone; IG-0 done jako projektowanie.
- **Następny etap:** IG-1.
- **Następna karta:** [IG-1](work/tasks/IG-1.md), bez rozpoczętej implementacji.

Właściciel wyraźnie zlecił w tej sesji wyłącznie plan. Nie rozpoczynać
implementacji w ramach kończenia dokumentów. Chce pełnego IG, bez kolejnego
POC. Docelowy IG ma umożliwiać deterministyczne i szybkie obliczanie legalnych
akcji, aby przeciwnik AI przeznaczał tokeny i kontekst na decyzje strategiczne.

Czytaj [STATUS](STATUS.md), [plan](IG-PLAN.md),
[architekturę importu](IG-WGU-ARCHITECTURE.md),
[legalne akcje](IG-LEGAL-ACTIONS.md), [model](IG-DATA-MODEL.md),
[mechaniki](IG-MECHANICS-PROFILES.md) i
[ADR-0040](adr/ADR-0040-ig-i-archiwum-poc.md).

Plan: pełny import KB → niezależny spis całego PDF → uzgodnienie źródeł
→ formalizacja stanu, akcji, wyborów, reakcji i skutków → review → kompilacja
→ deterministyczny mechanizm i kompaktowy interfejs dla AI. Wyszukiwanie
jest funkcją pomocniczą. Tekst opaque wpływający na legalność blokuje gotowość
wykonawczą; nie planujemy używania LLM do rozstrzygania go w każdej turze.

Przy realizacji dopiąć profil scenariusza/opcji, komplet potrzebnych źródeł,
organizację review i warunki pomiaru szybkości. Pełna instrukcja SPQR 5E
jest zakresem od początku. Rozdziały służą organizacji pracy, nie są pilotami.
Schemat danych pozostaje draftem; done IG-0 nie akceptuje semantyki gry.

Podstawa: private/ig/planning/wgu-spqr-2026-10-11/ zawiera inwentarz,
skrypt i przykłady mapowania. KB jest w C:/repo/wargame-projects/games/spqr/kb,
kod WGU w C:/repo/wargame-utils. Sąsiednich repo nie zmieniano. Wszystkie 36
źródeł wskazanych w konfiguracji jest nieobecnych pod tymi ścieżkami.
Archiwalny PDF 5E jest dostępny, ale identyczność z dawnym wejściem WGU
pozostaje nieznana. Brak pełnego review KB i odczytu całej instrukcji.

[Recenzja](reviews/IG-0-critical-review.md), private/ig/reviews/IG-0/ i badania
pozostają dowodami ze wskazanymi ograniczeniami. 36 przypadków nadal
niewykonane. Dokładna konfiguracja modelu/reasoning recenzji jest unknown;
zalecenie Astra/high nie potwierdza konfiguracji.

POC jest nieukończonym archiwum: archive/poc-2026-10-11/project/ oraz
private/archive/poc-2026-10-11/payload/. Manifest mapuje dawne ścieżki
na 3117 plików. Nie wznawiać M-POC, nie zmieniać gold ani oryginalnych
odpowiedzi. Nie tworzyć nowych czatów/agentów. Bez commit/push.

Kontrole: scripts/check.ps1 i git diff --check; logi private/ig/_checks/.
Kontrole dokumentacji nie są dowodem działania legalnych akcji.

Wynik końcowy planowania: 23 passed; integralność 3117 plików archiwum
zachowana; git diff --check — 0. Logi:
private/ig/_checks/active-0b47385fe50b4759abe3a28e3bcf88ae/.
