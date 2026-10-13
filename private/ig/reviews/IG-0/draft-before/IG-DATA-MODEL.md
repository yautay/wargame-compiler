# Propozycja struktury danych IG dla pełnej instrukcji

- **Status:** draft do krytycznej recenzji IG-0 i prób planu IG.
- **Data:** 2026-10-11.
- **Wersja propozycji:** ig-draft-0.2, po przeglądzie materiałów GMT, OSG i MMP.
- **Zakres:** model logiczny i robocza reprezentacja danych.
- **IG:** w tej propozycji Instruction Graph, czyli graf treści instrukcji i zależności reguł.

IG ma pozwalać odszukać regułę, sprawdzić jej źródło, prześledzić potrzebne
procedury i wyjątki oraz wskazać, czego brakuje do rozstrzygnięcia sytuacji.
Proponuję graf z osobnymi rekordami źródeł, obiektów instrukcji, twierdzeń,
relacji, luk i decyzji człowieka. Akceptacja pojedynczego warunku lub cytatu
obejmuje dokładnie ten zakres; nie nadaje akceptacji całej regule ani grafowi.

Wspólny rdzeń uzupełniają profile konkretnych systemów i wydań oraz opisy
zdarzeń, stanu, wyborów graczy, przestrzeni i obliczeń. Ich kontrakt opisuje
[rozszerzenie modelu dla mechanik gier](IG-MECHANICS-PROFILES.md).
SPQR, OSG TLNB, OSG Campaigns of Napoleon, OSG Days i GCACW mają osobne
przestrzenie znaczeń. Wspólny model danych nie zakłada identyczności ich reguł.

Właściciel zlecił zachowanie POC w archiwum i przyjęcie IG jako zalążka
narzędzia do digitalizacji gier. Aktywne są
[ADR-0040](adr/ADR-0040-ig-i-archiwum-poc.md) i [plan IG](IG-PLAN.md).
Przyjęcie kontraktu, wybór magazynu i implementacja pozostają dalszymi
decyzjami. Historyczna ocena POC i oryginalne wyniki pozostają niezmienione.

## Podstawa projektu

Punktem wyjścia jest prywatny
`private/archive/poc-2026-10-11/payload/private/poc/spqr-chapter9/formats/proposal-format-v1.md`.
Zachowujemy rozdzielenie transkrypcji od interpretacji, jawne stany niewiedzy,
dowody obrazowe, kierunek zależności i rejestr pokrycia źródła.

Dotychczasowy przegląd, opisany w [historycznym STATUS](../archive/poc-2026-10-11/project/docs/STATUS.md), wskazuje potrzebę
akceptacji na poziomie fragmentów i pól. Uzasadnienie lokalnej treści oraz
potwierdzenie wymagania źródła nie dostarczają jeszcze pełnego wyniku gry.
Przy pełnej instrukcji trzeba również rozdzielić wydania, warianty,
kontynuacje, odwołania między rozdziałami i fakty pochodzące ze scenariuszy.

## Kolekcje danych

Poniższe kolekcje składają się na jeden graf. Pola opisane dalej są roboczym
kontraktem; magazyn może reprezentować je jako dokumenty lub rekordy.

| Kolekcja | Jednostka zapisu | Najważniejsze pola |
|---|---|---|
| `sources` | Konkretna wersja materiału źródłowego | `id`, `game_id`, `edition`, `role`, `language`, `artifact`, `supersedes_source_ids` |
| `regions` | Fragment konkretnego źródła | `id`, `source_id`, `pdf_page`, `printed_page`, `locators`, `reading_order`, `parent_region_id` |
| `evidence` | Dowód treści lub interpretacji | `id`, `region_ids`, `kind`, `transcription`, `image_artifacts`, `normalization_notes` |
| `nodes` | Obiekt instrukcji o stabilnej tożsamości | `id`, `kind`, `labels`, `source_region_ids`, `parent_node_id`, `payload` |
| `assertions` | Jedno twierdzenie dotyczące obiektu | `id`, `subject_id`, `facet`, `state`, `value`, `representation`, `applicability`, `evidence_links`, `gap_ids` |
| `relations` | Jedna relacja między obiektami | `id`, `from`, `to`, `target_candidate`, `kind`, `explicitness`, `applicability`, `evidence_links`, `gap_ids` |
| `gaps` | Konkretny brak lub nierozstrzygnięcie | `id`, `class`, `affected_refs`, `needed_context`, `blocking_for`, `evidence_ids` |
| `reviews` | Decyzja lub obserwacja dotycząca dokładnej wersji danych | `id`, `actor`, `actor_role`, `decision`, `targets`, `basis`, `supersedes_review_ids` |
| `coverage` | Rozliczenie fragmentu źródła w konkretnym wyniku | `id`, `region_id`, `status`, `represented_refs`, `gap_ids`, `run_id` |
| `runs` | Pochodzenie propozycji lub przekształcenia | `id`, `kind`, `input_artifacts`, `prompt_artifact`, `response_artifact`, `configuration`, `measurement` |
| `snapshots` | Spójny zestaw wybranych wersji rekordów | `id`, `profile`, `parent_snapshot_id`, `selected_refs`, `conflicts`, `validation_artifact` |
| `profiles` | Definicja zgodnego zestawu reguł i możliwości modelu | `id`, `publisher_id`, `series_id`, `game_id`, `ruleset_id`, `source_requirements`, `capabilities`, `vocabulary`, `composition_decisions` |

