"""Commit of several files as one batch, with an undo journal and recovery (ADR-0031).

Generic over a journal directory and a base directory; `wgc.kb` uses `kb/.wgc-batch/` under the KB writer lock.
Standard library only. Steps of `commit`:
1. prepare: `<n>.new` (new content) and `<n>.old` (copy of the current file, if any), each flushed and fsynced;
2. manifest `manifest.json` with `state: prepared` (atomic write);
3. `os.replace(<n>.new → target)` for each file, in order;
4. commit marker: the manifest replaced with `state: committed`;
5. the journal directory removed.

A failure in steps 3–4 inside the writer first records the intent to roll back (`state: rolling_back`, atomic), then
restores the old content. Outcomes of `commit`: it returns (committed), `BatchError(outcome="rolled_back")` (the
old content is back and the journal is gone), or `BatchError(outcome="unresolved")` (the journal stays; `recover`
decides, and with `rolling_back` it always rolls back).

`recover` decides from the manifest state and the hashes of the targets (table in ADR-0031): `committed`, or
`prepared` with every target already new → finish forward; `rolling_back`, or `prepared` otherwise → restore every
target from its copy. A target with neither the old nor the new hash stops recovery with `BatchConflict` before
anything is changed. The caller holds the lock.

Journal formats: `wgc-kb-batch@1` (written; hashes `sha256:<hex>`; states `prepared`, `rolling_back`, `committed`)
and `wgc-kb-batch@0` (read only; states `prepared`, `committed`; hashes written with a doubled `sha256:sha256:`
prefix, normalized on load).
"""
from __future__ import annotations

import json
import os
import secrets
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from wgc import fsio
from wgc.canonical import sha256_hex

FORMAT = "wgc-kb-batch@1"
LEGACY_FORMAT = "wgc-kb-batch@0"
STATES = {FORMAT: ("prepared", "rolling_back", "committed"), LEGACY_FORMAT: ("prepared", "committed")}
MANIFEST = "manifest.json"


class BatchError(OSError):
    """A batch could not be written. `outcome`: `rolled_back` (old content confirmed, journal removed) or
    `unresolved` (journal kept; `rollback_decided` says whether `rolling_back` was recorded)."""

    def __init__(self, message: str, outcome: str, rollback_decided: bool = False):
        super().__init__(message)
        self.outcome = outcome
        self.rollback_decided = rollback_decided

    @property
    def rolled_back(self) -> bool:
        return self.outcome == "rolled_back"


class BatchConflict(Exception):
    """Recovery cannot decide: a target changed outside the batch, or a needed copy is missing or damaged."""


def _step(name: str) -> None:
    """Protocol checkpoint (`prepared`, `replaced:<n>`, `committed`, `rolling_back`, `recovered:<n>`); tests replace
    it to simulate a crash."""


def file_hash(path: Path) -> str | None:
    """`sha256:<hex>` of the bytes of a file, `None` when it does not exist."""
    try:
        return sha256_hex(path.read_bytes())
    except FileNotFoundError:
        return None


def _norm(value: str | None) -> str | None:
    """A hash of a `wgc-kb-batch@0` journal (`sha256:sha256:<hex>`) as `sha256:<hex>`."""
    if isinstance(value, str) and value.startswith("sha256:sha256:"):
        return value[len("sha256:"):]
    return value


