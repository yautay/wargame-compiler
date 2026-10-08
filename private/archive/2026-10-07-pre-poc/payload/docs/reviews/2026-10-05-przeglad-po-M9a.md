# Przegląd architektury i implementacji po M9a

Data: 2026-10-05. Rola: niezależny Architecture Model / Premium Reviewer. Punkt odniesienia: `96ded88` (M9a). Przegląd nie wprowadza zmian implementacji ani decyzji właściciela. „Fakt” oznacza obserwację kodu, dokumentu lub wykonanego scenariusza; „ocena” i „rekomendacja” oznaczają wniosek recenzenta. Numery linii odnoszą się do tego punktu odniesienia.

## 1. Werdykt

Kierunek jest dobry: podział WGC / GLU / igw, jawny Rule IR, KB jako źródło prawdy oraz brak automatycznego premium przy awarii LAN ograniczają istotne ryzyka projektu. Najmocniejszy jest działający pion deterministyczny od źródła do walidowanego, idempotentnego zapisu tabeli oraz rozdzielenie provenance od deklaracji wykonawcy. M0–M9a nie dowodzą jeszcze osiągnięcia jakości, przyrostowości ani kosztu premium ≤ 2× baseline: nie ma pomiaru baseline, gold ani wykonanego routingu modelowego. Największe obecne zagrożenia to utrata danych podczas zapisu KB, niespójne hashe wejść oraz kontrakt akceptacji, który nie obsłuży niejasności i dalszych etapów bez zmiany. Zalecam krótki etap naprawy granicy akceptacji i wcześniejszy przebieg domenowy z fake/replay, a następnie pomiary na fragmencie prawdziwej gry przed rozbudową infrastruktury i zamrożeniem `logic@1`.

### Podstawa oceny i wykonane kontrole

Przeczytano bootstrap, dokumenty wskazane w zleceniu, całą [ROADMAP](../ROADMAP.md), ADR-0001–0025, schematy i fixture'y, implementację WGC/GLU, testy, minigrę oraz historię i handoffy M0–M9a. [NODE](../inference/NODE.md) potraktowano jako przegląd projektu, bez weryfikacji zewnętrznych deklaracji o runtime'ach. Nie używano sieci ani modeli; nie instalowano zależności.

Kontrole wykonano na Windows, Python 3.13.1, pytest 8.1.1, przy użyciu już zainstalowanych zależności. Python w sandboxie nie widział `pytest` i `yaml`; po udostępnieniu istniejącego środowiska użytkownika polecenia wykonano bez instalacji. Pierwsze nieudane uruchomienia były problemem środowiska, nie wynikiem testów projektu.

| Kontrola | Wynik |
|---|---|
| `python -m pytest` | **424 passed**, 23,98 s |
| `python -m wgc validate contracts/fixtures/valid` | **OK**, files=6, records=90, errors=0, warnings=0 |
| `python -m wgc source extract --root <kopia>` | 31 segmentów, bez zmian treści |
| `python -m glu build --root <kopia> --stage 1 --dry-run` | 1 job parsowania tabeli; całe drzewo kopii identyczne bajtowo, brak `state.db` |
| `python -m glu build --root <kopia> --stage 1` | build `done`, 1 job `done`, nowy `TAB-4.3` |
| Ponowne identyczne polecenie build | build `done`, unchanged=1, KB identyczne bajtowo |
| `python -m glu status --root <kopia>` | oba buildy `done`, każdy z jednym ukończonym jobem |
| `python -m glu export --root <kopia> --out <eksport>` | 6 rekordów wykonania: 2 buildy, 2 joby, 2 próby |
| `python -m wgc validate <kopia>/source <kopia>/kb` | **OK**, files=2, records=34, errors=0, warnings=0 |
| `python -m wgc validate <eksport>` | **OK**, files=1, errors=0, warnings=0; licznik rekordów domenowych 0 nie oznacza pustego eksportu |

Kopia pochodziła z `bench/minigame`, bez `.glu/` i `kb/`, w katalogu tymczasowym `wgc-review-M9a-zq2ffyz5/live`. Wszystkie polecenia CLI powyżej zakończyły się kodem 0. Ponowny build sprawdza idempotencję zapisu, **nie trafienie cache**: planner nadal uruchamia każde zadanie (`glu/planner.py:5`). Pozostałe eksperymenty wykonano w osobnych katalogach tymczasowych; poniżej opisano dane wejściowe, ingerencję i obserwowany wynik. Nie dodano testów ani skryptów do repo.

## 2. Ustalenia, od najpoważniejszych

### F01 — Zapis KB może zniszczyć istniejący plik i zatwierdzić tylko część wyniku

- **Poziom / obszar:** krytyczne / trwałość źródła prawdy.
- **Dowód — fakt:** `wgc/kb.py:335` zapisuje zmienione pliki kolejno; `wgc/kb.py:380` otwiera docelowy plik przez `open("w")`, czyli go obcina przed ukończeniem zapisu. W scenariuszu P7 umieszczono dwie zaakceptowane tabele w dwóch plikach logicznych, zaproponowano zmianę obu i podmieniono `_write_file`: pierwszy zapis działał, drugi obcinał plik i zgłaszał `OSError`. Po wyjątku pierwszy plik zawierał nową wersję (726 bajtów), drugi miał **0 bajtów**. Walidacja całego kandydata przed zapisem tego nie zapobiega.
- **Skutek — ocena:** pojedynczy `accept()` może zostawić utracone dane oraz KB, której żadna pełna wersja nie przeszła walidacji. Git pomaga tylko wtedy, gdy poprzedni stan był zapisany w historii.
- **Rekomendacja:** najpierw zapis pliku tymczasowego w tym samym katalogu, flush i atomowa podmiana; osobno protokół zatwierdzenia całej partii plików z manifestem i odzyskiwaniem po przerwaniu. Atomowość pojedynczego pliku nie daje atomowości wielu plików. Przed M10 testy awarii przed podmianą i między podmianami.
- **ADR:** tak, granica transakcji KB i zasady recovery; samo zastąpienie `open("w")` nie wymaga osobnego ADR. Decyzja N01.

### F02 — Dwie poprawne akceptacje mogą zgubić jeden wynik

- **Poziom / obszar:** krytyczne / współbieżność i izolacja.
- **Dowód — fakt:** odczyt i merge w `wgc/kb.py:292` oraz zapis w `wgc/kb.py:341` nie mają blokady ani kontroli wersji. W P15 dwa wątki proponowały `TAB-a` i `TAB-b` do początkowo pustego KB. Bariera przy `_write_file` zapewniła, że oba najpierw odczytały i zwalidowały stary stan; zapis A wykonano przed B. **Oba `AcceptResult.ok=True`, na dysku tylko `TAB-b`.** To kontrolowany scenariusz dwóch wywołań API, nie pomiar równoległego CLI.
- **Skutek — ocena:** już dwa procesy budowania tej samej gry są niebezpieczne; przyszły MCP i równoległe joby zwiększą ryzyko. Transakcja SQLite w `glu/store.py:206` chroni bazę wykonania, nie pliki KB; WAL nie rozwiąże tego problemu.
- **Rekomendacja:** jeden pisarz projektu obejmujący cały odczyt–merge–walidację–commit, z kontrolą generacji KB i źródeł. Obliczenia mogą być równoległe, akceptacje powinny przechodzić przez kolejkę albo lease z porównaniem wersji. Sam lock wokół `_write_file` jest za późny.
- **ADR:** tak, polityka jednego pisarza i konflikty generacji. N02.

### F03 — Ten sam hash i klucz joba mogą oznaczać różne komórki tabeli

