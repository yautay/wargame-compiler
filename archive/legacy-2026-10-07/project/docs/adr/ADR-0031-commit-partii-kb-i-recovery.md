# ADR-0031: Commit partii plików KB z dziennikiem wycofania, receipt akceptacji i reconcile GLU

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M-STAB2

## Kontekst
- ADR-0026 dał atomowy zapis **pojedynczego** pliku `kb/` i blokadę pisarza wokół całego `accept()`. Akceptacja
  zmieniająca kilka plików podmieniała je po kolei: awaria po pierwszej podmianie zostawiała część wyniku (F01, N01
  [przeglądu po M9a](../reviews/2026-10-05-przeglad-po-M9a.md)).
- `glu/exec.py` zapisywał KB, a dopiero potem Attempt i przejścia joba, każde w osobnej transakcji. Awaria po zapisie
  KB zostawiała job w `validating` bez Attemptu, a build w `running` (F04, N04). Nie było polecenia wznowienia ani
  uzgodnienia.
- ADR-0004: `kb/` jest źródłem prawdy, a utrata `.glu/` kosztuje tylko ponowne obliczenia. Rozproszonej transakcji
  KB+SQLite ani przeniesienia KB do bazy nie wprowadzamy (N01 C, N04 C odrzucone w przeglądzie).
- Windows (ADR-0022): `os.replace` jest atomowe, ale katalogu nie da się otworzyć do `fsync`.
- M-STAB1 pozwala na dwa równoległe `glu build` tej samej gry: akceptacje idą po kolei pod blokadą `kb/`.

## Decyzja
**1. Partia plików (`wgc.fsbatch`, wołane przez `wgc.kb` pod blokadą pisarza).** Akceptacja zmieniająca jeden plik
zostaje przy atomowej podmianie (`wgc.fsio`, ADR-0026). Gdy zmienia dwa pliki lub więcej, idzie przez dziennik
wycofania (undo log) w katalogu `kb/.wgc-batch/`:
1. **przygotowanie:** dla każdego pliku nowa treść `<n>.new` i, jeśli plik istnieje, kopia starej treści `<n>.old`,
   każda z `flush` i `fsync`. Awaria w tym kroku nie zmienia żadnego pliku `kb/`;
2. **manifest** `manifest.json` (`state: prepared`), zapisany atomowo (`fsio.atomic_write`). Zawiera:
   - `format: wgc-kb-batch@1`, losowy `id` partii, `job` i `state` (`prepared`, `rolling_back`, `committed`);
   - listę `files`: `path` względem repo gry, `old` (`sha256:<hex>` starej treści albo `null` dla nowego pliku),
     `new` (`sha256:<hex>` nowej treści), `staged` (`<n>.new`) i `backup` (`<n>.old` albo `null`).

   Format jest wewnętrzny (opis w tym ADR), nie jest kontraktem w `contracts/`. Recovery czyta też dzienniki
   `wgc-kb-batch@0` z pierwszej wersji M-STAB2: stany `prepared` i `committed`, hashe zapisane z podwójnym
   przedrostkiem `sha256:sha256:<hex>`, normalizowane przy odczycie. Stan `rolling_back` w formacie `@0` to
   `KBBatchConflict`. Format `@0` nie ma intencji wycofania, więc jego `prepared` z nową treścią każdego pliku nadal
   idzie naprzód (pierwotny błąd); dotyczy to tylko dzienników z niezacommitowanej pierwszej wersji M-STAB2;
3. **podmiany:** `os.replace(<n>.new → plik)` po kolei, z ponowieniami po `PermissionError` na Windows (ADR-0026);
4. **znacznik zatwierdzenia:** atomowa podmiana manifestu na `state: committed`. Od tego momentu partia jest
   zatwierdzona;
5. **sprzątanie:** usunięcie `kb/.wgc-batch/`. Pozostałość po przerwanym sprzątaniu usuwa recovery.

**Awaria w kroku 3 albo 4 wewnątrz `accept()`** (np. `PermissionError` po ponowieniach, `OSError` przy zapisie
znacznika): piszący najpierw zapisuje atomowo **intencję wycofania** (`state: rolling_back`), potem przywraca stare
treści procedurą recovery. Z `rolling_back` recovery nigdy nie idzie naprzód. Są trzy rozłączne wyniki:

| Wynik | Kiedy | `accept()` | GLU |
|---|---|---|---|
| **zatwierdzony** | znacznik `committed` zapisany | `AcceptResult` z `receipt` | Attempt `accepted`, `→ accepted → done`, receipt usuwany |
| **potwierdzone wycofanie** | stare treści przywrócone i dziennik usunięty | `KBWriteError` „partia wycofana, kb/ bez zmian” | Attempt `error`, `→ failed`, receipt usuwany |
| **nierozstrzygnięty** | wycofanie nie dokończone (także gdy intencja jest zapisana) albo nie da się usunąć dziennika | `KBUnresolved` (podklasa `KBError`): dziennik i receipt zostają | brak Attemptu, job zostaje w `validating`, build przerwany (wyjątek, kod 2); rozstrzyga reconcile |