Wszystkie kolekcje mogą zawierać wiele rewizji jednego rekordu. Rekordy
źródłowe i surowe odpowiedzi zachowują swoje oryginalne bajty.

## Tożsamość i rewizje

Każdy rekord ma wspólną kopertę:

```json
{
  "id": "ig-demo:assertion:movement-limit",
  "revision_id": "rev-001",
  "record_type": "assertion",
  "schema_version": "ig-draft-0.2",
  "run_id": "ig-demo:run:manual-design",
  "supersedes_refs": []
}
```

`id` jest unikalne w przestrzeni grafu i pozostaje stabilne przy korektach.
Numer reguły jest etykietą, nie kluczem. Jeden numer może obejmować kilka
klauzul, a jedna klauzula może przechodzić między stronami. Tożsamość obiektu
nie wynika też wyłącznie z hasha jego treści.

`revision_id` wskazuje niezmienny zapis. Odwołanie do wersji ma postać
`{id, revision_id, sha256}`; hash dotyczy bajtów osobnego pliku rekordu UTF-8.
Hash jest w manifeście lub odwołaniu, poza hashowanym rekordem.
Zmiana tworzy nową rewizję. Rozdzielenie lub połączenie obiektów tworzy nowe
ID i jawne mapowanie w `supersedes_refs` z opisem `split` lub `merge`.

Przykładowe ID w dokumencie są czytelne dla człowieka. Docelowy generator
może stosować UUID z prefiksem przestrzeni grafu; etykiety pozostają osobno.
Nie wolno automatycznie scalać obiektów różnych wydań. Ewentualna zgodność
między nimi jest osobnym, sprawdzonym mapowaniem.

Odwołania semantyczne, np. `subject_id`, wskazują stabilne ID. Snapshot
jednoznacznie wybiera ich rewizje. Dowody i decyzje człowieka przypinają
konkretne rewizje oraz hashe, żeby późniejsza poprawka nie zmieniła ich sensu.

## Źródła i dowody

`sources.role` przyjmuje `rulebook`, `errata`, `faq`, `scenario`, `map`,
`counter_sheet`, `player_aid` lub `other`. Podręcznik bazowy może być kompletnie
przetworzony, a wynik sytuacji nadal zależeć od niedostępnej mapy lub tabeli.

`artifact` zawiera `path`, `sha256`, `media_type` i wielkość w bajtach.
Ścieżki rzeczywistych materiałów wydawcy znajdują się w `private/`.
Wydanie i rola są metadanymi źródła; jego pierwszeństwo wobec innych źródeł
wymaga osobnego uzasadnienia i decyzji.

Do identyfikacji dochodzą `publisher_id`, `series_id`, `ruleset_id`,
`document_part_id`, `rules_mode` i wersja odczytana z materiału. Etykieta
odwołania jest rozpatrywana w tej przestrzeni. Oznaczenie 1.0 w części
podstawowej i 1.0 w części zaawansowanej nie wskazują tego samego obiektu.
Nazwa pliku, tłumaczenie i data pobrania nie ustanawiają zgodności wydania.

`regions` zachowują stronę fizyczną PDF liczoną od 1, osobną drukowaną
etykietę, kolejność czytania i lokalizatory. Każdy lokalizator podaje typ,
układ współrzędnych i rozmiar obrazu albo sposób liczenia offsetów tekstu.
Obszar w punktach PDF, pikselach strony i pikselach wycinka to różne układy.

