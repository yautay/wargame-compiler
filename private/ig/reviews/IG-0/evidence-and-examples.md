# IG-0 — dowody, kontrprzykłady i szkice reprezentacji

2026-10-11. Materiał prywatny. Autor: Codex; exact model i reasoning unknown.
Status: manual_design_review, nie blind extraction, nie human_accepted.
Żaden szkic poniżej nie jest pełnym snapshotem ani wykonywalnym programem.
Skrócone identyfikatory S/T/N/D/G oznaczają rekordy źródeł w
[sources-manifest.json](sources-manifest.json). Hashe nie są zgadywane.
Pola szkiców są propozycją recenzenta, nie potwierdzonym schematem 0.2.

## Rejestr odczytu bieżącej sesji

Pełny odczyt instrukcji gry: **brak**. Odczyt całego tekstu stron nie
ustanawia pełnego odczytu wszystkich symboli i diagramów na tych stronach.
Automatycznie wydobyto tekst pobranych PDF, także stron nieprzeczytanych.
Pliki tekstowe są pomocą lokalizacyjną, nie nowym źródłem normatywnym.

| Źródło | Odczyt w tej sesji | Kontrola obrazu / niewiadome |
|---|---|---|
| S, spqr, 44 strony, 5E | Pełny tekst PDF 12, 13, 15, 26, 27. Metadane source-v1 i hash oryginału przez manifest POC | Obejrzano PDF 13 i 26 w renders/. Nie obejrzano ponownie całej instrukcji ani wszystkich dawnych renderów |
| T, tlnb, 24 strony | Okładka Version 7.38; tekst PDF 2, 5, 6, 9, 18 | Obraz PDF 9 obejrzany. Kontynuacja LOS z PDF 8 nieodczytana w całości; bez odtwarzania kompletnej polityki LOS |
| tlnb-tables, 4 strony | Tekst PDF 2: nagłówki, legendy i noty; wersja 2.7 / 7 January 2019 | Bez wizualnego review komórek; tekst pomieszany kolejnością. Zgodność z 7.38 unknown |
| N, nab, 9 stron | Pełny tekst PDF 1–3: 2020-b, ¶1–40 | Obraz PDF 3 obejrzany. CNS Standard Rules, manifesty sił, tory i tabele nieprzeczytane |
| D, lastdays, 32 strony | Pełny tekst PDF 10–11: dowodzenie, 8.0–8.4 | Obraz PDF 10 obejrzany. PDF1 jest pusty także w renderze Popplera. Etykieta „2nd Edition” pochodzi z wejściowej bibliografii; nie potwierdzono jej na PDF1; używać hasha |
| sevendays, 27 stron | Pełny tekst PDF 3, zwłaszcza 1.4 Mixed Type | Bez obrazu. 3.27 to nazwa pliku, nie potwierdzone wydanie. Pozostałe strony nieprzeczytane |
| G, gcacw, 24 strony | Tekst PDF 6–7 i 12; PDF 9: 5.3, 5.4 i część 5.5; PDF 11 fragmenty przy 6.3/7.1; PDF 16 fragment 7.5 o przyczynie fatigue | Obraz PDF 12 obejrzany. Basic 1.6; nie całe Advanced ani recovery |
| gcacw-tables, 4 strony | PDF 1: nagłówek, dwie grupy kolumn, legenda, noty, role i podtabele | Obraz PDF 1 obejrzany; nie zatwierdzono transkrypcji wszystkich komórek. Tytuł Thunder on the Mississippi, v1.6 |
| rtg2, 120 stron | Pełny tekst PDF 20: Here Come the Rebels, 6.3 Supply Status wraz z końcówką wcześniejszego paragrafu | Bez obrazu; pozostałe części tomu i ich zgodność z Basic 1.6 nieweryfikowane |

Strony WWW: przeczytano sekcję LIVING RULES/Description na oficjalnej
stronie GMT SPQR5, listę TLNB w OSG Game Support Files, opis CNS 1X oraz
listę Series Rules/Game Specific Rules w MMP GCACW Downloads. Linki do
konkretnych PDF zawiera manifest; linki katalogów — publiczna recenzja.
Pobranie OSG przez web zwracało błędy. Bezpośrednie pobranie przez urllib
po dopuszczeniu dostępu sieciowego powiodło się dla ośmiu PDF.

