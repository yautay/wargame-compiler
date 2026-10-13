"""Prepare, stage and verify the explicitly authorized feature/tests checkpoint."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
MAIN = Path(r"C:/dev/wargame-compiler")
P = ROOT / "private/poc/spqr-chapter9"
HERE = Path(__file__).resolve().parent
ALLOWED = {"docs/STATUS.md", "docs/HANDOFF.md", "docs/ROADMAP.md"}
HANDOFF = ROOT / "docs/handoff/2026-10-09-M-POC1C-publish.md"
NOW = datetime.now(timezone.utc).isoformat()
PARENT = "ae8f6f0433500933af4978b8f9ed50d828e6b5d0"

def git(*args):
    result = subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True,
                            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
    return result.stdout.decode("utf-8").strip()

def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def ref(path):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": digest, "bytes": path.stat().st_size}

def verify(item):
    assert ref(ROOT / item["path"]) == item, item["path"]

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def nested_refs(value):
    if isinstance(value, dict):
        if {"path", "sha256", "bytes"} <= value.keys():
            yield value
        for child in value.values():
            yield from nested_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from nested_refs(child)

assert git("branch", "--show-current") == "feature/tests"
assert git("rev-parse", "HEAD") == PARENT
assert not git("diff", "--cached", "--name-only"), "Existing staged changes"

if sys.argv[1] == "prepare":
    if not (HERE / "baseline.json").exists():
        frozen_manifest = P / "evaluation/eval-v1/manifest.json"
        assert ref(frozen_manifest)["sha256"] == "7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce"
        frozen = load(frozen_manifest)
        for item in frozen["artifacts"]:
            verify(item)
        seal = load(P / "evaluation/M-POC1C-review-008/closure-seal-after-freeze.json")
        for key in ("review_manifest", "completion", "measurement_completion", "frozen_manifest", "public_freeze_metadata"):
            verify(seal[key])
        for item in seal["public_documents"]:
            verify(item)

        with (HERE / "owner-publication-authorization.raw.txt").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write("commit + push\n")
        selected = set()
        for directory in (
            "evaluation/M-POC1C-review-007", "evaluation/M-POC1C-review-008",
            "evaluation/eval-v1", "measurement/M-POC1C-review-007",
            "measurement/M-POC1C-review-008",
        ):
            selected.update(path for path in (P / directory).rglob("*") if path.is_file())
        selected.add(P / "evaluation/freeze-public-v1.json")
        save(HERE / "baseline.json", {
            "recorded_at_utc": NOW, "branch": "feature/tests", "parent_head": PARENT,
            "files": [ref(path) for path in sorted(selected)],
            "public_documents_before": [ref(ROOT / name) for name in sorted(ALLOWED)],
            "allowed_public_updates": sorted(ALLOWED),
            "owner_authorization": ref(HERE / "owner-publication-authorization.raw.txt"),
            "main_head": subprocess.run(["git", "-C", str(MAIN), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip(),
            "main_index_sha256": hashlib.sha256((MAIN / ".git/index").read_bytes()).hexdigest(),
        })
        snapshots = []
        for name in sorted(ALLOWED):
            source = ROOT / name
            destination = HERE / "pre-publication-public-documents" / Path(name).name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as stream:
                stream.write(source.read_bytes())
            snapshots.append({"historical_public_reference": ref(source), "preserved_snapshot": ref(destination)})
        save(HERE / "public-document-snapshot-map.json", {
            "reason": "Retain exact pre-publication pointer bytes referenced by the completed freeze seal.",
            "files": snapshots,
        })

        status_path = ROOT / "docs/STATUS.md"
        status = status_path.read_text(encoding="utf-8")
        old = "główny HEAD/indeks pozostają zachowane. Brak commita/pusha tego zapisu."
        new = ("główny HEAD/indeks pozostają zachowane. Właściciel zlecił commit i push\n"
               "checkpointu na origin/feature/tests. Zakres i dowody publikacji prowadzi\n"
               "evaluation/M-POC1C-publication-20261009-01/; środowisko pozostaje lokalne.")
        assert old in status
        status_path.write_text(status.replace(old, new), encoding="utf-8", newline="\n")

        pointer = """# HANDOFF

    - **Ostatnia sesja:** [2026-10-09-M-POC1C-publish](handoff/2026-10-09-M-POC1C-publish.md)
    - **Wynik:** done
    - **Następny milestone:** M-POC2
    - **Następna karta:** M-POC2A

    M-POC1C zakończono po rzeczywistych decyzjach 06 (zakres) i 07 (freeze).
    eval-v1 jest zamrożone; freeze-public-v1 zawiera wyłącznie metadane.
    Nie powtarzać pytań o akceptację tego samego pakietu.

    Właściciel zlecił commit i push checkpointu na origin/feature/tests.
    Zakres publikacji i zgoda są w evaluation/M-POC1C-publication-20261009-01/
    pod private/poc/spqr-chapter9/. Obejmuje zamrożone dane, decyzje 06/07,
    raporty, hashe i potrzebne logi; .venv, instalatory i basetemp są lokalne.
    Dokładne SHA nowego commita i wynik remote są wynikiem operacji Git,
    nie polem wpisywanym do tego samego commita.

    Prywatne dane: evaluation/eval-v1/, evaluation/freeze-public-v1.json,
    evaluation/M-POC1C-review-007/ i 008/ oraz oba rejestry measurement.
    Źródła i wcześniejsze artefakty zachowano; pełne hashe prowadzą manifesty.

    Następny krok to M-POC2A: pakiet wejść, format, prompt i transfer-list.
    M-POC2A/B i ekstrakcja niewykonane; wyniki jakości n/a. M-POC2 jedyny next.
    Ekstraktor później dostaje odseparowany pakiet bez klucza oceny.

    Na tym laptopie kopię roboczą prowadzi prywatny locator głównego repo.
    W nowym klonie pracować bezpośrednio na feature/tests; historyczne lokalne
    ścieżki i informacje o master/shared objects są snapshotami poprzedniej maszyny.
    Nie kopiować środowiska. Istniejący lokalny Python z pytest jest wystarczający.

    [STATUS](STATUS.md), [ROADMAP](ROADMAP.md), [plan](POC-PLAN.md).
    """
        (ROOT / "docs/HANDOFF.md").write_text(pointer, encoding="utf-8", newline="\n")
        handoff = """# M-POC1C — checkpoint publikacyjny

    - **Milestone:** M-POC1
    - **Karta:** M-POC1C
    - **Wynik:** done
    - **Następny milestone:** M-POC2
    - **Następna karta:** M-POC2A

    Data: 2026-10-09, Europe/Warsaw. Właściciel jawnie polecił „commit + push”.
    Zgoda obejmuje zapis ukończonego M-POC1C na origin/feature/tests i potrzebnych
    prywatnych artefaktów; nie zmienia zakresu oceny, limitów ani zamrożonych bajtów.

    ## Stan i konkretne artefakty

    eval-v1 jest zamrożone po decyzjach 06 o zakresie i 07 o freeze.
    Manifest SHA-256:
    7debb9edffd9e0256a0065be335a743ce796660c67d5c6cdcfdddf433d3e8dce.
    Zakres: 66 grup lokalnej treści, 8 wymagań kontekstu, 20 sytuacji (17/3),
    5 jawnych i 3 niejawne relacje. 105 niepotwierdzonych propozycji pozostaje
    poza gold; 7 wzmianek i 7 kontynuacji osobno. Progi i limity niezmienione.

    Pod private/poc/spqr-chapter9/ publikowany checkpoint obejmuje:
    evaluation/M-POC1C-review-007/, evaluation/M-POC1C-review-008/,
    evaluation/eval-v1/, evaluation/freeze-public-v1.json, oba odpowiadające
    measurement/M-POC1C-review-007/ i 008/, oraz nowy
    evaluation/M-POC1C-publication-20261009-01/. W nim są zgoda, zakres publikacji,
    hashe, kontrole i kopie poprzednich wskaźników dokumentacji.
    Publikowane logi obejmują wyłącznie wskazane pliki, nie całe basetemp.

    Faktyczny zakres i hashe prowadzi publication-inventory.json. Nie zmieniono
    ignorowania /private/; staging jest jawną listą plików. Atrybuty -text
    zachowują surowe bajty prywatnych danych. Zamrożonych danych, oryginalnych
    odpowiedzi, manifestów i wcześniejszych handoffów nie nadpisywano.
    Dokładny SHA nowego commita ustala Git; nie wpisujemy go do niego samego.

    ## Kontrole i środowisko

    Zamknięcie freeze miało 95 passed oraz poprawne hashe i git diff --check.
    Checkpoint publikacji dodaje handoff; faktyczny nowy wynik scripts/check.ps1
    jest w osobnym completion wraz z hashem manifestu i audytem staged blobów.
    Testów i runtime legacy nie zmieniono ani nie importowano.

    .venv i pobrane narzędzia są lokalne, poza publikacją. Do kontroli wskazać
    istniejący Python z pytest przez -Python; TMP/TEMP lokalne i nowy basetemp.
    Historyczne ścieżki, HEAD/indeksy i locator sprzed publikacji są snapshotami;
    nie używać ich do przywracania Git ani uruchamiać historycznych record/close.

    ## Wznowienie nowej sesji

    Na bieżącym laptopie odczytać private/poc/active-feature-workspace.json
    głównego repo i użyć wskazanej kopii roboczej feature/tests.
    W świeżym klonie użyć feature/tests bezpośrednio i sprawdzić aktualny remote.

    Przeczytać CLAUDE, SESSION-PLAYBOOK, STATUS, HANDOFF i ten handoff, ROADMAP,
    POC-PLAN oraz kartę M-POC2A. Zweryfikować hashe eval-v1 i freeze-public-v1
    bez nadpisania. Nie powtarzać pytań o zakres/freeze — zgody już zapisane.

    Wykonać wyłącznie M-POC2A: wejścia, minimalny format, prompt i transfer-list.
    Stabilny PDF jest prywatnie w tym repo; oddzielić core i kontekst zgodnie
    ze source-v1 i supplementem lokalizacji. Zamrożonych odpowiedzi nie włączać
    do pakietu. Zakończyć kartę kontrolami i aktualizacją stanu/handoffu.

    M-POC2B jest kolejną osobną czystą sesją, ręcznie otwieraną przez właściciela,
    z wyłącznie odseparowanym pakietem. Nie przekazywać jej evaluation/,
    odpowiedzi wzorcowych, decyzji ani prywatnych handoffów oceny.
    M-POC2A/B i ekstrakcja jeszcze niewykonane; M-POC2 jedyny next.
    """
        with HANDOFF.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(handoff)

    else:
        baseline = load(HERE / "baseline.json")
        for item in baseline["files"]:
            verify(item)
        assert HANDOFF.is_file()
        selected = set()
        for directory in (
            "evaluation/M-POC1C-review-007", "evaluation/M-POC1C-review-008",
            "evaluation/eval-v1", "measurement/M-POC1C-review-007",
            "measurement/M-POC1C-review-008",
        ):
            selected.update(path for path in (P / directory).rglob("*") if path.is_file())
        selected.add(P / "evaluation/freeze-public-v1.json")
    selected.update({
        HANDOFF,
        ROOT / "docs/handoff/2026-10-09-M-POC1C-freeze.md",
        ROOT / "docs/handoff/2026-10-09-M-POC1C-review-007.md",
    })
    selected.update(path for path in HERE.rglob("*") if path.is_file())
    for relative in (
        "private/poc/_checks/active-38734ac2bf6b4cc789bb1668cfca891d/pytest.log",
        "private/poc/_checks/diagnostic-22420179c26a49149d8b5b0f63f11cc1/pytest.log",
    ):
        path = ROOT / relative
        if path.is_file():
            selected.add(path)
    tracked = set(git("ls-files").splitlines())
    queue = list(selected)
    seen = set()
    logs = set()
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        seen.add(path)
        if path.suffix != ".json":
            continue
        for item in nested_refs(load(path)):
            relative = item["path"]
            if relative in tracked or ROOT / relative in selected:
                continue
            target = ROOT / relative
            if relative.startswith("private/poc/_checks/") and target.is_file() and target.name in {"pytest.log", "result.json", "diff-check.log"}:
                verify(item)
                selected.add(target)
                logs.add(target)
                queue.append(target)
            else:
                raise AssertionError(f"Unpublished referenced artifact: {relative}")
    save(HERE / "publication-inventory.json", {
        "recorded_at_utc": NOW, "parent_head": PARENT, "branch": "feature/tests",
        "remote": "origin", "remote_url": "git@github.com:yautay/wargame-compiler.git",
        "owner_authorization": ref(HERE / "owner-publication-authorization.raw.txt"),
        "files": [ref(path) for path in sorted(selected)],
        "referenced_check_logs": [ref(path) for path in sorted(logs)],
        "public_documents": [ref(ROOT / name) for name in sorted(ALLOWED)] + [ref(HANDOFF), ref(ROOT / "docs/handoff/2026-10-09-M-POC1C-freeze.md"), ref(ROOT / "docs/handoff/2026-10-09-M-POC1C-review-007.md")],
        "staging": "Explicit individual paths with git add -f; no ignore policy change",
        "excluded": [".venv", "tool downloads", "runtime bases", "basetemp contents", "original checkout Git metadata", "credentials"],
        "normal_push_only": True, "frozen_data_changed": False,
        "repo_author_identity_source": "Most recent five commits use the same author identity; reuse it only as command-scoped Git identity.",
    })
    print(json.dumps({"scope_files": len(selected) + 1, "referenced_check_logs": len(logs)}, indent=2))

elif sys.argv[1] == "finish":
    directory = (ROOT / sys.argv[2]).resolve()
    result = load(directory / "result.json")
    assert result["tests_exit"] == result["diff_exit"] == 0
    log_bytes = (directory / "pytest.log").read_bytes()
    log = log_bytes.decode("utf-16" if log_bytes.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig")
    match = re.search(r"\b(\d+) passed\b", log)
    assert match
    baseline = load(HERE / "baseline.json")
    for item in baseline["files"]:
        verify(item)
    original = subprocess.run(["git", "-C", str(MAIN), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    assert original == baseline["main_head"]
    assert hashlib.sha256((MAIN / ".git/index").read_bytes()).hexdigest() == baseline["main_index_sha256"]
    save(HERE / "completion-before-publication.json", {
        "recorded_at_utc": NOW, "owner_authorization": ref(HERE / "owner-publication-authorization.raw.txt"),
        "publication_inventory": ref(HERE / "publication-inventory.json"),
        "tests_passed": int(match.group(1)), "checks_result": ref(directory / "result.json"),
        "checks_log": ref(directory / "pytest.log"),
        "protected_private_artifacts": len(baseline["files"]), "private_artifacts_unchanged": True,
        "original_HEAD_index_preserved": True, "frozen_manifest_unchanged": True,
        "commit_push_status": "prepared_and_authorized; final SHA and remote equality are post-commit results",
    })
    paths = {ROOT / item["path"] for item in load(HERE / "publication-inventory.json")["files"]}
    paths.update(path for path in HERE.rglob("*") if path.is_file())
    paths.update(ROOT / item["path"] for item in load(HERE / "publication-inventory.json")["public_documents"])
    paths.update({directory / "result.json", directory / "pytest.log"})
    save(HERE / "staging-manifest.json", {
        "recorded_at_utc": NOW, "files": [ref(path) for path in sorted(paths)],
        "intended_branch": "feature/tests", "parent_head": PARENT,
        "frozen_manifest": ref(P / "evaluation/eval-v1/manifest.json"),
    })
    paths.add(HERE / "staging-manifest.json")
    pathfile = HERE / "staging-paths.txt"
    with pathfile.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write("\n".join(path.relative_to(ROOT).as_posix() for path in sorted(paths | {pathfile})) + "\n")
    git("add", "-f", "--pathspec-from-file=" + str(pathfile))
    staged = set(git("diff", "--cached", "--name-only").splitlines())
    assert staged == {path.relative_to(ROOT).as_posix() for path in paths | {pathfile}}, "Unexpected staged paths"
    git("diff", "--cached", "--check")
    for path in paths | {pathfile}:
        content = subprocess.run(["git", "-C", str(ROOT), "show", ":" + path.relative_to(ROOT).as_posix()],
                                 check=True, capture_output=True).stdout
        assert content == path.read_bytes(), path
    print(json.dumps({"staged_files": len(staged), "tests_passed": int(match.group(1)),
                      "byte_exact_staged_artifacts": True}, indent=2))
else:
    raise ValueError("Expected prepare or finish")
