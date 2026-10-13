# M-POC5A.4b1 — rzeczywisty przegląd relacji

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wykonawca:** Codex, C:/repo/wargame-compiler, feature/tests
- **Wynik:** partial / waiting_review; pełny przydział porównany przez oceniającego
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A
- **Następna osobna część:** M-POC5A.4b2 po pakiecie decyzji .4b1

Zweryfikowano oryginalne bajty/hash obu odpowiedzi, eval-v1 i PDF. Szacunek
75–90 minut dla pełnej .4b1 zapisano przed semantycznym review. Porównano
wszystkie 65 ID / 125 wystąpień (60/65), źródłowe zakresy obu końców,
kierunek, rodzaj, jawność, konieczność i wpływ braków. Osobno porównano
22 zamrożone pary na wynik. Nie wykonano pozostałych partii.

Nowy prywatny pakiet reviews/semantic-01/part-04b1/ zawiera czytelne
comparisons.md i pełne comparisons.json z dowodami/pointers/bajtami,
review, issues, owner-focus, presentation i manifest. 60 ID / 116 wystąpień
ma pozytywne propozycje tylko w opisanych zakresach; 5 ID / 9 wystąpień
wydzielono do decyzji. Treść w prozie rozdzielono od braków osobnych rekordów.
Zachowano 3 krytyczne brakujące pary, 4 wzmianki i różnicę rodzaju; nie nadano
automatycznych TP/FP/FN. Nowe SEM-014–016 są propozycjami, nie werdyktami.

Udostępniony pakiet 125 / porównane przez oceniającego 125 / nowe human review
0 / pending 125. Faktyczny odczyt właściciela unknown. Additive stan:
current-state-09.json. owner-decision-03 i overlay-03 bez zmian: po 63 lokalne
zakresy i 3 wymagania źródła na wynik, 8 oczekiwań pending. Wcześniejsze
SEM-001–013 i warianty zachowane. Pełne metryki i budżet not_assessable/unknown.
105 niepotwierdzonych kandydatur nie staje się gold ani mianownikiem recall.

Bez nowych źródeł/pass-02, ekstrakcji/korekt, API inferencji, procesów modelowych,
nowych czatów, M-POC5B/6/7, architektury i commit/push. Nadal 1 dodatkowa strona /
1 reguła / 0 tabel, 1 runda / 0 korekt, 0 pełnych domknięć, 4 częściowe aktualizacje
i 4 nowe deklaracje. Trzeciego źródła nie pozyskano, stop ekspansji na granicy 2.
Izolacja nazw/ścieżek naruszona w historycznym context-01; odczyt treści oceny
niezaobserwowany, ekspozycja/czysty kontekst unknown, bez dowodu skażenia lub
pełnej izolacji. Aktywne czasy, selektory, tokeny, cena i zgodność budżetu unknown.

Dokładne wznowienie: owner-focus części .4b1 oraz wcześniejsze pending,
nowy owner-decision dopiero po rzeczywistej decyzji; następnie osobna .4b2
z istniejącą listą 30 ID / 60 wystąpień i oszacowaniem przed wykonaniem.
.4b3 (36/72), .4c/.4d i M-POC5B osobno. Pozostałe 132 wystąpienia przypisane.
M-POC5A/.4/.4b pozostają partial; M-POC5 jedyny next.

Rzeczywiste logi kontroli, audyt i append-only pomiar:
measurement/M-POC5A-semantic-04b1/ pod prywatnym korzeniem. Wyniki końcowych
kontroli prowadzi completion.json; nie nadają semantycznej akceptacji.

Kontrole: **135 passed**, git diff --check bez błędów. Zweryfikowano 35 095
zakresów provenance oraz zachowanie 1079 chronionych plików i wcześniejszego
prefiksu sessions.jsonl. Pierwsza kontrola wykazała błąd spójności nowego
handoffu; dokument poprawiono i zachowano log nieudanej kontroli.