SPQR: odnaleziono wpis manifestu o original_path
`private/poc/spqr-chapter9/source/original-pdf-20261008-01.pdf`, zweryfikowano
SHA-256 `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.
Źródła historyczne znalezione tą samą metodą: source-v1.json,
formats/proposal-format-v1.md i docs/STATUS.md. Format i metadane przeczytano
w całości; STATUS fragmentami (stan bieżący archiwum i wybrane wcześniejsze
liczby), bez zmiany lub wznowienia historycznych zadań.

Nie przenoszono wcześniejszych odczytów SPQR4, scenariuszy2018, zmian7.36,
not TLNB i capacity aid do kategorii „sprawdzone w tej sesji”. Brak ponownego
odczytu tych pozycji nie oznacza, że są fałszywe; ich ustalenia mają słabszą
podstawę w bieżącej recenzji. Nie potwierdzono pełnego modelu zwycięstwa,
pełnej geometrii map ani kompatybilności wszystkich materiałów.

## Errata materiału wejściowego

1. W acceptance-cases IG-C26 i IG-C27 odwołują się do GCACW1.6 5.4.
   W pobranym Basic1.6 **5.4 dotyczy Burn RR Station**, nie procedury assault.
   Właściwa podstawa dla naturalnego rzutu i zbioru wybranych uczestników
   assault to **7.1, PDF12, Attack Procedure (Assault Action Only), kroki 1–6**;
   5.3 PDF9 tylko wprowadza tę akcję. Alternatywny przykład raw/modified
   jest w **5.1 Force March, PDF7**. IG-C25 może poprawnie używać 5.4 jako
   kontrastu przyczyny fatigue; nie zamieniać tego odwołania mechanicznie.
2. W mechanics-evidence skrót do GCACW „7, 9” przy recovery jest mylący:
   spis treści i nagłówek identyfikują recovery jako 8.0, a 9.0 jako
   entrenchments. W tej sesji nie oceniano całej procedury recovery.
3. MMP opisuje link jako Standard Charts & Tables 1.6 **(TotM)**, a nagłówek
   PDF1 to Thunder on the Mississippi. Plik zawiera również jawnie modułowe
   modyfikatory. To nie dowód, że tabela jest niezgodna z innym modułem;
   to dowód, że sama nazwa URL i numer 1.6 nie wystarczają do ustalenia zakresu.
4. Last Days: zachowany PDF ma 32 strony. PDF1 nie dał tekstu i renderuje
   się jako pusta strona; wcześniejszej nazwy wydania nie używamy zamiast
   hasha. Należy jeszcze ustalić wydanie z innego dowodu przed ekstrakcją
   kontraktową.

Rendery końcowe: Poppler pdftoppm, 110 dpi dla siedmiu stron treści oraz
100 dpi dla pustej PDF1 Last Days. Wcześniejsze rendery pypdfium2 zastąpiono
renderami Popplera; oryginalnych PDF nie zmieniano.

Wcześniejsze mechanics-evidence.md i acceptance-cases.md zachowano bez
zmian. Errata nie zmienia 36 statusów proposed_not_run ani starego gold.

## S — SPQR5: jeden wybór używany w kolejnych krokach

Źródło: PDF26, 8.45 i 8.46[1.A–B]; PDF27, 8.46[3–4]. Wybór typu i kąta
ataku jest powiązany z późniejszym sprawdzeniem przewagi. Osobno agreguje
się Size i modyfikuje kolumnę, rzut oraz rozdzielane skutki. Nie liczę tych
elementów jako jednego „bonusu”.

Szkic do digitalizacji:

```yaml
clause_id: S-choice
source: {id: spqr, pdf_page: 26, labels: [8.45, '8.46[1.A]', '8.46[1.B]']}
aspects:
  attacker_choice: {owner: attacker, value: eligible_attacking_unit}
  defender_choice: {owner: defender, value: eligible_defending_unit}
  reuse: {reads: [attacker_choice, defender_choice], purpose: superiority}
bindings:
  - {id: attacker_choice, lifetime: this_shock_resolution, rechoose: forbidden_here}
  - {id: defender_choice, lifetime: this_shock_resolution, rechoose: forbidden_here}
