# Model jakości i benchmarki

## 1. Drabina walidacji
| Poziom | Co sprawdza | Kto | Kiedy blokuje akceptację |
|---|---|---|---|
| **L0 schemat** | zgodność z `wgc/*@N` | `wgc.contracts` | zawsze |
| **L1 referencje** | unikalność ID, zgodność `kind` ↔ prefiks, rozwiązywanie `refs`, `derived_from`, `realizes`, końców relacji, `anchors.seg` | `wgc.validate` (M1) | zawsze |
| **L2 domena** | provenance (cytat dosłowny w segmencie, zgodny `seg_hash`, rola dokumentu), sygnały źródło↔IR (zakaz → `must_not` lub negacja, operator graniczny → `cmp` z właściwym operatorem, liczby ze źródła obecne w IR), markery wyjątków → relacje, `partial` → `unformalized` | `wgc.validate` (M5) | błędy zawsze, ostrzeżenia podnoszą ryzyko |
| **L3 zgodność** | dwie niezależne ekstrakcje self-hosted zgodne po normalizacji; spór idzie do premium; `local_deep` przygotowuje tylko diff i pakiet review, bez prawa akceptacji (ADR-0028) | GLU + WGC (normalizacja IR) | dla `medium` |
| **L4 odpowiadalność** | każdy `case` da się odpowiedzieć wyłącznie z KB (łańcuch istnieje, werdykt zgodny) | WGC + lokalny model | gate Stage 1 |
| **L5 przegląd premium** | znaczenie, kompletność wyjątków, granice | premium | `high`/`critical`, spory, audyt |
| **L6 człowiek** | interpretacje, terminy, polityki | właściciel | `requires_human_interpretation` |

## 2. Metryki jakości
- **Dokładność ekstrakcji** (benchmark logiki): na poziomie pól IR. `modality`, `nature` i operator limitu porównywane
  dokładnie; `conditions` strukturalnie po normalizacji (kolejność `all`/`any` bez znaczenia); `refs` jako F1.
- **Relacje:** precyzja i czułość par (from, type, to).
- **Niejasności:** czułość wykrycia zasianych niejasności (gra benchmarkowa ma je opisane w `phenomena.yaml`).
- **FN-rate routingu:** odsetek błędnych rekordów zaakceptowanych lokalnie. Mierzony mutacjami (offline) i audytem
  premium (online). **Cel: 0 na mutacjach krytycznych.**
- **Koszt jakości:** eskalacje na 100 rekordów, tokeny premium na rekord (zob. [COST.md](COST.md)).

## 3. Testy mutacyjne (lekcja z próby SPQR)
Heurystyki i walidatory testujemy parami: poprawny artefakt i ten sam artefakt z wstrzykniętym błędem.

| Operator | Przykład | Klasa |
|---|---|---|
| `modality_flip` | `may` ↔ `must`, `must_not` → `may` | krytyczna |
| `boundary_shift` | `<=` → `<`, „equal to or less” → „less” | krytyczna |
| `drop_exception` | usunięcie relacji `exception_to` / zdania z „except” | krytyczna |
| `drop_limit` | usunięcie „only once per phase” | krytyczna |
| `scope_change` | `per: phase` → `per: game_turn` | krytyczna |
| `number_change` | 4 → 5 | krytyczna |
| `negation_scope` | „nie może ruszać się ani strzelać” → „nie może ruszać się lub strzelać” | wysoka |
| `actor_swap` | `active_player` → `opponent` | wysoka |
| `connective_swap` | `all` ↔ `any` | wysoka |
| `override_inversion` | odwrócenie `REL overrides` | wysoka |

Mutacje stosuje się do: IR (test walidatorów L2 i modelu ryzyka), tekstu przekładu (test kroków 1–3 weryfikacji
przekładu) i specyfikacji 1.5 (test interpretera testów). Wynik: tabela wykrycia per operator i per warstwa.

<a id="property-based"></a>
## 3a. Testy właściwości (property-based)
Złote przykłady to za mało. Od pierwszego użycia dochodzi **Hypothesis** (zależność deweloperska, dopisywana do
`requirements.txt` w milestonie, który jej użyje):

