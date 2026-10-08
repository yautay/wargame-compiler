# ADR-0030: Harvest terminów Tier 0: wzorce o pewnej kategorii, job na dokument, ID pojęć

- **Status:** przyjęty; zależności joba harvest w `prov.manifest` według ADR-0033, ownership dokumentu i wycofanie outputów według ADR-0035
- **Data:** 2026-10-05
- **Milestone:** M9b

## Kontekst
- ROADMAP M9b: zadanie `wgc.terms.harvest@0` daje rekordy `concept` tylko dla wzorców o pewnej kategorii (`NdM` →
  `die`, `Scenario: X` → `scenario`, pozycje listy sekwencji `… Phase` → `phase`). Kategorię pozostałych terminów
  ustala M14. Bez NLP, embeddingów i ontologii.
- `accept()` (ADR-0025, ADR-0026) jest jedyną drogą zapisu do `kb/`:
  - odrzuca wynik zadania z powtórzonym ID;
  - rekord tego samego producenta zastępuje;
  - rekord innego producenta to konflikt.

  Do M-STAB2 akceptacja zmieniająca kilka plików nie jest atomowa jako partia.
- W `bench/minigame` ten sam termin występuje w kilku segmentach (`1d6` w 4.2 i 5.2).
- DATA-CONTRACTS §4 podaje dla `CON-` tylko klucz `snake_case` i `scn.<nazwa>` dla scenariusza. Nie ma reguły dla
  wielu dokumentów.
- `wgc source init` nadaje pierwszemu dokumentowi `rules` ID `SRC-<gra>.rules` i `seg_prefix: <gra>`. Kolejne
  dokumenty tej roli dostają `.2`, `.3`. Klucz `SRC-` jest unikalny w inwentarzu (`duplicate_id`), a `seg_prefix`
  nie musi być.

## Decyzja
- **Wzorce** (`wgc/terms.py`). Inne dopasowania nie dają rekordu.

  | Kategoria | Wzorzec | Klucz | `name` |
  |---|---|---|---|
  | `die` | `NdM` jako całe słowo, z liczbą kostek: `1d6`, `2D6`; N ≥ 1, M ≥ 2 | `d<M>` | `d<M>` |
  | `scenario` | segment `heading`, którego cały tekst to `Scenario: X` | `scn.<slug(X)>` | `X` |
  | `phase` | wiersz listy numerowanej (`N.` albo `N)`, co najmniej dwa takie wiersze w segmencie), którego cała pozycja to słowa z wielkiej litery zakończone `Phase` (opcjonalnie kropka) | `<slug(name)>`, zawsze z końcówką `_phase` | jak w druku |

  - `slug`: NFKD, tylko ASCII, małe litery, ciągi `[a-z0-9]` łączone `_`. Słów się nie usuwa (`The Ford` →
    `scn.the_ford`). Klucz spoza gramatyki ID nie daje rekordu.
  - Kostka to pojęcie rozmiaru kostki: `1d6` i `2d6` dają jedno `CON-d6`.
  - Postaci klucza dla kategorii są rozłączne, więc dwie kategorie nie dają tego samego ID.
- **ID pojęcia:**
  - `CON-<klucz>` dla głównej instrukcji: dokumentu `rules` o najmniejszym ID `SRC-` (czyli `SRC-<gra>.rules`),
    niezależnie od kolejności dokumentów w inwentarzu;
  - `CON-<klucz SRC>:<klucz>` dla każdego innego dokumentu, np. `CON-dsk.scenario_book:scn.the_ford` albo
    `CON-dsk.rules.2:d6`;
  - klucz `SRC-` jest unikalny, więc dwa dokumenty nigdy nie proponują tego samego ID. Łączenie pojęć między
    dokumentami (np. `CON-d6` i `CON-dsk.scenario_book:d6`) należy do M14;
  - **warunek:** reguła zakłada nazewnictwo `wgc source init` (`SRC-<gra>.rules`, kolejne `.2`, `.3`). Dokument
    `rules` dopisany ręcznie z ID sortującym się wcześniej (np. `SRC-dsk.advanced`) przejąłby rolę głównej
    instrukcji. Wtedy zmieniłyby się ID pojęć obu dokumentów, a stare rekordy stałyby się nieaktualne (Q-12). Wybór
    głównej instrukcji dla `CON-` i `TAB-` to kwestia Q-17.
- **Joby:**
  - jeden job na dokument;
  - job powstaje, gdy zakres buildu zawiera segment z dopasowaniem;
  - jego wejścia to wszystkie segmenty tego dokumentu z dopasowaniem, niezależnie od zakresu. Rekord nie zależy od
    `--scope`: `chapter:5` po `all` nie zmienia `kb/`.
- **Propozycja:**
  - jedna na ID: `kind`, `id`, `category`, `name`, `source_terms`;
  - `source_terms` to terminy w druku w kolejności pierwszego wystąpienia;
  - każdy termin ma jedną kotwicę `{seg, quote}` w pierwszym wystąpieniu. `quote` to termin, a dla scenariusza cały
    `Scenario: X`, dosłownie z segmentu (po złączeniu białych znaków). Bez `span`.
