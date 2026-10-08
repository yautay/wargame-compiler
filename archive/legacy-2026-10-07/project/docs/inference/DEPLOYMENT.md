# Wdrożenie węzła inferencji (Windows 11 Pro, RTX 3090)

Plan wdrożenia, który milestone **M-NODE** (HUM) zamienia w sprawdzoną procedurę i skrypty PowerShell
(`deploy/node/`, tworzone w M-NODE). Architektura: [NODE.md](NODE.md). Decyzje: ADR-0015…0018 ([rejestr](../adr/README.md)).

> Ustalenia sprzed wdrożenia oznaczone **(weryfikacja M-NODE)** trzeba potwierdzić na sprzęcie. Po wykonaniu M-NODE
> ten plik opisuje stan faktyczny.

<a id="zalozenia"></a>
## 1. Założenia
| Element | Wartość |
|---|---|
| Węzeł | Windows 11 Pro, RTX 3090 24 GB, Ryzen 9800X3D (lub zbliżony), 128 GB RAM, NVMe na modele |
| Nazwa hosta | `ai-node` (nazwa komputera Windows + wpis w DNS routera albo rezerwacja DHCP z nazwą). **Nie wpisujemy IP w konfiguracji** |
| Port | **TCP 8443** (HTTPS, `igw`). Runtime `llama-server` na portach efemerycznych **tylko na 127.0.0.1** |
| Klienci | dev machine (Claude Desktop, MCP, GLU). Allowlista: konkretne adresy lub nazwy, nie cała podsieć |
| Konto | lokalne konto usługi bez uprawnień administratora (np. `svc-igw`) |
| Katalogi | `C:\igw\` (binarki, venv), `D:\models\` (GGUF), `%ProgramData%\igw\` (`node.yaml`, `secrets\`, `logs\`, certyfikat) |

<a id="instalacja"></a>
## 2. Instalacja (kolejność)
1. **Sterownik NVIDIA** (aktualny, gałąź Studio albo Game Ready), weryfikacja przez `nvidia-smi`. Zasilanie: plan
   „Wysoka wydajność”, **bez uśpienia i hibernacji**. Aktualizacje Windows z godzinami aktywności i bez automatycznego
   restartu w trakcie pracy.
2. **llama.cpp**: oficjalny build Windows z CUDA (wersja przypięta i zapisana w `node.yaml`). Rozpakowanie do
   `C:\igw\llama.cpp\`. Test ręczny: `llama-server.exe -m <model> --host 127.0.0.1 --port 8090`, potem
   `curl.exe http://127.0.0.1:8090/health`.
3. **Python ≥ 3.10** i venv `C:\igw\venv`, instalacja pakietu z `[node]` (od M-GW1).
4. **Modele**: pobierane świadomie przez właściciela, z sha256 zapisanym w `node.yaml`. Bramka weryfikuje sha256 przy
   pierwszym ładowaniu i liczy z niego `model_fingerprint`.
5. **Certyfikat TLS**: samopodpisany z SAN `DNS:ai-node`, ewentualnie `DNS:ai-node.lan`, ważny 2 lata. Klucz w
   `%ProgramData%\igw\secrets\` z ACL tylko dla `svc-igw` i administratorów. Część publiczna (`ai-node.pem`) trafia na
   dev machine do `~/.config/glu/` (`ca_file`). Narzędzie: `openssl` (np. z Git for Windows) albo
   `New-SelfSignedCertificate` z eksportem do PEM **(weryfikacja M-NODE)**.
6. **Tokeny**: `igw token new --client dev-machine` (M-GW1) zapisuje hash w `tokens.json` i wypisuje token raz.
   Token trafia do zmiennej środowiskowej `GLU_AI_NODE_TOKEN` na dev machine (albo do keyringu). Nigdy do repo.
7. **`node.yaml`**: profile, modele, limity, nasłuch na adresie interfejsu LAN (przykład w [NODE.md §4](NODE.md#profile)).
8. **Autostart** (§4) i **firewall** (§3).

<a id="siec"></a>
## 3. Sieć i Windows Firewall
- Profil sieci karty LAN: **Private** (Ustawienia → Sieć → właściwości). Reguła działa tylko w tym profilu.
- Reguła wejściowa (PowerShell jako administrator; adresy klienta z rezerwacji DHCP):

```powershell
New-NetFirewallRule -DisplayName "igw HTTPS (wargame-compiler)" -Direction Inbound -Action Allow `
  -Protocol TCP -LocalPort 8443 -Profile Private -RemoteAddress <IP dev machine>[,<IP drugiego klienta>] `
  -Program "C:\igw\venv\Scripts\python.exe"
```

- **Nie otwieramy** portów runtime'u. `llama-server` słucha na `127.0.0.1`, więc nie potrzebuje reguły.
- **Nie** robimy przekierowań portów na routerze. Węzeł nie jest dostępny z internetu.
- Nazwa hosta:
  - preferowany jest DNS routera (rezerwacja DHCP z nazwą);
  - wariant awaryjny: wpis w `C:\Windows\System32\drivers\etc\hosts` na dev machine (`<IP> ai-node`), utrzymywany
    przez właściciela.

  Konfiguracja GLU zawsze używa `https://ai-node:8443`.