- **Poziom / obszar:** krytyczne / integralność Stage 0 i przyszły cache.
- **Dowód — fakt:** `wgc/canonical.py:95` normalizuje wszystkie białe znaki; `wgc/tables.py:71` interpretuje tabulator strukturalnie. W P1 po ekstrakcji zmieniono w cache segmentu 4.3 `4 or less\tNo effect` na `4\tor less No effect`. `text_hash` i `planner.cache_key` pozostały identyczne, `source.verify(...).ok=True`, lecz pierwszy wiersz parsował się odpowiednio jako `[{min: null, max: 4}, "No effect"]` oraz `[4, "or less No effect"]`. [ADR-0024](../adr/ADR-0024-separator-komorek-tabel-w-tekscie-segmentu.md) zachowuje wersję i hash mimo zmiany reprezentacji komórek.
- **Skutek — ocena:** to więcej niż znany cache ze starym separatorem. Błędne granice komórek przechodzą kontrolę integralności; M11 może zwrócić semantycznie inny wynik pod tym samym kluczem. Cache M11 jeszcze nie istnieje, więc nie wykazano rzeczywistego trafienia błędnego cache.
- **Rekomendacja:** zachować normalizowany hash tekstu do porównywania przepływu tekstu, ale dodać hash struktury tabeli lub dokładnego, wersjonowanego artefaktu ekstrakcji. Parser, planner, provenance i verify muszą używać właściwego hasha. Zmienić wersję ekstraktora/formatu; jawnie regenerować poprzednie artefakty.
- **ADR:** tak, zastąpienie ADR-0024 i rozszerzenie semantyki hashy. N03.

### F04 — Utrwalone przejścia stanów nie zapewniają wznowienia

- **Poziom / obszar:** ważne / executor i recovery.
- **Dowód — fakt:** `glu/exec.py:58` zapisuje KB, a dopiero `glu/exec.py:71` dodaje accepted attempt i kończy job. W P8 `Store.add_attempt` zgłaszał `StoreError` po udanym `accept()`: KB istniała, build pozostał `running`, job `validating`, brak attempts. Następny zwykły build zakończył się poprawnie dzięki idempotencji, lecz stary build/job nadal pozostały w tych stanach. `glu/exec.py:81` zawsze tworzy nowy build; CLI ma build/status/export, bez resume.
- **Skutek — ocena:** dziennik jest użyteczny diagnostycznie, ale po awarii nie mówi wiarygodnie, czy wynik został zatwierdzony. Retry całego buildu nie jest wznowieniem starego joba.
- **Rekomendacja:** utrwalić propozycję i wynik walidacji przed commit; zapisać receipt/generację zatwierdzenia i dodać reconcile/recovery. Powiązane końcowe operacje store wykonać jedną transakcją; szczelinę między YAML a SQLite rozwiązać jawnym protokołem odzyskiwania. KB pozostaje prawdą także po utracie `.glu/` (ADR-0004).
- **ADR:** tak, rozszerzenie ADR-0023/0025. N04. `validating → failed` jest dziś dopuszczalnym, udokumentowanym wyborem Tier 0: attempt zachowuje `rejected` (`glu/exec.py:68`). Dla pętli M10 warto rozróżniać odrzucony wynik od awarii wykonania; samo użycie `failed` nie jest wykazaną utratą danych.

### F05 — `prov.inputs_hash` i hash wejścia joba mają różne definicje

- **Poziom / obszar:** ważne / provenance, stale i TaskSpec.
- **Dowód — fakt:** `wgc/tasks.py:60` używa deklarowanej `semantic_projection`, planner bierze ten hash (`glu/planner.py:39`). Natomiast `_provenance` nie otrzymuje `spec` ani `inputs`: liczy hash kotwic i `derived_from` przy użyciu projekcji `logic` (`wgc/kb.py:210`, `227`, `252`). W P3 własna projekcja zadania zwracała `[{table_cells: [1, 2]}]`; tabela została zaakceptowana, ale `prov.inputs_hash != spec.input_hash(...)`. P11 dodatkowo pokazał, że zmiana roli dokumentu `rules → errata` nie zmienia klucza joba, chociaż zmienia ID tabeli (`wgc/tables.py:66`) i rodzaj provenance (`wgc/kb.py:226`).
- **Skutek — ocena:** obecna zgodność dla jednej tabeli z jednej kotwicy jest przypadkiem szczególnym. Zadania modelowe mogą czytać kontekst niewymieniony w dowodach rekordu; po utracie `.glu/` sam hash nie wystarczy do odtworzenia ich zależności.
- **Rekomendacja:** rozdzielić dowody pojedynczego rekordu od manifestu całego wywołania. Manifest powinien zawierać task/version, projection/version, wejścia i kontekst z hashami oraz dane autorytetu źródeł użyte przez zadanie. Tier 0 może mieć pusty context/dependency_state **tylko jeśli** cały odczyt semantyczny jest w input_hash. Nie trzeba dodawać pustych pól dla samej kompletności kontraktu. Dla cache wyników wersjonować też schematy i politykę walidacji; trafienie nie zwalnia z aktualnej kontroli bramek.
- **ADR:** tak, definicja hashy i odtwarzalnego manifestu. N05.

### F06 — Projekcje pomijają treść normatywną niepełnego IR i część rodzajów rekordów

- **Poziom / obszar:** ważne / przyrostowość Rule IR.
- **Dowód — fakt:** projekcje rule w `wgc/canonical.py:26` nie obejmują `unformalized` ani `statement`; projekcja concept/digital pomija `definition` i `defined_by` (`wgc/canonical.py:34`). W P4 dla reguły `formalization: none` lub `partial` zmieniono zakaz i opis nieformalizowanej części: hashe logic/digital/publication zostały takie same. Rejestr projekcji ma tylko segment/rule/concept/relation; domyślne `TaskSpec.projections()` dla table/procedure/ambiguity/case/change lub rekordów digital zgłosi `KeyError` (`wgc/canonical.py:113`). Fallback w provenance jest inną, niewersjonowaną projekcją (`wgc/kb.py:237`).
- **Skutek — ocena:** oddzielenie glosy od formalnego IR jest słuszne dla kompletnego IR, ale przy niepełnym IR odrzucona glosa opisuje jeszcze znaczenie. Zmiana znaczenia predykatu również może nie unieważnić digitalizacji. Rekordy jako wejścia są wspierane typem `Inputs`, ale nie kompletną polityką projekcji.
- **Rekomendacja:** warunkowo uwzględniać nieformalizowaną treść; dla predykatów uwzględnić definicję lub jawne zależności do definiujących reguł. Zdefiniować projekcje dla rodzajów rzeczywiście używanych w M10–M14 i E2E, podbić wersję, sprawdzić mutacje znaczenia. Normalizację przemiennych `all/any` uzgodnić osobno: obecna kolejność list może generować zbędne missy i rozbieżności, nie wykazano przez nią błędnego trafienia.
- **ADR:** tak, korekta semantyki projekcji; nie zmienia zasady Rule IR niezależnego od języka. N06.

### F07 — Jeden status i jeden schemat akceptacji nie obsłużą M10–M14 ani Stage 1.5

- **Poziom / obszar:** ważne / granica propozycja–rekord.
- **Dowód — fakt:** status jest polem zastrzeżonym, następnie zawsze staje się `accepted` (`wgc/kb.py:192`, `280`). Tymczasem ambiguity wymaga statusu `open|requires_human_interpretation|resolved|house_rule|wont_fix` (`contracts/schemas/logic.schema.json:220`, `231`). W P2 prawidłowa merytorycznie propozycja ambiguity z dwiema readings została odrzucona właśnie przez `status: accepted`. Przyjęta interpretation wymaga `prov.decision` (`logic.schema.json:250`), którego obecny envelope i `_provenance` nie potrafią nadać. `accept()` zawsze waliduje `LOGIC` i zapisuje pod `kb/logic` (`wgc/kb.py:281`, `311`), niezależnie od deklarowanego `output_schema`.
- **Skutek — ocena:** TaskSpec jest dobrym punktem rozszerzenia, ale opcjonalne context_builder/prompt/decoding_schema nie czynią aktualnego accept gotowym na modelowe zadania i pion z `LEG-`. Status akceptacji jest pomieszany ze stanem rozstrzygnięcia niejasności.
- **Rekomendacja:** jawny schemat envelope propozycji, dispatch kontraktu etapu i polityka akceptacji dla rodzaju rekordu; oddzielić lifecycle od resolution. WGC nadal nadaje provenance i sprawdza HD, model jedynie proponuje treść. Homogeniczna lista wielu rekordów może pozostać; mieszane rodzaje wymagają świadomie zaprojektowanej partii lub kilku zależnych zadań, nie są konieczne w każdym jobie.
- **ADR:** tak, zmiana kontraktu ADR-0025 i zasad statusów. N07.

