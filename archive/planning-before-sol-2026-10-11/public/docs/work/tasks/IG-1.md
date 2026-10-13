# IG-1 Kontrakt i import pełnej KB WGU

- **Status:** next; karta przygotowana, kod nie rozpoczęty, obecna sesja tylko planuje.
- **Cel:** działający początek procesu WGC prowadzącego do IG całej instrukcji.
- **Wejście projektowe:** [architektura](../../IG-WGU-ARCHITECTURE.md),
  [plan](../../IG-PLAN.md), [draft modelu](../../IG-DATA-MODEL.md).
- **Wejście integracyjne:** pełna KB SPQR i manifest materiałów;
  opis w `private/ig/planning/wgu-spqr-2026-10-11/`.

## Do wykonania

1. Ustalić maszynowy schemat minimum: źródła/regiony, klauzule z aspektami,
   relacje, luki, coverage, origin bindings, rewizje, review i snapshot.
   Dodać kontrakt stanu, akcji, warunków, domen, skutków i kontynuacji według
   [legalnych akcji](../../IG-LEGAL-ACTIONS.md). Nie implementować jeszcze
   runtime ani uniwersalnego wykonawcy wszystkich profili.
2. Zbudować read-only adapter `wgu/kb@1` dla katalogu gry. Zachować pełne
   bajty wejść i nieznane pola. Odrzucać niebezpieczne tagi i duplikaty kluczy.
3. Zaimportować wszystkie kolekcje, także niejasności, zmiany, terminy bez ID,
   zagnieżdżone procedury i przypadki kontrolne. Dodatkowe pliki rozliczyć
   jako obsługiwane lub zachowane bez interpretacji.
4. Wprowadzić rejestr stabilnych ID i mapowanie wiele-do-wielu. Nie nadawać
   akceptacji na podstawie statusów WGU. Nie podmieniać `refs` na `requires`.
5. Zamrozić wskazane źródła lub zarejestrować brak. Obsłużyć lokalny override
   ścieżki w konfiguracji WGC z jawnym statusem identyczności materiału.
6. Dodać walidator, deterministyczny eksport roboczy i raport importu.
   Struktura review oraz aktualności jest potrzebna od pierwszego zapisu;
   pakiety wygodnego przeglądu można rozwinąć w IG-3.

## Odbiór

Cała KB ma rozliczenie bez cichych strat. Te same bajty dają te same
tożsamości i treść wyniku. Nieobecny PDF nie zatrzymuje importu opracowań,
ale uniemożliwia potwierdzenie zgodności. Wydania pozostają rozdzielone.

Testy obejmują utratę nieznanych pól, błędną składnię i powtórzone klucze,
duplikaty ID, relacje bez ID, zmianę kolejności terminów, zagnieżdżone kroki,
braki źródeł, referencje do podpunktów i wildcardów oraz brak automatycznej
akceptacji. Wildcard wymaga jawnego rozstrzygnięcia zakresu w IG.
Kontrola całego rzeczywistego wejścia jest prywatna; publiczne fixture
syntetyczne. Nie kopiować treści gry do publicznych testów.

IG-1 kończy działający import i kontrakt, nie pełny zweryfikowany IG.
Importowany tekst bez semantyki jest stanem przejściowym. Każda klauzula ma
klasyfikację wpływu na wykonanie oraz obowiązki formalizacji w IG-3.
IG-2 wykonuje pełną inwentaryzację PDF i dopasowanie do KB bez ponownego
pytania, czy ograniczyć pracę do kilku klauzul. Po implementacji aktualizować
kontrole repo do rzeczywistej struktury runtime; nie reaktywować kodu legacy.

## Poza zakresem

Runtime gry w IG-1 (planowany w IG-4), wykonywanie procedur, UI, API inferencji, modyfikowanie WGU,
dwukierunkowa synchronizacja, nowe czaty/agenci i zmiany w archiwalnym gold.
Obsługę gotowego bundle można dodać po adapterze katalogu, zachowując
wymagania manifestu i pochodzenia opisane w architekturze.
