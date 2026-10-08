# ADR-0019: Plik YAML może zawierać wiele dokumentów, każdy z własnym kontraktem

- **Status:** przyjęty
- **Data:** 2026-10-05
- **Milestone:** M1

## Kontekst
Koperta dokumentu ([DATA-CONTRACTS §3](../DATA-CONTRACTS.md#3-koperta-dokumentu)) nazywa jeden kontrakt w polu
`schema`. Kontrole provenance z M1 łączą rekordy różnych kontraktów: `anchor_hash_mismatch` porównuje kotwicę
rekordu `wgc/logic@0` z `text_hash` segmentu `wgc/source@0`. Fixture'y niepoprawne semantycznie
(`contracts/fixtures/invalid/semantic/`) mają być samowystarczalne: `wgc validate <plik>` ma dać dokładnie jeden
oczekiwany kod błędu, bez dociągania innych plików. Z jednym kontraktem na plik nie da się tego zapisać.

## Decyzja
- Plik YAML może zawierać kilka dokumentów oddzielonych `---`. Każdy dokument ma własne pole `schema` i jest
  walidowany względem swojego kontraktu (L0).
- `wgc validate` traktuje rekordy domenowe ze wszystkich dokumentów i plików jako jeden zbiór (L1, provenance).
  Lokalizacja diagnostyki wskazuje n-ty dokument jako `plik#n`.
- Pliki jednodokumentowe pozostają formą podstawową. `wgc/contracts.py:load` nadal czyta jeden dokument;
  wielodokumentowe czyta `wgc/validate.py:load_documents`.

## Konsekwencje
- Fixture'y i małe przykłady mogą łączyć Stage 0 i Stage 1 w jednym pliku.
- Narzędzia czytające pliki KB muszą używać `load_documents`, inaczej pominą dokumenty po pierwszym `---`.
- Układ plików nadal nie niesie semantyki (§3).

## Odrzucone warianty
- **Nakładka na `valid/`** (test waliduje `[valid/, fixture]`): fixture nie jest samowystarczalny, a `wgc validate`
  na pojedynczym pliku daje szum wiszących referencji.
- **Fixture jako katalog:** więcej plików, a kryterium akceptacji mówi o plikach.
