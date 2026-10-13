# Stan projektu IG

- **Data aktualizacji:** 2026-10-11.
- **Aktywny kierunek:** KB WGU + pełna instrukcja → IG → deterministyczne legalne akcje dla AI.
- **Bieżący etap:** IG-1.
- **Bieżąca karta:** [IG-1](work/tasks/IG-1.md), następna praca, kod nie rozpoczęty.
- **Wynik tej sesji:** wyłącznie recenzja, architektura i plan; IG-0 done jako praca projektowa.

Właściciel wskazał pełną instrukcję oraz reużycie KB WGU, wykluczył kolejny
POC i potwierdził, że obecna sesja ma opracować plan, bez implementacji.
Celem IG jest szybkie i deterministyczne dostarczanie legalnych akcji
przeciwnikowi AI, oszczędzając tokeny i kontekst na wybór strategii.

Dokumenty: [architektura importu](IG-WGU-ARCHITECTURE.md),
[legalne akcje](IG-LEGAL-ACTIONS.md), [plan](IG-PLAN.md),
[roadmapa](ROADMAP.md). Plan obejmuje źródłowy IG, warstwę semantyczną,
kompilowany pakiet i deterministyczny mechanizm reguł. Nie powstał importer,
pełny IG, runtime ani przeciwnik AI. Schemat nadal jest draftem.

Plan oparto na schemacie i kodzie WGU oraz inspekcji KB SPQR. Inwentarz
tekstowy wykazał 523 reguły, 233 relacje, 48 tabel i 11 głównych procedur.
36 skonfigurowanych źródeł nie jest dostępnych pod podanymi ścieżkami.
W archiwum WGC jest 44-stronicowy PDF 5E z potwierdzonym hashem; identyczność
z dawnym wejściem WGU jest nieznana. Rekomendacja: przypiąć go jako źródło
nowego IG i uzgodnić z nim opracowanie. Do gotowości legalnych akcji potrzebne
są także wszystkie materiały i dane wymagane przez wybrany profil.

Hashe, przykłady mapowania i ograniczenia inspekcji:
private/ig/planning/wgu-spqr-2026-10-11/. Nie wykonano pełnej walidacji YAML
WGU ani pełnego odczytu semantycznego KB i instrukcji. Ponowna kontrola
27 zinwentaryzowanych plików KB/konfiguracji/kodu WGU nie wykazała zmian.

Do dopięcia przy realizacji: źródła, scenariusz/opcje pierwszego profilu,
osoba i czas review oraz sprzęt i progi wydajności. To nie ponowna decyzja,
czy budować pełne IG. Opaque jest dopuszczalne przejściowo; jeśli wpływa
na legalność lub skutki, blokuje gotowość tego zakresu dla AI.

[Recenzja IG-0](reviews/IG-0-critical-review.md) zachowuje ustalenia i ich
ograniczenia. 36 przypadków badawczych nadal proposed_not_run; brak pomiaru
kosztu implementacji i czasu operatora. Mały pilot z D3 jest zastąpiony.

POC zachowano jako nieukończony. [Archiwum](../archive/poc-2026-10-11/README.md)
obejmuje 3117 plików; oryginalne wyniki i gold są niezmienne. Poprzednia
kontrola wersji planu: 22 passed, git diff --check — 0, logi
private/ig/_checks/active-6788619f8b8240268bd83ec0c8a041e0/.
Po doprecyzowaniu celu legalnych akcji: scripts/check.ps1 — 23 passed,
w tym niezmienność archiwum; git diff --check — 0. Końcowe odnośniki,
kolejkę, przykłady JSON i białe znaki sprawdzono dodatkowo po ostatnich korektach.
Logi: private/ig/_checks/active-0b47385fe50b4759abe3a28e3bcf88ae/.
Bez commit/push; zastane zmiany po migracji zachowane.
