# Własny przykład desktopowy: River watch (M-DESK1)

Cały tekst, grafika i PDF w tym katalogu są własnym materiałem testowym, udostępnionym jako CC0 1.0.
To mały przykład kontraktu, nie nowa gra benchmarkowa, eksporter ani wynik pracy modelu.

[PDF](source.pdf) ma dokładnie dwie strony PDF z drukowanymi etykietami 7 i 8.
Zachowane rendery: [strona 1](p001.png), [strona 2](p002.png); sprawdzono je wizualnie w sesji M-DESK1.

Oczekiwany odczyt:

- Strona 1: najpierw lewa kolumna (nagłówek, lista, ramka i reguła 3), potem prawa (reguła 2).
- `b.crossing-start` ze strony 1 i `b.crossing-end` ze strony 2 tworzą kontynuację:
  „A scout may cross the river only when the bridge is clear.”
- Niebieska ramka ogranicza regułę 3 do warunków powodzi; nie obejmuje reguły 2 w prawej kolumnie.
  Hierarchia `parent` i relacja `scope` zapisują dwa różne fakty.
- Strona 2: zakończenie reguły 2, tabela, potem prawa kolumna z regułą 5 i napisem
  `NIGHT: LIMIT 1`. Napis jest rastrem, nie tekstem PDF. Ma osobną transkrypcję i hash obrazu.
- Paginacja jest świadomym wyłączeniem. Tekst tabeli zachowuje cztery komórki, w tym nagłówki.

Pełne fixture'y: [pakiet](../../contracts/fixtures/valid/desktop.package.yaml),
[odpowiedź](../../contracts/fixtures/valid/desktop.response.yaml),
[dokument](../../contracts/fixtures/valid/desktop.document.yaml),
[rewizja](../../contracts/fixtures/valid/desktop.revision.yaml).
Rewizja ma `validation: valid`, ale wszystkie elementy mają `pending`, a kompletność to `partial`.
Wynik oczekiwany jest autorskim przykładem; nie zastępuje pilota w aplikacjach ani zatwierdzenia użytkownika.

Regeneracja (biblioteki wyłącznie z `requirements.txt`, bez inferencji):

```powershell
.\.venv\Scripts\python.exe bench/desktop-two-page/generate.py
```

Generator zapisuje tylko własne fixture'y i materiały tego przykładu. Po zmianie wersji renderera mogą zmienić
się bajty PNG i hash pakietu: wtedy zregenerować całość, uruchomić testy i porównać obie strony.
Kopia schematu w katalogu przykładu jest celowa: jej rzeczywiste bajty są objęte manifestem.
Nie uruchamiać generatora na prywatnych instrukcjach; docelowy eksporter należy do M-DESK2.

M-DESK2 dostarcza osobną komendę `python -m wgc desktop export`, która nie zna układu tego przykładu
i nie używa generatora ani oczekiwanej odpowiedzi. [Instrukcja wymiany](../../docs/DESKTOP-EXCHANGE.md)
opisuje przygotowany pakiet PDF 1 jako zakresu docelowego oraz PDF 2 jako kontekstu. Test eksportu obu stron
odtwarza powyższy gold po powiązaniu z nowym pakietem; testy offline nie są ręczną próbą w aplikacji.