`evidence` może obejmować kilka regionów, np. tekst z obu kolumn albo tabelę
z notą na następnej stronie. Dokładna transkrypcja, normalizacja i odczyt
niepewnych znaków pozostają odrębne. Obraz może dostarczać dowodu, którego
nie ma w tekście pomocniczym.

Powiązanie twierdzenia z dowodem ma `evidence_id`, `role` oraz uzasadnienie.
Role to `direct`, `context` i `counterevidence`. Samo dołączenie całej strony
do reguły nie dowodzi każdego jej warunku, parametru ani wyjątku.

## Obiekty instrukcji

`nodes.kind` określa rodzaj obiektu:

| Rodzaj | Reprezentacja |
|---|---|
| `section` | Rozdział lub podrozdział i hierarchia instrukcji |
| `rule` | Oznaczona reguła grupująca klauzule |
| `clause` | Najmniejszy fragment zachowujący pełny warunek i skutek |
| `definition` | Definicja pojęcia |
| `procedure`, `step` | Procedura i jej kroki |
| `table`, `table_row`, `table_column`, `table_cell` | Tabela, osie i komórki |
| `diagram`, `diagram_part` | Grafika i istotne elementy |
| `note`, `example` | Nota lub przykład z zachowaniem roli źródłowej |
| `concept`, `unit_type`, `phase`, `parameter` | Pojęcia i parametry, do których odnoszą się reguły |
| `scenario`, `map_feature`, `counter` | Obiekty innych materiałów gry, jeśli są dostępne |
| `action`, `event_type`, `state_variable`, `resource`, `timing_window` | Definicje działań, zdarzeń, stanów, zasobów i czasu |
| `choice`, `selector`, `spatial_policy`, `randomizer`, `calculation`, `outcome` | Wybory, zbiory obiektów, reguły przestrzeni, losowość i rozstrzygnięcia |

`labels` zachowują oryginalne oznaczenia z `source_id` i ich regionem.
`parent_node_id` opisuje hierarchię redakcyjną, np. klauzulę pod regułą.
Zależność wykonania jest osobną relacją. Przykład może ilustrować regułę;
przekształcenie jego treści w normę wymaga osobnego twierdzenia z dowodem.

`payload` przechowuje strukturę odpowiednią dla rodzaju obiektu. Tabela ma
ID osi i komórek, komórka ID wiersza i kolumny oraz informacje o scaleniu.
Wartość komórki, nagłówek, jednostka i zakres noty są osobnymi twierdzeniami.
Krok procedury ma kolejność źródłową; rozgałęzienia i powroty wymagają
warunkowych relacji. Diagram może mieć opis i obrazy bez pełnej geometrii.

Podział na klauzule wynika z warunków, skutków i wyjątków. Nie dzielimy
każdego zdania mechanicznie i nie odrywamy wyjątku od jego zakresu.

## Twierdzenia i znaczenie reguł

`assertions` rozdzielają tożsamość obiektu od proponowanych odczytów jego
treści. Jedna klauzula może mieć osobne twierdzenia dla transkrypcji,
warunku, skutku, parametru, wyjątku i czasu. `facet` wskazuje dokładny
element, np. `transcription`, `condition`, `effect`, `parameter`,
`scope`, `timing`, `definition` lub `table_value`.

Kontrakt rozszerza te aspekty o `permission`, `obligation`, `prohibition`,
`trigger`, `cost`, `choice`, `calculation`, `transition`, `duration`,
`aggregation`, `visibility` i `victory`. Struktura znaczenia jest zestawem
powiązanych twierdzeń, a nie jednym nieprzejrzanym polem `action_effect`.
Każde może mieć własny stan wiedzy, dowody i review.

`state` ma cztery wartości znane z formatu POC:

- `known`: wartość ustalona w propozycji i powiązana z dowodem; review jest osobne.
- `established_absent`: źródło potwierdza brak w podanym zakresie.
- `unknown`: `value` jest null; wymagane uzasadnienie i co najmniej jedna luka.
- `not_applicable`: `value` jest null; wymagane uzasadnienie niestosowalności.

Brak pola lub pusta lista nie oznaczają, że instrukcja nie zawiera wyjątku.
Brak wyjątku w jednej klauzuli nie oznacza jego braku w całej grze.

