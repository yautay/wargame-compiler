# Archeologia i analiza luk (Session 0, fazy A–B)

Stan na 2026-10-05. Źródła: repo `C:/dev/wargame_utils` (commit `86c4d81`) i repozytoria gier w `C:/dev`. Ten
dokument zapisuje fakty i wnioski. Nie jest instrukcją. Po ADR-0001 nowe narzędzie nie jest zobowiązane do
kompatybilności, ale nie powinno powtarzać błędów.

## 1. Co istnieje (faza A)

### 1.1 `wargame_utils` (`wgu`)
| Obszar | Stan | Gdzie |
|---|---|---|
| Plugin Claude Code | 9 skilli (`/wgu:atomizacja`, `tlumaczenie`, `digitalizacja`, `errata`, `czytelnosc`, `pomoce`, `projekt-pomocy`, `nowy-projekt`, `regula`). Skille to cienkie orkiestratory, procedury agentów w `procedura.md`. | `skills/`, `agents/` |
| Agenci | analityk zasad (Opus max), weryfikator zasad (Fable), tłumacz, redaktor językowy, projektant pomocy, grafik (Sonnet), architekt digitalizacji | `agents/*.md` |
| CLI Python (~3 tys. linii) | `pdf analyze/extract/images/render/layout/compare`, `kb import-legacy/lint/render/show/stats/export`, `terms lint/show/check/impact/for-chunk/glossary-tex`, `text mark`, `check fidelity`, `aids validate/build`, `tex build/style`, `init --setup` | `wgu/` |
| Kontrakt KB | `wgu/kb@1`: reguły z polami Markdown (`when`, `effect`, `exceptions`, `notes`), terminy, tabele, procedury, relacje (`overrides`, `exception-to`…, `status: imported/verified/inferred`), niejasności (`strength`), zmiany, „scenariusze” (pytania kontrolne). Pole `digital` reguły z enumem `kind`. | `wgu/schemas/kb.schema.json` |
| Glosariusz pojęciowy | `wgu/terms@1`: pojęcie (nie słowo) w warstwach common → era → series → game, statusy `proposal/approved/disputed/deprecated`, dowody z polem `supports`, formy odmiany, historia zmian | `terminology/`, `skills/tlumaczenie/references/polityka-terminologiczna.md` |
| Weryfikacja przekładu | trzy przebiegi u różnych wykonawców: terminologia (skrypt), znaczenie (Fable), redakcja (Opus); heurystyka `check fidelity` (liczby, odsyłacze, sygnały modalności i zakresu) | `wgu/check/fidelity.py`, `references/weryfikacja.md` |
| Oprawa | pomiar PDF → `layout.yaml` → generowany `.sty` na wspólnym API makr `wgu-base.sty`; porównanie stron | `wgu/pdf/layout.py`, `wgu/latex/style.py`, `templates/latex/` |
| Pomoce do gry | grafy decyzyjne YAML (węzły, krawędzie, ID reguł), walidator grafu, TikZ | `skills/projekt-pomocy`, `wgu/aids/validate.py` |
| Digitalizacja | procedura agenta + eksport `wgu/kb-bundle@1` (JSON) | `skills/digitalizacja/procedura.md`, `wgu/kb/export.py` |
| Testy | 5 plików pytest (core, layout, setup, terms, roundtrip) | `tests/` |
| Decyzje | rejestr decyzji właściciela D-01…D-10 (terminologia, styl) | `docs/decyzje.md` |
| Benchmark | procedura opisana, **tabela wyników pusta** | `docs/MODELE.md` |
| Próby | SPQR, 8 segmentów: heurystyka 5/6 błędów (przeoczony ≥ → >), weryfikator premium 6/6, pierwsza wersja heurystyk 8/8 fałszywych alarmów | `docs/proby/2026-10-04-spqr-tlumaczenie.md` |
| Cache, przyrostowość | brak cache wyjść modeli. Jest tylko `translation/source.json` (SHA-256 PDF) i ręczny tryb „aktualizacja przyrostowa” | — |
| Pamięć sesji | `translation/context.md` w repo gry („czytaj przy wznowieniu”); brak STATUS/HANDOFF/ADR narzędzia | — |

