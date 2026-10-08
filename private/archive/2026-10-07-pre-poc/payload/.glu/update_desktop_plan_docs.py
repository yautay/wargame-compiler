from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return (ROOT / name).read_text(encoding='utf-8')

def write(name, value):
    (ROOT / name).write_text(value, encoding='utf-8', newline='\n')

def replace_once(body, old, new):
    assert body.count(old) == 1, old[:100]
    return body.replace(old, new, 1)

road = read('docs/ROADMAP.md')
start = road.index('Sekcje niżej grupują milestone')
end = road.index('## Faza 0: fundament')
road = road[:start] + '''Aktywną kolejność ustala ADR-0037 i [plan implementacji](DESKTOP-IMPLEMENTATION-PLAN.md).
Przebudowujemy istniejący kod. Premium działa przez ChatGPT lub Claude Desktop, bez API inferencji.

```text
M-DESK0 (done) -> M-DESK1 (next) -> M-DESK2 -> M-DESK3 -> M-DESK4
 -> M-DESK5 (bramka jakości) -> M-DESK6a -> M-DESK6b -> M-DESK7 -> M-DESK9
                                                         -> M-DESK8 (optional)
```

**Milestone'y starszych faz o statusie `planned`/`optional` są odłożonym backlogiem, nie kolejką wykonania.**
Ich dawnych zakresów API, gatewaya, LAN i lokalnego routingu nie realizować. M-DESK9 przepisze przydatne
dalsze zadania według wyników pilota. Status `done` wcześniejszych etapów opisuje wykonane prace i pozostaje.
M-DESK8 nie blokuje M-DESK9. Q-11 jest otwarta i przechodzi do pilota M-DESK5, nie do ręcznego łatania 20 stron
legacy. M3 (gold) i M-BASE (pomiar) mają wczesny odpowiednik w M-DESK1/5; gateway nie jest zależnością gold.

## Aktywna przebudowa desktopowa

Szczegółowe zakresy, przypadki testowe i bramki: [plan](DESKTOP-IMPLEMENTATION-PLAN.md#7-etapy-i-kryteria-odbioru).
Każda sesja aktualizuje ten rejestr statusów; plan nie jest osobną kopią postępu.

### M-DESK0: Decyzja i plan przebudowy
- **Status:** done · **Rola:** ARCH · **Zależy od:** M-STAB3c
- **Wynik:** ADR-0037, plan implementacji, aktualizacja punktów wejścia i kolejności; kod bez zmian.

### M-DESK1: Minimalne kontrakty dokumentu i pakietu
- **Status:** next · **Rola:** ARCH + IMPL · **Zależy od:** M-DESK0
- **Zakres:** schematy pakietu, odpowiedzi, dowodów i rewizji; własny dwustronicowy przykład i fixture'y;
  DATA-CONTRACTS. Oddzielić zakres docelowy od kontekstu i poprawność strukturalną od zatwierdzenia.
- **Akceptacja:** kolumny, kontynuacja, ramka zakresu, transkrypcja obrazu mają reprezentację; negatywne
  fixture'y wykrywają brak dowodu i niespójny manifest; testy offline zielone.
- **Poza zakresem:** eksporter/importer, modele, GPU, migracja istniejącej gry.

### M-DESK2: Eksport pakietów do aplikacji desktopowej
- **Status:** planned · **Rola:** IMPL + HUM · **Zależy od:** M-DESK1
- **Zakres:** deterministyczny pakiet z tekstem/renderami, kontekstem, schematem i instrukcją odpowiedzi.
- **Akceptacja:** zgodne hashe przy ponowieniu; ręczny round-trip pliku w co najmniej jednej aplikacji,
  możliwości drugiej opisane bez obietnic automatycznej integracji; bez API/sterowania GUI.

### M-DESK3: Import i trwałe rewizje prywatnych artefaktów
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M-DESK2
- **Zakres:** import propozycji, diagnostyka, prywatny magazyn, eksport i odtworzenie.
- **Akceptacja:** stary/obcy pakiet odrzucony; powtórny import idempotentny; awaria zachowuje poprzedni wynik;
  utrata cache nie wymaga modelu. Brak zapisu do KB na tym etapie.

### M-DESK4: Podgląd, review i poprawki fragmentów
- **Status:** planned · **Rola:** IMPL + HUM · **Zależy od:** M-DESK3
- **Zakres:** porównanie renderu z blokami i tabelami, jawne zatwierdzanie i pakiet korekty obszaru.
- **Akceptacja:** poprawny fragment jest zachowany mimo innej luki; zależny zakres pozostaje zablokowany;
  tekst z obrazu może uzyskać zweryfikowany dowód bez udawania warstwy tekstowej.

### M-DESK5: Pilot jakości odczytu instrukcji
- **Status:** planned · **Rola:** HUM + ARCH · **Zależy od:** M-DESK4
- **Zakres:** 12–18 stron prywatnego korpusu, wcześniej ustalone oczekiwania i próbka kontrolna;
  raport pierwszego wyniku i korekt, czasu użytkownika i dostępnych metryk.
- **Akceptacja:** krytyczne elementy poprawne, brak cichych pominięć i dopowiedzeń, pokrycie rozliczone;
  decyzja kontynuować albo poprawić kontrakt. Nie zamykać Q-11 na podstawie samego JSON/schema validity.

### M-DESK6a: Ekstrakcja semantyczna z zatwierdzonego dokumentu
- **Status:** planned · **Rola:** ARCH + IMPL + HUM · **Zależy od:** M-DESK5
- **Zakres:** pakiet jednej sekcji z zależnościami, propozycje reguł/wyjątków/limitów i przypadków kontrolnych.
- **Akceptacja:** ślad reguły do dowodu tekstowego/wizualnego; przypadek pozytywny i negatywny sprawdzone
  względem źródła. Bez pełnej digitalizacji i bez bezpośredniego zapisu modelu do KB.

### M-DESK6b: Akceptacja KB i zmiana rewizji źródła
- **Status:** planned · **Rola:** ARCH + IMPL · **Zależy od:** M-DESK6a
- **Zakres:** integracja przez `accept()`, manifesty i ownership; dowody wizualne; Q-12/Q-16/Q-17 dla pilota.
- **Akceptacja:** odrzucenie starego pakietu i niepotwierdzonej kotwicy, kontrola zależnych rekordów po zmianie
  rewizji; konserwatywna blokada zakresu dopuszczalna przed pełnym grafem. Bez cichej migracji źródeł.

### M-DESK7: Kolejka pracy desktopowej w GLU
- **Status:** planned · **Rola:** IMPL · **Zależy od:** M-DESK6b
- **Zakres:** powiązanie istniejącego job store z eksportem, oczekiwaniem, importem i review.
- **Akceptacja:** restart zachowuje pracę, duplikat odpowiedzi nie dubluje akceptacji; brak odpowiedzi pozostawia
  oczekiwanie bez wywołania API. Zmiany stanów/kontraktów wymagają fixture'ów i testów recovery.

### M-DESK8: Opcjonalny lokalny kontroler
- **Status:** optional · **Rola:** IMPL + HUM · **Zależy od:** M-DESK7
- **Zakres:** worker przez proces/pliki, niezależna ekstrakcja kontrolna, raport rozbieżności.
- **Akceptacja:** porównanie wykrytych błędów/fałszywych alarmów/czasu z wariantem bez workera;
  bez samodzielnej akceptacji; brak lokalnego modelu nie blokuje podstawowej pracy desktopowej.

### M-DESK9: Migracja i dalsza roadmapa
- **Status:** planned · **Rola:** ARCH + IMPL · **Zależy od:** M-DESK7
- **Zakres:** jawny diff i odwracalne przełączenie projektu; aktualizacja dalszych etapów M3–M28.
- **Akceptacja:** regresje legacy/Markdown, zachowane dowody i rewizje, udokumentowana migracja i rollback;
  decyzja o wycofaniu legacy oparta na pilocie, bez przywracania API.

''' + road[end:]
road = replace_once(road, '- **Status:** next · **Rola:** IMPL · **Zależy od:** M9a, M-STAB3c', '- **Status:** planned · **Rola:** IMPL · **Zależy od:** M9a, M-STAB3c')
for title in ['### M10: Providerzy fake/replay/self_hosted + pętla structured output', '### M15: Premium: review package, `anthropic`, `desktop_pull`']:
    start = road.index(title)
    pos = road.index('\n', road.index('- **Status:**', start)) + 1
    road = road[:pos] + '- **Odłożone przez ADR-0037:** poniższy zakres jest historyczny; nie implementować API. Zastępuje go aktywny plan M-DESK.\n' + road[pos:]
