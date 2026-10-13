# Prompt krytycznej recenzji projektu IG

Zalecana konfiguracja nowej lokalnej sesji: **GPT-6 Astra, rozumowanie high**.
To dobór do trudnej recenzji, nie pomiar przewagi modelu. Oficjalna
[dokumentacja wyboru modelu](https://developers.openai.com/api/docs/guides/model-selection)
opisuje Astra jako najmocniejszy model, a
[dokumentacja reasoning](https://developers.openai.com/api/docs/guides/reasoning)
wskazuje high do złożonego rozumowania i planowania.
Faktycznie wybraną konfigurację zapisz w recenzji.

```text
Pracuj lokalnie w C:\repo\wargame-compiler po polsku.
Wykonaj IG-0: krytyczną recenzję Instruction Graph jako podstawy
narzędzia do digitalizacji instrukcji SPQR, OSG i GCACW z MMP.

Czytaj README.md, CLAUDE.md, docs/STATUS.md, docs/HANDOFF.md,
docs/IG-PLAN.md, docs/ROADMAP.md, docs/work/tasks/IG-0.md,
docs/IG-DATA-MODEL.md, docs/IG-MECHANICS-PROFILES.md i ADR-0040.
Czytaj private/ig/research/2026-10-11/mechanics-evidence.md
i acceptance-cases.md. Historyczne źródła odszukuj przez manifest
private/archive/poc-2026-10-11/manifest.json.

Nie traktuj draftu jako przyjętego kontraktu. Szukaj kontrprzykładów
i porównaj alternatywy, także prostszy model. Sprawdź oficjalne materiały
GMT, OSG i MMP, w tym SPQR5, TLNB7.38, CNS/NAB, OSG Days i GCACW.
Rozdziel pełny odczyt, odczyt fragmentów i nieweryfikowane założenia.

Oceń jednostkę reguły i review, wersje i zakresy źródeł, procedury,
reakcje i powroty, stany, przyczyny zdarzeń, historię, wybory uczestników
utrzymywane między krokami, geometrię wieloheksową, ZOC/LOS/ścieżki,
losowania z puli, wynik naturalny/zmodyfikowany, zaokrąglenia,
modyfikatory, tabele/legendy, informację ukrytą, scenariusze,
dowodzenie, zwycięstwo i regresje.

Pokaż przykład reprezentacji z każdej rodziny i kontrprzykład draftu
albo uzasadnij brak kontrprzykładu w dokładnie wskazanym zakresie odczytu.
Sprawdź koszt liczby rekordów i review. Oddziel minimum digitalizacji
i wyszukiwania od późniejszego wykonawcy reguł.

Zapisz docs/reviews/IG-0-critical-review.md. Konkretne reguły, cytaty,
grafiki i sytuacje wyłącznie w private/ig/. Zaktualizuj aktywne drafty,
jeśli zastrzeżenia uzasadniają zmiany. Podaj minimum IG-1, późniejsze
rozszerzenia i decyzje wymagające właściciela.

POC jest zarchiwizowany i nieukończony. Nie wznawiaj M-POC ani
nie zmieniaj archiwów, gold lub oryginalnych odpowiedzi. Nie buduj
silnika, UI, API inferencji ani nowych czatów lub agentów.
To recenzja projektu, nie ślepa ekstrakcja. Uruchom scripts/check.ps1
i git diff --check. Nie commituj ani nie pushuj. Zakończ jasnym raportem
ustaleń i konkretnym zakresem do decyzji właściciela.
```
