"""Freeze the accepted bounded eval-v1 and preserve its immutable parents.

Run once with "freeze" and a successful pre-freeze scripts/check root.
After final scripts/check, run "close" with that successful check root.
No source, historical response, Git ref or index is overwritten.
"""
from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
MAIN = Path(r"C:/dev/wargame-compiler")
P = ROOT / "private/poc/spqr-chapter9"
HERE = Path(__file__).resolve().parent
CANDIDATE = P / "evaluation/eval-v1-candidate-20261009-03"
EVAL = P / "evaluation/eval-v1"
PUBLIC = P / "evaluation/freeze-public-v1.json"
SCOPE = P / "evaluation/M-POC1C-review-007/decision-06-scope.json"
FREEZE = HERE / "decision-07-freeze.json"
HANDOFF = ROOT / "docs/handoff/2026-10-09-M-POC1C-freeze.md"
ALLOWED = {"docs/STATUS.md", "docs/ROADMAP.md", "docs/HANDOFF.md"}
DATA_KEYS = {"inventory.json": "items", "expectations.json": "expectations",
             "dependencies.json": "confirmed_execution_relations", "situations.json": "situations"}
NOW = datetime.now(timezone.utc).isoformat()

def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def ref(path):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest, "bytes": path.stat().st_size}

def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(value)

