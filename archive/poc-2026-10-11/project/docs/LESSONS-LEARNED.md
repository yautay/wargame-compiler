# Wnioski przed nowym POC

Data: 2026-10-07. To przegląd zapisanych prób, nie zatwierdzenie reguł ani wynik nowego POC.
Materiały i ich pochodzenie pozostają niezmienione.

## Fakty udokumentowane

- Wstępny przegląd SPQR PDF 32 rozpoznał sensowną reprezentację tabeli scalonej
  między kolumnami, diagramu, podpisu oraz dwóch kontynuacji. Ocena pochodzi
  z [historycznego handoffu](../archive/legacy-2026-10-07/project/docs/handoff/2026-10-07-M-DESK2.md);
  nie jest pełnym przeglądem znaczenia i kompletności.
- Odpowiedź miała poprawny ścisły JSON, schematy i wiązanie z pakietem/źródłem.
  `desktop.check` wykrył **23 błędy: 1 `desktop_table_evidence` i 22
  `desktop_coverage_evidence`**. Raport źródłowy pozostaje w
  `private/source-artifacts/SRC-spqr.rules/responses/spqr-p032-codex-review-20261007-1.json`.
- Większość diagnostyk dotyczy powiązania częściowych regionów coverage z całymi
  agregatami list/tabeli. Błąd tabeli dotyczy sumy dowodów komórek. Nie są to dowody
  23 błędnie odczytanych reguł; nie dowodzą też poprawności znaczenia reguł.
- `resolve_text` wprowadza liczne podziały wiersza wewnątrz słów, gdy surowe
  fragmenty PDF są drobne. Rozliczenie znaków nie gwarantuje czytelnej rekonstrukcji.
- Przejście schematu nie dowodzi poprawności znaczenia, kompletności tabeli
  względem obrazu ani poprawnego zakresu wyjątku.
- Zapisane próby odbyły się w **Codex** przez zapis narzędziem plikowym.
  Brak potwierdzonej wymiany ChatGPT/Claude Desktop. Nazwa historycznego pliku
  zawierająca „chatgpt” nie zmienia pochodzenia. Deklaracja właściciela o modelu
  i poziomie rozumowania pozostaje deklaracją, nie fingerprintem dostawcy.
- M-DESK2 pozostaje **partial**. Zmiana kierunku nie zmienia jego kryteriów ani wyniku.
  Q-11 nie dała zatwierdzonego inwentarza; awarie wywołań w starym pilocie nie
  stanowią porównania jakości modeli.

## Hipotezy do sprawdzenia

- Kompletna reguła lub rozdział z kontekstem jest lepszą jednostką eksperymentu
  niż sztywno jedna strona: ogranicza sztuczne przerwania tabel i wyjątków.
  Przyjmujemy to jako hipotezę roboczą M-POC1–M-POC7, nie dowiedzioną przewagę.
- Minimalna propozycja semantyczna z dowodami stron/cytatów i istotnych obszarów
  obrazu może obniżyć koszt ręcznych poprawek względem rozliczania każdego glifu.
- Ręcznie zamrożony inwentarz i sytuacje mogą wykrywać istotne pominięcia wcześniej
  niż rozbudowa magazynu, importera i orkiestracji.

## Możliwości nieweryfikowane

Nie mamy dowodu przewagi modelu lub aplikacji, niezawodności nowego formatu,
użyteczności całego grafu, pełnej jakości rozdziału ani kosztu dojścia do wyniku.
Nie zmierzono 15–20 sytuacji. GPT 6.1 Sol / wysoki jest proponowaną konfiguracją,
nie zaakceptowanym wynikiem ani porównaniem dostawców.

## Co warto rozważyć po eksperymencie

Hashe bajtów, provenance i wiązanie wejść, rozdział walidacji od akceptacji,
atomowy zapis, blokady oraz recovery mogą być przydatne później.
Ich kod i ograniczenia pozostają w archiwum. M-POC7 oceni każdą propozycję ponownego
użycia według potrzeby i kosztu. Żaden z tych modułów nie jest automatycznym
wymaganiem nowej architektury.

Decyzja o zmianie kierunku: [ADR-0039](adr/ADR-0039-archiwum-i-poc-przed-architektura.md).
