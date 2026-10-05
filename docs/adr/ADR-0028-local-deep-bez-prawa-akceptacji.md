# ADR-0028: `local_deep` bez prawa akceptacji w `routing@0`; spór i reguły `forced` zawsze idą do premium

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M-STAB1 (decyzja właściciela po sesji); wdrożenie M12

## Kontekst
- **Q-15 (przegląd po M9a, F14/N11):** dokumenty dawały sprzeczne konsekwencje sporu modeli:
  - LOGIC-MODEL: `local_disagreement` (dwie niezależne ekstrakcje różnią się po normalizacji) to reguła `forced`
    z klasą minimalną `high`;
  - INFERENCE-ROUTING reguła 6: każda reguła `forced` i klasa `high`/`critical` idą do Tier 3 (premium);
  - INFERENCE-ROUTING reguła 11: przy sporze `medium` `local_deep` rozstrzyga, a zgoda z jednym kandydatem, walidacja
    i brak `forced` dają akceptację lokalną. Przy sporze warunek „brak `forced`” nigdy nie zachodzi, więc reguła 11 była
    martwa albo sprzeczna z regułą 6, zależnie od kolejności czytania;
  - ADR-0017 wymienia `local_deep` jako rozjemcę sporów `medium`; QUALITY (L3) mówi „bez prawa do akceptacji
    `forced`/`high`”.
- Powtórzenie tego samego modelu albo podobnego promptu nie daje niezależnych błędów. Zgoda dwóch odpowiedzi nie jest
  pomiarem jakości. Gold (M3) i próbki kontrolnej (Q-02) jeszcze nie ma, więc nie da się skalibrować wyjątku.
- Właściciel przyjął rekomendację dla Q-15 (2026-10-05).

## Decyzja
- W `routing@0` `local_deep` **nigdy nie daje akceptacji**. Jego role:
  - pass naprawczy po błędach walidacji. Wynik przechodzi zwykłą walidację i podlega tym samym regułom ryzyka, co
    wynik Tier 1/2; sam pass nie obniża klasy ani nie znosi reguły `forced`;
  - przygotowanie diffu kandydatów i analizy rozbieżności do pakietu review dla Tier 3.
- Spór dwóch wykonań lokalnych (`local_disagreement`) zawsze kończy się Tier 3. Reguły `forced` oraz klasy `high`
  i `critical` idą do premium także po zgodzie `local_deep` (ADR-0010 bez zmian).
- Reguła 11 INFERENCE-ROUTING brzmi odtąd: spór Tier 1 vs Tier 2 albo wyczerpane próby na Tier 2 → `local_deep`
  przygotowuje diff, pass naprawczy i pakiet, potem Tier 3. Akceptacja lokalna tylko przez reguły 4 i 5.
- Wyjątek (akceptacja lokalna po rozstrzygnięciu `local_deep` dla określonej klasy sporu) wymaga osobnego ADR po
  kalibracji na gold i próbce kontrolnej: zdefiniowana klasa rozbieżności, normalizacja i zmierzony odsetek FN.

## Konsekwencje
- Jedna tabela pierwszeństwa: reguły 6 i 11 nie są już sprzeczne. M12 testuje to tabelarycznie (już w akceptacji M12:
  „reguły `forced` idą do premium także po zgodzie `local_deep`”).
- Wyższy udział premium dla sporów `medium` niż zakładał wariant z rozjemcą. Kosztorys (COST, `p_escalate`, `p_deep`)
  traktuje `local_deep` jako koszt czasu węzła zmniejszający pakiety review, nie jako źródło akceptacji.
- Linia „rozstrzygnięcia `local_deep`” w QUALITY nie dotyczy `routing@0`; wraca tylko z ADR wyjątku.
- ADR-0017 (lokalny multi-pass) obowiązuje; jego punkt o `local_deep` jako rozjemcy oznacza rozjemcę przygotowującego
  diff, bez prawa akceptacji.

## Odrzucone warianty
- **Rozjemca `local_deep` z prawem akceptacji sporów `medium` (pierwotna reguła 11):** brak dowodu bezpieczeństwa;
  sprzeczny z `local_disagreement` jako `forced`.
- **Głosowanie większością wykonań lokalnych bez kalibracji:** jak wyżej, błędy nie są niezależne.
- **Usunięcie `local_disagreement` z reguł `forced`:** osłabia ochronę przed FN, którą ADR-0010 stawia wyżej niż koszt.