Uzasadnienie stanu zapisujemy w `reason`. Wartość może mieć granice
czasowe i zależeć od przyczyny zdarzenia, odczytu wcześniejszego stanu lub
historii działań; szczegóły określa rozszerzenie mechanik.

`representation` to `literal`, `normalized` lub `interpreted`. Interpretacja
nie zastępuje literalnej treści. Jeżeli proponujemy strukturę logiczną,
wartość ma opis oraz opcjonalny `expression` z jawnie wskazanym stopniem
formalizacji. Minimum obejmuje `all`, `any`, `not`, `compare`, `ref`,
`quantity` i `opaque`. `opaque` zachowuje niezinterpretowany tekst i blokuje
wykonanie wymagające tej części. Domknięty język wykonawczy pozostaje otwarty.

Liczby zachowują jednostkę i operator, np. `<=` różni się od `<`.
Czas zawiera odniesienie do fazy lub zdarzenia, granice i moment obowiązywania.
Nie wprowadzamy globalnego priorytetu wyjątków przez zasadę „bardziej
szczegółowe zawsze wygrywa”. Zakres i pierwszeństwo wymagają źródła.

Przykład syntetyczny pokazuje pełną treść jednego twierdzenia wraz z kopertą.
Przywołane obiekty i dowód są elementami przykładu, nie istniejącymi rekordami POC.

```json
{
  "id": "ig-demo:assertion:movement-limit",
  "revision_id": "rev-001",
  "record_type": "assertion",
  "schema_version": "ig-draft-0.2",
  "run_id": "ig-demo:run:manual-design",
  "supersedes_refs": [],
  "subject_id": "ig-demo:clause:movement",
  "facet": "parameter",
  "state": "known",
  "representation": "interpreted",
  "value": {
    "name": "movement_distance",
    "operator": "<=",
    "quantity": {"value": 3, "unit_id": "ig-demo:concept:space"},
    "text": "W tym fikcyjnym przykładzie ruch obejmuje najwyżej trzy pola."
  },
  "applicability": {
    "state": "known",
    "description": "Zwykły ruch w fazie ruchu fikcyjnej gry",
    "node_ids": ["ig-demo:phase:movement"],
    "gap_ids": []
  },
  "evidence_links": [
    {"evidence_id": "ig-demo:evidence:movement", "role": "direct",
     "rationale": "Fikcyjna klauzula podaje limit i jednostkę."}
  ],
  "gap_ids": []
}
```

To fragment ilustrujący model, nie kompletny snapshot do importowania.
Sam `state: known` nie stwierdza akceptacji człowieka.

## Relacje i odwołania między rozdziałami

Dla zależności `from` oznacza obiekt korzystający z celu, a `to` obiekt
używany lub modyfikowany. Zachowujemy rodzaje POC: `procedure_use`,
`table_use`, `definition`, `condition`, `modification`, `exception`,
`continuation` i `mention`. Dodajemy `applies_to`, `illustrates` i
`precedes` z osobno określoną semantyką:

- `exception` i `modification`: reguła wyjątku lub zmiany → reguła bazowa.
- `continuation`: wcześniejszy fragment → późniejszy fragment.
- `applies_to`: klauzula → typ jednostki, faza lub inny obiekt jej stosowania.
- `illustrates`: przykład lub diagram → ilustrowana reguła.
- `precedes`: krok wcześniejszy → późniejszy; warunek przejścia zapisany osobno.

`explicitness` to `explicit` lub `implicit`. Relacja niejawna wymaga dowodu
potrzeby, nie tylko podobieństwa słów. Wzmianka nie jest zależnością wykonania.
Status dostępności celu i stan jego review pozostają niezależne.

`from` i rozstrzygnięte `to` mogą zawężać cel do `assertion_ids`.
`target_status` to `resolved`, `unresolved`, `ambiguous` lub `unsupported`.
Przy dwóch ostatnich stanach nie wybieramy po cichu jednego celu.
`target_candidate` zawiera oryginalne odwołanie, wydanie, przewidywany rodzaj
obiektu, opis i listę kandydatów; dla nierozstrzygniętego celu `to` jest null.
Numer bez kontekstu wydania nie wystarcza do dopasowania.

