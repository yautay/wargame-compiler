# ADR-0003: Model logiki niezależny od języka docelowego

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M0

## Kontekst
Bazy `wgu` (wg-spqr, virgin-queen, Ukraine43) mają `language.kb: pl`, czyli mechanikę zapisaną polskimi parafrazami.
Logika jest przez to związana z językiem tłumaczenia, a zmiana polskiego terminu dotyka bazy logiki. Silnik `spqr`
prowadził własną bazę po angielsku, niezależną od `wg-spqr`. SPQR był więc analizowany dwa razy, z niezgodnymi ID.

## Decyzja
- Stage 1 zapisuje mechanikę **strukturalnie** (Rule IR: modalność, aktor, akcja, warunki, efekty, limity, timing).
- Pole `statement` jest tylko glosą, domyślnie w języku źródła (`project.yaml: language.kb`).
- Pojęcia (`CON-…`) mają nazwy w języku źródła. Tłumaczenie terminów i glos należy do Stage 3: glosariusz wiąże
  `CON-…` z odpowiednikiem w języku docelowym.
- Jedna gra ma jeden model logiki. Z niego kompilują się digitalizacja, pomoce do gry i wydania.

## Konsekwencje
- Zmiana polskiego terminu nie unieważnia Stage 1 ani 1.5.
- Właściciel czyta glosy po angielsku albo widoki z przetłumaczonymi glosami (artefakt Stage 3, niekanoniczny).

## Odrzucone warianty
KB w języku docelowym (stan obecny): wiąże logikę z jednym przekładem.
