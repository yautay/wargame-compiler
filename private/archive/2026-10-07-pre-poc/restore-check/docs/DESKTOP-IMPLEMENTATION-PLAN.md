# Plan implementacji: ekstrakcja przez aplikację desktopową

- **Data:** 2026-10-06
- **Decyzja:** [ADR-0037](adr/ADR-0037-ekstrakcja-desktop-bez-api.md), uzgodniona z właścicielem.
- **Stan:** plan przyjęty; minimalne kontrakty opisuje [DATA-CONTRACTS §11](DATA-CONTRACTS.md#desktop).
- **Punkt startowy sesji:** [STATUS](STATUS.md) i [HANDOFF](HANDOFF.md). Statusy wykonania prowadzi wyłącznie [ROADMAP](ROADMAP.md).

## 1. Cel i granice

Przetworzyć złożoną instrukcję PDF w sprawdzalną strukturę dokumentu, następnie w reguły KB z dowodami.
Przebudowujemy istniejące narzędzie, zachowując walidację i bezpieczny zapis. Premium pracuje w ChatGPT lub
Claude Desktop. Nie implementujemy klientów API inferencji, kluczy API, endpointów ani automatycznego fallbacku
do API. Lokalny LLM jest opcjonalnym wykonawcą pomocniczym przez proces i pliki; infrastruktura LAN nie jest
zależnością. Nie zakładamy, że aplikacje desktopowe mają identyczny dostęp do plików czy integracji.

Minimalna droga użytkowa to jawny eksport pakietu, przekazanie go w aplikacji, zapis odpowiedzi i import pliku.
Nie wymaga sterowania GUI, Codex CLI ani MCP. Ewentualne ułatwienia desktopowe mogą później używać tego samego
kontraktu, dopiero po sprawdzeniu dostępnych możliwości. Nie budujemy automatyzacji interfejsu w tym planie.

Pierwszy cel to poprawny, mały przebieg, nie pełna digitalizacja gry ani publikacja przekładu.
Brak rozstrzygnięcia pozostaje jawną luką. Treść instrukcji jest materiałem źródłowym, nie poleceniami dla wykonawcy.

## 2. Co wykorzystujemy

| Element | Postępowanie |
|---|---|
| `wgc/contracts.py`, identyfikatory, kanonizacja, walidatory | Zachować; rozszerzać kontrakty z fixture'ami, testami i DATA-CONTRACTS w tej samej sesji |
| `wgc/kb.py`, `fsio.py`, `fsbatch.py`, manifesty i ownership | Zachować kontrolowaną akceptację, blokady i recovery; nie tworzyć drugiego sposobu zapisu KB |
| `wgc/ingest/pdf.py`: render i surowy odczyt | Wykorzystać jako przygotowanie dowodów, bez uznawania heurystycznej segmentacji za prawdę |
| Markdown i istniejące zadania Tier 0 | Zachować działanie i regresje |
| `pdf_hybrid.py`, przygotowanie/replay ADR-0036 | Zachować jako legacy do porównań; nowy format obok, bez dalszego rozbudowywania kontraktu opartego na każdym słowie |
| `glu.store`, planner, receipt i reconcile | Włączyć po przejściu pilota; nie uzależniać pierwszego eksportu/importu od nowej orkiestracji |
| Gateway, API providerów, wielopoziomowy routing | Nie realizować według starej roadmapy |

## 3. Docelowy przebieg

```text
PDF + surowy tekst + rendery
  -> pakiet stron z kontekstem i manifestem (kod)
  -> propozycja struktury dokumentu (premium w aplikacji)
  -> import, dopasowanie tekstu, kontrola pokrycia, raport (kod)
  -> przegląd i trwała zatwierdzona rewizja dokumentu
  -> pakiet sekcji i jej zależności -> propozycja reguł/relacji (premium)
  -> walidacja i przypadki kontrolne -> akceptacja KB
  -> opcjonalna niezależna kontrola lokalnym LLM i pakiet rozbieżności
```

WGC określa format i poprawność danych, GLU odpowiada za wykonanie i kolejkę. Adapter wymiany plikowej nie
interpretuje zasad gry. Warstwy Stage 1, 1.5, 2 i 3 pozostają; znacząca struktura wizualna jest odczytywana już
przed Stage 1. Dobór kroju pisma i skład publikacji nadal należą do późniejszych etapów.

## 4. Minimalny model dokumentu i dowodów

Poniższe wymagania projektowe mają minimalny schemat `wgc/desktop@0` od M-DESK1
([ADR-0038](adr/ADR-0038-minimalne-kontrakty-desktop.md)). CLI eksportu/importu należy do M-DESK2/3.

- Dokument ma hash oryginalnego pliku, numer strony PDF oraz osobną etykietę strony drukowanej.
- Bloki: nagłówek, akapit, lista i jej pozycje, tabela, ramka, ilustracja/diagram, podpis, nota, przykład.
  Hierarchia i kolejność czytania są osobnymi relacjami. Numer wydrukowanej reguły nie jest tożsamością bloku.
- Powiązania obejmują kontynuację między stronami/kolumnami, podpis ilustracji, legendę i zakres obowiązywania
  wynikający z koloru lub ramki. Cechy wizualne o znaczeniu dla zasad wchodzą do zależności semantycznych.
- Dowód tekstowy wskazuje surowe fragmenty z warstwy PDF; kod rekonstruuje tekst i dokładne obwiednie.
  Model podaje grupowanie i kolejność, nie przepisuje obowiązkowo tekstu oraz wszystkich ID słów.
  Fragmenty mogą wymagać podziału; nie zakładamy nieomylności wstępnego grupowania przez kod.
- Dowód obrazowy wskazuje stronę/obszar, hash obrazu i jawną transkrypcję lub opis. Transkrypcja z obrazu,
  odczyt tekstowy i interpretacja diagramu są odróżnialne. Rozbieżność z warstwą PDF jest zapisana, nie ukryta.
- Diagram zachowujemy jako źródło wizualne; opis modelu nie zastępuje oryginału ani nie staje się automatycznie
  regułą. Na pierwszy pilot nie budujemy uniwersalnego parsera heksów i żetonów.
- Tabela zachowuje komórki, nagłówki, przypisy i scalanie, jeśli występują. Liczba wierszy sama nie decyduje
  o tym, czy obiekt jest tabelą. Pełna normalizacja nietypowej tabeli może pozostać jawnym zadaniem przeglądu.
- Każdy obszar źródła ma klasyfikację: treść, świadomie pominięty element z powodem albo luka. Pokrycie warstwy
  tekstowej i przegląd widocznych elementów są odrębnymi kontrolami.
- W obrębie niezmienionego pakietu ID są stabilne i import jest idempotentny. Nowe wydanie lub zmieniony podział
  wymagają jawnej mapy zmian; nie obiecujemy automatycznej stabilności ID między dowolnymi wydaniami.

## 5. Pakiet, import i przegląd

Pakiet zawiera manifest (wersja, zadanie, hash źródła, zakres docelowy i kontekst, wersja instrukcji i schematu),
rendery/PDF wybranych stron, pomocniczy tekst, legendę dokumentu i przykład odpowiedzi. Kontekst sąsiedniej strony
nie jest dodatkowym zakresem zapisu: nakładające się pakiety nie mogą produkować dwóch właścicieli tego samego bloku.
Wielkość partii ustala pilot na podstawie gęstości, z pierwszą próbą na 2 sąsiednich stronach; nie wysyłamy
automatycznie całej instrukcji ani nie zakładamy stałego limitu aplikacji.

Odpowiedź wiążemy z ID i hashem pakietu. Import rozdziela błędy formatu, nieaktualne wejście, brak odpowiedzi,
niekompletność i wątpliwość merytoryczną. Zła odpowiedź nie zmienia zatwierdzonego wyniku. Naprawa dotyczy wskazanego
obszaru; wcześniejsze poprawne odpowiedzi są zachowane. Rejestrujemy aplikację i nazwę modelu, o ile są dostępne;
brak informacji pozostaje `unknown`, a deklaracja użytkownika/modelu nie jest fingerprintem od dostawcy.

Stan bloku rozdziela co najmniej: propozycję, poprawność strukturalną, oczekiwanie na przegląd, zatwierdzenie
i nieaktualność. Przejście walidatora nie oznacza potwierdzenia znaczenia. W pierwszym pilocie zatwierdzenie
merytoryczne jest jawne po porównaniu z renderem. Automatyczne akceptowanie wymaga późniejszej kalibracji.

Raport pokazuje obok siebie stronę, bloki, kolejność, tekst/transkrypcje, tabele, dowody i problemy. Użytkownik
poprawia mały pakiet albo zatwierdza zakres; nie musi edytować list tysięcy ID słów. Otwarta luka blokuje
zależne reguły; niezależne fragmenty można zapisać. Cały dokument nie dostaje statusu kompletnego, dopóki
istotne luki i zależności pozostają otwarte.

## 6. Trwałość, prywatność i migracja

- Oryginały, surowe odpowiedzi i zaakceptowane rewizje dokumentu są trwałymi prywatnymi artefaktami w repo gry
  (katalog ignorowany przez git) albo w skonfigurowanym prywatnym magazynie. Nie są cache `.glu/`.
- Domyślna proponowana lokalizacja to `private/source-artifacts/` w projekcie gry. M-DESK1 ustala układ;
  M-DESK3 dostarcza eksport/odtworzenie rewizji z kontrolą hashy. Sam `.gitignore` nie jest kopią zapasową.
- Repo narzędzia nie przechowuje tekstów ani obrazów komercyjnych instrukcji. Commitowane metadane w projekcie
  gry wskazują hash i wersję artefaktu, nie zawierają pełnego tekstu. Materiały testowe w repo są własne/CC0.
- Usunięcie cache nie wymusza kolejnej sesji z modelem. Brak trwałego artefaktu daje diagnostykę i odtworzenie
  z eksportu; nie uruchamia modelu i nie udaje identycznego wyniku.
- Nowa ścieżka jest jawnie wybierana. Nie migrujemy istniejącej KB ani inwentarza po cichu. Przed przełączeniem
  powstaje diff ID/hashów i lista zależnych rekordów. Q-12 (stale), Q-16 (ownership pojęć) i Q-17 (główne źródło)
  muszą być rozstrzygnięte dla wybranego zakresu, zanim zapis dotknie istniejącej gry.
- Wczesny pilot używa nowego prywatnego projektu, bez modyfikacji starych wyników. Wycofanie oznacza powrót
  do poprzedniej zatwierdzonej rewizji; nie kasuje odpowiedzi, dowodów ani historii przeglądu.

## 7. Etapy i kryteria odbioru

Każdy etap kończy się testami, aktualizacją STATUS/ROADMAP i handoffem. Jeśli zakres nie mieści się w jednej
ograniczonej sesji, podzielić etap przed implementacją. Bez uruchamiania późniejszych etapów na zapas.

| Etap | Wynik | Kryterium odbioru |
|---|---|---|
| M-DESK0 | Plan i ADR; zastąpienie starej ścieżki wykonania | Spójne dokumenty kontynuacji; bez zmiany kodu runtime |
| M-DESK1 | Minimalne kontrakty pakietu, odpowiedzi i dokumentu; własny przykład 2 stron | Fixture obejmuje kolumny, kontynuację, ramkę zakresu i tekst w obrazie; poprawne/niepoprawne przykłady przechodzą testy; status nie myli walidacji z review |
| M-DESK2 | Eksport pakietu i krótka instrukcja pracy w obu aplikacjach | Powtarzalny manifest, sąsiedni kontekst, brak komercyjnej treści w repo; ręczna próba przekazania/odebrania pakietu w co najmniej jednej aplikacji, ograniczenia drugiej jawnie zapisane |
| M-DESK3 | Import i prywatny magazyn rewizji | Walidacja, deduplikacja, stary/obcy pakiet odrzucony; round-trip eksportu i odtworzenie po utracie cache bez modelu; awaria zapisu nie psuje poprzedniej rewizji |
| M-DESK4 | Podgląd, przegląd fragmentu i pakiet poprawkowy | Można obejrzeć i zatwierdzić fragment, zachować luki i poprawić jeden obszar; niesprawdzona transkrypcja nie trafia do zatwierdzonych dowodów |
| M-DESK5 | Pilot struktury dokumentu i raport jakości | Kryteria sekcji 8; decyzja kontynuować/poprawić oparta na wynikach; Q-11 zamykana tylko w sprawdzonym zakresie |
| M-DESK6a | Pakiet semantyczny i propozycje Rule IR | Jeden fragment z regułą, wyjątkiem, limitem i odsyłaczem; trace do tekstu/obrazu; pozytywny i negatywny przypadek kontrolny ocenione względem źródła |
| M-DESK6b | Kontrolowany zapis propozycji do KB i obsługa rewizji pilota | `accept()` pozostaje jedyną granicą; przestarzały pakiet nie nadpisuje KB, niepotwierdzony dowód odrzucony; wskazane zależności po zmianie źródła blokowane, brak akceptacji na starej rewizji |
| M-DESK7 | Włączenie wymiany plikowej do GLU | Eksport -> oczekiwanie na odpowiedź -> import -> review -> akceptacja; restart i podwójny import nie dublują wyników; brak odpowiedzi nie powoduje wywołania API |
| M-DESK8 | Opcjonalny lokalny kontroler przez proces/pliki | Ślepa ekstrakcja kontrolna na części korpusu; wykryte błędy, fałszywe alarmy i czas porównane z wariantem bez niego; awaria workera nie blokuje bazowego przebiegu |
| M-DESK9 | Migracja i aktualizacja dalszej roadmapy | Jawny diff i odwracalne przełączenie przykładowego projektu; decyzja o wycofaniu legacy dopiero po regresjach; dalsze M3–M28 przepisane dla desktopu, bez przywracania API |

M-DESK8 nie jest zależnością M-DESK9. M-DESK6b nie wymaga pełnego grafu M13: dopuszczalna jest konserwatywna blokada
dotkniętego zakresu i jawna regeneracja, z opisanym ograniczeniem. Nie wolno jej zastąpić pominięciem kontroli stale.

## 8. Pilot i pomiar jakości

Wybrać 12–18 stron z trzech dostarczonych prywatnych instrukcji: dwie kolumny, przejście między stronami,
lista i numer reguły o tej samej etykiecie, tabela z wielowierszowymi komórkami, przypis, ramka/kolor określające
zakres, diagram z podpisem i tekst wyłącznie w obrazie. Ścieżki, hashe i strony zapisać w prywatnym manifeście
pilota poza repo narzędzia. Nie wybieramy automatycznie gry do pełnej digitalizacji (Q-02 pozostaje otwarta).

Przed oceną wyników przygotować ręcznie sprawdzoną listę oczekiwanych bloków, kolejności, powiązań i elementów
krytycznych. Część próbki zachować jako kontrolną po ustaleniu promptu. Te same strony oceniać tym samym rubric;
nie porównywać nowego modelu na łatwiejszej próbce ze starym na trudniejszej. Porównanie obu aplikacji ma sens
tylko przy dostępności obu; przy jednej raport nie rozstrzyga, która jest lepsza.

Mierzyć osobno wynik pierwszej odpowiedzi i wynik po korekcie:

- kompletność bloków i znaczących obszarów obrazowych; fałszywe bloki i wyłączenia;
- kolejność i kontynuacje, hierarchię oraz przypisanie wyjątków i zakresów;
- dokładność liczb, operatorów granicznych, negacji i komórek tabel;
- poprawność dowodów i transkrypcji; brak zgadywania brakujących treści;
- liczbę sesji/pakietów, nieudanych wymian, poprawek, czas użytkownika i czas całkowity;
- aplikację, dostępną nazwę modelu, wersję promptu i wejść; tokeny/limity tylko gdy widoczne;
  nieznane zużycie i koszt to brak danych, nie zero USD.

Warunek przejścia do M-DESK6a: wszystkie krytyczne elementy próbki mają poprawny, zweryfikowany wynik,
brak niewskazanych pominięć, błędów zakresu i niepopartych dopowiedzeń, wszystkie pozostałe obszary są rozliczone.
Otwarte kwestie muszą być jawne i wyłączone z zależnego zatwierdzonego zakresu. Raport obejmuje także liczbę
poprawek i czas: jeśli nadal wymagana jest ręczna rekonstrukcja większości stron, poprawić pakiet/kontrakt,
zamiast rozbudowywać GLU. Sukces na próbce nie dowodzi obsługi całego dokumentu ani wszystkich instrukcji.

Testy CI są offline i używają własnych PDF-ów, fixture'ów oraz replay. Testy modelowe są osobnym ręcznym pilotem.
Nie dodajemy zależności sieciowych/GPU do `python -m pytest`.

## 9. Rola lokalnego modelu

Najpierw działa wariant desktop premium + kod. Lokalny model później może niezależnie wyodrębniać warunki,
limity i wyjątki, proponować terminy i wskazywać rozbieżności. Dostaje źródło przed odpowiedzią premium,
jeżeli zadanie ma być niezależną ekstrakcją. Sam zgodny wynik dwóch modeli nie jest dowodem poprawności.

Lokalny worker nie nadaje akceptacji, nie nadpisuje KB i nie ma prawa rozstrzygać niejasności domenowych.
Wyniki są oznaczone rolą wykonawcy i trafiają do przeglądu. Zadanie opcjonalne można pominąć z jawnym powodem;
jeśli w przyszłości dana kontrola stanie się obowiązkowa, jej niedostępność pozostawia zakres oczekujący.
Brak GPU nie uruchamia API. Wybór modelu i runtime'u nastąpi po pomiarze M-DESK8, nie w tej sesji.

## 10. Następna sesja: M-DESK1

Instrukcję pierwszej sesji wykonano w [handoffie M-DESK1](handoff/2026-10-06-M-DESK1.md).
Bieżący punkt startowy kolejnej sesji wskazują STATUS i HANDOFF; poniżej pozostaje zakres pierwszego kroku.

1. Przeczytać CLAUDE, STATUS, ostatni HANDOFF, ten plan i ADR-0037.
2. Sprawdzić `git status`; zachować istniejące zmiany pilota Q-11. Bez commita/pusha bez prośby właściciela.
3. Przeczytać `wgc/ingest/__init__.py`, `pdf_hybrid.py`, `wgc/source.py`, schematy source/common/proposal,
   `wgc/contracts.py` i `tests/test_ingest_pdf_hybrid.py`.
4. Przygotować własny dwustronicowy przykład i minimalne poprawne/niepoprawne odpowiedzi; ustalić kontrakty
   dowodów i rewizji. Nie projektować jeszcze pełnej platformy analizy dokumentów.
5. Zaktualizować schematy, fixture'y, DATA-CONTRACTS i testy razem. Nie implementować w tej sesji eksportera,
   importera, lokalnego workera ani migracji komercyjnych źródeł.
6. Uruchomić pełne testy i test ciągłości, zaktualizować roadmapę oraz handoff z konkretnym poleceniem startowym.

Kwestie do rozwiązania w swoim etapie: dokładny kształt kontraktów i rozdział metadanych prywatnych (M-DESK1),
praktyczny transfer plików w aplikacjach (M-DESK2), ergonomia i budżet korekt (M-DESK4/5), dowody wizualne w kotwicach
KB oraz Q-12/Q-16/Q-17 (M-DESK6), przydatność lokalnego kontrolera (M-DESK8).
