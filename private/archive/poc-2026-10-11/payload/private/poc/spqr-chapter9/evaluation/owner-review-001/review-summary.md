# M-POC1A: rzeczywisty przegląd właściciela

Data: 2026-10-07, Europe/Warsaw. **Wynik karty: done**.
**M-POC1 nadal next; następna karta M-POC1B, niewykonana.**

Recenzent: właściciel w tym czacie; nie przypisano nazwiska ani innej tożsamości.
Codex pokazywał wycinki źródła, proponował decyzje i zapisywał odpowiedzi.
Dziesięć decyzji wynika z rzeczywistych odpowiedzi użytkownika: pierwsza „tak”,
pozostałe „zatwierdzam”. Każda dotyczy bezpośrednio poprzedzającego pytania.
Czasy są czasami zapisu; dokładne znaczniki wiadomości użytkownika są nieznane.
Pełne odpowiedzi, zakresy, daty i hashe obrazów: [rejestr](review-events.jsonl).

Zakończono uzgodniony przegląd roboczego inwentarza i sposobu raportowania
niepewności. **Nie zaakceptowano znaczenia reguł, oczekiwań ani całego grafu.**
Nie przypisano właścicielowi indywidualnego przeglądu wszystkich 98 grup tekstu,
96 kandydatur lub wszystkich drobnych napisów na ilustracjach.

## Jak czytać przekazanie

1. Przeczytaj niniejszy raport i [manifest](review-manifest.json).
2. Oryginalne [inventory.json](../draft/inventory.json),
   [dependency-candidates.json](../draft/dependency-candidates.json),
   [inventory-review.md](../draft/inventory-review.md) oraz
   [source-v1.json](../../source/source-v1.json) pozostają bajtowo niezmienione.
   Ich `pending`/`waiting_review` opisuje stan sprzed niniejszego przeglądu.
3. Bieżące decyzje i korekty odczytuj z osobnego rejestru oraz czterech
   uzupełnień poniżej. Uzupełnienia nie zastępują tekstu rodziców i nie zamrażają eval.
4. Zachowaj granice akceptacji: decyzja o polityce lub pokazanym przykładzie
   nie jest indywidualną akceptacją wszystkich rekordów podobnego typu.

