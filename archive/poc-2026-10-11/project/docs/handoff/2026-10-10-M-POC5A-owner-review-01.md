# M-POC5A — przyjęcie 22 dokładnych lokalnych zakresów

- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Data: 2026-10-10, Europe/Warsaw. Codex, C:/repo/wargame-compiler,
feature/tests. Właściciel odpowiedział „akceptuję” po pokazaniu pakietu
22 lokalnych propozycji zgodności. Nie rozszerzono decyzji na zakresy
wyłączone z propozycji lub rozbieżne warianty wymagające wyboru.

## Wejścia i rzeczywista decyzja

first-001: 617941 bajtów, SHA-256
3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307.
context-01: 712014 bajtów, SHA-256
95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
eval-v1: SHA-256
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.
Wszystkie ponownie zgodne. Oryginały i wcześniejsze raporty/review zachowane.

Prywatny korzeń private/poc/spqr-chapter9/.
reviews/semantic-01/owner-decision-01.json prowadzi dosłowną odpowiedź,
22 dokładne zakresy z dowodami i hashami, recenzenta i wyłączenia.
owner-review-overlay-01.json zapisuje osobne reviewed dla obu odpowiedzi
bez przepisywania starszego checklist. current-state-03.json i
owner-review-summary-01.md prowadzą aktualny stan po decyzji.
Nie poświadczono faktycznego otwarcia konkretnych obrazów lub całego pliku.

## Faktyczny zakres i ograniczenia

Po 22/66 potwierdzonych zakresów treści w każdej odpowiedzi; 44 zakresy
lokalne i 8 kontekstu, razem 52 oczekiwania, nadal pending. W części .2
pozostają trzy zakresy do rozstrzygnięcia; .3/.4 ma pozostałe 49.
85 diagnostycznych par rubryka/oczekiwanie dziedziczy wyłącznie zgodność
komponentów z zaakceptowanego reviewed_scope; nie powiększa mianownika
reguł i nie akceptuje całych kategorii lub pozycji inwentarza.

Błędny lokator i granice glifów zachowane. Akceptacja znaczenia nie
zaakceptowała dowodu geometrycznego, nowych/pozostałych relacji, aliasów,
szerszych pól/metadanych, realnego setupu, sytuacji lub całego grafu.
Wcześniejsze propozycje błędów i interpretacji nadal pending.
Odpowiedź „akceptuję” nie wskazała wariantu w nowej kwestii blokowania;
poproszono tylko o wybór tego wariantu, bez ponawiania zgody na 22 zakresy.
M-POC5A nadal partial/waiting_review, brak pełnych metryk lub TP/FP/FN.

Nie wykonano ekstrakcji, nowych źródeł/pass-02, korekt, M-POC5B ani M-POC6/7.
Łącznie nadal 1 strona/1 reguła/0 tabel, 1 runda kontekstu/0 korekt.
Stop pozyskiwania na granicy 2 zachowany, trzeciego źródła brak.
Historyczne niewiadome selektorów/czasów/tokenów/ceny i aktywnego budżetu
pozostają unknown. Listing/path discovery poza allowlistą potwierdzone;
ekspozycja i czysty kontekst unknown, bez dowodu skażenia lub pełnej izolacji.
Kalendarzowe czasy zapisu nie są aktywnym pomiarem.

## Dokładne wznowienie

Od current-state-03.json: wybór wariantu blokowania i pozostałe pending
pierwszego pakietu oraz części .2; następnie osobny pełny zakres .3/.4.
Nowe decyzje zapisywać osobno z dokładnymi hashami i zakresem, nie zmieniać
odpowiedzi, eval-v1 lub historycznych pomiarów. M-POC5 jedyny next.

Kontrole scripts/check.ps1 i git diff --check, audyt zakresu decyzji,
niezmienność i append-only sessions.jsonl prowadzi nowy pomiar
measurement/M-POC5A-owner-review-001/completion.json. Publikacji Git nie polecono.
Kontrole: **122 passed**, git diff --check bez błędów. Audyt zachował 225
chronionych plików, wcześniejsze decyzje/pakiety/pomiary i pierwotny prefiks
sessions.jsonl. Ostrzeżenia CRLF→LF w trzech dokumentach nie były błędami.
