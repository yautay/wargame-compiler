# M-POC1A: przegląd inwentarza draft-v1

Data: 2026-10-07. Wykonawca odczytu: Codex, ręczna sesja inwentarza.
Stan: **waiting_review**. Recenzent właściciel: brak; data przeglądu: brak;
akceptacja: nie została udzielona. Ten dokument nie jest ekstrakcją M-POC2B,
oczekiwaniami, sytuacjami ani zamrożonym eval-v1.

## Źródło i metoda

[Source-v1](../../source/source-v1.json) zapisuje pełny hash
`e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e`.
Jest zgodny z historycznym scope-candidates-v2; brak rozbieżności bajtów.
Źródło ma 44 strony, 3 965 827 bajtów. Okładka wizualnie potwierdza 5th Edition.
Numeracja PDF jest od 1; widoczne drukowane etykiety 31–37 są zgodne z nią.

Wszystkie siedem pełnych renderów obejrzano w tej sesji, w kolejności kolumn.
Pomocniczy tekst pdfplumber służy do transkrypcji i lokalizacji. Nie ustala granic,
struktury grafiki ani kolejności rozdzielonej tabeli. Dowody JSON zawierają stronę,
kolumnę, hash renderu, obwiednię w punktach PDF, zakres wierszy pomocniczych oraz
transkrypcję. Początek współrzędnych: lewy górny narożnik, x w prawo, y w dół;
strona 612 × 792 pt, render 150 dpi. Obwiednie grafik są przybliżone.

98 grup klauzul to robocze akapity, punkty list, kroki i skupienia zdań.
Obejmują także wprowadzenia do list oraz odrębny akapit stosowalności 9.7.
To nie 98 niezależnych norm ani sprawdzony mianownik kompletności semantycznej.
Podział długich akapitów na atomowe klauzule pozostaje do przeglądu (U-01).
Żadna grupa nie zastępuje całej treści oznaczenia nadrzędnego.

## Liczniki obserwacji Codex

| Typ | Liczba |
|---|---:|
| Nagłówek rozdziału | 1 |
| Nagłówki podrozdziałów | 9 |
| Oznaczenia reguł | 41 |
| Grupy klauzul, razem ze wprowadzeniami | 98 |
| Noty | 14 |
| Tabele / wiersze tabeli | 1 / 3 |
| Diagramy | 2 |
| Podpisy, w tym podpis-przykład diagramu | 3 |
| Pozostałe przykłady | 6 |
| Osobne ilustracje żetonów jednostek / znaczników | 3 / 2 |
| Kontynuacje fizyczne | 7 |

Łącznie 190 rekordów różnych poziomów. Nie wolno sumować tych poziomów jako
liczby reguł. [Inventory](inventory.json) ma osobno parent_id, typ i status każdego
rekordu. Wszystkie 12 obszarów kolumn rozdziału mają rozliczenie; każdy wiersz
pomocniczego tekstu core przypisano do elementu. Nagłówki bieżące i stopki są
paratekstem strony. Włączenie wszystkich liter na ilustracjach żetonów nie było
celem tej karty; rendery zachowują je do późniejszego przeglądu.

## Pierwszy krok właściciela: granice (U-08)

1. Otwórz [PDF 31](../../source/review-evidence/pdf-31.png). Core zaczyna się
   od **9.0 w prawej kolumnie** (okolice y=309,45 pt). Cała lewa kolumna oraz
   prawa przed 9.0 są kontekstem rozdziału 8, wyłączonym z liczników core.
2. Otwórz [PDF 37](../../source/review-evidence/pdf-37.png). Core to **lewa
   kolumna przed 10.0** (cięcie y=392,64 pt). Obejmuje dokończenie akapitu 9.96
   i trzy punkty listy. Lewa od 10.0 oraz cała prawa są kontekstem rozdziału 10.
3. Potwierdź lub wskaż korektę granic i kontekstu. Historyczne cięcia są w białym
   odstępie; obwiednia glifów pdfplumber zaczyna się o 1–2 pt niżej. To różnica
   metryki obwiedni, bez zmiany treści zakresu ani hasha.
