# M-POC5A — akceptacja części .3 i prompt do osobnej .4a

- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Data: 2026-10-10, Europe/Warsaw. Codex, C:/repo/wargame-compiler,
feature/tests. Właściciel: „Akceptuję i podaj prompt dla nowej sesji”.
Zapisano zgodę na dokładny pokazany pozytywny zakres części .3;
nierozstrzygnięte warianty nie zostały wybrane za człowieka.
Nowego czatu, ekstrakcji, korekty ani publikacji Git nie uruchomiono.

## Wejścia i decyzje

first-001: 617941 bajtów, SHA-256
3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
context-01: 712014 bajtów, SHA-256
95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
eval-v1: SHA-256
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.
Źródło PDF również zgodne. Źródła, odpowiedzi, wejścia, ocena oraz
wcześniejsze raporty/review/decisions/pomiary zachowane.

Prywatny korzeń private/poc/spqr-chapter9/.
reviews/semantic-01/owner-decision-02.json zapisuje 21 nowych lokalnych
zakresów i 2 wymagania źródła osobno dla obu hashów, z zakresem/dowodami,
recenzentem i wyłączeniami. owner-review-overlay-02.json prowadzi stan
łączny, current-state-05.json i owner-review-summary-02.md wznowienie.
Nie poświadczono faktycznego otwarcia konkretnych obrazów przez właściciela.

## Łączny wynik i otwarte zakresy

Po 43/66 zaakceptowanych lokalnych zakresów treści i 2/8 przejrzanych
wymagań kontekstu. Te dwa wymagania nie zamykają pełnych wyników/luk.
23 lokalne/6 kontekstu pending, razem 29 oczekiwań: 5 wcześniejszych
i ostatnie 24. 175 diagnostycznych par dotyczy tylko przyjętych komponentów,
nie dodatkowych punktów reguł ani całych kategorii.

Warianty i wcześniejsze rozbieżności nadal pending. Relacje/TP/FP/FN,
lokatory i granice glifów, szersze pola/aliasy, rzeczywiste dane setupu,
małe ratingi grafik i sytuacje nie zostały zaakceptowane.
Pełne metryki i budżet nieocenione; M-POC5A nadal partial.

## Podział i dokładna następna sesja

Przed wykonaniem podzielono nadrzędną .4: .4a ostatnie 24 oczekiwania,
.4b wszystkie relacje, .4c lokatory, .4d pozostały inwentarz/wcześniejsze
pending i rozliczenie. Karty, indeks, ROADMAP i STATUS zaktualizowane.
Większą część dzielić dalej przed wykonaniem, z listą ID; żadnego pominięcia.

Właściciel ręcznie otwiera nową sesję na C:/repo/wargame-compiler,
feature/tests i wskazuje prompts/semantic-review-part04a-start-v1.txt.
Ta sesja wykonuje tylko M-POC5A.4a: EXP-051–074 i powiązane zakresy.
Czyta aktualne decyzje, oba wyniki i eval-v1; przygotowuje nowe dodatki,
pokazuje dowody, a właściciel decyduje. .4b/.4c/.4d nie w tej samej sesji.
Nie oznaczać całej M-POC5A done, nie przechodzić do M-POC5B automatycznie.

Wcześniejsze ograniczenia zachowane: 1 dodatkowa strona/1 reguła/0 tabel,
1 runda kontekstu/0 korekt, brak trzeciego źródła, stop na granicy 2,
bez certyfikatu całego grafu. Izolacja nazw/ścieżek naruszona; ekspozycja
i czysty kontekst unknown, bez dowodu skażenia lub pełnej izolacji.
Selektory/aktywne czasy/tokeny/cena/budżet unknown; kalendarz nie mierzy
aktywnego czasu. Nowe źródła/pass-02, M-POC5B/6/7 i architektura wyłączone.

Kontrole i append-only pomiar decyzji/przekazania:
measurement/M-POC5A-owner-review-002/completion.json; scripts/check.ps1,
git diff --check, audyt niezmienności i zakresów z rzeczywistymi logami.
Wynik: **128 passed**, git diff --check bez błędów; 259 chronionych plików
i pierwotny prefiks sessions.jsonl zachowane. Prompt oraz karty podziału
zweryfikowano, bez wykonania .4a. Ostrzeżenia CRLF→LF w trzech edytowanych
dokumentach publicznych nie były błędami kontroli.
