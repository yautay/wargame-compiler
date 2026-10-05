# ADR-0027: Automatyczna akceptacja tylko z ról kanonicznych; niepotwierdzona kotwica to odrzucenie, nie inferencja

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M-STAB1 (decyzja właściciela po sesji); wdrożenie M-STAB3 i M10

## Kontekst
- **Q-13 (przegląd po M9a, F09):** `wgc.kb.accept()` daje `explicit_source` każdej kotwicy w dokumencie, którego rola
  nie jest errata, FAQ ani wyjaśnieniem autora. Dotyczy to też `community_interpretation` i `prior_translation`.
  LOGIC-MODEL mówi, że interpretacja społeczności „nigdy nie jest źródłem kanonicznym sama w sobie” i staje się
  kanoniczna dopiero po `HD-`. W scenariuszu P5 przeglądu taki rekord dostał `status: accepted`.
- **Q-14 (F07/N07):** ADR-0014 przewiduje, że kotwica, której nie da się potwierdzić (brak segmentu, cytat
  niedosłowny), daje `llm_inference` z `derived_from`. ADR-0025 odłożył to do M10 i do tego czasu odrzuca propozycję.
  Samo obniżenie do `llm_inference` zamieniłoby zmyślony cytat w „wniosek”, bez kontroli, że wniosek wynika ze źródła.
- Role dokumentów (`source_document.role`, `wgc/source@0`): `rules`, `living_rules`, `scenario_book`, `charts`,
  `errata`, `faq`, `designer_clarification`, `community_interpretation`, `cards`, `counters`, `map`, `module`,
  `prior_translation`, `other`.
- Właściciel przyjął rekomendacje dla Q-13 i Q-14 (2026-10-05).

## Decyzja
- **Autorytet ról (Q-13).** `accept()` korzysta z jawnej listy ról, które mogą dać automatyczną akceptację kotwiczoną.
  Nie ma permisywnej wartości domyślnej.

  | Rola dokumentu kotwicy | `prov.kind` przy automatycznej akceptacji |
  |---|---|
  | `rules`, `living_rules`, `scenario_book`, `charts`, `cards`, `counters`, `map`, `module` | `explicit_source` |
  | `errata`, `faq`, `designer_clarification` | ta sama nazwa (bez zmian, ADR-0014) |
  | `community_interpretation`, `prior_translation`, `other` i każda rola dodana w przyszłości | brak: propozycja odrzucona |

  - Odrzucenie podaje rolę i powód: źródło niekanoniczne może być tylko dowodem dla decyzji człowieka (`HD-`).
  - Zmiana samego `prov.kind` przy zachowaniu `status: accepted` jest wykluczona.
  - Ścieżka „dowód w pakiecie dla człowieka → `HD-`” powstaje z decyzjami człowieka (M16). Do tego czasu takie
    źródła nie dają rekordów `kb/`.
  - Nowa rola w `wgc/source@0` musi trafić do tej tabeli świadomie (zmiana kontraktu i ADR), inaczej jest odrzucana.
- **Niepotwierdzona kotwica (Q-14).** Kotwica, której nie da się potwierdzić, zawsze odrzuca propozycję, w każdym
  tierze. Dotyczy to braku segmentu, cytatu niedosłownego i `span` poza tekstem. Nie ma automatycznego obniżenia do
  `llm_inference`.
  - W pętli structured output (M10) odrzucenie to Attempt `rejected` z listą błędów zwracaną modelowi w kolejnej
    próbie. Po wyczerpaniu prób następuje eskalacja według polityki routingu.
  - `llm_inference` powstaje wyłącznie jawną ścieżką:
    - zadanie deklaruje, że dopuszcza inferencję (pole polityki w `TaskSpec` albo w kontrakcie propozycji, M-STAB3);
    - propozycja nie ma kotwic, ma `derived_from` wskazujące istniejące rekordy;
    - wykonawca jest tieru `local` albo `premium`.

    Zadanie bez tej deklaracji odrzuca propozycję modelu bez kotwic.
  - Ten punkt zastępuje zdanie ADR-0014 „w przeciwnym razie `llm_inference` z `derived_from`”. Reszta ADR-0014
    (rodzaj provenance nadaje WGC, model nie wysyła `prov`) obowiązuje bez zmian.

## Konsekwencje
- **Wdrożenie:**
  - M-STAB3 dodaje listę ról w `wgc.kb`, deklarację inferencji zadania i ich miejsce w kontrakcie propozycji
    (`wgc/proposal@0`), z testami dla każdej roli;
  - M10 dodaje informację zwrotną o odrzuconej kotwicy w pętli prób.
- **Do wdrożenia obowiązuje stan obecny** (ADR-0025):
  - kotwica w roli niekanonicznej nadal daje `explicit_source`. Gra benchmarkowa nie ma takich dokumentów, a zadania
    modelowe jeszcze nie istnieją;
  - propozycja modelu bez kotwic, z `derived_from`, nadal daje `llm_inference` bez deklaracji zadania.
- Dokument z rolą `other` nie da automatycznie rekordów, dopóki nie dostanie właściwej roli. To świadomie ostra
  reguła. Złagodzenie wymaga nowego ADR.
- Odrzucenia zamiast obniżeń zwiększą liczbę ponowień i eskalacji w M10–M14. Koszt mierzy M-INF i M14.
- Przy odrzuceniu kotwicy nie ma ryzyka cichego przyjęcia zmyślonego cytatu, a każdy rekord `llm_inference`
  pochodzi z zadania, które to jawnie dopuszcza.

## Odrzucone warianty
- **Tylko inny `prov.kind` dla ról niekanonicznych:** rekord nadal byłby `accepted`, czyli kanoniczny (przegląd, Q-13
  opcja C).
- **Osobny status `proposed` z promocją przez `HD-` już teraz:** pełniejszy workflow, ale wymaga decyzji człowieka
  (M16). Odłożony, nie odrzucony.
- **Automatyczne obniżenie niepotwierdzonej kotwicy do `llm_inference` (pierwotne ADR-0014):** legalizuje błędny
  cytat i ukrywa błąd modelu przed pętlą prób.
- **Lista ról zakazanych zamiast dozwolonych:** nowa rola przechodziłaby po cichu.
