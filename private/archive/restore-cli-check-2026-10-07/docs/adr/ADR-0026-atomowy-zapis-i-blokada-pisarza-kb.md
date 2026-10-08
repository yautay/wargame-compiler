# ADR-0026: Atomowy zapis pliku KB i blokada pisarza projektu wokół całego `accept()`

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M-STAB1

## Kontekst
- ADR-0004: `kb/` w YAML/git jest źródłem prawdy. ADR-0025: `wgc.kb.accept()` jest jedyną drogą zapisu do `kb/`.
- [Przegląd po M9a](../reviews/2026-10-05-przeglad-po-M9a.md) wykazał na `96ded88`:
  - **F01:** `_write_file` otwierał plik docelowy przez `open("w")`. Awaria w trakcie zapisu zostawiała plik obcięty
    (odtworzone: 10 bajtów zamiast poprzedniej treści);
  - **F02:** odczyt, merge i zapis w `accept()` nie miały blokady. Dwa poprawne `accept()` do pustego KB zgłosiły
    `ok`, a na dysku został jeden rekord (odtworzone dwoma wątkami);
  - **F08:** `record.id=[]` i `anchors[].quote=123` dawały `TypeError`, a `columns=5` wywracał `validate` zadania.
    Niepoprawny `span` (`[5, 2]`, koniec poza tekstem) przechodził bez diagnostyki.
- Transakcja SQLite (`glu/store.py`, ADR-0023) chroni tylko bazę wykonania, nie pliki KB. WAL tego nie zmienia.
- GLU działa natywnie na Windows (ADR-0022). Tam `os.replace` zwraca `PermissionError`, gdy inny proces trzyma
  plik docelowy otwarty, a katalogu nie da się otworzyć do `fsync`.
- Wolno używać tylko biblioteki standardowej, jeśli wystarcza (CLAUDE.md).

## Decyzja
- **Zapis pliku (`wgc.fsio.atomic_write`, wołany wyłącznie przez `wgc.kb._write_file`):**
  - plik tymczasowy `.<nazwa>.<losowe>.wgc-tmp` w tym samym katalogu, zapis bajtów, `flush`, `os.fsync`,
    zamknięcie, potem `os.replace`;
  - każda awaria przed podmianą usuwa plik tymczasowy i zostawia plik docelowy bajt w bajt. Nie ma awaryjnego
    zapisu w miejscu (obcinania celu);
  - na Windows `os.replace` ponawia się kilka razy po `PermissionError` (łącznie ok. 1,5 s), potem błąd przechodzi
    dalej. Na POSIX nie ma ponowień, a po podmianie wykonuje się `fsync` katalogu;
  - na Windows katalogu nie da się otworzyć do `fsync`, więc ten krok się pomija. Gwarancja jest tam słabsza:
    podmiana jest atomowa (po awarii widać starą albo nową treść, nigdy obciętą), ale jej trwałość nie jest
    wymuszona. Po odcięciu zasilania tuż po zapisie może wrócić poprzednia wersja pliku;
  - na POSIX plik tymczasowy dostaje tryb zastępowanego pliku (a nowy plik: `0666 & ~umask`), bo `mkstemp` tworzy
    `0600`;
  - przyrostek `.wgc-tmp` nie jest `.yaml`, więc pozostałość po zabitym procesie nie jest czytana jako KB. Usuwa ją
    następny zapis pod blokadą.
- **Blokada pisarza projektu (`wgc.kb.lock`, `wgc.fsio.exclusive`):**
  - plik `<repo gry>/.glu/kb.lock`, poza `kb/`, bo `.glu/` jest gitignored (ADR-0004). Pliku się nie usuwa;
  - blokada systemowa: `msvcrt.locking` na Windows, `fcntl.flock` na POSIX (a nie `lockf`, który nie wyklucza
    wątków), plus `threading.Lock` na ścieżkę. Wyklucza procesy i wątki. System zwalnia ją przy końcu procesu, więc
    po awarii nie ma wiszącej blokady;
  - zajęta blokada: `accept()` czeka do `lock_timeout` (domyślnie `kb.LOCK_TIMEOUT` = 60 s), potem `KBBusy`
    (podklasa `KBError`): błąd operacyjny, a nie odrzucenie danych.
- **Sekcja krytyczna obejmuje cały odczyt, merge, walidację i zapis.** Kolejność w `accept()`:
  1. bez blokady: typy i kształt propozycji, potem schemat każdego `record` bez pól nadawanych przez WGC.
     Odrzucone dane nie czekają na blokadę i nie dotykają dysku;
  2. pod blokadą:
     - kontrola inwentarza;
     - świeży odczyt `kb/`;
     - `TaskSpec.validate`;
     - provenance (`derived_from` rozwiązywane w `kb/` z tego odczytu);
     - merge i walidacja całego `kb/` z inwentarzem sprawdzonym w tej samej sekcji;
     - zapis.
- **Przekazany `Workspace` nie może nadpisać nowszego wyniku starym stanem:**
  - `Workspace` nie buforuje `kb/`: rekordy czyta z dysku przy każdym wywołaniu, a `accept()` pod blokadą;
  - `Workspace` zapamiętuje odcisk bajtów inwentarza (`inventory_hash`). Gdy pod blokadą inwentarz na dysku jest
    inny, `accept()` zgłasza `KBStale` i niczego nie zapisuje. Bez tego job policzony przed `wgc source extract`
    zastąpiłby wynik tego samego zadania policzony po nim (reguła „ten sam producent zastępuje”).
