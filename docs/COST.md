# Model kosztu i obserwowalność

## 1. Baseline (1.0×): jak go zmierzyć
**Stan dzisiejszy: baseline nie jest zmierzony.** Tabela benchmarku w starym `docs/MODELE.md` jest pusta. Dlatego
milestone **M-BASE** mierzy obecny workflow, zanim padną liczby. Robimy to **jak najwcześniej**, bo korpus (a)
istnieje od M0. Każda późniejsza zmiana routingu raportuje `premium_delta` względem tego punktu.

Procedura M-BASE:
1. Korpus: (a) gra benchmarkowa `bench/minigame` (w całości), (b) jeden rozdział prywatnej gry (np. rozdział walki
   z repo gry, w kopii roboczej).
2. Obecny workflow `wgu`: `/wgu:atomizacja` (analityk Opus, effort max) na korpusie, a dla (b) dodatkowo
   `/wgu:tlumaczenie --proba` (tłumacz + weryfikator + redaktor).
3. Pomiar: wywołania premium, tokeny wejścia i wyjścia per model, rozmiar kontekstu na wywołanie (z transkryptów
   sesji lub raportu użycia Claude Code), liczba tur, czas ścienny, liczba interwencji człowieka. Koszt = tokeny × cennik listowy API danego modelu w dniu pomiaru
   (także gdy praca szła w ramach subskrypcji, dla porównywalności).
4. Wynik: `B_logic` (koszt na 100 segmentów reguł) i `B_translate` (koszt na 100 segmentów przekładu) zapisane
   w `docs/STATUS.md` i w ADR, jeśli zmieniają decyzje.

## 2. Ograniczenie
**Koszt premium ≤ ok. 2× baseline**, docelowo poniżej 1× dzięki pracy self-hosted. **Limit dotyczy wyłącznie premium
LLM** (ADR-0017):

```text
SELF-HOSTED GPU = zasób obfity (bez limitu finansowego; ograniczają go czas i pojemność węzła)
PREMIUM LLM     = zasób drogi i selektywny (budżet ≤ 2× baseline)
```

Optymalizujemy **premium skorygowane o jakość**, a nie łączną liczbę wywołań inferencji. Dodatkowy pass self-hosted
jest dobry, jeśli zmniejsza eskalacje premium przy tym samym lub lepszym FN-rate.

Mierzone osobno:
- `premium_cost_usd`, `premium_calls`, `premium_tokens_in/out`, `premium_context_tokens` (rozmiar pakietów); obie drogi:
  API i `desktop_pull`;
- `premium_*` według `premium_reason`. Fallback dostępności (`self_hosted_unavailable`) jest liczony osobno jako
  `premium_fallback_cost_usd` i nie zaciera oceny routingu;
- `local_gpu_seconds` (raportowane przez węzeł, wraz z ładowaniem modeli), `local_queue_seconds`;
- `wall_seconds` (od startu buildu do stanu końcowego, bez czasu oczekiwania na człowieka i na węzeł; te liczymy osobno).

## 3. Model szacunkowy
Dla etapu z `N` jednostkami (segmenty lub rekordy):
```text
premium_tokens ≈ N × (p_escalate + p_audit) × T_package
premium_cost   ≈ premium_tokens_in × c_in + premium_tokens_out × c_out
local_gpu_time ≈ N × (1 + p_second_pass + p_retry + p_deep × k_deep) × t_job / concurrency + swaps × t_load
```
- `p_escalate`: udział `high`/`critical` + spory + porażki walidacji (z benchmarku; na start zakładamy 0,2–0,3),
- `p_audit`: próbka audytowa (0,1 na start, zmniejszana po kalibracji),
- `T_package`: rozmiar pakietu review (cel ≤ 4k tokenów wejścia, ≤ 1k wyjścia),
- `p_second_pass`: udział `medium` (druga niezależna ekstrakcja lokalna),
- `p_deep`, `k_deep`: udział jobów z passem `local_deep` i jego względny koszt czasu (model wolny, tryb wsadowy).
  Ten pass jest opłacalny, jeśli obniża `p_escalate`.

