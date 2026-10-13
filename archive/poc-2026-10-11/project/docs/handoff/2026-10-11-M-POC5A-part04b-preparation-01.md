# M-POC5A — prompt i podział .4b przed wykonaniem

- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

2026-10-11, Europe/Warsaw. Codex, C:/repo/wargame-compiler, feature/tests.
Właściciel poprosił o prompt do nowej sesji na duży postęp. Przygotowano
konkretny zakres; nie uruchomiono review relacji ani nowej sesji/czatu.

Nadrzędne .4b obejmuje 126/131 wystąpień relacji (257), 131 różnych ID.
Podział PRZED wykonaniem: .4b1 65 ID i 60/65 wystąpień (125), .4b2 30 ID
i 30/30 (60), .4b3 36 ID i 36/36 (72). Przydział rozłączny i wyczerpujący;
statusy ekstraktora służą routingowi i nie są oceną znaczenia/konieczności.
Listy prywatnie w measurement/M-POC5A-part04b-preparation-001/scope-plan.json
pod private/poc/spqr-chapter9/. Karty .4b1/2/3 w docs/work/tasks/semantic/.

Pierwsza duża partia obejmuje wszystkie relacje ze wskazanym dostępnym
celem, wzmianki, kontynuacje i pięć nowych relacji po kontekście; dodatkowo
zamrożone pary i jawne brakujące krytyczne powiązania. To plan, nie wynik.
Przed review nowa sesja oszacuje .4b1 i podzieli ją dalej z pełnymi ID,
jeśli przekracza 90 minut; wykona jedną największą spójną pierwszą część.
.4b2/.4b3/.4c/.4d osobno. Żadnego ukrytego pominięcia przypisanych ID.

Prompt: prompts/semantic-review-part04b1-start-v1.txt pod prywatnym korzeniem.
Właściciel ręcznie otwiera nową sesję i wskazuje ten plik. Prompt wymaga
rzeczywistego porównania, śladów obu odpowiedzi i opisu decyzji po ludzku:
źródło, zapis modelu, różnica, wpływ, propozycja i wyłączenia. Sam rejestr
pending lub techniczne ID/liczniki nie zastępują review lub objaśnienia.

Nowy additive current-state-08.json prowadzi planowanie. Semantyczny stan
owner-decision-03.json/owner-review-overlay-03.json bez zmiany: po 63/66
lokalnych zakresów i 3/8 wymagań kontekstu przejrzanych, 8 oczekiwań pending.
264 par rubryka/oczekiwanie to tylko przyjęte komponenty, nie dodatkowe punkty.
Przyjęta potrzeba źródła nie zamyka pełnego wyniku; wcześniejsze pending,
wszystkie relacje, lokatory, realne ratingi i sytuacje zachowane.
Pełne TP/FP/FN i aktywny budżet nieocenione. M-POC5A/.4/.4b partial,
M-POC5 jedyny next; brak akceptacji relacji z samego podziału.

Te same oryginały/hash/bajty i eval-v1. Brak nowych źródeł/pass-02,
ekstrakcji/korekt, API inferencji, automatycznych procesów modelowych,
M-POC5B/6/7 i architektury. Zachowano 1 dodatkową stronę/1 regułę/0 tabel,
1 rundę/0 korekt, 0 pełnych domknięć/4 częściowe uzupełnienia/4 deklaracje,
brak trzeciego źródła i stop na granicy 2. Izolacja/ekspozycja oraz
selektory/aktywny czas/tokeny/cena/budżet nadal unknown w zapisanym zakresie.

Kontrole, audyt niezmienności i append-only pomiar przygotowania:
measurement/M-POC5A-part04b-preparation-001/completion.json. Nie wykonano
dalszej części, nowych czatów, wiadomości do innych czatów ani commit/push.

Kontrole przygotowania: **134 passed**, git diff --check bez błędów; 1067 chronionych plików zachowanych. Wszystkie 257 wystąpień przypisano dokładnie raz; review relacji niewykonane.
