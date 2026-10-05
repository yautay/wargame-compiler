# ADR-0017: Niedostępność węzła nie eskaluje do premium; self-hosted jako zasób obfity

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M-INF0

## Kontekst
- Węzeł inferencji jest osobnym komputerem (ADR-0015), więc może być wyłączony, uśpiony, odcięty od LAN albo w trakcie
  ładowania modelu.
- Ograniczenie kosztu (COST.md) dotyczy premium: ≤ ok. 2× baseline.
- Naiwna obsługa błędu („provider nie odpowiada → wyższy tier”) wysłałaby cały build do premium i rozsadziła budżet,
  a w telemetrii wyglądałaby jak eskalacja semantyczna.

## Decyzja
- **Domyślna polityka niedostępności:** `fallback: {self_hosted_unavailable: queue, allow_premium_fallback: false}`
  (`glu/exec@0#/$defs/fallback_policy`, `build.policy.fallback`, konfiguracja w `profiles.yaml`):
  - job przechodzi w `waiting_inference`, a build w `waiting_inference` (z backoffem i circuit breakerem);
  - błąd dostępności (`unavailable`, `error_class` sieciowy) **nie zużywa** limitu prób jakościowych;
  - `block` zatrzymuje build, a `fail` kończy go błędem.
- **Premium fallback tylko jawnie:** `allow_premium_fallback: true` i budżet premium. Każdy taki przypadek ma
  `routing_decision.premium_reason: self_hosted_unavailable` i osobną metrykę `premium_fallback_cost_usd`.
  Decyzja routingu wybierająca premium zawsze ma `premium_reason`, co wymusza schemat.
- **Bez cichej degradacji:** brak profilu lub capability nie podmienia profilu ani modelu (`capability_missing`).
  Złe wyjście modelu to problem jakości (pętla retry i eskalacji), nie dostępności.
- **Ekonomia:**
  - **self-hosted compute jest zasobem obfitym** bez limitu finansowego, ograniczonym tylko czasem i pojemnością;
  - **premium jest zasobem drogim i selektywnym**;
  - limit 2× dotyczy wyłącznie premium;
  - optymalizujemy premium skorygowane o jakość (`premium_delta` względem baseline), a nie liczbę wywołań.
- **Lokalny multi-pass jest dozwolony**, gdy każdy pass ma cel zapisany w polityce routingu. Przykłady:
  - druga niezależna ekstrakcja;
  - weryfikator;
  - analiza rozbieżności;
  - pass naprawczy po błędach walidacji;
  - `local_deep` jako rozjemca sporów `medium`;
  - lokalne przygotowanie diffu kandydatów do pakietu review.

  Nie budujemy roju agentów.
- Reguły `forced` oraz klasy `high` i `critical` **nadal idą do premium** (ADR-0010 bez zmian). Rozstrzygnięcia
  `local_deep` mają wyższy odsetek audytu premium, dopóki kalibracja nie pokaże, że można go obniżyć.

## Konsekwencje
- Build z niezmienionym wejściem kończy się bez węzła (cache L2). Nowa praca czeka na węzeł.
- `glu stats` rozdziela premium według `premium_reason`, więc fallback nie zafałszuje oceny routingu.
- `glu doctor` (M-E2E) diagnozuje przyczynę `waiting_inference`.