write('docs/ROADMAP.md', road)

status = read('docs/STATUS.md')
status = replace_once(status, '- **Ostatni milestone:** M-STAB3c (kontrakt propozycji, ownership outputów, wdrożenie ADR-0027): done', '- **Ostatni milestone:** M-DESK0 (plan przebudowy desktopowej, ADR-0037): done')
status = replace_once(status, '- **Bieżący milestone:** M10', '- **Bieżący milestone:** M-DESK1')
status = replace_once(status, '## Gdzie jesteśmy\n', '''## Aktualny kierunek

Właściciel zatwierdził przebudowę istniejącego kodu. Premium wyłącznie w ChatGPT lub Claude Desktop,
bez API inferencji; bazowy transport to pakiety plików. Lokalny LLM jest opcjonalnym kontrolerem przez
proces/pliki. Gateway LAN i dawny routing nie są aktywnymi pracami. Obowiązuje
[ADR-0037](adr/ADR-0037-ekstrakcja-desktop-bez-api.md) i [plan](DESKTOP-IMPLEMENTATION-PLAN.md).

M-DESK0 zapisuje decyzję i plan, nie wdraża nowego ingestu. Dotychczasowy kod PDF i zmiany pilota Q-11 pozostają.
Nowa ścieżka powstaje obok legacy, z trwałymi prywatnymi rewizjami dokumentu, przeglądem obszarów i późniejszą
integracją z KB. Pełna kolejka i lokalny worker dopiero po potwierdzeniu jakości odczytu premium.

## Gdzie jesteśmy
Poniżej stan zaimplementowanych fundamentów i historia. Dawne oznaczenia przyszłych milestone'ów nie
ustanawiają kolejności; aktywna kolejność M-DESK jest w ROADMAP.
''')
a = status.index('**Inferencja (M-INF0):**')
b = status.index('| Etap / podsystem', a)
status = status[:a] + '''**Inferencja:** projekt M-INF0 opisywał węzeł LAN i gateway, których kod nie powstał. ADR-0037
zastępuje tę obowiązkową ścieżkę pracą desktopową bez API. Dawne dokumenty NODE/DEPLOYMENT są referencją
historyczną; nie wdrażać ich w ramach nowego planu. Lokalny sprzęt można później wykorzystać w M-DESK8.

''' + status[b:]
a = status.index('## Następny milestone:')
b = status.index('## Otwarte kwestie', a)
status = status[:a] + '''## Następny milestone: M-DESK1 Minimalne kontrakty dokumentu i pakietu

**Cel:** opisać model dokumentu i wymianę plików na własnym dwustronicowym przykładzie przed pisaniem eksportera.
Przeczytać [plan, sekcja 10](DESKTOP-IMPLEMENTATION-PLAN.md#10-następna-sesja-m-desk1), ADR-0037 i ostatni handoff.

**Zakres:** minimalne kontrakty pakietu, odpowiedzi, rewizji i dowodów, fixture'y, testy i DATA-CONTRACTS.
Uwzględnić kolumny, kontynuację, ramkę określającą zakres i tekst w obrazie. Rozdzielić zakres od kontekstu,
walidację od przeglądu oraz trwałe artefakty od cache. Wykorzystać istniejące mechanizmy WGC.

**Pierwsza czynność:** sprawdzić stan roboczy, przeczytać `wgc/ingest/__init__.py`, `pdf_hybrid.py`, `wgc/source.py`,
schematy source/common/proposal, `wgc/contracts.py` i testy hybrydy; przygotować własny przykład i oczekiwany wynik.

**Poza zakresem:** API, gateway, modele/GPU, eksporter/importer (M-DESK2/3), migracja istniejących źródeł i KB.
Nie kontynuować dawnego M10. Q-11 pozostaje otwarta do M-DESK5; Q-12/Q-16/Q-17 mają właściciela w M-DESK6b.

''' + status[b:]
status = replace_once(status, 'M10 pozostaje bieżącym milestone\'em; Q-11 nie jest zamknięta.', 'ADR-0037 przekierowuje Q-11 do M-DESK5. Nie zamykamy jej przez samo poprawienie replay legacy; bieżący etap to M-DESK1.')
lines = status.splitlines()
for i, line in enumerate(lines):
    if line.startswith('| Q-08 |'):
        lines[i] = '| Q-08 | Zamknięta przez ADR-0037: brak fallbacku API; lokalny kontroler opcjonalny, premium działa jawnie w aplikacji | właściciel | 2026-10-06 |'
    if line.startswith('| Q-11 |'):
        lines[i] = '| Q-11 | Legacy hybrid nie dał zatwierdzonego inwentarza. Nowy pilot struktury dokumentu według ADR-0037; sprawdzić kolumny, listy, tabele, kolor/zakres, diagramy i transkrypcje obrazu | M-DESK5 + właściciel | przed M-DESK6a |'
    if line.startswith('| Q-06 |') or line.startswith('| Q-07 |'):
        lines[i] = line + ' <!-- historyczne: gateway odłożony przez ADR-0037 -->'
