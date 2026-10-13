"""Independent synthetic contract probes; writes only this review directory."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
from unittest.mock import patch

from wgc.inputs import snapshot as s

HERE = Path(__file__).resolve().parent
BASE = HERE / "synthetic-controls-01"
RESULTS = []


def fixture(name):
    root = BASE / name
    root.mkdir(parents=True, exist_ok=False)
    game, registry = root / "game", root / "registry"
    (game / "kb").mkdir(parents=True)
    registry.mkdir()
    (game / "wgu.yaml").write_bytes(b"game: synthetic\r\n")
    (game / "kb/rule.yaml").write_bytes(b"rule: synthetic\n")
    (registry / "rulebook.pdf").write_bytes(b"%PDF-synthetic\x00\xff")
    (registry / "provenance.json").write_bytes(b'{"basis":"synthetic"}\n')

    def entry(root, name, role):
        raw = (root / name).read_bytes()
        return dict(relative_path=name, role=role, bytes=len(raw),
                    sha256=hashlib.sha256(raw).hexdigest())

    req = dict(game_root=str(game), registry_root=str(registry),
               game_files=[entry(game, "wgu.yaml", "game_config"),
                           entry(game, "kb/rule.yaml", "kb")],
               registry_files=[entry(registry, "provenance.json", "provenance"),
                               entry(registry, "rulebook.pdf", "selected_rulebook")],
               historical_configured_sources=[dict(relative_path="docs/original.pdf",
                                                     role="configured_source", availability="missing")],
               selection=dict(source_id="synthetic", role="rulebook", edition_label="synthetic-1",
                              edition_basis="Synthetic independent reviewer fixture",
                              selected_path="rulebook.pdf",
                              sha256=hashlib.sha256((registry / "rulebook.pdf").read_bytes()).hexdigest(),
                              identity_to_wgu_original="unknown", semantic_acceptance="not_granted"))
    return req, root / "inputs", root / "sources"


def probe(name, expected, operation):
    try:
        value = operation()
        actual = "accepted"
        detail = str(value)
    except (s.SnapshotError, OSError, ValueError, KeyError, TypeError) as error:
        actual = "rejected"
        detail = str(error)
    RESULTS.append(dict(name=name, expected=expected, actual=actual,
                        conforms=actual == expected, detail=detail))


def fail_copy(name, transform):
    f = fixture(name)
    real = s.digest_stream
    done = False

    def wrapped(stream, destination=None):
        nonlocal done
        result = real(stream, destination)
        if destination is not None and not done:
            done = True
            transform(stream, destination)
        return result

    with patch.object(s, "digest_stream", wrapped):
        try:
            return s.freeze_inputs(*f)
        finally:
            assert not list(f[1].glob("sha256-*"))
            assert not list(f[2].glob("sha256-*"))


def corrupt_copy(stream, destination):
    destination.seek(0)
    destination.write(b"corrupt copied bytes")


def change_during_read(stream, destination):
    # Windows sharing denies normal writes. fstat must also independently catch
    # a changed same-handle signature, including ctime with stable size/mtime.
    pass


def same_handle_ctime():
    f = fixture("same-handle-ctime")
    real = s.os.fstat
    calls = 0

    def changed(fd):
        nonlocal calls
        info = real(fd)
        calls += 1
        if calls == 3:
            values = {name: getattr(info, name) for name in
                      ["st_mode", "st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns"]}
            values["st_ctime_ns"] += 1
            return type("SyntheticChangedStat", (), values)()
        return info

    with patch.object(s.os, "fstat", changed):
        try:
            return s.freeze_inputs(*f)
        finally:
            assert not list(f[1].glob("sha256-*")) and not list(f[2].glob("sha256-*"))


def disappear():
    f = fixture("available-disappears")
    origin = Path(f[0]["game_root"]) / "docs/original.pdf"
    origin.parent.mkdir()
    origin.write_bytes(b"available original")
    f[0]["historical_configured_sources"][0]["availability"] = "available"
    real = s.measure

    def measure(path, destination=None):
        result = real(path, destination)
        if path == origin and destination is not None:
            origin.unlink()
        return result

    with patch.object(s, "measure", measure):
        try:
            return s.freeze_inputs(*f)
        finally:
            assert not list(f[1].glob("sha256-*")) and not list(f[2].glob("sha256-*"))


def disappear_kb():
    f = fixture("kb-disappears")
    origin = Path(f[0]["game_root"]) / "kb/rule.yaml"
    real = s.measure

    def measure(path, destination=None):
        result = real(path, destination)
        if path == origin and destination is not None:
            origin.unlink()
        return result

    with patch.object(s, "measure", measure):
        try:
            return s.freeze_inputs(*f)
        finally:
            assert not list(f[1].glob("sha256-*")) and not list(f[2].glob("sha256-*"))


def disjoint(name, kind):
    req, inputs, sources = fixture(name)
    if kind == "same":
        sources = inputs
    elif kind == "nested":
        sources = inputs / "nested"
    elif kind == "source-under-registry":
        sources = Path(req["registry_root"]) / "output"
    elif kind == "parent-of-game":
        inputs = Path(req["game_root"]).parent
    return s.freeze_inputs(req, inputs, sources)


def tamper(name, kind):
    f = fixture(name)
    result = s.freeze_inputs(*f)
    root = Path(result["source_snapshot"])
    if kind == "pin":
        pin = json.loads((root / "source-pin.json").read_bytes())
        pin["selection_purpose"] = "recovered_original"
        (root / "source-pin.json").write_bytes(s.canonical(pin) + b"\n")
    elif kind == "extra-kb":
        root = Path(result["input_snapshot"])
        (root / "files/kb/unlisted.yaml").write_bytes(b"unlisted input")
    elif kind == "missing-blob":
        root = Path(result["input_snapshot"])
        (root / "files/docs").mkdir()
        (root / "files/docs/original.pdf").write_bytes(b"missing source now present in sealed tree")
    elif kind == "extra-link":
        root = Path(result["input_snapshot"])
        outside = root.parent.parent / "outside"
        outside.mkdir()
        (outside / "secret").write_bytes(b"do not consume")
        code = subprocess.run(["cmd", "/c", "mklink", "/J", str(root / "files/kb/unlisted"), str(outside)],
                              capture_output=True)
        assert code.returncode == 0, code.stderr
    verified = s.verify_snapshot(root)
    reused = s.freeze_inputs(*f)
    return dict(same_result=result == reused, same_id=verified["snapshot_id"],
                unexpected_paths_retained=kind != "pin")


def unlisted_registry():
    f = fixture("registry-not-enumerated")
    secret = Path(f[0]["registry_root"]) / "secret.pdf"
    secret.write_bytes(b"not authorized")
    reads = []
    real = s.open_read

    def tracked(path):
        reads.append(Path(path))
        return real(path)

    with patch.object(s, "open_read", tracked):
        result = s.freeze_inputs(*f)
    assert secret not in reads
    assert not (Path(result["source_snapshot"]) / "files/secret.pdf").exists()
    return dict(secret_never_opened=True)


def cross_root_alias():
    f = fixture("cross-root-physical-alias")
    target = Path(f[0]["registry_root"]) / "rulebook.pdf"
    target.unlink()
    source = Path(f[0]["game_root"]) / "kb/rule.yaml"
    os.link(source, target)
    raw = source.read_bytes()
    entry = next(x for x in f[0]["registry_files"] if x["role"] == "selected_rulebook")
    entry.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    f[0]["selection"]["sha256"] = entry["sha256"]
    return s.freeze_inputs(*f)


def main():
    assert not BASE.exists()
    probe("same-handle ctime changes with stable identity/size/mtime", "rejected", same_handle_ctime)
    probe("independent copy corruption", "rejected", lambda: fail_copy("copy-corruption", corrupt_copy))
    probe("available configured source disappears between files", "rejected", disappear)
    probe("KB file disappears after copying", "rejected", disappear_kb)
    for kind in ["same", "nested", "source-under-registry", "parent-of-game"]:
        probe("destination overlap: " + kind, "rejected", lambda kind=kind: disjoint("overlap-" + kind, kind))
    probe("canonical but altered source pin", "rejected", lambda: tamper("altered-pin", "pin"))
    probe("cross-root physical hardlink alias", "rejected", cross_root_alias)
    probe("unlisted source registry bytes are never opened", "accepted", unlisted_registry)
    for kind in ["extra-kb", "missing-blob", "extra-link"]:
        probe("sealed tree tampering: " + kind, "rejected", lambda kind=kind: tamper("tamper-" + kind, kind))
    (HERE / "review-controls.json").write_text(json.dumps(RESULTS, indent=2) + "\n", encoding="utf-8")
    for row in RESULTS:
        print(row["name"], "expected=" + row["expected"], "actual=" + row["actual"],
              "conforms=" + str(row["conforms"]))
    return 0 if all(row["conforms"] for row in RESULTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