`C:/dev/wgu-1_5` to nietknięta kopia `wargame_utils` na tym samym commicie (`diff -rq` bez różnic).

### 1.2 Repozytoria gier
| Repo | Co to jest | Skala | Uwagi |
|---|---|---|---|
| `wg-spqr` | KB `wgu` + tłumaczenie w toku (SPQR 5 ed.) | 523 reguły, 233 relacje, 45 niejasności, 59 pytań, 48 tabel | KB po polsku; schemat łatany przez `extra.scope`; ręczna tabela niejasności nieaktualna wobec KB; karty tabel doszły po zbudowaniu KB (przepisanie T-20…T-29) |
| `virgin-queen` | KB `wgu` | 259 reguł | brak tabeli wpływów (bloker), tabele z obrazów wydania 2011, 112 kart poza KB, moduł Vassal nieużyty; brak commitów |
| `Ukraine43` | KB `wgu` | 266 reguł | przekreślenie widoczne tylko w renderze, pomieszane kolumny tabeli pogody, brak CRT/TEC w instrukcji (bloker), nowe pliki Vassal nieużyte; mieszane ID (`R-3.B5.1`, `R-S1`, `R-CLAR-*`, `R-ERR-*`); brak commitów |
| `GCACW-PL` | gotowe tłumaczenie (przed `wgu`), KB w Markdown | 238 reguł | kolejność „tłumaczenie → indeks”; równoległe agenty tworzyły różne odpowiedniki terminów; zepsute odsyłacze „patrz…” |
| `spqr` | silnik TypeScript (pnpm), własna KB po angielsku | 211 sekcji, 422 adnotacje `@rule`, ~1078 testów, 74 karty zadań | czysty stan, `step()`, DecisionRequest, ramki procedur, Computation + Modifier, trace z RuleRef, RNG w silniku, zapis `{seed, inputs, snapshot, hash}`, generowana TRACEABILITY z `--check`; ADR-0004: brak DSL reguł; **brak powiązania z `wg-spqr/kb`** |
| `gcacw` | pusty (PDF + settings) | — | — |

**Etap digitalizacji `wgu` nie został uruchomiony na żadnej grze.** Nie istnieje żaden plik `kb/digital/*`.

## 2. Wnioski (lekcje)
1. **Jeden model logiki na grę.** SPQR był analizowany dwa razy (`spqr/docs/rules`, `wg-spqr/kb`), z niezgodnymi
   ID i rejestrami. → ADR-0003, `docs/PIPELINE.md`.
2. **Logika nie może zależeć od języka docelowego.** KB `wgu` jest po polsku. → ADR-0003.
3. **Wolny tekst nie jest kontraktem.** `when/effect/exceptions` w Markdown nie dają się walidować ani przekładać na
   predykaty. → Rule IR (`docs/LOGIC-MODEL.md`).
4. **Wnioski muszą być odróżnialne od źródła.** `[wniosek]` w notatce to za mało. → provenance (ADR-0014).
5. **Ryzyko trzeba mierzyć deterministycznie.** Heurystyka przeoczyła ≥ → >, a samoocena modelu nie jest sygnałem
   wystarczającym. → `docs/LOGIC-MODEL.md#model-ryzyka`, ADR-0010.
6. **Heurystyki trzeba testować mutacjami** (para: poprawny tekst / tekst z wstrzykniętymi błędami). Inaczej toną
   w fałszywych alarmach. → `docs/QUALITY.md`.
7. **Inwentarz źródeł przed analizą.** Brakujące arkusze tabel blokowały każde repo, a źródła spóźnione (Vassal,
   karty) nie były włączane. → Stage 0, `source_document.present/complete`.
