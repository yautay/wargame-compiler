from pathlib import Path
ROOT = Path(r'C:\dev\wargame-compiler')
TASKS = ROOT / 'docs/work/tasks'
TASKS.mkdir(parents=True, exist_ok=True)
# Static one-off documentation authoring, not an active task management system.
cards = [
dict(id='M-POC0', milestone='M-POC0', title='Archiwum, wnioski i plan',
 goal='Zachować poprzedni projekt i rozpocząć odseparowaną aktywną strukturę.',
 question='Czy wszystkie istotne bajty można odtworzyć bez inferencji, a oba projekty uruchamiać niezależnie?',
 depends='Instrukcja właściciela z 2026-10-07; nie wymaga ukończenia M-DESK2.', role='Codex',
 reads=['archive/legacy-2026-10-07/project/CLAUDE.md', 'archive/legacy-2026-10-07/project/docs/SESSION-PLAYBOOK.md', 'archive/legacy-2026-10-07/project/docs/STATUS.md', 'archive/legacy-2026-10-07/project/docs/HANDOFF.md', 'archive/legacy-2026-10-07/project/docs/handoff/2026-10-07-M-DESK2.md', 'archive/legacy-2026-10-07/project/docs/ROADMAP.md', 'archive/legacy-2026-10-07/project/docs/DESKTOP-IMPLEMENTATION-PLAN.md', 'archive/legacy-2026-10-07/project/docs/DESKTOP-EXCHANGE.md', 'archive/legacy-2026-10-07/project/docs/adr/ADR-0037-ekstrakcja-desktop-bez-api.md', 'archive/legacy-2026-10-07/project/docs/adr/ADR-0038-minimalne-kontrakty-desktop.md', 'archive/legacy-2026-10-07/project/docs/DATA-CONTRACTS.md (sekcja 11)', 'private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/poc-plan-proposal.txt', 'private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json', 'private/source-artifacts/SRC-spqr.rules/responses/spqr-p032-codex-review-20261007-1.json'],
 inputs='Zastane pliki publiczne, private/source-artifacts i istotne .glu. Zestaw oceny jeszcze nie istnieje. Przed migracją czytano ścieżki bez prefiksu archive/legacy-2026-10-07/project/.',
 actions=['Zinwentaryzuj Git i pliki; snapshot do nowego katalogu, manifest SHA-256 i wyłączenia.', 'Zweryfikuj wszystkie kopie i odtworzenie przed przenoszeniem; przenieś strukturę bez edycji bajtów.', 'Zapisz mapę, instrukcje, ADR, wnioski, plan, karty i bootstrap. Sprawdź prywatność oraz testy legacy i aktywne.'],
 outputs=['private/archive/2026-10-07-pre-poc/manifest.json, payload/, restore-check/', 'archive/legacy-2026-10-07/README.md, movement-map.json, project/', 'private/archive/legacy-2026-10-07-state/', 'README.md, CLAUDE.md, docs/POC-PLAN.md, docs/LESSONS-LEARNED.md, docs/adr/ADR-0039-archiwum-i-poc-przed-architektura.md', 'docs/ROADMAP.md, docs/STATUS.md, docs/HANDOFF.md, docs/SESSION-PLAYBOOK.md, docs/work/tasks/, tests/'],
 checks='Pełna zgodność hashy i odtworzenia; importy legacy z własnego katalogu; osobne testy; poprawne linki i jeden next; git diff --check. Dopiero potem done i M-POC1 jako next.',
 excluded='M-POC1–M-POC7, ekstrakcja, pipeline, API/GUI, commit/push, zmiana historii.',
 human='Polecenie właściciela upoważnia do reorganizacji. Nie nadaje akceptacji reguł SPQR.',
 resume='Czytaj verification.json i movement-map.json przed wznowieniem; nie nadpisuj snapshotu ani już przeniesionych katalogów.',
 handoff='M-POC1A: sprawdzenie źródła i granic, następnie ręczny inwentarz.'),
dict(id='M-POC1A',milestone='M-POC1',title='Źródło i ręczny inwentarz',
 goal='Ustalić rzeczywistą zawartość rozdziału i granice oceny.',
 question='Jakie oznaczenia, klauzule, tabele, diagramy, noty i kontynuacje rzeczywiście występują?',
 depends='M-POC0 zakończony.',role='Codex; przegląd wspólny',
 reads=['docs/LESSONS-LEARNED.md','docs/handoff/2026-10-07-M-POC0.md','private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/poc-plan-proposal.txt','private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json',r'C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf (PDF 31–37)'],
 inputs='Oryginalny PDF i kandydaci zakresu. Ocena: draft, bez zamrożonej wersji.',
 actions=['Sprawdź istnienie, pełny SHA-256 i wydanie PDF; porównaj z kandydatem. Rozbieżność wymaga wyjaśnienia przed odczytem.', 'Sprawdź wizualnie początek prawej kolumny PDF 31 od 9.0 i koniec lewej PDF 37 przed 10.0; oddziel kontekst.', 'Spisz oznaczenia i klauzule z dowodami, tabele/diagramy/noty i kontynuacje. Nie zakładaj ciągłości numeracji. Zbierz odwołania liczbowe, nazwane i niejawne jako kandydatów.'],
 outputs=['P/source/source-v1.json','P/evaluation/draft/inventory.json','P/evaluation/draft/dependency-candidates.json','P/evaluation/draft/inventory-review.md'],
 checks='Każdy obszar rozdziału rozliczony ręcznie; element ma typ, lokalne ID, źródło/stronę i status. 19 kandydatów nie staje się automatycznie gold.',
 excluded='Ekstrakcja modelowa, oczekiwane wyniki sytuacji, domykanie całej instrukcji, kod pipeline’u.',
 human='Właściciel sprawdza granice i niepewne elementy inwentarza, bez uznawania propozycji modelu za akceptację.',
 resume='Odczytaj draft/inventory-review.md; wznowienie od pierwszego oznaczonego nieprzejrzanego obszaru, bez zmiany sprawdzonego źródła.',
 handoff='M-POC1B otrzymuje inwentarz i listę niepewności.'),
dict(id='M-POC1B',milestone='M-POC1',title='Oczekiwania i 15–20 sytuacji',
 goal='Przygotować źródłowo uzasadnioną ocenę niezależną od odpowiedzi.',
 question='Które fakty i zależności są krytyczne oraz jakie sytuacje ujawnią błąd lub brak kontekstu?',
 depends='M-POC1A; granice źródła sprawdzone.',role='Przegląd wspólny',
 reads=['P/source/source-v1.json','P/evaluation/draft/inventory.json','P/evaluation/draft/dependency-candidates.json','P/evaluation/draft/inventory-review.md',r'C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf (zakres i jawnie oznaczony kontekst)'],
 inputs='Ręczny inwentarz. Ocena: draft przed zamrożeniem, brak pierwszej odpowiedzi.',
 actions=['Przypisz krytyczność warunków, skutków, wyjątków, liczb, negacji, czasu i grafiki.', 'Sprawdź ręcznie relacje jawne/niejawne, kierunek i rodzaj; oddziel wzmianki. Brak celu zapisuj jako wymagający kontekstu.', 'Przygotuj 15–20 sytuacji zwykłych, granicznych, wyjątków i konfliktów z oczekiwanym wynikiem lub uzasadnioną blokadą. Każdy oczekiwany wynik ma podstawę źródłową.'],
 outputs=['P/evaluation/draft/expectations.json','P/evaluation/draft/dependencies.json','P/evaluation/draft/situations.json','P/evaluation/draft/review-questions.md'],
 checks='15–20 sytuacji; wszystkie oczekiwania mają dowód lub status wymagający kontekstu. Osobne mianowniki potwierdzone/niepotwierdzone, jawne/niejawne.',
 excluded='Ekstrakcja, dopasowanie gold do odpowiedzi, interpretacja bez źródła.',
 human='Właściciel uzasadnia krytyczność i oczekiwane rozstrzygnięcia; sporne oczekiwanie pozostaje niepotwierdzone.',
 resume='Kontynuuj od review-questions.md; sprawdź istniejące ID przed dopisaniem kolejnej sytuacji.',
 handoff='M-POC1C otrzymuje kompletny draft i pytania do zamrożenia.'),
dict(id='M-POC1C',milestone='M-POC1',title='Przegląd i zamrożenie eval-v1',
 goal='Zamrozić sprawdzoną podstawę porównania przed ekstrakcją.',
 question='Czy ocena i limity są wystarczająco wiarygodne, aby ocenić pierwszy wynik?',
 depends='M-POC1B; rzeczywisty przegląd właściciela.',role='Właściciel; Codex zapisuje decyzję i hashe',
 reads=['P/source/source-v1.json','P/evaluation/draft/inventory.json','P/evaluation/draft/expectations.json','P/evaluation/draft/dependencies.json','P/evaluation/draft/situations.json','P/evaluation/draft/review-questions.md','docs/POC-PLAN.md'],
 inputs='Draft oceny; wyniki modelu jeszcze nie istnieją.',
 actions=['Przejrzyj dowody, zakres oraz 15–20 sytuacji i zatwierdź tylko sprawdzone oczekiwania.', 'Utrwal progi i limity z planu albo zmień je jawnie przed próbą. Zapisz recenzenta, datę, zakres i nierozstrzygnięcia.', 'Zapisz nowy eval-v1 i pełne hashe plików; przygotuj freeze-public-v1.json zawierający tylko metadane, bez odpowiedzi.'],
 outputs=['P/evaluation/eval-v1/inventory.json','P/evaluation/eval-v1/expectations.json','P/evaluation/eval-v1/dependencies.json','P/evaluation/eval-v1/situations.json','P/evaluation/eval-v1/review.md','P/evaluation/eval-v1/manifest.json','P/evaluation/freeze-public-v1.json'],
 checks='Hashy zgodne, rzeczywisty przegląd zapisany, liczebności sprawdzone. Zamrożenie przed czasem pierwszej ekstrakcji; brak potwierdzenia oznacza waiting_review.',
 excluded='Ekstrakcja, ujawnienie odpowiedzi ekstraktorowi, zmiana historycznych plików.',
 human='Obowiązkowe zatwierdzenie podstawy oceny i limitów przez właściciela. Codex nie podpisuje tej decyzji.',
 resume='Sprawdź czy eval-v1 istnieje: jeśli tak, weryfikuj hashe; poprawki przez erratę i nową wersję, bez nadpisania.',
 handoff='M-POC2A dostaje źródło i metadane zamrożenia; M-POC2B wyłącznie odseparowany pakiet ekstrakcji.'),
dict(id='M-POC2A',milestone='M-POC2',title='Pakiet wejściowy i minimalny format',
 goal='Przygotować powtarzalne wejścia bez klucza oceny.',
 question='Czy pełna reguła/rozdział, obrazy i prosty format wystarczą do pierwszego odczytu?',
 depends='M-POC1C, zamrożony eval-v1.',role='Codex',
 reads=['P/source/source-v1.json','P/evaluation/freeze-public-v1.json','docs/POC-PLAN.md',r'C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf'],
 inputs='Zweryfikowany PDF; wersja oceny eval-v1 znana tylko jako ID/hash.',
 actions=['Przygotuj czytelne rendery PDF 31–37 i tekst pomocniczy, z rozdzielonym celem i kontekstem granicznych kolumn. Nie używaj legacy jako domyślnego importu.', 'Zapisz manifest pełnych hashy i wersji narzędzi. Minimalny format obejmuje reguły, osobne relacje, dowody i luki według planu; przykład wyłącznie syntetyczny.', 'Zapisz dokładny prompt i listę plików do ręcznej sesji. Sprawdź brak treści evaluation/ i oczekiwanych odpowiedzi w pakiecie.'],
 outputs=['P/inputs/v1/manifest.json i pliki wymienione w manifeście','P/formats/proposal-format-v1.md','P/prompts/first-v1.txt','P/inputs/v1/transfer-list.txt'],
 checks='Rendery czytelne; granice prawidłowe; wszystkie hashe sprawdzone; prompt wymaga jawnych luk i nie nadaje akceptacji. Pliki po wysłaniu są niezmienne.',
 excluded='Inferencja, pełny język reguł, importer, magazyn, pełne coverage glifów.',
 human='Oględziny czytelności i granic; techniczne zapisy nie wymagają osobnych potwierdzeń.',
 resume='Jeśli inputs/v1 już wysłano, nie zmieniaj go; porównaj hashe i zapisz nową wersję przy koniecznej zmianie.',
 handoff='M-POC2B otrzymuje wyłącznie transfer-list, manifest, prompt, format i pliki wejść.'),
dict(id='M-POC2B',milestone='M-POC2',title='Pierwsza ręczna ekstrakcja',
 goal='Uzyskać pierwszy wynik bez znajomości oczekiwanych odpowiedzi.',
 question='Jakiej jakości propozycję reguł i zależności daje pierwszy odczyt?',
 depends='M-POC2A; właściciel ręcznie otwiera czystą sesję bez historii oceny.',role='Codex w ręcznej sesji; właściciel obsługuje przekazanie',
 reads=['P/inputs/v1/manifest.json','P/inputs/v1/transfer-list.txt','P/prompts/first-v1.txt','P/formats/proposal-format-v1.md','P/evaluation/freeze-public-v1.json'],
 inputs='Wyłącznie pliki z transfer-list; eval-v1 jako ID/hash bez treści. Nie czytać evaluation/eval-v1, raportów ani prywatnych handoffów oceny.',
 actions=['Sprawdź hashe pakietu i brak oczekiwanych odpowiedzi w kontekście. Jeśli je widziano, oznacz contaminated i nie udawaj ślepej próby.', 'W ręcznej sesji wykonaj prompt; proponowana konfiguracja GPT 6.1 Sol / wysoki. Bez API, GUI i uruchamiania procesu inferencji.', 'Zachowaj całą odpowiedź w oryginalnych bajtach, metadane i dostępny czas. Brak odpowiedzi zapisz jako waiting_response, bez fixture’a.'],
 outputs=['P/runs/first-001/response.raw.txt (lub oryginalny pobrany plik)','P/runs/first-001/run.json','P/runs/first-001/session-evidence.txt','P/measurement/sessions.jsonl'],
 checks='Jeden pierwszy wynik; prompt i wszystkie wejścia znane; rzeczywista aplikacja/model/rozumowanie lub unknown, hashe i odbiór zapisane. Nie poprawiać odpowiedzi na tym etapie.',
 excluded='Oglądanie klucza oceny, korekty, lokalne uzupełnianie wyniku, akceptacja znaczenia.',
 human='Właściciel potwierdza fakty przekazania i widoczną konfigurację; to nie akceptacja reguł.',
 resume='Najpierw sprawdź run.json i plik odpowiedzi. Nie nadpisuj first-001; jawne ponowienie ma nowe ID i liczy czas.',
 handoff='M-POC3 otrzymuje oryginał, metadane i hashe; dopiero oceniający otwiera eval-v1.'),
dict(id='M-POC3',milestone='M-POC3',title='Raport pierwszego wyniku',
 goal='Utrwalić uczciwy baseline przed poprawkami.',
 question='Co jest poprawne strukturalnie, czego brakuje i co wymaga dalszej oceny?',
 depends='M-POC2B; odpowiedź lub udokumentowany brak.',role='Codex; przegląd wspólny rozbieżności',
 reads=['P/runs/first-001/response.raw.txt','P/runs/first-001/run.json','P/inputs/v1/manifest.json','P/formats/proposal-format-v1.md','P/evaluation/eval-v1/manifest.json','P/evaluation/eval-v1/inventory.json','P/evaluation/eval-v1/expectations.json','P/evaluation/eval-v1/dependencies.json'],
 inputs='Oryginalna odpowiedź oraz zamrożony eval-v1; dokładną nazwę pobranego pliku ustala run.json.',
 actions=['Sprawdź format, unikalność ID, referencje, wiązanie wejść, cytaty i obszary obrazów. Zapisz oddzielną reprezentację bez zmiany treści.', 'Porównaj z inwentarzem, rozdziel sześć klas błędów z planu. Podaj liczniki i sprawdzone mianowniki; nieocenialne pola oznacz not_assessable.', 'Zamknij raport przed korektą. Jeśli format blokuje ocenę, zapisz baseline i przejdź przez ograniczony tryb M-POC6A/B, potem wróć do tej karty.'],
 outputs=['P/proposals/first-001/proposal.json i provenance.json','P/reports/first-001/format.json','P/reports/first-001/inventory.json','P/reports/first-001/report.md','P/reports/first-001/metrics.json'],
 checks='Każdy element ma wynik lub jawną nieocenialność; surowy hash bez zmian; raport datowany przed korektą. Schemat nie oznacza akceptacji.',
 excluded='Domykanie wszystkich zależności, semantyczna akceptacja bez człowieka, zmiana eval-v1.',
 human='Wspólne rozstrzygnięcie klasy błędu i kwestii źródłowych; nierozstrzygnięcia pozostają w raporcie.',
 resume='Wznowienie z report.md i listy nieocenionych ID; po korekcie użyj nowego raportu i zachowaj pierwszy.',
 handoff='M-POC4A otrzymuje listę zależności blokujących; M-POC5 otrzyma jawny baseline.'),
dict(id='M-POC4A',milestone='M-POC4',title='Wybór ograniczonego kontekstu',
 goal='Dostarczyć źródło potrzebnych zależności bez rozszerzenia na całą instrukcję.',
 question='Ile dodatkowych stron/reguł/tabel potrzeba, aby usunąć istotne blokady?',
 depends='M-POC3; czytelny wynik i raport. Powtórzenie tylko jako pass-02 w limitach.',role='Codex; przegląd wspólny źródeł',
 reads=['P/source/source-v1.json','P/reports/first-001/report.md','P/reports/first-001/metrics.json','P/evaluation/eval-v1/dependencies.json','P/proposals/first-001/proposal.json',r'C:\dev\spqr\sources\SPQR+Deluxe_Rule+book_WEB.pdf'],
 inputs='eval-v1 i lista luk; przy drugim przejściu dodatkowo P/reports/context-01/report.md i P/context/pass-01/manifest.json.',
 actions=['Dla każdej krytycznej zależności znajdź źródło albo zapisz brak; określ przyczynę i wpływ na sytuacje.', 'Policz unikalny przyrost stron, reguł, tabel, głębokość i czas przed rozszerzeniem: maks. 8/20/4/2 kroki i 2 rundy.', 'Zapisz nowy pakiet kontekstu, dowody, prompt i manifest. Nie osiągalny cel pozostaje blocked_source.'],
 outputs=['P/context/pass-01/targets.json','P/context/pass-01/manifest.json','P/context/pass-01/prompt.txt i pliki dowodów','P/context/pass-01/review.md'],
 checks='Każdy dodany plik ma hash, powód i zakres; brak przekroczeń limitu; nazwane tabele i nienumerowane cele mają ID. Nierozstrzygnięcia nie znikają.',
 excluded='Cała instrukcja, automatyczne obejście limitów, nadpisanie wejść pierwszej próby.',
 human='Przegląd źródeł krytycznych i niejednoznaczności. Zwiększenie limitu wymaga nowej decyzji przed próbą.',
 resume='Czytaj targets.json i dotychczasowe liczniki. Dokończ bieżącą rundę przed rozpoczęciem drugiej.',
 handoff='M-POC4B otrzymuje zamrożony kontekst; bez źródła przekazuje jawną blokadę dalej.'),
dict(id='M-POC4B',milestone='M-POC4',title='Odpowiedź z kontekstem i jej kontrola',
 goal='Oddzielić poprawę wynikającą z kontekstu od późniejszych korekt.',
 question='Które luki zamyka dostarczenie źródła i jakie nowe zależności ujawnia?',
 depends='M-POC4A; runda w budżecie. Jeżeli kontekst niepotrzebny, udokumentowane n/a bez wywołania.',role='Codex w ręcznej sesji; przegląd wspólny',
 reads=['P/context/pass-01/manifest.json','P/context/pass-01/targets.json','P/context/pass-01/prompt.txt','P/runs/first-001/run.json','P/formats/proposal-format-v1.md','P/reports/first-001/report.md'],
 inputs='eval-v1 dla oceniającego; ekstraktor dostaje kontekst, poprzednią propozycję i prompt, bez pełnego klucza oceny.',
 actions=['Uzyskaj odpowiedź ręcznie i zachowaj jej bajty, konfigurację, czas i rodzica; nie mieszaj z niezależną korektą znaczenia.', 'Po odbiorze oceniający czyta P/evaluation/eval-v1/manifest.json, expectations.json, dependencies.json, inventory.json; ponawia kontrolę M-POC3.', 'Zmierz zamknięte/nowe luki i przyrost kontekstu. Drugi krok wymaga osobnej sesji M-POC4A/B i nowych pass-02/context-02.'],
 outputs=['P/runs/context-01/response.raw.txt i run.json','P/proposals/context-01/proposal.json','P/reports/context-01/report.md i metrics.json','P/measurement/sessions.jsonl'],
 checks='Osobna kolumna po kontekście; wszystkie krytyczne zależności poparte albo blokujące; limit nieprzekroczony, regresje zapisane.',
 excluded='Zastępowanie baseline, niejawne korekty, rozstrzygnięcie bez źródła.',
 human='Potwierdzenie, czy dostarczony fragment rzeczywiście uzasadnia domknięcie, nie tylko zgoda modelu.',
 resume='Czytaj run.json i report.md; brak odpowiedzi pozostaje waiting_response. Nie wysyłaj ponownie bez odnotowania próby.',
 handoff='M-POC5A otrzymuje jawnie wskazany hash wyniku po kontekście lub raport n/a.'),
dict(id='M-POC5A',milestone='M-POC5',title='Przegląd znaczenia reguł',
 goal='Ocenić semantykę wobec źródła.',question='Czy warunki, skutki, wyjątki, liczby, negacje i ograniczenia czasowe zachowano?',
 depends='M-POC4 z domknięciem lub jawnymi blokadami.',role='Przegląd wspólny; akceptuje właściciel',
 reads=['P/evaluation/eval-v1/manifest.json','P/evaluation/eval-v1/expectations.json','P/evaluation/eval-v1/inventory.json','P/evaluation/eval-v1/dependencies.json','P/reports/first-001/report.md','P/reports/context-01/report.md','P/proposals/context-01/proposal.json','P/inputs/v1/manifest.json','P/context/pass-01/manifest.json'],
 inputs='eval-v1, źródła wskazane manifestami, wybrany hash odpowiedzi. Przy braku rundy kontekstu użyć first-001 i zapisanego n/a.',
 actions=['Porównaj każde oczekiwanie krytyczne i resztę inwentarza ze źródłem, w tym tabele, diagramy, noty i zakres wyjątku.', 'Zapisz odrębnie błąd odczytu, interpretacji, brak kontekstu i niejednoznaczność. Nie poprawiaj oryginalnej odpowiedzi.', 'Nadaj stany reviewed/pending/blocked tylko z recenzentem i dowodem. Krytyczny brak blokuje zależne rozstrzygnięcia.'],
 outputs=['P/reviews/semantic-01/checklist.json','P/reviews/semantic-01/review.md','P/reviews/semantic-01/issues.json'],
 checks='Pełny spis ocenionych i nieocenionych oczekiwań, brak modelowej autoakceptacji; wszystkie liczby/negacje/wyjątki krytyczne sprawdzone.',
 excluded='Silnik gry, przyjęcie docelowego kontraktu, semantyczna akceptacja wyłącznie testem.',
 human='Właściciel rzeczywiście porównuje reguły z dowodami i zapisuje zakres akceptacji; brak udziału = waiting_review.',
 resume='Od pierwszego pending w checklist.json; zmiana hasha wyniku unieważnia podstawę wcześniejszej oceny dotkniętych elementów.',
 handoff='M-POC5B otrzymuje wynik przeglądu i listę blokowanych reguł; błędy do M-POC6A.'),
dict(id='M-POC5B',milestone='M-POC5',title='Ocena 15–20 sytuacji',
 goal='Sprawdzić użyteczność reguł na konkretnych sytuacjach bez pełnego silnika.',
 question='Czy zwykłe, graniczne i konfliktowe sytuacje mają poprawne rozstrzygnięcie lub właściwą blokadę?',
 depends='M-POC5A; podstawa semantyczna i jawne luki.',role='Przegląd wspólny; akceptuje właściciel',
 reads=['P/evaluation/eval-v1/manifest.json','P/evaluation/eval-v1/situations.json','P/evaluation/eval-v1/dependencies.json','P/reviews/semantic-01/review.md','P/reviews/semantic-01/issues.json','P/proposals/context-01/proposal.json','P/inputs/v1/manifest.json','P/context/pass-01/manifest.json'],
 inputs='Wszystkie 15–20 sytuacji eval-v1 i jawnie wybrany wynik; jeśli nie było kontekstu, first-001 z n/a.',
 actions=['Dla każdej sytuacji zapisz wniosek wynikający z propozycji reguł, użyte zależności oraz źródłowo uzasadniony expected z eval-v1.', 'Porównaj wynik, granice, konflikt i timing; brak krytycznego źródła blokuje odpowiedź, nie daje domyślnego wyniku.', 'Zlicz poprawne, błędne, właściwie/niezasadnie blokowane i nieocenione. Zachowaj pełen mianownik także przy blokadach.'],
 outputs=['P/reviews/situations-01/results.json','P/reviews/situations-01/review.md','P/reviews/situations-01/issues.json'],
 checks='Każda z 15–20 sytuacji oceniona albo jawnie oczekuje; expected i wniosek mają osobne dowody; brak zgadywania.',
 excluded='Implementacja silnika, generowanie nowego gold po zobaczeniu wyniku, usuwanie trudnych sytuacji.',
 human='Właściciel potwierdza rozstrzygnięcia i źródła, zwłaszcza konflikt/wyjątek/granicę. Deklaracja modelu nie zamyka review.',
 resume='Wznowienie od nieocenionej sytuacji; errata gold pozostaje osobno i wymaga ponownej oceny wszystkich porównywanych wariantów.',
 handoff='M-POC6A otrzymuje ID błędów; M-POC7 dostanie komplet wyników, także zablokowanych.'),
dict(id='M-POC6A',milestone='M-POC6',title='Jedna ograniczona korekta w rozmowie',
 goal='Uzyskać poprawkę z zachowaniem historii i mierzalnym kosztem.',
 question='Czy konkretny raport błędów pozwala poprawić wynik bez nowych regresji?',
 depends='Raport z M-POC3, M-POC4B lub M-POC5; budżet korekt niewyczerpany.',role='Codex w ręcznej rozmowie; właściciel przy kwestiach znaczenia',
 reads=['docs/POC-PLAN.md (pętla korekt i limity)','P/runs/first-001/run.json','P/reports/first-001/report.md','P/measurement/sessions.jsonl','P/formats/proposal-format-v1.md'],
 inputs='eval-v1 bez zmiany; konkretny raport i hash rodzica. Dla błędów późniejszych czytaj P/reports/context-01/report.md, P/reviews/semantic-01/issues.json i P/reviews/situations-01/issues.json, jeśli istnieją.',
 actions=['Przed próbą wybierz ograniczony pakiet ID błędów, przyczyny, dowody i spodziewany zakres zmiany. Zapisz correction-01/parent.json z dokładnymi ścieżkami raportów i hashami.', 'Uzyskaj kompletną poprawioną odpowiedź ręcznie, zachowaj prompt i surowe bajty osobno. Bez lokalnego łatania.', 'Zapisz czas i numer próby. Tryb wczesny formatu: najwyżej jedna próba; wszystkie korekty łącznie do trzech. Każda kolejna to nowa sesja i correction-02/03.'],
 outputs=['P/corrections/correction-01/parent.json','P/corrections/correction-01/prompt.txt','P/corrections/correction-01/response.raw.txt','P/corrections/correction-01/run.json','P/measurement/sessions.jsonl'],
 checks='Rodzic i raport istnieją przed korektą; pierwszy wynik niezmieniony; limit czasu/iteracji sprawdzony; brak odpowiedzi jawny.',
 excluded='Nadpisanie odpowiedzi, fixture zamiast modelu, nieograniczone retry, zmiana gold.',
 human='Rozstrzygnięcie niejednoznaczności źródła wymaga człowieka; odwracalny zapis pakietu nie wymaga dodatkowej zgody.',
 resume='Sprawdź parent.json, odpowiedź i licznik prób. Nie licz istniejącej odpowiedzi jako nowej; po przerwaniu zapisz faktyczny koszt.',
 handoff='M-POC6B ponawia właściwe kontrole, następnie wraca do przerwanego M-POC3/4/5 lub kończy pętlę.'),
dict(id='M-POC6B',milestone='M-POC6',title='Ponowna ocena, regresje i koszt',
 goal='Zmierzyć rezultat jednej korekty i zdecydować o końcu pętli.',
 question='Które błędy poprawiono, co zepsuto i ile kosztowała zmiana?',
 depends='M-POC6A; odpowiedź albo zapis braku.',role='Codex; przegląd wspólny',
 reads=['P/corrections/correction-01/parent.json','P/corrections/correction-01/response.raw.txt','P/corrections/correction-01/run.json','P/evaluation/eval-v1/manifest.json','P/evaluation/eval-v1/inventory.json','P/evaluation/eval-v1/expectations.json','P/evaluation/eval-v1/dependencies.json','P/evaluation/eval-v1/situations.json','P/measurement/sessions.jsonl'],
 inputs='Ta sama wersja oceny co rodzic, jego raporty wymienione dokładnie w parent.json; iteracje 02/03 analogicznie.',
 actions=['Ponów format/ID/referencje/dowody oraz kontrole dotkniętych i wszystkich krytycznych elementów. Przejrzyj również wcześniej poprawne sytuacje.', 'Zapisz poprawione błędy, nowe regresje, resztę luk i osobne metryki bez zastępowania baseline lub wyniku kontekstu.', 'Podsumuj iteracje i czas. Po kryteriach lub limicie zakończ pętlę; w trybie wczesnym wróć do wskazanego etapu.'],
 outputs=['P/reports/correction-01/report.md','P/reports/correction-01/metrics.json','P/reports/correction-01/regressions.json','P/reports/correction-01/human-review.md'],
 checks='Porównanie tych samych mianowników; zero ukrytych regresji; człowiek ponownie ocenia zmienione znaczenie. Koniec budżetu zapisany, nie obchodzony.',
 excluded='Kolejna inferencja w tej karcie, ukrywanie błędów przez zmianę testów/oczekiwań.',
 human='Właściciel akceptuje znaczenie poprawek lub utrzymuje pending/blocked; sam format nie wystarcza.',
 resume='Czytaj report.md i listę pending; każde ponowne review wskazuje konkretny hash odpowiedzi.',
 handoff='M-POC7A dostaje końcowy wynik i koszt; ewentualna kolejna M-POC6A wymaga pozostałego budżetu.'),
dict(id='M-POC7A',milestone='M-POC7',title='Porównanie wyników i warianty dalszej pracy',
 goal='Przedstawić podstawę decyzji bez deklarowania sukcesu z góry.',
 question='Czy jakość i koszt uzasadniają dalszą architekturę, zmianę metody lub odrzucenie?',
 depends='M-POC3–M-POC6 zakończone raportami, także przy limitach i blokadach.',role='Codex',
 reads=['P/reports/first-001/report.md','P/reports/first-001/metrics.json','P/reports/context-01/report.md','P/reviews/semantic-01/review.md','P/reviews/situations-01/review.md','P/reports/correction-01/report.md','P/measurement/sessions.jsonl','P/evaluation/eval-v1/manifest.json','docs/LESSONS-LEARNED.md'],
 inputs='eval-v1; wszystkie istniejące rundy są wyliczone ścieżką i hashem w nowym comparison-index.json. Nieistniejący etap ma udokumentowane n/a/blocked, nie wymyślony wynik.',
 actions=['Zbierz index raportów; porównaj pierwszy wynik, każdy kontekst i korekty na tych samych mianownikach. Oddziel naprawę formatu i skażenie oceną.', 'Sprawdź progi decyzji i budżet, podaj ograniczenia oraz brak danych. Przygotuj rekomendację z uzasadnieniem.', 'Rozważ kontrakt, magazyn i orkiestrację tylko jako propozycje wynikające z pomiaru; dla ewentualnego użycia legacy wskaż potrzebę, ograniczenie i alternatywę pozostawienia w archiwum.'],
 outputs=['P/decision/comparison-index.json','P/decision/comparison.md','P/decision/architecture-options.md'],
 checks='Metryki mają sprawdzone mianowniki; koszty obejmują nieudane próby; krytyczne luki jawne. Rekomendacja nie jest decyzją człowieka.',
 excluded='Implementacja architektury, import legacy, stwierdzenie przewagi modelu bez porównania.',
 human='Właściciel otrzymuje raport i dowody do M-POC7B; nie zatwierdza automatycznie rekomendacji.',
 resume='Od brakującego raportu w comparison-index.json; najpierw jawnie wyjaśnij brak danych.',
 handoff='M-POC7B otrzymuje porównanie, opcje i konkretne pytanie o dalszy kierunek.'),
dict(id='M-POC7B',milestone='M-POC7',title='Decyzja właściciela i następny plan',
 goal='Zamknąć eksperyment rzeczywistą decyzją i zakresem dalszej pracy.',
 question='Kontynuować, poprawić metodę czy odrzucić obecne podejście?',
 depends='M-POC7A i dostępny właściciel do przeglądu.',role='Właściciel; przegląd wspólny',
 reads=['P/decision/comparison-index.json','P/decision/comparison.md','P/decision/architecture-options.md','docs/POC-PLAN.md','docs/adr/ADR-0039-archiwum-i-poc-przed-architektura.md','docs/ROADMAP.md'],
 inputs='Ta sama zamrożona ocena co raporty; podstawa decyzji wyliczona hashami w comparison-index.json.',
 actions=['Przejrzyj krytyczne dowody i wynik progów; zapisz decyzję człowieka, zakres akceptacji oraz powody.', 'Dla kontynuacji zaproponuj minimalny następny kontrakt/magazyn/orkiestrację; dla poprawy nowy ograniczony eksperyment; dla odrzucenia zachowaj negatywny wynik.', 'Zapisz kolejny ADR (następny wolny numer od ADR-0040) i nowy plan tylko w zatwierdzonym zakresie. Uaktualnij STATUS/ROADMAP/HANDOFF i regułę next po zakończeniu eksperymentu.'],
 outputs=['P/decision/human-decision.md','docs/adr/ADR-0040-<temat-decyzji>.md (lub następny wolny numer)','docs/adr/README.md','docs/ROADMAP.md, docs/STATUS.md, docs/HANDOFF.md i nowy handoff'],
 checks='Recenzent, data, dowody, decyzja i ograniczenia zapisane; publiczne dokumenty nie ujawniają SPQR. Bez człowieka etap pozostaje waiting_review.',
 excluded='Implementacja następnej architektury, pozorna akceptacja przez model, zmiana historii wyników.',
 human='Obowiązkowa decyzja właściciela o kierunku i akceptacji znaczenia. Żaden inny wykonawca jej nie zastępuje.',
 resume='Czytaj human-decision.md; jeśli brak decyzji, przedstaw istniejące porównanie, nie powtarzaj inferencji.',
 handoff='Następna sesja wykonuje dopiero zatwierdzony nowy plan; archiwum pozostaje zachowane.'),
]
for c in cards:
    common = ('[CLAUDE](../../../CLAUDE.md), [playbook](../../SESSION-PLAYBOOK.md), '
              '[STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md) i wskazany tam handoff, '
              '[ROADMAP](../../ROADMAP.md), [POC-PLAN](../../POC-PLAN.md), '
              '[ADR-0039](../../adr/ADR-0039-archiwum-i-poc-przed-architektura.md).')
    body = f'''# {c['id']}: {c['title']}

- **ID:** {c['id']}
- **Milestone:** {c['milestone']}
- **Rola:** {c['role']}
- **Zależności:** {c['depends']}

## Cel i pytanie eksperymentalne

{c['goal']} {c['question']}

## Dokładne pliki do przeczytania

{common}
Ścieżki poniżej liczone od repo; `P/` oznacza dokładnie `private/poc/spqr-chapter9/`.
Plik przyszłego etapu musi istnieć przed wykonaniem zależnej czynności;
brak zapisujemy jako blokadę, nie uzupełniamy wynikiem modelu.

'''
    body += '\n'.join('- `' + p + '`' for p in c['reads'])
    body += f"\n\n## Wejścia i wersja oceny\n\n{c['inputs']}\n\n## Wymagane działania\n\n"
    body += '\n'.join(f'{i}. {a}' for i,a in enumerate(c['actions'],1))
    body += '\n\n## Artefakty wyjściowe i lokalizacje\n\n'
    body += '\n'.join('- `' + p + '`' for p in c['outputs'])
    body += f"\n\n## Kryteria zakończenia i kontrole\n\n{c['checks']}\n"
    body += '\nKontrole dokumentów: `scripts/check.ps1`; lokalne TMP/TEMP i nowy basetemp. '
    body += 'Zaktualizuj STATUS, ROADMAP i handoff z faktycznym wynikiem. '
    body += 'Jedna sesja do 90 minut; większy zakres podziel przed wykonaniem (M-POC0: jednorazowy zakres właściciela).\n'
    body += f"\n## Zakres wyłączony\n\n{c['excluded']}\n\n## Przegląd człowieka\n\n{c['human']}\n\n## Wznowienie\n\n{c['resume']}\n\n## Przekazanie\n\n{c['handoff']}\n"
    (TASKS / (c['id']+'.md')).write_text(body,encoding='utf-8',newline='\n')