**Test łączności** (z dev machine, PowerShell):

```powershell
Resolve-DnsName ai-node
Test-NetConnection ai-node -Port 8443
curl.exe --cacert $HOME\.config\glu\ai-node.pem https://ai-node:8443/healthz
curl.exe --cacert $HOME\.config\glu\ai-node.pem -H "Authorization: Bearer $env:GLU_AI_NODE_TOKEN" https://ai-node:8443/v1/health
```

Docelowo wszystko to robi `glu doctor` ([NODE.md §10](NODE.md#diagnostyka)).

<a id="autostart"></a>
## 4. Autostart i odporność na restart
Cel: po restarcie PC węzeł wraca do stanu `healthy/ready` bez logowania i bez ręcznego uruchamiania terminali.

- **MVP: Harmonogram zadań**:
  - wyzwalacz „Przy uruchomieniu systemu”;
  - konto `svc-igw`, opcja „Uruchom niezależnie od tego, czy użytkownik jest zalogowany”;
  - akcja: `C:\igw\venv\Scripts\igw.exe serve --config %ProgramData%\igw\node.yaml`;
  - ustawienia „Uruchom ponownie w razie niepowodzenia” (co 1 min, 3 razy) i „Nie zatrzymuj zadania po czasie”.

  Rejestracja przez skrypt `deploy/node/install-task.ps1` (M-NODE).
- **Jeden punkt startu:** uruchamiamy tylko `igw`. Bramka sama uruchamia, nadzoruje i restartuje procesy
  `llama-server` (M-GW2). W M-GW1 jest jeden stały proces runtime'u uruchamiany przez bramkę.
- **Wariant:** usługa Windows przez wrapper (WinSW) dla pełnej semantyki usługi. Wybór i uzasadnienie w M-NODE.
- Do sprawdzenia w M-NODE: dostęp do CUDA z zadania uruchamianego bez zalogowanego użytkownika **(weryfikacja M-NODE)**.
- Rozgrzewka: profile `pinned` ładują się przy starcie, więc `/v1/health` zwraca `loading`, a potem `ok`.

<a id="wsl2"></a>
## 5. Kiedy WSL2 (tylko ścieżka vLLM, opcjonalna)
Dotyczy wyłącznie M-VLLM, po benchmarku (ADR-0018). Wymaga:
- WSL2 Ubuntu i bibliotek CUDA dla WSL (sterownik po stronie Windows);
- modeli w systemie plików ext4 WSL, nie na `/mnt/c`;
- limitu pamięci w `.wslconfig`;
- wyłączenia `vmIdleTimeout`;
- trybu sieci `mirrored` albo `netsh interface portproxy` z regułą Hyper-V firewall;
- zadania startowego, które uruchomi WSL po restarcie.

Bramka `igw` zostaje natywnie na Windows i rozmawia z vLLM po `127.0.0.1` jak z każdym runtime'em OpenAI-compatible.

<a id="troubleshooting"></a>
## 6. Diagnozowanie problemów
| Objaw (na dev machine) | Najczęstsza przyczyna | Sprawdzenie / naprawa |
|---|---|---|
| `Resolve-DnsName ai-node` zawodzi | brak wpisu DNS lub hosts, zmiana IP | rezerwacja DHCP, wpis DNS w routerze, `hosts` |
| `Test-NetConnection` timeout | węzeł wyłączony lub uśpiony, profil sieci Public, brak reguły, zły `RemoteAddress` | zasilanie i uśpienie, profil Private, `Get-NetFirewallRule -DisplayName "igw*"` |
| odmowa połączenia | `igw` nie działa albo słucha na innym interfejsie | Harmonogram zadań (historia), `netstat -ano \| findstr 8443` na węźle, logi `%ProgramData%\igw\logs\` |
| błąd TLS | zły `ca_file`, SAN bez `ai-node`, wygasły certyfikat | `curl.exe -v --cacert …`, wygenerowanie certyfikatu i ponowna dystrybucja `.pem` |
| 401/403 | zły token, zmienna nieustawiona, IP spoza allowlisty | `igw token list`, `client_allowlist` w `node.yaml` |
| 503 `model_loading` przez długi czas | duży model, odczyt z dysku, brak VRAM | `/v1/models` (`est_load_seconds`), `/v1/health` (VRAM), `igw doctor` |
| 503 `runtime_unavailable` | crash `llama-server` (OOM VRAM, zła ścieżka modelu) | logi bramki i runtime'u, `vram_mb` w `node.yaml` |
| 504 lub długie odpowiedzi | kolejka (`queue_depth`), profil `deep` w trybie interaktywnym, za mały deadline | `/v1/metrics`, `priority: batch`, `deadline_s` |
| GLU w `waiting_inference` | dowolne z powyższych | `glu doctor` wskazuje pierwszy nieudany krok |
