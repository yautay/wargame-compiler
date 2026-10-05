"""Job store: execution state of GLU in SQLite, `.glu/state.db` of a game repo (ADR-0004, ADR-0023).

Tables `build`, `job`, `attempt` and `routing_decision` keep each record of `glu/exec@0` as JSON in `body`, plus
the columns needed for lookups; `transition` is the log of state changes. Every record is validated against the
contract before it is written, so the store never holds a record that `export()` could not emit. States change only
through the tables in `glu.states`. The schema of the database is versioned with `PRAGMA user_version`; migrations
are ordered lists of SQL statements in `MIGRATIONS`.

The clock and the ID generator are injected (deterministic tests). Connections are closed explicitly: on Windows an
open SQLite file cannot be removed (ADR-0022).
"""
from __future__ import annotations

import json
import secrets
import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterator

from glu import states
from wgc import contracts

CONTRACT = "glu/exec@0"
DB_DIR = ".glu"
DB_NAME = "state.db"

# Migration N (index N-1) moves the database from user_version N-1 to N. Append only; never edit an applied step.
MIGRATIONS: tuple[tuple[str, ...], ...] = (
    (
        """CREATE TABLE build (
            id TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            body TEXT NOT NULL)""",
        """CREATE TABLE job (
            id TEXT PRIMARY KEY,
            build TEXT NOT NULL REFERENCES build(id),
            state TEXT NOT NULL,
            tier TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            body TEXT NOT NULL)""",
        "CREATE INDEX job_build_state ON job(build, state)",
        """CREATE TABLE attempt (
            id TEXT PRIMARY KEY,
            job TEXT NOT NULL REFERENCES job(id),
            tier TEXT NOT NULL,
            outcome TEXT NOT NULL,
            created_at TEXT NOT NULL,
            body TEXT NOT NULL)""",
        "CREATE INDEX attempt_job ON attempt(job)",
        """CREATE TABLE routing_decision (
            id TEXT PRIMARY KEY,
            job TEXT NOT NULL REFERENCES job(id),
            chosen TEXT NOT NULL,
            created_at TEXT NOT NULL,
            body TEXT NOT NULL)""",
        "CREATE INDEX routing_decision_job ON routing_decision(job)",
        """CREATE TABLE transition (
            seq INTEGER PRIMARY KEY AUTOINCREMENT,
            entity TEXT NOT NULL,
            entity_id TEXT NOT NULL,
            src TEXT,
            dst TEXT NOT NULL,
            at TEXT NOT NULL,
            reason TEXT)""",
        "CREATE INDEX transition_entity ON transition(entity_id)",
    ),
)
SCHEMA_VERSION = len(MIGRATIONS)

NOUN = {"build": "buildu", "job": "joba", "attempt": "próby", "routing_decision": "decyzji routingu"}


class StoreError(Exception):
    """Operational error of the job store (message in Polish)."""


_CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"


