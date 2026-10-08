# ADR-0034: Projekcje semantyczne `wgc/projection@2`: treść nieformalizowana, definicje predykatów, rodzaje M10–M14 i E2E

- **Status:** przyjęty
- **Data:** 2026-10-06
- **Milestone:** M-STAB3b

## Kontekst
- Ustalenie F06 [przeglądu po M9a](../reviews/2026-10-05-przeglad-po-M9a.md):
  - projekcje reguły nie obejmują `unformalized` ani `statement`. Dla reguły z `formalization: none` albo `partial`
    zmiana zakazu opisanego tylko glosą nie zmieniała hashy `logic`, `digital` ani `publication` (P4);
  - projekcja `digital` pojęcia pomija `definition` i `defined_by`, więc zmiana znaczenia predykatu nie unieważnia
    digitalizacji;
  - rejestr ma tylko `segment`, `rule`, `concept` i `relation`. Domyślna projekcja wejścia innego rodzaju dawała
    `KeyError`, a `_provenance` miało niewersjonowany zapas (cały rekord bez pól WGC).
- Decyzja N06 przeglądu: wariant B, czyli warunkowe pola semantyczne i kompletne projekcje używanych rodzajów; cały
  rekord tylko jako jawnie wersjonowany wariant przejściowy.
- LOGIC-MODEL: `formalization` ma wartości `full`, `partial` i `none`, domyślnie `full`; przy `partial` wymagane jest
  `unformalized`. Predykat to pojęcie `category: predicate` z definicją i regułami definiującymi (`defined_by`).
- Rodzaje czytane w M10–M14 i M-E2E (ROADMAP): M14 czyta segmenty, pojęcia, reguły, relacje, tabele, procedury,
  przypadki i niejasności. M-E2E wyprowadza z reguły `LEG-` i `TST-` (Stage 1.5).
- ADR-0033 zapisuje wersję projekcji w manifeście wywołania.

## Decyzja
- **Wersja `wgc/projection@2`** (`wgc.canonical.PROJECTION_VERSION`). Wersja wchodzi do hashowanej treści manifestu
  i hasha dowodów (`prov.inputs_hash`), więc zmiana listy pól zawsze daje nowe klucze.
- **Pola warunkowe** (`wgc.canonical.CONDITIONAL`, dane jak `PROJECTIONS`):

  | Rodzaj | Warunek | Dodatkowe pola | Konsumenci |
  |---|---|---|---|
  | `rule` | `formalization` `none` albo `partial` (brak pola = `full`) | `statement`, `unformalized` | `logic`, `digital`, `publication` |
  | `concept` | `category: predicate` | `definition`, `defined_by` | `digital` (w `logic` już są, w `publication` jest `definition`) |

  Przy pełnym IR glosa nadal nie wchodzi do projekcji (ADR-0003).
- **Nowe pary w rejestrze:**

  | Rodzaj | `logic` | `digital` | `publication` |
  |---|---|---|---|
  | `source_document` | `role`, `seg_prefix`, `precedence` | — | — |
  | `table` | `title`, `columns`, `rows`, `complete` | `title`, `columns`, `rows`, `complete` | `title`, `columns`, `rows` |
  | `procedure` | `title`, `category`, `repeat`, `steps` | `title`, `category`, `repeat`, `steps` | `title`, `steps` |
  | `ambiguity` | `scope`, `question`, `readings`, `recommendation`, `impact`, `resolved_by` | — | — |
  | `interpretation` | `ambiguity`, `reading`, `statement` | `ambiguity`, `reading`, `statement` | — |
  | `case` | `polarity`, `question`, `expected`, `verdict`, `chain` | `polarity`, `question`, `expected`, `verdict`, `chain` | — |
  | `change` | `change_kind`, `affects`, `summary`, `from_edition`, `to_edition` | — | — |
  | `legality` | — | `applies_to`, `check`, `predicate`, `reason_code`, `unless`, `realizes` | — |
  | `test` | — | `category`, `from_case`, `covers`, `given`, `when`, `then`, `realizes` | — |

  - `interpretation.statement` to treść przyjętego odczytu, a nie glosa reguły, więc wchodzi do projekcji.
  - Każdy rodzaj rekordu `kb/logic` (`wgc.kb.KIND_FILES`) ma projekcję `logic`. Pilnuje tego test.
- **Bez zapasów:** rodzaj bez projekcji dla danego konsumenta to błąd z nazwą wersji projekcji:
  - w manifeście (wejście albo kontekst) `KBError`;
  - w `derived_from` propozycji odrzucenie.
- **Segment bez zmian:** `logic` z `text_hash` i `struct_hash`, `publication` z `text_hash` (ADR-0032). Projekcji
  segmentu tylko z `text_hash` nie dodajemy, bo żadne zadanie nie czyta wyłącznie `normalize_text`.

## Konsekwencje
- Zmiana treści nieformalizowanej reguły `none`/`partial` zmienia hashe wszystkich trzech konsumentów. Zmiana glosy
  reguły `full` nadal ich nie zmienia (testy).
- Zmiana definicji albo `defined_by` predykatu zmienia projekcję `digital` pojęcia. Znaczenie samych reguł
  definiujących (przechodnio, przez `defined_by` i `pred:` w wyrażeniach) dochodzi przez graf zależności (M13) albo
  `dependency_state` klucza joba. Ten ADR tego nie robi.
- Podbicie wersji zmienia każdy manifest i `prov.inputs_hash`. Pierwszy build po wdrożeniu zapisuje rekordy jednorazowo
  jako „zmienione”, razem ze skutkiem ADR-0033.
- Kolejność elementów list przemiennych (`all`, `any`) nadal wchodzi do hasha. Może dawać zbędne missy, ale nie błędne
  trafienia. Normalizacja wymaga osobnej decyzji (F06).
- Nowy rodzaj rekordu albo nowy konsument wymaga wpisu w rejestrze i nowej wersji projekcji.

## Odrzucone warianty
- **Glosa zawsze poza projekcją (N06 A):** przy `none`/`partial` glosa niesie znaczenie, którego IR nie ma.
- **Glosa zawsze w projekcji:** przy pełnym IR każda poprawka stylu unieważniałaby digitalizację i przekład.
- **Cały rekord bez pól WGC jako domyślna projekcja (N06 C):** ukrywa brak decyzji o polach i daje missy przy każdej
  zmianie notatek albo `refs`. Wariant zostaje możliwy tylko jako jawny wpis w rejestrze z nową wersją.
- **Niewersjonowany zapas w provenance:** dwie definicje zależności (F05).
- **Projekcje dla wszystkich rodzajów `wgc/digital@0`:** bez konsumentów przed M17. Dopisuje je milestone, który ich
  potrzebuje.