| Właściwość | Gdzie | Milestone |
|---|---|---|
| `content_hash` nie zależy od kolejności kluczy ani formy NFC; `text_hash` nie zależy od zawijania wierszy | `wgc.canonical` | M1 (opcjonalnie), M2a |
| build przyrostowy = build od zera (te same rekordy i hashe) dla losowych zmian segmentów | `glu.graph` | M13 |
| generowane stany gry spełniają inwarianty; snapshot round-trip zachowuje hash | `wgc/state@0` | M17 |
| akcja nielegalna nie zmienia stanu; `can_perform` jest czysty; granice `cmp` (≤/<) zachowują się na wartościach brzegowych | interpreter testów | M18, M21 |
| pierwszeństwo nadpisań: `REL overrides` wygrywa niezależnie od kolejności rekordów | interpreter testów | M19 |
| scheduler węzła: brak zagłodzenia profilu, liczba przełączeń ograniczona, budżet VRAM nieprzekroczony | `igw` | M-GW2 |

## 4. Korpus benchmarkowy
Teksty w repo narzędzia są **wyłącznie własne** (ADR-0012). Benchmarki na grach komercyjnych żyją w `private/bench/`.

```text
bench/
├── README.md
├── minigame/                       Drill Skirmish (CC0): rulebook.md + phenomena.yaml
│   ├── gold/                       (M3) złoty model: source, logic; (M17–M21) digital + testy; (M24) editorial;
│   │                               (M26) referencyjny przekład PL
│   └── mutations/                  (M4) definicje mutacji i oczekiwane wykrycia
└── suites/                         (M3+) opisy zestawów i scorery
private/bench/                      (gitignored) np. rozdział GCACW-PL przez importer kb@1 (M-LEG)
```

### Logic
explicit rules, exceptions, nested conditions, negation, numeric limits, scope, overrides, ambiguities, cross references.
Każde zjawisko ma w grze benchmarkowej ≥ 1 regułę (mapa w `bench/minigame/phenomena.yaml`). Scorer porównuje IR ze
złotym modelem (sekcja 2).

### Digitalization
state transitions, legal actions, illegal actions, triggers, events, randomness, hidden information, override priority,
replay, boundary cases. Scorer: (a) zgodność rekordów 1.5 ze złotymi (akcje, `LEG-` z `reason_code`, zdarzenia),
(b) testy wykonywane przez referencyjny interpreter (M21): spec przechodzi złote testy, a mutacje spec są wykrywane.

**Łańcuch benchmarku digitalizacji** (§41 promptu), dla kluczowych mechanik gry benchmarkowej:
```text
source meaning (rulebook.md 3.4) → Rule IR (R-3.4) → Digitalization Model (LEG-move.routed_adjacent) →
expected state transition (TST-001: odrzucenie z reason_code move.routed_adjacent, stan bez zmian)
```
Złoty łańcuch jest zapisany dla: ruchu z kosztem i wyjątkiem pierwszego heksu (3.2), zatrzymania obok wroga i jego
wyjątku (3.3/3.5), zakazu dla rozbitych (3.4), walki z modyfikatorem i tabelą (4.2–4.4), rally z granicą i
nadpisaniem scenariusza (5.2/7.1), ujawnienia rezerw (6.2, zablokowane przez AMB-001).

### Editorial
terminology (inwentarz terminów źródła i konwencji zapisu: F1), style/register (klasyfikacja rejestru segmentów:
trafność), modal language (konwencje modalności), structure (mapa sekcji, ramek i przykładów: zgodność).

### Translation
semantic fidelity (wsteczna ekstrakcja IR z przekładu zgodna z IR + wykrywanie mutacji przekładu), terminology
consistency (odsetek wystąpień `CON-` w zatwierdzonej formie), style preservation (ocena redaktora na próbce
+ zgodność z konwencjami Stage 2). Referencyjny przekład PL gry benchmarkowej powstaje w M26.

## 5. Progi akceptacji (do kalibracji)
| Obszar | Wstępny próg | Kiedy rewidować |
|---|---|---|
| Ekstrakcja self-hosted, pola krytyczne IR | ≥ 95% zgodności z gold przed akceptacją lokalną `low` | M-INF |
| Rozstrzygnięcia `local_deep` (spory `medium`) | nie występują w `routing@0` (ADR-0028); próg obowiązuje dopiero po ADR wyjątku: audyt premium 2× wyższy niż reguła 9, dopóki niezgodność ≤ 2% | po gold i próbce kontrolnej |
| Mutacje krytyczne, wykrycie przez L2 + ryzyko | 100% | każda zmiana `wgc/risk@N` |
| Audyt premium akceptacji lokalnych | niezgodność ≤ 2%, inaczej podnieść próg ryzyka | co build pilotażowy |
| Złote testy 1.5 na interpreterze | 100% | M21 |