4. Na [PDF 36](../../source/review-evidence/pdf-36.png) sprawdź przejście 9.91
   → 9.93. **9.92 nie występuje w obejrzanym źródle**; nie dopisano go.

## Rozliczenie obszarów

| Obszar | Obserwowany zakres | Szczególne punkty |
|---|---|---|
| A-31-R | 9.0, 9.1, nota, 9.11 do kroku 2 | granica początku; G-01; K-01 |
| A-32-L | kroki 3–4, 9.12–9.14, początek tabeli | N-02/N-03; T-01 |
| A-32-R | ostatni wiersz tabeli i dalszy 9.14 | K-02; D-01/X-01; K-03 |
| A-33-L | koniec 9.14, 9.15–9.19 i noty | N-04/N-05/N-06 |
| A-33-R | 9.2, 9.21–9.24 | G-02; N-07; K-04 |
| A-34-L | koniec 9.24, 9.3–9.4 | X-03/X-04/X-05; N-08 |
| A-34-R | 9.5, 9.51–9.53 | N-09; lista 5 i 7 punktów; X-06 |
| A-35-L | 9.6, 9.61–9.66 | N-10; D-02 i dwa podpisy; K-05 |
| A-35-R | koniec 9.66, 9.67–9.72 | X-07; nienumerowany akapit 9.7 |
| A-36-L | 9.8, 9.81–9.87; 9.9 i początek 9.91 | N-11/N-12; G-03/G-04/G-05; K-06 |
| A-36-R | koniec 9.91, 9.93–9.96 | brak 9.92; N-13/N-14; K-07 |
| A-37-L | dokończenie 9.96 i trzy punkty | granica przed 10.0 |

Pełne rendery środkowe: [32](../../source/review-evidence/pdf-32.png),
[33](../../source/review-evidence/pdf-33.png),
[34](../../source/review-evidence/pdf-34.png),
[35](../../source/review-evidence/pdf-35.png),
[36](../../source/review-evidence/pdf-36.png).

## Przegląd struktury i niepewności

| ID | Dokładny materiał do sprawdzenia | Wymagana decyzja / kontekst |
|---|---|---|
| U-01 | C-*; szczególnie długie akapity 9.15, 9.16, 9.41, 9.51, 9.61–9.68, 9.82, 9.85–9.86, 9.94–9.96 | Potwierdzić grupowanie lub rozdzielić klauzule; oddzielić wprowadzenia do list od norm. Akapit C-9.7-01 nie może zniknąć jako sam nagłówek. |
| U-02 | PDF 36 prawa, N-14 oraz R-9.96; PDF 37 lewa | Nota DESIGN zawiera polecenie dotyczące Combat Tables. Ustalić zakres tej treści; rodzaj noty nie przesądza braku treści operacyjnej. Dokładne tabele/cele wymagają kontekstu. |
| U-03 | N-03 na PDF 32; N-07 na PDF 33; N-09 na PDF 34 | Noty zawierają także wypowiedzi o stosowalności, klasyfikacji lub uprawnieniach scenariuszowych. Wyznaczyć granicę opisu i przyszłych oczekiwań. |
| U-04 | PDF 32: T-01/TR-01–03 i D-01/X-01; K-02 | Potwierdzić jedną tabelę: nagłówki i wiersze 0, 1–6 po lewej; 7–9 po prawej. Sprawdzić odróżnienie pierwszego i kolejnych rzutów oraz Leader Elephant. Diagram ma etykiety 1–6; podpis nakazuje użyć kompasu konkretnej mapy. Nie zamrażać przykładu jako uniwersalnej orientacji. |
| U-05 | PDF 35 lewa: D-02, CAP-01/CAP-02; 9.66 kończy się po prawej | Potwierdzić przypisanie paneli Original Deployment / After Manipular Line Extension do reguły 9.66 mimo grafiki przed jej nagłówkiem; sprawdzić K-05. |
| U-06 | dependency-candidates.json, zwłaszcza cele zewnętrzne i cele unknown | Potwierdzić identyfikatory, źródła, kierunek i rodzaj dopiero z potrzebnym kontekstem. Nie uznawać każdej wzmianki za zależność wykonawczą. |
| U-07 | N-09/X-06, C-9.7-01, 9.94–9.96 i odniesienia do mapy | Uprawnienia i setup scenariusza, tożsamość dowódcy, progi armii oraz kompas mapy są poza sprawdzonym inwentarzem rozdziału. W tej karcie nie wybrano scenariusza ani nie domknięto tych celów. |
| U-08 | granice PDF 31/37, numeracja PDF 36 | Potwierdzić granice i wyłączenie kontekstu; nie tworzyć 9.92. |
| U-09 | obwiednie D/G, pomocnicza transkrypcja końca 9.96 | Sprawdzić małe napisy, typografię markerów i dzielenie wyrazów na renderach. Tekst helper nie jest wierną transkrypcją całej grafiki. |