Przy wyniku nierozstrzygniętym z zapisaną intencją kierunek jest już przesądzony (recovery wycofa partię), ale GLU nadal
nie zapisuje wyniku joba: decyzję podejmuje reconcile z `kb/` po recovery. Bez zapisanej intencji (zapis manifestu też
zawiódł) recovery wybiera kierunek z hashy (tabela niżej), a reconcile ocenia job tym samym receiptem. To wyjątek od
zdania ADR-0026 „w każdym przypadku job kończy się `validating → failed`”: przy `KBUnresolved` job czeka
w `validating`, dopóki recovery i reconcile nie rozstrzygną wyniku. Następny `glu build` nie wystartuje, jeśli recovery
na starcie nadal zawodzi (`KBError`, kod 2).

**2. Recovery (`wgc.kb.recover`, polecenie `wgc kb recover [--dry-run]`).** Decyzję podejmuje się z hashy plików,
nie z samego znacznika:

| Stan `kb/.wgc-batch/` | Działanie | Wynik |
|---|---|---|
| brak katalogu | nic (usuwa tylko osierocone `*.wgc-tmp` po zapisie pojedynczego pliku) | bez zmian |
| katalog bez manifestu (przerwane przygotowanie) | usunięcie katalogu | całość stara |
| `committed` | pliki z hashem `old` i obecnym `<n>.new` są podmieniane, potem sprzątanie | całość nowa |
| `rolling_back` | pliki z hashem `new` wracają z `<n>.old` (nowe pliki są usuwane), sprzątanie | całość stara |
| `prepared`, każdy plik ma już hash `new` (znacznik nie zdążył albo zginął) | sprzątanie | całość nowa |
| `prepared`, w pozostałych przypadkach | jak przy `rolling_back` | całość stara |
| plik ma hash ani `old`, ani `new` (edytor, `git checkout`, autocrlf) albo brakuje potrzebnej kopii | `KBBatchConflict` (podklasa `KBError`), niczego nie zmienia | decyzja człowieka |

- Recovery najpierw ustala plan dla wszystkich plików, potem go wykonuje. Jest idempotentne: drugi przebieg nie ma
  nic do zrobienia, a przerwane recovery (także wycofanie piszącego) dokańcza się, uruchamiając je ponownie. Stan
  manifestu się przy tym nie zmienia, a pliki już przywrócone albo dokończone mają docelowy hash. Bez katalogu partii i plików `*.wgc-tmp` nie bierze nawet blokady (nie tworzy `.glu/kb.lock`). `--dry-run` wypisuje plan i niczego nie zapisuje (nie tworzy też `.glu/kb.lock`).
- Recovery nie jest nowym źródłem treści `kb/`: tylko kończy albo wycofuje partię, którą zaczął `accept()`,
  bajtami z dziennika zapisanego przez `accept()`. `accept()` pozostaje jedyną drogą, którą nowa treść trafia do
  `kb/` (ADR-0025).
- Recovery działa pod blokadą pisarza. `accept()` wywołuje je na początku sekcji krytycznej, więc nigdy nie scala
  wyniku z częściową `kb/`. Nierozstrzygnięty konflikt to `KBBatchConflict`, czyli Attempt `error` w GLU.
- **Dziennik leży w `kb/`, a nie w `.glu/`.** Utrata `.glu/` w trakcie partii nie może zostawić częściowej `kb/` bez
  śladu (ADR-0004). `kb/.wgc-batch/` jest widoczny w `git status` tylko po przerwanej partii. Repo gry **nie
  ignoruje** go w git (decyzja właściciela 2026-10-06, Q-18): `git clean -fdX` go nie usunie, a ewentualny commit po
  awarii zgłosi `wgc validate` (`kb_batch_pending`). Nazwy plików partii nie
  kończą się na `.yaml`, więc nie są czytane jako KB.
- **`wgc validate`** zgłasza błąd `kb_batch_pending`, gdy manifest partii leży w odpowiednim `kb/`: w podanym
  katalogu, w katalogu `kb` nadrzędnym (walidacja `kb/logic` albo pojedynczego pliku `kb/`) albo w katalogu `kb` pod
  podanym katalogiem.