Rozbieżność ADR-0014/0025 dotycząca błędnych kotwic jest świadomym ograniczeniem M9a: ADR-0025 wprost odkłada modelowe obniżenie do `llm_inference` na M10; odrzucenie kotwicy w Tier 0 jest poprawne, bo ten tier nie może deklarować inferencji LLM. Rekomenduję w M10 reject/retry dla niepotwierdzonego cytatu, a inferencję dopuścić osobną, jawną polityką zadania z poprawnym `derived_from`, zamiast automatycznie legalizować błędny cytat zmianą provenance. Samo występowanie cytatu nie dowodzi, że modelowa parafraza wynika ze źródła: tę jakość musi sprawdzić walidacja/review. To decyzja polityki akceptacji N07, wymagająca uzgodnienia obu ADR, nie dodatkowy błąd Tier 0.

### F08 — Błędne typy propozycji omijają diagnostykę i przerywają build

- **Poziom / obszar:** ważne / wejście modelu i izolacja błędów.
- **Dowód — fakt:** w P10 `record.id=[]` zgłaszał `TypeError: unhashable type: list` przy `wgc/kb.py:195`; `anchor.quote=123` zgłaszał `TypeError` przy `wgc/kb.py:221`. `spec.validate` działa przed walidacją schematu rekordu (`wgc/kb.py:271`), a executor łapie w fazie akceptacji tylko `KBError` (`glu/exec.py:60`), nie te błędy ani `OSError` zapisu.
- **Skutek — ocena:** błędny structured output może przerwać cały build i zostawić `validating`, zamiast dać użyteczną listę błędów do naprawy. Gramatyka dekodowania nie zastąpi pełnego schematu, co już rozpoznaje STATUS.
- **Rekomendacja:** pełna walidacja kształtu envelope/rekordu przed funkcjami domenowymi i provenance; type guards dla ID, cytatu i span. Rozróżnić błędy danych od błędów programu oraz awarii I/O; te ostatnie kierować przez recovery. Nie maskować wszystkich wyjątków jako „model podał zły JSON”.
- **ADR:** nie dla type guards; projekt envelope należy do N07. N08.

### F09 — Źródło społecznościowe może zostać automatycznie kanoniczne (Q-13)

- **Poziom / obszar:** ważne / autorytet źródeł.
- **Dowód — fakt:** `wgc/kb.py:226` dla nieznanej roli daje `explicit_source`. W P5 rolę dokumentu minigry zmieniono na `community_interpretation`, po czym zwykłe parsowanie i accept zwróciły **ok=True, status=accepted, prov.kind=explicit_source**. Jest to sprzeczne z `docs/LOGIC-MODEL.md:37`: „nigdy nie jest źródłem kanonicznym sama w sobie”, wymaga HD. Q-13 jest już jawnie otwarte w STATUS, więc nie jest to zatajenie ryzyka.
- **Skutek — ocena:** źródło z dowodem tekstowym niekoniecznie jest źródłem autorytatywnym. Przypisanie innego rodzaju provenance bez kontroli akceptacji również nie rozwiąże problemu.
- **Rekomendacja:** już przed pierwszym zadaniem modelowym odrzucać automatyczne kanoniczne akceptacje z `community_interpretation` i `prior_translation`; zachować możliwość użycia jako dowodu dla HD. Lista dopuszczonych ról ma być jawna, bez permissive fallback. Oddzielić pochodzenie, autorytet oraz pierwszeństwo; samo precedence nie rozstrzyga konfliktu bez CHG/REL.
- **ADR:** tak, rozstrzygnięcie Q-13 uzupełniające ADR-0014/0025.

### F10 — Przenumerowanie blokuje regenerację, a ID etykietowe nie są trwałą tożsamością (Q-12)

- **Poziom / obszar:** ważne / tożsamość i invalidacja.
- **Dowód — fakt:** w P6 najpierw zbudowano TAB-4.3, potem w źródle zmieniono `**4.3**` na `**4.8**` i wykonano extract. Próba accept nowej tabeli została odrzucona: `unresolved_ref TAB-4.3`, brak starego `SEG-dsk.4.3`. Przyczyną jest walidacja całego KB (`wgc/kb.py:326`). Segmenty tworzy się z etykiet (`wgc/source.py:90`), a `u1/u2` zależą od kolejności (ADR-0020). Ponadto `table_id` dla **każdego** dokumentu roli rules daje `TAB-<label>` (`wgc/tables.py:66`): dwie różne księgi rules z tabelą 4.3 mają to samo ID; ten przypadek wynika wprost z funkcji, nie uruchamiano dwóch takich pełnych buildów.
- **Skutek — ocena:** errata w osobnym dokumencie bywa poprawnie nazwowana, lecz przenumerowanie wewnątrz księgi zmienia tożsamość i blokuje naprawę. Zmiana etykiety nie dowodzi zmiany reguły, a ta sama etykieta nie dowodzi tej samej reguły. Nowe wydanie w osobnym repo nie rozwiązuje mapowania między wydaniami.
- **Rekomendacja:** trwałe logiczne ID, czytelna etykieta jako atrybut/alias, namespace dokumentu i jawna mapa przenumerowania/wydań. `uN` pozostawić tymczasowe, bez trwałych kotwic do reguł, dopóki nie ma uzgadniania tożsamości. CON-snake_case traktować jako czytelną nazwę nadaną raz z aliasami, nie ID regenerowane z aktualnego terminu; parser ID sam nie egzekwuje tej konwencji. Rozdzielić niepoprawny schemat/dangling ref od rozpoznanego stale po zmianie źródeł; stale nie przechodzi bramek, ale nie blokuje naprawy swojego podgrafu. Nie obniżać wszystkich `unresolved_ref` do ostrzeżeń.
- **ADR:** tak, Q-12 oraz trwała tożsamość N09. Rozstrzygnięcie potrzebne przed pierwszą regeneracją zmienionych źródeł, wcześniej niż pełny M13.

### F11 — Idempotencja pojedynczych rekordów nie uzgadnia zbioru wyników producenta

- **Poziom / obszar:** ważne / ownership i wiele rekordów z joba.
- **Dowód — fakt:** w P9 przyjęto dwie tabele z jednego wywołania, a następnie propozycję zawierającą tylko pierwszą. **Obie pozostały accepted**; pusta lista również może zakończyć accept powodzeniem. Kod merge aktualizuje wyłącznie obecne propozycje (`wgc/kb.py:295`). Producent jest porównywany po tool/prompt bez wersji (`wgc/kb.py:170`), a nie po zakresie wejść. W P16 drugi concept miał `derived_from` do pierwszego concept z tej samej partii: accept go nie znalazł, bo `_provenance` czyta jeszcze stare Workspace (`wgc/kb.py:231`).
- **Skutek — ocena:** usunięty atom reguły może pozostawać kanoniczny; ten sam task działający na innym źródle może nadpisać kolidujące ID. Wielorekordowy output działa dla niezależnych rekordów, ale nie dla ich pochodzenia wewnątrz partii.
- **Rekomendacja:** stabilny klucz ownership `task + logiczny zakres wejścia`, manifest poprzedniego zbioru outputów, jawne wycofanie brakujących rekordów i ochrona HD/ręcznych zmian. Versionless producent może pozostać identyfikatorem rodziny zadania, jeżeli migracja wersji jest jawna i ponownie walidowana. Dowody zależności wewnątrz partii liczyć na kandydacie z kontrolą cykli, nie na wyłącznie starej KB. Usunięcie samej wersji z porównania nie jest samodzielnie błędem.
- **ADR:** tak, ownership i semantyka partii. N10.

