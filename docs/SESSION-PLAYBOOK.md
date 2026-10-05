# Playbook sesji

Dotyczy sesji AI, które **rozwijają to narzędzie**. Pracę nad konkretną grą wykonuje GLU (buildy, joby) i właściciel
(decyzje). Ten playbook jej nie opisuje.

## Procedura sesji (8 kroków)
1. **Bootstrap:** przeczytaj `CLAUDE.md`, potem ten plik.
2. **Stan:** przeczytaj [STATUS.md](STATUS.md) (bieżący milestone, otwarte kwestie, ryzyka) i ostatni handoff
   ([HANDOFF.md](HANDOFF.md)).
3. **Milestone:** znajdź bieżący milestone w [ROADMAP.md](ROADMAP.md). Przeczytaj tylko dokumenty wskazane w jego
   zakresie i w handoffie (dyscyplina kontekstu).
4. **Jeden slice:** wykonaj zakres milestone'u, nic ponad. Rzeczy spoza zakresu zapisz jako kwestie w STATUS.
   Jeśli zakres jest za duży, podziel milestone (`Mna`/`Mnb`, bez kropki, bo test ciągłości przyjmuje tylko `M[\w-]+`)
   w ROADMAP **przed** pracą.
5. **Testy akceptacyjne:** `python -m pytest`. Testy milestone'u muszą przechodzić. Nie zostawiaj czerwonych testów.
   Jeśli coś się nie udało, zapisz to w handoffie z wynikiem testu.
6. **Decyzje:** każda decyzja architektoniczna to nowy ADR w `docs/adr/` + wpis w `docs/adr/README.md`. Decyzja
   odwracająca wcześniejszą to nowy ADR, który zastępuje stary.
7. **STATUS:** zaktualizuj [STATUS.md](STATUS.md): status milestone'u w ROADMAP, nowy bieżący milestone, kwestie, ryzyka.
8. **Handoff:** utwórz `docs/handoff/RRRR-MM-DD-Mn.md` według szablonu niżej i podmień wskaźnik w [HANDOFF.md](HANDOFF.md).

Test `tests/test_continuity.py` sprawdza, że STATUS, ROADMAP, HANDOFF i ADR są ze sobą spójne. Czerwony test ciągłości
oznacza niedokończoną sesję.

## Zasady
- **Zapisuj fakty, decyzje i stan, nie tok rozumowania.** Żadnego chain-of-thought w repo.
- Kod i nazwy pól po angielsku. Dokumentacja, komunikaty CLI dla użytkownika i skille po polsku.
- Teksty chronione (instrukcje wydawców) nigdy nie trafiają do tego repo (ADR-0012).
- Zmiana kontraktu (`contracts/schemas/`) w tej samej sesji aktualizuje fixture'y, testy i `docs/DATA-CONTRACTS.md`.
- Commit i push tylko na prośbę właściciela. Praca na gałęzi, jeśli właściciel tak ustali.
- Windows: pliki z backslashami i długie skrypty pisz narzędziem do zapisu plików, nie heredokiem (ADR-0008, ARCHAEOLOGY §3).

## Rozmiar sesji
Dobry milestone:
- kończy się w jednej sesji (orientacyjnie ≤ 10–15 zmienionych plików, ≤ ok. 1500 linii kodu i testów),
- ma kryteria akceptacji sprawdzalne testem,
- ma jasne „poza zakresem”,
- zostawia repo w stanie zielonym.

Zły milestone: „Implement GLU”, „Zrób digitalizację”. Dobry: „Implement job state model”, „Implement deterministic routing”.

<a id="role-modeli"></a>
## Role modeli
Proces nie jest związany z nazwą modelu. Role:
| Rola | Kto (dziś) | Do czego |
|---|---|---|
| **Architecture Model** | najmocniejszy dostępny model | Session 0, kontrakty, prompty zadań, złote modele, ADR o dużym zasięgu |
| **Implementation Model** | szybki model dobry w kodowaniu | milestone'y IMPL według ROADMAP |
| **Local Worker** | model self-hosted na węźle w LAN (profile `local_*`, ADR-0015) | joby GLU w buildach (nie rozwój narzędzia) |
| **Premium Reviewer** | mocny model przez API lub Claude Desktop | pakiety review w buildach, przegląd kontraktów na prośbę |
| **Human Reviewer** | właściciel | decyzje domenowe, interpretacje, terminy, akceptacja ADR o kosztach |

## Szablon handoffu (`docs/handoff/RRRR-MM-DD-Mn.md`)
```markdown
# Handoff: Mn <tytuł> (RRRR-MM-DD)
- **Model/rola:** …
- **Wynik:** done | partial | blocked
## Zrobione
- …(pliki, polecenia)
## Testy
- `python -m pytest`: N passed / M failed (jeśli failed: które i dlaczego)
## Decyzje
- ADR-NNNN …
## Niezrobione / poza zakresem
- …
## Następny krok
- Mn+1: … (pierwsza czynność, pliki do przeczytania)
## Ryzyka i pułapki odkryte w sesji
- …
```
