"""M8: `glu status` and `glu export` (glu.__main__) and the `glu` console script."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

from glu.__main__ import main
from glu.store import SCHEMA_VERSION, Store, db_path
from wgc import contracts
from wgc.validate import validate

from test_glu_store import CACHE_KEY, Clock, Ids

ROOT = Path(__file__).resolve().parent.parent


def seed(root: Path) -> tuple[str, str]:
    with Store.at_root(root, clock=Clock(), new_id=Ids()) as s:
        build = s.create_build("bench-minigame", "stage1", scope="chapter:3")
        s.transition_build(build, "running")
        first = s.create_job(build, "logic.rule.extract", ["SEG-mg.3.1"], CACHE_KEY, tier="local")
        s.create_job(build, "logic.rule.extract", ["SEG-mg.3.2"], CACHE_KEY, tier="local")
        s.transition_job(first, "ready")
        s.add_routing_decision(first, "routing@0", "local", {"risk_class": "low"}, ["low risk"])
        s.transition_job(first, "running")
        s.add_attempt(first, "local", "unavailable", error_class="network", endpoint="ai-node")
        s.transition_job(first, "waiting_inference")
        s.transition_build(build, "waiting_inference")
        other = s.create_build("bench-minigame", "stage0")
    return build, other


def test_status_without_database_is_operational_error(tmp_path, capsys):
    assert main(["status", "--root", str(tmp_path)]) == 2
    err = capsys.readouterr().err
    assert "BŁĄD: brak bazy stanu GLU" in err
    assert not (tmp_path / ".glu").exists()


def test_status_of_empty_store(tmp_path, capsys):
    Store.at_root(tmp_path).close()
    assert main(["status", "--root", str(tmp_path)]) == 0
    assert "Brak buildów" in capsys.readouterr().out


def test_status_lists_builds_and_job_counts(tmp_path, capsys):
    build, other = seed(tmp_path)
    assert main(["status", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert f"{build}  bench-minigame  stage1 chapter:3  stan: waiting_inference" in out
    assert "joby: 2 (pending 1, waiting_inference 1)" in out
    assert f"{other}  bench-minigame  stage0  stan: planning" in out
    assert "joby: 0\n" in out


def test_status_of_one_build_as_json(tmp_path, capsys):
    build, _ = seed(tmp_path)
    assert main(["status", "--root", str(tmp_path), "--build", build, "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert [b["id"] for b in data["builds"]] == [build]
    jobs = data["builds"][0]["job_list"]
    assert [(j["state"], j["attempts"]) for j in jobs] == [("waiting_inference", 1), ("pending", 0)]
    assert data["builds"][0]["jobs"] == {"pending": 1, "waiting_inference": 1}


def test_status_unknown_build_and_broken_database(tmp_path, capsys):
    seed(tmp_path)
    assert main(["status", "--root", str(tmp_path), "--build", "build_999999"]) == 2
    assert "nie ma buildu build_999999" in capsys.readouterr().err
    import sqlite3
    conn = sqlite3.connect(db_path(tmp_path))
    conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION + 1}")
    conn.close()
    assert main(["status", "--root", str(tmp_path)]) == 2
    assert "zaktualizuj narzędzie" in capsys.readouterr().err
    db_path(tmp_path).write_bytes(b"garbage" * 100)
    assert main(["status", "--root", str(tmp_path)]) == 2
    assert "nie jest poprawną bazą stanu GLU" in capsys.readouterr().err


def test_export_to_file_passes_wgc_validate(tmp_path, capsys):
    build, _ = seed(tmp_path)
    out = tmp_path / "reports" / "exec.yaml"
    out.parent.mkdir()
    assert main(["export", "--root", str(tmp_path), "--out", str(out)]) == 0
    assert "Zapisano 6 rekordów glu/exec@0" in capsys.readouterr().out
    doc = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert doc["schema"] == "glu/exec@0" and contracts.errors(doc) == []
    report = validate([out])
    assert report.ok and not report.diagnostics
    assert b"\r\n" not in out.read_bytes()


def test_export_one_build_to_stdout(tmp_path, capsys):
    build, other = seed(tmp_path)
    assert main(["export", "--root", str(tmp_path), "--build", other]) == 0
    doc = yaml.safe_load(capsys.readouterr().out)
    assert [r["id"] for r in doc["records"]] == [other]


def test_export_without_database(tmp_path, capsys):
    assert main(["export", "--root", str(tmp_path)]) == 2
    assert "brak bazy stanu GLU" in capsys.readouterr().err


def test_console_script_and_module_entry_point(tmp_path):
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert re.search(r'^glu = "glu\.__main__:main"$', pyproject, re.M)
    seed(tmp_path)
    run = subprocess.run([sys.executable, "-m", "glu", "status", "--root", str(tmp_path)], cwd=ROOT,
                         capture_output=True, text=True, encoding="utf-8")
    assert run.returncode == 0, run.stderr
    assert "stan: waiting_inference" in run.stdout