### F12 — Zielona walidacja @0 nie dowodzi kompletnej ani wykonalnej semantyki (Q-09)

- **Poziom / obszar:** ważne / kontrakty i L2.
- **Dowód — fakt:** w P12 w poprawnym zestawie fixture'ów zmieniono R-3.4 na `conditions: {pred: CON-missing}`, `effects: [{op: set}]`, `formalization: full`. `validate_documents` zwrócił **ok=True, brak diagnostyk**. Efekt wymaga tylko `op` (`contracts/schemas/logic.schema.json:63`), a aktualny zakres odsyłaczy nie obejmuje wszystkich zagnieżdżonych wyrażeń (`docs/DATA-CONTRACTS.md:167`). M1 deklaruje L0/L1, M5 planuje L2: to luka do kolejnych etapów, nie dowód niewykonania całego zadeklarowanego M1.
- **Skutek — ocena:** „schema valid” i „accepted” nie mogą być utożsamiane z poprawnością reguły. Formalization full może dziś obiecywać więcej niż struktura i walidator zapewniają.
- **Rekomendacja przed `logic@1`:** rekurencyjne referencje i typy celów, związanie zmiennych i sygnatury predykatów, operatory z wymaganymi operandami, zgodność nature/modality, ograniczenia formalization i tekstowych luk, zakresy/kompletność tabel, cykle priorytetów oraz rozstrzygnięcia AMB/INT/HD. `common` wymaga doprecyzowania pełnych SHA-256 dla produkcji (obecny wzorzec dopuszcza 16–64 hex), kolejności span i spójności quote/span oraz wymagania manifestu dla generowanych rekordów. Walidator `Draft202012Validator` bez FormatChecker (`wgc/contracts.py:48`) nie sprawdza automatycznie formatów dat.
- **ADR:** tak dla definicji full i polityki L2; same dodatkowe kontrole zadeklarowanych referencji realizują Q-09 i nie potrzebują osobnego ADR.

Dodatkowy przegląd kontraktów: `source@0` potrzebuje tożsamości i hashów z F03/F10/F13; `glu/exec@0` potrzebuje recovery, ownership i znaczenia wyników walidacji z F04/F11. `digital@0` i `gate@0` są użytecznymi szkicami, ale E2E musi ustalić minimalny dispatch zapisu, provenance i `LEG.then.verdict` (zmiana już planowana w M18), a gate musi jawnie podać zakres, stan i wersję walidatorów. `igw/api@0` słusznie nie zawiera domeny i wymaga fingerprintu wyniku; M10/M-GW1 powinny sprawdzać zgodność z oczekiwanym fingerprintem, odrzucać przerwane wyjście nawet przy poprawnym JSON oraz określić deduplikację idempotency key względem klienta, profilu i payloadu. Są to wymagania do nieistniejących jeszcze implementacji, nie błędy zaobserwowane w działającej bramce. Nie zamrażać wszystkich tych kontraktów jednocześnie z `logic@1`.

### F13 — PDF minigry nie sprawdza gotowości na prawdziwą księgę (Q-11)

- **Poziom / obszar:** ważne / Stage 0.
- **Dowód — fakt:** [ADR-0021](../adr/ADR-0021-ingest-pdf-biblioteka-i-segmentacja.md) ogranicza ekstrakcję do jednej kolumny i określonej segmentacji; STATUS jawnie wymienia kolumny, nagłówki/stopki i image_only jako Q-11. `tests/pdfgen.py:82` tworzy drukowaną wersję minigry zgodną z tym formatem; używa też `wgc.ingest.markdown.inline_text` (`tests/pdfgen.py:12`). Dodatkowo `verified_by_render` jest unieważniane tylko po zmianie text_hash (`wgc/source.py:264`), a projekcja segmentu pomija flags/bbox (`wgc/canonical.py:24`). Verify porównuje hashe tekstu, nie kompletną zgodność renderu i danych wizualnych (`wgc/source.py:365`).
- **Skutek — ocena:** pozytywny test PDF nie dowodzi poprawnej kolejności czytania kolumn ani znaczenia przekreśleń. Zmiana wizualna bez zmiany normalizowanych słów może pozostawić stare potwierdzenie renderu i przyszły cache. Nie uruchamiano osobnego PDF z takim wizualnym kontrprzykładem; ten drugi wniosek jest analizą kodu.
- **Rekomendacja:** przed modelową ekstrakcją pilota obejrzeć 1–2 reprezentatywne strony, tabelę i poprawkę; związać potwierdzenie renderu z hashem strony/artefaktu, wersją ekstraktora i istotnymi flags. Wykrywać nieobsługiwany układ i zatrzymać automatyczną akceptację. OCR i pełny wielokolumnowy parser wdrażać dopiero według rzeczywistej próbki, a nie jako szeroki pakiet z góry.
- **ADR:** tak dla zmiany reguł segmentacji i znaczenia verified; konkretne poprawki ekstraktora w ramach jego wersji nie wymagają osobnego ADR każda. Q-11, N03.

### F14 — Polityka `local_deep` jest sprzeczna z wymuszeniem premium przy disagreement

- **Poziom / obszar:** ważne / routing i koszt.
- **Dowód — fakt:** `docs/LOGIC-MODEL.md:126` ustawia `local_disagreement` jako forced minimum high. `docs/INFERENCE-ROUTING.md:30` kieruje każdy forced do premium, a reguła 11 (`:35`) pozwala po sporze zaakceptować zgodę local_deep z jednym kandydatem przy braku forced. Przy obecnej definicji sporu warunek braku forced nie zachodzi. Reguła 5 (`:29`) również kieruje brak zgody wprost do premium. Routing jest dopiero planowany na M12.
- **Skutek — ocena:** niejasna kolejność polityk może dać zbyt tani, ryzykowny acceptance albo premium częściej niż zakłada kosztorys. Powtarzanie identycznego modelu i promptu nie zapewnia niezależnych błędów; sama zgodność dwóch odpowiedzi nie jest pomiarem jakości.
- **Rekomendacja:** na początek zachować forced/high → premium; local_deep przygotowuje diff i pakiet review, bez obniżania ryzyka. Jeśli właściciel chce wyjątku, odrębnie zdefiniować klasę rozbieżności, normalizację i warunki kalibracji na holdout. Jedna tabela pierwszeństwa reguł, bez równoległych opisów o innych konsekwencjach.
- **ADR:** tak, rozstrzygnięcie polityki względem ADR-0010/0017. N11.

### F15 — Koszt i jakość są hipotezami, a plan odkłada część potrzebnych dowodów

- **Poziom / obszar:** ważne / kierunek i ROADMAP.
- **Dowód — fakt:** `docs/COST.md:4` mówi, że baseline jest niezmierzony; udział eskalacji 20–30% jest założeniem (`:46`). Jedyny obecny job modelowo nic nie kosztuje. Gold M3 może zacząć się po M2a (`docs/ROADMAP.md:110`), natomiast M-E2E czeka na M10 i M-NODE (`:269`), M-INF na gold i M-GW2 (`:306`), a premium review M15 jest po extraction M14 (`:345`, `:361`). M14 ma dowieść jakości, zanim istnieje cały wymagany tor jej przeglądu.
- **Skutek — ocena:** LAN skeleton ma sens techniczny, ale jest za późny jako pierwszy test przekładu kontraktów między etapami. Scheduler i dobór wielu modeli mogą pochłonąć czas zanim zostanie sprawdzona reprezentacja trudnej reguły. Nie ma podstaw, by dziś stwierdzić, że cel ≤ 2× zostanie osiągnięty albo przekroczony.
- **Rekomendacja:** wcześniej gold i baseline z tego samego reprezentatywnego fragmentu; domenowy E2E z fake/replay oddzielić od testu LAN. M-INF dla jednego profilu uruchomić przed pełnym schedulerem; potrzebny adapter premium przed oceną M14. Mierzyć koszt na zaakceptowany rezultat z uwzględnieniem liczby jobów, dwóch ekstrakcji, retry, audytu, rewizji i pracy człowieka. Oceniać jakość również na ukrytej próbce prawdziwej gry; minigra pozostaje szybkim testem regresji.
- **ADR:** nie dla kolejności; tak tylko jeśli zmienia się przyjęta polityka jakości/kosztu. Q-02, N12.