index = '''# Karty pojedynczych sesji

Status milestone'ów: [ROADMAP](../../ROADMAP.md). Bieżąca karta i blokady:
[STATUS](../../STATUS.md). Metoda i limity: [POC-PLAN](../../POC-PLAN.md).
Każda karta ma wejścia, wynik, sposób oceny i przekazanie. Nie jest automatyczną kolejką.

| Milestone | Karta | Rola |
|---|---|---|
'''
for c in cards:
    index += f"| {c['milestone']} | [{c['id']} — {c['title']}]({c['id']}.md) | {c['role']} |\n"
index += '''
M-POC6A/B można wywołać z M-POC3–M-POC5 jako ograniczoną korektę, następnie
wrócić do przerwanej karty. Nie zmienia to milestone'u next na późniejszy ani nie
oznacza wykonania M-POC6 z góry. Każda powtórzona runda to osobna sesja i nowe ID
artefaktów; maksymalnie trzy korekty oraz dwie rundy kontekstu.
Podział karty przed wykonaniem wymaga dopisania kart i aktualizacji indeksu,
ROADMAP oraz STATUS; nie uruchamiamy kilku dużych kart w jednej sesji.
'''
(TASKS/'README.md').write_text(index,encoding='utf-8',newline='\n')
print(f'Created {len(cards)} cards')
