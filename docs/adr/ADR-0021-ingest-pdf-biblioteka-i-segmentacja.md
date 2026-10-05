# ADR-0021: Ingest PDF na bibliotekach o licencjach liberalnych, segmentacja PDF i flagi wizualne

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M2b

## Kontekst
- ADR-0020 ustalił inwentarz Stage 0, segmentację Markdown i pola generowane segmentu (`pages`, `bbox`,
  `visual_flags`). Pola PDF czekały na M2b.
- Q-10: PyMuPDF jest na licencji AGPL-3.0 albo komercyjnej. Licencja repo narzędzia nie jest rozstrzygnięta (Q-05).
- Próba z biblioteką pdfplumber na PDF-ie zapisanym ręcznie (M2b) pokazała, że pdfplumber zwraca dla każdego znaku
  font, rozmiar, kolor wypełnienia i położenie, a także linie i prostokąty strony. Kolor przychodzi w natywnej
  przestrzeni barw, np. czarny jako `(0,)` w DeviceGray i czerwony jako `(1, 0, 0)` w DeviceRGB.
- Prawdziwe podręczniki oznaczają zmiany kolorem albo przekreśleniem. Przekreślenie bywa rysowane linią albo cienkim
  wypełnionym prostokątem.

## Decyzja
- **Biblioteki** (zależność wymagana w `requirements.txt` i `pyproject.toml`, z minimalnymi wersjami równymi
  przetestowanym):
  - `pdfplumber` (MIT, razem z `pdfminer.six`, MIT): znaki, kolory, linie i prostokąty;
  - `pypdfium2` (Apache-2.0/BSD-3): render strony;
  - `Pillow` (MIT-CMU): zapis PNG.

  PyMuPDF odpada ze względu na licencję. Testy nie używają biblioteki do generowania PDF: PDF-y buduje mały writer
  testowy `tests/pdfgen.py` (fonty base-14, WinAnsi), niezależny od testowanej biblioteki.
- **Ekstraktor `wgc.ingest.pdf@0`** (`wgc/ingest/pdf.py`) to czysta funkcja: bajty na wejściu, lista `Segment` na
  wyjściu. Rejestr `extractor_for` mapuje na niego rozszerzenie `.pdf`.
- **Wiersze:**
  - znaki grupuje się w wiersze według dolnej krawędzi (tolerancja 0,3 rozmiaru fontu);
  - wiersze czyta się od góry do dołu, więc obsługiwana jest jedna kolumna;
  - spacja to znak spacji albo przerwa większa niż 0,2 rozmiaru fontu;
  - przerwa większa niż 2 rozmiary fontu dzieli wiersz na komórki.
- **Segmentacja** według zasad ADR-0020:
  - **Nagłówek:** wiersz ma font większy niż 1,1 × rozmiar podstawowy, czyli najczęstszy rozmiar znaków niebiałych.
    - Kolejne wiersze tego samego rozmiaru tworzą jeden nagłówek, chyba że następny wiersz zaczyna się od numeru.
    - Liczba na początku nagłówka staje się etykietą.
    - Poziom nagłówka to ranga rozmiaru: największy rozmiar ma poziom 1.
  - **Numer reguły:** pierwsze słowo wiersza jest pogrubione (nazwa fontu zawiera `Bold`, `Black`, `Heavy`, `Semibold`
    albo `Demi`) i ma postać `N`, `N.N` itd.
    - Taki numer otwiera segment, który trwa do następnego numeru albo nagłówka.
    - Numer w zwykłym kroju, np. odsyłacz `3.4.` przeniesiony na początek wiersza, nie otwiera segmentu.
    - Pozycje list (`1. Rally Phase`) zostają w tekście.
  - **Typ segmentu:** segment, w którym co najmniej dwa wiersze mają kilka komórek, jest typu `table`. Inny numerowany
    segment jest typu `rule`, a treść bez numeru jest typu `other` z kluczem `u<n>`.
  - **Tekst:** etykieta nie należy do tekstu. Wiersze łączy się znakiem nowego wiersza, a komórki spacją. Tekst
    przekreślony zostaje w tekście („jak wydrukowany”) i dostaje flagę.
- **Pola układu:**
  - `pages` ma postać `"3"` albo `"3-4"` (pierwsza i ostatnia strona segmentu, numeracja od 1);
  - `bbox` to `[x0, top, x1, bottom]` w punktach, liczony od lewego górnego rogu **pierwszej** strony segmentu: suma
    jego wierszy na tej stronie, zaokrąglona do 0,1;
  - pola są zapisywane tylko dla formatów stronicowych, a puste `visual_flags` nie są zapisywane.
