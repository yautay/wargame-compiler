"""Independent F1 closure probes for declared types, parents and staging."""
import datetime
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
from types import SimpleNamespace
from unittest.mock import patch

from wgc.inputs import snapshot as s

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("saved_reviewer_fixture", HERE / "review_controls.py")
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
fixtures.BASE = HERE / "x"
assert not fixtures.BASE.exists()
ROWS = []
COUNT = 0


def new_fixture():
    global COUNT
    COUNT += 1
    return fixtures.fixture(str(COUNT))


def rejection(name, operation, root, expected_fragment, extra=None, scans_forbidden=None):
    reads, scans = [], []
    real_open, real_scan = s.open_read, s.os.scandir

    def opened(path):
        reads.append(Path(path))
        return real_open(path)

    def scanned(path):
        scans.append(Path(path))
        return real_scan(path)

    with patch.object(s, "open_read", opened), patch.object(s.os, "scandir", scanned):
        try:
            operation()
        except s.SnapshotError as error:
            reason = str(error)
        else:
            raise AssertionError(name + " did not reject")
    assert expected_fragment in reason, reason
    target_reads = [p for p in reads if p.is_relative_to(root)]
    assert target_reads == [root / "manifest.json"], target_reads
    if extra is not None:
        assert extra not in reads and extra not in scans
        assert extra.lstat()
    if scans_forbidden is not None:
        assert not any(p.is_relative_to(scans_forbidden) for p in scans)
        assert not any(p.is_relative_to(scans_forbidden) for p in reads)
    ROWS.append(dict(name=name, result="pass", rejection=reason,
                     target_content_reads=[str(p) for p in target_reads],
                     no_unexpected_content_read=True, no_link_traversal=True))


def declared_type(kind, action, entry_type):
    f = new_fixture()
    result = s.freeze_inputs(*f)
    root = Path(result[kind])
    target = root / ("files/kb/rule.yaml" if kind == "input_snapshot" else "files/rulebook.pdf")
    before = {root / "manifest.json": (root / "manifest.json").read_bytes()}
    if kind == "source_snapshot":
        before[root / "source-pin.json"] = (root / "source-pin.json").read_bytes()
    target.unlink()
    target.mkdir()
    operation = lambda: s.verify_snapshot(root) if action == "verify" else s.freeze_inputs(*f)
    rejection(kind + ": " + action + " declared blob replaced by directory", operation,
              root, "snapshot tree", target)
    assert target.is_dir()
    assert all(path.read_bytes() == raw for path, raw in before.items())


def missing_blob(kind):
    f = new_fixture()
    result = s.freeze_inputs(*f)
    root = Path(result[kind])
    target = root / ("files/kb/rule.yaml" if kind == "input_snapshot" else "files/rulebook.pdf")
    target.unlink()
    rejection(kind + ": missing available blob", lambda: s.verify_snapshot(root),
              root, "snapshot tree is missing")


def linked_parent(kind):
    f = new_fixture()
    result = s.freeze_inputs(*f)
    root = Path(result[kind])
    outside = root.parent.parent / "moved"
    files = root / "files"
    # Exact resolved paths are checked before moving a synthetic directory.
    assert files.resolve().is_relative_to(HERE.resolve())
    assert outside.absolute().is_relative_to(HERE.resolve()) and not outside.exists()
    files.rename(outside)
    created = subprocess.run(["cmd", "/c", "mklink", "/J", str(files), str(outside)], capture_output=True)
    assert created.returncode == 0, created.stderr
    rejection(kind + ": declared files parent is a real junction",
              lambda: s.verify_snapshot(root), root, "linked path", files, outside)


def symbolic_link(kind, directory):
    f = new_fixture()
    result = s.freeze_inputs(*f)
    root = Path(result[kind])
    outside = root.parent.parent / "symtarget"
    if directory:
        outside.mkdir()
        (outside / "secret").write_bytes(b"do not consume this")
    else:
        outside.write_bytes(b"do not consume this")
    link = root / "files/sym"
    os.symlink(outside, link, target_is_directory=directory)
    rejection(kind + ": real " + ("directory" if directory else "file") + " symlink",
              lambda: s.verify_snapshot(root), root, "linked path", link, outside)


def nonregular(kind):
    f = new_fixture()
    result = s.freeze_inputs(*f)
    root = Path(result[kind])
    target = root / ("files/kb/rule.yaml" if kind == "input_snapshot" else "files/rulebook.pdf")
    reads = []
    real_scan, real_open = s.os.scandir, s.open_read

    class Entry:
        def __init__(self, original):
            self.original = original
            self.path = original.path

        def stat(self, follow_symlinks=True):
            assert follow_symlinks is False
            if Path(self.path) == target:
                return SimpleNamespace(st_mode=stat.S_IFIFO | 0o600, st_file_attributes=0)
            return self.original.stat(follow_symlinks=False)

    class Scan:
        def __init__(self, path):
            self.scan = real_scan(path)

        def __enter__(self):
            return (Entry(e) for e in self.scan)

        def __exit__(self, *args):
            self.scan.close()

    def opened(path):
        reads.append(Path(path))
        return real_open(path)

    with patch.object(s.os, "scandir", Scan), patch.object(s, "open_read", opened):
        try:
            s.verify_snapshot(root)
        except s.SnapshotError as error:
            assert "non-regular entry" in str(error)
            reason = str(error)
        else:
            raise AssertionError("Nonregular declared entries must reject before content read")
    assert reads == [root / "manifest.json"]
    ROWS.append(dict(name=kind + ": simulated nonregular declared blob", result="pass",
                     rejection=reason, simulation="S_IFIFO metadata; Windows is not claimed to have a real FIFO",
                     no_unexpected_content_read=True))


def staging(kind):
    f = new_fixture()
    real_publish, real_open = s.publish, s.open_read
    injected = None
    reads = []

    def opened(path):
        if injected is not None:
            reads.append(Path(path))
        return real_open(path)

    def publish(stage, parent, manifest, source_pin=False):
        nonlocal injected
        if manifest["kind"] == kind:
            injected = stage
            (stage / "unknown.json").write_bytes(b'{"unexpected":"metadata"}\n')
        return real_publish(stage, parent, manifest, source_pin=source_pin)

    with patch.object(s, "publish", publish), patch.object(s, "open_read", opened):
        try:
            s.freeze_inputs(*f)
        except s.SnapshotError as error:
            assert "unexpected file in snapshot tree" in str(error)
            reason = str(error)
        else:
            raise AssertionError("Unlisted staging metadata must never publish")
    assert injected is not None
    assert reads == [injected / "manifest.json"]
    assert (injected / "unknown.json").read_bytes() == b'{"unexpected":"metadata"}\n'
    assert not list(f[1].glob("sha256-*"))
    assert len(list(f[2].glob("sha256-*"))) == (1 if kind == "input_snapshot" else 0)
    ROWS.append(dict(name=kind + ": unknown metadata injected before staging verification",
                     result="pass", rejection=reason, no_invalid_input_published=True,
                     source_publication_can_remain_if_valid=kind == "input_snapshot",
                     rejected_staging_retained=True, no_unexpected_content_read=True))


def main():
    for kind in ["input_snapshot", "source_snapshot"]:
        for action in ["verify", "reuse"]:
            declared_type(kind, action, "directory")
        missing_blob(kind)
        linked_parent(kind)
        symbolic_link(kind, False)
        symbolic_link(kind, True)
        nonregular(kind)
        staging(kind)
    result = dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  cases=ROWS, count=len(ROWS), all_pass=all(x["result"] == "pass" for x in ROWS))
    (HERE / "closure-probes.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
