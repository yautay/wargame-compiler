# M-POC5A.4d1 — przegląd pierwszej partii inwentarza

- **Data:** 2026-10-11, Europe/Warsaw
- **Milestone:** M-POC5
- **Karta:** M-POC5A
- **Wynik:** partial
- **Następny milestone:** M-POC5
- **Następna karta:** M-POC5A

Właściciel zatwierdził .4c3: 38 ograniczonych ocen komponentów.
Wszystkie 124 przypisane wystąpienia lokatorów mają teraz decyzje
właściciela; nie jest to akceptacja całych rekordów ani dobrych ramek.
Oryginalne wady zachowano. Owner-decision-10/overlay-10 prowadzą stan.

Przed review podzielono .4d na pięć osobnych kart, z rozłącznym przydziałem
39/68/59/41 pozycji i osobnym końcowym uzgodnieniem. Wykonano wyłącznie
.4d1: 39 pozycji / 78 wystąpień, osobno 39/39 w obu odpowiedziach.
Rzeczywiście porównano nagłówki, noty i przykłady w dostarczonych źródłach
z oryginalnymi rekordami. Prywatny pakiet part-04d1 zawiera dokładne
zakresy źródłowe, pola, hash/pointer/bajty, niepewności i owner-focus.

Proponowane 76 ocen ograniczonego wsparcia treści oraz 2 oceny częściowego
pominięcia w treści noty, z poprawnym cytatem dowodowym. Struktury danych
nie otrzymują certyfikatu dosłownej transkrypcji. Udostępniono 78,
porównano 78, nowych decyzji właściciela 0, pending 78. Faktyczny odczyt
plików przez właściciela unknown. Starsze nierozstrzygnięcia i wyłączone
pola pozostają otwarte. Pełne metryki not_assessable, gold bez zmiany.

257 wcześniejszych zakresów relacji, 124 zakresy lokatorów, 264 pary
rubryka/oczekiwanie, po 63 lokalne zakresy/3 wymagania źródła i 8 dawnych
oczekiwań pending zachowano. Nie dodaje się punktów za parent/child.
current-state-22 prowadzi nowy wynik. Nadrzędne karty partial;
M-POC5 pozostaje jedynym next.

Po decyzjach .4d1 pozostały cztery karty .4d: 168 pozycji w trzech
partiach 68/59/41, następnie końcowe uzgodnienie. Potem osobne M-POC5B:
20 zamrożonych sytuacji w dwóch odpowiedziach, czyli 40 ocen.
Pierwotny ogólny szacunek .4d 300–420 minut zachowano; suma zapisanych
przed review zakresów pięciu części wynosi 330–430 minut. Szacunek
obecnej części 70–85 minut. Przed kolejną częścią odświeżyć jej szacunek;
nie wykonano jej w tej sesji. Czas aktywny i zgodność budżetu unknown.
Nie wykonano nowych źródeł, ekstrakcji, korekt, czatów, commit/push.
Pomiar: measurement/M-POC5A-semantic-04d1/.

Wykonawca Codex; właściciel akceptuje znaczenie. Nowe propozycje
waiting_review, oryginalne odpowiedzi i wszystkie dawne prywatne artefakty
bez zmian. Hashe prowadzi nowy manifest i audyt niezmienności pomiaru.
Nie przenosić nowej pozytywnej oceny na starsze pending lub szersze pola.

Kontrole: scripts/check.ps1 offline, lokalne TMP/TEMP i nowy basetemp,
git diff --check, walidacja dokładnych bajtów/pointers i końcowy audyt.
Rzeczywiste wyniki i jeden append sessions.jsonl: nowy completion.json.
Selektory modelu/rozumowania, czasy aktywne, tokeny/cena/budżet unknown.
Historyczne naruszenie izolacji nazw/ścieżek zachowane; odczyt treści
oceny niezaobserwowany; exposure/clean context unknown.
Limity zachowano:1 dodatkowa strona/1 reguła/0 tabel,1 runda/0 korekt,
0 pełnych domknięć luk,4 częściowe uzupełnienia/4 nowe deklaracje,stop2.