- **Flagi wizualne** liczy się ze znaków tekstu segmentu, bez etykiety (kolorowy albo przekreślony numer reguły nie
  daje flagi):
  - `changed_color`: kolor wypełnienia znaku jest inny niż kolor podstawowy. Kolor podstawowy to najczęstszy kolor
    znaków niebiałych w dokumencie, po normalizacji Gray/RGB/CMYK do RGB 0–255. Nagłówki nie dostają tej flagi, bo
    podręczniki często drukują je w kolorze;
  - `strikethrough`: przez środkowy pas znaku (od 30% do 70% wysokości licząc od góry) przechodzi pozioma linia albo
    wypełniony prostokąt o grubości do 2 pt. Podkreślenie przy linii bazowej nie daje tej flagi.
  - Kolejność flag jest kolejnością enumu w kontrakcie.
- **Render:**
  - `python -m wgc source render` zapisuje strony do `.glu/source/<SRC-id>/pages/p<NNN>.png` (ADR-0012);
  - render to osobne polecenie, a nie część ekstraktora;
  - `verified_by_render` zostaje polem ręcznym.
- **Kryterium zgodności z Markdown:** ten sam tekst w Markdown i w PDF daje te same klucze, typy, rodziców, kolejność
  i `text_hash` segmentów. Test obejmuje także nagłówki, wstęp i tabelę gry benchmarkowej (`tests/test_ingest_pdf.py`).

## Konsekwencje
- Stage 0 działa na PDF-ach z warstwą tekstu w jednej kolumnie. Inwentarz z PDF-a ma te same ID i `text_hash` co
  z Markdown, więc kotwice nie zależą od formatu źródła.
- Ograniczenia, które obecny ekstraktor ma świadomie:
  - **Kilka kolumn:** wiersze kolumn leżące na tej samej wysokości zlewają się w jeden wiersz z kilkoma komórkami,
    przez co segment wygląda jak tabela. `column_scrambled` nie jest wykrywane.
  - **Nagłówki i stopki stron:** żywa pagina i numer strony wchodzą do tekstu segmentu, który przechodzi na następną
    stronę.
  - **Strony bez warstwy tekstu:** nie dają segmentów. `image_only` nie jest ustawiane i nie ma OCR.
  - **Tabele:** komórki łączy się w kolejności wierszy. Zgodność z Markdown jest sprawdzona dla prostych tabel
    (jedna linia tekstu na komórkę). Komórka zawijana w kilka wierszy da inny tekst niż Markdown.
  - **Heurystyka nagłówka:** większy font wyróżnienia (np. tytuł ramki) zostanie potraktowany jako nagłówek.
  - **Numer reguły:** wymaga pogrubionego kroju. Podręcznik, który nie pogrubia numerów, wymaga nowej wersji
    ekstraktora.
- Nowsza wersja `pdfplumber` albo `pdfminer.six` może zmienić wynik ekstrakcji (np. pozycje znaków), także między
  dwiema maszynami z tym samym inwentarzem. `wgc source verify` wykryje to jako `segment_hash_mismatch`. Progi
  i reguły ekstraktora zmienia nowa wersja `wgc.ingest.pdf@N`.
- Wydrukowane w kolorze nagłówki ani numery reguł nie dają `changed_color`. Zmiana zaznaczona tylko kolorem nagłówka
  nie zostanie oflagowana.
- `verify` nie porównuje `pages`, `bbox` ani `visual_flags` z ponowną ekstrakcją. Odświeża je `extract`.
- Narzędzie dostaje około ośmiu nowych pakietów z zależnościami przechodnimi: `pdfplumber`, `pdfminer.six`,
  `charset-normalizer`, `cryptography` (z `cffi` i `pycparser`), `pypdfium2` i `Pillow`. Wszystkie są na licencjach
  liberalnych.

## Odrzucone warianty
- **PyMuPDF:** jedna zależność i bogatsze API, ale licencja AGPL-3.0 (albo komercyjna) przesądzałaby Q-05.
- **reportlab do generowania PDF-ów w testach:** dodatkowa zależność. Własny writer daje pełną kontrolę nad fontami,
  kolorami i liniami.
- **Numer reguły rozpoznawany samym wzorcem na początku wiersza:** dzieli segment na odsyłaczu przeniesionym na
  początek wiersza i na pozycji listy.
- **Kolejność czytania z bloków tekstu pdfminer (`LAParams`):** wynik zależy od heurystyk grupowania bloków, które
  trudno przewidzieć i zmieniają się między wersjami. Proste wiersze są deterministyczne i wystarczają dla jednej kolumny.
- **Pusty segment z flagą `image_only` dla strony bez tekstu:** tworzy sztuczny segment z hashem pustego tekstu.
  Właściwe rozwiązanie wymaga OCR (poza zakresem).
