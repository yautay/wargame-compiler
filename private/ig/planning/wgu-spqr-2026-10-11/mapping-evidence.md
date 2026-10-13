# Podstawa planu: KB SPQR i WGU

Data: 2026-10-11. Inspekcja do projektu architektury, nie pełny import
ani ponowne zatwierdzenie znaczenia KB. Publiczna architektura:
`docs/IG-WGU-ARCHITECTURE.md`.

## Wejścia i metoda

KB: `C:/repo/wargame-projects/games/spqr/kb/`.
Konfiguracja: `C:/repo/wargame-projects/games/spqr/wgu.yaml`.
WGU: `C:/repo/wargame-utils/`.

Pełny odczyt: schemat `wgu/schemas/kb.schema.json`, `wgu/kb/store.py`,
`export.py`, `lint.py`, konfiguracja gry i manifest KB; dokumentacja
README, ARCHITECTURE, DIGITALIZACJA i opis atomizacji jako materiał
projektowy, bez uruchamiania tego workflow.

Odczyt fragmentów: reguły rozdziału 7, procedury, tabele, relacje, terminy,
niejasności, pytania kontrolne i zmiany. Nie przeczytano ponownie całej KB
ani pełnej instrukcji. Deklaracja manifestu o pełnym odczycie przez jego
autora nie jest odczytem wykonanym w tej sesji.

`inspect_inputs.py` wylicza hashe wszystkich plików KB i konfiguracji oraz
liczniki według zaobserwowanego układu tekstu YAML. Wynik:
`input-inventory.json`. To nie jest parser YAML ani walidator WGU.
Brak PyYAML w dostępnych interpreterach; pozyskanie zależności nie powiodło
się z powodu DNS. Nie uruchomiono `wgu kb lint`, nie deklarujemy zgodności
schematu. Git dla sąsiednich repo zwrócił Permission denied; commit i stan
dirty są unknown. Hashe bajtów są dostępne. Nie zmieniano sąsiednich repo
ani globalnej konfiguracji Git.

Inwentarz: 523 reguły (438 podstawowe + 85 z księgi scenariuszy), 134 terminy,
48 tabel, 11 procedur głównych i 4 podprocedury, 80 kroków, 233 relacje,
79 niejasności, 3 zmiany, 59 pytań kontrolnych. Razem 1090 pozycji głównych.
Wszystkie reguły mają source, żadna digital. 226 relacji ma verified.
48 tabel ma complete: true. Terminy nie mają jawnych ID. Liczniki nie są
dowodem poprawności zawartości.

36 skonfigurowanych materiałów (instrukcja, 34 karty/obrazy i księga
scenariuszy) jest nieobecnych pod wskazanymi ścieżkami. Nie oznacza to,
że właściciel nie posiada kopii w innym miejscu.

