# M-POC5A — część .3, porównanie EXP-026–050

- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Data: 2026-10-10, Europe/Warsaw. Codex, C:/repo/wargame-compiler,
feature/tests. Po „kontynuuj” wykonano niezależne porównania części .3;
nie wybrano wariantów wcześniejszych pending za właściciela.
Poprzednia akceptacja 22 lokalnych zakresów zachowana.

## Wejścia i integralność

first-001: 617941 bajtów, SHA-256
3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
context-01: 712014 bajtów, SHA-256
95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
eval-v1: SHA-256
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.
Źródło PDF także ponownie zgodne. Źródła, odpowiedzi, wejścia, ocena,
zamknięte raporty oraz wcześniejsze review/decisions/pomiary zachowane.

## Faktyczny zakres

Prywatny korzeń private/poc/spqr-chapter9/.
reviews/semantic-01/part-03/ zawiera comparisons.json, review.md,
issues.json, owner-focus.md, presentation.json i manifest.json.
Aktualny dodatek prowadzi current-state-04.json, nie przepisywanie checklist
lub wcześniejszej decyzji. Każdy wynik ma osobny hash i ślady do bajtów.

Porównano 25 oczekiwań: 22 lokalne i 3 kontekstu; powiązano 44 pozycje
źródłowe i 94 diagnostyczne pary rubryka/oczekiwanie. Propozycje modelu:
21 lokalnych zgodności, 2 właściwe potrzeby/blokady źródła, 1 niepełna
interpretacja lokalna i 1 jawność setupu do decyzji. Wszystkie nowe oceny
człowieka pending. Obejrzenie źródłowych regionów nie certyfikuje wszystkich
glifów, małych ratingów grafik lub pełnych szerszych pozycji inwentarza.

24 z 26 mapowanych reguł/węzłów mają te same wartości; dwa zmienione
zakresy pokazano osobno wobec źródła. Równość wartości nie poświadcza
leksykalnej identyczności bajtów. Dodany endpoint źródła nie zamyka pełnej
alokacji; interpretacja i kolejność działań nadal do przeglądu.

## Przegląd człowieka i ograniczenia

Właściciel otrzymał konkretny pakiet 21 lokalnych zakresów i 2 wymagań
źródła do decyzji oraz osobną kwestię jawności potrzeb setupu. Wcześniejsze
rozbieżności i warianty nadal pending. Nie nadano nowych akceptacji, TP/FP/FN
ani pełnych metryk. Nadal po 22/66 lokalnych zakresów przyjętych,
44 lokalne i 8 kontekstu pending. .4 ma 24 nieprzejrzane oczekiwania
oraz pozostałe szersze pozycje, wszystkie krawędzie i lokatory.

Nie pozyskano nowych źródeł/pass-02; 0 ekstrakcji, 0 kontekstu, 0 korekt
i 0 ocen sytuacji w tej części. Łącznie nadal 1 strona/1 reguła/0 tabel,
1 runda kontekstu/0 korekt, stop pozyskiwania na granicy 2. Trzecie źródło
niepozyskane; bez certyfikatu całego grafu. Krytyczny brak blokuje pełny
zależny wynik; znane lokalne operatory z zadanymi faktami oceniane osobno.

Historyczne ekspozycja/czysty kontekst i selektory/czasy/tokeny/cena oraz
aktywny budżet unknown. Naruszenie listing/path discovery nadal potwierdzone,
bez dowodu skażenia lub pełnej izolacji. Kalendarz nie jest aktywnym pomiarem.
Jedno diagnostyczne drukowanie danych grafiki zgłosiło brak opcjonalnego
pola tekstu; odczyt dostosowano i obraz obejrzano, bez wpływu na odpowiedzi.

## Dokładne wznowienie

Od current-state-04.json i part-03/owner-focus.md: decyzje właściciela
w dokładnych zakresach i hashach, z wyłączeniami; osobno wcześniejsze pending.
Nie traktować akceptacji lokalnego operatora jako zamknięcia pełnego wyniku
lub akceptacji nowej krawędzi. Następnie osobna część .4; przed wykonaniem
podzielić ją dalej, jeśli całość nie mieści się w 90 minutach.
M-POC5 jedyny next, M-POC5A partial. M-POC5B, M-POC6/7 niewykonane.

Kontrole scripts/check.ps1, git diff --check, audyt integralności i
append-only sessions.jsonl prowadzi nowy pomiar
measurement/M-POC5A-semantic-03/completion.json. Publikacji Git nie polecono.
Wynik: **123 passed**, git diff --check bez błędów. Audyt zachował 241
chronionych plików i wcześniejszy prefiks pomiarów, sprawdził 33 różne ślady
do oryginalnych rekordów w każdym wyniku. Ostrzeżenia CRLF→LF w trzech
dokumentach nie były błędami. Nowe decyzje człowieka nadal pending.
