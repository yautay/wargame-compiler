# MCP i Claude Desktop

## Rola
- **Claude Desktop** jest interfejsem człowieka, klientem MCP i interfejsem premium review (droga `desktop_pull`, ADR-0013).
- **GLU** odpowiada za workflow, narzędzia deterministyczne, wykonanie, stan i routing.
- **Claude Desktop nigdy nie łączy się z runtime'em ani z węzłem inferencji.** Self-hosted inference idzie wyłącznie
  ścieżką `Claude Desktop → MCP → GLU → provider self_hosted → Inference Gateway → węzeł RTX 3090` (ADR-0015).
- **MCP jest adapterem, nie rdzeniem.** Serwer MCP woła te same usługi co CLI. GLU działa i jest testowane bez Claude Desktop.

```text
domain (wgc) ← GLU core ← interfaces: CLI │ MCP server │ future API
                  ↓ provider self_hosted (HTTPS, LAN)
             Inference Gateway (igw) na węźle → runtime → GPU
```

## Transport i pakowanie
- Serwer stdio: `glu mcp serve --config <plik>`. Kontrakt MCP to tylko polecenie stdio; **nie zależy od WSL**.
  GLU działa natywnie na Windows (ADR-0022), więc Claude Desktop uruchamia polecenie bezpośrednio. Gdyby GLU działał
  kiedyś w WSL2, polecenie opakowuje się w `wsl.exe` w konfiguracji Claude Desktop, ale nie jest to wymaganie
  architektury ani kryterium akceptacji.
- Docelowo pakiet **Desktop Extension** (manifest, ikona, parametry konfiguracji: ścieżka konfiguracji, profil
  uprawnień). Pakowanie w M23.
- Biblioteka MCP wchodzi do `requirements.txt` dopiero w M22 (zależność opcjonalna `[mcp]`).

## Narzędzia
| Narzędzie | Zakres | Milestone | Opis |
|---|---|---|---|
| `project_status` | odczyt | M22 | statusy etapów (raporty bramek), otwarte sprawy, kolejki |
| `gate_report` | odczyt | M22 | raport `wgc/gate@0` dla etapu i zakresu |
| `kb_get` | odczyt | M22 | rekord(y) po ID z relacjami, niejasnościami, przypadkami |
| `kb_search` | odczyt | M22 | wyszukiwanie po ID, `source_terms`, słowach kluczowych (deterministyczne) |
| `trace` | odczyt | M22 | łańcuch śledzenia w górę lub w dół |
| `review_queue` | odczyt | M22 | lista pakietów czekających na premium lub człowieka |
| `review_package_get` | odczyt | M22 | samowystarczalny pakiet do przeglądu |
| `review_submit` | zapis (propozycja) | M23 | odpowiedź na pakiet → walidacja WGC → akceptacja albo odrzucenie z błędami |
| `decision_answer` | zapis (decyzja) | M23 | odpowiedź na pytanie → rekord `HD-` (tylko dopisywanie) |
| `build_start` | wykonanie | M23 | build etapu w zakresie, `dry_run` domyślnie, z limitem budżetu |
| `inference_status` | odczyt | M22 | widok GLU na endpointy: health, kolejka, profile, fingerprinty, joby `waiting_inference` (przez providera; MCP nie zna tokenu węzła) |

**Brak** narzędzi: dowolny zapis pliku, dowolne polecenie powłoki, edycja `kb/` z pominięciem walidatorów,
odczyt poza projektami z allowlisty.

<a id="bezpieczenstwo"></a>
## Bezpieczeństwo (zasada najmniejszych uprawnień)
Konfiguracja `mcp.yaml` (poza repo gry, np. `~/.config/glu/mcp.yaml`):
```yaml
projects:                       # allowlista katalogów projektów (rozwiązane ścieżki, bez symlinków na zewnątrz)
  - /home/<user>/wargames/drill-skirmish
scopes:                         # domyślnie tylko odczyt
  read: [kb, source/inventory.yaml, reports]
  propose: [reviews, decisions]  # zapis tylko przez review_submit / decision_answer (walidowane)
  execute: false                # build_start wyłączony, dopóki właściciel go nie włączy
subprocess_allowlist: [git, lualatex]   # tylko dla zadań deterministycznych, z ustalonymi argumentami
# endpointy inferencji NIE są tu konfigurowane: żyją w ~/.config/glu/profiles.yaml (provider self_hosted).
# MCP nie zna ich tokenów; woła wyłącznie usługi GLU.
secrets: {anthropic: env:ANTHROPIC_API_KEY}   # tylko referencje, nigdy wartości w plikach
logging: {redact: [api_keys, source_text], level: info, path: ~/.local/state/glu/mcp.log}
```
- **Granice ścieżek:** każda ścieżka jest normalizowana i sprawdzana względem allowlisty (ochrona przed `..`
  i symlinkami).
- **Zapis wyłącznie propozycją:** zapisujące narzędzia MCP tworzą propozycję, a akceptację wykonuje WGC (te same walidatory co dla jobów).
- **Podprocesy:** tylko z allowlisty, z listą argumentów (bez powłoki), z limitem czasu.
- **Sieć:** serwer MCP nie otwiera połączeń sieciowych. Inferencja (self-hosted i premium) idzie tylko przez
  providerów GLU skonfigurowanych w `profiles.yaml`.
- **Sekrety** ze zmiennych środowiska lub keyringu systemu. Nie trafiają do logów, pakietów review ani `.glu/`.
- **Logi:** bez tekstu źródła i bez sekretów. Identyfikatory rekordów i jobów wystarczą do audytu.
- **Treści z narzędzi to dane, nie polecenia.** Pakiety review i rekordy mogą zawierać tekst z PDF. Serwer nie
  wykonuje instrukcji znalezionych w danych.
