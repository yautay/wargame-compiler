# ADR-0029: Przekład Stage 3 pisze premium; wierność sprawdzają wykonawcy niezależni od tłumacza

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M9b (decyzja właściciela w trakcie sesji); wdrożenie M26

## Kontekst
- Dotychczasowy plan Stage 3 (EDITORIAL-PUBLICATION, M26): szkic przekładu pisze profil self-hosted `local_translate`,
  kontrole terminów i wsteczna ekstrakcja IR są lokalne, premium dostaje tylko rozbieżności, `high`/`critical`
  i próbkę audytową, a redakcja językowa jest „lokalnie lub premium”.
- Węzeł ma 24 GB VRAM (NODE §4): profil `semantic` to model rzędu 24–32B w 4 bitach. Jakość stylu polszczyzny
  takiego modelu jest według oceny właściciela i architekta wyraźnie niższa niż najmocniejszego modelu premium.
  Nie ma pomiaru.
- Wierność znaczeniu da się sprawdzić deterministycznie i lokalnie (kroki 1–3 weryfikacji). Stylu nie da się tak
  sprawdzić: redakcja słabego szkicu zwykle daje gorszy tekst niż przekład od zera.
- Właściciel ustalił (2026-10-05): przekład ma być możliwie najładniejszy językowo.
- Obecny workflow `wgu` (ARCHAEOLOGY §1.1) przekłada wyłącznie premium: tłumacz, weryfikator znaczenia i redaktor,
  czyli trzy przebiegi premium na segment. To baseline `B_translate` (COST §1, niezmierzony).

## Decyzja
- `translate.segment` wykonuje **premium** (profil `premium_translate`) dla każdego segmentu w zakresie. Pakiet
  zawiera segment źródła, projekcję semantyczną IR segmentu, zatwierdzone terminy glosariusza (`CON-`), konwencje
  Stage 2 i przewodnik stylu. Redakcja językowa (dawny krok 5) jest częścią tego przebiegu.
- Wierność sprawdzają wykonawcy **niezależni od tłumacza**:
  - kroki 1–2 deterministycznie (terminy, liczby, odsyłacze, sygnały vs IR);
  - krok 3 self-hosted (`local_semantic`): wsteczna ekstrakcja IR z przekładu i deterministyczne porównanie z IR.
  Płynność daje premium, poprawność kontrole, które nie dzielą jego błędów.
- Rozbieżność w krokach 1–3 wraca do premium z diffem (poprawka przekładu albo `requires_human_interpretation`).
  Poprawiony tekst przechodzi kroki 1–3 ponownie. Osobnego przeglądu znaczenia premium dla zgodnych segmentów nie ma.
- Wyczerpany budżet premium albo niedostępny provider premium: job czeka (`waiting_review`). **Nigdy** nie spada
  do szkicu lokalnego (jak reguła 10 INFERENCE-ROUTING i ADR-0017).
- Model lokalny nie pisze przekładu do `kb/publication/`. Profil `local_translate` i profil węzła `translate`
  przestają być wymagane.

## Konsekwencje
- **Kontrakt:** decyzja routingu z `chosen: premium` wymaga `premium_reason` (`glu/exec@0`), a żadna obecna wartość
  nie opisuje „zadanie ma premium jako tier podstawowy”. M26 dopisuje wartość (np. `task_policy`) jako zmianę
  addytywną szkicu `@0`, z fixture'ami, testami i DATA-CONTRACTS w tej samej sesji. Telemetria liczy ją osobno od
  `semantic_escalation` i `infrastructure_fallback`, żeby nie zacierać oceny routingu Stage 1.
- **Koszt:** Stage 3 staje się w większości premium (jeden przebieg pisania na segment + poprawki rozbieżności).
  Szacunek: ok. 0,4–0,7 × `B_translate`, bo znikają przebiegi weryfikatora i redaktora premium. To hipoteza
  do pomiaru względem `B_translate` z M-BASE. Limit premium ≤ ok. 2× baseline obowiązuje bez zmian (COST §2).
  Podział „większość pracy self-hosted” (VISION) dotyczy odtąd Stage 0–2; Stage 3 ma wyjątek z tego ADR.
- **M26:** zakres bez wyboru modelu przekładu na węźle. Akceptacja dostaje ślepe porównanie kilku stron przekładu
  nowego i obecnego workflow `wgu`, ocenione przez właściciela. Bez niego cel „najładniejszy przekład” nie jest
  mierzony.
- **M-INF:** nie musi wybierać modelu przekładu (nie było go w zakresie; NODE §4 przestaje go zakładać).
- **Ryzyko:** premium może „wygładzić” znaczenie (zmiękczyć zakaz, przesunąć granicę). Chronią przed tym kroki 1–3
  i testy mutacyjne przekładu (QUALITY §3). Wsteczna ekstrakcja ma niższą jakość niż premium, więc FN kroku 3
  trzeba zmierzyć na mutacjach w M26.
- **Prywatność:** cały tekst źródła w zakresie przekładu trafia do providera premium (dziś też tak jest).

## Odrzucone warianty
- **Szkic lokalny + redakcja premium każdego segmentu:** premium i tak czyta każdy segment, a redakcja słabego szkicu
  daje zwykle gorszy tekst niż przekład od zera. Oszczędność tylko na tokenach wyjścia.
- **Przekład lokalny, premium przy rozbieżności (dotychczasowy plan):** najtańszy, ale styl zależy od modelu 24 GB,
  sprzeczny z celem właściciela.
- **Rozstrzygnięcie ślepym testem przed decyzją:** właściciel wybrał jakość od razu; ślepe porównanie zostaje jako
  kryterium akceptacji M26, nie jako warunek decyzji.