### F16 — Wheel nie zawiera schematów i nie działa poza checkoutem

- **Poziom / obszar:** ważne / dystrybucja.
- **Dowód — fakt:** `wgc/contracts.py:16` szuka `../contracts/schemas`, a `pyproject.toml:22` włącza pakiety wgc/glu. W P17 skopiowano kod, kontrakty i pyproject do temp, uruchomiono `python -m pip wheel . --no-deps --no-build-isolation --no-index --wheel-dir <temp>`. Wheel powstał, ale miał **0 plików `.schema.json`**. Po wypakowaniu do temp i imporcie poza repo `schema_for("wgc/logic@0")` zgłosiło `referencing.exceptions.NoSuchResource`. Nie instalowano wheel do środowiska użytkownika. STATUS już dokumentuje ten problem jako zadanie M7.
- **Skutek — ocena:** testy checkoutu nie zapewniają działającego CLI po zwykłej instalacji; store GLU również potrzebuje tych schematów. M-NODE i przenośne smoke testy nie powinny czekać na późne widoki M7.
- **Rekomendacja:** dostarczać kontrakty jako zasoby pakietu i ładować przez `importlib.resources`; zrobić offline smoke wheel poza repo. Ustalić sposób współdzielenia zasobów z igw bez uzależniania węzła od domenowego wykonawcy WGC.
- **ADR:** nie dla naprawy wheel; mała decyzja o dystrybucji wspólnych kontraktów potrzebna przed wydzieleniem igw. N13.

### F17 — Poprawny ID może być niepoprawną ścieżką Windows

- **Poziom / obszar:** ważne / Windows i reprezentacja artefaktów.
- **Dowód — fakt:** gramatyka ID dopuszcza `:`, a `wgc/source.py:101` używa doc ID dosłownie jako katalogu cache. W P14 `source.init(root, "test:edition", [("rules", "rules.md")])` zaakceptował inwentarz; `source.extract` zakończył się **NotADirectoryError, WinError 267** dla `.glu/source/SRC-test:edition.rules`. `tests/test_ids.py` sprawdza podobne klucze, lecz nie roundtrip przez system plików.
- **Skutek — ocena:** kontrakt danych i platforma wspierana przez ADR-0022 nie są zgodne. Dwukropek w nazwie pliku ma też specjalne znaczenie na NTFS; nie badano osobno zachowania alternate data streams.
- **Rekomendacja:** oddzielić ID domenowe od nazw plików: deterministyczne kodowanie lub hash/mapa artefaktów. Nie zmieniać tożsamości rekordu tylko po to, żeby działała ścieżka. Sprawdzić zapis i odczyt dla dozwolonych znaków, nie sam parser ID.
- **ADR:** tak, krótka konwencja nazw artefaktów; bez nowej architektury. N14.

### F18 — Koszt akceptacji pojedynczego rekordu rośnie z całym KB

- **Poziom / obszar:** ważne / wydajność przy M14.
- **Dowód — fakt:** Workspace ponownie czyta pliki przy `record()` (`wgc/kb.py:75`), accept czyta/kopiuje KB (`:292`) i waliduje całość (`:326`). W P13 syntetyczne KB ze 100/500/1000 tabel: przyjęcie pełnej nowej partii trwało odpowiednio **0,563/2,739/8,754 s**; późniejsza zmiana jednego rekordu **0,584/3,721/6,710 s**. To pojedyncze próbki na tym środowisku, bez rozgrzewania/statystycznej analizy; nie benchmark rzeczywistej gry ani samego store.
- **Skutek — ocena:** atomizacja na tysiące małych jobów może powtarzać globalną pracę i zniwelować korzyści przyrostowości. Nie wykazano, że walidacja schematu store jest głównym kosztem; usunięcie jej według hipotezy z STATUS byłoby przedwczesne.
- **Rekomendacja:** indeksowany snapshot KB i cache skompilowanych walidatorów, następnie walidacja zmienionego domknięcia z okresową walidacją całości oraz kontrolą generacji. Ustalić budżet wydajności na zaakceptowany job dla typowej gry. Optymalizację poprzedzić profilem, zachować bezpieczeństwo F01/F02/Q-12.
- **ADR:** nie dla indeksu/cache walidatorów; tak przy zmianie gwarancji walidacji globalnej. N15.

### F19 — Proces ciągłości pomaga, ale nie wykrywa sprzecznej semantyki dokumentów

- **Poziom / obszar:** drobne / proces i granulacja.
- **Dowód — fakt:** `tests/test_continuity.py:41`, `67`, `81`, `91` kontroluje linki, statusy roadmapy, handoff i numerację ADR; mimo zielonej kontroli istnieją F07/F14. Z `git show --stat` dla M9a (`96ded88`): **24 pliki, 1801 insertions, 62 deletions**; M2a (`068f706`): 21/1466/118, M2b (`b19206e`): 18/1199/47, M8 (`cc532f4`): 15/1502/26. Liczby plików przekraczają lub sięgają orientacyjnego limitu SESSION-PLAYBOOK; statystyki linii obejmują też dokumenty i nie są miarą samego kodu/testów, dla których podano limit około 1500. Nie mierzono czasu poświęconego dokumentacji.
- **Skutek — ocena:** ciągłość realnie ułatwia odtworzenie intencji i rozpoznanie Q-12/Q-13. Kosztem jest powtarzanie kontraktów w wielu dokumentach; liczba zmian nie dowodzi sama w sobie spowolnienia.
- **Rekomendacja:** jedna normatywna specyfikacja interfejsu w DATA-CONTRACTS, inne dokumenty linkują; STATUS opisuje bieżący krok i decyzje, HANDOFF wynik i wyjątki. ADR dla trwałych wyborów architektonicznych, nie każdej funkcji. Dzielić milestone według sprawdzalnego pionu i ryzyka, nie mechanicznie liczby plików; nie dokładać osobnego milestone do każdej pozycji tego raportu.
- **ADR:** nie. N16.

### F20 — Testy są szerokie, ale część ich deklaracji jest mocniejsza od dowodu

- **Poziom / obszar:** drobne / jakość weryfikacji.
- **Dowód — fakt:** test „only writer” podmienia `_write_file` i nadal kończy build (`tests/test_glu_build.py:130`): dowodzi skierowania badanego zapisu przez helper, nie trwałości ani braku wszelkich alternatywnych pisarzy. Testy ścieżek stanów generują legalne ścieżki z tabeli samej maszyny (`tests/test_glu_store.py:56`, `137`): sprawdzają zgodność interpretera z tabelą, nie niezależny scenariusz biznesowy. Testy budowania importują helpery z innych modułów testowych (`tests/test_glu_build.py:12`) i używają globalnego licznika ID (`:21`). 424 przechodzące testy nie zawierają odtworzonych w tym przeglądzie awarii F01–F08/F11/F17.
- **Skutek — ocena:** łatwo przecenić gwarancje persistence/recovery; refaktoryzacja jednego testu może psuć inne. Nie znaleziono potrzeby zastąpienia całej obecnej strategii testowania.
- **Rekomendacja:** nazwać precyzyjnie dowód „only writer”; dodać niezależne scenariusze awarii, współbieżności, błędnych typów i usunięcia outputu oraz roundtrip wheel/Windows. Helpery przenieść do wspólnych fixture'ów lub modułu wsparcia z resetem ID na Workspace. Testy generowane z tabel zachować jako sprawdzanie mechaniki.
- **ADR:** nie. N17.

