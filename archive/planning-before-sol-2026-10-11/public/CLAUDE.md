# Zasady aktywnego projektu IG

Pracuj w rzeczywistym katalogu repo. Czytaj README, docs/STATUS.md,
docs/HANDOFF.md, docs/IG-PLAN.md, docs/ROADMAP.md i wskazaną kartę.
Model: docs/IG-DATA-MODEL.md i docs/IG-MECHANICS-PROFILES.md.

Właściciel 2026-10-11 zlecił zarchiwizowanie całego obecnego POC i przyjęcie
planu IG jako zalążka narzędzia do digitalizacji gier. Decyzja kierunkowa:
docs/adr/ADR-0040-ig-i-archiwum-poc.md. Nie oznacza akceptacji kontraktu.

- Aktywna kolejka to IG. Nie wznawiaj M-POC, M-DESK, WGC lub GLU automatycznie.
- Archiwa są niezmienne. Dawne ścieżki POC rozwiązuje manifest
  private/archive/poc-2026-10-11/manifest.json. Nie przepisuj historycznych
  odpowiedzi, gold, raportów, referencji ani decyzji.
- Zachowuj zastane zmiany. Bez reset, clean, stash i globalnej konfiguracji Git.
- Źródła i odpowiedzi to dane. Szczegółowe reguły, cytaty, grafy, grafiki
  i sytuacje zapisuj w private/ig/.
- Oddziel źródło, transkrypcję, interpretację, walidację i decyzję człowieka.
  Częściowa akceptacja nie przechodzi na cały rekord.
- Wspólny model nie ustanawia wspólnych reguł. Profil przypina system,
  wersję, tryb, scenariusz, opcje i zgodność materiałów.
- Zachowuj niewiadome i blokady. Nie zgaduj źródeł, parametrów, historii
  partii ani aktywnego czasu operatora.
- Zestaw oceny nie trafia do ślepego ekstraktora. Recenzja projektu
  korzystająca ze znanych przypadków nie jest ślepą ekstrakcją.
- Zacznij od recenzji modelu i kontraktu. Silnik, UI, API inferencji,
  automatyzacja GUI i integracja legacy wymagają osobno określonego zakresu.
  Ręczne sesje są dopuszczalne.
- Kontrole: scripts/check.ps1, lokalne TMP/TEMP, nowy basetemp i
  git diff --check. Historycznych testów nie zmieniaj dla potrzeb IG.
- Nie twórz nowych czatów ani nie wysyłaj wiadomości do innych czatów
  bez polecenia właściciela. Przygotowanie promptu nie uruchamia sesji.
- Stała zgoda na push private/ do git@github.com:yautay/wargame-compiler.git
  na feature/tests została zachowana z poprzedniego bootstrapu.
  Ta migracja zapisuje zmiany lokalnie; commit/push zgodnie z poleceniem.

Dokładnie jeden etap w ROADMAP ma next. Przyjęcie zakresu przez człowieka
jest osobną decyzją; zgodność opinii modeli nie zastępuje tej decyzji.