unresolved_dependencies: [eligibility_complete, clash_chart, superiority_chart]
representation: descriptive
review: unreviewed
```

Para do przyszłej próby: dwóch uprawnionych atakujących; raz zachowano
wybór, raz użyto innego uczestnika do przewagi. Drugi zapis narusza więź
źródłową nawet przy identycznych sumach. To nie kontrprzykład dla samego
`binding_id` draftu — ten mechanizm jest trafny. Draft nie określa jednak,
czy binding jest definicją czy wartością instancji. Dwa osobne starcia nie
mogą współdzielić wartości tego samego logicznego binding_id.

8.46[2], PDF26–27: zaokrąglenie zależy od wcześniejszego przejścia z
nieprzyległego pola do sąsiedztwa. Brak historii oznacza unknown, nie
automatyczne zaokrąglenie „jak zwykle”. 6.42 PDF15: jedna jednostka zajmuje
dwa heksy, koszt wynika z większego z kosztów; pamięć wcześniejszego wejścia
połówki zapobiega podwójnemu naliczeniu. Draft opisowo obsługuje te wymagania;
nie sprawdzono wszystkich wyjątków ruchu, klas ani map.

### S2 — mocniejszy kontrprzykład: unieważnienie czynności

Źródło: **5.45–5.46 PDF13**, prawa kolumna, obejrzany obraz.
Po udanym Trump lider w ZOC musi spełnić wymaganie działania; inaczej
czynność traktowana jest jako niezaistniała. Draft ma cancel/replace,
przyczynę i uporządkowane writes, ale nie definiuje, czy cancel cofa skutki
już zapisane przez powodzenie reakcji, liczniki i statusy innych liderów.

```yaml
clause_id: S-nullification
source: {id: spqr, pdf_page: 13, labels: [5.45, 5.46]}
trigger: successful_trump_from_enemy_zoc
required_followup: satisfy_5_45
if_not_satisfied: treat_trumping_action_as_not_occurred
formalization: opaque
gap: {class: unsupported_interpretation, needed: exact_effects_of_nullification}
blocking_for: executable_resolution_of_this_branch
```

Dwie implementacje cancel — zatrzymanie dalszych kroków i unieważnienie
wcześniejszych zmian — mogą dać różne stany. Źródło uzasadnia wymaganie,
ale nie ustalono tu pełnego zestawu cofanych skutków i losowań. Nie
wymyślamy transakcji ani refundu wszystkich kosztów. Dla digitalizacji
powyższy opis i luka są wystarczające; dla wykonawcy to blokada R4.

## T — TLNB7.38: kierunkowa przestrzeń i utrwalony stan

Źródło: PDF9, 8.42–8.43; PDF6, 6.2–6.4. Wyjątek LOS zależy od obserwatora;
zamiana obserwatora z celem może zmienić wynik. Status dowodzenia zachowuje
się do wskazanego segmentu, a udany test pojedynczej jednostki nie musi
usuwać OOC. Nie można wywnioskować statusu tylko z aktualnej odległości.

```yaml
clause_id: T-los-exceptions
source: {id: tlnb, pdf_page: 9, label: '8.43'}
policy: {purpose: sighting, arguments: [observer, target], symmetric: false}
aspects:
  crest_exception: {condition: adjacent_to_observer, effect: does_not_block_observer_los}
  slope_exception: {condition: adjacent_to_observer_on_hilltop, effect: does_not_block_observer_los}
dependencies: [blocking_hexes_8_42, adjacency_exception_8_41, weather_23]
formalization: descriptive
gap: full_path_geometry_not_encoded
```

W tym dokładnym zakresie brak kontrprzykładu przeciw kierunkowemu
spatial_policy draftu: ma odpowiednie pojęcia. Jest kontrprzykład przeciw
prostszej wersji „odległość + symetryczna widoczność” i wspólnemu boolean
„może działać”. Bez pełnej 8.41/23 i mapy nie obliczamy dowolnego LOS.
Starsza karta tabel (PDF2, 2019) wymaga osobnego sprawdzenia kompozycji;
R5 nie jest dowodem konkretnej różnicy wartości z 7.38.

## N — CNS/NAB: odroczona zmiana zasobu i niepełna kompozycja

Źródło: NAB2020-b PDF3 ¶31–33, 36–37; PDF2 ¶1, 6, 8–16.

```yaml
clause_id: N-source-change
source: {id: nab, pdf_page: 3, labels: ['31', '32', '33']}
aspects:
  begin: {state: changing_supply_source, representation: flipped_marker}
  interval: {duration: one_complete_game_turn, constraints: interim_effects_33}
  completion: {window: next_administrative_segment, modality: may, target: new_source}
