# Stage 2 (Editorial) i Stage 3 (Translation / Publication)

## Stage 2: model redakcyjny
**Pytanie:** jak oryginał komunikuje swoją treść? Stage 2 opisuje język i wygląd oryginału, żeby przekład mógł je
świadomie odwzorować. **Nie zmienia Stage 1.** Podejrzenie błędu logiki zgłasza jako `RR-` (`from_stage: stage2`).

| Obszar | Rekord (`wgc/editorial@0`, M24) | Przykład treści | Źródło danych |
|---|---|---|---|
| Rejestr i ton | `register_profile` | rejestr przepisu / przykładu / noty historycznej / noty projektanta; ton wojskowy | segmenty wg `segment_type` |
| Modalność | `modal_convention` | jak źródło wyraża obowiązek, uprawnienie, zakaz („may not”, „must”, „is not required to”) | segmenty + IR (`modality`) |
| Definiowanie pojęć | `term_convention` | pojęcie definiowane przez wielką literę, pogrubienie, słowniczek; `CON-` → forma zapisu | `CON-.source_terms`, flagi typograficzne |
| Wyjątki | `exception_convention` | „Exception:”, nawias, osobny akapit | segmenty + `REL-` |
| Struktura | `structure_map` | hierarchia sekcji, schemat numeracji, listy kroków, odsyłacze | segmenty (`parent`, `label`) |
| Elementy | `box_type` | ramki (designer note, historical note, play note, example) z kolorem, ramką, etykietą | pomiar PDF + render |
| Tabele i przykłady | `table_style`, `example_convention` | układ tabel, przykłady jako ramka czy akapit | pomiar PDF |
| Typografia i oprawa | `layout_spec` | format, kolumny, fonty (wolne zamienniki), nagłówki, paginy, kolory ról | pomiar PDF (idea `wgu pdf layout`) |
| Konwencje graficzne | `visual_convention` | żetony w tekście, diagramy heksów, ikony | render + inwentarz `SRC-counters` |

Wykonawcy: pomiar oprawy i struktura są deterministyczne (Tier 0). Rejestr, konwencje i rozpoznanie ramek robi model
lokalny, a weryfikuje je człowiek na próbce stron. Premium jest potrzebne rzadko (Stage 2 ma niskie ryzyko semantyczne).

## Stage 3: przekład i publikacja
**Pytanie:** jak powiedzieć to samo w języku docelowym i wydać to w oprawie oryginału? Stage 3 **nie analizuje
mechaniki od nowa**. Znaczenie bierze z IR, styl ze Stage 2, terminy z glosariusza.

### Wejścia
`source fragment` (segment) + **Logic Model** (projekcja semantyczna reguł segmentu: modalność, warunki, limity,
liczby, odwołania) + **Editorial Model** + **glosariusz** (warstwy) + **polityka przekładu** + **preferencje właściciela** (`HD-`).

### Glosariusz pojęciowy (idea przeniesiona z `wgu`, ALREADY EXISTS)
- Jednostką jest **pojęcie**, nie słowo. Pojęcie gry to `CON-` ze Stage 1. Warstwy wspólne (common → era → series)
  mają klucze globalne (np. `wg.zoc`), a pojęcie gry wskazuje swój odpowiednik warstwowy albo jawne `overrides`.
- Rekord: `concept`, `target_lang`, `term`, `forms` (odmiana), `rejected` (z powodem), `evidence` (`supports`:
  existence / sense / military-usage / usage-in-games / against), `notation` (pierwsze użycie, wielkie litery,
  tekst na komponentach), `status` (`proposal` → `approved` tylko decyzją `HD-`; `disputed`, `deprecated`), `history`.
- Dwie mechaniki nigdy nie dzielą odpowiednika (*rout* ≠ *withdrawal* ≠ *retreat*). Lint to wykrywa.
- **Bramka Stage 3:** wszystkie `CON-` użyte w zakresie mają termin `approved`, zanim ruszy przekład równoległy (lekcja 16).

### Wyjścia
- `translation_segment` (M26): `seg`, `lang`, `text` (przekład), `concepts_used`, `ir_hash`, `editorial_hash`,
  `glossary_hash`, `verification[]`, `status`. Hash wejść pozwala unieważnić tylko te segmenty, których wejście się zmieniło.
- LaTeX: tekst używa **wyłącznie semantycznych makr** (reguła, wyjątek, przykład, noty, nowe w wydaniu, glosa
  oryginału, żeton). Styl jest generowany z `layout_spec` (idea `wgu-base.sty` + `wgu tex style`). Zmiana oprawy nie
  zmienia tekstu i nie unieważnia Stage 1 ani przekładów.
- Odwołania do zasobów graficznych (żetony, diagramy) z inwentarza, pomoce do gry (z `PROC-` i Stage 1.5 `SEQ-`),
  słowniczek generowany z glosariusza, PDF.

### Weryfikacja przekładu (rozszerzenie trzech przebiegów z `wgu`)
| Krok | Wykonawca | Sprawdza |
|---|---|---|
| 1. Terminologia i liczby | deterministycznie | formy z glosariusza, odrzucone formy, liczby, odsyłacze, kości |
| 2. Sygnały vs IR | deterministycznie | słownik sygnałów języka docelowego porównywany z IR (np. `modality: must_not` → w przekładzie musi być zakaz; `limit op: <=` → „co najwyżej / do”; liczba warunków) |
| 3. Wsteczna ekstrakcja IR | lokalnie (`local_semantic`) | model czyta **przekład** i wyciąga IR-lite (modalność, warunki, limity, liczby, aktor). Porównanie z IR kanonicznym jest deterministyczne |
| 4. Znaczenie (selektywnie) | premium | segmenty z rozbieżnością w krokach 2–3, z ryzykiem `high`/`critical` i próbka audytowa |
| 5. Redakcja językowa | lokalnie lub premium | styl wg Stage 2 i przewodnika; zmiana dotykająca treści wraca do kroków 2–4 |
| 6. Terminy sporne, notatki tłumacza | człowiek | decyzje `HD-` |

Krok 3 zastępuje część kosztownego przeglądu premium: zamiast czytać każdy segment, premium dostaje tylko rozbieżności.

### Pomoce do gry
Grafy decyzyjne (idea `wgu` `kb/aids`) wyprowadzane są z `PROC-` (Stage 1) i `SEQ-`/`DP-` (Stage 1.5), a etykiety
z glosariusza. Walidator grafu (każda decyzja ma wyjścia, brak martwych gałęzi) jest deterministyczny. Grafika powstaje w Stage 3.
