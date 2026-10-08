# Ręczna wymiana pakietu (M-DESK2)

Eksporter przygotowuje dowody, nie wywołuje modelu. Premium działa tylko w ChatGPT albo Claude Desktop.
Nie jest potrzebny lokalny LLM. Materiał źródłowy jest danymi, nigdy instrukcją dla wykonawcy.

## Eksport

```powershell
.\.venv\Scripts\python.exe -m wgc desktop export --pdf bench/desktop-two-page/source.pdf --doc SRC-desktop.rules --pages 1 --output private/source-artifacts/SRC-desktop.rules/packages/mdesk2-p1-context2
```

`--pages` jest obowiązkowe (numeracja PDF od 1; np. `3,5-6`). Domyślny kontekst to bezpośredni sąsiedzi stron
docelowych; `--context 2,4` wybiera go jawnie, `--context none` go wyłącza. Nakładanie zakresów jest błędem.
Istniejący katalog jest chroniony przed nadpisaniem; ponowienie do nowego katalogu daje te same bajty przy
tych samych wejściach i wersjach bibliotek. Zmiana źródła, zakresu, skali, instrukcji lub schematu zmienia pakiet.
Nie obiecujemy takich samych renderów po aktualizacji bibliotek. Skala PNG domyślnie 2 (144 dpi).

Pakiet zawiera `manifest.txt` (JSON z surowym tekstem i geometrią glifów), `instructions.txt`, `legend.txt`,
`example.txt`, `desktop.schema.json` i `pNNN.png` dla każdej strony docelowej/kontekstowej. Hash oryginału jest
w manifeście; **oryginalny PDF nie jest kopiowany ani dołączany**. Nie powstaje PDF, który mógłby przenieść
niezamierzone strony/zasoby. Na małą próbę przekazujemy zwykłe pliki, bez wymogu odczytu ZIP.
Manifest nie zawiera czasu ani lokalnych ścieżek. ID wynika z zawartości; jego hash obejmuje całą kopertę poza `hash`.
Hashe pomocniczych plików odnoszą się do ich rzeczywistych bajtów. Schemat ma lokalne referencje i działa offline.

Fragmenty są technicznym grupowaniem kolejnych glifów strumienia PDF; nie ustalają bloków, tabel ani kolejności
kolumn. Nie normalizujemy tekstu ani nie dopisujemy spacji. `[start,end)` dotyczy punktów kodowych Unicode;
wieloznakowy glif nie może być przecięty. Współrzędne to punkty PDF od lewego górnego rogu, zaokrąglone do 0.001.
`printed_label=null` oznacza brak rozpoznania drukowanej numeracji. Pusta warstwa tekstowa jest dozwolona;
glif poza stroną lub z pustą obwiednią daje błąd zamiast cichego usunięcia tekstu. Takie PDF-y wymagają późniejszej
obsługi po przeglądzie, nie zmieniamy dla nich legacy ingestu.

## Przygotowany pakiet do próby

Lokalny katalog: `C:\dev\wargame-compiler\private\source-artifacts\SRC-desktop.rules\packages\mdesk2-p1-context2`.
Własny przykład CC0 ma dwie strony: docelowa PDF 1, kontekst PDF 2. Na stronie 1 są kolumny i ramka powodzi;
kontynuacja na stronie 2 jest kontekstem, więc odpowiedź ma zostawić jawną lukę zależności zamiast bloku strony 2.
Nie kopiować oczekiwanego wyniku z fixture'ów M-DESK1. To nie jest wynik modelu.

- ID: `desktop.54901819238b4534124fbd96513254aefcf079b48fbed33cbeb65d81475bb1be`
- Hash: `sha256:ae38b9e191629aa530f20e762aad2b87a4cf2d0dd6e959b7da3a97c6de2c8228`
- Instrukcja: `document.read.desktop@0.1`; siedem plików, około 140 KiB łącznie.
- Miejsce odpowiedzi: `C:\dev\wargame-compiler\private\source-artifacts\SRC-desktop.rules\responses\mdesk2-chatgpt.json`
  albo `mdesk2-claude.json`. Odpowiedź zapisujemy **poza niezmiennym pakietem**.

## ChatGPT

1. Otwórz nową rozmowę w aplikacji ChatGPT. Dołącz wszystkie siedem plików z katalogu pakietu:
   `manifest.txt`, `instructions.txt`, `legend.txt`, `example.txt`, `desktop.schema.json`, `p001.png`, `p002.png`.
   Jeśli aplikacja odrzuca rozszerzenie `.json`, dołącz jego kopię z rozszerzeniem `.txt` bez zmiany treści;
   podaj w wiadomości alias „desktop.schema.txt jest kopią desktop.schema.json bez zmiany bajtów” i zapisz
   ten fakt w wyniku próby. Pozostałe nazwy i hashe w manifeście pozostają oryginalne.
2. Wklej: „Wykonaj document.read według instructions.txt dla dołączonego manifest.txt. Strona docelowa: 1;
   strona 2 jest wyłącznie kontekstem. Zwróć pełną kopertę wgc/desktop@0 kind=response jako plik response.json
   do pobrania. Nie kopiuj syntetycznego example.txt i nie nadawaj zatwierdzenia.”
