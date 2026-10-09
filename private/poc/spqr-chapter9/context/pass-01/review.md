# M-POC4A / pass-01 - pakiet przygotowany do przeglądu

Wynik karty: **partial / waiting_review**. Wybór i audyt plikowy wykonano;
źródła krytyczne i znaczenie nie otrzymały nowej akceptacji człowieka.
Pakiet niezamrożony, nieprzekazany. M-POC4B nie rozpoczęto.

Baseline first-001 ma zgodne oryginalne bajty, manifesty, closure, eval-v1
i wszystkie 16 768 zakresów provenance. Pełny dowód jest w nowym
measurement/M-POC4A-pass-01/baseline-integrity.json. Samoopis ekstraktora
nie dowodzi konfiguracji, historycznego przekazania ani czystego kontekstu.
Wszystkie te kwestie oraz czas aktywny pozostają unknown.

## Wybór i koszt przed rozszerzeniem

Wybrano tylko kompletny Step 4 reguły 8.46: PDF27, lewa kolumna,
bbox PDF pt [40,413,300,650]. Pełne rendery PDF26/27 obejrzano: nagłówek
8.46, kontynuacja i granica przed 8.47 są zgodne. Obejrzano także finalny
wycinek: cztery bullety i końcowe odesłanie są czytelne i nieprzycięte.
To lokalizacja i kompletność wycinka ocenione przez Codex, bez akceptacji znaczenia.

Przyrost liczony przed utworzeniem context/pass-01: **1 unikalna strona,
1 reguła, 0 tabel**. Współdzielony fragment dla trzech deklaracji liczy się raz.
Dostarczona ścieżka 9.32 -> 8.46/Step-4 ma 1 krok; rozważana ścieżka
do CTX-TBL-SHOCK-CRT ma 2 kroki i kończy się blocked_source.
Na granicy 2 kroków zatrzymano dalsze rozszerzanie: nie dodano dalszych
gałęzi, tabel, pełnych procedur ani pass-02. Obowiązuje pierwszy osiągnięty limit.
Limity 8/20/4/2/2 bez zmian. Przygotowano 1 pass, zarezerwowano rundę 1;
wykonano **0 rund odpowiedzi, 0 nowych inferencji, 0 korekt**.
Czas aktywny i pozostały budżet unknown; zgodność budżetu czasu unknown.

Pełne rendery recenzenta i skan lokatorów 44 stron należą do pracy źródłowej
oceniającego, nie do wejść ekstraktora. Dodatkowy payload źródłowy to wyłącznie
wycinek PDF27 i jego pomocniczy tekst/metadane. Nie dostarczono całego PDF.
Odwołania do 8.45 i 10.13 w wycinku nie oznaczają dodania ich procedur.

## Rozliczenie źródeł i niepewności

critical-source-audit.json rozlicza 8 potwierdzonych zależności wykonawczych:
wszystkie mają istniejące źródła/cele w baseline, przyrost 0. Trzy brakujące
pary wewnętrzne zachowano jako obserwacje strukturalne, bez automatycznej
zewnętrznej ekspansji i bez lokalnej naprawy odpowiedzi.
Rozliczono również 8 zamrożonych wymagań kontekstu oraz 105 niepotwierdzonych
kandydatur. Deklarowaną krytyczność draftu zachowano jako deklarację;
nie rozszerza gold i nie nadaje akceptacji celu/aliasów.

| Wymaganie | Dostępność i wpływ |
|---|---|
| EXP-010 | blocked_source: brak wskazanej rzeczywistej mapy/kompasu; SIT-06 nadal blokada kierunku |
| EXP-019 | blocked_source: brak identyfikacji leadera/scenariusza i jego konkretnych wyjątków; brak przypisanego SIT |
| EXP-031 | tylko Step 4; dokładny Shock CRT blocked_source, kolejność/interpretacja do review; lokalna SIT-09 nie zastąpiona pełnym realnym wynikiem |
| EXP-033 | blocked_source: brak konkretnego scenariusza i listy DD; SIT-11 nadal blokada eligibility |
| EXP-050 | blocked_source: brak rzeczywistego setupu/date/OC/AWL/stanu; SIT-16 ma zadane dane syntetyczne i zachowuje lokalny zakres |
| EXP-064 | blocked_source: brak przypisania BI/leader/Initiative; SIT-18 nadal blokada, SIT-19 ma wyłącznie syntetyczny mapping |
| EXP-066 | blocked_source: brak dokładnych Combat Tables i wpisów CH; nie zaakceptowano aliasów ani nowych wartości |
| EXP-074 | warunkowa krytyczność; brak wskazanego rzeczywistego żetonu/parametru; nie zastępuje syntetycznych danych SIT-14/17 |

declaration-review.json zawiera **79/79** kandydatów: 3 z częściowym wybranym
źródłem, 56 z pomocniczymi kandydatami lokalizacji i 20 blocked_source.
Każdy ma surowy pointer/span/hash, powód, źródłowe wystąpienie, zakres,
wpływ i pending dla rzeczywistej konieczności. Lokator nagłówka nie dowodzi
kompletności procedury. Brak tabeli w pakiecie nie jest twierdzeniem, że
nie istnieje ona w całej grze. Wyszukiwanie nie objęło dowolnych innych
repozytoriów ani internetu. G916/G953 pozostają oddzielnymi deklaracjami
niejednoznaczności do M-POC5, bez domyślnego pozyskiwania wyjaśnień modelu.
Znaczenie, semantyczne TP/FP/FN i sytuacje pozostają not_assessable.

## Review człowieka i wznowienie

Brak nowej decyzji człowieka. Właściciel powinien obejrzeć trzy pliki evidence/
i potwierdzić albo odrzucić przydatność i zakres krytycznego źródła;
rozstrzygnięcie znaczenia i kolejności pozostaje osobnym zakresem jego review.
Do decyzji należy także jawne zachowanie brakującego CRT i konkretnych
źródeł scenario/map/counter, bez dorabiania pełnych rozstrzygnięć.
Akceptacja źródła nie oznacza akceptacji znaczenia ani zgodności budżetu czasu.

Dokładne wznowienie: M-POC4A od targets.json, manifest.json i tego review;
zapisać nowy rekord decyzji z zakresem/hashami, dopiero wtedy zamrozić
zaakceptowany pakiet i przekazać osobnej M-POC4B. Nie nadpisywać decyzji,
baseline ani zamrożonej oceny. Prompt jest przygotowanym draftem, niewykonanym.
Manifest oznacza allowlistę ekstraktora; cała reszta jest evaluator_only.