## 3. Rekomendowane zmiany w ROADMAP

To propozycja kolejności, bez edycji [ROADMAP](../ROADMAP.md) i [STATUS](../STATUS.md).

1. **Krótki etap stabilizacji po M9a, przed produkcyjnym M10.** Jedna sesja/mały ciąg sesji na ochronę zapisu, jednego pisarza, recovery, strukturę hashy i walidację propozycji (F01–F08). Nie trzeba wtedy budować pełnego grafu M13, ale trzeba ustalić status stale, manifest wywołania i zakres ownership, aby M11 nie utrwalił niewłaściwego kontraktu. Naprawić dystrybucję kontraktów i nazwy artefaktów jako część tego przygotowania.
2. **M3 i M-BASE zacząć teraz, po wyborze Q-02.** M3 nie zależy od modelowego wykonawcy. Gold powinien zawierać również niejasność, wyjątek i niepełną formalizację; aktualne fixture'y są ilustracją kontraktu, nie wzorcem działania parsera (STATUS wskazuje rozbieżność TAB-crt/TAB-4.3). Dodać małą prywatną próbkę z trudną tabelą/układem stron jako holdout; nie publikować chronionego źródła. Baseline i nową ścieżkę porównywać na tych samych materiałach i progach jakości z QUALITY.
3. **M9b może pozostać przed M10, ale nie jest warunkiem jego rozpoczęcia.** Harvest tylko pewnych kategorii jest użyteczny i tani jako drugi producent, który sprawdzi manifest i wielorekordowy output. Nie powinien opóźniać napraw F01–F08 ani pionu M10. Nie rozszerzać go teraz do NLP/embeddings/ontologii; dla E2E wystarczą ręcznie przygotowane pojęcia gold. Wybór „stabilizacja → mały M9b → M10a” jest rozsądny, jeśli M9b pozostanie w zadeklarowanym zakresie.
4. **Podzielić M10 na kontrakt/pętlę oraz połączenie.** Najpierw M10a: prawdziwy envelope i typed acceptance, joby na rekordach, fake/replay, pełna walidacja po constrained decoding, trwałe próby i klasy błędów. Potem M10b: provider self_hosted i fingerprint/capability/fallback zgodnie z igw. Context_builder powinien zwracać odtwarzalny kontekst/manifest z limitem i wersją, nie wyłącznie anonimową listę rekordów. `prompt` ma wskazywać wersjonowany artefakt; `output_schema` musi rzeczywiście sterować walidacją, a `decoding_schema` pozostaje pomocniczy.
5. **Rozdzielić M-E2E na wcześniejszy przebieg domenowy i późniejszy LAN.** E2Ea po M10a oraz minimalnym gold: źródło → reguła → digital legality → przypadek/test/gate, przez faktyczne API akceptacji, z fake/replay i regeneracją po zmianie źródła. To wykryje np. F07 przed M14. E2Eb po M-NODE/M10b: HTTPS, doctor, oczekiwany fingerprint, niedostępność, restart i brak automatycznego premium. Istniejący termin LAN skeleton nie jest za wczesny dla infrastruktury; jest za późny jako jedyny pierwszy pion domenowy.
6. **M11 dopiero po ustaleniu hashów, ownership i recovery.** Wymagane próby: zmiana samych komórek, roli źródła, definicji predykatu, niepełnego IR, promptu i wersji walidatora; utrata `.glu/`; zniknięcie jednego outputu. Trafienie L2 oznacza ponowne sprawdzenie aktualnych warunków akceptacji. Sam `output_schema: ...@0` nie identyfikuje treści schematu, jeśli @0 nadal jest edytowane.
7. **M5/M6 i politykę M12 domknąć przed oceną jakości M14; część Q-12 wcześniej.** M13 pozostawić na pełny graf i przyrostowy rebuild, ale mechanizm pozwalający naprawić stale bez ręcznego „odblokowywania” całej KB oraz mapa tożsamości są potrzebne już przed eksperymentem regeneracji. Q-13 rozstrzygnąć przed przyjęciem pierwszego niekanonicznego źródła, najlepiej z kontraktem M10.
8. **M-INF nie uzależniać od całego M-GW2.** Pierwszy pomiar jednego profilu i reprezentatywnego schematu wykonać przez minimalną bramkę; potem mierzyć scheduler, przełączanie i multi-pass. Wyprzedzająco nie wdrażać vLLM, async, embeddings ani multi-node. Cienka bramka z bezpieczeństwem, identyfikacją modelu i limitami jest uzasadniona i powinna pozostać.
9. **Minimalny adapter premium z M15 przenieść przed końcową akceptację M14.** Można rozwijać ekstrakcję M14 wcześniej na fake/replay, ale nie deklarować spełnienia premium review i celu jakości bez działającego toru albo niezależnego ręcznego pomiaru. Integrację MCP i rozbudowane pakiety review zostawić w późniejszych milestone'ach.
10. **M14 podzielić według jakości danych.** Najpierw concepts + atomowe rules, później relacje/wyjątki + cases/ambiguities z tym samym gold. `logic@1` zamrozić dopiero po przejściu L2, prób stale/renumber/awarii i holdout, nie po samym pierwszym buildzie minigry. Stage 2/3 i pełne digital@1 rozwijać w ich etapach; wcześnie ustalić tylko niezbędny pion i interfejsy.

Ocena celu VISION/COST: podział odpowiedzialności i strukturalny IR prowadzą w dobrą stronę, bo umożliwiają deterministyczną kontrolę i selektywne przeliczanie. Tę korzyść mogą zniweczyć niepełne projekcje, zależności schowane w context_builder, ciągła globalna walidacja i częste forced premium. Limit 2× dotyczy kosztu premium (`docs/COST.md:20`); czas GPU, oczekiwania i pracy człowieka trzeba raportować osobno, aby nie pomylić go z całkowitym kosztem workflow. LAN oraz brak fallbacku chronią kontrolę wydatku premium, ale opóźniony build nie jest „tanim zaakceptowanym wynikiem”. Brak obecnego pomiaru wyklucza ilościowy werdykt.

## 4. Decyzje dla właściciela

Każdy wiersz podaje alternatywy i ich konsekwencje. N01–N17 grupują nowe kwestie z ustaleń; nie proponują automatycznie siedemnastu nowych ADR ani milestone'ów. Decyzje o implementacji należy łączyć w opisane wyżej etapy.