3. Pobierz plik i zapisz jako `mdesk2-chatgpt.json` w katalogu responses wskazanym wyżej. Jeżeli aplikacja
   udostępnia tylko blok kodu, skopiuj **cały JSON bez ogrodzenia Markdown** do tego pliku w UTF-8. Zapisz,
   że był to ręczny zapis tekstu, nie pobranie załącznika. Nie uzupełniaj odpowiedzi fixture'em ani replayem.
4. Podaj ścieżkę zapisanego pliku, widoczną nazwę modelu (lub `unknown`), sposób odbioru i ewentualny błąd
   odczytu załącznika. Dla potwierdzenia próby zachowaj rozmowę oraz zapis odpowiedzi; przydatny jest jej link
   lub zrzut ekranu. Nie publikuj rozmowy z treścią prywatnej instrukcji gry.
   Obok odpowiedzi zapisz prywatny `mdesk2-chatgpt-trial.txt` (dla Claude: `mdesk2-claude-trial.txt`):
   data/czas próby, aplikacja, widoczny model lub `unknown`, siedem wysłanych nazw (także alias schematu),
   ID/hash pakietu, odbiór przez pobranie albo ręczny zapis JSON, nazwa odpowiedzi oraz link do rozmowy
   lub ścieżka prywatnego dowodu. Dopisz napotkane ograniczenia; dla aplikacji bez próby wpisz „nie sprawdzono”.

