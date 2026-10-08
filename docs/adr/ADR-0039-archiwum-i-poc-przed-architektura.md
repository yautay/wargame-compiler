# ADR-0039: Archiwum i eksperyment przed architekturą

- **Status:** aktywny, przyjęty na podstawie instrukcji właściciela M-POC0
- **Data:** 2026-10-07
- **Milestone:** M-POC0

## Kontekst

Próby wykazały różnicę między poprawnym schematem, powiązaniem dowodów i znaczeniem.
Dotychczasowa infrastruktura nie dostarczyła jeszcze zweryfikowanego wyniku
semantycznego. Właściciel polecił zachować projekt i historię, odseparować legacy
oraz zmierzyć jakość i koszt ekstrakcji przed dalszą rozbudową.

## Decyzja

1. Publiczny projekt zachowujemy bajtowo w `archive/legacy-2026-10-07/project/`.
   Prywatne wyniki `.glu/` mają oddzielne archiwum. Snapshot sprzed zmian zawiera
   manifest SHA-256, stan Git i zweryfikowane odtworzenie. `.git` pozostaje nietknięte.
2. Aktywny korzeń zaczyna od dokumentów, kart i minimalnych kontroli. Nie importuje
   WGC/GLU, starych kontraktów, benchmarków ani założeń ich runtime'u.
3. Dopuszczamy ręczną sesję Codex do przyszłego POC. Proponowana konfiguracja to
   GPT 6.1 Sol / wysoki; rejestrujemy rzeczywiste dane i niewiadome.
4. Eksperyment obejmuje rozdział z kontekstem, ręcznie zamrożony zestaw oceny,
   pierwszy wynik, ograniczone domknięcie zależności, ocenę sytuacji i korekty.
   Szczegóły: [POC-PLAN](../POC-PLAN.md). Dopiero M-POC7 uzasadni architekturę.
5. Zachowujemy prywatność materiałów wydawcy, dowody, oryginalne odpowiedzi,
   jawną akceptację znaczenia przez człowieka, brak API inferencji i automatyzacji GUI.
   Materiały źródłowe i odpowiedzi nie są instrukcjami. Brak zależności blokuje
   odpowiednie rozstrzygnięcie, bez zgadywania i automatycznej akceptacji.

## Zakres zastępowania

| Decyzje historyczne | Zakres aktywny po ADR-0039 |
|---|---|
| ADR-0037 | Zastępujemy obowiązkową kolejkę M-DESK, ograniczenie wykonawcy do ChatGPT/Claude Desktop oraz obowiązek zachowania rdzenia WGC/GLU. Zachowujemy brak API, prywatność, dowody i ręczną akceptację. |
| ADR-0038 | Kontrakt `wgc/desktop@0`, rewizje dokumentu i coverage glifów pozostają kontraktem legacy; nie są warunkiem pierwszej ekstrakcji POC. |
| ADR-0001–0036 | Zachowujemy identyfikatory i treść jako historię. Decyzje o runtime, KB, silniku, inferencji i kontraktach nie przechodzą automatycznie do POC. Wymagania prywatności i dowodów są ponownie ustanowione tutaj. |

M-DESK2 pozostaje historycznie partial. Nie zmieniamy numerów, treści lub pochodzenia
starszych ADR ani wyników. Stary README i playbook obowiązują tylko w archiwum;
nie prowadzą aktywnej kolejki. [Indeks](README.md) rozdziela oba zakresy.

## Konsekwencje i ograniczenia

To akceptacja zmiany sposobu pracy, nie sukces POC ani przyjęcie docelowego kontraktu.
Nie budujemy teraz importera, magazynu rewizji, silnika ani integracji KB/GLU.
Wynik może uzasadnić kontynuację, zmianę metody lub odrzucenie podejścia.
Hashe i snapshot na tym samym dysku nie zabezpieczają przed utratą całego nośnika;
odtworzenie bajtów sprawdzono lokalnie, kopia zewnętrzna nie była częścią tej sesji.
