# ADR-0035: Envelope propozycji, polityka etapu i ownership zbioru outputów

- **Status:** przyjęty
- **Data:** 2026-10-06
- **Milestone:** M-STAB3c

## Kontekst

F07 wskazało brak kontraktu wyjścia zadania i pomieszanie lifecycle rekordu `AMB-` ze stanem rozstrzygnięcia.
F11 wykazało, że przyjęcie mniejszej listy zostawia wcześniej zaakceptowany output. Manifest wywołania
ADR-0033 opisuje odczyt joba, ale nie jego kompletny wynik. ADR-0027 wymaga jawnej listy ról kanonicznych i
deklaracji inferencji przez zadanie. Q-12, Q-16 i Q-17 pozostają otwarte.

## Decyzja

1. **Granica propozycji.** `wgc/proposal@0` jest envelope `{schema, task, output_schema, proposals}`. Każda pozycja
   ma `record` bez `prov`, `status`, `risk` oraz opcjonalne `anchors` i `derived_from`. GLU przekazuje envelope do
   `wgc.kb.accept()`. Lista pozostaje skrótem API Pythona, zamienianym na ten sam envelope przed walidacją. Najpierw
   są sprawdzane kształt envelope i rekord, potem reguły zadania. `TaskSpec.output_schema` wybiera kontrakt etapu:
   `stage1` → `wgc/logic@0#kind`, `stage1.5` → `wgc/digital@0#kind`. Niepasująca para kończy się `KBError`.
   `decoding_schema` M10 pozostaje osobnym, pomocniczym podzbiorem; pełną walidację wykonuje WGC.
2. **Lifecycle a rozstrzygnięcie.** `AMB-` ma `status` z ogólnego lifecycle i osobne obowiązkowe `resolution`:
   `open`, `requires_human_interpretation`, `resolved`, `house_rule`, `wont_fix`. WGC nadaje przy akceptacji
   `status: accepted`; propozycja podaje `resolution`. `resolution` należy do projekcji `logic`, więc wersja
   projekcji rośnie do `wgc/projection@3`. Automatyczna akceptacja `INT-` nadal wymaga decyzji `HD-` w `prov`;
   zwykłe zadanie nie może jej samo nadać.
3. **Owner.** Rekord generowany ma `prov.owner: {task, scope}`. `task` to rodzina zadania bez wersji, `scope` to
   stabilne ID logicznych wejść joba, niezależne od `--scope` i hashy treści. Domyślnie to posortowana lista ID wejść; harvest
   używa ID dokumentu. `TaskSpec.ownership_scope` deklaruje odstępstwo. Jeden owner ma w
   `kb/outputs/<sha256(owner)>.yaml` manifest `wgc/outputs@0` z `active`, `hashes` i `retired`. `hashes` wiąże
   aktywne ID z treścią zaakceptowanego rekordu i chroni przed cichym nadpisaniem ręcznej zmiany. `retired` jest historią
   wycofań; wycofany rekord fizycznie znika z kanonicznych plików `kb/`. Pierwsza akceptacja może przejąć rekordy
   poprzedniej wersji, jeśli zapisany `prov.manifest` jednoznacznie wskazuje ten sam task i logiczny zakres.
4. **Uzgodnienie zbioru.** Pod blokadą pisarza WGC porównuje kompletną listę propozycji z `active` ownera.
   Brakujące ID wycofuje, obecne zastępuje lub zostawia bez zmian. Rekord innego taska, innego zakresu albo o
   statusie innym niż `accepted` jest chroniony konfliktem. Zapis rekordów i manifestu outputów jest jedną partią
   ADR-0031, z tym samym recovery. Receipt zawiera także `retired`, a diagnostyka sprawdza ich nieobecność.
   `derived_from` może wskazywać inny output tej samej partii; cykl jest odrzucany, a projekcja dowodu pochodzi z
   kandydata. Harvest uruchamia job także bez żadnego aktualnego dopasowania, jeśli istnieje manifest jego
   dokumentu; może wtedy wycofać ostatni output. Manifest wywołania nadal opisuje wejścia joba, nie outputy.
5. **Autorytet ADR-0027.** Jawne role `rules`, `living_rules`, `scenario_book`, `charts`, `cards`, `counters`, `map`,
   `module` dają `explicit_source`; `errata`, `faq`, `designer_clarification` dają własny `prov.kind`. Każda inna
   rola, w tym `community_interpretation`, `prior_translation`, `other`, odrzuca automatyczną akceptację. Cytat i
   `span` muszą być potwierdzone; błąd kotwicy zawsze odrzuca. Brak kotwic przy tierze `local` lub `premium` daje
   `llm_inference` tylko przy `TaskSpec.allow_llm_inference=True` i z poprawnym `derived_from`.

## Konsekwencje

- Pierwszy zapis ownera obejmuje co najmniej plik rekordu i manifest, więc używa partii ADR-0031.
- Zmiana roli źródła może zmienić ID wyniku i wycofać poprzedni output tego samego ownera. Rola niekanoniczna
  odrzuca całą akceptację; wcześniejszy rekord pozostaje do obsługi jako stale według Q-12.
- Rozwiązana jest kompletność wyników joba dla istniejącego logicznego zakresu, także po utracie `.glu/`. Nie ma
  jeszcze grafu zależności, trwałych ID, mapy przenumerowań ani polityki wzbogacania `CON-` przez M14.
- Jeśli nie ma już żadnego segmentu dokumentu, planner harvest nie może utworzyć joba na tym dokumencie. To
  przypadek usunięcia źródła (Q-12/M13), nie zniknięcia outputu w nadal istniejącym zakresie.

## Odrzucone warianty

- Manifest outputów wyłącznie w `.glu/`: utrata lokalnego stanu usuwałaby ownership.
- Usuwanie wszystkich rekordów rodziny zadania: niszczyłoby wyniki innych zakresów i decyzje człowieka.
- Ciche nadpisywanie rekordu o tym samym ID z innego zakresu: ukrywa kolizję Q-17.
- `status` niejasności jako stan rozstrzygnięcia: nie da się wtedy jednocześnie przyjąć rekordu i oznaczyć go jako
  wymagający interpretacji człowieka.
