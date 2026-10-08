# ADR-0037: Ekstrakcja premium przez aplikacje desktopowe, bez API

- **Status:** przyjęty; zastępuje ADR-0013 i docelowy kierunek ADR-0036; częściowo zastępuje decyzje wskazane niżej
- **Data:** 2026-10-06
- **Milestone:** M-DESK0

## Kontekst

[Pilot Q-11](../reviews/2026-10-06-q11-hybrydowy-ingest-pdf-pilot.md) nie dał zatwierdzonego inwentarza.
Rozdzielamy awarie wywołań od jakości modelu: 17 z 20 stron miało błąd providera, więc nie jest to porównanie
modeli premium. Obecny kontrakt wymaga rozliczania każdego słowa i blokuje tekst widoczny wyłącznie na obrazie.
Właściciel zdecydował: premium wyłącznie przez ChatGPT lub Claude Desktop, bez podpinania API; przebudowa
istniejącego kodu, lokalny LLM jako opcjonalna pomoc. Plan ma umożliwić kontynuację w małych etapach.

## Decyzja

1. Bazowy przebieg to pakiet plików -> praca premium w aplikacji -> import -> walidacja -> jawny przegląd.
   Nie implementujemy API inferencji ani jako drogi głównej, ani fallbacku. Nie wymagamy automatyzacji GUI,
   MCP, Codex CLI czy serwera LAN. Możliwości transferu plików sprawdzimy praktycznie w M-DESK2.
2. Premium odpowiada za odczyt struktury PDF i początkową ekstrakcję semantyki. Kod przygotowuje dowody,
   rekonstruuje tekst z referencji, nadaje ID/hashe, kontroluje pokrycie i zapis. Walidacja schematu nie oznacza
   potwierdzenia znaczenia. Nie przerzucamy całej ekstrakcji do heurystyk.
3. Przed Rule IR powstaje wersjonowana reprezentacja dokumentu z blokami, hierarchią, tabelami, diagramami,
   kontynuacjami i zakresem wynikającym z legend/ramek/koloru. Tekst z obrazu ma osobne pochodzenie i przegląd.
4. Oryginał i zaakceptowany wynik odczytu są trwałymi prywatnymi artefaktami; `.glu/` pozostaje stanem
   operacyjnym/cache. Hash nie odtwarza decyzji modelu. Potrzebne eksport/odtworzenie rewizji bez inferencji.
   Zakaz commitowania tekstów i obrazów wydawców pozostaje. Artefakty prywatne wymagają kopii zapasowej.
5. Zachowujemy kontrakty, provenance, kontrolowaną akceptację WGC, transakcje i recovery KB. Nowy ingest
   powstaje obok legacy. Migracja źródeł i zależnych rekordów jest jawna, odwracalna i sprawdzana diffem.
6. Lokalny LLM może później działać przez proces i pliki jako kontroler lub autor propozycji pomocniczych,
   bez samodzielnej akceptacji KB. Nie jest zależnością bazowego procesu. Nie wdrażamy obecnie gatewaya.
7. Kolejność to mały przebieg plikowy -> pilot jakości -> reguły z dowodami -> GLU -> opcjonalny lokalny
   kontroler. Dokument [DESKTOP-IMPLEMENTATION-PLAN](../DESKTOP-IMPLEMENTATION-PLAN.md) definiuje zakres i bramki.

## Zakres zastępowania wcześniejszych decyzji

| Decyzja | Co zmienia ADR-0037 |
|---|---|
| ADR-0013 | Całą strategię dwóch providerów premium; API usunięte, transport plikowy jest bazowy, MCP nie jest wymagany |
| ADR-0010, ADR-0017, ADR-0028 | Premium nie jest tylko eskalacją po lokalnym modelu; brak automatycznej akceptacji lokalnej i fallbacku API. Zachowujemy jawne ryzyko oraz brak zgadywania przy awarii |
| ADR-0015–0018 | Gateway, transport HTTPS i wdrożenie węzła nie są ścieżką aktywną. Lokalny oznacza self-hosted, lecz topologia nie jest obowiązkową zależnością |
| ADR-0012, ADR-0020, ADR-0021 | Deterministyczne przygotowanie zostaje; interpretacja struktury PDF jest modelowa, jej zatwierdzony wynik trwały. Polityka treści prywatnej pozostaje |
| ADR-0004 | KB nadal jest źródłem prawdy domenowej, ale jej dowody obejmują także prywatny trwały artefakt dokumentu poza cache |
| ADR-0036 | Nowy kontrakt i model review zastąpią podejście słowo-po-słowie; obecny kod pozostaje legacy do porównań i jawnej migracji |

Pozostałe decyzje zachowują moc w niesprzecznym zakresie. Wcześniejsze dokumenty opisujące API/routing są
historycznym projektem; nie upoważniają do wdrożenia zabronionej ścieżki. Zmiana planu nie oznacza, że schematy
i runtime zostały już zmigrowane. M-DESK1 rozpoczyna implementację kontraktów.

## Konsekwencje

- Najpierw mierzymy jakość i czas ręcznych korekt na prywatnym korpusie; nie deklarujemy zwycięzcy ChatGPT/Claude.
- Wymiana ręczna jest wspieranym trybem, więc brak odpowiedzi pozostawia zadanie oczekujące, bez retry inferencji.
- Dostępność modelu, tokenów czy ceny w aplikacji nie jest gwarantowana; brak danych raportujemy jawnie.
- Q-11 pozostaje otwarta do pilota. Q-12/Q-16/Q-17 wymagają rozwiązania w zakresie integracji z KB.
- Jedna niewyjaśniona ilustracja nie kasuje poprawnych fragmentów, lecz blokuje zależne reguły i pełną kompletność.
- Nie przepisujemy całego repo i nie usuwamy wcześniejszych niezatwierdzonych zmian użytkownika.