Kontynuacje do odhaczenia: K-01 (9.11 PDF31→32), K-02 (tabela PDF32 L→R),
K-03 (9.14 PDF32→33), K-04 (punkt 9.24 PDF33→34), K-05 (9.66 PDF35 L→R),
K-06 (9.91 PDF36 L→R), K-07 (9.96 PDF36→37). Kontynuacja ma dwa osobne dowody
fragmentów; gdy parent ID jest ten sam, nie tworzy to semantycznej pętli grafu.

## Kandydaci zależności

[Dependency candidates](dependency-candidates.json) zawiera 96 rekordów:
29 liczbowych (25 zewnętrznych i 4 wewnętrzne), 14 nazwanych,
46 bez numerów (w tym hipotezę powiązania Mounted Javelinists z MRRC),
7 kontynuacji. To liczniki kandydatur z jednostek źródłowych, **nie liczba
zweryfikowanych unikalnych krawędzi**. Kategorie mogą wskazywać pokrewne cele.

19 różnych liczbowych tokenów zewnętrznych jest zgodnych z historyczną listą.
Żaden z nich nie został automatycznie gold. Wewnętrzne odwołania wskazują
zaobserwowane etykiety 9.14, 9.11, 9.41 i 9.85; rozpoznanie etykiety nie jest
przeglądem znaczenia relacji. 10.13 jest widoczne w kontekście PDF37 prawej,
ale pozostaje poza core i poza weryfikacją znaczenia celu. Pozostałych rozdziałów
ani zewnętrznych tabel nie otwierano na potrzeby domknięcia grafu.

Kandydatury nazwane obejmują MRRC i wiersze, Clash of Spears and Swords,
Shock Superiority, Shock Combat Results/CRT, Stacking Charts, Movement Cost
Chart, zbiorcze Combat Tables, kompas mapy i lokalną tabelę/diagram. Nazwy,
aliasy, źródła tabel i hipotezy celów są osobnymi polami; to pozostaje do review.
Bez numerów zebrano między innymi użycia lub modyfikacje procedur ruchu,
dowodzenia, stosów, TQ, Shock, Rout, Recovery, Momentum, H&D oraz zależności
od scenariusza, LOS/ZOC i definicji jednostek. Jawne nazwanie procedury bez
numeru jest odróżnione od hipotezy potrzeby ogólnej reguły lub definicji.

## Stan przeglądu i wznowienie

Sprawdzone przez Codex: bajty i hash źródła, wydanie, granice wizualne,
oznaczenia, fizyczne jednostki tekstu, listy, noty, grafiki i kontynuacje.
Niepewne: atomowy podział klauzul, zakres operacyjny części not, aliasy/cel
oraz rodzaj i znaczenie zależności. Wymagające kontekstu: cele zewnętrzne,
setup scenariuszy, mapy i tabele nieobecne w core.

**Pierwszy nieprzejrzany obszar właściciela to A-31-R / U-08.** Następnie
A-37-L / U-08, tabela U-04, grafika U-05, noty U-02/U-03 oraz U-01/U-06/U-07.
Właściciel zapisuje faktyczny zakres, decyzje, datę i pozostałe niepewności.
Korektę draft można zapisać oddzielnie z mapą zmian; historycznych wejść i ich
bajtów nie zmieniać. Dopiero po tym przeglądzie przekazać inwentarz do
M-POC1B. M-POC1A pozostaje partial / waiting_review; M-POC1 nadal next.
Nie rozpoczęto M-POC1B/C, nie utworzono sytuacji i nie zamrożono eval-v1.