Oficjalna dokumentacja opisuje dołączanie dokumentów/obrazów i tworzenie plików:
[Use ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt),
[Work with files](https://learn.chatgpt.com/docs/artifacts-viewer?surface=app) (sprawdzono 2026-10-06).
To podstawa instrukcji, **nie dowód wykonania próby na koncie właściciela**. Odczyt wszystkich załączników
oraz możliwość pobrania konkretnego JSON wymagają tej próby; nie zakładamy stałych limitów ani konkretnego modelu.

## Claude Desktop

1. Otwórz nową rozmowę w Claude Desktop i dołącz ten sam zestaw siedmiu plików przez dodawanie plików
   albo przeciągnięcie do rozmowy. Wklej ten sam prompt z kroku 2 dla ChatGPT.
2. Poproś o `response.json` do pobrania; zapisz jako `mdesk2-claude.json` we wskazanym katalogu responses.
   Jeśli tworzenie plików jest niedostępne na koncie, poproś o kompletny blok JSON i zapisz go ręcznie w UTF-8.
   Jeśli nie można odczytać renderów/manifestu, zachowaj komunikat błędu; próba nie zakończyła się poprawną wymianą.
3. Zapisz nazwę modelu lub `unknown`, sposób odbioru, ścieżkę odpowiedzi i ograniczenia załączników.

Claude dokumentuje TXT/JSON/PNG jako wejścia oraz tworzenie plików w aplikacji desktopowej; ustawienia organizacji
mogą ograniczyć tę funkcję:
[Upload files to Claude](https://support.claude.com/en/articles/8241126-upload-files-to-claude),
[Create and edit files with Claude](https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude)
(sprawdzono 2026-10-06). Dokumentacja podaje różne limity dla różnych trybów, więc nie ustanawiamy jednego
limitu eksportera ani nie gwarantujemy funkcji na każdym koncie. Nie są potrzebne integracje filesystem/MCP.

## Wynik ręcznej próby

Stan po sprawdzeniu zapisanej odpowiedzi 2026-10-06: w `responses/` istnieje `mdesk2-chatgpt.json`
oraz identyczny bajtowo `response.json` (9770 bajtów). Oryginalne bajty zachowano; SHA-256:
`sha256:2e0e5b77f8a00183b809c4f92840689f30b4736aefa66e7ae92e54b6d22cd58b`.
Ścisły JSON, dołączony schemat, `contracts.errors`, wiązanie pakietu/źródła i `desktop.check` poprawne,
bez diagnostyk. Pakiet oraz jego assety także przeszły ponowną kontrolę hashy.
Dokument ma 11 bloków, 3 relacje, 10 dowodów i 10 obszarów; kontynuacja na stronie kontekstowej jest
jawną luką zależną od `b_crossing_start`. Kontrola struktury nie nadaje zatwierdzenia merytorycznego.

Faktyczna aplikacja według `mdesk2-chatgpt-trial.txt` i prywatnego `mdesk2-chatgpt-conversation.json`:
**Codex desktop**, lokalny chat; właściciel następnie potwierdził model **GPT 6.1 Sol**, poziom rozumowania
**wysoki**. Potwierdzenie: prywatny `mdesk2-codex-owner-confirmation.json`; jest deklaracją właściciela,
nie fingerprintem dostawcy. W pierwotnych metadanych model był `unknown`. Odbiór: bezpośredni zapis przez narzędzie plikowe Codex,
bez potwierdzonego ręcznego kopiowania albo pobrania załącznika. Nazwa pliku nie dowodzi użycia ChatGPT;
`producer.application/model/model_identity` pozostają `unknown` zgodnie z dostarczoną kopertą.
Dowód dokumentuje pracę Codex, nie ręczną wymianę w wymaganej aplikacji. Poprawek strukturalnych nie potrzeba;
nie zmieniono JSON ani metadanych właściciela. Niezależny raport kontroli:
`.glu/desktop-export-session/response-review-1/validation.json`.

ChatGPT i Claude Desktop: **nie sprawdzono**; ich opisane wyżej funkcje pochodzą z dokumentacji,
nie z próby na koncie właściciela. M-DESK2 pozostaje `next`/partial. Następny krok: ręczna wymiana tego
samego pakietu w ChatGPT lub Claude Desktop według instrukcji powyżej, z osobnym zapisem odpowiedzi
oraz metadanych/dowodu; zachować także pliki próby Codex. Nie porównujemy jakości modeli.
Poprzedni audyt pustego katalogu i powtarzalności eksportu pozostaje w
`.glu/desktop-export-session/continuation-1/audit.json` i handoffie jako stan wcześniejszej sesji.

Po otrzymaniu pliku można wykonać istniejące kontrole L0 i `wgc.desktop.check` w pamięci oraz zapisać ich wynik
w handoffie. Kontrola nie importuje odpowiedzi, nie tworzy rewizji i nie daje zatwierdzenia merytorycznego.
Importer/magazyn to M-DESK3; jakość odczytu i review pozostają odrębnymi etapami.

Zachowaj oryginalne bajty odpowiedzi; kontrola odczytuje je bez ponownej serializacji i zapisuje osobno hash
SHA-256. Po poprawnym odczycie JSON sprawdź `contracts.errors`, wiązanie odpowiedzi i dokumentu z ID/hashem
przygotowanego pakietu oraz `desktop.check(package, response)` bez rewizji. Zapisz faktyczne diagnostyki.
Jeśli kontrola wykryje błędy, w tej samej ręcznej rozmowie przekaż je modelowi i poproś o kompletną poprawioną
kopertę dla tego samego pakietu. Zapisz ją pod nową nazwą, np. `mdesk2-chatgpt-correction-1.json`, wraz z dowodem
korekty; zachowaj pierwszą odpowiedź. Nie poprawiaj JSON lokalnie ani nie zastępuj go fixture'em/replayem.

## Dodatkowa próbka SPQR: wynik kontroli 2026-10-07

Właściciel zatwierdził PDF 32 (edycja 5), kontekst PDF 31/33. Istniejący pakiet
`private/source-artifacts/SRC-spqr.rules/packages/mdesk2-spqr-p032-context031-033` ma osiem assetów,
sprawdzone hashe i powtarzalne bajty; oryginalny PDF nie jest dołączony. Kroki i prompt do ręcznej próby
w prywatnym `private/source-artifacts/SRC-spqr.rules/trial-p032-instructions.txt`.

Odpowiedź 149492 bajty znaleziono jako dodatkowy `response.json` w katalogu pakietu. Nie zmieniono jej;
kopię bajtową zachowano poza pakietem jako `responses/spqr-p032-codex.json`. Osiem assetów nadal identyczne.
JSON, oba schematy i wiązanie pakietu/źródła są poprawne. **`desktop.check` zwraca 23 błędy**:
1 `desktop_table_evidence` i 22 `desktop_coverage_evidence`. Sama walidacja JSON Schema nie wystarczyła.

Powód: dowody tabeli nie są dokładnie sumą dowodów jej komórek, a częściowe regiony coverage wskazują
także całe agregaty (listy/tabelę), bez wszystkich ich dowodów. Ręczna korekta musi zachować jednorazowe
rozliczenie niebiałych znaków; nie wystarczy dodać pełne dowody tekstowe do każdego regionu.
Prywatny raport `responses/spqr-p032-codex-review-20261007-1.json` i gotowy prompt
`responses/spqr-p032-correction-prompt-20261007.txt`. Poprawkę zapisać pod nową nazwą poza pakietem.

Wstępne porównanie renderów: scalona tabela 4x2, diagram, podpis, kierunki i kolorowe noty są reprezentowane
spójnie z próbką; dwie kontynuacje pozostają lukami. Nie nadano zatwierdzenia znaczenia/kompletności.
Rekonstruowany przez `resolve_text` tekst ma liczne podziały wewnątrz słów przy drobnych fragmentach;
to osobne ograniczenie do późniejszego rozwiązania, bez cichego zmieniania surowej warstwy w tej sesji.

Dowód: chat „Przygotuj response dla PDF 32”, prywatny `responses/spqr-p032-codex-conversation-20261007.json`.
Faktyczna aplikacja **Codex desktop**, model `gpt sol 6.1`, `reported`, rozumowanie wysoki według właściciela;
odbiór przez narzędzie plikowe. `producer.application: unknown` zachowano. ChatGPT i Claude Desktop nadal
**nie sprawdzono**. M-DESK2 pozostaje partial; poprawność struktury i wymagana ręczna wymiana są oddzielne.