| Kwestia | Opcje i skutki | Rekomendacja z uzasadnieniem | Kiedy |
|---|---|---|---|
| **Q-02: pilot i rozdział baseline** | A: czekać do M28 — prostszy obecny scope, późny dowód; B: jedna dostępna właścicielowi gra i reprezentatywny rozdział teraz — szybkie ujawnienie PDF/IR/kosztu; C: dwie gry od razu — większa różnorodność, więcej pracy gold. | B, rozdział z wyjątkiem, granicą liczbową i tabelą; kilka stron osobno jako holdout. Minigra jest zbyt dopasowana do ekstraktora (F13/F15). Konkretnego tytułu nie wybieram bez materiałów właściciela. | Przed M-BASE, teraz. |
| **Q-04: język glos** | A: tylko EN — najmniejszy koszt; B: EN kanoniczne glosy, PL jako widok Stage 3 — dodatkowa publikacja bez duplikacji IR; C: równorzędne glosy EN/PL w KB — dwie wersje do uzgadniania. | B, jeśli PL ma użytkowników; do Stage 1 wystarcza A. Nie mieszać tożsamości i formalnej semantyki z językiem glosy (ADR-0003, F06). | Przed widokami M7/Stage 3; nie blokuje M10. |
| **Q-05: licencja narzędzia** | A: MIT — prosty wybór dla narzędzia do szerokiego użycia; B: Apache-2.0 — bardziej rozbudowany tekst licencji; C: wstrzymać publiczne udostępnianie — odkłada decyzję. | A jako domyślna polityka projektu, jeśli właściciel chce swobodnej dystrybucji; B, jeśli ma uzasadnioną preferencję organizacyjną. Oddzielić licencję narzędzia od uprawnień do źródeł gry (ADR-0012). Nie wykonywano audytu prawnego. | Przed publikacją. |
| **Q-06: nazwa i adres węzła** | A: rezerwacja DHCP + nazwa w lokalnym DNS — wspólna konfiguracja; B: stały adres + hosts na kliencie — mniej zależności, ręczna synchronizacja; C: zmienny adres/wykrywanie — więcej mechanizmów w MVP. | A, o ile router to umożliwia; B jako prosty fallback. Wybrać nazwę zgodną z SAN certyfikatu i adres dev machine do allowlisty (NODE §7). Nie sprawdzano routera. | Przed M-NODE. |
| **Q-07: autostart** | A: Harmonogram zadań — mniej elementów wdrożenia; B: WinSW/usługa — dodatkowy wrapper i konfiguracja; C: ręczny start — szybki eksperyment, wymaga operatora. | A w MVP, z testem po restarcie i uruchomieniem bez sesji użytkownika; B dopiero gdy pomiar/operacje wymagają usługi. C tylko podczas prób (NODE, ROADMAP M-NODE). | M-NODE. |
| **Q-08: premium przy niedostępnym LAN** | A: zawsze false — kontrola kosztu, build może czekać; B: jawny opt-in konkretnego buildu z limitem — możliwość dokończenia pilota; C: globalnie true — dostępność kosztem nieprzewidywalnego wydatku. | A domyślnie, B wyłącznie świadomie przy terminie i zapisanym budżecie/premium_reason. Nie zmieniać semantycznych eskalacji high na lokalne akceptacje (ADR-0017). | Polityka przed M12; opt-in przed konkretnym buildem. |
| **Q-09: zakres referencji/L2** | A: pozostać przy liście M1 — prosto, F12 nadal przechodzi; B: rekurencyjna kontrola wszystkich zadeklarowanych referencji i typów celów — większy zakres, pełny dowód; C: kontrolować tylko referencje potrzebne obecnym zadaniom — krócej, trzeba oznaczyć niezweryfikowane rodzaje. | B w M5, z kontrolami rodzaju i zmiennych; C dopuszczalne wczesne E2E z jawną granicą, bez deklaracji pełnego L2. | Przed jakościową akceptacją M14. |
| **Q-11: PDF** | A: wspierać wyłącznie obecny układ i blokować inne — bezpieczny mały scope; B: dostosować kolumny/stopki do próbki pilota — praktyczny koszt; C: pełny OCR i ogólny layout teraz — duży niezweryfikowany zakres. | A jako minimum, następnie B według próbki Q-02; C odłożyć. Nie dowodzić gotowości testem PDF wygenerowanym z minigry. | Preflight przed pierwszą modelową ekstrakcją realnego PDF, nie dopiero M28. |
| **Q-12: stale kontra błąd** | A: ręcznie naprawiać KB przed każdym accept — obecna blokada; B: jawne stale/tombstones/mapa zmian, regeneracja podgrafu — więcej stanu domenowego, naprawialność; C: wszystkie błędy refs jako warning — łatwo przepuścić uszkodzoną KB. | B; zablokowane bramki dla stale, nadal twarde błędy schematu i nierozpoznane dangling refs. | Minimalna polityka przed regeneracją/M11; pełny graf M13. |
| **Q-13: źródła niekanoniczne** | A: odrzucić automatyczny canonical accept — proste i zgodne z LOGIC-MODEL; B: osobne evidence/proposed z promocją przez HD — pełniejszy workflow; C: zmienić tylko prov.kind — nadal można niesłusznie zaakceptować. | A teraz, B później przy HD; C niewystarczające. | Przed użyciem takich źródeł, najlepiej kontrakt M10. |
| **N01: trwałość partii (F01)** | A: atomowy plik — chroni przed obcięciem, nie częściową partią; B: pliki + manifest commit/recovery — zachowuje YAML i odtwarzalność; C: przenieść canonical KB do DB — większa zmiana ADR-0004. | B, wdrażane od A jako pierwszego zabezpieczenia. | Przed M10. |
| **N02: jeden pisarz (F02)** | A: lock całego accept — najprostsza izolacja; B: lease/CAS generacji + kolejka akceptacji — gotowe na równoległe obliczenia; C: WAL SQLite — nie chroni KB. | A teraz, projekt B przy tym samym protokole commit; C tylko po osobnym pomiarze store. | Przed równoczesnymi buildami; nie czekać do MCP. |
| **N03: strukturalny/visual hash (F03/F13)** | A: dalej tylko text_hash — kolizje struktury; B: dodatkowy wersjonowany hash struktury/artefaktu — rozdziela tekst od parsera; C: hashować wyłącznie surowy plik źródła — bezpieczniejsze missy, utrata selektywności segmentów. | B; hash pliku/strony jako uzupełnienie dla renderu, nie zamiennik wszystkich zależności. | Przed M11, najlepiej stabilizacja M9a. |
| **N04: recovery (F04)** | A: uruchamiać nowy build — prosty retry, stare stany wiszą; B: reconcile z receipt/generacją — odtwarza wynik i diagnozę; C: jedna baza obejmująca KB i store — zmienia źródło prawdy. | B, bez rozproszonej transakcji; atomiczne końcowe wpisy store. | Przed modelowymi kosztownymi jobami. |
| **N05: manifest wejść (F05)** | A: hash samych dowodów — niepełna zależność; B: jawny manifest wywołania i osobne dowody rekordu — odtwarzalne po utracie .glu; C: wszystkie dane Workspace w hash — bezpieczne, lecz każda zmiana unieważnia wszystko. | B; Tier 0 pusty context tylko dla rzeczywiście czystego zadania. | Kontrakt M10, przed M11. |
| **N06: projekcje (F06)** | A: zawsze ignorować glosy — unsafe dla partial/none; B: warunkowe pola semantyczne i kompletne projekcje używanych kinds — precyzyjna invalidacja; C: cały rekord bez prov/status — bezpieczny start, więcej missów. | B, C jako jawnie wersjonowany tymczasowy wariant dla nowego rodzaju. | Przed cache i jobami na rekordach. |
| **N07: envelope/status/etap (F07)** | A: osobne accept dla każdego etapu — duplikacja reguł; B: wspólna granica i typed policies/dispatch — współdzielona trwałość, poprawna domena; C: model nadaje status/prov — łamie ADR-0014. | B; lifecycle oddzielone od AMB resolution, HD kontrolowane przez WGC. Błędne kotwice reject/retry, inferencja wyłącznie jawną ścieżką z derived_from. | Przed M10a/E2Ea. |
| **N08: błędne dane (F08)** | A: gramatyka wystarcza — exceptions; B: envelope/schema przed domeną — naprawialne wyjście; C: łapać każde Exception jako rejection — maskuje awarie programu. | B, z osobną obsługą awarii I/O/recovery. | Najbliższa sesja. |
| **N09: trwałe ID (F10)** | A: aktualna etykieta jest ID — prostota, renumber łamie refs; B: stałe ID z aliasami/namespace i mapą wydań — jawna tożsamość; C: ID z hasha treści — zmiana treści zmienia tożsamość. | B; czytelne początkowe ID mogą zostać, ale nie są regenerowane z nowych etykiet. | Przed pierwszą erratą/przenumerowaniem i logic@1. |
| **N10: ownership i zbiór outputów (F11)** | A: merge append/update — pozostają usunięte atomy; B: task+scope i manifest outputów, tombstones — uzgadnianie całości; C: usuwać wszystkie rekordy taska — niszczy inne scope i decyzje. | B, z ochroną HD i kandydatem dla derived_from wewnątrz partii. | Przed wielorekordowym M14, projekt w M10. |
| **N11: local_deep/disagreement (F14)** | A: forced/high zawsze premium, deep tylko pakiet — zgodne z ostrożną polityką; B: kalibrowany wyjątek po określonej klasie sporu — możliwa oszczędność, nowa polityka ryzyka; C: większość głosów bez kalibracji — brak dowodu bezpieczeństwa. | A teraz; B tylko po gold/holdout i świadomym ADR. | Przed M12. |
| **N12: dowody i kolejność (F15)** | A: obecny plan z jednym późnym E2E — późne wykrycie złych interfejsów; B: gold/baseline + offline E2E wcześniej, LAN osobno — szybszy dowód; C: od razu pełny pilot — szeroki scope bez infrastruktury kontroli. | B i minimalny tor premium przed końcową oceną M14. | Ustalenie następnego ciągu sesji. |
| **N13: kontrakty w dystrybucji (F16)** | A: tylko editable checkout — działa lokalnie, ogranicza instalację; B: package resources — działający wheel; C: osobny pakiet kontraktów — niezależność igw, dodatkowa dystrybucja. | B teraz; sposób C lub wspólnego zasobu ustalić przy wydzielaniu igw, bez domenowych zależności workerowi. | Przed M10b/M-NODE, nie późny M7. |
| **N14: ID a ścieżka (F17)** | A: zakazać ':' w ID — zmiana danych; B: encode/mapowanie nazw plików — zachowuje kontrakt; C: skrócone hashe nazw — potrzebna kontrola kolizji/mapa. | B albo pełny hash artefaktu; wybrać jedną konwencję i roundtrip Windows. | Najbliższe przygotowanie Stage 0. |
| **N15: wydajność/globalna walidacja (F18)** | A: globalnie przy każdym jobie — proste, koszt N×jobs; B: snapshot/index + changed closure + końcowy full — szybsze, wymaga izolacji; C: wyłączyć walidację store — brak wykazanego związku z kosztem. | B etapami po pomiarze; nie robić C na podstawie obecnych wyników. | Pomiar przed M14, closure w M13. |
| **N16: ciągłość (F19)** | A: zachować duplikację opisów — więcej ręcznej synchronizacji; B: jedna specyfikacja + krótkie statusy i linki — mniej rozjazdów; C: usunąć handoff/ADR — utrata intencji. | B, zachować test linków i historię decyzji. | Przy kolejnych sesjach, bez dużej migracji dokumentów. |
| **N17: granice dowodów testowych (F20)** | A: obecne testy wystarczają — nie obejmą fault paths; B: uzupełnić scenariusze ryzyka i fixture helpers — konkretne gwarancje; C: szeroki nowy framework — koszt bez koniecznego dowodu. | B, bez przebudowy całego zestawu testów. | Z naprawami odpowiadających ustaleń. |

