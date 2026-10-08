# ADR-0015: Self-hosted inference na osobnym węźle w LAN

- **Status:** przyjęty (zastępuje ADR-0008)
- **Data:** 2026-10-05
- **Milestone:** M-INF0

## Kontekst
- ADR-0008 zakładał jedną maszynę: Windows 11 + WSL2 + RTX 3090, a na niej GLU, serwery modeli (`127.0.0.1`), LaTeX
  i Claude Desktop (przez `wsl.exe`).
- Właściciel ma inny układ. Maszyna z Claude Desktop (dev machine, bez GPU, tu powstała Session 0) to inny host niż
  dedykowany komputer inferencji w LAN: Windows 11 Pro, RTX 3090 24 GB, Ryzen klasy 9800X3D, 128 GB RAM.
- „Lokalny model” w dokumentacji znaczył dotąd „model na localhost”.

## Decyzja
- **`local` znaczy self-hosted.** Modele działają na naszej infrastrukturze i pod naszą kontrolą, na dowolnym hoście.
  Tier `local` i profile `local_*` zachowują nazwy, a zmienia się ich definicja. Nic w projekcie nie zakłada localhost.
- **Inference node** to osobny komputer w LAN z Inference Gateway (`igw`, ADR-0016) i runtime'em modeli (ADR-0018).
  Jest **wymienialnym workerem obliczeniowym**:
  - nie zna domeny WGC (reguł, etapów, gier, przekładu);
  - nie jest źródłem prawdy;
  - nie przechowuje KB, cache wyników, promptów ani tekstu źródeł.

  Wyczyszczenie lub wymiana węzła kosztuje najwyżej ponowne obliczenia.
- Warstwy i kierunek zależności:

  ```text
  WGC → GLU → Provider abstraction → self_hosted provider → LAN (HTTPS) → igw → runtime → GPU/CPU/RAM
  ```

  - WGC nie wie nic o sieci ani GPU;
  - GLU nie wie, czy bramka działa na localhost, w LAN, w WSL czy na Linuksie.
- **Dev machine** (Claude Desktop, MCP, GLU, repo gier, `.glu/`) nie wymaga GPU ani WSL2. GLU i WGC są wieloplatformowe,
  więc mogą działać natywnie na Windows albo w WSL2. LaTeX (TeX Live) pozostaje do wyboru: WSL2 albo natywnie.
- **Sieć i bezpieczeństwo są częścią architektury** (docs/inference/NODE.md §7, DEPLOYMENT.md):
  - endpoint wskazuje nazwę hosta, a nie IP;
  - HTTPS z przypiętym certyfikatem, token dla każdego klienta;
  - Windows Firewall wpuszcza tylko hosty z allowlisty;
  - runtime słucha wyłącznie na `127.0.0.1` węzła.
- **Testy (bez zmian z ADR-0008):**
  - żaden test nie wymaga GPU, sieci ani modelu;
  - testy providera i bramki używają atrap w procesie (`fake` runtime, transport w pamięci), a nie gniazd;
  - core działa na Windows i Linuksie.
- MVP to jeden węzeł. API nie zakłada dokładnie jednego GPU (`node_id`, lista profili, lista endpointów w konfiguracji
  GLU), więc drugi węzeł albo router o tym samym API nie zmienia GLU.

## Konsekwencje
- Dochodzą milestone'y M-GW1, M-NODE, M-E2E i M-GW2 (ROADMAP). Zmieniają się M10, M11, M12, M-INF i M22.
- `kb/` nigdy nie zapisuje hosta ani węzła (`prov.by.model` to id modelu lub fingerprint). Węzeł zapisuje się tylko
  w `.glu/` (Attempt).
- Teksty źródeł (ADR-0012) przechodzą przez LAN do własnego węzła. Węzeł nie zapisuje ich na dysk ani do logów.
- Q-03 (repo gier w systemie plików WSL) dotyczy już tylko dev machine i tylko wtedy, gdy GLU działa w WSL2.

## Odrzucone warianty
- Model na tej samej maszynie co Claude Desktop: maszyna nie ma GPU, a połączenie obu ról miesza odpowiedzialności.
- GLU łączący się bezpośrednio z runtime'em (ADR-0009): wiąże GLU z runtime'em i nie daje miejsca na kolejkę,
  cykl życia modeli, autoryzację ani telemetrię węzła.
