# Próba ingest PDF — 2026-10-06

Źródło: `C:\dev\game-test\dtp_rulebook.pdf` (tylko odczyt). Kopia testowa: `private/rules.pdf`.
SHA-256 obu plików: `1E851FF7C5468B3972ED9D95E2631634739030E34546588CC23E45C8EC02682D`.

## Polecenia i wyniki

- `python -m pytest tests/test_ingest_pdf.py -q` → kod 1, `No module named pytest`.
- `python -m wgc source init --root .glu/dtp-ingest-test --game dtp --doc rules:private/rules.pdf` → kod 1, `No module named yaml`.
- `python -m wgc source extract --root .glu/dtp-ingest-test` → kod 1, `No module named yaml`.
- `python -m wgc source verify --root .glu/dtp-ingest-test` → kod 1, `No module named yaml`.
- `python -m wgc source render --root .glu/dtp-ingest-test --doc SRC-dtp.rules --pages 2,4,8,13,19-20 --scale 1.5` → kod 1, `No module named yaml`.
- `python -m glu build --root .glu/dtp-ingest-test --stage 1 --dry-run` → kod 1, `No module named yaml`.
- `pdfinfo private/rules.pdf` → 20 stron, 683.15 × 683.15 pt, PDF 1.4, 8 538 672 bajty, bez szyfrowania.
- Bezpośrednio `wgc.ingest.pdf.extract(Path(".glu/dtp-ingest-test/private/rules.pdf").read_bytes())` z dołączonym Pythonem 3.12 → `IngestError: Etykieta 1 występuje dwukrotnie (strony 2 i 4)`.
- Bezpośrednio `wgc.ingest.pdf.render_page` → sześć PNG `wgc-render-p*.png` dla stron 2, 4, 8, 13, 19, 20; obrazy poprawne. Niezależny `pdftoppm` dał `p*.png`.

## Obserwacje

- Wszystkie 20 stron ma warstwę tekstową (625–2805 znaków na stronę); brak strony całkiem bez tekstu.
- `_page_lines` utworzył 753 wiersze; 189 ma więcej niż jedną komórkę. `page-metrics.json` zawiera metryki stron oraz segmentację uruchomioną osobno dla każdej strony. Te lokalne segmenty nie są poprawnym inwentarzem całego dokumentu.
- Strona 4 sama wywołuje duplikat etykiety `1`: pogrubione `1.` w liście faz i ozdobny numer sekcji `1`. Strona 2 ma inny numer `1` w liście setupu.
- Wiele stron od 3 do 18 ma sklejenia dwóch kolumn w jednym wierszu; na stronie 4 wiersz zaczynający się od punktu `2.` obejmuje także tekst prawej kolumny. Strona 13 ma 16 wierszy z wieloma komórkami, a strona 20 ma ich 30 w układzie komponentów.
- Paginacja wchodzi do tekstu: przy próbie prefiksu stron 1–3 ostatni segment kończy się `Roma.\n3`. Na oglądanych stronach 2, 4, 8, 13, 19 i 20 numer strony występuje w dolnym wierszu tekstu.
- Prefiks stron 1–3 daje 16 segmentów: błędne `table` dla sekcji setupu, jednowyrazowe `heading` dla numerów 7 i 8 oraz tekst przecinający granicę stron. Pełna liczba i kolejność segmentów są nieokreślone, bo ekstrakcja zatrzymuje się na stronie 4.
- Na stronie 20 lokalna segmentacja daje fałszywe `rule` dla numerów komponentów `5`, `4` i `1`, a także fałszywą `table`.
- Lokalna segmentacja stron nie wykryła `strikethrough`; `changed_color` wystąpiło w 15 segmentach lokalnych, często w treści pomieszanej z kolorowymi oznaczeniami graficznymi. Tych flag nie można uznać za zweryfikowane zmiany zasad.
- Część dużych tytułów jest grafiką; warstwa tekstowa nie obejmuje całego znaczenia stron mimo niezerowej liczby znaków.

## Ograniczenia wyniku i propozycja

CLI, walidacja, receipt i manifest outputów nie mogły powstać: brakuje zależności, a ekstrakcja pełnego PDF i tak kończy się `IngestError`. Do diagnostyki użyto lokalnego `pdfplumber 0.11.9`, czyli wersji o 0.0.1 niższej niż minimum projektu `0.11.10`; `pypdfium2 5.13.0`, `Pillow 12.3.0`.

Q-11 wymaga co najmniej wykrycia/obsługi kolumn przed segmentacją, filtrowania pagin, rozdzielenia numerowanych list od numerów sekcji i decyzji, jak oznaczać znaczący tekst pozostający wyłącznie w grafice. Najmniejszy bezpieczny krok dla obecnego ekstraktora: wykrywać taki układ i zwracać diagnostykę zamiast inwentarza z przemieszanym tekstem; pełna obsługa potrzebuje ustalenia kolejności bloków i nowej wersji ekstraktora.