`applicability` relacji i twierdzeń ma `state`, `description`, `node_ids`
oraz `gap_ids`; opcjonalnie zawiera wyrażenie warunku. Scope może być
nieznany i wymagać luki. Przy interpretacji trzeba zachować jego źródło.

`requirement` relacji opisuje `required`, `conditional` lub `informational`.
Gdy kilka celów jest potrzebnych łącznie albo alternatywnie, relacje mają
`requirement_group_id` i `group_operator: all|any`. Odtworzenie takiej grupy
wymaga dowodu. Pozwala to odróżnić brak jednego z obowiązkowych kroków od
braku niewykorzystanej alternatywy.

Cykle między regułami są dopuszczalne. Należy je zgłaszać i rozpatrywać
w kontekście procedur; nie wolno zakładać, że cały graf jest DAG.

Relacje mechaniczne `reads`, `writes`, `triggers`, `schedules`, `resumes`,
`constrains` i `uses_binding` mają osobno określone kierunki w rozszerzeniu.
Wyszukiwanie następstw zmiany musi obejmować te relacje i jawne ograniczenia
wyborów, również wtedy, gdy lokalna treść drugiej reguły się nie zmieniła.

## Braki i gotowość do rozstrzygnięcia

`gaps.class` obejmuje `missing_source`, `unreadable`, `unprocessed`,
`ambiguous_reference`, `ambiguous_source`, `unsupported_interpretation`
i `conflicting_claims`. Błąd odczytu jest obserwacją review; luka zapisuje
wynikający z niego brak użytecznej informacji.

`affected_refs` wskazują dokładne obiekty lub twierdzenia. `blocking_for`
opisuje ograniczony wpływ: np. ustalenie wartości, wykonanie procedury lub
pełne rozstrzygnięcie wskazanego rodzaju sytuacji. Dostarczenie źródła nie
zamyka luki automatycznie; trzeba sprawdzić jego treść i nową propozycję.

Gotowość jest wynikiem zapytania dla snapshotu, profilu i faktów sytuacji.
Nie zapisujemy jednego globalnego `rule_ready: true`. Raport rozróżnia:

1. Czy treść lokalna ma potrzebne zaakceptowane twierdzenia.
2. Czy potrzebne cele zależności są dostępne i sprawdzone w tym zakresie.
3. Czy konkretny wynik sytuacji jest rozstrzygalny przy podanych faktach.

Luka w wymaganej zależności przechodzi do uzasadnienia blokady wyniku.
Przy nieznanym warunku stosowania nie zakładamy, że zależność jest nieistotna.
Alternatywy, wyjątki, cykle i konflikt źródeł wymagają jawnej obsługi.
Reguła może mieć zaakceptowany lokalny limit i nadal nie pozwalać obliczyć
pełnego skutku bez tabeli. Zakres przetworzenia pełnej instrukcji jest
odrębny od gotowości całej gry.

## Przegląd człowieka

`reviews` zawierają decyzję `accepted`, `rejected` lub `needs_context`
albo obserwację `observation`. `actor_role` określa `human_owner`,
`human_reviewer`, `model` lub `validator`; tylko uprawniony człowiek może
nadać semantyczną akceptację. Uprawnienia recenzenta wymagają ustalenia.

`targets` wskazują dokładne rewizje i hashe twierdzeń lub relacji oraz
`scope_description`. Dodatkowy `field_path` może zawężać zakres, ale decyzja
nie rozszerza się automatycznie na inne pola ani potomków. `basis` wskazuje
dowody, autora, datę, uzasadnienie, ograniczenia i artefakt decyzji.

Zmiana zaakceptowanego twierdzenia wymaga decyzji o nowej rewizji.
Akceptacja niezmienionej rewizji może być użyta w kolejnym snapshocie,
o ile nie zmieniły się jej zależności i zakres stosowania. Akceptacja
pojedynczego twierdzenia pozostaje lokalna; wynik sytuacji trzeba sprawdzić
ponownie po zmianie jej podstawy.

Sprzeczne decyzje pozostają w historii. Zastąpienie wskazuje
`supersedes_review_ids` i wymaga jawnego uzasadnienia; późniejsza data sama
nie rozstrzyga konfliktu. Obserwacje walidatora i modelu nie stają się
decyzjami człowieka.

## Pokrycie i pomiary

`coverage` rozlicza ustalony inwentarz regionów. `represented`, `partial`,
`unprocessed` i `excluded` opisują reprezentację w danym wyniku;
`excluded` wymaga jawnego powodu i zatwierdzonej granicy zakresu.
Pokrycie nie jest oceną poprawności znaczenia.

