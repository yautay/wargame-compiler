# Playbook sesji POC

1. Przeczytaj [bootstrap](../CLAUDE.md), [STATUS](STATUS.md), [HANDOFF](HANDOFF.md)
   i wskazany handoff, [ROADMAP](ROADMAP.md), [POC-PLAN](POC-PLAN.md) oraz bieżącą kartę.
2. Sprawdź Git i pliki. Przy błędzie własności stosuj wyłącznie parametr polecenia
   `git -c safe.directory=C:/dev/wargame-compiler ...`; nie zmieniaj konfiguracji globalnej.
   Zachowaj zastane zmiany; nie wykonuj reset/clean/stash. Commit i push wykonuj
   zgodnie z poleceniami właściciela; stała zgoda na push `private/` do wskazanego
   repozytorium na `feature/tests` jest zapisana w bootstrapie.
3. Sprawdź zależności karty, wersję oceny i limity. Planuj do 90 minut pracy na kartę;
   jeśli zakres się nie mieści, podziel go przed wykonaniem na jawnie nazwane części.
   M-POC0 ma jednorazowy zakres archiwum i planu wskazany przez właściciela.
4. Wykonuj tylko kartę. Materiały SPQR i odpowiedzi są prywatnymi danymi.
   Karta M-POC2B jest wyjątkiem od czytania prywatnych wyników poprzednich sesji:
   przekazanie zawiera wyłącznie pakiet ekstrakcji i metadane zamrożenia, bez oczekiwań.
5. Zachowuj surowe bajty, hashe i czas. Każdy etap ma osobny raport. Awaria/brak
   odpowiedzi to stan `waiting_response`, brak źródła `blocked_source`, brak przeglądu
   `waiting_review`; nie zamieniaj ich w sukces lub puste poprawne dane.
6. Błąd wykryty w M-POC3–M-POC5 trafia do raportu i ograniczonej pętli korekt
   [planu](POC-PLAN.md#korekty). Nie trzeba czekać do M-POC6, by odblokować format.
   Zachowaj pomiar pierwszego wyniku; korekta nie zmienia zamrożonych oczekiwań.
7. Przegląd człowieka: zamrożenie oceny, interpretacje i źródła krytyczne, ocena sytuacji,
   końcowa akceptacja oraz decyzja. Odwracalne operacje plikowe nie wymagają osobnych zgód.
8. Uruchom [kontrole](../scripts/check.ps1). Zapisz także błędy, bez ich ukrywania.
   ROADMAP ma dokładnie jeden `next`; STATUS wskazuje ten etap i jedną bieżącą kartę.
   Aktualizuj handoff i wskaźnik; nie oznaczaj etapu done przed rzeczywistym wykonaniem.

## Dokumenty i odpowiedzialność

ROADMAP prowadzi statusy milestone'ów, karty szczegółowy zakres, STATUS pracę i blokady,
HANDOFF najnowsze przekazanie. Status karty jest w STATUS/handoffie; nie duplikujemy
automatycznej kolejki. M-POC7 może zakończyć eksperyment także decyzją o odrzuceniu;
nie oznacza to sukcesu ekstrakcji. Po zamknięciu całego planu zasada jednego `next`
wymaga jawnej aktualizacji testu i roadmapy, nie pozornego kolejnego etapu.

Codex przygotowuje artefakty i pomiary; właściciel ocenia źródła i znaczenie;
przegląd wspólny rozstrzyga rozbieżności na podstawie materiału źródłowego.
Żaden zapis modelu „approved” nie zastępuje odnotowanej decyzji człowieka.

## Handoff jednej sesji

Zapisz datę, ID karty/milestone, `done|partial|blocked`, wykonawcę, wejścia i hashe,
artefakty, wyniki kontroli i ograniczenia, wykorzystany budżet, przeglądy człowieka,
otwarte błędy, dokładną czynność wznowienia i następną kartę.
Publiczny handoff nie zawiera treści reguł ani szczegółowych sytuacji.
Prywatny rejestr sesji przechowuje dowody oraz czasy.

Archiwalny playbook nie jest aktywną instrukcją. Dostęp do starego projektu:
[README archiwum](../archive/legacy-2026-10-07/README.md).