8. **Rozjazd wydań jest normą** (tabele ze starszych edycji). → `edition_skew`, `precedence`, ambiguity `scope: edition_skew`.
9. **Ekstrakcja PDF jest zawodna.** Trzeba renderu stron i flag wizualnych (przekreślenie, kolor zmian, kolumny). → `segment.visual_flags`, `verified_by_render`.
10. **Jedna gramatyka ID.** Repo wymyślały `R-SC0`, `R-SCEN-n`, `R-S1`, `R-CLAR-*`… → `docs/DATA-CONTRACTS.md#identyfikatory`.
11. **Nazwy muszą znaczyć to, co mówią.** `scenarios.yaml` zawierał pytania kontrolne, nie scenariusze gry. → rekord `case` (`CASE-`) ≠ scenariusz (`CON-scn.*`).
12. **Statusy i widoki generować, nie pisać.** Ręczne tabele i karty się dezaktualizowały. → ADR-0011.
13. **Implementacja znajduje błędy KB** (spqr: korekta SPQR-3.0/6.82). Potrzebny jest kanał zwrotny bez prawa
    zapisu w górę. → `review_request` (`RR-`).
14. **Decyzje człowieka jako typowany rejestr** z budżetem pytań na przebieg (spqr: 3 nowe INT/OQ na run). → `HD-`, `build.policy.max_human_questions`.
15. **Przykłady i pytania kontrolne to złote testy** (spqr `EX-*` → golden tests). → `case` → `test` (Stage 1.5).
16. **Równoległe tłumaczenie wymaga zamrożonej terminologii** i wspólnej mapy tytułów i odsyłaczy. → gate Stage 3.
17. **Tekst źródła poza repo, deterministycznie odtwarzalny.** → ADR-0012.
18. **Dyscyplina kontekstu.** Karty z listą `context:`, świeży subagent na jednostkę pracy, wznowienie z plików,
    nie z pamięci. → `docs/SESSION-PLAYBOOK.md`, pakiety review (`docs/GLU.md`).
19. **Wyjątki zapisane w dwóch miejscach się rozjeżdżają.** → ADR-0005.
20. **Brak zmierzonego baseline kosztu.** Tabela w `docs/MODELE.md` jest pusta. → `docs/COST.md` definiuje pomiar.

## 3. Analiza luk (faza B)
Legenda: **ALREADY EXISTS**: mechanizm sprawdzony w `wgu`/`spqr`, przenosimy ideę (nie kod). **EXTEND**: idea
istnieje, ale wymaga rozbudowy. **NEW**: brak odpowiednika. **DEPRECATE**: świadomie porzucamy. **AVOID**: znana
pułapka. Ryzyka: **COST RISK**, **MIGRATION RISK** (dotyczy przenoszenia istniejących gier), **DIGITALIZATION RISK**.