Osobno liczymy oznaczenia, klauzule, tabele, diagramy, twierdzenia,
zaakceptowane zakresy i rozstrzygnięte zależności. Kilka reprezentacji tej
samej klauzuli nie zwiększa liczby poprawnie pokrytych klauzul.
Pełna instrukcja wymaga inwentarza wszystkich stron i materiałów w zakresie,
w tym wprowadzeń, not i kontynuacji bez numeru reguły.

Ocena jakości pozostaje w osobnym zestawie `evaluation`, poza kontekstem
ekstraktora. Wynik oceny wskazuje snapshot, hashe odpowiedzi i wersję
oczekiwań. Zmiana IG nie zmienia zamrożonego gold.
`runs.measurement` rozdziela czas operatora, modelu i czas kalendarzowy.
Nieznane wartości są null ze stanem `unknown`, nigdy zerem.

## Snapshot i warianty instrukcji

`snapshots.profile` określa grę, wydanie, obowiązujące materiały,
wybrane warianty i opcjonalny scenariusz. Profil wskazuje decyzje o zakresie
i pierwszeństwie źródeł. Errata i reguła bazowa pozostają odrębnymi zapisami;
przyjęta modyfikacja jest widoczna w relacji i zestawie twierdzeń.

Pole `profile` zawiera przypięte odwołanie do rekordu `profiles` oraz
konfigurację `rules_mode`, `option_ids`, `scenario_id` i zestawu map/żetonów.
Definicja profilu opisuje reguły i możliwości, a nie bieżącą pozycję partii.
Stan sytuacji wejściowej i jej historia są osobnymi danymi zapytania lub
oceny, przypiętymi do snapshotu; nie stają się twierdzeniami instrukcji.

`selected_refs` wylicza każdą wybraną rewizję z hashem, włącznie z dowodami
i decyzjami. Jeden snapshot wybiera najwyżej jedną rewizję każdego ID.
Może zachować konkurencyjne twierdzenia o różnych ID jako konflikt.
`conflicts` wskazuje grupy sprzecznych twierdzeń, zakres i brakujące decyzje.
Wybór nowszej odpowiedzi nie rozstrzyga ich automatycznie.

Snapshot z lukami jest poprawnym zapisem częściowego grafu.
Przed użyciem do konkretnego rozstrzygnięcia zapytanie musi zwrócić
wykorzystane twierdzenia, ścieżki zależności, dowody, review i blokady.
Ocena tej odpowiedzi nie certyfikuje innych zapytań ani całego snapshotu.

## Roboczy zapis plików w repozytorium

Proponowany przyszły układ danych prywatnych:

```text
private/ig/<game>/<edition>/
  sources/<source-id>/manifest.json
  sources/<source-id>/artifacts/...
  runs/<run-id>/run.json
  runs/<run-id>/prompt.txt
  runs/<run-id>/response.raw.txt
  records/<collection>/<record-id>/<revision-id>.json
  snapshots/<snapshot-id>/manifest.json
  reports/<snapshot-id>/...
  evaluation/<evaluation-id>/...
```

Nazwy katalogów muszą mieć bezpieczne mapowanie z logicznych ID; dwukropki
w przykładach nie przechodzą bezpośrednio do nazw plików na Windows.
Jeden rekord na plik ułatwia przypięcie dowodu lub decyzji do dokładnych
bajtów. Zestaw ekstrakcji może być przekazywany jako pojedynczy JSON;
jego rozdzielenie zachowuje surową odpowiedź i mapę pochodzenia.

Manifest snapshotu wylicza pliki, ID, rewizje, wielkości i pełne SHA-256.
Ma stan `draft` lub `sealed`; sealed wymaga spójności referencji i hashy.
Nie oznacza jakości semantycznej. Wskaźnik bieżącego snapshotu jest osobnym
plikiem; wcześniejsze manifesty pozostają niezmienne.

To propozycja formatu wymiany i organizacji plików. Wybór bazy danych,
indeksów, transakcji i wykonawcy reguł wymaga osobnej decyzji po pomiarach.

## Budowanie grafu pełnej instrukcji

1. Zidentyfikować wydanie i dostępne materiały; utworzyć inwentarz źródeł,
   regionów, oznaczeń, tabel, diagramów i not.
