# M-POC5A.4a — ostatnie 24 porównania, waiting_review

- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Część:** M-POC5A.4a
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Data: 2026-10-10, Europe/Warsaw. Codex, C:/repo/wargame-compiler,
feature/tests. Wykonano tylko porównania EXP-051–074 z promptu .4a;
polecenie kontynuacji nie nadało akceptacji znaczenia. Zastane zmiany
zachowano. Bez ekstrakcji, korekty, nowych źródeł lub publikacji Git.

Oryginały zgodne: first-001 617941 bajtów,
SHA-256 3a4f7d9a1d20373fe5c320850456b8cb1acce5db00b86b5ca98f410656c51307;
context-01 712014 bajtów,
SHA-256 95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b.
eval-v1 manifest SHA-256
7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce;
PDF SHA-256 e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e.

Prywatny korzeń private/poc/spqr-chapter9/. Nowe artefakty:
reviews/semantic-01/part-04a/ (comparisons, review, issues, owner-focus,
presentation, manifest), additive current-state-06.json oraz osobny
measurement/M-POC5A-semantic-04a/. Porównano 21 zakresów lokalnych i 3
wymagania kontekstu, 31 powiązanych pozycji i 95 diagnostycznych par.
26 mapowanych rekordów zachowuje wartości, przy osobnych bajtach/hashach.
Propozycje: 20 lokalnych zgodności, 1 właściwa potrzeba/blokada źródła,
3 kwestie wymagające osobnej decyzji. Nie są to nowe zaakceptowane wyniki.

Właściciel nadal przyjął po 43/66 lokalnych zakresów i przejrzał 2/8
wymagań kontekstu, bez domknięcia pełnych wyników. 23 lokalne/6 kontekstu
pending. Wszystkie 74 oczekiwania mają teraz porównanie; cały review
niezamknięty. Wcześniejsze pending i kwestie zachowane. Pełne metryki,
TP/FP/FN, graf, lokatory, rzeczywiste ratingi i sytuacje niezaakceptowane.

Dokładne wznowienie: właściciel porównuje part-04a/owner-focus.md i pełny
review.md, decyduje o pozytywnym zestawie oraz trzech kwestiach osobno.
Zapisać nową owner-decision z hashami i dokładnymi reviewed_scope tylko
po rzeczywistej decyzji. Nie zmieniać wcześniejszych decyzji lub pakietów.
Następnie osobna .4b dla relacji; .4c i .4d nadal planned. Przed wykonaniem
większej części podzielić zakres z ID. M-POC5A i nadrzędna .4 partial,
M-POC5 jedyny next. M-POC5B dla 20 sytuacji jest osobną kartą.

Ograniczenia zachowane: 1 dodatkowa strona/1 reguła/0 tabel, 1 runda
kontekstu/0 korekt; 0 pełnych domknięć, 4 częściowe uzupełnienia nadal
blocking, 4 nowe deklaracje. Brak trzeciego źródła, stop ekspansji na
granicy 2. Listing/path discovery poza allowlistą potwierdzony; treść
oceny niezaobserwowana, ekspozycja/czysty kontekst unknown, bez dowodu
skażenia lub pełnej izolacji. Aktywny czas/budżet, selektory, tokeny i cena
unknown. Kalendarz nie mierzy aktywnego budżetu.

Kontrole i końcowy audyt prowadzi nowy completion.json w pomiarze .4a,
z rzeczywistymi logami scripts/check.ps1 i git diff --check. Zweryfikowano
35 095 zakresów provenance obu odpowiedzi i 1018 chronionych plików.
Kontrole integralności nie akceptują znaczenia.

Wynik scripts/check.ps1: **129 passed**, git diff --check bez błędów,
lokalne TMP/TEMP i nowy basetemp. Ostrzeżenia CRLF→LF są zapisane w logu,
nie były błędami kontroli. Pakiet owner-focus przekazano do panelu Codex
ze statusem queued; brak dowodu faktycznego odczytu obrazów/raportu przez
właściciela. Nowych decyzji 0; sessions.jsonl dopisany wyłącznie append-only.