def save(path, value):
    write_new(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True,
                            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
    return result.stdout.decode("utf-8").strip()

def checked_run(directory):
    directory = directory.resolve()
    assert directory.is_relative_to((ROOT / "private/poc/_checks").resolve())
    result = load(directory / "result.json")
    assert result["tests_exit"] == result["diff_exit"] == 0
    log_bytes = (directory / "pytest.log").read_bytes()
    log = log_bytes.decode("utf-16" if log_bytes.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
    match = re.search(r"\b(\d+) passed\b", log)
    assert match, "Missing real passing test count"
    return {"passed": int(match.group(1)), "result": ref(directory / "result.json"),
            "log": ref(directory / "pytest.log"), "basetemp": result["basetemp"]}

def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()

def verify_item(item):
    assert ref(ROOT / item["path"]) == item, item["path"]

assert git(ROOT, "branch", "--show-current") == "feature/tests"
assert git(ROOT, "rev-parse", "HEAD") == "ae8f6f0433500933af4978b8f9ed50d828e6b5d0"
candidate_manifest = load(CANDIDATE / "manifest.json")
assert ref(CANDIDATE / "manifest.json")["sha256"] == "178b0e3ec40b43cbb4feef2ce35362b7376caf1dadb5052d211807c7f0f9ac8b"
for item in candidate_manifest["artifacts"] + candidate_manifest["provenance"] + [candidate_manifest["source"]]:
    verify_item(item)
assert load(SCOPE)["actual_owner_response"] == "zatwierdzam"
assert load(FREEZE)["actual_owner_response"] == "zatwierdzam"
assert load(FREEZE)["freeze_authorized"] is True
check = checked_run(ROOT / sys.argv[2])

if sys.argv[1] == "freeze":
    assert not EVAL.exists() and not PUBLIC.exists(), "Existing evaluation: verify, never overwrite"
    source_paths = set()
    for directory in ("docs", "scripts", "tests", "archive/legacy-2026-10-07", "private/poc/spqr-chapter9"):
        source_paths.update(path for path in (ROOT / directory).rglob("*") if path.is_file())
    source_paths.update(ROOT / name for name in ("README.md", "CLAUDE.md", ".gitignore", ".gitattributes", "pyproject.toml"))
    main_index = MAIN / ".git/index"
    with main_index.open("rb") as stream:
        main_index_sha = hashlib.file_digest(stream, "sha256").hexdigest()
    save(HERE / "baseline-before-freeze.json", {
        "recorded_at_utc": NOW, "files": [ref(path) for path in sorted(source_paths)],
        "allowed_public_updates": sorted(ALLOWED), "main_head": git(MAIN, "rev-parse", "HEAD"),
        "main_branch": git(MAIN, "branch", "--show-current"), "main_index_sha256": main_index_sha,
        "pre_freeze_checks": check,
    })
    write_new(HERE / "workspace-locator-before-freeze.raw.json",
              (MAIN / "private/poc/active-feature-workspace.json").read_text(encoding="utf-8"))
    EVAL.mkdir()
    maps = []
    for name in (*DATA_KEYS, "measurement-policy.json"):
        original = load(CANDIDATE / name)
        final = deepcopy(original)
        final.update({
            "evaluation_id": "eval-v1", "status": "frozen_owner_approved_bounded_scope",
            "frozen": True, "freeze_authorized": True, "scope_approved": True,
            "frozen_at_utc": NOW, "candidate_origin": ref(CANDIDATE / name),
            "owner_scope_decision": ref(SCOPE), "owner_freeze_decision": ref(FREEZE),
            "whole_record_gold": False,
            "gold_scope_policy": "Only the owner-reviewed bounded scopes under the approved measurement policy; unreviewed fields and unconfirmed candidates are excluded.",
        })
        if name == "measurement-policy.json":
            final["owner_approved"] = True
        else:
            final["gold"] = False  # No whole-record/all-field certification.
        changed = {key for key in final if key not in original or final[key] != original[key]}
        for key in original:
            if key not in changed:
                assert final[key] == original[key]
        if name in DATA_KEYS:
            assert canonical(final[DATA_KEYS[name]]) == canonical(original[DATA_KEYS[name]])
        save(EVAL / name, final)
        maps.append({
            "source": ref(CANDIDATE / name), "destination": ref(EVAL / name),
            "top_level_metadata_changed": sorted(changed),
            "original_nested_records_unchanged": True,
        })
    review = (
        "# eval-v1 — zamrożony ograniczony zestaw oceny\n\n"
        f"Zamrożono: {NOW}. Recenzent: właściciel tej rozmowy; tożsamość osobowa unknown.\n\n"
        "Rzeczywista decyzja 06 zatwierdziła zakres i politykę pomiaru; osobna decyzja 07\n"
        "zatwierdziła zamrożenie. Obie odpowiedzi „zatwierdzam” i pokazane pytania mają\n"
        "osobne, niezmienione zapisy. Jest to akceptacja dokładnych reviewed_scope,\n"
        "grupowania i rubryk, bez nadania gold nieprzejrzanym polom całych rekordów.\n\n"
        "Zakres: 66 grup lokalnej treści, 8 wymagań kontekstu; 20 sytuacji (17 wyników\n"
        "lokalnych i 3 uzasadnione blokady); 5 jawnych i 3 niejawne relacje wykonawcze.\n"
        "105 niepotwierdzonych propozycji nie jest gold ani pewnym FP.\n"
        "7 wzmianek i 7 kontynuacji oceniane są osobno. Inwentarz ma 207 rekordów.\n\n"
        "Pełne zatwierdzone rubryki, progi, limity i wyłączenia są w\n"
        "[measurement-policy.json](measurement-policy.json). Zero błędów krytycznych\n"
        "pozostaje nadrzędne wobec nominalnego progu 95%. Dotychczasowy aktywny czas\n"
        "jest unknown i nie potwierdza dostępnego budżetu. Zestaw nie certyfikuje\n"
        "całego grafu, całego rozdziału, wszystkich pól tabel ani wszystkich diagramów.\n\n"
        "Szczegółowe zaakceptowane granice i ograniczenia zachowuje niezmieniony\n"
        "[przegląd rodzica](../eval-v1-candidate-20261009-03/review.md).\n"
        "Jego historyczne oznaczenia waiting_review dotyczą stanu przed decyzjami 06/07.\n\n"
        "Pierwsza ekstrakcja nie została wykonana. Do jej czystej sesji przekazuje się\n"
        "wyłącznie pakiet wejściowy i freeze-public-v1.json z metadanymi bez odpowiedzi;\n"
        "niniejszy katalog, decyzje, oczekiwania i raporty pozostają poza pakietem.\n\n"
        "Zamrożonych plików nie nadpisujemy. Korekty zestawu przez erratę, decyzję\n"
        "właściciela i ewentualną nową wersję z mapą różnic.\n"
    )
    write_new(EVAL / "review.md", review)
    save(EVAL / "change-map.json", {
        "operation": "Freeze approved candidate-03 bounded scopes; only top-level lifecycle/provenance metadata changed.",
        "candidate_manifest": ref(CANDIDATE / "manifest.json"),
        "scope_decision": ref(SCOPE), "freeze_decision": ref(FREEZE), "files": maps,
        "review_document": {"source": ref(CANDIDATE / "review.md"),
                            "destination": ref(EVAL / "review.md"),
                            "operation": "New final review referencing the preserved approved scope review"},
        "original_artifacts_modified": [], "new_rules_relations_situations": [],
        "plan_thresholds_changed": False, "plan_limits_changed": False,
    })
    artifacts = [ref(path) for path in sorted(EVAL.iterdir()) if path.is_file()]
    manifest = {
        "id": "eval-v1", "card": "M-POC1C", "status": "frozen_owner_approved_bounded_scope",
        "frozen": True, "freeze_authorized": True, "scope_approved": True,
        "frozen_at_utc": NOW, "reviewer": "owner in this chat; personal identity unknown",
        "candidate_manifest": ref(CANDIDATE / "manifest.json"),
        "owner_scope_decision": ref(SCOPE), "owner_freeze_decision": ref(FREEZE),
        "source": candidate_manifest["source"], "artifacts": artifacts,
        "counts": candidate_manifest["counts"], "whole_record_gold": False,
        "gold_scope_policy": "Only approved reviewed_scope and exact confirmed relation tuples; no acceptance of unreviewed fields or unknown candidates.",
        "pre_freeze_checks": check, "plan_thresholds_changed": False, "plan_limits_changed": False,
        "quality_results": "n/a: first extraction not performed",
    }
    save(EVAL / "manifest.json", manifest)
    manifest_ref = ref(EVAL / "manifest.json")
    save(PUBLIC, {
        "evaluation_id": "eval-v1", "frozen": True, "frozen_at_utc": NOW,
        "scope_approved": True, "freeze_authorized": True,
        "manifest_sha256": manifest_ref["sha256"], "manifest_bytes": manifest_ref["bytes"],
        "artifact_hashes": {Path(item["path"]).name: item["sha256"] for item in artifacts},
        "source_sha256": candidate_manifest["source"]["sha256"],
        "owner_scope_decision_id": "M-POC1C-owner-decision-06",
        "owner_freeze_decision_id": "M-POC1C-owner-decision-07",
    })
    old_status = (ROOT / "docs/STATUS.md").read_text(encoding="utf-8")
    history = old_status[old_status.index("Poniżej zachowano przekazanie B"):]
    status = """# STATUS

- **Data aktualizacji:** 2026-10-09
- **Bieżący milestone:** M-POC2
- **Bieżąca karta:** M-POC2A
- **Wynik M-POC0:** done
- **Blokady:** brak dla M-POC2A; lokalny pakiet ekstrakcji jeszcze nieprzygotowany
- **Wynik M-POC1A:** done — przegląd struktury źródła zakończony w zapisanym zakresie
- **Wynik M-POC1B:** done — przygotowanie i przegląd oczekiwań oraz sytuacji zakończone
- **Wynik M-POC1C:** done — decyzje 06 o zakresie i 07 o freeze zapisane; eval-v1 zamrożone

Zamrożono eval-v1 z zatwierdzonego kandydata 03. Zakres i politykę pomiaru
zatwierdzono decyzją 06; osobna decyzja 07 zatwierdziła zamrożenie.
Nie powtarzać zakończonych przeglądów ani pytań o ten sam zakres/freeze.
Źródła, kandydaci, odpowiedzi, decyzje i historyczne handoffy pozostają zachowane.

Zamrożony zakres: 66 lokalnych grup treści, 8 wymagań kontekstu, 20 sytuacji
(17 wyników lokalnych / 3 blokady), 5 relacji jawnych i 3 niejawne.
105 pozostałych propozycji nie jest gold; 7 wzmianek i 7 kontynuacji osobno.
Progi i limity bez zmian; zero krytycznych błędów jest nadrzędne wobec 95%.
Dotychczasowy aktywny czas i dostępny budżet pozostają unknown.

Artefakty pod private/poc/spqr-chapter9/: evaluation/eval-v1/,
evaluation/freeze-public-v1.json i evaluation/M-POC1C-review-008/.
Prywatny manifest i completion prowadzą pełne SHA-256, decyzje i kontrole.
Metadane freeze nie zawierają treści oczekiwań ani odpowiedzi.

Kontrole przed zamrożeniem: scripts/check.ps1 — 94 passed, diff check poprawny.
Końcowe kontrole zapisuje completion sesji. Utworzono lokalną .venv w głównym
repo na zgodnym interpreterze z pytest; środowisko i narzędzia pozostają lokalne.
Praca jest w osobnej kopii feature/tests od ae8f6f0 wskazanej w locatorze;
główny HEAD/indeks pozostają zachowane. Brak commita/pusha tego zapisu.

Dokładny następny krok: M-POC2A — wejścia, minimalny format, prompt i transfer-list.
M-POC2A/B i pierwsza ekstrakcja niewykonane; wyniki jakości n/a.
Ekstraktor w M-POC2B dostaje wyłącznie odseparowany pakiet bez klucza oceny.
M-POC2 jest jedynym next. Docelowa architektura czeka na wynik M-POC7.

## Historia wcześniejszego przygotowania i przekazania

"""
    (ROOT / "docs/STATUS.md").write_text(status + history, encoding="utf-8", newline="\n")
    roadmap_path = ROOT / "docs/ROADMAP.md"
    roadmap = roadmap_path.read_text(encoding="utf-8")
    roadmap = re.sub(r"(?m)^\| M-POC1 \|.*$", "| M-POC1 | done | M-POC1A/B/C zakończone w zatwierdzonych zakresach; decyzje 06/07 i zamrożony eval-v1; 66 grup/8 wymagań kontekstu, 20 sytuacji (17/3), 5 relacji jawnych/3 niejawne; progi i limity bez zmian | [M-POC1A](work/tasks/M-POC1A.md), [M-POC1B](work/tasks/M-POC1B.md), [M-POC1C](work/tasks/M-POC1C.md) |", roadmap)
    roadmap = roadmap.replace("| M-POC2 | planned |", "| M-POC2 | next |")
    roadmap_path.write_text(roadmap, encoding="utf-8", newline="\n")
    handoff = f"""# M-POC1C — zamrożenie eval-v1

- **Milestone:** M-POC1
- **Karta:** M-POC1C
- **Wynik:** done
- **Następny milestone:** M-POC2
- **Następna karta:** M-POC2A

Data: 2026-10-09, Europe/Warsaw. Właściciel odpowiedział „zatwierdzam”
na osobne pytanie freeze. Decyzja 07 jest zapisana; wcześniejsza decyzja 06
zatwierdziła zakres/rubryki/wyłączenia/progi/limity. Nie pytać ponownie.

## Wynik

Pod private/poc/spqr-chapter9/: evaluation/eval-v1/ zawiera cztery pliki danych,
measurement-policy.json, review.md, change-map.json i manifest.json.
evaluation/freeze-public-v1.json zawiera tylko ID/hash/data/potwierdzenie freeze,
bez treści oczekiwań. Manifest eval-v1 SHA-256:
{manifest_ref["sha256"]}.

Zamrożenie: {NOW}, przed pierwszą ekstrakcją.
Zakres: 66 lokalnych grup treści, 8 wymagań kontekstu, 20 sytuacji (17/3),
5 relacji jawnych i 3 niejawne. 105 niepotwierdzonych propozycji poza gold;
7 wzmianek i 7 kontynuacji osobno. Globalnego certyfikatu grafu/pól nie nadano.
Progi i limity niezmienione; nieznany aktywny czas nie potwierdza budżetu.

## Kontrole i zachowanie danych

Kontrole przed freeze: scripts/check.ps1 — {check["passed"]} passed i git diff --check poprawny.
Końcowe kontrole, hashe, błędy środowiska i audyt zachowania poprzedników są
w evaluation/M-POC1C-review-008/ i measurement/M-POC1C-review-008/completion.json.
Źródłowy PDF i kandydaci zachowują bajty; zmieniono wyłącznie top-level metadane
cyklu życia w nowych kopiach, bez zmiany zagnieżdżonych rekordów.
M-POC1C done; M-POC2A/B i ekstrakcja niewykonane.

Właściciel zezwolił na lokalne .venv. Python i pytest są w głównym repo;
lokalne TMP/TEMP i nowy basetemp prowadzi scripts/check.ps1 uruchamiany z
-Python C:/dev/wargame-compiler/.venv/Scripts/python.exe.
Pierwsza próba na Pythonie 3.13 napotkała błąd dostępu do prywatnego basetemp;
zgodne lokalne środowisko 3.11.9 przechodzi niezmienione testy.
Poprzednie błędy/logi zachowano; nie dopisywano i nie osłabiano testów.

Kopia robocza jest od ae8f6f0 na feature/tests, jej ścieżka w
private/poc/active-feature-workspace.json głównego repo. Główny .git jest
chroniony; jego HEAD i indeks pozostają zachowane. Kopia wymaga obiektów
Git głównego repo. Nie ma commita/pusha tej sesji ani instalacji globalnej.

## Dokładne wznowienie

Odczytać bootstrap, bieżący STATUS/HANDOFF i kartę M-POC2A.
Sprawdzić hashe eval-v1 i freeze-public-v1; żadnego nadpisania.
Przygotować powtarzalny pakiet źródłowy, format, prompt i transfer-list.
Stabilny PDF jest już prywatnie w tym repo; historyczne ścieżki innego laptopa
nie są poleceniem modyfikowania drugiego repozytorium.
Czystą sesję M-POC2B otwiera ręcznie właściciel; nie przekazywać jej evaluation/,
oczekiwań, decyzji ani prywatnych handoffów oceny. Ta sesja zna klucz oceny.
"""
    write_new(HANDOFF, handoff)
    pointer = """# HANDOFF

- **Ostatnia sesja:** [2026-10-09-M-POC1C-freeze](handoff/2026-10-09-M-POC1C-freeze.md)
- **Wynik:** done
- **Następny milestone:** M-POC2
- **Następna karta:** M-POC2A

M-POC1C zakończono po rzeczywistych decyzjach 06 (zakres) i 07 (freeze).
eval-v1 jest zamrożone; freeze-public-v1 zawiera wyłącznie metadane.
Nie powtarzać pytań o akceptację tego samego pakietu.

Prywatny korzeń private/poc/spqr-chapter9/: evaluation/eval-v1/,
evaluation/freeze-public-v1.json i evaluation/M-POC1C-review-008/.
Pełne hashe, kontrole i audyt zachowania rodziców prowadzi completion.

Następny krok to M-POC2A: pakiet wejść, format, prompt i transfer-list.
M-POC2A/B oraz ekstrakcja niewykonane; wyniki jakości n/a.
M-POC2 jedyny next. Ekstraktor później dostaje pakiet bez klucza oceny.

Zapis lokalny w kopii feature/tests od ae8f6f0; główny HEAD/indeks zachowane,
bez commita/pusha. Lokalna .venv z pytest jest dostępna w głównym repo;
lokalizację kopii roboczej prowadzi prywatny locator.

[STATUS](STATUS.md), [ROADMAP](ROADMAP.md), [plan](POC-PLAN.md).
"""
    (ROOT / "docs/HANDOFF.md").write_text(pointer, encoding="utf-8", newline="\n")
    print(json.dumps({"frozen": True, "manifest": manifest_ref, "next_card": "M-POC2A"}, indent=2))

elif sys.argv[1] == "close":
    baseline = load(HERE / "baseline-before-freeze.json")
    unchanged, updates = 0, []
    for item in baseline["files"]:
        after = ref(ROOT / item["path"])
        if after == item:
            unchanged += 1
        else:
            assert item["path"] in ALLOWED, item["path"]
            updates.append({"before": item, "after": after})
    assert len(updates) == 3
    assert git(MAIN, "rev-parse", "HEAD") == baseline["main_head"]
    assert git(MAIN, "branch", "--show-current") == baseline["main_branch"]
    with (MAIN / ".git/index").open("rb") as stream:
        assert hashlib.file_digest(stream, "sha256").hexdigest() == baseline["main_index_sha256"]
    frozen = load(EVAL / "manifest.json")
    for item in frozen["artifacts"]:
        verify_item(item)
    for name, key in DATA_KEYS.items():
        assert canonical(load(EVAL / name)[key]) == canonical(load(CANDIDATE / name)[key])
    deps = load(EVAL / "dependencies.json")
    for key in ("mentions", "continuations", "unconfirmed_execution_candidates"):
        assert canonical(deps[key]) == canonical(load(CANDIDATE / "dependencies.json")[key])
    policy = load(EVAL / "measurement-policy.json")
    original_policy = load(CANDIDATE / "measurement-policy.json")
    for key in ("categories", "relations", "situations", "criticality", "thresholds", "limits"):
        assert canonical(policy[key]) == canonical(original_policy[key])
    public = load(PUBLIC)
    assert public["manifest_sha256"] == ref(EVAL / "manifest.json")["sha256"]
    assert set(public) == {"evaluation_id", "frozen", "frozen_at_utc", "scope_approved",
                          "freeze_authorized", "manifest_sha256", "manifest_bytes",
                          "artifact_hashes", "source_sha256",
                          "owner_scope_decision_id", "owner_freeze_decision_id"}
    assert all(Path(path).name == path for path in public["artifact_hashes"])
    assert not (P / "runs/first-001").exists()
    validation = {
        "recorded_at_utc": NOW, "status": "passed",
        "candidate_manifest_references_verified": 22,
        "frozen_artifact_hashes_verified": len(frozen["artifacts"]),
        "nested_data_and_approved_policy_unchanged": True,
        "public_freeze_metadata_allowlist_verified": True,
        "preserved_files_checked": len(baseline["files"]),
        "unchanged_files": unchanged, "intentional_public_updates": updates,
        "main_HEAD_branch_index_preserved": True, "post_freeze_checks": check,
        "semantic_extraction_run": False,
    }
    save(HERE / "validation-after-freeze.json", validation)
    completion = {
        "id": "M-POC1C-review-008-after-freeze", "recorded_at_utc": NOW, "date": "2026-10-09",
        "card": "M-POC1C", "outcome": "done", "workflow_status": "done",
        "milestone": "M-POC1", "next_milestone": "M-POC2", "next_card": "M-POC2A",
        "branch": "feature/tests", "head": git(ROOT, "rev-parse", "HEAD"),
        "working_copy": str(ROOT), "original_checkout": str(MAIN),
        "scope_decision": ref(SCOPE), "freeze_decision": ref(FREEZE),
        "frozen_manifest": ref(EVAL / "manifest.json"), "public_freeze_metadata": ref(PUBLIC),
        "candidate_manifest": ref(CANDIDATE / "manifest.json"),
        "pre_freeze_checks": baseline["pre_freeze_checks"], "post_freeze_checks": check,
        "validation": ref(HERE / "validation-after-freeze.json"),
        "local_environment": {
            "python": str(MAIN / ".venv/Scripts/python.exe"), "version": sys.version.split()[0],
            "pytest": "8.4.2", "global_installation": False,
            "installation": "Project virtualenv; verified wheel contents installed locally for python -m pytest",
            "prior_python313_temp_permission_failure_preserved": True,
        },
        "preservation": {"checked": len(baseline["files"]), "unchanged": unchanged,
                         "intentional_public_updates": 3, "main_HEAD_branch_index_unchanged": True},
        "measurement": {"user_active_time": "unknown", "model_active_time": "unknown",
                        "tokens": "unknown", "cost": "unknown", "calendar_time_is_active": False},
        "freeze_authorized": True, "frozen": True, "semantic_extraction_run": False,
        "plan_thresholds_changed": False, "plan_limits_changed": False,
        "git_commit_or_push": False, "remaining_owner_freeze_gate": None,
    }
    save(HERE / "completion-after-freeze.json", completion)
    measure = P / "measurement/M-POC1C-review-008/completion.json"
    save(measure, completion)
    save(HERE / "review-manifest-after-freeze.json", {
        "recorded_at_utc": NOW,
        "files": [ref(path) for path in sorted(HERE.iterdir()) if path.is_file()],
        "frozen_manifest": ref(EVAL / "manifest.json"), "public_freeze_metadata": ref(PUBLIC),
        "public_documents": [ref(ROOT / path) for path in sorted(ALLOWED)] + [ref(HANDOFF)],
        "measurement_completion": ref(measure),
    })
    save(HERE / "closure-seal-after-freeze.json", {
        "recorded_at_utc": NOW, "review_manifest": ref(HERE / "review-manifest-after-freeze.json"),
        "completion": ref(HERE / "completion-after-freeze.json"),
        "measurement_completion": ref(measure), "frozen_manifest": ref(EVAL / "manifest.json"),
        "public_freeze_metadata": ref(PUBLIC),
        "public_documents": [ref(ROOT / path) for path in sorted(ALLOWED)] + [ref(HANDOFF)],
        "status": "done", "next_card": "M-POC2A",
    })
    locator_path = MAIN / "private/poc/active-feature-workspace.json"
    locator = load(locator_path)
    locator.update({
        "recorded_at_utc": NOW, "latest_handoff": str(HANDOFF),
        "freeze_decision": str(FREEZE), "frozen_manifest": str(EVAL / "manifest.json"),
        "manifest_sha256": ref(EVAL / "manifest.json")["sha256"],
        "next_question": None, "next_milestone": "M-POC2", "next_card": "M-POC2A",
        "required_tests": f"passed: {check['passed']} tests",
        "venv_python": str(MAIN / ".venv/Scripts/python.exe"),
    })
    locator_path.write_text(json.dumps(locator, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"done": True, "tests_passed": check["passed"],
                      "preserved_files": unchanged, "manifest": ref(EVAL / "manifest.json"),
                      "next_card": "M-POC2A"}, indent=2))
else:
    raise ValueError("Expected freeze or close")