Obecny workflow wysyła **całość** pracy do modelu premium (czytanie całej instrukcji, ekstrakcja, relacje, przegląd).
Nowy wysyła tylko `p_escalate + p_audit` (rzędu 30–40% jednostek na start), a każdy pakiet jest mały i samowystarczalny.
Ostateczna ocena pochodzi z pomiaru (M28), nie z tego szacunku.

## 4. Dźwignie kosztu
| Dźwignia | Efekt | Ryzyko |
|---|---|---|
| Tier 0 dla wszystkiego, co deterministyczne | 0 tokenów | — |
| Cache L1/L2 + early cutoff | ponowne buildy kosztują ~0 | błędny klucz cache → nieaktualny wynik (stąd fingerprinty) |
| Fale wg profilu | mniej przełączeń modelu | dłuższy czas ścienny przy małych buildach |
| Mały kontekst (`context_builder` z grafu) | mniejsze pakiety | brak kontekstu → błąd; łagodzi ryzyko `dependency_degree` |
| Spadek `p_audit` po kalibracji | mniej premium | wolniej wykryty dryf modelu lokalnego |
| `desktop_pull` | koszt w subskrypcji | limity i czas człowieka |
| Lokalny multi-pass (weryfikator, rozjemca `local_deep`, pass naprawczy) | mniej `p_escalate`, mniejsze pakiety | dłuższy czas węzła; FN, jeśli kalibracja zawiedzie (stąd podwyższony audyt) |
| Brak premium fallbacku przy niedostępnym węźle (domyślnie) | awaria LAN nie zużywa budżetu | build czeka (`waiting_inference`) |

<a id="obserwowalnosc"></a>
## 5. Obserwowalność
Każdy Attempt i Build zapisuje metryki w `.glu/state.db`. `glu stats [--build ID] [--since DATA] [--json]`
(M11) raportuje:

| Metryka | Definicja |
|---|---|
| `jobs_total`, `jobs_deterministic`, `jobs_local`, `jobs_premium`, `jobs_human` | joby wg tieru, który je zakończył |
| `cache_hits` (L1, L2) | trafienia na poziom |
| `retries`, `escalations` | próby ponowne, przejścia tieru (z powodem) |
| `tokens_in/out` per tier i profil | z Attempt |
| `premium_cost_usd` | suma kosztów API (+ szacunek dla `desktop_pull`) |
| `local_gpu_seconds`, `model_swaps`, `local_queue_seconds` | czas GPU, przełączenia modeli, czas w kolejce węzła (raportuje węzeł) |
| `premium_calls`, `premium_context_tokens`, `premium_by_reason` | wywołania premium, rozmiar pakietów, podział według `premium_reason` |
| `premium_delta` | zmiana premium względem baseline i względem poprzedniej wersji polityki routingu (`glu stats --compare`) |
| `inference_unavailable_seconds`, `premium_fallback_cost_usd` | czas w `waiting_inference`; koszt jawnie dozwolonego fallbacku |
| `wall_seconds`, `human_wait_seconds` | czas ścienny, czas oczekiwania na człowieka |
| `routing_decisions` per reguła polityki | ile razy zadziałała reguła 1–10 z `routing@N` |
| `validation_failures` per kod błędu | L0/L1/L2 |
| `audit_disagreements` | niezgodności audytu premium (szacunek FN) |
| `stage_coverage` | z raportów bramek |
| `digitalization_coverage` | metryki z [DIGITALIZATION.md](DIGITALIZATION.md#pokrycie) |

Raport buildu (`reports/builds/<build>.json`, opcjonalnie commitowany) zawiera te agregaty i wersje polityk
(`routing@N`, `wgc/risk@N`, `gate.*@N`), więc da się porównać buildy w czasie.