status = '\n'.join(lines) + '\n'
status = replace_once(status, '## Ryzyka\n', '''## Ryzyka aktualnego planu

| Ryzyko | Łagodzenie |
|---|---|
| Poprawny JSON pomija regułę albo zakres ramki | Osobny przegląd semantyczny, ręcznie sprawdzona próbka i testy mutacyjne |
| Różne możliwości transferu plików w aplikacjach | Ręczny round-trip M-DESK2; nie obiecywać automatycznej integracji |
| Wynik odczytu istnieje tylko w cache | Trwałe prywatne rewizje i eksport/odtworzenie M-DESK3 |
| Koszt obsługi ręcznej przewyższa korzyść | Pomiar czasu i korekt M-DESK5 przed kolejką/local workerem |
| Zmienione dowody zostawiają stare reguły w KB | Manifest rewizji, blokada zależnego zakresu i Q-12 w M-DESK6b |
| Lokalny kontroler powiela błąd premium | Ślepa ekstrakcja kontrolna, pomiar fałszywych alarmów; brak prawa akceptacji |

## Rejestr wcześniejszych ryzyk
Ryzyka kodu pozostają aktualne, jeśli dotyczą używanej funkcji. Poniższe ryzyka API/LAN, wymaganego węzła,
akceptacji lokalnej i dawnego routingu są historyczne, odłożone przez ADR-0037.
''')
write('docs/STATUS.md', status)

readme = read('README.md')
a = readme.index('> **Status:**')
b = readme.index('\n\n', a)
readme = readme[:a] + '''> **Aktualny kierunek (2026-10-06):** przebudowa ingestu PDF przez ChatGPT lub Claude Desktop, bez API inferencji.
> Zachowujemy rdzeń WGC/GLU; lokalny LLM jest opcjonalnym kontrolerem. Plan zapisany, implementacja od M-DESK1.
> Zacznij od [planu implementacji](docs/DESKTOP-IMPLEMENTATION-PLAN.md) i [STATUS](docs/STATUS.md).
> Opisy gatewaya i routingu poniżej odzwierciedlają wcześniejszy projekt, zastąpiony w tym zakresie przez ADR-0037.''' + readme[b:]
readme = replace_once(readme, '| [docs/ROADMAP.md](docs/ROADMAP.md) | milestone\'y M0–M28 |', '| [docs/ROADMAP.md](docs/ROADMAP.md) | aktywne etapy M-DESK i historyczny backlog |\n| [docs/DESKTOP-IMPLEMENTATION-PLAN.md](docs/DESKTOP-IMPLEMENTATION-PLAN.md) | przebudowa ingestu, kryteria odbioru i start kolejnej sesji |')
write('README.md', readme)
