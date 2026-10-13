# Rejestr badań mechanik dla IG

Data: 2026-10-11. Zakres: wybrane źródła pierwotne i wymagania modelu.
To analiza projektowa, nie ekstrakcja całych instrukcji ani przyjęcie reguł.
Każda obserwacja niżej opisuje tylko przeczytany zakres. Szczegółowe treści
wydawców i przyszła ocena pozostają w private/.

## SPQR 5E w repo

Plik użyty w przeglądzie:
`private/archive/poc-2026-10-11/payload/private/poc/spqr-chapter9/source/original-pdf-20261008-01.pdf`.
SHA-256: `e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.
44 strony. Strona tytułowa potwierdza 5th Edition i copyright 2026.
Źródło zgodne z zachowanym source-v1.json w tym samym katalogu.
Dawne ścieżki private/poc/ należy rozwiązywać przez manifest archiwum POC.

Odczytano spis treści i wybrane fragmenty stron fizycznych 6, 10–15,
19–21, 24–27, 37–38, 41–42. Pełne teksty stron 13, 15, 26–27
odczytano ponownie. Obrazy stron 13, 15, 26 przejrzano:
`render-checks/spqr5-p13.png`, `spqr5-p15.png`, `spqr5-p26.png`.
Rendery sporządzono pypdfium2 w skali 1.5; źródła nie zmieniono.

Obserwacje 5E:

- 5.3–5.5, PDF 11–13: aktywacja, Momentum, Trump i inicjatywa elitarna
  wymagają osobnych stanów lidera, okien decyzji i rozliczenia liczników.
  Obejście lidera nie jest jego zakończeniem aktywacji; ponowne użycie
  reguły elitarnej ma odrębne ograniczenia. Reakcja może zastąpić aktywację.
- 6.41–6.45, PDF 15: wieloheksowa jednostka jest jednym obiektem.
  Koszt zależy od terenu, ruchu połów jednostki i wcześniejszych działań;
  potrzebna jest pamięć, które koszty już rozliczono.
- 6.51, PDF 15: reakcja na ruch odczytuje moment podejścia i położenie
  oraz porównuje możliwości ruchowe; dystans reakcji i dostępny koszt
  ruchu są różnymi miarami.
- 8.45–8.46, PDF 26–27: wybrana jednostka używana w ustaleniu kolumny
  jest też używana w sprawdzaniu odpowiedniej przewagi. Odrębne są
  wybory graczy, całkowita wielkość siły i jednostka reprezentująca typ.
  Zaokrąglenie może zależeć od wcześniejszego podejścia do przeciwnika.
- 8.46–8.47, PDF 27: kolejno modyfikuje się kolumnę, rzut i wynik;
  rozdziela straty, sprawdza ucieczkę oraz wykonuje następne czynności.
  Poszczególne korekty nie są jednym uniwersalnym bonusem.
- 10.1 i 11.0, PDF 37–38 i 41: stan jednostki, rozdział strat i
  globalna ocena armii to odrębne zakresy oraz momenty obliczeń.

Wniosek: źródłowe odczyty wymagają semantyki zdarzeń, historii,
wiązań wyboru, uporządkowanych obliczeń i zapytań zależnych od sytuacji.
Nie ustalono kompletu pól dla wszystkich klas jednostek i scenariuszy.

## Źródła internetowe i ograniczony odczyt

Przeczytano strony wydawców i wskazane niżej fragmenty PDF. Nie pobrano
kopii internetowych PDF do repo. Ich SHA-256 jest unknown; przed użyciem
w rzeczywistej ekstrakcji trzeba zachować bajty, wersję i manifest.

| Materiał | Dokładny odczyt i ograniczone ustalenie | Znaczenie dla projektu |
|---|---|---|
| [SPQR 5E product](https://www.gmtgames.com/p-1118-spqr-deluxe-5th-edition.aspx) | Lista materiałów rozdziela wydania i wskazuje setupy Simple GBoH | Osobne systemy i zgodność materiałów |
| [SPQR 4E Oct2022](https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/gbsp/SPQR_4thEdition_Living_Rules_Draft_Oct2022.pdf) | 2.0, 5.4, 6.4, 8.2, 11.0; odczyt pomocniczy, bez mapowania akceptacji do 5E | Kontrola różnic wydania |
| [SPQR 4E errata](https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/gbsp/SPQR_4th_Ed_Errata_and_Clarifications_Oct2022.pdf) | PDF 1: korekty terminologii i zakresów dowodzenia | Errata modyfikuje dokładny cel |
| [SPQR scenarios 2018](https://gmtwebsiteassets.s3.us-west-2.amazonaws.com/gbsp/SPQR-Scenario-Book-2018-5.pdf) | PDF 6–7, 14–15, 21, 27: tabele uprawnień linii, warianty i warunki zwycięstwa | Scenariusz jest źródłem reguł, nie tylko setupem; zgodność z 5E niepotwierdzona |
| [OSG series](https://napoleongames.com/pages/3-different-game-series) | Wydawca rozróżnia TLNB, CNS i Days | OSG jest wydawcą kilku systemów |
| [TLNB 7.38](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/TLNB_SeriesRules-7.38-2.pdf?v=1741466415) | 1.2, 2.1, 5–6, 7.65, 8, 10.4–11, 17, 21–23; PDF 2–3, 5–6, 8–11, 17–18, 21–22. Procedury dowodzenia, LOS, supply, recovery; zachowanie ułamków i niesymetryczna widoczność | Hierarchia, moment odczytu, kierunkowe polityki przestrzeni |
| [TLNB tables](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/COMBAT_TABLES.pdf?v=1603420083) | PDF 1–2: osie, legendy i następne procedury; na stronach widoczne wersje z 2018/2019 | Zgodność z 7.38 wymaga sprawdzenia; wynik nie jest jedną liczbą |
| [TLNB notes](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/NOTES_TO_COMBAT_TABLES.pdf?v=1603420077) | PDF 1: noty 2019; rozdział modyfikacji siły, kolumny, rzutu i skutków | Osobne etapy obliczeń |
| [TLNB changes 7.36](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/Changes_to_TLNB_Series_Rules_7.36-3.pdf?v=1706111836) | PDF 1: wygasanie znacznika, zaokrąglenie, nieodwzajemniony LOS; również zapis house rule | Wersja celu i normatywny status zmiany |
| [TLNB capacity aid](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/TLNB_table-1.pdf?v=1690797176) | Tekst PDF 1: schemat zależny od dowodzenia i testów, opcjonalna gałąź. Obraz niedostępny narzędziem web | Nie rekonstruować drzewa wyłącznie z kolejności wyciągu |
| [CNS description](https://napoleongames.com/pages/campaigns-of-napoleon-series-1x) | Opis mechanik wydawcy: administracja, łączność, ukryte siły i organizacja poza mapą | Wymagania profilu; nie zastępuje instrukcji |
| [NAB Exclusive 2020-b](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/nab_exclusive_rules_update_kit__24k.pdf?v=1601499015) | PDF 1–3; paragrafy 1, 6, 8–16, 29–39. Zmiana reguł standardowych, manifest sił, morale, supply i opóźniona zmiana źródła zaopatrzenia | Zasoby, podporządkowanie i skutki odroczone; standardy CNS nie w całości sprawdzone |
| [Seven Days of 1809](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/7D09-Rules_3.27.pdf?v=1603456254) | PDF 2–4, 20; 1.0–1.4 i 17.0: ukryty ruch, organizacja, specjalne role jednostki | Klasyfikacja zależna od czynności; 3.27 jest nazwą pliku, nie potwierdzoną wersją tekstu |
| [Last Days 2nd Ed](https://cdn.shopify.com/s/files/1/0443/6423/4910/files/ldga_1.12paged.pdf?v=1603458711) | PDF 3, 6, 10–11, 20–23; 2.2, 8.1–8.2, 17–21: żetony inicjatywy, ukryte cele rozkazów, koalicja i gra zespołowa | Losowanie z puli, wybór z ręki, perspektywa i tożsamość strony |
| [GCACW 1.6](https://mmpgamers.com/support/gcacw/GCACW_Series_Rules_1.6.pdf) | PDF 5–7, 12–16, 18–19, 23–24; 2.4, 4–5, 7, 9: cykl, marsz, assault, przyczyna fatigue, odczyt rzutów, ZOC i recovery | Stany niezależne, naturalny rzut, licznik cyklu, przyczyna zdarzenia |
| [GCACW tables 1.6](https://mmpgamers.com/support/gcacw/GCACW_Charts_Tables_1.6.pdf) | Tekst PDF 1–2: przedziały osi, osobne strony odczytu, symbole i dekoracje, reguły odwrotu. Screenshot PDF 1 niedostępny | Wielocelowy wynik i jawne legendy; obrazu przed formalną transkrypcją nadal brakuje |
| [RTG II](https://mmpgamers.com/support/gcacw/RTG2_Rules.pdf) | PDF 17, 20–21, 68, 104: Basic/Advanced, różne części tomu, checkpoint supply i dodatkowe fazy | Kwalifikowany numer reguły, profil scenariusza i pamięć sprawdzonego stanu |

To rejestr odczytanego zakresu, nie deklaracja pełnego przeglądu stron
scenariuszy ani dokładnej transkrypcji tabel. Nie nadano ludzkiej akceptacji
ich znaczeniu. Metadane modeli/czas aktywny/tokeny/cena: unknown.

## Dostępność narzędzi

Link do 5E z oficjalnej strony nie zwrócił odczytywalnego PDF w web.
Nie zgadujemy jego dokładnego URL ani zgodności bajtów z lokalną kopią.
Web screenshot TLNB PDF 3 został wywołany, ale obraz nie był dostępny
w wyjściu tej sesji. Dla tabel GCACW i capacity aid zgłoszono błąd
screenshotu. Wnioski o ich geometrii ograniczono do struktury wymaganej
przez odczytaną treść; wartości komórek nie zostały transkrybowane.

## Przekazanie

Wspólny model i reguły nowych pól: docs/IG-DATA-MODEL.md oraz
docs/IG-MECHANICS-PROFILES.md. Przypadki do przyszłego sprawdzenia:
acceptance-cases.md. Każdy wymaga rzeczywistych wejść, dowodów,
reprezentacji i review. Żaden nie został wykonany jako test mechanik.
