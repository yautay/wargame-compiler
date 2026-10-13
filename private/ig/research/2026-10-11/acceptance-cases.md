# Proponowane przypadki sprawdzenia modelu IG

Data: 2026-10-11. Status wszystkich pozycji: **proposed_not_run**.
To katalog wymagań przyszłego eksperymentu, nie nowy gold ani rozszerzenie
zamrożonego eval-v1 POC. Podstawa odczytu: mechanics-evidence.md.

Każdy przypadek potrzebuje własnego ID wejść, wersji źródła, obrazu,
przypiętego snapshotu, reprezentacji reguł i jawnej decyzji człowieka.
Sprawdzamy reprezentację i wnioski, a późniejszy wykonawca dostaje osobne
testy. Nierozstrzygnięcia zachowujemy jako oczekiwane blokady.

| ID | Profil i podstawa | Para sytuacji lub granica do sprawdzenia | Wymaganie modelu |
|---|---|---|---|
| IG-C01 | SPQR5, 5.4 | Lider ominięty / lider zakończony | Oddzielne stany i uprawnienia |
| IG-C02 | SPQR5, 5.42 | Udana / nieudana reakcja Trump | Zastąpienie aktywacji i dalsza kontynuacja |
| IG-C03 | SPQR5, 5.43 | Dwie próby w tej samej / innej aktywacji | Tożsamość instancji licznika |
| IG-C04 | SPQR5, 5.5 | Aktywacja elitarna / normalna | Wariant wejścia procedury |
| IG-C05 | SPQR5, 6.41 | Pierwszy / następny ruch | Historia niezależna od bieżącej pozycji |
| IG-C06 | SPQR5, 6.42 | Jeden żeton w dwóch heksach | Jeden obiekt, rozliczenie bez duplikacji |
| IG-C07 | SPQR5, 6.43–6.45 | Pivot / obrót w tej samej pozycji | Footprint, teren i zmiana orientacji |
| IG-C08 | SPQR5, 8.45–8.46 | Dwóch kandydatów na jednostkę reprezentującą | Ten sam wybór utrzymany między krokami |
| IG-C09 | SPQR5, 8.46 | Ta sama proporcja, inne wcześniejsze podejście | Warunkowa polityka zaokrąglenia |
| IG-C10 | SPQR5, 8.46–8.47 | Kilka skutków jednego wyniku | Kolejność, wybór celów i wywołanie procedury |
| IG-C11 | SPQR scenarios2018 | Dwa scenariusze, ten sam rodzaj oddziału | Scenariusz jako źródło zakresu; nie przenosić do 5E |
| IG-C12 | TLNB7.38, 5–6 | To samo miejsce, inna formacja | Dowodzenie i podporządkowanie |
| IG-C13 | TLNB7.38, 8.43 | Zamiana obserwatora i celu | Kierunkowy LOS |
| IG-C14 | TLNB7.38, 17 | Obecna ścieżka / stan w checkpoint | Trwałość ustalonego statusu |
| IG-C15 | TLNB7.38, 7.65 | Naprawa i dwa rodzaje użycia | Różne momenty dostępności |
| IG-C16 | TLNB tables, PDF2 | Wynik z wywołaniem kolejnej tabeli | Jawna kontynuacja rozstrzygnięcia |
| IG-C17 | TLNB notes, PDF1 | Korekta siły / kolumny / rzutu | Osobne etapy i cele |
| IG-C18 | TLNB changes7.36 | Stare uzupełnienie w nowym profilu | Zgodność wersji bez podwójnej poprawki |
| IG-C19 | NAB2020-b, ¶29–39 | Zmiana źródła supply w toku / zakończona | Odroczony skutek i stan pośredni |
| IG-C20 | NAB2020-b, ¶6,13 | Siła na displayu / lider na mapie | Obiekt poza mapą i hierarchia |
| IG-C21 | LastDays2E, 8.1 | Losowanie / wybór z ręki | Pula i właściciel decyzji |
| IG-C22 | LastDays2E, 8.23 | Wiedza właściciela / przeciwnika | Tajny cel i warunek ujawnienia |
| IG-C23 | SevenDays, 1.4 | Klasyfikacja tej samej jednostki dla innych czynności | Typ zależny od celu reguły |
| IG-C24 | GCACW1.6, 4 | Powrót po działaniu / zamknięcie cyklu | Pętla i warunek końca |
| IG-C25 | GCACW1.6, 5.1,5.4,7.5 | Ta sama fatigue, różna przyczyna | Wyzwalacz uwzględniający zdarzenie |
| IG-C26 | GCACW1.6, 5.4 | Ten sam wynik zmodyfikowany, różny naturalny | Zachowanie wyniku oryginalnego |
| IG-C27 | GCACW1.6, 5.4 | Uczestnik wybrany / rzeczywiście walczący | Osobne zbiory i koszt próby |
| IG-C28 | GCACW1.6, 2.4 | ZOC w różnych rodzajach czynności | Polityka zależna od kontekstu |
| IG-C29 | GCACW tables, PDF1 | Dwa cele jednego odczytu | Osobne role wyników |
| IG-C30 | GCACW tables, PDF1 | Granica przedziału i znak/dekoracja | Przedziały, legenda, adnotacje |
| IG-C31 | GCACW tables, PDF2 | Kilka legalnych tras odwrotu | Priorytet ścieżki i wybór gracza |
| IG-C32 | RTGII, PDF17,68,104 | Ten sam numer w innych częściach tomu | Kwalifikowanie celu odwołania |
| IG-C33 | RTGII, PDF20 | Supply między checkpointami | Stan utrwalony w określonym momencie |
| IG-C34 | Wspólny rdzeń | Poprawka zaakceptowanego twierdzenia | Nowa rewizja bez odziedziczonej akceptacji |
| IG-C35 | Wspólny rdzeń | Reguła lokalnie poprawna, brak tabeli | Jawna blokada wyniku bez zgadywania |
| IG-C36 | Wspólny rdzeń | Zmiana wiązania, niezmieniony tekst kolejnego kroku | Analiza wpływu i regresji |

Pierwsza próba powinna wybrać ograniczony zestaw z każdej rodziny.
Nie trzeba od razu wykonywać wszystkich 36 pozycji. Nie ma jeszcze
zweryfikowanych expected, kosztu operatora ani pokrycia mechanik serii.
