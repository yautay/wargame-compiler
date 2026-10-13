# M-POC5A.4c3 — ostatnia przypisana partia lokatorów

Wykonałem przegląd wszystkich 22 ID / 38 wystąpień: 16 w first-001
i 22 w context-01. Porównałem krótki cytat, obraz, jego oryginalną ramkę,
pełną obwiednię znaków i widoczny raster. Nie poprawiłem cytatu, ramki
lub odpowiedzi. Twoje zatwierdzenie poprzedniej .4c2 zapisałem jako
owner-decision-09: 42 ograniczone oceny; razem 86 wcześniejszych
wystąpień ma decyzje właściciela. Nowe 38 tutaj to propozycje.

## 1. Źródło i geometria są poprawne, ale pełne obwiednie nie mieszczą się

Każdy cytat odnaleziono w dostarczonym źródle i niezależnym helperze.
Hashe obrazów, wymiary i układ współrzędnych zgadzają się; ramki są
w granicach właściwych obrazów. W 16 wspólnych ID cytat i obraz są takie
same między odpowiedziami, ale zachowano osobne ślady do bajtów.
Sześć dodatkowych ID występuje tylko po kontekście; nie przypisano
oceny lokatora nieistniejącym rekordom pierwszej odpowiedzi.

W tych sześciu przypadkach ramka jest liczona względem dostarczonego
obrazu 433×395, obejmującego tylko Step 4. Użyto jego znanego przesunięcia
na wcześniejszym renderze do porównania z PDF. Nie oglądano ani nie
szukano tekstu poza dostarczonym wycinkiem strony 27.

Każde z 38 wystąpień ma mierzalne przekroczenie pełnej obwiedni glifu.
Przykładowo dolna obwiednia nagłówka ARTILLERY wychodzi o 2.811 punktu
PDF, choć litery widać w całości. Obwiednia fontu obejmuje również
przestrzeń bez tuszu, dlatego to osobna miara od widocznego ucięcia.
W tej partii nie ma przypadku z samą różnicą rzędu 10⁻¹⁴ punktu;
wcześniejsze E962 pozostają nieocenialne z powodu precyzji.

**Rekomendacja 1:** przyjąć poprawne źródłowe wskazanie krótkich cytatów
i geometrię 38 wystąpień, zachowując wszystkie 38 naruszeń pełnych
obwiedni. Nie nadaje to akceptacji całej reguły, całego dużego cropu,
diagramu lub wartości żetonu. Wady ramki nie są automatycznie błędem znaczenia.

## 2. 36 krótkich rastrów jest czytelnych bez zaobserwowanej utraty tuszu

Na stronach 36–37 widać m.in. negację zwykłego Reaction Fire Scorpio,
wartość –1 dla pierwszej próby Momentum, brak Size/TQ dla CH i próg
rout równy lub większy od TQ. Sześć cytatów Step 4 zachowuje stronę
atakującego/obrońcy, mnożniki 2x/3x, połowę z zaokrągleniem w dół,
limit 1 Hit i wyjątek Routed. Długi cytat LC zawiera również
„cumulative with bullet #1”. To potwierdza odczyt cytatu, bez nowego
rozstrzygnięcia wcześniejszego pytania o kolejność AS/LC.

Wszystkie te krótkie teksty są widoczne mimo przekroczeń obwiedni.
Nie rozszerzam tej oceny na pozostałą zawartość szerokich ramek.
Przykładowo crop E981 pokazuje też żeton Scorpio; jego wartości
nie otrzymują akceptacji przez ocenę krótkiego zdania.

**Rekomendacja 2:** przyjąć czytelność 36 krótkich cytatów bez
zaobserwowanej utraty tuszu. Są to wszystkie przypisane wystąpienia
poza dwoma E1011. Ramki pozostają niezmienione, bez ścisłego „pass”.

## 3. Dwa E1011 są czytelne, ale dolne części liter zostały przycięte

Instrukcja mówi, że Routed units przy sprawdzaniu TQ używają wartości
1 zamiast printed TQ. Obie odpowiedzi mają zgodny krótki cytat.
Jednak oryginalna ramka kończy się tak blisko dolnej linii, że ucina
dolną część „p” w printed i ogonek „Q”. Porównałem dokładny wycinek
z tym samym źródłem oraz powiększeniami obu granic.

Tekst nadal daje się odczytać; nie wykazałem tu błędnej interpretacji
reguły. Diagnostyka wspiera widoczne przycięcie: poniżej ramki jest
6 ciemnych pikseli „p” i 1 „Q”; dolna obwiednia wystaje o 1.6836 punktu.
To wada dowodu rastrowego w obu wynikach. Oryginalny tekst i bbox zachowano.

**Rekomendacja 3:** przyjąć te dwa ograniczone wyniki jako czytelne,
ale niepełne dowody; zachować przycięcie bez naprawy lub automatycznego
błędu semantycznego. Nie przyjmować tych cropów jako zawierających całe litery.

## Ile jeszcze do końca etapu 5

Po tej partii wszystkie 124 przypisane wystąpienia lokatorów mają
rzeczywiste porównanie. Nowych decyzji właściciela jest 0, pending 38;
poprzednich 86 ma decyzje w dokładnych zakresach. Powyższe trzy
rekomendacje dotyczą różnych cech tych samych 38 wystąpień, nie 76 punktów.
Faktyczne otwarcie lub odczyt plików przez właściciela pozostaje unknown.

Pozostają dwa bloki etapu 5:

1. **M-POC5A.4d:** rozliczenie wszystkich 207 pozycji, szerszych
   nieprzejrzanych komponentów, 66/8 oczekiwań i dawnych nierozstrzygnięć.
   Zakres trzeba oszacować i ewentualnie podzielić przed wykonaniem.
2. **M-POC5B:** 20 zamrożonych sytuacji, osobno dla obu odpowiedzi —
   40 ocen. Brak źródła może dać uzasadnioną blokadę, bez zgadywania wyniku.

To co najmniej dwa kolejne bloki pracy, nie obietnica dokładnie dwóch
sesji. Wiarygodny szacunek godzin wymaga rozliczenia pozostałego zakresu .4d
i wcześniejszego oszacowania partii sytuacji. Tych prac tutaj nie wykonano.

[Wszystkie porównania](comparisons.md) · [Pełne ślady JSON](comparisons.json).
257 komponentowych decyzji relacji, 264 pary rubryka/EXP i osiem dawnych
oczekiwań zachowane. Inne znaczenia, brakujące źródła i starsze
nierozstrzygnięcia pozostają otwarte. Pełne TP/FP/FN/precision/recall
nieocenialne; gold i limity bez zmiany. Nadrzędne karty nadal partial.
