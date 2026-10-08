"""Safe file I/O of a game repo: atomic replacement of one file and an exclusive inter-process lock (ADR-0026).

Standard library only, Windows and POSIX:
- `atomic_write(path, data)`: temporary file in the same directory, flush + `fsync`, then `os.replace`. A failure
  before the replacement leaves the previous file byte for byte and removes the temporary file. There is no fallback
  to writing the target in place. One file only: several files as one commit go through `wgc.fsbatch` (ADR-0031).
- `exclusive(path, timeout)`: lock on a lock file (`msvcrt.locking` on Windows, `fcntl.flock` on POSIX), plus a
  thread lock per path, so threads of one process and separate processes exclude each other. The OS releases the
  lock when the process dies; the lock file itself is never removed. Busy for longer than `timeout` → `LockBusy`.
  The lock is advisory: only code that takes it is excluded (not an editor, not git).
"""
from __future__ import annotations

import errno
import os
import stat
import tempfile
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

TMP_SUFFIX = ".wgc-tmp"
# Windows: `os.replace` fails with PermissionError while another process holds the target open (a reader, an
# antivirus scan, the search indexer). Short waits between the attempts, in seconds; then the error is raised.
REPLACE_RETRIES = (0.05, 0.1, 0.2, 0.4, 0.8)
POLL = 0.05  # seconds between attempts to take a busy lock

if os.name == "nt":
    import msvcrt
else:
    import fcntl

    _UMASK = os.umask(0)  # read once at import (os.umask can only be read by setting it)
    os.umask(_UMASK)
    _NEW_FILE_MODE = 0o666 & ~_UMASK  # what open("w") would give a new file


class LockBusy(OSError):
    """The lock is held by another process or thread for longer than the timeout."""


def temp_files(directory: Path) -> list[Path]:
    """Temporary files `atomic_write` leaves behind when a process is killed before the replacement."""
    return sorted(p for p in Path(directory).rglob(f"*{TMP_SUFFIX}") if p.is_file()) if Path(directory).is_dir() else []


def atomic_write(path: Path, data: bytes) -> None:
    """Replace `path` with `data` atomically (see the module docstring)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=TMP_SUFFIX)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if os.name != "nt":  # mkstemp creates 0600: keep the mode of the replaced file, or the usual one for a new file
            os.chmod(tmp, stat.S_IMODE(os.stat(path).st_mode) if path.exists() else _NEW_FILE_MODE)
        _replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    _fsync_dir(path.parent)


def _replace(src: str, dst: Path) -> None:
    waits = list(REPLACE_RETRIES) if os.name == "nt" else []
    while True:
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if not waits:
                raise
            time.sleep(waits.pop(0))


def _fsync_dir(directory: Path) -> None:
    """Make the new directory entry durable (POSIX). Windows cannot open a directory for `fsync`: NTFS journals the
    rename itself, so the step is skipped there."""
    if os.name == "nt":
        return
    try:
        fd = os.open(directory, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


# --- lock -----------------------------------------------------------------------------------------------------------

_THREAD_LOCKS: dict[str, threading.Lock] = {}
_GUARD = threading.Lock()


def _thread_lock(path: Path) -> threading.Lock:
    key = os.path.normcase(os.path.abspath(path))
    with _GUARD:
        return _THREAD_LOCKS.setdefault(key, threading.Lock())


def _try_lock(fd: int) -> bool:
    try:
        if os.name == "nt":
            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError as e:
        if e.errno in (errno.EACCES, errno.EAGAIN, errno.EDEADLK):
            return False
        raise


def _unlock(fd: int) -> None:
    if os.name == "nt":
        os.lseek(fd, 0, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(fd, fcntl.LOCK_UN)


@contextmanager
def exclusive(path: Path, timeout: float) -> Iterator[None]:
    """Hold the exclusive lock on `path` (created if missing) for the body of the `with` block."""
    path = Path(path)
    deadline = time.monotonic() + max(timeout, 0.0)
    tlock = _thread_lock(path)
    if not (tlock.acquire(timeout=timeout) if timeout > 0 else tlock.acquire(blocking=False)):
        raise LockBusy(errno.EACCES, "lock busy", str(path))
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
        try:
            while not _try_lock(fd):
                if time.monotonic() >= deadline:
                    raise LockBusy(errno.EACCES, "lock busy", str(path))
                time.sleep(POLL)
            try:
                yield
            finally:
                _unlock(fd)
        finally:
            os.close(fd)
    finally:
        tlock.release()