- **`validate` zadania:**
  - kategoria spoza `die`, `phase`, `scenario` jest odrzucana;
  - klucz musi mieć postać swojej kategorii;
  - kotwica musi mieć `quote` i wskazywać wejście joba;
  - wzorce uruchamia się ponownie na wejściach joba: ID z kategorią i każda para (segment, cytat) muszą pochodzić
    z rzeczywistego dopasowania.

  „Brak zgadywanych kategorii” jest więc kontrolą, a nie tylko konwencją: poprawnie zbudowana propozycja z cytatem
  dosłownym, której żaden wzorzec nie daje, jest odrzucana.
- Polityka provenance bez zmian: `accept()` jak w M-STAB1. Rekordy pojęć leżą w jednym pliku
  `kb/logic/concepts.yaml`, więc akceptacja joba harvest zmienia jeden plik.

## Konsekwencje
- **Gra benchmarkowa:** `CON-rally_phase`, `CON-movement_phase`, `CON-combat_phase`, `CON-end_phase`, `CON-d6`,
  `CON-scn.the_ford`. Ponowny build daje „bez zmian 7” razem z `TAB-4.3`.
- **`inputs_hash` w `prov`** to hash projekcji segmentów kotwic rekordu (DATA-CONTRACTS §10). Dla harvest nie jest
  równy `input_hash` klucza cache joba, który obejmuje wszystkie segmenty z dopasowaniem w dokumencie.
- **Termin znika ze źródła:**
  - od M-STAB3c harvest uzgadnia kompletny zbiór outputów dokumentu i wycofuje brakujące pojęcie (ADR-0035);
  - jeśli znikną wszystkie segmenty dokumentu, planner nie ma już wejścia dla joba; usunięcie źródła pozostaje
    w Q-12/M13.
- **Zmiana tekstu segmentu z kotwicami pojęć:** pierwszy build po niej może się nie udać dla zadań wykonywanych
  przed harvest (`wgc.tables.parse` widzi stare `seg_hash`). Harvest odświeża swoje rekordy, a następny build
  przechodzi. To ta sama kwestia Q-12.
- **Fixture `logic.minigame.yaml`** przypisuje `wgc.terms.harvest@0` pojęcia o kategoriach, których to zadanie nie
  daje (`CON-rally` jako `action`, `CON-game`, `CON-enter_hex`), i klucz `CON-scn.ford`. Fixture pozostaje
  ilustracją kontraktu, nie gold (jak `TAB-crt`).
- **Pojęcie z dokumentu niekanonicznego** (`community_interpretation`, `prior_translation`) jest odrzucane od
  M-STAB3c (ADR-0027). Ponieważ job obejmuje jeden dokument, odrzucenie nie zablokuje
  pojęć z innych dokumentów.
- **Rekord tego samego ID od innego producenta** (np. model w M14 albo `HD-`) daje konflikt i job harvest kończy się
  `failed`. M-STAB3c przypisuje ownera do taska i zakresu wejść; polityka wzbogacania pojęć przez M14 pozostaje
  otwarta (Q-16).
- **Wzorce ścisłe:**
  - pominięte są `Scenario 2: X`, pozycje listy z opisem (`1. Movement Phase: …`), listy punktowane (Stage 0 usuwa
    punktory), kroki `… Step` i gołe `d6`;
  - rozszerzenie wzorców to nowa wersja zadania (`@1`).
- `TAB-` zachowuje regułę z M9a (`role: rules` bez przedrostka). Przy dwóch dokumentach `rules` dwie tabele o tej
  samej etykiecie dostałyby to samo ID. To kwestia do STATUS, nie zmiana w M9b.

## Odrzucone warianty
- **Job na segment:** `CON-d6` z 4.2 i z 5.2 nadpisywałyby się nawzajem. Każdy rebuild zmieniałby `kb/`.
- **Wejścia joba = segmenty z zakresu:** `--scope chapter:5` po `all` przenosiłby kotwicę `CON-d6` z 4.2 do 5.2.
- **Jeden job na cały build (wszystkie dokumenty):**
  - kotwice z dokumentów o różnych rolach w jednym rekordzie są odrzucane;
  - te same nazwy scenariuszy w dwóch modułach dałyby jedno ID;
  - odrzucenie jednego pojęcia (np. przez ADR-0027) blokowałoby wszystkie.
- **`CON-<seg_prefix>:<klucz>` (jak `TAB-`):** `seg_prefix` jest polem ręcznym i nie musi być unikalny.
- **Główna instrukcja = każdy dokument `rules` albo pierwszy w kolejności inwentarza:** kolizja przy dwóch
  dokumentach `rules` albo ID zależne od kolejności wpisów.
- **Usuwanie przedimków, skrótów i liczby kostek z klucza (`scn.ford`, `2d6`):** to zgadywanie, a liczba kostek nie
  jest cechą pojęcia kostki.
- **Kategorie z kontekstu zdania (`Routed` → `state`, `rally attempt` → `action`):** to zadanie modelu w M14.