def _write_new(path: Path, data: bytes) -> None:
    with open(path, "xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def _manifest(journal: Path, state: str, batch_id: str, job: str | None, files: list[dict]) -> None:
    doc = {"format": FORMAT, "id": batch_id, "state": state, "job": job, "files": files}
    fsio.atomic_write(journal / MANIFEST, (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))


def _remove(journal: Path) -> None:
    shutil.rmtree(journal, ignore_errors=True)


def commit(base: Path, journal: Path, changes: list[tuple[Path, bytes]], job: str | None = None) -> None:
    """Replace every target in `changes` with its bytes, all or nothing (see the module docstring for outcomes)."""
    base, journal = Path(base), Path(journal)
    if journal.exists():
        raise BatchError(f"{_rel(journal, base)} już istnieje: najpierw recovery przerwanej partii.",
                         outcome="rolled_back")  # nothing of this batch was written
    batch_id = secrets.token_hex(8)
    files = []
    try:
        journal.mkdir(parents=True)
        for n, (target, data) in enumerate(changes):
            entry = {"path": Path(target).relative_to(base).as_posix(), "old": file_hash(target),
                     "new": sha256_hex(data), "staged": f"{n}.new", "backup": None}
            _write_new(journal / entry["staged"], data)
            if entry["old"] is not None:
                entry["backup"] = f"{n}.old"
                _write_new(journal / entry["backup"], Path(target).read_bytes())
            files.append(entry)
        fsio._fsync_dir(journal)
        _manifest(journal, "prepared", batch_id, job, files)
    except BaseException:
        _remove(journal)  # no target touched yet
        raise
    try:
        _step("prepared")
        for n, entry in enumerate(files):
            target = base / entry["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            fsio._replace(str(journal / entry["staged"]), target)
            fsio._fsync_dir(target.parent)
            _step(f"replaced:{n}")
        _manifest(journal, "committed", batch_id, job, files)
    except Exception as e:
        # the writer gives up: record the intent first, so recovery can never go forward from here
        try:
            _manifest(journal, "rolling_back", batch_id, job, files)
            decided = True
        except OSError:
            decided = False
        _step("rolling_back")
        try:
            recover(base, journal, rollback=True)
        except (OSError, BatchConflict) as e2:
            raise BatchError(f"{e}; wycofanie partii też się nie udało: {e2}", outcome="unresolved",
                             rollback_decided=decided) from e
        raise BatchError(str(e), outcome="rolled_back") from e
    _step("committed")
    _remove(journal)


def _rel(path: Path, base: Path) -> str:
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.as_posix()


@dataclass
class Plan:
    """What `recover` does or would do."""
    state: str                      # clean | orphan | rollback | forward
    actions: list[str] = field(default_factory=list)
    job: str | None = None
    files: list[dict] = field(default_factory=list, repr=False)  # manifest entries, hashes normalized


def _load(base: Path, journal: Path) -> dict:
    manifest = journal / MANIFEST
    try:
        doc = json.loads(manifest.read_text(encoding="utf-8"))
        files = [{**f, "old": _norm(f["old"]), "new": _norm(f["new"])} for f in doc["files"]]
        state = doc["state"]
        [f["path"] for f in files]
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise BatchConflict(f"nieczytelny manifest {_rel(manifest, base)}: {e}") from None
    if state not in STATES.get(doc.get("format"), ()):
        raise BatchConflict(f"nieznany format albo stan manifestu {_rel(manifest, base)}: "
                            f"{doc.get('format')!r}, {state!r}")
    return {**doc, "files": files}


def plan(base: Path, journal: Path, rollback: bool = False) -> Plan:
    """Decide recovery without changing anything (`BatchConflict` when it cannot be decided). `rollback`: the
    writer itself gave up, so the batch is undone whatever the manifest says."""
    base, journal = Path(base), Path(journal)
    if not journal.exists():
        return Plan("clean")
    name = _rel(journal, base)
    if not (journal / MANIFEST).is_file():
        return Plan("orphan", [f"usunięcie {name} (przerwane przygotowanie partii, kb/ bez zmian)"])
    doc = _load(base, journal)
    files, state = doc["files"], doc["state"]
    current = {f["path"]: file_hash(base / f["path"]) for f in files}
    for f in files:
        if current[f["path"]] not in (f["old"], f["new"]):
            raise BatchConflict(f"{f['path']} zmienił się poza partią (hash różny od starej i nowej treści); "
                                f"recovery niczego nie zmienia: sprawdź plik i przywróć go z git albo z {name}")
    # `prepared` with every target new: the marker was lost (never after `rolling_back`, which is written first)
    forward = not rollback and (state == "committed"
                                or (state == "prepared" and all(current[f["path"]] == f["new"] for f in files)))
    actions = []
    for f in files:
        cur = current[f["path"]]
        if forward and cur != f["new"]:
            if file_hash(journal / f["staged"]) != f["new"]:
                raise BatchConflict(f"brak albo uszkodzona nowa treść {f['staged']} dla {f['path']}")
            actions.append(f"dokończenie: {f['path']}")
        elif not forward and cur != f["old"]:
            if f["old"] is None:
                actions.append(f"wycofanie: usunięcie nowego pliku {f['path']}")
            elif file_hash(journal / f["backup"]) != f["old"]:
                raise BatchConflict(f"brak albo uszkodzona kopia {f['backup']} dla {f['path']}")
            else:
                actions.append(f"wycofanie: {f['path']}")
    actions.append(f"usunięcie {name}")
    return Plan("forward" if forward else "rollback", actions, doc.get("job"), files)


def recover(base: Path, journal: Path, dry_run: bool = False, rollback: bool = False) -> Plan:
    """Finish or roll back an interrupted batch; idempotent (an interrupted recovery is simply run again).
    `dry_run`: only the plan."""
    base, journal = Path(base), Path(journal)
    p = plan(base, journal, rollback)
    if dry_run or p.state == "clean":
        return p
    for n, f in enumerate(p.files):
        target = base / f["path"]
        cur = file_hash(target)
        if p.state == "forward" and cur != f["new"]:
            fsio._replace(str(journal / f["staged"]), target)
        elif p.state == "rollback" and cur != f["old"]:
            if f["old"] is None:
                target.unlink()
            else:
                fsio._replace(str(journal / f["backup"]), target)
        else:
            continue
        fsio._fsync_dir(target.parent)
        _step(f"recovered:{n}")
    _remove(journal)
    if journal.exists():
        raise OSError(f"nie można usunąć {_rel(journal, base)}; ponów recovery")
    return p
