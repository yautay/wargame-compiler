# ADR-0023: Job store GLU w SQLite i maszyna stanów joba i buildu jako tabela

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M8

## Kontekst
- ADR-0004 umieszcza stan wykonania w `.glu/` repo gry: Build, Job, Attempt i RoutingDecision w SQLite.
- [GLU §3](../GLU.md#3-cykl-życia-joba) opisuje cykl życia joba diagramem. Nie wyznacza wszystkich krawędzi, na
  przykład `cancelled`, `stale` i cyklu życia buildu.
- Kontrakt `glu/exec@0` jest szkicem i może się jeszcze zmieniać bez migracji (DATA-CONTRACTS §2).
- GLU działa natywnie na Windows (ADR-0022): otwarty plik SQLite blokuje jego usunięcie.
- Biblioteka standardowa ma `sqlite3`, więc store nie potrzebuje nowej zależności.

## Decyzja
- **Baza:** `<repo gry>/.glu/state.db` (`glu.store.db_path`), `sqlite3` z biblioteki standardowej.
  - Domyślny journal (bez WAL).
  - `foreign_keys = ON`.
  - `isolation_level=None` i jawne transakcje `BEGIN IMMEDIATE` wokół każdego odczytu, sprawdzenia i zapisu.
  - Połączenie zamykane jawnie (`Store` jako context manager).
- **Tabele:**
  - `build`, `job`, `attempt` i `routing_decision`. Każdy rekord `glu/exec@0` leży w całości w kolumnie `body`
    (JSON), a osobne kolumny (`state`, `tier`, `build`, `job`, czasy) służą tylko wyszukiwaniu;
  - `transition` to dziennik zmian stanu: `src`, `dst`, czas i powód. `src` jest pusty przy utworzeniu rekordu;
  - `job.attempts` nie jest zapisywane, tylko wyliczane z tabeli `attempt` w kolejności zapisu.
- **Walidacja przy zapisie:** każdy rekord przechodzi `glu/exec@0` (`wgc.contracts`) przed zapisem. Store nie trzyma
  rekordu, którego `export()` nie mógłby wydać. Stąd na przykład `premium_reason` jest wymagany przy `chosen: premium`.
- **Migracje schematu bazy:**
  - wersja w `PRAGMA user_version`;
  - migracje to uporządkowana lista kroków SQL w kodzie (`glu.store.MIGRATIONS`), tylko dopisywana;
  - każdy krok wykonuje się instrukcja po instrukcji w jednej transakcji razem ze zmianą `user_version`. Nie używamy
    `executescript`, który sam zatwierdza transakcję;
  - baza w wersji nowszej niż kod jest odrzucana z błędem.
- **Przejścia są danymi:** `glu.states.JOB_RULES` i `BUILD_RULES`.
  - Reguła ma źródło i cel, a opcjonalnie strażnika (nazwany warunek), efekt (nazwana zmiana rekordu) i listę
    przyjmowanych parametrów.
  - `states.step` jest jedynym interpreterem tabel.
  - Przejście spoza tabeli, niespełniony strażnik albo nieprzyjmowany parametr to `IllegalTransition` z komunikatem
    po polsku. Stan się wtedy nie zmienia.
  - Tabele zapisuje [GLU §3](../GLU.md#3-cykl-życia-joba).
- **Ustalenia ponad diagram GLU §3:**
  - `cancelled` z każdego aktywnego stanu joba;
  - `rejected`, `failed` i `cancelled` są końcowe;
  - `stale → pending`;
  - `waiting_inference → running` (a nie `ready`);
  - `waiting_inference → escalated` tylko przy `policy.fallback.allow_premium_fallback: true` (strażnik, ADR-0017);
  - `escalated → ready` musi podnieść `tier` (kolejność `deterministic < local < premium < human`);
  - cache hit `ready → accepted` ustawia `cache_hit: true`, a `ready → running` ustawia `cache_hit: false`.
- **Build:**
  - `planning → running`;
  - `running` ⇄ `waiting_inference` / `waiting_review` / `waiting_human`;
  - `done` tylko z `running`;
  - `failed` i `cancelled` z każdego aktywnego stanu;
  - stany końcowe `done`, `failed` i `cancelled` ustawiają `finished_at` i przyjmują `metrics`. Wznowienie po
    `failed` to nowy build.
- **Stan buildu nie jest wyliczany ze stanów jobów.** Ustawia go wykonawca (M9, M10).
- **Próby jakościowe:** store nie trzyma licznika. `quality_attempts(job, tier)` liczy Attempty z
  `outcome ≠ unavailable`, więc `waiting_inference` nie zużywa prób (ADR-0017). Limit N egzekwuje pętla structured
  output (M10).
- **ID i czas** są wstrzykiwane (`clock`, `new_id`).
  - Domyślnie: UTC zapisany jako `RRRR-MM-DDTHH:MM:SSZ` i ID w stylu ULID (26 znaków base32 Crockforda,
    sortowalne po czasie), np. `job_01K…`.
  - Prefiksy `build`, `job`, `att` i `rd` zgadzają się z `xid` w `glu/exec@0`.
  - Testy używają licznika (`job_000001`) i stałego zegara.
- **Eksport:** `Store.export()` i `glu export [--build] [--out]`.
  - Wynik to jeden dokument `glu/exec@0`: każdy build, jego joby, a dla każdego joba jego Attempty i RoutingDecision.
  - Pola idą w kolejności definicji kontraktu.
  - Dokument jest walidowany przed wydaniem.
  - `review_package` nie jest jeszcze przechowywany (M12/M13).
- **CLI:**
  - skrypt `glu` w `[project.scripts]`;
  - `glu status [--root] [--build] [--json]` nie tworzy `.glu/`;
  - brak bazy, uszkodzona baza, baza z nowszej wersji albo nieznany build to błąd operacyjny z kodem 2, tak jak w `wgc`.

## Konsekwencje
- Zmiana pól `glu/exec@0` w okresie `@0` nie wymaga migracji bazy, bo rekordy leżą w `body`. Migracja jest potrzebna
  tylko przy zmianie kolumn albo indeksów.
- Każde przejście można przetestować z samej tabeli: testy generują ścieżkę do stanu źródłowego (BFS) i sprawdzają
  każdą krawędź oraz każdą parę spoza tabeli.
- Walidacja schematem przy każdym zapisie kosztuje czas, ale jest pomijalna przy setkach jobów. Gdy pomiar pokaże
  problem, można ją ograniczyć do eksportu.
- Jeden pisarz naraz. MCP (M22) i równoległe polecenia mogą wymagać WAL albo dłuższego `timeout`: decyzja w M22.

## Odrzucone warianty
- **Tabela wersji `schema_migrations`:** `user_version` jest atomowe w transakcji migracji i nie wymaga dodatkowej tabeli.
- **Pełne kolumny dla wszystkich pól kontraktu:** każda zmiana szkicu `@0` wymagałaby migracji bazy.
- **Licznik prób w rekordzie joba:** łatwo go rozjechać z tabelą `attempt`. Liczba wyliczana z Attemptów jest
  jednoznaczna.
- **Stan buildu wyliczany triggerem ze stanów jobów:** to logika wykonawcy, a nie store'u.
- **ORM albo inna biblioteka:** nowa zależność bez potrzeby.