dependencies: [CNS_standard_rules, legal_LOC, communications_table]
missing: [standard_rules_version_and_content, complete_source_eligibility]
```

Nie zamieniamy „may” w automatyczny skutek schedule. Wybór i możliwość
zakończenia zmiany to różne aspekty. W odczytanych ¶31–33 draft ma potrzebne
pojęcia duration/checkpoint/choice i brak dowodu, że model opisowy ich nie
pomieści. Granica: brak Standard Rules i tabel uniemożliwia przyjęcie pełnej
procedury CNS. ¶1 jawnie określa Exclusive jako dodatek/modyfikację;
nie daje globalnego pierwszeństwa wszystkich tekstów OSG.

¶6/12 rozdzielają siły na displayu i liderów na mapie. ¶8 wiąże zwycięstwo
z torem morale i końcem gry; ¶10–11 dodają zmiany czasowe/zależne od kontroli.
Bez toru i całego scenariusza nie ustalamy progów ani pełnego wyniku.
Minimum powinno zachować wymagane źródła i punkty oceny, nie fikcyjne liczby.

## D — OSG Days: pula, ręka i sprzeczność źródłowa

Źródło Last Days PDF10, 8.1–8.16, obraz obejrzany.

```yaml
clause_id: D-initiative
source: {id: lastdays, pdf_page: 10, labels: ['8.1', '8.13', '8.14']}
resources: [cup_multiset, player_hand_multiset, played_chits]
operations:
  regular_day: {kind: draw, from: cup, then: play}
  forced_march: {kind: player_choice, from: hand, constraints: [not_previous_turn, eligible_units]}
  return: {from: played_chits, to: cup, when: turn_end}
  night: {kind: draw, play: false}
missing: [scenario_initial_counts, complete_night_hand_transfer_review]
formalization: descriptive
```

Kontrprzykład dla użycia `set` wartości: pula zawierająca dwa fizyczne
żetony o tych samych wartościach redukuje się do jednego elementu. To
kontrprzykład modelu danych puli, nie twierdzenie, że przeczytany scenariusz
zawiera dokładnie taką pulę (składu scenariuszy nie sprawdzono). Wykonawca
potrzebuje wielokrotności albo instancji elementów; tekstowy randomizer nie
wyznacza jeszcze rozkładu ani transferów. Nie zakładamy równomierności
tam, gdzie skład lub procedura są unknown.

D2: na tej samej PDF10 **7.31** dopuszcza ruch jednostek OOC, a końcowe
zdanie wprowadzenia **8.0** wymaga In Command do ruchu. To widoczne napięcie
źródłowe, nie uprawnienie recenzenta do naprawy reguły. Zapisać obie tezy,
`conflicting_claims`, zakres „movement eligibility OOC” i blokadę
jednoznacznej odpowiedzi do wyjaśnienia kontekstu/erraty. Mechanizm konfliktu
draftu jest odpowiedni, jeżeli dopuszcza cele w jednym źródle i aspekcie.
Nie stwierdzamy ostatecznej sprzeczności całego systemu po odczycie dwóch stron.

D3: PDF11 **8.23–8.25**: tajny cel rozkazu, ujawnienie na końcu gry,
utrzymanie rozkazu i trasa zależna od celu. Ślad „brak drogi do tajnego celu X”
może ujawnić X nawet po usunięciu samego pola celu. To kontrprzykład
wystarczalności samego viewer_role/filtra faktów, nie wada przechowania
instrukcji. W IG-1 zapisujemy regułę widoczności i blokadę wykonania.

### D4 — Seven Days: klasyfikacja zależna od czynności

Źródło PDF3, 1.4 Mixed Type. Dwa aspekty jednego typu:

```yaml
clause_id: D7-mixed-type
source: {id: sevendays, pdf_page: 3, label: '1.4 Mixed Type'}
aspects:
  stacking: {classification: cavalry}
  combined_arms: {classification: infantry}
binding: classification_is_qualified_by_purpose
formalization: descriptive
review: unreviewed
```

Draft z applicability potrafi to zachować. Kontrprzykład dotyczy próby
redukcji typu jednostki do jednego globalnego enum. Nie przenosić do
Last Days ani TLNB tylko na podstawie podobnego słownika OSG.

## G — GCACW: próba, skutek, naturalny rzut i kontynuacja

Źródło Basic1.6 PDF12, 7.1 Assault kroki1–6 (zamiast błędnego 5.4).

```yaml
clause_id: G-assault
source: {id: gcacw, pdf_page: 12, label: '7.1 Assault'}
bindings:
  selected: {owner: active_player, frozen_at: step_1, scope: this_assault}