## 5. Szybkie poprawki do najbliższej sesji (każda ≤ 1 h)

Szacunki dotyczą wąskich zmian wykonywanych przez osobę znającą kod; nie oznaczają, że wszystkie ustalenia mieszczą się w godzinie. W tym przeglądzie żadnej z tych zmian nie wykonano.

| Poprawka | Sprawdzalny wynik i granica |
|---|---|
| Type guards dla `record.id`, `anchors.quote` i `span` w envelope | P10 daje diagnostykę zamiast TypeError. Nie zastępuje kompletnego kontraktu M10. |
| Usunąć permissive role fallback z automatycznej akceptacji | P5 odrzucony dla community/prior_translation z jasnym powodem; HD workflow później. Właściciel najpierw rozstrzyga Q-13. |
| Atomowy zapis **pojedynczego** pliku przez temp i replace | Awaria przed replace zachowuje poprzednie bajty; F01 dla wielu plików nadal wymaga protokołu partii. |
| Test zmiany granic komórek oraz krótki komunikat o potrzebie regeneracji starego cache | Utrwala kontrprzykład F03 i ogranicza przypadkowe użycie starych artefaktów; właściwy hash/wersja to osobna naprawa. |
| Uzgodnić w dokumentacji pierwszeństwo forced nad regułą local_deep | Jeden jednoznaczny opis N11 po decyzji właściciela; nie wdraża routera. |
| Nazwać precyzyjnie test „only writer” i wydzielić współdzielone fixture ID | Test opisuje delegowanie zapisu, brak zależności od kolejności testów; nie zapewnia recovery. |
| Dodać offline smoke wheel poza checkoutem | Wykrywa brak schematów w artefakcie. Naprawę package resources szacować osobno zależnie od współdzielenia z igw. |
| Ustalić i zapisać zakres próbki Q-02/M-BASE | Jasna lista reguł, tabela, wyjątek, materiał holdout i metryki; nie jest to wykonanie całego baseline. |

Nie przedstawiam full recovery, trwałego ID, multi-file commit ani walidacji przyrostowej jako „szybkiej poprawki”: wymagają decyzji i testów granicznych. Nie zalecam na tym etapie usuwania schematowej walidacji store, dodawania WAL w celu ochrony KB ani budowania ogólnego OCR.

## 6. Czego nie sprawdzono i dlaczego

- **Modele i sieć:** zgodnie ze zleceniem brak wywołań inferencji, dostępu do LAN/igw, TLS, DNS, GPU, benchmarku llama.cpp/vLLM, premium i aktualizacji źródeł zewnętrznych. Deklaracje NODE o możliwościach runtime'ów oceniono jako projekt i hipotezy; nie potwierdzono ich niezależnie.
- **Jakość i koszt:** brak wybranego PDF pilota, wykonanego gold/M-BASE oraz holdout. Nie zmierzono dokładności, FN, jakości przekładu, eskalacji, kosztu tokenów ani czasu człowieka; 424 testy i parse tabeli tych miar nie zastępują. Nie oceniano praw do konkretnego materiału gry ani prawnego doboru licencji.
- **Stage 1.5–3 i router/cache:** schematy i plan przeczytano, lecz wykonawcy, routing M12, cache M11 i graf M13 jeszcze nie istnieją. Kontrprzykłady hashy wskazują ryzyko przyszłego cache, nie wykonane błędne trafienie. Nie uruchomiono pełnego modelowego pionu.
- **PDF wizualnie:** zestaw testowy wykonuje ekstrakcję i render syntetycznych PDF, ale w tym przeglądzie nie przeprowadzono ręcznej oceny PNG prawdziwej księgi. Gotowość na kolumny, skany, nagłówki, erratę i nietypografowane numery pozostaje nieudowodniona.
- **Awaria fizyczna:** P7/P8 używają wstrzykniętych wyjątków, a P15 dwóch wątków z kontrolowaną kolejnością. Nie odcinano zasilania, nie zabijano procesów przy fsync i nie testowano dwóch niezależnych CLI ani blokad sieciowego systemu plików. Nie badano rzeczywistych ADS na NTFS. Wyniki wystarczają do wykazania opisanych błędów, nie do specyfikacji wszystkich awarii.
- **Skala i platformy:** P13 jest syntetyczny i jednokrotny, nie obejmuje grafu zależności prawdziwej gry. Nie profilowano store niezależnie. Nie uruchamiano bieżącego kodu na Python 3.10 ani Linux/WSL; historyczny handoff M0 opisuje takie testy dla wcześniejszej wersji.
- **Dystrybucja:** wheel zbudowano offline i wypakowano do temp; nie zmieniano instalacji użytkownika, nie publikowano pakietu i nie testowano osobnego instalatora igw.

Jedyną zamierzoną zmianą repo jest ten raport. Kod, kontrakty, fixture'y, ROADMAP, STATUS i ADR pozostają bez zmian; nie wykonano commit ani push. Końcowa kontrola `python -m pytest tests/test_continuity.py` po zapisaniu raportu: **68 passed**, 0,57 s, w tym poprawność względnych linków nowego dokumentu.
