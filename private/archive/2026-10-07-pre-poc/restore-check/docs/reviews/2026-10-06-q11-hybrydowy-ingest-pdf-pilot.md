# Q-11: pilot hybrydowego ingestu PDF — problemy i stan (2026-10-06)

## Zakres i prywatność

Sprawdzono 20 stron prywatnego pliku `C:\dev\game-test\dtp_rulebook.pdf` (SHA-256:
`1e851ff7c5468b3972ed9d95e2631634739030e34546588cc23e45c8ec02682d`). Oryginał był tylko odczytywany.
Ten raport zawiera wyłącznie metryki i diagnozy; nie zawiera tekstu ani obrazów wydawcy. Surowy raport i rendery leżą
w ignorowanym `.glu/dtp-ingest-test/.glu/source/SRC-dtp.rules/hybrid/`.

## Wynik

- Jawny ekstraktor `wgc.ingest.pdf.hybrid@2` (ADR-0036) przetestowano na wszystkich 20 stronach przez zalogowany
  Codex CLI, bez klucza API i bez GPU. Wariant `pdf@1` pozostał domyślny dla zwykłego PDF.
- Warstwa tekstowa dała 7450 słów; wszystkie niebiałe znaki PDF należały do wyodrębnionych słów na każdej z 20
  stron. Rendery wszystkich stron zostały obejrzane; strony 2, 4, 8, 13, 19 i 20 oceniono także pod kątem układu.
- **20/20 stron wymaga przeglądu; nie zatwierdzono segmentów.** Prywatny inwentarz wskazuje wybrany tryb hybrydowy,
  a `source verify` zgłasza brak zatwierdzonego artefaktu. Nie pojawia się błąd duplikatu etykiety `1` z `pdf@1`.
- Główny przebieg zmierzył **co najmniej 179 557 tokenów wejścia i 31 797 wyjścia**. Trzy późniejsze kontrole
  punktowe stron 4, 8 i 20 zużyły dodatkowo 94 598/15 217 tokenów. Nieudane wywołania mogły zużyć tokeny
  nieujęte w metrykach. Codex CLI nie podał kosztu pieniężnego; koszt USD pozostaje nieznany.

## Problemy wykryte w pilocie

1. **Niestabilne wywołania Codex CLI:** 17 stron skończyło z błędem providera także po jednym ponowieniu. Pojedyncze
   późniejsze wywołania reprezentatywnych stron mogły się powieść, więc błąd nie jest trwałą cechą tych stron.
   Raport pierwotnego przebiegu nie zawiera szczegółu stderr; nowszy kod zapisuje skróconą przyczynę w diagnostyce.
2. **Niezgodna propozycja strony 2:** walidator wykrył brak obszaru, niezgodność tekstu ze wskazanymi słowami,
   obszar nierozstrzygnięty i tekst widoczny tylko w obrazie. Strona nie została zaakceptowana.
3. **Katalog komponentów na stronie 20:** kontrola punktowa nie zaproponowała segmentów `rule`, ale utworzyła dwie
   fałszywe jednorzędowe `table`. Walidator wymaga teraz co najmniej dwóch wierszy i dwóch komórek w każdym
   wierszu oraz równej liczby komórek, więc te kandydaty wymagają przeglądu. Model zgłosił też trzy obszary tekstu
   tylko na obrazie; pagina była jawnie wyłączona z powodem.
4. **Tekst w grafikach:** oglądane rendery pokazują tytuły bez odpowiednika w warstwie tekstowej co najmniej na
   stronach 2, 4 i 19 oraz drobne napisy w ilustracjach. Sama kompletność 7450 słów nie dowodzi kompletności
   widocznej treści. Strony z takim tekstem wymagają przeglądu zamiast pustego segmentu OCR.
5. **Kryteria jakości niezamknięte:** brak zatwierdzonej propozycji uniemożliwia potwierdzenie kolejności kolumn
   na stronach 4, 8 i 13, list na stronach 2 i 4, wszystkich wyłączeń pagin oraz pełnego oznaczenia tekstu w
   obrazach. Wszystkie 20 stron pozostają niepewne.

## Testy i dalsza praca

Testy syntetyczne obejmują dwie kolumny, listę, tabelę, powtórzoną etykietę `1`, paginy, obszary na dwóch stronach,
pokrycie słów, tekst źródłowy, granice obszarów, komórki tabel, stronę bez warstwy tekstowej i replay. Działają
offline, bez modelu i GPU. `python -m pytest` oraz `tests/test_continuity.py` były zielone; wynik końcowego
przebiegu zapisano w stanie sesji.

Przed zamknięciem Q-11 należy przygotować poprawione propozycje wszystkich 20 stron z pakietów w `.glu`, sprawdzić
je przez `wgc source hybrid --replay-dir` i porównać zatwierdzone obszary z renderami, szczególnie na stronach
2, 4, 8, 13, 19 i 20. Q-11 pozostaje otwarta, a M10 nadal jest bieżącym milestone'em.