Źródło: SPQR 5th Edition, PDF 31–37. Pełny SHA-256 ponownie sprawdzony:
`e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.

## Decyzje właściciela

| Decyzja | Zakres zatwierdzony | Podstawa / dokładny zapis |
|---|---|---|
| 01 / U-08 | Początek od 9.0 PDF31 prawa; cała lewa i prawa przed9.0 są kontekstem | [Decyzja01](decision-01.md), A-31-R-start.png; H-9.0 |
| 02 / U-08 | Koniec przed10.0 PDF37 lewa, dokończenie9.96 i trzy punkty; kontekst wyłączony. Obserwacja9.91→9.93, brak9.92 bez dopisywania/przyczyny | [Decyzja02](decision-02.md), cztery wycinki PDF36/37; K-07/R-9.96/R-9.91/K-06/R-9.93 |
| 03 / U-04 | Jedna tabela T-01 przy9.14, kolumny Die Roll/Result, wiersze0/1–6 po lewej i7–9 po prawej; K-02. Zachowanie fragmentów pierwszego/kolejnych rzutów i Leader Elephant; D-01/X-01 jako przykład | [Decyzja03](decision-03.md), trzy wycinki PDF32; kompas mapy nadal wymaga kontekstu |
| 04 / U-05 | D-02 jeden diagram przy9.66, dwa panele; CAP-01 górny ze strzałkami, CAP-02 dolny; K-05 lewa→prawa | [Decyzja04](decision-04.md), dwa wycinki PDF35 |
| 05a / U-02 | N-14 zachowana cała; trzy fragmenty opis/instrukcyjny kandydat/opis i scenariusze. DC-038 pozostaje kandydatem wymagającym kontekstu | [Decyzja05a](decision-05a.md), wycinek PDF36 |
| 05b / U-03 | N-03/N-07/N-09 zachowane całe; po dwa fragmenty: opis i końcowe zdanie wymagające wyróżnienia | [Decyzja05b](decision-05b.md), trzy wycinki PDF32/33/34; znaczenie niezatwierdzone |
| 05c / U-01 | 98 grup jako roboczy indeks, bez98 norm/pełnej atomowości. Pokazane9.66 sześć zdań, akapit9.7 dwa fragmenty; korekta klasyfikacji C-9.71-01 i zachowanie powiązania z listą | [Decyzja05c](decision-05c.md), wycinki PDF35; inne grupy nieprzejrzane indywidualnie |
| 06a / U-06 | Polityka kandydatów i pokazane przykłady:96 kandydatur,19 tokenów zewnętrznych nie jest gold; cele zewnętrzne/aliasy wymagają kontekstu, wewnętrzne oznaczenie odnalezione nie dowodzi relacji; DC-031 pozostaje hipotezą | [Decyzja06a](decision-06a.md), DC-019–022/DC-017/DC-031 i wcześniejszy DC-038; pozostałe kandydatury bez indywidualnego review |
| 06b / U-07 | Cele scenariuszowe i mapowe, tożsamość dowódcy/przypisanie jednostek, uprawnienia i parametry armii pozostają wymagające kontekstu | [Decyzja06b](decision-06b.md), C-9.94-03/C-9.95-02 oraz wcześniejsze N-09/C-9.7-01/D-01/X-01 |
| 06c / U-09 | Obwiednia D-02 poszerzona do674pt; render podstawą grafiki/typografii, helper zachowany. Drobne napisy/wartości niewyczerpująco transkrybowane i bez pełnego indywidualnego review | [Decyzja06c](decision-06c.md), dwa wycinki PDF35/37; D-02/CAP-02/C-9.96-07 |

## Uzupełnienia i mapa zmian

| Uzupełnienie | Zmiana | Mapa |
|---|---|---|
| [05a](inventory-supplement-05a.json) | N-14-S1–S3: opis przed Thus; pełne zdanie Thus ignore jako kandydat instrukcyjny; pozostały opis i wzmianka scenariuszowa | [Mapa05a](change-map-05a.json) |
| [05b](inventory-supplement-05b.json) | N-03/N-07/N-09, po S1/S2; końcowe zdania o stosowalności, klasyfikacji/manewrze i kontekście scenariusza | [Mapa05b](change-map-05b.json) |
| [05c](inventory-supplement-05c.json) | C-9.66-01-S1–S6, C-9.7-01-S1/S2; C-9.71-01: `heading_or_list_introduction` → `instruction_bearing_and_list_introduction_candidate` | [Mapa05c](change-map-05c.json) |
| [06c](inventory-supplement-06c.json) | D-02: `[80,516,266,665]` → `[80,516,266,674]`; osobna adnotacja typograficzna przy C-9.96-07, bez zmiany helpera | [Mapa06c](change-map-06c.json) |

Łącznie: **17 dodatkowych fragmentów źródłowych, 2 korekty metadanych**.
Nie dodano oznaczeń reguł. Bazowe liczniki pozostają: 41 reguł, 98 grup tekstu,
14 not, jedna tabela, dwa diagramy, siedem kontynuacji; 190 rekordów bazowych.
Źródło, rodzice, stare ID i cały pierwotny tekst pozostają dostępne.
Obwiednie dodatkowych fragmentów tekstu obejmują kontekst rodzica; precyzyjny
fragment lokalizuje dosłowna transkrypcja w jego dowodzie. Nie są to nowe dokładne
prostokąty każdego zdania/glifu.

## Kryteria i pozostałe niepewności

[Ocena kryteriów](criteria-review-v1.json) rozlicza źródło, granice, obszary,
typy/ID/dowody, kandydatury oraz rzeczywisty przegląd. Końcowe kontrole
domyka [completion-checks-v1.json](completion-checks-v1.json).

- U-08: granice i obserwacja numeracji rozstrzygnięte.
- U-04/U-05: wskazana struktura tabeli, diagramów, podpisów i kontynuacji rozstrzygnięta;
  kompas konkretnej mapy pozostaje wymagający kontekstu.
- U-02/U-03: sposób zachowania i wyróżnienia tekstu not rozstrzygnięty;
  dokładny zakres operacyjny i znaczenie nie są zatwierdzone.
- U-01: polityka i pokazane podziały zatwierdzone. Pełny podział atomowy oraz
  pozostałe grupy bez indywidualnego przeglądu właściciela.
- U-06: zatwierdzona polityka i pokazane przykłady; graf, rodzaje/kierunki,
  konieczność i krytyczność relacji nie są zweryfikowane.
- U-07: zatwierdzone odroczenie; uprawnienia scenariuszowe, data/dowódca,
  przypisanie jednostek, parametry armii i mapy nie są uzupełnione.
- U-09: korekta i ograniczenia dowodów zaakceptowane; pełna transkrypcja
  drobnych napisów/wartości grafiki pozostaje niewykonana.

To świadomie opisane ograniczenia dalszej oceny. **Done karty M-POC1A nie nadaje
tym fragmentom statusu gold ani akceptacji semantycznej.**

## Kontrole i czas

Audyt lokalnych ID, rodziców, fragmentów źródła, map zmian, decyzji, hashy wycinków
oraz niezmienności czterech oryginalnych artefaktów: [passed](integrity-audit-v1.json).
Audyt9298 historycznych plików: [wynik](historical-integrity-audit-v1.json).

Pierwszy check:60 passed/1 failed — format `done;` w polu STATUS zamiast `done`.
Naprawiono separator w dokumencie, nie osłabiono kontroli.
Następny check: **61 passed**, diff-check0, nowy basetemp i lokalne TMP/TEMP.
Log: `private/poc/_checks/active-fd8ddbc15c6d4b7f9aa5e1f6d4fd360f/`.
Ostateczny log po uzupełnieniu dokumentacji jest w completion-checks-v1.json.

Aktywna kontrola ciągłości odróżnia zakończenie jednej karty od zakończenia
milestone'u; osiem przypadków pozytywnych/negatywnych chroni kolejność A/B/C.
Testy legacy bez zmian. Żaden check nie nadaje znaczeniu statusu akceptacji.

Czas kalendarzowy wieloturowego przeglądu obejmuje oczekiwanie na odpowiedzi.
Dokładny czas aktywnej pracy właściciela/modelu, tokeny i cena: unknown.
Pomiar kalendarzowy i ograniczenie pomiaru budżetu90min zapisano w measurement/sessions.jsonl.

## Dokładny następny krok

W kolejnej sesji wykonać bootstrap i kartę **M-POC1B**, zaczynając od tego raportu,
manifestu, uzupełnień/map oraz oryginalnego draftu. Dopiero tam przypisywać
krytyczność, sprawdzać relacje i opracować 15–20 sytuacji z dowodami lub
uzasadnioną blokadą. W tym przeglądzie nie wykonano M-POC1B/C ani M-POC2B;
nie utworzono oczekiwań/sytuacji i nie zamrożono eval-v1.