- **Spójny odczyt: wspólna blokada z pisarzem.** Sam hash treści tego nie gwarantuje. Partie nowa → stara → nowa
  między odczytami a kontrolami przywracają identyczne bajty (problem ABA), a porównanie przepuszcza wtedy stary
  pierwszy plik z nowym drugim. Dlatego walidator:
  - na czas całego odczytu trzyma blokadę pisarza `<repo>/.glu/kb.lock` każdego odpowiedniego `kb/`, której plik
    istnieje. Tę samą blokadę biorą `accept()` i recovery, więc żaden z nich nie zmieni `kb/` w trakcie odczytu. Wzięcie
    blokady systemowej na istniejącym pliku niczego nie zapisuje, a brakującego pliku blokady walidator nie tworzy;
  - w repo bez pliku blokady korzysta z tego, że każdy pisarz tworzy go przed pierwszą zmianą i nikt go nie usuwa.
    Plik, którego nie było przed odczytem, a jest po nim, oznacza, że mógł zacząć się pierwszy zapis. Wtedy walidator
    czyta ponownie, już pod tą blokadą;
  - dodatkowo, dla zmian spoza blokady (edytor, git), po odczycie sprawdza, że nie pojawił się manifest, zbiór plików
    jest ten sam, a każdy plik ma przeczytane bajty.

  Przy niepowodzeniu czyta ponownie (do 5 prób), potem zgłasza `kb_read_unstable`. Tak samo, gdy blokada jest zajęta
  dłużej niż 60 s. Gwarancja obejmuje pisarzy, którzy biorą blokadę (`accept()`, recovery). Zmiana spoza blokady,
  która między kontrolami przywraca identyczne bajty, pozostaje niewykrywalna (blokada jest doradcza, ADR-0026).
  Walidacja czeka na trwający `accept()` i odwrotnie. Częściowa `kb/` nigdy nie przechodzi walidacji jako poprawna.

**3. Receipt akceptacji.** Po walidacji, a przed zapisem plików, `accept()` z podanym `job` zapisuje receipt
`.glu/kb-receipts/<job>.json` (atomowo). Ten sam receipt wraca w `AcceptResult.receipt` i trafia do Attemptu jako
`kb_receipt`. Zawiera:
- `generation`: `content_hash` listy par (ścieżka pliku `kb/`, `sha256:<hex>` jego bajtów) po akceptacji, czyli
  generacja `kb/`. Receipty z pierwszej wersji M-STAB2 liczyły składniki z podwójnym przedrostkiem, więc ich
  `generation` różni się od obecnej dla tego samego `kb/`. `check_receipt` nie porównuje `generation`, więc nic się
  nie psuje;
- `records`: ID każdego zaproponowanego rekordu → `content_hash` rekordu w `kb/` po akceptacji (także rekordu bez
  zmian).

Receipt opisuje zamiar. Dowodem jest dopiero zgodność z `kb/`: `wgc.kb.check_receipt` porównuje `records` z bieżącym
`kb/` pod blokadą, po recovery. GLU usuwa receipt po zapisie Attemptu, a reconcile usuwa osierocone.

**4. Końcowe wpisy store w jednej transakcji.** `Store.finish_job` zapisuje Attempt i przejścia joba (`validating →
accepted → done` albo `→ failed`) w jednej transakcji SQLite. Przerwanie zostawia job w stanie sprzed tych wpisów,
nigdy z Attemptem bez przejścia.

**5. Reconcile (`glu.reconcile`, polecenie `glu reconcile [--dry-run]`, krok startu `glu build`).**
- **Żywotność buildu:** `glu.exec.run` przez cały build trzyma blokadę systemową `.glu/builds/<build>.lock`
  (`fsio.exclusive`). Reconcile dotyka tylko buildów niezakończonych, których blokadę da się wziąć od razu. Po awarii
  procesu system zwalnia blokadę, więc nie ma heurystyk wieku. Start buildu (reconcile i utworzenie buildu z jego
  blokadą) wykonuje się pod krótką blokadą `.glu/build.lock`, żeby reconcile nie uznał za martwy buildu, który
  właśnie powstaje.
- **Kolejność:** najpierw recovery `kb/` (wgc), potem joby martwego buildu (żadna nowa krawędź tabeli przejść):

| Stan joba | Działanie |
|---|---|
| `validating` z receiptem zgodnym z `kb/` | Attempt `accepted` z `kb_receipt`, `validating → accepted → done` (`accepted_records` z receiptu) |
| `validating` z receiptem niezgodnym albo bez receiptu | Attempt `error` (`runtime`), `validating → failed`, powód „reconcile: …” |
| `running` | Attempt `error` (`runtime`), `running → failed` |
| `accepted` | `accepted → done` |
| `pending`, `ready`, `proposed` i pozostałe aktywne | `→ cancelled` |

  Potem build: `done`, gdy każdy job jest `done`, inaczej `failed`, z `metrics` z liczby jobów. Każdy job jest
  uzgadniany jedną transakcją (`finish_job`).
