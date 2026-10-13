# IG-0 Krytyczna recenzja modelu danych

- **Etap:** IG-0.
- **Status:** done jako recenzja i planowanie po doprecyzowaniu celu; bez akceptacji semantyki gry.
- **Wykonawca:** nowa sesja recenzująca; właściciel przyjmuje zakres kontraktu.

Czytaj README, CLAUDE, [STATUS](../../STATUS.md), [HANDOFF](../../HANDOFF.md),
[plan](../../IG-PLAN.md), [model](../../IG-DATA-MODEL.md),
[profile](../../IG-MECHANICS-PROFILES.md),
[ADR-0040](../../adr/ADR-0040-ig-i-archiwum-poc.md) i
[prompt](../../prompts/IG-0-critical-review.md).
Prywatne badania: private/ig/research/2026-10-11/.

Sprawdź źródła i struktury. Szukaj mechanik bez jednoznacznej reprezentacji,
nadmiarów i mieszania wiedzy o regułach ze stanem partii. Porównaj alternatywy,
zapisz konkretne przykłady, sprawdź źródłowo trudne przypadki.

Raport: docs/reviews/IG-0-critical-review.md; szczegóły w private/ig/.
Każde istotne zastrzeżenie ma dowód, wpływ i proponowaną zmianę.
Wynik określa minimum IG-1, rozszerzenia i pytania dla właściciela.
Pierwotnie etap był partial do ustalenia kierunku. Właściciel doprecyzował
pełną instrukcję, reużycie KB oraz deterministyczne legalne akcje dla AI.
Plan został zapisany; przyszła implementacja zaczyna się od IG-1.

Aktualizacja po doprecyzowaniu właściciela: przygotowano
[architekturę WGU + instrukcja → IG](../../IG-WGU-ARCHITECTURE.md)
i [plan pełnej instrukcji](../../IG-PLAN.md). Mała próba z D3 nie jest już
rekomendowanym następnym krokiem. Przy realizacji dopiąć źródła, profil
wykonawczy i organizację review. Wymagania wykonawcze:
[legalne akcje](../../IG-LEGAL-ACTIONS.md). Kolejna karta to [IG-1](IG-1.md).

Wyłączenia: pełna ekstrakcja, silnik, importer legacy, API inferencji,
automatyzacja GUI, zmiana archiwum lub historycznej oceny.

## Wynik recenzji 2026-10-11

[Raport](../../reviews/IG-0-critical-review.md) porównuje cztery alternatywy,
wskazuje dziesięć zastrzeżeń, minimum IG-1, koszty i decyzje D1–D5.
Poprawiono oba aktywne drafty (IG-0-review-1). Dowody i siedem szkiców
reprezentacji z pięciu rodzin profili są w private/ig/reviews/IG-0/.
Odczyty fragmentaryczne i ograniczenia jawne; 36 przypadków nie wykonano
jako testów. Nie powstał silnik ani przyjęty kontrakt. Na moment samej
recenzji etap pozostawał partial; później ukończono plan zgodny z celem
właściciela. Done dotyczy pracy projektowej, nie poprawności całego IG.