2. Ekstrahować kompletne jednostki treści w ograniczonych pakietach.
   Pakiet wskazuje regiony właściwe i kontekst; powtórzony kontekst nie
   zwiększa pokrycia instrukcji.
3. Utworzyć propozycje obiektów, twierdzeń i relacji z dowodami.
   Odwołania do nieprzetworzonych rozdziałów zachować jako kandydatów.
4. Rozstrzygać kandydatów na podstawie indeksu oznaczeń i treści celu.
   Połączenie przez sam numer jest propozycją wymagającą sprawdzenia.
5. Kontrolować format i integralność, następnie przedstawić człowiekowi
   konkretne twierdzenia, konflikty i ich źródła.
6. Budować snapshot z jawnym pokryciem i lukami. Sprawdzać sytuacje
   między rozdziałami oraz wpływ korekt na wcześniej poprawne wyniki.

Pełny graf może powstawać stopniowo. Dostępność większej liczby źródeł
nie nadaje akceptacji znaczeniu, a akceptacja kilku rozdziałów nie
certyfikuje pozostałych.

## Kontrole proponowanego kontraktu

Przyszły walidator powinien sprawdzać:

- Unikalność ID i rewizji, hashe, referencje oraz zgodność manifestu.
- Stan niewiedzy z luką, stany braku z uzasadnieniem i zakres dowodów.
- Jawnego kandydata i lukę dla nierozstrzygniętych lub niejednoznacznych celów.
- Rodzaj i kierunek relacji, zakres warunku oraz kompletność grup wymagań.
- Osie, komórki, scalenia i noty tabel; jednostki, operatory i timing.
- Przypięcie decyzji do konkretnych rewizji i brak akceptacji modelowej.
- Rozliczenie wszystkich regionów zakresu, duplikaty i konflikty.

Przegląd znaczenia powinien sprawdzić co najmniej: klauzulę na dwóch
stronach, wyjątek z innego rozdziału, tabelę z notą, nieznaną jednostkę,
cykl procedur, konflikt wydania i erraty, brak źródła scenariusza,
częściową akceptację oraz regresję po zmianie wcześniej przyjętego warunku.
Każdy przypadek musi mieć źródłowo uzasadniony wynik lub blokadę.

## Decyzje do recenzji i prób IG

| Pytanie | Sposób sprawdzenia |
|---|---|
| Czy twierdzenie jest właściwą jednostką korekty i akceptacji | Odwzorować jeden pakiet korekt bez utraty wcześniejszych decyzji i wykryć zmienione zakresy |
| Czy podział na klauzule i obiekty tabel jest wystarczający | Sprawdzić trudne sytuacje oraz koszt dokładnego powiązania dowodów |
| Ile struktury logicznej potrzeba | Sprawdzić, co da się ocenić z tekstu, a co wymaga jawnych warunków, czasu i grup zależności |
| Czy model pokrywa różne części instrukcji | W kolejnym zatwierdzonym eksperymencie użyć innego rodzaju rozdziału i zależności między rozdziałami |
| Jak ograniczyć pracę operatora | Mierzyć czas review i przygotowania korekt osobno; przedstawiać dokładne zmiany z ich źródłami |
| Czy przyjąć kontrakt i rozpocząć implementację | W IG-0 i kolejnych próbach porównać zakres, jakość, regresje, pokrycie i koszt, a następnie zapisać decyzję właściciela |

Rekomendowany pierwszy zakres wdrożenia po przyjęciu: źródła i dowody,
obiekty, twierdzenia, relacje, luki, review oraz manifest snapshotu.
Formalny wykonawca procedur i zapytań o wynik gry wymaga późniejszego,
osobno sprawdzonego kontraktu.

## Zmiany po przeglądzie mechanik

Wersja 0.2 dodaje profile systemów, kwalifikowane odwołania, typy obiektów
mechanicznych i aspekty twierdzeń. Rozszerzenie określa przyczynę zdarzenia,
pamięć działań, przerwania i powroty, wybory utrzymywane między krokami,
polityki przestrzeni, tabele wieloetapowe i jawne zasady obliczeń.
Plan sprawdzenia oraz bibliografia są w
[IG-MECHANICS-PROFILES](IG-MECHANICS-PROFILES.md).
To rozszerzenie propozycji, nie wynik ekstrakcji ani zaliczenie testów mechanik.