- **Rozróżnienie wyników akceptacji:**
  - dane odrzucone → `AcceptResult.issues`;
  - awaria operacyjna → `KBError` (`KBBusy`, `KBStale`, `KBWriteError`);
  - każdy inny wyjątek to błąd programu i przechodzi dalej.

  Wykonawca GLU zapisuje odrzucenie jako Attempt `rejected`, a dwa pozostałe przypadki jako Attempt `error`
  (`error_class: runtime`) z osobnym powodem przejścia. W każdym przypadku job kończy się `validating → failed`.
  Kontrakt `glu/exec@0` się nie zmienia.
- **Typy propozycji (F08)** sprawdza kod `accept()`, bez nowego kontraktu. Schemat `wgc/proposal@0` z envelope
  i polityką statusów należy do następnego etapu (N07 przeglądu).

## Konsekwencje
- Awaria zapisu nie niszczy już pojedynczego pliku KB, a dwa `accept()` (wątki, procesy, dwa `glu build`) nie gubią
  rekordów. Testy: `tests/test_kb_safety.py` i `tests/test_glu_build.py`.
- **Granice, które zostają (nie rozwiązuje ich ten ADR):**
  - **brak commitu partii:** akceptacja zmieniająca kilka plików podmienia je po kolei. Awaria po pierwszym
    zostawia w `kb/` część wyniku, której żadna pełna wersja nie przeszła walidacji. `KBWriteError` wymienia
    podmienione pliki. Ponowny build nie zawsze to naprawi: jeśli stan częściowy ma niespełnione odsyłacze między
    plikami, walidacja całego `kb/` odrzuci każdy kolejny `accept()` (jak w Q-12) i pliki trzeba przywrócić z git.
    Naprawa: commit partii z manifestem i recovery (N01);
  - **brak recovery między `kb/` a `.glu/state.db`:** udany zapis KB, po którym zawiedzie zapis Attemptu, zostawia
    job w `validating` (F04, N04);
  - **blokada jest doradcza:** nie chroni przed ręczną edycją, `git checkout`/`merge` ani przed czytelnikami bez
    blokady (`wgc validate`, planner). Ci mogą zobaczyć stan między plikami partii, a na Windows trzymając plik
    otwarty mogą wymusić ponowienia `os.replace`;
  - **kontrola świeżości obejmuje tylko inwentarz:** `Workspace` nie zapisuje generacji `kb/` ani rekordów
    przeczytanych jako kontekst. Zadanie, które czyta rekordy KB do obliczenia wyniku (przyszłe zadania modelowe),
    może dać wynik ze starego kontekstu, choć `derived_from` w `prov` liczy się z bieżącego `kb/`. Naprawa: manifest
    wejść i generacja KB (N05);
  - **zbadane są tylko awarie wstrzykiwane wyjątkiem:** nie testowano odcięcia zasilania, zabicia procesu w trakcie
    `fsync` ani dysków sieciowych (blokady na SMB/NFS mogą działać inaczej);
  - **gałąź POSIX nie była uruchamiana:** `fcntl.flock`, `fsync` katalogu i tryb pliku sprawdzono tylko w kodzie
    i w testach pomijanych na Windows. M-STAB1 testowano na Windows 11 i Pythonie 3.13, nie na 3.10.
- Każdy `accept()` tworzy `.glu/kb.lock`, także w repo bez wcześniejszego `.glu/state.db`. Dry-run (`glu build
  --dry-run`) nie woła `accept()`, więc niczego nie tworzy.
- Akceptacje jednego projektu wykonują się po kolei. Przy tysiącach jobów i globalnej walidacji (F18) blokada staje
  się wąskim gardłem. Obliczenia mogą iść równolegle, ale akceptacje czekają: pomiar w M11/M14.

## Odrzucone warianty
- **Blokada tylko wokół `_write_file`:** odczyt i merge na starym stanie nadal gubią rekordy (F02).
- **WAL albo transakcja SQLite jako ochrona `kb/`:** dotyczy tylko bazy wykonania.
- **Blokada w `kb/` (`kb/.lock`):** byłaby widoczna w git repo gry.
- **Plik blokady tworzony wyłącznie (`O_EXCL`) i usuwany po zapisie:** po zabitym procesie zostaje wisząca blokada,
  którą trzeba usuwać ręcznie albo heurystyką wieku.
- **Awaryjny zapis w miejscu po nieudanym `os.replace`:** przywraca F01.
- **Zależność `filelock`/`portalocker`:** biblioteka standardowa wystarcza (`msvcrt`, `fcntl`).
- **Natychmiastowy błąd przy zajętej blokadzie:** dwa równoległe buildy tej samej gry kończyłyby się błędem, choć
  ich akceptacje trwają ułamki sekund. Wybrano czekanie z limitem.
- **Generacja całego `kb/` porównywana przy każdym `accept()` (CAS):** własne zapisy buildu unieważniałyby jego
  `Workspace`, a dla zadań Tier 0, które czytają tylko segmenty, nic nie wnosi. Wraca z manifestem wejść (N05).
