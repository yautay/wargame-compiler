# ADR-0038: Minimalne kontrakty wymiany desktopowej i rewizji dokumentu

- **Status:** przyjęty
- **Data:** 2026-10-06
- **Milestone:** M-DESK1

## Kontekst

[ADR-0037](ADR-0037-ekstrakcja-desktop-bez-api.md) wymaga struktury dokumentu przed Rule IR, dowodów
tekstowych i obrazowych oraz trwałego prywatnego wyniku. Kontrakt słów legacy nie pozwala sprawnie zapisać
transkrypcji obrazu i myli zatwierdzenie z przejściem deterministycznej kontroli. Najpierw potrzebny jest
mały, testowalny przykład; transport, zapis i ergonomia należą do kolejnych etapów.

## Decyzja

1. Jedna rodzina `wgc/desktop@0` z zamkniętymi kopertami `package`, `response`, `document`, `revision`.
   Dowody są wspólną definicją schematu dokumentu, bez osobnego globalnego rejestru. Obecne kontrakty
   `source`, `common`, `proposal` oraz zapis KB nie zmieniają semantyki. Nie zamrażamy `@1` przed konsumentem.
2. Pakiet określa rozłączne `target_pages` i `context_pages`. Tożsamość jest lokalna dla pakietu, nie oparta
   na numerze wydrukowanej reguły. Bloki należą tylko do zakresu docelowego. Relacja wymagająca nieobecnego
   bloku pozostaje luką z `affects`; nie tworzymy bloku w kontekście. Granularność obszarowa eksportu może
   rozszerzyć szkic po pilocie; teraz właścicielstwo dotyczy całych stron.
3. Kod przekazuje surowe fragmenty z zakresami glifów i ich obwiedniami. Model zwraca uporządkowane
   `[start,end)` w surowym tekście (punkty kodowe Unicode); kod rekonstruuje tekst i dokładne obwiednie.
   Nie wymagamy list wszystkich ID słów ani kopii tekstu od modelu. Transkrypcja obrazu, opis diagramu
   i dowód zakresu ramki/koloru są odrębne i wskazują obraz z manifestu. Żaden opis nie zastępuje obrazu.
4. Hierarchia, kolejność czytania i relacje (kontynuacja, podpis, legenda, zakres) są oddzielne.
   Tabela zachowuje siatkę, role komórek, scalenia i noty; pojedynczy wiersz nie powoduje odrzucenia tabeli.
5. Hash pakietu/rewizji to istniejący kanoniczny hash WGC całej koperty bez własnego `hash`.
   Obrazy/PDF/instrukcje/schemat mają pełne hashe bajtów; wskaźniki dokumentu i odpowiedzi mają hashe
   kanonicznie odczytanych danych. Odpowiedź nie nadaje hashy rewizji ani stanów przeglądu.
6. Rewizja osobno zapisuje wynik walidacji i stan każdego bloku, dowodu, relacji oraz obszaru.
   Zatwierdzenie wymaga jawnego recenzenta i podstawy porównania z dokumentem/renderami. Element zależny
   od luki, dowodu oczekującego lub nieaktualnego nie jest zatwierdzony. M-DESK1 kontroluje spójność tych
   deklaracji, nie wykonuje przeglądu i nie daje prawa zapisu KB.
7. Prywatny układ to `private/source-artifacts/<SRC-id>/`: `originals/`, `packages/`, `responses/`,
   `documents/`, `revisions/`. Pliki rewizji są niezmienne, wskazują rodzica i jawną mapę zmian
   (dodanie/usunięcie/podział/połączenie). Ścieżki w kopertach są względne, POSIX, bez `..`.
   Commitowane metadane gry będą zawierać wyłącznie ID/hashe/wskaźnik rewizji, nie tekst, rendery ani
   surowe odpowiedzi. Cache `.glu/` nie jest trwałym magazynem; implementacja zapisu/odtworzenia to M-DESK3.

## Konsekwencje

- [Własny przykład](../../bench/desktop-two-page/README.md) daje reprezentację kolumn, kontynuacji,
  ramki i napisu w obrazie. Wszystkie jego stany przeglądu pozostają `pending` mimo poprawnej struktury.
- `wgc.desktop.check` jest kontrolą danych w pamięci. Nie czyta prywatnego magazynu, nie importuje,
  nie wywołuje modeli i nie aktualizuje source/KB/GLU. Kontrola rzeczywistych bajtów, starych pakietów,
  konfliktów nakładających się zakresów oraz atomowy zapis należą do M-DESK2/3.
- Schemat nie dowodzi pełnego pokrycia widocznego obrazu ani poprawnego znaczenia transkrypcji,
  kolejności kolumn czy zakresu. Zmiana tych elementów zmienia hash dokumentu i unieważnia podstawę review.
- Q-11 pozostaje otwarta. Premium działa wyłącznie w ChatGPT/Claude Desktop, bez API inferencji;
  opcjonalny lokalny kontroler nie jest zależnością kontraktu ani wykonawcą zatwierdzenia.