def ulid() -> str:
    """26 characters, Crockford base32: 48-bit time in ms + 80 random bits; sorts by creation time."""
    value = (time.time_ns() // 1_000_000) << 80 | secrets.randbits(80)
    return "".join(_CROCKFORD[(value >> (5 * i)) & 31] for i in reversed(range(26)))


def new_id(prefix: str) -> str:
    """Execution-state ID matching glu/exec@0 `xid`: build_, job_, att_, rd_ or pkg_ + ULID."""
    return f"{prefix}_{ulid()}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def timestamp(moment: datetime) -> str:
    if moment.tzinfo is None:
        raise StoreError("zegar GLU musi zwracać czas ze strefą (UTC), a zwrócił czas bez strefy")
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def db_path(root: str | Path) -> Path:
    return Path(root) / DB_DIR / DB_NAME


def record_errors(record: dict) -> list[str]:
    """Schema errors of one execution-state record (empty list = valid)."""
    prefix = "records/0/"
    return [e[len(prefix):] if e.startswith(prefix) else e
            for e in contracts.errors({"schema": CONTRACT, "records": [record]})]


def _field_order(kind: str) -> list[str]:
    return list(contracts.schema_for(CONTRACT)["$defs"][kind]["properties"])


def ordered(record: dict) -> dict:
    """Record with keys in the order of its contract definition (stable, readable export)."""
    order = _field_order(record["kind"])
    return {k: record[k] for k in sorted(record, key=lambda k: order.index(k) if k in order else len(order))}


def migrate(conn: sqlite3.Connection) -> int:
    """Bring the database to SCHEMA_VERSION; returns the number of applied migrations."""
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    if version > SCHEMA_VERSION:
        raise StoreError(f"baza ma wersję schematu {version}, a ta wersja GLU zna najwyżej {SCHEMA_VERSION}; "
                         "zaktualizuj narzędzie")
    applied = 0
    while version < SCHEMA_VERSION:
        conn.execute("BEGIN IMMEDIATE")
        try:
            version = conn.execute("PRAGMA user_version").fetchone()[0]  # another process may have migrated
            if version < SCHEMA_VERSION:
                for statement in MIGRATIONS[version]:
                    conn.execute(statement)
                version += 1
                conn.execute(f"PRAGMA user_version = {version}")
                applied += 1
        except sqlite3.Error as e:
            conn.execute("ROLLBACK")
            raise StoreError(f"migracja bazy stanu GLU do wersji {version + 1} nie powiodła się: {e}") from e
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        conn.execute("COMMIT")
    return applied


class Store:
    """Open job store. Use as a context manager or call `close()`."""

    def __init__(self, path: str | Path, *, create: bool = True,
                 clock: Callable[[], datetime] = utc_now, new_id: Callable[[str], str] = new_id):
        self.path = Path(path)
        if not create and not self.path.is_file():
            raise StoreError(f"brak bazy stanu GLU: {self.path} (nie utworzono jeszcze żadnego buildu)")
        if create:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._clock = clock
        self._new_id = new_id
        try:
            self._conn = sqlite3.connect(self.path, isolation_level=None, timeout=5.0)
        except sqlite3.Error as e:
            raise StoreError(f"nie można otworzyć bazy stanu GLU {self.path}: {e}") from e
        try:
            self._conn.execute("PRAGMA foreign_keys = ON")
            self.applied_migrations = migrate(self._conn)
        except sqlite3.OperationalError as e:  # e.g. locked by another process
            self._conn.close()
            raise StoreError(f"baza stanu GLU {self.path} jest niedostępna: {e}") from e
        except sqlite3.DatabaseError as e:
            self._conn.close()
            raise StoreError(f"{self.path} nie jest poprawną bazą stanu GLU: {e}") from e
        except BaseException:
            self._conn.close()
            raise

    @classmethod
    def at_root(cls, root: str | Path, **kwargs) -> "Store":
        """Store of a game repo: `<root>/.glu/state.db`."""
        return cls(db_path(root), **kwargs)

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    @property
    def schema_version(self) -> int:
        return self._conn.execute("PRAGMA user_version").fetchone()[0]

    # --- internals -------------------------------------------------------------------------------------------

    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            yield self._conn
        except BaseException:
            self._conn.execute("ROLLBACK")
            raise
        self._conn.execute("COMMIT")

    def _now(self) -> str:
        return timestamp(self._clock())

    def _load(self, table: str, record_id: str) -> dict:
        row = self._conn.execute(f"SELECT body FROM {table} WHERE id = ?", (record_id,)).fetchone()
        if row is None:
            raise StoreError(f"nie ma {NOUN[table]} {record_id}")
        return json.loads(row[0])

    def _bodies(self, sql: str, args: tuple = ()) -> list[dict]:
        return [json.loads(r[0]) for r in self._conn.execute(sql, args)]

    @staticmethod
    def _check(record: dict) -> None:
        errors = record_errors(record)
        if errors:
            raise StoreError(f"rekord {record.get('kind')} {record.get('id')} niezgodny z {CONTRACT}: "
                             + "; ".join(errors))

    def _insert(self, conn: sqlite3.Connection, table: str, columns: dict, record: dict) -> None:
        self._check(record)
        names = [*columns, "body"]
        values = [*columns.values(), json.dumps(record, ensure_ascii=False)]
        try:
            conn.execute(f"INSERT INTO {table} ({', '.join(names)}) VALUES ({', '.join('?' * len(names))})", values)
        except sqlite3.IntegrityError as e:
            raise StoreError(f"nie można zapisać {NOUN[table]} {record['id']}: {e}") from e

    @staticmethod
    def _log(conn: sqlite3.Connection, entity: str, entity_id: str, src: str | None, dst: str, at: str,
             reason: str | None) -> None:
        conn.execute("INSERT INTO transition (entity, entity_id, src, dst, at, reason) VALUES (?, ?, ?, ?, ?, ?)",
                     (entity, entity_id, src, dst, at, reason))

    # --- builds ----------------------------------------------------------------------------------------------

    def create_build(self, project: str, stage: str, *, scope: str | None = None, policy: dict | None = None,
                     project_rev: str | None = None, inference_snapshot: dict | None = None,
                     reason: str | None = None) -> str:
        now = self._now()
        target = {"stage": stage, **({"scope": scope} if scope is not None else {})}
        optional = {"project_rev": project_rev, "policy": policy, "inference_snapshot": inference_snapshot}
        record = {"kind": "build", "id": self._new_id("build"), "project": project, "target": target,
                  **{k: v for k, v in optional.items() if v is not None},
                  "state": states.BUILD_INITIAL, "started_at": now}
        with self._tx() as conn:
            self._insert(conn, "build", {"id": record["id"], "state": record["state"], "started_at": now}, record)
            self._log(conn, "build", record["id"], None, record["state"], now, reason)
        return record["id"]

    def build(self, build_id: str) -> dict:
        return ordered(self._load("build", build_id))

    def builds(self) -> list[dict]:
        return [ordered(b) for b in self._bodies("SELECT body FROM build ORDER BY rowid")]

    def transition_build(self, build_id: str, dst: str, *, reason: str | None = None,
                         metrics: dict | None = None) -> dict:
        now = self._now()
        with self._tx() as conn:
            record = self._load("build", build_id)
            new = states.step("build", record, dst, {"metrics": metrics}, now=now)
            self._check(new)
            conn.execute("UPDATE build SET state = ?, finished_at = ?, body = ? WHERE id = ?",
                         (new["state"], new.get("finished_at"), json.dumps(new, ensure_ascii=False), build_id))
            self._log(conn, "build", build_id, record["state"], dst, now, reason)
        return ordered(new)

    # --- jobs ------------------------------------------------------------------------------------------------

    def create_job(self, build_id: str, task: str, inputs: list[str], cache_key: dict, *,
                   depends_on: list[str] = (), tier: str | None = None, risk_class: str | None = None,
                   reason: str | None = None) -> str:
        now = self._now()
        with self._tx() as conn:
            build = self._load("build", build_id)
            if build["state"] in states.BUILD_TERMINAL:
                raise StoreError(f"build {build_id} jest zakończony ({build['state']}); nie można dodać joba")
            for dep in depends_on:
                row = conn.execute("SELECT build FROM job WHERE id = ?", (dep,)).fetchone()
                if row is None or row[0] != build_id:
                    raise StoreError(f"zależność {dep} nie jest jobem buildu {build_id}")
            optional = {"depends_on": list(depends_on) or None, "tier": tier, "risk_class": risk_class}
            record = {"kind": "job", "id": self._new_id("job"), "build": build_id, "task": task,
                      "inputs": list(inputs), **{k: v for k, v in optional.items() if v is not None},
                      "state": states.JOB_INITIAL, "cache_key": cache_key}
            self._insert(conn, "job", {"id": record["id"], "build": build_id, "state": record["state"],
                                       "tier": tier, "created_at": now, "updated_at": now}, record)
            self._log(conn, "job", record["id"], None, record["state"], now, reason)
        return record["id"]

    def _with_attempts(self, job: dict) -> dict:
        ids = [r[0] for r in self._conn.execute("SELECT id FROM attempt WHERE job = ? ORDER BY rowid", (job["id"],))]
        return ordered({**job, "attempts": ids} if ids else job)

    def job(self, job_id: str) -> dict:
        return self._with_attempts(self._load("job", job_id))

    def jobs(self, build_id: str) -> list[dict]:
        self._load("build", build_id)
        return [self._with_attempts(j) for j in self._bodies("SELECT body FROM job WHERE build = ? ORDER BY rowid",
                                                             (build_id,))]

    def job_counts(self, build_id: str) -> dict[str, int]:
        """Number of jobs per state, in the order of the contract enum."""
        counts = dict(self._conn.execute("SELECT state, COUNT(*) FROM job WHERE build = ? GROUP BY state",
                                         (build_id,)).fetchall())
        return {s: counts[s] for s in states.JOB_STATES if s in counts}

    def transition_job(self, job_id: str, dst: str, *, reason: str | None = None, tier: str | None = None,
                       accepted_records: list[str] | None = None) -> dict:
        now = self._now()
        params = {"tier": tier, "accepted_records": list(accepted_records) if accepted_records is not None else None}
        with self._tx() as conn:
            record = self._load("job", job_id)
            build = self._load("build", record["build"])
            new = states.step("job", record, dst, params, build=build, now=now)
            self._check(new)
            conn.execute("UPDATE job SET state = ?, tier = ?, updated_at = ?, body = ? WHERE id = ?",
                         (new["state"], new.get("tier"), now, json.dumps(new, ensure_ascii=False), job_id))
            self._log(conn, "job", job_id, record["state"], dst, now, reason)
        return self.job(job_id)

    # --- attempts and routing decisions (append-only) --------------------------------------------------------

    def add_attempt(self, job_id: str, tier: str, outcome: str, **fields) -> str:
        """Record one executor run. `fields`: optional Attempt fields of glu/exec@0 (profile, error_class, …)."""
        reserved = sorted({"kind", "id", "job", "tier", "outcome"} & set(fields))
        if reserved:
            raise StoreError(f"pól {', '.join(reserved)} nie podaje się w fields próby")
        now = self._now()
        with self._tx() as conn:
            job = self._load("job", job_id)
            if job["state"] in states.JOB_TERMINAL:
                raise StoreError(f"job {job_id} jest zakończony ({job['state']}); nie można dodać próby")
            record = {"kind": "attempt", "id": self._new_id("att"), "job": job_id, "tier": tier, "outcome": outcome,
                      **fields}
            self._insert(conn, "attempt", {"id": record["id"], "job": job_id, "tier": tier, "outcome": outcome,
                                           "created_at": now}, record)
        return record["id"]

    def attempts(self, job_id: str) -> list[dict]:
        return [ordered(a) for a in self._bodies("SELECT body FROM attempt WHERE job = ? ORDER BY rowid", (job_id,))]

    def quality_attempts(self, job_id: str, tier: str | None = None) -> int:
        """Attempts that consume the quality-retry limit: every outcome except `unavailable` (ADR-0017).
        The limit itself is enforced by the structured-output loop (M10)."""
        sql = "SELECT COUNT(*) FROM attempt WHERE job = ? AND outcome != 'unavailable'"
        args: tuple = (job_id,)
        if tier is not None:
            sql += " AND tier = ?"
            args += (tier,)
        return self._conn.execute(sql, args).fetchone()[0]

    def add_routing_decision(self, job_id: str, policy: str, chosen: str, signals: dict, reasons: list[str], *,
                             premium_reason: str | None = None) -> str:
        now = self._now()
        with self._tx() as conn:
            self._load("job", job_id)
            record = {"kind": "routing_decision", "id": self._new_id("rd"), "job": job_id, "policy": policy,
                      "chosen": chosen, **({"premium_reason": premium_reason} if premium_reason else {}),
                      "signals": signals, "reasons": list(reasons)}
            self._insert(conn, "routing_decision", {"id": record["id"], "job": job_id, "chosen": chosen,
                                                    "created_at": now}, record)
        return record["id"]

    def routing_decisions(self, job_id: str) -> list[dict]:
        return [ordered(r) for r in self._bodies("SELECT body FROM routing_decision WHERE job = ? ORDER BY rowid",
                                                 (job_id,))]

    # --- history and export ----------------------------------------------------------------------------------

    def history(self, entity_id: str) -> list[dict]:
        """State changes of a build or job, oldest first (`src` is None at creation)."""
        rows = self._conn.execute("SELECT src, dst, at, reason FROM transition WHERE entity_id = ? ORDER BY seq",
                                  (entity_id,))
        return [{"src": src, "dst": dst, "at": at, "reason": reason} for src, dst, at, reason in rows]

    def export(self, build_id: str | None = None) -> dict:
        """One `glu/exec@0` document: each build, then its jobs, then per job its attempts and routing decisions.
        Review packages are not stored yet (M12/M13)."""
        records: list[dict] = []
        for build in [self.build(build_id)] if build_id else self.builds():
            records.append(build)
            jobs = self.jobs(build["id"])
            records += jobs
            for job in jobs:
                records += self.attempts(job["id"]) + self.routing_decisions(job["id"])
        doc = {"schema": CONTRACT, "records": records}
        errors = contracts.errors(doc)
        if errors:
            raise StoreError(f"eksport niezgodny z {CONTRACT}: " + "; ".join(errors))
        return doc