Kandydat instrukcji rozwiązany przez manifest archiwum:
original_path `private/poc/spqr-chapter9/source/original-pdf-20261008-01.pdf`;
archive_path zapisany w inwentarzu. SHA-256:
`e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.
44 strony według inspekcji IG-0; hash ponownie zgodny. KB nie ma hasha
pierwotnego PDF, więc nie potwierdzono identyczności bajtów. Nowy IG może
użyć tego PDF jako jawnie wybranego źródła do uzgodnienia opracowania WGU.
Archiwum pozostaje niezmienione.

## Konkretne mapowania projektowe

Lokalizatory poniżej są deklaracjami KB, nie nowo zweryfikowanymi dowodami PDF.
Propozycje nie mają akceptacji semantycznej ani wydanych ID IG.

### R-7.15.1 i R-7.15.2: klauzule oraz wyjątek

Plik: `kb/rules/07-ukierunkowanie-zoc.yaml`. R-7.15.1 ma when, effect
i exceptions: wyzwalacz reakcji, warunek braku innej wrogiej ZOC, ograniczenie
użycia, test, dalszy ostrzał i przypadek stosu. R-7.15.2 opisuje wyjątek
dla jazdy wobec piechoty.

Mapowanie: zewnętrzne ID WGU prowadzi do klauzuli z adresami trigger,
eligibility, action, use-limit, check, continuation i stack-case. Aspekty
zachowują tekst WGU; grupy semantyczne wiążą warunki z akcją/testem.
Osobna klauzula wyjątku wskazuje aspekt testu i skutków, nie automatycznie
całą regułę. Odwołania do ostrzału są najpierw nawigacją; typowanie wymaga
odczytu źródeł. Dowód ma objąć klauzule i Play Note, nie tylko stronę 20.

Nie wystarcza import 1:1 do atomu: effect zawiera powiązane twierdzenia.
Nie trzeba też osobnego rekordu i decyzji dla każdego pola: całość jest
pakietem review z adresowalnymi aspektami.

### P-05: procedura i wybory

Plik: `kb/procedures.yaml`. Zachować 12 kroków P-05, podprocedurę P-05a,
numery, znaczniki i refs. Krok 6 opisuje wybory uczestników do tabeli
starcia; kolejne kroki odnoszą się do przewagi, przesunięć, rzutu i trafień.
Lista sama nie określa trwałości wszystkich wyborów ani parametrów P-05a.

Najpierw procedura z lokalnymi stabilnymi ID kroków i kolejnością deklarowaną
przez KB. Po uzgodnieniu: dowody dla kroków, opis wyborów, wywołań i powrotów.
Nierozstrzygnięte binding/resume-point to luki formalizacji. Nie zakładać,
że wybór z jednego kroku obowiązuje wszystkie następne. Nie wykonywać gry.

### T-01 i tabele kart

T-01 z `kb/tables.yaml` jest opracowaniem o kości i testach z kilku miejsc
instrukcji. Nie musi być literalną tabelą z PDF. Odróżniać editorial_summary
od publisher_table/transcription. Wiersze/komórki mają adresy i właściwe
podstawy; nie tworzyć fikcyjnego regionu PDF dla całego zestawienia.

T-20…T-29 i pozostałe karty wymagają własnych źródeł. complete: true
oznacza deklarację kompletności opracowania; N-01 nadal wskazuje mieszane
wydania. Nie dziedziczyć 5E z manifest.game na wszystkie wartości tabel.
Zgodność przykładów liczbowych nie dowodzi tożsamości tabel.

### N-01, reguły scenariuszy i Q: różne role

N-01 w `ambiguities.yaml` opisuje braki i ryzyka materiałów; status open.
Przenieść do luk źródłowych/zgodności, zachować wspólne pochodzenie i
rekomendację autora. probable nie jest decyzją o współstosowaniu wydań.

`rules/12-scenariusze-ksiega-2018.yaml`: 85 reguł księgi 4E z 2018 r.
Importować z oddzielnym profilem i statusem zgodności z 5E. To nie jest
część 44-stronicowej instrukcji podstawowej.

Q-01 w `scenarios.yaml` to pytanie z odpowiedzią i łańcuchem odwołań.
Mapować na acceptance_case/imported_answer, nie battle_scenario.
Odpowiedź to materiał do sprawdzenia i regresji, nie niezależny expected.

### C-01 i aktualizacja

C-01 w `changes.yaml` opisuje zmianę wydania z odwołaniem do R-7.24.1.
Importować deklarację zmiany; nie tworzyć automatycznie pełnej poprzedniej
wersji reguły, której źródła nie ma.

Zmiana R-7.24.1 w WGU po korekcie WGC wymaga porównania starego WGU,
nowego WGU i bieżącego WGC. Konflikt wymaga propozycji rozstrzygnięcia.
Review innego, niezależnego pola może pozostać aktualne, ale niekompletna
lista jego podstaw daje unknown.

## Pułapki adaptera wynikające z kodu

- source_rev eksportera to krótki commit, bez identyfikacji zmian dirty.
- Bundle pomija pełny wgu.yaml, notes/overview.md i terminology.yaml.
  Import katalogu rozlicza te pliki; bundle potrzebuje sidecarów lub luk.
- source.pages jest tekstem, nie potwierdzonym indeksem PDF.
- known() akceptuje wildcard .x i część sufiksów podpunktów. IG potrzebuje
  dokładnego celu lub jawnego nierozstrzygniętego zakresu.
- Pola opcjonalne i rozszerzenia schematu nie mogą znikać przy imporcie.
- Referencje w wolnym tekście mogą nie występować w refs.
- Relacje i terminy bez ID oraz lokalne numery kroków wymagają rejestru
  mapowania do obsługi aktualizacji bez utraty review.

Nie wykonano atomizacji, semantycznego importu ani pełnego IG. Powstały
architektura, plan etapów, karta IG-1, przykłady mapowania i inwentarz wejść.

Późniejsze doprecyzowanie właściciela: celem są szybkie, deterministyczne
legalne akcje dla przeciwnika AI, bez zużywania kontekstu na legalność.
Dodano docs/IG-LEGAL-ACTIONS.md i rozszerzono plan o formalizację oraz
kompilację. Opisane wyżej mapowania tekstowe są początkiem procesu;
nierozstrzygnięte wybory, kontynuacje i wartości potrzebne legalności
blokują gotowość wykonawczą. Sesja nadal obejmuje wyłącznie planowanie.
