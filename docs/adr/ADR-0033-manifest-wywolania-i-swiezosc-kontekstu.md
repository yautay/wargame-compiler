# ADR-0033: Manifest wywołania zadania w `prov.manifest`, jedna definicja zależności, świeżość kontekstu `kb/` i diagnostyka receiptu

- **Status:** przyjęty
- **Data:** 2026-10-06
- **Milestone:** M-STAB3b

## Kontekst
- Ustalenie F05 [przeglądu po M9a](../reviews/2026-10-05-przeglad-po-M9a.md): klucz joba i `prov.inputs_hash` mają
  różne definicje.
  - Planner bierze `TaskSpec.input_hash` (projekcja zadania albo projekcje `logic` wejść). `_provenance` liczy hash
    projekcji `logic` kotwic i `derived_from`, z niewersjonowanym zapasem dla rodzajów bez projekcji.
  - Własna projekcja zadania (`semantic_projection`) daje więc `prov.inputs_hash` różny od klucza joba (P3).
  - Zmiana roli dokumentu (`rules` → `errata`) zmienia ID tabeli i `prov.kind`, ale nie zmienia klucza joba (P11).
  - Pojęcie z `wgc.terms.harvest` ma `prov.inputs_hash` tylko z segmentów swoich kotwic, a job czyta wszystkie
    segmenty dokumentu z dopasowaniem. Pierwsze wystąpienie, kolejność `source_terms` i ID pojęcia (główna
    instrukcja, ADR-0030) zależą od całego odczytu.
  - Po utracie `.glu/` sam hash nie wystarcza do odtworzenia zależności.
- Decyzja N05 przeglądu: wariant B, czyli jawny manifest wywołania i osobne dowody rekordu. Tier 0 może mieć pusty
  kontekst tylko wtedy, gdy cały odczyt semantyczny jest w `input_hash`.
- `KBStale` (ADR-0026) sprawdza tylko inwentarz. Przyszłe zadanie modelowe czytające rekordy `kb/` jako kontekst
  mogłoby zapisać wynik obliczony ze starego kontekstu (ryzyko w STATUS).
- ADR-0031 liczy generację `kb/` (`wgc.kb.generation`: hash par ścieżka pliku i `sha256` bajtów) i zapisuje ją
  w receipcie akceptacji. Generacja obejmuje każdy plik `kb/`, także plik, do którego zadanie pisze wynik.
- Decyzja właściciela (2026-10-06): przed M10 potrzebne jest polecenie porównujące receipt wskazanego joba
  z bieżącym `kb/`. Polecenie tylko raportuje i niczego nie naprawia. Różnica względem historycznego receiptu nie
  oznacza sama w sobie uszkodzenia.
- Projekcje (F06) zmienia osobny ADR-0034. Ten ADR korzysta z jego wersji `wgc/projection@2`.

## Decyzja
**1. Manifest wywołania (`wgc/manifest@0`).** Jedyną definicją tego, co job czyta, jest `wgc.manifest.build(ws, spec,
inputs)`. Planner liczy z niej klucz joba, a `accept()` zapisuje ją w `prov.manifest`. Nic innego nie liczy hashy
wejść. Manifest zawiera:

| Pole | Zawartość |
|---|---|
| `format` | `wgc/manifest@0` |
| `task` | `id@wersja` zadania |
| `projection` | wersja projekcji (`wgc/projection@2`, ADR-0034) |
| `inputs` | `{id, hash}` każdego wejścia joba, w kolejności wejść. `hash` to `content_hash` projekcji wejścia: własnej projekcji zadania (`semantic_projection(ws, id)`) albo, domyślnie, projekcji `logic` |
| `authority` | `{id, hash}` dokumentów źródłowych, z których zadanie czyta dane autorytetu, posortowane po ID. `hash` to projekcja `logic` dokumentu (`role`, `seg_prefix`, `precedence`). Zawsze obejmuje dokumenty segmentów wejściowych, bo `accept()` wybiera z roli rodzaj provenance (ADR-0014). Zadanie dopisuje inne dokumenty przez `authority_selector`: harvest dopisuje każdy dokument `rules`, bo wybiera spośród nich główną instrukcję (ADR-0030) |
| `context` | `{id, hash}` rekordów `kb/`, które zadanie czyta jako kontekst (`context_selector`), posortowane po ID, z projekcją `logic`. Pomijane, gdy zadanie nie czyta kontekstu |

- W manifeście nie ma niczego zmiennego: ID joba, buildu, zakresu, czasu ani generacji `kb/`. `chapter:5` po `all`
  nie zmienia `kb/` (ADR-0030).
- Klucz joba (`glu/exec@0#cache_key`): `input_hash` = `content_hash` manifestu bez `context`, a `context_hash` =
  `content_hash` listy `context`. Dla zadania bez kontekstu to hash pustej listy, jak dotąd. Dane autorytetu są
  w `input_hash`, więc Tier 0 z pustym kontekstem obejmuje cały swój odczyt.