- `glu reconcile` bierze tę samą blokadę startu co `glu build`. Zajęta dłużej niż 60 s daje błąd operacyjny (kod 2).
- `--dry-run` wypisuje plan bez zapisu: nie tworzy `.glu/`, bazy ani plików blokad. `glu build --dry-run` nie wykonuje
  reconcile.
- Reconcile zależy od `wgc` (recovery, receipt), a `wgc` nie importuje `glu` (ADR-0002). Plików `kb/` dotyka tylko
  `wgc`.

**6. Kontrakt.** `glu/exec@0` dostaje opcjonalne pole Attemptu `kb_receipt: {generation, records}` (zmiana
addytywna w `@0`, bez migracji bazy: rekordy leżą w `body`, ADR-0023).

## Konsekwencje
- Przerwanie procesu w dowolnym punkcie akceptacji, wycofania piszącego albo recovery kończy się po (ponownym)
  recovery `kb/` w całości starą albo w całości nową, przechodzącą `wgc validate`. Testowane przez `os._exit`
  w procesie potomnym.
- Potwierdzone wycofanie, zatwierdzenie i wynik nierozstrzygnięty mają różne skutki w GLU (tabela wyżej). Dowód
  (receipt, dziennik) nie jest usuwany przed rozstrzygnięciem.
- Job nie zostaje w `validating` po awarii między zapisem KB a zapisem Attemptu: reconcile kończy go `done`, gdy
  `kb/` ma jego wynik, albo `failed`.
- Koszt: partia ≥ 2 plików zapisuje każdy plik dwa razy (kopia, nowa treść) plus dwa zapisy manifestu. Pliki `kb/`
  są małe. Receipt to jeden mały plik na job w `.glu/`.
- **Granice gwarancji:**
  - **Windows bez `fsync` katalogu:** podmiany plików i znacznika są atomowe względem awarii procesu, ale ich
    trwałość po odcięciu zasilania nie jest wymuszona. Spójność (całość stara albo całość nowa) zależy wtedy od
    tego, że NTFS utrwala operacje na metadanych w kolejności dziennika. Tego nie testujemy. Jeśli zginie znacznik,
    a zostaną podmiany, recovery uzna partię za zatwierdzoną (wszystkie pliki mają `new`). Jeśli zginą też podmiany,
    wróci stan stary. SQLite robi `fsync`, więc Attempt `accepted` może przetrwać utratę zmian `kb/`. Reconcile tego
    nie wykryje (job jest zakończony). Rozbieżność pokazuje porównanie `kb_receipt` z `kb/`, a naprawia ją ponowny
    build;
  - **POSIX:** po każdej podmianie wykonuje się `fsync` katalogu. Gałąź nie była uruchamiana (jak w ADR-0026);
  - **czytelnicy bez blokady** (`wgc validate`, planner, edytor) mogą zobaczyć stan w trakcie partii. `wgc validate`
    zgłosi wtedy `kb_batch_pending`;
  - **ręczna zmiana pliku partii przed recovery** daje `KBBatchConflict`, a nie zgadywanie;
  - **receipt po utracie `.glu/`** znika razem z bazą stanu, więc nie ma czego uzgadniać. `kb/` pozostaje prawdą;
  - **receipt dowodzi zgodności, nie autorstwa:** rekord identyczny z innego joba też go spełni. Wystarcza to do
    uzgodnienia stanu.
- Reconcile kończy przerwany build `failed` albo `done`. Wznowienie przerwanych jobów to nadal nowy build (ADR-0023).

## Odrzucone warianty
- **Dziennik w `.glu/`:** utrata `.glu/` w trakcie partii zostawiłaby częściową `kb/` bez śladu, a `wgc validate`
  mogłoby ją uznać za poprawną.
- **Dziennik ponawiania (znacznik przed podmianami):** awaria podmiany w żywym procesie wymagałaby dokończenia
  partii przez recovery po tym, jak GLU zapisał już Attempt `error`. Zakończony job przeczyłby wtedy `kb/`. Dziennik
  wycofania pozwala wycofać partię od razu.
- **Partia także dla jednego pliku:** dodatkowe zapisy bez zysku, bo atomowa podmiana wystarcza.
- **Dowód z samego `kb/` (`prov.job`) zamiast receiptu:** rekordy bez zmian zachowują `prov.job` wcześniejszego joba,
  więc akceptacji bez zmian nie dałoby się potwierdzić, a `accepted_records` byłoby niepełne.
- **Receipt zapisywany po plikach `kb/`:** awaria pomiędzy zostawiłaby wynik w `kb/` bez dowodu. Receipt przed zapisem
  plus kontrola zgodności obejmuje oba przypadki.
- **Reconcile bez blokady żywotności:** zakończyłby joby równoległego, żywego buildu.
- **Rozproszona transakcja KB+SQLite albo KB w bazie:** zmienia źródło prawdy (ADR-0004).
