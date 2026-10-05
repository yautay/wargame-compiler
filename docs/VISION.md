# Wizja

**wargame-compiler** przeprowadza kontrolowaną kompilację instrukcji gry wojennej. Nie budujemy łańcucha
„PDF → AI → tłumaczenie”, tylko kompilator z jawnymi etapami, kontraktami, bramkami i śledzeniem:

```text
SOURCE RULEBOOK (+ errata, FAQ, karty, tabele)
        ↓  Stage 0: inwentarz i segmenty (deterministycznie)
SEMANTIC COMPILATION
        ↓  Stage 1: Logic / Data
CANONICAL LOGICAL MODEL ───────────────→ Stage 1.5: Digitalization Architecture → GAME ENGINE SPEC (+ testy)
        ↓
Stage 2: EDITORIAL MODEL (jak oryginał komunikuje treść)
        ↓
Stage 3: TRANSLATION / PUBLICATION MODEL → LaTeX, PDF, pomoce do gry
```

## Zasady
1. **Model logiki jest źródłem prawdy semantycznej.** Wszystko inne się z niego kompiluje, a nic go nie zmienia
   bez przeglądu.
2. **Każdy fakt ma pochodzenie.** Inferencja nigdy nie udaje treści instrukcji.
3. **Niepewność jest wynikiem, nie błędem.** `requires_human_interpretation` to poprawny stan końcowy automatu.
4. **Model nie jest pamięcią projektu.** Stan żyje w plikach: `INPUT → EXECUTOR → PROPOSED → VALIDATOR → ACCEPTED`.
5. **Najpierw deterministycznie, potem self-hosted, premium selektywnie, człowiek tam, gdzie zgadywanie jest
   niedopuszczalne.**
6. **Niezmienione wejście = zero wywołań modelu.** Zmiana jednej reguły przelicza tylko to, co od niej zależy.
7. **Śledzenie w obie strony:** od segmentu źródła do testu silnika i od nieudanego testu z powrotem do źródła.
8. **Repozytorium jest pamięcią projektu.** Sesje AI zaczynają od plików, nie od historii rozmowy.

## Role
- **WGC** (pakiet `wgc`, rola „WGU”) to domena: kontrakty, KB, walidatory, narzędzia deterministyczne, zadania.
- **GLU** (pakiet `glu`) to wykonanie: joby, routing, providerzy, cache, przyrostowość, interfejsy CLI i MCP.
- **Knowledge Base** w repo gry jest źródłem prawdy.
- **Self-hosted LLM** („local”: nasza infrastruktura, dedykowany węzeł RTX 3090 w LAN za Inference Gateway, nie
  localhost) wykonuje większość pracy. To zasób obfity, a węzeł jest wymienialnym workerem bez wiedzy domenowej.
  **Premium LLM** jest drogim, selektywnym, bezstanowym recenzentem. **Człowiek** rozstrzyga to, czego system nie
  powinien zgadywać.

## Poza zakresem (na teraz)
Pełny silnik gry, edytor wizualny, wiele gier naraz w jednym repo, baza wektorowa jako źródło prawdy.