- `TaskSpec` (ARCHITECTURE §2):
  - `semantic_projection(ws, id) → dict` dla pojedynczego wejścia (wcześniej lista dla wszystkich wejść);
  - nowe pola `authority_selector(ws, wejścia) → [SRC-…]` i `context_selector(ws, wejścia) → [ID rekordów kb/]`;
  - znikają metody `projections` i `input_hash`.

**2. Dowody rekordu osobno od manifestu.** Dowodami pojedynczego rekordu są kotwice (`seg_hash` = `text_hash`) i
`derived_from`. `prov.inputs_hash` to hash dowodów: `content_hash({projection: <wersja>, records: [projekcje logic
segmentów kotwic i rekordów derived_from]})`.
- Każdy dowód należy do odczytu joba: segment kotwicy i każdy rekord `derived_from` muszą być w `inputs` albo
  `context` manifestu. Inaczej propozycja jest odrzucana, bo manifest nie obejmowałby tego, z czego rekord wynika.
- Zależność rekordu niesie `prov.manifest`. Rekord jest nieaktualny, gdy któryś wpis manifestu ma dziś inny hash albo
  zniknął. Liczy to `wgc.manifest.check(ws, manifest)` z samego inwentarza i `kb/`, bez `.glu/`.
  `check` nie uruchamia ponownie `input_selector`: nowe wejście (np. segment, który zaczął pasować do wzorca) wykrywa
  dopiero klucz joba przy następnym buildzie. Oznaczanie rekordów jako `stale` i graf to M13.
- Walidator sprawdza `prov.manifest` tylko schematem. Brakujący segment albo rekord z manifestu nie blokuje
  `accept()` (Q-12).

**3. Świeżość kontekstu `kb/`.** Zadanie czyta `kb/`, gdy ma `context_selector` albo wejście, które nie jest segmentem.
- **Migawka:** `wgc.kb.read_snapshot` czyta każdy plik `kb/` raz i z tych samych bajtów liczy generację i dokumenty.
  `Workspace.pinned(migawka)` daje widok, z którego `record()` i `kb_documents()` czytają tylko tę migawkę.
- **Wykonawca:** przed implementacją czyta migawkę (pod blokadą pisarza, ale bez tworzenia pliku blokady) i liczy
  z niej manifest, a implementacja czyta z tego samego widoku. Manifest wykonania różny od manifestu z planu (np.
  wcześniejszy job tego buildu zmienił kontekst) kończy job błędem przed `accept()`. Kolejność jobów należy do M13.
  Klucz joba w store i `prov.manifest` nigdy się więc nie rozjeżdżają.
- **`accept(…, manifest=…)`**, pod blokadą, po recovery, na migawce `kb/` czytanej pod blokadą, przed `validate`
  zadania i przed receiptem:
  - zadanie czytające `kb/` bez manifestu wykonania → `KBError`;
  - generacja migawki równa generacji z wykonania → kontekst ten sam (generacja to hash treści, więc równa generacja
    oznacza te same bajty, także po zmianie tam i z powrotem);
  - generacja inna → manifest liczony na nowo. Inny → `KBContextStale` (podklasa `KBStale`) z listą zmienionych
    wpisów. Niczego nie zapisano. W GLU to Attempt `error` i powód „kontekst kb/ zmienił się między wykonaniem a
    akceptacją”;
  - zadanie, które nie czyta `kb/`: manifest porównywany zawsze (tylko inwentarz), bez generacji. Zmiany `kb/` innych
    zadań (równoległy build) go nie blokują;
  - zapisany `prov.manifest` to manifest wykonania, sprawdzony powyżej.
- **Generacja jest tylko tokenem porównania.** Nie trafia do manifestu, `prov` ani klucza joba: obejmuje plik wyniku,
  więc każdy rebuild zmieniałby `kb/`.
- Gwarancje ADR-0026 i ADR-0031 bez zmian: ta sama blokada pisarza, recovery przed odczytem, odmowa przed receiptem
  i zapisem.

**4. Diagnostyka receiptu: `glu receipt <job> [--root] [--json]`.** Polecenie tylko czyta:
- bazę `.glu/state.db` otwiera tylko do odczytu (`mode=ro`), bez migracji. Inna wersja schematu bazy to błąd;
- `kb/` czyta pod blokadą pisarza tylko wtedy, gdy plik blokady istnieje (nie tworzy go);
- nie robi recovery ani reconcile, nie usuwa receiptów, nie bierze blokady startu buildów.

Receipt to `kb_receipt` Attemptu `accepted`. Gdy go nie ma, a job czeka w `validating` z receiptem w
`.glu/kb-receipts/`, porównywany jest ten receipt (oznaczony jako nierozstrzygnięty). Wynik:

| Status | Kiedy | Kod wyjścia |
|---|---|---|
| `match` | każdy rekord receiptu ma w `kb/` tę samą treść | 0 |
| `differs` | rekord ma inną treść albo go brak; dla każdego: bieżące `prov.job` i czy to późniejszy job | 1 |
| `no_job` | joba nie ma w bazie | 1 |
| `no_receipt` | job bez receiptu (np. `failed`, przerwany przed akceptacją) | 1 |
| `pending_batch` | `kb/` ma przerwaną partię; porównanie po `wgc kb recover` | 1 |
| błąd operacyjny | brak bazy, nieczytelny `kb/`, blokada zajęta dłużej niż 60 s | 2 |

Polecenie podaje też, czy generacja `kb/` jest równa generacji z receiptu. Komunikat przy różnicy mówi, że późniejszy
poprawny `accept()` (inny job, ręczna decyzja) też zmienia rekord, więc różnica nie oznacza sama w sobie uszkodzenia.
Receipty z pierwszej wersji M-STAB2 liczyły generację inaczej, więc ich generacja zawsze się różni.

**5. Kontrakt.** `common.schema.json`: `$defs/manifest` i opcjonalne `provenance.manifest` (zmiana addytywna w `@0`);
opis `provenance.inputs_hash` mówi teraz „hash dowodów rekordu”. `glu/exec@0` bez zmian.

## Konsekwencje
- F05 (P3, P11, harvest) rozwiązany testami: własna projekcja zadania daje równy klucz i `prov.manifest`; zmiana roli
  dokumentu zmienia klucz i `prov.manifest`; zmiana dowolnego wejścia joba harvest albo dokumentu `rules` zmienia
  manifest każdego pojęcia tego joba.
- Pierwszy build po wdrożeniu zapisuje istniejące rekordy z `prov.manifest` i nowym `prov.inputs_hash` (jednorazowo
  „zmienione”). Rekord bez `prov.manifest` nie jest błędem walidacji.
- Pojęcia harvest zmieniają się (`prov.manifest`), gdy zmieni się którekolwiek wejście ich joba, także segment bez ich
  kotwic. To poprawne, bo wynik zależy od całego odczytu.
- **Koszt:** manifest jest powtarzany w każdym rekordzie joba (harvest: w każdym pojęciu dokumentu). Pliki `kb/` rosną,
  a linie `prov` są długie. Przy dużych grach można przenieść manifesty do osobnego pliku w nowym ADR.
- Zmiana roli dokumentu nie odrzuca jeszcze propozycji (ADR-0027, M-STAB3c), a stary rekord o poprzednim ID zostaje
  w `kb/` (F11, Q-16, Q-12). Manifest tylko zapisuje dane, z których zadanie wybiera główną instrukcję. Reguła Q-17 się
  nie zmienia.
- Żadne zadanie nie czyta dziś `kb/` jako kontekstu. Mechanizm sprawdzają testy z zadaniem testowym. Pierwsze zadania
  z kontekstem przychodzą w M10/M14.
- Zadanie czytające `kb/` w buildzie, w którym wcześniejszy job zmienia jego kontekst, kończy się błędem i wymaga
  ponownego buildu. Kolejność i zależności między jobami to M13.
- Ryzyko „Windows bez `fsync` katalogu” ma narzędzie diagnostyczne: `glu receipt` pokazuje rozbieżność Attemptu
  `accepted` z `kb/`. Naprawą pozostaje ponowny build.

## Odrzucone warianty
- **Hash samych dowodów jako zależność (N05 A):** pomija odczyty spoza kotwic (harvest) i dane autorytetu.
- **Cały `Workspace` albo generacja `kb/` w hashu (N05 C):** każda zmiana unieważnia wszystko. Generacja obejmuje plik
  wyniku, więc każdy rebuild zmieniałby `kb/` bez końca.
- **Manifesty w osobnym pliku `kb/` (np. `kb/manifests/`):** każda akceptacja byłaby partią dwóch plików, potrzebny
  byłby nowy kontrakt dokumentu i sprzątanie osieroconych manifestów, a rekord bez manifestu stałby się błędem
  blokującym `accept()` (Q-12).
- **Manifest tylko w `.glu/`:** ginie razem z bazą stanu (ADR-0004).
- **Ścisłe porównanie generacji dla każdego zadania:** równoległe buildy odrzucałyby nawzajem swoje wyniki przez zmiany
  niezwiązanych plików.
- **Odczyt kontekstu z dysku przy każdym wywołaniu w trakcie joba:** kontrola sprawdzałaby manifest, a nie to, co
  przeczytała implementacja.
- **Diagnostyka receiptu w `wgc`:** receipt leży w Attemptcie w `.glu/state.db`, a `wgc` nie importuje `glu`
  (ADR-0002). Porównanie z `kb/` liczy `wgc`.
- **Diagnostyka z automatycznym recovery albo naprawą:** decyzja właściciela (2026-10-06): tylko raport.