| Element | Ocena | Ryzyka | Uwagi |
|---|---|---|---|
| KB jako YAML w git, źródło prawdy | ALREADY EXISTS | — | ADR-0004 |
| Stabilne ID, `refs`, lint | ALREADY EXISTS → EXTEND | MIGRATION RISK | jedna gramatyka, typowane prefiksy, walidacja referencji w M1 |
| Reguły atomowe z cytatem źródła | EXTEND | — | cytat → kotwica `SEG-` + hash (ADR-0012) |
| Rule IR (modalność, aktor, akcja, warunki, efekty, limity, timing) | NEW | DIGITALIZATION RISK | gramatyka wyrażeń minimalna, `formalization` pozwala na stopniowe dochodzenie |
| Pojęcia typowane (`CON-`: encje, stany, zmienne, predykaty, zdarzenia) | NEW (z `terms.yaml`) | — | glosariusz Stage 3 wiąże się z `CON-` |
| Relacje wyjątków i nadpisań | ALREADY EXISTS → EXTEND | — | jedyne miejsce zapisu (ADR-0005), `priority_basis` |
| Niejasności z wariantami i siłą rekomendacji | ALREADY EXISTS → EXTEND | — | `impact.digital`, `requires_human_interpretation` |
| Pytania kontrolne | ALREADY EXISTS → EXTEND | — | `case` z polaryzacją (positive/negative/boundary/override…) |
| Provenance | EXTEND (z `[wniosek]`, `status: inferred`) | — | 8 rodzajów, nadawany deterministycznie (ADR-0014) |
| Model ryzyka | NEW (zaczątek: `strength`) | COST RISK | błędna kalibracja = zbyt wiele eskalacji albo fałszywie negatywne wyniki |
| Inwentarz źródeł, mapa segmentów | NEW | — | Stage 0 |
| Ekstrakcja PDF, render, flagi wizualne | ALREADY EXISTS → EXTEND | — | przepisać deterministycznie z hashami segmentów |
| Pomiar oprawy → styl LaTeX, API makr | ALREADY EXISTS | — | Stage 2 (pomiar) + Stage 3 (styl) |
| Glosariusz pojęciowy w warstwach, dowody `supports` | ALREADY EXISTS | MIGRATION RISK | warstwy common/era/series przenieść danymi (decyzje D-01…D-10 są właściciela) |
| Trzy przebiegi weryfikacji przekładu | ALREADY EXISTS → EXTEND | COST RISK | dochodzi wsteczna ekstrakcja IR z przekładu (lokalnie) |
| `check fidelity` (heurystyki sygnałów) | EXTEND | — | porównywać przekład z IR, nie tylko z tekstem źródła; testy mutacyjne |
| Pomoce do gry (grafy decyzyjne) | ALREADY EXISTS → EXTEND | — | wyprowadzane z `procedure` + Stage 1.5 `sequence`; publikacja w Stage 3 |
| Eksport pakietu dla silnika | EXTEND | DIGITALIZATION RISK | `engine kit` ze śledzeniem i wynikami testów zwrotnie |
| Model stanu/akcji/legalności/zdarzeń | NEW (opisany tylko w procedurze `wgu`) | DIGITALIZATION RISK | kształt wzorowany na doświadczeniu `spqr` (ADR-0007) |
| Statusy etapów, bramki | NEW | — | obliczane (ADR-0011) |
| Orkiestracja (GLU), joby, routing, cache, przyrostowość | NEW | COST RISK | dziś „orkiestratorem” jest sesja Claude Code |
| Lokalna inferencja | NEW | COST RISK | jakość modeli lokalnych do zmierzenia (M-INF) |
| MCP / Claude Desktop | NEW | — | adapter (ADR-0013) |
| Skille jako orkiestratory, procedury agentów w plikach | ALREADY EXISTS | — | zostają jako interfejs ludzki; ciężka praca przechodzi do GLU |
| KB w języku docelowym | DEPRECATE | MIGRATION RISK | ADR-0003 |
| `exceptions` jako tekst w regule | DEPRECATE | — | ADR-0005 |
| `scenarios.yaml` jako pytania kontrolne | DEPRECATE | — | `case` |
| Ręczne tabele statusów/niejasności | AVOID | — | generować |
| Równoległe tłumaczenie bez zamrożonej terminologii | AVOID | COST RISK | poprawki po fakcie są drogie |
| DSL reguł do wykonania | AVOID | DIGITALIZATION RISK | ADR-0006 |
| Heurystyki bez testów mutacyjnych | AVOID | — | 8/8 fałszywych alarmów w pierwszej wersji |
| Pułapki Windows (heredoc, backslash, BOM, MiKTeX) | AVOID | — | ADR-0008; potwierdzone w Session 0: długi heredoc w Git Bash się nie sparsował, pliki pisane narzędziem Write |
| YAML 1.1: klucze `on`, `yes`, `no` czytane jako bool | AVOID | — | wykryte w Session 0 (`triggers.on` → `True`); pola nazwane `event`, `fires_on` |

## 4. Mechanizmy do ponownego wykorzystania (idee, nie kod)
- `wgu/check/fidelity.py`: słownik sygnałów EN/PL (modalność, zakaz, warunek, wyjątek, limit, kolejność, zakres) jako
  punkt startowy cech ryzyka i kontroli przekładu.
- `wgu/pdf/layout.py`: pomiar oprawy (fonty, kolumny, nagłówki, ramki z kolorami).
- `templates/latex/wgu-base.sty`: zasada „tekst używa tylko semantycznych makr”.
- `wgu/aids/validate.py`: walidacja grafu (każda decyzja ma wyjścia, brak martwych gałęzi).
- `wgu/terms/ops.py` (`impact`): punktowa aktualizacja po zmianie terminu.
- `spqr`: DecisionRequest z wyliczonymi opcjami, ramki procedur na stosie, Computation + Modifier + trace z RuleRef,
  zapis `{seed, inputs, snapshot, hash}`, generowane TRACEABILITY z `--check`, karty zadań z listą `context:`.