aspects:
  attempt_cost: {targets: selected, change: fatigue_plus_1, at: step_2, extended_march: false}
  natural_failure: {condition: raw_roll_equals_6, effect: end_action, at: step_5}
  participation: {from: selected, constraint: assault_number, at: step_5}
  grand_assault_return: {failure: resume_parent_step_7}
missing: [complete_eligibility, command_values, scenario_modifiers, combat_chart_review]
```

Naturalne 6 i zmodyfikowane 6 to nie ta sama przesłanka. Zmiana selected
na participating przy koszcie próby usuwałaby koszt części uczestników.
Draft słusznie rozdziela oba zbiory i oba wyniki. W tym odczytanym zakresie
nie ma kontrprzykładu przeciw tym rozróżnieniom; pozostaje R1: te aspekty
muszą być powiązane z konkretną gałęzią i instancją, nie tylko wspólnym subject.

PDF7 5.1 vs PDF9 5.4 oraz PDF16 7.5: taki sam próg fatigue nie pozwala
wywoływać Extended March po dowolnej przyczynie. PDF6–7 4.0–4.4 wymaga
powtarzanej Action Phase i zamknięcia na właściwym warunku, nie dwóch
dowolnych pass z całej tury. Dane sytuacji muszą zawierać instancję fazy.

RTGII PDF20, HCR6.3: status ustalony w Supply Status Phase trwa między
checkpointami; stan OOS może zmienić się przez foraging. To potwierdza
checkpoint + osobne przejścia, nie jednokrotne globalne `supply=true`.
Nie twierdzimy zgodności całego HCR2018 z Basic1.6 na podstawie tej strony.

Tabela 1.6/TotM PDF1: osobne grupy kolumn, role wyników, przedziały,
kursywa o znaczeniu modułowym, legenda i noty. Numer wiersza/kolumny bez
grupy i powiązanej legendy nie identyfikuje znaczenia komórki. Obejrzano
układ; nie wykonano tabelarycznego gold ani kontroli wszystkich liczb.

## Kontrprzykłady konstrukcyjne kontraktu

X1 (R1), syntetyczny: jedno subject ma condition C1/C2 i effect E1/E2.
Graf bez grupowania dopuszcza C1→E1/C2→E2 oraz C1→E2/C2→E1. Oba zawierają
te same atomy i hashe. Sama akceptacja atomów nie przyjmuje implikacji.
Naprawa: dwie klauzule lub jawne semantic_groups z adresami aspektów.

X2 (R2), syntetyczny: niezmienione twierdzenie A@1 używa definicji D@1
w snapshot S1; w S2 wybrano D@2. Review A@1 jest nadal poprawnym faktem
historycznym, ale ocena znaczenia A w S2 wymaga ponownej decyzji. Zapis
basis_refs wykrywa zmianę bez przepisywania A; incomplete basis daje unknown.

X3 (R3), syntetyczny: S2 wybiera A@2 i zachowuje review R(A@1).
Jeżeli wszystkie refs muszą celować tylko w selected_refs, snapshot jest
albo błędny, albo musiałby wybrać dwie rewizje A. Naprawa: historyczny cel
review rozwiązuje się w niezmiennym repozytorium rewizji, a aktywne użycie
reguły wyłącznie przez selekcję snapshotu. To nie wyjątek od kontroli hashy.

Te trzy kontrprzykłady przeanalizowano ręcznie. Nie napisano walidatora
ani nie nazwano ich zaliczonymi testami. Proponowane regresje IG-1:
zamiana par X1, podmiana D w X2, zachowanie starego review X3, konflikt
jednego źródła D2, zmiana binding przy niezmienionym tekście konsumenta,
brak legendy, dwa losowania z tej samej zmiennej puli i split klauzuli.
Źródłowe expected i ich akceptacja wymagają osobnego etapu.

## Koszt historyczny jako sygnał, nie benchmark

Odnaleziony przez manifest historyczny STATUS podaje w opisie uzgodnienia
granice 218 oryginalnych rekordów reguł/węzłów, 414 zakresów inwentarza,
257 zakresów relacji i 124 lokatory. Bieżący stan archiwum pozostawia
40 nowych ocen sytuacji pending i pełne metryki not_assessable. To liczby
raportowane przez dawny proces, nie ponowne przeliczenie czy nadanie
akceptacji w IG-0. Pokazują, dlaczego „liczba reguł” nie jest mianownikiem
czasu review. Nie sumować kategorii jako niezależnych decyzji człowieka;
część dotyczy tych samych obiektów. Aktywny czas operatora nadal unknown.
